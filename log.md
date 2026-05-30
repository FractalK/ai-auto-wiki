---
type: log
title: Operation Log
created: 2026-04-22
updated: 2026-05-29
last_entry: 2026-05-29
entry_count: 95
---

## [2026-05-29] ingest | Claude Opus 4.6 System Card
Added: [[2026-claude-opus-4-6-system-card]]. Updated: [[anthropic-claude-opus-4-6]], [[ai-alignment]], [[reward-hacking]], [[ai-agentic-workflows]], [[ai-capability-benchmarking]], [[ai-agentic-workflows-pitfalls]], [[ai-alignment-pitfalls]], [[frontier-llm-benchmark-comparison]]. Contradictions flagged: 0. Auto-resolved: 0. New pages created: 2.

## [2026-05-29 PT] session-stats | ingest
Queue size at session start: 1 staged file
Documents attempted: 1
Documents completed: 1
Session limit hit: no (this session was Phase 2 continuation after prior session compaction during pre-flight)
Time window: off-peak
Source type mix: policy-document: 1
Approx tokens (from /cost): unavailable (continuation session)
Notes: HIGH-DENSITY source (53,637 words). Decomposed into 6 chapter chunks. All chunks processed in single session by reading original file in sections — chunk files retained in raw/staged/ until housekeeping. Prior session (same day) handled pre-flight and form generation.

