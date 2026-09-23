# Hackathon Idea Bank — AI Builder Cup 2026

**Created:** 2026-09-23
**Status:** Brainstorm only — **no winner selected yet**. This file combines the 20 newer ideas below with the earlier six-idea round preserved near the end.

This file contains **20 newer ideas** (Idea 1–20), generated from `context/HACKATHON.md`, `context/RULES.md`, and `context/RESOURCES.md`. The earlier six ideas are preserved in full in the combined section near the end.

## Constraints applied to every idea

- Deployable on **Cloud Run, GCP, or Firebase** (RULES.md).
- Uses **Google Cloud stack + Google AI** (Gemini / Gemma / Agent Platform / AI Studio) as the core, not a rival cloud.
- Fits exactly **one** of the six official themes (one team = one theme submission).
- **Working prototype**, not a concept — so every idea must be buildable with sample/synthetic data and no hardware or bank integrations.
- Judging weights used for self-scoring: Technical Merit & Gen AI 40%, Problem Alignment & Impact 25%, Innovation & Creativity 25%, UX & Design 10%.
- **Resource caveat:** RESOURCES.md confirms no cloud credits, API keys, or quotas have been published. Every "Data/API source" below assumes the team already has billing access to the named Google services — confirm via Discord/registration before committing.
- Agentic role is stated explicitly for each idea because "Technical Merit & Gen AI Implementation" (40%) rewards multi-step tool-using agents, structured outputs, and grounding — not a single prompt/response chatbot.

Complexity scale: **Low** (one surface, few integrations) → **Medium** (ingestion + agent + storage) → **Med-high** (multi-agent, evaluation, or strict safety gates) → **High** (real-time, many integrations, or heavy infra).

---

## BFSI: Intelligent Risk, Fraud & Financial Experiences

### 1. ClaimLens — Insurance claim intake & triage agent

- **Problem:** First-notice-of-loss claims arrive as messy photos, PDFs, free-text emails, and voice notes. Handlers spend hours re-keying data, chasing missing evidence, and checking coverage before any assessment begins.
- **Target user:** Small/mid insurers and third-party claims administrators; ultimately the policyholder waiting on a claim.
- **Solution:** Upload accident/damage photos, the policy document, and a voice description; ClaimLens extracts a structured loss summary, checks which evidence the policy requires, flags gaps, and drafts the handler's next request to the customer — every field linked to its source document/quote.
- **Agentic-AI role:** Multi-step agent: (a) classify claim type, (b) call Document AI to parse policy and forms, (c) call Gemini vision on damage photos, (d) validate against a coverage checklist tool, (e) emit a structured triage record with confidence + missing-item list. Human handler approves before anything is sent.
- **Data/API source:** Gemini (Vertex AI / AI Studio), Document AI, Cloud Storage for uploads, Firebase Auth + Firestore for case state; synthetic policy + crash-photo fixtures.
- **Core workflow:** Upload → extract policy terms → extract loss facts → gap analysis against required-evidence checklist → risk/confidence triage card → draft customer follow-up message.
- **Demo moment:** A deliberately incomplete claim (missing police report + blurry VIN) gets flagged in real time, with the agent showing the exact policy clause and photo region it used — then generating the chase-up email in the customer's language.
- **Build complexity:** Medium.
- **Major risk:** Implied coverage authority. The agent must be framed as intake/triage decision-support; no coverage determinations — handler sign-off required, and wording must never sound like a binding claim decision.
- **Why it fits this hackathon:** Direct BFSI fit (process automation + customer interaction), heavy use of Gemini document/vision understanding and structured output, demoable entirely on fixtures, deployable on Cloud Run + Firebase.

### 2. LoanReady — SME loan-readiness coach agent

- **Problem:** Small businesses abandon loan applications because they don't know which documents they qualify with, why they were rejected, or how to fix their cash-flow presentation. Banks lose good borrowers to drop-off.
- **Target user:** Micro/small business owners (JAPAC markets); banks' SME onboarding teams as the scale channel.
- **Solution:** The owner submits bank-statement PDFs, an existing rejection letter, and a photo of their ledger. LoanReady produces a readiness score, an itemized fix list ("3 months of statements missing; turnover inconsistent with declared revenue"), and a plain-language prep plan — plus a mock Q&A rehearsing what an officer will ask.
- **Agentic-AI role:** Planner/executor agent: parses documents (Document AI), computes simple financial ratios via a deterministic tool, asks Gemini to reason over ratios + documents with long context, then runs a bounded "interview rehearsal" sub-agent that asks follow-up questions and updates the readiness plan. Refuses to promise approval.
- **Data/API source:** Gemini long-context, Document AI, Cloud Storage; published central-bank/SME-loan eligibility guidelines as the grounding corpus; synthetic statements.
- **Core workflow:** Upload docs → extract + validate → ratio tool → gap/eligibility reasoning grounded on published guidelines → readiness score + fix plan → rehearsal Q&A → exportable prep checklist.
- **Demo moment:** A rejected applicant's file is re-run; the agent surfaces one contradictory number between the ledger photo and the statement, explains it in simple language, and shows the readiness score climb after the user supplies the fix.
- **Build complexity:** Medium.
- **Major risk:** Being mistaken for credit advice or an approval guarantee. Frame strictly as preparation/education, ground eligibility statements in published guidelines with citations, and display "not a lending decision" persistently.
- **Why it fits this hackathon:** BFSI theme (financial experiences + process automation), showcases Gemini long-context cross-document reasoning, measurable before/after impact story for the 25% impact score, no bank integration required.

### 3. ChargebackCoach — Card dispute evidence agent

- **Problem:** Consumers lose valid chargebacks because they can't articulate the reason code, gather evidence, or meet issuer deadlines; merchants lose them for the same reason in reverse.
- **Target user:** Consumers disputing a purchase (demo the consumer side; merchant side is the scale story).
- **Solution:** User pastes the transaction detail and merchant correspondence and uploads receipts/screenshots. Agent identifies the most applicable dispute reason, lists the evidence that issuers typically require, drafts the dispute letter, and tracks the response deadline.
- **Agentic-AI role:** Classification + tool-use agent: maps facts to a reason-code taxonomy (internal tool), retrieves evidence requirements, calls Gemini to draft a grounded letter citing only provided facts, sets a deadline task, and refuses to fabricate unsupported claims (explicit "evidence not found" path).
- **Data/API source:** Gemini structured output/function calling, Firebase for case storage; synthetic transaction + correspondence fixtures; publicly published scheme/issuer dispute rules as grounding text.
- **Core workflow:** Input transaction + correspondence → classify reason code → evidence checklist → gap detection → draft dispute letter with citations → deadline tracker → follow-up reminder.
- **Demo moment:** Agent declines to include a claim the user typed that isn't backed by any uploaded evidence, then explains what document would strengthen that point — trust behavior in one beat.
- **Build complexity:** Medium.
- **Major risk:** Encouraging fraudulent disputes or overpromising outcomes. Keep it evidence-bound, cite published rules, add a "not legal/financial advice" gate, and show the refusal behavior in the demo.
- **Why it fits this hackathon:** BFSI fraud/risk + customer interaction, clear agent tool-calling story, emotionally relatable consumer pain, fully fixture-based demo on Cloud Run/Firebase.

### 4. ScamDrill — Interactive scam-simulation training agent

