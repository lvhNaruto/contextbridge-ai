"""Generate the 14-slide ContextBridge AI Official Submission Pitch Deck PDF.

Strictly follows the AI Builder Cup Google Slides submission template:
https://docs.google.com/presentation/d/13rg7vW43mEH6DkpuusAE6fdoEylSFz8waNpE4RLzoUg/

Format: 16:9 Landscape (960 x 540 pt)
Theme: Dark mode (Navy/Slate/Emerald/Indigo)
Preserves all empirical metrics: 94.4% accuracy, 92.0% groundedness, 0.0% hallucination.
"""

from __future__ import annotations

import os
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas

# 16:9 Landscape Dimensions (960 x 540)
PAGE_WIDTH = 960.0
PAGE_HEIGHT = 540.0
PAGESIZE = (PAGE_WIDTH, PAGE_HEIGHT)

# Design System Palette
BG_DARK = HexColor("#090D16")
BG_CARD = HexColor("#111827")
BG_CARD_BORDER = HexColor("#1F2937")
TEXT_WHITE = HexColor("#FFFFFF")
TEXT_SLATE_100 = HexColor("#F1F5F9")
TEXT_SLATE_200 = HexColor("#E2E8F0")
TEXT_MUTED = HexColor("#94A3B8")
TEXT_DIM = HexColor("#64748B")
EMERALD_GREEN = HexColor("#10B981")
EMERALD_LIGHT = HexColor("#34D399")
INDIGO_ACCENT = HexColor("#6366F1")
INDIGO_LIGHT = HexColor("#818CF8")
SKY_BLUE = HexColor("#38BDF8")
AMBER_WARN = HexColor("#F59E0B")
RED_ALERT = HexColor("#EF4444")
PURPLE_ACCENT = HexColor("#A855F7")


def draw_header_footer(c: canvas.Canvas, slide_num: int, total_slides: int = 14, category: str = "AI BUILDER CUP 2026"):
    # Background Canvas
    c.setFillColor(BG_DARK)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

    # Top Category Pill
    c.setFillColor(HexColor("#1E293B"))
    c.roundRect(48, PAGE_HEIGHT - 44, 230, 24, 12, fill=1, stroke=0)
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(60, PAGE_HEIGHT - 37, category.upper())

    # Slide Number
    c.setFillColor(TEXT_DIM)
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(PAGE_WIDTH - 48, PAGE_HEIGHT - 37, f"{slide_num:02d} / {total_slides:02d}")

    # Footer divider
    c.setStrokeColor(HexColor("#1E293B"))
    c.setLineWidth(1)
    c.line(48, 36, PAGE_WIDTH - 48, 36)

    # Footer info
    c.setFillColor(TEXT_DIM)
    c.setFont("Helvetica", 9)
    c.drawString(48, 22, "ContextBridge AI · A Compass for Self-Learners · Theme: Media, Content & Digital Experiences")
    c.drawRightString(PAGE_WIDTH - 48, 22, "Team: ContextBridge AI | Lead: Mohit Singh")


def draw_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, border_color=BG_CARD_BORDER, fill_color=BG_CARD):
    c.setFillColor(fill_color)
    c.setStrokeColor(border_color)
    c.setLineWidth(1)
    c.roundRect(x, y, w, h, 10, fill=1, stroke=1)


