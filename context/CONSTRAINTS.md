# Constraints — ContextBridge (AI Builder Cup 2026)

**Owner doc:** `context/CONSTRAINTS.md` · architecture `context/ARCHITECTURE.md` · API contract `context/API.md`
**Purpose:** the binding rules every build decision must respect. If a design choice conflicts with this file, the design choice loses.

---

## 1. The frontend is LOCKED BY DESIGN, EXTENSIBLE BY GAP ANALYSIS (the supreme constraint)

The existing Next.js frontend in `web/` is **final and approved as the visual and UX foundation**. It is the fixed UI contract and the source of truth for the user experience. Per the product-owner directive of 2026-09-23 it is **locked but extensible**: requirements (`REQUIREMENTS.md`, `PRODUCT.md`, `HACKATHON.md`) remain the functional source of truth, and an important P0/P1 capability missing from the UI MAY be added — as the smallest natural addition that fits the existing design system, never as a redesign.

- **Do not redesign, restyle, restructure, rewrite, or replace the frontend.** No changes to existing UI/UX, layouts, colors, typography, animations, components, navigation, routes, or existing frontend behavior.
- **Additive extensions are allowed only when all four hold:** (a) the capability is a P0 or justified-P1 gap recorded in `context/FRONTEND_GAP_ANALYSIS.md`; (b) it is one small additive component — never a new page; (c) it removes nothing and adds no visual clutter; (d) it is recorded in `context/DECISIONS.md`. The approved set today is A1–A7 (contradiction card, transcript panel, ask-request history, chapter confidence, real captions, copyable evidence card, honest analysis progress).
- **Type/payload additions must be additive and optional** (new optional fields on existing requests/responses) so untouched components compile and behave identically.
- No replacing the chosen stack: Next.js 16 / React 19 / TypeScript / Tailwind v4 / shadcn-style primitives / Motion / GSAP stay as they are.
- No new frontend architecture; no moving frontend files unless a hard technical integration issue leaves no alternative (none is currently known).
- **The backend is built around the frontend contract — never the reverse.** `web/lib/api.ts` + `web/types/index.ts` define endpoints, payload shapes, and error semantics; the backend conforms to them exactly (camelCase fields, ISO `createdAt` on `Lesson`, epoch-ms `createdAt` on `ChatMessage`, `res.ok`-only error branching).
- The frontend's loading, processing, and progress states are cosmetic client-side timers. The backend must not require SSE, websockets, or polling to support them.
- Anything the frontend already owns stays client-owned: saved-lesson library, conversation history, learner/accessibility settings (localStorage), voice transcription (Web Speech API), and read-aloud (speechSynthesis). **Do not build server endpoints that duplicate client-owned state.**

## 2. Backend integration rules

- Implement **only** the APIs the frontend uses (`context/API.md`); do not invent endpoints for hypothetical features. The approved UI extensions (§1) ride existing endpoints as additive optional fields — **no new endpoints were needed**.
- Preserve existing working business logic: `contextbridge_schema.py` (`MediaAnalysis` validation) and `contextbridge_store.py` (SQLite store) are reused as-is; the Gemini analysis prompt from `app.py` moves into the pipeline with unchanged behaviour. Refactor only what is needed to expose clean HTTP APIs.
- **Kill the mock:** `_ask_gemini → _mock_answer` is replaced by the real grounded agent (P0-1). No mocked answer path may remain reachable from the API.
- `GET /analyses/demo-binary` must always succeed — the locked "Try the demo lesson" button hard-routes to it.
- `Lesson.videoUrl` must be directly playable and seekable (HTTP Range) by a plain HTML5 `<video>` element.
- The honest not-found path is a feature: when the video does not contain the answer, return a truthful `evidenceType:"unknown"` / `notInVideo:true` answer — **never** a fabricated one, and never mix video evidence with web sources in one answer (the UI forbids it; the backend enforces it).

## 3. Reconciliation decisions (recorded, binding)

