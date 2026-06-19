#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the Nature Kids Studio agent-team PLAN as a Hebrew (RTL) PDF."""
from fpdf import FPDF
from bidi.algorithm import get_display

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SAND = (250, 247, 240)
INK = (40, 40, 45)
GREEN = (34, 110, 64)
LEAF = (60, 140, 80)
GREY = (110, 110, 115)
LINE = (210, 205, 195)
BOXBG = (240, 246, 240)


def rtl(s: str) -> str:
    return get_display(s)


class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-12)
        self.set_font("Dejavu", "", 8)
        self.set_text_color(*GREY)
        self.cell(0, 8, rtl(f"טבע לילדים · תוכנית צוות הסוכנים · עמ' {self.page_no()}"),
                  align="C")


pdf = PDF(format="A4")
pdf.set_auto_page_break(auto=True, margin=18)
pdf.add_font("Dejavu", "", f"{FONT_DIR}/DejaVuSans.ttf")
pdf.add_font("Dejavu", "B", f"{FONT_DIR}/DejaVuSans-Bold.ttf")
pdf.set_margins(18, 18, 18)
W = 210 - 36  # usable width


def H1(t):
    pdf.ln(2)
    pdf.set_font("Dejavu", "B", 18)
    pdf.set_text_color(*GREEN)
    pdf.multi_cell(W, 9, rtl(t), align="R")
    pdf.ln(1)


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


def para(t, size=10.5, color=INK):
    pdf.set_font("Dejavu", "", size)
    pdf.set_text_color(*color)
    pdf.multi_cell(W, 6, rtl(t), align="R")
    pdf.ln(0.5)


def bullet(t, size=10.5):
    pdf.set_font("Dejavu", "", size)
    pdf.set_text_color(*INK)
    pdf.multi_cell(W, 5.8, rtl(t + " •"), align="R")
    pdf.ln(0.3)


def box(lines, title=None):
    pdf.set_fill_color(*BOXBG)
    pdf.set_draw_color(*LEAF)
    pdf.set_line_width(0.4)
    start = pdf.get_y()
    pdf.ln(1)
    if title:
        pdf.set_font("Dejavu", "B", 11)
        pdf.set_text_color(*GREEN)
        pdf.set_x(20)
        pdf.multi_cell(W - 4, 6.5, rtl(title), align="R")
    pdf.set_font("Dejavu", "", 10)
    pdf.set_text_color(*INK)
    for l in lines:
        pdf.set_x(20)
        pdf.multi_cell(W - 4, 5.6, rtl(l), align="R")
    pdf.ln(1)
    end = pdf.get_y()
    pdf.rect(18, start, W, end - start, style="D")
    pdf.ln(2)


# ---------- Cover ----------
pdf.add_page()
pdf.set_fill_color(*GREEN)
pdf.rect(0, 0, 210, 70, style="F")
pdf.set_y(22)
pdf.set_font("Dejavu", "B", 26)
pdf.set_text_color(255, 255, 255)
pdf.multi_cell(W, 12, rtl("צוות הסוכנים של \"טבע לילדים\""), align="R")
pdf.set_font("Dejavu", "", 13)
pdf.multi_cell(W, 8, rtl("תוכנית בנייה — אדריכל קודם, ואז הצוות המלא"), align="R")
pdf.set_y(78)
pdf.set_font("Dejavu", "", 10)
pdf.set_text_color(*GREY)
pdf.multi_cell(W, 6, rtl("מסמך לסקירה ואישור · 19 ביוני 2026 · כל הסוכנים על מודל Opus"),
               align="R")
pdf.ln(4)

H2("בקצרה")
box([
    "בנינו עד כה skill יחיד — \"מוח\" אחד שעושה הכל. אתה רוצה צוות סוכנים אמיתי:",
    "לכל תפקיד סוכן ייעודי משלו, עם ההקשר, הכלים והמומחיות שלו.",
    "בנוסף: סוכן-אדריכל שמגייס ומציע את הצוות, ומנגנון שמשפר את הצוות לאורך זמן.",
    "",
    "סדר הבנייה שבחרת: אדריכל קודם ← הוא מציע צוות ← אתה מאשר ← בונים את השאר.",
    "המודל: כולם על Opus (איכות מקסימלית).",
], title="מה משתנה ולמה")

# ---------- How agents work ----------
pdf.add_page()
H1("איך סוכנים עובדים ב-Claude Code")
para("חשוב להבין לפני אישור — כדי שהציפיות יהיו מדויקות:")
bullet("סוכן = קובץ ב-.claude/agents/NAME.md עם הגדרה (שם, תיאור, כלים, מודל) + הוראות התפקיד.")
bullet("כל סוכן רץ בחלון הקשר (context) נפרד עם הכלים והמומחיות שלו — זו ההפרדה שאתה רוצה.")
bullet("מגבלה אמיתית (בכנות): סוכן לא יכול להפעיל סוכן אחר ישירות. התיאום נעשה ע\"י המפיק (orchestrator).")
bullet("הסוכנים \"מדברים\" ביניהם דרך קבצים משותפים בתיקיית הריצה videos/[slug]/ — כל אחד קורא את פלט הקודם וכותב את שלו.")
bullet("ה-skill הקיים nature-kids-studio נשאר — הוא הופך ל\"ספר הנהלים\" + מאגר הידע שכל סוכן קורא ממנו.")

