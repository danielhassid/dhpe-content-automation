#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
binance_client.py — לקוח Binance REST מינימלי, stdlib בלבד.

עקרונות:
- מפתחות רק ממשתני סביבה. לעולם לא מודפסים, לא נכתבים לקובץ.
- env נקבע מ-trading-desk/config/phase.json, עם אפשרות override דרך BINANCE_ENV
  (paper / testnet / live). ב-paper אין קריאות חתומות בכלל.
- קריאות ציבוריות (מחירים) מותרות בכל env, כולל paper.
- מכבד HTTPS_PROXY אוטומטית (urllib) ואת ה-CA bundle של הסביבה אם קיים.
"""

import hashlib
import hmac
import json
import os
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DESK = os.path.join(REPO_ROOT, "trading-desk")
PHASE_FILE = os.path.join(DESK, "config", "phase.json")
LIMITS_FILE = os.path.join(DESK, "config", "limits.json")
KILL_SWITCH = os.path.join(DESK, "KILL-SWITCH")
ORDERS_LOG = os.path.join(DESK, "state", "orders-log.jsonl")

BASE_URLS = {
    "testnet": "https://testnet.binance.vision",
    "live": "https://api.binance.com",
}
# hosts ציבוריים לנתוני שוק (בלי מפתחות); מנסים לפי הסדר
PUBLIC_DATA_HOSTS = [
    "https://api.binance.com",
    "https://data-api.binance.vision",
    "https://testnet.binance.vision",
]

CA_BUNDLE = "/root/.ccr/ca-bundle.crt"


def _ssl_context():
    if os.path.exists(CA_BUNDLE):
        return ssl.create_default_context(cafile=CA_BUNDLE)
    return ssl.create_default_context()


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_phase():
    return load_json(PHASE_FILE)


def load_limits():
    return load_json(LIMITS_FILE)


def current_env():
    """paper / testnet / live. BINANCE_ENV גובר, אבל live דורש phase=2 בקובץ."""
    phase = load_phase()
    env = os.environ.get("BINANCE_ENV") or phase.get("env", "paper")
    if env not in ("paper", "testnet", "live"):
        raise SystemExit(f"BINANCE_ENV לא חוקי: {env}")
    if env == "live" and int(phase.get("phase", 0)) != 2:
        raise SystemExit("סירוב: env=live אבל phase.json אינו ב-phase 2. דניאל מקדם שלב ידנית בלבד.")
    if env == "testnet" and int(phase.get("phase", 0)) < 1:
        raise SystemExit("סירוב: env=testnet אבל phase.json עדיין ב-phase 0 (נייר).")
    return env


def kill_switch_active():
    return os.path.exists(KILL_SWITCH)


def _keys_for(env):
    if env == "testnet":
        k = os.environ.get("BINANCE_TESTNET_API_KEY")
        s = os.environ.get("BINANCE_TESTNET_API_SECRET")
    elif env == "live":
        k = os.environ.get("BINANCE_API_KEY")
        s = os.environ.get("BINANCE_API_SECRET")
    else:
        return None, None
    if not k or not s:
        raise SystemExit(f"חסרים מפתחות בסביבה עבור env={env} (env vars בלבד — לעולם לא בקבצים).")
    return k, s


def _http(url, method="GET", headers=None, timeout=15):
    req = urllib.request.Request(url, method=method, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout, context=_ssl_context()) as resp:
        return json.loads(resp.read().decode("utf-8"))


def public_get(path, params=None):
    """GET ציבורי (בלי מפתחות) עם fallback בין hosts. path כמו '/api/v3/ticker/price'."""
    qs = ("?" + urllib.parse.urlencode(params)) if params else ""
    last_err = None
    for host in PUBLIC_DATA_HOSTS:
        try:
            return _http(host + path + qs)
        except Exception as e:  # noqa: BLE001 — מנסים host הבא
            last_err = e
    raise SystemExit(f"כל ה-hosts הציבוריים נכשלו ({type(last_err).__name__}: {last_err}). "
                     "ככל הנראה egress חסום — עובדים במצב המלצות בלבד.")


def signed_request(path, params=None, method="GET"):
    """קריאה חתומה (HMAC-SHA256). אסורה ב-paper."""
    env = current_env()
    if env == "paper":
        raise SystemExit("סירוב: קריאה חתומה במצב paper. אין מפתחות ואין רשת במצב נייר.")
    key, secret = _keys_for(env)
    base = BASE_URLS[env]
    params = dict(params or {})
    params["timestamp"] = int(time.time() * 1000)
    params.setdefault("recvWindow", 5000)
    qs = urllib.parse.urlencode(params)
    sig = hmac.new(secret.encode(), qs.encode(), hashlib.sha256).hexdigest()
    url = f"{base}{path}?{qs}&signature={sig}"
    try:
        return _http(url, method=method, headers={"X-MBX-APIKEY": key})
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        # body של ביננס לא מכיל סודות; ה-URL כן (signature) — לא מדפיסים אותו
        raise SystemExit(f"Binance HTTP {e.code}: {body}")


def get_price(symbol):
    return float(public_get("/api/v3/ticker/price", {"symbol": symbol})["price"])


def append_order_log(record):
    """רישום append-only. אסור שיכיל סודות — הסכימה לא כוללת שדה כזה."""
    record.setdefault("ts", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    with open(ORDERS_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def trigger_signature(trigger, limits_raw):
    """hash תקינות: תוכן הטריגר (בלי sig/status) + בייטים של limits.json.
    שינוי בטריגר אחרי אישור, או שינוי מגבלות — מפסלים את החתימה."""
    core = {k: v for k, v in trigger.items() if k not in ("sig", "status")}
    payload = json.dumps(core, sort_keys=True, ensure_ascii=False) + limits_raw
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def limits_raw_bytes():
    with open(LIMITS_FILE, "r", encoding="utf-8") as f:
        return f.read()
