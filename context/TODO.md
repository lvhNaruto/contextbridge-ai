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

### Phase 7 · Submission (P0-11)
- [ ] **P0-11** Dry-run ≥ 2 days early: deployed URL · public repo (in-window history) · video < 3:00 public · English PDF deck
- [ ] **VIDEO** Demo video scripted + recorded (< 3 min strict)
- [ ] **DECK** PDF deck with P0-8 metrics, architecture one-liners, P1-5 auth scoping, P2 as scalability lines

---

## P1 — Should ship (start only when every P0 above is green)

- [ ] **P1-1** Scale eval set to 20 videos / 100 questions; targets refined from first fixture run
- [ ] **P1-2** Evidence-card rendering polish across answer types (core built as A6)
- [ ] **P1-3** Mobile/responsive validation of workspace incl. A1/A2 panels
- [ ] **P1-4** Shareable lesson links (only if no new endpoints needed)
- [ ] **P1-5** Auth scoping note for deck (design only — no build)
- [ ] **P1-7** Backup demo recording captured early; live path rehearsed on stable network

---

## P2 — Deferred (deck narrative only; needs a new directive to build — D-09)

- [ ] Multi-video projects / cross-video search
- [ ] Automatic external actions (email, posting, integrations)
- [ ] Enterprise permissions / multi-tenant / roles
- [ ] Clip rendering pipeline (vertical re-encode, StorySplice)
- [ ] FGA §5 frontend P2 set: summary/topics header · `plainLanguage` wiring · AI-disclaimer microcopy · multi-fixture picker · `uncertaintyReason` note · REQUIREMENTS.md Streamlit-wording reconciliation
- [ ] Roadmap verticals (FixFlow / ShelfSense / TrustLens / RescueGrid class)

---

## Definition of done — MVP (check all, then Phase 6 may start)

- [ ] 1. Deployed URL: visitor picks fixture → timeline + transcript → question → timestamped grounded answer or honest "not found", no local setup
- [ ] 2. Evidence click seeks video to the correct moment (~1 s)
- [ ] 3. Contradictory pair surfaced, both timestamps clickable
- [ ] 4. One accessible artifact generates from the stored index, timestamps preserved
- [ ] 5. Eval script reports the four metrics; numbers in the deck
- [ ] 6. Four submission artifacts pass the P0-11 dry run
