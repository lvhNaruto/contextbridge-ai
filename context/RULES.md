# Rules, judging, and submission

**Status:** compiled from official pages and Terms accessible on 2026-09-23. Where official pages conflict, the conflict is preserved.

## Judging criteria

The same criteria apply to all six themes:

| Criterion | Weight |
|---|---:|
| Technical Merit & Gen AI Implementation | 40% |
| Problem Alignment & Impact | 25% |
| Innovation & Creativity | 25% |
| User Experience & Solution Design | 10% |

The FAQ says there is a scoring round before the Grand Finale. The judging panel had not yet been announced.

## Technology and prototype rules

- Submit a **working prototype**, not only a concept or pitch.
- The prototype must demonstrate the idea end-to-end and be deployed on **Cloud Run, GCP, or Firebase**.
- The solution must use Google Cloud's technology stack; solutions built primarily on another cloud platform are not eligible.
- The requirements identify Google AI models/tools including **Gemini**, **Gemma**, **Agent Platform**, **Antigravity**, and **AI Studio**. No specific model versions are published.
- Only fresh projects built during the hackathon timeline are eligible. Pre-existing or previously started projects are not eligible.
- All submission materials, code, documentation, and presentations must be in English.

## Required submission package

The official pages require:

1. A solution deck/proposal explaining the vision, problem, user/community benefit, feasibility, and scalability; the requirements page specifies PDF format.
2. A working deployed prototype and its URL.
3. A public video link (YouTube, Vimeo, or public Google Drive).
4. A public GitHub repository containing the source code.

### Video length discrepancy

The requirements page says **3 minutes**; the FAQ and Terms say **under three minutes**. Use a video strictly under three minutes unless the organizer confirms otherwise.

## Eligibility, teams, and conduct

- Participants must be 21+, working professionals/entrepreneurs/startups, and based in JAPAC.
- Students are ineligible; a student on a team can disqualify the entire team.
- Teams must have 2–4 members during building. Only two shortlisted members may attend the finale.
- One participant may register with only one team and submit one solution under one theme/problem statement.
- Roster changes are allowed only while registration is open. The FAQ/Terms say that window closes 4 Oct; the overview says 11 Oct.
- Registration and participation are free.
- Organizers may verify government ID, employment credentials, and age.
- Organizers may require use of official communication channels such as Slack, Discord, Telegram, or WhatsApp.
- Submissions must be original or properly licensed and free of malware. Unlawful, infringing, malicious, defamatory, hateful, harassing, or otherwise objectionable content is prohibited.
- Organizer/judge decisions are final. The organizer may cancel, postpone, or change date, venue, or time.
- Prizes are non-transferable; the Terms state payment within 60 days, subject to applicable TDS.

## Finale travel terms

- Only two members per team may attend, even at their own expense.
- FAQ: sponsorship includes flights, stay, and meals on the day of the Grand Finale; detailed information is to be shared with shortlisted teams.
- Terms: sponsorship for two representatives includes economy flights, accommodation, and designated event-day meals. Visa procurement and other ancillary expenses are the attendee's responsibility.
- Flights are booked in each traveler's name and last-minute substitutions are not accommodated.

## Rights and licensing

The Terms grant the organizer broad rights to use submitted content and related marketing content, and include a six-month right of first refusal for an exclusive license/acquisition after the hackathon. Review the [full Terms](https://docs.google.com/document/d/e/2PACX-1vRm7ChZ6Ij9fG7uFDkxzUMpwgVeBmnQ6cMDnAIEEX84AiLBOOQ9cYbl3S5OzFBbcVb8TF55s-eVpiXb/pub) before submitting proprietary work.

## Unresolved official inconsistency

An older/leftover requirements item reportedly names Healthcare, Education, Sustainability, Accessibility, and Social Good, which conflicts with the current six-theme page. The current themes page is the authoritative accessible challenge list; the older list is **unverified as current**.

## Development rule

Whatever changes or whatever decision we take that affects the code, we have to document it somewhere. Somewhere is this `context/DECISIONS.md` file.

---

## Engineering & Product Guardrails (The Compass Era)

### 1. The Vision Line (Core Invariant)
> **"Not a tutor. A compass for self-learners — every answer anchored to the video you chose, in your language, with proof, and honest about where the video ends."**

Every product, architectural, and code decision must strictly serve this vision line.

### 2. The Three Pillars (Priority Order)

| Pillar | Meaning | Invariant (Never Violate) |
|---|---|---|
| **P1 — Anchored** | The student's chosen video is the source of truth. Video answers must come from the video, verified against its transcript, with a clickable timestamp. | **Never weaken quote_matches_transcript / validate_answer_draft** — the anti-fabrication gate is the company. |
| **P2 — Proof** | Trust must be visible: every answer shows what world it came from (video / web-beyond / honestly not covered) and its evidence is one click from the exact video moment. | **Never blend video and web evidence in one answer** (`notInVideo: true` invariant stands). |
| **P3 — Boundary Honesty** | When curiosity steps beyond the video, the companion says so clearly and offers labeled web research — the boundary is a designed feature, not a failure. | **Never silently degrade** — the user must always know which branch answered. |

**Secondary Identity:** Multilingual self-learner — Hindi and English first-class, code-mixed (Hinglish) input supported, answers in the language the learner thinks in.

### 3. Standing Rules for Every Task
1. **The gate is sacred:** `quote_matches_transcript`, timestamp-range validation, and `MediaAnalysis.from_dict` must never be weakened — only extended in coverage.
2. **Governance first:** Every UI addition must have a `DECISIONS.md` entry (D-XX) answering the seven checks before code is touched. No ad-hoc UI edits.
3. **Tests before and after:** Every backend change ships with pytest coverage; all 78 baseline tests must pass before and after every task. Frontend lint + build (`npm run build`) is a mandatory gate for every `web/` change.
4. **Deployable at all times:** Every task ends with a green pytest + green `npm run build` + a deployable revision. No long-lived broken states.
5. **Wire format contract:** camelCase wire format everywhere on the external interface; snake_case only inside internal Python logic.
6. **No compromise on quality:** Never cut corners or omit tests for speed. Maintain clean architecture and strict type safety throughout.

### 4. What the Model Must Not Do
- ❌ **No new pages, routes, or navigation items** (the Next.js page topology is locked).
- ❌ **No new API endpoints** (additive optional fields on existing endpoints only; zero breaking changes).
- ❌ **No auth, payments, multi-tenancy, Postgres, or heavy queues** (post-hackathon backlog).
- ❌ **No weakening of gates:** quote verification, timestamp boundary checks, honest fallbacks, round budget ($\le 2$ LLM calls), `notInVideo` invariant.
- ❌ **No restyling of locked components** — only new small, focused additive components in `web/components/`.
- ❌ **No new external library dependencies in `web/`** except zero-dep utilities.
- ❌ **No backend dependency churn** unless strictly required; keep the provider ladder intact.
- ❌ **Never deploy without verification:** green pytest $\rightarrow$ green `npm run build` $\rightarrow$ `sweep_deployed.py` pass.

