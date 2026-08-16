# DHPE Content Automation — סטטוס התקדמות

## שלבים שבוצעו (1-10)

- [x] **צעד 1** — נוצר repo ב-GitHub: `danielhassid/dhpe-content-automation`
- [x] **צעד 2** — נוצר מבנה התיקיות המלא
- [x] **צעד 3** — נבנה SKILL.md עם הוראות הפעלה מלאות
- [x] **צעד 4** — הועתק כל התוכן ל-knowledge (business-context, pricing, competitors, target-audience)
- [x] **צעד 5** — נבנה post-template.md עם המבנה האחיד
- [x] **צעד 6** — נבנה seo-checklist.md עם כל רכיבי ה-SEO
- [x] **צעד 7** — נבנה schema-faq.json עם תבנית Schema Markup
- [x] **צעד 8** — נבנה feeding-email.md עם תבנית מייל ההזנה (כולל כתובת dh052597@gmail.com)
- [x] **צעד 9** — נבנה draft-ready-email.md עם תבנית מייל ההתראה
- [x] **צעד 10** — הועלה ל-GitHub (commit + push)

## שלבים שנותרו (11-14)

- [ ] **צעד 11** — הגדרת Routine ב-claude.ai/code/routines
  - Repo: `danielhassid/dhpe-content-automation`
  - Skill: `dhpe-content-writer`
  - Connectors: WordPress + Gmail
  - Trigger כתיבה: ראשון + רביעי ב-08:00
  - Trigger הזנה: שבת + שלישי ב-17:00
- [ ] **צעד 12** — הרצה ידנית ראשונה של מייל הזנה — בדיקה שמגיע נכון
- [ ] **צעד 13** — הרצה ידנית ראשונה של כתיבת פוסט — בדיקה שהטיוטה מלאה
- [ ] **צעד 14** — הפעלת לוח הזמנים האוטומטי (רק אחרי שצעדים 12-13 עובדים)

---

# שולחן המסחר ביננס — סטטוס התקדמות

## שלבים שבוצעו (2026-08-16)

- [x] **צעד 1** — נבנה עץ `trading-desk/` מלא: config (limits.json, phase.json ב-Phase 0), inbox, decisions, state, rules
- [x] **צעד 2** — נכתבו הסקריפטים ב-`scripts/binance/`: client, connectivity, prices, portfolio, place_order (כל שערי הבטיחות), market_watcher, sign_trigger, kill_check
- [x] **צעד 3** — בדיקת קישוריות: api.binance.com / testnet / data-api — **כולם חסומים מה-sandbox (403)**. המערכת נשארת ב-Phase 0
- [x] **צעד 4** — נבדקו שערי הבטיחות בפועל: פקודת נייר תקינה ✓, חסימת notional ✓, חסימת קנייה בלי סטופ ✓, חסימת סימבול זר ✓, KILL-SWITCH ✓
- [x] **צעד 5** — נבדק ה-watcher בפועל: טריגר חתום נורה פעם אחת ✓, אין ביצוע כפול ✓, טריגר שנערך אחרי חתימה נפסל ✓, TTL פג ✓
- [x] **צעד 6** — נבנו 7 הסקילים: binance-cio (אלון), binance-macro-analyst (תמר), binance-technical-analyst (יואב), binance-news-sentiment (נועה), binance-risk-manager (מרים), binance-trade-executor (איתן), binance-performance-retro (גדי)
- [x] **צעד 7** — נכתבו CLAUDE.md, .gitignore, ועודכן README

## שלבים שנותרו

- [ ] **צעד 8** — הרצה ידנית מלאה של צנרת הבוקר ב-Phase 0 (תמר → נועה → יואב → אלון → מרים → איתן) ובדיקה שכל סוכן כותב רק את קובץ החוזה שלו
- [ ] **צעד 9** — רטרו ראשון של גדי אחרי שבוע נייר
- [ ] **צעד 10** — הגדרת Routine "סריקת בוקר" (א'–ה' 07:30) + "רטרו שבועי" (ו' 09:00) — רק אחרי שצעד 8 עובר
- [ ] **צעד 11** — Phase 1: יצירת מפתחות testnet (testnet.binance.vision) כ-env secrets, מארח חיצוני ל-market_watcher, עדכון phase.json ידנית
- [ ] **צעד 12** — פקודת LIMIT אחת ב-testnet שנראית ב-get_portfolio.py
- [ ] **צעד 13** — שבועיים / 10 עסקאות נקיות ב-testnet בלי הפרת חוזה
- [ ] **צעד 14** — Phase 2: מפתחות אמיתיים (spot בלבד, בלי משיכות, IP whitelist), תקרות זעירות ב-limits.json, עדכון phase.json ידנית

## הערות חשובות — שולחן המסחר

1. **עומס Routines:** מסחר 6/שבוע + תוכן 4/שבוע; היום העמוס ביותר = 2 ריצות — בתוך מגבלת 5/יום. אפשר להתחיל א'/ג'/ה' בלבד
2. **egress:** כל ה-hosts של ביננס חסומים מה-sandbox. ה-watcher חייב VPS / Raspberry Pi / מחשב דולק
3. **מפתחות:** env secrets בלבד. לא לחזור על תקרית הסיסמה ב-RUN-LOG
4. **קבצים שרק דניאל עורך:** limits.json, phase.json. מחיקת KILL-SWITCH — רק דניאל

## הערות חשובות להמשך

1. **WordPress connector** — צריך לבדוק אם dhpe.co.il הוא WordPress.com או self-hosted, כי זה משפיע על הגדרת ה-connector
2. **כתובת מייל** — dh052597@gmail.com כבר מוגדרת בקבצי התבניות
3. **אין פרסום אוטומטי** — הסקיל מעלה טיוטות בלבד, דניאל מפרסם ידנית
4. **מגבלת Pro** — 5 ריצות ביום, הפרויקט דורש 4 ריצות בשבוע (בתוך המגבלה)
5. **מסמך מקור** — הקובץ `dhpe-content-automation-master-v2.md` נמצא בתיקייה הראשית ומכיל את כל ההנחיות המלאות
