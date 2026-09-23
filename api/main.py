"""ContextBridge API — Phase 0 skeleton (P0-10b).

Deployed early per BUILD_PLAN Phase 4 (P0-9a): the Cloud Run service exists
and answers /health before any real feature lands. Phase 1 adds:
  POST /analyses            (P0-2a — multipart upload -> Gemini pipeline)
  GET  /analyses/{id}       (P0-2a — Lesson payload per context/API.md §3.1)
  GET  /analyses/{id}/video (P0-2a — Range-supporting stream)
  POST /questions           (P0-1  — agent loop, Phase 2)
  POST /lessons/{id}/outputs (P0-5 — accessible artifacts, Phase 2)
  POST /evaluate            (P0-8  — internal eval harness, Phase 5)
Error envelope, fixtures, and serialisation follow context/API.md exactly.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import get_settings

settings = get_settings()

app = FastAPI(
    title="ContextBridge API",
    version="0.1.0",
    description="Video understanding copilot — grounded answers with timestamps.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.web_origin],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health() -> dict:
    """Smoke/liveness probe for Cloud Run and P0-9c deployed smoke tests."""
    return {
        "status": "ok",
        "service": "contextbridge-api",
        "phase": "0-skeleton",
        "analysis_enabled": settings.analysis_enabled,
        "model": settings.vertex_model_id if settings.analysis_enabled else None,
    }
