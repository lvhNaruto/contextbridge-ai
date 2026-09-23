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


