# Credentials Guide — מבנה בלבד (⚠️ ללא סודות אמיתיים בגיט)

> **חוק ברזל:** קובץ זה מתעד *מבנה* ו-*שמות* בלבד. ערכים אמיתיים (tokens, secrets)
> נשמרים כ-env vars / Routine secrets ב-Claude.ai — **לעולם לא בקבצי הגיט.**
> Coach **לעולם לא** עורך את הקובץ הזה.

## Environment Variables נדרשים (ערכים מחוץ לגיט)

| שם | מקור | תיאור |
|---|---|---|
| `YOUTUBE_CLIENT_ID` | Google Cloud Console | OAuth client ID |
| `YOUTUBE_CLIENT_SECRET` | Google Cloud Console | OAuth client secret |
| `YOUTUBE_REFRESH_TOKEN` | OAuth flow חד-פעמי | refresh token להעלאות |

## Playlist IDs (לא סודי — אפשר כאן אחרי יצירה)

| פלייליסט | ID | מטרה |
|---|---|---|
| Animals | `<TO_BE_FILLED>` | סרטוני חיות |
| Ocean & Sea | `<TO_BE_FILLED>` | אוקיינוס |
| Nature Facts (Shorts) | `<TO_BE_FILLED>` | Shorts |
| New Videos | `<TO_BE_FILLED>` | כל החדשים |

## Channel info (לא סודי)

| שדה | ערך |
|---|---|
| Channel ID | `<TO_BE_FILLED>` |
| Channel handle | `<TO_BE_FILLED>` |

## Higgsfield assets (לא סודי — ראה גם brand-voice.md)

| נכס | ID |
|---|---|
| Pip reference asset | `<TO_BE_FILLED>` |
| Voice ID | `<TO_BE_FILLED>` |

## בדיקת ביטחון לפני כל commit

- [ ] אין tokens/secrets אמיתיים בשום קובץ.
- [ ] רק שמות env vars מתועדים, לא ערכים.