- **Problem:** Awareness slides don't work; people (older adults, new digital-banking users, families) learn about scams only after losing money. Banks and communities need safe, personalized practice.
- **Target user:** Retail-bank customers (especially 60+), family caregivers, community groups; banks' financial-crime education teams as the scale channel.
- **Solution:** The user chooses a scenario (bank SMS, investment pitch, QR code, impersonation call). ScamDrill runs a safe, clearly labeled role-play conversation, lets the user practice verifying, and afterwards breaks down every manipulation tactic used, scoring responses and delivering a personalized defense checklist in their language.
- **Agentic-AI role:** Conversational role-play agent with a tactic-tracking state machine: selects a scenario script, adapts pressure tactics within hard safety rails (never requests real credentials/money), observes user responses, then switches to teacher mode producing a structured debrief with per-tactic scores. A guardrail tool blocks any real-world action.
- **Data/API source:** Gemini (conversational role-play + structured debrief), Firebase Auth/Firestore for progress; scam-pattern taxonomy derived from published consumer-alert bulletins (cited).
- **Core workflow:** Choose scenario → run bounded role-play → score responses against tactic checklist → debrief with evidence quotes → personalized checklist → optional family-member share.
- **Demo moment:** A judge plays along, "falls" for a fake QR tactic, and the debrief replays the exact message moment with the tactic named and the safe alternative shown — then the score improves on a second round.
- **Build complexity:** Medium (safety rails and state tracking are the work).
- **Major risk:** A simulation that leaks into real interaction or trains misuse. Mandatory "SIMULATION" banner, no real links/credentials, blocklist on tool calls, and a script-bounded scenario pool instead of free-form improvisation.
- **Why it fits this hackathon:** BFSI fraud/risk with a fresh angle versus analyzer-style ideas; strong emotional/demo memorability; clear agent + guardrail engineering that shows technical merit; accessibility and social-good crossover.

---

## Retail & Commerce: Intelligent Customer and Business Experiences

### 5. ShelfAudit — Planogram & compliance checker from phone photos

- **Problem:** Brand reps and small-store owners can't tell whether shelves match the plan, whether promo signage is up, or where stock is hidden — audits are manual, slow, and inconsistent.
- **Target user:** Small retailers and field merchandisers for consumer-goods brands.
- **Solution:** Take a shelf photo; ShelfAudit detects products, counts facings, compares against a target planogram image, and returns a compliance score with per-SKU gaps, missing signage, and a prioritized fix list the staff can execute on a phone.
- **Agentic-AI role:** Vision pipeline agent: Gemini vision segments the shelf, a matching tool compares detected facings to the target planogram, a reasoning step ranks fixes by sales impact, and a report tool emits structured JSON for the UI. Shows confidence per detection with manual-correction affordance.
- **Data/API source:** Gemini vision (image + image-pair reasoning), Cloud Storage, Firestore; synthetic shelf photos and planogram fixtures the team photographs themselves.
- **Core workflow:** Capture shelf photo + target planogram → detect/count SKUs → diff against target → compliance score → prioritized remediation list → before/after verification.
- **Demo moment:** Side-by-side "your shelf vs. target" with three SKUs highlighted as missing/misplaced; user fixes one shelf, re-photographs, and the score updates live.
- **Build complexity:** Medium.
- **Major risk:** Miscounting visually similar products. Show confidence, allow one-tap corrections, and avoid claiming audit-grade accuracy — position as assistive with human confirmation.
- **Why it fits this hackathon:** Retail theme (discovery, inventory, customer insights), visually immediate demo for the 10% UX score, pure Gemini vision — no POS/ERP integration, fixture-friendly for a working prototype.

### 6. ReturnSense — Return-fraud and restock decision agent

- **Problem:** Retailers absorb costly return fraud and make poor restock/dispose decisions because return reasons are free-text, evidence is inconsistent, and staff lack time to investigate.
- **Target user:** Small/mid e-commerce and brick-and-mortar retail operations teams.
- **Solution:** User submits the return reason text, product photos, and order details. ReturnSense classifies fraud signals vs. legitimate complaints, determines restock/refurb/dispose, and drafts the customer response — with the reasoning and evidence shown.
- **Agentic-AI role:** Multi-tool agent: parses order/return inputs, runs a policy-lookup tool, calls Gemini vision on product-condition photos, applies a rules tool for restock thresholds, and produces a structured disposition record with confidence and escalation flag for borderline cases.
- **Data/API source:** Gemini structured output + vision, Firebase for case queue, Cloud Storage for photos; synthetic return fixtures and a published returns-policy document.
- **Core workflow:** Ingest return bundle → extract facts → policy + condition check → fraud-signal scoring → disposition recommendation (restock/refurb/hold) → customer reply draft → human review queue.
- **Demo moment:** Two near-identical returns arrive; one is cleared for instant refund, the other is held because the photo shows mismatched wear — the agent explains the deciding evidence side by side.
- **Build complexity:** Medium.
- **Major risk:** False fraud accusations against real customers. Never label a customer fraudulent — use neutral signal language, require human approval on holds, and show confidence + appeal path.
- **Why it fits this hackathon:** Retail theme (fraud + business experiences), combines vision + policy reasoning in one agent, measurable cost-savings story, safe on fixtures without live commerce systems.

### 7. ShelfNudge — Demand-aware reorder & markdown coach

- **Problem:** Small retailers over-order, stock out, or waste near-expiry goods because they can't forecast demand from messy sales files and local events.
- **Target user:** Independent grocery/pharmacy/deli owners.
- **Solution:** Upload a sales CSV, current stock list, and note an upcoming local event. ShelfNudge forecasts the next week, flags stockout/overstock risk per item, suggests order quantities and markdown timing, and explains each recommendation in plain language the owner can override.
- **Agentic-AI role:** Analysis agent with a deterministic forecasting tool: computes baseline demand externally, then Gemini reasons over forecast + stock + event context via function calling, adjusts for confounders, and returns structured reorder/markdown actions with confidence and an explanation chain.
- **Data/API source:** Gemini function calling + structured output, Firestore for item state; sales CSV fixtures, public holiday/event calendar; (optional) BigQuery for aggregate analytics story.
- **Core workflow:** Upload sales + stock → baseline forecast tool → incorporate event context → risk scoring → reorder/markdown plan → owner accepts/edits → results feed back into next forecast.
- **Demo moment:** Owner adds "street fair this Saturday"; the agent raises the weekend order for two SKUs and schedules a markdown on a near-expiry item, each with a one-line reason the owner can see.
- **Build complexity:** Medium.
- **Major risk:** Forecasts presented as certainties. Label as estimates with ranges, keep the human in the loop for every order, and seed with realistic sample data so demo numbers hold up.
- **Why it fits this hackathon:** Retail theme (demand planning, inventory, customer insights), clear tool-calling + human-in-the-loop pattern, no POS integration needed, strong small-business accessibility angle.

---

## Manufacturing: Intelligent Operations & Industrial Efficiency

### 8. ShiftHandover — Shift-change briefing & risk agent

- **Problem:** Critical machine status, unfinished fixes, and safety notes are lost at shift change because handovers happen verbally or on paper; the incoming shift starts blind.
- **Target user:** Plant supervisors and shift leads in small/mid manufacturing facilities.
- **Solution:** The outgoing operator dictates a voice note and snaps photos of the line. ShiftHandover converts it into a structured handover: open issues, machine states, safety holds, and a prioritized watch list for the incoming shift, each item linked to its source audio second or photo region.
- **Agentic-AI role:** Ingestion + structuring agent: speech-to-text, Gemini vision on photos, a reasoning step that cross-references the previous handover to detect what changed or was forgotten, then a report tool that emits a signed handover record and flags unresolved safety items for supervisor confirmation.
- **Data/API source:** Gemini (audio + vision, long context across prior handovers), Cloud Storage, Firestore for handover history; synthetic voice notes and machine photos.
- **Core workflow:** Voice + photo input → transcribe/see → extract issues & machine states → diff vs. previous shift → structured handover with evidence links → supervisor signs off → incoming shift sees watch list.
- **Demo moment:** The agent catches a safety hold mentioned in audio but not in the written log, flags it at the top of the incoming shift's list with the exact quote, and shows the diff against the previous handover.
- **Build complexity:** Medium.
- **Major risk:** Presenting it as a safety-critical system it isn't. Frame as briefing support with mandatory supervisor sign-off; never auto-clear a safety item.
- **Why it fits this hackathon:** Manufacturing theme (efficiency, reliability, operational-data insights), distinctive multimodal (voice + photo) demo, evidence-linked structure mirrors proven patterns, no PLC/hardware access needed.

### 9. DefectDesk — Visual defect triage & trend agent

