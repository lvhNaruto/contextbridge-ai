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


