# הצעת צוות הסוכנים — "טבע לילדים"

> **מסמך לאישור.** הופק ע"י *אדריכל הצוות* (team-architect) לאחר קריאת `SKILL.md`,
> קבצי ה-knowledge וה-templates. כל סוכן ממופה על שלב אמיתי בצנרת ועל כלים זמינים.
> אתה מאשר / משנה / מסיר — ורק אחר כך נבנים הסוכנים בפועל.

## איך לקרוא

לכל סוכן: **שם עברי** (זהות הצוות) + **מזהה טכני** (slug לטיני לקובץ ולהפעלה),
ייעוד, שלב בצנרת, כלים, קלט/פלט, handoffs ומדדי הצלחה. כולם על **Opus**.

---

## טבלת הצוות (12 סוכנים)

| # | שם עברי | מזהה טכני | שלב בצנרת | כלים עיקריים |
|---|---|---|---|---|
| 1 | אדריכל הצוות | `team-architect` | מטא — עיצוב הצוות | Read, WebSearch, Write |
| 2 | מפיק הסטודיו | `studio-orchestrator` | שלב 1 + 8 (ניהול) | Read, Write, Gmail |
| 3 | חוקר הטרנדים | `trend-researcher` | שלב 2 — מחקר | Ahrefs, Read, Write |
| 4 | התסריטאי | `scriptwriter` | שלב 3 — תסריט | Read, Write |
| 5 | המנהל האמנותי | `art-director` | שלב 4a — וידאו | Higgsfield (image/video) |
| 6 | מפיק הקריינות | `voice-producer` | שלב 4b — קריינות | Higgsfield (audio/voices) |
| 7 | אסטרטג ה-SEO | `seo-strategist` | שלב 4c — SEO | Ahrefs, Read, Write |
| 8 | עורך הווידאו | `video-editor` | שלב 5 — הרכבה | Adobe `video_render` |
| 9 | מפקח הבטיחות | `safety-inspector` | שלב 6 — וטו | Read, Write |
| 10 | מנהל ההפצה | `publisher` | שלב 7 — העלאה | YouTube API ⚠️, Gmail |
| 11 | אנליסט הנתונים | `analytics-analyst` | מצב Analytics | YouTube API ⚠️, Write |
| 12 | מאמן הצוות | `team-coach` | מצב Coach | Read, Write |

⚠️ = תלוי ב-YouTube connector שמוגדר ב-`setup/setup-guide.md` (אין כרגע כלי MCP ישיר ל-YouTube).

---

## פירוט הסוכנים

### 1. אדריכל הצוות — `team-architect`
- **ייעוד:** חוקר, מעצב ומרענן את הרכב הצוות. מציע — לא בונה.
- **כלים:** Read, Glob, Grep, WebSearch, WebFetch, Write · **מודל:** Opus
- **קלט:** SKILL.md, knowledge/, templates/, README/PROGRESS.
- **פלט:** `PROPOSED-TEAM.md` (המסמך הזה).
- **Handoffs:** מקבל בקשה מהמשתמש → מעביר הצעה למשתמש לאישור.
- **הצלחה:** הצעה ממופה למציאות, גבולות אחריות ברורים, אושרה במינימום שינויים.

### 2. מפיק הסטודיו — `studio-orchestrator`
- **ייעוד:** מנהל הריצה: בוחר נושא, מאציל לכל סוכן בתורו, אוכף שערים, מסכם.
- **כלים:** Read, Write, Gmail (מייל סטטוס) · **מודל:** Opus
- **קלט:** `content-calendar/30-day-plan.md` + `rotation-logic.md`.
- **פלט:** תיקיית `videos/[slug]/` + `RUN-LOG.md`; עדכון הקלנדר `pending→published`.
- **Handoffs:** הלב של הצוות — מתאם בין כל הסוכנים דרך קבצי `videos/[slug]/`.
- **הצלחה:** ריצה שלמה בלי דילוג על שלב; חוק הברזל (אין העלאה לפני PASS) נאכף.

### 3. חוקר הטרנדים — `trend-researcher`
- **ייעוד:** מחקר מילות מפתח ונושאים (שלב 2).
- **כלים:** Ahrefs (`keywords-explorer-overview` / `matching-terms` / `related-terms`),
  Read, Write · **מודל:** Opus
- **קלט:** הנושא מהמפיק; fallback ל-`knowledge/keyword-bank.md` (סימון `[USED]`).
- **פלט:** `research-brief.md` — מילת מפתח ראשית, 5 משניות, ~10 תגיות, 3 כותרות.
- **Handoffs:** מפיק → חוקר → תסריטאי + אסטרטג SEO.
- **הצלחה:** מילות מפתח עם ביקוש אמיתי; כותרות עומדות בכללי הגיל.