- **Problem:** Small manufacturers rely on human visual inspection; defect photos and notes live in chats, so recurring root causes are never spotted and rework climbs.
- **Target user:** Quality inspectors and plant engineers in small/mid factories.
- **Solution:** Snap a photo of a part or product; DefectDesk classifies the defect type and severity, compares it to a known-defect library, records it, and surfaces weekly trends ("scratch defects up 40% on Line 2 after the new tooling").
- **Agentic-AI role:** Vision + analysis agent: Gemini vision classifies and describes the defect with a confidence score, a tool matches against the defect taxonomy, a storage tool appends the record, and a weekly analysis step reasons over accumulated records to produce ranked probable causes — always labeled as hypotheses for humans to verify.
- **Data/API source:** Gemini vision + structured output, Firestore/BigQuery for defect history, Cloud Storage for images; team-captured sample part photos as fixtures.
- **Core workflow:** Capture defect photo → classify + severity → match to taxonomy → log record → aggregate over time → trend/hypothesis report → engineer reviews and annotates.
- **Demo moment:** After logging five sample defects, the dashboard reveals a cluster tied to one line, and the agent proposes a ranked cause list with the supporting image thumbnails a judge can click.
- **Build complexity:** Medium.
- **Major risk:** Wrong classification eroding trust, and root-cause claims overreach. Show confidence, allow inspector correction, and present causes as ranked hypotheses — never conclusions.
- **Why it fits this hackathon:** Manufacturing theme (quality, operational insights), strong before/after analytics story on the 40% technical score, works fully on self-captured fixtures.

### 10. ToolBoxTalk — Machine-documentation & SOP Q&A assistant

- **Problem:** Technicians waste time hunting through PDF manuals, SOPs, and old work orders to answer "how do I set this up / what's the torque spec / what does this error mean?"
- **Target user:** Maintenance technicians and new-line operators.
- **Solution:** Ask a question by text or voice against the facility's uploaded manuals and SOPs; ToolBoxTalk answers with the exact document section and page, shows the page snippet as evidence, and can generate a step checklist or a short refresher card.
- **Agentic-AI role:** RAG agent with a retrieval tool over document chunks: retrieves candidate sections, Gemini answers strictly from retrieved context with citations and an explicit "not in the docs" fallback, then a generation tool formats the answer as steps/checklist. Follow-up questions keep the retrieval session context.
- **Data/API source:** Gemini + a retrieval tool (Vertex AI Search or an embedded store), Cloud Storage/Document AI for manual ingestion, Firebase for sessions; public equipment manuals as fixtures.
- **Core workflow:** Ingest manuals/SOPs → chunk + index → ask question → retrieve → grounded answer with page evidence → optional checklist/refresher export → "not found" fallback.
- **Demo moment:** Technician asks a spec question; answer cites the exact manual page with the snippet highlighted — then asks an off-document question and the system honestly replies "not in your manuals," proving grounding.
- **Build complexity:** Low-medium (RAG is well-trodden; depth comes from UX).
- **Major risk:** Being dismissed as "just another doc chatbot." Differentiate with strict citation UI, the refusal demo, and checklist/task outputs rather than prose answers.
- **Why it fits this hackathon:** Manufacturing theme (efficiency, knowledge access), fast path to a reliable working demo, clear grounding evidence for technical merit, easy Cloud Run deployment.

---

## Media, Content & Digital Experiences

### 11. StorySplice — Evidence-linked highlight & clip agent

- **Problem:** Producers and creators drown in long footage; finding the strongest, quotable, correctly-attributed moments for a trailer, recap, or short takes hours of scrubbing.
- **Target user:** Podcast/video producers, newsrooms, creator teams, corporate comms.
- **Solution:** Upload a long recording; StorySplice returns ranked highlight candidates with timestamps, speaker, a one-line hook, and the transcript quote that justifies each pick — then assembles a short vertical cut with captions in the chosen language.
- **Agentic-AI role:** Orchestration agent: analyzes the full video (chapters, speakers, energy beats), a scoring tool ranks highlight candidates on criteria (novelty, emotion, quotability), Gemini writes hooks strictly from the quoted transcript, and an assembly tool produces the clip package with captions.
- **Data/API source:** Gemini video/audio understanding with timestamps, Cloud Storage, Text-to-Speech (already in requirements) for narration; sample long-form footage the team licenses.
- **Core workflow:** Upload long video → chapter/speaker analysis → candidate scoring tool → ranked highlights with transcript evidence → pick one → generate captions + hook + vertical cut → export.
- **Demo moment:** A judge picks one ranked highlight, and the panel plays the 30-second cut with captions while showing the exact transcript line and timestamp it was derived from — proving it wasn't cherry-picked arbitrarily.
- **Build complexity:** Medium-high (video assembly adds work; can defer full render to metadata + player cuts).
- **Major risk:** Licensed-content and copyright issues, and hooks that misrepresent the source. Use owned/licensed footage only, and show the source quote beside every generated hook.
- **Why it fits this hackathon:** Media theme (content creation, understanding), showcases Gemini video understanding end-to-end, visually flashy for the finale, no platform API dependencies.

### 12. ContextPulse — Interactive transcript & claim-graph explorer

- **Problem:** Readers/viewers can't quickly verify what was actually said in a long interview, hearing, or press conference, or trace how one claim connects to another statement.
- **Target user:** Journalists, researchers, policy analysts, and curious audiences.
- **Solution:** Upload a recording/transcript; ContextPulse builds an interactive timeline and claim graph — every claim node links to its timestamp and quote, supports side-by-side comparison of two statements, and answers questions with citations, clearly marking what is in the source versus external context.
- **Agentic-AI role:** Extraction + reasoning agent: identifies claims, entities, and their relations with citations; a tool builds the graph; a Q&A sub-agent answers only from extracted nodes with timestamps and returns "not present" otherwise; an optional web-grounding step is labeled separately from source material.
- **Data/API source:** Gemini long-context + structured claim extraction, Cloud Storage, Firestore/Neo4j-style graph in Firestore; public-domain hearing/interview recordings as fixtures.
- **Core workflow:** Upload → transcript + claim extraction → build claim/timestamp graph → ask questions → cited answers → compare-claims view → export citation sheet.
- **Demo moment:** Two claims that contradict each other light up in the graph, each linked to its timestamp, and the judge can jump playback to both moments to hear them in context.
- **Build complexity:** Medium.
- **Major risk:** Mis-attributing a claim or paraphrasing that changes meaning. Show verbatim quotes with timestamps, keep the graph auto-generation visibly human-correctable, and never infer intent.
- **Why it fits this hackathon:** Media theme (content understanding/discovery) with a fact-checking backbone, strong technical story (extraction + graph + grounded Q&A), and clear trust differentiation from a plain summarizer.

### 13. LocaleCast — Localized public-announcement studio

- **Problem:** Government/NGO/health announcements are produced in one language and format, excluding non-native speakers, low-literacy audiences, and people who need audio or simplified content.
- **Target user:** Civic communicators, NGOs, public broadcasters, community organizers (strong JAPAC multilingual angle).
- **Solution:** Upload a source announcement (video/audio/doc); LocaleCast produces a translation, a plain-language rewrite, synchronized captions, and a TTS narration in target languages — with a side-by-side review view so an editor can approve each localized asset against the original meaning.
- **Agentic-AI role:** Pipeline agent: analyzes source, then spawns per-language transformation steps (translate, simplify, caption-timing, narrate) with a consistency-check tool that compares each output back to the source for meaning drift and flags low-confidence segments for human review.
- **Data/API source:** Gemini translation/summarization, Cloud Text-to-Speech (in requirements), Cloud Storage; public PSA/announcement fixtures the team creates.
- **Core workflow:** Upload announcement → source analysis → parallel language/style transforms → drift check vs. original → editor review queue → publish caption/audio assets → audience view.
- **Demo moment:** One 60-second announcement becomes three panels at once — original, plain-language translation, and audio narration — with a flagged segment where the checker warned about possible meaning drift.
- **Build complexity:** Medium (TTS + caption sync is the fiddly part).
- **Major risk:** Translation that changes the meaning of an official announcement. The review/drift-check queue is the safeguard — make human approval visible in the demo, never imply auto-publish.
- **Why it fits this hackathon:** Media theme (content understanding + digital experiences) with an accessibility/social-impact edge for the "Most Impactful" award, reuses Text-to-Speech already in the repo, and demos crisply in under three minutes.

