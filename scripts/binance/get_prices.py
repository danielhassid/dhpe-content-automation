#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""מחירים ונרות ל-whitelist — endpoints ציבוריים בלבד, בלי מפתחות. משמש את יואב.

שימוש:
  python3 get_prices.py                 # מחיר נוכחי לכל הסימבולים המותרים
  python3 get_prices.py BTCUSDT --klines 4h 50   # 50 נרות 4 שעות
"""

import sys

from binance_client import load_limits, public_get, get_price


def main():
    limits = load_limits()
    symbols = limits["allowed_symbols"]
    args = sys.argv[1:]

    if args and args[0].upper() in symbols and "--klines" in args:
        symbol = args[0].upper()
        i = args.index("--klines")
        interval = args[i + 1] if len(args) > i + 1 else "4h"
        limit = int(args[i + 2]) if len(args) > i + 2 else 50
        rows = public_get("/api/v3/klines", {"symbol": symbol, "interval": interval, "limit": limit})
        print(f"# {symbol} {interval} — {len(rows)} נרות (open-time, open, high, low, close, volume)")
        for r in rows:
            print(f"{r[0]},{r[1]},{r[2]},{r[3]},{r[4]},{r[5]}")
        return

    print("| symbol | price |")
    print("|---|---|")
    for s in symbols:
        print(f"| {s} | {get_price(s)} |")


if __name__ == "__main__":
    main()
