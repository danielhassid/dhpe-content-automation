#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""כלי עזר למרים: חתימת טריגר. קורא active-triggers.json, מחשב sig לכל טריגר
עם "sig": "PENDING" והופך אותו ל-active. מריצים אחרי שמרים אישרה וכתבה את הטריגר.

שימוש: python3 sign_trigger.py T-2026-08-16-01
"""

import json
import os
import sys

from binance_client import DESK, limits_raw_bytes, trigger_signature, load_limits

TRIGGERS_FILE = os.path.join(DESK, "state", "active-triggers.json")


def main():
    if len(sys.argv) != 2:
        raise SystemExit("שימוש: sign_trigger.py <trigger_id>")
    tid = sys.argv[1]
    with open(TRIGGERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    limits = load_limits()
    limits_raw = limits_raw_bytes()
    for t in data.get("triggers", []):
        if t.get("trigger_id") != tid:
            continue
        # בדיקות שפיות לפני חתימה — מרים לא חותמת על מה ש-place_order יחסום ממילא
        if t["symbol"] not in limits["allowed_symbols"]:
            raise SystemExit(f"סירוב חתימה: {t['symbol']} לא ברשימה הלבנה")
        if float(t["order"].get("notional_usdt", 0)) > limits["max_order_notional_usdt"]:
            raise SystemExit("סירוב חתימה: notional מעל התקרה")
        if limits.get("require_stop_loss") and t["order"].get("side") == "BUY" and not t["order"].get("stop"):
            raise SystemExit("סירוב חתימה: קנייה בלי סטופ")
        t["approved_by"] = "miriam"
        t["status"] = "active"
        t["sig"] = trigger_signature(t, limits_raw)
        tmp = TRIGGERS_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, TRIGGERS_FILE)
        print(f"נחתם: {tid} (תקף עד {t.get('expires_at')})")
        return
    raise SystemExit(f"לא נמצא טריגר {tid}")


if __name__ == "__main__":
    main()
