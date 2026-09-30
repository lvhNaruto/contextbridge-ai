# MEDIA_PLAN.md
Product: Context Bridge
Event: BHARAT AGENTIC 2026 (aiKart) — EdTech & Future Skills
Deadline (internal): 1 Oct 2026, 18:00 IST
Length: 3:00–4:00
YouTube to replace: https://youtu.be/z5w-Mze7RCw
Live app: https://contextbridge-web-c5ltxo3mkq-uc.a.run.app/
GitHub: https://github.com/lvhNaruto/contextbridge-ai

## Lesson video (MUST be official Google)

Do NOT use the old Pixel / Japanese Google Ads clip as the hero lesson.
It looks like a product ad, not a student learning session.

### Primary (use this)
- Title: Google for Education 101 (in 101 seconds)
- Channel: Google for Education (official)
- Length: 1:42
- URL: https://www.youtube.com/watch?v=uXFUl0KcIkA
- Why: short, clearly educational, Google-owned, enough spoken content for chapters + Q&A + “not in video”

### Backup if upload/YouTube ingest fails
- Drive and Docs: Basics — https://www.youtube.com/watch?v=ejp-MaWxgMA (5:36, Google for Education)
- What is Cloud Storage? (Google Cloud Tech whiteboard) — https://cloud.google.com/blog/topics/developers-practitioners/picture-10-whiteboard-sketch-videos-bring-google-cloud-life
- Gemini in Vids product demo — https://www.youtube.com/watch?v=fNAVFeP1laM (1:07, Google for Education)

Download path for Cursor / local:
1. Open the Primary URL on YouTube.
2. Use YouTube “Share” only as the source of truth for judges.
3. If the app needs a file upload, download the official video with a tool you already use, or paste the YouTube URL if Context Bridge accepts URLs.
4. Keep attribution on screen: “Lesson video: Google for Education.”

## Demo story (agent loop)

Problem: Bharat students watch one-way lectures and cannot ask the teacher.
Agent: Context Bridge understands the video, answers only from it, jumps to proof, and says so when the answer is not in the video.

Must show on camera:
1. Ingest / chapters / transcript
2. In-video question + Evidence badge + timestamp jump
3. Hindi (text or voice)
4. Off-video question + BoundaryCard (not a fake quote)
5. Explore chips OR contradiction if the lesson surfaces them
6. End card: Context Bridge + live URL + GitHub

Do not show: Docker, Cloud Run architecture slides, test counts, Cursor.

## Scene list for recording (silent walkthrough, 5–6 min raw)

| # | Clock in final video | Operator clicks | Say later in VO |
|---|----------------------|-----------------|-----------------|
| 0 | 0:00–0:20 | Home page only | Problem + promise |
| 1 | 0:20–0:45 | Upload / or open demo lesson using Google for Education 101 | Agent reads the video |
| 2 | 0:45–1:15 | Wait for chapters + transcript | Ground truth is the lesson |
| 3 | 1:15–1:55 | Ask an IN-video question (see bank) → click evidence → player jumps | Proof in one click |
| 4 | 1:55–2:25 | Switch Hindi, ask one Hindi question | Built for Bharat |
| 5 | 2:25–2:50 | Click an Explore chip if visible | Agent plans next learning |
| 6 | 2:50–3:25 | Ask an OUT-of-video question with web research ON | Boundary honesty |
| 7 | 3:25–3:45 | End card | Live URL + GitHub |

## Question bank (tied to Google for Education 101)

Adjust wording to match the actual transcript after ingest.

IN-video (must be answerable from that clip):
- What is Google for Education?
- Which Google tools does this video mention for classrooms?
- What problem is Google trying to solve for teachers and students?

OUT-video (must NOT be in the 101-second clip):
- What is the current prize pool of BHARAT AGENTIC 2026?
- How do I apply for a government scholarship in India?
- What is the latest Gemini model name in 2026?

Hindi:
- Google Classroom kya karta hai?
- Is video ke mutabik students kaise seekhte hain?

If a question fails live, cut it. Never fake the badge.

## Recording rules
- 1920×1080, browser zoom 100–110%
- Clean desktop, no extra tabs
- Do not talk while recording (VO added in Supademo)
- Pause 2 seconds after each answer appears
- If a feature errors, stop that take and skip the scene

## Pipeline
1. Record silent walkthrough
2. Import to Supademo (free credits)
3. Paste voiceover from SCRIPT section (to be locked next)
4. Export MP4
5. Replace YouTube z5w-Mze7RCw
6. Stop by 18:00 IST on 1 Oct

Fallback if Supademo credits fail: raw MP4 + Grok Voice + captions.

## Cursor instructions
- Do not change product code unless a demo-blocking bug appears
- Do not invent features
- Prefer the Google for Education 101 video as the in-app lesson
- If you update files, note them in CHANGELOG
- Human approves the final video before YouTube replace
