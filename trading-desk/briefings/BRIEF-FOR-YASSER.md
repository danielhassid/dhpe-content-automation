# תדריך ליאסר — שולחן המסחר ביננס (Binance Trading Desk)

> נכתב: 2026-08-16. קהל היעד: יאסר — סוכן AI שרץ על המחשב האישי של דניאל.
> התדריך עצמאי לחלוטין: הוא מניח שאינך מכיר את הריפו בכלל.

---

## 1. מה הפרויקט

דניאל מפעיל בריפו `danielhassid/dhpe-content-automation` (גיטהאב) שתי מערכות
סוכנים: מערכת תוכן לאתר dhpe.co.il, ו**שולחן מסחר ביננס** — התדריך הזה עוסק בשני.

שולחן המסחר הוא צוות של 7 סוכני AI שמנהל תיק השקעות בביננס בשיטת ליבה-לוויין
(Core + Satellite): ליבה ארוכת טווח (יעד 80% מהתיק) ותיק מסחר אקטיבי קטן
(עד 20%). כרגע הכול על נייר — אף שקל אמיתי לא זז (Phase 0, paper trading).

## 2. הצוות ושרשרת ההחלטה

| פרסונה | סקיל (skill) | תפקיד | הקובץ שהיא כותבת |
|---|---|---|---|
| **תמר** | `binance-macro-analyst` | מאקרו — משטר שוק (risk-on/risk-off) | `trading-desk/inbox/market-view.md` |
| **נועה** | `binance-news-sentiment` | חדשות וסנטימנט — כולל דגל אדום (red_flag) שמקפיא עסקאות Satellite חדשות | `trading-desk/inbox/news-sentiment.md` |
| **יואב** | `binance-technical-analyst` | טכני — סטאפים, רמות, סטופים (Satellite בלבד) | `trading-desk/inbox/technical-view.md` |
| **אלון** | `binance-cio` | מנהל השקעות ראשי — מסנתז את השלושה להחלטת יום והצעות עסקה | `trading-desk/decisions/YYYY-MM-DD-decision.md`, `trade-proposals.md` |
| **מרים** | `binance-risk-manager` | סיכונים — היחידה שמאשרת; וטו סופי; חותמת טריגרים | `trading-desk/decisions/risk-verdict.md` + חתימה ב-`active-triggers.json` |
| **איתן** | `binance-trade-executor` | ביצוע — היחיד שנוגע ב-API; מבצע רק APPROVED טרי של מרים | `trading-desk/state/` (portfolio-state, orders-log, trade-journal) |
| **גדי** | `binance-performance-retro` | מבקר — רטרוספקטיבה שבועית וכללים מחייבים | `trading-desk/rules/trading-rules.md`, `learnings-log.md` |

שרשרת ההחלטה: **תמר / נועה / יואב ← אלון ← מרים ← איתן**, ובסוף השבוע גדי.
כל סוכן רץ כסאב-איג'נט נפרד; התקשורת ביניהם היא **דרך קבצים בלבד** — כל סוכן
כותב אך ורק את קובץ החוזה שלו.

## 3. חוזה הקבצים — עץ trading-desk/

```
trading-desk/
├── config/
│   ├── limits.json        # מגבלות קשיחות — רק דניאל עורך ידנית
│   └── phase.json         # שלב נוכחי (0/1/2) — רק דניאל עורך ידנית
├── KILL-SWITCH            # אם הקובץ קיים — כל ביצוע נעצר מיידית
├── inbox/                 # דוחות האנליסטים: market-view, technical-view, news-sentiment
├── decisions/             # החלטות יום (YYYY-MM-DD-decision.md), trade-proposals, risk-verdict
├── state/                 # active-triggers.json, portfolio-state.md, orders-log.jsonl, trade-journal
├── rules/                 # trading-rules.md (מחייב), learnings-log.md
└── briefings/             # תדריכים — כולל הקובץ הזה
scripts/binance/           # הקוד: binance_client, place_order (שערי הבטיחות),
                           # market_watcher, sign_trigger, kill_check ועוד
```

המגבלות הקשיחות כרגע ב-`limits.json` (מקור האמת היחיד למספרים אלה):
סמלים מותרים BTCUSDT / ETHUSDT / SOLUSDT / BNBUSDT; פוזיציה עד 10% מהתיק;
פקודה עד 50 USDT; עד 3 פוזיציות Satellite פתוחות; מגבלת הפסד יומית 2% ושבועית 5%;
חלוקת Core/Satellite ‏80/20; סטופ-לוס חובה; קירור 24 שעות אחרי הפסד;
תוקף טריגר עד 24 שעות; פסק דין של מרים תקף 12 שעות.

## 4. כללי הברזל

1. **מרים היא היחידה שמאשרת** עסקאות. הווטו שלה סופי להיום.
2. **איתן הוא היחיד שמבצע**, ורק דרך `scripts/binance/place_order.py`, ורק
   הצעות APPROVED טריות מפסק הדין של מרים. בלי APPROVED טרי — איתן לא עושה כלום.
