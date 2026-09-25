"""P0-1a tool tests — retrieval, answer-draft validation, research shape.

Zero LLM calls: gemini_answer is exercised with the provider ladder stubbed
(monkeypatched `_clients` / `_generate_json`), everything else is pure code.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from types import SimpleNamespace

from api import pipeline, tools


def _settings() -> SimpleNamespace:
    """Minimal settings stand-in — only what _call_with_ladder touches."""
    return SimpleNamespace(vertex_model_id="test-model")

FIXTURE = Path(__file__).resolve().parent.parent / "api" / "fixtures" / "demo_binary.json"


@pytest.fixture(scope="module")
def envelope() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


# --- retrieve_video_context (deterministic) --------------------------------


def test_retrieve_ranks_relevant_event(envelope: dict):
    slices = tools.retrieve_video_context(envelope, "What feature is introduced?")
    event_ids = [e["id"] for e in slices["events"]]
    assert "ch-videoboost" in event_ids
    texts = [s["text"] for s in slices["transcript"]]
    assert any("Video Boost" in t or "Night Sight" in t for t in texts)
    # chronological order preserved for prompt coherence
    starts = [s["startSeconds"] for s in slices["transcript"]]
    assert starts == sorted(starts)


def test_retrieve_no_overlap_returns_fewer_slices(envelope: dict):
    slices = tools.retrieve_video_context(envelope, "zjxqv wkmbp florbnax")
    assert slices["events"] == []
    assert slices["transcript"] == []


def test_retrieve_devanagari_query_returns_bounded_fallback(envelope: dict):
    # Pure Devanagari Hindi question against English video
    slices = tools.retrieve_video_context(envelope, "सायका शिमाडा टोक्यो में क्या काम करती हैं?")
    assert len(slices["transcript"]) > 0
    assert len(slices["events"]) > 0
    # Chronological ordering preserved
    starts = [s["startSeconds"] for s in slices["transcript"]]
    assert starts == sorted(starts)


# --- quote verification (the anti-fabrication net) -------------------------


def test_quote_matches_transcript(envelope: dict):
    assert tools.quote_matches_transcript(
        "Tokyo has many faces. The city at night is totally different from what you see during the day.", envelope
    )
    # fuzzy: extra whitespace still matches
    assert tools.quote_matches_transcript(
        "Tokyo  has many faces. The city at night is totally different from what you see during the day.", envelope
    )
    # fabricated quote must NOT pass
    assert not tools.quote_matches_transcript(
        "The teacher says quantum computers run on binary.", envelope
    )
    assert not tools.quote_matches_transcript("", envelope)


def test_silent_video_event_quote_matching():
    silent_envelope = {
        "summary": "Silent short tutorial",
        "transcript": [],
        "events": [
            {
                "id": "ev-1",
                "title": "Unboxing Desk Setup Accessories",
                "description": "Showing three minimalist desk organizer trays on table.",
                "startSeconds": 0.0,
                "endSeconds": 5.0,
            }
        ],
    }
    # Verbatim match from event description
    assert tools.quote_matches_transcript(
        "Showing three minimalist desk organizer trays on table.", silent_envelope
    )
    # Verbatim match from event title
    assert tools.quote_matches_transcript(
        "Unboxing Desk Setup Accessories", silent_envelope
    )
    # Fabricated quote should still be rejected
    assert not tools.quote_matches_transcript(
        "The speaker talks about rocket science.", silent_envelope
    )


def test_retrieve_video_context_silent_video_baseline_events():
    silent_envelope = {
        "summary": "Silent short tutorial",
        "transcript": [],
        "events": [
            {
                "id": "ev-1",
                "title": "Opening the box",
                "description": "Unboxing scene",
                "startSeconds": 0.0,
                "endSeconds": 5.0,
            }
        ],
    }
    slices = tools.retrieve_video_context(silent_envelope, "what items are shown?")
    assert len(slices["events"]) > 0
    assert slices["events"][0]["id"] == "ev-1"


# --- validate_answer_draft (the Evaluate gate) ------------------------------


def _good_draft() -> dict:
    return {
        "text": "Video Boost is introduced at 00:13.",
        "found": True,
        "confidence": 0.96,
        "evidence": {
            "startSeconds": 13,
            "endSeconds": 21,
            "quote": "In low light, it activates 'Night Sight' to make the quality even better.",
        },
    }


def test_validate_answer_draft_accepts_video_evidence(envelope: dict):
    draft = tools.validate_answer_draft(_good_draft(), envelope)
    assert draft["found"] is True
    assert draft["confidence"] == 0.96
    assert draft["evidence"]["startSeconds"] == 13.0


@pytest.mark.parametrize(
    "mutation",
    [
        lambda d: d.update(evidence={**d["evidence"], "startSeconds": 900}),
        lambda d: d.update(evidence={**d["evidence"], "endSeconds": 100}),
        lambda d: d.update(evidence={**d["evidence"], "quote": "invented words"}),
        lambda d: d.update(confidence=1.7),
        lambda d: d.update(found="yes"),
        lambda d: d.update(text="  "),
        lambda d: d.update(evidence=None),
    ],
    ids=[
        "start-out-of-range",
        "end-before-start",
        "fabricated-quote",
        "confidence-out-of-range",
        "found-not-bool",
        "empty-text",
        "missing-evidence",
    ],
)
def test_validate_answer_draft_rejects_violations(envelope: dict, mutation):
    bad = _good_draft()
    mutation(bad)
    with pytest.raises(ValueError):
        tools.validate_answer_draft(bad, envelope)


def test_validate_answer_draft_not_found_carries_no_evidence(envelope: dict):
    draft = tools.validate_answer_draft(
        {"text": "The video does not cover this.", "found": False, "confidence": 0.9},
        envelope,
    )
    assert draft["found"] is False
    assert draft["confidence"] == 0.0  # forced to 0 — honest refusal
    assert "evidence" not in draft



# --- gemini_answer with a stubbed provider ladder ---------------------------


def _stub_ladder(monkeypatch, responses: list):
    calls = {"n": 0}

    def fake_generate(client, model_id, parts):
        calls["n"] += 1
        return responses[min(calls["n"] - 1, len(responses) - 1)]

    monkeypatch.setattr(pipeline, "_clients", lambda settings: [object()])
    monkeypatch.setattr(pipeline, "_generate_json", fake_generate)
    monkeypatch.setattr(pipeline.time, "sleep", lambda _: None)
    return calls


def test_gemini_answer_returns_validated_draft(monkeypatch, envelope: dict):
    _stub_ladder(monkeypatch, [_good_draft()])
    slices = tools.retrieve_video_context(envelope, "What is binary?")
    draft = tools.gemini_answer(
        "What is binary?",
        slices,
        envelope,
        {"answerLanguage": "auto", "explanationLevel": "beginner"},
        settings=_settings(),
    )
    assert draft["found"] is True
    assert draft["evidence"]["quote"] in " ".join(
        s["text"] for s in envelope["transcript"]
    )


def test_gemini_answer_retries_once_with_feedback(monkeypatch, envelope: dict):
    calls = _stub_ladder(
        monkeypatch,
        [
            {
                **_good_draft(),
                "evidence": {"startSeconds": 1, "endSeconds": 2, "quote": "fabricated"},
            },
            _good_draft(),
        ],
    )
    slices = tools.retrieve_video_context(envelope, "What is binary?")
    draft = tools.gemini_answer("q", slices, envelope, {}, settings=_settings())
    assert calls["n"] == 2  # one retry, then success (§6.3 Retry)
    assert draft["found"] is True


def test_gemini_answer_total_failure_raises_pipeline_error(monkeypatch, envelope: dict):
    _stub_ladder(monkeypatch, [{"garbage": True}])
    with pytest.raises(pipeline.PipelineError):
        tools.gemini_answer(
            "q", {"events": [], "transcript": []}, envelope, {}, _settings()
        )


def test_gemini_answer_prompt_uses_history(monkeypatch, envelope: dict):
    seen = {}

    def fake_generate(client, model_id, parts):
        seen["prompt"] = parts[0].text
        return {"text": "follow-up resolved", "found": False, "confidence": 0}

    monkeypatch.setattr(pipeline, "_clients", lambda settings: [object()])
    monkeypatch.setattr(pipeline, "_generate_json", fake_generate)
    history = [{"role": "user", "text": "earlier question"}] * 9  # > 6 turns
    tools.gemini_answer(
        "tell me more",
        {"events": [], "transcript": []},
        envelope,
        {},
        _settings(),
        history,
    )
    assert seen["prompt"].count("earlier question") == 6  # hard cap (P0-7)


# --- gemini_web_research helpers (no network) -------------------------------


def test_validate_research_draft_drops_malformed_sources():
    draft = tools.validate_research_draft(
        {
            "text": "From the web: …",
            "sources": [
                {"title": "OK", "url": "https://example.com/a", "description": "d"},
                {"title": "no url"},
                {"url": "notaurl"},
                "junk",
            ],
        }
    )
    assert len(draft["sources"]) == 1
    assert draft["sources"][0]["domain"] == "example.com"


def test_grounding_sources_tolerates_missing_metadata():
    assert tools._grounding_sources(object()) == []


# --- declare_not_found -------------------------------------------------------


def test_declare_not_found_shape_and_language():
    en = tools.declare_not_found({"answerLanguage": "auto"})
    assert en["evidenceType"] == "unknown"
    assert en["confidence"] == 0.0
    assert en["notInVideo"] is True
    assert "could not find" in en["text"]
    hi = tools.declare_not_found({"answerLanguage": "hi"})
    assert "वीडियो" in hi["text"]



# --- exception taxonomy (P0-1b: judgement failure vs infra failure) ----------


def test_validation_exhaustion_raises_distinct_error(monkeypatch, envelope: dict):
    _stub_ladder(monkeypatch, [{"garbage": True}])
    with pytest.raises(tools.AnswerValidationExhausted):
        tools.gemini_answer(
            "q", {"events": [], "transcript": []}, envelope, {}, _settings()
        )


def test_provider_failure_stays_plain_pipeline_error(monkeypatch, envelope: dict):
    def explode(client, model_id, parts):
        raise RuntimeError("quota exceeded")

    monkeypatch.setattr(pipeline, "_clients", lambda settings: [object()])
    monkeypatch.setattr(pipeline, "_generate_json", explode)
    monkeypatch.setattr(pipeline.time, "sleep", lambda _: None)
    with pytest.raises(pipeline.PipelineError) as excinfo:
        tools.gemini_answer(
            "q", {"events": [], "transcript": []}, envelope, {}, _settings()
        )
    assert not isinstance(excinfo.value, tools.AnswerValidationExhausted)


def test_answer_prompt_carries_stored_contradiction_pass(
    monkeypatch, envelope: dict
):
    assert envelope.get("contradictions"), "fixture must ship the D-02 pair"
    seen: dict = {}

    def fake_generate(client, model_id, parts):
        seen["prompt"] = parts[0].text
        return {"text": "ok", "found": False, "confidence": 0}

    monkeypatch.setattr(pipeline, "_clients", lambda settings: [object()])
    monkeypatch.setattr(pipeline, "_generate_json", fake_generate)
    tools.gemini_answer(
        "did the teacher contradict themselves?",
        {"events": [], "transcript": []},
        envelope,
        {},
        _settings(),
    )
    pair = envelope["contradictions"][0]
    assert pair["claim"] in seen["prompt"]
    assert pair["statementA"]["quote"] in seen["prompt"]
    assert pair["statementB"]["quote"] in seen["prompt"]


# --- P0-5: accessible artifacts (plain-language & Hindi) ---------------------


def test_answer_prompt_carries_accessible_settings(monkeypatch, envelope: dict):
    seen: dict = {}

    def fake_generate(client, model_id, parts):
        seen["prompt"] = parts[0].text
        return {"text": "ok", "found": False, "confidence": 0}

    monkeypatch.setattr(pipeline, "_clients", lambda settings: [object()])
    monkeypatch.setattr(pipeline, "_generate_json", fake_generate)
    tools.gemini_answer(
        "What is binary?",
        {"events": [], "transcript": []},
        envelope,
        {"explanationLevel": "beginner", "answerLanguage": "hi"},
        _settings(),
    )
    assert "Explanation level: beginner" in seen["prompt"]
    assert "Answer language: Hindi (Devanagari)" in seen["prompt"]


def test_answer_prompt_carries_expert_and_en_settings(monkeypatch, envelope: dict):
    seen: dict = {}

    def fake_generate(client, model_id, parts):
        seen["prompt"] = parts[0].text
        return {"text": "ok", "found": False, "confidence": 0}

    monkeypatch.setattr(pipeline, "_clients", lambda settings: [object()])
    monkeypatch.setattr(pipeline, "_generate_json", fake_generate)
    tools.gemini_answer(
        "What is binary?",
        {"events": [], "transcript": []},
        envelope,
        {"explanationLevel": "expert", "answerLanguage": "en"},
        _settings(),
    )
    assert "Explanation level: expert" in seen["prompt"]
    assert "Answer language: English" in seen["prompt"]


def test_accessible_answer_preserves_source_timestamps(envelope: dict):
    # P0-5 acceptance: accessible answer preserves source timestamps and quotes
    hindi_draft = {
        "text": "कम रोशनी में, यह वीडियो क्वालिटी को और बेहतर बनाने के लिए नाइट साइट को सक्रिय करता है।",
        "found": True,
        "confidence": 0.95,
        "evidence": {
            "startSeconds": 15,
            "endSeconds": 21,
            "quote": "In low light, it activates 'Night Sight' to make the quality even better.",
        },
    }
    validated = tools.validate_answer_draft(hindi_draft, envelope)
    assert validated["found"] is True
    assert validated["evidence"]["startSeconds"] == 15.0
    assert validated["evidence"]["endSeconds"] == 21.0
    assert "Night Sight" in validated["evidence"]["quote"]


def test_retrieve_video_context_supports_chapters_key():
    lesson = {
        "summary": "Demonstration of productivity tools",
        "chapters": [
            {
                "id": "ch-1",
                "startSeconds": 0,
                "endSeconds": 2,
                "title": "Title Screen with Google App Icons",
                "description": "Introduction showing various product icons",
            }
        ],
        "transcript": [],
    }
    slices = tools.retrieve_video_context(lesson, "how many product in the starting of the video")
    assert len(slices["events"]) >= 1
    assert slices["events"][0]["id"] == "ch-1"


def test_quote_matches_transcript_falls_back_to_chapter_events():
    envelope = {
        "transcript": [{"startSeconds": 5, "endSeconds": 10, "text": "Spoken audio later in the clip"}],
        "chapters": [
            {
                "id": "ch-1",
                "startSeconds": 0,
                "endSeconds": 2,
                "title": "Title screen introducing small micro-habits",
                "description": "Accompanied by various Google app icons",
            }
        ],
    }
    assert tools.quote_matches_transcript(
        "Title screen introducing small micro-habits", envelope
    ) is True


