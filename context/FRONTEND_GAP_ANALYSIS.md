# Frontend Gap Analysis — ContextBridge

**Owner doc:** `context/FRONTEND_GAP_ANALYSIS.md` · decisions `context/DECISIONS.md` · constraints `context/CONSTRAINTS.md` · API `context/API.md` · architecture `context/ARCHITECTURE.md`
**Date:** 2026-09-23 · **Trigger:** product-owner directive — *"PRESERVE THE EXISTING DESIGN + EXTEND IT WHEN IMPORTANT."*
**Governing rule:** the `web/` frontend is the **preserved visual & UX foundation** — never redesigned — but it is **not a hard feature ceiling**. When `HACKATHON.md` / `REQUIREMENTS.md` / `RESOURCES.md` / `PRODUCT.md` identify an important P0/P1 capability the UI lacks, the **smallest natural addition** that fits the existing design system is allowed — and, for P0 and justified P1 gaps, made automatically. Every addition is recorded in `DECISIONS.md`.

> FRONTEND DESIGN = PRESERVED · REQUIREMENTS = AUTHORITATIVE · MISSING IMPORTANT FEATURES = ALLOWED · UNNECESSARY REDESIGN = NOT ALLOWED

---

## 1. Method

Every P0/P1 line of `REQUIREMENTS.md`, every product behaviour in `PRODUCT.md` §5/§10/§13, and the submission gates in `HACKATHON.md` were checked against the actual code of all five routes and every component (`app/*`, `components/*`, `lib/*`, `types/index.ts`). **"Already supported?" means a judge can see and use it today in mock mode** — not merely that a type field exists. Two capabilities that previously looked "covered" failed this test (transcript, contradictions), and two existing controls proved to be inert (captions toggle, `captionsPreferred`).

## 2. What the preserved frontend already nails (do not touch)

Grounded Q&A chat with evidence badge (`From video` / `Web research` / `Not in this video`), quote block, click-to-jump timestamp button, High/Medium/Low confidence badge (P0-1, P1-4) · chapter list with active-chapter tracking and click-to-seek (P0-3, chapters half) · voice input via Web Speech + MediaRecorder with graceful fallback toasts (P1-3) · read-aloud per answer in en/hi (P0-5 TTS artifact) · answer language + explanation level + research-toggle settings bar (P0-5) · accessibility page with live-applied high contrast / reduced motion, keyboard nav, screen-reader labels · library with save/restore/archive/delete (P0-7) · demo lesson auto-seeded and hard-routed (P0-6) · honest error toasts + fallback answer cards · help page that explains the trust labels.

## 3. Gap matrix

