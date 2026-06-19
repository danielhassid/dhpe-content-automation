# SKILL: nature-kids-studio

ערוץ יוטיוב "טבע לילדים" באנגלית. דמות מנחה: Pip 🦉.
**Shorts כמנוע גידול + 2 Long-form בשבוע לשעות צפייה.** ערוץ `made-for-kids`.

## מתי להפעיל

- **מצב Short** — יצירת Short יומי (א'-ו' 06:00 UTC).
- **מצב Long-form** — יצירת סרטון 3-5 דק' (ראשון + רביעי 06:00 UTC).
- **מצב Analytics** — דוח שבועי (שני 08:00 UTC).
- **מצב Coach** — הצעות שיפור שבועיות (שני 09:00 UTC).

> לפני ריצה ראשונה: ודא שכל שלבי `setup/setup-guide.md` הושלמו.

---

## צוות הסוכנים (האצלה)

הצנרת מורצת ע"י צוות סוכנים ב-`.claude/agents/`. **מאיה** (מפיק הסטודיו) מנצחת על
הריצה, וכל שלב מואצל למומחה שלו דרך קבצי `videos/[slug]/`. ה-conductor (ה-session
הראשי) מפעיל כל סוכן עם תיקיית הריצה כהקשר — סוכן אינו מפעיל סוכן אחר.

| שלב | סוכן (דמות) | מזהה טכני |
|---|---|---|
| 1 + 8 — ניהול וסיכום | מאיה 🐝 מפיק הסטודיו | `studio-orchestrator` |
| 2 — מחקר | רוני 🦊 חוקר הטרנדים | `trend-researcher` |
| 3 — תסריט | זמיר 🐦 התסריטאי | `scriptwriter` |
| 4a — וידאו | טל 🦚 המנהל האמנותי | `art-director` |
| 4b — קריינות | קולי 🦗 מפיק הקריינות | `voice-producer` |
| 4c — SEO | נמי 🐜 אסטרטג ה-SEO | `seo-strategist` |
| 5 — הרכבה | עֵדֶן 🐿️ עורך הווידאו | `video-editor` |
| 6 — בטיחות (וטו) | שומי 🐻 מפקח הבטיחות | `safety-inspector` |
| 7 — העלאה | דפנה 🕊️ מנהל ההפצה | `publisher` |
| Analytics | טוביה 🐭 אנליסט הנתונים | `analytics-analyst` |
| Coach | אלון 🐘 מאמן הצוות | `team-coach` |
| מטא — עיצוב הצוות | בּוֹני 🦫 אדריכל הצוות | `team-architect` |

---

## קריאת חובה לפני כל ריצת תוכן

- `knowledge/brand-voice.md` — Pip, סגנון ויזואלי, asset/voice IDs
- `knowledge/educational-framework.md` — מבנה לימודי
- `knowledge/age-targeting.md` — כללי שפה וקצב
- `knowledge/kids-safety-policy.md` — בטיחות ו-Inspector
- `knowledge/youtube-algorithm.md` — מה עובד

---

## מצב Short / Long-form — ה-pipeline

צור תיקייה `videos/[slug]/` וכתוב `RUN-LOG.md`. כל שלב מסומן ✅ לפני הבא.
**חוק ברזל: אסור להעלות לפני שכל שלב קודם ✅, ולפני ש-Inspector = PASS.**

### שלב 1 — בחירת נושא (Orchestrator)
- קרא `content-calendar/30-day-plan.md` + `rotation-logic.md`.
- בחר הפריט הבא (`pending`). Short נגזר מנושא ה-Long של אותו שבוע.

### שלב 2 — מחקר (Research)
- Ahrefs: `keywords-explorer-overview` / `matching-terms` / `related-terms` למילת המפתח.
- אם Ahrefs לא זמין → קח מ-`knowledge/keyword-bank.md` וסמן `[USED]`.
- פלט: מילת מפתח ראשית, 5 משניות, ~10 תגיות, 3 אפשרויות כותרת.

### שלב 3 — תסריט (Script Writer)
- Short → `templates/short-script.md`; Long → `templates/long-script.md`.
- עמוד בכל כללי `age-targeting.md` (≤8 מילים/משפט, מילת מפתח מוקדם, [PAUSE]).
- פלט: `videos/[slug]/script-final.md` + עבור את הצ'קליסט בתבנית.

