"""Canonical structured outputs shared by ContextBridge workflows."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def _number(value: Any, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field_name} must be a number")
    return float(value)


def _text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True)
class EvidenceReference:
    start_seconds: float
    end_seconds: float
    quote: str = ""

    @classmethod
    def from_dict(cls, value: Any) -> "EvidenceReference":
        if not isinstance(value, dict):
            raise ValueError("evidence must be an object")
        start = _number(value.get("startSeconds"), "evidence.startSeconds")
        end = _number(value.get("endSeconds"), "evidence.endSeconds")
        if start < 0 or end < start:
            raise ValueError("evidence timestamps must be ordered and non-negative")
        quote = value.get("quote", "")
        if not isinstance(quote, str):
            raise ValueError("evidence.quote must be a string")
        return cls(start_seconds=start, end_seconds=end, quote=quote.strip())


@dataclass(frozen=True)
class MediaEvent:
    id: str
    start_seconds: float
    end_seconds: float
    title: str
    description: str
    confidence: float
    evidence: tuple[EvidenceReference, ...] = field(default_factory=tuple)

    @classmethod
    def from_dict(cls, value: Any, index: int) -> "MediaEvent":
        if not isinstance(value, dict):
            raise ValueError(f"events[{index}] must be an object")
        start = _number(value.get("startSeconds"), f"events[{index}].startSeconds")
        end = _number(value.get("endSeconds"), f"events[{index}].endSeconds")
        confidence = _number(value.get("confidence"), f"events[{index}].confidence")
        if start < 0 or end < start:
            raise ValueError(f"events[{index}] timestamps are invalid")
        if not 0 <= confidence <= 1:
            raise ValueError(f"events[{index}].confidence must be between 0 and 1")
        raw_evidence = value.get("evidence", [])
        if not isinstance(raw_evidence, list):
            raise ValueError(f"events[{index}].evidence must be an array")
        return cls(
            id=_text(value.get("id"), f"events[{index}].id"),
            start_seconds=start,
            end_seconds=end,
            title=_text(value.get("title"), f"events[{index}].title"),
            description=_text(value.get("description"), f"events[{index}].description"),
            confidence=confidence,
            evidence=tuple(
                EvidenceReference.from_dict(item) for item in raw_evidence
            ),
        )


@dataclass(frozen=True)
class MediaAnalysis:
    summary: str
    language: str
    events: tuple[MediaEvent, ...]
    transcript: tuple[dict[str, Any], ...]
    topics: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary,
            "language": self.language,
            "topics": list(self.topics),
            "events": [
                {
                    "id": event.id,
                    "startSeconds": event.start_seconds,
                    "endSeconds": event.end_seconds,
                    "title": event.title,
                    "description": event.description,
                    "confidence": event.confidence,
                    "evidence": [
                        {
                            "startSeconds": evidence.start_seconds,
                            "endSeconds": evidence.end_seconds,
                            "quote": evidence.quote,
                        }
                        for evidence in event.evidence
                    ],
                }
                for event in self.events
            ],
            "transcript": list(self.transcript),
        }

    @classmethod
    def from_dict(cls, value: Any) -> "MediaAnalysis":
        if not isinstance(value, dict):
            raise ValueError("Gemini response must be a JSON object")
        raw_events = value.get("events", [])
        raw_transcript = value.get("transcript", [])
        raw_topics = value.get("topics", [])
        if not isinstance(raw_events, list):
            raise ValueError("events must be an array")
        if not isinstance(raw_transcript, list):
            raise ValueError("transcript must be an array")
        if not isinstance(raw_topics, list) or not all(
            isinstance(topic, str) and topic.strip() for topic in raw_topics
        ):
            raise ValueError("topics must be an array of non-empty strings")
        transcript: list[dict[str, Any]] = []
        for index, segment in enumerate(raw_transcript):
            if not isinstance(segment, dict):
                raise ValueError(f"transcript[{index}] must be an object")
            start = _number(
                segment.get("startSeconds"), f"transcript[{index}].startSeconds"
            )
            end = _number(
                segment.get("endSeconds"), f"transcript[{index}].endSeconds"
            )
            if start < 0 or end < start:
                raise ValueError(f"transcript[{index}] timestamps are invalid")
            transcript.append(
                {
                    "startSeconds": start,
                    "endSeconds": end,
                    "text": _text(segment.get("text"), f"transcript[{index}].text"),
                }
            )
        return cls(
            summary=_text(value.get("summary"), "summary"),
            language=_text(value.get("language"), "language"),
            events=tuple(
                MediaEvent.from_dict(item, index)
                for index, item in enumerate(raw_events)
            ),
            transcript=tuple(transcript),
            topics=tuple(topic.strip() for topic in raw_topics),
        )