| # | Requirement | Already supported? | Missing? | Priority | Proposed UI addition |
|---|---|---|---|---|---|
| 1 | P0-1 grounded Q&A + honest not-found | Yes — chat: evidence badge, quote, timestamp jump, confidence, distinct "Not in this video" card | — | No change | backend work only |
| 2 | P0-2 schema-validated analysis pipeline | Yes — dropzone + progress card | — | No change | backend work only |
| 3 | P0-3 chapters + click-to-jump | Yes — `ChapterList`, seek lands ~1 s | — | No change | — |
| 4 | P0-3 **searchable transcript** | **No** — `Lesson.transcript` is fetched on every workspace load and rendered by **zero** components; no search exists anywhere | entire transcript UI | **P0 — must add** | **A2** `TranscriptPanel` (§4) |
| 5 | P0-3 timeline shows **confidence** | Partial — answers show it; the `Chapter` type drops the schema's per-event `confidence` | per-chapter confidence | **P1 — justified** | **A4** badge on chapter rows (§4) |
| 6 | P0-4 **contradiction / claim surfacing** | **No** — reachable only if a judge guesses to ask "did the teacher contradict themselves?" (DoD #3 requires it *surfaced*, both timestamps clickable; PRODUCT §13 names "the contradiction panel") | contradiction display | **P0 — must add** | **A1** `ContradictionCard` (§4) |
| 7 | P0-5 one accessible artifact | Yes — per-answer read-aloud (TTS) with timestamp preserved on the card; Hindi + beginner level ride existing settings (P0-minimum: one of three) | — | No change | — |
| 8 | P0-6 fixtures + demo path | Yes — demo button hard-routes; library auto-seeds `demo-binary` | multi-fixture picker | P2 | optional; not added |

| 9 | P0-7 persistence / return to analysis | Yes — localStorage library + per-lesson conversation restore | — | No change | — |
| 10 | P0-7 **multi-turn follow-ups keep context** | **No** — history is stored client-side (`cb-conv-*`) but `askQuestion` sends only `{question, settings}`; "tell me more about that" is unanswerable | follow-up context to the agent | **P0 — must add** | **A3** `history` passthrough — no visual change (§4) |
| 11 | P0-8 eval harness · P0-9 deploy · P0-10 provenance · P0-11 submission | n/a — no UI surface | — | No change | numbers go in the deck |
| 12 | P1-1 eval at full size | n/a | — | No change | — |
| 13 | P1-2 all three accessible outputs | Yes — TTS, translation, plain language all reachable | — | No change | — |
| 14 | P1-2 **shareable evidence card** | Partial — the copy button copies answer text only (no timestamp/quote) | formatted evidence card | **P1 — justified** | **A6** copy-payload extension (§4) |
| 15 | P1-3 voice question input | Yes — full implementation with fallbacks | — | No change | — |
| 16 | P1-4 confidence / uncertainty UI | Yes — badges + visually distinct not-found path | per-answer uncertainty-reason note | P2 | optional; not added |
| 17 | P1-5 auth / per-user scoping | Deliberately deferred (`CONSTRAINTS.md` §4) | — | No change | — |
| 18 | P1-6 second frontend | Superseded — `web/` **is** the surface (`CONSTRAINTS.md` §3.1) | — | No change | `REQUIREMENTS.md` Streamlit wording reconciled separately |
| 19 | P1-7 rehearsal + backup recording | n/a | — | No change | — |
| 20 | **Status information** during real analysis (directive example) | Partial — `AnalysisProgress` runs a fixed ~5 s cosmetic cadence while a real analysis takes ~30–90 s; the screen then looks stuck | honest progress for live uploads | **P1 — justified** | **A7** elapsed time + honest copy (§4) |
| 21 | **Accessibility controls** (directive example): captions | **Inert** — the player's captions toggle only recolors the button (`captionsOn` feeds nothing; no `<track>`, no transcript prop); `captionsPreferred` is stored but never read | real captions | **P1 — justified** | **A5** client-side WebVTT from `Lesson.transcript` (§4) |
| 22 | Accessibility: `plainLanguage` toggle | Inert — but redundant with the explanation-level control | wiring | P2 | optional one-line override; not added |
| 23 | **Trust / provenance indicators** (directive example) | Yes — video/web never mixed, confidence badges, quotes, help page explains labels | "AI can make mistakes" microcopy | P2 | optional; not added |
| 24 | **Required actions** / library management (directive example) | Yes — archive / delete / restore / empty state | — | No change | — |
| 25 | **Required hackathon functionality** (deployed URL, repo, <3-min video, PDF deck) | n/a — not UI | — | No change | — |
| 26 | Lesson summary/topics display | Partial — both ship in the `Lesson` payload, neither renders in the workspace (title/meta show on library cards) | summary header | P2 | optional; not added |

**Outcome: 3 P0 additions + 4 justified-P1 additions approved for automatic build (A1–A7, §4). 6 P2 items deferred (§5). Everything else: no change.**

---

## 4. Approved additions (P0 + justified P1 — built automatically)

### A1 — Contradiction findings card · **P0** (gap #6)

1. **Requirement satisfied:** P0-4; Definition-of-done #3 ("a prepared contradictory pair is *surfaced* with both timestamps and both are clickable"); PRODUCT.md §5.5 and §13 ("the contradiction panel showing *both* statements").
2. **Why important:** contradiction surfacing is the Innovation (25%) answer to "isn't this just a Gemini video demo?" A feature a judge must guess to ask for scores zero.
3. **Where it fits:** workspace left column (`/lesson/[id]`), between the video and the "Ask your teacher" card — same vertical rhythm as the existing cards.
4. **Smallest additive component:** one new `components/contradictions/contradiction-card.tsx`. Each pair shows the claim label and **both** statements, each with the existing `TimestampButton` wired to the existing `onJump` (seek + timeline highlight). Hidden entirely when `contradictions` is empty. Data arrives as additive optional `Lesson.contradictions?` — no new endpoint; the seeded `demo-binary` fixture ships one genuine pair; mock mode mirrors it in `lib/mock-data.ts`.
5. **Clutter:** zero when no pairs; one card max otherwise; amber accent only (caution semantics) on the existing card chrome; it shows both sides and never picks a winner (PRODUCT §13).
6. **Nothing removed:** the Q&A agent still answers contradiction questions in chat; all chat behaviour unchanged.
7. **Recorded:** `DECISIONS.md` D-02 — supersedes the Q&A-only reconciliation formerly in `CONSTRAINTS.md` §3.2.

### A2 — Searchable transcript panel · **P0** (gap #4)

1. **Requirement satisfied:** P0-3 — "display … a searchable transcript; clicking an evidence card or transcript row seeks the video"; Definition-of-done #1 ("see its evidence timeline and transcript").
2. **Why important:** the transcript is the raw proof that the pipeline actually heard the video — the fastest trust check a judge has. Today the data is fetched on every workspace load and rendered nowhere.
3. **Where it fits:** desktop right rail, directly under the existing "In this video" chapter list; mobile, a second collapsible drawer immediately under the existing chapters drawer — mirroring that pattern exactly.
4. **Smallest additive component:** one new `components/transcript/transcript-panel.tsx` — a search input (client-side filter of `lesson.transcript`) over a bounded-height list of rows (`formatTime(startSeconds)` + text) that call the existing `onJump`. No endpoint, no new state owner, no backend change.
5. **Clutter:** collapsed-by-default drawer on mobile; one compact section with a single input on desktop.
6. **Nothing removed:** chapters UI untouched.
7. **Recorded:** `DECISIONS.md` D-03.

### A3 — Conversation history in the ask request · **P0** (gap #10, no visual change)

1. **Requirement satisfied:** P0-7 acceptance — "multi-turn follow-ups keep conversation context".
2. **Why important:** "Can you explain that more simply?" / "why?" are the most natural follow-ups a judge will ask; without history the agent cannot resolve "that". The history already exists client-side (`cb-conv-*`) — it is simply never sent.
3. **Where it fits:** invisible — `WorkspaceClient.ask` / `lib/api.ts` only.
4. **Smallest additive change:** optional `history: { role, text }[]` (last ≤ 6 messages) added to the `POST /analyses/:id/questions` body. Mock mode ignores it; the server stays stateless — history is client-supplied per request and never stored (CONSTRAINTS §3.4 stands).
5. **Clutter:** none — no UI at all.
6. **Nothing removed:** omitting `history` reproduces today's behaviour exactly.
7. **Recorded:** `DECISIONS.md` D-04.

### A4 — Chapter confidence badge · **P1, justified** (gap #5)

1. **Requirement satisfied:** P0-3 requirement text — "display the evidence timeline (chapters, timestamps, **confidence**)".
2. **Why justified:** the schema's per-event `confidence` already exists end-to-end and is dropped only at the `Chapter` serialisation boundary; showing it extends the product's trust design (PRODUCT §13) to the timeline. Trivial cost, real provenance value.
3. **Where it fits:** `ChapterList` rows, beside the existing timestamp.
4. **Smallest additive change:** additive optional `confidence?: number` on `Chapter`; render the existing `ConfidenceBadge` only when present.
5. **Clutter:** one small badge per row, identical to the answer-card badge.
6. **Nothing removed.**
7. **Recorded:** `DECISIONS.md` D-05.

### A5 — Real captions generated from the transcript · **P1, justified** (gap #21)

1. **Requirement satisfied:** the directive's "accessibility controls" example; the P0-5 accessibility/impact story (25% criterion); and the product's one rule — today the player ships a captions toggle and the settings page a `captionsPreferred` switch that **change nothing** (an inert control claims a capability the product does not deliver).
2. **Why justified:** turns two inert controls honest, demonstrates "one index, many outputs" (PRODUCT §9), and costs no backend work — the transcript already ships with every lesson.
3. **Where it fits:** `VideoPlayer` gains one optional `transcript` prop; the workspace passes `lesson.transcript`.
4. **Smallest additive change:** build a WebVTT blob URL from the segments client-side, attach one `<track kind="captions">`; the existing captions toggle switches the track mode; the default honours `loadA11y().captionsPreferred`.
5. **Clutter:** none — native captions render inside the existing player chrome; no new buttons.
6. **Nothing removed:** all existing player controls behave as before.
7. **Recorded:** `DECISIONS.md` D-06.

### A6 — Copyable evidence card · **P1, justified** (gap #14)

1. **Requirement satisfied:** P1-2 — "a copyable **shareable evidence card** (answer + timestamp + quote)".
2. **Why justified:** the tangible proof object a user pastes into notes/chat; the current copy button captures the answer text only, losing the timestamp and quote that make it evidence.
3. **Where it fits:** the existing copy button on each assistant message.
4. **Smallest additive change:** extend the clipboard payload to a formatted card (answer + quote + `mm:ss` + lesson title); toast copy becomes "Evidence card copied". Same button, same icon, same position.
5. **Clutter:** zero new UI.
6. **Nothing removed.**
7. **Recorded:** `DECISIONS.md` D-07.

### A7 — Honest analysis progress for live uploads · **P1, justified** (gap #20)

1. **Requirement satisfied:** the directive's "important status information" example; demo reliability on the live-upload path (P0-9, P1-7); the honesty principle — `AnalysisProgress` completes six stages on a fixed ~5 s cadence while a real analysis takes ~30–90 s.
2. **Why justified:** during the one live-upload demo a judge watches all stages "complete" in five seconds and then an apparently frozen screen for a minute — it reads as a hang, on stage.
3. **Where it fits:** the existing `AnalysisProgress` card on `/`.
4. **Smallest additive change:** add an elapsed-time line ("Analyzing… 0:42 — usually under two minutes") and drive stage highlighting from elapsed time instead of the fixed 700 ms tick; the final stage already waits for the real response.
5. **Clutter:** one line of text inside the existing card.
6. **Nothing removed:** same stages, same card, same animation language.
7. **Recorded:** `DECISIONS.md` D-08.

---

## 5. Deferred — P2, not built without a new directive

| Item (gap #) | Why deferred |
|---|---|
| Lesson summary/topics header in the workspace (#26) | nice context, but nothing requires it; the library card already carries title/meta |
| `plainLanguage` toggle wiring (#22) | redundant — the explanation-level control already delivers plain-language answers; a one-line override can land later |
| "AI can make mistakes — verify with the timestamp" microcopy (#23) | the help page already explains every trust label; low marginal value |
| Multi-fixture picker on the landing page (#8) | one hard-routed demo satisfies P0-6; extra fixtures arrive via the library automatically |
| Per-answer `uncertaintyReason` note (#16) | P1-4's core (badges + distinct not-found) already ships; the note is polish |
| `REQUIREMENTS.md` Streamlit wording (#18) | documentation reconciliation, not a UI change — tracked in `CONSTRAINTS.md` §3.1 |

## 6. Design-system guardrails (apply to every addition)

- **Reuse before create:** card chrome (`rounded-2xl border border-white/[0.08] bg-[#0D1322]`), `Badge`, `TimestampButton`, `ConfidenceBadge`, `formatTime`, `motion/react` spring entrances, `aria-live` / aria-label patterns, lucide icons, sonner toasts.
- New components live beside their siblings (`components/contradictions/`, `components/transcript/`) and are typed from `types/index.ts` — **additive optional fields only; never renames or removed fields.**
- No new routes, no new pages, no navigation changes, no palette changes. Amber is the only new accent and is reserved for contradiction findings (semantic: caution).
- **Mock mode must keep working:** `lib/mock-data.ts` gains seeded `contradictions` and chapter `confidence` so the full experience still runs with `NEXT_PUBLIC_API_BASE_URL` unset.
- If an addition cannot meet these guardrails, it goes back to P2 — it does not get a redesign.

## 7. Contract impact (all additive, zero breaking changes)

| Change | Where | Breaking? |
|---|---|---|
| `Lesson.contradictions?: ContradictionPair[]` | `GET /analyses/:id` response | No — optional field; untouched components ignore it |
| `Chapter.confidence?: number` | same payload | No — optional field |
| `history?: {role,text}[]` | `POST /analyses/:id/questions` request body | No — optional; omitting it reproduces current behaviour |
| A2, A5, A6, A7 | client-side only | No backend change at all |

**No new endpoints. No changed fields. No removed fields.** The backend serialisation gains two field mappings (event → chapter confidence; stored contradiction pairs → `Lesson.contradictions`) and the agent gains an optional history block in its prompt — that is the entire server-side delta of this amendment.




