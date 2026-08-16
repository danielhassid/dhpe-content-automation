#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""יתרות ופקודות פתוחות (קריאה חתומה) → markdown מוכן ל-portfolio-state.md.
במצב paper אין מה לשאול את הבורסה — התיק הווירטואלי מתוחזק ע"י איתן בקובץ עצמו."""

import time

from binance_client import current_env, signed_request


def main():
    env = current_env()
    if env == "paper":
        print("מצב paper: אין תיק בבורסה. איתן מתחזק את trading-desk/state/portfolio-state.md ידנית לפי orders-log.jsonl.")
        return

    account = signed_request("/api/v3/account")
    open_orders = signed_request("/api/v3/openOrders")

    print(f"# מצב תיק — portfolio-state (env: {env})")
    print()
    print("## יתרות")
    print("| נכס | free | locked |")
    print("|---|---|---|")
    for b in account.get("balances", []):
        free, locked = float(b["free"]), float(b["locked"])
        if free > 0 or locked > 0:
            print(f"| {b['asset']} | {b['free']} | {b['locked']} |")
    print()
    print("## פקודות פתוחות בבורסה")
    if not open_orders:
        print("אין.")
    else:
        print("| symbol | side | type | qty | price | stopPrice | orderId |")
        print("|---|---|---|---|---|---|---|")
        for o in open_orders:
            print(f"| {o['symbol']} | {o['side']} | {o['type']} | {o['origQty']} | {o['price']} | {o.get('stopPrice','-')} | {o['orderId']} |")
    print()
    print(f"_עדכון אחרון: {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}_")


if __name__ == "__main__":
    main()
