"""Analysis pipeline — upload → Gemini → schema validation → persist (P0-2b).

Preserved working logic (PROVENANCE.md): the analysis prompt and JSON parsing
come from app.py `_vertex_analysis` with unchanged behaviour, plus the added
`durationSeconds` request (ARCHITECTURE.md §4.1). The SDK is `google-genai`
per D-11 (app.py's deprecated `vertexai.generative_models` is NOT reused).

`MediaAnalysis.from_dict` remains the single validation gate: invalid model
output is retried once with the error fed back, then rejected, never persisted.
The contradiction pass (P0-4a) is a second structured extraction over the
STORED analysis — no second video call (ARCHITECTURE §5.1 step 3).
"""

from __future__ import annotations

import json
import logging
import re
import struct
import time
import uuid
from pathlib import Path
from typing import Any

from api.config import Settings
from contextbridge_schema import MediaAnalysis
from contextbridge_store import update_analysis

logger = logging.getLogger(__name__)

MAX_UPLOAD_BYTES = 100 * 1024 * 1024  # CONTRACT: ≤ 100 MB (ARCHITECTURE §4.2)
ALLOWED_EXTENSIONS = {".mp4", ".mov", ".mpeg", ".mpg", ".webm", ".avi"}

# Preserved verbatim from app.py, plus durationSeconds (read before validation;
# MediaAnalysis.from_dict ignores it but Lesson needs it — no ffprobe).
ANALYSIS_PROMPT = """
Analyze this video for ContextBridge. Return JSON only.
Required keys:
summary, language, topics, events, transcript, durationSeconds.
Each event must contain id, startSeconds, endSeconds, title, description,
confidence, and evidence. Each evidence item must contain startSeconds,
endSeconds, and quote. Each transcript item must contain startSeconds,
endSeconds, and text. durationSeconds is the total video length in seconds.

Rules:
- Use seconds from the beginning of the video.
- Timestamps and durationSeconds are plain seconds (e.g. 45 means 45 seconds
  in, 90 means 1:30). Never minutes, never fractions of the video length.
- Keep events chronological and include only meaningful moments.
- Separate observable facts from interpretation.
- Do not invent speech, events, or timestamps.
- If speech is unclear, omit it rather than guessing.
- Confidence must be between 0 and 1.
"""

# P0-4a: structured extraction over the stored analysis, never the video.
CONTRADICTION_PROMPT = """
You are given a stored video analysis as JSON (summary, events, transcript).
Identify statements in the transcript that genuinely conflict with each other
about the same underlying claim. Return JSON only, with one key
"contradictions": a list of objects with keys id, claim, statementA,
statementB, note. Each statement is an object with keys text, startSeconds,
endSeconds, quote.

Rules:
- Use seconds from the beginning of the video, taken from the transcript.
- quote must be copied verbatim from the transcript text.
- claim names the shared topic; note explains the conflict in neutral
  phrasing — never pick a winner.
- Do not invent statements, speech, or timestamps.
- If there are no genuine conflicts, return {"contradictions": []}.

Analysis JSON:
"""


class PipelineError(RuntimeError):
    """Analysis failed in a way the user can retry as a new upload (→ 502)."""


def new_analysis_id() -> str:
    return f"an-{uuid.uuid4().hex[:12]}"


def envelope_duration(envelope: dict[str, Any]) -> float:
    """Model-reported durationSeconds, clamped from below by observed content.

    The model's duration estimate is unreliable (observed 0.563 for a 62 s
    clip), so the contract invariant — all timestamps ≤ durationSeconds — wins.
    """
    ends = [
        s.get("endSeconds")
        for s in envelope.get("transcript", [])
        if isinstance(s, dict)
    ]
    ends += [
        e.get("endSeconds") for e in envelope.get("events", []) if isinstance(e, dict)
    ]
    ends = [v for v in ends if isinstance(v, (int, float)) and not isinstance(v, bool)]
    observed = max(ends, default=0.0)
    duration = envelope.get("durationSeconds")
    if (
        not isinstance(duration, (int, float))
        or isinstance(duration, bool)
        or duration < observed
    ):
        return observed
    return float(duration)


def _mp4_duration_seconds(video_bytes: bytes) -> float | None:
    """Best-effort stdlib mvhd parse (no ffprobe dependency, ARCHITECTURE §4.1).

    Returns None for non-MP4 containers or unparseable files.
    """
    start = 0
    while True:
        i = video_bytes.find(b"mvhd", start)
        if i < 0:
            return None
        body = video_bytes[i + 4 : i + 4 + 32]
        if len(body) >= 20:
            try:
                if body[0] == 1:  # 64-bit creation/modification fields
                    timescale, units = struct.unpack(">II", body[20:28])
                else:
                    timescale, units = struct.unpack(">II", body[12:20])
                if 1 <= timescale <= 10_000_000:
                    seconds = units / timescale
                    if 0.1 <= seconds <= 6 * 3600:  # sanity window
                        return seconds
            except (struct.error, ZeroDivisionError):
                pass
        start = i + 4


