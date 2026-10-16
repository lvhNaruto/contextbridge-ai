"""Build the 5-minute pitch deck: docs/contextbridge_pitch.pptx (python scripts/build_pitch_pptx.py)."""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "contextbridge_pitch.pptx"
BG = RGBColor(0x0B, 0x0F, 0x19)
CARD = RGBColor(0x15, 0x1B, 0x2B)
LINE = RGBColor(0x2A, 0x33, 0x4A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
MUTED = RGBColor(0x94, 0xA3, 0xB8)
INDIGO = RGBColor(0x81, 0x8C, 0xF8)
GREEN = RGBColor(0x34, 0xD3, 0x99)
RED = RGBColor(0xF8, 0x71, 0x71)
AMBER = RGBColor(0xFB, 0xBF, 0x24)
SKY = RGBColor(0x38, 0xBD, 0xF8)

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)


def text(slide, x, y, w, h, value, size=18, color=WHITE, bold=False, align=PP_ALIGN.LEFT):
    tf = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
    tf.word_wrap = True
    for i, line in enumerate(value.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        run = p.add_run()
        run.text = line
        run.font.size, run.font.bold, run.font.color.rgb, run.font.name = Pt(size), bold, color, "Segoe UI"
    return tf


def box(slide, x, y, w, h, fill=CARD, border=LINE):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.adjustments[0] = 0.08
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = border
    shape.shadow.inherit = False
    return shape


def card(slide, x, y, w, h, title, body, accent=INDIGO, title_size=20, body_size=14):
    box(slide, x, y, w, h, border=accent)
    text(slide, x + 0.25, y + 0.2, w - 0.5, 0.6, title, title_size, accent, bold=True)
    text(slide, x + 0.25, y + 0.85, w - 0.5, h - 1.0, body, body_size, MUTED)


def new_slide(tag, title, notes, number):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = BG
    text(slide, 0.6, 0.35, 8, 0.4, tag.upper(), 12, INDIGO, bold=True)
    if number:
        text(slide, 11.2, 0.35, 1.5, 0.4, f"{number:02d} / 06", 12, MUTED, align=PP_ALIGN.RIGHT)
    if title:
        text(slide, 0.6, 0.75, 12.1, 1.0, title, 34, WHITE, bold=True)
    text(slide, 0.6, 7.0, 12.1, 0.3, "ContextBridge  ·  Team Naruto  ·  AI Builder Cup 2026  ·  contextbridge-web-c5ltxo3mkq-uc.a.run.app", 10, MUTED)
    slide.notes_slide.notes_text_frame.text = notes
    return slide


# 1 — Evidence
s = new_slide("Evidence", "The problem is real, and it is measured", (
    "[~30s] Open with the hook: \"Raise your hand if you've ever scrubbed a 45-minute video to find the "
    "10 seconds you needed.\" Then point at two or three of these, not all five.\n"
    "Key line: \"People already learn from video. They don't finish, they don't trust AI answers, "
    "and most new learners in India don't learn in English.\""
), 1)
evidence = [
    ("51%", "of YouTube users say it is 'very important' for learning how to do things they haven't done before.", "Pew Research Center, 2018", GREEN),
    ("3.13%", "completion rate for MITx / HarvardX online courses (2017-18).", "Reich & Ruipérez-Valiente, Science, 2019", RED),
    ("66%", "of developers are frustrated by AI answers that are 'almost right, but not quite'; 46% distrust AI accuracy.", "Stack Overflow Developer Survey, 2025", AMBER),
    ("9 in 10", "new internet users in India are likely to be Indian-language users.", "KPMG & Google, 'Indian Languages', 2017", SKY),
    ("1.8 h/day", "the average knowledge worker spends searching for and gathering information.", "McKinsey Global Institute, 2012", INDIGO),
]
for i, (stat, body, source, accent) in enumerate(evidence):
    x, y = (0.6 + (i % 3) * 4.12, 1.9) if i < 3 else (0.6 + (i - 3) * 4.12 + 2.06, 4.45)
    box(s, x, y, 3.9, 2.35, border=accent)
    text(s, x + 0.25, y + 0.15, 3.4, 0.8, stat, 34, accent, bold=True)
    text(s, x + 0.25, y + 0.95, 3.4, 1.0, body, 13, WHITE)
    text(s, x + 0.25, y + 1.9, 3.4, 0.4, source, 10, MUTED)

# 3 — Cost
s = new_slide("Cost of the problem", "Lost minutes add up to lost money", (
    "[~25s] Walk the math left to right. Be explicit it's a model: \"Take a 50-person engineering team "
    "that onboards from recorded trainings. 10 lookups a day, about 3 minutes each to scrub and re-watch. "
    "That's 6,000 hours a year - roughly $300,000 - spent finding things that were already recorded.\"\n"
    "Then the hidden cost: a confident wrong AI answer means rework, bugs and lost trust."
), 2)
steps = [("50", "engineers"), ("× 10", "lookups / day"), ("× 3 min", "scrub & re-watch"), ("× 240", "work days")]
for i, (v, label) in enumerate(steps):
    x = 0.6 + i * 2.35
    box(s, x, 2.0, 2.15, 1.6)
    text(s, x, 2.15, 2.15, 0.8, v, 32, WHITE, bold=True, align=PP_ALIGN.CENTER)
    text(s, x, 2.95, 2.15, 0.5, label, 13, MUTED, align=PP_ALIGN.CENTER)
box(s, 10.05, 2.0, 2.7, 1.6, fill=RGBColor(0x2A, 0x12, 0x16), border=RED)
text(s, 10.05, 2.05, 2.7, 0.7, "6,000 h", 32, RED, bold=True, align=PP_ALIGN.CENTER)
text(s, 10.05, 2.75, 2.7, 0.8, "≈ $300,000 / year\nat $50 / hour", 14, WHITE, align=PP_ALIGN.CENTER)
text(s, 0.6, 3.75, 12, 0.4, "Illustrative model - our assumptions, for one 50-person team.", 11, MUTED)
card(s, 0.6, 4.4, 3.9, 2.3, "Time", "Minutes per lookup, every day, for every learner. Most give up before the end (3% finish).", AMBER)
card(s, 4.72, 4.4, 3.9, 2.3, "Wrong answers", "A confident but invented AI quote means rework, bugs and wrong decisions.", RED)
card(s, 8.84, 4.4, 3.9, 2.3, "Lost learners", "Millions who think in Hindi / Hinglish are left out of English-only video.", SKY)

# 4 — Solution
s = new_slide("The solution", "Ask your video. Get the answer, with proof.", (
    "[~30s] Zero jargon. \"You pick a video. You ask a question - typing or speaking, in English or Hindi. "
    "ContextBridge answers only from that video, shows you the exact words, and one click jumps the video "
    "to that moment. If the video doesn't cover it, it tells you honestly, and can look it up on the web - "
    "clearly labeled as 'beyond this video'.\" Then: \"Let me show you.\"\n"
    "[~2:00] LIVE DEMO: 1. Landing page -> 'Try the demo lesson'. 2. Ask an in-video question -> point at the "
    "'Verified' badge + quote -> click 'Jump to' -> video seeks, transcript scrolls. 3. Click an 'Explore from "
    "here' chip. 4. Ask something NOT in the video -> honest 'Beyond this video' card with web sources. "
    "5. Hindi / Hinglish voice question -> Hindi answer, read aloud. Backup video (2:42): https://youtu.be/Tf0LZE93oxw"
), 3)
box(s, 0.6, 1.85, 8.1, 4.9)
text(s, 0.9, 2.0, 7.5, 0.4, "Demo lesson: Gemini lesson plan template · Google for Education", 12, MUTED)
box(s, 3.6, 2.5, 4.85, 0.65, fill=RGBColor(0x31, 0x2E, 0x81), border=INDIGO)
text(s, 3.75, 2.6, 4.6, 0.5, "What does the Gemini draft include?", 16, WHITE, align=PP_ALIGN.RIGHT)
box(s, 0.9, 3.35, 7.55, 3.2, fill=BG)
text(s, 1.15, 3.5, 7.1, 0.5, "It drafts objectives, steps to follow, and ways to adapt the lesson for beginners and advanced learners.", 15, WHITE)
box(s, 1.15, 4.3, 3.3, 0.45, fill=RGBColor(0x0E, 0x2A, 0x22), border=GREEN)
text(s, 1.15, 4.33, 3.3, 0.4, "✓ Verified from this video · 100%", 13, GREEN, bold=True, align=PP_ALIGN.CENTER)
box(s, 4.65, 4.3, 1.9, 0.45, fill=RGBColor(0x7C, 0x3A, 0xED), border=INDIGO)
text(s, 4.65, 4.33, 1.9, 0.4, "▶ Jump to 00:21", 13, WHITE, bold=True, align=PP_ALIGN.CENTER)
text(s, 1.15, 4.95, 7.1, 1.0, "\u201cGemini quickly generates a draft that includes objectives, steps to follow, and even ways to adapt the material for students who are new to the topic and advanced learners.\u201d", 13, MUTED)
text(s, 1.15, 5.95, 7.1, 0.4, "Explore from here →   How does the coach share the template with educators?", 12, INDIGO)
for i, (title, body, accent) in enumerate([
    ("1. Ask", "Type or speak a question, in English, Hindi or Hinglish.", INDIGO),
    ("2. See the proof", "The exact words from the video, with a 'Verified from this video' badge.", GREEN),
    ("3. Jump there", "One click plays the video at that exact second.", AMBER),
    ("4. Honest edges", "Not in the video? It says so, and can search the web, clearly labeled.", SKY),
]):
    y = 1.85 + i * 1.27
    box(s, 8.95, y, 3.8, 1.15, border=accent)
    text(s, 9.15, y + 0.08, 3.4, 0.4, title, 16, accent, bold=True)
    text(s, 9.15, y + 0.48, 3.4, 0.7, body, 12, MUTED)
# 5 — Before / After
s = new_slide("Before & after", "The difference is stark", (
    "[~25s] Read only the big numbers: \"Finding the moment: minutes before, seconds after. "
    "Invented quotes: unknown before, zero after - measured on our 25-question test set. "
    "For our 50-person team model: 6,000 hours down to about 400.\"\n"
    "Measured numbers come from context/eval_results.json (25 cases: 100% timestamp accuracy, 100% grounded, "
    "0% unsupported, 6.2s average). 'Before' values and the team model are estimates."
), 4)
rows = [
    ("Find the exact moment", "~3 min of scrubbing", "~6 s, one click"),
    ("Answers with invented quotes", "Unverifiable", "0%  (25-case eval)"),
    ("Correct timestamp", "Guesswork", "100%  (25-case eval)"),
    ("Languages", "English only", "English · Hindi · Hinglish + voice"),
    ("50-person team, per year", "6,000 h  ≈ $300,000", "~400 h  ≈ $20,000"),
]
text(s, 4.6, 1.75, 3.9, 0.4, "BEFORE", 14, RED, bold=True, align=PP_ALIGN.CENTER)
text(s, 8.75, 1.75, 4.0, 0.4, "AFTER - CONTEXTBRIDGE", 14, GREEN, bold=True, align=PP_ALIGN.CENTER)
for i, (label, before, after) in enumerate(rows):
    y = 2.2 + i * 0.86
    text(s, 0.6, y + 0.2, 3.9, 0.6, label, 16, WHITE, bold=True)
    box(s, 4.6, y, 3.9, 0.78, fill=RGBColor(0x2A, 0x12, 0x16), border=RED)
    text(s, 4.6, y + 0.17, 3.9, 0.5, before, 17, RED, align=PP_ALIGN.CENTER)
    box(s, 8.75, y, 4.0, 0.78, fill=RGBColor(0x0E, 0x2A, 0x22), border=GREEN)
    text(s, 8.75, y + 0.17, 4.0, 0.5, after, 17, GREEN, bold=True, align=PP_ALIGN.CENTER)
text(s, 0.6, 6.6, 12, 0.3, "Measured: 25-case evaluation on the demo lesson. Before values and team cost: estimates (10 lookups/day, $50/h).", 10, MUTED)

# 6 — Architecture
s = new_slide("Architecture", "Simple, robust pipeline + a self-checking AI agent", (
    "[~20s, optional - skip if short on time] \"A video is analysed once into a validated index. "
    "Every question runs a small agent: find the evidence, draft an answer, then CHECK that the quote really "
    "appears in the transcript and the timestamp is real. If the check fails it retries once, then says "
    "'not found' instead of inventing. Web research is a separate, labeled branch. All on Google Cloud Run "
    "with Gemini 2.5 Flash.\""
), 5)
text(s, 0.6, 1.7, 6, 0.4, "1 · INGEST ONCE (data pipeline)", 14, INDIGO, bold=True)
for i, label in enumerate(["Upload video", "Gemini 2.5 Flash\nmultimodal analysis", "Schema\nvalidation gate", "Stored index\nSQLite + GCS"]):
    x = 0.6 + i * 3.1
    box(s, x, 2.15, 2.7, 1.0, border=INDIGO)
    text(s, x, 2.3, 2.7, 0.8, label, 14, WHITE, bold=True, align=PP_ALIGN.CENTER)
    if i < 3:
        text(s, x + 2.7, 2.35, 0.4, 0.5, "→", 22, INDIGO, align=PP_ALIGN.CENTER)
text(s, 0.6, 3.45, 8, 0.4, "2 · EVERY QUESTION (AI orchestration: ≤ 2 model calls, 1 retry)", 14, GREEN, bold=True)
for i, label in enumerate(["Question\n(text / voice)", "Find evidence\nin the index", "Draft answer\n(Gemini)", "Verify quote +\ntimestamp", "Answer + proof\nor honest 'not found'"]):
    x = 0.6 + i * 2.48
    box(s, x, 3.9, 2.1, 1.05, border=GREEN)
    text(s, x, 4.02, 2.1, 0.9, label, 13, WHITE, bold=True, align=PP_ALIGN.CENTER)
    if i < 4:
        text(s, x + 2.1, 4.1, 0.38, 0.5, "→", 22, GREEN, align=PP_ALIGN.CENTER)
card(s, 0.6, 5.25, 3.9, 1.5, "Separate web branch", "Google Search grounding only when the video lacks the answer - always labeled.", SKY, 16, 12)
card(s, 4.72, 5.25, 3.9, 1.5, "Anti-fabrication gate", "Quotes must appear in the transcript; timestamps must be inside the video.", AMBER, 16, 12)
card(s, 8.84, 5.25, 3.9, 1.5, "Production-ready", "Stateless FastAPI + Next.js on Google Cloud Run, Vertex AI, eval harness.", INDIGO, 16, 12)

# 7 — Team
s = new_slide("Team & execution", "Team Naruto: enterprise engineering that ships", (
    "[~20s] \"I'm Mohit Singh, leading Team Naruto, with Shanu Gupta on frontend. I bring 10+ years of "
    "enterprise engineering - systems that have to be reliable, measured and secure. That's why ContextBridge "
    "is already live on Google Cloud, tested, and measured - not a mock-up.\" "
    "Close: \"Not a tutor - a compass. Every answer anchored to your video, with proof. Thank you.\""
), 6)
card(s, 0.6, 1.9, 5.9, 2.4, "Mohit Singh - Team Leader", "10+ years of enterprise engineering.\nReliable, secure, production systems.\nmohitsinghgeek@gmail.com", GREEN, 22, 15)
card(s, 6.85, 1.9, 5.9, 2.4, "Shanu Gupta - Frontend Designer", "Designs the screens a learner uses:\nthe lesson, the proof, and the voice.", INDIGO, 22, 15)
for i, (v, label) in enumerate([("Live", "on Google Cloud Run"), ("25 / 25", "eval cases grounded"), ("0%", "invented answers"), ("EN · HI", "voice in & out")]):
    x = 0.6 + i * 3.1
    box(s, x, 4.6, 2.85, 1.35)
    text(s, x, 4.7, 2.85, 0.7, v, 28, GREEN, bold=True, align=PP_ALIGN.CENTER)
    text(s, x, 5.4, 2.85, 0.4, label, 13, MUTED, align=PP_ALIGN.CENTER)
text(s, 0.6, 6.2, 12.1, 0.6, "Not a tutor. A compass - every answer anchored to your video, with proof.", 20, WHITE, bold=True, align=PP_ALIGN.CENTER)

prs.save(OUT)
print(f"saved {OUT}")
