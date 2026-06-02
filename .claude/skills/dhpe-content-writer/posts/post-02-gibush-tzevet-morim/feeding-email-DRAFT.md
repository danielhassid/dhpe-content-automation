# Feeding email — drafted but NOT sent (SMTP egress blocked)

**Run date:** 2026-06-02 (יום שלישי, 17:00 slot)
**Mode:** feeding-email
**Target post:** גיבוש צוות מורים בתחילת שנת הלימודים (חודש 1 / שבוע 1 / רביעי, נישה 2 — צוות מורים)
**Focus keyword:** גיבוש צוות מורים
**Status:** ❌ נחסם — SMTP egress (smtp.gmail.com:465/587/25) חסום בסנדבוקס. אותה תקלה כמו ב-post-01 RUN-LOG.

## תוכן המייל שהוכן

**אל:** dh052597@gmail.com
**נושא:** שאלה קצרה לפוסט הבא — גיבוש צוות מורים בתחילת שנת הלימודים

**גוף:**

```
היי דניאל,

ביום רביעי הקרוב עולה הפוסט: גיבוש צוות מורים בתחילת שנת הלימודים

יש לי שאלה אחת קצרה — אם יש לך דקה, תשובה במשפט-שניים תעשה את הפוסט הרבה יותר אמיתי:

---

תזכור לי יום גיבוש למורים שהובלת ממש בפתיחת שנה — מה היה המתח שהמנהל/ת שיתפ/ה איתך בשיחת התיאום (מורים חדשים שצריך לחבר לוותיקים, צוות שיצא משנה קשה, חילוקי דעות פדגוגיים פנימיים), ומה היה הרגע באותו יום שבו ראית שמשהו בצוות באמת זז?

---

אין חובה לענות. אם לא תגיב עד 07:30 ביום רביעי, הפוסט ייכתב עם האיכות הרגילה — פשוט בלי הסיפור האישי שלך.

DHPE Content System
```

## בדיקות שבוצעו בריצה הזו

```
Attempt 1 (default getaddrinfo, AF_UNSPEC):
  OSError: [Errno 97] Address family not supported by protocol
  (סנדבוקס לא תומך ב-IPv6; getaddrinfo החזיר תוצאות IPv6 ראשונות.)

Attempt 2 (monkey-patched getaddrinfo → AF_INET only):
  TimeoutError: timed out

Egress probe:
  timeout 8 bash -c 'cat < /dev/tcp/smtp.gmail.com/465' → exit 124
  timeout 8 bash -c 'cat < /dev/tcp/smtp.gmail.com/587' → exit 124
  timeout 8 bash -c 'cat < /dev/tcp/smtp.gmail.com/25'  → exit 124
```

החסימה היא ברמת ה-egress policy של ה-environment — אותו ממצא כמו ב-post-01.

## כדי לשלוח ידנית מסביבה עם גישה

```bash
PYTHONIOENCODING=utf-8 python3 /tmp/send_feeding.py
```

(הסקריפט כולל את ה-IPv4-patch ושמור ב-`/tmp/send_feeding.py` בריצה זו.)

## פתרון מתמשך

יש להוסיף `smtp.gmail.com:465` ל-egress allowlist של ה-environment ב-`https://code.claude.com/docs/en/claude-code-on-the-web` (Settings → Network policy), אחרת כל ריצה של feeding-email תיחסם.
