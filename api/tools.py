"""Q&A agent tools (P0-1a) — ARCHITECTURE.md §6.3 cycle, §8 inventory.

Three read-only tools plus one terminal constructor:
  retrieve_video_context  deterministic field-weighted keyword retrieval over
                          the stored MediaAnalysis (no vector DB — a ≤ 15-min
                          transcript is ~2k words; retrieval only trims prompts)
  gemini_answer           LLM structured draft constrained to retrieved
                          evidence; output validated against the STORED
                          transcript before anything reaches the UI
  gemini_web_research     LLM + Google Search grounding; only when the video
                          lacks the answer AND researchMissingContext is on —
                          never blended with video evidence (API.md §2 inv. 2)
  declare_not_found       honest `unknown` / `notInVideo:true` / confidence 0

The agent loop itself lives in api/agent.py (P0-1b). Nothing here stores
state; every function is pure given its inputs (LLM calls excepted).
"""

from __future__ import annotations

import difflib
import json
import logging
import re
from typing import Any

from api import pipeline
from api.config import Settings

logger = logging.getLogger(__name__)

STOPWORDS = frozenset(
    "a an and are as at be by did do does for from had has have how i in is it "
    "of on or so that the their them they this to was we what when where which "
    "who why will with you your me my can could would should about into than "
    "then there here its it's not no yes".split()
)

_ANSWER_PROMPT = """
You are the ContextBridge answer engine. Answer the user's question using ONLY
the retrieved evidence slices from one analysed video. Return JSON only with
keys: text, found, evidence, confidence.

Rules:
- "found" is true only when the evidence slices genuinely answer the question.
  If they do not, set found=false, evidence=null, confidence=0 and make text a
  short honest statement that the video does not cover this.
- When found=true, evidence is an object with startSeconds, endSeconds and
  quote. quote MUST be copied verbatim from one of the provided transcript
  slices. Timestamps must be plain seconds within [0, durationSeconds].
- confidence is between 0 and 1.
- Write "text" at the requested explanation level and in the requested
  language. Mention the moment (mm:ss) when helpful.
- Never invent speech, facts, sources, or timestamps.

Question: {question}
Explanation level: {level}
Answer language: {language}
Video durationSeconds: {duration}
Video summary: {summary}
Recent conversation (for resolving follow-ups only):
{history}

Retrieved evidence slices (JSON):
{slices}
"""

_RESEARCH_PROMPT = """
You are the ContextBridge web-research tool. The analysed video does NOT
answer the user's question, and the user explicitly enabled "research missing
context". Use Google Search to answer briefly and factually. Return JSON only
with keys: text, sources.

Rules:
- "text" is a short answer in the requested language at the requested level,
  prefixed by a clear note that this comes from web research, not the video.
- "sources" is a list of 1-4 objects with keys title, domain, url,
  description. Only include sources you actually grounded on; never fabricate
  URLs. If grounding yields nothing, return an empty list.
- Answer language: {language}. Explanation level: {level}.

Question: {question}
"""

_NOT_FOUND_TEXT = {
    "en": (
        "I could not find an answer to that in this video, and web research "
        "is turned off. Try rephrasing, or enable “Research missing context”."
    ),
    "hi": (
        "इस वीडियो में इसका उत्तर नहीं मिला और वेब शोध बंद है। "
        "प्रश्न दोबारा लिखकर देखें या “Research missing context” चालू करें।"
    ),
}


# ---------------------------------------------------------------------------
# Tool 1 — retrieve_video_context (deterministic, no LLM)
# ---------------------------------------------------------------------------


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9']+", text.lower())
        if token not in STOPWORDS and len(token) > 1
    }


def _score(query_tokens: set[str], *fields: tuple[str, int]) -> int:
    """Field-weighted overlap: (text, weight) pairs → integer score."""
    total = 0
    for text, weight in fields:
        total += weight * len(query_tokens & _tokens(text))
    return total


