# Inspector Report — שער בטיחות (שומי 🐻)

> מפקח: שומי 🐻 (safety-inspector) · שלב 6 — שער עם זכות וטו
> מקור הקריטריונים: `knowledge/kids-safety-policy.md` + `templates/inspector-checklist.md`

---

**Slug:** `w1-ocean-animals`
**Type:** Long-form (אופקי 1920×1080)
**Reviewed:** 2026-06-19 (UTC)
**Video URL:** `<pending — DRY RUN, לא הורכב>` (assembled-video-url.txt = תוכנית הרכבה בלבד)
**מצב ריצה:** 🧪 DRY RUN — שלבי המדיה הם briefs (אין וידאו/אודיו מורכב בפועל).

> **הערת מתודולוגיה:** הערכת הבטיחות מבוססת על התסריט, ה-briefs ותוכנית ההרכבה.
> סעיפים התלויים ב-output מדיה אמיתי (artifacts ויזואליים, איכות קריינות בפועל,
> עוצמות אודיו בפועל) מסומנים **"לבדיקה חוזרת אחרי הרכבה אמיתית"** — אינם מכשילים
> כשלעצמם בריצת יבש, אך **חובה** לאמת לפני העלאה אמיתית.

---

## ויזואלי

- [x] **אין artifacts מפחידים** — PASS (תכנון). כל ה-prompts מציינים "big round eyes,
  gentle smile", "not scary", "soft rounded shapes". אין פנים מעוותות מתוכננות.
  *לבדיקה חוזרת אחרי הרכבה אמיתית* (artifacts יכולים להופיע רק ב-generation בפועל).
- [x] **אין סצנה חשוכה/מאיימת/אלימה** — PASS. Style block: "Bright sunlit turquoise
  water... Happy, calm, safe mood. No scary, dark, or threatening elements." אין חושך.
- [x] **דמות Pip עקבית עם ה-reference** — PASS (תכנון). חוק עקביות Pip מוגדר: כל beat
  שבו Pip מופיע משתמש ב-`<PIP_ASSET_ID>` כ-reference. Pip מופיע ב-beats 1,2,3,4,5,6,7,8,10.
  *לבדיקה חוזרת אחרי הרכבה אמיתית* — `<PIP_ASSET_ID>` הוא placeholder; חובה למלא asset
  ID אמיתי מ-`brand-voice.md` ולאמת זהות ויזואלית בין סצנות לפני העלאה.
- [x] **אין טקסט מעוות/ג'יבריש על המסך** — PASS. טקסט מתוכנן מינימלי וברור: thumbnail
  "OCEAN ANIMALS!", end card "Bye-bye!"/"See you next time!". *לבדיקה חוזרת* (rendering בפועל).
- [x] **אין תוכן מטריד (דם/פציעה/פחד/טריפה)** — PASS. **בדיקת כריש מועצמת:** הכריש
  מוגדר במפורש "small friendly... big soft smile and round gentle eyes (absolutely
  not scary, no sharp teeth shown), swims happily and waves". אין טריפה, אין שיניים,
  אין סכנה. כל החיות מוצגות ידידותיות. אין מוות/חושך/סכנה.

## תוכן/שפה

- [x] **מידע עובדתי נכון על הטבע** — PASS. תמנון בעל 8 זרועות ומשנה צבע ✓; לוויתן כחול
  הוא בעל החיים הגדול ביותר ✓; לבו גדול מאוד (השוואה "כמוך" — ניסוח ידידותי-לגיל,
  לא מטעה מהותית) ✓; צב ים עם שריון קשה ✓; סוס ים אוחז בזנבו ✓. אין שגיאה עובדתית.
- [x] **שפה הולמת, פשוטה, לא מפחידה** — PASS. אוצר מילים פרה-סקול, פנייה ישירה חמה
  ("Look!", "Can you see?"), טון מעודד. אין מילים מפחידות.
