# Idea Review — AI Builder Cup 2026 (V2)

**Date:** 2026-09-25 · **Nature:** independent critical re-review — supersedes the 2026-09-23 draft while preserving its section anchors (`§6` docs comparison, `§7` fallback ladder) referenced by `REQUIREMENTS.md` and `DECISIONS.md` D-10.

**Inputs:** `context/HACKATHON.md`, `context/RULES.md` (incl. the Compass-era engineering guardrails), `context/RESOURCES.md`, `context/IDEAS.md` (the 26-idea bank: 20 new + earlier six preserved), **and both historical `docs/` files** — `docs/ai-builder-cup-ideas.txt` (six-idea selection doc; since merged into `IDEAS.md` and deleted) and `docs/contextbridge-build-plan.txt` (execution plan; deleted by `DECISIONS.md` D-10) — each read in full and compared in §6. Also weighed: the actual repository and deployment state (39 in-window commits, `api/` FastAPI service, `web/` Next.js surface, 83 tests, live Cloud Run stack, eval harness v2).

> **Preserved historical annotation (D-10):** `docs/contextbridge-build-plan.txt` was superseded by `context/ARCHITECTURE.md` + `context/BUILD_PLAN.md` and removed; citations treat it as a historical input.

## Verdict up front

**ContextBridge (Media, Content & Digital Experiences) — the strongest direction, now re-earned by execution rather than inherited.** It survives every hard gate (deadline, deployability, safety, Gemini fit) and is no longer just "the idea with scaffolding": it is a deployed, evaluated product with the three amendments the 2026-09-23 draft demanded already shipped (contradiction surfacing = P0-4/A1, tangible artifact = P0-5/A6, risk hardening = fixtures + deploy-first + 25-case eval). Its weakest axis was always **innovation** ("isn't this a Gemini video demo?") — the Compass-era answers to that (EvidenceBadge trust worlds, ExploreSuggestions, BoundaryCard, clarify/simplify moves, honest not-found) are live and measured (unsupported-answer rate 0.0%, suggestions coverage 100%). **Fallback if the direction were being chosen today from scratch: ScamDrill (BFSI). Highest-ceiling alternative: RescueRoute (Sustainability).** No new contender from the bank overtakes the primary — see §7.

---

## 1. Constraints that dominate every score

1. **~23 days remain** (25 Sep → prototype deadline 18 Oct; roster lock possibly 4 Oct — treat the earlier date). The budget also covers the PDF deck, a strictly-under-3-minute video, a **public GitHub repo**, and the deployed prototype. Effective build time ≈ 13–16 days.
2. **Judging weights:** Technical Merit & Gen AI 40%, Problem Alignment & Impact 25%, Innovation & Creativity 25%, UX & Design 10%. "Useful" loses; the demo must *show* agentic, grounded, tool-using Gen AI with evidence.
3. **Resources:** RESOURCES.md still publishes no credits/quotas/keys — but the repo now proves a working Vertex path (D-11 smoke PASS, live Cloud Run serving Gemini). The unverified part is *quota headroom* (video-understanding volume for uploads + eval runs), not credentials.
4. **Fresh-project rule:** only 7 Sep–18 Oct work is eligible. Mitigated in practice: git initialised 24 Sep, first commit explicitly "in-window" with `context/PROVENANCE.md`, 39 commits since, `_mock_answer` deleted from the product path. **Open: no git remote yet** — the public-repo artifact does not exist.
5. **One team = one theme = one submission.** Platform visions score zero.
6. **Compass guardrails** (`RULES.md`): no new endpoints, no new pages/routes, no new `web/` dependencies, gates (`quote_matches_transcript`, ≤2 LLM rounds, `notInVideo` invariant) untouchable. These now *constrain idea selection*: any pivot must fit inside the locked architecture or it is not a pivot, it is a restart.
7. **Team size unknown (2–4 allowed).** Time-to-build scores assume a small team.

## 2. Method — the ten dimensions, scored 1–5

| Dimension | 5 means |
|---|---|
| **Hackathon fit** | Dead-center of one official theme + showcases the Google stack the rules name |
| **Innovation** | Novel vs. both market products and the likely hackathon field |
| **Agentic-AI depth** | Genuine multi-step tool use, state, guardrails — not a prompt chain |
| **User value** | Real, frequent, felt pain with a clear beneficiary |
| **Feasibility** | Buildable on synthetic fixtures; no hardware, bank, or platform APIs |
| **Demo impact** | Wow + comprehension in <3 minutes; legible in a 30-second judge pitch |
| **Time-to-build** | Comfortably shippable in ~13–16 effective days |
| **Resource availability** | Survives unconfirmed quotas (cheap models, small payloads) |
| **Differentiation** | Defensible answer to "haven't I seen this demo before?" |
| **Risk** | 5 = safe. Safety/legal/eligibility/demo-failure exposure (risk ≤2 is a **gate**, not averaged away) |

