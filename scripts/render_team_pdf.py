#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the final Nature Kids Studio team as a polished Hebrew (RTL) PDF."""
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
        self.cell(0, 8, rtl(f"טבע לילדים · צוות הסוכנים · עמ' {self.page_no()}"), align="C")


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


# ---------- Cover ----------
pdf.add_page()
pdf.set_fill_color(*GREEN)
pdf.rect(0, 0, 210, 58, style="F")
pdf.set_y(17)
pdf.set_font("Dejavu", "B", 25)
pdf.set_text_color(255, 255, 255)
pdf.multi_cell(W, 12, rtl("צוות הסוכנים"), align="R")
pdf.set_font("Dejavu", "", 13)
pdf.multi_cell(W, 8, rtl("Nature Kids Studio · \"טבע לילדים\""), align="R")
pdf.set_y(64)
pdf.set_font("Dejavu", "", 9.5)
pdf.set_text_color(*GREY)
pdf.multi_cell(W, 5.4, rtl("12 סוכנים מתמחים · כולם על מודל Opus · דמות מנחה בסרטונים: Pip הינשוף"),
               align="R")
pdf.ln(3)

# ---------- Roster grouped ----------
groups = [
    ("מנהיגות", [
        ("בּוֹני", "בונה", "אדריכל הצוות", "team-architect", "חוקר ומציע את הרכב הצוות"),
        ("מאיה", "דבורה", "מפיק הסטודיו", "studio-orchestrator", "מנהל ומאציל את כל הריצה"),
    ]),
    ("קו הייצור", [
        ("רוני", "שועל", "חוקר הטרנדים", "trend-researcher", "מחקר מילות מפתח ונושאים"),
        ("זמיר", "ציפור", "התסריטאי", "scriptwriter", "כתיבת תסריט Short/Long"),
        ("טל", "טווס", "המנהל האמנותי", "art-director", "יצירת וידאו (Seedance 2.0)"),
        ("קולי", "צרצר", "מפיק הקריינות", "voice-producer", "קריינות TTS בקול הקבוע"),
        ("עֵדֶן", "סנאי", "עורך הווידאו", "video-editor", "הרכבת הסרטון הסופי"),
    ]),
    ("שערים", [
        ("נמי", "נמלה", "אסטרטג ה-SEO", "seo-strategist", "מטא-דאטה ל-SEO + made-for-kids"),
        ("שומי", "דוב", "מפקח הבטיחות", "safety-inspector", "שער בטיחות לילדים — וטו"),
        ("דפנה", "יונה", "מנהל ההפצה", "publisher", "העלאה + אישור אנושי"),
    ]),
    ("שיפור מתמשך", [
        ("טוביה", "חפרפרת", "אנליסט הנתונים", "analytics-analyst", "דוח ביצועים שבועי"),
        ("אלון", "פיל", "מאמן הצוות", "team-coach", "הצעות שיפור לצוות"),
    ]),
]

cw = [56, 44, 74]  # role | character | mission  (RTL: character | role | mission)
for title, members in groups:
    H2(title)
    for he, animal, role, slug, mission in members:
        pdf.set_fill_color(*CARDBG)
        pdf.set_draw_color(*LEAF)
        pdf.set_line_width(0.3)
        start = pdf.get_y()
        pdf.ln(1)
        # line 1: character (bold) + role
        pdf.set_x(20)
        pdf.set_font("Dejavu", "B", 11)
        pdf.set_text_color(*GREEN)
        pdf.cell(W - 4, 6, rtl(f"{he} ({animal}) — {role}"), align="R")
        pdf.ln(6)
        # line 2: mission + slug
        pdf.set_x(20)
        pdf.set_font("Dejavu", "", 9)
        pdf.set_text_color(*INK)
        pdf.cell(W - 4, 5, rtl(f"{mission}"), align="R")
        pdf.ln(4.6)
        pdf.set_x(20)
        pdf.set_font("Dejavu", "", 8)
        pdf.set_text_color(*GREY)
        pdf.cell(W - 4, 4.5, slug, align="R")
        pdf.ln(5)
        end = pdf.get_y()
        pdf.rect(18, start, W, end - start, style="D")
        pdf.ln(1.6)

# ---------- Flow ----------
pdf.add_page()
H2("זרימת העבודה (handoffs)")
pdf.set_font("Dejavu", "", 10)
pdf.set_text_color(*INK)
flow = [
    "מאיה (מפיק) בוחרת נושא ופותחת תיקיית ריצה.",
    "",
    "מאיה ← רוני (מחקר) ← זמיר (תסריט)",
    "        ואז במקביל: טל (וידאו) + קולי (קריינות) + נמי (SEO)",
    "        ← עֵדֶן (הרכבה) ← שומי (בטיחות, וטו)",
    "        ← (PASS) דפנה (העלאה) ← מאיה (סיכום)",
    "",
    "מחזור שבועי: דפנה ← טוביה (אנליטיקס) ← אלון (קואצ') ← הצעות ← דניאל",
]
for l in flow:
    pdf.set_x(18)
    pdf.multi_cell(W, 6.2, rtl(l), align="R")
pdf.ln(2)

H2("עקרונות הצוות")
for p in [
    "כל סוכן רץ בהקשר נפרד עם הכלים והמומחיות שלו; התיאום דרך קבצים משותפים.",
    "מפקח הבטיחות (שומי) הוא שער עם זכות וטו — אין העלאה לפני PASS.",
    "3 העלאות ראשונות = private + מייל אישור לדניאל.",
    "מאמן הצוות (אלון) מציע שיפורים בלבד — כל שינוי דורש אישור.",
    "ה-skill nature-kids-studio הוא ספר הנהלים ומאגר הידע של כל הצוות.",
]:
    pdf.set_x(18)
    pdf.set_font("Dejavu", "", 9.5)
    pdf.set_text_color(*INK)
    pdf.multi_cell(W, 5.6, rtl(p + " •"), align="R")
    pdf.ln(0.3)

os.makedirs("docs", exist_ok=True)
out = "docs/team-he.pdf"
pdf.output(out)
print("WROTE", out)
