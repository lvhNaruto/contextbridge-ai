# Requirements — ContextBridge (AI Builder Cup 2026)

**Owner doc:** `context/REQUIREMENTS.md`; **product spec** in `context/PRODUCT.md`; **selection rationale** in `context/IDEA_REVIEW.md`.
**Purpose:** prioritised, checkable requirements for the prototype submission (deadline 18 Oct 2026).
**How to read priorities:**

- **P0** — must ship. Without it the submission is incomplete or the demo fails. Do not start P1/P2 before P0 is green.
- **P1** — should ship. Raises judging scores (demo polish, video quality) but the product still works without it.
- **P2** — could ship / explicitly deferred. Only if every P0 and P1 above it is done. Most of these are deck scalability lines, not build commitments.

**MVP reality check (from `IDEA_REVIEW.md`):** ~15–18 effective build days for code plus deck, public repo, and a strictly-under-3-minute video. Single frontend (Streamlit recommended), pre-computed fixtures, ≤2-minute sample videos, live Q&A only on pre-analysed content.

**Hard gates that generate requirements:** working deployed prototype on Cloud Run/GCP/Firebase; public GitHub repo; public video link <3 min; PDF deck; all materials in English; one theme, one submission; fresh-project provenance (7 Sep–18 Oct window).

---

## P0 — Must ship (MVP)

### P0-1 Real grounded Q&A over video + transcript
**Requirement:** replace the mocked `_ask_gemini` → `_mock_answer` path in `app.py` with a real Gemini call. The agent must retrieve relevant context from the stored `MediaAnalysis` (timeline events + transcript segments) and return a structured answer with source timestamps.
**Acceptance:** for a pre-analysed sample video, a question whose answer exists in the video returns the answer plus at least one timestamp that lands on the correct segment; a question the video does not answer returns an explicit **"not found in this video"** rather than an invented answer.
**Judging link:** Technical Merit (40%) — this is the critical-path gap in the current repo.

### P0-2 Structured analysis pipeline (reuse, do not rebuild)
**Requirement:** video upload → Gemini on Vertex AI → schema-validated `MediaAnalysis` (summary, language, topics, transcript with timestamps, evidence timeline with `id`/`startSeconds`/`endSeconds`/`title`/`description`/`confidence`/`evidence`) → persisted via the existing `contextbridge_store.py`.
**Acceptance:** a new sample video can be analysed end to end and its analysis reloaded from the store; invalid model output is rejected by schema validation rather than persisted.
**Judging link:** Technical Merit — real pipeline, not a single endpoint.

### P0-3 Evidence timeline UI with click-to-jump
**Requirement:** display the evidence timeline (chapters, timestamps, confidence) and a searchable transcript; clicking an evidence card or transcript row seeks the video to that timestamp.
**Acceptance:** a judge can navigate the video by clicking events without watching it linearly; seeking lands within ~1s of the stated timestamp.
**Judging link:** Technical Merit + UX (10%).

### P0-4 Contradiction / claim surfacing (binding amendment 1)
**Requirement:** a second structured extraction pass over the **same** `MediaAnalysis` (no second video call) that flags claims and highlights conflicting pairs, each with its source timestamp.
**Acceptance:** at least one prepared sample video contains a genuine conflicting pair; the UI shows both statements with timestamps and clicking each jumps to the corresponding moment.
**Judging link:** Innovation (25%) — the required answer to "isn't this just a Gemini video demo?"

### P0-5 One accessible artifact from the same index (binding amendment 2)
**Requirement:** from the existing `MediaAnalysis`, generate on demand (user-chosen): a plain-language summary, a translation into one supported target language, or spoken audio narration via Text-to-Speech. One of the three is P0-minimum; all three share the same generation path.
**Acceptance:** one button produces the chosen output for the current video/answer, correctly derived from the analysis (not a fresh video call), with the source timestamp preserved on the artifact.
**Judging link:** Problem Alignment & Impact (25%) — the accessibility / JAPAC angle.

### P0-6 Pre-analysed fixtures + one live-upload path
**Requirement:** ship a small fixture set of **≤2-minute sample videos** (curated educational/public-service style clips), each with its `MediaAnalysis` already computed and stored. Live upload + analysis must also work, but the rehearsed demo runs on fixtures.
**Acceptance:** the full demo (timeline → Q&A → contradiction → artifact) completes using fixtures without waiting for video analysis; at least one fresh upload has been analysed live once before submission.
**Judging link:** demo reliability (UX + overall pass/fail — a long live analysis on stage is an avoidable risk).

### P0-7 Session state + persisted analyses
**Requirement:** a user can return to a previously analysed video and ask follow-up questions; analyses persist across restarts (store survives redeploy, or fixtures re-seed deterministically).
**Acceptance:** reload the app / redeploy → prior video and analysis still available; multi-turn follow-ups keep conversation context.
**Judging link:** Technical Merit — real state, not a one-shot script.

### P0-8 Evaluation set + measurable results
**Requirement:** an evaluation dataset of questions with known-answer timestamps over the sample videos, plus a script/report measuring: timestamp-retrieval accuracy, groundedness, unsupported-answer rate, processing time per video.
**Acceptance:** one command or notebook produces the four numbers; results go into the deck. Minimum viable: one fixture video with ~20 questions (scale in P1-1).
**Judging link:** Technical Merit (40%) — turns "it works" into evidence.

### P0-9 Deployed prototype on Google Cloud
**Requirement:** the app runs as a deployed service on **Cloud Run** (or Firebase frontend + Cloud Run backend), reachable by URL, using Gemini on Vertex AI. Deploy the thinnest skeleton in week 1, not at the end.
**Acceptance:** a judge can open the URL and complete the demo path end to end; no local-only step remains in the critical path.
**Judging link:** hard submission gate + Technical Merit.

