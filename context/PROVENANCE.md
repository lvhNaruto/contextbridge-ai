# Provenance — ContextBridge (AI Builder Cup 2026)

**Rule:** fresh project built during the hackathon window **7 Sep – 18 Oct 2026** (`context/RULES.md`). This file records what existed before version control and when it was created, so the in-window origin of every inherited file is auditable. From the first commit onward, `git` history is the provenance record.

## Pre-VCS inventory (recorded 2026-09-23, before `git init`)

| File | Created (OneDrive FS) | Last modified | Origin |
|---|---|---|---|
| `app.py` | 2026-09-22 16:10 | 2026-09-23 02:20 | Streamlit prototype authored in-window this week; single-file analysis UI; Q&A was mock (`_mock_answer`); to be superseded by `api/` (ARCHITECTURE §16.2) |
| `contextbridge_schema.py` | 2026-09-22 15:09 | 2026-09-22 16:09 | Canonical `MediaAnalysis` contract + validation, authored in-window; imported by the prototype |
| `contextbridge_store.py` | 2026-09-22 16:09 | 2026-09-22 16:11 | SQLite persistence adapter, authored in-window; reused by the FastAPI backend |
| `contextbridge.db` | 2026-09-22 16:10 | 2026-09-23 02:38 | Local runtime artifact — **not committed** (`.gitignore`) |
| `requirements.txt` | 2026-09-22 15:09 | 2026-09-22 18:29 | Prototype deps, authored in-window |
| `.env.local` | 2026-09-22 15:33 | 2026-09-23 02:35 | Local config/secrets — **never committed** (`.gitignore`); keys documented in `.env.example` |
| `web/` | in-window (this week) | — | Next.js 16 + TS + Tailwind + shadcn/ui frontend; reviewed in `context/FRONTEND_GAP_ANALYSIS.md` §7 (score 2.9/5 vs spec) |
| `context/*.md` | 2026-09-23 | — | Documentation set produced in the selection/planning sessions (see DECISIONS.md D-01…D-10) |
| `docs/` (diagrams, screenshots, sources) | pre-existing | — | Reference material only; the superseded `docs/contextbridge-build-plan.txt` was removed 2026-09-23 (D-10) |

## Provenance red flag — found and fixed

- **Stale `.git` worktree pointer** at repo root pointed to `C:/.../SchemaSentinel-Strands - Copy/.git/worktrees/greeting-response-c2cebd58` — a *different project* (the red flag predicted in `context/IDEA_REVIEW.md` §6). It made `git status` fail with "not a git repository".
- **Action (2026-09-23):** pointer file deleted; no commits from that worktree ever contained this folder's files. Verified file creation dates (table above) are all inside the hackathon window.
- **Lesson for P0-10:** the fresh `git init` in this folder is the *first* genuine history of this project. Nothing from `SchemaSentinel-Strands` is inherited.

## Authorship

All code and docs in this repository were authored during the hackathon window by the project owner (GCP account on record) with AI-assistant tooling; architecture and scope decisions are logged in `context/DECISIONS.md`.