1. **Surface switch, by directive.** `REQUIREMENTS.md` originally named Streamlit the committed surface with `web/` shelved. The product owner's directive now declares `web/` final and locked — `web/` **is** the surface. The "one frontend" guardrail stands, now pointing at Next.js; `app.py`'s Streamlit UI is superseded (file untouched, no longer the product). Its business logic is preserved per §2.
2. **Contradiction surfacing (P0-4) — first-class UI (supersedes the earlier Q&A-only reconciliation).** The 2026-09-23 directive lifted the hard feature lock, and the gap analysis classified the missing contradiction display as **P0** (`FRONTEND_GAP_ANALYSIS.md` A1): a small additive *Worth checking*-style card on the workspace shows each conflicting pair with both statements and both timestamp buttons. The backend computation is unchanged (a second structured extraction over the *stored* `MediaAnalysis` — no second video call); pairs are served as an additive `contradictions` field on `GET /analyses/:id`, and the Q&A agent still answers contradiction questions with real evidence timestamps.
3. **Accessible artifacts (P0-5) ride existing controls.** Plain-language and Hindi outputs are delivered through the locked settings the UI already sends (`explanationLevel:"beginner"`, `answerLanguage:"hi"`); narration is the UI's browser read-aloud. No artifact endpoint is built — none is consumed.
4. **No server-side conversations, library, or settings.** The frontend owns them in localStorage. `GET /analyses/:id/conversation` is documented but deliberately unimplemented; `getConversation()` never fetches even in real mode. Follow-up context (P0-7) is honoured without breaking this rule: the client sends the last few messages as an optional `history` field with each question; the server uses it for that request only and stores nothing.

## 4. Security constraints

- **No request authentication can be added** — the locked `request()` sends no credentials. Compensate with: CORS allowlist (deployed frontend origin only), per-IP rate limits on `POST /analyses` and `POST …/questions`, upload caps (100 MB / 15 min / allowlisted formats), and question length caps.
- Secrets (`GOOGLE_API_KEY`, project config) live in env vars / Secret Manager, never in the repo; `.env.local` stays gitignored.
- Least-privilege service account: `roles/aiplatform.user` + object access to **one** bucket. Nothing else.
- User questions are treated as untrusted data inside a fenced system prompt; agent tools are read-only; all model output is schema-validated before it can reach a response (prompt-injection and tool-safety detail in `ARCHITECTURE.md` §13).
- No PII is requested or stored; uploaded videos are user-supplied demo content with a defined lifecycle (wiped post-hackathon).

## 5. Technology constraints

- **Google Cloud stack, sponsor-aligned:** Gemini 2.5 Flash on Vertex AI (video understanding, grounded answers, contradiction extraction, Google Search grounding), Cloud Run (both services), GCS (videos), Cloud Logging/Monitoring (observability). No second model family, no embeddings, no vector DB, no Speech-to-Text or TTS services (the browser does both) — every service has a named responsibility; no sprinkling for slide credit.
- **One backend framework:** FastAPI (Python) so `contextbridge_schema.py` and `contextbridge_store.py` import unchanged. No new language, no second backend.
- **One database:** SQLite via the existing store. No Cloud SQL, no Postgres, no Redis.
- **No orchestration frameworks** (no LangGraph/ADK requirement, no task queues, no Kubernetes): the agent loop is ~100 lines of plain Python inside one service.
- The evaluation harness (P0-8) and fixtures (P0-6) are build tooling, not runtime services.

## 6. Hackathon constraints (from `context/HACKATHON.md`, `context/RULES.md`, `context/RESOURCES.md`)

- Prototype build window **7 Sep – 18 Oct 2026**; all code committed inside it (fresh-project provenance, P0-10).
- One theme (Media, Content & Digital Experiences), one submission; team of 2–4 working professionals, JAPAC, 21+.
- Submission artifacts: **deployed prototype URL (Cloud Run/GCP/Firebase) · public GitHub repo · public demo video < 3 min · English PDF deck**.
- **No sponsor credits/quotas are confirmed** (`RESOURCES.md`): fixtures and the AI-Studio fallback ladder keep the demo independent of live Vertex quota.
- All materials in English; demo must work for a first-time visitor with zero local setup.

## 7. Non-goals

- No user accounts, login, or multi-tenancy (would require forbidden frontend changes).
- No multi-video library server-side, playlists, or cross-video search — one video at a time (PRODUCT.md §11).
- No clip rendering / video editing / re-encoding pipeline.
- No server-side conversation persistence, notifications, or external actions (email/posting/booking).
- No streaming responses, websockets, or realtime collaboration.
- ~~No dedicated contradiction panel UI~~ — superseded (§3.2): the panel is an approved P0 addition. Still out: any *redesign* to accommodate it.
- No production hardening beyond what a public demo needs (no WAF, no org policies, no VPC-SC).

---

**The one rule above all (unchanged from PRODUCT.md §13): do not claim certainty the video does not give.** Every constraint above either protects the locked frontend or protects that rule.


