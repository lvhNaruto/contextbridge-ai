"""Small persistent store for ContextBridge analysis jobs and results."""

from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _db_path() -> Path:
    configured = os.getenv("CONTEXTBRIDGE_DB_PATH", "contextbridge.db")
    path = Path(configured)
    return path if path.is_absolute() else Path(__file__).resolve().parent / path


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(_db_path())
    connection.row_factory = sqlite3.Row
    return connection


def initialize() -> None:
    _db_path().parent.mkdir(parents=True, exist_ok=True)
    with _connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS analyses (
                analysis_id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                mime_type TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                storage_uri TEXT,
                result_json TEXT,
                error TEXT
            )
            """
        )


def create_analysis(analysis_id: str, filename: str, mime_type: str) -> None:
    now = datetime.now(timezone.utc).isoformat()
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO analyses
            (analysis_id, filename, mime_type, status, created_at, updated_at)
            VALUES (?, ?, ?, 'uploaded', ?, ?)
            """,
            (analysis_id, filename, mime_type, now, now),
        )


def update_analysis(
    analysis_id: str,
    *,
    status: str,
    result: dict[str, Any] | None = None,
    storage_uri: str | None = None,
    error: str | None = None,
) -> None:
    now = datetime.now(timezone.utc).isoformat()
    updates = ["status = ?", "updated_at = ?"]
    values: list[Any] = [status, now]
    if result is not None:
        updates.append("result_json = ?")
        values.append(json.dumps(result, ensure_ascii=False))
    if storage_uri is not None:
        updates.append("storage_uri = ?")
        values.append(storage_uri)
    if error is not None:
        updates.append("error = ?")
        values.append(error)
    values.append(analysis_id)
    with _connect() as connection:
        connection.execute(
            f"UPDATE analyses SET {', '.join(updates)} WHERE analysis_id = ?",
            values,
        )


def get_analysis(analysis_id: str) -> sqlite3.Row | None:
    with _connect() as connection:
        return connection.execute(
            "SELECT * FROM analyses WHERE analysis_id = ?", (analysis_id,)
        ).fetchone()


def list_analyses(limit: int = 20) -> list[sqlite3.Row]:
    with _connect() as connection:
        return list(
            connection.execute(
                """
                SELECT * FROM analyses
                ORDER BY updated_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        )