### שלב 4 — וידאו + קריינות + SEO (במקביל)
**4a. Video (M&M / Higgsfield)**
- השתמש ב-Pip asset ID הקבוע (`media_import_url` / reference) — עקביות.
- `generate_video` לכל visual beat; שמור job IDs (`job_display`).
- יחס: Short אנכי 1080x1920 / Long אופקי 1920x1080.
- פלט: `video-brief.md` (URLs + timestamps).
- **גיבוי אם Higgsfield נכשל:** slideshow תמונות סטטיות + קריינות → דווח ל-Orchestrator.

**4b. Voice (Cotton / Higgsfield TTS)**
- voice ID קבוע מ-brand-voice. אודיו לכל קטע. קצב 120 wpm, השהיה ב-[PAUSE].
- פלט: `tts-brief.md` (URLs + משכים).

**4c. SEO (Twix)**
- מלא `templates/seo-package.md` → `videos/[slug]/seo-package.md`.
- **`selfDeclaredMadeForKids: true` חובה.** בלי קישורים חיצוניים.

### שלב 5 — הרכבה (Assembly)
- `video_render`: וידאו + קריינות + מוזיקה (‎-12db‎).
- end card 5-10 שניות (Long). פלט: `videos/[slug]/assembled-video-url.txt`.

### שלב 6 — 🛡️ Inspector (שער בטיחות — וטו)
- מלא `templates/inspector-checklist.md` → `videos/[slug]/inspector-report.md`.
- **FAIL ⇒ עצור, סמן ❌ ב-RUN-LOG, אל תעלה, דווח למשתמש.**
- PASS ⇒ המשך.

### שלב 7 — 🚦 Upload (KitKat — שער אישור אנושי)
- בנה `youtube-payload.json` מהתבנית. ודא `selfDeclaredMadeForKids: true`.
- **3 ריצות ראשונות:** העלה `private` + שלח מייל אישור ל-dh052597@gmail.com. **אל תפרסם.**
- אחרי אישור / בלוק יציבות: `scheduled` עם `publishAt` מבוסס-נתונים (ברירת מחדל ~21:00 UTC).
- `playlistItems.insert` לפלייליסט הנושאי + New Videos.
- עדכן `30-day-plan.md`: `pending` → `published`.

### שלב 8 — סיכום (Orchestrator)
- השלם `RUN-LOG.md`, שלח מייל סטטוס.

---

## מצב Analytics (שבועי)

- `videos.list` (statistics) ל-7 הימים האחרונים.
- סמן סרטונים עם שיעור השלמה < 40% לבדיקה.
- חשב התקדמות לעבר YPP (4,000 שעות + 1,000 מנויים **או** 10M Shorts views).
- פלט: `analytics-snapshot.md` + מייל דוח שבועי.

## מצב Coach (שבועי, אחרי Analytics)

- קרא 4 דוחות `analytics-snapshot.md` אחרונים + `team-improvements.md`.
- זהה דפוסים (איזה פורמט/biome זוכה).
- **כתוב הצעות בלבד** ל-`team-improvements.md` + RUN-LOG. הצע A/B tests ל-Orchestrator.
- **לעולם לא עריכה אוטומטית** של SKILL.md/templates — כל שינוי דורש commit שהמשתמש מאשר.
- **לעולם לא נוגע** ב-`credentials-guide.md`.
- שלח מייל "מה הצעתי השבוע".

---

## כללי ברזל

1. **אסור להעלות** לפני שכל השלבים ✅ ו-Inspector = PASS.
2. **`selfDeclaredMadeForKids: true`** בכל העלאה — מאומת.
3. **אין קישורים חיצוניים / CTA** (COPPA).
4. **סודות לא בגיט** — env vars בלבד.
5. **3 העלאות ראשונות = private + אישור אנושי.**
6. **Coach מציע, לא מיישם** — שינויי skill דורשים אישור.
7. **איכות על כמות** — נושא ממוקד, ערך לימודי אמיתי (נגד "mass-produced").
8. **בלי תוכן מפחיד** — בלי טריפה/מוות/סכנה/חושך.

---

## אימות (ריצת יבש)

תיקיית `videos/[slug]/` חייבת לכלול: `script-final.md`, `video-brief.md`, `tts-brief.md`,
`assembled-video-url.txt`, `inspector-report.md` (PASS), `seo-package.md`
(עם made-for-kids), `youtube-payload.json`, `RUN-LOG.md`.
בדוק: אורך תקין, [PAUSE] במקום, מילת מפתח מוקדם, MP4 נגיש, יחס מסך נכון, Pip עקבי.
