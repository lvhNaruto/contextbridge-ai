# TODO — ContextBridge (AI Builder Cup 2026)

**Plan:** `context/BUILD_PLAN.md` · **Priorities:** P0 must ship → P1 after all P0 green → P2 deferred (D-09) · **Deadline:** 18 Oct 2026.
**Legend:** `[ ]` open · `[x]` done · IDs map to `REQUIREMENTS.md`; A-IDs map to `FRONTEND_GAP_ANALYSIS.md`.

---

## ✅ Done (documentation phase)

- [x] FGA — `FRONTEND_GAP_ANALYSIS.md` complete (§1–7, 26-row matrix, A1–A7 approved)
- [x] D-01…D-09 — `DECISIONS.md` (rule amendment + A1–A7 + P2 deferrals)
- [x] CONTRACTS — `API.md`, `ARCHITECTURE.md`, `CONSTRAINTS.md` amended for ✳ additive fields
- [x] PLAN — `BUILD_PLAN.md` + `TODO.md` created

---

## P0 — Must ship (in build order)

### Phase 0 · Foundation
- [x] **P0-10a** `git init`, first in-window commit; provenance note for `app.py` / `contextbridge_schema.py` / `contextbridge_store.py`
- [x] **P0-10b** `api/` FastAPI structure beside preserved `web/`; `requirements.txt`, `.env.example`, `Dockerfile` stub
- [x] **P0-10c** Gemini-on-Vertex quota/credentials smoke test (≤ 30 s clip); record outcome in DECISIONS
- [x] **P0-10d** CI lint/test stub; `.gitignore` covers db/env/log/`__pycache__`

### Phase 1 · Core feature — analysis pipeline
- [x] **P0-2a** FastAPI skeleton: `POST /analyses` (multipart), `GET /analyses/:id`, `GET /analyses/:id/video` (Range), error envelope, CORS
- [x] **P0-2b** Real Gemini analysis call (reuse `app.py` prompt) → schema validation → `contextbridge_store.py` → GCS video
- [x] **P0-2c** `MediaAnalysis` → `Lesson` serialisation (events→chapters, ✳ `confidence` passthrough)
- [x] **P0-4a** Contradiction pass over stored analysis (no 2nd video call) → served as ✳ `Lesson.contradictions`
- [x] **P0-6** Fixture set seeded at startup incl. `demo-binary` with genuine contradiction pair (zero LLM calls)

### Phase 2 · Agent workflow
- [x] **P0-1a** Tools: `retrieve_video_context`, `gemini_answer`, `gemini_web_research` (gated on `researchMissingContext`)
- [x] **P0-1b** Agent loop observe→reason→select→verify→reply → `ChatMessage`; **`_mock_answer` deleted**
- [x] **P0-1c** Honest "not found in this video" path (`answerFound=false`), verified never invented
- [x] **P0-7** Accept ✳ `history` (≤ 6 msgs) in `POST /questions`; per-request only, nothing stored
- [x] **P0-5** Accessible artifact from stored index (plain-language / translation / TTS-ready) with source timestamps

### Phase 3 · Frontend additions (additive only, preserved design)
- [x] **A1** `components/contradictions/contradiction-card.tsx` — both timestamps seek (P0-4 UI)
- [x] **A2** `components/transcript/transcript-panel.tsx` — searchable, rows seek (P0-3)
- [x] **A4** ✳ `Chapter.confidence` badge via existing `ConfidenceBadge` (P0-3)
- [x] **A3** `lib/api.ts` sends last ≤ 6 messages as `history` (P0-7, no visual change)
- [x] **A5** Client-side WebVTT captions from `lesson.transcript`; toggle + `captionsPreferred` honoured
- [x] **A6** Copyable evidence card: answer + quote + mm:ss + title (P1-2, pulled forward)
- [x] **A7** Elapsed-time line in `AnalysisProgress`
- [x] **TYPES** ✳ optional fields in `web/types/index.ts` (`Lesson.contradictions?`, `Chapter.confidence?`, `ContradictionPair`)
- [x] **MOCK** Seed contradictions + confidence in `lib/mock-data.ts` / `demo-answers.ts`; `npm run build` clean

### Phase 4 · Integration
- [x] **P0-9a** FastAPI deployed to Cloud Run (env vars per ARCHITECTURE §16.3; startup seeding) — early, before features finish
- [x] **P0-9b** `web/` deployed as Next.js node server on Cloud Run; `NEXT_PUBLIC_API_BASE_URL` set; CORS updated
- [x] **P0-9c** Deployed smoke: fixture journey end to end (open → chapters → ask → answer → evidence seek)
- [x] **P0-9d** One real live upload through the deployed stack; progress cadence acceptable

### Phase 5 · Testing
- [x] **P0-8** Evaluation harness: fixtures × {in-video, follow-up, contradiction, unanswerable}; reports timestamp accuracy, groundedness, unsupported-answer rate, processing time
- [x] **SWEEP** All P0-1…P0-9 acceptance criteria executed on the deployed URL
- [x] **FAIL** ARCHITECTURE §15 nine failure-path drills verified
- [x] **REG** `_mock_answer` absent; schema rejects malformed output; mock mode unbroken

---

## 🧭 The Compass Era — Practical Sweet Spot Tasks (Winning Path)

