# RUN-LOG — w1-ocean-animals

| שדה | ערך |
|---|---|
| **כותרת עבודה** | Ocean Animals — meet the sea |
| **נושא / Biome** | שבוע 1 — 🌊 Ocean (פריט L1) |
| **מילת מפתח ראשית** | ocean animals for kids |
| **slug** | `w1-ocean-animals` |
| **סוג** | Long-form (3-5 דק', אופקי 1920x1080) |
| **מצב** | 🧪 DRY RUN |
| **תאריך** | 2026-06-19 |
| **דמות מנחה** | Pip 🦉 |
| **מנצח** | מאיה 🐝 (studio-orchestrator) |

---

## ⚠️ הערות DRY RUN

- **לא מבצעים generation בתשלום.** ההקמה ב-`setup/setup-guide.md` עדיין לא הושלמה:
  `Pip asset ID` = `<TO_BE_FILLED>`, `Voice ID` = `<TO_BE_FILLED>`, אין connector ל-YouTube.
- **שלבי מדיה (4a Video / 4b Voice / 5 Assembly):** נוצר **brief בלבד** — מתארים מה
  *היה* נוצר (prompts, beats, timestamps, job placeholders). אין קריאה ל-`generate_video`/
  `generate_audio`/`video_render`.
- **שלב 7 (העלאה): מושבת.** נבנה `youtube-payload.json` כ-artifact בלבד; אין connector,
  אין `videos.insert`, אין עדכון של `30-day-plan.md` ל-`published`.
- מטרת הריצה: לאמת זרימה מקצה-לקצה של הצוות, וקיום כל הפלטים הנדרשים.

---

## ✅ צ'קליסט שלבים (1-8)

> כל שלב מתחיל ⬜ ומסומן ✅ רק כשהפלט שלו קיים ואומת. חוק ברזל: אין מעבר לשלב הבא
> לפני שהקודם ✅. אין שלב 7 לפני ש-`inspector-report.md` = **PASS**.

| # | שלב | דמות (מזהה) | קלט → פלט | סטטוס |
|---|---|---|---|---|
| 1 | בחירת נושא + פתיחת ריצה | מאיה 🐝 (`studio-orchestrator`) | calendar + rotation-logic → תיקיית ריצה + `RUN-LOG.md` | ✅ |
| 2 | מחקר מילות מפתח | רוני 🦊 (`trend-researcher`) | `ocean animals for kids` → `research-brief.md` | ⬜ |
| 3 | תסריט | זמיר 🐦 (`scriptwriter`) | `research-brief.md` + `templates/long-script.md` → `script-final.md` | ⬜ |
| 4a | וידאו (brief בלבד) | טל 🦚 (`art-director`) | `script-final.md` → `video-brief.md` | ⬜ |
| 4b | קריינות (brief בלבד) | קולי 🦗 (`voice-producer`) | `script-final.md` → `tts-brief.md` | ⬜ |
| 4c | SEO | נמי 🐜 (`seo-strategist`) | `research-brief.md` + `script-final.md` → `seo-package.md` | ⬜ |
| 5 | הרכבה (brief בלבד) | עֵדֶן 🐿️ (`video-editor`) | `video-brief.md` + `tts-brief.md` → `assembled-video-url.txt` | ⬜ |
| 6 | בטיחות (שער וטו) | שומי 🐻 (`safety-inspector`) | כל הפלטים → `inspector-report.md` (PASS/FAIL) | ⬜ |
| 7 | העלאה — **מושבת ב-DRY RUN** | דפנה 🕊️ (`publisher`) | `seo-package.md` + `inspector-report.md` (PASS) → `youtube-payload.json` (artifact בלבד) | ⬜ |
| 8 | סיכום | מאיה 🐝 (`studio-orchestrator`) | כל הפלטים → השלמת `RUN-LOG.md` + מייל סטטוס | ⬜ |

---

## 📋 יומן אירועים

- **2026-06-19** — מאיה: שלב 1 הושלם. נושא נבחר (Ocean L1), slug `w1-ocean-animals`,
  תיקיית ריצה נפתחה, `RUN-LOG.md` נכתב במצב DRY RUN. ממתין להאצלת שלב 2 ע"י ה-conductor.
