"""P0-6 fixture seeding — the pre-analysed demo lesson, zero LLM calls.

`demo-binary` is seeded on every startup (Cloud Run cold starts included) so
`/healthz` and the locked demo button work immediately, even with the LLM
quota exhausted or the database ephemeral (ARCHITECTURE §11, §15). The fixture
ships one genuine contradiction pair (D-02) and per-event confidence (D-05),
and still passes through `MediaAnalysis.from_dict` — the same validation gate
as live Gemini output.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from api.config import Settings
from contextbridge_schema import MediaAnalysis
from contextbridge_store import create_analysis, get_analysis, initialize, update_analysis

DEMO_ANALYSIS_ID = "demo-binary"
FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "demo_binary.json"

# A real binary-lesson video can be dropped in at api/fixtures/demo-binary.mp4
# to override the public fallback (D-13). The fallback is Google's public
# cloud-samples-data clip (the mock's gtv-videos-bucket turned private in 2026).
LOCAL_DEMO_VIDEO = Path(__file__).resolve().parent / "fixtures" / "demo-binary.mp4"
PUBLIC_DEMO_VIDEO_URL = (
    "https://storage.googleapis.com/cloud-samples-data/generative-ai/video/pixel8.mp4"
)

_demo_row: dict[str, Any] | None = None  # in-memory store-row copy (§15 fallback)


def load_fixture() -> dict[str, Any]:
    """Load and validate the fixture envelope through the canonical gate."""
    raw = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    analysis = MediaAnalysis.from_dict(raw)  # same gate as live model output
    envelope = analysis.to_dict()
    for extra in ("durationSeconds", "title", "createdAt", "contradictions"):
        if extra in raw:
            envelope[extra] = raw[extra]
    return envelope


def _demo_storage_uri(settings: Settings) -> str:
    if LOCAL_DEMO_VIDEO.exists():
        return str(LOCAL_DEMO_VIDEO)
    if settings.bucket:
        try:  # use the bucket copy only if it actually exists
            from google.cloud import storage

            client = storage.Client(project=settings.google_project_id)
            blob = client.bucket(settings.bucket).blob("fixtures/demo-binary.mp4")
            if blob.exists():
                return f"gs://{settings.bucket}/{blob.name}"
        except Exception:
            pass
    return PUBLIC_DEMO_VIDEO_URL


def seed_fixtures(settings: Settings) -> bool:
    """Idempotent startup seed. Returns True when the demo lesson is servable."""
    global _demo_row
    try:
        envelope = load_fixture()
    except Exception:
        return False
    storage_uri = _demo_storage_uri(settings)
    try:
        initialize()
        if not get_analysis(DEMO_ANALYSIS_ID):
            create_analysis(DEMO_ANALYSIS_ID, "demo-binary.mp4", "video/mp4")
        update_analysis(
            DEMO_ANALYSIS_ID,
            status="completed",
            result=envelope,
            storage_uri=storage_uri,
        )
        row = get_analysis(DEMO_ANALYSIS_ID)
        _demo_row = {key: row[key] for key in row.keys()} if row else None
    except Exception:
        # DB unreachable — the in-memory seed keeps the demo truthful (§15).
        _demo_row = {
            "analysis_id": DEMO_ANALYSIS_ID,
            "filename": "demo-binary.mp4",
            "mime_type": "video/mp4",
            "status": "completed",
            "created_at": envelope.get("createdAt", ""),
            "storage_uri": storage_uri,
            "result_json": json.dumps(envelope, ensure_ascii=False),
            "error": None,
        }
    return _demo_row is not None


def demo_row() -> dict[str, Any] | None:
    """In-memory seed row — serves demo-binary even when the DB is down (§15)."""
    return _demo_row
