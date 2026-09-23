# Idea Review — AI Builder Cup 2026

**Date:** 2026-09-23
**Inputs reviewed:** `context/HACKATHON.md`, `context/RULES.md`, `context/RESOURCES.md`, `context/IDEAS.md` (combined 26-idea bank and recommendation), `docs/contextbridge-build-plan.txt` (execution plan), **plus the actual repository state** (`app.py`, `contextbridge_schema.py`, `contextbridge_store.py`, `contextbridge.db`, `requirements.txt`, `web/`, `server.log`).

> *Note (2026-09-23): `docs/contextbridge-build-plan.txt` was subsequently superseded by `context/ARCHITECTURE.md` + `context/BUILD_PLAN.md` and removed (`context/DECISIONS.md` D-10). It is cited below as a historical review input.*

## Verdict up front

**Build ContextBridge (Media, Content & Digital Experiences) — but not as currently scoped.** It survives every hard gate (deadline, deployability, safety, Gemini fit) and is the only idea with real scaffolding in the repo. Its one weak axis is the 25% innovation criterion, so it must be upgraded with ContextPulse-style claim/contradiction depth and one tangible output artifact (details in §7). **Fallback: ScamDrill (BFSI).** **Highest-ceiling alternative: RescueRoute (Sustainability).**

---

## 1. Constraints that dominate every score

These come from the rules/resources files, not from preferences — any idea that ignores them is scored wrong:

1. **~25 days remain** (today 23 Sep → prototype deadline 18 Oct). That budget also has to cover the PDF deck, a strictly-under-3-minute video, a **public GitHub repo**, and a **deployed** prototype on Cloud Run/GCP/Firebase. Effective build time ≈ 15–18 days.
2. **Judging weights:** Technical Merit & Gen AI Implementation 40%, Problem Alignment & Impact 25%, Innovation & Creativity 25%, UX & Design 10%. An idea that is merely "useful" loses; it must *demonstrate* agentic, tool-using, grounded Gen AI.
3. **No credits, API keys, quotas, or model versions are confirmed** (RESOURCES.md). Every idea silently assumes billing-enabled GCP. This penalty is not evenly distributed — it hits video-heavy and Document AI pipelines hardest.
4. **Fresh-project rule (RULES.md):** only work built inside the 7 Sep–18 Oct window is eligible. The repo already contains ContextBridge code of unverified provenance, and the build plan's own resume note references a *different* project folder (`...\SchemaSentinel-Strands - Copy.worktrees\greeting-response-c2cebd58`). Every reused file's authorship date must be audited before relying on it.
5. **The workspace is not a git repository yet.** The submission requires a public GitHub repo; a credible in-window commit history is part of compliance.
6. **One team = one theme = one submission.** Platform visions score zero; one polished working prototype scores everything.
7. **Team size unknown (2–4 allowed).** Time-to-build scores below assume a small team; adjust ±1 if 4 strong builders.

---

## 2. Method

Each of the 26 ideas (20 new + 6 prior) is scored 1–5 on the ten requested dimensions:

| Dimension | What 5 means |
|---|---|
| Fit | Dead-center of one official theme + showcases Google stack |
| Innovation | Novel vs. both market products and the likely hackathon field |
| Agentic depth | Genuine multi-step tool use / state / guardrails — not a prompt chain |
| User value | Real, frequent, felt pain with a clear beneficiary |
| Feasibility | Buildable on synthetic fixtures; no hardware, bank, or platform APIs |
| Demo impact | Wow + comprehension in <3 minutes / a 30-second judge pitch |
| Time-to-build | Comfortably shippable in ~15–18 effective days |
| Resource availability | Survives unconfirmed credits/quotas (cheap models, small payloads) |
| Differentiation | Defensible answer to "haven't I seen this demo before?" |
| Risk | 5 = safe. Safety/legal/eligibility/demo-failure exposure (risk ≤ 2 is a **gate**, not averaged away) |

