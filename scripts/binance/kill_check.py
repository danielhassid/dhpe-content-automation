#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""יוצא בקוד 1 אם KILL-SWITCH קיים. משמש כל נתיב ביצוע לפני פעולה."""

import sys

from binance_client import kill_switch_active

if kill_switch_active():
    print("KILL-SWITCH פעיל — כל ביצוע חסום. מחיקת הקובץ trading-desk/KILL-SWITCH משחררת.")
    sys.exit(1)
print("אין KILL-SWITCH — ביצוע מותר (בכפוף לשאר השערים).")
sys.exit(0)