### 4. התסריטאי — `scriptwriter`
- **ייעוד:** כתיבת תסריט Short/Long לפי התבניות וכללי הגיל (שלב 3).
- **כלים:** Read, Write · **מודל:** Opus
- **קלט:** `research-brief.md`, `templates/short-script.md` / `long-script.md`,
  `age-targeting.md`, `educational-framework.md`, `brand-voice.md`.
- **פלט:** `script-final.md` + צ'קליסט (≤8 מילים/משפט, מילת מפתח מוקדם, `[PAUSE]`).
- **Handoffs:** חוקר → תסריטאי → מנהל אמנותי + מפיק קריינות.
- **הצלחה:** תסריט תואם-גיל, קול Pip עקבי, מבנה לימודי ברור.

### 5. המנהל האמנותי — `art-director`
- **ייעוד:** יצירת הוויזואל/וידאו עם עקביות Pip (שלב 4a).
- **כלים:** Higgsfield `generate_image`, `generate_video`, `job_display`,
  `media_import_url`, `show_characters`, `motion_control` · **מודל:** Opus
- **קלט:** `script-final.md`, Pip reference asset ID + סגנון מ-`brand-voice.md`.
- **פלט:** `video-brief.md` (URLs + timestamps). יחס: Short 1080×1920 / Long 1920×1080.
- **גיבוי:** אם Higgsfield נכשל → slideshow תמונות סטטיות, דיווח למפיק.
- **Handoffs:** תסריטאי → מנהל אמנותי → עורך הווידאו.
- **הצלחה:** Pip זהה בין סצנות, פלטת צבעים על-פי המותג, בלי סצנות מפחידות.

### 6. מפיק הקריינות — `voice-producer`
- **ייעוד:** קריינות TTS בקול הקבוע (שלב 4b).
- **כלים:** Higgsfield `generate_audio`, `list_voices`, `dubbing`, `voice_change` · **מודל:** Opus
- **קלט:** `script-final.md`, Voice ID מ-`brand-voice.md`.
- **פלט:** `tts-brief.md` (URLs + משכים). קצב ~120 wpm, השהיה ב-`[PAUSE]`.
- **Handoffs:** תסריטאי → מפיק קריינות → עורך הווידאו.
- **הצלחה:** קול חם וברור, תזמון תואם ל-beats של הוידאו.

### 7. אסטרטג ה-SEO — `seo-strategist`
- **ייעוד:** חבילת מטא-דאטה לפרסום (שלב 4c).
- **כלים:** Ahrefs (`serp-overview`), Read, Write · **מודל:** Opus
- **קלט:** `research-brief.md`, `templates/seo-package.md`, `youtube-algorithm.md`.
- **פלט:** `seo-package.md` — כותרת/תיאור/תגיות, **`selfDeclaredMadeForKids: true`**,
  בלי קישורים חיצוניים/CTA (COPPA).
- **Handoffs:** חוקר → אסטרטג SEO → מנהל ההפצה.
- **הצלחה:** מטא-דאטה תואמת-COPPA, כותרת עם CTR גבוה, תגיות רלוונטיות.

### 8. עורך הווידאו — `video-editor`
- **ייעוד:** הרכבה סופית של וידאו+קריינות+מוזיקה (שלב 5).
- **כלים:** Adobe `video_render`, `video_metadata`, `video_resize`,
  Higgsfield `upscale_video` · **מודל:** Opus
- **קלט:** `video-brief.md`, `tts-brief.md`, מוזיקת רקע (‎-12db‎).
- **פלט:** `assembled-video-url.txt`. end card 5–10ש' ל-Long.
- **Handoffs:** מנהל אמנותי + מפיק קריינות → עורך → מפקח הבטיחות.
- **הצלחה:** סנכרון אודיו-וידאו, יחס מסך נכון, MP4 נגיש.

### 9. מפקח הבטיחות — `safety-inspector` 🛡️
- **ייעוד:** שער בטיחות לילדים עם **זכות וטו** (שלב 6).
- **כלים:** Read, Write · **מודל:** Opus
- **קלט:** כל פלטי `videos/[slug]/`, `templates/inspector-checklist.md`, `kids-safety-policy.md`.
- **פלט:** `inspector-report.md` (PASS/FAIL). **FAIL ⇒ עצור, ❌ ב-RUN-LOG, אל תעלה, דווח.**
- **Handoffs:** עורך → מפקח → (PASS) מנהל ההפצה / (FAIL) חזרה למפיק.
- **הצלחה:** אפס תוכן מפחיד/מסוכן עובר; כל כללי הבטיחות מאומתים.

