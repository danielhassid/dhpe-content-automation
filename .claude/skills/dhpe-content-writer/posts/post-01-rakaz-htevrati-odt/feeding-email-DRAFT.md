# Feeding email — drafted but NOT sent (SMTP egress still blocked)

**Run date:** 2026-06-30 (יום שלישי, 17:00 slot)
**Mode:** feeding-email (routine)
**Target post:** מה הרכז החברתי באמת צריך מפעילות ODT (חודש 1 / שבוע 1 / ראשון, נישה 1 — ליבה)
**Focus keyword:** רכז חברתי ODT
**Angle:** שלוש שכבות הצורך של הרכז/ת החברתי/ת — מתחת לבקשה הגלויה ("יום כיף", "גיבוש", "משחקים"). הנקודה שמבדילה את DHPE ממתחרים שמדברים בשפת גיבוש עובדים ארגוני.
**Status:** ❌ נחסם שוב — אותה חסימת SMTP egress כמו בריצות 2026-04-29 / 05-30 / 06-02 / 06-09 / 06-13 / 06-20 / 06-23 / 06-27. הריצה הזו היא ה-8th draft ברצף.

## תוכן המייל שהוכן

**אל:** dh052597@gmail.com
**נושא:** שאלה קצרה לפוסט הבא — מה הרכז החברתי באמת צריך מ-ODT

**גוף:**

```
היי דניאל,

ביום ראשון הקרוב עולה הפוסט: מה הרכז החברתי באמת צריך מפעילות ODT

הזווית של הפוסט: לפענח את שלוש שכבות הצורך של הרכז/ת החברתי/ת — מתחת לבקשה הגלויה ("יום כיף", "גיבוש", "משחקים"). זה בדיוק המקום שמבדיל אותך מהמתחרים שמדברים שפת גיבוש עובדים ארגוני.

יש לי שאלה אחת קצרה — 2-3 משפטים יהפכו את הפוסט מתיאוריה לסיפור שמרגיש אמיתי:

---

תזכר ברכז/ת חברתי/ת ספציפי/ת שבסוף יום ה-ODT ניגש/ה אליך עם משפט שגרם לך להבין שמה שהוא/היא קיבל/ה מהיום היה משהו שלא ביקש/ה מראש — לא התלמידים, אלא הוא/היא עצמו/ה. מה הוא/היא אמר/ה, ומה זה לימד אותך על מה שרכז חברתי באמת מחפש כשהוא מזמין ODT — גם אם הוא לא יודע לנסח את זה בהזמנה?

---

אין חובה לענות. אם לא תגיב עד 07:30 ביום ראשון, הפוסט ייכתב עם האיכות הרגילה — פשוט בלי הסיפור האישי שלך.

DHPE Content System
```

## בדיקות שבוצעו בריצה הזו

```
Attempt 1 — smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30), default getaddrinfo:
  OSError: [Errno 97] Address family not supported by protocol
  (אותה תקלת IPv6 כמו בכל ריצה קודמת.)

Attempt 2 — smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=60) + getaddrinfo monkey-patched ל-AF_INET only:
  TimeoutError: timed out

Egress probe (raw TCP):
  timeout 8 bash -c 'cat < /dev/tcp/smtp.gmail.com/465' → Terminated (exit 143)
  timeout 8 bash -c 'cat < /dev/tcp/smtp.gmail.com/587' → Terminated (exit 143)

Proxy status:
  /root/.ccr/README.md → "Not supported through the proxy ... non-443 HTTPS ports, raw-TCP databases."
  curl $HTTPS_PROXY/__agentproxy/status → enabled:true, recentRelayFailures:[]
```

החסימה היא ברמת ה-egress policy של ה-environment ולא ניתן לעקוף אותה דרך ה-agent proxy (הוא תומך רק ב-HTTPS/443).

## הזווית של השאלה הזו לעומת ה-DRAFTs הקודמים

- 2026-06-27 (DRAFT 7): גילוי הצורך האמיתי **בשיחת תיאום ראשונית** — פער בין בקשה גלויה לצורך נסתר.
- 2026-06-20 (DRAFT 6): "יום כיף" → צורך אמיתי, כללי.
- 2026-06-13 / 06-09 / 06-02 / 05-30: ווריאציות נוספות על אותו ציר.
- **2026-06-30 (DRAFT 8 — זה):** מעבר מ"רגע המכירה" ל**רגע סיום היום** — מה הרכז עצמו/ה לקח/ה מהיום, לאו דווקא התלמידים. זה פותח לדניאל זיכרון מסוג אחר (סוף-יום במקום שיחת-תיאום), ומחזק את אנגל הפוסט: ה-ODT לא רק משרת את התלמידים — הוא משרת את הרכז כפוזיציה מקצועית.

אם ה-egress ייפתח לפני 07:30 ביום ראשון 2026-07-05 — לשלוח כפי שהיא.

## פתרון מתמשך (חוזר על עצמו בשמיני ריצות)

יש להוסיף `smtp.gmail.com:465` (ועדיף גם `:587`) ל-egress allowlist של ה-environment ב-Settings → Network policy של Claude Code on the web (https://code.claude.com/docs/en/claude-code-on-the-web), **או** להחליף את ה-iron rule "Email MUST land in Inbox via SMTP" במסלול Gmail HTTPS API (messages.send דרך OAuth). עד שאחד מהם יקרה — כל ריצת feeding-email תיחסם.