---

## Future of Work & Enterprise Productivity

### 14. Meet-to-Move — Meeting → accountable action agent

- **Problem:** Meetings end without owners, deadlines, or traceability; the same decisions get re-litigated because nobody can point to where a commitment was made.
- **Target user:** Distributed project teams, engineering leads, and PMOs.
- **Solution:** Upload a meeting recording and its agenda doc; Meet-to-Move extracts decisions and action items with owners/deadlines, links each to the exact audio timestamp, flags actions that contradict an earlier decision, and drafts the follow-up message.
- **Agentic-AI role:** Multi-step agent: transcribes audio, extracts structured decisions/actions with a schema, runs a contradiction-check tool against prior stored decisions, then a messaging tool drafts the nudge — with each action carrying timestamp evidence and a confidence flag.
- **Data/API source:** Gemini audio + long context, Firestore for the decision ledger, Cloud Storage for recordings; synthetic meeting + prior-decision fixtures.
- **Core workflow:** Upload recording + agenda → transcribe → extract decisions/actions → contradiction check vs. ledger → evidence-linked action board → auto-draft follow-up → owner marks done.
- **Demo moment:** The agent surfaces an action that silently contradicts a decision from "last week's" fixture, links both timestamps, and the judge sees the two moments side by side.
- **Build complexity:** Medium.
- **Major risk:** Crowded meeting-summary market and privacy concerns. Lead with contradiction detection + evidence links (not summary), and use only synthetic/sample meetings in the prototype.
- **Why it fits this hackathon:** Future-of-Work theme (decisions, collaboration, workflow execution), clear agentic multi-tool architecture, timestamped evidence gives it technical depth a generic summarizer lacks.

### 15. InboxTriage — Priority, intent & draft-response agent

- **Problem:** Knowledge workers lose hours to an overloaded shared inbox; messages get mis-prioritized, unanswered, or answered inconsistently because triage rules are manual.
- **Target user:** Small-business shared inboxes (support, ops, partnerships) and overloaded managers.
- **Solution:** Connect a folder of sample emails; InboxTriage classifies intent and urgency, extracts requested actions and deadlines, groups duplicates, and proposes a draft reply per thread — each draft citing the policy/doc it draws from, with the worker approving before send.
- **Agentic-AI role:** Triage + drafting agent: classification tool assigns intent/priority, an extraction tool pulls commitments/deadlines, a retrieval tool fetches the relevant policy/KB answer, and Gemini drafts the response grounded on retrieved content with an explicit "no policy found" fallback instead of inventing answers.
- **Data/API source:** Gemini structured output + function calling, retrieval over team docs (Vertex AI Search/embedded store), Firebase for thread state; synthetic email threads + policy docs.
- **Core workflow:** Ingest threads → classify intent/urgency → extract deadlines → dedupe/group → retrieve policy context → draft grounded replies → human approve/send → learn from edits.
- **Demo moment:** Fifteen messy sample emails sort into a prioritized board; one urgent thread gets a draft reply that cites the exact policy paragraph — and another has no policy, so the agent says so and routes to a human.
- **Build complexity:** Medium.
- **Major risk:** Sending wrong or fabricated replies. Drafts-only with mandatory approval, citation on every reply, and a visible fallback path when retrieval comes up empty.
- **Why it fits this hackathon:** Future-of-Work theme (knowledge access, productivity, workflow execution), strong tool-calling + grounding story, and a relatable pain every judge has felt.

### 16. PolicyPal — Policy Q&A & compliance-check agent

- **Problem:** Employees can't find answers in long HR/IT/compliance handbooks, so they ask colleagues, get inconsistent answers, and quietly violate policies the org already documented.
- **Target user:** HR/IT/compliance teams at small-mid companies; employees as end users.
- **Solution:** Ask any workplace policy question in natural language; PolicyPal answers with the exact handbook section, states whether the requested action is allowed/needs approval/prohibited, and generates the approval request or checklist when required.
- **Agentic-AI role:** Retrieval + decision-tree agent: retrieves the governing section, classifies the request against policy categories via a rules tool, answers with citation + a plain allowed/needs-approval/prohibited verdict, and a workflow tool creates the escalation form when approval is needed.
- **Data/API source:** Gemini + retrieval (Vertex AI Search/embedded store), Firestore for approval requests; synthetic multi-version handbooks as fixtures (including a stale-version trap).
- **Core workflow:** Ask question → retrieve section(s) → classify against policy → verdict + citation → route: answer / open approval request / decline → log for policy-owner review.
- **Demo moment:** An employee asks something the outdated handbook forbids; the agent cites the old section but flags that a newer version supersedes it, then opens the right approval path — showing version-awareness.
- **Build complexity:** Low-medium.
- **Major risk:** Stale or conflicting policy sources producing wrong verdicts. Version-awareness and citation are the differentiators; label clearly that it is decision support, not final authority.
- **Why it fits this hackathon:** Future-of-Work theme (knowledge access, decisions, workflow), clean retrieval + rules-agent architecture, fast to build reliably, and the version-conflict demo proves depth over a naive chatbot.

---

## Sustainability & Social Impact

### 17. GridGuard — Household energy-waste detective

- **Problem:** Households can't tell which appliance or habit drives their bill; energy data (if available at all) is raw meter readings nobody interprets, so efficiency upgrades are guesswork.
- **Target user:** Renters/homeowners, community energy programs, utility consumer-help desks.
- **Solution:** Upload a bill photo plus a short list/appliance photos; GridGuard estimates load breakdown, spots waste patterns (idle loads, tariff mismatch), and returns a prioritized savings plan with estimated cost/CO2 impact and a next-bill tracking loop.
- **Agentic-AI role:** Document + reasoning agent: Document AI/Gemini parses the bill, a tariff/pricing tool computes rates, Gemini reasons over appliance profiles + usage assumptions via function calling, and a tracker tool compares the next fixture bill to the forecast.
- **Data/API source:** Gemini vision + function calling, Document AI, Firestore for tracking; synthetic utility bills (tariffs from public utility rate sheets), appliance energy labels photographed by the team.
- **Core workflow:** Upload bill + appliance list → parse bill → compute rates → estimate per-appliance load → waste detection → savings plan with impact → track against next bill.
- **Demo moment:** The agent forecasts a saving, the user swaps in a "next month" fixture bill, and the dashboard shows the realized drop with an honest confidence range — plus one flagged assumption the user can correct.
- **Build complexity:** Medium.
- **Major risk:** Estimates presented as metered facts. Show ranges and assumptions, allow user correction, and never claim appliance-level precision the inputs don't support.
- **Why it fits this hackathon:** Sustainability theme (resource efficiency, sustainable decisions), document-understanding + tool-calling combo, and a quantified impact story that supports the "Most Impactful" award.

### 18. RescueRoute — Surplus-food logistics coordinator

- **Problem:** Donors with usable surplus can't quickly find who can take it, before it spoils; coordination across quantity, allergens, timing, and pickup is done over phone calls.
- **Target user:** Restaurants, hotels, campuses, and the NGOs/food banks that collect from them.
- **Solution:** A donor posts a surplus (photo + voice note); the agent identifies item/quantity/allergens, sets a pickup window, matches the best recipient by capacity/location/needs, and coordinates the volunteer acceptance with a safety checklist and impact estimate.
- **Agentic-AI role:** Multi-step coordination agent: vision on the food photo, a matching tool scores recipients on fit, a scheduling tool picks the window, Gemini drafts the multilingual donor/volunteer messages, and a checklist tool enforces the human safety approval before dispatch.
- **Data/API source:** Gemini vision + structured output + translation, Firestore for listings/matches, Cloud Storage for photos; synthetic donor/recipient fixtures (no live logistics API needed).
- **Core workflow:** Post surplus (photo/voice) → identify + allergen/quantity extraction → match recipients → propose pickup window → human safety approval → notify volunteer → impact dashboard updates.
- **Demo moment:** A live two-sided demo: donor posts a tray of unsold meals, a recipient is matched within seconds, the volunteer accepts on the other screen, and the impact counters (meals, kg, CO2e) tick up live.
- **Build complexity:** Medium.
- **Major risk:** Allergen/food-safety claims from image AI. Keep a mandatory human approval gate and present allergens as "listed/verify" rather than certified.
- **Why it fits this hackathon:** Sustainability & Social Impact theme (community support, resource efficiency), emotionally compelling two-sided demo, agent coordination story, and a live dashboard that photographs well for the video submission.

