# Product Definition — ContextBridge

**Theme:** Media, Content & Digital Experiences
**Owner doc:** `context/PRODUCT.md`; **requirements** live in `context/REQUIREMENTS.md`.
**Status:** aligned to `context/IDEA_REVIEW.md` — ContextBridge selected with three binding amendments (contradiction surfacing, tangible artifact, risk hardening).
**References:** architecture in `context/ARCHITECTURE.md`, API contract in `context/API.md`, build plan in `context/BUILD_PLAN.md`. This file is the product spec, not a build plan. (The early draft `docs/contextbridge-build-plan.txt` was fully superseded and removed — `context/DECISIONS.md` D-10.)

---

## 1. Name & Vision Line

**ContextBridge**

> **Vision Line:** "Not a tutor. A compass for self-learners — every answer anchored to the video you chose, in your language, with proof, and honest about where the video ends."

### The Three Pillars (Priority Order)
1. **P1 — Anchored:** The student's chosen video is the source of truth. Video answers must come strictly from the video, verified against its transcript, with a clickable timestamp.
2. **P2 — Proof:** Trust must be visible. Every answer shows what world it came from (video / web-beyond / honestly not covered) and its evidence is one click from the exact video moment. Video and web evidence are never blended.
3. **P3 — Boundary Honesty:** When curiosity steps beyond the video, the companion says so clearly and offers labeled web research — the boundary is a designed feature, not a failure.

**Secondary Identity:** Multilingual self-learner — Hindi and English first-class, code-mixed (Hinglish) input supported, answers delivered in the language the learner thinks in.

Tagline (deck only):
> *A compass for self-learners: Turn long video into anchored, verifiable, multilingual knowledge.*

---

## 2. One-line pitch

A compass for self-learners that anchors every answer to the video you choose with verbatim quotes and clickable timestamps, speaks your language (English & Hindi), and honestly marks the boundary with labeled external research when you step beyond.

---

## 3. Problem

Important knowledge is locked in long recordings — technical tutorials, lectures, deep-dives, coding walk-throughs. Self-learners face a painful dilemma: watch the whole 45 minutes or risk missing crucial context.

Worse, generic AI chatbots fail self-learners in three fatal ways:
1. **Fabricated certainty:** Chatbots invent plausible quotes and hallucinate timestamps, destroying learner trust.
2. **Opaque sourcing:** Learners cannot tell if an answer came from their trusted instructor or from arbitrary model weights.
3. **Language & literacy barriers:** Many self-learners in JAPAC think in Hindi or Hinglish, but tutorials are recorded in English (or vice versa) without verifiable audio-first navigation.

A generic chatbot summarizes. ContextBridge acts as an **exploratory compass**: it anchors answers to the actual video, visibly proves them, guides exploration from the video's own concepts, and honestly refuses to pretend the video said what it didn't.

---

## 4. Target users

**Primary (the hackathon prototype):**
- **Self-directed learners & students** navigating complex video tutorials (coding, technical, domain-specific) who need exact, verifiable answers fast.
- **Vernacular & multilingual learners** (JAPAC / India) who understand technical concepts better when explained in Hindi or conversational Hinglish with audio narration.
- **Visual & auditory learners** who learn by jumping between video moments, transcripts, and spoken explanations.

**Scale story (deck only):**
- Technical documentation & developer platforms adding video knowledge indexing.
- Continuous learning & enterprise onboarding.
- Accessibility-first educational hubs.

---

## 5. Solution (what it actually does)

ContextBridge ingests a video once and transforms it into an **anchored, verifiable exploration workspace**:

1. **One-pass multimodal indexing:** Analyzed with Gemini 2.5 Flash on Vertex AI into a validated `MediaAnalysis`: summary, topics, chapters, exact transcript, and confidence-scored events.
2. **Visual Proof & EvidenceBadge:** Every answer visibly identifies its source world (`✅ Verified from this video · 96%`, `🌐 Beyond this video`, or `🤷 Not covered`).
3. **Interactive TranscriptSync:** Clicking an evidence quote or timestamp seeks the video player to the exact second and highlights/auto-scrolls the transcript row.
4. **ExploreSuggestions:** After every answer, the companion suggests 2–3 "Explore from here →" paths derived from the video's own unasked concepts and chapters.
5. **BoundaryCard for Web Beyond:** Stepping beyond the video triggers an explicitly framed external research card with verified source citations — never blended into video claims.
6. **Bilingual Voice Loop:** Learners can speak and listen in English, Hindi, or Hinglish with native Gemini multimodal transcription and language-matched TTS.
7. **Contradiction Surfacing:** Identifies conflicting claims within the video with dual clickable timestamps so learners can inspect nuance.


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

Why this is not "just a Gemini video demo" or "another AI tutor," stated as product facts:

