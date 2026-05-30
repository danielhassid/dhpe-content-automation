# Feeding email — drafted but NOT sent (SMTP egress blocked)

**Run date:** 2026-05-30 (יום שבת)
**Mode:** feeding-email
**Target post:** מה הרכז החברתי באמת צריך מפעילות ODT (חודש 1 / שבוע 1 / ראשון, נישה 1)
**Status:** ❌ נחסם — SMTP egress (smtp.gmail.com:465/587/25) חסום בסנדבוקס. אותה תקלה כמו ב-RUN-LOG.md מהריצה הקודמת.

## תוכן המייל שהוכן

**אל:** dh052597@gmail.com
**נושא:** שאלה קצרה לפוסט הבא — מה הרכז החברתי באמת צריך מפעילות ODT

**גוף:**

```
היי דניאל,

ביום ראשון הקרוב עולה הפוסט: מה הרכז החברתי באמת צריך מפעילות ODT

יש לי שאלה אחת קצרה — אם יש לך דקה, תשובה במשפט-שניים תעשה את הפוסט הרבה יותר אמיתי:

---

תזכור לי שיחת תיאום אחרונה עם רכז חברתי שהזמין ODT לכיתה: מה הוא ביקש בדף ההזמנה, ומה הסתבר בפועל באותו יום שהוא באמת היה צריך מהפעילות? איפה הפער הזה צץ?

---

אין חובה לענות. אם לא תגיב עד 07:30 ביום ראשון, הפוסט ייכתב עם האיכות הרגילה — פשוט בלי הסיפור האישי שלך.

DHPE Content System
```

## בדיקות שבוצעו

```
$ python3 smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30)
TimeoutError: timed out

$ timeout 8 bash -c 'cat < /dev/tcp/smtp.gmail.com/465'   → exit 124
$ timeout 8 bash -c 'cat < /dev/tcp/smtp.gmail.com/587'   → exit 124
$ timeout 8 bash -c 'cat < /dev/tcp/smtp.gmail.com/25'    → exit 124
$ timeout 8 curl https://smtp-relay.gmail.com             → 403
$ timeout 8 curl https://gmail.googleapis.com/.../profile → 401 (reachable, but no OAuth token)
```

IPv4-only patch על `socket.getaddrinfo` נוסה — לא פתר. החסימה היא במדיניות ה-egress של הסנדבוקס.

## כדי להריץ ידנית

מסביבה עם גישה ל-smtp.gmail.com:465:

```bash
PYTHONIOENCODING=utf-8 python3 /tmp/send_feeding.py
```

(הסקריפט נשמר ב-`/tmp/send_feeding.py` בריצה זו — אם פג, ניתן לבנות מחדש מהבלוק שלמעלה.)

או — אם רוצים לאפשר לסנדבוקס לשלוח: להוסיף `smtp.gmail.com:465` ל-egress allowlist של ה-environment.
