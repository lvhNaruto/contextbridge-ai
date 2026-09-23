"""Phase 1 contract tests — API.md §2/§3 shapes against a seeded demo fixture.

Zero LLM calls: seeding is fixture-only, and the upload tests stop at input
validation (a valid file would reach Gemini, which belongs to the live smoke).
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.seed import DEMO_ANALYSIS_ID
from contextbridge_store import create_analysis, update_analysis


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:  # lifespan runs the fixture seed
        yield test_client


def _minimal_envelope() -> dict:
    return {
        "summary": "A test lesson.",
        "language": "English",
        "topics": ["Testing"],
        "events": [],
        "transcript": [],
        "durationSeconds": 10,
    }


# --- ops -----------------------------------------------------------------


def test_healthz_reports_seeded_demo(client: TestClient):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["demoSeeded"] is True
    assert body["model"]


# --- the seeded demo lesson (P0-6 + P0-2c + P0-4a) ------------------------


def test_demo_lesson_matches_contract(client: TestClient):
    resp = client.get(f"/analyses/{DEMO_ANALYSIS_ID}")
    assert resp.status_code == 200
    lesson = resp.json()
    for key in (
        "id", "title", "videoUrl", "durationSeconds", "createdAt",
        "language", "summary", "topics", "chapters", "transcript",
    ):
        assert key in lesson, key
    assert lesson["id"] == DEMO_ANALYSIS_ID
    assert lesson["title"] == "Understanding binary & computer language"
    assert lesson["videoUrl"].endswith(f"/analyses/{DEMO_ANALYSIS_ID}/video")
    assert lesson["durationSeconds"] == 888
    assert lesson["createdAt"].endswith("Z")


def test_demo_lesson_chapters_carry_confidence(client: TestClient):
    lesson = client.get(f"/analyses/{DEMO_ANALYSIS_ID}").json()
    assert len(lesson["chapters"]) == 5
    for chapter in lesson["chapters"]:
        assert 0 <= chapter["confidence"] <= 1  # ✳ A4 passthrough
        assert 0 <= chapter["startSeconds"] <= chapter["endSeconds"] <= 888


def test_demo_lesson_has_genuine_contradiction_pair(client: TestClient):
    lesson = client.get(f"/analyses/{DEMO_ANALYSIS_ID}").json()
    pairs = lesson.get("contradictions")
    assert pairs, "demo-binary must ship one genuine pair (D-02)"
    pair = pairs[0]
    transcript_text = " ".join(seg["text"] for seg in lesson["transcript"])
    for key in ("statementA", "statementB"):
        stmt = pair[key]
        # API §2 invariant 5: real timestamps in range, quotes in transcript
        assert 0 <= stmt["startSeconds"] <= stmt["endSeconds"] <= 888
        assert stmt["quote"] in transcript_text
    assert pair["statementA"]["startSeconds"] < pair["statementB"]["startSeconds"]


def test_chapters_reserved_projection(client: TestClient):
    lesson = client.get(f"/analyses/{DEMO_ANALYSIS_ID}").json()
    resp = client.get(f"/analyses/{DEMO_ANALYSIS_ID}/chapters")
    assert resp.status_code == 200
    assert resp.json() == lesson["chapters"]


# --- video playback (P0-2a Range) -----------------------------------------


def test_demo_video_is_playable(client: TestClient):
    resp = client.get(f"/analyses/{DEMO_ANALYSIS_ID}/video", follow_redirects=False)
    # Local fixture file → 200/206; otherwise a 302 to the public sample (D-13)
    assert resp.status_code in (200, 206, 302)
    if resp.status_code == 302:
        assert resp.headers["location"].startswith("https://")


def test_video_range_requests(client: TestClient, tmp_path):
    payload = bytes(range(256)) * 4  # 1024 deterministic bytes
    video_file = tmp_path / "clip.mp4"
    video_file.write_bytes(payload)
    create_analysis("an-rangetest", "clip.mp4", "video/mp4")
    update_analysis(
        "an-rangetest",
        status="completed",
        result=_minimal_envelope(),
        storage_uri=str(video_file),
    )

    full = client.get("/analyses/an-rangetest/video")
    assert full.status_code == 200
    assert full.content == payload
    assert full.headers["accept-ranges"] == "bytes"

    partial = client.get(
        "/analyses/an-rangetest/video", headers={"Range": "bytes=100-199"}
    )
    assert partial.status_code == 206
    assert partial.headers["content-range"] == "bytes 100-199/1024"
    assert partial.content == payload[100:200]

    unsatisfiable = client.get(
        "/analyses/an-rangetest/video", headers={"Range": "bytes=5000-6000"}
    )
    assert unsatisfiable.status_code == 416
    assert unsatisfiable.json()["error"]["code"] == "invalid_range"


# --- error envelope & validation ------------------------------------------


def test_unknown_lesson_404_envelope(client: TestClient):
    resp = client.get("/analyses/an-does-not-exist")
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "not_found"


def test_malformed_id_rejected(client: TestClient):
    resp = client.get("/analyses/bad!!id")
    assert resp.status_code == 400
    assert resp.json()["error"]["code"] == "invalid_id"


def test_failed_analysis_returns_409(client: TestClient):
    create_analysis("an-failedone", "broken.mp4", "video/mp4")
    update_analysis("an-failedone", status="failed", error="boom")
    resp = client.get("/analyses/an-failedone")
    assert resp.status_code == 409
    body = resp.json()
    assert body["error"]["code"] == "analysis_failed"
    assert "boom" in body["error"]["message"]


def test_upload_requires_a_file(client: TestClient):
    resp = client.post("/analyses")
    assert resp.status_code == 400
    assert resp.json()["error"]["code"] == "missing_file"


def test_upload_rejects_non_video(client: TestClient):
    resp = client.post(
        "/analyses", files={"video": ("notes.txt", b"hello world", "text/plain")}
    )
    assert resp.status_code == 422
    assert resp.json()["error"]["code"] == "unsupported_video"


def test_upload_rejects_spoofed_extension(client: TestClient):
    resp = client.post(
        "/analyses", files={"video": ("fake.mp4", b"not a real video", "video/mp4")}
    )
    assert resp.status_code == 422
    assert resp.json()["error"]["code"] == "unsupported_video"


# --- timestamp unit repair (live-observed model slip) ----------------------


def test_mp4_duration_parse_synthetic():
    import struct

    from api.pipeline import _mp4_duration_seconds

    body = bytes([0, 0, 0, 0]) + b"\x00" * 8 + struct.pack(">II", 1000, 57000)
    blob = b"\x00" * 16 + b"mvhd" + body
    assert _mp4_duration_seconds(blob) == 57.0
    assert _mp4_duration_seconds(b"no atoms here") is None


def test_rescale_repairs_percent_unit_slip():
    from api.pipeline import _rescale_timestamps

    envelope = {
        "summary": "s",
        "language": "en",
        "topics": [],
        "durationSeconds": 0.563,
        "events": [
            {
                "id": "ev-1",
                "startSeconds": 0.05,
                "endSeconds": 0.12,
                "title": "t",
                "description": "d",
                "confidence": 0.9,
                "evidence": [{"startSeconds": 0.06, "endSeconds": 0.1, "quote": "q"}],
            }
        ],
        "transcript": [{"startSeconds": 0.05, "endSeconds": 0.56, "text": "hi"}],
    }
    out = _rescale_timestamps(envelope, 57.0)
    assert out["durationSeconds"] == 57.0
    assert out["events"][0]["startSeconds"] == 5.0
    assert out["events"][0]["evidence"][0]["endSeconds"] == 10.0
    assert out["transcript"][0]["endSeconds"] == 56.0


def test_rescale_noop_when_model_is_accurate():
    from api.pipeline import _rescale_timestamps

    envelope = {
        "summary": "s",
        "language": "en",
        "topics": [],
        "durationSeconds": 56.0,
        "events": [],
        "transcript": [{"startSeconds": 5.0, "endSeconds": 12.0, "text": "hi"}],
    }
    out = _rescale_timestamps(envelope, 57.0)
    assert out["durationSeconds"] == 57.0  # container truth always wins
    assert out["transcript"][0]["endSeconds"] == 12.0  # timestamps untouched


# --- config ----------------------------------------------------------------


def test_get_settings_is_cached():
    from api.config import get_settings

    assert get_settings() is get_settings()  # single instance, env parsed once