### P0-10 Public repo + provenance audit + git hygiene
**Requirement:** `git init` immediately; audit every existing file's creation date against the 7 Sep–18 Oct eligibility window and document the audit; commit fresh work openly; final repo public on GitHub with an English README.
**Acceptance:** commit history exists and is in-window for all claimed work; audit note committed; repo public before submission.
**Judging link:** eligibility gate (fresh-project rule) — non-negotiable.

### P0-11 Submission package
**Requirement:** all four artifacts prepared and checked: deployed prototype URL, public GitHub repo, public video link **strictly under 3 minutes**, PDF deck. All in English.
**Acceptance:** dry-run checklist completed at least 2 days before 18 Oct; video re-recorded if it runs long; deck is a valid PDF.
**Judging link:** submission completeness — missing any one is disqualifying regardless of quality.

---

## P1 — Should ship (raises scores; cut only under time pressure)

### P1-1 Evaluation set at full size
Scale the P0-8 set toward the intended **20 short videos / 100 questions** with known-answer timestamps; report all four metrics in the deck.

### P1-2 All three accessible outputs + shareable evidence card
P0-5 requires one output path; P1-2 ships **all three** (plain-language summary, one translation, TTS audio narration) on a single toggle, plus a copyable **shareable evidence card** (answer + timestamp + quote) as the tangible artifact.

### P1-3 Voice question input
Ask by voice (speech-to-text or direct audio question to Gemini) so the demo has a multimodal beat beyond video-in.

### P1-4 Confidence / uncertainty UI
Surface per-answer confidence and an uncertainty note in the answer card (data already in the schema); make the "not found" path visually distinct from an answer.

### P1-5 Auth + per-user video scoping
Firebase Auth so each user sees only their own videos/analyses. Optional for a single-judge demo; strengthens the "real product" read.

### P1-6 Second frontend polish pass
Only if a dedicated frontend owner exists: bring the Next.js surface to feature parity. Otherwise keep Streamlit as the single surface and spend the time on P0/P1 above.

### P1-7 Demo rehearsal + fallback recording
Record a clean backup demo video early; rehearse the live path against the deployed URL on a stable network.

---

## P2 — Could ship / explicitly deferred (deck scalability lines only)

- **Multi-video projects / cross-video search** — one video at a time in the prototype.
- **Automatic external actions** (email, posting, invoking outside systems) — not in scope.
- **Enterprise permissions / multi-tenant access control / team roles.**
- **Rendering pipeline** (vertical clip re-encode/export, StorySplice full version) — the amendment deliberately excludes it.
- **"Reusable Multimodal Intelligence Platform" packaging** — deck scalability narrative, not a build target.
- **Every possible Google service** (Document AI, Speech-to-Text, BigQuery, …) — add a service only if it has a clear responsibility in the working product; do not sprinkle the stack for slide credit.
- **Post-hackathon verticals** (FixFlow, ShelfSense, TrustLens, RescueGrid, DecisionLoop-class extensions) — one theme, one submission; roadmap mention only.

---

## Out-of-scope guardrails (applies to every tier)

- **One frontend.** Streamlit is the committed surface unless P1-6 is triggered; never maintain two half-finished frontends.
- **One video at a time.** No playlists, no cross-video index, no platform language in the UI.
- **No invented answers.** The "not found in this video" path is a feature; it is never patched with a hallucination. Optional external context (if built at all) must be visibly separated and labelled.
- **No service sprinkling.** Every Google Cloud service in the stack must have a named responsibility in `PRODUCT.md` §7 or a P0/P1 item here.
- **No scope after freeze.** After the evaluation set (P0-8) and deployed skeleton (P0-9) are green, new ideas go to P2/backlog unless every P0 and P1 above them is complete.

---

## Risks that generate requirements (watch these first)

| Risk | Signal | Mitigation already encoded |
|---|---|---|
| Cloud/Gemini video quota unconfirmed (RESOURCES.md) | Analysis calls fail or are rate-limited past ~27 Sep | P0-6 fixtures keep the demo independent of live quota; fallback ladder in IDEA_REVIEW §7 |
| Mocked Q&A ships by accident | `_mock_answer` still reachable | P0-1 acceptance requires the real path + not-found behaviour |
| Fresh-project/provenance challenge | Files with pre-7 Sep origins claimed as new | P0-10 audit note + in-window commit history |
| Live demo fails on stage | Long analysis, network, or deploy issue | P0-6 fixtures, P0-9 URL, P1-7 backup recording |
| Two frontends dilute effort | `web/` and Streamlit both half-done | Out-of-scope guardrail: one frontend; P1-6 is conditional only |

---

## Definition of done (MVP)

The MVP is done when **all** of the following are true:

1. From the deployed URL, a new visitor can pick a fixture video, see its evidence timeline and transcript, ask a question, and receive a timestamped grounded answer — or an honest "not found" — without any local setup.
2. Clicking an answer's evidence jumps the video to the correct moment.
3. A prepared contradictory pair is surfaced with both timestamps and both are clickable.
4. One accessible artifact (summary / translation / TTS) generates from the stored analysis with its source timestamp preserved.
5. The evaluation script reports timestamp-retrieval accuracy, groundedness, unsupported-answer rate, and processing time, and those numbers appear in the deck.
6. The four submission artifacts (deployed URL, public repo with in-window history, <3-min video, English PDF deck) pass the P0-11 dry-run checklist.

Stretch goals (P1/P2) are only picked up after this list is fully green.