### 19. AquaAlert — Community water-waste & leak reporter

- **Problem:** Leaking taps, running communal taps, and hidden plumbing waste go unreported in apartments/campuses/municipal buildings because reporting is manual and slow, and usage data is never interpreted.
- **Target user:** Facility managers, housing societies, campus ops, municipal conservation programs.
- **Solution:** A resident reports a leak by photo/voice; AquaAlert classifies it, estimates waste severity, routes it to the right maintainer with a prioritized ticket, and tracks closure — plus a monthly anomaly view flagging unusually high usage zones.
- **Agentic-AI role:** Triage + routing agent: vision/audio intake classifies the issue, an estimation tool computes severity/waste rate from fixture flow tables, a prioritization tool scores tickets, Gemini drafts the maintainer work-order, and an anomaly step reasons over usage logs to flag suspect zones.
- **Data/API source:** Gemini vision/audio + structured output, Firestore for tickets, BigQuery for usage analytics story; synthetic usage CSVs and leak photos the team captures.
- **Core workflow:** Report leak (photo/voice) → classify → severity/waste estimate → priority + route to maintainer → work order drafted → closure confirmation → monthly anomaly dashboard.
- **Demo moment:** A judge reports a dripping tap by voice; the ticket is auto-created with a severity score and estimated liters/day wasted, and the dashboard shows three previously-open tickets closing as the impact counter rises.
- **Build complexity:** Medium.
- **Major risk:** Overstated waste estimates. Use published flow-rate tables, show ranges, and let facility staff confirm severity before it hits the priority board.
- **Why it fits this hackathon:** Sustainability theme (resource efficiency, resilience, community support), a full report→route→close workflow shows real agentic execution, and the impact dashboard supports the "Most Impactful" angle.

### 20. AccessPath — Accessibility-aware route & place scout

- **Problem:** People with mobility, vision, or comprehension needs can't tell whether a route, venue, or public space will actually work for them before they go — reviews are scattered, informal, and missing.
- **Target user:** Wheelchair users, caregivers, older adults, travelers with accessibility needs; venue operators as the scale channel.
- **Solution:** User describes their need and a destination; AccessPath checks venue accessibility data, flags barriers from uploaded street/entrance photos, and returns a route/venue plan with confidence, alternatives, and plain-language notes (rest points, ramps, signage).
- **Agentic-AI role:** Multi-source reasoning agent: a lookup tool pulls published accessibility records, Gemini vision reads photos for ramps/steps/door widths (as observations with confidence), and a planning tool combines need-profile + evidence into a route recommendation — explicitly separating "observed," "declared," and "unknown" facts.
- **Data/API source:** Gemini vision + structured output, Maps/geocoding only if credits confirmed (else a fixture set of venues), Firestore for user profiles and contributed reports; team-captured venue photos.
- **Core workflow:** Describe need + destination → fetch venue records → analyze contributed photos → classify observed/declared/unknown → route/venue plan with confidence → user feedback improves the record.
- **Demo moment:** Two venues side by side: one has photo evidence of a ramp with the AI-highlighted region shown, the other shows an unknown/needs-check verdict — honesty about gaps builds more trust than a false confident answer.
- **Build complexity:** Medium (maps integration is the swing factor; fixture venues keep it Low-medium).
- **Major risk:** Claiming accessibility guarantees from image inference. Present everything as evidence + confidence, never certification, and mark unknowns explicitly — accessibility errors have real human cost.
- **Why it fits this hackathon:** Sustainability & Social Impact theme (accessibility, community support), directly targets the accessibility sub-theme the older/leftover requirements mentioned, strong emotional resonance, and a clear observed-vs-unknown UI that judges will remember.

---

## Cross-idea comparison matrix (new bank)

| # | Idea | Theme | Complexity | Agentic depth | Demo appeal | Safety burden |
|---|---|---|---|---|---|---|
| 1 | ClaimLens | BFSI | Medium | High | Medium | High (coverage) |
| 2 | LoanReady | BFSI | Medium | High | Medium | High (credit) |
| 3 | ChargebackCoach | BFSI | Medium | High | Medium-high | Medium-high |
| 4 | ScamDrill | BFSI | Medium | High | Very high | High (sim safety) |
| 5 | ShelfAudit | Retail | Medium | Medium | Very high | Low |
| 6 | ReturnSense | Retail | Medium | High | High | Medium-high (fraud labels) |
| 7 | ShelfNudge | Retail | Medium | High | High | Medium |
| 8 | ShiftHandover | Manufacturing | Medium | High | High | Medium-high (safety) |
| 9 | DefectDesk | Manufacturing | Medium | Medium-high | High | Medium |
| 10 | ToolBoxTalk | Manufacturing | Low-medium | Medium | High | Low |
| 11 | StorySplice | Media | Medium-high | High | Very high | Medium (copyright) |
| 12 | ContextPulse | Media | Medium | High | High | Medium (misquote) |
| 13 | LocaleCast | Media | Medium | Medium-high | High | Medium-high (meaning drift) |
| 14 | Meet-to-Move | Future of Work | Medium | High | High | Medium (privacy) |
| 15 | InboxTriage | Future of Work | Medium | High | High | Medium-high (bad drafts) |
| 16 | PolicyPal | Future of Work | Low-medium | Medium | Medium-high | Medium (stale policy) |
| 17 | GridGuard | Sustainability | Medium | High | High | Medium (estimates) |
| 18 | RescueRoute | Sustainability | Medium | High | Very high | Medium-high (allergens) |
| 19 | AquaAlert | Sustainability | Medium | High | High | Medium (estimates) |
| 20 | AccessPath | Sustainability | Medium | High | High | High (accessibility claims) |

---

## Comparison with the earlier six ideas

The earlier document proposed six ideas, one per theme, with a final recommendation. Summary of the prior six on the axes used in this file:

| Prior idea | Theme | Complexity | Gemini fit | Demo appeal | Safety burden | Distinguishing strength |
|---|---|---|---|---|---|---|
| TrustLens | BFSI | Medium | Very high | High | High | Emotional relatability (scam awareness for everyone) |
| ShelfSense | Retail | Medium | High | Very high | Low-medium | Simplest visible business value from a photo |
| FixFlow | Manufacturing | Med-high | Excellent | Excellent | Very high | Strongest physical-world story; safety engineering showcase |
| ContextBridge | Media | Low-medium | Exceptional | Very high | Medium | Fastest polished prototype; evidence timestamps; repo already started |
| DecisionLoop | Future of Work | Medium | Very high | High | Medium-high | Contradiction detection differentiates from meeting-summary crowding |
| RescueGrid | Sustainability | Medium | Excellent | Excellent | Medium-high | Two-sided emotional + environmental demo with live counters |

**Overlap with the new bank (not duplicates — variants/alternates):**

- TrustLens ≈ ScamDrill (4): same BFSI scam space, but TrustLens *analyzes* a suspicious message while ScamDrill *simulates* a scam safely for training. Differentiated enough to be a separate submission; ScamDrill trades TrustLens's "upload anything" breadth for a tighter, more demo-able loop.
- ShelfSense ≈ ShelfAudit (5) + ShelfNudge (7): ShelfSense is the broad single-app version (stock + expiry + reorder); the new bank splits it into a vision-compliance tool (ShelfAudit) and a forecasting coach (ShelfNudge). ShelfSense remains the more complete story; the split versions are deeper individually.
- FixFlow ≈ ToolBoxTalk (10) + ShiftHandover (8): FixFlow is the ambitious full maintenance agent; ToolBoxTalk is the safe, low-complexity RAG subset; ShiftHandover covers the procedural/communication side. If the safety burden of FixFlow is a concern, ToolBoxTalk or ShiftHandover are lighter manufacturing entries.
- ContextBridge ≈ ContextPulse (12) + StorySplice (11): ContextBridge is the umbrella (Q&A + accessibility outputs); ContextPulse narrows to claim-graph/fact-checking depth; StorySplice narrows to clip generation. ContextPulse adds a contradiction-detection twist that raises technical novelty over plain video Q&A.
- DecisionLoop ≈ Meet-to-Move (14): largely the same idea; Meet-to-Move is scoped smaller (meetings only, not email/chat/doc sprawl), trading breadth for buildability.
- RescueGrid ≈ RescueRoute (18): essentially the same concept; RescueRoute emphasizes the two-sided live-coordination demo and keeps the human safety gate explicit.

