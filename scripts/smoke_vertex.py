"""P0-10c smoke test — Gemini-on-Vertex credentials + quota.

Verifies the two capabilities the whole product depends on:
  1. Text generation (auth + quota path).
  2. Video understanding on a short (<=30 s) clip — the core capability risk
     from context/ARCHITECTURE.md (quota/rate limits are the #1 recorded risk).

Run from the repo root:  python scripts/smoke_vertex.py
Exit code 0 = both pass. Outcome is recorded in context/DECISIONS.md.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # repo root

import vertexai
from vertexai.generative_models import GenerativeModel, Part

from api.config import get_settings

# Public Google Cloud sample videos (Vertex AI docs). First reachable one wins.
SAMPLE_VIDEOS = [
    "gs://cloud-samples-data/generative-ai/video/pixel8.mp4",
    "gs://cloud-samples-data/video/animals.mp4",
]


def timed(fn):
    start = time.perf_counter()
    result = fn()
    return result, time.perf_counter() - start


def main() -> int:
    settings = get_settings()
    if not settings.google_project_id:
        print("FAIL: GOOGLE_PROJECT_ID not set (.env.local). Fixtures-only mode.")
        return 1

    vertexai.init(project=settings.google_project_id, location=settings.google_region)
    model = GenerativeModel(settings.vertex_model_id)
    print(f"project={settings.google_project_id} region={settings.google_region} "
          f"model={settings.vertex_model_id}")

    ok = True

    # --- 1. Text ---
    try:
        resp, dt = timed(lambda: model.generate_content(
            "Reply with exactly: ContextBridge smoke OK"))
        print(f"PASS text   ({dt:.1f}s): {resp.text.strip()[:80]}")
    except Exception as exc:  # noqa: BLE001 - smoke test reports any failure
        ok = False
        print(f"FAIL text: {type(exc).__name__}: {exc}")

    # --- 2. Video (<=30 s clip) ---
    video_ok = False
    for uri in SAMPLE_VIDEOS:
        try:
            clip = Part.from_uri(uri=uri, mime_type="video/mp4")
            resp, dt = timed(lambda: model.generate_content(
                ["In one short sentence, what happens in this video?", clip]))
            print(f"PASS video  ({dt:.1f}s) {uri}\n  -> {resp.text.strip()[:120]}")
            video_ok = True
            break
        except Exception as exc:  # noqa: BLE001
            print(f"  video source failed {uri}: {type(exc).__name__}: "
                  f"{str(exc)[:160]}")
    if not video_ok:
        ok = False
        print("FAIL video: no sample clip could be analysed.")

    print("SMOKE RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