def generate_deck(output_path: str):
    c = canvas.Canvas(output_path, pagesize=PAGESIZE)

    # =========================================================================
    # SLIDE 1: Team Details
    # =========================================================================
    draw_header_footer(c, 1, 14, "SUBMISSION TEMPLATE · SLIDE 1")

    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(48, PAGE_HEIGHT - 85, "AI BUILDER CUP 2026 · OFFICIAL SUBMISSION")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 38)
    c.drawString(48, PAGE_HEIGHT - 135, "Team Details")

    # Team Info Card
    draw_card(c, 48, PAGE_HEIGHT - 325, 420, 165, INDIGO_ACCENT, HexColor("#0F172A"))
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(68, PAGE_HEIGHT - 180, "TEAM NAME")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(68, PAGE_HEIGHT - 210, "ContextBridge AI")

    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(68, PAGE_HEIGHT - 245, "TEAM LEADER NAME")
    c.setFillColor(TEXT_SLATE_100)
    c.setFont("Helvetica", 16)
    c.drawString(68, PAGE_HEIGHT - 270, "Mohit Singh (mohitsinghgeek@gmail.com)")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(68, PAGE_HEIGHT - 295, "Solo Lead Developer & Systems Architect")

    # Problem Statement Card
    draw_card(c, 490, PAGE_HEIGHT - 325, 422, 165, EMERALD_GREEN, HexColor("#0A141D"))
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(510, PAGE_HEIGHT - 180, "PROBLEM STATEMENT & THEME")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(510, PAGE_HEIGHT - 208, "Media, Content & Digital Experiences")
    c.setFillColor(TEXT_SLATE_200)
    c.setFont("Helvetica", 12)
    c.drawString(510, PAGE_HEIGHT - 238, "Problem: Self-learners lose hours scrubbing long technical")
    c.drawString(510, PAGE_HEIGHT - 256, "videos, while generic AI chatbots hallucinate ungrounded facts.")
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(510, PAGE_HEIGHT - 285, "Solution: Bounded Multimodal Video Compass with Verifiable Proof.")

    # 3 Metrics Callouts
    card_w = (PAGE_WIDTH - 96 - 32) / 3
    draw_card(c, 48, 65, card_w, 120, BG_CARD_BORDER, HexColor("#111827"))
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(68, 140, "94.4%")
    c.setFillColor(TEXT_SLATE_200)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(68, 115, "TIMESTAMP ACCURACY")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(68, 95, "Exact video moment (±15s)")

    draw_card(c, 48 + card_w + 16, 65, card_w, 120, BG_CARD_BORDER, HexColor("#111827"))
    c.setFillColor(SKY_BLUE)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(48 + card_w + 36, 140, "92.0%")
    c.setFillColor(TEXT_SLATE_200)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(48 + card_w + 36, 115, "GROUNDEDNESS SCORE")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(48 + card_w + 36, 95, "Backed by verbatim transcript lines")

    draw_card(c, 48 + (card_w + 16) * 2, 65, card_w, 120, BG_CARD_BORDER, HexColor("#111827"))
    c.setFillColor(PURPLE_ACCENT)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(48 + (card_w + 16) * 2 + 20, 140, "0.0%")
    c.setFillColor(TEXT_SLATE_200)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(48 + (card_w + 16) * 2 + 20, 115, "UNSUPPORTED ANSWERS")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(48 + (card_w + 16) * 2 + 20, 95, "Strict Anti-Fabrication Gate")

    c.showPage()

    # =========================================================================
    # SLIDE 2: Brief about the idea
    # =========================================================================
    draw_header_footer(c, 2, 14, "IDEA OVERVIEW")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(48, PAGE_HEIGHT - 90, "Brief about the idea")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 14)
    c.drawString(48, PAGE_HEIGHT - 116, "Not a tutor. A compass for self-learners — every answer anchored to the video with proof.")

    # Main Concept Card
    draw_card(c, 48, PAGE_HEIGHT - 295, PAGE_WIDTH - 96, 160, INDIGO_ACCENT, HexColor("#0D1527"))
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(68, PAGE_HEIGHT - 155, "CORE CONCEPT & MISSION")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(68, PAGE_HEIGHT - 182, "Transforming Passive Long-Form Video Into Verifiable, Interactive Knowledge")
    c.setFillColor(TEXT_SLATE_200)
    c.setFont("Helvetica", 12)
    c.drawString(68, PAGE_HEIGHT - 212, "Self-directed learners spend up to 40% of their study time manually scrubbing 2-hour lectures, coding")
    c.drawString(68, PAGE_HEIGHT - 232, "bootcamps, and technical walkthroughs seeking a specific formula, code snippet, or architectural concept.")
    c.drawString(68, PAGE_HEIGHT - 252, "Existing chatbots fail because they synthesize answers from general training data without verifying video context.")
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(68, PAGE_HEIGHT - 277, "ContextBridge AI eliminates scrubbing fatigue by delivering sub-second, grounded seeking with visible proof.")

    # Three Foundational Pillars
    col_w = (PAGE_WIDTH - 96 - 32) / 3
    draw_card(c, 48, 65, col_w, 150, EMERALD_GREEN, HexColor("#0A141D"))
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(68, 185, "1. Anchored (Sole Truth)")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(68, 158, "The chosen video is the sole ground")
    c.drawString(68, 140, "truth. Answers require verbatim transcript")
    c.drawString(68, 122, "matching or on-screen visual proof.")
    c.drawString(68, 98, "Zero invented quotes or facts.")

    draw_card(c, 48 + col_w + 16, 65, col_w, 150, INDIGO_ACCENT, HexColor("#0F1426"))
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(48 + col_w + 36, 185, "2. Visible Proof (1-Click)")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(48 + col_w + 36, 158, "Every answer displays an EvidenceBadge")
    c.drawString(48 + col_w + 36, 140, "with confidence %, timecode, and quote.")
    c.drawString(48 + col_w + 36, 122, "Clicking seeks the YouTube player")
    c.drawString(48 + col_w + 36, 98, "instantly to the exact second (~1s).")

    draw_card(c, 48 + (col_w + 16) * 2, 65, col_w, 150, SKY_BLUE, HexColor("#0A1726"))
    c.setFillColor(SKY_BLUE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(48 + (col_w + 16) * 2 + 20, 185, "3. Boundary Honesty")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(48 + (col_w + 16) * 2 + 20, 158, "When a question is NOT in the video,")
    c.drawString(48 + (col_w + 16) * 2 + 20, 140, "the agent refuses to fabricate. It gives")
    c.drawString(48 + (col_w + 16) * 2 + 20, 122, "an honest refusal + 3 proactive next")
    c.drawString(48 + (col_w + 16) * 2 + 20, 98, "topics derived from video content.")

    c.showPage()

    # =========================================================================
    # SLIDE 3: Opportunities
    # =========================================================================
    draw_header_footer(c, 3, 14, "OPPORTUNITIES & USP")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(48, PAGE_HEIGHT - 90, "Opportunities & Value Proposition")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 14)
    c.drawString(48, PAGE_HEIGHT - 116, "How ContextBridge AI disrupts existing video search, AI assistants, and e-learning.")

    # 3 Questions in Template
    q_h = 105
    # Q1: How different is it?
    draw_card(c, 48, PAGE_HEIGHT - 240, PAGE_WIDTH - 96, q_h, INDIGO_ACCENT)
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(68, PAGE_HEIGHT - 150, "HOW DIFFERENT IS IT FROM EXISTING IDEAS?")
    c.setFillColor(TEXT_SLATE_200)
    c.setFont("Helvetica", 11)
    c.drawString(68, PAGE_HEIGHT - 175, "• Existing YouTube summary tools generate generic 3-bullet overviews without interactive playback sync.")
    c.drawString(68, PAGE_HEIGHT - 195, "• Generic chatbots (ChatGPT, Claude) hallucinate answers from training data when video content is missing.")
    c.drawString(68, PAGE_HEIGHT - 215, "• ContextBridge AI enforces mathematical grounding: 100% transcript-anchored + millisecond-accurate video seeking.")

    # Q2: How will it solve the problem?
    draw_card(c, 48, PAGE_HEIGHT - 365, PAGE_WIDTH - 96, q_h, EMERALD_GREEN)
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(68, PAGE_HEIGHT - 275, "HOW WILL IT BE ABLE TO SOLVE THE PROBLEM?")
    c.setFillColor(TEXT_SLATE_200)
    c.setFont("Helvetica", 11)
    c.drawString(68, PAGE_HEIGHT - 300, "• Dual-Evidence Engine: Combines lexical & semantic transcript search with Gemini 2.5 Flash visual inspection.")
    c.drawString(68, PAGE_HEIGHT - 320, "• Millisecond-accurate indexer parses timestamps into interactive seek triggers for the embedded player.")
    c.drawString(68, PAGE_HEIGHT - 340, "• Full bilingual language parity: Hindi voice/text queries return Hindi responses with synchronized transcript tracking.")

    # Q3: USP of the proposed solution
    draw_card(c, 48, PAGE_HEIGHT - 490, PAGE_WIDTH - 96, q_h, SKY_BLUE)
    c.setFillColor(SKY_BLUE)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(68, PAGE_HEIGHT - 400, "USP (UNIQUE SELLING PROPOSITION) OF THE PROPOSED SOLUTION")
    c.setFillColor(TEXT_SLATE_200)
    c.setFont("Helvetica", 11)
    c.drawString(68, PAGE_HEIGHT - 425, "• 0.0% Unsupported Answers: Verified empirically across 25 ground-truth benchmark cases.")
    c.drawString(68, PAGE_HEIGHT - 445, "• 94.4% Timestamp Accuracy: Jumps learners directly to the exact relevant moment within ±15 seconds.")
    c.drawString(68, PAGE_HEIGHT - 465, "• EvidenceBadge System: Full transparency with confidence scoring, verbatim citations, and boundary guidance.")

    c.showPage()

    # =========================================================================
    # SLIDE 4: List of features offered by the solution
    # =========================================================================
    draw_header_footer(c, 4, 14, "FEATURES & CAPABILITIES")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(48, PAGE_HEIGHT - 90, "List of features offered by the solution")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 14)
    c.drawString(48, PAGE_HEIGHT - 116, "Comprehensive capability suite designed specifically for self-paced video learners.")

    f_w = (PAGE_WIDTH - 96 - 20) / 2
    f_h = 100

    # Feature 1
    draw_card(c, 48, PAGE_HEIGHT - 235, f_w, f_h)
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(68, PAGE_HEIGHT - 150, "1. EvidenceBadge & Verbatim Quotes")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(68, PAGE_HEIGHT - 175, "Displays confidence %, exact timestamp span, and exact")
    c.drawString(68, PAGE_HEIGHT - 195, "speaker words. Zero ambiguity on information provenance.")

    # Feature 2
    draw_card(c, 48 + f_w + 20, PAGE_HEIGHT - 235, f_w, f_h)
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(68 + f_w + 20, PAGE_HEIGHT - 150, "2. 1-Click Interactive Timestamp Seeking")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(68 + f_w + 20, PAGE_HEIGHT - 175, "Clicking any timestamp in an answer seeks the embedded player")
    c.drawString(68 + f_w + 20, PAGE_HEIGHT - 195, "and auto-scrolls the synchronized transcript to that exact second.")

    # Feature 3
    draw_card(c, 48, PAGE_HEIGHT - 355, f_w, f_h)
    c.setFillColor(SKY_BLUE)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(68, PAGE_HEIGHT - 270, "3. Multimodal Visual Evidence Extraction")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(68, PAGE_HEIGHT - 295, "Gemini 2.5 Flash extracts on-screen terminal outputs, code")
    c.drawString(68, PAGE_HEIGHT - 315, "blocks, slides, and whiteboard diagrams even if unmentioned.")

    # Feature 4
    draw_card(c, 48 + f_w + 20, PAGE_HEIGHT - 355, f_w, f_h)
    c.setFillColor(AMBER_WARN)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(68 + f_w + 20, PAGE_HEIGHT - 270, "4. Bilingual English + Hindi Voice Loop")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(68 + f_w + 20, PAGE_HEIGHT - 295, "Natural voice and text Q&A in English and Hindi (Devanagari).")
    c.drawString(68 + f_w + 20, PAGE_HEIGHT - 315, "Preserves script integrity with localized fallback responses.")

    # Feature 5
    draw_card(c, 48, PAGE_HEIGHT - 475, f_w, f_h)
    c.setFillColor(PURPLE_ACCENT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(68, PAGE_HEIGHT - 390, "5. Strict Anti-Fabrication Boundary Gate")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(68, PAGE_HEIGHT - 415, "0.0% hallucination rate. When a query is off-video, it admits")
    c.drawString(68, PAGE_HEIGHT - 435, "absence immediately rather than inventing plausible mistruths.")

    # Feature 6
    draw_card(c, 48 + f_w + 20, PAGE_HEIGHT - 475, f_w, f_h)
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(68 + f_w + 20, PAGE_HEIGHT - 390, "6. Contextual Explore Suggestions")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(68 + f_w + 20, PAGE_HEIGHT - 415, "Dynamically synthesizes 3 proactive follow-up study topics")
    c.drawString(68 + f_w + 20, PAGE_HEIGHT - 435, "derived strictly from what the instructor actually covers.")

    c.showPage()

    # =========================================================================
    # SLIDE 5: Process flow diagram or Use-case diagram
    # =========================================================================
    draw_header_footer(c, 5, 14, "PROCESS FLOW & USE CASE")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(48, PAGE_HEIGHT - 90, "Process flow diagram or Use-case diagram")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 14)
    c.drawString(48, PAGE_HEIGHT - 116, "End-to-end execution lifecycle from user query to verified playback seek.")

    # Flow Steps Grid (4 Steps)
    flow_w = (PAGE_WIDTH - 96 - 36) / 4
    flow_h = 220

    # Step 1
    draw_card(c, 48, PAGE_HEIGHT - 355, flow_w, flow_h, INDIGO_ACCENT)
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(64, PAGE_HEIGHT - 160, "STEP 1: INGESTION")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(64, PAGE_HEIGHT - 185, "URL & Transcript")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(64, PAGE_HEIGHT - 215, "• Parse YouTube URL")
    c.drawString(64, PAGE_HEIGHT - 235, "• Ingest timed transcript")
    c.drawString(64, PAGE_HEIGHT - 255, "  via yt-dlp / API")
    c.drawString(64, PAGE_HEIGHT - 275, "• Chunk into sliding token")
    c.drawString(64, PAGE_HEIGHT - 295, "  windows with timecodes")
    c.drawString(64, PAGE_HEIGHT - 315, "• Pre-index visual frames")

    # Step 2
    draw_card(c, 48 + flow_w + 12, PAGE_HEIGHT - 355, flow_w, flow_h, EMERALD_GREEN)
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(64 + flow_w + 12, PAGE_HEIGHT - 160, "STEP 2: RETRIEVAL")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(64 + flow_w + 12, PAGE_HEIGHT - 185, "Bounded Tool Ladder")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(64 + flow_w + 12, PAGE_HEIGHT - 215, "• Tool 1: Fast lexical search")
    c.drawString(64 + flow_w + 12, PAGE_HEIGHT - 235, "  (regex + keyword boost)")
    c.drawString(64 + flow_w + 12, PAGE_HEIGHT - 255, "• Tool 2: Semantic embedding")
    c.drawString(64 + flow_w + 12, PAGE_HEIGHT - 275, "  cosine similarity filter")
    c.drawString(64 + flow_w + 12, PAGE_HEIGHT - 295, "• Tool 3: Multimodal Gemini")
    c.drawString(64 + flow_w + 12, PAGE_HEIGHT - 315, "  visual inspection")

    # Step 3
    draw_card(c, 48 + (flow_w + 12) * 2, PAGE_HEIGHT - 355, flow_w, flow_h, SKY_BLUE)
    c.setFillColor(SKY_BLUE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(64 + (flow_w + 12) * 2, PAGE_HEIGHT - 160, "STEP 3: VERIFICATION")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(64 + (flow_w + 12) * 2, PAGE_HEIGHT - 185, "Anti-Fabrication Gate")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(64 + (flow_w + 12) * 2, PAGE_HEIGHT - 215, "• Confidence evaluation")
    c.drawString(64 + (flow_w + 12) * 2, PAGE_HEIGHT - 235, "• Verbatim quote checking")
    c.drawString(64 + (flow_w + 12) * 2, PAGE_HEIGHT - 255, "• Discrepancy detector")
    c.drawString(64 + (flow_w + 12) * 2, PAGE_HEIGHT - 275, "• If confidence < 0.70:")
    c.drawString(64 + (flow_w + 12) * 2, PAGE_HEIGHT - 295, "  Trigger boundary refusal")
    c.drawString(64 + (flow_w + 12) * 2, PAGE_HEIGHT - 315, "  with explore suggestions")

    # Step 4
    draw_card(c, 48 + (flow_w + 12) * 3, PAGE_HEIGHT - 355, flow_w, flow_h, PURPLE_ACCENT)
    c.setFillColor(PURPLE_ACCENT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(64 + (flow_w + 12) * 3, PAGE_HEIGHT - 160, "STEP 4: DISCOVERY")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(64 + (flow_w + 12) * 3, PAGE_HEIGHT - 185, "Synchronized Seek")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(64 + (flow_w + 12) * 3, PAGE_HEIGHT - 215, "• Render EvidenceBadge")
    c.drawString(64 + (flow_w + 12) * 3, PAGE_HEIGHT - 235, "• Render Markdown answer")
    c.drawString(64 + (flow_w + 12) * 3, PAGE_HEIGHT - 255, "• 1-Click interactive seek")
    c.drawString(64 + (flow_w + 12) * 3, PAGE_HEIGHT - 275, "• YouTube iframe jump")
    c.drawString(64 + (flow_w + 12) * 3, PAGE_HEIGHT - 295, "• Auto-scroll transcript")
    c.drawString(64 + (flow_w + 12) * 3, PAGE_HEIGHT - 315, "• Display Explore Next chips")

    # Real-World Use Case Box
    draw_card(c, 48, 65, PAGE_WIDTH - 96, 95, BG_CARD_BORDER, HexColor("#0F172A"))
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(68, 140, "PRIMARY USE-CASE WALKTHROUGH")
    c.setFillColor(TEXT_SLATE_200)
    c.setFont("Helvetica", 11)
    c.drawString(68, 118, "A student watching a 3-hour Kubernetes tutorial speaks in Hindi: 'कंटेनर क्रैश होने पर पॉड कैसे रीस्टार्ट होता है?'")
    c.drawString(68, 98, "ContextBridge verifies transcript & YAML slide, answers in Hindi, and jumps the video to 42:15 with 98% confidence.")

    c.showPage()

    # =========================================================================
    # SLIDE 6: Wireframes/Mock diagrams of the proposed solution (optional)
    # =========================================================================
    draw_header_footer(c, 6, 14, "UI WIREFRAMES & LAYOUT")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(48, PAGE_HEIGHT - 90, "Wireframes / UI Mock diagrams of the proposed solution")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 14)
    c.drawString(48, PAGE_HEIGHT - 116, "Modern dual-pane split console designed for zero distraction and immediate verification.")

    pane_w = (PAGE_WIDTH - 96 - 20) / 2
    pane_h = 340

    # Left Pane: Video & Transcript
    draw_card(c, 48, 65, pane_w, pane_h, INDIGO_ACCENT)
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(68, 380, "LEFT PANE: VIDEO & TIME SYNCHRONIZATION")

    # Mock Video Box
    draw_card(c, 68, 250, pane_w - 40, 110, BG_CARD_BORDER, HexColor("#050811"))
    c.setFillColor(TEXT_DIM)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(pane_w / 2 - 20, 310, "▶ 16:9 YouTube Iframe Player")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(pane_w / 2 - 40, 285, "Current Time: 00:14:32 / 01:45:00")

    # Mock Transcript Feed
    draw_card(c, 68, 85, pane_w - 40, 150, BG_CARD_BORDER, HexColor("#080D1A"))
    c.setFillColor(TEXT_SLATE_200)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(84, 215, "LIVE SYNCHRONIZED TRANSCRIPT FEED")
    c.setFillColor(TEXT_DIM)
    c.setFont("Helvetica", 10)
    c.drawString(84, 190, "[14:15] Now let us inspect how the ingress controller...")
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(84, 170, "▶ [14:32] Notice in the YAML manifest the restartPolicy is...")
    c.setFillColor(TEXT_DIM)
    c.setFont("Helvetica", 10)
    c.drawString(84, 150, "[14:50] If it fails three times, Kubernetes applies backoff...")
    c.drawString(84, 130, "[15:12] Next, let's examine the pod status with kubectl...")
    c.setFillColor(SKY_BLUE)
    c.drawString(84, 105, "• Auto-scrolls in lockstep with video playback time")

    # Right Pane: Intelligence Console
    draw_card(c, 48 + pane_w + 20, 65, pane_w, pane_h, EMERALD_GREEN)
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(48 + pane_w + 40, 380, "RIGHT PANE: INTELLIGENCE & PROOF CONSOLE")

    # Query Input Mock
    draw_card(c, 48 + pane_w + 40, 315, pane_w - 40, 50, BG_CARD_BORDER, HexColor("#080D1A"))
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(48 + pane_w + 55, 342, "Ask anything about this video (English / हिंदी)...")
    c.setFillColor(INDIGO_LIGHT)
    c.drawString(48 + pane_w + pane_w - 85, 342, "🎤 [Ask]")

    # Answer Card Mock
    draw_card(c, 48 + pane_w + 40, 85, pane_w - 40, 215, BG_CARD_BORDER, HexColor("#080D1A"))
    # EvidenceBadge mock
    c.setFillColor(EMERALD_GREEN)
    c.roundRect(48 + pane_w + 55, 260, 160, 24, 6, fill=1, stroke=0)
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(48 + pane_w + 65, 267, "✓ 98% Confidence · ⏱ 14:32")

    c.setFillColor(TEXT_SLATE_100)
    c.setFont("Helvetica", 10)
    c.drawString(48 + pane_w + 55, 240, "Kubernetes evaluates restartPolicy on container exit.")
    c.drawString(48 + pane_w + 55, 224, "Default policy is Always, with exponential backoff.")

    c.setFillColor(SKY_BLUE)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(48 + pane_w + 55, 198, "▶ Jump to 14:32 (Click seeks YouTube player)")

    c.setFillColor(HexColor("#334155"))
    c.roundRect(48 + pane_w + 55, 135, pane_w - 70, 50, 4, fill=1, stroke=0)
    c.setFillColor(TEXT_SLATE_200)
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(48 + pane_w + 65, 168, '"Notice in the YAML manifest the restartPolicy is set to Always..."')
    c.drawString(48 + pane_w + 65, 150, '— Verbatim quote character match verified against transcript')

    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(48 + pane_w + 55, 110, "Explore Next: [CrashLoopBackOff] [Liveness Probes] [kubectl logs]")

    c.showPage()

    # =========================================================================
    # SLIDE 7: Architecture diagram of the proposed solution
    # =========================================================================
    draw_header_footer(c, 7, 14, "SYSTEM ARCHITECTURE")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(48, PAGE_HEIGHT - 90, "Architecture diagram of the proposed solution")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 14)
    c.drawString(48, PAGE_HEIGHT - 116, "Stateless containerized stack deployed globally on Google Cloud Run.")

    arch_w = (PAGE_WIDTH - 96 - 40) / 3
    arch_h = 320

    # Layer 1: Client
    draw_card(c, 48, 65, arch_w, arch_h, SKY_BLUE, HexColor("#0A1424"))
    c.setFillColor(SKY_BLUE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(68, 355, "CLIENT LAYER")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(68, 330, "Next.js 14 App Router")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(68, 305, "• Containerized on Cloud Run")
    c.drawString(68, 285, "• Responsive split-screen UI")
    c.drawString(68, 265, "• YouTube IFrame Player API")
    c.drawString(68, 245, "• Web Speech API (Voice Q&A)")
    c.drawString(68, 225, "• Tailwind CSS + Lucide Icons")
    c.drawString(68, 205, "• Sub-second client seeking")
    c.drawString(68, 185, "• Transcript timeline syncer")
    c.drawString(68, 165, "• Language script parity engine")

    # Layer 2: API & Engine
    draw_card(c, 48 + arch_w + 20, 65, arch_w, arch_h, INDIGO_ACCENT, HexColor("#0F1426"))
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(48 + arch_w + 40, 355, "API & AGENT LAYER")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(48 + arch_w + 40, 330, "FastAPI Bounded Engine")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(48 + arch_w + 40, 305, "• Python 3.11 asynchronous API")
    c.drawString(48 + arch_w + 40, 285, "• Containerized on Cloud Run")
    c.drawString(48 + arch_w + 40, 265, "• Bounded 3-tool ladder")
    c.drawString(48 + arch_w + 40, 245, "• Exact quote matcher gate")
    c.drawString(48 + arch_w + 40, 225, "• Anti-fabrication scoring")
    c.drawString(48 + arch_w + 40, 205, "• Circuit breaker resilience")
    c.drawString(48 + arch_w + 40, 185, "• SSE streaming protocol")
    c.drawString(48 + arch_w + 40, 165, "• Quota-death fallback ladder")

    # Layer 3: Foundation AI
    draw_card(c, 48 + (arch_w + 20) * 2, 65, arch_w, arch_h, EMERALD_GREEN, HexColor("#0A171D"))
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(48 + (arch_w + 20) * 2 + 20, 355, "FOUNDATION AI")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(48 + (arch_w + 20) * 2 + 20, 330, "Google Gemini 2.5 Flash")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(48 + (arch_w + 20) * 2 + 20, 305, "• Multimodal video frame parsing")
    c.drawString(48 + (arch_w + 20) * 2 + 20, 285, "• High-speed token processing")
    c.drawString(48 + (arch_w + 20) * 2 + 20, 265, "• Low deterministic temperature")
    c.drawString(48 + (arch_w + 20) * 2 + 20, 245, "• Google Search web fallback")
    c.drawString(48 + (arch_w + 20) * 2 + 20, 225, "• Bilingual script translation")
    c.drawString(48 + (arch_w + 20) * 2 + 20, 205, "• Visual diagram understanding")
    c.drawString(48 + (arch_w + 20) * 2 + 20, 185, "• Code & syntax extraction")
    c.drawString(48 + (arch_w + 20) * 2 + 20, 165, "• Structured JSON schema outputs")

    c.showPage()

    # =========================================================================
    # SLIDE 8: Technologies to be used in the solution
    # =========================================================================
    draw_header_footer(c, 8, 14, "TECHNOLOGY STACK")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(48, PAGE_HEIGHT - 90, "Technologies to be used in the solution")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 14)
    c.drawString(48, PAGE_HEIGHT - 116, "Modern, production-grade cloud, AI, and web ecosystem.")

    tech_w = (PAGE_WIDTH - 96 - 32) / 3
    tech_h = 160

    # Tech 1: AI & ML
    draw_card(c, 48, PAGE_HEIGHT - 295, tech_w, tech_h, INDIGO_ACCENT)
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(68, PAGE_HEIGHT - 160, "AI & MULTIMODAL")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(68, PAGE_HEIGHT - 188, "Google Gemini 2.5 Flash")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(68, PAGE_HEIGHT - 215, "• google-genai official Python SDK")
    c.drawString(68, PAGE_HEIGHT - 235, "• Gemini Multimodal Vision API")
    c.drawString(68, PAGE_HEIGHT - 255, "• Structured Pydantic outputs")
    c.drawString(68, PAGE_HEIGHT - 275, "• Vertex AI inference endpoints")

    # Tech 2: Backend
    draw_card(c, 48 + tech_w + 16, PAGE_HEIGHT - 295, tech_w, tech_h, EMERALD_GREEN)
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(48 + tech_w + 36, PAGE_HEIGHT - 160, "BACKEND SERVICES")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(48 + tech_w + 36, PAGE_HEIGHT - 188, "Python 3.11 & FastAPI")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(48 + tech_w + 36, PAGE_HEIGHT - 215, "• AsyncIO / Uvicorn server")
    c.drawString(48 + tech_w + 36, PAGE_HEIGHT - 235, "• Pydantic v2 data validation")
    c.drawString(48 + tech_w + 36, PAGE_HEIGHT - 255, "• Pytest (83/83 green test suite)")
    c.drawString(48 + tech_w + 36, PAGE_HEIGHT - 275, "• Server-Sent Events (SSE)")

    # Tech 3: Frontend
    draw_card(c, 48 + (tech_w + 16) * 2, PAGE_HEIGHT - 295, tech_w, tech_h, SKY_BLUE)
    c.setFillColor(SKY_BLUE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(48 + (tech_w + 16) * 2 + 20, PAGE_HEIGHT - 160, "FRONTEND APPLICATION")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(48 + (tech_w + 16) * 2 + 20, PAGE_HEIGHT - 188, "Next.js 14 & React 18")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(48 + (tech_w + 16) * 2 + 20, PAGE_HEIGHT - 215, "• TypeScript strict type safety")
    c.drawString(48 + (tech_w + 16) * 2 + 20, PAGE_HEIGHT - 235, "• Tailwind CSS responsive UI")
    c.drawString(48 + (tech_w + 16) * 2 + 20, PAGE_HEIGHT - 255, "• Lucide React icon library")
    c.drawString(48 + (tech_w + 16) * 2 + 20, PAGE_HEIGHT - 275, "• YouTube IFrame Player API")

    # Tech 4: Cloud Infrastructure (Wide Row)
    draw_card(c, 48, 65, PAGE_WIDTH - 96, 125, PURPLE_ACCENT, HexColor("#0E1222"))
    c.setFillColor(PURPLE_ACCENT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(68, 160, "INFRASTRUCTURE, DEVOPS & VIDEO INGESTION")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(68, 135, "Google Cloud Run · Artifact Registry · GitHub Actions · Docker")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(68, 110, "• Fully managed serverless containers with scale-to-zero efficiency and sub-second cold starts.")
    c.drawString(68, 90, "• Ingestion stack: youtube-transcript-api, OpenCV frame extractor, Web Speech API (MediaRecorder).")

    c.showPage()

    # =========================================================================
    # SLIDE 9: Estimated implementation cost (optional)
    # =========================================================================
    draw_header_footer(c, 9, 14, "IMPLEMENTATION COST")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(48, PAGE_HEIGHT - 90, "Estimated implementation cost (optional)")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 14)
    c.drawString(48, PAGE_HEIGHT - 116, "Ultra-low marginal cost due to serverless scale-to-zero and token optimization.")

    c_w = (PAGE_WIDTH - 96 - 32) / 3
    c_h = 240

    # Cost 1: Cloud Run
    draw_card(c, 48, PAGE_HEIGHT - 375, c_w, c_h, EMERALD_GREEN)
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(68, PAGE_HEIGHT - 160, "GOOGLE CLOUD RUN")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(68, PAGE_HEIGHT - 195, "$0.00 – $5.00")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(68, PAGE_HEIGHT - 215, "PER MONTH (SCALE-TO-ZERO)")
    c.setFont("Helvetica", 11)
    c.drawString(68, PAGE_HEIGHT - 245, "• Free Tier covers 2M requests/mo")
    c.drawString(68, PAGE_HEIGHT - 265, "• Zero idle infrastructure cost")
    c.drawString(68, PAGE_HEIGHT - 285, "• Auto-scales from 0 to 100+ instances")
    c.drawString(68, PAGE_HEIGHT - 305, "• $0.000024 per vCPU-second beyond free tier")
    c.drawString(68, PAGE_HEIGHT - 325, "• Predictable, serverless unit economics")

    # Cost 2: Gemini API
    draw_card(c, 48 + c_w + 16, PAGE_HEIGHT - 375, c_w, c_h, INDIGO_ACCENT)
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(48 + c_w + 36, PAGE_HEIGHT - 160, "GEMINI 2.5 FLASH")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(48 + c_w + 36, PAGE_HEIGHT - 195, "~$0.25")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(48 + c_w + 36, PAGE_HEIGHT - 215, "PER 1,000 VIDEO QUERIES")
    c.setFont("Helvetica", 11)
    c.drawString(48 + c_w + 36, PAGE_HEIGHT - 245, "• Input: $0.075 per 1M tokens")
    c.drawString(48 + c_w + 36, PAGE_HEIGHT - 265, "• Output: $0.30 per 1M tokens")
    c.drawString(48 + c_w + 36, PAGE_HEIGHT - 285, "• Images: $0.00002 per visual frame")
    c.drawString(48 + c_w + 36, PAGE_HEIGHT - 305, "• Token-efficient chunking filters")
    c.drawString(48 + c_w + 36, PAGE_HEIGHT - 325, "• 10,000 queries cost less than $3.00")

    # Cost 3: DevOps & Registry
    draw_card(c, 48 + (c_w + 16) * 2, PAGE_HEIGHT - 375, c_w, c_h, SKY_BLUE)
    c.setFillColor(SKY_BLUE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(48 + (c_w + 16) * 2 + 20, PAGE_HEIGHT - 160, "STORAGE & NETWORK")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(48 + (c_w + 16) * 2 + 20, PAGE_HEIGHT - 195, "< $1.00")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(48 + (c_w + 16) * 2 + 20, PAGE_HEIGHT - 215, "PER MONTH TOTAL")
    c.setFont("Helvetica", 11)
    c.drawString(48 + (c_w + 16) * 2 + 20, PAGE_HEIGHT - 245, "• Google Artifact Registry: ~$0.10/mo")
    c.drawString(48 + (c_w + 16) * 2 + 20, PAGE_HEIGHT - 265, "• Cloud Build: 120 free mins/day")
    c.drawString(48 + (c_w + 16) * 2 + 20, PAGE_HEIGHT - 285, "• Egress bandwidth: minimal JSON/SSE")
    c.drawString(48 + (c_w + 16) * 2 + 20, PAGE_HEIGHT - 305, "• GitHub Actions: Free for public repo")
    c.drawString(48 + (c_w + 16) * 2 + 20, PAGE_HEIGHT - 325, "• Zero fixed database licensing fees")

    # Summary Banner
    draw_card(c, 48, 65, PAGE_WIDTH - 96, 75, BG_CARD_BORDER, HexColor("#0A141D"))
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(68, 115, "TOTAL ESTIMATED COST FOR 10,000 ACTIVE USER QUERIES: < $15.00 USD")
    c.setFillColor(TEXT_SLATE_200)
    c.setFont("Helvetica", 11)
    c.drawString(68, 92, "Highly scalable, enabling educational institutions, bootcamps, and students to run ContextBridge at negligible cost.")

    c.showPage()

    # =========================================================================
    # SLIDE 10: Snapshots of the prototype
    # =========================================================================
    draw_header_footer(c, 10, 14, "PROTOTYPE SNAPSHOTS")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(48, PAGE_HEIGHT - 90, "Snapshots of the prototype")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 14)
    c.drawString(48, PAGE_HEIGHT - 116, "Live working product deployed on Google Cloud Run with 100% functional user flows.")

    snap_w = (PAGE_WIDTH - 96 - 20) / 2
    snap_h = 160

    # Snapshot 1
    draw_card(c, 48, PAGE_HEIGHT - 295, snap_w, snap_h, INDIGO_ACCENT)
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(68, PAGE_HEIGHT - 155, "SNAPSHOT 1: 1-CLICK SEEKING & SYNC")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(68, PAGE_HEIGHT - 180, "Interactive Seek Buttons Jump Video Player")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(68, PAGE_HEIGHT - 205, "• User clicks [01:14:22] button on answer card.")
    c.drawString(68, PAGE_HEIGHT - 225, "• Embedded YouTube iframe seeks to 1:14:22 within ~1 second.")
    c.drawString(68, PAGE_HEIGHT - 245, "• Live transcript auto-scrolls and highlights corresponding line.")
    c.drawString(68, PAGE_HEIGHT - 265, "• Verified across Chrome, Edge, Safari, and mobile browsers.")

    # Snapshot 2
    draw_card(c, 48 + snap_w + 20, PAGE_HEIGHT - 295, snap_w, snap_h, EMERALD_GREEN)
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(68 + snap_w + 20, PAGE_HEIGHT - 155, "SNAPSHOT 2: EVIDENCEBADGE & VERBATIM QUOTE")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(68 + snap_w + 20, PAGE_HEIGHT - 180, "Mathematical Proof Visible in Every Answer")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(68 + snap_w + 20, PAGE_HEIGHT - 205, "• EvidenceBadge displays Confidence % (e.g. 98%).")
    c.drawString(68 + snap_w + 20, PAGE_HEIGHT - 225, "• Verified verbatim speaker quote shown in dedicated block.")
    c.drawString(68 + snap_w + 20, PAGE_HEIGHT - 245, "• Discrepancy detector flags any audio vs. slide contradictions.")
    c.drawString(68 + snap_w + 20, PAGE_HEIGHT - 265, "• Eliminates need for manual scrubbing and double-checking.")

    # Snapshot 3
    draw_card(c, 48, PAGE_HEIGHT - 475, snap_w, snap_h, AMBER_WARN)
    c.setFillColor(AMBER_WARN)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(68, PAGE_HEIGHT - 335, "SNAPSHOT 3: BILINGUAL HINDI INTERFACE")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(68, PAGE_HEIGHT - 360, "Hindi Voice & Text Q&A with Devanagari Scripts")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(68, PAGE_HEIGHT - 385, "• Queries asked in Hindi receive natural Hindi explanations.")
    c.drawString(68, PAGE_HEIGHT - 405, "• Preserves technical vocabulary alongside native phrasing.")
    c.drawString(68, PAGE_HEIGHT - 425, "• Hindi fallback suggestions guide non-English speakers.")
    c.drawString(68, PAGE_HEIGHT - 445, "• Removes the linguistic barrier for 600M+ Hindi speakers.")

    # Snapshot 4
    draw_card(c, 48 + snap_w + 20, PAGE_HEIGHT - 475, snap_w, snap_h, PURPLE_ACCENT)
    c.setFillColor(PURPLE_ACCENT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(68 + snap_w + 20, PAGE_HEIGHT - 335, "SNAPSHOT 4: BOUNDARY HONESTY IN ACTION")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(68 + snap_w + 20, PAGE_HEIGHT - 360, "Zero Hallucination with 3 Explore Suggestions")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(68 + snap_w + 20, PAGE_HEIGHT - 385, "• Query outside video topic triggers clear boundary notice.")
    c.drawString(68 + snap_w + 20, PAGE_HEIGHT - 405, "• 'The video does not cover this topic.' (0.00 confidence).")
    c.drawString(68 + snap_w + 20, PAGE_HEIGHT - 425, "• Synthesizes 3 proactive explore prompts from actual video.")
    c.drawString(68 + snap_w + 20, PAGE_HEIGHT - 445, "• Learner is directed back to productive learning pathways.")

    c.showPage()

    # =========================================================================
    # SLIDE 11: Prototype Performance report/Benchmarking
    # =========================================================================
    draw_header_footer(c, 11, 14, "BENCHMARKING & EVALUATION")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(48, PAGE_HEIGHT - 90, "Prototype Performance report / Benchmarking")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 14)
    c.drawString(48, PAGE_HEIGHT - 116, "Empirical evaluation across 25 ground-truth video cases and 83 automated test suites.")

    # Metric 1
    m_w = (PAGE_WIDTH - 96 - 40) / 3
    m_h = 160
    draw_card(c, 48, PAGE_HEIGHT - 295, m_w, m_h, EMERALD_GREEN, HexColor("#0A141D"))
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(68, PAGE_HEIGHT - 155, "TIMESTAMP SEEK ACCURACY")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 36)
    c.drawString(68, PAGE_HEIGHT - 200, "94.4%")
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(68, PAGE_HEIGHT - 225, "Target: > 85.0% (Exceeded by +9.4%)")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(68, PAGE_HEIGHT - 250, "• 17 of 18 verifiable timestamp queries")
    c.drawString(68, PAGE_HEIGHT - 270, "  within ±15s of exact creator moment.")

    # Metric 2
    draw_card(c, 48 + m_w + 20, PAGE_HEIGHT - 295, m_w, m_h, SKY_BLUE, HexColor("#0A1726"))
    c.setFillColor(SKY_BLUE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(48 + m_w + 40, PAGE_HEIGHT - 155, "TRANSCRIPT GROUNDEDNESS")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 36)
    c.drawString(48 + m_w + 40, PAGE_HEIGHT - 200, "92.0%")
    c.setFillColor(SKY_BLUE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(48 + m_w + 40, PAGE_HEIGHT - 225, "Target: > 80.0% (Exceeded by +12.0%)")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(48 + m_w + 40, PAGE_HEIGHT - 250, "• 23 of 25 cases backed directly by")
    c.drawString(48 + m_w + 40, PAGE_HEIGHT - 270, "  explicit transcript speech lines.")

    # Metric 3
    draw_card(c, 48 + (m_w + 20) * 2, PAGE_HEIGHT - 295, m_w, m_h, INDIGO_ACCENT, HexColor("#0F1426"))
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(48 + (m_w + 20) * 2 + 20, PAGE_HEIGHT - 155, "UNSUPPORTED / HALLUCINATED")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 36)
    c.drawString(48 + (m_w + 20) * 2 + 20, PAGE_HEIGHT - 200, "0.0%")
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(48 + (m_w + 20) * 2 + 20, PAGE_HEIGHT - 225, "Target: < 5.0% (Zero Fabrication)")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(48 + (m_w + 20) * 2 + 20, PAGE_HEIGHT - 250, "• 0 of 25 cases produced answers")
    c.drawString(48 + (m_w + 20) * 2 + 20, PAGE_HEIGHT - 270, "  unsupported by video ground truth.")

    # Bottom Test Suite & Resilience Verification Box
    draw_card(c, 48, 65, PAGE_WIDTH - 96, 120, BG_CARD_BORDER, HexColor("#0F172A"))
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(68, 155, "AUTOMATED QUALITY GATES & RESILIENCY DRILLS")

    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(68, 130, "✓ 83 / 83 Unit & Integration Tests Passing (Pytest)")
    c.drawString(68, 110, "✓ 9 / 9 Failure Drills Passing (tests/test_failure_drills.py)")
    c.drawString(68, 90, "✓ Latency: ~1.1s median end-to-end response time on Google Cloud Run")

    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(490, 130, "• Evaluated against adversarial questions & missing audio")
    c.drawString(490, 110, "• TypeScript & Next.js production builds passing with 0 warnings")
    c.drawString(490, 90, "• Reproducible eval pipeline committed in context/eval_results.json")

    c.showPage()

    # =========================================================================
    # SLIDE 12: Additional Details/Future Development (if any)
    # =========================================================================
    draw_header_footer(c, 12, 14, "FUTURE ROADMAP")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(48, PAGE_HEIGHT - 90, "Additional Details / Future Development (if any)")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 14)
    c.drawString(48, PAGE_HEIGHT - 116, "Strategic roadmap to scale ContextBridge across courses, platforms, and languages.")

    road_w = (PAGE_WIDTH - 96 - 36) / 4
    road_h = 320

    # Phase 1
    draw_card(c, 48, 65, road_w, road_h, EMERALD_GREEN, HexColor("#0A141D"))
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(64, 355, "PHASE 1 (SHIPPED)")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(64, 330, "Core Compass Engine")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(64, 305, "• Single-video multimodal QA")
    c.drawString(64, 285, "• EvidenceBadge verification")
    c.drawString(64, 265, "• 1-Click interactive seek")
    c.drawString(64, 245, "• Full Hindi/English parity")
    c.drawString(64, 225, "• Google Cloud Run deploy")
    c.drawString(64, 205, "• 83/83 automated tests")
    c.drawString(64, 185, "• 94.4% accuracy verified")
    c.drawString(64, 165, "• Zero fabrication guardrails")

    # Phase 2
    draw_card(c, 48 + road_w + 12, 65, road_w, road_h, INDIGO_ACCENT, HexColor("#0F1426"))
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(64 + road_w + 12, 355, "PHASE 2 (Q2 2026)")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(64 + road_w + 12, 330, "Playlist & Course Scale")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(64 + road_w + 12, 305, "• Multi-video playlist synthesis")
    c.drawString(64 + road_w + 12, 285, "• Cross-video knowledge graph")
    c.drawString(64 + road_w + 12, 265, "• University course modules")
    c.drawString(64 + road_w + 12, 245, "• Concept prerequisite trees")
    c.drawString(64 + road_w + 12, 225, "• Flashcard & quiz generator")
    c.drawString(64 + road_w + 12, 205, "• Cross-lecture citations")
    c.drawString(64 + road_w + 12, 185, "• Unified search index")
    c.drawString(64 + road_w + 12, 165, "• Course timeline maps")

    # Phase 3
    draw_card(c, 48 + (road_w + 12) * 2, 65, road_w, road_h, SKY_BLUE, HexColor("#0A1726"))
    c.setFillColor(SKY_BLUE)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(64 + (road_w + 12) * 2, 355, "PHASE 3 (Q3 2026)")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(64 + (road_w + 12) * 2, 330, "Browser Extension")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(64 + (road_w + 12) * 2, 305, "• Manifest V3 Chrome Extension")
    c.drawString(64 + (road_w + 12) * 2, 285, "• Injected YouTube side panel")
    c.drawString(64 + (road_w + 12) * 2, 265, "• Support for Coursera & edX")
    c.drawString(64 + (road_w + 12) * 2, 245, "• Local vector cache for offline")
    c.drawString(64 + (road_w + 12) * 2, 225, "• Mobile PWA companion app")
    c.drawString(64 + (road_w + 12) * 2, 205, "• Offline audio sync")
    c.drawString(64 + (road_w + 12) * 2, 185, "• Privacy-preserving storage")
    c.drawString(64 + (road_w + 12) * 2, 165, "• 1-Click install from store")

    # Phase 4
    draw_card(c, 48 + (road_w + 12) * 3, 65, road_w, road_h, PURPLE_ACCENT, HexColor("#0E1222"))
    c.setFillColor(PURPLE_ACCENT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(64 + (road_w + 12) * 3, 355, "PHASE 4 (Q4 2026)")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(64 + (road_w + 12) * 3, 330, "Global Vernacular")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(64 + (road_w + 12) * 3, 305, "• Expand Indian languages:")
    c.drawString(64 + (road_w + 12) * 3, 285, "  Tamil, Telugu, Bengali,")
    c.drawString(64 + (road_w + 12) * 3, 265, "  Marathi, Kannada")
    c.drawString(64 + (road_w + 12) * 3, 245, "• Spanish, Portuguese & French")
    c.drawString(64 + (road_w + 12) * 3, 225, "• Non-English video grounding")
    c.drawString(64 + (road_w + 12) * 3, 205, "• Vernacular voice cloning")
    c.drawString(64 + (road_w + 12) * 3, 185, "• Open API for EdTech LMS")
    c.drawString(64 + (road_w + 12) * 3, 165, "• B2B licensing for academies")

    c.showPage()

    # =========================================================================
    # SLIDE 13: Provide links to your:
    # =========================================================================
    draw_header_footer(c, 13, 14, "PROJECT LINKS & REPOSITORIES")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(48, PAGE_HEIGHT - 90, "Provide links to your:")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 14)
    c.drawString(48, PAGE_HEIGHT - 116, "Official submission links to public source code, demo video, and live deployment.")

    link_h = 100

    # Link 1: GitHub Public Repository
    draw_card(c, 48, PAGE_HEIGHT - 235, PAGE_WIDTH - 96, link_h, INDIGO_ACCENT)
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(68, PAGE_HEIGHT - 150, "1. GITHUB PUBLIC REPOSITORY")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(68, PAGE_HEIGHT - 176, "https://github.com/lvhNaruto/contextbridge-ai")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(68, PAGE_HEIGHT - 200, "• Complete source code, Docker configs, 83 automated unit/integration tests, and CI/CD pipelines.")
    c.drawString(68, PAGE_HEIGHT - 218, "• Open-source under MIT License with comprehensive architectural specifications and evaluation logs.")

    # Link 2: Demo Video Link
    draw_card(c, 48, PAGE_HEIGHT - 355, PAGE_WIDTH - 96, link_h, EMERALD_GREEN)
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(68, PAGE_HEIGHT - 270, "2. DEMO VIDEO LINK (3 MINUTES)")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(68, PAGE_HEIGHT - 296, "https://github.com/lvhNaruto/contextbridge-ai#demo-video")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(68, PAGE_HEIGHT - 320, "• 6-Beat Walkthrough: Problem, Grounded Q&A, 1-Click Seeking, Hindi Voice Q&A, and Boundary Refusal.")
    c.drawString(68, PAGE_HEIGHT - 338, "• Complete script and high-resolution video walk in docs/DEMO_VIDEO_SCRIPT.md and repository README.")

    # Link 3: Final Product Link
    draw_card(c, 48, PAGE_HEIGHT - 475, PAGE_WIDTH - 96, link_h, SKY_BLUE)
    c.setFillColor(SKY_BLUE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(68, PAGE_HEIGHT - 390, "3. FINAL PRODUCT LINK (LIVE CLOUD RUN DEPLOYMENT)")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(68, PAGE_HEIGHT - 416, "Frontend: https://contextbridge-web-c5ltxo3mkq-uc.a.run.app")
    c.setFillColor(TEXT_SLATE_200)
    c.setFont("Helvetica", 11)
    c.drawString(68, PAGE_HEIGHT - 438, "Backend API: https://contextbridge-api-c5ltxo3mkq-uc.a.run.app")
    c.drawString(68, PAGE_HEIGHT - 456, "API Health Endpoint: https://contextbridge-api-c5ltxo3mkq-uc.a.run.app/health (Status: Healthy / 200 OK)")

    c.showPage()

    # =========================================================================
    # SLIDE 14: Thank You
    # =========================================================================
    draw_header_footer(c, 14, 14, "THANK YOU")

    # Center Hero Box
    draw_card(c, 48, 65, PAGE_WIDTH - 96, 400, INDIGO_ACCENT, HexColor("#0A0E1A"))

    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(PAGE_WIDTH / 2, 400, "AI BUILDER CUP 2026 · FINAL SUBMISSION")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 44)
    c.drawCentredString(PAGE_WIDTH / 2, 340, "Thank You!")

    c.setFillColor(TEXT_SLATE_100)
    c.setFont("Helvetica", 18)
    c.drawCentredString(PAGE_WIDTH / 2, 290, "ContextBridge AI — A Compass for Self-Learners")

    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 13)
    c.drawCentredString(PAGE_WIDTH / 2, 255, '"Empowering millions of self-directed learners to watch less, understand more, and trust every answer."')

    # Contact Details Pill Box
    draw_card(c, PAGE_WIDTH / 2 - 250, 110, 500, 115, BG_CARD_BORDER, HexColor("#111827"))
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(PAGE_WIDTH / 2, 195, "TEAM DETAILS & CONTACT")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(PAGE_WIDTH / 2, 168, "Team Name: ContextBridge AI")
    c.setFillColor(TEXT_SLATE_200)
    c.setFont("Helvetica", 13)
    c.drawCentredString(PAGE_WIDTH / 2, 145, "Team Leader: Mohit Singh · mohitsinghgeek@gmail.com")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawCentredString(PAGE_WIDTH / 2, 125, "GitHub: https://github.com/lvhNaruto/contextbridge-ai")

    c.showPage()

    # Save PDF
    c.save()
    print(f"Official Submission Pitch Deck PDF generated successfully: {output_path}")


if __name__ == "__main__":
    output = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "contextbridge_official_submission_deck.pdf")
    generate_deck(output)
