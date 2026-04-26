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

## שלבים שנותרו (12-14)

- [x] **צעד 11** — הוגדרו 4 שיגרות ב-claude.ai/code/routines (2026-04-26)
  - Repo: `danielhassid/dhpe-content-automation`
  - Skill: `dhpe-content-writer`
  - Model: `claude-opus-4-7` (Opus 4.7)
  - Environment: `daniel hassid`
  - Triggers (Asia/Jerusalem, DST):
    - `dhpe-feeding-sat` — שבת 21:00 (אחרי צאת שבת) — Gmail
    - `dhpe-feeding-tue` — שלישי 17:00 — Gmail
    - `dhpe-write-sun` — ראשון 08:00 — Gmail + WP REST API
    - `dhpe-write-wed` — רביעי 08:00 — Gmail + WP REST API
- [ ] **צעד 12** — הרצה ידנית ראשונה של מייל הזנה — בדיקה שמגיע נכון
- [ ] **צעד 13** — הרצה ידנית ראשונה של כתיבת פוסט — בדיקה שהטיוטה מלאה
- [ ] **צעד 14** — הפעלת לוח הזמנים האוטומטי (רק אחרי שצעדים 12-13 עובדים)

## הערות חשובות להמשך

1. **WordPress connector** — צריך לבדוק אם dhpe.co.il הוא WordPress.com או self-hosted, כי זה משפיע על הגדרת ה-connector
2. **כתובת מייל** — dh052597@gmail.com כבר מוגדרת בקבצי התבניות
3. **אין פרסום אוטומטי** — הסקיל מעלה טיוטות בלבד, דניאל מפרסם ידנית
4. **מגבלת Pro** — 5 ריצות ביום, הפרויקט דורש 4 ריצות בשבוע (בתוך המגבלה)
5. **מסמך מקור** — הקובץ `dhpe-content-automation-master-v2.md` נמצא בתיקייה הראשית ומכיל את כל ההנחיות המלאות