Composite maps onto official weights: **Technical 40%** = agentic 20 + feasibility 10 + time 5 + resources 5 · **Impact 25%** = fit 10 + value 10 + demo 5 · **Innovation 25%** = innovation 15 + differentiation 10 · **UX 10%** = demo 5 + time-to-polish 5. Scores are informed judgment from the source documents and repo inspection, not measurements.

---

## 3. Scoring matrix — all 26 ideas

### 3.1 Earlier six (`context/IDEAS.md`)

| Idea | Theme | Fit | Innov | Agentic | Value | Feasib | Demo | Time | Resrc | Diff | Risk | Composite |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TrustLens | BFSI | 5 | 3 | 3 | 5 | 4 | 4 | 4 | 4 | 3 | 3 ⚠ | 3.75 |
| ShelfSense | Retail | 4 | 3 | 3 | 4 | 4 | 5 | 3 | 4 | 3 | 4 | 3.55 |
| FixFlow | Manufacturing | 5 | 4 | 4 | 5 | 3 | 5 | 2 | 4 | 4 | 2 ⛔ | 4.00 |
| **ContextBridge** | Media | 5 | 3 | 3 | 4 | 5 | 5 | 5 | 3 | 3 | 4 | 3.90* |
| DecisionLoop | Future of Work | 4 | 3 | 4 | 4 | 3 | 3 | 3 | 4 | 3 | 3 | 3.45 |
| RescueGrid | Sustainability | 5 | 3 | 5 | 4 | 4 | 5 | 3 | 4 | 4 | 3 | 4.15 |

\* plus the only existing-code head start — see §5 and §7.

### 3.2 New bank (`context/IDEAS.md`)

| # | Idea | Theme | Fit | Innov | Agentic | Value | Feasib | Demo | Time | Resrc | Diff | Risk | Composite |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ClaimLens | BFSI | 5 | 3 | 4 | 4 | 3 | 4 | 3 | 3 | 3 | 2 ⛔ | 3.60 |
| 2 | LoanReady | BFSI | 4 | 3 | 4 | 4 | 4 | 3 | 3 | 4 | 3 | 2 ⛔ | 3.55 |
| 3 | ChargebackCoach | BFSI | 4 | 4 | 4 | 3 | 4 | 4 | 4 | 4 | 4 | 3 | 3.90 |
| 4 | **ScamDrill** | BFSI | 5 | 4 | 4 | 5 | 4 | 5 | 3 | 5 | 4 | 2 ⛔ | **4.25** |
| 5 | ShelfAudit | Retail | 4 | 3 | 3 | 4 | 4 | 5 | 4 | 4 | 3 | 5 | 3.65 |
| 6 | ReturnSense | Retail | 4 | 3 | 4 | 3 | 3 | 3 | 3 | 4 | 4 | 3 | 3.45 |
| 7 | ShelfNudge | Retail | 4 | 3 | 3 | 4 | 4 | 3 | 4 | 4 | 3 | 4 | 3.45 |
| 8 | ShiftHandover | Manufacturing | 5 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 3 | 4.10 |
| 9 | DefectDesk | Manufacturing | 5 | 3 | 3 | 4 | 4 | 4 | 4 | 4 | 2 | 4 | 3.55 |
| 10 | ToolBoxTalk | Manufacturing | 4 | 2 | 3 | 4 | 5 | 3 | 5 | 4 | 2 | 5 | 3.40 |
| 11 | StorySplice | Media | 5 | 4 | 4 | 4 | 3 | 5 | 2 | 3 | 4 | 3 | 3.85 |
| 12 | **ContextPulse** | Media | 5 | 4 | 4 | 3 | 4 | 4 | 3 | 4 | 4 | 3 | 3.90 |
| 13 | LocaleCast | Media | 4 | 4 | 3 | 4 | 4 | 4 | 4 | 4 | 4 | 3 | 3.80 |
| 14 | Meet-to-Move | Future of Work | 4 | 3 | 4 | 4 | 4 | 4 | 4 | 4 | 2 | 4 | 3.65 |
| 15 | InboxTriage | Future of Work | 4 | 3 | 4 | 4 | 4 | 3 | 4 | 4 | 2 | 3 | 3.55 |
| 16 | PolicyPal | Future of Work | 4 | 2 | 3 | 3 | 5 | 3 | 5 | 4 | 2 | 3 | 3.30 |
| 17 | GridGuard | Sustainability | 5 | 3 | 4 | 3 | 3 | 3 | 3 | 4 | 3 | 4 | 3.45 |
| 18 | **RescueRoute** | Sustainability | 5 | 4 | 5 | 4 | 4 | 5 | 3 | 4 | 4 | 3 | **4.30** |
| 19 | AquaAlert | Sustainability | 5 | 3 | 4 | 3 | 4 | 4 | 4 | 4 | 3 | 4 | 3.75 |
| 20 | AccessPath | Sustainability | 5 | 4 | 4 | 5 | 3 | 4 | 3 | 3 | 5 | 2 ⛔ | 4.05 |

