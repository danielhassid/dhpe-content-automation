# Run log — Post 01

**Date:** 2026-04-29 (יום ראשון)
**Mode:** write-and-publish
**Operator:** Claude Code (Opus 4.7) running in sandboxed harness

## Outcomes

| שלב | סטטוס |
|---|---|
| 1. בחירת פוסט הבא מהתוכנית | ✅ נבחר: "מה הרכז החברתי באמת צריך מפעילות ODT" (חודש 1 / שבוע 1 / ראשון) |
| 2. אימות שלא פורסם בוורדפרס | ⚠️ חסום — ה-host www.dhpe.co.il לא ב-egress allowlist של הסנדבוקס |
| 3. חיפוש תשובת דניאל בג'ימייל | ✅ אין תשובה — רק מייל ההזנה היוצא מה-26.4 |
| 4. WebSearch + ניתוח תחרות | ✅ זוהה פער תוכן: אף תוצאה מובילה לא מדברת בשפת הרכז החברתי |
| 5. כתיבת פוסט 1500-2000 מילים | ✅ 1533 מילים, עברית, ללא סיפור אישי |
| 6. חבילת SEO | ✅ Meta/OG/Twitter/Slug/FAQ schema |
| 7. העלאה כטיוטה לוורדפרס | ❌ חסום (HTTP 403 host_not_allowed) |
| 8. שליחת מייל התראה ב-SMTP | ❌ חסום (TCP timeout ל-smtp.gmail.com:465 ו-:587) |
| 9. עדכון תוכנית פוסטים | ⚠️ נשאר pending — לא בוצעה העלאה אמיתית |

## Network blockers (מילולית)

```
$ curl -s -u '...' -X POST 'https://www.dhpe.co.il/wp-json/wp/v2/posts' -d @wp-payload.json
HTTP=403
< x-deny-reason: host_not_allowed
Host not in allowlist
```

```
$ python3 smtplib.SMTP_SSL('smtp.gmail.com', 465)
SMTP_FAIL: OSError [Errno 97] Address family not supported by protocol
TCP probe (IPv4): smtp.gmail.com:465 timed out
TCP probe (IPv4): smtp.gmail.com:587 timed out
```

## מה דרוש כדי לסיים את הריצה הזו

אופציה א — להריץ את הסקיל מסביבה ללא חסימת egress:
1. `cd /path/to/dhpe-content-automation` (עם הקבצים מהקומיט הזה)
2. הרצת הפקודה המוכנה:
   ```bash
   curl -u 'dh052597@gmail.com:6fZA HCsa nTIw rFYh JQnL PU42' \
     -X POST 'https://www.dhpe.co.il/wp-json/wp/v2/posts' \
     -H 'Content-Type: application/json; charset=utf-8' \
     --data-binary @.claude/skills/dhpe-content-writer/posts/post-01-rakaz-htevrati-odt/wp-payload.json
   ```
   קח את ה-`id` שחוזר.
3. החלף `__POST_ID__` ב-`notification-email.md` ב-ID האמיתי, והרץ את סקריפט ה-SMTP מהסעיף 8 בהוראות המקוריות.
4. עדכן את `content-plan/24-posts-plan.md` (שורת "חודש 1 שבוע 1 ראשון") מ-`pending` ל-`draft-ready`.

אופציה ב — להוסיף את `www.dhpe.co.il` ו-`smtp.gmail.com` ל-allowlist של הסנדבוקס שמפעיל את Claude Code, ולהריץ את הסקיל שוב.
