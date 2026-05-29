---
type: tool
title: Claude Opus 4.8
created: 2026-05-29
updated: 2026-05-29
summary: Anthropic's production flagship model as of May 2026, advancing on Opus 4.7 with stronger agentic task performance, substantially improved alignment, and dynamic multi-agent workflows in Claude Code — at unchanged standard pricing.
status: active
vendor: Anthropic
pricing_model: usage-based
access_tier:
  - consumer
  - api
  - enterprise
capabilities:
  - Agentic task execution — 84% on Online-Mind2Web; only model to complete every Super-Agent benchmark case end-to-end
  - Legal agent performance — first model to break 10% on Legal Agent Benchmark all-pass standard
  - Code quality — ~4× less likely to allow code flaws than Opus 4.7; fixes comment-verbosity and tool-calling issues
  - CursorBench — exceeds all prior Opus models at every effort level
  - Dynamic workflows (Claude Code research preview) — hundreds of parallel subagents per session
  - Effort control: high (default), xhigh, and max levels
  - Mid-task instruction updates via system entries inside the Messages API messages array
limitations:
  - Fast mode doubles per-token pricing relative to standard (\$10/\$50 per million input/output tokens)
  - Dynamic workflows available only in Claude Code research preview; not generally available
primary_use_cases:
  - Agentic web navigation and multi-step task automation
  - Code review, generation, and long-horizon coding agents
  - Legal and financial document analysis
  - Multi-agent orchestration via Claude Code
source_count: 1
last_assessed: 2026-05-29
related_tools:
  - "[[anthropic-claude-opus-4-7]]"
  - "[[anthropic-claude-mythos-preview]]"
related_topics:
  - "[[ai-agentic-workflows]]"
  - "[[prompt-injection]]"
teaching_relevance: true
competency_domains:
  - capability-horizon-awareness
  - tool-evaluation-and-selection
professional_contexts:
  - software-and-ai-development
  - project-and-program-management
  - professional-and-continuing-education
technical_depth: practitioner
teaching_notes_reviewed: 2026-05-29
---

Claude Opus 4.8 is Anthropic's production flagship model released May 28, 2026, succeeding Claude Opus 4.7. It is available through claude.ai, the Anthropic API, Amazon Bedrock, Google Cloud Vertex AI, and Claude Code for Enterprise, Team, and Max plan users. Standard pricing is unchanged at \$5/\$25 per million input/output tokens. A new Fast mode operates at \$10/\$50 per million tokens — approximately three times cheaper than Fast mode for prior Anthropic models — for deployments where lower-latency response matters more than per-token cost.

## Agentic Task Performance

Opus 4.8's most substantial advances are in agentic task benchmarks. The model scores 84% on Online-Mind2Web, a benchmark measuring real-world web navigation and multi-step task completion in live browser environments. It is the only model to complete every case end-to-end on the Super-Agent benchmark. On the Legal Agent Benchmark, Opus 4.8 is the first model to break 10% on the all-pass standard, which requires completing every step of a complex multi-stage legal task without any single step failing. On CursorBench, Opus 4.8 exceeds prior Opus models at every effort level.

These results represent meaningful advances over Opus 4.7, which showed limitations on agentic web navigation and multi-step task completion in operational evaluations. For deployments involving automated research, browser-based workflows, or multi-step document analysis pipelines, Opus 4.8's agentic improvements warrant evaluation against the specific task type before assuming upgrade benefit.

## Code Quality

Opus 4.8 is approximately four times less likely than Opus 4.7 to allow flaws in code, and fixes two specific issues documented in Opus 4.7: comment-verbosity (excessive or inaccurate inline comment generation) and tool-calling reliability. Both were identified as friction points in production coding agent deployments. The fixes make Opus 4.8 better suited for automated code review workflows and multi-step coding agents where correct tool use across a long pipeline is required.

## Dynamic Workflows and API Updates

Dynamic workflows in Claude Code (research preview) enable hundreds of parallel subagents within a single session. This is the first broadly available implementation of this multi-agent orchestration pattern for Claude users without custom infrastructure. The capability is most relevant for tasks that decompose into independent parallel units — large codebase analysis, concurrent document review, parallel research queries — where a sequential agent would be a throughput bottleneck.

