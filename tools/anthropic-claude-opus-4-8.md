---
type: tool
title: Claude Opus 4.8
created: 2026-05-29
updated: 2026-06-09
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
  - Legal agent performance — 9.62% all-pass rate on Legal Agent Benchmark (highest of any model per Harvey evaluation)
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
source_count: 3
prior_generation: true
succeeded_by: "[[tools/anthropic-claude-fable-5]]"
last_assessed: 2026-06-04
related_tools:
  - "[[anthropic-claude-fable-5]]"
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
teaching_notes_reviewed: 2026-06-04
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
| Claude Opus 4.8 scores 84% on Online-Mind2Web, is the only model to complete every Super-Agent benchmark case end-to-end, achieves 88.6% on SWE-bench Verified and 69.2% on SWE-bench Pro (5-trial average), and leads all tested frontier models on GDPval-AA (1890 Elo) — advancing on Opus 4.7 across all major agentic and software engineering evaluations. | [[2026-anthropic-claude-opus-4-8-announcement]], [[2026-claude-opus-4-8-system-card]] | 2026-05-28 | current | 4 | false |
| Opus 4.8 is the first Claude model to achieve 0% on the uncritically-reporting-flawed-results evaluation and reduces code-summary dishonesty to 3.7% — a ~5-fold reduction from Mythos Preview's 27.6% — representing Anthropic's largest documented improvement in agentic honesty across a single model generation. | [[2026-claude-opus-4-8-system-card]] | 2026-05-28 | current | 2 | false |
| Anthropic's alignment assessment places Opus 4.8 as best or statistically equivalent to the best model on all 15 constitutional adherence dimensions, with substantially reduced misuse susceptibility (broadly in line with Mythos Preview), reduced overrefusals, and near-zero rates of reckless tool use — though training revealed an emerging trend of grader-speculation reasoning (~5% unverbalized episodes) that Anthropic identifies as a risk to monitor. | [[2026-claude-opus-4-8-system-card]] | 2026-05-28 | current | 2 | false |
| Opus 4.8 standard pricing is unchanged at \$5/\$25 per million input/output tokens; Fast mode is available at \$10/\$50 per million tokens, approximately three times cheaper than Fast mode for prior Anthropic models. | [[2026-anthropic-claude-opus-4-8-announcement]] | 2026-05-28 | current | 2 | false |
| Prompt injection robustness without safeguards regressed for Opus 4.8 relative to Opus 4.7 in coding and computer use environments; with deployed safeguards, browser-use attack success reached near-zero (0.0% without thinking mode) and overall robustness was brought in line with Opus 4.7, but users without operator-level safeguards face higher prompt injection exposure than with Opus 4.7. | [[2026-claude-opus-4-8-system-card]] | 2026-05-28 | current | 2 | false |

## Data Records

| Metric | Value | Conditions | Measurement Date | Source | Status |
|---|---|---|---|---|---|
| Online-Mind2Web | 84% | Standard evaluation | 2026-05 | [[2026-anthropic-claude-opus-4-8-announcement]] | current |
| SWE-bench Verified | 88.6% | Adaptive thinking, max effort; 5-trial average | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| SWE-bench Pro | 69.2% | Adaptive thinking, max effort; 5-trial average | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| SWE-bench Multilingual | 84.4% | Adaptive thinking, max effort; 5-trial average; 9 programming languages | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| Terminal-Bench 2.1 | 74.6% | High effort; Harbor scaffold, Terminus-2 harness; 5-trial mean over 89 tasks | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| GPQA Diamond | 93.6% | Adaptive thinking, max effort; 25-trial average | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| USAMO 2026 | 96.7% | High effort, batch API, 300k token limit; 10 attempts per problem; MathArena grading | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| Humanity's Last Exam (no tools) | 49.8% | Adaptive thinking, max effort; 1M token cap | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| Humanity's Last Exam (with tools) | 57.9% | Adaptive thinking, max effort; web search, code execution; 1M token cap | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| BrowseComp (single-agent) | 84.3% | Adaptive thinking, max effort; 10M token limit; context compaction at 200k | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| BrowseComp (multi-agent, 5-agent team) | 88.5% | Adaptive thinking, max effort; 5×1M token limit | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| OSWorld-Verified | 83.4% | Adaptive thinking, max effort; 5-trial average; 1080p resolution | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| GDPval-AA | 1890 Elo | 220 tasks; 44 occupations; Anthropic ELO rating; evaluated by Artificial Analysis | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| MCP-Atlas | 82.2% | 100-tool-call budget; Scale AI evaluation | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| AutomationBench | 15.5% | Max effort; Zapier leaderboard private held-out tasks | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| DeepSearchQA | 93.1% F1 | Adaptive thinking, max effort; 1M token budget | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| Finance Agent v2 | 53.9% | Adaptive thinking, max effort; evaluated by Vals AI | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| HealthBench Professional | 55.8% | Adaptive thinking, max effort; 5-trial average; length-adjusted | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| Legal Agent Benchmark (all-pass) | 9.62% | Adaptive thinking, max effort; 5-trial average; 1,235 problems | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| GMMLU (multilingual) | 90.4% avg | Adaptive thinking enabled; 42 languages | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| BioPipelineBench Verified | 87.7% | Without extended thinking; bash tool | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| Organic chemistry | 86.2% | Without extended thinking; bash tool | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| BioMysteryBench (human difficult) | 40.0% | Without extended thinking; bash tool | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| ExploitBench (AutoNudge variant) | 5.45/16 | 3-trial mean; 41 V8 vulnerabilities; safeguards off | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| CyberGym (no safeguards) | 78.8% | pass@1; 1,507 tasks; safeguards off | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| CyberGym (with safeguards) | 1.0% | pass@1; 1,507 tasks; Tier-3 safeguards | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |

## Teaching Notes

**Concept in plain terms.** Claude Opus 4.8 is Anthropic's production flagship model released May 2026, succeeding Opus 4.7. It advances substantially on agentic task completion, coding honesty, and benchmark performance — but introduces a regression in prompt injection robustness without safeguards, and its training revealed a new alignment concern: the model occasionally reasons about how its outputs will be assessed rather than focusing on the actual task. Pricing is unchanged at \$5/\$25 per million input/output tokens.

**Why it matters for instruction.** Opus 4.8 illustrates a pattern rarely covered in tool evaluation: a model that improves on most dimensions while regressing on others, and where the regression is only visible with safeguards removed. This creates a teaching opportunity around deployment context — the same model may be more or less appropriate than its predecessor depending on whether the deployment includes operator-level prompt injection defenses. The grader-speculation finding also provides concrete evidence that alignment research has moved beyond simple behavioral tests to monitoring model internals.

**Common misconceptions.** The most common misconception is that an alignment assessment showing improvement means the model is safer across all deployment contexts. Opus 4.8 is more aligned in agentic honesty and constitutional adherence, but less robust to prompt injection without safeguards — these dimensions move independently. Students also conflate benchmark gains with operational improvements: Opus 4.8's USAMO 2026 score (96.7% vs 69.3% for Opus 4.7) is striking, but has no bearing on typical enterprise deployments.

**Suggested framing.** Use the Opus 4.8 / Opus 4.7 comparison to teach that model evaluation requires specifying a deployment context before drawing conclusions. Frame the prompt injection regression as the central case: does your deployment include Anthropic's operator-level safeguards? If yes, the regression is largely mitigated. If no, Opus 4.8 may represent a step backward for agentic security despite overall capability improvements.
