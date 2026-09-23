# Product Definition — ContextBridge

**Theme:** Media, Content & Digital Experiences
**Owner doc:** `context/PRODUCT.md`; **requirements** live in `context/REQUIREMENTS.md`.
**Status:** aligned to `context/IDEA_REVIEW.md` — ContextBridge selected with three binding amendments (contradiction surfacing, tangible artifact, risk hardening).
**References:** architecture in `context/ARCHITECTURE.md`, API contract in `context/API.md`, build plan in `context/BUILD_PLAN.md`. This file is the product spec, not a build plan. (The early draft `docs/contextbridge-build-plan.txt` was fully superseded and removed — `context/DECISIONS.md` D-10.)

---

## 1. Name

**ContextBridge**

Tagline (deck only, not the product UI):
> Turn long, hard-to-access video into searchable, timestamped, accessible knowledge.

Do not brand the prototype as a "reusable Multimodal Intelligence Platform." That is a scalability line for the deck. One product, one surface, one theme, one submission.

---

## 2. One-line pitch

Upload a long video, ask it questions, and get a grounded answer with the exact timestamp, the quote that supports it, and one accessible version — plain-language summary, translation, or spoken narration — of the same content.

---

## 3. Problem

Important information is trapped in long recordings — lectures, trainings, public hearings, corporate talks, news conferences, webinars, long-form video. A person who needs one answer usually has two options: watch the whole thing or give up.

The pain is specific and frequent:

- A student misses a concept in a 40-minute lecture and cannot find the exact moment it was explained.
- A new hire sits through onboarding video they will not remember; the same question gets asked repeatedly.
- A resident, caregiver, or non-native speaker cannot engage with a public-service video in their own language or reading level.
- A viewer cannot verify what was actually said, or tell whether one statement conflicts with another later in the video.

A generic video chatbot can summarise. ContextBridge exists because a summary is not the job — the job is **find the answer, prove where it came from, and make it reachable for the next viewer**.

---

## 4. Target users

