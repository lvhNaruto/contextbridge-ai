from __future__ import annotations

import json
import os
import re
import time
import uuid
from pathlib import Path
from typing import Any

import streamlit as st
from dotenv import load_dotenv

from contextbridge_schema import MediaAnalysis
from contextbridge_store import (
    create_analysis,
    get_analysis,
    initialize,
    list_analyses,
    update_analysis,
)

APP_DIR = Path(__file__).resolve().parent
load_dotenv(APP_DIR / ".env.local")
load_dotenv(APP_DIR / ".env")
initialize()

st.set_page_config(
    page_title="ContextBridge",
    page_icon=":material/video_library:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _init_session_state() -> None:
    defaults: dict[str, Any] = {
        "page": "learn",
        "analysis": None,
        "analysis_id": None,
        "video_bytes": None,
        "video_filename": None,
        "video_mime_type": None,
        "conversation": [],
        "settings": {
            "answer_language": "Same as question",
            "explanation_level": "Beginner",
            "research_missing": True,
        },
        "selected_start": 0.0,
        "is_recording": False,
        "audio_question_bytes": None,
        "processing": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


_init_session_state()


def _config(name: str, default: str = "") -> str:
    value = os.getenv(name, "")
    if value:
        return value
    try:
        return str(st.secrets.get(name, default))
    except (FileNotFoundError, KeyError):
        return default


def _format_time(seconds: float) -> str:
    total = max(0, int(seconds))
    minutes, remaining = divmod(total, 60)
    hours, minutes = divmod(minutes, 60)
    return (
        f"{hours}:{minutes:02d}:{remaining:02d}"
        if hours
        else f"{minutes}:{remaining:02d}"
    )


def _parse_analysis(row: Any) -> MediaAnalysis | None:
    if row is None or not row["result_json"]:
        return None
    try:
        return MediaAnalysis.from_dict(json.loads(row["result_json"]))
    except Exception:
        return None


# -----------------------------------------------------------------------------
# Styling
# -----------------------------------------------------------------------------


def _load_css() -> None:
    css = """
    <style>
    :root { --cb-navy: #0B1020; --cb-panel: #151C32; --cb-panel-light: #1E2744; --cb-purple: #7C3AED; --cb-purple-light: #A78BFA; --cb-text: #F8FAFC; --cb-muted: #94A3B8; --cb-border: rgba(148,163,184,0.18); --cb-radius: 18px; --cb-radius-sm: 12px; }
    .stApp { background: var(--cb-navy) !important; }
    [data-testid="stSidebar"] { background: var(--cb-panel) !important; border-right: 1px solid var(--cb-border); }
    h1, h2, h3, h4, h5, h6 { color: var(--cb-text) !important; font-weight: 600 !important; }
    .cb-hero { text-align: center; padding: 3rem 1rem 2rem; }
    .cb-hero h1 { font-size: 2.6rem; margin-bottom: 0.6rem; background: linear-gradient(90deg, #F8FAFC 0%, #A78BFA 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .cb-hero p { color: var(--cb-muted); font-size: 1.15rem; max-width: 640px; margin: 0 auto 1.5rem; }
    .cb-upload-card { background: var(--cb-panel); border: 2px dashed var(--cb-border); border-radius: var(--cb-radius); padding: 2.5rem 2rem; text-align: center; transition: border-color 0.2s ease; }
    .cb-upload-card:hover { border-color: var(--cb-purple-light); }
    .cb-chip { display: inline-block; background: var(--cb-panel-light); border: 1px solid var(--cb-border); border-radius: 999px; padding: 0.35rem 0.85rem; margin: 0.25rem; color: var(--cb-text); font-size: 0.9rem; }
    .cb-chapter { background: var(--cb-panel); border: 1px solid var(--cb-border); border-radius: var(--cb-radius-sm); padding: 0.9rem 1rem; margin-bottom: 0.6rem; cursor: pointer; transition: all 0.15s ease; }
    .cb-chapter:hover { border-color: var(--cb-purple-light); background: var(--cb-panel-light); }
    .cb-chapter.active { border-color: var(--cb-purple); background: rgba(124,58,237,0.12); }
    .cb-chapter-time { color: var(--cb-purple-light); font-weight: 700; font-variant-numeric: tabular-nums; min-width: 48px; }
    .cb-chapter-title { color: var(--cb-text); font-weight: 600; margin-bottom: 0.15rem; }
    .cb-chapter-desc { color: var(--cb-muted); font-size: 0.9rem; line-height: 1.35; }
    .cb-chat-pill { display: flex; align-items: center; background: #FFFFFF; border-radius: 999px; padding: 0.35rem 0.35rem 0.35rem 1.2rem; box-shadow: 0 4px 24px rgba(0,0,0,0.18); max-width: 760px; margin: 0 auto; }
    .cb-chat-pill input { flex: 1; border: none; outline: none; background: transparent; color: #0F172A; font-size: 1rem; padding: 0.6rem 0; }
    .cb-chat-pill input::placeholder { color: #64748B; }
    .cb-mic-btn { width: 40px; height: 40px; border-radius: 50%; border: none; background: var(--cb-panel-light); color: var(--cb-purple); cursor: pointer; display: flex; align-items: center; justify-content: center; transition: background 0.2s ease; }
    .cb-mic-btn:hover { background: #E9D5FF; }
    .cb-mic-btn.recording { background: #FEE2E2; color: #DC2626; animation: pulse 1.2s infinite; }
    @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.08); } 100% { transform: scale(1); } }
    .cb-message { max-width: 760px; margin: 0 auto 1rem; }
    .cb-message-user { background: var(--cb-panel-light); border: 1px solid var(--cb-border); border-radius: var(--cb-radius-sm); border-bottom-right-radius: 4px; padding: 0.8rem 1rem; color: var(--cb-text); margin-left: auto; width: fit-content; max-width: 85%; }
    .cb-message-assistant { padding: 0.4rem 0; color: var(--cb-text); }
    .cb-teacher-label { color: var(--cb-purple-light); font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.3rem; }
    .cb-badge { display: inline-flex; align-items: center; gap: 0.35rem; background: rgba(124,58,237,0.15); color: var(--cb-purple-light); border-radius: 999px; padding: 0.25rem 0.7rem; font-size: 0.78rem; font-weight: 600; margin-right: 0.4rem; }
    .cb-badge.web { background: rgba(56,189,248,0.15); color: #38BDF8; }
    .cb-confidence { color: var(--cb-muted); font-size: 0.8rem; }
    .cb-source-card { background: var(--cb-panel); border: 1px solid var(--cb-border); border-radius: var(--cb-radius-sm); padding: 0.7rem 0.9rem; margin-top: 0.5rem; }
    .cb-source-card a { color: var(--cb-purple-light); text-decoration: none; font-weight: 500; }
    .cb-lesson-card { background: var(--cb-panel); border: 1px solid var(--cb-border); border-radius: var(--cb-radius-sm); padding: 1rem; margin-bottom: 0.75rem; }
    .cb-lesson-title { color: var(--cb-text); font-weight: 600; margin-bottom: 0.25rem; }
    .cb-lesson-meta { color: var(--cb-muted); font-size: 0.85rem; }
    .cb-status { display: flex; align-items: center; gap: 0.6rem; color: var(--cb-muted); font-size: 0.95rem; padding: 0.5rem 0; }
    .cb-spinner { width: 18px; height: 18px; border: 2px solid var(--cb-border); border-top-color: var(--cb-purple); border-radius: 50%; animation: spin 0.8s linear infinite; }
    @keyframes spin { to { transform: rotate(360deg); } }
    button:focus-visible, input:focus-visible, a:focus-visible { outline: 2px solid var(--cb-purple-light); outline-offset: 2px; }
    .cb-workspace h2 a, .cb-workspace h3 a { display: none !important; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


_load_css()



# -----------------------------------------------------------------------------
# Mock data for functional prototype
# -----------------------------------------------------------------------------


def _mock_analysis() -> MediaAnalysis:
    return MediaAnalysis.from_dict(
        {
            "summary": (
                "An introduction to binary language: how computers represent "
                "information using only 0 and 1, with practical examples."
            ),
            "language": "English",
            "topics": ["binary", "computers", "data representation"],
            "events": [
                {
                    "id": "ch-1",
                    "startSeconds": 0,
                    "endSeconds": 173,
                    "title": "Introduction",
                    "description": "Welcomes learners and explains what the lesson will cover.",
                    "confidence": 0.98,
                    "evidence": [{"startSeconds": 0, "endSeconds": 15, "quote": "Today we will learn how computers speak."}],
                },
                {
                    "id": "ch-2",
                    "startSeconds": 173,
                    "endSeconds": 376,
                    "title": "What is binary language?",
                    "description": "Defines binary as a two-state counting system built from 0 and 1.",
                    "confidence": 0.96,
                    "evidence": [{"startSeconds": 180, "endSeconds": 210, "quote": "Binary language uses only two digits: zero and one."}],
                },
                {
                    "id": "ch-3",
                    "startSeconds": 376,
                    "endSeconds": 642,
                    "title": "How computers represent information",
                    "description": "Shows how bits encode numbers, text, images, and sound.",
                    "confidence": 0.94,
                    "evidence": [{"startSeconds": 400, "endSeconds": 430, "quote": "Every letter, pixel, and note becomes a pattern of bits."}],
                },
                {
                    "id": "ch-4",
                    "startSeconds": 642,
                    "endSeconds": 860,
                    "title": "Practical example",
                    "description": "Walks through converting a small number to binary.",
                    "confidence": 0.95,
                    "evidence": [{"startSeconds": 650, "endSeconds": 680, "quote": "To write five in binary, we use one-zero-one."}],
                },
                {
                    "id": "ch-5",
                    "startSeconds": 860,
                    "endSeconds": 1000,
                    "title": "Summary",
                    "description": "Recaps that binary is the foundation of digital information.",
                    "confidence": 0.97,
                    "evidence": [{"startSeconds": 870, "endSeconds": 890, "quote": "Binary turns the physical world into digital information."}],
                },
            ],
            "transcript": [
                {"startSeconds": 0, "endSeconds": 15, "text": "Today we will learn how computers speak."},
                {"startSeconds": 180, "endSeconds": 210, "text": "Binary language uses only two digits: zero and one."},
                {"startSeconds": 400, "endSeconds": 430, "text": "Every letter, pixel, and note becomes a pattern of bits."},
                {"startSeconds": 650, "endSeconds": 680, "text": "To write five in binary, we use one-zero-one."},
                {"startSeconds": 870, "endSeconds": 890, "text": "Binary turns the physical world into digital information."},
            ],
        }
    )


WEB_SOURCES = [
    {
        "title": "Binary number - Wikipedia",
        "domain": "wikipedia.org",
        "url": "https://en.wikipedia.org/wiki/Binary_number",
    },
    {
        "title": "How Computers Work: Binary & Data",
        "domain": "code.org",
        "url": "https://code.org/education/computers",
    },
]




def _mock_answer(question: str, analysis: MediaAnalysis, settings: dict[str, Any]) -> dict[str, Any]:
    """Return a mock answer grounded in the sample video or web research."""
    q = question.lower().strip()
    lang = settings.get("answer_language", "Same as question")
    level = settings.get("explanation_level", "Beginner")
    research = settings.get("research_missing", True)

    if any(word in q for word in ["binary", "0 and 1", "zero and one", "bits"]):
        answer = (
            "Binary language is the way computers represent information using only two symbols: "
            "0 and 1. The video introduces this idea at 02:53. Each 0 or 1 is called a bit, and "
            "groups of bits can represent numbers, letters, sounds, and images."
        )
        if level == "Beginner":
            answer = (
                "Binary language is like a light switch that is either off (0) or on (1). "
                "The video explains at 02:53 that computers use these two states to store every kind of information."
            )
        elif level == "Expert":
            answer = (
                "Binary is a base-2 positional numeral system. As the video states at 02:53, "
                "all digital information is encoded as sequences of bits, which map to voltage levels "
                "in hardware and are interpreted by instruction sets."
            )
        if lang == "Hindi":
            answer = (
                "बाइनरी भाषा वह तरीका है जिससे कंप्यूटर सूचना को 0 और 1 के रूप में दर्शाते हैं। "
                "वीडियो इस विचार को 02:53 पर समझाता है।"
            )
        return {
            "type": "video",
            "answer": answer,
            "start_seconds": 173,
            "end_seconds": 376,
            "confidence": 0.96,
        }

    if any(word in q for word in ["computer", "represent", "information", "store"]):
        answer = (
            "Computers represent information by turning it into patterns of bits. "
            "The video covers this at 06:16, explaining that numbers, text, images, and sound all become binary patterns."
        )
        if lang == "Hindi":
            answer = (
                "कंप्यूटर सूचना को बिट्स के पैटर्न में बदलकर दर्शाते हैं। "
                "वीडियो इसे 06:16 पर समझाता है।"
            )
        return {
            "type": "video",
            "answer": answer,
            "start_seconds": 376,
            "end_seconds": 642,
            "confidence": 0.94,
        }

    if any(word in q for word in ["example", "five", "5", "convert"]):
        answer = (
            "At 10:42 the video shows a practical example: the number five is written as 101 in binary. "
            "That is 4 (2²) plus 1 (2⁰), with no 2¹ place."
        )
        if level == "Beginner":
            answer = (
                "At 10:42 the video shows that five in binary is 101. "
                "Think of it as one group of four, no twos, and one single."
            )
        if lang == "Hindi":
            answer = "10:42 पर वीडियो में उदाहरण दिखाया गया है: पांच को बाइनरी में 101 लिखा जाता है।"
        return {
            "type": "video",
            "answer": answer,
            "start_seconds": 642,
            "end_seconds": 860,
            "confidence": 0.95,
        }

    if research:
        answer = (
            "The video mentions related ideas, but does not fully answer this question. "
            "Here is additional context from web research."
        )
        if lang == "Hindi":
            answer = (
                "वीडियो में इस प्रश्न का पूर्ण उत्तर नहीं दिया गया है। "
                "वेब शोध से अतिरिक्त संदर्भ नीचे दिया गया है।"
            )
        return {
            "type": "web",
            "answer": answer,
            "sources": WEB_SOURCES,
            "confidence": 0.72,
        }

    answer = "The video does not explain this, and web research is turned off, so I cannot answer confidently."
    if lang == "Hindi":
        answer = "वीडियो में इसे नहीं बताया गया है और वेब शोध बंद है, इसलिए मैं इसका उत्तर नहीं दे सकता।"
    return {"type": "unknown", "answer": answer}


def _jump_to(seconds: float) -> None:
    st.session_state["selected_start"] = max(0.0, float(seconds))



# -----------------------------------------------------------------------------
# Navigation and sidebar
# -----------------------------------------------------------------------------


def _render_sidebar() -> None:
    st.sidebar.markdown("## :material/video_library: ContextBridge")
    st.sidebar.caption("Turn any educational video into a conversation.")
    st.sidebar.divider()

    nav = st.sidebar.radio(
        "Navigation",
        options=["Learn", "My lessons", "Accessibility", "Help"],
        index=["learn", "lessons", "accessibility", "help"].index(st.session_state["page"]),
        label_visibility="collapsed",
    )
    page_map = {"Learn": "learn", "My lessons": "lessons", "Accessibility": "accessibility", "Help": "help"}
    if nav and page_map[nav] != st.session_state["page"]:
        st.session_state["page"] = page_map[nav]
        st.rerun()

    st.sidebar.divider()
    st.sidebar.markdown("### My lessons")
    analyses = list_analyses(limit=20)
    if not analyses:
        st.sidebar.info("No lessons yet. Upload a video to get started.")
    for row in analyses:
        analysis = _parse_analysis(row)
        chapter_count = len(analysis.events) if analysis else 0
        with st.sidebar.container():
            cols = st.sidebar.columns([4, 1])
            cols[0].markdown(
                f"<div class='cb-lesson-title'>{row['filename']}</div>"
                f"<div class='cb-lesson-meta'>{chapter_count} chapters • {row['updated_at'][:10]}</div>",
                unsafe_allow_html=True,
            )
            if cols[1].button(":material/play_arrow:", key=f"resume-{row['analysis_id']}", help="Resume lesson"):
                if analysis:
                    st.session_state["analysis"] = analysis
                    st.session_state["analysis_id"] = row["analysis_id"]
                    st.session_state["video_filename"] = row["filename"]
                    st.session_state["conversation"] = []
                    st.session_state["page"] = "learn"
                    st.rerun()
                else:
                    st.sidebar.warning("This lesson is still processing or failed.")


def _render_help() -> None:
    st.markdown("<div class='cb-hero'><h1>Help</h1></div>", unsafe_allow_html=True)
    st.markdown(
        """
        **How do I upload a video?**
        Go to *Learn*, drag a supported video file into the upload area, and click *Analyze video*.

        **What formats are supported?**
        MP4, MOV, MPEG, WEBM, and AVI.

        **How do I ask a question?**
        Type in the chat pill below the video and press Enter, or click the microphone to record.

        **What does “From video” mean?**
        The answer is grounded in the uploaded video and shows the exact timestamp where the evidence appears.

        **What does “Web research” mean?**
        The video does not contain a full answer, so ContextBridge searched the web and is showing trusted sources.
        """
    )


def _render_accessibility() -> None:
    st.markdown("<div class='cb-hero'><h1>Accessibility settings</h1></div>", unsafe_allow_html=True)
    st.toggle("High-contrast mode", value=False, key="cb-high-contrast", help="Increase contrast across the interface")
    st.toggle("Reduce motion", value=False, key="cb-reduce-motion", help="Disable animations")
    st.select_slider("Text size", options=["Small", "Medium", "Large"], value="Medium", key="cb-text-size")
    st.checkbox("Always show captions when available", value=True, key="cb-captions")
    st.success("Settings are saved for this session.")



# -----------------------------------------------------------------------------
# Landing / upload page
# -----------------------------------------------------------------------------


def _trigger_demo() -> None:
    analysis_id = f"demo-{uuid.uuid4().hex[:12]}"
    analysis = _mock_analysis()
    create_analysis(analysis_id, "Demo: Introduction to binary language", "video/mp4")
    update_analysis(analysis_id, status="completed", result=analysis.to_dict())
    st.session_state["analysis_id"] = analysis_id
    st.session_state["analysis"] = analysis
    st.session_state["video_filename"] = "Demo: Introduction to binary language"
    st.session_state["conversation"] = []
    st.session_state["selected_start"] = 0.0
    st.rerun()


def _handle_upload(uploaded_file: Any, use_real_api: bool) -> None:
    if uploaded_file is None:
        return
    analysis_id = f"analysis-{uuid.uuid4().hex[:12]}"
    video_bytes = uploaded_file.getvalue()
    mime_type = uploaded_file.type or "video/mp4"
    create_analysis(analysis_id, uploaded_file.name, mime_type)
    st.session_state["analysis_id"] = analysis_id
    st.session_state["video_filename"] = uploaded_file.name
    st.session_state["video_bytes"] = video_bytes
    st.session_state["video_mime_type"] = mime_type
    st.session_state["conversation"] = []
    st.session_state["selected_start"] = 0.0

    if not use_real_api:
        # Prototype path: save mock result immediately so the UI is testable.
        update_analysis(analysis_id, status="completed", result=_mock_analysis().to_dict())
        st.session_state["analysis"] = _mock_analysis()
        st.rerun()
        return

    update_analysis(analysis_id, status="processing")
    try:
        storage_uri = _upload_to_cloud_storage(analysis_id, uploaded_file.name, video_bytes, mime_type)
        model_id = _config("VERTEX_MODEL_ID", "gemini-2.5-flash")
        analysis = _vertex_analysis(video_bytes, mime_type, model_id)
        update_analysis(
            analysis_id,
            status="completed",
            result=analysis.to_dict(),
            storage_uri=storage_uri,
        )
        st.session_state["analysis"] = analysis
    except Exception as exc:
        update_analysis(analysis_id, status="failed", error=str(exc))
        st.error(f"Analysis failed: {exc}")


def _render_landing() -> None:
    st.markdown(
        """
        <div class="cb-hero">
            <h1>Turn any educational video into a conversation.</h1>
            <p>Ask questions, jump to the right moment, and understand more without watching everything again.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("<div class='cb-upload-card'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Drag and drop a video here",
            type=["mp4", "mov", "mpeg", "webm", "avi"],
            label_visibility="collapsed",
            help="Supported formats: MP4, MOV, MPEG, WEBM, AVI",
        )
        if uploaded_file:
            st.caption(f"Selected: {uploaded_file.name}")
        use_real_api = st.toggle(
            "Analyze with real Gemini API (requires credentials)",
            value=False,
            help="If off, the prototype uses realistic mock data so the UI can be tested immediately.",
        )
        analyze_clicked = st.button(
            "Analyze video",
            type="primary",
            icon=":material/auto_awesome:",
            disabled=uploaded_file is None,
            use_container_width=True,
        )
        if analyze_clicked and uploaded_file is not None:
            _handle_upload(uploaded_file, use_real_api)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='text-align:center; margin-top:1rem; color:#94A3B8; font-size:0.9rem;'>or try a demo lesson</div>", unsafe_allow_html=True)
        if st.button("Try the binary-language demo", icon=":material/play_circle:", use_container_width=False):
            _trigger_demo()

        st.markdown(
            """
            <div style="text-align:center; margin-top:1.25rem;">
                <span class="cb-chip">Lectures</span>
                <span class="cb-chip">Programming tutorials</span>
                <span class="cb-chip">Exam preparation</span>
                <span class="cb-chip">Workplace training</span>
                <span class="cb-chip">Public-service videos</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()
    st.markdown(
        "**Privacy note:** Uploaded videos are analyzed to create chapters and a transcript. "
        "Data is stored locally in this prototype unless cloud storage is configured.",
        help="Set GOOGLE_PROJECT_ID and CONTEXTBRIDGE_BUCKET to enable cloud-backed analysis.",
    )



# -----------------------------------------------------------------------------
# Video learning workspace
# -----------------------------------------------------------------------------


def _render_workspace(analysis: MediaAnalysis) -> None:
    st.markdown("<div class='cb-workspace'>", unsafe_allow_html=True)
    st.markdown(f"## {st.session_state.get('video_filename', 'Untitled lesson')}")

    video_col, chapter_col = st.columns([2.2, 1])

    with video_col:
        video_bytes = st.session_state.get("video_bytes")
        if video_bytes:
            st.video(video_bytes, start_time=int(st.session_state["selected_start"]))
        else:
            st.info("Demo mode: no video file is loaded, so the player uses a placeholder. Upload a real video to watch it here.")
            st.video("https://storage.googleapis.com/coverr-main/mp4/Mt_Baker.mp4", start_time=int(st.session_state["selected_start"]))

    with chapter_col:
        st.markdown("### In this video")
        for event in analysis.events:
            is_active = event.start_seconds <= st.session_state["selected_start"] < event.end_seconds
            active_class = "active" if is_active else ""
            container = st.container()
            with container:
                st.markdown(
                    f"""
                    <div class="cb-chapter {active_class}" role="button" aria-label="Jump to {event.title} at {_format_time(event.start_seconds)}">
                        <div style="display:flex; gap:0.75rem; align-items:flex-start;">
                            <div class="cb-chapter-time">{_format_time(event.start_seconds)}</div>
                            <div style="flex:1;">
                                <div class="cb-chapter-title">{event.title}</div>
                                <div class="cb-chapter-desc">{event.description}</div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(
                    "Jump to moment",
                    key=f"jump-{event.id}",
                    icon=":material/play_arrow:",
                    help=f"Play from {_format_time(event.start_seconds)}",
                ):
                    _jump_to(event.start_seconds)
                    st.rerun()

    st.divider()
    _render_settings_bar()
    _render_conversation()
    _render_chat_input()
    st.markdown("</div>", unsafe_allow_html=True)


def _render_settings_bar() -> None:
    settings = st.session_state["settings"]
    cols = st.columns([1.2, 1.2, 1.4, 3])
    with cols[0]:
        settings["answer_language"] = st.selectbox(
            "Answer language",
            options=["Same as question", "English", "Hindi"],
            index=["Same as question", "English", "Hindi"].index(settings["answer_language"]),
            label_visibility="collapsed",
            help="Language used for the AI answer",
        )
    with cols[1]:
        settings["explanation_level"] = st.selectbox(
            "Explanation level",
            options=["Beginner", "Intermediate", "Expert"],
            index=["Beginner", "Intermediate", "Expert"].index(settings["explanation_level"]),
            label_visibility="collapsed",
            help="How simple or technical the explanation should be",
        )
    with cols[2]:
        settings["research_missing"] = st.toggle(
            "Research missing context on Google",
            value=settings["research_missing"],
        )
    with cols[3]:
        st.empty()




def _render_conversation() -> None:
    st.markdown("### Conversation")
    conversation = st.session_state.get("conversation", [])
    if not conversation:
        st.markdown(
            "<div style='text-align:center; color:#94A3B8; padding:1.5rem 0;'>"
            "Ask your first question about this lesson.</div>",
            unsafe_allow_html=True,
        )
        return

    for index, message in enumerate(conversation):
        if message["role"] == "user":
            st.markdown(
                f"<div class='cb-message'><div class='cb-message-user'>{message['content']}</div></div>",
                unsafe_allow_html=True,
            )
        else:
            with st.container():
                st.markdown("<div class='cb-message'><div class='cb-message-assistant'>", unsafe_allow_html=True)
                st.markdown("<div class='cb-teacher-label'>Teacher</div>", unsafe_allow_html=True)
                st.write(message["content"])

                if message.get("type") == "video":
                    start = message.get("start_seconds", 0)
                    end = message.get("end_seconds", start)
                    confidence = message.get("confidence", 0)
                    cols = st.columns([1.2, 1, 3])
                    cols[0].markdown("<span class='cb-badge'>From video</span>", unsafe_allow_html=True)
                    cols[1].markdown(f"<span class='cb-confidence'>{confidence:.0%} confidence</span>", unsafe_allow_html=True)
                    if cols[2].button(
                        f"Jump to {_format_time(start)}",
                        key=f"jump-answer-{index}-{start}",
                        icon=":material/play_arrow:",
                    ):
                        _jump_to(start)
                        st.rerun()
                    if end > start:
                        st.caption(f"Evidence from {_format_time(start)} – {_format_time(end)}")

                elif message.get("type") == "web":
                    st.markdown("<span class='cb-badge web'>Web research</span>", unsafe_allow_html=True)
                    if message.get("confidence"):
                        st.caption(f"Confidence: {message['confidence']:.0%}")
                    st.markdown("**Sources**")
                    for source in message.get("sources", []):
                        st.markdown(
                            f"""
                            <div class="cb-source-card">
                                <a href="{source['url']}" target="_blank" rel="noopener noreferrer">{source['title']}</a>
                                <div style="color:#94A3B8; font-size:0.8rem;">{source['domain']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                if message.get("audio_url"):
                    st.audio(message["audio_url"])
                st.markdown("</div></div>", unsafe_allow_html=True)




def _submit_question(question: str, is_voice: bool = False) -> None:
    if not question.strip():
        return
    analysis = st.session_state.get("analysis")
    if not isinstance(analysis, MediaAnalysis):
        return

    st.session_state["conversation"].append(
        {"role": "user", "content": question.strip(), "is_voice": is_voice}
    )
    st.session_state["processing"] = "Searching video evidence…"

    # Simulate network delay for realistic UX
    time.sleep(0.4)
    result = _mock_answer(question.strip(), analysis, st.session_state["settings"])

    assistant_message: dict[str, Any] = {"role": "assistant", "is_voice": is_voice}
    if result["type"] == "video":
        assistant_message.update(
            {
                "content": result["answer"],
                "type": "video",
                "start_seconds": result["start_seconds"],
                "end_seconds": result["end_seconds"],
                "confidence": result["confidence"],
            }
        )
    elif result["type"] == "web":
        assistant_message.update(
            {
                "content": result["answer"],
                "type": "web",
                "answer": result["answer"],
                "sources": result.get("sources", []),
                "confidence": result.get("confidence"),
            }
        )
    else:
        assistant_message.update({"content": result["answer"], "type": "unknown"})

    if is_voice and st.session_state["settings"]["answer_language"] == "Hindi":
        assistant_message["audio_url"] = _mock_hindi_tts(result["answer"])
    elif is_voice:
        assistant_message["audio_url"] = _mock_english_tts(result["answer"])

    st.session_state["conversation"].append(assistant_message)
    st.session_state["processing"] = None


def _on_text_submit() -> None:
    question = st.session_state.get("chat-question", "")
    if question and question.strip():
        st.session_state["chat-question"] = ""
        _submit_question(question, is_voice=False)
        st.rerun()


def _render_chat_input() -> None:
    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

    chat_css = """
    <style>
    .cb-chat-pill-wrapper {
        background: #FFFFFF;
        border-radius: 999px;
        padding: 0.3rem 0.5rem 0.3rem 1rem;
        box-shadow: 0 4px 24px rgba(0,0,0,0.18);
        max-width: 760px;
        margin: 0 auto;
        display: flex;
        align-items: center;
    }
    .cb-chat-pill-wrapper [data-testid="stTextInput"] {
        flex: 1;
    }
    .cb-chat-pill-wrapper [data-testid="stTextInput"] input {
        border: none !important;
        background: transparent !important;
        color: #0F172A !important;
        font-size: 1rem !important;
        padding: 0.55rem 0 !important;
    }
    .cb-chat-pill-wrapper [data-testid="stTextInput"] input:focus {
        box-shadow: none !important;
    }
    .cb-chat-pill-wrapper button {
        border-radius: 50% !important;
        min-width: 40px !important;
        height: 40px !important;
        padding: 0 !important;
    }
    </style>
    """
    st.markdown(chat_css, unsafe_allow_html=True)

    st.markdown("<div class='cb-chat-pill-wrapper'>", unsafe_allow_html=True)
    cols = st.columns([10, 1, 1], gap="small")
    with cols[0]:
        st.text_input(
            "Ask anything about this lesson",
            placeholder="Ask anything about this lesson…",
            label_visibility="collapsed",
            key="chat-question",
            on_change=_on_text_submit,
        )
    with cols[1]:
        send_clicked = st.button(
            ":material/send:",
            key="send-question",
            help="Send question",
        )
    with cols[2]:
        mic_clicked = st.button(
            ":material/mic:",
            key="mic-toggle-real",
            help="Record a voice question",
        )
    st.markdown("</div>", unsafe_allow_html=True)

    if send_clicked:
        _on_text_submit()

    if mic_clicked:
        st.session_state["is_recording"] = not st.session_state.get("is_recording", False)
        st.rerun()

    if st.session_state.get("is_recording"):
        st.markdown(
            "<div class='cb-status'><div class='cb-spinner'></div>Recording... speak your question</div>",
            unsafe_allow_html=True,
        )
        audio = st.audio_input("Record your question", key="voice-question")
        if audio is not None:
            transcription = _mock_transcribe(audio)
            st.session_state["is_recording"] = False
            _submit_question(transcription, is_voice=True)
            st.rerun()
        if st.button("Cancel recording", key="cancel-recording"):
            st.session_state["is_recording"] = False
            st.rerun()


def _mock_transcribe(audio: Any) -> str:
    # In a real implementation this would call a speech-to-text API.
    return "What does binary language mean?"


def _mock_english_tts(text: str) -> str:
    # In a real implementation this would call Google Cloud Text-to-Speech.
    return "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"


def _mock_hindi_tts(text: str) -> str:
    # In a real implementation this would call Google Cloud Text-to-Speech with hi-IN.
    return "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"



# -----------------------------------------------------------------------------
# Backend helpers (ready for real API wiring)
# -----------------------------------------------------------------------------


def _upload_to_cloud_storage(
    analysis_id: str, filename: str, video_bytes: bytes, mime_type: str
) -> str | None:
    bucket_name = _config("CONTEXTBRIDGE_BUCKET")
    if not bucket_name:
        return None
    try:
        from google.cloud import storage
    except ImportError as exc:
        raise RuntimeError(
            "Cloud Storage is configured but google-cloud-storage is missing."
        ) from exc
    client = storage.Client(project=_config("GOOGLE_PROJECT_ID"))
    safe_filename = re.sub(r"[^A-Za-z0-9._-]+", "_", Path(filename).name)
    blob = client.bucket(bucket_name).blob(f"analyses/{analysis_id}/{safe_filename}")
    blob.upload_from_string(video_bytes, content_type=mime_type)
    return f"gs://{bucket_name}/{blob.name}"


def _vertex_analysis(video_bytes: bytes, mime_type: str, model_id: str) -> MediaAnalysis:
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel, Part
    except ImportError as exc:
        raise RuntimeError(
            "The Vertex AI SDK is missing. Run `pip install -r requirements.txt`."
        ) from exc

    project_id = _config("GOOGLE_PROJECT_ID")
    if not project_id:
        raise RuntimeError(
            "GOOGLE_PROJECT_ID is not configured. Set it in .env.local or Streamlit secrets."
        )
    vertexai.init(project=project_id, location=_config("GOOGLE_REGION", "us-central1"))
    prompt = """
Analyze this video for ContextBridge. Return JSON only.
Required keys:
summary, language, topics, events, transcript.
Each event must contain id, startSeconds, endSeconds, title, description,
confidence, and evidence. Each evidence item must contain startSeconds,
endSeconds, and quote. Each transcript item must contain startSeconds,
endSeconds, and text.

Rules:
- Use seconds from the beginning of the video.
- Keep events chronological and include only meaningful moments.
- Separate observable facts from interpretation.
- Do not invent speech, events, or timestamps.
- If speech is unclear, omit it rather than guessing.
- Confidence must be between 0 and 1.
"""
    response = GenerativeModel(model_id).generate_content(
        [Part.from_data(data=video_bytes, mime_type=mime_type), prompt]
    )
    raw = response.text or ""
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    if not raw:
        raise RuntimeError("Gemini returned an empty analysis response.")
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Gemini response was not valid JSON: {exc}") from exc
    return MediaAnalysis.from_dict(parsed)


def _ask_gemini(
    question: str,
    analysis: MediaAnalysis,
    settings: dict[str, Any],
    video_bytes: bytes | None = None,
    mime_type: str | None = None,
) -> dict[str, Any]:
    """Placeholder for the real /analyses/:id/questions endpoint."""
    # In production this would call Gemini with video + transcript context.
    return _mock_answer(question, analysis, settings)


def _text_to_speech(text: str, language_code: str = "en-US") -> bytes:
    try:
        from google.cloud import texttospeech
    except ImportError as exc:
        raise RuntimeError("google-cloud-texttospeech is not installed.") from exc
    client = texttospeech.TextToSpeechClient(project=_config("GOOGLE_PROJECT_ID"))
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )
    return response.audio_content


def _render_lessons() -> None:
    st.markdown("<div class='cb-hero'><h1>My lessons</h1></div>", unsafe_allow_html=True)
    analyses = list_analyses(limit=50)
    if not analyses:
        st.info("You haven't analyzed any videos yet. Go to Learn to upload one.")
        return

    for row in analyses:
        analysis = _parse_analysis(row)
        chapter_count = len(analysis.events) if analysis else 0
        status_color = "green" if row["status"] == "completed" else "orange"
        with st.container(border=True):
            cols = st.columns([4, 2, 1])
            cols[0].markdown(
                f"""
                <div class='cb-lesson-title'>{row['filename']}</div>
                <div class='cb-lesson-meta'>{row['updated_at'][:10]} • {chapter_count} chapters</div>
                """,
                unsafe_allow_html=True,
            )
            cols[1].markdown(f"<span style='color:{status_color};'>{row['status'].capitalize()}</span>", unsafe_allow_html=True)
            if cols[2].button("Resume", key=f"lib-resume-{row['analysis_id']}", type="primary"):
                if analysis:
                    st.session_state["analysis"] = analysis
                    st.session_state["analysis_id"] = row["analysis_id"]
                    st.session_state["video_filename"] = row["filename"]
                    st.session_state["conversation"] = []
                    st.session_state["page"] = "learn"
                    st.rerun()
                else:
                    st.warning("This lesson is not ready yet.")



# -----------------------------------------------------------------------------
# App entry point
# -----------------------------------------------------------------------------


def main() -> None:
    _render_sidebar()

    page = st.session_state["page"]
    analysis = st.session_state.get("analysis")

    if page == "help":
        _render_help()
        return

    if page == "accessibility":
        _render_accessibility()
        return

    if page == "lessons":
        _render_lessons()
        return

    # Learn page
    if isinstance(analysis, MediaAnalysis):
        _render_workspace(analysis)
    else:
        _render_landing()


if __name__ == "__main__":
    main()

