---
type: comparison
title: Frontier LLM Benchmark Comparison
created: 2026-05-18
updated: 2026-06-04
comparison_type: tool-vs-tool
entities_compared:
  - "[[tools/anthropic-claude-opus-4-8]]"
  - "[[tools/openai-gpt-5-5]]"
  - "[[tools/openai-gpt-5-5-pro]]"
  - "[[tools/google-gemini-3-5-flash]]"
use_case: Selecting a frontier AI model for agentic coding, knowledge work, and scientific research as of May 2026
status: current
source_count: 7
related_topics:
  - "[[llm-fundamentals]]"
---
> **Source note:** Benchmark data for Claude Opus 4.8 is drawn from the Anthropic system card (May 2026). Benchmark data for GPT-5.5 and GPT-5.5 Pro is derived from the Vellum LLM Leaderboard (2026), a vendor-operated aggregator.
> *(vendor-aggregated — benchmark selection, model inclusion, and methodology reflect
> commercial context; treat rankings and scores with caution)*
>
> **Gemini 3.5 Flash data is sourced exclusively from Google's product blog post (vendor-reported).
> All Gemini 3.5 Flash figures are self-reported and independently unverified in this comparison's
> source set.**

Selecting among Claude Opus 4.8, GPT-5.5, GPT-5.5 Pro, and Gemini 3.5 Flash for agentic coding, knowledge work, and scientific research as of May 2026 reveals a clear capability stratification: Claude Opus 4.8 leads on production software engineering, professional task execution, and scientific benchmarks with the lowest output cost at this tier; GPT-5.5 leads on abstract reasoning with a 1M-token context window; GPT-5.5 Pro extends GPT-5.5 for frontier mathematics and multi-source web research at a 6x price premium; and Gemini 3.5 Flash occupies a distinct position as the lowest-latency, lowest-cost option with vendor-claimed agentic throughput — though all Gemini performance figures are self-reported.

