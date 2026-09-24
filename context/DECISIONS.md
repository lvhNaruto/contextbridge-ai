# Decisions — ContextBridge

**Purpose:** append-only log of binding product/architecture decisions, newest last. Rules live in `context/CONSTRAINTS.md`; gap evidence in `context/FRONTEND_GAP_ANALYSIS.md`. The earlier reconciliations (surface switch to `web/`, mock-kill, client-owned conversations/library/settings, no-auth compensating controls) are recorded in `CONSTRAINTS.md` §2–§4 and incorporated here by reference.

Each frontend-extension entry answers the directive's seven checks: requirement · importance · placement · smallest additive form · clutter · nothing removed · recorded.

---

## D-01 · 2026-09-23 · Frontend rule amended: locked by design, extensible by gap analysis

- **Requirement/directive:** product-owner rule change — preserve `web/` as the visual/UX foundation, but allow the smallest natural UI addition for important missing P0/P1 capabilities identified from `REQUIREMENTS.md` / `PRODUCT.md` / `HACKATHON.md` / `RESOURCES.md`.
- **Why important:** the hard lock had forced two recorded compromises that put P0 acceptance at risk — contradiction findings hidden behind a guessed question (P0-4), and a transcript fetched on every load but never displayed (P0-3).
- **Where it fits:** governance only. `CONSTRAINTS.md` §1 reworded; `FRONTEND_GAP_ANALYSIS.md` created as the gate; every approved addition logged below.
- **Form:** process change; no UI.
- **Clutter:** n/a.
- **Nothing removed:** the design lock itself stands — redesign, restyling, rerouting, and removal of existing functionality remain forbidden.
- **Status:** binding.

## D-02 · 2026-09-23 · A1 — Contradiction findings card (P0)

- **Requirement:** P0-4; Definition-of-done #3 ("a prepared contradictory pair is *surfaced* with both timestamps and both are clickable"); PRODUCT.md §5.5 and §13 ("the contradiction panel showing *both* statements").
- **Why important:** contradiction surfacing is the Innovation (25%) answer to "isn't this just a Gemini video demo?" A feature a judge must guess to ask for is a feature that scores zero.
- **Where it fits:** workspace left column, between the video and the "Ask your teacher" card — same vertical rhythm as existing cards.
- **Smallest additive form:** one new `components/contradictions/contradiction-card.tsx`. Each pair shows the claim label and **both** statements, each with the existing `TimestampButton` wired to the existing `onJump` (seek + timeline highlight). Amber accent (caution semantics), hidden entirely when the analysis found no pairs. Data arrives as additive optional `Lesson.contradictions?` — no new endpoint; `demo-binary` seeds one genuine pair; mock mode mirrors it in `lib/mock-data.ts`.
- **Clutter:** zero when empty; at most one card otherwise. It never picks a winner (PRODUCT §13).
- **Nothing removed:** the Q&A agent still answers contradiction questions in chat.
- **Status:** approved — supersedes the Q&A-only reconciliation formerly in `CONSTRAINTS.md` §3.2. Queued for implementation.

## D-03 · 2026-09-23 · A2 — Searchable transcript panel (P0)

- **Requirement:** P0-3 ("a searchable transcript", rows seek the video); Definition-of-done #1.
- **Why important:** `Lesson.transcript` is fetched on every workspace load and rendered by zero components — a required, already-paid-for capability that is simply invisible.
- **Where it fits:** desktop right rail under "In this video"; mobile as a second collapsible drawer under the chapters drawer.
- **Smallest additive form:** `components/transcript/transcript-panel.tsx` — client-side search filter + timestamped rows calling the existing `onJump`. No endpoint or backend change.
- **Clutter:** collapsed drawer on mobile; one bounded section on desktop.
- **Nothing removed.**
- **Status:** approved, queued for implementation.

## D-04 · 2026-09-23 · A3 — Conversation history sent with each question (P0, no visual change)

- **Requirement:** P0-7 acceptance — "multi-turn follow-ups keep conversation context".
- **Why important:** follow-ups ("tell me more about that") are the most natural judge behaviour; history exists client-side but was never sent, making them unanswerable.
- **Where it fits:** request body only — `WorkspaceClient.ask` / `lib/api.ts`.
- **Smallest additive form:** optional `history: { role, text }[]` (last ≤ 6 messages) on `POST /analyses/:id/questions`; mock mode ignores it; the server uses it for that request only and stores nothing — the client-owned-conversations rule (`CONSTRAINTS.md` §3.4) stands.
- **Clutter:** none — no UI.
- **Nothing removed:** omitting `history` reproduces previous behaviour.
- **Status:** approved, queued for implementation.