**Composite formula (sums to 100, preserving the official 40/25/25/10 intent):** agentic 20 · feasibility 10 · time-to-build 10 (5 under Technical Merit + 5 under UX/polish) · resources 5 · fit 10 · value 10 · demo 10 (5 under Impact + 5 under UX) · innovation 15 · differentiation 10. Demo and time are double-counted exactly as the official rubric implies. Scores are informed judgment from the source documents and repo inspection, not measurements; the formula was spot-checked to reproduce every entry sampled (ContextBridge 3.90, RescueRoute 4.30, ScamDrill 4.25).

---

## 3. Scoring matrix — all 26 ideas

### 3.1 Earlier six (original `ai-builder-cup-ideas.txt`, preserved in `IDEAS.md`)

| Idea | Theme | Fit | Innov | Agentic | Value | Feasib | Demo | Time | Resrc | Diff | Risk | Composite |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TrustLens | BFSI | 5 | 3 | 3 | 5 | 4 | 4 | 4 | 4 | 3 | 3 ⚠ | 3.75 |
| ShelfSense | Retail | 4 | 3 | 3 | 4 | 4 | 5 | 3 | 4 | 3 | 4 | 3.55 |
| FixFlow | Manufacturing | 5 | 4 | 4 | 5 | 3 | 5 | 2 | 4 | 4 | 2 ⛔ | 4.00 |
| **ContextBridge** | Media | 5 | 3 | 3 | 4 | 5 | 5 | 5 | 3 | 3 | 4 | 3.90* |
| DecisionLoop | Future of Work | 4 | 3 | 4 | 4 | 3 | 3 | 3 | 4 | 3 | 3 | 3.45 |
| RescueGrid | Sustainability | 5 | 3 | 5 | 4 | 4 | 5 | 3 | 4 | 4 | 3 | 4.15 |

\* plus the only real code head start at selection time — see §5 and §9.

### 3.2 New bank (`IDEAS.md` ideas 1–20)

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

**Read this ranking honestly:** the raw composite favors RescueRoute and ScamDrill over ContextBridge. The composite measures *ideas*; §7 re-ranks them as *executions* against three hard gates (time-to-deployed-prototype, demo reliability, safety burden pre-designed). If you dispute those gates, the honest alternatives sit at the top of the table.

---

## 4. Per-idea critique — the weakest assumption, challenged

### BFSI (1–4 + TrustLens)

- **1 ClaimLens.** Strongest BFSI pipeline on paper (classify → Document AI → vision → checklist → triage), but the demo depends on two extraction services *agreeing* on fixtures the team must author, and coverage-authority risk turns a third of the UI into disclaimers.
- **2 LoanReady.** Quietly requires the agent to be *right about eligibility* across divergent JAPAC guidelines; the permanent "not a lending decision" frame erodes the wow of the climbing score.
- **3 ChargebackCoach.** Genuinely fresh (reason-code taxonomies are obscure and real) with a clean refusal path, but the pain is episodic — judges don't *feel* it in three minutes.
- **4 ScamDrill.** Best demo *concept* in the bank (judge plays, falls for the fake QR, gets scored) and cheapest to run — but one broken rail is a catastrophic stage failure, free-form role-play is the hardest thing to rehearse, and "we built a scam simulator" needs disciplined dual-use framing (script-bounded scenarios, permanent SIMULATION banner, bank-training narrative).
- **TrustLens (prior).** Hugely relatable but an *analyzer* — and analyzers are a JAPAC hackathon staple. It can never say "safe" (a false negative is real harm), which flattens the demo into hedged language. ScamDrill is the strictly more memorable variant of the same theme.

### Retail (5–7 + ShelfSense)