### 10. מנהל ההפצה — `publisher` 🚦
- **ייעוד:** העלאה ליוטיוב + שער אישור אנושי (שלב 7).
- **כלים:** YouTube Data API ⚠️ (`videos.insert`, `playlistItems.insert`), Gmail · **מודל:** Opus
- **קלט:** `assembled-video-url.txt`, `seo-package.md`, `templates/youtube-payload.json`.
- **פלט:** `youtube-payload.json`. **3 העלאות ראשונות = `private` + מייל אישור** ל-dh052597@gmail.com.
- **Handoffs:** מפקח (PASS) → מנהל ההפצה → מפיק (סיכום).
- **הצלחה:** `selfDeclaredMadeForKids: true` תמיד; אין פרסום בלי אישור בשלב הראשוני.

### 11. אנליסט הנתונים — `analytics-analyst`
- **ייעוד:** דוח ביצועים שבועי (מצב Analytics).
- **כלים:** YouTube Data API ⚠️ (`videos.list` statistics), Write · **מודל:** Opus
- **קלט:** נתוני 7 ימים אחרונים.
- **פלט:** `analytics-snapshot.md` + מייל דוח. מסמן סרטונים עם השלמה <40%; מחשב התקדמות ל-YPP.
- **Handoffs:** מנהל ההפצה (נתונים) → אנליסט → מאמן הצוות.
- **הצלחה:** דוח מדויק, מזהה מגמות אמיתיות.

### 12. מאמן הצוות — `team-coach`
- **ייעוד:** מנתח ביצועים ותפקוד הצוות, **מציע** שיפורים (מצב Coach).
- **כלים:** Read, Write, Gmail · **מודל:** Opus
- **קלט:** 4 דוחות `analytics-snapshot.md` אחרונים + `team-improvements.md`.
- **פלט:** הצעות ל-`team-improvements.md` + RUN-LOG; הצעות A/B למפיק; מייל "מה הצעתי".
- **כלל ברזל:** **מציע, לא מיישם.** כל שינוי skill/template/agent דורש commit שהמשתמש מאשר. לעולם לא נוגע ב-credentials.
- **הצלחה:** הצעות מבוססות-נתונים שמשפרות retention/צמיחה לאורך זמן.

---

## זרימת ה-handoffs (סדר הצנרת)

```
מפיק הסטודיו → חוקר הטרנדים → התסריטאי → ┌ המנהל האמנותי ┐
                                          ├ מפיק הקריינות ┤→ עורך הווידאו → מפקח הבטיחות
                                          └ אסטרטג ה-SEO  ┘                      │
                                                                          (PASS) ▼
                                       מפיק (סיכום) ← מנהל ההפצה ←──────────────────┘

מחזור שבועי:  מנהל ההפצה → אנליסט הנתונים → מאמן הצוות → (הצעות) → מפיק/משתמש
```

---

## שינויים מההצעה ההתחלתית (המלצות האדריכל)

1. **שמירה על הפרדה מנהל-אמנותי ↔ עורך-וידאו.** ב-SKILL שלב 4a (יצירה, Higgsfield) ושלב
   5 (הרכבה, Adobe `video_render`) משתמשים בכלים שונים לגמרי — עדיף שני סוכנים חדים.
2. **אין סוכן נפרד ל-Short.** ה-Short נגזר מנושא ה-Long של אותו שבוע; אותו צוות מטפל בשניהם
   עם פרמטר יחס-מסך. הוספת סוכן נפרד תייצר כפילות.
3. **תלות YouTube מסומנת בכנות (⚠️).** למנהל ההפצה ולאנליסט אין כרגע כלי MCP ישיר ל-YouTube;
   הם תלויים ב-connector שמוגדר ב-`setup/setup-guide.md`. אם תרצה, אפשר לגשר דרך Make/Routines.
4. **השמות העבריים תואמים לשמות הקוד הקיימים** ב-SKILL (Orchestrator/Research/Script/M&M/
   Cotton/Twix/Inspector/KitKat/Analytics/Coach) — אז המעבר חלק וללא בלבול.

---

## שאלות פתוחות לאישורך

1. **גודל הצוות:** לאשר את כל ה-12, או למזג (למשל מנהל-אמנותי+עורך לסוכן "וידאו" אחד)?
2. **YouTube:** לגשת דרך connector קיים, או שאתכנן גישור Make/Routines למנהל ההפצה+אנליסט?
3. **שמות:** להשאיר שמות-תפקיד (אדריכל הצוות, התסריטאי…), או שתרצה שמות-דמות אישיים?
