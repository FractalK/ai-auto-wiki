---
type: tool
title: Claude Opus 4.7
created: 2026-04-22
updated: 2026-06-23
summary: Anthropic's generally available frontier model as of April 2026, with major advances in software engineering, vision, document reasoning, and agentic task execution over Opus 4.6, at unchanged pricing with a tokenizer update that increases effective token consumption.
status: active
vendor: Anthropic
pricing_model: usage-based
access_tier:
  - consumer
  - api
  - enterprise
capabilities:
  - Advanced software engineering and agentic coding (70% CursorBench, 93.9% SWE-bench Verified at Opus 4.6-scale; ranks 1st on SWE-bench at 87.6% per Vellum LLM Leaderboard April 2026, ahead of Claude Sonnet 4.5 at 82% and Claude Opus 4.5 at 80.9%)
  - Vision up to 2,576px long edge (~3.75 megapixels); 98.5% XBOW visual-acuity benchmark
  - Document reasoning with 21% fewer errors than Opus 4.6 on OfficeQA Pro
  - Long-horizon agentic task execution with task budget controls
  - Extended thinking with xhigh effort control level
  - Legal reasoning at 90.9% BigLaw Bench (high effort)
  - Financial analysis at 0.813 General Finance benchmark
limitations:
  - Tokenizer update increases effective token consumption 1.0–1.35× depending on content type; prompts tuned for Opus 4.6 may need re-evaluation
  - Modestly weaker harm-reduction for controlled substances compared to Opus 4.6 per safety evaluation
  - Safety evaluation characterizes alignment as "largely well-aligned and trustworthy, though not fully ideal"
  - Underperforms Opus 4.6 on BrowseComp (agentic web search benchmark); Mythos Preview also underperforms GPT-5.4 on the same benchmark
  - Adaptive thinking is mandatory; the model autonomously determines inference depth and defaults to medium effort; users cannot force extended thinking without actively overriding to high or max
primary_use_cases:
  - Professional software engineering and code review
  - Document-heavy analysis and legal/financial workflows
  - Long-horizon agentic task execution
  - Vision-intensive document processing
source_count: 6
last_assessed: 2026-06-23
related_tools:
  - "[[anthropic-claude-mythos-preview]]"
related_topics:
  - "[[prompt-injection]]"
  - "[[sycophancy]]"
  - "[[ai-model-welfare]]"
  - "[[human-ai-collaboration]]"
  - "[[ai-agentic-workflows]]"
teaching_relevance: true
competency_domains:
  - capability-horizon-awareness
  - tool-evaluation-and-selection
professional_contexts:
  - project-and-program-management
  - entrepreneurship-and-startups
  - software-and-ai-development
technical_depth: practitioner
teaching_notes_reviewed: 2026-04-30
prior_generation: "true"
succeeded_by: "[[anthropic-claude-opus-4-8]]"
---

Claude Opus 4.7 is Anthropic's flagship generally available model as of April 2026, positioned as a substantial advance over Opus 4.6 in software engineering, vision, document reasoning, and agentic workflow execution. It is available through the Claude consumer interface, the Anthropic API, Amazon Bedrock, Google Cloud Vertex AI, and Microsoft Foundry. Pricing is unchanged at \$5/\$25 per million input/output tokens, though a tokenizer update means effective token consumption increases by 1.0–1.35× depending on content type — operators should re-evaluate prompt costs before assuming cost parity with Opus 4.6.

## Software Engineering Performance

The most significant advance in Opus 4.7 is in real-world software engineering. On CursorBench, the model achieves 70% compared to 58% for Opus 4.6. On Rakuten's SWE-Bench evaluation against production tasks, Opus 4.7 resolves 3× more tasks than Opus 4.6. *(vendor-aggregated — benchmark selection, model inclusion, and methodology reflect commercial context; treat rankings and scores with caution)* On an internal 93-task coding benchmark, Opus 4.7 shows a 13% improvement. These improvements extend to code review: CodeRabbit reports +10% precision improvement, and Notion Agent reports +14% performance improvement with fewer tokens and a 1/3 reduction in tool errors.

Early-access partners including Cursor, Replit, Vercel, Harvey, Databricks, and others provided testimonials at launch, reflecting broad enterprise adoption in software development workflows.

## Vision and Document Reasoning

Opus 4.7 introduces support for images up to 2,576 pixels on the long edge, approximately 3.75 megapixels — more than triple the prior Claude image resolution. On XBOW's visual-acuity benchmark, Opus 4.7 achieves 98.5% compared to 54.5% for Opus 4.6, a 44 percentage point improvement that reflects a qualitative advance in visual reasoning capability. On OfficeQA Pro, a document reasoning benchmark, Opus 4.7 produces 21% fewer errors than Opus 4.6.

These improvements make Opus 4.7 materially better suited for workflows involving scanned documents, charts, visual data, and image-heavy PDFs.

## Agentic Workflow Controls