## [2026-05-29 PT] session-stats | ingest (prior session)
Queue size at session start: 2
Documents attempted: 2
Documents completed: 1
Session limit hit: yes — context compaction between pre-flight (prior session) and Phase 2 execution
Time window: off-peak
Source type mix: industry-blog: 1, fetch-failed: 1
Approx tokens (from /cost): unavailable (multi-session)
Notes: OpenAI Codex URL (https://openai.com/index/codex-for-almost-everything/) returned HTTP 403 — marked fetch-failed in queue.md.

## [2026-05-29] ingest | Introducing Claude Opus 4.8
Added: [[2026-anthropic-claude-opus-4-8-announcement]]. Updated: [[anthropic-claude-opus-4-7]] (deprecated, superseded_by [[tools/anthropic-claude-opus-4-8]]), [[anthropic-claude]] (related_tools updated). Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 2 ([[anthropic-claude-opus-4-8]], [[2026-anthropic-claude-opus-4-8-announcement]]).

## [2026-05-28 PT] session-stats | ingest
Queue size at session start: 3 (INGEST-STAGED operation; 3 files in raw/staged/)
Documents attempted: 3
Documents completed: 3
Session limit hit: yes — continued from prior context window (compaction occurred between Phase 1 and Phase 2)
Time window: off-peak
Source type mix: policy-document: 1, research-paper: 1, vendor-content: 1
Approx tokens (from /cost): unavailable (multi-session)
Notes: Phase 1 pre-flight and form generation completed in prior context window; all 3 sources processed in resumed session after user submitted decision string.

## [2026-05-28] ingest | The Agentic AI Landscape and Its Conceptual Foundations
Added: [[2026-oecd-agentic-ai-full-report]]. Updated: [[ai-agentic-workflows]] (data records added, Key Claim 5 co-sourced with full report). Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 1 (source page).

## [2026-05-28] ingest | Algorithmic Monocultures in Hiring
Added: [[2026-bommasani-algorithmic-monocultures-hiring]]. Updated: [[llm-self-preference-bias]] (related_topics). Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 3 ([[algorithmic-monoculture]], [[algorithmic-monoculture-pitfalls]], [[2026-bommasani-algorithmic-monocultures-hiring]]).

## [2026-05-28] ingest | Gemini 3.5: Frontier Intelligence with Action
Added: [[2026-google-gemini-3-5-flash-announcement]]. Updated: [[frontier-llm-benchmark-comparison]] (Gemini 3.5 Flash added as 4th entity). Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 2 ([[google-gemini-3-5-flash]], [[2026-google-gemini-3-5-flash-announcement]]).

## [2026-05-27 PT] session-stats | ingest
Queue size at session start: 2 (INGEST-QUEUE operation; 2 URLs in raw/queue.md [queued])
Documents attempted: 2
Documents completed: 2
Session limit hit: yes — continued from prior context window (compaction occurred between Phase 1 and Phase 2)
Time window: off-peak
Source type mix: vendor-content: 1, publication-article: 1
Approx tokens (from /cost): unavailable (multi-session)
Notes: Phase 1 pre-flight and form generation completed in prior context window; both sources fetched and processed in resumed session. Status correction: IBM Defense Model classified as emerging (not stub — stub is restricted to ingested-in-error correction procedure per schema).

## [2026-05-27] ingest | A First Look at IBM's New Large Language Model Fine-Tuned for Defense Applications
Added: [[2025-ibm-llm-defense-applications]]. Updated: none. Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 2 ([[ibm-defense-model]], [[2025-ibm-llm-defense-applications]]).

## [2026-05-27] ingest | Introducing the IBM Granite 4.1 Family of Models
Added: [[2026-ibm-granite-4-1-models]]. Updated: none. Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 2 ([[ibm-granite-4-1]], [[2026-ibm-granite-4-1-models]]).
  Citation nominations: 2 — DeepStack vision architecture (https://arxiv.org/abs/2406.04334; peer-reviewed), Speech NAR generation (https://arxiv.org/abs/2603.08397; peer-reviewed) — both added to queue.md [nominated].

## [2026-05-27] session-stats | ingest
Queue size at session start: 0 (INGEST-STAGED operation; 2 files in raw/staged/)
Documents attempted: 2
Documents completed: 2
Session limit hit: yes — continued from prior context window
Time window: off-peak
Source type mix: youtube-video: 1, publication-article: 1
Approx tokens (from /cost): unavailable (multi-session)
Notes: session resumed from context compaction; Source 1 complete at session boundary, Source 2 completed in resumed session

## [2026-05-27] ingest | How AI is Transforming Scientific Discovery While Keeping Humans at the Center
Added: [[2026-stanford-hai-ai-science-discovery]]. Updated: [[ai-in-science]] (major), [[ai-governance-policy]], [[ai-capability-benchmarking]]. Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 2 (source page, pitfalls page).

## [2026-05-27] ingest | American Roulette — AI Scenarios for America's Future
Added: [[2026-whitlock-american-roulette-scenarios]]. Updated: [[ai-research-ecosystem]], [[ai-workforce-complementarity]]. Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 1.

## [2026-05-26] ops | teaching relevance — prompt-engineering
[[prompt-engineering]] tagged teaching_relevance: true. Domains: practical-ai-use-and-interaction, output-verification-and-risk-assessment. Contexts: teaching-and-instruction, graduate-and-doctoral-education. Teaching Notes section added (teaching_notes_reviewed: 2026-05-26). Confirmed via B2:A post-ingest decision.

## [2026-05-26] contradiction-resolved | Google NotebookLM
Page: [[google-notebooklm]]
Contradiction ID: CTRD-001
Claim: NotebookLM lacks native mind-map visualization
Resolution path: human-review
Resolution: overridden
Human action: override signal received 2026-05-26 (chat)
Final claim status: current
Note: Human confirmed atlas guide claim is correct — NotebookLM generates AI mind maps as read-only output but lacks import, export, or editing of mind map files; claim text updated to reflect this distinction; [[2025-huang-notebooklm-thirty-minutes]] added as [minority view] source.

## [2026-05-26 PT] session-stats | ingest
Queue size at session start: 0 queued URLs; 3 staged files
Documents attempted: 3
Documents completed: 3
Session limit hit: yes (context window compacted between Phase 1 and Phase 2; Phase 2 executed in resumed session)
Time window: off-peak
Source type mix: research-paper: 1, youtube-video: 2
Notes: Phase 1 pre-flight and form generation completed in prior context window; decision 1:A (create prompt-engineering topic page). All 3 staged sources processed; CTRD-001 flagged on google-notebooklm (mind-map feature — Path B, both sources practitioner weight=1, |diff|=0 ≤ 2).

## [2026-05-26] ingest | The AI System Most People Aren't Building (Gemini + NotebookLM + Gems)
Added: [[2026-question-forward-gemini-notebooklm-workflow]]. Updated: [[google-notebooklm]] (source_count 2→3; KC5 added — notebook-as-stable-knowledge-container principle; multi-notebook prose section added; related_topics adds ai-agentic-workflows), [[ai-agentic-workflows]] (source_count 5→6; three-layer agentic architecture paragraph added to Delegation section; related_tools adds google-notebooklm). Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 1.

## [2026-05-26] ingest | NotebookLM In 30 Minutes
Added: [[2025-huang-notebooklm-thirty-minutes]]. Updated: [[google-notebooklm]] (source_count 1→2; KC3 updated with save-to-notes; KC4 expanded to full Studio suite — Audio/Video Overviews, Mind Maps, Reports; KC2 marked contested CTRD-001; no-chat-history limitation added). Contradictions flagged: 1 (CTRD-001).
Auto-resolved: 0. New pages created: 1.

## [2026-05-26] contradiction-flag | Google NotebookLM
Page: [[google-notebooklm]]
Claim: NotebookLM lacks native mind-map visualization
Contesting source: [[2025-huang-notebooklm-thirty-minutes]] (practitioner, weight=1)
Existing support score: 1
Resolution path: human-review
Contradiction ID: CTRD-001
Override window closes: 2026-06-02

## [2026-05-26] ingest | Mind Your Tone: Investigating How Prompt Politeness Affects LLM Accuracy
Added: [[2025-dobariya-prompt-politeness-llm-accuracy]]. Updated: none. Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 2 ([[prompt-engineering]], [[2025-dobariya-prompt-politeness-llm-accuracy]]).
  Citation nominations: Yin et al. 2024 (ACL SICon; peer-reviewed), Webb et al. 2023 (Nature Human Behaviour; peer-reviewed) — both added to queue.md [nominated].

## [2026-05-26] query | instructor summary — agentic AI, delegation, accountability for leadership course
Pattern: synthesis
Result quality: rich
Topic tags: agentic-ai, delegation, human-in-the-loop, accountability, trust-calibration
Pages consulted: 10 — [[ai-agentic-workflows]], [[ai-agentic-workflows-pitfalls]], [[prompt-injection]], [[prompt-injection-pitfalls]], [[scalable-oversight]], [[ai-trustworthiness]], [[ai-trustworthiness-pitfalls]], [[responsible-ai-government-evaluation]], [[ai-workforce-complementarity]], [[ai-governance-policy]]
Filed: yes — [[teaching/agentic-ai-delegation-accountability-instructor-brief]]
Gap nominations surfaced: no

## [2026-05-26] query | instructor summary — AI capabilities and failure modes for leadership course
Pattern: synthesis
Result quality: rich
Topic tags: ai-capabilities, failure-modes, hallucination, output-verification, accountability, organizational-trust
Pages consulted: 14 — [[llm-fundamentals]], [[llm-fundamentals-pitfalls]], [[ai-trustworthiness]], [[ai-trustworthiness-pitfalls]], [[legal-ai-hallucination]], [[legal-ai-hallucination-pitfalls]], [[ai-alignment]], [[ai-alignment-pitfalls]], [[scalable-oversight]], [[llm-self-preference-bias]], [[llm-self-preference-bias-pitfalls]], [[ai-search-citation-accuracy]], [[ai-search-citation-accuracy-pitfalls]], [[reward-hacking]]
Filed: yes — [[teaching/ai-capabilities-failure-modes-instructor-brief]]
Gap nominations surfaced: no

## [2026-05-25] lint | pass 3
Pages assessed: 102. Stale flags: 5 (L5c — stale data records, informational only). Contradiction flags: 0.
Support scores recalculated: 1 (L3 — openai-gpt-5-5 anomaly resolved via source schema fix). Teaching Index regenerated.
Collection gaps confirmed: 0 | addressed: 0 | dismissed: 0.
Source schema fix: [[2026-vellum-llm-leaderboard]] — corrected credibility_tier (vendor-content → practitioner) and source_type (practitioner-reference → vendor-content); caused erroneous L3 score flag.
L16 wikilink proliferation (first run): 20 Tier 1 candidates confirmed (decision 1:A). Insertions across 14 pages: [[ai-alignment]] ×3, [[reward-hacking]] ×4, [[reinforcement-learning-from-human-feedback]] ×3, [[retrieval-augmented-generation]] ×2, [[sycophancy]] ×1, [[prompt-injection]] ×2, [[constitutional-ai]] ×1, [[jailbreaking]] ×2, [[red-teaming]] ×1, [[ai-alignment]] ×1.
L7 concept gaps: 1,841 candidates dismissed (all schema structural terms or Teaching Notes template labels); 0 new gap stubs.
Orphan pages (L6): 15 informational — no action.

## [2026-05-22] lint | pass 2
Pages assessed: 99. Stale flags: 0. Contradiction flags: 0.
Support scores recalculated: 0. Teaching Index regenerated.
Collection gaps confirmed: 0 | addressed: 0 | dismissed: 0.
Schema fixes: teaching_notes_reviewed added to [[ai-in-higher-education-pitfalls]]; non-schema fields (teaching_relevance, competency_domains, professional_contexts) removed from [[frontier-llm-benchmark-comparison]].
Concept gap stubs created: [[reinforcement-learning-from-human-feedback]], [[sycophancy]], [[red-teaming]].
Schema drift (L11): Key Claims count >5 flagged on [[ai-alignment]], [[ai-in-medicine]], [[ai-workforce-complementarity]] — acknowledged, correction deferred to next ingest session.
Skill file flag: EXTRACTION-SKILL.md § 6.2 and CONTRADICTION-SKILL.md § 7 (all 5 subsections) remain unpopulated after 25+ ingests.

## [2026-05-21 PT] session-stats | ingest
Queue size at session start: 0 queued URLs; 2 staged files
Documents attempted: 2
Documents completed: 2
Session limit hit: yes (context compaction occurred mid-session; Phase 2 writes completed in resumed session)
Time window: off-peak
Source type mix: publication-article: 1, research-paper: 1
Notes: Resumed from compacted context. All wiki writes, index updates, and teaching-index regeneration completed in resumed session.

## [2026-05-21] ingest | Trust in AI: Progress, Challenges, and Future Directions
Added: [[2024-afroogh-trust-ai-review]]. Created: [[ai-trustworthiness]] (teaching_relevance: true, 5 Key Claims, Support Score 1.5 — decay applied: source published 2024-11-17, ~18 months old), [[ai-trustworthiness-pitfalls]] (7 failure modes). Contradictions flagged: 0. Auto-resolved: 0. New pages created: 3.
  Nominated entry removed from queue.md: "Perceived personal agency and AI reliance" (same URL as Afroogh et al.; now ingested as [[2024-afroogh-trust-ai-review]]).

## [2026-05-21] ingest | Agentic AI at Scale: Redefining Management for a Superhuman Workforce
Added: [[2025-mit-sloan-bcg-agentic-ai-management]]. Updated: [[ai-agentic-workflows]] (source_count 4→5; Key Claims 1 and 3 replaced with governance/accountability claims from MIT Sloan/BCG; Organizational Implications expanded; Teaching Notes updated — teaching_notes_reviewed reset to 2026-05-21). Created: [[ai-agentic-workflows-pitfalls]] (7 failure modes). Contradictions flagged: 0. Auto-resolved: 0. New pages created: 2.

## [2026-05-20 PT] session-stats | ingest
Queue size at session start: 0 queued URLs; 3 staged files
Documents attempted: 3
Documents completed: 2 (Source 1 aborted — exact URL duplicate, user choice 1:A)
Session limit hit: yes (context window compaction occurred between Phase 1 and Phase 2)
Time window: off-peak
Source type mix: publication-article: 2, duplicate-aborted: 1
Notes: Phase 1 pre-flight completed in prior context window; Phase 2 executed in resumed session after compaction.

## [2026-05-20] ingest | Who's at Fault when AI Fails in Health Care?
Added: [[2024-stanford-hai-healthcare-ai-liability]]. Updated: [[ai-in-medicine]] (source_count 1→2; Key Claim 5 on healthcare AI liability added; legal-practice added to professional_contexts). Created: [[ai-in-medicine-pitfalls]] (8 failure modes, teaching_relevance: true — auto-applied, criterion A: 2 competency domains). Contradictions flagged: 0. Auto-resolved: 0. New pages created: 2.
  Citation nominated: 1 — Mello & Guha, NEJM 2024 (https://www.nejm.org/doi/full/10.1056/NEJMhle2308901).

## [2026-05-20] ingest | The AI Efficiency Trap: When Productivity Tools Create Perpetual Pressure
Added: [[2025-walther-ai-efficiency-trap]]. Created: [[ai-efficiency-trap]], [[ai-efficiency-trap-pitfalls]] (5 failure modes, teaching_relevance: true). Contradictions flagged: 0. Auto-resolved: 0. New pages created: 3.
  Citation nominated: 1 — Perceived personal agency and AI reliance, Humanities and Social Sciences Communications (https://www.nature.com/articles/s41599-024-04044-8).

## [2026-05-20] ingest | The AI Index 2026 Annual Report — Part 11: Appendix (enrichment pass)
Appendix contains supplementary methodology and data tables only; no substantive claims extractable for wiki pages. No pages updated. Contradictions flagged: 0. Auto-resolved: 0. New pages created: 0.

## [2026-05-20] ingest | The AI Index 2026 Annual Report — Part 10: Public Opinion (enrichment pass)
Added: [[ai-public-opinion]] (new Topic page — global survey evidence on expert-public optimism gap, regional variation, workplace adoption, trust in AI governance institutions; teaching_relevance proposed; 5 Key Claims, 15 Data Records). Updated: [[ai-companion-risks]] (Data Records section created — 5 rows on expert-forecast AI companion adoption: 10%/15%/30% daily use by 2027/2030/2040; global and US Ipsos-Google excitement). Contradictions flagged: 0. Auto-resolved: 0. New pages created: 1.

## [2026-05-20] ingest | The AI Index 2026 Annual Report — Part 09: Policy and Governance (enrichment pass)
Updated: [[ai-governance-policy]] (summary updated; prose fully restructured with rolling overwrite — AI Sovereignty section added (5-dimension framework; European supercomputing 3→44 clusters 2018–2025; data localization East Asia Pacific 77 vs North America 3 laws); US Legislative Activity section added (state bills <10 in 2020 → 150 in 2025; Congressional witnesses 5→102; California 62 total bills); Public Investment section added (US \$20.5B public 2013–2024 vs \$285.9B private in 2025; EU country-level investments); Data Records section expanded from 3→16 rows; related_topics updated to add [[ai-public-opinion]] and [[ai-compute-and-infrastructure]]). Contradictions flagged: 0. Auto-resolved: 0. New pages created: 0.

## [2026-05-20] ingest | The AI Index 2026 Annual Report — Part 08: Education (enrichment pass)
Updated: [[ai-in-higher-education]] (source_count 4→5; summary updated; Section 2 compressed; "Institutional and Policy Dimensions" section replaced with "Scale, Policy Gap, and K–12 Context" — 80% global student adoption, policy gap data, K–12 CS/AI curriculum landscape, China/UAE AI mandates; Key Claim 5 gained [[2026-stanford-hai-ai-index]] as additional source, support score 1→3; Data Records section created with 6 rows on adoption rates, CS enrollment, master's graduate trends, policy coverage; related_topics added [[ai-research-ecosystem]]), [[ai-research-ecosystem]] (source_count 1→2; Talent section updated with AI PhD placement reversal — industry share 77%→65%, academic share nearly doubled 2022–2024; Data Records section created with 12 rows covering model landscape, patent data, talent flows, and PhD placement). Contradictions flagged: 0. Auto-resolved: 0. New pages created: 0.

## [2026-05-20] ingest | The AI Index 2026 Annual Report — Part 07: Medicine (enrichment pass)
Updated: [[ai-in-medicine]] (status stub→developing; full prose body written; 2 existing KCs updated, 3 new KCs added — MAI-DxO 85.5% vs 20% physicians, FDA 1,357 devices with only 2.4% RCT-supported, molecular scale paradox GPN-Star 200M > Evo 2 40B; added Molecular and Genomic AI section, Clinical Applications and Deployment section, Patient Engagement and Ethics section; related_topics expanded to include ai-in-science, ai-agentic-workflows). Contradictions flagged: 0. Auto-resolved: 0. New pages created: 0.

## [2026-05-20] ingest | The AI Index 2026 Annual Report — Part 06: Science (enrichment pass)
Updated: [[ai-in-science]] (status stub→developing; full prose body written; 3 existing KCs updated; 2 new KCs added — end-to-end science agents + AI publication growth; added Performance on Scientific Tasks and Autonomous Science Agents sections; PaperArena 38.8% vs. 83.5% PhD baseline, PHYBench 36.9% vs. 61.9%, Google AI Co-Scientist, Sakana AI Scientist-v2, Aardvark Weather). Contradictions flagged: 0. Auto-resolved: 0. New pages created: 0.

## [2026-05-20] ingest | The AI Index 2026 Annual Report — Part 05: Economy (enrichment pass)
Updated: [[ai-workforce-complementarity]] (summary updated; added workforce exposure gap and occupational churn paragraph in Evidence section; expanded Adoption/Productivity section with additional studies — METR −19%, accountants +55%, authors +200%, learning penalties, macro J-curve, OECD G7 projections, executive survey; updated Key Claim 5 precision fix "from 2022 peak"; added Key Claim 6 on macro J-curve; 7 new Data Records), [[ai-compute-and-infrastructure]] (summary updated; added Investment and Capital Flows prose section; 9 new Data Records). Contradictions flagged: 0. Auto-resolved: 0. New pages created: 0.

## [2026-05-20] ingest | The AI Index 2026 Annual Report — Part 04: Responsible AI (enrichment pass)
Enriched: [[2026-stanford-hai-ai-index]] (related_topics: added [[ai-companion-risks]], [[jailbreaking]], [[ai-alignment]]). Updated: [[ai-companion-risks]] (status stub→developing; source_count 1→2; added Companion System Design and Safety Tradeoffs prose section; 4th and 5th KC on INTIMA benchmark and Replika/Zhang et al. relational harm findings), [[jailbreaking]] (status stub→developing; source_count 0→1; full prose written; 3 KC on HELM Safety ceiling, AILuminate jailbreak degradation, Grok July 2025 incident), [[ai-alignment]] (source_count 1→2; added RAI Dimension Tradeoffs prose section; 6th KC on safety/fairness/accuracy tradeoffs from Kemmerzell/Cecchini/Wasif studies), [[ai-governance-policy]] (expanded International Coordination: Paris AI Action Summit 2025 + AI Safety Institutes; expanded AI Incident Trends: organizational RAI maturity 2.3/4, governance role growth 17%, ISO/IEC 42001 and NIST AI RMF adoption), [[ai-research-ecosystem]] (Publications: added RAI paper geographic shift — China 812 vs US 394 in 2025, reversing 2024 US lead). Contradictions flagged: 0. Auto-resolved: 0. New pages created: 0.
  Teaching relevance proposals pending (see post-ingest summary PS items).

## [2026-05-20] ingest | The AI Index 2026 Annual Report — Part 03: Technical Performance (enrichment pass)
Enriched: [[2026-stanford-hai-ai-index]] (related_topics: added [[retrieval-augmented-generation]]). Updated: [[ai-capability-benchmarking]] (source_count 1→2; added Performance Convergence prose section; 5th KC on frontier convergence + US-China parity; 13 new Data Records including Arena Elo, GPQA Diamond, HLE, SWE-bench Verified, OSWorld, MMLU-Pro, ClockBench), [[ai-agentic-workflows]] (source_count 3→4; Data Records section added: OSWorld, GAIA, WebArena, MLE-bench, τ-bench, Cybench, Terminal-Bench), [[retrieval-augmented-generation]] (status stub→developing; source_count 0→1; full prose written; 2 new source KCs added; Data Records added: context window growth, LongBench v2, MTEB), [[llm-hallucination]] (source_count 1→2; Context Grounding Failure section added; 4th KC on document grounding failure in legal benchmarks). Contradictions flagged: 0. Auto-resolved: 0. New pages created: 0.
  Citation harvesting: Corrêa et al. 2025 (PlanBench) at https://arxiv.org/pdf/2511.09378 — peer-reviewed; nominated to queue.md.

## [2026-05-20] ingest | The AI Index 2026 Annual Report — Part 02: Research and Development (enrichment pass)
Enriched: [[2026-stanford-hai-ai-index]] (related_topics updated). Updated: [[ai-capability-benchmarking]] (Data Records section added: AIME 2025 benchmark data for 5 models; Transparency prose enriched with Chapter 1 parameter/training-code disclosure data). New pages created: 2 — [[ai-compute-and-infrastructure]] (developing, 5 KC, Data Records), [[ai-research-ecosystem]] (developing, 5 KC). Contradictions flagged: 0. Auto-resolved: 0.

## [2026-05-20 20:00 PT] session-stats | ingest
Queue size at session start: 0 queued URLs
Documents attempted: 1 (ai_index_report_2026.pdf — enrichment pass, Part 01 of 11)
Documents completed: 1
Session limit hit: no
Time window: off-peak
Source type mix: white-paper: 1
Notes: Large-document decomposition. 11 chunk files + manifest created in raw/staged/ (gitignored). Part 01 (intro-top-takeaways, 3,311 words) processed this session. Parts 02-11 queued for subsequent sessions via manifest.

## [2026-05-20] ingest | The AI Index 2026 Annual Report — Part 01: Introduction and Top Takeaways (enrichment pass)
Enriched: [[2026-stanford-hai-ai-index]] (updated, enriched: 2026-05-20). Updated: [[ai-governance-policy]] (source added, new prose: AI Incident Trends and Responsible AI Gap, AI Sovereignty and Public Trust, Data Records), [[ai-workforce-complementarity]] (new prose: adoption/consumer value/productivity, Data Records). New pages created: 2 — [[ai-in-science]] (stub, 3 KC), [[ai-in-medicine]] (stub, 2 KC). Contradictions flagged: 0. Auto-resolved: 0.

## [2026-04-30] ingest | AI Coding Agents Guide: A Map of the Four Workflow Types
Added: [[2026-realpython-coding-agent-workflow-types]]. Updated: none. Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 3 ([[ai-coding-agent-workflow-types]], [[ai-coding-agent-workflow-types-pitfalls]], [[2026-realpython-coding-agent-workflow-types]]).

## [2026-04-30] ingest | AI Threats in the Wild: The Current State of Prompt Injections on the Web
Added: [[2026-google-prompt-injection-wild]]. Updated: [[llm-fundamentals-pitfalls]] (source added, prompt injection entry expanded with empirical findings). Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 3 ([[prompt-injection]], [[prompt-injection-pitfalls]], [[2026-google-prompt-injection-wild]]).

## [2026-04-30] ingest | Introducing GPT-5.5
Added: [[2026-openai-gpt-5-5-announcement]]. Updated: none. Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 3 ([[openai-gpt-5-5]], [[openai-gpt-5-5-pro]], [[2026-openai-gpt-5-5-announcement]]).

## [2026-04-30] session-stats | ingest
Queue size at session start: 2
Documents attempted: 3
Documents completed: 3
Session limit hit: yes (context window exhausted; resumed in second session)
Time window: off-peak
Source type mix: practitioner-reference: 1, industry-blog: 1, vendor-content: 1
Approx tokens (from /cost): not captured (session split across two context windows)

## [2026-05-18] ingest | The AI Index 2026 Annual Report (Stanford HAI)
Added: [[2026-stanford-hai-ai-index]]. Updated: [[llm-hallucination]] (stub→developing; 3 Key Claims added from KaBLE benchmark and RAI reporting gap data), [[ai-workforce-complementarity]] (source_count 1→2; Key Claim 5 added on early-career developer employment decline; labor market prose extended), [[ai-agentic-workflows]] (source_count 2→3; OSWorld benchmark data added to Equation of Agentic Work prose), [[ai-in-higher-education]] (source_count 3→4; student AI adoption statistics and policy gap data added to Institutional and Policy Dimensions prose), [[llm-fundamentals-pitfalls]] (failure_mode_count 8→9; Benchmark Saturation and Gaming added to Technical Limitations), [[ai-alignment-pitfalls]] (failure_mode_count 7→8; Responsible AI Dimension Tradeoffs added to Alignment and Safety Concerns). Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 2 ([[2026-stanford-hai-ai-index]], [[ai-capability-benchmarking]]).

## [2026-05-18 PT] session-stats | ingest
Queue size at session start: 0 (0 queue URLs; 1 staged file)
Documents attempted: 1
Documents completed: 1
Session limit hit: yes (context window exhausted after pre-flight; Phase 2 executed in resumed session after compaction)
Time window: off-peak
Source type mix: white-paper: 1
Approx tokens (from /cost): not captured (session resumed from prior context summary)
Notes: PDF extracted via pypdf (425 pages, 24MB). 5 pre-flight decisions; all confirmed. Teaching relevance proposals for llm-hallucination and ai-capability-benchmarking deferred to next lint or ingest — not included in pre-flight.

## [2026-05-18] ingest | Vellum LLM Leaderboard 2026
Added: [[2026-vellum-llm-leaderboard]]. Updated: [[anthropic-claude-opus-4-7]] (capabilities list), [[openai-gpt-5-5]] (ARC-AGI-2 Key Claim source field, support score 1→2). Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 2 ([[2026-vellum-llm-leaderboard]], [[frontier-llm-benchmark-comparison]]).

## [2026-05-18] ingest | Critically Evaluating AI — The CRAAP Model (Bristol)
Added: [[2026-bristol-craap-ai-evaluation]]. Updated: [[ai-in-higher-education]] (CRAAP paragraph added to Student-Side Considerations; KC4 corroborated, support score 1→2). Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 2 ([[2026-bristol-craap-ai-evaluation]], [[ai-in-higher-education-pitfalls]]).

## [2026-05-18] ingest | New MIT Sloan Research Suggests AI Is More Likely to Complement, Not Replace, Human Workers
Added: [[2025-mit-sloan-ai-complement-workers]]. Updated: [[llm-fundamentals-pitfalls]] (Statistical Boundary Conditions failure mode added; failure_mode_count 7→8). Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 2 ([[2025-mit-sloan-ai-complement-workers]], [[ai-workforce-complementarity]]).

## [2026-05-18 PT] session-stats | ingest
Queue size at session start: 3
Documents attempted: 3
Documents completed: 3
Session limit hit: yes (context window exhausted after pre-flight; continued in resumed session)
Time window: off-peak
Source type mix: practitioner-reference: 2, publication-article: 1
Approx tokens (from /cost): not captured (session resumed from prior context summary)
Notes: session ran out of context after writing all 10 content files; infrastructure updates completed in second session

## [2026-04-30] ops | teaching notes back-population
Teaching notes written: 29 pages. Fields added: teaching_notes_reviewed. No ingest performed.

## [2026-04-22] ingest | LLM Wiki
Added: [[2026-karpathy-llm-wiki-pattern]]. Updated: none. Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 2 ([[llm-wiki-pattern]], [[2026-karpathy-llm-wiki-pattern]]).

## [2026-04-22] ingest | Automated Alignment Researchers
Added: [[2026-anthropic-automated-alignment-researchers]]. Updated: none. Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 3 ([[scalable-oversight]], [[weak-to-strong-supervision]], [[2026-anthropic-automated-alignment-researchers]]).

## [2026-04-22] ingest | Using LLMs to Improve Workplace Social Skills
Added: [[2026-stanford-hai-llms-workplace-skills]]. Updated: none. Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 2 ([[ai-assisted-skills-training]], [[2026-stanford-hai-llms-workplace-skills]]).

## [2026-04-22] ingest | Management as AI Superpower
Added: [[2026-mollick-management-ai-superpower]]. Updated: none. Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 2 ([[ai-agentic-workflows]], [[2026-mollick-management-ai-superpower]]).

## [2026-04-22] ingest | Emotion Concepts and Their Function in a Large Language Model
Added: [[2026-anthropic-emotion-concepts-llm]]. Updated: [[scalable-oversight]] (new Key Claim, source_count 1→2). Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 2 ([[llm-functional-emotions]], [[2026-anthropic-emotion-concepts-llm]]).

## [2026-04-22] ingest | Constitutional Classifiers: Defending against Universal Jailbreaks
Added: [[2025-anthropic-constitutional-classifiers-jailbreaks]]. Updated: none. Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 2 ([[constitutional-classifiers]], [[2025-anthropic-constitutional-classifiers-jailbreaks]]).

## [2026-04-22 04:55 PT] session-stats | ingest
Queue size at session start: 5
Documents attempted: 5
Documents completed: 2
Session limit hit: no
Time window: off-peak
Source type mix: practitioner-reference: 1, industry-blog: 1, fetch-failed: 3
Notes: 3 Stanford HAI URLs returned no usable content (content truncated by fetch tool, no article text delivered); tagged [fetch-failed] in queue.md

## [2026-04-22 12:30 PT] session-stats | ingest
Queue size at session start: 7 (4 staged files + 3 queue.md URLs)
Documents attempted: 5
Documents completed: 4
Session limit hit: no
Time window: peak
Source type mix: industry-blog: 3, publication-article: 1, fetch-failed: 1
Notes: ctl.stanford.edu/aimes/ai-teaching-strategies returned 403; tagged [fetch-failed]. 2 arxiv/transformer-circuits nominations added to queue.md [nominated].

## [2026-04-22] ingest | AI Teaching Strategies
Added: [[undated-stanford-ctl-ai-teaching-strategies]]. Updated: none. Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 2 ([[ai-in-higher-education]] (partial), [[undated-stanford-ctl-ai-teaching-strategies]]).
  Note: Source fetched from URL after staged file was found to be truncated (pre-flight forced choice 1:A).

## [2026-04-22] ingest | AI and Your Learning: A Guide for Students
Added: [[undated-stanford-ctl-student-ai-guide]]. Updated: [[ai-in-higher-education]] (source_count 1→2, Key Claims added). Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 1 ([[undated-stanford-ctl-student-ai-guide]]).
  Citation nominated: 1 — Dunlosky et al. 2013 (Psychological Science in the Public Interest) — evaluated as practitioner tier per venue logic; not added to nominated queue.

## [2026-04-22] ingest | Project Glasswing: Securing critical software for the AI era
Added: [[2026-anthropic-project-glasswing]]. Updated: none. Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 3 ([[anthropic-claude-mythos-preview]], [[ai-assisted-vulnerability-discovery]], [[2026-anthropic-project-glasswing]]).
  Citations nominated: 5 — Anthropic Red Team blog posts (3) and OpenAI cyber resilience post (1) added to queue.md [nominated]; Anthropic research/building-ai-cyber-defenders added to queue.md [nominated].

## [2026-04-22] ingest | AI Alignment Paradox: Claude Mythos (MindStudio)
Added: [[2026-mindstudio-claude-mythos-alignment-paradox]]. Updated: [[anthropic-claude-mythos-preview]] (source_count 1→2, Key Claim 4 added). Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 3 ([[constitutional-ai]], [[mindstudio]], [[2026-mindstudio-claude-mythos-alignment-paradox]]).
  Source type: vendor-content (practitioner, vendor_bias: true).

## [2026-04-22] ingest | How to Use NotebookLM Effectively for Research and Study
Added: [[2026-atlas-notebooklm-usage-guide]]. Updated: none. Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 2 ([[google-notebooklm]], [[2026-atlas-notebooklm-usage-guide]]).

## [2026-04-22] ingest | Introducing Claude Opus 4.7
Added: [[2026-anthropic-claude-opus-4-7-announcement]]. Updated: none. Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 2 ([[anthropic-claude-opus-4-7]], [[2026-anthropic-claude-opus-4-7-announcement]]).

## [2026-04-22] session-stats | ingest
Queue size at session start: 6 (4 staged files + 2 queue.md URLs)
Documents attempted: 6
Documents completed: 6
Session limit hit: no
Time window: peak
Source type mix: practitioner-reference: 2, industry-blog: 3, vendor-content: 1
Approx tokens (from /cost): not captured — /cost not run before log write
Notes: Source 1 staged file was truncated; URL fetched successfully via agent subagent.

## [2026-04-22] skill-enrichment | EXTRACTION-SKILL.md § 6.1
Case: Staged file existed in raw/staged/ but was truncated (intro only, body absent); pre-flight forced choice offered URL fallback; URL fetch succeeded via subagent despite prior session 403.

## [2026-04-22] skill-enrichment | TAGGING-SKILL.md § 5.1
Case: Two tool pages created same session required opposite teaching_relevance decisions — google-notebooklm tagged (practitioner-sourced, observable behaviors) vs. mindstudio deferred (all coverage vendor-sourced, all Key Claims carry vendor-bias hedging).

## [2026-04-22] ingest | AI Teaching Strategies (enrichment)
Added: (enrichment — no new source page). Updated: [[ai-in-higher-education]] (prose additions: safety valve mechanism, AI dependency risk, CJR citation corroboration). Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 0.
  Note: staged file was full content matching prior URL fetch; Key Claims at ceiling (5), no new claims added.

## [2026-04-22] ingest | AI and Your Learning: A Guide for Students (enrichment)
Added: (enrichment — no new source page). Updated: none (existing Key Claims and prose fully capture source content). Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 0.

## [2026-04-22] ingest | Can we create a clear understanding of what agentic AI is and does?
Added: [[2026-oecd-agentic-ai-landscape]]. Updated: [[ai-agentic-workflows]] (source_count 1→2, definitional intro added, OECD Key Claim 5 added). Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 1 ([[2026-oecd-agentic-ai-landscape]]).
  Citation nominated: 1 — OECD full report "The agentic AI landscape and its conceptual foundations" added to queue.md [nominated].

## [2026-04-22] ingest | Claude For Dummies
Added: [[2026-hassid-claude-beginners-guide]]. Updated: none. Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 4 ([[anthropic-claude]], [[openai-chatgpt]], [[anthropic-claude-vs-openai-chatgpt]], [[2026-hassid-claude-beginners-guide]]).

## [2026-04-22] session-stats | ingest
Queue size at session start: 4 (4 staged files + 0 queued URLs)
Documents attempted: 4
Documents completed: 4
Session limit hit: no
Time window: off-peak
Source type mix: practitioner-reference: 2 (enrichment), publication-article: 1, practitioner-reference: 1
Approx tokens (from /cost): not captured

## [2026-04-23] ingest | Claude Opus 4.7 — A New Frontier, in Performance and Drama
Added: [[2026-aiexplained-claude-opus-4-7]]. Updated: [[anthropic-claude-opus-4-7]] (source_count 1→2, limitations extended, prose updated), [[anthropic-claude-mythos-preview]] (source_count 2→3, prose updated with survey methodology critique and Vidok findings). Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 1 ([[2026-aiexplained-claude-opus-4-7]]).

## [2026-04-23] ingest | The AI Dilemma with Tristan Harris
Added: [[2025-pivot-harris-ai-dilemma]]. Updated: none. Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 3 ([[2025-pivot-harris-ai-dilemma]], [[ai-companion-risks]], [[ai-governance-policy]]).

## [2026-04-23] session-stats | ingest
Queue size at session start: 2 (2 staged files + 0 queued URLs)
Documents attempted: 2
Documents completed: 2
Session limit hit: no
Time window: off-peak
Source type mix: youtube-video: 2
Approx tokens (from /cost): not captured

## [2026-04-25] ingest | On the Emergence of Position Bias in Transformers
Added: [[2025-emergence-position-bias-transformers]]. Updated: none. Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 2 ([[llm-position-bias]], [[2025-emergence-position-bias-transformers]]).
  Citation harvesting: full-depth extraction; no URL-resolvable citations identified in fetched content.
  Teaching relevance deferred for [[llm-position-bias]] — page created at stub status.

## [2026-04-25] ingest | AI on Trial: Legal Models Hallucinate in 1 out of 6 (or More) Benchmarking Queries
Added: [[2024-ai-trial-legal-models-hallucinate]]. Updated: none. Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 7 ([[legal-ai-hallucination]], [[legal-ai-hallucination-pitfalls]], [[legal-ai-tools-hallucination-comparison]], [[lexisnexis-lexis-plus-ai]], [[thomson-reuters-westlaw-ai]], [[thomson-reuters-ask-practical-law-ai]], [[2024-ai-trial-legal-models-hallucinate]]).

## [2026-04-25] ingest | AI Search Has a Citation Problem
Added: [[2025-ai-search-citation-problem]]. Updated: [[openai-chatgpt]] (source_count 1→2, Key Claim 3 added, status stub→developing). Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 4 ([[ai-search-citation-accuracy]], [[ai-search-citation-accuracy-pitfalls]], [[ai-search-tools-citation-comparison]], [[2025-ai-search-citation-problem]]).

## [2026-04-26] ingest | AI Alignment: A Comprehensive Survey
Added: [[2025-ai-alignment-comprehensive-survey]]. Updated: [[scalable-oversight]] (source_count 3→4, prose update on IDA/RRM/Debate/CIRL), [[weak-to-strong-supervision]] (source_count 1→2, Key Claim 5 added). Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 5 ([[ai-alignment]], [[reward-hacking]], [[goal-misgeneralization]], [[ai-alignment-pitfalls]], [[2025-ai-alignment-comprehensive-survey]]).
  Citation harvesting: full-depth extraction; all bibliography citations use author+year format without resolvable URLs in the extracted content — no nominations generated.

## [2026-04-26] ingest | AI Self-preferencing in Algorithmic Hiring: Empirical Evidence and Insights
Added: [[2026-self-preference-llm-hiring]]. Updated: none. Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 3 ([[llm-self-preference-bias]], [[llm-self-preference-bias-pitfalls]], [[2026-self-preference-llm-hiring]]).
  Spot-check — [[2026-self-preference-llm-hiring]]:
    Claim: LLMs prefer LLM-generated resumes at 67–82% self-preference rate. Source passage: documented in experimental conditions on the ArXiv hiring dataset with multiple LLM evaluators.
    Claim: 23–60% shortlisting advantage for LLM-generated content. Source passage: shortlisting rates compared between AI-generated and human-written resumes under the same evaluator.
    Claim: Self-recognition is the primary mechanism. Source passage: when model self-recognition is reduced experimentally, self-preference declines proportionally.
    Claim: Mitigations reduce bias 60–71%. Source passage: system prompting and majority voting each achieve 60–71% reduction in self-preference rates.

## [2026-04-26] ingest | [1hr Talk] Intro to Large Language Models
Added: [[2023-karpathy-intro-large-language-models]]. Updated: [[scalable-oversight]] (source_count 2→3, prose addition). Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 3 ([[llm-fundamentals]], [[llm-fundamentals-pitfalls]], [[2023-karpathy-intro-large-language-models]]).

## [2026-04-25 PT] session-stats | ingest
Queue size at session start: 3 (3 staged files + 0 queued URLs)
Documents attempted: 3
Documents completed: 3
Session limit hit: no
Time window: off-peak
Source type mix: publication-article: 2, research-paper: 1
Notes: Source 3 staged file was MIT News article (thin practitioner); user selected 1:B to fetch full ICML 2025 arxiv paper instead (peer-reviewed, full extraction). All 3 staged files moved to raw/processed/.

## [2026-04-26 PT] session-stats | ingest
Queue size at session start: 3 (3 staged files + 0 queued URLs)
Documents attempted: 3
Documents completed: 3
Session limit hit: no
Time window: off-peak
Source type mix: youtube-video: 1, research-paper: 2
Notes: Source 3 staged file was MIT News article about the alignment survey (thin practitioner); user selected 1:B to fetch full arxiv paper instead (practitioner tier, full-depth extraction). All 3 staged files moved to raw/processed/.

## [2026-04-26] skill-enrichment | TAGGING-SKILL.md § 5.2
Case: Three Pitfalls pages created in the same session had different domain profiles — llm-fundamentals-pitfalls mapped to practical-ai-use-and-interaction + output-verification, ai-alignment-pitfalls to ai-safety-and-alignment-literacy + output-verification, and llm-self-preference-bias-pitfalls to output-verification + ai-integration — demonstrating that Pitfalls page domain tagging is not uniform and must be derived from the failure mode content, not the page type.

## [2026-04-27] ingest | Responsible AI for Public Evaluation
Added: [[2025-responsible-ai-public-evaluation]]. Updated: none. Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 2 ([[responsible-ai-government-evaluation]], [[2025-responsible-ai-public-evaluation]]).
  Source: white-paper (IBM Center for The Business of Government), practitioner, staged PDF.

## [2026-04-27] ingest | Government in the AI Era
Added: [[2025-ibm-government-ai-era]]. Updated: [[ai-governance-policy]] (source_count 1→3, status stub→developing, teaching_relevance tagged, 2 Key Claims added, prose expanded with US policy reversals and IBM survey data). Contradictions flagged: 0.
Auto-resolved: 0. New pages created: 3 ([[2025-ibm-government-ai-era]], [[ai-governance-policy-pitfalls]], pitfalls page for ai-governance-policy).
  Source: white-paper (IBM Institute for Business Value), practitioner, staged PDF.
  Fetch-failed: 3 queued URLs (openai.com/introducing-gpt-5-5/, thenewstack.io/disappearing-ai-middle-class/, openai.com/strengthening-cyber-resilience/) — all returned 403 or access-blocked. Tagged [fetch-failed] in queue.md.

## [2026-04-27 PT] session-stats | ingest
Queue size at session start: 5 (2 staged files + 3 queued URLs)
Documents attempted: 5
Documents completed: 2
Session limit hit: no
Time window: off-peak
Source type mix: white-paper: 2, fetch-failed: 3
Approx tokens (from /cost): not captured
Notes: 3 queued URLs all returned 403 or access-blocked errors; user instructed to proceed with PDFs only. Both staged PDFs processed successfully; moved to raw/processed/.

## [2026-04-28] lint | pass 1
Pages assessed: 39 (21 Topics, 9 Tools, 3 Comparisons, 6 Pitfalls). Sources in wiki: 24.
Support scores recalculated: 1 page (4 claims updated: constitutional-classifiers 2→1).
Expired contradictions auto-confirmed: 0 — none
CTRD-NNN signals processed: 0 — none
Pages downgraded to stale: 1 — [[anthropic-claude-vs-openai-chatgpt]]
Orphan pages flagged: 2 — [[mindstudio]], [[anthropic-claude-vs-openai-chatgpt]]
Concept gaps surfaced: 1 — confirmed: [[retrieval-augmented-generation]] stub created
decay_exempt confirmed: 0 — none
Schema drift flags: 0 — none (1 individual deviation auto-corrected: openai-chatgpt status developing→active)
Teaching relevance ratio: 76.7% (above 20% threshold)
Collection gaps confirmed: 0 | addressed: 0 | dismissed: 0
Nominations aged to stale: 0 — none
Stale nominations deleted: 0 — none
Teaching Index regenerated: no
Skill enrichment staleness flags: 1 — CONTRADICTION-SKILL.md § 7 (all 5 sub-sections unpopulated after 26 ingests)

## [2026-04-29] schema-change | DM-081–DM-086
Applied DM-081 through DM-086: teaching notes (DM-081, DM-082), teaching-brief page type and
instructor summary query mode (DM-083), lint cadence guideline (DM-084), OPERATIONS.md split
executed (DM-085), ingest operation mode separation INGEST-STAGED/INGEST-QUEUE/INGEST-BOTH (DM-086).
Added OPERATIONS.md to wiki root. Created teaching/ directory. Updated CLAUDE.md, wiki-verify.sh,
and pre-commit hook. Regenerated prompts/ stubs (7 stubs; deleted old ingest.md).
Pages affected: 0 content pages; scaffold and operational files updated. Sources processed: 0.

## [2026-05-03] lint | pass 2
Pages assessed: 46 (24 topics + 11 tools + 8 pitfalls + 3 comparisons). Stale flags: 0 new.
Contradiction flags: 0. Support scores recalculated: 35 (all topic and tool pages). Teaching Index regenerated.
Collection gaps confirmed: 0 | addressed: 0 | dismissed: 0.
CTRD-NNN signals processed: 0 — none.
Pages downgraded to stale: 0.
Orphan pages flagged: 0 new (mindstudio remains orphan from lint 1; no ingest has addressed it).
Concept gaps created: 2 — [[jailbreaking]] (stub), [[llm-hallucination]] (stub).
Schema corrections auto-applied: 28 pages corrected updated field to 2026-04-30 (teaching notes back-population on 2026-04-30 had not updated frontmatter).
Teaching Index updated: excerpts added for all 33 teaching-tagged pages (Teaching Notes sections present since 2026-04-30 back-population; excerpts were absent from prior index generation).
Skill enrichment staleness flags: 3 — CONTRADICTION-SKILL.md § 7 (5 sub-sections still unpopulated); TAGGING-SKILL.md §§ 5.3–5.4 (placeholder); EXTRACTION-SKILL.md §§ 6.2–6.4 (placeholder).
Note: anthropic-claude-vs-openai-chatgpt remains status: stale — comparison updated 2026-04-29 is now older than anthropic-claude.md corrected to 2026-04-30. Schema has no automated upgrade path for comparison pages; recommend manual review.

## [2026-05-21] vocab-expansion | software-and-ai-development
Pages assessed: 45. Additions confirmed: 8. Pages updated: [[topics/ai-coding-agent-workflow-types]], [[topics/prompt-injection]], [[topics/ai-assisted-vulnerability-discovery]], [[topics/llm-wiki-pattern]], [[pitfalls/ai-coding-agent-workflow-types-pitfalls]], [[pitfalls/prompt-injection-pitfalls]], [[tools/anthropic-claude-opus-4-7]], [[tools/anthropic-claude-mythos-preview]].
Teaching Index regenerated: yes.
