# Build Plan — ContextBridge (AI Builder Cup 2026)

**Sources:** `context/REQUIREMENTS.md` (priorities P0/P1/P2, acceptance criteria, DoD) · `context/PRODUCT.md` (solution, guardrail, judging links) · `context/ARCHITECTURE.md` (two-service design, pipeline §5, agent §6, deployment §16) · `context/API.md` (contract) · `context/CONSTRAINTS.md` (locked-but-extensible frontend) · `context/FRONTEND_GAP_ANALYSIS.md` + `DECISIONS.md` (approved additions A1–A7).
**Deadline:** 18 Oct 2026. **Sequencing rule:** P0 first, always — no P1 task starts until every P0 in the phases above it is green (`REQUIREMENTS.md` line 7). P2 is deck narrative only.
**Tracking:** task checkboxes live in `context/TODO.md`; binding scope decisions in `context/DECISIONS.md`.

---

## Phase overview

| # | Phase | Purpose | Requirements | Exit gate |
|---|---|---|---|---|
| 0 | **Foundation** | Repo, provenance, quota, structure | P0-10 | In-window commit history; Gemini video call confirmed |
| 1 | **Core feature** | Real analysis pipeline + fixtures (demo safety net) | P0-2, P0-4(backend), P0-6 | New video analysed end to end, reloaded from store; `demo-binary` served with contradiction pair |
| 2 | **Agent workflow** | Grounded Q&A agent + honest not-found + artifacts | P0-1, P0-7, P0-5 | Real timestamped answers; "not found" works; follow-ups resolve; one artifact generates |
| 3 | **Frontend** | Approved additions A1–A7 in preserved `web/` | P0-3, P0-4(UI) | All additions live against mock data; nothing existing changed |
| 4 | **Integration** | Wire frontend to backend, deploy skeleton | P0-9 | Deployed URL serves the full real flow on a fixture |
| 5 | **Testing** | Eval harness + failure paths + acceptance sweeps | P0-8, all P0 acceptance | Eval numbers exist; all P0 criteria pass on the deployed URL |
| 6 | **Polish** | P1 upgrades (only after Phase 5 green) | P1-1…P1-5, P1-7 | P1 items pass without regressing any P0 |
| 7 | **Demo** | Video, deck, submission dry run | P0-11, P1-7 | Four artifacts pass the dry run ≥ 2 days before deadline |

**MVP definition of done** (`REQUIREMENTS.md` §DoD) is reached at the end of **Phase 5**. Phases 6–7 harden the submission.

---

## Phase 0 — Foundation (P0-10)

**Goal:** a buildable, deployable skeleton with honest provenance.

1. **P0-10a · `git init` + provenance.** Fresh repo, first commit in-window (7 Sep–18 Oct). Pre-existing logic (`app.py`, `contextbridge_schema.py`, `contextbridge_store.py`) committed with a README provenance note. *Acceptance: no pre-7 Sep file claimed as new; in-window history from commit 1.*
2. **P0-10b · Project structure.** Create `api/` (FastAPI) beside the preserved `web/`; reusable core imported, not rewritten (ARCHITECTURE §4). `requirements.txt`, `.env.example`, `Dockerfile` stub.
3. **P0-10c · Quota + credentials smoke test.** One real Gemini-on-Vertex call on a ≤ 30 s clip — de-risks the RESOURCES.md quota risk *first*; if it fails, escalate per the IDEA_REVIEW §7 fallback ladder. Record result in DECISIONS.
4. **P0-10d · CI + hygiene.** `.github/workflows` lint/test stub; `.gitignore` covers `contextbridge.db`, `.env.local`, `server.log`, `__pycache__`.

**Exit gate:** in-window `git log`; a Gemini video-analysis call succeeds from a clean checkout using only documented env vars.

---

## Phase 1 — Core feature: analysis pipeline (P0-2, P0-4 backend, P0-6)

**Goal:** the deterministic pipeline (ARCHITECTURE §5.1) works for real, and the demo never depends on live quota.