A parallel API update allows system entries inside the messages array, enabling mid-task instruction updates. Prior Claude APIs fixed system context at session start, preventing updated instructions based on intermediate task results. This change removes that structural constraint for agentic deployments that need to adapt task instructions at runtime.

## Alignment Properties

Anthropic's alignment assessment rates Opus 4.8's misaligned behavior rates as substantially lower than Opus 4.7 and comparable to Claude Mythos Preview — Anthropic's highest-aligned model. The assessment documents new highs on prosocial traits, including supporting user autonomy and acting in users' best interests. This is a material improvement from Opus 4.7's rating of "largely well-aligned and trustworthy, though not fully ideal." The alignment improvement is particularly relevant for deployments where user autonomy support and honest representation of capabilities are explicit requirements.

Effort controls — high (default), xhigh, and max — provide explicit management of reasoning depth without the mandatory-adaptive-thinking constraint introduced in Opus 4.7.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| Claude Opus 4.8 scores 84% on Online-Mind2Web, is the only model to complete every Super-Agent benchmark case end-to-end, and is the first model to break 10% on the Legal Agent Benchmark all-pass standard — advancing on Opus 4.7 across all three major agentic task evaluations. | [[2026-anthropic-claude-opus-4-8-announcement]] | 2026-05-28 | current | 2 | false |
| Opus 4.8 is approximately four times less likely than Opus 4.7 to allow flaws in code and fixes the comment-verbosity and tool-calling issues present in Opus 4.7, making it better suited for automated code review and multi-step coding agents. | [[2026-anthropic-claude-opus-4-8-announcement]] | 2026-05-28 | current | 2 | false |
| Anthropic's alignment assessment rates Opus 4.8's misaligned behavior rates as substantially lower than Opus 4.7 and comparable to Claude Mythos Preview, with new highs on prosocial traits including supporting user autonomy and acting in users' best interests. | [[2026-anthropic-claude-opus-4-8-announcement]] | 2026-05-28 | current | 2 | false |
| Opus 4.8 standard pricing is unchanged at \$5/\$25 per million input/output tokens; Fast mode is available at \$10/\$50 per million tokens, approximately three times cheaper than Fast mode for prior Anthropic models. | [[2026-anthropic-claude-opus-4-8-announcement]] | 2026-05-28 | current | 2 | false |
| Dynamic workflows in Claude Code (research preview) enable hundreds of parallel subagents within a single session, making large-scale multi-agent orchestration available without custom infrastructure for the first time in Anthropic's product stack. | [[2026-anthropic-claude-opus-4-8-announcement]] | 2026-05-28 | current | 2 | false |

## Data Records

| Metric | Value | Conditions | Measurement Date | Source | Status |
|---|---|---|---|---|---|
| Online-Mind2Web | 84% | Standard evaluation | 2026-05 | [[2026-anthropic-claude-opus-4-8-announcement]] | current |

## Teaching Notes

**Concept in plain terms.** Claude Opus 4.8 is Anthropic's current production flagship model, released May 2026. It builds on Opus 4.7 with measurably better agentic task completion, higher code quality, and improved alignment — while maintaining the same standard pricing. A new Fast mode doubles the per-token cost in exchange for lower latency, introducing an explicit cost-latency tradeoff decision that practitioners need to evaluate for each deployment context.

**Why it matters for instruction.** Opus 4.8 is useful for teaching tool evaluation because it illustrates how capability advances, alignment improvements, and pricing structure changes can occur simultaneously in a single model release — and how each dimension requires separate evaluation against the practitioner's specific use case. The alignment improvement from "largely not fully ideal" to near-Mythos-Preview levels is also a useful data point for teaching how Anthropic's internal alignment assessments work and what they measure.

**Common misconceptions.** Students often treat benchmark improvements as directly transferable to any use case. Opus 4.8's agentic gains — in web navigation and legal agent tasks — are meaningful only if the deployment involves those specific task types. For general knowledge work or document summarization, the difference between Opus 4.7 and 4.8 may not be operationally significant. Fast mode's 2× price premium is also frequently misread as a premium tier; it is a latency-cost tradeoff, not a capability upgrade.

**Suggested framing.** Use Opus 4.8 alongside Opus 4.7 as a before/after case study in incremental model evaluation: given a specific deployment context (coding agent, legal research tool, general writing assistant), does this particular upgrade matter — and how would you determine that before paying for it?
