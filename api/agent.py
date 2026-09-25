"""The ContextBridge Q&A agent (P0-1b) — ARCHITECTURE.md §6.3 loop.

Observe → Reason → Select → Act → Evaluate over exactly three tools
(api/tools.py), always terminating in a valid ChatMessage (API.md §2):

  * gemini_answer found=true  → evidenceType "video" + verified evidence
  * found=false + research on → evidenceType "web" + real grounded sources
  * found=false + research off→ evidenceType "unknown" (declare_not_found)
  * draft failed the gate on the
    ladder's single retry     → declare_not_found (§6.3 Fallback)
  * video-referential query   → declare_not_found (blocks irrelevant web search)
  * web research failed       → declare_not_found (§6.5 branch fallback)
  * infra failure (credentials,
    quota, SDK — never a draft)→ PipelineError → endpoint maps to 502 (§6.5)

Budget (§6.4): exactly one answering branch per answer; the video attempt's
single retry is the second LLM round, so a failed attempt never opens a
third (web) round.

Stateless per request (§5.2, §9): inputs are the stored envelope, the
question, the settings and (from P0-7 on) optional client-owned history —
nothing is stored server-side. Wire-up: POST /analyses/{id}/questions in
api/main.py; tools and verification live in api/tools.py.
"""

from __future__ import annotations

import json
import logging
import re
import secrets
import time
from typing import Any

from api import pipeline, tools
from api.config import Settings

logger = logging.getLogger(__name__)

# The locked mock shows 0.72 for web answers (web/lib/demo-answers.ts);
# AssistantAnswer.confidence is a required field in the locked types.
_WEB_CONFIDENCE = 0.72


def _chat_message(
    answer: dict[str, Any],
    *,
    is_voice: bool,
    suggestions: list[str] | None = None,
) -> dict[str, Any]:
    """Wrap a verified AssistantAnswer in the ChatMessage envelope (API §2)."""
    msg: dict[str, Any] = {
        "id": f"msg-{secrets.token_hex(3)}",
        "role": "assistant",
        "text": answer["text"],
        "isVoice": is_voice,
        "createdAt": int(time.time() * 1000),  # epoch ms — a NUMBER, not a string
        "answer": answer,
    }
    if suggestions:
        msg["suggestions"] = suggestions
    return msg


_AMBIGUOUS_KEYWORDS = frozenset({
    "what", "why", "how", "explain", "tell me", "help", "hello", "hi", "hey", "video",
    "kya", "kaise", "kyun", "batao", "samjhao", "kya hai", "madad",
    "क्या", "कैसे", "क्यों", "बताओ", "समझाइए", "नमस्ते", "मदद"
})


def _is_ambiguous_query(text: str) -> bool:
    cleaned = text.strip().lower().strip("?!.,।")
    if not cleaned or (len(cleaned.split()) <= 1 and cleaned in _AMBIGUOUS_KEYWORDS):
        return True
    return False


def _wants_simplification(text: str) -> bool:
    low = text.strip().lower()
    return any(p in low for p in (
        "i don't understand", "i dont understand", "samajh nahi", "samajh nhi",
        "confused", "explain simply", "simple terms", "eli5", "easy words",
        "saral bhasha", "kuch samajh nahi"
    ))


