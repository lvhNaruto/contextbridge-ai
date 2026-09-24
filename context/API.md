# API Contract — ContextBridge

**Owner doc:** `context/API.md` · architecture `context/ARCHITECTURE.md` · constraints `context/CONSTRAINTS.md`
**Rule zero:** this document describes **only what the frontend (`web/`) actually consumes**, derived line-by-line from `web/lib/api.ts` and `web/types/index.ts`. The API adapts to the frontend, never the reverse; no endpoint may be added without a UI caller. **Amendment 2026-09-23 (frontend extensible per `CONSTRAINTS.md` §1):** the approved UI additions (`FRONTEND_GAP_ANALYSIS.md` A1–A7) consume three **additive optional fields** on existing endpoints — marked ✳ below. No new endpoints.

---

## 1. Conventions

| Concern | Decision | Why |
|---|---|---|
| Base URL | `NEXT_PUBLIC_API_BASE_URL` (e.g. `https://contextbridge-api-xxx.a.run.app`) | The only switch the frontend has; unset → mock mode |
| Protocol | HTTPS, plain `fetch` + `res.json()` | `web/lib/api.ts` `request()` — **no SSE, no websockets, no polling anywhere in the UI** |
| Auth | **None on requests** | The locked `request()` sends no `Authorization` header and cannot be changed. Compensating controls: CORS allowlist + per-IP rate limits + input caps (see `CONSTRAINTS.md`) |
| CORS | Allow the deployed frontend origin + `http://localhost:3000`; methods `GET, POST`; headers `Content-Type` | Browser calls are cross-origin from the Next.js app |
| Errors | `{"error": {"code": "snake_case", "message": "human readable"}}` with proper status | The frontend branches only on `res.ok`; codes serve operators, logs, and judges |
| Timeouts | `POST /analyses` ≤ 300 s · `POST …/questions` ≤ 25 s · reads ≤ 5 s | Frontend shows indefinite spinners; budgets keep waits humane |
| Idempotency | GETs and questions are side-effect-free; each `POST /analyses` creates a new id | Retries are always safe; conversation history is client-owned |

**Streaming:** none. Loading states (`AnalysisProgress` stages, `checking-video → finding-moment → preparing-answer` beats) are cosmetic client-side timers in the locked UI. The backend must **not** require streaming to look alive — it must simply answer within budget.

---

## 2. Data models (mirror of `web/types/index.ts`; ✳ = additive field from the 2026-09-23 extension amendment)

Field names are camelCase and exact. The backend serialises `MediaAnalysis` (`contextbridge_schema.py`) into the `Lesson` shape — `chapters` are the analysis `events` (their schema `confidence` now rides along, ✳). All ✳ fields are optional: untouched locked components compile and behave identically whether they are present or not.

```jsonc
// Lesson — GET /analyses/{id}
{
  "id": "demo-binary",
  "title": "Understanding binary & computer language",
  "videoUrl": "https://api…/analyses/demo-binary/video", // directly playable, seekable
  "durationSeconds": 888,
  "createdAt": "2026-09-20T10:00:00.000Z",                // ISO 8601 string
  "language": "English",
  "summary": "An introduction to binary language…",
  "topics": ["Binary", "Data representation", "Computers"],
  "chapters": [
    { "id": "ch-binary", "startSeconds": 173, "endSeconds": 376,
      "title": "What is binary language?", "description": "…",
      "confidence": 0.96 }           // ✳ optional — the schema event's confidence
  ],
  "transcript": [
    { "startSeconds": 173, "endSeconds": 210,
      "text": "Binary language uses only two digits: zero and one." }
  ],
  "contradictions": [                // ✳ optional — absent when none found
    { "id": "cx-1",
      "claim": "Whether all information is stored as binary",
      "statementA": { "text": "…first statement…",
                      "startSeconds": 210, "endSeconds": 224, "quote": "…" },
      "statementB": { "text": "…conflicting later statement…",
                      "startSeconds": 615, "endSeconds": 630, "quote": "…" },
      "note": "The second statement qualifies the first." }
  ]
}
```

```jsonc
// ChatMessage — response of POST /analyses/{id}/questions
{
  "id": "msg-m4x8k2",
  "role": "assistant",
  "text": "In low light, Night Sight is activated…",
  "isVoice": false,
  "createdAt": 1759161600000,                 // epoch ms — a NUMBER, not a string
  "suggestions": [                            // ✳ optional: 2-3 explore anchors derived from video
    "How does Video Boost compare to Night Sight?",
    "Where in Tokyo was this video filmed?",
    "What camera settings were recommended?"
  ],
  "answer": {
    "text": "In low light, Night Sight is activated…",
    "evidenceType": "video",                  // "video" | "web" | "unknown"
    "evidence": { "startSeconds": 15, "endSeconds": 21,
                  "quote": "In low light, it activates 'Night Sight' to make the quality even better." },
    "confidence": 0.96,                       // 0–1; badge hidden when 0
    "explanationOf": "Verified against spoken transcript at 00:15", // ✳ optional branch rationale
    "sources": [                              // only when evidenceType = "web"
      { "title": "Google Pixel Night Sight Explained", "domain": "support.google.com",
        "url": "https://support.google.com/pixelphone/answer/...",
        "description": "How computational photography powers low light video..." }
    ],
    "notInVideo": true                        // only when the video lacks the answer
  }
}
```

