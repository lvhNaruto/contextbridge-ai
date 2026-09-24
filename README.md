# ContextBridge AI 🧭

> **"Not a tutor. A compass for self-learners — every answer anchored to the video you chose, in your language, with proof, and honest about where the video ends."**

[![Cloud Run Backend](https://img.shields.io/badge/Google_Cloud_Run-Backend_Live-4285F4?logo=googlecloud&logoColor=white)](https://contextbridge-api-c5ltxo3mkq-uc.a.run.app/health)
[![Cloud Run Web](https://img.shields.io/badge/Google_Cloud_Run-Frontend_Live-34A853?logo=googlecloud&logoColor=white)](https://contextbridge-web-c5ltxo3mkq-uc.a.run.app)
[![Gemini 2.5 Flash](https://img.shields.io/badge/AI_Engine-Gemini_2.5_Flash-orange?logo=googlegemini&logoColor=white)](https://ai.google.dev/)
[![Eval Benchmark](https://img.shields.io/badge/Eval_Harness_V2-94.4%25_Accuracy-blueviolet)](context/eval_results.json)
[![Zero Hallucination](https://img.shields.io/badge/Unsupported_Answers-0.0%25_Strict-brightgreen)](context/eval_results.json)
[![Next.js 16](https://img.shields.io/badge/Next.js-16_(Turbopack)-black?logo=next.js&logoColor=white)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Tests Passing](https://img.shields.io/badge/pytest-83%2F83_Passing-success)](tests/)

---

## 🌟 Live Deployments

- 🖥️ **Live Web Application:** [https://contextbridge-web-c5ltxo3mkq-uc.a.run.app](https://contextbridge-web-c5ltxo3mkq-uc.a.run.app)
- ⚡ **Backend API Interactive Docs:** [https://contextbridge-api-c5ltxo3mkq-uc.a.run.app/docs](https://contextbridge-api-c5ltxo3mkq-uc.a.run.app/docs)
- 🩺 **Live Health & Metrics:** [https://contextbridge-api-c5ltxo3mkq-uc.a.run.app/health](https://contextbridge-api-c5ltxo3mkq-uc.a.run.app/health)

---

## 🎯 The Three Pillars of ContextBridge

ContextBridge transforms passive video watching into active, self-directed exploration. Built around three non-negotiable principles:

| Pillar | Meaning | Engineering Guarantee |
| :--- | :--- | :--- |
| **P1 — Anchored** | The student's chosen video is the sole ground truth. Video answers must come strictly from the video. | Verbatim transcript quote verification (`quote_matches_transcript`) and container-bounded timestamps. The anti-fabrication gate structurally prevents inventing quotes. |
| **P2 — Proof** | Trust must be visible in 10 seconds. Every answer shows where it came from. | `EvidenceBadge` displays trust level (`Verified from this video · 98%`). Clicking any evidence button seeks the video player to the exact second (~1s) and auto-scrolls `TranscriptPanel` to the spoken line. |
| **P3 — Boundary Honesty** | Refusal and external web research are explicit features, not bugs. | Answers outside the video never blend with creator statements. They receive a distinct `BoundaryCard` container (*"You've stepped beyond this video — external research, real sources"*) with live Google Search citations. |

---

## ✨ Key Features & Innovation Highlights

### 1. 🧭 The Compass: Guided Self-Exploration (`ExploreSuggestions`)
Underneath every response, ContextBridge derives 2–3 contextual *"Explore from here →"* clickable chips. These questions are calculated dynamically from remaining video chapters and topics with **zero extra LLM latency**, guiding curious learners through unexplored concepts.

### 2. ⚡ Live Transcript Synchronization (`TranscriptSync`)
Clicking any timestamp evidence jumps video playback directly to that moment, while the right-rail transcript panel smoothly scrolls the corresponding segment into view with glowing emerald highlighting.

### 3. 🔍 Contradiction Detection
ContextBridge analyzes tutorials for contrasting perspectives or conflicting statements within the same video (e.g., *natural low-light videography vs. computational Night Sight enhancement*), presenting side-by-side statements with dual interactive jump buttons.

### 4. 🌐 Distinct Boundary Card (`BoundaryCard`)
When curiosity steps beyond the uploaded video, ContextBridge activates Google Search grounding. The response is encapsulated in a dedicated card with external source links, keeping creator claims and web findings strictly separated.

### 5. 🎙️ Bilingual Voice Loop (English, Hindi & Hinglish)
- **Multimodal Transcription:** Uploaded audio or microphone input is transcribed in real-time using Gemini's native multimodal audio understanding (`POST /transcribe`).
- **Language-Matched TTS:** Read-aloud synthesis automatically matches student preference (`hi-IN` / `en-US`).
- **Interactive Avatar States:** Real-time visual feedback for listening, thinking, and speaking with animated waveform rings.
- **Instant Barge-In:** Tapping the microphone immediately cancels active text-to-speech for seamless interruption.

### 6. ♿ Accessible Output Modes
- **Adaptive Explanation Levels:** Switch seamlessly between `Beginner` (intuitive analogies), `Intermediate`, and `Expert`.
- **Client-Side WebVTT Captions:** Subtitle tracks generated on the fly from transcript timestamps.
- **Evidence Card Clipboard Export:** One-click copy formatted with timestamp, quote, and source citation.

---

## 🏗️ System Architecture

```
                          ┌───────────────────────────────┐
                          │   Next.js 16 Web Frontend    │
                          │   (Tailwind CSS v4 + Motion)  │
                          └──────────────┬────────────────┘
                                         │ HTTP / JSON / Audio
                                         ▼
                          ┌───────────────────────────────┐
                          │   FastAPI Backend (Cloud Run) │
                          │   api/main.py · Stateless     │
                          └──────────────┬────────────────┘
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        │                                │                                │
        ▼                                ▼                                ▼
┌──────────────────┐           ┌──────────────────┐             ┌──────────────────┐
│  Video Pipeline  │           │   Agent Engine   │             │   Audio Engine   │
│  api/pipeline.py │           │   api/agent.py   │             │   Gemini Native  │
│  Gemini 2.5 Flash│           │  3-Tool Bound    │             │  POST /transcribe│
└────────┬─────────┘           └────────┬─────────┘             └──────────────────┘
         │                              │
         │ Chapters, Transcript,        │ Observe: retrieve_video_context
         │ Contradictions               │ Evaluate: validate_answer_draft (Gate)
         ▼                              ▼
┌──────────────────┐           ┌──────────────────────────────────────────────────┐
│ In-Memory & Demo │           │ External Web Research                            │
│ Fixture Store    │           │ Google Search Tool (Grounding Chunks & Sources)  │
└──────────────────┘           └──────────────────────────────────────────────────┘
```

### The 3-Tool Agent Loop:
1. **`retrieve_video_context` (Deterministic, no LLM):** Lexical token matching + bounded Devanagari Unicode window fallback.
2. **`gemini_answer` (LLM + Anti-Fabrication Draft Gate):** Produces answer draft. The draft gate strictly validates start/end timestamps within $[0, \text{duration}]$ and ensures quotes match stored transcript segments verbatim. If invalid, allows exactly 1 retry; on failure, honestly reports `not_found`.
3. **`gemini_web_research` (Google Search Grounding):** Activates only when a question cannot be answered from the video and web research is enabled. Returns real Google Search sources with zero hallucinated URLs.

---

## 📊 Empirical Evaluation (25-Case Live Benchmark)

ContextBridge measures quality continuously using an automated 25-case benchmark harness (`scripts/eval_harness.py`) executed against the deployed Cloud Run instance:

| Metric | Target | Result on Live Cloud Run | Status |
| :--- | :---: | :---: | :---: |
| **Unsupported-Answer Rate** | `0.0%` | **`0.0%`** | 🟢 **Zero Hallucination** |
| **Timestamp Retrieval Accuracy** | $\ge 90.0\%$ | **`94.4%`** | 🟢 **Pass (17/18 in-video cases)** |
| **Groundedness Rate** | $\ge 90.0\%$ | **`92.0%`** | 🟢 **Pass (Verbatim quotes)** |
| **Explore Suggestions Coverage** | $\ge 90.0\%$ | **`100.0%`** | 🟢 **Pass (25/25 returned chips)** |
| **Average Q&A Latency** | $< 5.0\text{ s}$ | **`3.59s`** | 🟢 **Fast & Bounded** |

*Full evaluation artifact persisted at [`context/eval_results.json`](context/eval_results.json).*

---

## 🛡️ Architecture §15: Nine Failure-Path Drills

ContextBridge guarantees graceful degradation across all failure modes (`python scripts/test_failure_paths.py`):

1. **Analysis LLM Outage:** Status marked `failed`, cleanly isolated with `409 analysis_failed`.
2. **Q&A Outage vs. Unanswerable:** Unanswerable yields honest `200 unknown` (`notInVideo: true`); total LLM outage traps as structured `502 answer_failed`.
3. **Agent Loop Crash:** Trapped by top-level FastAPI exception handler into structured JSON.
4. **Web Search Failure:** Degrades to `declare_not_found`; zero sources or evidence invented.
5. **External API Quota Exhaustion:** Pre-seeded demo fixture (`demo-binary`) serves seamlessly from memory.
6. **Database Connection Loss:** Immediate fallback to in-memory seed; demo lesson remains 200 OK.
7. **Input Validation:** Rejects missing files (`400`), non-videos (`422`), oversized uploads >100MB (`413`), and invalid queries (`422`).
8. **Iteration Bound:** Agent iteration capped at 1 attempt before graceful unknown fallback (no infinite loops).
9. **Partial Analysis Isolation:** Incomplete analyses safely shielded from retrieval (`409 analysis_incomplete`).

---

## 💻 Quickstart & Local Development

### Prerequisites
- Python 3.11+
- Node.js 18+ (Node 20+ recommended)
- Google Cloud Project with Gemini API / Vertex AI access (or `GEMINI_API_KEY`)

### 1. Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add GEMINI_API_KEY or configure gcloud auth application-default login

# Run FastAPI dev server
uvicorn api.main:app --reload --port 8000
```
Backend will be available at `http://localhost:8000` (`/docs` for Swagger UI).

### 2. Frontend Setup
```bash
cd web
npm install
npm run dev
```
Frontend will be available at `http://localhost:3000`.

### 3. Verification & Quality Gates
```bash
# Run backend test suite (83 tests)
python -m pytest

# Run 9 failure-path drills
python scripts/test_failure_paths.py

# Lint & build frontend
cd web
npm run lint    # 0 errors, 0 warnings
npm run build   # Turbopack clean production build
```

---

## 🏆 Hackathon Context

- **Competition:** AI Builder Cup 2026
- **Theme:** Media, Content & Digital Experiences
- **Core Technology:** Google Gemini 2.5 Flash, Google Search Grounding, Google Cloud Run
- **Evaluation Criteria Alignment:**
  - **Technical Merit (40%):** Zero-hallucination anti-fabrication gate, verbatim transcript verification, sub-second video seeking, 83 passing tests, 9 failure drills.
  - **Impact (25%):** Empowers self-directed learners to master technical video content with proof, bilingual voice equity (Hindi/English), and accessibility.
  - **Innovation (25%):** Moves beyond passive summarizers into an active compass: dynamic exploration chips, contradiction surfacing, and boundary cards.
  - **UX & Polish (10%):** Micro-animations, responsive right-rail transcript sync, playback rate selector, and audio wave avatar states.

---

## 📄 License & Attribution

Built for the **AI Builder Cup 2026**. Video sample courtesy of Google Cloud Samples (`pixel8.mp4`). Licensed under the [MIT License](LICENSE).