⛔ = risk gate (≤2): shippable only with serious guardrail engineering. ⚠ = elevated.

**Ranking (composite):** RescueRoute 4.30 > ScamDrill 4.25 > RescueGrid 4.15 > ShiftHandover 4.10 > AccessPath 4.05 > FixFlow 4.00 > ContextBridge / ContextPulse / ChargebackCoach 3.90 > StorySplice 3.85 > LocaleCast 3.80 > TrustLens / AquaAlert 3.75 > ShelfAudit / Meet-to-Move 3.65 > ClaimLens 3.60 > ShelfSense / LoanReady / DefectDesk / InboxTriage 3.55 > DecisionLoop / ReturnSense / ShelfNudge / GridGuard 3.45 > ToolBoxTalk 3.40 > PolicyPal 3.30.

**Read this ranking honestly:** the raw composite favors RescueRoute and ScamDrill over ContextBridge. §7 explains why the recommendation still lands on ContextBridge — the composite measures *ideas*, and three execution gates (time, demo reliability, existing head start) re-rank them. If you dispute those gates, the honest alternatives are right there at the top of the table.


---

## 4. Per-idea critique — challenging each idea's weakest assumption

### BFSI (1–4 + TrustLens)

- **1 ClaimLens.** The strongest BFSI agent pipeline on paper (classify → Document AI → vision → coverage-checklist validation → structured triage), but the demo hinges on Document AI and Gemini vision *agreeing* on synthetic fixtures the team must author itself. The coverage-gap analysis is the only genuinely hard part and is exactly where demo gremlins live. And the coverage-authority risk means a third of the UI becomes disclaimers. Good, not best.
- **2 LoanReady.** The "readiness score climbs after the fix" beat is nice, but the product quietly requires the agent to be *right about eligibility* — ground truth must be authored and kept consistent with published guidelines that differ across JAPAC markets. The permanent "not a lending decision" framing erodes the wow. Middle of the pack.
- **3 ChargebackCoach.** Genuinely fresh (reason-code taxonomies are real and obscure), and evidence-bound drafting with an explicit refusal path is a good technical story. But the pain is episodic — consumers dispute rarely — so judges may not *feel* it in three minutes. Sleeper pick if the team insists on BFSI.
- **4 ScamDrill.** The best demo *concept* in the entire bank: a judge plays along, "falls" for a simulated QR scam, and gets scored. Also the cheapest to run (pure conversation + Firebase — survives the unconfirmed-credits problem best). But it is one broken safety rail away from catastrophic demo failure, free-form role-play quality is the hardest thing to rehearse, and "we built a scam simulator" has dual-use optics that demand disciplined framing (bank-partner training narrative, script-bounded scenarios, permanent SIMULATION banner).
- **TrustLens (prior).** Hugely relatable, but it is an *analyzer* — and scam analyzers are a hackathon staple in JAPAC. Its deepest flaw: a false negative ("looks safe") is a real-world harm, so it can never say "safe," which flattens the demo into hedged language. ScamDrill is the strictly more memorable variant of the same theme.

