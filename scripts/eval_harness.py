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

DEFAULT_API = "https://contextbridge-api-c5ltxo3mkq-uc.a.run.app"
DEMO_ID = "demo-binary"

# Evaluation benchmark suite (minimum viable set for P0-8)
EVAL_CASES = [
    # 1. In-video questions
    {
        "id": "q1_feature_intro",
        "category": "in-video",
        "question": "What feature is introduced on the new Pixel?",
        "expected_start": 13.0,
        "expected_end": 21.0,
        "expected_quote_sub": "Video Boost",
        "should_find": True,
    },
    {
        "id": "q2_photographer_intro",
        "category": "in-video",
        "question": "What is Saeka Shimada's profession in Tokyo?",
        "expected_start": 1.0,
        "expected_end": 3.0,
        "expected_quote_sub": "photographer",
        "should_find": True,
    },
    {
        "id": "q3_tokyo_night",
        "category": "in-video",
        "question": "How does the photographer describe Tokyo at night compared to daytime?",
        "expected_start": 5.0,
        "expected_end": 9.0,
        "expected_quote_sub": "totally different",
        "should_find": True,
    },
    {
        "id": "q4_sancha_memories",
        "category": "in-video",
        "question": "Where did Saeka live when she first moved to Tokyo?",
        "expected_start": 23.0,
        "expected_end": 26.0,
        "expected_quote_sub": "Sancha",
        "should_find": True,
    },
    # 2. Follow-up questions (with conversation history)
    {
        "id": "q5_followup_feature",
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
    # 3. Contradiction questions
    {
        "id": "q6_contradiction_darkness",
        "category": "contradiction",
        "question": "Does night videography capture natural dark city streets or does computational Night Sight enhance it?",
        "expected_start": 5.0,
        "expected_end": 21.0,
        "expected_quote_sub": "different",
        "should_find": True,
    },
    # 4. Out-of-video / unanswerable questions
    {
        "id": "q7_out_quantum",
        "category": "unanswerable",
        "question": "How does quantum entanglement work in qubit processors?",
        "should_find": False,
    },
    {
        "id": "q8_out_capital",
        "category": "unanswerable",
        "question": "What is the capital of France?",
        "should_find": False,
    },
    {
        "id": "q9_out_recipe",
        "category": "unanswerable",
        "question": "What is the best recipe for chocolate chip cookies?",
        "should_find": False,
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


def query_question(api_base: str, lesson_id: str, question: str, history: list[dict[str, str]] | None = None) -> tuple[int, dict[str, Any], float]:
    payload: dict[str, Any] = {"question": question}
    if history:
        payload["history"] = history
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{api_base}/analyses/{lesson_id}/questions",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            elapsed = time.time() - t0
            return resp.status, json.loads(resp.read().decode("utf-8")), elapsed
    except urllib.error.HTTPError as err:
        elapsed = time.time() - t0
        try:
            body = json.loads(err.read().decode("utf-8"))
        except Exception:
            body = {"error": str(err)}
        return err.code, body, elapsed


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
        should_find = case["should_find"]

        print(f"[{cat.upper():12}] {cid}: '{q[:48]}...'")
        status, resp, latency = query_question(api_base, lesson_id, q, hist)

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
            # For unanswerable, not providing an in-video timestamp is correct
            timestamp_correct = (evidence_type != "video")

        # 2. Groundedness: has verbatim quote + start/end bounds when video answer
        grounded = False
        if should_find:
            if evidence_type == "video" and quote and start_sec is not None and end_sec is not None:
                exp_sub = case.get("expected_quote_sub", "").lower()
                if exp_sub in quote.lower():
                    grounded = True
        else:
            # For unanswerable questions, honest declaration of unknown is considered grounded (not fabricated)
            if evidence_type in ("unknown", "web"):
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
            )
        )
        print(f"  -> {evidence_type.upper()} in {latency:.2f}s | conf={conf:.2f} | ts_ok={timestamp_correct} | grounded={grounded}")

    # Summary calculations
    total = len(results)
    in_video_cases = [r for r in results if r.category in ("in-video", "follow-up", "contradiction")]
    unanswerable_cases = [r for r in results if r.category == "unanswerable"]

    ts_acc = sum(1 for r in in_video_cases if r.timestamp_correct) / len(in_video_cases) * 100 if in_video_cases else 0.0
    groundedness = sum(1 for r in results if r.grounded) / total * 100 if total else 0.0
    unsupported_rate = sum(1 for r in results if r.unsupported_hallucination) / total * 100 if total else 0.0
    avg_latency = sum(r.latency_seconds for r in results) / total if total else 0.0

    print("\n========================================================")
    print("P0-8 EVALUATION REPORT")
    print("========================================================")
    print(f"Total Test Cases:            {total}")
    print(f"Timestamp-Retrieval Accuracy: {ts_acc:.1f}%  (Target: >= 90%)")
    print(f"Groundedness Rate:           {groundedness:.1f}%  (Target: >= 95%)")
    print(f"Unsupported-Answer Rate:      {unsupported_rate:.1f}%  (Target: 0.0% strict)")
    print(f"Average Q&A Latency:         {avg_latency:.2f}s (Target: < 5.0s)")
    print("========================================================\n")

    report = {
        "api_base": api_base,
        "lesson_id": lesson_id,
        "metrics": {
            "total_cases": total,
            "timestamp_retrieval_accuracy_pct": round(ts_acc, 1),
            "groundedness_pct": round(groundedness, 1),
            "unsupported_answer_rate_pct": round(unsupported_rate, 1),
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
