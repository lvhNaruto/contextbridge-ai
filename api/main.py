"""ContextBridge API — Phase 1 pipeline + Phase 2 agent (P0-1a/b).

Contract: context/API.md — the API adapts to the locked frontend, never the
reverse. Implemented here:
  POST /analyses                multipart upload → synchronous Gemini pipeline
  GET  /analyses/{id}           full Lesson (✳ contradictions, ✳ confidence)
  GET  /analyses/{id}/video     Range-supporting playback (local / GCS / 302)
  GET  /analyses/{id}/chapters  reserved projection (locked api.ts names it)
  POST /analyses/{id}/questions grounded Q&A — the agent (api/agent.py)
  GET  /healthz                 ops probe (demoSeeded + store reachability)
  GET  /health                  Phase 0 smoke alias
Still reserved (unwired): the voice-question alias (API.md §4.1) and
Phase 5's internal eval harness.
"""

from __future__ import annotations

import json
import re
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Literal

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse, StreamingResponse
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool
from starlette.exceptions import HTTPException as StarletteHTTPException

from api import agent, pipeline, seed
from api.config import get_settings
from contextbridge_schema import MediaAnalysis
from contextbridge_store import create_analysis, get_analysis

settings = get_settings()

ID_PATTERN = re.compile(r"^[a-zA-Z0-9-]{1,64}$")  # §4.2 — blocks traversal


def _envelope(code: str, message: str) -> dict[str, Any]:
    """The one error shape everywhere (API.md §1, ARCHITECTURE §4.3)."""
    return {"error": {"code": code, "message": message}}


