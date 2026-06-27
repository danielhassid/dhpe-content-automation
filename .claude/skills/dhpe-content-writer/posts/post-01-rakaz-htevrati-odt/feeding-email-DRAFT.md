# Feeding email — drafted but NOT sent (SMTP egress still blocked)

**Run date:** 2026-06-27 (יום שבת, slot 17:00 — לפוסט יום ראשון 2026-06-28)
**Mode:** feeding-email
**Target post:** מה הרכז החברתי באמת צריך מפעילות ODT (חודש 1 / שבוע 1 / ראשון, נישה 1 — ליבה)
**Focus keyword:** ODT לבית ספר / מה רכז חברתי צריך מפעילות ODT
**Angle:** הפער בין הבקשה הראשונית של הרכז/ת ("רוצים יום כיף", "צריך גיבוש", "תביא משחקים") לצורך האמיתי שמתחת — המקום שבו דניאל שונה מהמתחרים שמדברים שפת גיבוש עובדים ארגוני
**Status:** ❌ נחסם שוב — SMTP egress (smtp.gmail.com:465 / :587) חסום. אותה חסימה כמו בכל הריצות מאז 2026-04-29. ה-agent proxy תומך רק ב-HTTPS/443 (`/root/.ccr/README.md` → "Not supported through the proxy: ... non-443 HTTPS ports, raw-TCP databases").

## תוכן המייל שהוכן

**אל:** dh052597@gmail.com
**נושא:** שאלה קצרה לפוסט הבא — מה הרכז החברתי באמת צריך מ-ODT

**גוף:**

```
היי דניאל,

ביום ראשון הקרוב עולה הפוסט: **מה הרכז החברתי באמת צריך מפעילות ODT**

יש לי שאלה אחת קצרה — אם יש לך דקה, תשובה במשפט-שניים תעשה את הפוסט הרבה יותר אמיתי:

---

תזכר במקרה ספציפי שרכז חברתי פנה אליך עם בקשה אחת ("רוצה משהו כיפי לכיתה ז'2", "צריך יום גיבוש", "תביא משחקים"), ותוך כדי השיחה גילית שמה שהוא באמת צריך זה משהו אחר לגמרי. מה הוא ביקש בהתחלה, מה הבנת שהוא באמת צריך מתחת לפני השטח, ואיך זה שינה את הפעילות שבניתם בסוף?

---

אין חובה לענות. אם לא תגיב עד 07:30 ביום ראשון, הפוסט ייכתב עם האיכות הרגילה — פשוט בלי הסיפור האישי שלך.

DHPE Content System
```

## בדיקות שבוצעו בריצה הזו

```
Attempt 1 — smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30), default getaddrinfo:
  OSError: [Errno 97] Address family not supported by protocol

Attempt 2 — smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30), AF_INET only:
  TimeoutError: timed out

Attempt 3 — smtplib.SMTP('smtp.gmail.com', 587, timeout=60) + STARTTLS:
  TimeoutError: timed out

Attempt 4 — HTTP CONNECT tunnel דרך ה-agent proxy אל smtp.gmail.com:587:
  ה-CONNECT הצליח (HTTP/1.1 200), אך ה-SMTP greeting לא הגיע — ה-upstream policy חוסם את ה-relay.

Egress probe:
  nc -zvw 10 smtp.gmail.com 587 → connect timed out
  nc -zvw 10 smtp.gmail.com 465 → connect timed out

agent-proxy status: recentRelayFailures: []  (CONNECTים לא נרשמים כ-relay failures)
```

## פתרון

יש להוסיף `smtp.gmail.com:465` (ועדיף גם `:587`) ל-egress allowlist של ה-environment ב-Settings → Network policy של Claude Code on the web, **או** להחליף את ה-iron rule "Email MUST land in Inbox via SMTP" במסלול Gmail API דרך HTTPS (כלי MCP מתאים, או OAuth ידני). ראה https://code.claude.com/docs/en/claude-code-on-the-web. עד שזה ייפתר — כל ריצת feeding-email תיחסם.

## הערה לריצה הבאה

השאלה הזו (פער בין בקשה ראשונית של רכז ל"מה הוא באמת צריך מתחת לפני השטח") קרובה לווריאציה מ-2026-06-20 ("יום כיף → צורך אמיתי") אבל פתוחה יותר לסוגי בקשות שונים ולכן צפויה לעורר זיכרון של מקרה אחר. אם ה-egress ייפתח לפני 07:30 ביום ראשון 2026-06-28 — לשלוח כפי שהיא.