## D-05 · 2026-09-23 · A4 — Chapter confidence badge (P1, justified)

- **Requirement:** P0-3 requirement text — the timeline display includes confidence.
- **Why important:** the schema's per-event `confidence` was being dropped at the `Chapter` boundary; showing it extends the trust design (PRODUCT §13) to the timeline at trivial cost.
- **Where it fits:** `ChapterList` rows beside the timestamp.
- **Smallest additive form:** optional `confidence?: number` on `Chapter`; existing `ConfidenceBadge` rendered when present.
- **Clutter:** one small badge per row, identical to answer cards.
- **Nothing removed.**
- **Status:** approved, queued for implementation.

## D-06 · 2026-09-23 · A5 — Real captions generated from the transcript (P1, justified)

- **Requirement:** directive example "accessibility controls"; P0-5 impact story; the product's one rule — the player's captions toggle and the `captionsPreferred` setting were inert, claiming an undelivered capability.
- **Why important:** makes two existing controls honest and demonstrates "one index, many outputs" (PRODUCT §9) with zero backend work — the transcript already ships with every lesson.
- **Where it fits:** `VideoPlayer` gains an optional `transcript` prop, fed by the workspace.
- **Smallest additive form:** client-side WebVTT blob from segments → one `<track kind="captions">`; the existing toggle switches track mode; default honours `captionsPreferred`.
- **Clutter:** none — native captions inside the existing player chrome.
- **Nothing removed.**
- **Status:** approved, queued for implementation.

## D-07 · 2026-09-23 · A6 — Copyable evidence card (P1, justified)

- **Requirement:** P1-2 — shareable evidence card (answer + timestamp + quote).
- **Why important:** the current copy button loses the timestamp and quote — the parts that make an answer *evidence*.
- **Where it fits:** the existing copy button on assistant messages.
- **Smallest additive form:** richer clipboard payload (answer + quote + `mm:ss` + lesson title); toast becomes "Evidence card copied". Same button, icon, position.
- **Clutter:** zero new UI.
- **Nothing removed.**
- **Status:** approved, queued for implementation.

## D-08 · 2026-09-23 · A7 — Honest analysis progress for live uploads (P1, justified)

- **Requirement:** directive example "important status information"; demo reliability (P0-9 live path, P1-7); honesty principle — a fixed ~5 s cosmetic cadence misrepresents a real ~30–90 s analysis.
- **Why important:** on the live-upload demo, six stages "completing" in 5 s followed by a minute of apparent freeze reads as a hang, on stage.
- **Where it fits:** the existing `AnalysisProgress` card.
- **Smallest additive form:** elapsed-time line ("Analyzing… 0:42 — usually under two minutes"); stage highlighting driven by elapsed time; final stage still waits for the real response.
- **Clutter:** one line of text.
- **Nothing removed:** same stages, card, and animation language.
- **Status:** approved, queued for implementation.

## D-09 · 2026-09-23 · P2 items deferred

The six P2 items in `FRONTEND_GAP_ANALYSIS.md` §5 (summary/topics header, `plainLanguage` wiring, AI-disclaimer microcopy, multi-fixture picker, `uncertaintyReason` note, REQUIREMENTS.md Streamlit wording) are **not built** under this amendment. Each requires a new directive or promotion to P1 with justification. The REQUIREMENTS.md wording item is a documentation reconciliation only, tracked in `CONSTRAINTS.md` §3.1.

## D-10 · 2026-09-23 · `docs/contextbridge-build-plan.txt` deleted (superseded draft)

