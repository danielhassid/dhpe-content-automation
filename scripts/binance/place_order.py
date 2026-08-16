#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
place_order.py — נתיב הקוד היחיד שמותר לו לשלוח פקודה.

שערים (כולם חייבים לעבור, כל כשל נרשם כ-status="blocked"):
  1. אין KILL-SWITCH ואין עצירת-יום (DAILY-HALT-<תאריך>)
  2. phase.json מתיר את ה-env (live רק ב-phase 2)
  3. יש ‎--proposal-id או ‎--trigger-id (עקיבות מלאה — אין פקודה "יתומה")
  4. הסימבול ב-allowed_symbols
  5. סוג הפקודה ב-order_types_allowed
  6. notional עד max_order_notional_usdt
  7. require_stop_loss: פקודת BUY נכנסת רק עם ‎--stop
מגבלות שדורשות תמונת תיק (הפסד יומי/שבועי, מספר פוזיציות) נאכפות ע"י מרים בפסק
הדין; כשמגבלת הפסד נפרצת — מרים/איתן יוצרים קובץ DAILY-HALT והקוד חוסם מכנית.

שימוש:
  python3 place_order.py --proposal-id P-2026-08-16-01 --symbol BTCUSDT --side BUY \
      --type LIMIT --notional 50 --price 58000 --stop 56500
"""

import argparse
import os
import sys
import time

from binance_client import (
    DESK, append_order_log, current_env, get_price, kill_switch_active,
    load_limits, signed_request,
)


def daily_halt_active():
    return os.path.exists(os.path.join(DESK, "state", "DAILY-HALT-" + time.strftime("%Y-%m-%d", time.gmtime())))


def _blocked(record, reason):
    record.update(status="blocked", error=reason)
    append_order_log(record)
    print(f"חסום: {reason}")
    return 1


def execute_order(spec, source, ref_id):
    """spec: dict עם symbol, side, type, notional_usdt, price, stop, take_profit.
    מחזיר exit code. משמש גם את market_watcher.py — אותם שערים בדיוק."""
    limits = load_limits()
    env = current_env()
    record = {
        "env": env, "source": source, "ref_id": ref_id,
        "symbol": spec.get("symbol"), "side": spec.get("side"), "type": spec.get("type"),
        "notional_usdt": spec.get("notional_usdt"), "price": spec.get("price"),
        "stop": spec.get("stop"), "take_profit": spec.get("take_profit"),
    }

    if kill_switch_active():
        return _blocked(record, "KILL-SWITCH פעיל")
    if daily_halt_active():
        return _blocked(record, "עצירת יום (DAILY-HALT) פעילה — נפרצה מגבלת הפסד יומי")
    if not ref_id:
        return _blocked(record, "אין proposal-id/trigger-id — פקודה ללא עקיבות אסורה")
    if spec["symbol"] not in limits["allowed_symbols"]:
        return _blocked(record, f"סימבול {spec['symbol']} לא ברשימה הלבנה")
    if spec["type"] not in limits["order_types_allowed"]:
        return _blocked(record, f"סוג פקודה {spec['type']} לא מותר")
    notional = float(spec.get("notional_usdt") or 0)
    if notional <= 0 or notional > limits["max_order_notional_usdt"]:
        return _blocked(record, f"notional {notional} מחוץ לטווח (מקס {limits['max_order_notional_usdt']} USDT)")
    if limits.get("require_stop_loss") and spec["side"] == "BUY" and not spec.get("stop"):
        return _blocked(record, "require_stop_loss: פקודת קנייה בלי סטופ אסורה")

    if env == "paper":
        fill_price = float(spec.get("paper_price") or spec.get("price") or 0)
        if not fill_price:
            try:
                fill_price = get_price(spec["symbol"])
            except SystemExit:
                return _blocked(record, "paper: אין מחיר (egress חסום) ולא סופק --paper-price")
        qty = round(notional / fill_price, 8)
        record.update(status="filled_paper", fill_price=fill_price, qty=qty)
        append_order_log(record)
        print(f"נייר: {spec['side']} {qty} {spec['symbol']} @ {fill_price} (notional {notional} USDT)")
        return 0

    # testnet / live — פקודה אמיתית
    price_for_qty = float(spec.get("price") or get_price(spec["symbol"]))
    qty = round(notional / price_for_qty, 6)
    try:
        if spec["type"] == "MARKET":
            resp = signed_request("/api/v3/order", {
                "symbol": spec["symbol"], "side": spec["side"], "type": "MARKET",
                "quoteOrderQty": notional}, method="POST")
        elif spec["type"] == "OCO":
            if not (spec.get("price") and spec.get("stop")):
                return _blocked(record, "OCO דורש price (יעד) וגם stop")
            stop = float(spec["stop"])
            resp = signed_request("/api/v3/order/oco", {
                "symbol": spec["symbol"], "side": spec["side"], "quantity": qty,
                "price": spec["price"], "stopPrice": stop,
                "stopLimitPrice": round(stop * (0.995 if spec["side"] == "SELL" else 1.005), 2),
                "stopLimitTimeInForce": "GTC"}, method="POST")
        elif spec["type"] in ("STOP_LOSS_LIMIT", "TAKE_PROFIT_LIMIT"):
            trigger_price = spec.get("stop") if spec["type"] == "STOP_LOSS_LIMIT" else spec.get("take_profit")
            if not (spec.get("price") and trigger_price):
                return _blocked(record, f"{spec['type']} דורש price וגם מחיר הפעלה")
            resp = signed_request("/api/v3/order", {
                "symbol": spec["symbol"], "side": spec["side"], "type": spec["type"],
                "timeInForce": "GTC", "quantity": qty,
                "price": spec["price"], "stopPrice": trigger_price}, method="POST")
        else:  # LIMIT
            if not spec.get("price"):
                return _blocked(record, "LIMIT דורש --price")
            resp = signed_request("/api/v3/order", {
                "symbol": spec["symbol"], "side": spec["side"], "type": "LIMIT",
                "timeInForce": "GTC", "quantity": qty, "price": spec["price"]}, method="POST")
    except SystemExit as e:
        return _blocked(record, str(e))

    order_id = resp.get("orderId") or resp.get("orderListId")
    record.update(status="submitted", qty=qty, binance_order_id=order_id)
    append_order_log(record)
    print(f"נשלח ({env}): {spec['type']} {spec['side']} {qty} {spec['symbol']} — order id {order_id}")
    return 0


def main():
    p = argparse.ArgumentParser()
    ref = p.add_mutually_exclusive_group(required=True)
    ref.add_argument("--proposal-id")
    ref.add_argument("--trigger-id")
    p.add_argument("--symbol", required=True)
    p.add_argument("--side", required=True, choices=["BUY", "SELL"])
    p.add_argument("--type", required=True)
    p.add_argument("--notional", type=float, required=True, help="גודל בפקודה ב-USDT")
    p.add_argument("--price", type=float)
    p.add_argument("--stop", type=float)
    p.add_argument("--take-profit", type=float, dest="take_profit")
    p.add_argument("--paper-price", type=float, dest="paper_price", help="מחיר מילוי מדומה כשאין רשת")
    a = p.parse_args()

    spec = {"symbol": a.symbol.upper(), "side": a.side, "type": a.type.upper(),
            "notional_usdt": a.notional, "price": a.price, "stop": a.stop,
            "take_profit": a.take_profit, "paper_price": a.paper_price}
    source = "routine" if a.proposal_id else "watcher"
    sys.exit(execute_order(spec, source, a.proposal_id or a.trigger_id))


if __name__ == "__main__":
    main()