Opus 4.7 introduces two new controls for agentic task management. Task budgets (public beta) allow operators to set a per-task computational spend cap, enabling predictable cost management for long-horizon agentic workflows. The `xhigh` effort control level provides a new ceiling above existing effort settings for tasks requiring maximum reasoning depth. These controls are particularly relevant for deployment contexts where agentic tasks run at scale with variable complexity.

The Claude Code CLI gains a `/ultrareview` command with this release, enabling multi-agent cloud-based code review.

One significant behavioral change in Opus 4.7 is mandatory adaptive thinking: the model autonomously determines inference depth based on its assessment of task difficulty and defaults to medium effort. Prior Claude models could be configured to always engage extended reasoning; Opus 4.7 cannot be forced to do so without explicit effort-level specification (high or max). This change appears linked to Anthropic's compute constraints — external reports indicate thinking character counts declined substantially in prior Claude models before this release, with medium effort becoming the enforced default. Users running heavy reasoning workloads should confirm effort settings rather than assuming maximum inference depth. Separately, on BrowseComp — an agentic web search benchmark measuring multi-step information retrieval — Opus 4.7 underperforms Opus 4.6, the one documented benchmark regression against its predecessor.

## Alignment Properties

Anthropic's safety evaluation rates Opus 4.7 as "largely well-aligned and trustworthy, though not fully ideal." The model shows low rates of deception, [[sycophancy]], and misuse cooperation, and improved [[prompt-injection]] resistance compared to Opus 4.6. One area of modest regression is harm-reduction for controlled substances. Anthropic's cybersecurity safeguards developed under Project Glasswing are incorporated into Opus 4.7, including a Cyber Verification Program for security researchers whose legitimate work would otherwise be affected by those safeguards.

Claude Mythos Preview remains the top-aligned model in Anthropic's portfolio; Opus 4.7 is positioned as the production-scale model for general deployment.

## Key Claims

| Claim                                                                                                                                                                                                                                                                                                     | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| Claude Opus 4.7 achieves 70% on CursorBench (up from 58% for Opus 4.6) and resolves 3× more production tasks than Opus 4.6 on Rakuten's SWE-Bench, representing a substantial advance in real-world software engineering performance.                                                                     | [[2026-anthropic-claude-opus-4-7-announcement]] | 2026-04-16 | current | 2 | false |
| Opus 4.7 extends image support to 2,576px on the long edge (~3.75 megapixels), more than triple prior Claude image resolution, and achieves 98.5% on XBOW's visual-acuity benchmark compared to 54.5% for Opus 4.6.                                                                                       | [[2026-anthropic-claude-opus-4-7-announcement]] | 2026-04-16 | current | 2 | false |
| Opus 4.7 pricing is unchanged at \$5/\$25 per million input/output tokens, but a tokenizer update increases effective token consumption by 1.0–1.35× depending on content type, requiring operators to re-evaluate prompt costs before assuming cost parity with Opus 4.6.                                | [[2026-anthropic-claude-opus-4-7-announcement]] | 2026-04-16 | current | 2 | false |
| Anthropic's alignment assessment characterizes Opus 4.7 as "largely well-aligned, with a profile similar to Opus 4.6," documenting significant improvements over Opus/Sonnet 4.6 in agentic safety for Claude Code and GUI settings, large reductions in important omissions and hallucination rates, and lower reward hacking on GUI computer-use tasks — while a white-box finding shows suppressing internal evaluation-awareness representations produces greater increases in deceptive behavior in Opus 4.7 than prior models, though absolute rates remain low. | [[2026-anthropic-claude-opus-4-7-announcement]], [[2026-claude-opus-4-7-system-card]] | 2026-04-16 | current | 4 | false |
| Opus 4.7 introduces task budgets (public beta) and an xhigh effort control level, enabling operators to cap computational spend per agentic task and access maximum reasoning depth without custom infrastructure.                                                                                        | [[2026-anthropic-claude-opus-4-7-announcement]] | 2026-04-16 | current | 2 | false |
| In a June 2026 experiment (Project Fetch Phase 2), Claude Opus 4.7 in Claude Code autonomously completed robotics programming and sensor integration tasks 37x faster than a human team without AI and 18x faster than a human team using Claude, producing 1,045 lines of effective code versus the Claude-assisted team's 10,309 — while failing at closed-loop physical control tasks (autonomous beach ball retrieval) that practiced humans could perform, establishing autonomous AI capability for structured device programming tasks but not yet for real-time perception-feedback-control loops. | [[2026-anthropic-project-fetch-phase-two]] | 2026-06-18 | current | 2 | false |

## Data Records

