# Feeding email — drafted but NOT sent (SMTP egress still blocked)

**Run date:** 2026-08-01 (יום שבת, 17:00 slot)
**Mode:** feeding-email (routine)
**Target post:** מה הרכז החברתי באמת צריך מפעילות ODT (חודש 1 / שבוע 1 / ראשון, נישה 1 — ליבה)
**Focus keyword:** רכז חברתי ODT
**Angle:** הרגע שבו הרכז/ת מוסר/ת לך את הכיתה — התנוחה, המשפט הפותח, הפרט הקטן שמסגיר מה הוא/היא באמת רוצה מהיום. הזווית שמבדילה את DHPE ממתחרים שמדברים שפת גיבוש עובדים ארגוני.
**Status:** ❌ נחסם שוב — אותה חסימת SMTP egress כמו בכל הריצות מאז 2026-04-29. הריצה הזו היא ה-9th draft ברצף לפוסט הזה, ואף מייל הזנה לא הגיע לתיבה של דניאל.

## תוכן המייל שהוכן

**אל:** dh052597@gmail.com
**נושא:** שאלה קצרה לפוסט הבא — מה הרכז החברתי באמת צריך מ-ODT

**גוף:**

```
היי דניאל,

ביום ראשון הקרוב עולה הפוסט: מה הרכז החברתי באמת צריך מפעילות ODT

הזווית של הפוסט: הפער בין מה שהרכז/ת החברתי/ת מבקש/ת בטלפון לבין מה שהוא/היא באמת צריך/ה — הפער שמתחרים שמדברים שפת גיבוש עובדים ארגוני מפספסים לגמרי.

יש לי שאלה אחת קצרה — 2-3 משפטים יהפכו את הפוסט מתיאוריה לסיפור שמרגיש אמיתי:

---

תזכר ברכז/ת חברתי/ת שמסר/ה לך את הכיתה בבוקר יום ה-ODT — הרגע הראשון של המפגש, עוד לפני שהתחלתם. מה הוא/היא אמר/ה לך? האם היה שם משפט קטן, תנועה, או בקשה בצד ("רק שים לב ל…", "אל תעשה איתם…", "אני צריכה שהיום…") שגילה לך שההזמנה שקיבלת בטלפון הייתה רק שכבה אחת — ומה השכבה האמיתית שהתגלתה באותו רגע מסירה?

---

אין חובה לענות. אם לא תגיב עד 07:30 ביום ראשון, הפוסט ייכתב עם האיכות הרגילה — פשוט בלי הסיפור האישי שלך.

DHPE Content System
```

## בדיקות שבוצעו בריצה הזו

```
Attempt 1 — smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30), default getaddrinfo:
  OSError: [Errno 97] Address family not supported by protocol
  (IPv6 unavailable — אותה תקלה כמו בכל ריצה קודמת.)

Attempt 2 — smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30) + getaddrinfo monkey-patched ל-AF_INET only:
  TimeoutError: timed out

Egress probes (raw TCP, IPv4, 30s timeout):
  timeout 30 bash -c 'exec 3<>/dev/tcp/smtp.gmail.com/465' → exit 124 (timed out)
  timeout 30 bash -c 'exec 3<>/dev/tcp/smtp.gmail.com/587' → exit 124 (timed out)
  timeout 30 bash -c 'exec 3<>/dev/tcp/smtp.gmail.com/25'  → exit 124 (timed out)

Proxy check:
  curl $HTTPS_PROXY/__agentproxy/status → enabled:true, recentRelayFailures:[]
  /root/.ccr/README.md → "Not supported through the proxy ... non-443 HTTPS ports, raw-TCP databases."
```

החסימה היא ברמת ה-egress policy של ה-environment ולא ניתן לעקוף אותה דרך ה-agent proxy (הוא תומך רק ב-HTTPS/443).

## היסטוריית זוויות (DRAFT 1→9 לאותו פוסט)

- DRAFT 1-5 (2026-04-29 → 06-13): ווריאציות על "יום כיף → צורך אמיתי", כלליות.
- DRAFT 6 (2026-06-20): "יום כיף" → צורך אמיתי, נוסח יותר חד.
- DRAFT 7 (2026-06-27): גילוי הצורך האמיתי **בשיחת תיאום ראשונית** — פער בין בקשה גלויה לצורך נסתר.
- DRAFT 8 (2026-06-30): מעבר מ"רגע המכירה" ל**רגע סיום היום** — מה הרכז עצמו/ה לקח/ה מהיום.
- **DRAFT 9 (2026-08-01 — זה):** מעבר ל**רגע מסירת הכיתה בבוקר** — המשפט הצדדי, הבקשה השקטה, התנוחה של הרכז/ת ברגע שהוא/היא מוסר/ת את הכיתה לספק. זווית שלישית שפותחת לדניאל זיכרון חדש (לא שיחת-תיאום, לא סיום-יום, אלא רגע ההעברה) ומחזקת את הפער בין ההזמנה הרשמית להזמנה הסמויה.

## פתרון מתמשך (חוזר על עצמו ב-9 ריצות)

יש להוסיף `smtp.gmail.com:465` (ועדיף גם `:587`) ל-egress allowlist של ה-environment ב-Settings → Network policy של Claude Code on the web (https://code.claude.com/docs/en/claude-code-on-the-web), **או** להחליף את ה-iron rule "Email MUST land in Inbox via SMTP" במסלול Gmail HTTPS API (messages.send דרך OAuth) שיעבור בפרוקסי ה-443 הקיים. עד שאחד מהם יקרה — כל ריצת feeding-email תיחסם, ופוסט 01 יישאר תקוע ב-pending לצמיתות (כבר יותר מ-3 חודשים).
