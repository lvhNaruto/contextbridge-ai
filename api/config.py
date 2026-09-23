"""Environment configuration for the ContextBridge API.

Reads the same keys as the preserved Streamlit prototype (app.py) so both
runtimes share one .env.local. Never commit real values — see .env.example.
"""

from __future__ import annotations

import functools
import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv(".env.local")
load_dotenv()  # .env as fallback; real deployment uses platform env vars


@dataclass(frozen=True)
class Settings:
    google_project_id: str | None
    google_region: str
    vertex_model_id: str
    db_path: str
    bucket: str | None
    web_origin: str
    google_api_key: str | None  # AI-Studio fallback path only (ARCHITECTURE §10)

    @property
    def analysis_enabled(self) -> bool:
        """Real Gemini analysis requires a project; otherwise fixtures only."""
        return bool(self.google_project_id)


@functools.lru_cache(maxsize=1)  # parse env once; tests set env before first call
def get_settings() -> Settings:
    return Settings(
        google_project_id=os.getenv("GOOGLE_PROJECT_ID") or None,
        google_region=os.getenv("GOOGLE_REGION", "us-central1"),
        vertex_model_id=os.getenv("VERTEX_MODEL_ID", "gemini-2.5-flash"),
        db_path=os.getenv("CONTEXTBRIDGE_DB_PATH", "contextbridge.db"),
        bucket=os.getenv("CONTEXTBRIDGE_BUCKET") or None,
        web_origin=os.getenv("WEB_ORIGIN", "http://localhost:3000"),
        google_api_key=os.getenv("GOOGLE_API_KEY") or None,
    )
