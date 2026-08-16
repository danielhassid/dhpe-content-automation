# Run log — Post 03

**Date:** 2026-07-29 (יום רביעי)
**Mode:** write-and-publish
**Operator:** Claude Code (Opus 4.7) running in scheduled routine
**Target post:** חמישה סימנים שהכיתה שלך צריכה ODT דחוף (חודש 1 / שבוע 2 / ראשון, נישה 1 — ליבה)

## Outcomes

| שלב | סטטוס |
|---|---|
| 1. בחירת פוסט הבא מהתוכנית | ✅ נבחר: "חמישה סימנים שהכיתה שלך צריכה ODT דחוף" (הראשון שאין לו עדיין תיקיית write-mode; posts 01+02 כבר יש להם, אבל upload שלהם עדיין תלוי egress) |
| 2. אימות שלא פורסם בוורדפרס | ⚠️ חסום — HTTP 403 host_not_allowed ל-www.dhpe.co.il |
| 3. חיפוש תשובת דניאל בג'ימייל ל-48 שעות אחרונות | ✅ חופש דרך Gmail MCP `search_threads` (`from:dh052597@gmail.com newer_than:14d` + `newer_than:7d (סימנים OR ODT OR ...)`). אין תשובה מדניאל בנושא הפוסט. הפוסט נכתב בלי סיפור אישי. |
| 4. WebSearch + ניתוח תחרות | ✅ 3 תוצאות מובילות ב-Hebrew: koobiot/hulahoop/321odt לצד תוצאות קליניות (rimonclinic, drtal, licbt). פער תוכן זוהה: אין תוצאה שמדברת בשפת הרכזת החברתית עם קריטריונים אבחוניים לדינמיקה כיתתית (רק דיבור עסקי-שיווקי או קליני-הורים). |
| 5. כתיבת פוסט 1500-2000 מילים | ✅ 1945 מילים בעברית, ללא סיפור אישי (לא זמין) |
| 6. חבילת SEO | ✅ Meta Title 45 תווים, Meta Desc 142 תווים, Slug, Focus Keyword, OG/Twitter, 5 שאלות FAQ + Schema JSON-LD |
| 7. העלאה כטיוטה לוורדפרס | ❌ חסום (HTTP 403 host_not_allowed) |
| 8. שליחת מייל התראה ב-SMTP | ❌ חסום (TimeoutError על smtp.gmail.com:465 גם עם pre-resolve ל-IPv4) |
| 9. עדכון תוכנית פוסטים | ⚠️ נשאר `pending` — לא בוצעה העלאה אמיתית ל-WP, לפי אותה החלטה מ-RUN-LOG של post-01 ו-post-02 |

## Network blockers (מילולית)

```
$ curl -sS -w "HTTP=%{http_code}\n" -u 'dh052597@gmail.com:***' \
    -X POST 'https://www.dhpe.co.il/wp-json/wp/v2/posts' \
    -H 'Content-Type: application/json; charset=utf-8' \
    --data-binary @wp-payload.json
curl: (56) CONNECT tunnel failed, response 403
HTTP=000
# /root/.ccr status: recentRelayFailures →
#   "gateway answered 403 to CONNECT (policy denial or upstream failure)"
#   host: "www.dhpe.co.il:443"
```

```
$ python3 -c "smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30)  # IPv4-only"
SMTP FAIL: TimeoutError: timed out
```

הבעיה זהה ל-RUN-LOGs של post-01 (2026-04-29), post-02 (2026-06-10), ולכל ה-feeding-email DRAFTs מ-2026-05-30 עד 2026-07-18.

## Content-plan status

`content-plan/24-posts-plan.md` **לא עודכן** — הפוסט נשאר `pending`. הוא יעודכן ל-`draft-ready` רק כאשר ה-WP upload יבוצע בפועל (בין אם ידנית מסביבה עם egress פתוח, ובין אם ב-routine עתידית לאחר עדכון ה-network policy).

## מה דרוש כדי לסיים את הריצה הזו

**אופציה א — להריץ את הסקיל מסביבה ללא חסימת egress:**