H2("ארכיטקטורת הצוות (הצעה התחלתית)")
para("זו נקודת המוצא בלבד. הרשימה הסופית תיקבע ע\"י אדריכל הצוות ותאושר על ידך (שלב 3).",
     color=GREY)
para("לכל סוכן שם עברי (זהות הצוות) + מזהה טכני באנגלית שמשמש את הקובץ וההפעלה.",
     color=GREY)

# ---------- Roster table ----------
rows = [
    ("#", "שם עברי", "מזהה טכני", "ייעוד"),
    ("1", "אדריכל הצוות", "team-architect", "חוקר ומציע את הצוות"),
    ("2", "מפיק הסטודיו", "studio-orchestrator", "מנהל ומאציל את כל הריצה"),
    ("3", "חוקר הטרנדים", "trend-researcher", "מחקר מילות מפתח ונושאים"),
    ("4", "התסריטאי", "scriptwriter", "כתיבת תסריט Short/Long"),
    ("5", "המנהל האמנותי", "art-director", "יצירת וידאו וויזואל"),
    ("6", "מפיק הקריינות", "voice-producer", "קריינות TTS"),
    ("7", "עורך הווידאו", "video-editor", "הרכבת הסרטון הסופי"),
    ("8", "מפקח הבטיחות", "safety-inspector", "בדיקת בטיחות + וטו"),
    ("9", "אסטרטג ה-SEO", "seo-strategist", "מטא-דאטה ל-SEO"),
    ("10", "מנהל ההפצה", "publisher", "העלאה + אישור אנושי"),
    ("11", "אנליסט הנתונים", "analytics-analyst", "דוח ביצועים שבועי"),
    ("12", "מאמן הצוות", "team-coach", "הצעות שיפור לצוות"),
]
# column widths. Visual order RTL: # | שם עברי | מזהה טכני | ייעוד
cw = [10, 40, 46, 78]  # sums to 174 = W
for i, (c0, c1, c2, c3) in enumerate(rows):
    if i == 0:
        pdf.set_fill_color(*GREEN)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Dejavu", "B", 9.5)
    else:
        pdf.set_fill_color(*(SAND if i % 2 else (255, 255, 255)))
        pdf.set_text_color(*INK)
        pdf.set_font("Dejavu", "", 9)
    pdf.set_x(18)
    # left-to-right render so RTL reading order is: # | שם עברי | מזהה | ייעוד
    pdf.cell(cw[3], 7, rtl(c3), border=0, fill=True, align="R")
    pdf.cell(cw[2], 7, (c2 if i else rtl(c2)), border=0, fill=True, align="R")
    pdf.cell(cw[1], 7, rtl(c1), border=0, fill=True, align="R")
    pdf.cell(cw[0], 7, rtl(c0), border=0, fill=True, align="C")
    pdf.ln(7)
pdf.ln(2)

# ---------- Build sequence ----------
pdf.add_page()
H1("סדר הבנייה (אדריכל קודם)")
box(["מיד עם אישורך אפיק את התוכנית הזו כ-PDF בעברית (המסמך שאתה קורא).",
     "לא בונה כלום עד שתסתכל ותאשר."], title="שלב 0 — PDF של התוכנית")
para("שלב 1 — בניית אדריכל הצוות (team-architect) בלבד, על Opus: סוכן יחיד שמתמחה בעיצוב צוותים.")
para("שלב 2 — הרצת אדריכל הצוות: חוקר (רשת + הריפו + הידע הקיים) ומפיק PROPOSED-TEAM.md — הצעת צוות מפורטת: לכל סוכן שם עברי, ייעוד, כלים, מודל, קלט/פלט, handoffs ומדדי הצלחה.")
box(["אמיר את הצעת האדריכל ל-PDF בעברית ואשלח.",
     "תוכל לשנות / להוסיף / להסיר סוכנים. רק אחרי אישורך ממשיכים."],
    title="שלב 3 — עצירה לאישורך")
para("שלב 4 — בניית כל הסוכנים שאושרו ב-.claude/agents/ (כולם Opus).")
para("שלב 5 — חיווט: עדכון ה-skill כך שהמפיק יאציל כל שלב לסוכן המתאים; הגדרת ה-handoffs וקבצי ה-RUN-LOG.")
para("שלב 6 — שיפור הצוות: אנליסט הנתונים (analytics-analyst) + מאמן הצוות (team-coach) פועלים שבועית ומציעים שדרוגים — הצעות בלבד, באישורך. זה ה\"נשפר את הצוות\".")

H2("שערי בקרה אנושיים (נשמרים)")
bullet("אישור רשימת הצוות — אחרי שהאדריכל מציע (שלב 3).")
bullet("מפקח הבטיחות (safety-inspector) — וטו אוטומטי על תוכן שאינו בטוח לילדים.")
bullet("3 העלאות ראשונות — private + מייל אישור לפני פרסום.")
bullet("שינויי מאמן הצוות (team-coach) — הצעות בלבד, רק מה שתאשר נכנס.")
bullet("סודות (מפתחות/טוקנים) — משתני סביבה בלבד, אף פעם לא בגיט.")

H2("הצעד הבא")
para("באישור התוכנית: (1) אפיק את ה-PDF הזה לסקירה; (2) אם תאשר — אבנה את אדריכל הצוות (team-architect), אריץ אותו, ואחזיר לך הצעת-צוות כ-PDF בעברית לאישור לפני בניית שאר הסוכנים.")

import os
os.makedirs("docs", exist_ok=True)
out = "docs/team-plan-he.pdf"
pdf.output(out)
print("WROTE", out)