class ApiError(Exception):
    def __init__(self, status_code: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message


@asynccontextmanager
async def lifespan(app: FastAPI):
    # P0-6: fixtures seed on every cold start; zero LLM calls (§16.4).
    app.state.demo_seeded = seed.seed_fixtures(settings)
    yield


app = FastAPI(
    title="ContextBridge API",
    version="0.2.0",
    description="Video understanding copilot — grounded answers with timestamps.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip() for origin in settings.web_origin.split(",") if origin.strip()
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.exception_handler(ApiError)
async def api_error_handler(_: Request, exc: ApiError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code, content=_envelope(exc.code, exc.message)
    )


@app.exception_handler(StarletteHTTPException)
async def http_error_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
    code = {404: "not_found", 405: "method_not_allowed"}.get(
        exc.status_code, "http_error"
    )
    message = exc.detail if isinstance(exc.detail, str) else code
    return JSONResponse(status_code=exc.status_code, content=_envelope(code, message))


@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=_envelope("invalid_request", "Request validation failed."),
    )


def _check_id(analysis_id: str) -> None:
    if not ID_PATTERN.fullmatch(analysis_id):
        raise ApiError(400, "invalid_id", "Malformed analysis id.")


def _load_row(analysis_id: str) -> dict[str, Any]:
    """Store row as a plain dict; falls back to the in-memory demo seed."""
    try:
        row = get_analysis(analysis_id)
        if row is not None:
            return {key: row[key] for key in row.keys()}
    except Exception:
        pass  # DB down — demo-binary must survive (ARCHITECTURE §15)
    if analysis_id == seed.DEMO_ANALYSIS_ID:
        fallback = seed.demo_row()
        if fallback is not None:
            return fallback
    raise ApiError(404, "not_found", "Unknown analysis id.")


# ---------------------------------------------------------------------------
# P0-2c — MediaAnalysis → Lesson serialisation (API.md §2, camelCase exact)
# ---------------------------------------------------------------------------


def _clean_number(value: float) -> int | float:
    """173.0 → 173 — matches the integral timestamps in web/lib/mock-data.ts."""
    return int(value) if float(value).is_integer() else value


def _iso_z(timestamp: str) -> str:
    return timestamp.replace("+00:00", "Z")


def _derive_title(filename: str) -> str:
    """Exactly as the mock does: strip extension, '-'/'_' → spaces (API §3.2)."""
    return re.sub(r"[-_]+", " ", Path(filename).stem).strip() or "Untitled lesson"


def _clean_statement(stmt: dict[str, Any]) -> dict[str, Any]:
    cleaned = {
        "text": stmt["text"],
        "startSeconds": _clean_number(stmt["startSeconds"]),
        "endSeconds": _clean_number(stmt["endSeconds"]),
    }
    if stmt.get("quote"):
        cleaned["quote"] = stmt["quote"]
    return cleaned


def _lesson_from_row(row: dict[str, Any], base_url: str) -> dict[str, Any]:
    envelope = json.loads(row["result_json"])
    analysis = MediaAnalysis.from_dict(envelope)  # corrupt rows raise → 409
    # durationSeconds comes from the model and can be unreliable; the contract
    # invariant (timestamps ≤ durationSeconds) wins, so clamp from below.
    duration = pipeline.envelope_duration(envelope)
    lesson: dict[str, Any] = {
        "id": row["analysis_id"],
        "title": envelope.get("title") or _derive_title(row["filename"]),
        "videoUrl": f"{base_url}/analyses/{row['analysis_id']}/video",
        "durationSeconds": _clean_number(float(duration)),
        "createdAt": _iso_z(envelope.get("createdAt") or row["created_at"]),
        "language": analysis.language,
        "summary": analysis.summary,
        "topics": list(analysis.topics),
        "chapters": [
            {
                "id": event.id,
                "startSeconds": _clean_number(event.start_seconds),
                "endSeconds": _clean_number(event.end_seconds),
                "title": event.title,
                "description": event.description,
                "confidence": event.confidence,  # ✳ A4 — no longer dropped
            }
            for event in analysis.events
        ],
        "transcript": [
            {
                "startSeconds": _clean_number(segment["startSeconds"]),
                "endSeconds": _clean_number(segment["endSeconds"]),
                "text": segment["text"],
            }
            for segment in analysis.transcript
        ],
    }
    if envelope.get("contradictions"):  # ✳ A1 — absent when none (API §2)
        lesson["contradictions"] = [
            {
                "id": pair["id"],
                "claim": pair["claim"],
                "statementA": _clean_statement(pair["statementA"]),
                "statementB": _clean_statement(pair["statementB"]),
                **({"note": pair["note"]} if pair.get("note") else {}),
            }
            for pair in envelope["contradictions"]
        ]
    return lesson


def _completed_row(analysis_id: str) -> dict[str, Any]:
    """Row guard shared by the lesson and question routes (404 / 409, API §3.2)."""
    row = _load_row(analysis_id)
    if row["status"] == "failed":
        raise ApiError(
            409, "analysis_failed", row.get("error") or "This analysis failed."
        )
    if row["status"] != "completed" or not row.get("result_json"):
        raise ApiError(409, "analysis_incomplete", "Analysis has not completed.")
    return row


def _completed_lesson(analysis_id: str, base_url: str) -> dict[str, Any]:
    """The lesson-shaped routes' body (404 / 409 per API §3.2)."""
    row = _completed_row(analysis_id)
    try:
        return _lesson_from_row(row, base_url)
    except (ValueError, json.JSONDecodeError) as exc:
        raise ApiError(409, "analysis_failed", f"Stored analysis is invalid: {exc}")


def _completed_envelope(analysis_id: str) -> dict[str, Any]:
    """Stored MediaAnalysis envelope for the agent (404 / 409 per API §3.4)."""
    row = _completed_row(analysis_id)
    try:
        envelope = json.loads(row["result_json"])
    except json.JSONDecodeError as exc:
        raise ApiError(409, "analysis_failed", f"Stored analysis is invalid: {exc}")
    if not isinstance(envelope, dict):
        raise ApiError(409, "analysis_failed", "Stored analysis is invalid.")
    return envelope


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/health")
def health() -> dict[str, Any]:
    """Phase 0 smoke alias — kept for P0-9c deployed smoke tests."""
    return {
        "status": "ok",
        "service": "contextbridge-api",
        "phase": "1-analysis-pipeline",
        "analysis_enabled": settings.analysis_enabled,
        "model": settings.vertex_model_id if settings.analysis_enabled else None,
    }


@app.get("/healthz")
def healthz(request: Request) -> JSONResponse:
    """Ops probe (API.md §5): 503 when the demo failed to seed or store is down."""
    store_ok = True
    try:
        get_analysis(seed.DEMO_ANALYSIS_ID)
    except Exception:
        store_ok = False
    seeded = bool(getattr(request.app.state, "demo_seeded", False))
    if not (seeded and store_ok):
        return JSONResponse(
            status_code=503,
            content=_envelope("not_ready", "Demo fixture or store unavailable."),
        )
    return JSONResponse(
        status_code=200,
        content={"status": "ok", "demoSeeded": True, "model": settings.vertex_model_id},
    )


@app.post("/analyses")
async def create_analysis_endpoint(
    video: UploadFile | None = File(default=None),
) -> dict[str, str]:
    """Upload & analyse, synchronously (API.md §3.1) — the frontend never polls."""
    if video is None or not video.filename:
        raise ApiError(400, "missing_file", "Attach a video file as 'video'.")
    data = await video.read(pipeline.MAX_UPLOAD_BYTES + 1)
    if not data:
        raise ApiError(400, "missing_file", "The uploaded file is empty.")
    if len(data) > pipeline.MAX_UPLOAD_BYTES:
        raise ApiError(413, "file_too_large", "Videos are limited to 100 MB.")
    mime_type = pipeline.sniff_video_mime(data[:16], video.filename)
    if mime_type is None:
        raise ApiError(
            422,
            "unsupported_video",
            "Unsupported or undecodable video (mp4, mov, mpeg, webm, avi).",
        )
    if not (settings.analysis_enabled or settings.google_api_key):
        raise ApiError(
            503, "analysis_disabled", "Gemini credentials are not configured."
        )
    analysis_id = pipeline.new_analysis_id()
    create_analysis(analysis_id, video.filename, mime_type)
    try:
        await run_in_threadpool(
            pipeline.run_analysis,
            analysis_id,
            video.filename,
            data,
            mime_type,
            settings,
        )
    except pipeline.PipelineError:
        raise ApiError(
            502, "analysis_failed", "The video could not be analysed. Please retry."
        )
    return {"id": analysis_id}


@app.get("/analyses/{analysis_id}")
def get_lesson(analysis_id: str, request: Request) -> dict[str, Any]:
    """The full Lesson (API.md §3.2), incl. ✳ contradictions and ✳ confidence."""
    _check_id(analysis_id)
    return _completed_lesson(analysis_id, str(request.base_url).rstrip("/"))


@app.get("/analyses/{analysis_id}/chapters")
def get_chapters(analysis_id: str, request: Request) -> list[dict[str, Any]]:
    """Reserved projection (API.md §4.2) — named by locked api.ts, uncalled today."""
    _check_id(analysis_id)
    return _completed_lesson(analysis_id, str(request.base_url).rstrip("/"))["chapters"]


# ---------------------------------------------------------------------------
# P0-1b — POST /analyses/{id}/questions: the agent (API.md §3.4, ARCH. §6.3)
# ---------------------------------------------------------------------------


class LessonSettingsIn(BaseModel):
    """LessonSettings exactly as the locked client sends them (API §2 inv. 4)."""

    answerLanguage: Literal["auto", "en", "hi"] = "auto"
    explanationLevel: Literal["beginner", "intermediate", "expert"] = "beginner"
    researchMissingContext: bool = True


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    settings: LessonSettingsIn = Field(default_factory=LessonSettingsIn)
    isVoice: bool = False


@app.post("/analyses/{analysis_id}/questions")
def ask_question(analysis_id: str, payload: QuestionRequest) -> dict[str, Any]:
    """Grounded Q&A (API.md §3.4) via the agent loop (ARCHITECTURE §6.3).

    Stateless per question (§5.2): the stored envelope is the only server-side
    input besides the request; nothing about the conversation is kept. The
    sync route runs in FastAPI's threadpool, so the provider ladder's waits
    never block the event loop (25 s budget: API.md §1 timeouts).
    """
    _check_id(analysis_id)
    question = payload.question.strip()
    if not question:
        raise ApiError(422, "invalid_question", "The question is empty.")
    envelope = _completed_envelope(analysis_id)
    try:
        return agent.answer_question(
            question,
            envelope,
            payload.settings.model_dump(),
            settings,
            is_voice=payload.isVoice,
        )
    except pipeline.PipelineError:
        # §6.5 last resort — total LLM failure, honestly reported (API.md §3.4).
        raise ApiError(
            502, "answer_failed", "The model could not answer right now. Please retry."
        )


# ---------------------------------------------------------------------------
# GET /analyses/{id}/video — Range-supporting playback (API.md §3.3)
# ---------------------------------------------------------------------------

_VIDEO_HEADERS = {"Accept-Ranges": "bytes", "Cache-Control": "private, max-age=3600"}


def _parse_range(range_header: str | None, size: int) -> tuple[int, int, int]:
    """→ (start, end, status). Raises ApiError(416) on unsatisfiable ranges."""
    if not range_header:
        return 0, size - 1, 200
    match = re.fullmatch(r"bytes=(\d*)-(\d*)", range_header.strip())
    if not match or not (match.group(1) or match.group(2)):
        raise ApiError(416, "invalid_range", "Malformed Range header.")
    first, last = match.group(1), match.group(2)
    if not first:  # suffix range: the last N bytes
        start = max(0, size - int(last))
        end = size - 1
    else:
        start = int(first)
        end = int(last) if last else size - 1
    if start >= size or end < start:
        raise ApiError(416, "invalid_range", f"Range outside 0-{size - 1}.")
    return start, min(end, size - 1), 206


def _serve_local_file(path: Path, range_header: str | None, mime_type: str):
    size = path.stat().st_size
    start, end, status = _parse_range(range_header, size)
    headers = {
        **_VIDEO_HEADERS,
        "Content-Range": f"bytes {start}-{end}/{size}",
        "Content-Length": str(end - start + 1),
    }

    def stream():
        with path.open("rb") as handle:
            handle.seek(start)
            remaining = end - start + 1
            while remaining > 0:
                chunk = handle.read(min(64 * 1024, remaining))
                if not chunk:
                    break
                remaining -= len(chunk)
                yield chunk

    return StreamingResponse(
        stream(), status_code=status, headers=headers, media_type=mime_type
    )


def _serve_gcs(uri: str, range_header: str | None, mime_type: str):
    from google.cloud import storage

    bucket_name, blob_name = uri[5:].split("/", 1)
    blob = storage.Client(project=settings.google_project_id).bucket(
        bucket_name
    ).blob(blob_name)
    blob.reload()
    size = int(blob.size or 0)
    if size <= 0:
        raise ApiError(404, "not_found", "Video object is empty or missing.")
    start, end, status = _parse_range(range_header, size)
    data = blob.download_as_bytes(start=start, end=end)
    headers = {
        **_VIDEO_HEADERS,
        "Content-Range": f"bytes {start}-{end}/{size}",
        "Content-Length": str(len(data)),
    }
    return StreamingResponse(
        iter([data]), status_code=status, headers=headers, media_type=mime_type
    )


@app.get("/analyses/{analysis_id}/video")
def get_video(analysis_id: str, request: Request):
    """Playback bytes: GCS proxy, local fixture/upload file, or a 302 (§3.3)."""
    _check_id(analysis_id)
    row = _load_row(analysis_id)
    uri = row.get("storage_uri") or ""
    if not uri:
        raise ApiError(404, "not_found", "No video stored for this analysis.")
    mime_type = row.get("mime_type") or "video/mp4"
    range_header = request.headers.get("range")
    if uri.startswith("gs://"):
        try:
            return _serve_gcs(uri, range_header, mime_type)
        except ApiError:
            raise
        except Exception as exc:
            raise ApiError(404, "not_found", f"Video object unavailable: {exc}")
    if uri.startswith(("http://", "https://")):
        return RedirectResponse(uri, status_code=302)
    path = Path(uri)
    if path.exists():
        return _serve_local_file(path, range_header, mime_type)
    raise ApiError(404, "not_found", "Video file is unavailable.")