1. `cd /path/to/dhpe-content-automation` עם הקבצים מהקומיט הזה
2. הרצת העלאת ה-draft:
   ```bash
   curl -u 'dh052597@gmail.com:6fZA HCsa nTIw rFYh JQnL PU42' \
     -X POST 'https://www.dhpe.co.il/wp-json/wp/v2/posts' \
     -H 'Content-Type: application/json; charset=utf-8' \
     --data-binary @.claude/skills/dhpe-content-writer/posts/post-03-chamisha-simanim-odt/wp-payload.json
   ```
   קחו את ה-`id` שחוזר.
3. הכינו את מייל ההתראה: החליפו `__POST_ID__` ב-`notification-email.md` ב-ID האמיתי, ושילחו את זה דרך `/tmp/send_notify.py` (או הריצו את סקריפט ה-SMTP מהוראות המקוריות).
4. עדכנו את `content-plan/24-posts-plan.md` בשורה "חודש 1 / שבוע 2 / ראשון" מ-`pending` ל-`draft-ready`.

**אופציה ב — להוסיף את `www.dhpe.co.il` ו-`smtp.gmail.com` ל-network policy allowlist:**

הגדרות ה-egress של ה-remote environment ב-Settings → Network policy של Claude Code on the web. תיעוד: https://code.claude.com/docs/en/claude-code-on-the-web. עד שזה ייפתר, כל ריצות הסקיל יסתיימו באותה תבנית — קבצים מוכנים בקומיט, WP upload ו-SMTP notify חסומים.

## Content notes

**זווית הפוסט:** מיועד ל-**רכזת חברתית ולמחנכת** — לא למנהל ולא להורים. הפער שזוהה במחקר: הכל בעברית שמתקרב לנושא "בעיות חברתיות בכיתה" כתוב או בשפה **שיווקית של ספק ODT** (koobiot, hulahoop, 321odt) או בשפה **קלינית-הורים** (rimonclinic, drtal, licbt). אין תוצאה מובילה שמדברת ב**שפת הרכזת החברתית** עם קריטריונים אבחוניים לדינמיקה כיתתית שלמה (כמו יחידה) — זה בדיוק ה-USP של דניאל שנוצל בפוסט.

**חמישה סימנים ספציפיים:**
1. ישיבה קפואה בהפסקה (2+ שבועות ללא תזוזה בהרכבי קבוצות)
2. שיחות שנעצרות כשמורה נכנסת
3. תלמידים ליחידים או זוגות מבודדים ("קבוצה מבחירה שאין" vs "מכורח")
4. ירידה >40% בהתנדבות לתפקידים חברתיים לעומת השנה הקודמת
5. טון שיחה צייקני עם כינויים מובנים

לכל סימן — מה לחפש הספציפי ואיך למדוד בשטח בתוך שבוע.

**H2 נוסף שלא במבנה המקורי:** הוספתי סעיף "איך רכזת מעבירה את הסימנים למנהל" עם 3 צעדים קונקרטיים (תיעוד 3-שורתי, הצעת מחיר קונקרטית, מדד הצלחה מראש). זה מוסיף ערך פרקטי לרכזת שקוראת ומסביר למה הפוסט הזה שווה יותר מקוראים ברמת "עוד רשימה של סימנים".

**מחירון:** כלול, כולל הבהרת 15 תלמידים לפעילות (חובה).

**קישורים:** 2 פנימיים לדומיין (blog + contact), 0 חיצוניים. הבחירה — לא לקשר לתוצאות חיצוניות שלא באמת מחזקות את הזווית של הפוסט. אם דניאל מעדיף חיצוני — pop.education.gov.il "הקניית מיומנויות חברתיות" הוא המקור המומלץ.

**סיפור אישי:** לא הוטמע. פעם הבאה שדניאל עונה על מייל הזנה של הפוסט הזה — אפשר לחזור לפוסט ולהוסיף פסקה של "דוגמה מהשטח" באחד מחמשת הסימנים, ולעדכן את הטיוטה ב-WP.
