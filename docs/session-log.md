# יומן הפרויקט — צוות הסוכנים "טבע לילדים"

> תיעוד מלא של השיחה והעבודה. עודכן: 2026-06-22.
> ענף: `claude/youtube-kids-agent-system-a23kvd`.

---

## 1. המטרה

דניאל ביקש להפוך את ה-skill היחיד `nature-kids-studio` ל**צוות סוכנים אמיתי** — כל
תפקיד = סוכן ייעודי עם הקשר, כלים ומומחיות משלו. בנוסף: סוכן-אדריכל שמגייס/מציע את הצוות,
ומנגנון שמשפר את הצוות לאורך זמן. הכל בעברית, עם תוכנית ב-PDF לאישור.

## 2. החלטות מרכזיות (לפי הסדר)

1. **סדר בנייה:** אדריכל קודם → מציע צוות → אישור → בונים את השאר.
2. **מודל:** כל הסוכנים על **Opus**.
3. **שמות:** שמות-דמות אישיים (בעלי חיים), לצד מזהה טכני לטיני לכל סוכן.
4. **הרכב:** כל 12 הסוכנים אושרו.
5. **YouTube:** דרך connector שמוגדר ב-setup (לא כלי MCP ישיר).
6. **כלי וידאו:** נשארים על Higgsfield (דורג "Best"); טל עודכן להעדיף Seedance 2.0.

## 3. מה נבנה

### אדריכל הצוות
- `.claude/agents/team-architect.md` — בּוֹני 🦫. נבנה והורץ; הפיק `PROPOSED-TEAM.md`.

### 12 הסוכנים (כולם Opus, `.claude/agents/`)
| דמות | תפקיד | מזהה | שלב |
|---|---|---|---|
| בּוֹני 🦫 | אדריכל הצוות | `team-architect` | מטא |
| מאיה 🐝 | מפיק הסטודיו | `studio-orchestrator` | 1+8 ניהול |
| רוני 🦊 | חוקר הטרנדים | `trend-researcher` | 2 מחקר |
| זמיר 🐦 | התסריטאי | `scriptwriter` | 3 תסריט |
| טל 🦚 | המנהל האמנותי | `art-director` | 4a וידאו |
| קולי 🦗 | מפיק הקריינות | `voice-producer` | 4b קריינות |
| נמי 🐜 | אסטרטג ה-SEO | `seo-strategist` | 4c SEO |
| עֵדֶן 🐿️ | עורך הווידאו | `video-editor` | 5 הרכבה |
| שומי 🐻 | מפקח הבטיחות | `safety-inspector` | 6 וטו |
| דפנה 🕊️ | מנהל ההפצה | `publisher` | 7 העלאה |
| טוביה 🐭 | אנליסט הנתונים | `analytics-analyst` | Analytics |
| אלון 🐘 | מאמן הצוות | `team-coach` | Coach |

### חיווט
- `SKILL.md` עודכן עם טבלת האצלה (שלב → סוכן). ה-skill נשאר "ספר הנהלים" + מאגר ידע.

## 4. ריצת היבש — `w1-ocean-animals`

נושא: **"Ocean Animals — meet the sea"** (מילת מפתח `ocean animals for kids`).
הצוות רץ מקצה לקצה (אני כ-conductor האצלתי לכל סוכן). תיקייה:
`.claude/skills/nature-kids-studio/videos/w1-ocean-animals/`.

| שלב | דמות | פלט | הערה |
|---|---|---|---|
| 2 | רוני | `research-brief.md` | Ahrefs החזיר `Insufficient plan` → נפילה ל-keyword-bank |
| 3 | זמיר | `script-final.md` | 6 חיות, ~3:35, ≤8 מילים/משפט, כריש ידידותי |
| 4a | טל | `video-brief.md` | 10 beats + prompts (בלי generation) |
| 4b | קולי | `tts-brief.md` | 9 קטעים (בלי generation) |
| 4c | נמי | `seo-package.md` | made-for-kids=true, בלי קישורים |
| 5 | עֵדֶן | `assembled-video-url.txt` | תוכנית הרכבה ~4:40 (בלי render) |
| 6 | שומי | `inspector-report.md` | **PASS** |
| 7 | דפנה | `youtube-payload.json` | private, **בלי העלאה** |
| 8 | מאיה | `RUN-LOG.md` | סיכום, מצב = הצלחה |