- **What:** removed the 529-line early draft execution plan from `docs/`.
- **Why safe:** every section is superseded by a current owner doc — vision/why → `PRODUCT.md`; canonical data contract → `contextbridge_schema.py` + `API.md`; GCP architecture → `ARCHITECTURE.md`; MVP scope → `REQUIREMENTS.md`; demo story → `BUILD_PLAN.md` Phase 7; trust design → `PRODUCT.md` §13; build order → `BUILD_PLAN.md` + `TODO.md`; future verticals → P2 deck lines only.
- **Why delete rather than keep:** the draft actively contradicts current binding decisions — it brands the product a "Reusable Multimodal Intelligence Platform" (banned by `PRODUCT.md` §1/§11), assumes a different repo's provenance (red flag per `IDEA_REVIEW.md` §6), and puts deployment last (reversed by the deployed-skeleton-first guardrail). A stale doc that contradicts the spec is worse than no doc.
- **References fixed:** `PRODUCT.md` reference line now points to `ARCHITECTURE.md`/`BUILD_PLAN.md`; historical citations in `IDEA_REVIEW.md` §header/§6 and `IDEAS.md` annotated as removed.
- **Recovery:** OneDrive version history/recycle bin; deletion happened before `git init` (P0-10a), so no in-repo history exists.
- **Status:** done.

## D-11 · 2026-09-23 · Phase 0 outcomes — provenance fix, Vertex smoke PASS, SDK choice

- **Stale worktree pointer (P0-10a):** repo root held a `.git` pointer into `SchemaSentinel-Strands - Copy` worktrees — the exact provenance red flag predicted in `IDEA_REVIEW.md` §6. Deleted; fresh `git init -b main`; baseline commit `452d4dd`. Full inventory + creation-date evidence in `context/PROVENANCE.md` — all inherited files created 22–23 Sep 2026, inside the window.
- **Vertex smoke test (P0-10c): PASS.** `scripts/smoke_vertex.py` — text call 3.5 s; video understanding on a public ≤ 30 s-class sample (`gs://cloud-samples-data/generative-ai/video/pixel8.mp4`) 8.6 s with a correct grounded description. ADC credentials and quota confirmed working; the #1 architecture risk (Gemini-on-Vertex video quota) is de-risked.
- **SDK choice for `api/` (binding):** the smoke run surfaced that `vertexai.generative_models` (used by `app.py`) is a deprecated path. **New backend code uses the `google-genai` SDK instead** (already in `requirements.txt`, v2.24.0 installed). P0-2b reuses app.py's *prompt and parsing logic*, not its client. The preserved prototype stays untouched.
- **Repo identity:** local git author set from the authenticated GCP account (`mohitsinghgeek@gmail.com`); amend with `git config user.name/email` if a different display name should appear in the public history.
- **Phase 0 exit gate:** repo initialised with provenance note ✓ · `api/` skeleton runs (`/health` live, config shared with prototype) ✓ · credentials/quota verified ✓ · CI stub + `.gitignore` cover db/env/log/`__pycache__` ✓.
- **Status:** done — Phase 1 unblocked.

## D-12 · 2026-09-24 · Removed `streamlit` and `google-cloud-texttospeech` from `requirements.txt`

- **What:** deleted `streamlit>=1.57,<2` and `google-cloud-texttospeech>=2.16.0` from `requirements.txt`. `app.py` stays in the repo untouched as a reference file.
- **Why:** both packages are used exclusively by the superseded Streamlit prototype (`app.py`). The production stack is FastAPI (`api/`) + Next.js (`web/`) — neither imports Streamlit or TTS. Browser-side `speechSynthesis` handles read-aloud (`CONSTRAINTS.md` §5). Removing them saves ~200 MB on every `pip install`, Docker build, and CI run.
- **What stays:** `app.py` remains at root for provenance and as a reference for the Gemini analysis prompt (copied into `api/pipeline.py` in Phase 1, P0-2b). It will not run standalone — expected and intentional.
- **Risk:** none. No file in `api/` or `web/` imports either package. CI `python -m compileall api` still passes.
- **Status:** done.

## D-13 · 2026-09-24 · Phase 1 outcomes — demo-video fallback, timestamp unit repair, live validation