def retrieve_video_context(
    envelope: dict[str, Any], question: str, *, top_k: int = 6
) -> dict[str, Any]:
    """Top-k evidence slices for a question over the stored analysis.

    Returns {"events": [...], "transcript": [...]} — both chronologically
    ordered after selection so the LLM sees coherent context. An empty-question
    or no-overlap result simply yields fewer slices; the LLM then judges
    coverage (that judgement is the agent's Reason step, §6.3).
    """
    query = _tokens(question)
    summary = str(envelope.get("summary") or "")

    scored_events: list[tuple[int, int, dict[str, Any]]] = []
    for index, event in enumerate(envelope.get("events", [])):
        quotes = " ".join(
            str(q.get("quote") or "") for q in event.get("evidence", [])
        )
        score = _score(
            query,
            (str(event.get("title") or ""), 3),
            (str(event.get("description") or ""), 2),
            (quotes, 2),
            (summary, 1),
        )
        if score:
            scored_events.append((-score, index, event))

    scored_segments: list[tuple[int, int, dict[str, Any]]] = []
    for index, segment in enumerate(envelope.get("transcript", [])):
        score = _score(query, (str(segment.get("text") or ""), 2))
        if score:
            scored_segments.append((-score, index, segment))

    events = [event for _, _, event in sorted(scored_events)[: max(1, top_k // 2)]]
    segments = [segment for _, _, segment in sorted(scored_segments)[:top_k]]
    # Chronological order beats rank order for prompt coherence.
    events.sort(key=lambda e: float(e.get("startSeconds") or 0))
    segments.sort(key=lambda s: float(s.get("startSeconds") or 0))
    return {"events": events, "transcript": segments}


# ---------------------------------------------------------------------------
# Shared verification helpers (the agent's Evaluate step, §6.3)
# ---------------------------------------------------------------------------


def _transcript_text(envelope: dict[str, Any]) -> str:
    return " ".join(
        str(seg.get("text") or "") for seg in envelope.get("transcript", [])
    )


def quote_matches_transcript(quote: str, envelope: dict[str, Any]) -> bool:
    """Fuzzy verbatim check: containment, then per-segment similarity ≥ 0.75.

    The UI renders the quote next to a jump button, so a quote the stored
    transcript does not contain is a fabrication — rejected, never rendered.
    """
    norm = lambda s: " ".join(s.lower().split())  # noqa: E731
    haystack = norm(_transcript_text(envelope))
    needle = norm(quote)
    if not needle:
        return False
    if needle in haystack:
        return True
    for segment in envelope.get("transcript", []):
        candidate = norm(str(segment.get("text") or ""))
        if (
            candidate
            and difflib.SequenceMatcher(None, needle, candidate).ratio() >= 0.75
        ):
            return True
    return False


def _check_seconds(value: Any, limit: float) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError("timestamps must be numbers")
    seconds = float(value)
    if not (0 <= seconds <= limit):
        raise ValueError(f"timestamp {seconds} outside [0, {limit}]")
    return seconds


def validate_answer_draft(
    parsed: dict[str, Any], envelope: dict[str, Any]
) -> dict[str, Any]:
    """The gemini_answer output gate (API.md §2 invariants 1 and 3).

    Raises ValueError on any contract violation — the caller feeds the error
    back for one retry (§6.3 Retry) before declaring not-found.
    """
    text = parsed.get("text")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("answer.text must be a non-empty string")
    found = parsed.get("found")
    if not isinstance(found, bool):
        raise ValueError("answer.found must be a boolean")
    confidence = parsed.get("confidence", 0)
    if (
        not isinstance(confidence, (int, float))
        or isinstance(confidence, bool)
        or not (0 <= float(confidence) <= 1)
    ):
        raise ValueError("answer.confidence must be in [0, 1]")

    draft: dict[str, Any] = {
        "text": text.strip(),
        "found": found,
        "confidence": round(float(confidence), 3) if found else 0.0,
    }
    if not found:
        return draft  # API §2 inv. 3 — honest refusal carries no evidence

    evidence = parsed.get("evidence")
    if not isinstance(evidence, dict):
        raise ValueError("found=true requires an evidence object")
    limit = pipeline.envelope_duration(envelope)
    start = _check_seconds(evidence.get("startSeconds"), limit)
    end = _check_seconds(evidence.get("endSeconds"), limit)
    if start > end:
        raise ValueError("evidence.startSeconds must be ≤ endSeconds")
    quote = evidence.get("quote")
    if not isinstance(quote, str) or not quote_matches_transcript(quote, envelope):
        raise ValueError("evidence.quote must match the stored transcript")
    draft["evidence"] = {
        "startSeconds": start,
        "endSeconds": end,
        "quote": quote.strip(),
    }
    return draft


# ---------------------------------------------------------------------------
# Tool 2 — gemini_answer (LLM, structured output, constrained to evidence)
# ---------------------------------------------------------------------------


def _language_directive(code: str) -> str:
    return {
        "auto": "the same language as the question",
        "en": "English",
        "hi": "Hindi (Devanagari)",
    }.get(code, "the same language as the question")


def gemini_answer(
    question: str,
    slices: dict[str, Any],
    envelope: dict[str, Any],
    qa_settings: dict[str, Any],
    settings: Settings,
    history: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    """Draft an answer constrained to retrieved slices; validate + retry once.

    Returns a validated draft: {text, found, confidence, evidence?}.
    Raises PipelineError only on total LLM failure (→ agent's honest 502).
    """
    history_text = "(none)"
    if history:
        history_text = "\n".join(
            f"{turn.get('role', 'user')}: {turn.get('text', '')}"
            for turn in history[-6:]  # P0-7 — never more than 6 turns
        )
    prompt = _ANSWER_PROMPT.format(
        question=question.strip(),
        level=qa_settings.get("explanationLevel", "beginner"),
        language=_language_directive(qa_settings.get("answerLanguage", "auto")),
        duration=pipeline.envelope_duration(envelope),
        summary=str(envelope.get("summary") or "")[:500],
        history=history_text,
        slices=json.dumps(slices, ensure_ascii=False)[:8000],
    )
    from google.genai import types

    base_parts = [types.Part.from_text(text=prompt)]
    return pipeline._call_with_ladder(
        settings,
        base_parts,
        lambda parsed: validate_answer_draft(parsed, envelope),
    )


# ---------------------------------------------------------------------------
# Tool 3 — gemini_web_research (LLM + Google Search grounding)
# ---------------------------------------------------------------------------


def _domain_of(url: str) -> str:
    match = re.search(r"https?://([^/]+)", url)
    return match.group(1).removeprefix("www.") if match else ""


def validate_research_draft(parsed: dict[str, Any]) -> dict[str, Any]:
    """Web answers must carry real, well-formed sources — never fabricated."""
    text = parsed.get("text")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("research.text must be a non-empty string")
    sources: list[dict[str, str]] = []
    for item in (parsed.get("sources") or [])[:4]:
        if not isinstance(item, dict):
            continue
        url = item.get("url")
        title = item.get("title")
        if not (isinstance(url, str) and url.startswith(("http://", "https://"))):
            continue  # drop malformed rather than fail the whole answer
        if not isinstance(title, str) or not title.strip():
            title = _domain_of(url) or url
        sources.append(
            {
                "title": title.strip(),
                "domain": str(item.get("domain") or _domain_of(url)),
                "url": url,
                "description": str(item.get("description") or "").strip(),
            }
        )
    return {"text": text.strip(), "sources": sources}


def _grounding_sources(response: Any) -> list[dict[str, str]]:
    """Pull real grounding chunks off the response — the anti-fabrication net."""
    sources: list[dict[str, str]] = []
    try:
        metadata = response.candidates[0].grounding_metadata
        for chunk in getattr(metadata, "grounding_chunks", None) or []:
            web = getattr(chunk, "web", None)
            uri = getattr(web, "uri", None)
            if uri:
                sources.append(
                    {
                        "title": getattr(web, "title", None) or _domain_of(uri),
                        "domain": _domain_of(uri),
                        "url": uri,
                        "description": "",
                    }
                )
    except (AttributeError, IndexError, TypeError):
        pass
    return sources[:4]


def gemini_web_research(
    question: str, qa_settings: dict[str, Any], settings: Settings
) -> dict[str, Any]:
    """Answer from the web with Google Search grounding (§8 tool inventory).

    Sources come from the response's grounding metadata when available
    (guaranteed real); the model's own JSON source list is the fallback,
    validated for shape. Raises PipelineError on failure — the agent degrades
    to declare_not_found, never to an invented source list (§6.5).
    """
    from google.genai import types

    prompt = _RESEARCH_PROMPT.format(
        question=question.strip(),
        language=_language_directive(qa_settings.get("answerLanguage", "auto")),
        level=qa_settings.get("explanationLevel", "beginner"),
    )
    last_error: Exception | None = None
    for client in pipeline._clients(settings):
        try:
            response = client.models.generate_content(
                model=settings.vertex_model_id,
                contents=[
                    types.Content(
                        role="user", parts=[types.Part.from_text(text=prompt)]
                    )
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                ),
            )
            raw = (response.text or "").strip()
            raw = (
                raw.removeprefix("```json").removeprefix("```").removesuffix("```")
            )
            draft = validate_research_draft(json.loads(raw))
            grounded = _grounding_sources(response)
            if grounded:
                draft["sources"] = grounded  # real chunks beat model-listed URLs
            if not draft["sources"]:
                raise ValueError("web research returned no usable sources")
            return draft
        except Exception as exc:  # noqa: BLE001 — any failure → next provider
            last_error = exc
            logger.warning("gemini_web_research failed on a provider: %s", exc)
    raise pipeline.PipelineError(f"web research failed: {last_error}")


# ---------------------------------------------------------------------------
# Terminal constructor — declare_not_found (no LLM)
# ---------------------------------------------------------------------------


def declare_not_found(qa_settings: dict[str, Any]) -> dict[str, Any]:
    """The honest unknown (API.md §2 invariant 3). Never an invention."""
    language = qa_settings.get("answerLanguage", "auto")
    text = _NOT_FOUND_TEXT["hi" if language == "hi" else "en"]
    return {
        "text": text,
        "evidenceType": "unknown",
        "confidence": 0.0,
        "notInVideo": True,
    }