1. **P0-2a · FastAPI skeleton.** `POST /analyses` (multipart, `demoKey`), `GET /analyses/:id`, `GET /analyses/:id/video` (Range streaming), error envelope `{error:{code,message}}`, CORS allowlist (API.md §1, §3.1–3.3).
2. **P0-2b · Gemini analysis call.** Reuse the existing prompt from `app.py`; validate with `contextbridge_schema.py`; persist via `contextbridge_store.py`; GCS upload for the video. *Acceptance: new sample video analysed end to end and reloaded from the store; invalid model output rejected by schema validation, never persisted.*
3. **P0-2c · Serialisation mapping.** `MediaAnalysis` → `Lesson` (events → chapters; ✳ `confidence` rides along, API.md §2).
4. **P0-4a · Contradiction pass.** Second structured extraction over the **stored** `MediaAnalysis` (no second video call, ARCHITECTURE §5.1 step 3); pairs stored and served as ✳ `Lesson.contradictions`. *Backend acceptance: fixture yields ≥ 1 genuine pair with both quotes (fuzzy-)matching the stored transcript.*
5. **P0-6 · Fixture set.** Pre-analysed ≤ 2-min videos seeded at startup, incl. **`demo-binary` with its real contradiction pair**; fixtures work with zero LLM calls (cold-start mitigation, ARCHITECTURE §16.4).

**Exit gate:** against the local API — upload a fixture video → `GET /analyses/:id` returns a schema-valid `Lesson` with chapters (+confidence), transcript, contradiction pair; video streams with seeking.

---

## Phase 2 — Agent workflow (P0-1, P0-7, P0-5)

**Goal:** the one agent (ARCHITECTURE §6–7) replaces `_mock_answer` — the critical-path gap (P0-1).

1. **P0-1a · Tools.** `retrieve_video_context` (timestamped slices from the stored analysis), `gemini_answer` (grounded generation), `gemini_web_research` (Search grounding — only when `researchMissingContext=true`, separately labelled per CONSTRAINTS §3.3).
2. **P0-1b · Agent loop.** Observe → reason → select tool → verify (timestamps within duration; quote matches transcript) → reply, mapped onto `ChatMessage` (`evidence`, `confidence`, `uncertaintyReason`, `usedResearch`, `plainLanguage`). **`_mock_answer` is deleted, not bypassed** (REQUIREMENTS risk table, line 128).
3. **P0-1c · Honest not-found.** Unanswerable questions return explicit "not found in this video" (`answerFound=false`) — never patched with invention (PRODUCT.md §13).
4. **P0-7 · Follow-ups.** Accept ✳ `history` (≤ 6 messages) in `POST /questions`; used per-request only, never stored (API.md §3.4, CONSTRAINTS §3.4).
5. **P0-5 · Accessible artifact.** On-demand generation from the stored index (plain-language summary / translation / TTS-ready text) with source timestamps preserved — "one index, many outputs".

**Exit gate (P0-1 acceptance verbatim):** on a fixture, an in-video question returns an answer + ≥ 1 timestamp landing on the correct segment; an unanswerable question returns honest "not found"; a contradiction question cites both stored statements; a follow-up ("tell me more about that") resolves via `history`.

---

## Phase 3 — Frontend: approved additions (P0-3, P0-4 UI · A1–A7)

**Goal:** implement the gated additions in the preserved `web/` — additive only, mock mode keeps working (CONSTRAINTS §1, FGA §4/§6). No other frontend change is permitted.

1. **A1 · Contradiction card** (P0-4 UI). `components/contradictions/contradiction-card.tsx`; both timestamps seek via existing `onJump`; seeded in `mock-data.ts`/`demo-answers.ts`. *Acceptance = P0-4 UI half: both statements shown, both buttons seek correctly.*
2. **A2 · Transcript panel** (P0-3). `components/transcript/transcript-panel.tsx`, searchable, rows seek.
3. **A4 · Chapter confidence badge** (P0-3). ✳ `Chapter.confidence` + existing `ConfidenceBadge`.
4. **A3 · History passthrough** (P0-7, no visual change). `lib/api.ts` sends the last ≤ 6 messages.
5. **A5 · Real captions.** Client-side WebVTT from `lesson.transcript`; the existing toggle controls it; honours `captionsPreferred`.
6. **A6 · Copyable evidence card** (P1-2 — pulled forward, same component surface as A1/A3). Clipboard = answer + quote + mm:ss + title.
7. **A7 · Honest progress.** Elapsed-time line in `AnalysisProgress`.

**Exit gate:** with mock data, a judge can click chapters / transcript rows / contradiction timestamps and land within ~1 s (P0-3/P0-4 acceptance); `npm run build` clean; zero diffs outside the approved file list in FGA §4.

---

## Phase 4 — Integration (P0-9)