- **Demo-video fallback URL changed (binding):** the frontend mock's `gtv-videos-bucket` sample bucket went private (anonymous `storage.objects.get` now denied). `api/seed.py` falls back to the still-public `https://storage.googleapis.com/cloud-samples-data/generative-ai/video/pixel8.mp4` for `demo-binary`; dropping a real clip at `api/fixtures/demo-binary.mp4` still overrides it. The lesson payload keeps the canonical 888 s fixture data; the locked frontend mock is untouched (its mock-mode URL is frontend-owned).
- **Timestamp unit repair (binding):** live P0-2b validation caught `gemini-2.5-flash` emitting timestamps in the wrong unit (0.563 for a 57 s clip — percent/100). Two-layer fix in `api/pipeline.py`: (1) prompt hardened ("plain seconds, never minutes, never fractions"); (2) safety net — stdlib `mvhd` parse gives container ground truth (no ffprobe, per ARCHITECTURE §4.1), `durationSeconds` is always replaced with container truth, and when the model's duration is off by a known factor (×60 minutes / ×100 percent, ±15%) all event/evidence/transcript timestamps are rescaled. Serializer additionally clamps `durationSeconds` from below by observed content so the API.md §2 invariant (timestamps ≤ durationSeconds) can never be violated.
- **Sync upload latency:** real upload of a 5 MB / 57 s clip completes in ~30 s end-to-end (analysis + contradiction pass) — acceptable for the synchronous `POST /analyses` contract (API.md §3.1).
- **Validation:** 16/16 contract tests green (zero LLM calls); live smoke verified fixture journey (lesson + contradiction pair + 302 video redirect) and full upload journey (real chapters with second-based timestamps, 200/206 Range serving, contradiction field correctly omitted for a video without genuine conflicts).
- **Status:** done — Phase 1 complete; Phase 2 (agent loop, P0-1/P0-7/P0-5) unblocked.


## D-14 · 2026-09-23 · P0-1b — agent loop lands; `_mock_answer` deleted from the product path

- **`_mock_answer` deletion (binding interpretation):** the mocked `_ask_gemini → _mock_answer` path is deleted *from the product* — `POST /analyses/{id}/questions` runs only `api/agent.py`, and no file under `api/` contains a mock answer path (locked in by a regression test). `app.py` itself stays byte-untouched per CONSTRAINTS §3.1 ("file untouched, no longer the product"); editing it would break the binding reconciliation decision, and it is superseded code kept for provenance, not served by the API (ARCHITECTURE §4.1 reads "the path is deleted" together with "the file is untouched" — the deletion therefore applies to the serving path).
- **Exception taxonomy (agent reliability):** `tools.AnswerValidationExhausted(pipeline.PipelineError)` distinguishes a *judgement* failure — the model never produced evidence passing the draft gate even with the one §6.3 retry → agent answers with `declare_not_found` — from an *infra* failure (credentials/quota/SDK) → plain `PipelineError` → the endpoint's honest 502 (§6.5 last resort). Detection: the gate records whether validation ever fired; only then is ladder exhaustion reclassified. Existing `pytest.raises(PipelineError)` tests stay green (subclass).
- **Stored contradiction pass injected into the answer prompt** (`envelope["contradictions"]`, verified earlier against the same transcript) so API.md §3.4's contradiction-question behaviour has real timestamps/quotes to cite — no second video call, no new tool, no new endpoint.
- **Web `confidence` fixed at 0.72** mirrors the locked mock (`web/lib/demo-answers.ts`); `AssistantAnswer.confidence` is required in the locked TS types.
- **Deferred (next items):** the `history` request field stays out of the endpoint model (P0-7; pydantic ignores unknown keys, so early senders are safe) and the reserved `voice-question` alias remains unwired (API.md §4.1). Rate limiting (429) is likewise a later security item.
- **Validation:** `python -m compileall api tests` clean; full suite green (54 passed — 36 pre-existing + 18 new).
- **Status:** done.


## D-15 · 2026-09-24 · Phase 2 complete — P0-7 history passthrough, P0-5 accessible outputs, voice alias

- **P0-7 history passthrough (binding):** `QuestionRequest` in `api/main.py` gains optional `history: list[HistoryTurn] | None = None` (`role` in `{"user", "assistant"}`, `text` non-empty string). The endpoint slices the last ≤ 6 messages (`payload.history[-6:]`) and passes them to `agent.answer_question`, which injects them into `_ANSWER_PROMPT`. The server stores nothing in SQLite/db — statelessness per `CONSTRAINTS.md` §3.4 and `API.md` §3.4 is strictly preserved.
- **P0-5 accessible outputs (binding):** Verified that `explanationLevel` (`beginner`, `intermediate`, `expert`) and `answerLanguage` (`hi`, `en`, `auto`) condition the answer engine to output plain-language explanations or Hindi (Devanagari) translations while strictly enforcing `validate_answer_draft` invariants — exact start/end seconds within duration and verbatim quotes matched against the stored transcript. Audio narration is handled client-side via Web Speech API (`CONSTRAINTS.md` §3.3).
- **Reserved alias wired (`POST /analyses/{id}/voice-question`):** Implemented the multipart endpoint per `API.md` §4.1 (`transcript` string form field + optional `audio` blob upload). Answers through `agent.answer_question` with `isVoice: true`, ensuring the locked `web/lib/api.ts:askVoiceQuestion` function succeeds cleanly.
- **Validation:** `python -m compileall api tests` clean; full test suite green (64 passed — 54 pre-existing + 10 new).
- **Status:** done — Phase 2 complete; Phase 3 (Frontend additions: A1–A7) unblocked.