def _rescale_timestamps(
    envelope: dict[str, Any], true_seconds: float
) -> dict[str, Any]:
    """Repair model timestamps emitted in the wrong unit.

    Observed live: gemini-2.5-flash returned timestamps as a fraction of the
    video (0.563 for a 57 s clip — i.e. percent/100). durationSeconds from the
    container is ground truth; when the model's duration is off by a known
    unit factor (minutes ×60 or percent ×100), rescale every timestamp.
    durationSeconds itself is always replaced with the container truth.
    """
    reported = envelope.get("durationSeconds")
    if (
        isinstance(reported, (int, float))
        and not isinstance(reported, bool)
        and reported > 0
    ):
        ratio = true_seconds / reported
        if abs(ratio - 1.0) > 0.15:
            factor = min((60.0, 100.0), key=lambda f: abs(ratio - f))
            if abs(ratio - factor) / factor <= 0.15:
                _scale_envelope(envelope, factor)
                logger.warning(
                    "rescaled model timestamps by x%s (unit slip detected)", factor
                )
    envelope["durationSeconds"] = true_seconds
    return envelope


def _scale_envelope(envelope: dict[str, Any], factor: float) -> None:
    def scale(value: Any) -> Any:
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return round(value * factor, 3)
        return value

    for event in envelope.get("events", []):
        event["startSeconds"] = scale(event.get("startSeconds"))
        event["endSeconds"] = scale(event.get("endSeconds"))
        for quote in event.get("evidence", []):
            quote["startSeconds"] = scale(quote.get("startSeconds"))
            quote["endSeconds"] = scale(quote.get("endSeconds"))
    for seg in envelope.get("transcript", []):
        seg["startSeconds"] = scale(seg.get("startSeconds"))
        seg["endSeconds"] = scale(seg.get("endSeconds"))


def sniff_video_mime(head: bytes, filename: str) -> str | None:
    """Server-side MIME sniff against the frontend allowlist (§4.2)."""
    if Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS:
        return None
    if len(head) >= 12 and head[4:8] == b"ftyp":
        return "video/quicktime" if head[8:12] == b"qt  " else "video/mp4"
    if head[:4] == b"\x1a\x45\xdf\xa3":
        return "video/webm"
    if len(head) >= 12 and head[:4] == b"RIFF" and head[8:12] == b"AVI ":
        return "video/x-msvideo"
    if len(head) >= 4 and head[:3] == b"\x00\x00\x01" and head[3] in (0xBA, 0xB3):
        return "video/mpeg"
    return None


# ---------------------------------------------------------------------------
# Gemini access (google-genai SDK — D-11) with the §6.5 retry/fallback ladder
# ---------------------------------------------------------------------------


def _clients(settings: Settings) -> list:
    """Vertex first; AI-Studio key as the provider fallback (ARCHITECTURE §10)."""
    from google import genai

    clients = []
    if settings.google_project_id:
        clients.append(
            genai.Client(
                vertexai=True,
                project=settings.google_project_id,
                location=settings.google_region,
            )
        )
    if settings.google_api_key:
        clients.append(genai.Client(api_key=settings.google_api_key))
    if not clients:
        raise PipelineError("No Gemini credentials configured.")
    return clients


