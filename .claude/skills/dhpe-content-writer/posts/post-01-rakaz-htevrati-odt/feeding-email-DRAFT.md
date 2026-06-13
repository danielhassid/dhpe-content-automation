# Feeding email — drafted but NOT sent (SMTP egress still blocked)

**Run date:** 2026-06-13 (יום שבת, slot 17:00 — לפוסט יום ראשון 2026-06-14)
**Mode:** feeding-email
**Target post:** מה הרכז החברתי באמת צריך מפעילות ODT (חודש 1 / שבוע 1 / ראשון, נישה 1 — ליבה)
**Focus keyword:** ODT לבית ספר / מה רכז חברתי צריך מפעילות ODT
**Angle:** הפער בין הבקשה ("אנחנו רוצים יום כיף") לצורך האמיתי של הרכז/ת החברתי/ת
**Status:** ❌ נחסם שוב — SMTP egress (smtp.gmail.com:465) חסום. אותה חסימה כמו ב-RUN-LOG של post-01 ושל post-02, ו-DRAFTs מ-2026-05-30, 2026-06-02, 2026-06-09.

## תוכן המייל שהוכן

**אל:** dh052597@gmail.com
**נושא:** שאלה קצרה לפוסט יום ראשון — מה הרכז החברתי באמת צריך מ-ODT

**גוף:**

```
היי דניאל,

ביום ראשון הקרוב עולה הפוסט: מה הרכז החברתי באמת צריך מפעילות ODT

זווית הפוסט: להראות שמה שרכזים חברתיים מבקשים בשיחת התיאום הוא לרוב לא מה שהם באמת זקוקים לו — וזה בדיוק היתרון שלך מול המתחרים שמדברים בשפת גיבוש עובדים ארגוני.

יש לי שאלה אחת קצרה — תשובה של 2-3 משפטים תהפוך את הפוסט למשהו אמיתי במקום עוד תיאוריה:

---

זכור לי רכז/ת חברתי/ת אחד/ת ספציפי/ת שעבדת איתה בשנה האחרונה — מה היא ביקשה ממך בשיחת התיאום הראשונה (במילים שלה: "אנחנו רוצים..."), ומה היא אמרה לך אחרי היום שזה היה לה הכי חשוב שקרה? אני רוצה להציג בפוסט בדיוק את הפער הזה — בין הבקשה לצורך האמיתי.

---

אין חובה לענות. אם לא תגיב עד 07:30 ביום ראשון, הפוסט ייכתב עם האיכות הרגילה — פשוט בלי הסיפור האישי שלך.

DHPE Content System
```

## בדיקות שבוצעו בריצה הזו

```
Attempt 1 — smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30), default getaddrinfo:
  OSError: [Errno 97] Address family not supported by protocol
  (סנדבוקס לא תומך ב-IPv6.)

Attempt 2 — smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30), monkey-patched getaddrinfo → AF_INET only:
  TimeoutError: timed out
```

זהה לחסימה ברמת ה-egress policy של ה-environment.

## פתרון

יש להוסיף `smtp.gmail.com:465` ל-egress allowlist של ה-environment ב-Settings → Network policy של Claude Code on the web. ראה https://code.claude.com/docs/en/claude-code-on-the-web. עד שזה ייפתר — כל ריצת feeding-email תיחסם.
