#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""סורק שוק רוחבי — endpoints ציבוריים בלבד, בלי מפתחות. משמש את לירון (binance-market-scanner).

מאתר אנומליות שמקדימות פריצת מחיר, ולא פריצות שכבר קרו.

שימוש:
  python3 scan_anomalies.py                    # סריקה מלאה, פלט JSON
  python3 scan_anomalies.py --top 8            # 8 מועמדים במקום 5
  python3 scan_anomalies.py --quote USDT       # צמד ציטוט (ברירת מחדל USDT)
  python3 scan_anomalies.py --min-volume 500000  # רצפת נזילות, דורס את limits.json
  python3 scan_anomalies.py --symbols VETUSDT,ADAUSDT  # בדיקה ממוקדת

⚠️ הסקריפט מדווח בלבד. הוא לא מציע עסקה, לא קובע רמות ולא נוגע בשום קובץ מצב.
כל מטבע שהוא מחזיר נמצא כמעט תמיד **מחוץ** ל-allowed_symbols, ולכן אינו סחיר
עד שדניאל מוסיף אותו לרשימה הלבנה ידנית. זו הכוונה: הסורק מרחיב את שדה הראייה,
לא את הרשאות המסחר.
"""

import argparse
import json
import sys
import time

from binance_client import load_limits, public_get

# רצפת נזילות ברירת מחדל — מתחת לזה השוק דק מדי מכדי לצאת ממנו
DEFAULT_MIN_VOLUME_USDT = 500_000
# מטבעות ממונפים ומוצרים נגזרים — לא נכסי ספוט אמיתיים, מסננים החוצה
JUNK_SUFFIXES = ("UPUSDT", "DOWNUSDT", "BULLUSDT", "BEARUSDT")
STABLE_BASES = {"USDC", "FDUSD", "TUSD", "BUSD", "DAI", "USDP", "EURI", "AEUR", "XUSD"}


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def fetch_universe(quote, min_volume):
    """כל הצמדים מול quote שעוברים את רצפת הנזילות. קריאה אחת, לא לולאה."""
    rows = public_get("/api/v3/ticker/24hr")
    out = []
    for r in rows:
        sym = r.get("symbol", "")
        if not sym.endswith(quote) or sym.endswith(JUNK_SUFFIXES):
            continue
        base = sym[: -len(quote)]
        if base in STABLE_BASES or not base:
            continue
        vol = _f(r.get("quoteVolume"))
        if vol < min_volume:
            continue
        out.append({
            "symbol": sym,
            "quote_volume_24h": vol,
            "price": _f(r.get("lastPrice")),
            "pct_24h": _f(r.get("priceChangePercent")),
            "high_24h": _f(r.get("highPrice")),
            "low_24h": _f(r.get("lowPrice")),
            "trades_24h": int(r.get("count") or 0),
        })
    return out


def daily_candles(symbol, days=60):
    return public_get("/api/v3/klines", {"symbol": symbol, "interval": "1d", "limit": days})


def analyze(symbol, candles):
    """שלוש האנומליות שניתן לחשב מנתוני ספוט ציבוריים בלבד."""
    if len(candles) < 20:
        return None

    closes = [_f(c[4]) for c in candles]
    highs = [_f(c[2]) for c in candles]
    lows = [_f(c[3]) for c in candles]
    qvols = [_f(c[7]) for c in candles]  # quote asset volume

    today_vol = qvols[-1]
    base_vols = qvols[-15:-1]  # 14 ימים אחורה, בלי היום
    avg_vol = sum(base_vols) / len(base_vols) if base_vols else 0.0
    vol_ratio = (today_vol / avg_vol) if avg_vol > 0 else 0.0

    day_range_pct = ((highs[-1] - lows[-1]) / lows[-1] * 100) if lows[-1] else 0.0

    window = closes[-60:] if len(closes) >= 60 else closes
    peak = max(highs[-len(window):])
    trough = min(lows[-len(window):])
    range_pct = ((peak - trough) / trough * 100) if trough else 0.0
    drawdown_from_peak = ((peak - closes[-1]) / peak * 100) if peak else 0.0

    # שער-על: אנומליה שמעניינת אותנו קורית **לפני** תנועת המחיר. יום שכבר זז
    # בחדות הוא פריצה שהחמצנו או פאמפ, ובשני המקרים לא מועמד לצבירה שקטה.
    # בלי השער הזה הסורק מחזיר בדיוק את מה שהוא אמור לסנן החוצה (נבדק 16.8:
    # UTKUSDT עלה עם טווח יומי 247% וקיבל ציון גבוה).
    if day_range_pct > 12.0:
        return None

    # דחיסה יחסית: 3% הוא טווח צר למטבע אחד ורחב למטבע אחר. משווים כל מטבע
    # לעצמו — לחציון הטווח היומי שלו ב-14 הימים האחרונים.
    prior_ranges = sorted(
        ((highs[i] - lows[i]) / lows[i] * 100) for i in range(-15, -1) if lows[i]
    )
    median_range = prior_ranges[len(prior_ranges) // 2] if prior_ranges else 0.0
    compression_ratio = (day_range_pct / median_range) if median_range else 0.0

    signals = []
    # 1. נפח חריג בתוך דחיסת מחיר — הצבירה השקטה
    if vol_ratio >= 2.5 and day_range_pct < 3.0:
        signals.append("volume_spike_price_compression")
    # 1ב. אותה תבנית, במידה של המטבע עצמו: נפח קופץ והטווח מתכווץ מתחת ל-60%
    # מהחציון שלו. תופס מטבעות שהטווח היומי הרגיל שלהם גדול מ-3%.
    if vol_ratio >= 2.5 and 0 < compression_ratio < 0.6:
        signals.append("relative_compression_absorption")
    # 2. בסיס ארוך: טווח צר לאורך זמן עם התעוררות ראשונית בנפח
    if range_pct < 25.0 and len(window) >= 45 and vol_ratio >= 1.8:
        signals.append("long_base_awakening")
    # 3. ירידה עמוקה מהשיא בחלון + נפח מתעורר, בלי שהמחיר כבר קפץ
    if drawdown_from_peak >= 40.0 and vol_ratio >= 2.0 and day_range_pct < 8.0:
        signals.append("deep_base_volume_return")

    if not signals:
        return None

    return {
        "symbol": symbol,
        "signals": signals,
        "volume_ratio_vs_14d": round(vol_ratio, 2),
        "quote_volume_24h": round(today_vol, 2),
        "avg_quote_volume_14d": round(avg_vol, 2),
        "day_range_pct": round(day_range_pct, 2),
        "median_day_range_14d_pct": round(median_range, 2),
        "compression_vs_own_median": round(compression_ratio, 2),
        "window_range_pct": round(range_pct, 2),
        "drawdown_from_window_peak_pct": round(drawdown_from_peak, 2),
        "window_days": len(window),
        "last_close": closes[-1],
        "window_low": trough,
        "window_high": peak,
        "score": round(vol_ratio * len(signals), 2),
    }


def main():
    p = argparse.ArgumentParser(description="סורק אנומליות שוק — דיווח בלבד")
    p.add_argument("--quote", default="USDT")
    p.add_argument("--top", type=int, default=5)
    p.add_argument("--min-volume", type=float, default=None)
    p.add_argument("--symbols", default=None, help="רשימה מופרדת בפסיקים, עוקף את הסריקה הרחבה")
    p.add_argument("--max-candidates", type=int, default=120,
                   help="כמה צמדים למשוך להם נרות (כל אחד = קריאה נפרדת)")
    args = p.parse_args()

    limits = load_limits()
    min_volume = args.min_volume
    if min_volume is None:
        min_volume = _f(limits.get("min_daily_quote_volume_usdt")) or DEFAULT_MIN_VOLUME_USDT

    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    if args.symbols:
        universe = [{"symbol": s.strip().upper()} for s in args.symbols.split(",") if s.strip()]
    else:
        universe = fetch_universe(args.quote, min_volume)
        universe.sort(key=lambda r: r["quote_volume_24h"], reverse=True)
        universe = universe[: args.max_candidates]

    findings, errors = [], []
    for row in universe:
        sym = row["symbol"]
        try:
            res = analyze(sym, daily_candles(sym))
        except Exception as exc:  # רשת/סימבול לא קיים — לא מפיל את הסריקה
            errors.append({"symbol": sym, "error": f"{type(exc).__name__}: {exc}"})
            continue
        if res:
            res["whitelisted"] = sym in limits.get("allowed_symbols", [])
            findings.append(res)

    findings.sort(key=lambda r: r["score"], reverse=True)

    report = {
        "scanned_at_utc": started,
        "quote": args.quote,
        "min_daily_quote_volume_usdt": min_volume,
        "pairs_in_universe": len(universe),
        "pairs_with_anomaly": len(findings),
        "errors": errors[:10],
        "note": "דיווח בלבד. מטבע שאינו ב-allowed_symbols אינו סחיר עד שדניאל יוסיף אותו ידנית.",
        "candidates": findings[: args.top],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not (errors and not findings) else 0


if __name__ == "__main__":
    sys.exit(main())