def _generate_json(client, model_id: str, parts: list) -> dict[str, Any]:
    """One LLM round → parsed JSON object (fence-stripping preserved from app.py)."""
    from google.genai import types

    response = client.models.generate_content(
        model=model_id,
        contents=[types.Content(role="user", parts=parts)],
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    raw = (response.text or "").strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    if not raw:
        raise ValueError("Gemini returned an empty analysis response.")
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("Gemini response must be a JSON object")
    return parsed


def _call_with_ladder(settings: Settings, base_parts: list, validate):
    """Retry once with the validation error fed back, then provider fallback."""
    from google.genai import types

    last_error: Exception | None = None
    for client in _clients(settings):
        parts = list(base_parts)
        for attempt in range(2):
            try:
                return validate(_generate_json(client, settings.vertex_model_id, parts))
            except PipelineError:
                raise
            except Exception as exc:  # validation errors AND SDK/quota errors
                last_error = exc
                feedback = (
                    f"The previous response failed validation: {exc}. "
                    "Return corrected JSON only."
                )
                parts = list(base_parts) + [types.Part.from_text(text=feedback)]
                if attempt == 0:
                    time.sleep(2)  # §6.5: retry once with backoff
    raise PipelineError(f"Gemini pipeline failed: {last_error}")


def analyze_video(
    video_bytes: bytes, mime_type: str, settings: Settings
) -> dict[str, Any]:
    """Gemini multimodal analysis → validated MediaAnalysis envelope."""
    from google.genai import types

    base_parts = [
        types.Part.from_bytes(data=video_bytes, mime_type=mime_type),
        types.Part.from_text(text=ANALYSIS_PROMPT),
    ]

    def validate(parsed: dict[str, Any]) -> dict[str, Any]:
        duration = parsed.get("durationSeconds")
        analysis = MediaAnalysis.from_dict(parsed)  # the single validation gate
        envelope = analysis.to_dict()
        if isinstance(duration, (int, float)) and not isinstance(duration, bool):
            if duration > 0:
                envelope["durationSeconds"] = float(duration)
        return envelope

    return _call_with_ladder(settings, base_parts, validate)


def _validate_contradictions(
    parsed: dict[str, Any], duration: float | None
) -> list[dict[str, Any]]:
    raw = parsed.get("contradictions", [])
    if not isinstance(raw, list):
        raise ValueError("contradictions must be an array")
    limit = duration if duration else float("inf")
    pairs: list[dict[str, Any]] = []
    for index, item in enumerate(raw[:4]):
        if not isinstance(item, dict):
            raise ValueError(f"contradictions[{index}] must be an object")
        claim = item.get("claim")
        if not isinstance(claim, str) or not claim.strip():
            raise ValueError(f"contradictions[{index}].claim must be a string")
        pair: dict[str, Any] = {
            "id": str(item.get("id") or f"cx-{index + 1}"),
            "claim": claim.strip(),
        }
        for key in ("statementA", "statementB"):
            stmt = item.get(key)
            if not isinstance(stmt, dict):
                raise ValueError(f"contradictions[{index}].{key} must be an object")
            text = stmt.get("text")
            start, end = stmt.get("startSeconds"), stmt.get("endSeconds")
            if not isinstance(text, str) or not text.strip():
                raise ValueError(f"{key}.text must be a non-empty string")
            if not all(isinstance(v, (int, float)) and not isinstance(v, bool)
                       for v in (start, end)):
                raise ValueError(f"{key} timestamps must be numbers")
            if not (0 <= start <= end <= limit):
                raise ValueError(f"{key} timestamps out of range")
            clean: dict[str, Any] = {
                "text": text.strip(),
                "startSeconds": start,
                "endSeconds": end,
            }
            if isinstance(stmt.get("quote"), str) and stmt["quote"].strip():
                clean["quote"] = stmt["quote"].strip()
            pair[key] = clean
        if isinstance(item.get("note"), str) and item["note"].strip():
            pair["note"] = item["note"].strip()
        pairs.append(pair)
    return pairs


def extract_contradictions(
    envelope: dict[str, Any], settings: Settings
) -> list[dict[str, Any]]:
    """P0-4a: second structured pass over the STORED analysis (no video call).

    Non-fatal by design: any failure degrades to [] and the lesson simply omits
    the additive `contradictions` field (API.md §2 — optional, absent when none).
    """
    from google.genai import types

    duration = envelope_duration(envelope)
    payload = json.dumps(
        {
            "summary": envelope.get("summary"),
            "events": envelope.get("events"),
            "transcript": envelope.get("transcript"),
        },
        ensure_ascii=False,
    )
    base_parts = [types.Part.from_text(text=CONTRADICTION_PROMPT + payload)]
    try:
        return _call_with_ladder(
            settings,
            base_parts,
            lambda parsed: _validate_contradictions(parsed, duration),
        )
    except PipelineError:
        return []


# ---------------------------------------------------------------------------
# Video storage — GCS when configured, local disk otherwise (app.py logic)
# ---------------------------------------------------------------------------


def store_video(
    analysis_id: str,
    filename: str,
    video_bytes: bytes,
    mime_type: str,
    settings: Settings,
) -> str:
    """Persist the upload; returns a storage URI (gs://… or a local path)."""
    safe_filename = re.sub(r"[^A-Za-z0-9._-]+", "_", Path(filename).name)
    if settings.bucket:
        try:
            from google.cloud import storage

            client = storage.Client(project=settings.google_project_id)
            blob = client.bucket(settings.bucket).blob(
                f"analyses/{analysis_id}/{safe_filename}"
            )
            blob.upload_from_string(video_bytes, content_type=mime_type)
            return f"gs://{settings.bucket}/{blob.name}"
        except Exception:
            pass  # fall through to local disk so the demo path never dies
    local_dir = (
        Path(settings.db_path).resolve().parent / "uploaded_videos" / analysis_id
    )
    local_dir.mkdir(parents=True, exist_ok=True)
    target = local_dir / safe_filename
    target.write_bytes(video_bytes)
    return str(target)


def run_analysis(
    analysis_id: str,
    filename: str,
    video_bytes: bytes,
    mime_type: str,
    settings: Settings,
) -> dict[str, Any]:
    """Synchronous all-or-nothing pipeline (ARCHITECTURE §5.1, §15)."""
    update_analysis(analysis_id, status="processing")
    try:
        storage_uri = store_video(
            analysis_id, filename, video_bytes, mime_type, settings
        )
        envelope = analyze_video(video_bytes, mime_type, settings)
        true_seconds = _mp4_duration_seconds(video_bytes)
        if true_seconds is not None:
            envelope = _rescale_timestamps(envelope, true_seconds)
        contradictions = extract_contradictions(envelope, settings)
        if contradictions:
            envelope["contradictions"] = contradictions
        update_analysis(
            analysis_id, status="completed", result=envelope, storage_uri=storage_uri
        )
        return envelope
    except Exception as exc:
        update_analysis(analysis_id, status="failed", error=str(exc)[:500])
        if isinstance(exc, PipelineError):
            raise
        raise PipelineError(str(exc)) from exc
