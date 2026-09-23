# ContextBridge web

Premium, production-quality frontend for ContextBridge — turn any
educational video into a conversation.

Built with Next.js (App Router), React 19, TypeScript, Tailwind CSS v4,
customized shadcn/ui-style primitives, Motion for product animation, and
GSAP reserved for the cinematic hero entrance.

## Run

```bash
npm install
npm run dev     # http://localhost:3000
npm run build   # production build
```

## Demo moment

1. Open the app and click **Try the demo lesson**.
2. Ask: **“What does binary language mean?”**
3. The answer is grounded in the video at 02:53 — click **Jump to 02:53**
   and the video seeks to the exact moment, the chapter becomes active,
   and the timeline shows the evidence marker.
4. Ask something the video doesn't cover (e.g. “What is quantum computing?”)
   to see the clearly-labelled **Web research** fallback with source cards.
5. Switch the answer language to **Hindi** and ask again.

## Architecture

```
app/                    routes (landing, /lesson/[id], /library, /help, /accessibility)
components/
  ui/                   customized shadcn-style primitives
  video/                VideoPlayer — custom controls + intelligent chapter timeline
  chapters/             ChapterList with active-state tracking
  chat/                 Conversation, AssistantMessage, QuestionInput (voice)
  evidence/             EvidenceBadge, TimestampButton, WebSourceCard
  upload/               UploadDropzone, AnalysisProgress
  library/              LessonCard
  settings/             LessonSettingsBar (language / level / research toggle)
  workspace/            WorkspaceClient — the learning workspace orchestrator
lib/
  api.ts                typed API layer — 1:1 with backend endpoints
  mock-data.ts          demo lesson (matches contextbridge_schema.py)
  demo-answers.ts       mock answer engine (video evidence vs web research)
  store.ts              localStorage persistence (lessons, conversation, settings)
  blob-store.ts         IndexedDB video storage for uploaded lessons
types/                  shared TypeScript contracts
hooks/                  useLocalStorage
```

## Connecting the real backend

`lib/api.ts` maps directly to the backend. Set the base URL and every
function switches from mock data to real requests — no UI changes needed:

```bash
# web/.env.local
NEXT_PUBLIC_API_BASE_URL=https://your-backend.example.com
```

Endpoints used:

- `POST   /analyses`                    — upload a video
- `GET    /analyses/:id`                — lesson, chapters, transcript
- `POST   /analyses/:id/questions`      — ask a question
- `POST   /analyses/:id/voice-question` — ask by voice
- `GET    /analyses/:id/chapters`       — chapters
- `GET    /analyses/:id/conversation`   — restore conversation history

Response shapes live in `types/index.ts` and intentionally mirror
`contextbridge_schema.py` (MediaAnalysis) so the Streamlit/Vertex backend
can be adapted without frontend rewrites.