## D-16 · 2026-09-24 · Phase 3 complete — Frontend additions (A1–A7, TYPES, MOCK)

- **A1 Contradiction Card (P0-4 UI):** Implemented `web/components/contradictions/contradiction-card.tsx` rendering detected contradictions with side-by-side statements and dual interactive `TimestampButton`s seeking video playback. Preserved amber palette strictly for contradictions.
- **A2 Searchable Transcript Panel (P0-3):** Implemented `web/components/transcript/transcript-panel.tsx` with live search input, count summary, and interactive timestamped rows that seek the player. Embedded into right-rail (desktop) and collapsible drawer (mobile).
- **A4 Chapter Confidence Badge (P0-3):** Integrated `ConfidenceBadge` alongside timestamp and duration in `web/components/chapters/chapter-list.tsx`.
- **A3 Conversation History (P0-7):** Updated `askQuestion` in `web/lib/api.ts` to transmit the last ≤ 6 message turns (`HistoryTurn[]`), wired from `web/components/workspace/workspace-client.tsx`.
- **A5 Client-Side WebVTT Captions (D-06):** In `web/components/video/video-player.tsx`, generated in-memory WebVTT blob URLs from `transcript` segments, initialized toggle from `loadA11y().captionsPreferred`, and synchronized `<track>` showing/hidden modes.
- **A6 Copyable Evidence Card (D-07):** In `web/components/chat/assistant-message.tsx`, extended clipboard copy payload to include answer text, quote, timestamp (`mm:ss`), and lesson title. Triggered `toast.success("Evidence card copied")`.
- **A7 & MOCK Honest Analysis Progress (D-08):** In `web/components/upload/analysis-progress.tsx`, added elapsed-time ticker line (`Analyzing… m:ss — usually under two minutes`) and drove stage highlights by elapsed time, with optional `isReady` gate for live upload responses. Seeded demo data with contradiction pairs and chapter confidences.
- **Validation:** `npm run build` compiles with 0 errors/warnings; all 64 Python tests green (`python -m pytest`).
- **Status:** done — Phase 3 complete; Phase 4 (Deployment & Integration) unblocked.

## D-17 · 2026-09-24 · Phase 4 complete — Deployment & Cloud Run Integration (P0-9)

- **P0-9a Backend Cloud Run Deployment (`contextbridge-api`):** Deployed FastAPI container via Google Cloud Build to `us-central1` on project `quantum-device-401006` with startup fixture seeding. Public endpoint active at `https://contextbridge-api-c5ltxo3mkq-uc.a.run.app`. Verified `/health` returns 200 OK with `gemini-2.5-flash` active.
- **P0-9b Frontend Cloud Run Deployment (`contextbridge-web`):** Containerized Next.js 16 App Router as node server in `web/Dockerfile` with `NEXT_PUBLIC_API_BASE_URL=https://contextbridge-api-c5ltxo3mkq-uc.a.run.app` baked into build. Deployed to `us-central1` at `https://contextbridge-web-c5ltxo3mkq-uc.a.run.app`. CORS allowlist configured on backend.
- **P0-9c Deployed Smoke Test:** Scripted verification (`scripts/smoke_deployed.py`) confirmed end-to-end fixture journey: landing page 200 OK → demo lesson 200 OK → backend lesson retrieval (5 chapters with confidence, 1 contradiction pair) → live Gemini Q&A agent response with exact quote, timestamp (173.0s), and confidence (0.97) → Range-supporting 302 video redirect.
- **P0-9d Live Upload Verification:** Real video upload (`scripts/smoke_upload.py`, 4.72 MB clip) to `POST /analyses` completed in **24.5s** (within honest progress expectation). Created 6 chapters with confidence (0.97–0.99), 14 transcript segments, and answered subsequent question citing newly extracted timestamp `00:12`.
- **Status:** done — Phase 4 complete; Phase 5 (Testing & Evaluation Harness) unblocked.

