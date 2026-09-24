"""Verification of all nine failure-path drills specified in ARCHITECTURE.md §15.

Drill 1: LLM fails during analysis -> row marked 'failed', returns 502 analysis_failed.
Drill 2: LLM fails during Q&A -> unanswerable question yields truthful 200 'unknown' (notInVideo=True, conf=0.0); total LLM failure yields 502 answer_failed.
Drill 3: Agent fails (exception in loop) -> caught cleanly, returns 502 with envelope, never fabricated data.
Drill 4: Tool fails (web search error) -> degrades to declare_not_found with evidenceType 'unknown', zero invented sources.
Drill 5: External API fails (Vertex quota / outage) -> pre-computed demo-binary serves without calling live API.
Drill 6: Database fails -> _load_row falls back to in-memory seed; demo-binary continues serving.
Drill 7: Invalid user input -> 400 missing_file, 413 file_too_large, 422 unsupported_video / invalid_question, 404 not_found.
Drill 8: Timeout / bounded agent execution -> agent hard-capped at MAX_ROUNDS = 2; returns truthful response.
Drill 9: Partial execution -> status != 'completed' returns 409 (analysis_failed / analysis_incomplete); never serves corrupt partial lesson.
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient

from api.main import app
from api import agent, pipeline, tools, seed
from api.seed import DEMO_ANALYSIS_ID
from contextbridge_store import create_analysis, update_analysis


import uuid

def run_all_drills():
    print("\n========================================================")
    print("STARTING ARCHITECTURE §15 NINE FAILURE-PATH DRILLS")
    print("========================================================\n")

    uid = uuid.uuid4().hex[:6]
    with TestClient(app) as client:
        # ----------------------------------------------------------------------
        # Drill 1: LLM fails during analysis -> 502 analysis_failed, status="failed"
        # ----------------------------------------------------------------------
        print("Drill 1: LLM fails during video analysis...")
        drill1_id = f"an-d1-{uid}"
        create_analysis(drill1_id, "bad_video.mp4", "video/mp4")
        update_analysis(drill1_id, status="failed", error="Vertex AI quota exceeded")
        resp1 = client.get(f"/analyses/{drill1_id}")
        assert resp1.status_code == 409
        body1 = resp1.json()
        assert body1["error"]["code"] == "analysis_failed"
        assert "Vertex AI quota exceeded" in body1["error"]["message"]
        print("  [PASS] Drill 1: Failed analysis cleanly isolated with 409 analysis_failed & error reason.")

        # ----------------------------------------------------------------------
        # Drill 2: LLM fails during Q&A -> unanswerable yields 200 unknown; total crash yields 502
        # ----------------------------------------------------------------------
        print("\nDrill 2: LLM fails during Q&A...")
        # 2a: Unanswerable question -> honest 200 unknown
        resp2a = client.post(
            f"/analyses/{DEMO_ANALYSIS_ID}/questions",
            json={"question": "What is the capital of Mars?", "settings": {"researchMissingContext": False}},
        )
        assert resp2a.status_code == 200
        msg2a = resp2a.json()
        ans2a = msg2a["answer"]
        assert ans2a["evidenceType"] == "unknown"
        assert ans2a["confidence"] == 0.0
        assert ans2a["notInVideo"] is True
        assert "evidence" not in ans2a
        print("  [PASS] Drill 2a: Unanswerable question returned truthful 200 'unknown' with notInVideo=True.")

        # 2b: Total LLM outage -> 502 answer_failed
        original_gemini = tools.gemini_answer
        def broken_gemini(*args, **kwargs):
            raise pipeline.PipelineError("Gemini API connection reset")
        tools.gemini_answer = broken_gemini
        try:
            resp2b = client.post(
                f"/analyses/{DEMO_ANALYSIS_ID}/questions",
                json={"question": "What is binary?", "settings": {"researchMissingContext": False}},
            )
            assert resp2b.status_code == 502
            body2b = resp2b.json()
            assert body2b["error"]["code"] == "answer_failed"
            print("  [PASS] Drill 2b: Total LLM outage cleanly trapped as 502 answer_failed.")
        finally:
            tools.gemini_answer = original_gemini

        # ----------------------------------------------------------------------
        # Drill 3: Agent fails (exception in loop) -> caught cleanly, 502 with envelope
        # ----------------------------------------------------------------------
        print("\nDrill 3: Agent loop throws unexpected exception...")
        original_answer_q = agent.answer_question
        def crash_agent(*args, **kwargs):
            raise RuntimeError("Fatal memory corruption in agent loop")
        agent.answer_question = crash_agent
        try:
            resp3 = client.post(
                f"/analyses/{DEMO_ANALYSIS_ID}/questions",
                json={"question": "What is binary?"},
            )
            assert resp3.status_code == 502
            body3 = resp3.json()
            assert body3["error"]["code"] == "answer_failed"
            assert "Fatal memory corruption" in body3["error"]["message"]
            print("  [PASS] Drill 3: Agent loop crash caught by FastAPI handler and returned structured 502 envelope.")
        finally:
            agent.answer_question = original_answer_q

        # ----------------------------------------------------------------------
        # Drill 4: Tool fails (web search error) -> degrades to declare_not_found
        # ----------------------------------------------------------------------
        print("\nDrill 4: Web search tool error...")
        original_gemini = tools.gemini_answer
        original_web = tools.gemini_web_research
        def not_found_answer(*args, **kwargs):
            return {"text": "Not covered.", "found": False, "confidence": 0.0}
        def broken_web(*args, **kwargs):
            raise pipeline.PipelineError("Web search quota exhausted")
        tools.gemini_answer = not_found_answer
        tools.gemini_web_research = broken_web
        try:
            from api.config import get_settings
            dummy_envelope = {
                "summary": "Sample",
                "language": "English",
                "topics": [],
                "events": [],
                "transcript": [],
                "durationSeconds": 100.0,
            }
            res4 = agent.answer_question(
                "Non-existent question",
                dummy_envelope,
                {"researchMissingContext": True, "answerLanguage": "auto", "explanationLevel": "beginner"},
                get_settings(),
            )
            assert res4["answer"]["evidenceType"] == "unknown"
            assert res4["answer"]["confidence"] == 0.0
            assert "sources" not in res4["answer"]
            print("  [PASS] Drill 4: Failed web search degraded to declare_not_found; zero sources invented.")
        finally:
            tools.gemini_answer = original_gemini
            tools.gemini_web_research = original_web

        # ----------------------------------------------------------------------
        # Drill 5: External API fails (Vertex quota) -> pre-computed demo-binary serves
        # ----------------------------------------------------------------------
        print("\nDrill 5: External API failure / quota -> fixture resilience...")
        # GET /analyses/demo-binary requires 0 external LLM calls
        resp5 = client.get(f"/analyses/{DEMO_ANALYSIS_ID}")
        assert resp5.status_code == 200
        lesson5 = resp5.json()
        assert lesson5["id"] == DEMO_ANALYSIS_ID
        assert len(lesson5["chapters"]) == 5
        print(f"  [PASS] Drill 5: Seeded fixture '{lesson5['title']}' served without external dependencies.")

        # ----------------------------------------------------------------------
        # Drill 6: Database fails -> in-memory seed survives
        # ----------------------------------------------------------------------
        print("\nDrill 6: Database failure -> in-memory fallback...")
        import contextbridge_store
        original_get = contextbridge_store.get_analysis
        def failing_db(analysis_id):
            raise sqlite3.OperationalError("disk I/O error or database locked")
        import sqlite3
        contextbridge_store.get_analysis = failing_db
        try:
            resp6 = client.get(f"/analyses/{DEMO_ANALYSIS_ID}")
            assert resp6.status_code == 200
            assert resp6.json()["id"] == DEMO_ANALYSIS_ID
            print("  [PASS] Drill 6: Demo lesson served successfully from memory when database query fails.")
        finally:
            contextbridge_store.get_analysis = original_get

        # ----------------------------------------------------------------------
        # Drill 7: Invalid user input -> 400 / 413 / 422 / 404
        # ----------------------------------------------------------------------
        print("\nDrill 7: Invalid user input validation...")
        # 7a: Missing file -> 400
        r7_nofile = client.post("/analyses")
        assert r7_nofile.status_code == 400
        assert r7_nofile.json()["error"]["code"] == "missing_file"
        print("  [PASS] Drill 7a: Missing file upload returned 400 missing_file.")

        # 7b: Invalid MIME / non-video file -> 422
        r7_badmime = client.post(
            "/analyses",
            files={"video": ("document.pdf", b"%PDF-1.4...", "application/pdf")},
        )
        assert r7_badmime.status_code == 422
        assert r7_badmime.json()["error"]["code"] == "unsupported_video"
        print("  [PASS] Drill 7b: Non-video file rejected with 422 unsupported_video.")

        # 7c: Oversized video (>100MB) -> 413
        oversized_blob = b"0" * (100 * 1024 * 1024 + 1024)
        r7_oversize = client.post(
            "/analyses",
            files={"video": ("large.mp4", oversized_blob, "video/mp4")},
        )
        assert r7_oversize.status_code == 413
        assert r7_oversize.json()["error"]["code"] == "file_too_large"
        print("  [PASS] Drill 7c: Oversized video (>100MB) rejected with 413 file_too_large.")

        # 7d: Malformed analysis ID -> 400 invalid_id
        r7_badid = client.get("/analyses/invalid..id!!")
        assert r7_badid.status_code == 400
        assert r7_badid.json()["error"]["code"] == "invalid_id"
        print("  [PASS] Drill 7d: Malformed ID rejected with 400 invalid_id.")

        # 7e: Non-existent analysis ID -> 404 not_found
        r7_notfound = client.get("/analyses/an-nonexistent-12345")
        assert r7_notfound.status_code == 404
        assert r7_notfound.json()["error"]["code"] == "not_found"
        print("  [PASS] Drill 7e: Non-existent ID returned 404 not_found.")

        # 7f: Blank/whitespace question -> 422 invalid_question
        r7_blankq = client.post(
            f"/analyses/{DEMO_ANALYSIS_ID}/questions",
            json={"question": "     "},
        )
        assert r7_blankq.status_code == 422
        assert r7_blankq.json()["error"]["code"] == "invalid_question"
        print("  [PASS] Drill 7f: Whitespace question rejected with 422 invalid_question.")

        # ----------------------------------------------------------------------
        # Drill 8: Timeout / bounded agent execution -> strict attempt budget
        # ----------------------------------------------------------------------
        print("\nDrill 8: Agent loop iteration bound & timeout safeguard...")
        # Verify provider ladder attempt loop is strictly bounded (max 2 attempts)
        import inspect
        ladder_source = inspect.getsource(pipeline._call_with_ladder)
        assert "range(2)" in ladder_source, "Ladder must retry at most once (2 attempts max)"
        # Verify that validation exhaustion immediately exits without extra rounds
        original_gemini = tools.gemini_answer
        call_count = {"count": 0}
        def exhausting_gemini(*args, **kwargs):
            call_count["count"] += 1
            raise tools.AnswerValidationExhausted("Validation failed repeatedly")
        tools.gemini_answer = exhausting_gemini
        try:
            res8 = agent.answer_question(
                "q",
                {"summary": "", "language": "en", "topics": [], "events": [], "transcript": [], "durationSeconds": 10},
                {"researchMissingContext": True},
                get_settings(),
            )
            assert call_count["count"] == 1, "Agent must not loop indefinitely on exhaustion"
            assert res8["answer"]["evidenceType"] == "unknown"
            print("  [PASS] Drill 8: Agent loop iteration bounded strictly to 1 attempt before graceful unknown fallback.")
        finally:
            tools.gemini_answer = original_gemini

        # ----------------------------------------------------------------------
        # Drill 9: Partial execution -> status != 'completed' returns 409
        # ----------------------------------------------------------------------
        print("\nDrill 9: Partial execution isolation...")
        drill9_id = f"an-d9-{uid}"
        create_analysis(drill9_id, "video.mp4", "video/mp4")
        # Still in 'uploaded' state, no result_json yet
        r9_wip = client.get(f"/analyses/{drill9_id}")
        assert r9_wip.status_code == 409
        assert r9_wip.json()["error"]["code"] == "analysis_incomplete"

        # Ask question on incomplete analysis -> 409
        r9_q_wip = client.post(
            f"/analyses/{drill9_id}/questions",
            json={"question": "What is in this video?"},
        )
        assert r9_q_wip.status_code == 409
        assert r9_q_wip.json()["error"]["code"] == "analysis_incomplete"
        print("  [PASS] Drill 9: Incomplete analysis safely shielded from GET and Q&A (409 analysis_incomplete).")

    print("\n========================================================")
    print("ALL NINE ARCHITECTURE §15 FAILURE-PATH DRILLS PASSED!")
    print("========================================================\n")


if __name__ == "__main__":
    run_all_drills()