**מה הוכח:** האצלה עובדת, השערים נאכפים (אין העלאה לפני PASS), הגבולות נשמרים
(אפס generation בתשלום, אפס העלאה, אפס מייל), כל סוכן כיבד את תחומו.

## 5. כלי וידאו ו-Higgsfield (חקירה)

- **מחוברים ל-Higgsfield** ופעיל. Higgsfield הוא שער לכל המודלים המובילים (Seedance 2.0,
  Kling 3.0, Wan, Grok) — אז ה"Good" וה"Best" מהדירוג כבר זמינים דרך connector אחד.
- **טל עודכן** להעדיף Seedance 2.0 (reference-driven, עקביות דמות), נפילה ל-Kling/Wan.
- **Pip נוצר באמת** 🦉 — `generate_image` (model `soul_2`), job
  `b62d1148-0654-4021-a018-c3c34e398ebd`. נשמר כ-Pip reference asset ID ב-`brand-voice.md`.

### מבצע "Unlimited Seedance" (בדיקה מול החשבון)
- החשבון: תוכנית **free**, ~9.88 קרדיטים.
- **כל מודלי הווידאו חסומים** ב-free ("Requires basic plan or higher") — נבדק Seedance,
  Kling Turbo, Grok. הקרדיטים שנשארו טובים **רק לתמונות**.
- ה"30 יום חינם" של האינפלואנסר **לא אומת**: Seedance הוא הטבה של תוכניות **בתשלום**
  (PLUS $49/חודש, ULTRA $129/חודש), לא ניסיון חינם. חלון "Buy until June 20" אולי נסגר.
- **המלצה:** לבדיקת איכות — PLUS חודשי מספיק (1,000 קרדיטים ≈ 200 קליפים), ניתן לבטל.

## 6. חסמים פתוחים (דורשים את דניאל)

1. **תוכנית Higgsfield** — שדרוג ל-PLUS/ULTRA כדי לייצר וידאו בכלל.
2. **Adobe `video_render`** — שרת ה-MCP התנתק; נדרש לחיבור מחדש (להרכבה מלאה).
3. **הקמת YouTube** — ערוץ, OAuth, מפתחות (חשבונות וסודות של דניאל).
4. **Ahrefs** — תוכנית נוכחית מחזירה `Insufficient plan` (יש fallback ל-keyword-bank).

## 7. הצעדים הבאים

- לשדרג Higgsfield → אריץ קליפ Pip אמיתי (Seedance 2.0) להדגמת איכות, בלי העלאה.
- לחבר מחדש Adobe → הרכבת Long-form מלאה.
- להשלים `setup/setup-guide.md` → ריצה אמיתית מקצה לקצה → העלאה private + אישור אנושי.

## 8. מפת קבצים

- `.claude/agents/*.md` — 12 הסוכנים + `PROPOSED-TEAM.md`.
- `.claude/skills/nature-kids-studio/` — ה-skill (SKILL.md, knowledge, templates, calendar).
- `.claude/skills/nature-kids-studio/videos/w1-ocean-animals/` — פלטי ריצת היבש.
- `docs/team-plan-he.pdf`, `docs/proposed-team-he.pdf` — תוכנית והצעת הצוות בעברית.
- `scripts/render_team_plan_pdf.py`, `scripts/render_proposed_team_pdf.py` — מחוללי ה-PDF.
- `docs/session-log.md` — היומן הזה.