- [x] **כל משפט ≤ 8 מילים** — PASS. נבדק משפט-משפט בכל 9 הקטעים. המשפטים הארוכים ביותר
  (8 מילים): "The sea horse holds on with its tail." / "A friendly shark, a sea horse,
  a whale." — שניהם בדיוק 8. אין חריגה.
- [x] **מילת מפתח ב-15 מילים ראשונות** — PASS. "ocean animals for kids" מופיעה במילים
  11–14 של ה-HOOK ("Do you love **ocean animals for kids**?"). חוזרת ב-Explore (shark)
  וב-Recap.

## אודיו

- [x] **קריינות ברורה, קצב נכון, בלי רעש** — PASS (תכנון). tts-brief מגדיר ~120wpm,
  טון "חם, ברור, איטי-מתון", "בלי רעשי רקע מפחידים". *לבדיקה חוזרת אחרי הרכבה אמיתית*
  — Voice ID = `<TO_BE_FILLED>`; חובה להפיק אודיו אמיתי ולאמת בהירות/קצב לפני העלאה.
- [x] **מוזיקה -12db מתחת לקריינות** — PASS (תכנון). תוכנית ההרכבה: Track C מוזיקת רקע
  gain≈0.25 (≈-12dB), קריינות Track B gain 1.0. *לבדיקה חוזרת* — לאמת עוצמות ב-render בפועל.

## תאימות

- [x] **`selfDeclaredMadeForKids: true` בחבילת SEO** — PASS. קיים מפורשות ב-seo-package.md
  (`selfDeclaredMadeForKids: true`).
- [x] **אין קישור חיצוני / CTA בתיאור** — PASS. התיאור נקי מקישורים/URLs/CTA חיצוני.
  End card מתוכנן COPPA-safe (אין Subscribe/Like/URLs). רק "Bye-bye" ויזואלי.
- [x] **יחס מסך נכון (Long אופקי)** — PASS. 1920×1080 אופקי בכל ה-beats, בתוכנית ההרכבה,
  וב-RUN-LOG. תקין ל-Long-form.
- [x] **אורך בטווח (Long 3:00-4:30)** — PASS. אורך תוכן מתוכנן ~4:30 (+ end card ~7s).
  בטווח. *לבדיקה חוזרת* — לאמת משכי clip ב-video_metadata לפני render אמיתי.

---

## הכרעה

**PASS ✅ / FAIL ❌:** **PASS ✅**

**נימוק:**
כל סעיפי הצ'קליסט עוברים ברמת התכנון. אין ולו ❌ אחד. בטיחות הילד נשמרת:
אין תוכן מפחיד/חושך/מוות/סכנה/טריפה; הכריש מוצג ידידותי-מחייך ללא שיניים/איום;
מצב רוח שמח ובטוח; שפה תואמת-גיל (כל משפט ≤8 מילים); מילת מפתח ב-15 המילים הראשונות;
`selfDeclaredMadeForKids: true` קיים; אין קישורים חיצוניים/CTA; חוק עקביות Pip מוגדר;
יחס מסך 1920×1080; אורך בטווח.

**תנאי חובה לפני העלאה אמיתית (gating conditions — לא מכשילים ב-DRY RUN):**
1. השלמת setup: מילוי `<PIP_ASSET_ID>` ו-`<VOICE_ID>` ב-`brand-voice.md`.
2. הפקת מדיה אמיתית (generate_video / generate_audio / video_render).
3. **בדיקה חוזרת של שומי** על הסרטון המורכב בפועל לסעיפים המסומנים
   "לבדיקה חוזרת" (artifacts ויזואליים, עקביות Pip, איכות קריינות, עוצמות אודיו,
   טקסט על המסך, משכים) — לפני שדפנה מעלה.

**Handoff:** PASS → דפנה 🕊️ (distribution-manager). בריצה אמיתית: ההעלאה חסומה עד
מילוי תנאי ה-gating ובדיקה חוזרת.
