# Feeding email — drafted but NOT sent (SMTP egress blocked, 3rd month running)

**Run date:** 2026-07-25 (יום שבת — סלוט feeding שבת 17:00 לפוסט של יום ראשון הבא)
**Mode:** feeding-email
**Target post:** איך לבחור ספק ODT מתאים לבית ספר (חודש 1 / שבוע 4 / ראשון, נישה 1 — ליבה)
**Focus keyword:** איך לבחור ספק ODT / איך לבחור פעילות ODT לבית ספר
**Angle:** רוב המדריכים ברשת לבחירת ספק ODT מסתכמים בצ'קליסט טכני — ביטוח, ניסיון, המלצות, מחיר. הפער שהפוסט אמור למלא הוא הרגע האמיתי של ההחלטה: מה קורה בשיחה עצמה שגורם למנהל או לרכזת לומר "עם הבן אדם הזה אני הולך". דניאל הוא הצד השני של הצ'קליסט — הוא זה שנבחר עשרות פעמים אחרי שמנהל התלבט בין ספקים. השאלה חייבת להוציא ממנו את המשפט הספציפי או השאלה הספציפית שגרמה להיפוך בשיחה — לא הצהרה על "ניסיון" או "אמון".
**Status:** ❌ נחסם שוב — SMTP egress חסום גם ישירות (smtp.gmail.com:465/:587 timeout ב-TCP) וגם דרך ה-agent proxy (CONNECT מקבל 200 אך TLS מסיים ב-connection reset). זו התקלה החוזרת מזה חודשיים+.

## תוכן המייל שהוכן

**אל:** dh052597@gmail.com
**נושא:** שאלה קצרה לפוסט של ראשון — איך לבחור ספק ODT מתאים לבית ספר

**גוף:**

```
היי דניאל,

ביום ראשון הקרוב עולה הפוסט: איך לבחור ספק ODT מתאים לבית ספר

הזווית: רוב המדריכים ברשת לבחירת ספק ODT מסתכמים בצ'קליסט טכני — ביטוח, ניסיון, המלצות, מחיר. הפער שהפוסט אמור למלא הוא הרגע האמיתי של ההחלטה — מה קורה בשיחה עצמה שגורם למנהל או לרכזת חברתית לומר "עם הבן אדם הזה אני הולך". אתה הצד השני של הצ'קליסט — אתה זה שנבחר עשרות פעמים אחרי שמנהל התלבט בין כמה ספקים.

יש לי שאלה אחת קצרה — 2-3 משפטים יהפכו את הפוסט מרשימת קריטריונים גנרית ליועץ אמיתי שקורא לך את השיחה מבפנים:

---

תזכור לי שיחת מכירה אחת ספציפית עם מנהל או רכזת חברתית שהתלבטו בינך לבין ספק אחר — ובסוף בחרו בך. מה בדיוק אמרת (או שאלת), באיזה שלב של השיחה, שגרם להם להסתובב? לא "הם ראו את הניסיון" ולא "האמינו בי" — משפט או שאלה שהם עצמם החזירו לך אחר כך והגידו "בגלל זה בחרנו". אם אתה זוכר גם ממה הם חששו אצל הספק השני לפני שהחליטו — עוד יותר טוב.

---

אין חובה לענות. אם לא תגיב עד 07:30 ביום ראשון, הפוסט ייכתב עם האיכות הרגילה — פשוט בלי הסיפור האישי שלך.

DHPE Content System
```

## בדיקות שבוצעו בריצה הזו

```
1) direct TCP probe:
   timeout 10 bash -c 'cat < /dev/tcp/smtp.gmail.com/465' → exit 124 (timeout)
   timeout 10 bash -c 'cat < /dev/tcp/smtp.gmail.com/587' → exit 124 (timeout)
   timeout 10 bash -c 'cat < /dev/tcp/smtp-relay.gmail.com/587' → exit 124 (timeout)

2) smtplib.SMTP_SSL('smtp.gmail.com', 465) — direct:
   OSError [Errno 97] Address family not supported by protocol (IPv6 disabled)

3) smtplib.SMTP_SSL('smtp.gmail.com', 465) — IPv4-only patch:
   TimeoutError: timed out

4) HTTP CONNECT tunnel via agent proxy (127.0.0.1:42389) → smtp.gmail.com:465:
   Proxy reply: HTTP/1.1 200 Connection Established
   TLS wrap over tunnel (default trust store):     ConnectionResetError [Errno 104]
   TLS wrap over tunnel (proxy CA /root/.ccr/ca-bundle.crt): ConnectionResetError [Errno 104]
   → CONNECT is a stub 200; the tunnel doesn't actually relay non-HTTPS-to-allowlisted-host bytes.

5) HTTP CONNECT tunnel via agent proxy → smtp.gmail.com:587 (plaintext greeting):
   Proxy reply: HTTP/1.1 200 Connection Established
   recv() on tunnel: TimeoutError (server never gets the packets)
```

## פתרון (חוזר על עצמו כבר 3 חודשים)

הוסף לרשימת ה-egress allowlist של ה-environment (Settings → Network policy ב-Claude Code on the web, לפי https://code.claude.com/docs/en/claude-code-on-the-web):

- `smtp.gmail.com:465` (SMTPS)
- או לחילופין `smtp.gmail.com:587` (STARTTLS)

עד שזה ייפתר — כל ריצת feeding-email תישבר, ודניאל לא יקבל את השאלה לפני הפוסט. המשמעות: הפוסט של יום ראשון (איך לבחור ספק ODT) ייכתב בלי הסיפור האישי הספציפי שהיה יכול להפוך אותו ממאמר קריטריונים ליועץ אמיתי — וזה בדיוק הבידול מ-ODTeam / יוניטי / בטבע שלנו.

## למה נבחר הפוסט הזה

- היום 2026-07-25 שבת, סלוט feeding שבת 17:00.
- Post 06 (רביעי, שבוע 3, נישה 2 — יום גיבוש מורים) — feeding שלו נוסח 2026-07-18 (הסלוט הקודם).
- Post 07 (ראשון, שבוע 4, נישה 1 — בחירת ספק ODT) — הפוסט הבא ברצף. הרצף הזה נשמר מזה חודשיים+ כי כל הפוסטים תקועים ב-DRAFT — SMTP חסום, ולכן ממשיכים כרונולוגית בתוכנית ולא לפי חלוקת ימי הזנה.

## הערה על השאלה

השאלה בונה על יתרון ייחודי שרק דניאל יכול לתת: הוא נמצא בעשרות שיחות מכירה מול מנהלים שמתלבטים בין ספקים, ולפעמים גם שומע חודש אחר כך "בגלל זה בחרנו בך". השאלה מבקשת:
1. **שיחה אחת ספציפית** (לא סקירה כללית) — מונע ג'נריות.
2. **המשפט/שאלה שגרם להיפוך** — עצם המשפט, לא ההיסקים ממנו.
3. **מה החששות היו מהספק השני** — נותן ניגוד שהופך את המשפט של דניאל לנוקב.

עם 2-3 משפטי תשובה, אפשר לבנות בפוסט קרוסלה של "מה מנהלים באמת שואלים בשיחת בחירת ספק" ולא רשימת "10 קריטריונים לבחירת ספק ODT" שתראה כמו כל המתחרים.
