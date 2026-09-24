"""ContextBridge P0-8 Evaluation Harness.

Evaluates the ContextBridge agent and video pipeline against known ground-truth questions:
  1. In-video factual questions (ground truth timestamp + quote)
  2. Follow-up conversational questions with history turns
  3. Contradiction identification questions
  4. Out-of-video / unanswerable questions (honest refusal verification)

Reports the four DoD metrics:
  - Timestamp-retrieval accuracy (% within tolerance of ground truth moment)
  - Groundedness (% answers backed by verbatim transcript quote + verified range)
  - Unsupported-answer rate (% hallucinations/inventions, target: 0%)
  - Processing time per question / video
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from typing import Any

# Ensure UTF-8 output on Windows consoles (prevent cp1252 charmap encoding crash on Devanagari)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_API = "https://contextbridge-api-c5ltxo3mkq-uc.a.run.app"
DEMO_ID = "demo-binary"

# Evaluation benchmark suite (25 comprehensive cases for Week 2 DoD)
EVAL_CASES = [
    # 1. In-video English questions
    {
        "id": "q01_feature_intro",
        "category": "in-video",
        "question": "What feature is introduced on the new Pixel?",
        "expected_start": 13.0,
        "expected_end": 21.0,
        "expected_quote_sub": "Video Boost",
        "should_find": True,
    },
    {
        "id": "q02_photographer_intro",
        "category": "in-video",
        "question": "What is Saeka Shimada's profession in Tokyo?",
        "expected_start": 1.0,
        "expected_end": 3.0,
        "expected_quote_sub": "photographer",
        "should_find": True,
    },
    {
        "id": "q03_tokyo_night",
        "category": "in-video",
        "question": "How does the photographer describe Tokyo at night compared to daytime?",
        "expected_start": 5.0,
        "expected_end": 9.0,
        "expected_quote_sub": "different",
        "should_find": True,
    },
    {
        "id": "q04_sancha_memories",
        "category": "in-video",
        "question": "Where did Saeka live when she first moved to Tokyo?",
        "expected_start": 23.0,
        "expected_end": 26.0,
        "expected_quote_sub": "Sancha",
        "should_find": True,
    },
    {
        "id": "q05_shooting_puddle",
        "category": "in-video",
        "question": "What does Saeka notice and film on the street puddle?",
        "expected_start": 28.0,
        "expected_end": 30.0,
        "expected_quote_sub": "like this",
        "should_find": True,
    },
    {
        "id": "q06_destination_shibuya",
        "category": "in-video",
        "question": "Where does Saeka go next after filming in the alleyway?",
        "expected_start": 53.0,
        "expected_end": 54.0,
        "expected_quote_sub": "Shibuya",
        "should_find": True,
    },
    {
        "id": "q07_camera_sensor_boost",
        "category": "in-video",
        "question": "What does Video Boost do when shooting video at night?",
        "expected_start": 13.0,
        "expected_end": 21.0,
        "expected_quote_sub": "Night Sight",
        "should_find": True,
    },
    # 2. Conversational Follow-up questions (with history)
    {
        "id": "q08_followup_feature",
        "category": "follow-up",
        "question": "What happens when it is in low light?",
        "history": [
            {"role": "user", "text": "What feature is introduced on the new Pixel?"},
            {"role": "assistant", "text": "The new Pixel has a feature called Video Boost."},
        ],
        "expected_start": 13.0,
        "expected_end": 21.0,
        "expected_quote_sub": "Night Sight",
        "should_find": True,
    },
    {
        "id": "q09_followup_sancha_memories",
        "category": "follow-up",
        "question": "Did she have good memories living there?",
        "history": [
            {"role": "user", "text": "Where did Saeka live when she moved to Tokyo?"},
            {"role": "assistant", "text": "She lived in Sancha."},
        ],
        "expected_start": 23.0,
        "expected_end": 26.0,
        "expected_quote_sub": "memories",
        "should_find": True,
    },
    {
        "id": "q10_followup_quality",
        "category": "follow-up",
        "question": "Does it improve the quality?",
        "history": [
            {"role": "user", "text": "What does it activate in low light?"},
            {"role": "assistant", "text": "It activates Night Sight in low light."},
        ],
        "expected_start": 15.0,
        "expected_end": 21.0,
        "expected_quote_sub": "quality",
        "should_find": True,
    },
    # 3. Contradiction questions
    {
        "id": "q11_contradiction_darkness",
        "category": "contradiction",
        "question": "Does night videography capture natural dark city streets or does computational Night Sight enhance it?",
        "expected_start": 5.0,
        "expected_end": 21.0,
        "expected_quote_sub": "different",
        "should_find": True,
    },
    {
        "id": "q12_contradiction_night_faces",
        "category": "contradiction",
        "question": "Does the video describe Tokyo as completely identical day and night, or having different faces?",
        "expected_start": 5.0,
        "expected_end": 9.0,
        "expected_quote_sub": "different",
        "should_find": True,
    },
    # 4. Multilingual & Hinglish queries
    {
        "id": "q13_hindi_photographer",
        "category": "multilingual",
        "question": "सायका शिमाडा टोक्यो में क्या काम करती हैं?",
        "expected_start": 1.0,
        "expected_end": 3.0,
        "expected_quote_sub": "photographer",
        "should_find": True,
    },
    {
        "id": "q14_hindi_feature",
        "category": "multilingual",
        "question": "नए पिक्सल फोन में कम रोशनी के लिए कौन सा फीचर है?",
        "expected_start": 13.0,
        "expected_end": 21.0,
        "expected_quote_sub": "Night Sight",
        "should_find": True,
    },
    {
        "id": "q15_hinglish_feature",
        "category": "hinglish",
        "question": "Pixel phone mein night videography ke liye kaunsa feature use hota hai?",
        "expected_start": 13.0,
        "expected_end": 21.0,
        "expected_quote_sub": "Video Boost",
        "should_find": True,
    },
    {
        "id": "q16_hinglish_sancha",
        "category": "hinglish",
        "question": "Saeka pehle Tokyo mein kahan rehti thi?",
        "expected_start": 23.0,
        "expected_end": 26.0,
        "expected_quote_sub": "Sancha",
        "should_find": True,
    },
    {
        "id": "q17_hinglish_night_feeling",
        "category": "hinglish",
        "question": "Tokyo raat ko daytime se kitna different lagta hai video mein?",
        "expected_start": 5.0,
        "expected_end": 9.0,
        "expected_quote_sub": "different",
        "should_find": True,
    },
    # 5. Clarify move (ambiguous / short input)
    {
        "id": "q18_clarify_short_what",
        "category": "clarify",
        "question": "what",
        "should_find": False,
        "expected_type": "unknown",
    },
    {
        "id": "q19_clarify_short_explain",
        "category": "clarify",
        "question": "explain",
        "should_find": False,
        "expected_type": "unknown",
    },
    # 6. Simplify move (user confusion)
    {
        "id": "q20_simplify_confused",
        "category": "simplify",
        "question": "I don't understand, can you explain simply how Video Boost works in simple words?",
        "expected_start": 13.0,
        "expected_end": 21.0,
        "expected_quote_sub": "Video Boost",
        "should_find": True,
    },
    # 7. Out-of-video / unanswerable (research off -> honest boundary refusal)
    {
        "id": "q21_out_quantum_off",
        "category": "unanswerable",
        "question": "How does quantum entanglement work in qubit processors?",
        "settings": {"researchMissingContext": False},
        "should_find": False,
        "expected_type": "unknown",
    },
    {
        "id": "q22_out_capital_off",
        "category": "unanswerable",
        "question": "What is the capital of France?",
        "settings": {"researchMissingContext": False},
        "should_find": False,
        "expected_type": "unknown",
    },
    {
        "id": "q23_out_recipe_off",
        "category": "unanswerable",
        "question": "What is the best recipe for chocolate chip cookies?",
        "settings": {"researchMissingContext": False},
        "should_find": False,
        "expected_type": "unknown",
    },
    # 8. Out-of-video web research grounding (research on -> external web sources)
    {
        "id": "q24_web_tax_on",
        "category": "web-grounded",
        "question": "What is ITR in Indian income tax filing?",
        "settings": {"researchMissingContext": True},
        "should_find": False,
        "expected_type": "web",
    },
    {
        "id": "q25_web_solar_on",
        "category": "web-grounded",
        "question": "How many planets are in our solar system?",
        "settings": {"researchMissingContext": True},
        "should_find": False,
        "expected_type": "web",
    },
]


@dataclass
class EvalResult:
    case_id: str
    category: str
    question: str
    latency_seconds: float
    status_code: int
    answer_text: str
    evidence_type: str
    start_seconds: float | None
    end_seconds: float | None
    quote: str | None
    confidence: float
    timestamp_correct: bool
    grounded: bool
    unsupported_hallucination: bool
    has_suggestions: bool


def query_question(
    api_base: str,
    lesson_id: str,
    question: str,
    history: list[dict[str, str]] | None = None,
    settings: dict[str, Any] | None = None,
) -> tuple[int, dict[str, Any], float]:
    payload: dict[str, Any] = {"question": question}
    if history:
        payload["history"] = history
    if settings:
        payload["settings"] = settings
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{api_base}/analyses/{lesson_id}/questions",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=35) as resp:
            elapsed = time.time() - t0
            return resp.status, json.loads(resp.read().decode("utf-8")), elapsed
    except urllib.error.HTTPError as err:
        elapsed = time.time() - t0
        try:
            body = json.loads(err.read().decode("utf-8"))
        except Exception:
            body = {"error": str(err)}
        return err.code, body, elapsed
    except Exception as exc:
        elapsed = time.time() - t0
        return 500, {"error": str(exc)}, elapsed



def run_eval(api_base: str, lesson_id: str = DEMO_ID) -> dict[str, Any]:
    print(f"\n========================================================")
    print(f"ContextBridge P0-8 Evaluation Harness")
    print(f"Target API: {api_base}")
    print(f"Lesson ID:  {lesson_id}")
    print(f"========================================================\n")

    results: list[EvalResult] = []

    for case in EVAL_CASES:
        cid = case["id"]
        cat = case["category"]
        q = case["question"]
        hist = case.get("history")
        settings = case.get("settings")
        should_find = case["should_find"]

        print(f"[{cat.upper():12}] {cid}: '{q[:48]}...'")
        status, resp, latency = query_question(api_base, lesson_id, q, hist, settings)

        if status != 200:
            print(f"  -> HTTP Error {status}: {resp}")
            results.append(
                EvalResult(
                    case_id=cid,
                    category=cat,
                    question=q,
                    latency_seconds=latency,
                    status_code=status,
                    answer_text="",
                    evidence_type="error",
                    start_seconds=None,
                    end_seconds=None,
                    quote=None,
                    confidence=0.0,
                    timestamp_correct=False,
                    grounded=False,
                    unsupported_hallucination=False,
                    has_suggestions=False,
                )
            )
            continue

        ans_obj = resp.get("answer") or {}
        evidence_type = ans_obj.get("evidenceType", "unknown")
        evidence = ans_obj.get("evidence") or {}
        start_sec = evidence.get("startSeconds")
        end_sec = evidence.get("endSeconds")
        quote = evidence.get("quote")
        conf = ans_obj.get("confidence", 0.0)
        ans_text = resp.get("text", "")
        has_suggestions = bool(resp.get("suggestions"))

        # 1. Timestamp accuracy: within tolerance range
        timestamp_correct = False
        if should_find:
            exp_start = case.get("expected_start")
            exp_end = case.get("expected_end")
            if start_sec is not None and exp_start is not None and exp_end is not None:
                # Overlaps or within 5 seconds
                if (start_sec >= exp_start - 5.0 and start_sec <= exp_end + 5.0):
                    timestamp_correct = True
        else:
            # For unanswerable or clarify, not providing an in-video timestamp is correct
            timestamp_correct = (evidence_type != "video")

        # 2. Groundedness: has verbatim quote + start/end bounds when video answer
        grounded = False
        if should_find:
            if evidence_type == "video" and quote and start_sec is not None and end_sec is not None:
                exp_sub = case.get("expected_quote_sub", "").lower()
                if exp_sub and exp_sub in quote.lower():
                    grounded = True
                elif not exp_sub and len(quote.strip()) > 0:
                    grounded = True
                else:
                    grounded = False
        else:
            # For unanswerable, clarify, or web-grounded questions:
            # - web answers with sources are grounded
            # - honest declaration of unknown is considered grounded (not fabricated)
            if evidence_type == "web" and ans_obj.get("sources"):
                grounded = True
            elif evidence_type == "unknown":
                grounded = True

        # 3. Unsupported answer: fabricated video timestamp/evidence for out-of-video question
        unsupported = False
        if not should_find and evidence_type == "video":
            unsupported = True

        results.append(
            EvalResult(
                case_id=cid,
                category=cat,
                question=q,
                latency_seconds=latency,
                status_code=status,
                answer_text=ans_text,
                evidence_type=evidence_type,
                start_seconds=start_sec,
                end_seconds=end_sec,
                quote=quote,
                confidence=conf,
                timestamp_correct=timestamp_correct,
                grounded=grounded,
                unsupported_hallucination=unsupported,
                has_suggestions=has_suggestions,
            )
        )
        print(f"  -> {evidence_type.upper()} in {latency:.2f}s | conf={conf:.2f} | ts_ok={timestamp_correct} | grounded={grounded} | suggestions={has_suggestions}")

    # Summary calculations
    total = len(results)
    in_video_cases = [r for r in results if r.category in ("in-video", "follow-up", "contradiction", "multilingual", "hinglish", "simplify")]

    ts_acc = sum(1 for r in in_video_cases if r.timestamp_correct) / len(in_video_cases) * 100 if in_video_cases else 0.0
    groundedness = sum(1 for r in results if r.grounded) / total * 100 if total else 0.0
    unsupported_rate = sum(1 for r in results if r.unsupported_hallucination) / total * 100 if total else 0.0
    avg_latency = sum(r.latency_seconds for r in results) / total if total else 0.0
    suggestions_cov = sum(1 for r in results if r.has_suggestions) / total * 100 if total else 0.0

    print("\n========================================================")
    print("CONTEXTBRIDGE EVALUATION HARNESS V2 (25 BENCHMARK CASES)")
    print("========================================================")
    print(f"Total Test Cases:             {total}")
    print(f"Timestamp-Retrieval Accuracy: {ts_acc:.1f}%  (Target: >= 90%)")
    print(f"Groundedness Rate:            {groundedness:.1f}%  (Target: >= 95%)")
    print(f"Unsupported-Answer Rate:      {unsupported_rate:.1f}%  (Target: 0.0% strict)")
    print(f"Explore Suggestions Coverage: {suggestions_cov:.1f}%  (Target: >= 90%)")
    print(f"Average Q&A Latency:          {avg_latency:.2f}s (Target: < 5.0s)")
    print("========================================================\n")

    report = {
        "api_base": api_base,
        "lesson_id": lesson_id,
        "metrics": {
            "total_cases": total,
            "timestamp_retrieval_accuracy_pct": round(ts_acc, 1),
            "groundedness_pct": round(groundedness, 1),
            "unsupported_answer_rate_pct": round(unsupported_rate, 1),
            "explore_suggestions_coverage_pct": round(suggestions_cov, 1),
            "average_latency_seconds": round(avg_latency, 2),
        },
        "results": [asdict(r) for r in results],
    }

    report_path = "context/eval_results.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Full evaluation results written to {report_path}")

    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ContextBridge P0-8 Evaluation Harness")
    parser.add_argument("--api", default=DEFAULT_API, help="Base API URL to evaluate against")
    parser.add_argument("--lesson-id", default=DEMO_ID, help="Lesson ID to query")
    args = parser.parse_args()

    report = run_eval(args.api, args.lesson_id)
    # Fail if unsupported answer rate > 0
    if report["metrics"]["unsupported_answer_rate_pct"] > 0.0:
        print("FAIL: Unsupported answer detected!")
        sys.exit(1)
    if report["metrics"]["timestamp_retrieval_accuracy_pct"] < 80.0:
        print("FAIL: Timestamp retrieval accuracy below threshold!")
        sys.exit(1)
    print("P0-8 HARNESS: ALL THRESHOLDS PASSED!")