**Shape invariants the UI depends on:**

1. `evidenceType:"video"` ⇒ `evidence` present, `0 ≤ startSeconds ≤ endSeconds ≤ durationSeconds`, `quote` copied from the stored transcript. The jump button seeks to `startSeconds`.
2. `evidenceType:"web"` ⇒ `sources` non-empty, `notInVideo:true`, **no** `evidence` block. Video and web are never mixed.
3. `evidenceType:"unknown"` ⇒ honest refusal, `confidence:0`, `notInVideo:true`.
4. `LessonSettings` sent with every question: `{"answerLanguage":"auto|en|hi","explanationLevel":"beginner|intermediate|expert","researchMissingContext":true|false}`.
5. ✳ `contradictions` (when present): both statements carry real timestamps within `[0, durationSeconds]`, each quote (fuzzy-)matching the stored transcript — both jump buttons must seek correctly. The UI shows both sides and never picks a winner (PRODUCT.md §13).

✳ **`ContradictionPair` model** (additive, consumed by the A1 workspace card):

```jsonc
{ "id": "string", "claim": "the shared topic both statements address",
  "statementA": { "text": "string", "startSeconds": 0, "endSeconds": 0, "quote": "string?" },
  "statementB": { "text": "string", "startSeconds": 0, "endSeconds": 0, "quote": "string?" },
  "note": "string?" }               // why they conflict — neutral phrasing, no verdict
```

---

## 3. Endpoints

### 3.1 `POST /analyses` — upload & analyse (synchronous)

Called by `createAnalysis(file)` from the upload dropzone. One request does upload **and** analysis, because the locked frontend never polls a status endpoint.

- **Request:** `multipart/form-data`, single field `video` (MP4/MOV/MPEG/WEBM/AVI, ≤ 100 MB, ≤ 15 min).
- **Response `200`:** `{"id": "an-9f3k…"}` — returned only after the analysis is validated and persisted. The frontend immediately calls `GET /analyses/{id}`.
- **Errors:** `400` no/invalid file · `413` too large · `422` unsupported/undecodable video · `429` rate limited · `502` Gemini/pipeline failure (`error.message` logged server-side; UI shows its generic retry state).
- **Semantics:** all-or-nothing. A lesson is served only from a fully schema-validated `MediaAnalysis`; failures persist `status:"failed"` + error, never a partial result. Retrying re-uploads as a **new** id — always safe.
- **Example:**
  ```
  curl -F "video=@lecture.mp4" $API/analyses
  → {"id": "an-9f3k2m"}
  ```

### 3.2 `GET /analyses/{id}` — the lesson

Called by `WorkspaceClient` on mount (and by `createAnalysis` after upload).

- **Response `200`:** a full `Lesson` (§2). `videoUrl` points at `GET /analyses/{id}/video`; `title` derives from the uploaded filename exactly as the mock does (strip extension, `-`/`_` → spaces). Includes ✳ `contradictions` when the analysis surfaced conflicting pairs (A1) and ✳ per-chapter `confidence` (A4); the seeded `demo-binary` fixture ships one genuine contradiction pair so the workspace card demonstrates on stage.
- **Errors:** `404` unknown id → UI shows "We couldn't load this lesson." · `409` analysis failed → same screen; details in `error.message`.
- **Special id:** `demo-binary` is seeded at startup and always returns `200` (the locked demo button routes straight to it).
- **Example:** `GET /analyses/demo-binary` → the `Lesson` shown in §2.

### 3.3 `GET /analyses/{id}/video` — playback (required, implied by `Lesson.videoUrl`)

Not listed in `api.ts`'s comments but **required by the contract**: the locked `VideoPlayer` sets `Lesson.videoUrl` as a `<video>` src and seeks programmatically.

- **Response `200`/`206`:** the video bytes with `Accept-Ranges: bytes` and full **Range** support (evidence buttons jump mid-file), correct `Content-Type`, `Cache-Control: private, max-age=3600`.
- **Errors:** `404` unknown id.
- **Note:** implemented as a GCS proxy stream or a 302 to a signed URL — invisible to the frontend either way.

### 3.4 `POST /analyses/{id}/questions` — grounded Q&A (the agent)

Called by `askQuestion(lessonId, question, settings, isVoice)` from the workspace. Voice questions arrive here too — the browser transcribes via the Web Speech API and submits text with `isVoice=true`.