### Retail & Commerce (5–7 + ShelfSense)

- **5 ShelfAudit.** Lowest risk in the bank and an instantly legible demo (photo → compliance score). The unchallenged assumption: that Gemini vision will reliably count facings on *unstaged* shelf photos. A staged fixture works; a judge's live photo may not. Decide explicitly which demo you're doing — don't discover the answer on stage.
- **6 ReturnSense.** B2B pain judges don't personally feel, and "this customer is probably a fraudster" is a demo-unfriendly output no matter how carefully labeled. Weakest retail entry emotionally.
- **7 ShelfNudge.** Honest, buildable, and boring — forecast charts will not hold a demo against flashier entries. Works better as a feature inside ShelfSense than as a standalone submission.
- **ShelfSense (prior).** The broadest retail story, but scope is the trap: photos + invoices + sales CSV + voice + reorder logic is four products in one trench coat. The prior doc's own fallback ("the accessibility angle must be central") concedes it's technically ununique. If chosen, cut to two inputs.

### Manufacturing (8–10 + FixFlow)

- **8 ShiftHandover.** The most underrated idea in the bank. The demo beat — the agent catches a safety hold that was *said* in the voice note but never *written* in the log, with the exact quote — is a perfect three-minute moment, and voice+photo fixtures are trivial to produce. Real concern: it asks judges to imagine a factory; the emotional hook is weaker than consumer-facing ideas.
- **9 DefectDesk.** Walks straight into the most crowded industrial-AI category (visual inspection). Differentiation must come from the trend/hypothesis layer, not classification — but if classification visibly fails live, the trend story collapses with it. Stage the defect library with discipline.
- **10 ToolBoxTalk.** The safest build and the weakest submission. "Chat with manuals + citations + honest refusal" was impressive in 2023; in 2026 it is the default demo every judge has seen a dozen times. Only viable if the checklist/task-output UX is exceptional — and UX is only 10%.
- **FixFlow (prior).** The best physical-world story and the worst prototype-round risk profile. The mandated safety architecture (evidence citations, stop conditions, refusal paths, audit trail) is itself a multi-day build, and its own spec says the correct output for high-risk equipment is often a refusal — a demo whose climax is "I cannot safely answer" needs flawless choreography. Finals-quality idea; wrong deadline.


### Media, Content & Digital Experiences (11–13 + ContextBridge)

- **11 StorySplice.** The flashiest artifact in the bank (a finished vertical clip with captions) — and video assembly/rendering is exactly where hackathon demos go to die. The smart scope-cut ("metadata cuts" in the player instead of rendering) turns it into ContextBridge's timeline with an export button. Conclusion: it is a ContextBridge *feature*, not a separate product.
- **12 ContextPulse.** The best *innovation* story in Media: claim graphs and contradiction surfacing answer the "isn't this just Gemini video Q&A?" judge question head-on. Two costs: a narrower audience (journalists/analysts) weakens the 25% impact narrative, and every claim must be verbatim-quoted or a misquote destroys the product's entire premise.
- **13 LocaleCast.** Meaning-drift in public-safety translation is a real problem and a risky demo — one visible mistranslation of an emergency announcement undermines the whole pitch. Strong JAPAC multilingual angle; better absorbed into ContextBridge as a labeled translation feature than shipped alone.
- **ContextBridge (prior).** See §7 — full treatment there. Short version: strongest execution profile, weakest innovation story as currently scoped; both facts are fixable.

### Future of Work (14–16 + DecisionLoop)