def _is_video_referential_query(query: str) -> bool:
    """Detect if query specifically asks about internal video contents, speaker, or timeline."""
    q = query.lower()
    markers = (
        "in the video",
        "in this video",
        "of this video",
        "from this video",
        "about this video",
        "this video",
        "the video",
        "in video",
        "start of the video",
        "end of the video",
        "beginning of the video",
        "in the start",
        "at the start",
        "start of",
        "in the starting",
        "at the starting",
        "starting of",
        "at the beginning",
        "in the beginning",
        "beginning of",
        "at the end",
        "in the end",
        "end of",
        "on screen",
        "on-screen",
        "in the clip",
        "in this clip",
        "this clip",
        "the clip",
        "in the short",
        "in this short",
        "in the lecture",
        "in this lecture",
        "this lecture",
        "the lecture",
        "did the speaker",
        "does the speaker",
        "speaker say",
        "speaker mention",
        "the speaker",
        "what is shown",
        "what does it show",
        "shown in",
        "mentioned in",
        "video me",
        "video mein",
        "video k",
        "video ke",
        "video pr",
        "video par",
        "video pe",
        "screen par",
        "screen pr",
        "screen pe",
        "shuru me",
        "shuru mein",
        "shuruaat me",
        "video ke shuru",
        "video ke start",
        "video ke end",
        "speaker ne",
        "speaker kya",
        "वीडियो में",
        "वीडियो के",
        "वीडियो पर",
        "वीडियो",
        "स्क्रीन पर",
        "स्क्रीन",
        "शुरुआत में",
        "शुरू में",
        "स्पीकर ने",
        "दिखाया गया",
    )
    return any(m in q for m in markers)


def derive_suggestions(envelope: dict[str, Any], current_question: str) -> list[str]:
    """Derive 2–3 next-explore questions from the video's own content (D-25).

    Zero extra LLM calls: inspects unused chapters, topics, and contradictions.
    """
    suggestions: list[str] = []
    q_norm = current_question.lower()

    # 1. Contradictions if available and not already asked
    for pair in envelope.get("contradictions", []):
        claim = str(pair.get("claim", "")).strip()
        if claim and claim.lower() not in q_norm:
            clean_claim = claim if len(claim) <= 45 else f"{claim[:42]}..."
            suggestions.append(f"Why is there a contradiction about {clean_claim}?")
            break

    # 2. Chapters not mentioned
    chapters = envelope.get("events") or envelope.get("chapters") or []
    for ch in chapters:
        title = str(ch.get("title", "")).strip()
        if not title:
            continue
        if title.lower() not in q_norm and len(title) > 3:
            clean_title = title if len(title) <= 40 else f"{title[:37]}..."
            suggestions.append(f"What happens in '{clean_title}'?")
        if len(suggestions) >= 2:
            break

    # 3. Topics if we still need more
    for topic in envelope.get("topics", []):
        topic_str = str(topic).strip()
        if topic_str and topic_str.lower() not in q_norm:
            suggestions.append(f"How does the video explain {topic_str}?")
        if len(suggestions) >= 3:
            break

    return suggestions[:3]


def _log_run(
    question: str,
    branch: str,
    verified: bool,
    retries: int,
    t0: float,
    cost_estimate: float,
    is_voice: bool,
) -> None:
    latency_ms = round((time.perf_counter() - t0) * 1000, 2)
    entry = {
        "event": "agent_run",
        "branch": branch,
        "verified": verified,
        "retries": retries,
        "latency_ms": latency_ms,
        "cost_estimate_usd": cost_estimate,
        "is_voice": is_voice,
        "question_preview": question[:80],
    }
    logger.info("AGENT_RUN_METRIC %s", json.dumps(entry))


