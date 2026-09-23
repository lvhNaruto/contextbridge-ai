"""The ContextBridge Q&A agent (P0-1b) — ARCHITECTURE.md §6.3 loop.

Observe → Reason → Select → Act → Evaluate over exactly three tools
(api/tools.py), always terminating in a valid ChatMessage (API.md §2):

  * gemini_answer found=true  → evidenceType "video" + verified evidence
  * found=false + research on → evidenceType "web" + real grounded sources
  * found=false + research off→ evidenceType "unknown" (declare_not_found)
  * draft failed the gate on the
    ladder's single retry     → declare_not_found (§6.3 Fallback)
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

import secrets
import time
from typing import Any

from api import pipeline, tools
from api.config import Settings

# The locked mock shows 0.72 for web answers (web/lib/demo-answers.ts);
# AssistantAnswer.confidence is a required field in the locked types.
_WEB_CONFIDENCE = 0.72


def _chat_message(answer: dict[str, Any], *, is_voice: bool) -> dict[str, Any]:
    """Wrap a verified AssistantAnswer in the ChatMessage envelope (API §2)."""
    return {
        "id": f"msg-{secrets.token_hex(3)}",
        "role": "assistant",
        "text": answer["text"],
        "isVoice": is_voice,
        "createdAt": int(time.time() * 1000),  # epoch ms — a NUMBER, not a string
        "answer": answer,
    }


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
    # Observe — top-k evidence slices, no LLM (§8 retrieve_video_context).
    slices = tools.retrieve_video_context(envelope, question)

    # Act on the video branch; the draft gate inside gemini_answer is Evaluate.
    try:
        draft = tools.gemini_answer(
            question, slices, envelope, qa_settings, settings, history
        )
    except tools.AnswerValidationExhausted:
        # §6.3 Fallback: the model could not produce a *verified* video answer
        # even with its one retry — honest refusal, never an unverified jump
        # button. The §6.4 round budget is spent, so no web round is taken.
        return _chat_message(tools.declare_not_found(qa_settings), is_voice=is_voice)
    except pipeline.PipelineError:
        raise  # infra failure → the endpoint's honest 502 (§6.5 last resort)

    if draft["found"]:
        video_answer: dict[str, Any] = {
            "text": draft["text"],
            "evidenceType": "video",
            "evidence": draft["evidence"],
            "confidence": draft["confidence"],
        }
        return _chat_message(video_answer, is_voice=is_voice)

    # Reason: the video does not answer it. Select per researchMissingContext.
    if qa_settings.get("researchMissingContext", False):
        try:
            research = tools.gemini_web_research(question, qa_settings, settings)
        except pipeline.PipelineError:
            pass  # §6.5 — a failed web search degrades to honest not-found
        else:
            web_answer = {
                "text": research["text"],
                "evidenceType": "web",
                "confidence": _WEB_CONFIDENCE,
                "sources": research["sources"],
                "notInVideo": True,  # API §2 inv. 2 — video and web never blend
            }
            return _chat_message(web_answer, is_voice=is_voice)

    return _chat_message(tools.declare_not_found(qa_settings), is_voice=is_voice)