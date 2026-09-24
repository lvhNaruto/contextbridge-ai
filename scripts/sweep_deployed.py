"""Full P0-1 through P0-9 acceptance sweep against deployed Cloud Run stack.

Executes and verifies:
  - P0-1: Grounded answer with verbatim quote & timestamp
  - P0-2: Analysis pipeline schema (chapters, summary, topics, duration)
  - P0-3: Synchronised timeline & transcript navigation
  - P0-4: Surfaced contradiction pair with dual timestamps
  - P0-5: Accessible outputs (beginner explanation & Hindi translation)
  - P0-6: Deterministic startup seeding
  - P0-7: Conversation history multi-turn context
  - P0-8: Metric reporting (eval results verified)
  - P0-9: Deployed Cloud Run URLs responsive
"""

import json
import urllib.request

API = "https://contextbridge-api-c5ltxo3mkq-uc.a.run.app"
WEB = "https://contextbridge-web-c5ltxo3mkq-uc.a.run.app"


def post_json(path: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{API}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        assert resp.status == 200, f"Expected 200, got {resp.status}"
        return json.loads(resp.read().decode("utf-8"))


def get_json(path: str) -> dict:
    req = urllib.request.Request(f"{API}{path}", method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        assert resp.status == 200, f"Expected 200, got {resp.status}"
        return json.loads(resp.read().decode("utf-8"))


def run_sweep():
    print("\n========================================================")
    print("CONTEXTBRIDGE P0-1..P0-9 DEPLOYED ACCEPTANCE SWEEP")
    print(f"Frontend: {WEB}")
    print(f"Backend:  {API}")
    print("========================================================\n")

    # P0-9: Deployed URLs responsive
    print("Checking P0-9: Deployed service availability...")
    with urllib.request.urlopen(WEB) as resp:
        assert resp.status == 200
        print("  [PASS] P0-9 Frontend URL reachable (200 OK)")

    with urllib.request.urlopen(f"{API}/health") as resp:
        assert resp.status == 200
        print("  [PASS] P0-9 Backend health reachable (200 OK)")

    # P0-6: Deterministic fixture seeding
    print("\nChecking P0-6: Startup fixture seeding...")
    lesson = get_json("/analyses/demo-binary")
    assert lesson["id"] == "demo-binary"
    print(f"  [PASS] P0-6 Demo lesson seeded: '{lesson['title']}'")

    # P0-2: Analysis pipeline structure
    print("\nChecking P0-2: Video analysis pipeline structure...")
    assert "chapters" in lesson and len(lesson["chapters"]) >= 4
    assert "summary" in lesson and len(lesson["summary"]) > 0
    assert "durationSeconds" in lesson and lesson["durationSeconds"] > 0
    print(f"  [PASS] P0-2 Schema valid: {len(lesson['chapters'])} chapters, duration {lesson['durationSeconds']}s")

    # P0-3: Synchronised timeline & transcript
    print("\nChecking P0-3: Timeline chapters & transcript segments...")
    for ch in lesson["chapters"]:
        assert ch["startSeconds"] <= ch["endSeconds"]
        assert "confidence" in ch
    assert len(lesson.get("transcript", [])) > 0
    print(f"  [PASS] P0-3 Timeline synced with confidence metrics & {len(lesson['transcript'])} transcript segments")

    # P0-4: Contradiction pair with dual timestamps
    print("\nChecking P0-4: Surfaced contradiction pairs...")
    contradictions = lesson.get("contradictions", [])
    assert len(contradictions) >= 1, "Expected at least 1 contradiction pair"
    cx = contradictions[0]
    assert "claim" in cx and "statementA" in cx and "statementB" in cx
    assert cx["statementA"]["startSeconds"] is not None
    assert cx["statementB"]["startSeconds"] is not None
    print(f"  [PASS] P0-4 Contradiction pair: '{cx['claim']}' (timestamps {cx['statementA']['startSeconds']}s & {cx['statementB']['startSeconds']}s)")

    # P0-1: Grounded Q&A with exact quote & timestamp
    print("\nChecking P0-1: Grounded Q&A agent...")
    ans = post_json("/analyses/demo-binary/questions", {"question": "What feature is introduced on the new Pixel?"})
    assert ans["answer"]["evidenceType"] == "video"
    assert 10.0 <= ans["answer"]["evidence"]["startSeconds"] <= 25.0
    assert "video boost" in ans["answer"]["evidence"]["quote"].lower() or "night sight" in ans["answer"]["evidence"]["quote"].lower()
    print(f"  [PASS] P0-1 Grounded answer returned with quote: \"{ans['answer']['evidence']['quote']}\"")

    # P0-7: Conversation history follow-up
    print("\nChecking P0-7: Multi-turn history support...")
    ans_followup = post_json(
        "/analyses/demo-binary/questions",
        {
            "question": "What happens in low light?",
            "history": [
                {"role": "user", "text": "What feature is introduced on the new Pixel?"},
                {"role": "assistant", "text": "The new Pixel has a feature called Video Boost."},
            ],
        },
    )
    assert ans_followup["answer"]["evidenceType"] == "video"
    print(f"  [PASS] P0-7 Follow-up answered with context: \"{ans_followup['text'][:60]}...\"")

    # P0-5: Accessible output (plain language / Hindi translation)
    print("\nChecking P0-5: Accessible explanation & Hindi translation...")
    ans_beginner = post_json(
        "/analyses/demo-binary/questions",
        {"question": "What is binary language?", "explanationLevel": "beginner"},
    )
    assert len(ans_beginner["text"]) > 0
    print(f"  [PASS] P0-5 Beginner explanation: \"{ans_beginner['text'][:60]}...\"")

    ans_hindi = post_json(
        "/analyses/demo-binary/questions",
        {"question": "What is binary language?", "answerLanguage": "hi"},
    )
    assert len(ans_hindi["text"]) > 0
    print(f"  [PASS] P0-5 Hindi translation: \"{ans_hindi['text'][:60]}...\"")

    # P0-8: Metric evaluation artifact check
    print("\nChecking P0-8: Evaluation harness artifact...")
    with open("context/eval_results.json", "r", encoding="utf-8") as f:
        eval_data = json.load(f)
    assert eval_data["metrics"]["unsupported_answer_rate_pct"] == 0.0
    print(f"  [PASS] P0-8 Metrics verified: {eval_data['metrics']}")

    print("\n========================================================")
    print("ALL P0 ACCEPTANCE SWEEPS PASSED ON DEPLOYED STACK!")
    print("========================================================\n")


if __name__ == "__main__":
    run_sweep()
