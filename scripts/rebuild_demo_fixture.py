"""Rebuild api/fixtures/demo_binary.json from api/fixtures/demo-binary.mp4.

Uses the same Gemini pipeline as a live upload. Does not invent a transcript.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.config import get_settings
from api.pipeline import (
    _mp4_duration_seconds,
    _rescale_timestamps,
    analyze_video,
    extract_contradictions,
)

FIXTURE_MP4 = ROOT / "api" / "fixtures" / "demo-binary.mp4"
FIXTURE_JSON = ROOT / "api" / "fixtures" / "demo_binary.json"
LESSON_TITLE = "Create a lesson plan template using Gemini in Docs"


def main() -> None:
    settings = get_settings()
    if not settings.analysis_enabled and not settings.google_api_key:
        raise SystemExit("No Gemini credentials. Set GOOGLE_PROJECT_ID or GOOGLE_API_KEY.")
    video = FIXTURE_MP4.read_bytes()
    envelope = analyze_video(video, "video/mp4", settings)
    true_seconds = _mp4_duration_seconds(video)
    if true_seconds is not None:
        envelope = _rescale_timestamps(envelope, true_seconds)
    contradictions = extract_contradictions(envelope, settings)
    if contradictions:
        envelope["contradictions"] = contradictions
    envelope["title"] = LESSON_TITLE
    envelope["createdAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    FIXTURE_JSON.write_text(
        json.dumps(envelope, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    first = (envelope.get("transcript") or [{}])[0].get("text", "")
    print("title:", envelope.get("title"))
    print("duration:", envelope.get("durationSeconds"))
    print("events:", len(envelope.get("events") or []))
    print("transcript lines:", len(envelope.get("transcript") or []))
    print("contradictions:", len(envelope.get("contradictions") or []))
    print("first line:", first)


if __name__ == "__main__":
    main()