- **5 ShelfAudit.** Lowest risk in the bank; the unchallenged assumption is that Gemini vision counts facings reliably on *unstaged* photos. Decide which demo you're doing — don't discover on stage.
- **6 ReturnSense.** B2B pain judges don't personally feel, and "probably a fraudster" is demo-unfriendly output no matter how it's labeled.
- **7 ShelfNudge.** Honest, buildable, boring — forecast charts lose a live demo to flashier entries. Better as a feature inside ShelfSense than a submission.
- **ShelfSense (prior).** Photos + invoices + CSV + voice + reorder is four products in one trench coat; the prior doc concedes the accessibility angle "must be central" because the tech is ununique. If chosen: cut to two inputs.

### Manufacturing (8–10 + FixFlow)

- **8 ShiftHandover.** Most underrated idea here: the demo beat — catching a safety hold that was *said* but never *written*, with the exact quote — is a perfect three-minute moment, and voice+photo input is a distinctive multimodal story. Its flaw is persuading judges this is Manufacturing (not Future of Work).
- **9 DefectDesk.** Solid quality-analytics loop, but "photos clustered by line → ranked hypotheses" needs several logged defects *and* an attentive judge to land; incremental vs. existing machine-vision QC.
- **10 ToolBoxTalk.** The safest, fastest build (RAG with citations) and the weakest innovation score — doc-chat is the most commodited pattern in the bank. Its honest "not in your manuals" demo is its only memorability.
- **FixFlow (prior).** Best physical-world story and a genuinely sophisticated refusal architecture — gated on verified manual + machine ID + safety conditions + human approval. But risk 2 is a *gate*: an imperfect refusal on stage is worse than no demo, and it had the worst time-to-build of the prior six.

### Media (11–13 + ContextBridge)

