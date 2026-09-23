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
    slices = tools.retrieve_video_context(envelope, "What does binary language mean?")
    event_ids = [e["id"] for e in slices["events"]]
    assert "ch-binary" in event_ids
    texts = [s["text"] for s in slices["transcript"]]
    assert any("two digits" in t for t in texts)
    # chronological order preserved for prompt coherence
    starts = [s["startSeconds"] for s in slices["transcript"]]
    assert starts == sorted(starts)


def test_retrieve_no_overlap_returns_fewer_slices(envelope: dict):
    slices = tools.retrieve_video_context(envelope, "zjxqv wkmbp florbnax")
    assert slices["events"] == []
    assert slices["transcript"] == []


# --- quote verification (the anti-fabrication net) -------------------------


def test_quote_matches_transcript(envelope: dict):
    assert tools.quote_matches_transcript(
        "Binary language uses only two digits: zero and one.", envelope
    )
    # fuzzy: extra whitespace still matches
    assert tools.quote_matches_transcript(
        "binary  language uses only two digits: zero and one.", envelope
    )
    # fabricated quote must NOT pass
    assert not tools.quote_matches_transcript(
        "The teacher says quantum computers run on binary.", envelope
    )
    assert not tools.quote_matches_transcript("", envelope)


# --- validate_answer_draft (the Evaluate gate) ------------------------------


def _good_draft() -> dict:
    return {
        "text": "Binary is introduced at 02:53.",
        "found": True,
        "confidence": 0.96,
        "evidence": {
            "startSeconds": 173,
            "endSeconds": 210,
            "quote": "Binary language uses only two digits: zero and one.",
        },
    }


def test_validate_answer_draft_accepts_video_evidence(envelope: dict):
    draft = tools.validate_answer_draft(_good_draft(), envelope)
    assert draft["found"] is True
    assert draft["confidence"] == 0.96
    assert draft["evidence"]["startSeconds"] == 173.0


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

