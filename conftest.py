"""Pytest bootstrap — runs before any test module import.

Points the store at a throwaway database so contract tests never touch the
developer's real contextbridge.db, and puts the repo root on sys.path so
`api.*` / `contextbridge_*` import cleanly. load_dotenv (override=False) in
api/config.py respects the pre-set value.
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

_TEST_DIR = Path(tempfile.mkdtemp(prefix="contextbridge-test-"))
os.environ["CONTEXTBRIDGE_DB_PATH"] = str(_TEST_DIR / "test.db")