### Week 1 — "Trust Visible" (The Moat Becomes Obvious in 10 Seconds)
- [x] **1.1** **Decision records first:** Write D-23…D-28 entries (`EvidenceBadge`, `ExploreSuggestions`, `BoundaryCard`, `VoiceLoop`, `TranscriptSync`, `Landing`) answering the 7 checks in `context/DECISIONS.md`.
- [x] **1.2** **`EvidenceBadge` visual trust upgrade:** Update `web/components/evidence/evidence-badge.tsx` with 3 explicit states: `Verified from this video · 96%` (emerald), `Beyond this video (web, clearly labeled)` (sky), ` Not covered (honest boundary)` (muted). Data already exists (`evidenceType`, `confidence`).
- [x] **1.3** **`TranscriptSync` wiring:** Evidence click $\rightarrow$ `onJump` seeks video and auto-scrolls the active segment row into view in `TranscriptPanel` (`scrollIntoView({ behavior: 'smooth', block: 'nearest' })`).
- [x] **1.4** **Structured agent-run logging:** Per question: branch, verified, retries, latency_ms, cost_estimate as JSON logs; keep tiny metrics counter in `/healthz` (questions answered by branch).
- [x] **1.5** **Deploy Checkpoint #1:** Deploy both services to Cloud Run; run `python scripts/sweep_deployed.py`; record revision.

### Week 2 — "The Compass" (Self-Learning Becomes Visible)
- [x] **2.1** **Backend: `suggestions` field:** Derive 2–3 next-explore questions from video's own content (topics/chapters) without adding LLM round overhead; return in `ChatMessage.suggestions`.
- [x] **2.2** **`ExploreSuggestions` component:** Create `web/components/chat/explore-suggestions.tsx` with *"Explore from here →"* clickable chips under each answer; clicking sends the question.
- [x] **2.3** **`BoundaryCard` component:** Web-research answers get distinct framed container: *"You've stepped beyond this video — external research, real sources"* + source chips. Video answers never get this frame.
- [x] **2.4** **Backend: `clarify` + `simplify` moves:** Ambiguous/short input triggers a clarifying question; "I don't understand / samajh nahi aaya" triggers beginner analogy mode. Kept within $\le 2$ LLM round budget.
- [x] **2.5** **`eval_harness v2` baseline:** Expand `scripts/eval_harness.py` to 25 benchmark cases (in-video, out-of-video, Hindi, contradictions); store scorecard in `context/eval_results.json`.
- [x] **2.6** **Deploy Checkpoint #2:** Deploy, sweep, record revision; run eval v2 against deployed Cloud Run.

### Week 3 — "Speak My Language" (Multilingual + Voice Loop)
- [x] **3.1** **TTS answers (speak-aloud):** Per-answer 🔊 Listen + auto-speak toggle. Language-matched voice selection (`hi-IN` / `en-US`), interruptible on mic tap.
- [x] **3.2** **Voice loop states:** Dynamic listening… / thinking… / speaking… avatar states during voice flow.
- [x] **3.3** **Hinglish input hardening:** Answer prompt rules for code-mixed queries $\rightarrow$ answer in same mix. Add 3 Hinglish eval cases to suite.
- [x] **3.4** **Landing page rewrite:** Additive copy change on hero (`components/hero.tsx`): vision line, the 3 pillars (Anchored / Proof / Boundary), one CTA. Layout untouched.
- [x] **3.5** **Transcript panel i18n polish:** Verify Hindi transcript search, font rendering (Noto Sans Devanagari fallback), and character matching.
- [x] **3.6** **Deploy Checkpoint #3:** Deploy, sweep, eval v2 delta vs week-2 baseline (no regressions).

### Week 4 — "Demo Proof" (Rehearse, Harden, Freeze)
- [x] **4.1** **Bugfix buffer:** Address any edge cases or UI inconsistencies. Strict rule: no new features, only fixes.
- [x] **4.2** **Quota-death & fallback drill:** Simulate offline/quota outage in testing; verify that `demo-binary` fixture serves seamlessly via in-memory store.
- [ ] **4.3** **Recorded backup demo:** Clean 90-second screen recording of live deployed app following demo script (<3 min public MP4).
- [ ] **4.4** **Demo script rehearsal:** Rehearse the 90-second live presentation 5× until seamless.
- [x] **4.5** **README + Pitch Deck:** Finalize README with architecture diagram and live links; produce 8-10 slide PDF deck citing metrics.
- [ ] **4.6** **Final deploy freeze:** Deploy final frozen revision $\ge 48$h before deadline. Run full test suite, sweep, and lock revision.

---

## 🏆 Definition of Done — Hackathon Win

- [x] 1. Deployed URL: visitor picks fixture → timeline + transcript → question → timestamped grounded answer or honest "not found", no local setup
- [x] 2. Evidence click seeks video to the correct moment (~1 s)
- [x] 3. Contradictory pair surfaced, both timestamps clickable
- [x] 4. One accessible artifact generates from the stored index, timestamps preserved
- [x] 5. Eval script reports baseline metrics; numbers in the deck
- [x] 6. Visual trust indicators live (`EvidenceBadge`, `BoundaryCard`, `TranscriptSync`)
- [x] 7. Guided exploration active (`ExploreSuggestions` derived from video)
- [x] 8. Full bilingual voice loop verified in Hindi and English
- [x] 9. Eval harness v2 reports $\ge 92\%$ correct branch and 100% verified citations on 25 cases
- [ ] 10. Four submission artifacts pass the P0-11 dry run (deployed URL, public repo, <3 min video, PDF deck)