3. **KILL-SWITCH:** קיום הקובץ `trading-desk/KILL-SWITCH` עוצר כל ביצוע מיידית,
   כולל ה-watcher החיצוני. דניאל ומרים רשאים ליצור; רק דניאל מוחק.
4. **קבצים שרק דניאל עורך ידנית:** `trading-desk/config/limits.json`,
   `trading-desk/config/phase.json`. סוכן שרוצה שינוי — מציע בכתב, לא עורך.
5. **מפתחות API לעולם לא בריפו** — משתני סביבה בלבד (`BINANCE_API_KEY/SECRET`,
   `BINANCE_TESTNET_API_KEY/SECRET`). בצד ביננס: הרשאת spot trade בלבד,
   **משיכות כבויות לתמיד** (withdrawals disabled).
6. **מודל השלבים:** Phase 0 נייר ← Phase 1 בורסת ניסיון (testnet) ← Phase 2 חי
   בתקרות זעירות. קידום שלב = עריכה ידנית של דניאל ב-`phase.json` בלבד,
   אחרי הצ'קליסט ב-PROGRESS.md.
7. **עקיבות:** כל פקודה נושאת proposal_id או trigger_id. אין פקודות יתומות.
8. **אין המצאת נתונים.** אין נתון = אומרים "אין נתון". מספר שיש לו קובץ —
   מצטטים מהקובץ, לא מהזיכרון.

## 5. מצב נוכחי (16.08.2026)

- **Phase 0 — נייר/המלצות בלבד** (`phase.json`: phase 0, env paper, אושר על ידי
  דניאל ב-16.08.2026). איתן מדמה מילוי ורושם ל-orders-log.jsonl בלבד.
- **ריצת בכורה בוצעה היום.** תמצית החלטת היום של אלון
  (`decisions/2026-08-16-decision.md`): מאקרו risk-off מתון (תמר), אין דגל אדום
  (נועה), BTC בתחתית הטווח 62,500–65,000 (יואב). ההחלטה: מתחילים DCA הדרגתי
  לליבה — מנה ראשונה קטנה ב-BTC בלבד; ETH נדחה לריצה הבאה.
- **התיק הווירטואלי** (`state/portfolio-state.md`): יתרת פתיחה 1,000 USDT.
  אחרי מילוי נייר P-2026-08-16-01: ‏950 USDT ‏+ ‏0.0007959 BTC (כ-50 USDT
  במחיר ייחוס 62,822.24). ‏Core בפועל 5% (יעד 80%), ‏Satellite ‏0%.
  סטופ מבני לליבת BTC: ‏56,000.
- **טריגר פעיל אחד** (`state/active-triggers.json`): ‏T-2026-08-16-01 —
  קניית BTCUSDT ב-LIMIT אם המחיר יורד ל-60,200 ומטה, ‏50 USDT ל-Satellite,
  סטופ 58,900, יעד 63,800. חתום על ידי מרים, פג תוקף 17.08 ב-07:35 UTC.

## 6. ארכיטקטורת מוח-שריר — והנקודה שרלוונטית אליך

- **המוח:** הסוכנים רצים בתזמון (Routine) ומייצרים החלטות + טריגרים מותנים
  חתומים עם תוקף (TTL) ב-`trading-desk/state/active-triggers.json`.
- **הבורסה קודם:** כל תנאי שביננס יודעת להחזיק כפקודה נחה (LIMIT / OCO / STOP)
  מונח ישירות בבורסה — אמין יותר מכל לולאה.
- **השריר:** `scripts/binance/market_watcher.py` — סקריפט בלי מודל שפה שמנטר
  מחירים ומבצע טריגרים שהתנאי שלהם התקיים, עם אותם שערי בטיחות בדיוק.
  **הוא חייב מארח קבוע** — שרת פרטי, Raspberry Pi או מחשב דולק — כי סביבת
  claude.ai חוסמת גישה לביננס (נבדק 16.08.2026).

**הצעה לדניאל (לא הוראה):** אם יאסר רץ על מחשב קבוע של דניאל, הוא מועמד טבעי
להריץ את ה-watcher — משיכת עדכונים מהריפו (git pull) ואז
`python3 scripts/binance/market_watcher.py --interval 60`. ההחלטה אם וכיצד —
של דניאל בלבד, והיא רלוונטית בפועל רק מ-Phase 1 ואילך (ב-Phase 0 אין בורסה).

## 7. איך יאסר מתעדכן שוטף

1. `git pull` על הריפו `danielhassid/dhpe-content-automation`.
2. לקרוא את `trading-desk/decisions/` — החלטת היום האחרונה, הצעות העסקה
   ופסק הדין של מרים.
3. לקרוא את `trading-desk/state/` — מצב התיק (portfolio-state.md) והטריגרים
   הפעילים (active-triggers.json).
4. מספרים ומגבלות — תמיד מ-`trading-desk/config/limits.json` ו-`phase.json`,
   לא מהזיכרון.

זהו. ברוך הבא לשולחן.