**Primary (the prototype's surface):**

- Students and self-learners working with educational videos and tutorials.
- Instructors and trainers publishing video lessons who want learners to ask follow-ups without re-recording explanations.
- Anyone who has watched a long video and needed a specific answer, in a specific language or reading level.

**Scale story (deck only — not built now):**

- Education platforms and schools.
- Corporate training, onboarding, and compliance video.
- Public-service and civic communication (government, health, emergency video).
- Accessibility-first audiences: non-native speakers, screen-reader users, lower-literacy viewers, audio-first viewers.
- Long-form content platforms adding a conversational layer to existing video libraries.

Keep the prototype aimed at the primary user. Do not dilute the 25% impact score by pitching six audiences at once.

---

## 5. Solution (what it actually does)

A user uploads a short-to-medium video, ContextBridge analyses it once, and the product becomes a **searchable, questionnable, linkable version of that video**:

1. **One-pass analysis.** The video is sent to Gemini and returns a structured, schema-validated `MediaAnalysis`: a short summary, language, topics, a transcript with timestamps, and an evidence timeline of meaningful events — each with a confidence score and source quotes.
2. **An evidence timeline the viewer can read and click.** Chapters and timestamps, a searchable transcript, and evidence cards that jump playback to the relevant moment.
3. **Grounded Q&A.** A user asks a question; the product answers from the video's own analysis, attaches the source timestamps, and says **"not found in this video"** when the answer is not there. It does not invent answers.
4. **One accessible output.** From the same analysis the product generates, on request: a plain-language summary, a translation into one other language, or an audio narration via Text-to-Speech. The same content, a different format.
5. **Contradiction/claim surfacing.** A second extraction pass over the *same* analysis flags claims and highlights **pairs that conflict** — each with its timestamp, so a judge can click both and hear them in context. This is the amendment that answers the "isn't this just a Gemini video demo?" question.

The product does nothing outside the video and its own analysis unless a clearly separated, explicitly labelled optional context feature is enabled — never blended into the core answer.

---

## 6. Why agentic AI is necessary

Sending a video to Gemini and printing the response is a demo frame, not a product — and it scores poorly on the 40% technical-merit criterion. The work is not the model call; the work is the **orchestration around it**. ContextBridge needs an agent because the job is genuinely multi-step with real constraints:

- **Parse multimodal input** (video + embedded speech + on-screen text) and convert it into a **structured, schema-validated object**, not free text — otherwise downstream steps break.
- **Separate observation from interpretation**, attach evidence to every important claim, record confidence, and be **willing to say "not found"** — a designed behavior, not a lucky prompt.
- **Retrieve from a canonical index**, not the raw video, on every question — so repeated questions are fast and consistent and the live demo survives on stage.
- **Run a second reasoning pass** (claims/contradictions) over the same structured object without re-analysing the video — otherwise the contradiction feature doubles cost and latency for no reason.
- **Produce accessible outputs from the same structured representation** (summary, translation, audio) without a separate processing pipeline — one index, many outputs.
- **Be evaluable.** The agent's choices must be measured against a written evaluation set with known answer timestamps, groundedness, and an unsupported-answer rate. That only works if the pipeline is real and inspectable.

The model is the intelligence inside the loop; the agent is the loop — **ingest → validate → index → retrieve → answer-with-evidence → transform-and-label → evaluate**. Judges score the loop.

---

## 7. How the agent behaves (phases A–F)

These phases are the product's job description. Each maps to existing schema/state where possible — reuse `contextbridge_schema.py`, `contextbridge_store.py`, and the `analysis_jobs` status model rather than inventing new ones.

### Phase A — Ingest
Accept a video upload (≤2 minutes for the demo), record an `analysis_jobs` entry with status `running`, and pass model/context settings by video length. Failures set status `failed` with a reason instead of dying silently.

### Phase B — Analyse (one pass, schema-validated)
Call Gemini on Vertex AI with video + audio + on-screen text and parse the response strictly against the `MediaAnalysis` schema: summary, language, topics, transcript segments with timestamps, and evidence timeline events (`id`, `startSeconds`, `endSeconds`, `title`, `description`, `confidence`, `evidence` quotes). Invalid output is rejected and surfaced — never persisted as if it were good.

### Phase C — Index (canonical, reusable)
Persist the validated analysis through `contextbridge_store.py` so every later phase reads the **same stored object**, never re-analyses the video, and survives a page reload or redeploy. This is what makes repeated questions fast and the demo safe.

### Phase D — Answer (grounded, with evidence)
On each question: retrieve the relevant transcript segments and timeline events from the stored analysis, ask Gemini for a structured answer carrying `sourceTimestamps`, `foundInSource`, `confidence`, and `uncertaintyReason`. If retrieval or the model indicates the video does not contain the answer, return **"not found in this video"**. Any optional external context (web, user-provided document) is requested, stored, and rendered **separately and labelled** — never blended into the video-grounded answer.

### Phase E — Transform (accessible outputs)
From the same `MediaAnalysis`, on request: plain-language summary, translation into one supported target language, or Text-to-Speech narration of the relevant segment. Each output keeps a pointer back to its source timestamps so the evidence card stays verifiable. These reformats restate structured content; they never invent new claims.

### Phase F — Evaluate (the loop closes)
Run the evaluation set (P0-8) against the pipeline and record timestamp-retrieval accuracy, groundedness, unsupported-answer rate, and processing time. A behaviour that cannot be measured is not shippable — this phase is what lets the deck claim numbers instead of adjectives.

**Cross-cutting: contradiction surfacing.** Between C and D, a second extraction pass over the stored analysis (no new video call) produces claim nodes with timestamps and flags conflicting pairs for the UI — cheap, consistent, and demo-visible.

---

## 8. User journey

The end-to-end path a judge (or a first-time visitor) walks, and the path the <3-minute submission video should mirror:

1. **Arrive.** Open the deployed URL. No account required for the demo path; a fixture video is offered up front so nobody waits on an upload or analysis.
2. **Orient.** The video and its evidence timeline are on screen: chapters, timestamps, searchable transcript, evidence cards. The product explains itself without copy.
3. **Navigate.** Click a timeline event → the video seeks to that moment. Proof the timestamps are real, obtained in seconds.
4. **Ask.** Type a question about the video ("What did the speaker claim about the deadline?").
5. **Verify.** The answer appears with source timestamp(s) and quote; clicking the evidence card jumps playback to that exact moment. The claim and the clip are one click apart.
6. **Probe honesty.** Ask something the video does not contain → the product says **"not found in this video"** and offers no fabricated answer. This beat is rehearsed, not accidental.
7. **See the contradiction.** The contradiction panel shows two conflicting statements with their timestamps; clicking either one plays the segment. The innovation beat of the demo.
8. **Take it accessible.** One click produces the plain-language summary / translation / TTS narration of the same content, with its source timestamps intact. The impact beat.
9. **Leave with the artifact.** The visitor can share the evidence card — answer, quote, timestamp — proving the output is inspectable, not a vibe.

**First-run note:** phases 1–4 must work for a brand-new visitor on the live URL with zero local setup. Everything after that is the rehearsed demo script.

---

## 9. Differentiator

Why this is not "just a Gemini video demo," stated as product facts:

- **Honest not-found path.** Generic video chatbot demos only show the happy path; ContextBridge makes refusal a visible, testable feature. Honesty is the trust design.
- **Evidence as a first-class object.** Every important answer carries timestamped, clickable evidence that seeks the video — verifiability is built into the schema (`sourceTimestamps`, evidence timeline), not decorated into the UI.
- **Contradiction surfacing over the same analysis.** A second reasoning pass over one stored index surfaces conflicting claims without a second video call — a cheap, distinctly product-level behaviour.
- **Accessibility as an output, not a claim.** Plain language, translation, and TTS narration are generated from the same structured index and stay linked to their source timestamps — the JAPAC/accessibility angle is demonstrable in one click.
- **One canonical index.** Timeline, transcript, Q&A, and contradiction detection all read the same schema-validated `MediaAnalysis`; no second pipeline, no drift between features.
- **Measured, not asserted.** An evaluation set with known-answer timestamps reports timestamp accuracy, groundedness, unsupported-answer rate, and processing time — the deck can cite numbers.

**Positioning line for the deck:** "Every other tool gives you a summary of a video. ContextBridge gives you the answer, the exact moment it came from, an honest admission of what it doesn't know, and the same content in a form the next viewer can actually use."

---

## 10. Core features

**Tier 1 — MVP (must ship, maps 1:1 to P0 in `REQUIREMENTS.md`):**

- **Fixture-first video intake** — pre-analysed ≤2-minute sample videos plus one live upload/analysis path (P0-6).
- **Schema-validated analysis pipeline** — Gemini on Vertex AI → `MediaAnalysis` → persisted store, with `analysis_jobs` status (P0-2).
- **Evidence timeline + transcript** — chapters, timestamps, searchable transcript, evidence cards, click-to-seek (P0-3).
- **Grounded Q&A** — real Gemini answers with `sourceTimestamps` / `foundInSource` / `confidence` / `uncertaintyReason`, and the explicit "not found in this video" path (P0-1).
- **Contradiction / claim surfacing** — conflicting statement pairs with both timestamps, clickable to play, derived from the same analysis (P0-4).
- **One accessible artifact** — plain-language summary, one translation, or TTS narration from the stored index, each keeping its source timestamps (P0-5).
- **Session persistence** — return to an analysed video, keep follow-up conversation context (P0-7).
- **Evaluation harness** — known-answer timestamp set reporting timestamp accuracy, groundedness, unsupported-answer rate, processing time (P0-8).
- **Deployed Cloud URL** — working Cloud Run (or Firebase) deployment as the single demo surface (P0-9).

**Tier 2 — demo polish (P1, in priority order):**

- Full-size evaluation set (20 videos / 100 questions) with metrics in the deck (P1-1).
- All three accessible outputs + shareable evidence card (P1-2).
- Voice question input (P1-3).
- Confidence / uncertainty display on answers, distinct not-found styling (P1-4).
- Firebase Auth with per-user video scoping (P1-5).
- Second frontend at parity — **conditional** on a dedicated frontend owner (P1-6).
- Rehearsed demo + fallback recording (P1-7).

**Tier 3 — post-hackathon (P2 / deck scalability only):** multi-video projects, cross-video search, external actions, enterprise permissions, clip-rendering pipeline, packaging the stack as a reusable "Multimodal Intelligence Platform," additional verticals.

---

## 11. Non-goals

Explicitly **not** ContextBridge, for this hackathon:

- **Not a clip-rendering / video-editing product.** No re-encode, export, or StorySplice rendering pipeline — the amendment deliberately dropped it.
- **Not a multi-video platform.** One video in, one analysis out; no cross-video search, playlists, or library.
- **Not an actions system.** No emails, posts, bookings, or autonomous external actions — read, understand, explain, surface.
- **Not an enterprise permissions product.** Auth (P1) is scoping only; no teams, roles, audit consoles, or multi-tenant admin.
- **Not a generic chatbot.** No open-domain conversation inside the product; questions are about the video, and anything else gets the honest not-found (or a clearly separated, labelled optional context feature — never blended).
- **Not a multi-frontend project.** Streamlit is the surface; `web/` stays shelved unless P1-6 is explicitly triggered.
- **Not "six verticals in one demo."** One theme (Media), one submission — FixFlow/ShelfSense/RescueGrid/TrustLens-class ideas are roadmap lines only.
- **Not a service showcase.** Google services enter the stack only with a named responsibility; no sprinkling Document AI/Speech-to-Text/BigQuery for slide credit.

---

## 12. Success criteria

**Product success (what we demo):**

1. A first-time visitor on the deployed URL picks a fixture, understands the screen in ≤30 seconds, and reaches a timestamped, verifiable answer in under 3 clicks / 1 typed question.
2. Every answer's evidence click seeks the video to within ~1s of the claimed timestamp (spot-check: ≥4/5 correct on stage).
3. The honest "not found in this video" path visibly works when rehearsed.
4. A real contradictory pair surfaces with both timestamps and both segments playable.
5. One accessible artifact generates from the stored index with its source timestamps preserved.

**Measurable success (what we cite):** the P0-8 harness reports — timestamp-retrieval accuracy, groundedness, unsupported-answer rate, processing time per video — with targets set from the first fixture run and reported in the deck (P1-1 scales the set to 20 videos / 100 questions).

**Judging success (weights from `HACKATHON.md`):**

- **Technical / GenAI (40%)** — the agent pipeline (A–F) runs end-to-end on the deployed URL: no mocked Q&A, structured schema-validated output, evidence, measured eval numbers.
- **Problem alignment & impact (25%)** — one concrete user, one real pain, verifiable in the demo journey; the accessibility output demonstrates reach.
- **Innovation (25%)** — contradiction surfacing + honest refusal + one-index-many-outputs read as clearly beyond "summary demo."
- **UX (10%)** — first-run path needs zero explanation; timeline, answer card, and artifact button are self-evident.

**Submission success:** deployed URL live, public GitHub repo with in-window commit history, public demo video strictly <3 minutes, valid English PDF deck — all passing the P0-11 dry-run ≥2 days before 18 Oct 2026.

---

## 13. Guardrail principle (the one rule above all)

**Do not claim certainty the video does not give.**

Every feature derives from that rule: timestamps and quotes on answers, the confidence and uncertainty fields, the not-found path, the separation of observation from interpretation, the contradiction panel showing *both* statements instead of picking a winner, and (if built) the strict separation of any external context. When trade-offs arise — a flaky answer that *looks* confident vs. an honest miss — the product stays honest. The product's credibility **is** the trust design.