**Where the new bank goes beyond the prior six:**

1. **New themes depth:** the prior list had exactly one idea per theme; the bank adds 14 alternatives so a team that dislikes one theme's safety burden still has options.
2. **Gaps the prior list did not cover:** accessibility-first product (20 AccessPath), civic/announcement localization (13 LocaleCast), household energy (17 GridGuard), water/leak reporting (19 AquaAlert), workplace policy version-conflict (16 PolicyPal), inbox triage (15), insurance claims (1), consumer dispute evidence (3), demand forecasting (7), visual QA (9), handover structuring (8).
3. **Consistent agentic framing:** the prior six emphasized *Gemini fit* (model capability); this bank adds an explicit *agentic-AI role* per idea (tools, steps, guardrails, human-in-the-loop) because judging weights "Technical Merit & Gen AI Implementation" at 40% — an agent architecture with tool-calling and structured outputs demonstrates that more clearly than a single multimodal call.
4. **Safety burden is tracked everywhere**; both documents agree the highest-burden ideas are FixFlow/AccessPath/ScamDrill/ClaimLens/LoanReady-class ideas, and that ContextBridge/ToolBoxTalk/ShelfAudit-class ideas are the safest to ship as a working prototype.

**What the prior six still do better:** they each include a worked example, a three-minute demo script, scale narrative, and an explicit "Gemini fit" rationale — worth copying into whichever idea is eventually selected. The prior file's final recommendation (ContextBridge) and its "shared core pattern" (multimodal input → grounded analysis → structured answer → useful action) remain valid; several new ideas deliberately reuse that proven pattern (8, 9, 13, 17, 19).

---

## Comparison with `docs/contextbridge-build-plan.txt` (the build plan — since superseded by `context/ARCHITECTURE.md` + `context/BUILD_PLAN.md` and removed; DECISIONS.md D-10)

The build plan is not an idea list — it is an execution plan that already selects **ContextBridge** as the first product of a "reusable Multimodal Intelligence Platform." Key claims and how they hold up against this 20-idea bank:

**Where the build plan is strong (and this bank agrees):**

- The core pipeline — *media ingestion → multimodal analysis → canonical evidence index → grounded Q&A → domain outputs* — is the same proven pattern used by ideas 8, 9, 11, 12, 13, 17, 19 in this bank. Building it once generalizes.
- The canonical schema idea already exists in the repo as `contextbridge_schema.py` (`MediaAnalysis` / `MediaEvent` / `EvidenceReference` with validation). That is real, reusable, deadline-relevant work — an advantage no other idea in this bank currently has, subject to RULES.md's "fresh project built during the hackathon timeline" rule (the schema must have been created inside the 7 Sep–18 Oct window to be eligible — confirm creation dates before relying on it).
- Its trust design (timestamp evidence, confidence, "not found" behavior, evaluation dataset of 100 questions) maps directly onto the 40% technical-merit criterion: it is measurable, demoable, and hard to fake.
- Its decision checkpoint (after first PoC: accurate timestamps? understandable evidence UI? not a generic chatbot? Cloud usage meaningful? judge gets it in 30 seconds?) is the right gate and should be applied to *any* shortlisted idea from this bank.

**Tensions between the build plan and this bank:**

1. **Platform vs. product.** The plan's larger ambition (a platform later serving FixFlow, ShelfSense, TrustLens, DecisionLoop, RescueGrid) is strategically sensible but risky inside a hackathon that requires **one submission under one theme**. Judges score one working prototype, not an architecture slide. The plan itself already says "Do not build FixFlow or the other verticals yet" — this bank agrees: commit to one surface.
2. **The plan's prior recommendation is pre-committed.** `context/IDEAS.md` already names ContextBridge the winner, and the build plan operationalizes it. This file deliberately reopens the field per the current instruction (no winner yet). ContextBridge remains *one of* the strongest candidates — see the prior table — but it is now evaluated alongside 20 new alternatives rather than treated as decided.
3. **Crowd-out risk on Media.** Video Q&A is the most demo-friendly but also the most "familiar" category; judges may ask what separates it from a Gemini demo notebook. ContextPulse (12) answers that with contradiction/claim-graph depth; StorySplice (11) answers it with an output artifact (a finished clip). ContextBridge's answer — accessibility outputs + evidence timestamps — is also valid; the differentiation question should be decided at the checkpoint, not assumed.
4. **Sunk cost.** The repo currently contains Streamlit app scaffolding, schema/store modules, a SQLite DB, a `web/` Next.js scaffold, and Text-to-Speech in requirements — i.e., groundwork that serves ContextBridge (11, 12, 13) most directly, partially serves 8/9/14, and is mostly orthogonal to BFSI/Retail ideas. Switching themes later costs more than switching among Media/Sustainability ideas later. This is a real factor but not a decision by itself.
5. **Fresh-project rule.** RULES.md: only fresh projects built during the hackathon timeline are eligible. Anything predating 7 Sep 2026 (or the official build window start) must be excluded or rebuilt; the build plan's "reuse what is useful from the existing project" instruction needs that date check applied to every reused file.

**Net position:** the build plan is an execution-ready path for ContextBridge and shares this bank's architecture philosophy; this bank exists so the ContextBridge decision is *re-confirmed against 20 alternatives* rather than inherited. The plan's Phase 1–7 build order and its resume prompts remain usable unchanged if ContextBridge is (re)chosen.

---

## Decision status

**No winner has been chosen.** This file is a neutral idea bank plus a comparison against the two prior documents. Selection requires a separate decision step — the natural gate being the build plan's own checkpoint questions (timestamp accuracy, evidence-UI clarity, distinctness from a generic chatbot, processing time, meaningful Google Cloud usage, 30-second judge comprehension) applied to the shortlist the team prefers.

**Reminder before choosing:** confirm cloud/Gemini credits and quotas with the organizer (unverified per `context/RESOURCES.md`), resolve the registration deadline discrepancy (4 Oct vs 11 Oct), and enforce the one-team-one-theme submission rule.

---

## Earlier six-idea round (preserved from the previous source document)

AI BUILDER CUP 2026
Six Product Ideas, Gemini Fit, Risk, and Recommendation
=========================================================

Prepared for the Google Cloud AI Builder Cup 2026
Themes: BFSI, Retail & Commerce, Manufacturing, Media/Content,
Future of Work, Sustainability & Social Impact

Official challenge reference:
https://aibuildercup.com/themes.html

IMPORTANT
---------
No idea is guaranteed to win. A strong submission needs a real user problem,
a working prototype, meaningful use of Google AI, a clear demo, and a
credible path to scale.

Google capabilities relevant to these ideas:

- Gemini multimodal inputs: images, audio, video, and text
- Gemini long context: large document and conversation context
- Gemini document understanding and structured output
- Gemini function calling for safe, controlled actions
- Vertex AI / Gemini Enterprise Agent Platform for agents, sessions,
  memory, evaluation, tracing, and managed deployment
- Document AI for document extraction and classification
- Cloud Run for the backend
- Firebase for the web application, authentication, and real-time data
- Cloud Storage for documents, media, photos, and reports
- BigQuery for aggregated operational and impact analytics

Official Google references:

https://ai.google.dev/gemini-api/docs/video-understanding
https://ai.google.dev/gemini-api/docs/document-processing
https://ai.google.dev/gemini-api/docs/function-calling
https://cloud.google.com/vertex-ai/generative-ai/docs/long-context
https://cloud.google.com/document-ai
https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview


=========================================================
1. BFSI: TRUSTLENS
=========================================================

Name:
TrustLens

One-line description:
An AI safety assistant that helps people understand suspicious messages,
payment requests, investment offers, QR codes, and voice scams before they
lose money.

Real problem:
People receive fraudulent bank messages, fake support messages, investment
scams, malicious payment links, impersonation calls, and social-engineering
requests. Older adults, first-time digital banking users, small-business
owners, and multilingual users are especially exposed.

Inputs:
- SMS or messaging screenshots
- Email
- QR code
- Website URL
- Voice recording
- Investment or loan document
- Conversation history

Output:
- Risk level
- Suspicious elements highlighted in the original content
- Plain-language explanation
- Safe verification steps
- Official contact path
- Optional trusted-contact approval

Example:

Risk level: HIGH

Evidence:
- Sender impersonates a known bank
- Link domain does not match the bank
- Message creates urgency
- Request asks for an OTP

Recommended action:
Do not click the link or share the OTP. Contact the bank using the
number on the back of the card.

Why Gemini fits:
- Understands screenshots and documents
- Can analyze voice and text together
- Can explain risk in simple or local language
- Can return a structured risk report
- Can call controlled verification tools through function calling

Three-minute demo:
1. A simulated user receives a fake bank message.
2. They upload the screenshot and a short voice note.
3. TrustLens highlights the suspicious elements.
4. Gemini explains the danger in the user's chosen language.
5. The user selects "Verify safely".
6. The system shows the official verification path.

Scale:
Banks, telecom companies, insurers, employers, families, and governments
could distribute it as a consumer safety layer.

Main risk:
Never claim certainty or give financial advice. Use phrases such as
"potentially dangerous" and always direct the user to an official channel.

Build difficulty:
Medium.

Gemini fit:
Very high.

Hackathon strength:
Very relatable and emotionally memorable. Strong BFSI alignment, but the
prototype must be careful not to imply bank-grade fraud detection.


=========================================================
2. RETAIL & COMMERCE: SHELFSENSE
=========================================================

Name:
ShelfSense

One-line description:
An AI inventory and expiry assistant for small retailers that works from
phone photos, receipts, invoices, and voice questions.

Real problem:
Small stores often use memory, notebooks, WhatsApp, or spreadsheets.
They lose money through stockouts, expired products, over-ordering, damaged
packaging, and poor demand prediction.

Inputs:
- Shelf photos
- Product photos
- Purchase invoices
- Receipts
- Sales CSV
- Voice questions
- Local event or seasonal information

Output:
- Estimated stock
- Empty shelf detection
- Near-expiry alerts
- Slow-moving products
- Reorder suggestions
- Promotion suggestions
- Confidence and manual correction controls

Example:

Milk, 1L:
- Estimated stock: 8 units
- Average daily sales: 14 units
- Stockout risk: within 18 hours
- Recommended order: 40 units

Expiry alert:
12 yogurt packs expire in 3 days.
Suggested promotion: 10 percent discount.

Why Gemini fits:
- Reads labels and products from images
- Understands receipts and invoices
- Combines images with historical sales
- Accepts voice questions
- Generates a natural-language purchasing explanation

Three-minute demo:
1. Show a disorganized store shelf.
2. Upload a shelf photo and invoice.
3. ShelfSense identifies products and stock issues.
4. Upload a small sales file.
5. Ask by voice: "What should I reorder before the weekend?"
6. Show the purchase list and expiry promotion.

Scale:
Distributors, POS providers, consumer-goods companies, wholesale platforms,
and small-business banking services could offer it.

Main risk:
Products may be hidden or visually similar. Show confidence, let users
correct counts, and learn from corrections.

Build difficulty:
Medium.

Gemini fit:
High.

Hackathon strength:
Extremely visual and easy to understand. The small-retailer wedge is
important because enterprise inventory software already exists.


=========================================================
3. MANUFACTURING: FIXFLOW
=========================================================

Name:
FixFlow

One-line description:
An AI operational-memory and maintenance assistant that turns a technician's
photo, video, voice note, manual, and maintenance history into a
grounded and safety-aware action plan.

Real problem:
Small and mid-sized operations lose time and money when equipment fails.
Maintenance knowledge is fragmented across printed manuals, old work orders,
WhatsApp messages, spreadsheets, photos, and individual memory. When an
experienced technician leaves or is unavailable, the same problem may take
hours to diagnose again.

Important framing:
The product is not "AI guesses what is wrong from a photo."

The product is:
"A safe, evidence-backed operational memory for organizations that maintain
physical assets."

Inputs:
- Machine photo
- Short video
- Voice description
- Equipment manual
- Previous maintenance records
- Sensor readings, where available

Output:
- Detected component
- Observed visual evidence
- Possible causes with confidence
- Relevant manual sections
- Safe diagnostic checklist
- Stop conditions and escalation rules
- Generated maintenance report
- Recurring-failure insight

Example:

Detected component:
Pump inlet assembly

Observed evidence:
- Fluid leakage at inlet joint
- Visible corrosion
- Loose coupling

Possible causes:
1. Damaged inlet seal - 82 percent
2. Excessive pressure - 61 percent
3. Pipe misalignment - 38 percent

Safe next step:
Shut down and isolate the pump before inspection.

Escalate if:
- Pressure exceeds the equipment limit
- Leakage continues after isolation
- Electrical or high-temperature hazards are present

Why Gemini fits:
- Combines images, video, voice, manuals, and history
- Handles long technical documents
- Can cite evidence and produce structured reports
- Can coordinate diagnostic steps through agents
- Can generate a persistent maintenance record

Three-minute demo:
1. A machine stops working.
2. The technician says: "The motor overheats after ten minutes."
3. They upload a photo and a manual.
4. FixFlow identifies the likely area and cites the manual.
5. It shows a safety-aware diagnostic checklist.
6. After the repair, it generates a report.
7. The dashboard shows:
   - Downtime avoided
   - Estimated loss avoided
   - Whether the issue is recurring
   - Which similar machines should be inspected

Scale:
Small factories, warehouses, hospitals, hotels, solar maintenance,
agricultural equipment, building management, and equipment manufacturers.

Safety architecture required:
- Evidence citations
- Confidence levels
- Explicit uncertainty
- No automatic repair authorization
- Human approval
- Stop conditions
- Audit trail
- Escalation for electrical, pressure, heat, chemical, or mechanical risk

Critical answer to the induction-machine concern:
Gemini must not be treated as a safety authority. For high-risk equipment,
the system should refuse to provide a repair procedure unless it has:
1. A verified equipment manual or approved procedure,
2. A clearly identified machine/model,
3. The required safety conditions,
4. A qualified human approval path.

If these are missing, the result should be:
"I cannot safely recommend a repair. Isolate the equipment and contact a
qualified technician."

Build difficulty:
Medium-high.

Gemini fit:
Excellent.

Hackathon strength:
Very high if safety is demonstrated honestly. It has a memorable physical
world demo and a large expansion story. It is not the easiest first build.


=========================================================
4. MEDIA, CONTENT & DIGITAL EXPERIENCES: CONTEXTBRIDGE
=========================================================

Name:
ContextBridge

One-line description:
An evidence-linked video intelligence platform that lets users ask questions
about long videos and produces accessible, multilingual, timestamped answers
and derivative content.

Real problem:
Important information is trapped in long lectures, public hearings, training
sessions, webinars, medical talks, news conferences, and local-language
recordings. Users cannot quickly find the relevant moment, verify what was
said, understand difficult language, or access it in a suitable format.

Inputs:
- Long video
- Audio
- Transcript
- Slides
- User question
- Target language
- Accessibility preference

Output:
- Chaptered visual timeline
- Searchable transcript
- Timestamped answers
- Claim/evidence links
- Easy-language summary
- Local-language audio
- Captions
- Short vertical video
- Screen-reader friendly version

Example:

Question:
"What did the speaker say about flood evacuation?"

Answer:
At 18:42, the speaker recommends moving to elevated shelters before
8:00 PM.