## D-18 · 2026-09-24 · Phase 5 complete — Testing, DoD Evaluation Harness & Failure-Path Drills (P0-8, SWEEP, FAIL, REG)

- **P0-8 Evaluation Harness (`scripts/eval_harness.py`):** Executed 9-case evaluation benchmark against the live deployed Cloud Run API (`https://contextbridge-api-c5ltxo3mkq-uc.a.run.app`). Reported the 4 Definition of Done metrics:
  - **Unsupported-answer rate:** `0.0%` (target ≤ 5%, zero hallucinated moments on unanswerable questions)
  - **Timestamp retrieval accuracy:** `83.3%` (target ≥ 80% on in-video questions)
  - **Groundedness:** `88.9%` (verified against transcript and citation invariants)
  - **Average Q&A latency:** `2.53s` (well within the 25s agent budget)
  Benchmark results persisted to `context/eval_results.json`.
- **SWEEP Acceptance Sweep (`scripts/sweep_deployed.py`):** Executed end-to-end acceptance checks against live Cloud Run URLs (`contextbridge-web` and `contextbridge-api`), validating P0-1 through P0-9:
  - P0-9: Frontend and backend endpoints responsive with 200 OK.
  - P0-6: Deterministic startup fixture seeding of `demo-binary`.
  - P0-2 & P0-3: 5 chapters with confidence metrics (0.97–0.99) and 7 transcript segments.
  - P0-4: Surfaced genuine contradiction pair with dual clickable timestamps (210s & 615s).
  - P0-1: Grounded Q&A with exact quote (`"Binary language uses only two digits: zero and one."`) and timestamp (173.0s).
  - P0-7: Multi-turn conversation history follow-up with context continuity.
  - P0-5: Accessible plain-language explanation and Hindi translation (`answerLanguage: "hi"`).
  - P0-8: Metric evaluation artifact verified.
- **FAIL Nine Failure-Path Drills (`scripts/test_failure_paths.py`):** Implemented and verified all 9 ARCHITECTURE §15 failure scenarios:
  1. *Analysis LLM failure:* Status marked `failed`, isolated with 409 `analysis_failed`.
  2. *Q&A unanswerable vs outage:* Unanswerable yields honest 200 `unknown` (`notInVideo: true`, confidence 0.0); total outage yields 502 `answer_failed`.
  3. *Agent loop crash:* Caught by exception handler; returns structured 502 envelope.
  4. *Web search failure:* Degrades to `declare_not_found`; zero sources or evidence invented.
  5. *External API failure:* Seeded demo fixture serves without live API dependency.
  6. *Database failure:* Catch-all falls back to in-memory seed; demo lesson remains 200 OK.
  7. *Input validation:* 400 `missing_file`, 413 `file_too_large`, 422 `unsupported_video` / `invalid_question`, 404 `not_found`.
  8. *Timeout & iteration bound:* Strict attempt budget (max 2 attempts per ladder); no indefinite loops.
  9. *Partial execution isolation:* Incomplete analysis safely shielded (409 `analysis_incomplete`).
- **REG Regression Guard (`tests/test_regression.py`):**
  - Confirmed `_mock_answer` is completely absent from all serving code in `api/`.
  - Confirmed `MediaAnalysis.from_dict` rejects malformed payloads, invalid timestamps, and non-numeric confidence.
  - Confirmed Next.js mock mode toggle (`USE_MOCK = !API_BASE`) and mock data structures remain intact.
- **Validation:** All 76 Python tests pass (`python -m pytest`); Next.js production build clean with 0 errors/warnings (`npm run build`).
- **Status:** done — Phase 5 complete; Phase 7 (Submission & Dry Run) unblocked.

## D-19 · 2026-09-24 · User Feedback & UX Polish — Chapter Truncation, Playback Dropdown, Web Research Switch, Dynamic Questions

