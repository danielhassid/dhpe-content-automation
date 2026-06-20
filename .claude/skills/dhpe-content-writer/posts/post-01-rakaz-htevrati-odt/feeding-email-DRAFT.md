# Feeding email — drafted but NOT sent (SMTP egress still blocked)

**Run date:** 2026-06-20 (יום שבת, slot 17:00 — לפוסט יום ראשון 2026-06-21)
**Mode:** feeding-email
**Target post:** מה הרכז החברתי באמת צריך מפעילות ODT (חודש 1 / שבוע 1 / ראשון, נישה 1 — ליבה)
**Focus keyword:** ODT לבית ספר / מה רכז חברתי צריך מפעילות ODT
**Angle:** הפער בין הבקשה הראשונית של הרכז/ת ("אנחנו רוצים יום כיף") לצורך האמיתי שמתחת — המקום שבו דניאל שונה מהמתחרים שמדברים שפת גיבוש עובדים ארגוני
**Status:** ❌ נחסם שוב — SMTP egress (smtp.gmail.com:465 / :587 / :25) חסום. אותה חסימה כמו ב-RUN-LOG של post-01 ו-post-02 וב-DRAFTs מ-2026-05-30, 2026-06-02, 2026-06-09, 2026-06-13.

## תוכן המייל שהוכן

**אל:** dh052597@gmail.com
**נושא:** שאלה קצרה לפוסט יום ראשון — מה הרכז החברתי באמת צריך מ-ODT

**גוף:**

```
היי דניאל,

ביום ראשון הקרוב עולה הפוסט: מה הרכז החברתי באמת צריך מפעילות ODT

הזווית: להראות את הפער בין מה שרכזים חברתיים מבקשים בשיחת התיאום הראשונה לבין מה שהם באמת זקוקים לו — וזה בדיוק המקום שבו אתה שונה מהמתחרים שמדברים בשפת גיבוש עובדים ארגוני.

שאלה אחת קצרה — 2-3 משפטים יהפכו את הפוסט מתיאוריה לסיפור אמיתי:

---

תזכור לי שיחת תיאום אחת ספציפית מהשנה האחרונה שבה רכז/ת חברתי/ת פתחה איתך ב"אנחנו רוצים יום כיף" (או ניסוח דומה), ובמהלך השיחה הוצאת ממנה את הצורך האמיתי שמתחת. מה היא ביקשה בהתחלה, איזו שאלה שאלת אותה ששינתה את כיוון השיחה, ומה היא בסוף הבינה שהיא באמת צריכה?

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

Egress probe:
  timeout 10 bash -c 'cat < /dev/tcp/smtp.gmail.com/465' → exit 124
  timeout 10 bash -c 'cat < /dev/tcp/smtp.gmail.com/587' → exit 124
  timeout 10 bash -c 'cat < /dev/tcp/smtp.gmail.com/25'  → exit 124
  timeout 10 bash -c 'cat < /dev/tcp/aspmx.l.google.com/25' → exit 124
```

זהה לחסימה ברמת ה-egress policy של ה-environment.

## פתרון

יש להוסיף `smtp.gmail.com:465` (ועדיף גם `:587`) ל-egress allowlist של ה-environment ב-Settings → Network policy של Claude Code on the web. ראה https://code.claude.com/docs/en/claude-code-on-the-web. עד שזה ייפתר — כל ריצת feeding-email תיחסם.

## הערה לריצה הבאה

אם ה-egress ייפתח, השאלה הזו (הפער בין "יום כיף" לצורך האמיתי בשיחת תיאום קונקרטית) שונה מהווריאציות הקודמות (שדיברו על "רכז/ת ספציפי/ת" באופן כללי). היא יותר ממוקדת ב-call-to-action קונקרטי שדניאל יוכל לענות עליו תוך 2-3 משפטים — בדיוק כפי שתבנית `feeding-email.md` דורשת.