- **14 Meet-to-Move.** Enters the single most saturated category in GenAI (meeting summarizers). Contradiction detection is the only defensible differentiator — and it is a feature, not a product. It is DecisionLoop with smaller scope; same verdict.
- **15 InboxTriage.** Relatable pain and a decent agentic story, but every email client shipped this in 2025. "Drafts cite policy and refuse when none exists" is good engineering that judges will read as table stakes.
- **16 PolicyPal.** The policy version-conflict angle is genuinely interesting; everything else is an internal-tools chatbot. Lowest innovation ceiling in the bank alongside ToolBoxTalk.
- **DecisionLoop (prior).** The strongest enterprise pain in the whole 26 — and the least believable 25-day build: ingesting meetings + email + chat + docs + tickets *convincingly* is not realistic, and judge questions about privacy/permissions are ones a fixture-based prototype cannot answer. The contradiction-detection core deserves to live on — inside Meet-to-Move scope if this theme is ever chosen.

### Sustainability & Social Impact (17–20 + RescueGrid)

- **17 GridGuard.** The estimation layer is the whole product, and it is precisely the part synthetic data cannot validate — a judge cannot tell whether the savings numbers are derived or a lookup table. Weak trust story for a 40%-technical event.
- **18 RescueRoute.** The best *agentic execution* story in the bank: intake → match → schedule → coordinate → human safety gate is a real closed loop, and the two-sided live demo with ticking impact counters is emotionally strong and a natural "Most Impactful Solution" award candidate. The unchallenged cost: two UIs, two personas, choreographed simultaneity — the most demo-moving-parts of any idea. Allergen risk is manageable via "listed/verify, human approves" framing.
- **19 AquaAlert.** A complete, honest workflow with a modest ceiling. "Report a leak" does not emotionally land like food rescue or accessibility, and the who-actually-pays question (municipal procurement) is unanswered.
- **20 AccessPath.** The most *differentiated* idea in the bank — nobody else will build it — and the one with the highest human cost if wrong. The observed/declared/unknown honesty design is genuinely excellent, but it also means the demo's climax is sometimes "we don't know," which is a harder sell on stage than it reads on paper. Maps/geocoding dependency + unconfirmed credits is a real feasibility swing factor. If a teammate has a personal connection to accessibility, this becomes the passion pick; otherwise the risk gate is real.
- **RescueGrid (prior).** Same concept as RescueRoute with slightly broader scope; RescueRoute is the better-scoped version. Verdict: pick RescueRoute's framing if this theme is chosen.


---

## 5. Cross-cutting assumptions, challenged

1. **"Agentic depth" as written is inflated.** Most of the 26 entries describe 3–5 sequential Gemini calls — a prompt chain, not an agent. Judges scoring 40% on Gen AI implementation will probe for tools with side effects, persisted state, guardrails, and evaluation. Only RescueRoute (matching/scheduling tools + human gate), ScamDrill (state machine + guardrails), ClaimLens (multi-service pipeline), and the evidence-grounded Media ideas survive that probe without hand-waving. Whatever is chosen needs real function-calling tools, a state store, and a *published* evaluation set — the build plan's 100-question eval dataset is exactly right; keep it.
2. **"Repo momentum" is partially a myth.** Inspection shows: Q&A in `app.py` is **mocked** (`_ask_gemini` → `_mock_answer`); two divergent frontends exist (a ~1,000-line Streamlit app *and* a barely-started Next.js `web/` scaffold) — that is split effort, not velocity; there is **no git history**; and the build plan's resume note points at a `SchemaSentinel-Strands` worktree path, implying the code may originate from a pre-existing project — a direct eligibility exposure under the fresh-project rule. The genuine assets are `contextbridge_schema.py` (validated canonical schema), `contextbridge_store.py`, one working Vertex AI analysis call path, and TTS in requirements — real, but narrower than "half built."
3. **"Video Q&A demos well" cuts both ways.** It is Google's own flagship Gemini marketing demo; judges may have seen the official version. "Ask a video questions" cannot be the differentiator — evidence (timestamps, confidence, not-found behavior), contradiction surfacing, and accessibility outputs must be. Also: video analysis is slow and token-hungry; the demo needs pre-analyzed content and ≤2-minute samples, with live upload as a bonus, never the critical path.
4. **"Crowded theme = bad" is unproven — but "crowded *pattern* = bad" is real.** Doc-chat (ToolBoxTalk, PolicyPal), meeting summaries (Meet-to-Move, DecisionLoop), and inbox triage lose the 25% innovation axis no matter how well built. BFSI will likely be the most popular theme overall; that alone shouldn't disqualify ScamDrill, but it raises the differentiation bar.
5. **The unconfirmed-resources risk is not evenly distributed.** ScamDrill can degrade to cheap text-only conversation; ContextBridge/StorySplice (video understanding) and ClaimLens/LoanReady (Document AI) cannot. Mitigating evidence: the repo's `server.log`, `contextbridge.db`, `.env.local`, and `__pycache__` indicate a working local Gemini path already exists — but quota *headroom for video* is unverified and must be confirmed in the Discord before committing.
6. **The platform vision scores zero.** "Reusable Multimodal Intelligence Platform serving six verticals" belongs on the scalability slide of the deck, not on the build critical path. One theme, one prototype, one submission.
7. **The Terms include a six-month right of first refusal** for an exclusive license/acquisition (RULES.md). It doesn't change the ranking, but a team with startup intentions should read it before submitting proprietary work.
8. **Deadline-discrepancy risk is real.** Roster lock is stated as both 4 Oct and 11 Oct — plan against the earlier date.


