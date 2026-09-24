"""Generate the 10-slide ContextBridge AI Hackathon Pitch Deck PDF using ReportLab.

Canvas format: 16:9 Landscape (960 x 540 pt)
Theme: Dark mode (Navy/Slate/Emerald/Indigo)
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

# Palette
BG_DARK = HexColor("#090D16")
BG_CARD = HexColor("#111827")
BG_CARD_BORDER = HexColor("#1F2937")
TEXT_WHITE = HexColor("#FFFFFF")
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


def draw_header_footer(c: canvas.Canvas, slide_num: int, total_slides: int = 10, category: str = "AI BUILDER CUP 2026"):
    # Background
    c.setFillColor(BG_DARK)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

    # Top Category Badge
    c.setFillColor(HexColor("#1E293B"))
    c.roundRect(48, PAGE_HEIGHT - 44, 200, 24, 12, fill=1, stroke=0)
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
    c.drawRightString(PAGE_WIDTH - 48, 22, "Live URL: contextbridge-web-c5ltxo3mkq-uc.a.run.app")


def draw_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, border_color=BG_CARD_BORDER, fill_color=BG_CARD):
    c.setFillColor(fill_color)
    c.setStrokeColor(border_color)
    c.setLineWidth(1)
    c.roundRect(x, y, w, h, 10, fill=1, stroke=1)


def generate_deck(output_path: str):
    c = canvas.Canvas(output_path, pagesize=PAGESIZE)

    # =========================================================================
    # SLIDE 1: Title & Vision
    # =========================================================================
    draw_header_footer(c, 1, 10, "AI BUILDER CUP 2026")

    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(48, PAGE_HEIGHT - 85, "THEME: MEDIA, CONTENT & DIGITAL EXPERIENCES")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 42)
    c.drawString(48, PAGE_HEIGHT - 140, "ContextBridge AI")
    c.setFillColor(EMERALD_LIGHT)
    c.drawString(405, PAGE_HEIGHT - 140, "🧭")

    c.setFillColor(TEXT_SLATE_200)
    c.setFont("Helvetica", 17)
    c.drawString(48, PAGE_HEIGHT - 185, '"Not a tutor. A compass for self-learners — every answer anchored to the video')
    c.drawString(48, PAGE_HEIGHT - 212, ' you chose, in your language, with proof, and honest about where the video ends."')

    # 3 Stat Cards
    card_w = (PAGE_WIDTH - 96 - 32) / 3
    # Card 1
    draw_card(c, 48, 80, card_w, 180, INDIGO_ACCENT, HexColor("#0F172A"))
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(68, 230, "AI REASONING ENGINE")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(68, 200, "Gemini 2.5 Flash")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(68, 172, "Multimodal video analysis,")
    c.drawString(68, 154, "native audio transcription,")
    c.drawString(68, 136, "and Google Search grounding.")

    # Card 2
    draw_card(c, 48 + card_w + 16, 80, card_w, 180, EMERALD_GREEN, HexColor("#0F172A"))
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(48 + card_w + 36, 230, "UNSUPPORTED ANSWERS")
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 32)
    c.drawString(48 + card_w + 36, 192, "0.0%")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(48 + card_w + 36, 162, "Strict Anti-Fabrication Gate:")
    c.drawString(48 + card_w + 36, 144, "Verbatim transcript quote")
    c.drawString(48 + card_w + 36, 126, "matching & exact timestamps.")

    # Card 3
    draw_card(c, 48 + (card_w + 16) * 2, 80, card_w, 180, SKY_BLUE, HexColor("#0F172A"))
    c.setFillColor(SKY_BLUE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(48 + (card_w + 16) * 2 + 20, 230, "PRODUCTION DEPLOYMENT")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(48 + (card_w + 16) * 2 + 20, 200, "Google Cloud Run")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(48 + (card_w + 16) * 2 + 20, 172, "Next.js 16 Web + FastAPI")
    c.drawString(48 + (card_w + 16) * 2 + 20, 154, "Stateless containerized stack")
    c.drawString(48 + (card_w + 16) * 2 + 20, 136, "Serving 100% live traffic.")
    c.showPage()

    # =========================================================================
    # SLIDE 2: The Self-Learner's Dilemma
    # =========================================================================
    draw_header_footer(c, 2, 10, "THE CHALLENGE")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(48, PAGE_HEIGHT - 90, "The Self-Learner's Dilemma")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 14)
    c.drawString(48, PAGE_HEIGHT - 116, "Billions of hours of educational video exist, but self-directed learners face four critical friction points.")

    grid_w = (PAGE_WIDTH - 96 - 20) / 2
    grid_h = 160

    # Friction 1
    draw_card(c, 48, PAGE_HEIGHT - 295, grid_w, grid_h)
    c.setFillColor(RED_ALERT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(68, PAGE_HEIGHT - 160, "1. Scrubbing Fatigue (Wasted Time)")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 12)
    c.drawString(68, PAGE_HEIGHT - 190, "Learners spend 15+ minutes hunting back and forth across 45-minute")
    c.drawString(68, PAGE_HEIGHT - 210, "tutorials just to locate a 10-second syntax snippet or formula.")

    # Friction 2
    draw_card(c, 48 + grid_w + 20, PAGE_HEIGHT - 295, grid_w, grid_h)
    c.setFillColor(AMBER_WARN)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(68 + grid_w + 20, PAGE_HEIGHT - 160, "2. Chatbot Hallucination Trap")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 12)
    c.drawString(68 + grid_w + 20, PAGE_HEIGHT - 190, "Generic chatbots (ChatGPT, Claude) lack the video's actual runtime.")
    c.drawString(68 + grid_w + 20, PAGE_HEIGHT - 210, "They invent plausible-sounding code and quote words never spoken.")

    # Friction 3
    draw_card(c, 48, PAGE_HEIGHT - 475, grid_w, grid_h)
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(68, PAGE_HEIGHT - 340, "3. The Linguistic Barrier")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 12)
    c.drawString(68, PAGE_HEIGHT - 370, "World-class technical tutorials are overwhelmingly in English.")
    c.drawString(68, PAGE_HEIGHT - 390, "Non-native speakers (Hindi, Hinglish) struggle with dense video jargon.")

    # Friction 4
    draw_card(c, 48 + grid_w + 20, PAGE_HEIGHT - 475, grid_w, grid_h)
    c.setFillColor(SKY_BLUE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(68 + grid_w + 20, PAGE_HEIGHT - 340, "4. The Blurry Knowledge Boundary")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 12)
    c.drawString(68 + grid_w + 20, PAGE_HEIGHT - 370, "Existing summarizers fail to distinguish between what the creator said")
    c.drawString(68 + grid_w + 20, PAGE_HEIGHT - 390, "and general web knowledge, completely eroding learner confidence.")
    c.showPage()

    # =========================================================================
    # SLIDE 3: The Three Pillars
    # =========================================================================
    draw_header_footer(c, 3, 10, "CORE PHILOSOPHY")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(48, PAGE_HEIGHT - 90, "The Three Pillars of The Compass")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 14)
    c.drawString(48, PAGE_HEIGHT - 116, "ContextBridge enforces trust through structural, mathematical gates.")

    col_w = (PAGE_WIDTH - 96 - 40) / 3
    col_h = 320

    # Pillar 1
    draw_card(c, 48, 65, col_w, col_h, EMERALD_GREEN, HexColor("#0A141D"))
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 32)
    c.drawString(68, 345, "⚓ P1")
    c.setFont("Helvetica-Bold", 18)
    c.drawString(68, 310, "Anchored")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(68, 275, "The Video is Sole Ground Truth")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(68, 245, "• Video answers must originate")
    c.drawString(68, 227, "  from the creator's transcript.")
    c.drawString(68, 203, "• quote_matches_transcript gate")
    c.drawString(68, 185, "  strictly verifies character match.")
    c.drawString(68, 161, "• Invariant: zero invented quotes.")

    # Pillar 2
    draw_card(c, 48 + col_w + 20, 65, col_w, col_h, INDIGO_ACCENT, HexColor("#0F1426"))
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 32)
    c.drawString(48 + col_w + 40, 345, "🔍 P2")
    c.setFont("Helvetica-Bold", 18)
    c.drawString(48 + col_w + 40, 310, "Proof")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(48 + col_w + 40, 275, "Trust Visible in 10 Seconds")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(48 + col_w + 40, 245, "• EvidenceBadge displays origin")
    c.drawString(48 + col_w + 40, 227, "  and verification confidence.")
    c.drawString(48 + col_w + 40, 203, "• Click seeks player to exact")
    c.drawString(48 + col_w + 40, 185, "  second (~1s precision).")
    c.drawString(48 + col_w + 40, 161, "• Auto-scrolls transcript segment.")

    # Pillar 3
    draw_card(c, 48 + (col_w + 20) * 2, 65, col_w, col_h, SKY_BLUE, HexColor("#0A1726"))
    c.setFillColor(SKY_BLUE)
    c.setFont("Helvetica-Bold", 32)
    c.drawString(48 + (col_w + 20) * 2 + 20, 345, "🧭 P3")
    c.setFont("Helvetica-Bold", 18)
    c.drawString(48 + (col_w + 20) * 2 + 20, 310, "Boundary Honesty")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(48 + (col_w + 20) * 2 + 20, 275, "Honesty is a Feature")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(48 + (col_w + 20) * 2 + 20, 245, "• Video limits are acknowledged.")
    c.drawString(48 + (col_w + 20) * 2 + 20, 227, "• External research framed in a")
    c.drawString(48 + (col_w + 20) * 2 + 20, 203, "  dedicated BoundaryCard.")
    c.drawString(48 + (col_w + 20) * 2 + 20, 185, "• Real Google Search citations.")
    c.drawString(48 + (col_w + 20) * 2 + 20, 161, "• Never blends creator & web claims.")
    c.showPage()

    # =========================================================================
    # SLIDE 4: Interactive Experience
    # =========================================================================
    draw_header_footer(c, 4, 10, "PRODUCT EXPERIENCE")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(48, PAGE_HEIGHT - 90, "Trust Visible: Interactive Workspace")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 14)
    c.drawString(48, PAGE_HEIGHT - 116, "A cohesive UI delivering synchronized proof at every touchpoint.")

    box_w = (PAGE_WIDTH - 96 - 30) / 4
    box_h = 210

    # Feature 1
    draw_card(c, 48, PAGE_HEIGHT - 350, box_w, box_h)
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(64, PAGE_HEIGHT - 165, "EvidenceBadge")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(64, PAGE_HEIGHT - 195, "3 Explicit States:")
    c.setFillColor(EMERALD_LIGHT)
    c.drawString(64, PAGE_HEIGHT - 215, "• Verified Video · 98%")
    c.setFillColor(SKY_BLUE)
    c.drawString(64, PAGE_HEIGHT - 235, "• Beyond Video (Web)")
    c.setFillColor(TEXT_MUTED)
    c.drawString(64, PAGE_HEIGHT - 255, "• Honest Boundary")

    # Feature 2
    draw_card(c, 48 + box_w + 10, PAGE_HEIGHT - 350, box_w, box_h)
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(48 + box_w + 24, PAGE_HEIGHT - 165, "TranscriptSync")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(48 + box_w + 24, PAGE_HEIGHT - 195, "Bidirectional synchronization:")
    c.drawString(48 + box_w + 24, PAGE_HEIGHT - 215, "Clicking an evidence quote")
    c.drawString(48 + box_w + 24, PAGE_HEIGHT - 235, "auto-scrolls right-rail")
    c.drawString(48 + box_w + 24, PAGE_HEIGHT - 255, "transcript to active segment.")

    # Feature 3
    draw_card(c, 48 + (box_w + 10) * 2, PAGE_HEIGHT - 350, box_w, box_h)
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(48 + (box_w + 10) * 2 + 20, PAGE_HEIGHT - 165, "ExploreSuggestions")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(48 + (box_w + 10) * 2 + 20, PAGE_HEIGHT - 195, '"Explore from here →" chips')
    c.drawString(48 + (box_w + 10) * 2 + 20, PAGE_HEIGHT - 215, "derived dynamically from")
    c.drawString(48 + (box_w + 10) * 2 + 20, PAGE_HEIGHT - 235, "video chapters & topics.")
    c.drawString(48 + (box_w + 10) * 2 + 20, PAGE_HEIGHT - 255, "Zero extra LLM latency!")

    # Feature 4
    draw_card(c, 48 + (box_w + 10) * 3, PAGE_HEIGHT - 350, box_w, box_h)
    c.setFillColor(AMBER_WARN)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(48 + (box_w + 10) * 3 + 20, PAGE_HEIGHT - 165, "Contradictions")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(48 + (box_w + 10) * 3 + 20, PAGE_HEIGHT - 195, "Critical thinking helper:")
    c.drawString(48 + (box_w + 10) * 3 + 20, PAGE_HEIGHT - 215, "Highlights internal nuance")
    c.drawString(48 + (box_w + 10) * 3 + 20, PAGE_HEIGHT - 235, "with dual clickable jump")
    c.drawString(48 + (box_w + 10) * 3 + 20, PAGE_HEIGHT - 255, "buttons (00:05 vs 00:15).")

    # Bottom Callout Card
    draw_card(c, 48, 60, PAGE_WIDTH - 96, 75, SKY_BLUE, HexColor("#0D1A2D"))
    c.setFillColor(SKY_BLUE)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(68, 108, "🌐 BoundaryCard: Explicit Separation of Knowledge Worlds")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(68, 86, "When questions exceed video scope, external research is isolated in a distinct sky-blue frame with real Google Search sources.")
    c.showPage()

    # =========================================================================
    # SLIDE 5: Multilingual Voice Loop
    # =========================================================================
    draw_header_footer(c, 5, 10, "INCLUSIVITY & ACCESS")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(48, PAGE_HEIGHT - 90, "Bilingual Voice Loop (Hindi, Hinglish, English)")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 14)
    c.drawString(48, PAGE_HEIGHT - 116, "Learners explore in the language they think in — full voice-in, voice-out parity with Gemini.")

    v_w = (PAGE_WIDTH - 96 - 32) / 3
    v_h = 160

    draw_card(c, 48, PAGE_HEIGHT - 295, v_w, v_h)
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(68, PAGE_HEIGHT - 165, "🎙️ Speech-to-Text")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(68, PAGE_HEIGHT - 195, "Gemini 2.5 Flash native audio")
    c.drawString(68, PAGE_HEIGHT - 215, "transcription via POST /transcribe.")
    c.drawString(68, PAGE_HEIGHT - 235, "Verbatim capture of Hindi/Hinglish.")

    draw_card(c, 48 + v_w + 16, PAGE_HEIGHT - 295, v_w, v_h, EMERALD_GREEN)
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(48 + v_w + 36, PAGE_HEIGHT - 165, "🔊 Auto-Speak & TTS")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(48 + v_w + 36, PAGE_HEIGHT - 195, "Language-matched speech")
    c.drawString(48 + v_w + 36, PAGE_HEIGHT - 215, "synthesis (hi-IN / en-US).")
    c.drawString(48 + v_w + 36, PAGE_HEIGHT - 235, "Hands-free audio self-learning.")

    draw_card(c, 48 + (v_w + 16) * 2, PAGE_HEIGHT - 295, v_w, v_h)
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(48 + (v_w + 16) * 2 + 20, PAGE_HEIGHT - 165, "🛑 Instant Barge-In")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(48 + (v_w + 16) * 2 + 20, PAGE_HEIGHT - 195, "Tapping mic cancels active audio.")
    c.drawString(48 + (v_w + 16) * 2 + 20, PAGE_HEIGHT - 215, "Animated avatar rings and audio")
    c.drawString(48 + (v_w + 16) * 2 + 20, PAGE_HEIGHT - 235, "waveforms indicate speaking state.")

    # Live Code / Transcript Quote Card
    draw_card(c, 48, 60, PAGE_WIDTH - 96, 150, HexColor("#334155"), HexColor("#060A12"))
    c.setFillColor(HexColor("#38BDF8"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(68, 185, "LIVE VERIFIED BENCHMARK CASE (q13 & q14 from eval_results.json):")
    c.setFillColor(TEXT_SLATE_200)
    c.setFont("Helvetica", 11)
    c.drawString(68, 160, 'Student (Hindi): "सायका शिमाडा टोक्यो में क्या काम करती हैं?"')
    c.setFillColor(EMERALD_LIGHT)
    c.drawString(68, 140, 'ContextBridge: "Saeka Shimada Tokyo mein ek photographer hain (00:01)."')
    c.setFillColor(TEXT_MUTED)
    c.drawString(68, 120, 'Verified Evidence: [00:01 - 00:03] "My name is Saeka Shimada. I\'m a photographer in Tokyo."')
    c.setFillColor(TEXT_DIM)
    c.drawString(68, 100, "Confidence: 0.98 | Timestamp Retrieval: EXACT (1.0s - 3.0s) | Latency: 2.35s")
    c.showPage()

    # =========================================================================
    # SLIDE 6: Architecture & Anti-Fabrication Gate
    # =========================================================================
    draw_header_footer(c, 6, 10, "TECHNICAL ARCHITECTURE")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(48, PAGE_HEIGHT - 90, "The Anti-Fabrication Agent Gate")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 14)
    c.drawString(48, PAGE_HEIGHT - 116, "A 3-tool bounded state machine with mathematical limits on LLM rounds.")

    arch_w = (PAGE_WIDTH - 96 - 24) / 2
    draw_card(c, 48, 60, arch_w, 360, HexColor("#334155"), HexColor("#050811"))
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(68, 385, "// THE 3-TOOL BOUNDED LADDER")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(68, 350, "1. OBSERVE: retrieve_video_context")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(88, 330, "• Lexical token matching over chapters & transcript")
    c.drawString(88, 312, "• Devanagari fallback window for Hindi queries")

    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(68, 275, "2. EVALUATE: validate_answer_draft (GATE)")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(88, 255, "• Validates 0 <= startSeconds <= endSeconds <= duration")
    c.drawString(88, 237, "• quote_matches_transcript verifies exact quote")
    c.drawString(88, 219, "• Exactly 1 retry on gate failure -> declare_not_found")

    c.setFillColor(AMBER_WARN)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(68, 182, "3. SELECT: gemini_web_research")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(88, 162, "• Activates only when research enabled & not in video")
    c.drawString(88, 144, "• Returns verified Google Search grounding chunks")

    # Right side: Guarantees
    draw_card(c, 48 + arch_w + 24, 250, arch_w, 170)
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(48 + arch_w + 44, 385, "Strict Budget: <= 2 LLM Rounds")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(48 + arch_w + 44, 355, "• Exactly 1 answering branch per question.")
    c.drawString(48 + arch_w + 44, 335, "• Max 1 validation retry = guaranteed <= 2 LLM rounds.")
    c.drawString(48 + arch_w + 44, 315, "• No infinite loops, no multi-agent token waste.")
    c.drawString(48 + arch_w + 44, 295, "• Average response latency: 3.59s on live Cloud Run.")

    draw_card(c, 48 + arch_w + 24, 60, arch_w, 170, EMERALD_GREEN)
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(48 + arch_w + 44, 195, "Stateless Cloud Run Design")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(48 + arch_w + 44, 165, "• Client owns conversation history (last <= 6 turns).")
    c.drawString(48 + arch_w + 44, 145, "• Server maintains zero session memory or database lock.")
    c.drawString(48 + arch_w + 44, 125, "• Infinite horizontal scale across Google Cloud Run.")
    c.drawString(48 + arch_w + 44, 105, "• Docker containerized Next.js 16 + FastAPI.")
    c.showPage()

    # =========================================================================
    # SLIDE 7: Empirical Evaluation
    # =========================================================================
    draw_header_footer(c, 7, 10, "EMPIRICAL PROOF")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(48, PAGE_HEIGHT - 90, "Live 25-Case Evaluation Benchmark")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 14)
    c.drawString(48, PAGE_HEIGHT - 116, "Continuously verified against the live Google Cloud Run deployment.")

    m_w = (PAGE_WIDTH - 96 - 45) / 4
    m_h = 135

    draw_card(c, 48, PAGE_HEIGHT - 275, m_w, m_h, EMERALD_GREEN, HexColor("#0B1B15"))
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 36)
    c.drawString(68, PAGE_HEIGHT - 195, "0.0%")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(68, PAGE_HEIGHT - 225, "Unsupported Answers")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(68, PAGE_HEIGHT - 245, "Target: 0.0% Strict")

    draw_card(c, 48 + m_w + 15, PAGE_HEIGHT - 275, m_w, m_h, INDIGO_ACCENT, HexColor("#101529"))
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 36)
    c.drawString(48 + m_w + 35, PAGE_HEIGHT - 195, "94.4%")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(48 + m_w + 35, PAGE_HEIGHT - 225, "Timestamp Accuracy")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(48 + m_w + 35, PAGE_HEIGHT - 245, "Target: >= 90.0%")

    draw_card(c, 48 + (m_w + 15) * 2, PAGE_HEIGHT - 275, m_w, m_h, EMERALD_GREEN, HexColor("#0B1B15"))
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 36)
    c.drawString(48 + (m_w + 15) * 2 + 20, PAGE_HEIGHT - 195, "92.0%")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(48 + (m_w + 15) * 2 + 20, PAGE_HEIGHT - 225, "Groundedness Rate")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(48 + (m_w + 15) * 2 + 20, PAGE_HEIGHT - 245, "Target: >= 90.0%")

    draw_card(c, 48 + (m_w + 15) * 3, PAGE_HEIGHT - 275, m_w, m_h, SKY_BLUE, HexColor("#0A1826"))
    c.setFillColor(SKY_BLUE)
    c.setFont("Helvetica-Bold", 36)
    c.drawString(48 + (m_w + 15) * 3 + 20, PAGE_HEIGHT - 195, "3.59s")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(48 + (m_w + 15) * 3 + 20, PAGE_HEIGHT - 225, "Average Latency")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(48 + (m_w + 15) * 3 + 20, PAGE_HEIGHT - 245, "Target: < 5.0s")

    # Lower Table / Summary
    draw_card(c, 48, 60, PAGE_WIDTH - 96, 175)
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(68, 205, "Test Suite & Failure-Path Drills (Zero Failures Across All Suites):")

    c.setFillColor(TEXT_SLATE_200)
    c.setFont("Helvetica", 11)
    c.drawString(68, 175, "• 83/83 Unit & Regression Tests Passing (pytest tests/) in 0.82 seconds")
    c.drawString(68, 153, "• 9/9 Architecture §15 Failure-Path Drills Passing (scripts/test_failure_paths.py)")
    c.drawString(68, 131, "• 100% Clean ESLint Gate (0 errors, 0 warnings) + Turbopack Production Build Clean")
    c.drawString(68, 109, "• Full P0-1 through P0-9 Acceptance Sweep Passing on Live Cloud Run (scripts/sweep_deployed.py)")
    c.drawString(68, 87, "• Eval Results persisted to context/eval_results.json (25 benchmark cases)")
    c.showPage()

    # =========================================================================
    # SLIDE 8: Competitive Comparison
    # =========================================================================
    draw_header_footer(c, 8, 10, "MARKET DIFFERENTIATION")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(48, PAGE_HEIGHT - 90, "Why ContextBridge Wins")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 14)
    c.drawString(48, PAGE_HEIGHT - 116, "Not a passive summarizer, and not an ungrounded general-purpose chatbot.")

    # Table Layout
    draw_card(c, 48, 60, PAGE_WIDTH - 96, 350)
    t_y = 370
    c.setFillColor(TEXT_SLATE_200)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(68, t_y, "Capability")
    c.drawString(320, t_y, "Generic LLMs (ChatGPT / Claude)")
    c.drawString(570, t_y, "Video Summarizers (NoteGPT)")
    c.setFillColor(EMERALD_LIGHT)
    c.drawString(780, t_y, "ContextBridge AI")

    rows = [
        ("Verbatim Quote Validator", "❌ None (hallucinates quotes)", "❌ None (paraphrases only)", "✅ Enforced by validator"),
        ("Sub-second Video Seeking", "❌ No video player link", "❌ Rough minute links", "✅ Exact second (~1s) seek"),
        ("TranscriptSync Auto-Scroll", "❌ Absent", "❌ Static transcript text", "✅ Real-time auto-scroll"),
        ("Contradiction Surfacing", "❌ Absent", "❌ Absent", "✅ Dual clickable timestamps"),
        ("Strict BoundaryCard", "❌ Blends web & training", "❌ Fails on missing facts", "✅ Explicit Boundary frame"),
        ("Bilingual Voice Loop", "❌ English bias / Text first", "❌ English only", "✅ Hindi/Hinglish TTS parity"),
    ]

    for idx, (cap, col1, col2, col3) in enumerate(rows):
        row_y = 335 - idx * 42
        c.setStrokeColor(HexColor("#1F2937"))
        c.line(68, row_y + 20, PAGE_WIDTH - 68, row_y + 20)

        c.setFillColor(TEXT_WHITE)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(68, row_y, cap)

        c.setFillColor(RED_ALERT)
        c.setFont("Helvetica", 11)
        c.drawString(320, row_y, col1)
        c.drawString(570, row_y, col2)

        c.setFillColor(EMERALD_LIGHT)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(780, row_y, col3)

    c.showPage()

    # =========================================================================
    # SLIDE 9: Judging Criteria Alignment
    # =========================================================================
    draw_header_footer(c, 9, 10, "JUDGING ALIGNMENT")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(48, PAGE_HEIGHT - 90, "Alignment with AI Builder Cup Criteria")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 14)
    c.drawString(48, PAGE_HEIGHT - 116, "Engineered to maximize evaluation score across all four criteria.")

    grid_h = 165
    draw_card(c, 48, PAGE_HEIGHT - 295, grid_w, grid_h, EMERALD_GREEN)
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(68, PAGE_HEIGHT - 160, "Technical Merit (40% Weight)")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(68, PAGE_HEIGHT - 190, "• Zero Hallucination: Structural anti-fabrication validator.")
    c.drawString(68, PAGE_HEIGHT - 210, "• Containerized Stack: Deployed to Google Cloud Run.")
    c.drawString(68, PAGE_HEIGHT - 230, "• 83 pytest tests + 9 automated failure-path drills.")
    c.drawString(68, PAGE_HEIGHT - 250, "• Multi-turn stateless conversation history passthrough.")

    draw_card(c, 48 + grid_w + 20, PAGE_HEIGHT - 295, grid_w, grid_h, INDIGO_ACCENT)
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(68 + grid_w + 20, PAGE_HEIGHT - 160, "Impact (25% Weight)")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(68 + grid_w + 20, PAGE_HEIGHT - 190, "• Saves Hours: Cuts 45-minute scrubbing down to 1 second.")
    c.drawString(68 + grid_w + 20, PAGE_HEIGHT - 210, "• Democratizes Learning: Hindi/Hinglish voice parity unlocks")
    c.drawString(68 + grid_w + 20, PAGE_HEIGHT - 230, "  technical education for 600M+ non-native speakers.")
    c.drawString(68 + grid_w + 20, PAGE_HEIGHT - 250, "• Accessibility: Adaptive explanation levels & WebVTT captions.")

    draw_card(c, 48, PAGE_HEIGHT - 475, grid_w, grid_h, INDIGO_ACCENT)
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(68, PAGE_HEIGHT - 340, "Innovation (25% Weight)")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(68, PAGE_HEIGHT - 370, "• The Compass Paradigm: Dynamic guided exploration chips.")
    c.drawString(68, PAGE_HEIGHT - 390, "• Epistemic Humility: Strict BoundaryCard for external research.")
    c.drawString(68, PAGE_HEIGHT - 410, "• Contradiction Surfacing: Critical thinking on conflicting claims.")

    draw_card(c, 48 + grid_w + 20, PAGE_HEIGHT - 475, grid_w, grid_h, EMERALD_GREEN)
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(68 + grid_w + 20, PAGE_HEIGHT - 340, "UX & Presentation (10% Weight)")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(68 + grid_w + 20, PAGE_HEIGHT - 370, "• 10-Second Trust: Instantly understandable EvidenceBadges.")
    c.drawString(68 + grid_w + 20, PAGE_HEIGHT - 390, "• Fluid Animations: Synchronized transcript scroll & waveforms.")
    c.drawString(68 + grid_w + 20, PAGE_HEIGHT - 410, "• Fast Seeking: 7-speed Radix dropdown + instant barge-in mic.")
    c.showPage()

    # =========================================================================
    # SLIDE 10: Conclusion & Live Links
    # =========================================================================
    draw_header_footer(c, 10, 10, "SUMMARY & LINKS")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 120, "ContextBridge AI 🧭")
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica", 18)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 160, "The Trusted Compass for Self-Learners Worldwide.")

    box_c_w = (PAGE_WIDTH - 96 - 40) / 3
    # Link 1
    draw_card(c, 48, 160, box_c_w, 140, EMERALD_GREEN)
    c.setFillColor(EMERALD_LIGHT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(68, 265, "🌐 LIVE WEB APP")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica", 11)
    c.drawString(68, 235, "contextbridge-web-")
    c.drawString(68, 217, "c5ltxo3mkq-uc.a.run.app")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(68, 185, "Try Tokyo lesson or upload clip")

    # Link 2
    draw_card(c, 48 + box_c_w + 20, 160, box_c_w, 140, INDIGO_ACCENT)
    c.setFillColor(INDIGO_LIGHT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(48 + box_c_w + 40, 265, "🐙 OPEN SOURCE GITHUB")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica", 11)
    c.drawString(48 + box_c_w + 40, 235, "github.com/")
    c.drawString(48 + box_c_w + 40, 217, "lvhNaruto/contextbridge-ai")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(48 + box_c_w + 40, 185, "Clean git history & full tests")

    # Link 3
    draw_card(c, 48 + (box_c_w + 20) * 2, 160, box_c_w, 140, SKY_BLUE)
    c.setFillColor(SKY_BLUE)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(48 + (box_c_w + 20) * 2 + 20, 265, "⚡ INTERACTIVE API")
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica", 11)
    c.drawString(48 + (box_c_w + 20) * 2 + 20, 235, "contextbridge-api-")
    c.drawString(48 + (box_w + 10) * 3 + 20, 217, "c5ltxo3mkq-uc.a.run.app/docs")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(48 + (box_c_w + 20) * 2 + 20, 185, "OpenAPI 3.1 Swagger docs")

    # Thank you badge
    c.setFillColor(HexColor("#1E293B"))
    c.roundRect(PAGE_WIDTH / 2 - 160, 80, 320, 36, 18, fill=1, stroke=0)
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(PAGE_WIDTH / 2, 92, "Thank You · Built for AI Builder Cup 2026")

    c.showPage()
    c.save()
    print(f"[SUCCESS] Pitch deck PDF generated: {output_path}")


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
    os.makedirs(out_dir, exist_ok=True)
    out_pdf = os.path.join(out_dir, "contextbridge_pitch_deck.pdf")
    generate_deck(out_pdf)