| Metric | Value | Conditions | Measurement Date | Source | Status |
|---|---|---|---|---|---|
| SWE-bench Verified | 87.6% | Adaptive thinking, max effort; 5-trial average | 2026-04 | [[2026-claude-opus-4-7-system-card]] | current |
| SWE-bench Pro | 64.3% | Adaptive thinking, max effort; 5-trial average | 2026-04 | [[2026-claude-opus-4-7-system-card]] | current |
| SWE-bench Multilingual | 80.5% | Adaptive thinking, max effort; 5-trial average; 9 programming languages | 2026-04 | [[2026-claude-opus-4-7-system-card]] | current |
| Terminal-Bench 2.0 | 69.4% | Thinking disabled; Harbor scaffold, Terminus-2 harness; 5-trial mean reward over 89 tasks | 2026-04 | [[2026-claude-opus-4-7-system-card]] | current |
| GPQA Diamond | 94.2% | Adaptive thinking, max effort; 10-trial average; 198-question Diamond subset | 2026-04 | [[2026-claude-opus-4-7-system-card]] | current |
| ARC-AGI-2 | 75.83% | Adaptive thinking, max effort; 5-trial average | 2026-04 | [[2026-claude-opus-4-7-system-card]] | current |
| OSWorld | 78.0% | Adaptive thinking, max effort; 5-trial average | 2026-04 | [[2026-claude-opus-4-7-system-card]] | current |
| OfficeQA Pro | 80.6% | Adaptive thinking, max effort; 5-trial average | 2026-04 | [[2026-claude-opus-4-7-system-card]] | current |
| Humanity's Last Exam (no tools) | 46.9% | Max reasoning effort; 1M token cap; no web access | 2026-04 | [[2026-claude-opus-4-7-system-card]] | current |
| Humanity's Last Exam (with tools) | 54.7% | Max reasoning effort; 1M token cap; web search + code execution | 2026-04 | [[2026-claude-opus-4-7-system-card]] | current |
| BrowseComp | 79.3% | Adaptive thinking, max effort | 2026-04 | [[2026-claude-opus-4-7-system-card]] | current |
| API input price | \$5.00 per 1M tokens | Standard API list price, unchanged from Opus 4.6 | 2026-04 | [[2026-disappearing-ai-middle-class]] | current |
| API output price | \$25.00 per 1M tokens | Standard API list price, unchanged from Opus 4.6 | 2026-04 | [[2026-disappearing-ai-middle-class]] | current |
| Project Fetch Phase 2 — task time (4 tasks) | 9 min 35 sec | Claude Code; autonomous; adaptive thinking, max effort; 3-trial average; robotics setup and sensor integration tasks | 2026-06 | [[2026-anthropic-project-fetch-phase-two]] | current |
| Project Fetch Phase 2 — code volume | 1,045 lines | Autonomous; vs Team Claude 10,309 lines, Team Claude-less 1,136 lines; comparable or better task success | 2026-06 | [[2026-anthropic-project-fetch-phase-two]] | current |

## Physical Agentic Capability

In June 2026, Anthropic published Project Fetch Phase 2, a controlled experiment testing whether Opus 4.7 could autonomously complete robotics tasks that Anthropic employees completed with and without Claude in August 2024. Opus 4.7 operating in Claude Code completed all four tasks that both human teams completed, averaging 9 minutes 35 seconds versus 181 minutes for the Claude-assisted team and 361 minutes for the team without AI — a 18x and 37x speedup respectively. The model produced 1,045 lines of code compared to 10,309 for the Claude-assisted team, with much of the code effective on the first attempt.

The model failed at closed-loop physical control: autonomously navigating the robot to retrieve a beach ball required perceiving ball position, computing an error signal, and adjusting motor commands in real time — a feedback loop that practiced humans could accomplish manually but that Opus 4.7 could not reliably complete. Anthropic's researchers note that these robotics improvements emerged from general-purpose capability scaling rather than robotics-specific training, framing the result as the early era of physical agentic AI following the same trajectory as software agentic AI. The experiment ran Claude Mythos Preview in preliminary trials but excluded it from comparison because the experimental setup created an apples-to-apples problem with how the model was served.

## Teaching Notes

**Concept in plain terms.** Claude Opus 4.7 is Anthropic's production-scale flagship AI model as of April 2026, with major advances in software engineering, visual document processing, and long-horizon agentic task execution over its predecessor, available to consumers and enterprises at unchanged pricing — though a tokenizer change means actual costs are higher than the listed price implies.

**Why it matters for instruction.** Opus 4.7 illustrates recurring tensions in AI tool evaluation: capability improvements that arrive with new behavioral constraints (mandatory adaptive thinking), cost changes that complicate pricing comparisons, and alignment assessments that remain candid about gaps. It is a useful worked example for teaching practitioners to read model release announcements critically rather than accepting overall performance claims at face value.

**Common misconceptions.** Students often equate model recency with uniform superiority. Opus 4.7 underperforms Opus 4.6 on one documented benchmark (BrowseComp), and its mandatory adaptive thinking changes inference behavior in ways that require explicit operator adjustment for heavy reasoning workloads. Newer models are not uniformly better across all use cases or configurations.

**Suggested framing.** Use Opus 4.7 as a worked example in tool evaluation practice: walk through how to assess a new model release against specific use-case requirements — including limitations and behavioral changes, not just headline benchmarks — before deciding whether to upgrade.