**Goal:** one environment variable flips the frontend from mock to the real backend; the skeleton deploys early.

1. **P0-9a · Deploy skeleton now.** FastAPI to Cloud Run per ARCHITECTURE §16 (env vars §16.3, startup fixture seeding). *Deployed-skeleton-first is a REQUIREMENTS freeze guardrail — do it before features are finished.*
2. **P0-9b · Frontend deploy + wiring.** Next.js node server on Cloud Run (§16.2 — no static export, no frontend config edits); set `NEXT_PUBLIC_API_BASE_URL`; update the CORS allowlist.
3. **P0-9c · End-to-end smoke.** Fixture journey on the deployed URL: open `demo-binary` → chapters → ask → timestamped answer → click evidence → video seeks. Mock mode still works with the env var unset.
4. **P0-9d · Live-upload path check.** One real upload through the deployed stack (with A7's honest progress); confirm the ~30–90 s cadence reads acceptably on stage.

**Exit gate:** deployed URL passes P0-9 acceptance — a fresh visitor completes the fixture journey with no local setup; mock and real modes both work.

---

## Phase 5 — Testing (P0-8 + all P0 acceptance)

**Goal:** measured quality, not vibes — the numbers the deck cites come from here.

1. **P0-8 · Evaluation harness.** Scripted set: fixtures × questions (in-video, follow-up, contradiction, unanswerable). Reports the four DoD metrics: timestamp-retrieval accuracy, groundedness, unsupported-answer rate, processing time per video.
2. **Acceptance sweep.** Every P0 acceptance criterion (P0-1…P0-9) executed against the **deployed** URL and checked off in TODO.md.
3. **Failure-path drills.** ARCHITECTURE §15's nine cases (invalid file, oversized video, model garbage, Gemini down → fallback, 404s, research-off behaviour) each verified to land on the honest locked-UI outcome.
4. **Regression guard.** Schema validation rejects malformed analyses; `_mock_answer` confirmed absent; mock mode unaffected by every change.

**Exit gate:** eval numbers recorded (deck inputs); all P0 acceptance criteria green on the deployed URL = **MVP done** per REQUIREMENTS §DoD items 1–5.

---

## Phase 6 — Polish (P1 — only after Phase 5 is green)

1. **P1-1 · Scale the eval set** to 20 videos / 100 questions; refine targets from the first fixture run.
2. **P1-2 · Evidence card sharing polish** — already built as A6; here: verify rendering across answer types.
3. **P1-3 · Mobile/responsive validation** of the workspace incl. A1/A2 panels.
4. **P1-4 · Shareable links** (state-encoded lesson links) if achievable without new endpoints.
5. **P1-5 · Auth scoping note** for the deck (design only — no build; PRODUCT.md §11).
6. **P1-7 · Backup demo recording** — clean run recorded early; live path rehearsed on a stable network.

**Exit gate:** each adopted P1 item passes acceptance with zero P0 regressions; anything shaky is cut, not patched.

---

## Phase 7 — Demo & submission (P0-11)

**Goal:** the four artifacts, dry-run tested, with buffer before 18 Oct.

1. **Demo video (< 3 min, strict).** Script: problem → fixture open → timeline/transcript/contradiction clicks → grounded answer → evidence seek → honest not-found → accessible artifact → eval numbers. PRODUCT.md §12 success criteria are the storyboard.
2. **PDF deck (English).** One-sentence-per-component architecture (ARCHITECTURE §17), P0-8/P1-1 metrics, P1-5 auth scoping, P2 items as scalability narrative only.
3. **P0-11 · Dry-run checklist ≥ 2 days early.** Deployed URL live · public repo with in-window history · video < 3:00 and public · valid English PDF · one theme, one submission.
4. **Buffer.** Final days reserved for dry-run findings only — no new features (REQUIREMENTS freeze guardrail).

**Exit gate:** all four artifacts pass the dry run; MVP DoD item 6 checked.

---

## Requirement → phase map

| Req | Phase | Req | Phase | Req | Phase |
|---|---|---|---|---|---|
| P0-1 | 2 | P0-7 | 2 + 3(A3) | P1-2 | 3(A6) + 6 |
| P0-2 | 1 | P0-8 | 5 | P1-3 | 6 |
| P0-3 | 3 (A2, A4) | P0-9 | 4 | P1-4 | 6 |
| P0-4 | 1(backend) + 3(A1) | P0-10 | 0 | P1-5 | 6 |
| P0-5 | 2 | P0-11 | 7 | P1-7 | 6 + 7 |
| P0-6 | 1 | P1-1 | 6 | P2-* | deferred (D-09) |

**Critical path:** P0-10 → P0-2 → P0-6 → P0-1 → {P0-4, P0-5, P0-7} → A1–A7 → P0-9 → P0-8 → P0-11. P0-9's skeleton deploy starts in parallel with Phase 2.

---

## The Compass Era — Practical Sweet Spot Execution Plan (Winning Path)

**Strategy:** Zero compromises on code quality, zero dropped features. Execute strictly task-by-task, maintaining all 78 green tests and deployable revisions at every checkpoint.

### 🔒 Standing Rules for Every Task
1. **The gate is sacred:** `quote_matches_transcript`, timestamp-range validation, and `MediaAnalysis.from_dict` must never be weakened — only extended.
2. **Governance first:** Every UI addition requires a `DECISIONS.md` entry (D-XX) answering the seven checks before code is touched.
3. **Continuous test verification:** All 78 tests must pass before and after every backend change. `npm run build` must succeed before every frontend commit.
4. **Deployable at all times:** Every milestone concludes with a deployed Cloud Run revision and a `sweep_deployed.py` pass.
5. **Contract consistency:** camelCase on the wire; snake_case only inside internal Python logic.

---

### Week 1 — "Trust Visible" (The Moat Becomes Obvious in 10 Seconds)
**Goal:** Anyone looking at the screen for 10 seconds immediately understands the proof system.

| # | Task | Scope & Implementation | Done When |
|---|---|---|---|
| **1.1** | Decision records | Formally document D-23…D-28 in `context/DECISIONS.md` answering the 7 checks. | Entries merged and referenced. |
| **1.2** | `EvidenceBadge` polish | Update `web/components/evidence/evidence-badge.tsx` with 3 explicit states: `✅ Verified from this video · 96%` (emerald), `🌐 Beyond this video` (sky), `🤷 Not covered` (muted). | All 3 states render cleanly in assistant answers. |
| **1.3** | `TranscriptSync` wiring | Enhance `web/components/transcript/transcript-panel.tsx` so clicking evidence or seeking auto-scrolls the active segment into view (`scrollIntoView({ behavior: 'smooth', block: 'nearest' })`). | Clicking evidence seeks video AND scrolls transcript to the exact row. |
| **1.4** | Structured agent-run logging | Add structured JSON logging per agent query in `api/agent.py` & `api/main.py`: `branch, verified, retries, latency_ms, cost_estimate`, plus a `/healthz` metrics counter. | Logs visible in Cloud Run console; `/healthz` shows query breakdown. |
| **1.5** | Deploy Checkpoint #1 | Deploy backend and frontend revisions to Cloud Run; execute `python scripts/sweep_deployed.py`. | Both services live, healthy, and verified. |

---

### Week 2 — "The Compass" (Self-Learning Becomes Visible)
**Goal:** The product actively guides curiosity from the video's own concepts — establishing the "Compass, Not a Tutor" identity.

| # | Task | Scope & Implementation | Done When |
|---|---|---|---|
| **2.1** | Backend `suggestions` field | In `api/agent.py`, derive 2–3 next-question exploration anchors from stored chapters and topics without adding LLM round overhead; return in `ChatMessage.suggestions`. | `POST /questions` returns `suggestions: string[]`. |
| **2.2** | `ExploreSuggestions` component | Build `web/components/chat/explore-suggestions.tsx` rendering *"Explore from here →"* clickable chips under each answer. Clicking sends the question. | Chips render, click sends question, respects language. |
| **2.3** | `BoundaryCard` component | Frame external web research answers in a distinctive container: *"You've stepped beyond this video — external research, real sources"* + source chips. Video answers never get this frame. | Web answer visibly distinct from video answers. |
| **2.4** | Teaching moves (`clarify` + `simplify`) | Ambiguous input triggers a clarifying question; "I don't understand / samajh nahi aaya" triggers a beginner-friendly analogy. Keep within $\le 2$ round budget. | Unit tests pass for both moves; round budget invariant holds. |
| **2.5** | `eval_harness v2` baseline | Expand `scripts/eval_harness.py` to 25 benchmark cases (in-video, out-of-video, Hindi, contradictions). Save scorecard to `context/eval_results.json`. | Baseline recorded; reports citation accuracy and latency. |
| **2.6** | Deploy Checkpoint #2 | Deploy updates to Cloud Run; run eval harness against deployed URL. | Live deployment passes full suite. |

---

### Week 3 — "Speak My Language" (Multilingual & Voice Loop)
**Goal:** Flawless bilingual voice exploration in Hindi and English.

| # | Task | Scope & Implementation | Done When |
|---|---|---|---|
| **3.1** | TTS answers (speak-aloud) | Upgrade `useSpeak` with language-matched voice selection (`hi-IN` / `en-US`), interruptible on mic tap, and audio playback toggle. | Hindi answers speak in authentic Hindi voice; barge-in cancels on mic tap. |
| **3.2** | Voice loop states | Show dynamic listening… / thinking… / speaking… visual avatar states during voice interactions. | Avatar states visible during live voice input. |
| **3.3** | Hinglish input hardening | Refine prompt instructions for code-mixed queries (Hindi + English) to answer naturally in the same mix. Add 3 Hinglish eval cases. | Hinglish eval cases pass language fidelity check. |
| **3.4** | Landing page rewrite | Update hero copy in `web/components/hero.tsx` to the vision line: *"Not a tutor. A compass for self-learners"*, with the 3 pillars. Zero CSS/layout breakage. | Landing page clearly conveys compass positioning. |
| **3.5** | Transcript i18n polish | Verify Hindi transcript search, font rendering (Noto Sans Devanagari fallback), and character matching. | Search in Hindi works seamlessly; clean typography. |
| **3.6** | Deploy Checkpoint #3 | Deploy to Cloud Run; run `sweep_deployed.py` and verify eval v2 delta $\ge$ baseline. | Live revision green with zero regressions. |

---

### Week 4 — "Demo Proof" (Rehearse, Harden, Freeze)
**Goal:** Bulletproof reliability, recorded backup, and judge-ready presentation.

| # | Task | Scope & Implementation | Done When |
|---|---|---|---|
| **4.1** | Bugfix buffer | Address any edge cases or UI inconsistencies. Strict rule: no new features, only fixes. | Zero open P0/P1 defects. |
| **4.2** | Quota-death & fallback drill | Simulate offline/quota outage in testing; verify that `demo-binary` fixture serves seamlessly via in-memory store. | Fixture demo operates independently of live API quota. |
| **4.3** | Recorded backup demo | Record a clean 90-second screen recording of the live deployed app following the demo script. | Offline MP4 artifact ready and verified. |
| **4.4** | Rehearse demo script 5× | Practice the 90-second live presentation until completely second-nature. | Demo runs smoothly within $\le 90$ seconds. |
| **4.5** | README & Deck (PDF) | Finalize GitHub README with architecture diagram, live links, and eval scorecard; produce 8-10 slide PDF deck citing metrics. | Submission-ready deck and public repo. |
| **4.6** | Final deploy freeze | Deploy final frozen revision $\ge 48$h before deadline. Run full test suite, sweep, and lock revision. | Final Cloud Run revision frozen and tagged. |

---

### The 90-Second Winning Demo Script

| Beat | Duration | Action | The Line You Say |
|---|---|---|---|
| **1 · Hook** | 10s | Landing page | *"Self-learners don't want a tutor. They want to explore — and know what to trust. This is a compass, anchored to the video you choose."* |
| **2 · Explore** | 20s | Ask a question in the demo lesson $\rightarrow$ answer with quote $\rightarrow$ click evidence button | *"Every answer is verified against this actual transcript — click the proof, and the video jumps to the exact second while the transcript syncs. Our AI structurally cannot invent a quote."* |
| **3 · Compass** | 15s | Click an *"Explore from here →"* chip | *"It guides exploration directly from the video's own concepts — not generic chatbot suggestions."* |
| **4 · Boundary** | 15s | Ask a question NOT in the video with web research enabled | *"When curiosity steps beyond the video, it says so clearly with a distinct Boundary Card and verified Google Search grounding. The boundary is a feature, not a failure."* |
| **5 · Language** | 15s | Voice question in Hindi $\rightarrow$ Hindi answer + 🔊 listen | *"Learners explore in the language they think in — full bidirectional voice in Hindi and English."* |
| **6 · Proof** | 15s | Show eval scorecard slide + decision log | *"We measure quality on every single deploy: 100% verified citations, 78 green tests, and an append-only decision record. This is reliable GenAI."* |

