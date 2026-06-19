# 📋 Setup Guide — הקמה חד-פעמית צעד-צעד

> בצע **לפי הסדר**. סמן ✅ כל שלב. בלי זה ה-pipeline לא ירוץ.
> ⚠️ סודות (tokens) נשמרים כ-env vars / Routine secrets — **לעולם לא בגיט.**

---

## שלב 1 — ערוץ יוטיוב + פלייליסטים

1. ב-[youtube.com](https://youtube.com) → צור ערוץ (מומלץ Brand Account נפרד).
2. שם מוצע: משהו עם "Pip" + Nature/Kids (למשל "Pip's Nature World").
3. תמונת פרופיל = Pip; באנר טבעי בהיר.
4. צור 4 פלייליסטים: **Animals**, **Ocean & Sea**, **Nature Facts (Shorts)**, **New Videos**.
5. **Settings → Channel → Advanced → "Set channel as made for kids".**
6. שמור את ה-IDs של הערוץ והפלייליסטים ב-`knowledge/credentials-guide.md`.

## שלב 2 — Google Cloud Console

1. [console.cloud.google.com](https://console.cloud.google.com) → צור פרויקט חדש.
2. **APIs & Services → Enable APIs**: הפעל
   - YouTube Data API v3
   - YouTube Analytics API
3. **OAuth consent screen**: External, מלא פרטים, הוסף את עצמך כ-Test user.
4. **Credentials → Create Credentials → OAuth client ID** → סוג "Desktop app".
5. שמור את ה-Client ID וה-Client Secret (לא בגיט!).

## שלב 3 — OAuth → Refresh Token (חד-פעמי)

1. השתמש ב-OAuth Playground או סקריפט מקומי עם scopes:
   `https://www.googleapis.com/auth/youtube.upload` +
   `https://www.googleapis.com/auth/youtube`
2. השלם את ה-consent → קבל **refresh token**.
3. שמור כ-env vars (ב-Claude.ai Routine secrets):
   - `YOUTUBE_CLIENT_ID`
   - `YOUTUBE_CLIENT_SECRET`
   - `YOUTUBE_REFRESH_TOKEN`

## שלב 4 — Higgsfield: דמות Pip + קול

1. הפעל `generate_image` עם תיאור ה-reference מ-`knowledge/brand-voice.md`.
2. בחר את התוצאה הטובה ביותר → שמור את ה-**asset ID** ב-`brand-voice.md` ו-`credentials-guide.md`.
3. הפעל `list_voices` → בחר קול חם/ברור/איטי → שמור **voice ID** ב-`brand-voice.md`.
4. (אופציונלי) בחר/הכן מוזיקת רקע אינסטרומנטלית עליזה.

## שלב 5 — מילוי keyword-bank

- ודא ש-`knowledge/keyword-bank.md` מכיל מספיק מילים ל-90 יום (הרחב לפי biomes).

## שלב 6 — Routines ב-Claude.ai

| Routine | Trigger (UTC) | Skill mode |
|---|---|---|
| Daily Short | א'-ו' 06:00 | Short |
| Long-form #1 | ראשון 06:00 | Long-form |
| Long-form #2 | רביעי 06:00 | Long-form |
| Analytics | שני 08:00 | Analytics |
| Coach | שני 09:00 | Coach |

- Connectors: Higgsfield, Ahrefs, Gmail, (ו-YouTube דרך ה-env vars).
- Repo: `danielhassid/dhpe-content-automation`, Skill: `nature-kids-studio`.

## שלב 7 — ריצת יבש + העלאה ראשונה

1. הרץ ידנית מצב Long-form **ללא העלאה** → בדוק `videos/[slug]/` מלא (ראה אימות ב-SKILL.md).
2. הרץ העלאה ראשונה כ-`private` → קבל מייל אישור → אשר ידנית.
3. אחרי 3 העלאות יציבות → אפשר מעבר לאוטומציה מלאה (`scheduled`).

---

### ✅ צ'קליסט סיום הקמה
- [ ] ערוץ + 4 פלייליסטים + made-for-kids מסומן
- [ ] env vars מוגדרים (3)
- [ ] Pip asset ID + voice ID שמורים
- [ ] keyword-bank מלא
- [ ] 5 Routines מוגדרים
- [ ] ריצת יבש עברה