---

## 6. The two `docs/` files, compared

They are different *kinds* of document, and treating either as a neutral evaluation is a mistake:

| | `context/IDEAS.md` | `contextbridge-build-plan.txt` (since removed — D-10) |
|---|---|---|
| **What it is** | A **selection** document: 6 ideas, one per theme, ending in a verdict | An **execution** document: assumes the verdict, defines schema/architecture/phases |
| **Verdict** | ContextBridge 1st, FixFlow 2nd, ShelfSense 3rd | ContextBridge, pre-committed, no alternatives |
| **Strengths** | Worked examples; 3-minute demo scripts; per-idea Gemini-fit rationale; honest risk framing (FixFlow's refusal architecture is excellent) | Trust/eval design (timestamps, not-found, 100-question eval set, metrics) maps perfectly onto the 40% criterion; disciplined MVP scope; a real decision checkpoint |
| **Weaknesses** | One idea per theme artificially constrains the field; no scoring method behind the "final recommendation"; asks "does Gemini fit?" (model capability) instead of "does this demonstrate agentic implementation?" (the actual 40% criterion) | Inherits the selection without re-validating it; "reuse the existing project" collides with the fresh-project rule, and its referenced repo path is a *different project folder* (`SchemaSentinel-Strands` worktree) — provenance red flag; platform ambition is out of scope for scoring; deployment is Phase 7, backwards with a hard deadline |
| **Blind spot** | Never considers that video Q&A might be *too* familiar to judges | Assumes momentum = advantage without auditing what the code actually does (Q&A is mocked) |

**Where they agree:** the same core pattern (multimodal input → grounded analysis → structured answer → safe action) and the same winner (ContextBridge). **Where they conflict:** the ideas doc says "build a small PoC first, switch to FixFlow if it feels generic" — the build plan says "commit to ContextBridge as product #1 of a platform." One treats the choice as provisional, the other as settled. **Net assessment:** the build plan is the more valuable artifact (its trust/eval design and checkpoint are reusable regardless of idea), but its selection premise must be re-earned — which §7 does. IDEAS.md's own neutral conclusion (no winner; ContextBridge/ToolBoxTalk/ShelfAudit safest to ship; FixFlow/AccessPath/ScamDrill/ClaimLens/LoanReady highest safety burden) is consistent with this review's independent scoring.


---

## 7. Recommendation

### Primary: ContextBridge — with three binding amendments

The raw composite puts RescueRoute (4.30) and ScamDrill (4.25) above ContextBridge (3.90). The composite measures *ideas*; the recommendation must measure *executions* against three hard gates:

1. **Time-to-deployed-prototype.** ContextBridge is the only entry with working scaffolding: a validated canonical schema, a persistence layer, a Gemini-on-Vertex analysis call path, TTS already in requirements, and evidence the app has run locally. That is worth 3–5 days of a ~25-day budget, plus it de-risks the biggest unknown ("does Gemini video analysis actually produce our schema?").
2. **Demo reliability.** Content can be pre-analyzed; the live part (Q&A over a known evidence index) is fast and rehearseable. Compare: RescueRoute needs two choreographed UIs updating simultaneously; ScamDrill needs a guardrailed role-play that cannot break character on stage; FixFlow needs refusal paths that fire perfectly.
3. **Safety burden.** Medium and *already specified* — the build plan's trust design (timestamp evidence, confidence, not-found, observation-vs-interpretation) is written down. No other top-5 idea has its guardrails pre-designed.

But ContextBridge as currently scoped loses the 25% innovation axis ("isn't this a Gemini demo notebook?"). Three amendments fix that — all cheap because they reuse the same pipeline:

- **Amendment 1 — Contradiction/claim surfacing (from ContextPulse, #12):** a second structured extraction pass over the *same* `MediaAnalysis` schema that flags conflicting claims. Demo beat: two contradictory statements in one video light up, each timestamped, judge clicks both. Highest-leverage innovation add available.
- **Amendment 2 — One tangible artifact (StorySplice-lite, #11):** multilingual plain-language summary + a shareable evidence card. No rendering pipeline. The accessibility framing (captions, easy-language, audio narration via the already-included Text-to-Speech) doubles as the JAPAC impact story.
- **Amendment 3 — Risk hardening:** pre-computed fixtures + ≤2-minute samples; live Q&A only on pre-analyzed content; audit every existing file's authorship against the 7 Sep window and rebuild anything older; init git **today**; deploy a Cloud Run + Firebase skeleton in week 1 (not Phase 7); pick **one** frontend by day 2 — recommendation: Streamlit for the prototype round (UX is only 10%; the video and deck carry more), Next.js only if a dedicated frontend builder owns it.


### When to override this recommendation

- **Credits/quota for video understanding can't be confirmed by ~27 Sep** → switch to **ScamDrill**. Cheapest text-only path, most memorable demo in the bank, and its guardrail build is the right size for the remaining days.
- **Team is 3–4 strong builders (incl. a frontend dev) and targets the "Most Impactful Solution" award** → **RescueRoute** is the highest-ceiling alternative; accept the two-sided choreography cost.
- **The build plan's checkpoint fails after the first PoC** (timestamps inaccurate, feels like a generic chatbot, judge can't get it in 30 s) → pivot to **ContextPulse**: same theme, same schema, same store, higher innovation, narrower impact story. Lowest possible switching cost.

**Fallback ladder (switching cost ascending):** ContextBridge → ContextPulse (same theme/pipeline) → ScamDrill (new theme, no pipeline reuse) → RescueRoute (new theme, no reuse). Do not switch themes after the roster lock (4/11 Oct).

---

## 8. Actions this week (in order)

1. Confirm cloud/Gemini credits and video-understanding quota in the AI Builder Cup Discord; raise the 4-vs-11-Oct registration discrepancy with the organizer.
2. Audit every existing file's creation date against the 7 Sep eligibility window; document the audit; init a clean git repo and commit fresh work in the open from now on.
3. Choose **one** frontend surface (day 2); shelve the other.
4. Replace `_mock_answer` in `app.py` with the real grounded-Q&A call (video + transcript context) — the current critical-path gap.
5. Assemble the evaluation set (20 short videos, 100 questions with known-answer timestamps) *before* adding features — the eval harness is itself a 40%-criterion asset and demo-able.
6. Deploy the thinnest Cloud Run + Firebase skeleton in week 1; iterate against a live URL.
7. Schedule deck + <3-minute video production now — they are deliverables, not afterthoughts.