- **Request:**
  ```json
  { "question": "What does binary language mean?",
    "settings": { "answerLanguage": "auto",
                  "explanationLevel": "beginner",
                  "researchMissingContext": true },
    "history": [ { "role": "user", "text": "…" },
                 { "role": "assistant", "text": "…" } ] }  // ✳ optional, last ≤ 6 messages
  ```
- **Response `200`:** a resolved assistant `ChatMessage` (§2) — `role:"assistant"`, `createdAt` as epoch-ms number, `isVoice` echoed, `answer` honouring the three shape invariants.
- **Behaviour contract:**
  - Answer present in the video → `evidenceType:"video"` + real timestamps + transcript quote, language/level per `settings`.
  - Answer absent + `researchMissingContext:true` → `evidenceType:"web"`, `notInVideo:true`, `sources` from Google Search grounding, clearly separated.
  - Answer absent + research off → `evidenceType:"unknown"`, `confidence:0`, honest refusal text (never an invention).
  - Contradiction questions (e.g. "did the teacher contradict themselves?") are answered from the stored contradiction pass with video evidence — independently of the ✳ `contradictions` field that drives the workspace card (A1).
  - ✳ `history` (A3, P0-7): client-supplied recent messages used only to resolve follow-ups ("tell me more about that") in this request; the server stores nothing and stays stateless. Requests omitting it get the previous behaviour.
- **Errors:** `404` unknown lesson · `422` invalid question/settings · `429` rate limited · `502` total LLM failure. The UI already renders a toast + honest fallback message on any non-2xx — but a truthful 200 is always preferred over a 5xx when the model simply lacks the answer.
- **Latency:** ≤ 25 s hard cap; typical ≤ 8 s (one LLM round).
- **Example:**
  ```
  curl -X POST $API/analyses/demo-binary/questions \
       -H "Content-Type: application/json" \
       -d '{"question":"Where does the teacher explain binary language?",
            "settings":{"answerLanguage":"auto","explanationLevel":"beginner",
                        "researchMissingContext":true}}'
  → ChatMessage with evidence {"startSeconds":173,"endSeconds":376,
     "quote":"Binary language uses only two digits: zero and one."}, confidence 0.97
  ```

---

## 4. Reserved by the locked API layer (implement thin, or leave unwired)

These functions exist in the locked `web/lib/api.ts`, so their routes are documented — but **no component currently invokes them**. Implementing the two trivial ones costs minutes and keeps the locked layer honest; conversation storage is deliberately **not** built.

### 4.1 `POST /analyses/{id}/voice-question` — reserved alias

`askVoiceQuestion()` is defined but never called (the browser transcribes client-side and routes voice through `POST /questions`).

- **Request:** `multipart/form-data` with `audio` (Blob) and `transcript` (string).
- **Response:** identical to §3.4, `isVoice:true`. Implementation: ignore `audio` (or retain it untouched), answer `transcript` via the same agent path.

### 4.2 `GET /analyses/{id}/chapters` — reserved projection

`getChapters()` is defined but never called (the workspace reads `lesson.chapters`).

- **Response `200`:** `Chapter[]` — a projection of the `Lesson` from §3.2.

### 4.3 `GET /analyses/{id}/conversation` — **do not implement**

`getConversation()` reads localStorage even in real mode — conversation history is client-owned by design. Building this would duplicate client state with zero callers. Documented here only because `api.ts` names it.

---

## 5. Operations endpoint (not frontend-consumed)

### `GET /healthz`

Cloud Run health/liveness check. `200 {"status":"ok","demoSeeded":true,"model":"gemini-2.5-flash"}` · `503` when the demo fixture failed to seed or the store is unreachable.

---

## 6. Contract summary — who calls what

| Endpoint | Caller in locked UI | Status |
|---|---|---|
| `POST /analyses` | `UploadDropzone` → `createAnalysis` | **required** |
| `GET /analyses/{id}` | `WorkspaceClient` → `getAnalysis`; also after upload | **required** (incl. seeded `demo-binary`) |
| `GET /analyses/{id}/video` | `VideoPlayer` via `Lesson.videoUrl` | **required** (Range support) |
| `POST /analyses/{id}/questions` | `WorkspaceClient` → `askQuestion` (typed + voice) | **required** |
| `GET /analyses/{id}/chapters` | none today | reserved, trivial |
| `POST /analyses/{id}/voice-question` | none today | reserved alias |
| `GET /analyses/{id}/conversation` | never fetched | **not built** |
| `GET /healthz` | Cloud Run | ops only |

Four frontend-facing endpoints, two reserved, one ops. Anything beyond this list is invention.

**Additive fields (2026-09-23 amendment, `FRONTEND_GAP_ANALYSIS.md` A1–A7):** `Lesson.contradictions?`, `Chapter.confidence?`, and the `POST …/questions` body's `history?` are **fields, not endpoints** — all optional, all ignored by untouched components. A2 (transcript panel), A5 (captions), A6 (evidence-card copy), and A7 (progress honesty) are purely client-side and consume data already in this contract.



