"""REG — Regression guard per context/TODO.md and context/BUILD_PLAN.md.

Verifies:
1. `_mock_answer` is absent from all code under api/
2. Schema MediaAnalysis.from_dict rejects malformed output
3. Mock mode files (mock-data.ts, demo-answers.ts) are intact and structurally valid
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from contextbridge_schema import MediaAnalysis, EvidenceReference, MediaEvent


def test_no_mock_answer_in_api_code():
    api_dir = Path(__file__).resolve().parent.parent / "api"
    for py_file in api_dir.glob("*.py"):
        content = py_file.read_text(encoding="utf-8")
        assert "_mock_answer" not in content, f"_mock_answer found in {py_file.name}"


@pytest.mark.parametrize(
    "bad_payload, expected_err",
    [
        ("not a dict", "Gemini response must be a JSON object"),
        ({"summary": "ok", "events": "not a list"}, "events must be an array"),
        ({"summary": "ok", "events": [], "transcript": "not a list"}, "transcript must be an array"),
        ({}, "summary must be a non-empty string"),
        ({"summary": "ok"}, "language must be a non-empty string"),
        (
            {
                "summary": "ok",
                "language": "en",
                "events": [{"id": "e1", "startSeconds": 10, "endSeconds": 5, "title": "t", "description": "d", "confidence": 0.9}],
                "transcript": [],
            },
            "timestamps are invalid",
        ),
        (
            {
                "summary": "ok",
                "language": "en",
                "events": [{"id": "e1", "startSeconds": 1, "endSeconds": 5, "title": "t", "description": "d", "confidence": 1.5}],
                "transcript": [],
            },
            "confidence must be between 0 and 1",
        ),
        (
            {
                "summary": "ok",
                "language": "en",
                "events": [],
                "transcript": [{"startSeconds": 5, "endSeconds": 2, "text": "hello"}],
            },
            "timestamps are invalid",
        ),
        (
            {
                "summary": "ok",
                "language": "en",
                "events": [],
                "transcript": [{"startSeconds": 1, "endSeconds": 2, "text": "   "}],
            },
            "text must be a non-empty string",
        ),
    ],
    ids=[
        "non-dict",
        "events-not-array",
        "transcript-not-array",
        "missing-summary",
        "missing-language",
        "event-start-after-end",
        "confidence-over-1",
        "transcript-start-after-end",
        "transcript-empty-text",
    ],
)
def test_schema_rejects_malformed_output(bad_payload, expected_err):
    with pytest.raises(ValueError, match=expected_err):
        MediaAnalysis.from_dict(bad_payload)


def test_schema_accepts_valid_payload():
    payload = {
        "summary": "Valid video summary.",
        "language": "English",
        "topics": ["tech", "coding"],
        "durationSeconds": 120.0,
        "events": [
            {
                "id": "ev-1",
                "startSeconds": 0.0,
                "endSeconds": 30.0,
                "title": "Introduction",
                "description": "Intro to topic",
                "confidence": 0.95,
                "evidence": [{"startSeconds": 5.0, "endSeconds": 10.0, "quote": "welcome"}],
            }
        ],
        "transcript": [{"startSeconds": 0.0, "endSeconds": 30.0, "text": "welcome to the lesson"}],
    }
    analysis = MediaAnalysis.from_dict(payload)
    assert analysis.summary == "Valid video summary."
    assert analysis.language == "English"
    assert len(analysis.events) == 1
    assert len(analysis.transcript) == 1


def test_mock_mode_fixtures_exist_and_consistent():
    web_dir = Path(__file__).resolve().parent.parent / "web"
    mock_data = web_dir / "lib" / "mock-data.ts"
    demo_answers = web_dir / "lib" / "demo-answers.ts"
    api_ts = web_dir / "lib" / "api.ts"

    assert mock_data.exists(), "mock-data.ts missing"
    assert demo_answers.exists(), "demo-answers.ts missing"
    assert api_ts.exists(), "api.ts missing"

    api_content = api_ts.read_text(encoding="utf-8")
    assert "USE_MOCK = !API_BASE" in api_content, "Mock fallback toggle missing in api.ts"
    assert "resolveDemoAnswer" in api_content, "resolveDemoAnswer missing in api.ts"
    assert "DEMO_LESSON" in api_content, "DEMO_LESSON missing in api.ts"
