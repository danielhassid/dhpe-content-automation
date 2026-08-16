#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
market_watcher.py — "השריר": לולאת ניטור בלי LLM.

קורא את trading-desk/state/active-triggers.json, מנטר מחירים דרך endpoint ציבורי,
וכשתנאי טריגר מתקיים — מבצע דרך אותם שערים בדיוק של place_order.execute_order.

חייב לרוץ על מארח קבוע (VPS / Raspberry Pi / מחשב דולק) — ה-sandbox של claude.ai
הוא ephemeral. לפני כל מחזור מומלץ `git pull` כדי לקבל טריגרים עדכניים.

טריגר (נכתב ע"י מרים בלבד, אחרי אישור):
{
  "trigger_id": "T-2026-08-16-01",
  "symbol": "BTCUSDT",
  "condition": {"op": "<=", "price": 58000},
  "order": {"type": "LIMIT", "side": "BUY", "notional_usdt": 50,
            "price": 58000, "stop": 56500, "take_profit": 62000},
  "created_at": "2026-08-16T05:00:00Z",
  "expires_at": "2026-08-17T05:00:00Z",
  "approved_by": "miriam",
  "sig": "<sha256>",
  "status": "active"
}
sig = sha256(תוכן הטריגר ללא sig/status + הבייטים של limits.json). זהו hash תקינות:
טריגר שנערך אחרי האישור, או ש-limits.json השתנה מאז — נפסל אוטומטית.

שימוש:
  python3 market_watcher.py --once          # מעבר יחיד (בדיקות / cron)
  python3 market_watcher.py --interval 60   # לולאה, ברירת מחדל 60 שניות
"""

import argparse
import json
import os
import time

from binance_client import (
    DESK, current_env, get_price, kill_switch_active, limits_raw_bytes,
    trigger_signature,
)
from place_order import execute_order

TRIGGERS_FILE = os.path.join(DESK, "state", "active-triggers.json")

OPS = {
    "<=": lambda a, b: a <= b,
    ">=": lambda a, b: a >= b,
    "<": lambda a, b: a < b,
    ">": lambda a, b: a > b,
}


def _now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _load():
    with open(TRIGGERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_atomic(data):
    tmp = TRIGGERS_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, TRIGGERS_FILE)


def pass_once():
    if kill_switch_active():
        print(f"{_now()} KILL-SWITCH פעיל — מדלג על הכול.")
        return
    current_env()  # מוודא ש-phase/env חוקיים לפני כל דבר

    data = _load()
    limits_raw = limits_raw_bytes()
    changed = False

    for t in data.get("triggers", []):
        if t.get("status") != "active":
            continue

        if t.get("expires_at", "") <= _now():
            t["status"] = "expired"
            changed = True
            print(f"{_now()} {t['trigger_id']}: פג תוקף (TTL).")
            continue

        if t.get("approved_by") != "miriam" or t.get("sig") != trigger_signature(t, limits_raw):
            t["status"] = "invalidated"
            changed = True
            print(f"{_now()} {t['trigger_id']}: חתימה לא תקפה (נערך אחרי אישור, או ש-limits.json השתנה) — נפסל.")
            continue

        try:
            # במצב paper בלבד: PAPER_PRICE_<SYMBOL> מאפשר בדיקת הלולאה בלי רשת
            override = os.environ.get(f"PAPER_PRICE_{t['symbol']}")
            if override and current_env() == "paper":
                price = float(override)
            else:
                price = get_price(t["symbol"])
        except SystemExit as e:
            print(f"{_now()} {t['trigger_id']}: אין מחיר ({e}) — מנסים במחזור הבא.")
            continue

        cond = t["condition"]
        if not OPS[cond["op"]](price, float(cond["price"])):
            continue

        print(f"{_now()} {t['trigger_id']}: תנאי התקיים ({t['symbol']} {price} {cond['op']} {cond['price']}) — מבצע.")
        # מסמנים consumed לפני השליחה — עדיף טריגר אבוד מביצוע כפול
        t["status"] = "consumed"
        t["consumed_at"] = _now()
        t["fired_price"] = price
        _save_atomic(data)
        changed = False
        rc = execute_order(dict(t["order"], symbol=t["symbol"]), source="watcher", ref_id=t["trigger_id"])
        t["execution_rc"] = rc
        _save_atomic(data)

    if changed:
        _save_atomic(data)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--once", action="store_true")
    p.add_argument("--interval", type=int, default=60)
    a = p.parse_args()

    if a.once:
        pass_once()
        return
    print(f"market_watcher פעיל, מחזור כל {a.interval} שניות. עצירה: Ctrl+C או יצירת KILL-SWITCH.")
    while True:
        try:
            pass_once()
        except Exception as e:  # noqa: BLE001 — הלולאה לא מתה על שגיאה בודדת
            print(f"{_now()} שגיאה במחזור: {type(e).__name__}: {e}")
        time.sleep(a.interval)


if __name__ == "__main__":
    main()