- **A Compass, Not a Tutor:** We do not lecture or replace the creator. We provide an orientation tool that anchors every answer to the learner's chosen video, guides exploration, and admits boundaries.
- **Evidence as a First-Class Citizen:** Every video answer carries verbatim quotes and exact clickable timestamps that seek the player. The anti-fabrication gate (`quote_matches_transcript`) structurally prevents hallucinated citations.
- **Visible Trust Worlds (EvidenceBadge & BoundaryCard):** The UI immediately signals where an answer originated (`✅ Verified from this video · 96%` vs `🌐 Beyond this video` vs `🤷 Not covered`). Video and web evidence are never blended into an ambiguous slurry.
- **Exploration Anchors (ExploreSuggestions):** Guides curiosity by suggesting 2–3 next-question chips derived from the video's own unasked chapters and concepts, rather than generic open-ended chatbot prompts.
- **Boundary Honesty as a Feature:** Out-of-video questions trigger explicit, honest recognition. When external research is enabled, it presents verified Google Search grounding in a dedicated `BoundaryCard`. Refusal is not a failure; it is the trust anchor.
- **Contradiction Surfacing Over One Index:** A secondary analytical pass over the stored index reveals contrasting statements without duplicate video calls.
- **Vernacular First-Class (Hindi/English/Hinglish):** Full bidirectional voice loop powered by native Gemini multimodal audio transcription and speech synthesis in the learner's native tongue.
- **Measured Quality:** Performance is proven by reproducible evaluation scorecards (`eval_results.json`) measuring citation accuracy, groundedness, honest refusal rate, and latency.

**Positioning line for the deck:**
> *"Every other tool tries to tutor you with generic summaries and unverified AI claims. ContextBridge is a compass: every answer is anchored to your video, verified with proof you can click, spoken in your language, and completely honest about where the video ends."*

---

## 10. Core features (The Compass Architecture)

**Tier 1 — MVP & Winning Foundation (All active and verified):**

- **Fixture-first intake & live upload:** Pre-analyzed sample video (`demo-binary` synchronized to Tokyo Night videography) plus live upload pipeline via Gemini 2.5 Flash on Vertex AI (P0-2, P0-6).
- **Schema-validated multimodal indexing:** `MediaAnalysis.from_dict` validation gate enforcing chapters, confidence scores, and verbatim transcripts.
- **Visual EvidenceBadge & Trust Indicators:** Immediate badge display (`✅ Verified from this video · 96%`, `🌐 Beyond this video`, `🤷 Not covered`).
- **TranscriptSync:** Interactive transcript panel with real-time active segment highlighting and smooth auto-scroll on evidence click.
- **ExploreSuggestions ("Explore from here →"):** 2–3 exploration chips under each answer derived from video topics and chapters.
- **BoundaryCard for Web Research:** Formatted external research container with live Google Search citations for questions beyond the lesson.
- **Multilingual Voice Loop:** Real audio speech-to-text via Gemini `/transcribe` endpoint + browser `speechSynthesis` with language-matched voices (`hi-IN` / `en-US`).
- **Teaching Moves (Clarify & Simplify):** Support for beginner simplification ("samajh nahi aaya") with analogy explanations and fast query handling.
- **Contradiction Surfacing Card:** Conflicting claim pairs with dual clickable jump buttons (P0-4).
- **Evaluation Harness v2:** Automated 25-question evaluation suite covering in-video, out-of-video, Hindi, and contradiction queries.

---

## 11. Non-goals

Explicitly **not** ContextBridge, for this hackathon:

- **Not a replacement tutor:** No prescriptive grading, curriculum design, or claiming to know more than the video creator.
- **Not an open-domain chat assistant:** Does not converse loosely on unrelated topics; out-of-video queries trigger boundary honesty or labeled web research.
- **Not a video rendering / editing suite:** No video re-encoding, clipping exports, or ffmpeg heavy video modifications.
- **Not a complex multi-tenant enterprise system:** No auth walls, user databases, billing, or permission trees.
- **No unverified answers:** No answer is presented as video truth unless it passes the strict quote-matching gate.

---

## 12. Success criteria (The Winning Scorecard)

**Product success (what we demo in 90 seconds):**

1. **Orientation (10s):** Landing page immediately communicates "Compass for self-learners, not a tutor."
2. **Anchored Exploration (20s):** Ask a question $\rightarrow$ answer with quote $\rightarrow$ click evidence button $\rightarrow$ video seeks and transcript scrolls to exact second.
3. **Compass Suggestions (15s):** Click an "Explore from here →" chip to navigate video concepts.
4. **Boundary Honesty (15s):** Ask an out-of-video question $\rightarrow$ visible `BoundaryCard` with real Google Search sources and "stepped beyond this video" notice.
5. **Language & Voice (15s):** Voice question in Hindi $\rightarrow$ natural Hindi answer + audio read-aloud.
6. **Proof of Quality (15s):** Show eval scorecard with 100% verified citation rate, 78 green tests, and decision history.

**Measurable success targets:**
- **In-video verified-citation rate:** 100% (enforced by gate).
- **Correct-branch rate:** $\ge 92\%$.
- **Honest-refusal appropriateness:** 100% of out-of-video queries properly labeled or refused.
- **Language fidelity:** $\ge 95\%$ of Hindi/Hinglish queries answered in matched language.
- **p95 question latency:** $\le 8$ seconds.
- **Test suite:** 78 baseline tests passing + new coverage with zero regressions.

---

## 13. Guardrail principle (The Compass Pledge)

**Do not claim certainty the video does not give. The boundary is a feature, not a failure.**

Every feature derives from that pledge: verbatim quotes, strict timestamp validation, explicit refusal when context is missing, distinct visual framing for external research, and dual-perspective contradiction surfacing. Credibility is our moat.





