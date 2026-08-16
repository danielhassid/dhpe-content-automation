#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""בדיקת קישוריות ל-Binance: prod, testnet, ו-host הנתונים הציבורי.
מדפיס פסק דין לכל host. אם הכול חסום — המערכת נשארת במצב המלצות (phase 0)."""

import json
import ssl
import sys
import urllib.request
import os

CA_BUNDLE = "/root/.ccr/ca-bundle.crt"
HOSTS = {
    "prod (api.binance.com)": "https://api.binance.com/api/v3/ping",
    "testnet (testnet.binance.vision)": "https://testnet.binance.vision/api/v3/ping",
    "public data (data-api.binance.vision)": "https://data-api.binance.vision/api/v3/ping",
}


def ctx():
    if os.path.exists(CA_BUNDLE):
        return ssl.create_default_context(cafile=CA_BUNDLE)
    return ssl.create_default_context()


def main():
    ok_any = False
    for name, url in HOSTS.items():
        try:
            with urllib.request.urlopen(url, timeout=10, context=ctx()) as r:
                r.read()
            print(f"OK      {name}")
            ok_any = True
        except Exception as e:  # noqa: BLE001
            print(f"BLOCKED {name} — {type(e).__name__}: {e}")
    print()
    if ok_any:
        print("פסק דין: יש קישוריות לפחות ל-host אחד. אפשר לשקול קידום שלב (דניאל בלבד).")
    else:
        print("פסק דין: אין קישוריות לביננס מהסביבה הזו. המערכת נשארת ב-phase 0 (נייר/המלצות).")
    sys.exit(0 if ok_any else 1)


if __name__ == "__main__":
    main()