| Benchmark / Dimension | Claude Opus 4.8 | GPT-5.5 | GPT-5.5 Pro | Gemini 3.5 Flash |
|---|---|---|---|---|
| Software engineering (SWE-Bench Pro) | 69.2% | 58.6% | — | — |
| Agentic coding (Terminal-Bench 2.1) | 74.6% | 78.2% Terminal-Bench 2.0 | — | 76.2% Terminal-Bench 2.1 (vendor) |
| Abstract reasoning (ARC-AGI-2) | — | 85.0% | — | — |
| Frontier math (FrontierMath T4) | — | 35.4% | 39.6% | — |
| Web research (BrowseComp) | 84.3% (single-agent) | 84.4% | 90.1% | — |
| Professional task execution (GDPval-AA) | 1890 Elo | 1769 Elo | — | — |
| Agentic evaluation (GDPval-AA) | — | — | — | 1656 Elo (vendor) |
| Multi-agent/MCP (MCP Atlas) | 82.2% | 75.3% | — | 83.6% (vendor) |
| Knowledge work (Humanity's Last Exam, with tools) | 57.9% | 52.2% | 57.2% | — |
| API pricing (input/output per 1M tokens) | \$5/\$25 | \$5/\$30 | \$30/\$180 | — |
| Context window | — | 1M tokens | — | — |
| Safety assessment | "broadly unconcerning alignment" (Anthropic system card) | "High" Preparedness Framework — cyber/bio (OpenAI) | — | "Frontier Safety Framework — improved cyber/CBRN" (Google, self-reported) |

All benchmark figures are vendor-reported unless noted in Evidence Notes.

## Verdict

Prefer [[anthropic-claude-opus-4-8]] when the primary task is production software engineering (SWE-Bench Pro 69.2% vs 58.6% for GPT-5.5), professional task execution across enterprise domains (GDPval-AA 1890 Elo vs 1769 for GPT-5.5), or scientific research tasks requiring strong life sciences capability — at the lowest output cost of any model in this comparison at \$25 per 1M output tokens. Prefer [[openai-gpt-5-5]] when the task requires state-of-the-art abstract reasoning (ARC-AGI-2 85.0%), a 1M-token context window, or general knowledge work at GPT-5.5 pricing. Prefer [[openai-gpt-5-5-pro]] when the task involves frontier mathematics, multi-step multi-source web research, or scientific bioinformatics workflows and the \$180/1M output cost is acceptable. Prefer [[google-gemini-3-5-flash]] when the primary requirement is agentic task throughput at the lowest latency and cost in this comparison — vendor-claimed at 4x output speed and less than half the cost of comparable frontier models — and multi-agent coordination via MCP or Antigravity is within the deployment stack; note that all Gemini 3.5 Flash figures are vendor-reported and independently unverified.

## Data Records

| Metric | Value | Conditions | Measurement Date | Source | Status |
|---|---|---|---|---|---|
| SWE-bench Verified — Claude Opus 4.6 | 80.8% | Adaptive thinking, max effort; 25-trial average (prior generation baseline) | 2026-02 | [[2026-claude-opus-4-6-system-card]] | superseded |
| ARC-AGI-2 — Claude Opus 4.6 | 68.8% | High effort; prior generation baseline; SOTA at February 2026 release | 2026-02 | [[2026-claude-opus-4-6-system-card]] | superseded |
| GPQA Diamond — Claude Opus 4.6 | 91.3% | Adaptive thinking, max effort; 5-trial average; prior generation baseline | 2026-02 | [[2026-claude-opus-4-6-system-card]] | superseded |
| OSWorld-Verified — Claude Opus 4.6 | 72.7% | 5-run average; prior generation baseline | 2026-02 | [[2026-claude-opus-4-6-system-card]] | superseded |
| Terminal-Bench 2.0 — Claude Opus 4.6 | 65.4% | Adaptive thinking, max effort; 1,335 trials; prior generation baseline | 2026-02 | [[2026-claude-opus-4-6-system-card]] | superseded |
| SWE-bench Verified — Claude Opus 4.7 | 87.6% | Adaptive thinking, max effort; 5-trial average (prior generation baseline) | 2026-04 | [[2026-claude-opus-4-7-system-card]] | superseded |
| SWE-bench Pro — Claude Opus 4.7 | 64.3% | Adaptive thinking, max effort; 5-trial average (prior generation baseline) | 2026-04 | [[2026-claude-opus-4-7-system-card]] | superseded |
| Terminal-Bench 2.0 — Claude Opus 4.7 | 69.4% | Thinking disabled; Harbor scaffold, Terminus-2 harness; 5-trial mean over 89 tasks (prior generation) | 2026-04 | [[2026-claude-opus-4-7-system-card]] | superseded |
| GPQA Diamond — Claude Opus 4.7 | 94.2% | Adaptive thinking, max effort; 10-trial average (prior generation) | 2026-04 | [[2026-claude-opus-4-7-system-card]] | superseded |
| ARC-AGI-2 — Claude Opus 4.7 | 75.83% | Adaptive thinking, max effort; 5-trial average (prior generation) | 2026-04 | [[2026-claude-opus-4-7-system-card]] | superseded |
| OSWorld — Claude Opus 4.7 | 78.0% | Adaptive thinking, max effort; 5-trial average (prior generation) | 2026-04 | [[2026-claude-opus-4-7-system-card]] | superseded |
| SWE-bench Verified — Claude Opus 4.8 | 88.6% | Adaptive thinking, max effort; 5-trial average | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| SWE-bench Pro — Claude Opus 4.8 | 69.2% | Adaptive thinking, max effort; 5-trial average | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| Terminal-Bench 2.1 — Claude Opus 4.8 | 74.6% | High effort; Harbor scaffold, Terminus-2 harness; 5-trial mean over 89 tasks | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| GPQA Diamond — Claude Opus 4.8 | 93.6% | Adaptive thinking, max effort; 25-trial average | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| OSWorld-Verified — Claude Opus 4.8 | 83.4% | Adaptive thinking, max effort; 5-trial average; 1080p resolution | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| BrowseComp (single-agent) — Claude Opus 4.8 | 84.3% | Adaptive thinking, max effort; 10M token limit; context compaction at 200k | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| GDPval-AA — Claude Opus 4.8 | 1890 Elo | 220 tasks; Anthropic Elo rating; evaluated by Artificial Analysis | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| HLE with tools — Claude Opus 4.8 | 57.9% | Adaptive thinking, max effort; web search + code execution; 1M token cap | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |

## Evidence Notes

**Claude Opus 4.8 system card benchmarks:** SWE-bench Verified, SWE-bench Pro, Terminal-Bench 2.1, GPQA Diamond, OSWorld-Verified, BrowseComp, GDPval-AA, and HLE figures are from the Anthropic Claude Opus 4.8 System Card (May 2026). These supersede the prior Opus 4.7 baseline rows for the same metrics.<br>
**GDPval-AA cross-model comparison:** Artificial Analysis independently evaluated Opus 4.8 on GDPval-AA and reports a 121-Elo gap over GPT-5.5 (1890 vs 1769), implying a 66.7% pairwise win rate. This is the strongest cross-model professional task comparison available from an independent evaluator in this source set.<br>
**Benchmark scope gaps:** OpenAI does not separately report GPT-5.5 Pro scores on several benchmarks; the Pro variant's advantage appears concentrated in research-intensive and mathematics-heavy tasks. ARC-AGI-2 scores are not available for Opus 4.8 in published sources.<br>
**Terminal-Bench versioning:** Terminal-Bench 2.1 (Opus 4.8, 74.6%) and Terminal-Bench 2.0 (GPT-5.5, 78.2%) are different benchmark versions and are not directly comparable; both appear in the "Agentic coding" row for contextual reference only.<br>
**Gemini 3.5 Flash benchmark methodology:** All Gemini 3.5 Flash figures are drawn from Google's product blog announcement (vendor-reported) rather than system card or independent evaluation. GDPval-AA (Gemini 3.5 Flash: 1656 Elo) uses a vendor-self-reported figure; the Opus 4.8 GDPval-AA figure (1890) is from an independent evaluation by Artificial Analysis. Gemini 3.5 Flash pricing is vendor-stated as less than half the cost of comparable frontier models but specific per-token prices are not published in the available source.
