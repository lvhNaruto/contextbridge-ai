"""P0-1b agent tests — branch selection, API §2 invariants, endpoint wiring.

Zero LLM calls: gemini_answer / gemini_web_research are stubbed at the
api.tools module boundary (the agent resolves them at call time); retrieval
stays real against small envelopes.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api import agent, pipeline, tools
from api.main import app
from api.seed import DEMO_ANALYSIS_ID

QA_ON = {
    "answerLanguage": "auto",
    "explanationLevel": "beginner",
    "researchMissingContext": True,
}
QA_OFF = {**QA_ON, "researchMissingContext": False}

VIDEO_DRAFT = {
    "text": "Binary is introduced at 02:53.",
    "found": True,
    "confidence": 0.96,
    "evidence": {
        "startSeconds": 173.0,
        "endSeconds": 376.0,
        "quote": "Binary language uses only two digits: zero and one.",
    },
}
NOT_FOUND_DRAFT = {"text": "Not covered.", "found": False, "confidence": 0.0}
WEB_DRAFT = {
    "text": "From the web: ...",
    "sources": [
        {
            "title": "Binary number - Wikipedia",
            "domain": "wikipedia.org",
            "url": "https://en.wikipedia.org/wiki/Binary_number",
            "description": "The base-2 system.",
        }
    ],
}


@pytest.fixture
def envelope() -> dict:
    return {
        "summary": "Binary basics.",
        "language": "English",
        "topics": ["binary"],
        "events": [],
        "transcript": [
            {
                "startSeconds": 173.0,
                "endSeconds": 376.0,
                "text": "Binary language uses only two digits: zero and one.",
            }
        ],
        "durationSeconds": 888.0,
    }


def _stub(monkeypatch, *, answer=None, answer_error=None, web=None, web_error=None):
    """Replace the two LLM tools; return a call counter."""
    calls = {"answer": 0, "web": 0, "last_history": None}

    def fake_answer(*args, **kwargs):
        calls["answer"] += 1
        if "history" in kwargs:
            calls["last_history"] = kwargs["history"]
        elif len(args) >= 6:
            calls["last_history"] = args[5]
        if answer_error is not None:
            raise answer_error
        return dict(answer)

    def fake_web(*args, **kwargs):
        calls["web"] += 1
        if web_error is not None:
            raise web_error
        return dict(web)

    monkeypatch.setattr(tools, "gemini_answer", fake_answer)
    monkeypatch.setattr(tools, "gemini_web_research", fake_web)
    return calls


# --- branch selection (ARCHITECTURE §6.3) ------------------------------------


def test_found_answer_returns_video_chat_message(monkeypatch, envelope):
    _stub(monkeypatch, answer=VIDEO_DRAFT)
    msg = agent.answer_question("What is binary?", envelope, QA_ON, None)
    assert msg["id"].startswith("msg-")
    assert msg["role"] == "assistant"
    assert msg["text"] == VIDEO_DRAFT["text"]
    assert msg["isVoice"] is False
    assert isinstance(msg["createdAt"], int)
    assert msg["createdAt"] > 1_600_000_000_000  # epoch ms NUMBER (API §2)
    answer = msg["answer"]
    assert answer["evidenceType"] == "video"
    assert answer["evidence"]["startSeconds"] == 173.0
    assert answer["confidence"] == 0.96
    assert "sources" not in answer and "notInVideo" not in answer


def test_not_found_research_off_declares_unknown(monkeypatch, envelope):
    calls = _stub(monkeypatch, answer=NOT_FOUND_DRAFT)
    msg = agent.answer_question("q", envelope, QA_OFF, None)
    answer = msg["answer"]
    assert answer["evidenceType"] == "unknown"
    assert answer["confidence"] == 0.0
    assert answer["notInVideo"] is True
    assert "evidence" not in answer and "sources" not in answer
    assert calls["web"] == 0  # research off → Tool 3 never runs (§6.3 Select)


def test_not_found_research_on_answers_from_web_only(monkeypatch, envelope):
    calls = _stub(monkeypatch, answer=NOT_FOUND_DRAFT, web=WEB_DRAFT)
    msg = agent.answer_question("q", envelope, QA_ON, None)
    answer = msg["answer"]
    assert answer["evidenceType"] == "web"
    assert answer["notInVideo"] is True
    assert answer["sources"][0]["url"].startswith("https://")
    assert answer["confidence"] == 0.72  # locked-mock parity (demo-answers.ts)
    assert "evidence" not in answer  # API §2 inv. 2 — video and web never blend
    assert calls["web"] == 1


def test_web_failure_falls_back_to_not_found(monkeypatch, envelope):
    _stub(
        monkeypatch,
        answer=NOT_FOUND_DRAFT,
        web_error=pipeline.PipelineError("search down"),
    )
    msg = agent.answer_question("q", envelope, QA_ON, None)
    assert msg["answer"]["evidenceType"] == "unknown"  # §6.5 — never fabricated


def test_validation_exhaustion_declares_not_found(monkeypatch, envelope):
    calls = _stub(
        monkeypatch, answer_error=tools.AnswerValidationExhausted("bad evidence")
    )
    msg = agent.answer_question("q", envelope, QA_ON, None)
    answer = msg["answer"]
    assert answer["evidenceType"] == "unknown"
    assert answer["confidence"] == 0.0
    assert calls["web"] == 0  # §6.4 round budget spent on the one retry


def test_infra_pipeline_error_propagates_for_honest_502(monkeypatch, envelope):
    _stub(
        monkeypatch,
        answer_error=pipeline.PipelineError("No Gemini credentials configured."),
    )
    with pytest.raises(pipeline.PipelineError) as excinfo:
        agent.answer_question("q", envelope, QA_ON, None)
    assert not isinstance(excinfo.value, tools.AnswerValidationExhausted)


def test_voice_flag_is_echoed(monkeypatch, envelope):
    _stub(monkeypatch, answer=VIDEO_DRAFT)
    msg = agent.answer_question("q", envelope, QA_ON, None, is_voice=True)
    assert msg["isVoice"] is True


# --- POST /analyses/{id}/questions (API.md §3.4) ------------------------------


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:  # lifespan seeds the demo lesson
        yield test_client


def test_post_question_unknown_lesson_is_404(client):
    resp = client.post(
        "/analyses/an-notreal/questions",
        json={"question": "hi?", "settings": QA_ON},
    )
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "not_found"


def test_post_question_empty_string_is_422(client):
    resp = client.post(
        f"/analyses/{DEMO_ANALYSIS_ID}/questions",
        json={"question": "", "settings": QA_ON},
    )
    assert resp.status_code == 422


def test_post_question_whitespace_is_422(client):
    resp = client.post(
        f"/analyses/{DEMO_ANALYSIS_ID}/questions",
        json={"question": "   ", "settings": QA_ON},
    )
    assert resp.status_code == 422
    assert resp.json()["error"]["code"] == "invalid_question"


def test_post_question_bad_settings_is_422(client):
    resp = client.post(
        f"/analyses/{DEMO_ANALYSIS_ID}/questions",
        json={"question": "What is binary?", "settings": {"answerLanguage": "fr"}},
    )
    assert resp.status_code == 422


def test_post_question_incomplete_analysis_is_409(client):
    from contextbridge_store import create_analysis

    create_analysis("an-questwip", "x.mp4", "video/mp4")
    resp = client.post(
        "/analyses/an-questwip/questions",
        json={"question": "What is binary?", "settings": QA_ON},
    )
    assert resp.status_code == 409
    assert resp.json()["error"]["code"] == "analysis_incomplete"


def test_post_question_happy_path_returns_chat_message(client, monkeypatch):
    _stub(monkeypatch, answer=VIDEO_DRAFT)
    resp = client.post(
        f"/analyses/{DEMO_ANALYSIS_ID}/questions",
        json={"question": "What is binary?", "settings": QA_ON, "isVoice": True},
    )
    assert resp.status_code == 200
    msg = resp.json()
    assert msg["role"] == "assistant"
    assert msg["isVoice"] is True
    assert isinstance(msg["createdAt"], int)
    answer = msg["answer"]
    assert answer["evidenceType"] == "video"
    assert answer["evidence"]["quote"]  # jump-button invariant (inv. 1)


def test_post_question_502_on_total_llm_failure(client, monkeypatch):
    _stub(
        monkeypatch,
        answer_error=pipeline.PipelineError("No Gemini credentials configured."),
    )
    resp = client.post(
        f"/analyses/{DEMO_ANALYSIS_ID}/questions",
        json={"question": "What is binary?", "settings": QA_ON},
    )
    assert resp.status_code == 502
    assert resp.json()["error"]["code"] == "answer_failed"


# --- P0-7: history & follow-up context ----------------------------------------


def test_agent_passes_history_to_gemini_answer(monkeypatch, envelope):
    calls = _stub(monkeypatch, answer=VIDEO_DRAFT)
    history = [
        {"role": "user", "text": "What is binary?"},
        {"role": "assistant", "text": "Binary uses only two digits."},
    ]
    msg = agent.answer_question(
        "Tell me more about that", envelope, QA_ON, None, history=history
    )
    assert calls["answer"] == 1
    assert calls["last_history"] == history
    assert msg["answer"]["evidenceType"] == "video"


def test_post_question_with_valid_history(client, monkeypatch):
    calls = _stub(monkeypatch, answer=VIDEO_DRAFT)
    resp = client.post(
        f"/analyses/{DEMO_ANALYSIS_ID}/questions",
        json={
            "question": "Tell me more about that",
            "settings": QA_ON,
            "history": [
                {"role": "user", "text": "What is binary?"},
                {"role": "assistant", "text": "Binary uses two digits."},
            ],
        },
    )
    assert resp.status_code == 200
    assert calls["answer"] == 1
    assert len(calls["last_history"]) == 2
    assert calls["last_history"][0]["text"] == "What is binary?"


def test_post_question_history_clamped_to_last_six(client, monkeypatch):
    calls = _stub(monkeypatch, answer=VIDEO_DRAFT)
    long_history = [{"role": "user", "text": f"turn {i}"} for i in range(10)]
    resp = client.post(
        f"/analyses/{DEMO_ANALYSIS_ID}/questions",
        json={
            "question": "Follow-up",
            "settings": QA_ON,
            "history": long_history,
        },
    )
    assert resp.status_code == 200
    assert len(calls["last_history"]) == 6
    assert calls["last_history"][-1]["text"] == "turn 9"


def test_post_question_invalid_history_role_is_422(client):
    resp = client.post(
        f"/analyses/{DEMO_ANALYSIS_ID}/questions",
        json={
            "question": "hi",
            "settings": QA_ON,
            "history": [{"role": "system", "text": "invalid role"}],
        },
    )
    assert resp.status_code == 422


def test_post_question_empty_history_text_is_422(client):
    resp = client.post(
        f"/analyses/{DEMO_ANALYSIS_ID}/questions",
        json={
            "question": "hi",
            "settings": QA_ON,
            "history": [{"role": "user", "text": ""}],
        },
    )
    assert resp.status_code == 422


# --- reserved alias: POST /analyses/{id}/voice-question ----------------------


def test_post_voice_question_happy_path(client, monkeypatch):
    _stub(monkeypatch, answer=VIDEO_DRAFT)
    resp = client.post(
        f"/analyses/{DEMO_ANALYSIS_ID}/voice-question",
        data={"transcript": "What is binary?"},
    )
    assert resp.status_code == 200
    msg = resp.json()
    assert msg["isVoice"] is True
    assert msg["answer"]["evidenceType"] == "video"


def test_post_voice_question_empty_transcript_is_422(client):
    resp = client.post(
        f"/analyses/{DEMO_ANALYSIS_ID}/voice-question",
        data={"transcript": "   "},
    )
    assert resp.status_code == 422
    assert resp.json()["error"]["code"] == "invalid_question"


def test_post_voice_question_with_audio_transcription(client, monkeypatch):
    _stub(monkeypatch, answer=VIDEO_DRAFT)
    monkeypatch.setattr(
        "api.pipeline.transcribe_audio",
        lambda audio_bytes, mime, settings, language_hint=None: "What is binary?",
    )
    resp = client.post(
        f"/analyses/{DEMO_ANALYSIS_ID}/voice-question",
        data={"transcript": ""},
        files={"audio": ("question.webm", b"FAKEAUDIOBYTES" * 10, "audio/webm")},
    )
    assert resp.status_code == 200
    msg = resp.json()
    assert msg["isVoice"] is True
    assert msg["transcribedQuestion"] == "What is binary?"
    assert msg["answer"]["evidenceType"] == "video"


def test_post_transcribe_endpoint(client, monkeypatch):
    monkeypatch.setattr(
        "api.pipeline.transcribe_audio",
        lambda audio_bytes, mime, settings, language_hint=None: "Transcribed speech text",
    )
    resp = client.post(
        "/transcribe",
        data={"language": "en"},
        files={"audio": ("speech.webm", b"AUDIOBYTES12345" * 10, "audio/webm")},
    )
    assert resp.status_code == 200
    assert resp.json()["text"] == "Transcribed speech text"


def test_api_package_contains_no_mock_answer_path():
    api_dir = Path(__file__).resolve().parent.parent / "api"
    sources = {p.name: p.read_text(encoding="utf-8") for p in api_dir.glob("*.py")}
    assert sources, "api/ package not found"
    for name, text in sources.items():
        assert "_mock_answer" not in text, f"mock path still present in {name}"


def test_derive_suggestions_produces_anchored_questions():
    envelope = {
        "topics": ["Video Boost", "Night Sight", "Low light videography"],
        "events": [{"title": "Saeka in Tokyo"}, {"title": "Exploring Sancha at Night"}],
        "contradictions": [{"claim": "natural darkness vs computational enhancement"}],
    }
    s = agent.derive_suggestions(envelope, "Tell me about Tokyo")
    assert len(s) >= 2
    assert any("contradiction" in q.lower() for q in s)


def test_ambiguous_question_triggers_clarification(client):
    resp = client.post(
        f"/analyses/{DEMO_ANALYSIS_ID}/questions",
        json={"question": "what"},
    )
    assert resp.status_code == 200
    msg = resp.json()
    assert msg["answer"]["evidenceType"] == "unknown"
    assert "specify" in msg["text"].lower()
    assert len(msg.get("suggestions", [])) > 0