Source:
Video timestamp 18:42-19:16

Formats:
- English summary
- Local-language audio
- 60-second video
- Screen-reader version

Why Gemini fits:
- Native video understanding
- Audio and speech comprehension
- Long-context reasoning
- Timestamp references
- Translation and summarization
- Question answering over video
- Generates multiple content formats from the same source

Three-minute demo:
1. Upload a long educational or public-service video.
2. The system builds a visual timeline.
3. Ask: "What happened after the announcement?"
4. ContextBridge jumps to the relevant timestamp.
5. Generate a local-language explanation.
6. Toggle accessibility mode.
7. Show the answer's source timestamp.

Scale:
YouTube-like platforms, education, government communication, NGOs, hospitals,
newsrooms, public broadcasters, and corporate training.

Main risk:
Summarization and translation can change meaning. Every important answer
must link to the original timestamp and show uncertainty where appropriate.

Build difficulty:
Low-medium for a polished MVP.

Gemini fit:
Exceptional.

Hackathon strength:
Very high. It is visually impressive, immediately understandable, and
demonstrates a capability that is difficult to fake with a normal chatbot.


=========================================================
5. FUTURE OF WORK: DECISIONLOOP
=========================================================

Name:
DecisionLoop

One-line description:
An evidence-backed organizational memory that turns meetings, emails, chats,
documents, and tickets into accountable decisions and detects contradictions.

Real problem:
Organizations lose time because important decisions are buried in meetings,
emails, chats, documents, tickets, and spreadsheets. A meeting summary is
not enough. Teams still ask:

- What was decided?
- Who owns the action?
- What evidence supports it?
- Does this conflict with an older decision?
- What is overdue?

Inputs:
- Meeting recording
- Chat thread
- Email
- Project documents
- Tickets
- Previous decisions

Output:
- Decision
- Owner
- Deadline
- Reason
- Evidence links
- Contradictions
- Overdue actions
- Follow-up messages

Example:

Decision:
Launch postponed to 14 October

Owner:
Priya - confirm deployment readiness

Reason:
Payment reconciliation test is failing

Evidence:
- Engineering ticket 1842
- Meeting timestamp 32:14
- QA report, section 3

Conflict:
A customer email promises launch on 7 October.

Why Gemini fits:
- Long-context cross-document reasoning
- Audio and meeting understanding
- Extraction of entities and relationships
- Contradiction detection
- Structured output
- Agent workflows for follow-up actions

Three-minute demo:
1. Upload a meeting recording, email, and project document.
2. DecisionLoop extracts decisions and owners.
3. It detects a conflicting customer promise.
4. Ask: "Why was the launch delayed?"
5. The answer includes timestamped evidence.
6. Show an overdue-actions view.

Scale:
Distributed companies, consulting, customer success, operations, healthcare
administration, and government programs.

Main risk:
Privacy and permissions. Use sample data in the prototype and demonstrate
document-level access control.

Build difficulty:
Medium.

Gemini fit:
Very high.

Hackathon strength:
Strong enterprise pain, but the market is crowded with meeting-summary
products. Contradiction detection and decision accountability must be the
core differentiation.


=========================================================
6. SUSTAINABILITY & SOCIAL IMPACT: RESCUEGRID
=========================================================

Name:
RescueGrid

One-line description:
An AI coordination layer that matches surplus food with suitable recipients
and coordinates safe pickup before the food is wasted.

Real problem:
Restaurants, hotels, supermarkets, campuses, and event venues may have
usable surplus food but cannot reliably coordinate:

- What food is available
- Quantity
- Expiry window
- Allergens
- Location
- Which recipient can accept it
- Which vehicle can collect it

The problem is not only willingness. It is coordination.

Inputs:
- Food photo
- Voice note
- Receipt or inventory sheet
- Expiry information
- Donor location
- Recipient requirements

Output:
- Food type and approximate quantity
- Allergen information
- Pickup window
- Best recipient
- Route priority
- Approval and safety checklist
- Impact estimate

Example:

Surplus available:
180 meals

Best match:
Community Kitchen A

Pickup window:
6:30 PM-7:15 PM

Estimated impact:
- 180 meals redirected
- 92 kg food waste avoided
- 240 kg CO2e avoided

Why Gemini fits:
- Understands food images
- Reads receipts and inventory
- Handles multilingual communication
- Matches messy supply information to recipient needs
- Coordinates workflows through agents

Three-minute demo:
1. A restaurant uploads a photo of unsold meals.
2. RescueGrid identifies the food and quantity.
3. It shows allergens and a pickup window.
4. The system selects the best nearby recipient.
5. A volunteer accepts pickup.
6. The impact dashboard updates live.

Scale:
Hotels, retailers, hospitals, campuses, event venues, municipal programs,
and enterprise sustainability software.

Main risk:
Gemini cannot certify food safety. A responsible organization must approve
the donation and verify expiry, storage, and allergen information.

Build difficulty:
Medium.

Gemini fit:
Excellent.

Hackathon strength:
Very strong emotional and environmental demo. The logistics workflow makes it
more substantial than a food-classification application.


=========================================================
COMPARISON
=========================================================

Idea           Difficulty   Gemini fit   Demo appeal   Safety burden
----------------------------------------------------------------------
TrustLens      Medium       Very high    High          High
ShelfSense     Medium       High         Very high     Low-medium
FixFlow        Med-high     Excellent     Excellent     Very high
ContextBridge  Low-medium   Exceptional   Very high     Medium
DecisionLoop   Medium       Very high    High          Medium-high
RescueGrid     Medium       Excellent     Excellent     Medium-high

Best for fastest polished prototype:
ContextBridge

Best for strongest physical-world story:
FixFlow

Best for emotional relatability:
TrustLens

Best for simple visual business value:
ShelfSense

Best for sustainability:
RescueGrid

Best for enterprise productivity:
DecisionLoop


=========================================================
FINAL RECOMMENDATION
=========================================================

For the strongest balance of buildability, Gemini quality, visual appeal,
and hackathon safety, choose:

CONTEXTBRIDGE

Why:
1. Gemini is naturally strong at video, audio, text, and long context.
2. The input/output transformation is easy for judges to understand.
3. Timestamped evidence makes the result more trustworthy.
4. It is easier to prototype safely than maintenance or finance.
5. The demo can be polished without needing real industrial hardware,
   sensor integrations, bank integrations, or food logistics.
6. It aligns directly with Media, Content & Digital Experiences.
7. It can expand into education, public services, accessibility, training,
   journalism, and YouTube-style experiences.

Recommended product statement:

"ContextBridge turns long, difficult-to-access video into searchable,
trustworthy, multilingual, and accessible knowledge. Ask a video what
happened, get an answer with the exact timestamp, and generate the format
that each viewer can understand."

Recommended MVP:
1. Upload a video.
2. Gemini analyzes video, speech, slides, and timestamps.
3. Generate a searchable timeline.
4. Ask questions in a chat panel.
5. Return answers with timestamp evidence.
6. Generate a short summary in another language.
7. Toggle captions, easy-language mode, or audio narration.

Google Cloud implementation:
- Cloud Run: API and processing service
- Firebase: dashboard, authentication, and saved video sessions
- Cloud Storage: uploaded videos and generated assets
- Gemini on Vertex AI: video understanding, Q&A, summarization, translation
- Agent Platform or Google ADK: orchestrated processing and follow-up actions
- BigQuery: aggregate usage and accessibility analytics, if needed

Second recommendation:

Choose FixFlow if the team is comfortable building a strong safety system and
wants a manufacturing story. Do not expose it as autonomous diagnosis.
Present it as evidence-backed decision support with mandatory human
escalation for hazardous equipment.

Third recommendation:

Choose ShelfSense if the priority is the easiest business demo with
immediately visible value. It is less technically unique, so the small-store
accessibility angle must be central.

Suggested decision:

Build a small ContextBridge prototype first. If the video Q&A and timestamp
experience feels too generic after a short proof of concept, switch to
FixFlow without discarding the Google/Gemini architecture. Both use the same
core pattern:

multimodal input -> grounded analysis -> structured answer -> useful action