def answer_question(
    question: str,
    envelope: dict[str, Any],
    qa_settings: dict[str, Any],
    settings: Settings,
    *,
    is_voice: bool = False,
    history: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    """Run one agent round and return the resolved assistant ChatMessage.

    Observe is the deterministic retrieval; Evaluate (timestamps within
    [0, duration], quote fuzzy-matched to the stored transcript, confidence
    in [0, 1]) lives inside gemini_answer's draft gate; this function does
    Select plus the honest fallbacks.
    """
    t0 = time.perf_counter()
    retries = 0
    suggestions = derive_suggestions(envelope, question)

    # Move: Clarify ambiguous or ultra-short input without wasting LLM budget
    if _is_ambiguous_query(question):
        topics = envelope.get("topics") or []
        first_topic = str(topics[0]) if topics else "this video"
        ans_lang = (qa_settings.get("answerLanguage") or "auto").lower()
        is_hindi = ans_lang == "hi" or bool(re.search(r"[\u0900-\u097F]", question)) or any(
            w in question.lower() for w in ("kya", "kaise", "kyun", "batao", "samjhao", "madad")
        )
        if is_hindi:
            topic_str = first_topic if first_topic != "this video" else "इस वीडियो"
            clarify_text = f"कृपया बताएं कि आप {topic_str} के बारे में क्या जानना चाहते हैं? नीचे दिए गए सुझावों में से चुनें।"
        else:
            clarify_text = f"Could you please specify what you would like to explore about {first_topic}? You can tap one of the suggested questions below."
        _log_run(question, "clarify", False, 0, t0, 0.0, is_voice)
        return _chat_message(
            {
                "text": clarify_text,
                "evidenceType": "unknown",
                "confidence": 0.0,
                "notInVideo": True,  # API §2 inv. 3 — unknown always carries notInVideo
            },
            is_voice=is_voice,
            suggestions=suggestions,
        )

    # Move: Simplify if the student expressed confusion or asked for beginner level
    active_qa_settings = dict(qa_settings)
    if _wants_simplification(question):
        active_qa_settings["explanationLevel"] = "beginner"

    # Observe — top-k evidence slices, no LLM (§8 retrieve_video_context).
    slices = tools.retrieve_video_context(envelope, question)
    is_video_ref = _is_video_referential_query(question)

    # Act on the video branch; the draft gate inside gemini_answer is Evaluate.
    try:
        draft = tools.gemini_answer(
            question, slices, envelope, active_qa_settings, settings, history
        )
    except tools.AnswerValidationExhausted:
        # §6.3 Fallback: the model could not produce a *verified* video answer
        # even with its one retry — honest refusal, never an unverified jump
        # button. The §6.4 round budget is spent, so no web round is taken.
        retries = 1
        _log_run(question, "not_found", False, retries, t0, 0.00025, is_voice)
        return _chat_message(
            tools.declare_not_found(active_qa_settings, is_video_referential=is_video_ref),
            is_voice=is_voice,
            suggestions=suggestions,
        )
    except pipeline.PipelineError:
        raise  # infra failure → the endpoint's honest 502 (§6.5 last resort)

    if draft["found"]:
        _log_run(question, "video", True, retries, t0, 0.00015, is_voice)
        video_answer: dict[str, Any] = {
            "text": draft["text"],
            "evidenceType": "video",
            "evidence": draft["evidence"],
            "confidence": draft["confidence"],
        }
        return _chat_message(video_answer, is_voice=is_voice, suggestions=suggestions)

    # Reason: the video does not answer it. Select per researchMissingContext.
    # Video-referential queries (e.g. "what's at the start of this video") must NOT
    # trigger public Google search, because public search does not have access to
    # the user's private/uploaded video and returns confusing external disclaimers.
    if active_qa_settings.get("researchMissingContext", False) and not is_video_ref:
        try:
            logger.info("Triggering gemini_web_research for: %s", question)
            research = tools.gemini_web_research(question, active_qa_settings, settings)
        except pipeline.PipelineError as exc:
            logger.warning("gemini_web_research failed in agent: %s", exc)
            pass  # §6.5 — a failed web search degrades to honest not-found
        else:
            _log_run(question, "web", True, retries, t0, 0.00035, is_voice)
            web_answer = {
                "text": research["text"],
                "evidenceType": "web",
                "confidence": _WEB_CONFIDENCE,
                "sources": research["sources"],
                "notInVideo": True,  # API §2 inv. 2 — video and web never blend
            }
            return _chat_message(web_answer, is_voice=is_voice, suggestions=suggestions)

    _log_run(question, "not_found", False, retries, t0, 0.00008, is_voice)
    return _chat_message(
        tools.declare_not_found(active_qa_settings, is_video_referential=is_video_ref),
        is_voice=is_voice,
        suggestions=suggestions,
    )
