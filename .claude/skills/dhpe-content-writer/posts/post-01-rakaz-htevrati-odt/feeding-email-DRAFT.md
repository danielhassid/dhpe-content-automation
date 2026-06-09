# Feeding email — drafted but NOT sent (SMTP egress blocked)

**Run date:** 2026-06-09 (יום שלישי, slot 17:00 — לפוסט ראשון של חודש 1 שבוע 1 שעדיין pending)
**Mode:** feeding-email
**Target post:** מה הרכז החברתי באמת צריך מפעילות ODT (חודש 1 / שבוע 1 / ראשון, נישה 1 — ליבה)
**Focus keyword:** ODT לבית ספר / מה רכז חברתי צריך מפעילות ODT
**Angle:** מציג את ה-ODT דרך עיני הרכז/ת החברתי/ת — מה הם באמת מבקשים מהיום, מה הצורך מתחת לבקשה
**Status:** ❌ נחסם — SMTP egress (smtp.gmail.com:465 ו-:587) חסום בסנדבוקס. אותה תקלה כמו ב-RUN-LOG מהריצה הקודמת ומה-DRAFT של 2026-05-30.

## תוכן המייל שהוכן

**אל:** dh052597@gmail.com
**נושא:** שאלה קצרה לפוסט הבא — מה הרכז החברתי באמת צריך מפעילות ODT

**גוף:**

```
היי דניאל,

ביום ראשון הקרוב עולה הפוסט: מה הרכז החברתי באמת צריך מפעילות ODT

יש לי שאלה אחת קצרה — אם יש לך דקה, תשובה במשפט-שניים תעשה את הפוסט הרבה יותר אמיתי:

---

תזכר ברכז/ת חברתי/ת ספציפי/ת שפנו אליך לקראת יום ODT, ובמהלך שיחת התיאום הבנת שמה שהם באמת צריכים זה לא מה שהם ביקשו בהתחלה. מה הם אמרו בהתחלה שהם רוצים מהיום, ומה גילית בפועל שהם היו צריכים?

---

אין חובה לענות. אם לא תגיב עד 07:30 ביום ראשון, הפוסט ייכתב עם האיכות הרגילה — פשוט בלי הסיפור האישי שלך.

DHPE Content System
```

## בדיקות שבוצעו בריצה הזו

```
Attempt 1 — smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30), default getaddrinfo:
  OSError: [Errno 97] Address family not supported by protocol
  (סנדבוקס לא תומך ב-IPv6; getaddrinfo החזיר תוצאות IPv6 ראשונות.)

Attempt 2 — smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30), monkey-patched getaddrinfo → AF_INET only:
  TimeoutError: timed out

Attempt 3 — smtplib.SMTP('smtp.gmail.com', 587) + STARTTLS, AF_INET only:
  TimeoutError: timed out

Egress probes:
  curl -m 8 telnet://smtp.gmail.com:587 → "Connection timed out after 8002 ms"
  curl -m 8 telnet://smtp.gmail.com:465 → "Connection timed out after 8002 ms"
  curl -m 10 https://gmail.googleapis.com → HTTP 404 (יציאה 443 פתוחה, ה-API בהישג יד דרך HTTPS)
```

החסימה היא ברמת ה-egress policy של ה-environment — TCP אל יציאות SMTP (25/465/587) חסום. רק HTTPS (443) פתוח החוצה.

## כדי לשלוח ידנית מסביבה עם גישה

```bash
PYTHONIOENCODING=utf-8 python3 /tmp/send_feeding.py
```

(הסקריפט עם monkey-patch ל-IPv4 שמור ב-`/tmp/send_feeding.py` בריצה זו; ה-credentials: dh052597@gmail.com + app password.)

## פתרון מתמשך

יש להוסיף `smtp.gmail.com:465` (או :587) ל-egress allowlist של ה-environment ב-Settings → Network policy של Claude Code on the web. חלופה: לעבור ל-Gmail API ב-HTTPS — אבל זה דורש OAuth2 access token במקום app password (לא יעבוד עם המפתח הנוכחי).