- **11 StorySplice.** High wow (finished clip + captions), but real video assembly is where hackathon weekends go to die, and hooks derived from quotes invite misrepresentation claims if the footage isn't owned.
- **12 ContextPulse.** The innovation answer *within* the chosen theme: claim-graph + contradiction detection is materially harder than summarization and demonstrably not a chatbot. Its flaw is value legibility — fact-checking needs a journalist narrative the judges must be walked into.
- **13 LocaleCast.** JAPAC-native multilingual angle with a built-in "Most Impactful" story; the drift-check queue is a smart honesty device. Weakened by TTS/caption-sync fiddliness and the weight of "official announcement" expectations.
- **ContextBridge (prior).** The only entry that arrived with working scaffolding — validated schema, store, Vertex call path — and a trust/eval design that maps directly onto the 40% criterion. Its weaknesses: familiarity (video Q&A is Google's own flagship demo), analysis latency (must pre-compute), and — at selection time — a *mocked* Q&A path and two half-built frontends (both since resolved: §5, §9).

### Future of Work (14–16 + DecisionLoop)

- **14 Meet-to-Move.** DecisionLoop's contradiction-detection core with buildable scope (meetings only). Still fights the meeting-summary crowd; the ledger-vs-new-action conflict beat must carry the demo.
- **15 InboxTriage.** Relatable pain, respectable retrieval+drafting agent — but "draft replies grounded in policy" is a pattern every team will ship; the no-policy-found refusal is doing all the differentiation work.
- **16 PolicyPal.** The version-conflict demo (stale handbook superseded) is clever and cheap; the overall shape is doc-chat with a verdict, which caps innovation at 2.
- **DecisionLoop (prior).** Broadest FoW ambition (meetings + email + chat + docs + tickets) = breadth trap; privacy/permissions as the gating risk can't be shown honestly without synthetic fixtures everywhere. Meet-to-Move is the salvageable core.

### Sustainability (17–20 + RescueGrid)

- **17 GridGuard.** Document parsing + tariff tools + honest ranges is respectable; appliance-level estimates from a bill photo invite a fact-check the demo can't survive.
- **18 RescueRoute.** Highest composite (4.30): two-sided matching + scheduling tools + human safety gate is *real* agentic depth, and live counters ticking up is the best emotional demo in the bank. Cost: two choreographed UIs and allergen-framing discipline.
- **19 AquaAlert.** Full report → route → close workflow with quantified waste — strong. The assumption: liters/day estimates hold up only with published flow tables plus staff confirmation.
- **20 AccessPath.** Accessibility-first positioning is powerful and the observed/declared/unknown honesty model is sophisticated — but risk 2 is earned: image-inferred accessibility claims that turn out wrong harm real people, and "venue not verified" is the most likely outcome for a judge's chosen location.
- **RescueGrid (prior).** Same concept as RescueRoute with broader scope; RescueRoute's tighter two-sided framing is the better-scoped version.

---

## 5. Cross-cutting assumptions, challenged

1. **"Agentic depth" across the bank is mostly inflated.** Most entries describe 3–5 sequential Gemini calls — a prompt chain, not an agent. Judges scoring 40% on Gen AI implementation probe for tools with side effects, persisted state, guardrails, and *evaluation*. Only RescueRoute (matching/scheduling + human gate), ScamDrill (state machine + rails), ClaimLens (multi-service pipeline), and the evidence-grounded Media ideas survive that probe without hand-waving. Whatever is chosen needs real function-calling tools, a state store, and a published evaluation set.
2. **"Repo momentum" was partially a myth at selection time — and is now true.** The 2026-09-23 draft found: mocked Q&A (`_ask_gemini` → `_mock_answer`), two divergent frontends, no git history, and a resume note pointing at a *different project folder* (`SchemaSentinel-Strands` worktree) — a provenance red flag. **As of 2026-09-25 all four are resolved:** the agent path is real with the mock deleted (D-14, enforced by `test_api_package_contains_no_mock_answer_path`); Next.js `web/` is the single committed surface (D-01) with Streamlit removed from requirements (D-12); git holds 39 in-window commits with `PROVENANCE.md`; and the stack is deployed and evaluated on Cloud Run. Remaining gap: **no git remote** — the public-repo artifact still does not exist.
3. **"Video Q&A demos well" cuts both ways.** It is Google's own flagship Gemini marketing demo; judges may have seen the official version. Evidence (timestamps, confidence, not-found), contradiction surfacing, and accessibility outputs must be the differentiator — which is exactly what the Compass amendments deliver. Video analysis stays slow and token-hungry: pre-analyzed content remains the demo path; live upload is a bonus, never critical.
4. **"Crowded theme = bad" is unproven — but "crowded *pattern* = bad" is real.** Doc-chat (ToolBoxTalk, PolicyPal), meeting summaries (Meet-to-Move, DecisionLoop), and inbox triage lose the 25% innovation axis no matter how well built. BFSI will be the most popular theme; that raises ScamDrill's differentiation bar rather than disqualifying it.
5. **Unconfirmed-resource risk is not evenly distributed.** ScamDrill degrades to cheap text-only conversation; video-understanding and Document AI pipelines cannot. Credentials are no longer hypothetical (D-11 Vertex smoke PASS; live stack serving), but **quota headroom for video** remains unverified — confirm in Discord before committing to any upload-heavy demo plan.
6. **The platform vision scores zero.** "Reusable Multimodal Intelligence Platform" belongs on the scalability slide, not the build critical path. One theme, one prototype, one submission — the old build plan's multi-vertical framing was correctly banned by `PRODUCT.md` §1/§11.
7. **The Terms include a six-month right of first refusal** (RULES.md). It does not change the ranking, but a team with startup intentions should read it before submitting proprietary work.
8. **Deadline-discrepancy risk is real.** Roster lock is stated as both 4 Oct and 11 Oct — plan against the earlier date; every week-3/4 task compresses if 4 Oct binds.

---

## 6. The two `docs/` files, compared

Both files were read in full for this review; both have since been removed from the tree — `docs/ai-builder-cup-ideas.txt` merged into `context/IDEAS.md` ("Earlier six-idea round"), `docs/contextbridge-build-plan.txt` deleted by `DECISIONS.md` D-10. They remain different *kinds* of document, and treating either as a neutral evaluation is a mistake:

| | `docs/ai-builder-cup-ideas.txt` | `docs/contextbridge-build-plan.txt` |
|---|---|---|
| **What it is** | A **selection** document: six ideas (one per theme), worked examples, 3-minute demo scripts, per-idea Gemini-fit rationale, ending in a verdict | An **execution** document: assumes the verdict, defines the canonical schema, reusable intelligence layer, phases 1–7, trust/eval design |
| **Verdict** | ContextBridge 1st, FixFlow 2nd, ShelfSense 3rd — with an explicit "small PoC first, switch if it feels generic" escape hatch | ContextBridge pre-committed as product #1 of a "Reusable Multimodal Intelligence Platform"; no alternatives considered |
| **Strengths** | Honest risk framing (FixFlow's refusal architecture; "never claim certainty"); asks "does Gemini fit?" and answers per idea; preserves the switch option | Trust/eval design (timestamp evidence, confidence, not-found, 100-question eval set, metrics) maps perfectly onto the 40% criterion; disciplined MVP scope; a real decision checkpoint |
| **Weaknesses** | One idea per theme artificially constrains the field; no scoring method behind the final recommendation; "Gemini fit" (model capability) is the wrong question — the rubric scores *agentic implementation* | Inherits the selection without re-validating it; "reuse the existing project" collides with the fresh-project rule and its resume note pointed at a *different project folder* (`SchemaSentinel-Strands`); platform ambition scores zero; deployment parked as Phase 7 backwards from a hard deadline |
| **Blind spots** | Never considers that video Q&A might be *too* familiar to judges (it's Google's own demo) | Assumes momentum = advantage without auditing what the code actually did (Q&A was mocked) |

**Where they agree:** the same core pattern (multimodal input → grounded analysis → structured answer → safe action) and the same winner (ContextBridge). **Where they conflict:** the ideas doc treats the choice as *provisional* ("build a small PoC first, switch to FixFlow if generic"); the build plan treats it as *settled* ("commit as platform product #1"). One is a hypothesis, the other is a plan.

**What the verdicts got right:** ContextBridge was chosen — and executed. Its checkpoint questions ("timestamps accurate? evidence UI understandable? not a generic chatbot? Cloud usage meaningful? judge gets it in 30s?") are now measurable: sweep P0-1..P0-9 pass on the live URL, eval v2 reports 94.4% timestamp accuracy / 92.0% groundedness / 0.0% unsupported / 100% suggestions coverage over 25 cases, and the Compass UI (EvidenceBadge, BoundaryCard, ExploreSuggestions) answers the "generic chatbot" challenge directly. **What they got wrong:** the ideas doc's runner-up (FixFlow) never got built because its risk gate was real; the build plan's platform framing was correctly banned (D-10, `PRODUCT.md` §1/§11), its provenance hint was a genuine red flag (resolved via `PROVENANCE.md` + in-window git history), and "deployment in Phase 7" was inverted in practice — deploy-first (P0-9 early) is now a standing rule. **Net assessment:** the build plan remains the more valuable artifact *as engineering culture* (its eval discipline is the 40%-criterion backbone), but its selection premise had to be re-earned — §7 and §9 do that.

---

## 7. Recommendation

### Primary: ContextBridge (Media) — reaffirmed, with the three binding amendments now largely shipped

The raw composite puts RescueRoute (4.30) and ScamDrill (4.25) above ContextBridge (3.90). The composite measures *ideas*; the recommendation must measure *executions* against three hard gates:

1. **Time-to-deployed-prototype.** ContextBridge was the only entry with a validated schema, a persistence layer, and a working Vertex call path — worth 3–5 days of the budget and de-risking the biggest unknown ("does Gemini video analysis actually produce our schema?"). *Now moot as an advantage but decisive as momentum:* the product is built, deployed (revisions `api-00009`/`web-00009`), and evaluated. Switching themes today forfeits 39 commits and every green checkpoint.
2. **Demo reliability.** Content is pre-analyzed; the live part (Q&A over a known evidence index) is fast (3.59 s avg) and rehearseable. RescueRoute needs two choreographed UIs updating simultaneously; ScamDrill needs a role-play that cannot break character on stage; FixFlow needs refusal paths that fire perfectly.
3. **Safety burden.** Medium and *already specified* — timestamp evidence, confidence, not-found behavior, observation-vs-interpretation, eval dataset. No other top-5 idea has its guardrails pre-designed.

The three amendments the original draft demanded as the price of ContextBridge's weaker innovation axis:

- **Amendment 1 — Contradiction/claim surfacing (from ContextPulse #12).** → **SHIPPED:** P0-4 + `contradiction-card.tsx`, surfaced on `demo-binary` with both timestamps clickable (sweep-verified).
- **Amendment 2 — One tangible artifact (StorySplice-lite #11).** → **SHIPPED:** P0-5 accessible outputs + A6 copyable evidence card, timestamps preserved (sweep-verified; Hindi translation demonstrated live).
- **Amendment 3 — Risk hardening.** → **LARGELY SHIPPED:** fixtures + demo-first sequencing (P0-9 early, now a standing rule), provenance audit + in-window git history, single frontend (Next.js), 25-case eval harness. **Outstanding:** public remote/video/deck (Week 4), quota-headroom confirmation.

### When to override this recommendation

- **Quota headroom for video understanding can't be confirmed** → the fixture path already carries the demo (Drill 5 proves the stack serves without live API); only *new* analysis is at risk. If the team were restarting, **ScamDrill** is the cheapest text-only fallback.
- **Team decides to re-enter selection for a higher ceiling** → **RescueRoute** (Sustainability), accepting the two-sided choreography cost and the allergen-verification gate framing burden.
- **Build plan's checkpoint fails in rehearsal** (timestamps fumble, feels generic, judge can't get it in 30 s) → narrow to **ContextPulse**: same theme, same schema, same store, higher innovation, narrower story — lowest possible switching cost.

**Fallback ladder (switching cost ascending):** ContextBridge → ContextPulse (same theme/pipeline) → ScamDrill (new theme, no pipeline reuse) → RescueRoute (new theme, no reuse). Do not switch themes after roster lock (4 Oct / 11 Oct — assume the earlier).

---

## 8. Actions (updated for 2026-09-25; ordered)

1. **Create the public GitHub remote and push** — the submission's public-repo artifact does not exist yet (no `git remote` configured). Highest-severity open compliance item.
2. **Confirm quota headroom** for video-understanding in the AI Builder Cup Discord; re-raise the 4-vs-11-Oct roster discrepancy.
3. **Schedule deck + strictly-under-3-minute video production now** (DoD #10 / P0-11 are the only unchecked Definition-of-Done items; both are Week 4).
4. **Fix the doc drift** noted in this review cycle: `REQUIREMENTS.md` still names Streamlit as "the committed surface" (superseded by D-01); keep P1-6 wording consistent with the single-frontend reality.
5. **Keep lint in the gate** — `npm run lint` was silently red until D-33; wire it into any pre-commit/CI habit, not just `next build`.
6. **Rehearse against the checkpoint questions** (build plan §13) with peers or judges before freeze; the numbers for the deck already exist (`context/eval_results.json`).

---

## 9. Re-validation at Week 3 complete (2026-09-25) — how the review holds up against reality

| Claim in this review | Verified against | Status |
|---|---|---|
| Repo momentum was partly myth (mocked Q&A, split frontends, no git) | D-14 + `test_api_package_contains_no_mock_answer_path`; D-01/D-12 (single Next.js surface); 39 in-window commits + `PROVENANCE.md` | ✅ Resolved (git remote still absent → §8.1) |
| Innovation axis needed amendment 1 (contradiction surfacing) | P0-4/A1 `contradiction-card.tsx`; sweep confirms clickable pair at 5s/15s on `demo-binary` | ✅ Shipped & sweep-verified |
| Amendment 2 (tangible artifact) | P0-5 + A6 evidence card; sweep confirms beginner explanation + Hindi translation with source timestamps | ✅ Shipped & sweep-verified |
| Amendment 3 (risk hardening: fixtures, deploy-first, eval set) | P0-6 fixtures serve with zero external deps (Drill 5); P0-9 deployed; eval v2 25 cases in `context/eval_results.json` | ✅ Shipped (public artifacts pending) |
| Eval discipline is the 40%-criterion backbone | 25-case harness: 94.4% timestamp accuracy, 92.0% groundedness, 0.0% unsupported, 100% suggestions coverage, 3.59 s avg — on live Cloud Run | ✅ Exceeds DoD #9 thresholds (92%/100%) |
| "Not a chatbot" differentiation must come from evidence + boundary UX | EvidenceBadge 3 states, BoundaryCard (web-only frame), ExploreSuggestions, honest not-found — all in `assistant-message.tsx` paths, all tested | ✅ Shipped (Compass pillars P1–P3 in code) |
| Lint/build gates must be real gates | `npm run lint` was exiting 1 (setState-in-effect) while validations recorded "build passed" — fixed under D-33; lint now 0 errors | ⚠️ Was false-green; repaired this review |
| One theme / one submission; platform framing scores zero | `PRODUCT.md` §1/§11 bans the platform brand; single Media submission maintained | ✅ Holding |
| Deadline: plan against 4 Oct roster lock | Week 4 (Demo Proof) remains open — the only unchecked DoD item is #10 (submission artifacts) | ⏳ On track, not yet done |

**Honest residual risks (unchanged by this review):** video-quota headroom unconfirmed; no public repo/video/deck yet; `REQUIREMENTS.md` Streamlit lines stale; evaluation-phase judges may still ask "what makes this not a Gemini demo" — the answer must be demonstrated in the first 30 seconds (evidence click → exact moment; boundary card; contradiction pair), not narrated.

---

*End of review. Scores are judgment, not measurement; the recommendation is falsifiable via the override conditions in §7.*