- **A4 / Chapter Layout & Truncation Fix (`web/components/chapters/chapter-list.tsx`):**
  - *Root Cause:* The chapter item row used a single horizontal flex line (`flex items-center gap-2`) containing timestamp (~45px), chapter title (`truncate`), and `ConfidenceBadge` (`ml-auto shrink-0`, ~120px) inside a ~190px sidebar. With 165px occupied, the title was squashed into a 15px box, truncating titles down to single letters: `00:00 H` (*"Humans and communication"*), `00:02 C` (*"Computers and machine language"*), `00:06 T.` (*"The question of how to represent words"*), `00:09 I..` (*"Intermediate representation: decimal digits"*), and `00:18 E` (*"Evolution to binary: 0 and 1"*).
  - *User Impact:* Seeing `00:02 C` led the user to reasonably conclude the application was hardcoded and restricted solely to the C programming language.
  - *Fix:* Restructured each chapter item into a 3-row vertical layout:
    - *Row 1:* Timestamp + `ConfidenceBadge` side-by-side (`justify-between`).
    - *Row 2:* Full chapter title across 100% width with wrapping (`break-words`, `text-sm font-medium text-slate-200`), completely eliminating character clipping.
    - *Row 3:* Chapter description (`text-xs text-slate-400 line-clamp-2`).
- **Playback Speed Dropdown Selector (`web/components/video/video-player.tsx`):**
  - *Root Cause:* The playback rate button operated as a cyclic single-direction toggle (`1x -> 1.25x -> 1.5x -> 1.75x -> 2x -> 0.5x -> 0.75x`), requiring up to 5 repetitive clicks to switch from 1x to 0.5x.
  - *Fix:* Replaced the cycle button with a Radix UI `DropdownMenu` offering direct single-click selection across 7 granular speed presets: `0.5x`, `0.75x`, `1x (Normal)`, `1.25x`, `1.5x`, `1.75x`, and `2x`. Added a checkmark indicator (`Check` icon) beside the active rate and updated the trigger label dynamically.
- **Web Research Toggle & Tooltip Event Fix (`web/components/settings/lesson-settings.tsx`):**
  - *Root Cause:* The "Research missing context" toggle was wrapped in an outer HTML `<label>` element around the Radix UI `<Switch>` (which renders a `<button role="switch">`). In HTML, clicking an interactive button nested inside a `<label>` causes the label to fire a synthetic click event on the control, resulting in an immediate double-toggle (ON then immediately OFF), freezing the switch. Redundant `<Tooltip>` wrappers on `DropdownMenuTrigger` elements also swallowed pointer events.
  - *Fix:* Removed the outer `<label>`, replaced with a dedicated accessible button switch (`role="switch"`, `aria-checked`), and eliminated tooltip wrappers around dropdown triggers to restore smooth, unhindered click interactions.
- **Dynamic Video-Specific Question Suggestions (`web/components/workspace/workspace-client.tsx`):**
  - *Root Cause:* Suggested question starter chips below the input box were hardcoded to `DEMO_SUGGESTED_QUESTIONS.slice(0, 3)` (*"What does binary language mean?"*, *"Why do computers use 0 and 1?"*), regardless of what video was being analyzed. Clicking them triggered binary questions even when analyzing unrelated custom videos.
  - *Fix:* Replaced the static array with dynamic question generation derived from the loaded lesson's actual `lesson.topics` and `lesson.chapters` (e.g. *"What does the video explain about [Topic]?"*, *"What is covered in [Chapter Title]?"*). Custom typed queries continue to route to the deployed Gemini 2.5 Flash agent (`POST /analyses/:id/questions`) returning timestamp-grounded answers.
- **Local Dev vs Live Cloud Run Synchronization:**
  - Configured `web/.env.local` with `NEXT_PUBLIC_API_BASE_URL=https://contextbridge-api-c5ltxo3mkq-uc.a.run.app` so local dev targets the live Cloud Run backend instead of fallback mock mode.
  - Built updated container `gcr.io/quantum-device-401006/contextbridge-web:latest` via Cloud Build and deployed revision `contextbridge-web-00003-xbl` to Cloud Run at `https://contextbridge-web-263542412452.us-central1.run.app`.
- **Validation:** Next.js production build clean with 0 errors/warnings (`npm run build` completed in 1110ms); all 76 Python test cases passing (`python -m pytest`).
- **Status:** done — fixes deployed live to Cloud Run and verified.

