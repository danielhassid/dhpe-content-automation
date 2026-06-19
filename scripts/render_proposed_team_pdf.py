#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the architect's PROPOSED-TEAM roster as a Hebrew (RTL) PDF."""
from fpdf import FPDF
from bidi.algorithm import get_display
import os

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SAND = (250, 247, 240)
INK = (40, 40, 45)
GREEN = (34, 110, 64)
LEAF = (60, 140, 80)
GREY = (110, 110, 115)
LINE = (210, 205, 195)
CARDBG = (244, 249, 244)
W = 210 - 36


def rtl(s):
    return get_display(s)


class PDF(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_font("Dejavu", "", 8)
        self.set_text_color(*GREY)
        self.cell(0, 8, rtl(f"טבע לילדים · הצעת צוות הסוכנים · עמ' {self.page_no()}"),
                  align="C")


pdf = PDF(format="A4")
pdf.set_auto_page_break(auto=True, margin=18)
pdf.add_font("Dejavu", "", f"{FONT_DIR}/DejaVuSans.ttf")
pdf.add_font("Dejavu", "B", f"{FONT_DIR}/DejaVuSans-Bold.ttf")
pdf.set_margins(18, 18, 18)


def H2(t):
    pdf.ln(2)
    pdf.set_font("Dejavu", "B", 13)
    pdf.set_text_color(*LEAF)
    pdf.multi_cell(W, 7.5, rtl(t), align="R")
    pdf.set_draw_color(*LINE)
    pdf.set_line_width(0.3)
    y = pdf.get_y() + 0.5
    pdf.line(18, y, 18 + W, y)
    pdf.ln(2)


def para(t, size=10, color=INK):
    pdf.set_font("Dejavu", "", size)
    pdf.set_text_color(*color)
    pdf.multi_cell(W, 5.6, rtl(t), align="R")
    pdf.ln(0.4)


PERSONA = {
    "team-architect": "בוני (בונה)", "studio-orchestrator": "מאיה (דבורה)",
    "trend-researcher": "רוני (שועל)", "scriptwriter": "זמיר (ציפור)",
    "art-director": "טל (טווס)", "voice-producer": "קולי (צרצר)",
    "seo-strategist": "נמי (נמלה)", "video-editor": "עדן (סנאי)",
    "safety-inspector": "שומי (דוב)", "publisher": "דפנה (יונה)",
    "analytics-analyst": "טוביה (חפרפרת)", "team-coach": "אלון (פיל)",
}


def agent_card(num, he, slug, lines):
    if pdf.get_y() > 248:
        pdf.add_page()
    pdf.set_fill_color(*CARDBG)
    pdf.set_draw_color(*LEAF)
    pdf.set_line_width(0.4)
    start = pdf.get_y()
    pdf.ln(1.5)
    # title row
    pdf.set_x(20)
    pdf.set_font("Dejavu", "B", 11.5)
    pdf.set_text_color(*GREEN)
    persona = PERSONA.get(slug, "")
    pdf.cell(W - 4, 6.5, rtl(f"{num}. {persona} — {he}   ·   {slug}"), align="R")
    pdf.ln(7)
    pdf.set_font("Dejavu", "", 9.5)
    pdf.set_text_color(*INK)
    for label, val in lines:
        pdf.set_x(20)
        pdf.set_font("Dejavu", "B", 9.5)
        pdf.set_text_color(*LEAF)
        # render value then label on the right
        full = f"{val}  :{label}"
        pdf.set_font("Dejavu", "", 9.5)
        pdf.set_text_color(*INK)
        pdf.multi_cell(W - 4, 5.2, rtl(full), align="R")
    pdf.ln(1.5)
    end = pdf.get_y()
    pdf.rect(18, start, W, end - start, style="D")
    pdf.ln(2.5)


# ---------- Cover ----------
pdf.add_page()
pdf.set_fill_color(*GREEN)
pdf.rect(0, 0, 210, 60, style="F")
pdf.set_y(18)
pdf.set_font("Dejavu", "B", 24)
pdf.set_text_color(255, 255, 255)
pdf.multi_cell(W, 11, rtl("הצעת צוות הסוכנים"), align="R")
pdf.set_font("Dejavu", "", 13)
pdf.multi_cell(W, 8, rtl("\"טבע לילדים\" · הופק ע\"י אדריכל הצוות"), align="R")
pdf.set_y(66)
pdf.set_font("Dejavu", "", 9.5)
pdf.set_text_color(*GREY)
pdf.multi_cell(W, 5.4, rtl("אושר 19/06/2026 · 12 סוכנים נבנו · כולם על Opus · YouTube דרך connector · שמות-דמות אישיים"),
               align="R")
pdf.ln(3)

H2("טבלת הצוות")
rows = [
    ("#", "דמות", "שם תפקיד", "מזהה טכני"),
    ("1", "בוני (בונה)", "אדריכל הצוות", "team-architect"),
    ("2", "מאיה (דבורה)", "מפיק הסטודיו", "studio-orchestrator"),
    ("3", "רוני (שועל)", "חוקר הטרנדים", "trend-researcher"),
    ("4", "זמיר (ציפור)", "התסריטאי", "scriptwriter"),
    ("5", "טל (טווס)", "המנהל האמנותי", "art-director"),
    ("6", "קולי (צרצר)", "מפיק הקריינות", "voice-producer"),
    ("7", "נמי (נמלה)", "אסטרטג ה-SEO", "seo-strategist"),
    ("8", "עדן (סנאי)", "עורך הווידאו", "video-editor"),
    ("9", "שומי (דוב)", "מפקח הבטיחות", "safety-inspector"),
    ("10", "דפנה (יונה)", "מנהל ההפצה", "publisher"),
    ("11", "טוביה (חפרפרת)", "אנליסט הנתונים", "analytics-analyst"),
    ("12", "אלון (פיל)", "מאמן הצוות", "team-coach"),
]
cw = [10, 44, 46, 74]
for i, (c0, c1, c2, c3) in enumerate(rows):
    if i == 0:
        pdf.set_fill_color(*GREEN); pdf.set_text_color(255, 255, 255); pdf.set_font("Dejavu", "B", 9.5)
    else:
        pdf.set_fill_color(*(SAND if i % 2 else (255, 255, 255))); pdf.set_text_color(*INK); pdf.set_font("Dejavu", "", 9)
    pdf.set_x(18)
    pdf.cell(cw[3], 7, (c3 if i else rtl(c3)), border=0, fill=True, align="R")
    pdf.cell(cw[2], 7, rtl(c2), border=0, fill=True, align="R")
    pdf.cell(cw[1], 7, rtl(c1), border=0, fill=True, align="R")
    pdf.cell(cw[0], 7, rtl(c0), border=0, fill=True, align="C")
    pdf.ln(7)
para("⚠️ דפנה (מנהל ההפצה) וטוביה (אנליסט) — YouTube דרך ה-connector שמוגדר ב-setup.",
     size=8.5, color=GREY)

# ---------- Detail cards ----------
pdf.add_page()
H2("פירוט הסוכנים")

cards = [
    (1, "אדריכל הצוות", "team-architect", [
        ("ייעוד", "חוקר, מעצב ומרענן את הרכב הצוות — מציע, לא בונה."),
        ("כלים", "Read, WebSearch, WebFetch, Write"),
        ("פלט", "PROPOSED-TEAM.md (המסמך הזה)"),
        ("הצלחה", "הצעה מעוגנת במציאות, אושרה במינימום שינויים."),
    ]),
    (2, "מפיק הסטודיו", "studio-orchestrator", [
        ("ייעוד", "בוחר נושא, מאציל לכל סוכן, אוכף שערים, מסכם."),
        ("כלים", "Read, Write, Gmail"),
        ("קלט", "content-calendar/30-day-plan.md + rotation-logic.md"),
        ("פלט", "videos/[slug]/ + RUN-LOG.md; עדכון הקלנדר"),
        ("הצלחה", "ריצה שלמה; חוק הברזל (אין העלאה לפני PASS) נאכף."),
    ]),
    (3, "חוקר הטרנדים", "trend-researcher", [
        ("ייעוד", "מחקר מילות מפתח ונושאים."),
        ("כלים", "Ahrefs (keywords-explorer), Read, Write"),
        ("פלט", "research-brief.md — מפתח ראשי, 5 משניות, ~10 תגיות, 3 כותרות"),
        ("גיבוי", "אם Ahrefs לא זמין → keyword-bank.md (סימון [USED])"),
        ("הצלחה", "מילות מפתח עם ביקוש אמיתי; כותרות תואמות-גיל."),
    ]),
    (4, "התסריטאי", "scriptwriter", [
        ("ייעוד", "תסריט Short/Long לפי תבניות וכללי הגיל."),
        ("כלים", "Read, Write"),
        ("קלט", "research-brief.md + תבניות + age-targeting + brand-voice"),
        ("פלט", "script-final.md (≤8 מילים/משפט, מפתח מוקדם, [PAUSE])"),
        ("הצלחה", "תסריט תואם-גיל, קול Pip עקבי, מבנה לימודי ברור."),
    ]),
    (5, "המנהל האמנותי", "art-director", [
        ("ייעוד", "יצירת הוויזואל/וידאו עם עקביות Pip."),
        ("כלים", "Higgsfield: generate_image, generate_video, job_display, motion_control"),
        ("פלט", "video-brief.md (URLs+timestamps). Short 1080x1920 / Long 1920x1080"),
        ("גיבוי", "אם Higgsfield נכשל → slideshow + דיווח למפיק"),
        ("הצלחה", "Pip זהה בין סצנות, פלטה על-פי המותג, בלי סצנות מפחידות."),
    ]),
    (6, "מפיק הקריינות", "voice-producer", [
        ("ייעוד", "קריינות TTS בקול הקבוע."),
        ("כלים", "Higgsfield: generate_audio, list_voices, dubbing, voice_change"),
        ("פלט", "tts-brief.md (URLs+משכים). ~120 wpm, השהיה ב-[PAUSE]"),
        ("הצלחה", "קול חם וברור, תזמון תואם ל-beats של הוידאו."),
    ]),
    (7, "אסטרטג ה-SEO", "seo-strategist", [
        ("ייעוד", "חבילת מטא-דאטה לפרסום."),
        ("כלים", "Ahrefs (serp-overview), Read, Write"),
        ("פלט", "seo-package.md — כותרת/תיאור/תגיות, made-for-kids=true, בלי קישורים"),
        ("הצלחה", "מטא-דאטה תואמת-COPPA, כותרת עם CTR גבוה."),
    ]),
    (8, "עורך הווידאו", "video-editor", [
        ("ייעוד", "הרכבה סופית: וידאו + קריינות + מוזיקה."),
        ("כלים", "Adobe video_render / video_metadata / video_resize; upscale_video"),
        ("קלט", "video-brief.md + tts-brief.md + מוזיקת רקע (-12db)"),
        ("פלט", "assembled-video-url.txt; end card 5-10ש' ל-Long"),
        ("הצלחה", "סנכרון אודיו-וידאו, יחס מסך נכון, MP4 נגיש."),
    ]),
    (9, "מפקח הבטיחות", "safety-inspector", [
        ("ייעוד", "שער בטיחות לילדים עם זכות וטו."),
        ("כלים", "Read, Write"),
        ("קלט", "כל פלטי videos/[slug]/ + inspector-checklist + kids-safety-policy"),
        ("פלט", "inspector-report.md (PASS/FAIL). FAIL => עצור, אל תעלה, דווח."),
        ("הצלחה", "אפס תוכן מפחיד/מסוכן עובר; כל הכללים מאומתים."),
    ]),
    (10, "מנהל ההפצה", "publisher", [
        ("ייעוד", "העלאה ליוטיוב + שער אישור אנושי."),
        ("כלים", "YouTube Data API ⚠️ (videos.insert, playlistItems.insert), Gmail"),
        ("פלט", "youtube-payload.json. 3 ראשונות = private + מייל אישור"),
        ("הצלחה", "made-for-kids=true תמיד; אין פרסום בלי אישור בשלב הראשוני."),
    ]),
    (11, "אנליסט הנתונים", "analytics-analyst", [
        ("ייעוד", "דוח ביצועים שבועי."),
        ("כלים", "YouTube Data API ⚠️ (videos.list statistics), Write"),
        ("פלט", "analytics-snapshot.md + מייל. מסמן השלמה <40%; מחשב התקדמות ל-YPP"),
        ("הצלחה", "דוח מדויק, מזהה מגמות אמיתיות."),
    ]),
    (12, "מאמן הצוות", "team-coach", [
        ("ייעוד", "מנתח ביצועים ותפקוד הצוות, מציע שיפורים."),
        ("כלים", "Read, Write, Gmail"),
        ("קלט", "4 דוחות analytics-snapshot אחרונים + team-improvements.md"),
        ("כלל ברזל", "מציע, לא מיישם. כל שינוי דורש אישור. לא נוגע ב-credentials."),
        ("הצלחה", "הצעות מבוססות-נתונים שמשפרות retention/צמיחה."),
    ]),
]
for c in cards:
    agent_card(*c)

# ---------- Flow + recommendations ----------
pdf.add_page()
H2("זרימת ה-handoffs")
pdf.set_font("Dejavu", "", 9)
pdf.set_text_color(*INK)
flow = [
    "מפיק הסטודיו ← חוקר הטרנדים ← התסריטאי",
    "      ואז במקביל: המנהל האמנותי + מפיק הקריינות + אסטרטג ה-SEO",
    "      ← עורך הווידאו ← מפקח הבטיחות ← (PASS) מנהל ההפצה ← מפיק (סיכום)",
    "",
    "מחזור שבועי: מנהל ההפצה ← אנליסט הנתונים ← מאמן הצוות ← (הצעות) ← משתמש",
]
for l in flow:
    pdf.set_x(18)
    pdf.multi_cell(W, 6, rtl(l), align="R")
pdf.ln(2)

H2("המלצות האדריכל (שינויים מההצעה ההתחלתית)")
recs = [
    "1. שמירה על הפרדה מנהל-אמנותי ↔ עורך-וידאו: שלב 4a (Higgsfield) ושלב 5 (Adobe) שונים בכלים — עדיף שני סוכנים חדים.",
    "2. אין סוכן נפרד ל-Short: הוא נגזר מנושא ה-Long; אותו צוות מטפל בשניהם עם פרמטר יחס-מסך.",
    "3. תלות YouTube מסומנת בכנות (⚠️): למנהל ההפצה ולאנליסט אין כלי MCP ישיר ל-YouTube — תלויים ב-connector מ-setup. אפשר לגשר דרך Make/Routines.",
    "4. השמות העבריים תואמים לשמות הקוד הקיימים ב-SKILL — מעבר חלק ללא בלבול.",
]
for r in recs:
    pdf.set_x(18)
    pdf.set_font("Dejavu", "", 9.5)
    pdf.set_text_color(*INK)
    pdf.multi_cell(W, 5.6, rtl(r), align="R")
    pdf.ln(0.6)

H2("שאלות פתוחות לאישורך")
qs = [
    "1. גודל הצוות: לאשר את כל ה-12, או למזג (למשל מנהל-אמנותי + עורך לסוכן \"וידאו\" אחד)?",
    "2. YouTube: connector קיים, או שאתכנן גישור Make/Routines למנהל ההפצה + אנליסט?",
    "3. שמות: להשאיר שמות-תפקיד, או שתרצה שמות-דמות אישיים?",
]
for q in qs:
    pdf.set_x(18)
    pdf.set_font("Dejavu", "", 9.5)
    pdf.set_text_color(*INK)
    pdf.multi_cell(W, 5.6, rtl(q), align="R")
    pdf.ln(0.6)

os.makedirs("docs", exist_ok=True)
out = "docs/proposed-team-he.pdf"
pdf.output(out)
print("WROTE", out)
