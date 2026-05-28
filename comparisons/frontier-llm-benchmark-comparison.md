---
type: comparison
title: Frontier LLM Benchmark Comparison
created: 2026-05-18
updated: 2026-05-28
comparison_type: tool-vs-tool
entities_compared:
  - "[[tools/anthropic-claude-opus-4-7]]"
  - "[[tools/openai-gpt-5-5]]"
  - "[[tools/openai-gpt-5-5-pro]]"
  - "[[tools/google-gemini-3-5-flash]]"
use_case: Selecting a frontier AI model for agentic coding, knowledge work, and scientific research as of May 2026
status: current
source_count: 5
related_topics:
  - "[[llm-fundamentals]]"
---
> **Source note:** Benchmark data for Claude Opus 4.7, GPT-5.5, and GPT-5.5 Pro is derived
> from the Vellum LLM Leaderboard (2026), a vendor-operated aggregator.
> *(vendor-aggregated — benchmark selection, model inclusion, and methodology reflect
> commercial context; treat rankings and scores with caution)*
>
> **Gemini 3.5 Flash data is sourced exclusively from Google's product blog post (vendor-reported).
> All Gemini 3.5 Flash figures are self-reported and independently unverified in this comparison's
> source set.**

Selecting among Claude Opus 4.7, GPT-5.5, GPT-5.5 Pro, and Gemini 3.5 Flash for agentic coding, knowledge work, and scientific research reveals a clear capability stratification with a cost-speed tradeoff at the frontier: Claude Opus 4.7 leads on production software engineering at the lowest output cost; GPT-5.5 leads on abstract reasoning with a 1M-token context window; GPT-5.5 Pro extends GPT-5.5 for frontier mathematics and multi-source web research at a 6x price premium; and Gemini 3.5 Flash occupies a distinct position as the lowest-latency, lowest-cost option with vendor-claimed agentic throughput — though all Gemini performance figures are self-reported.

| Benchmark / Dimension | Claude Opus 4.7 | GPT-5.5 | GPT-5.5 Pro | Gemini 3.5 Flash |
|---|---|---|---|---|
| Software engineering (SWE-Bench Pro) | 64.3% | 58.6% | — | — |
| Agentic coding | 70% CursorBench | 82.7% Terminal-Bench 2.0 | — | 76.2% Terminal-Bench 2.1 (vendor) |
| Abstract reasoning (ARC-AGI-2) | — | 85.0% | — | — |
| Frontier math (FrontierMath T4) | 22.9% | 35.4% | 39.6% | — |
| Web research (BrowseComp) | — | 84.4% | 90.1% | — |
| Interdisciplinary reasoning (HLE w/tools) | — | 52.2% | 57.2% | — |
| Scientific analysis (GeneBench) | — | — | 33.2% | — |
| Agentic evaluation (GDPval-AA) | — | — | — | 1656 Elo (vendor) |
| Multi-agent/MCP (MCP Atlas) | — | — | — | 83.6% (vendor) |
| API pricing (input/output per 1M tokens) | \$5/\$25 | \$5/\$30 | \$30/\$180 | — |
| Context window | — | 1M tokens | — | — |
| Safety assessment | "largely well-aligned, not fully ideal" (Anthropic) | "High" Preparedness Framework — cyber/bio (OpenAI) | — | "Frontier Safety Framework — improved cyber/CBRN" (Google, self-reported) |

All benchmark figures are vendor-reported unless noted in Evidence Notes.

## Verdict

Prefer [[anthropic-claude-opus-4-7]] when the primary task is production software engineering and output cost must stay at or below \$25 per 1M tokens. Prefer [[openai-gpt-5-5]] when the task requires state-of-the-art abstract reasoning (ARC-AGI-2), a 1M-token context window, or general knowledge work at GPT-5.5 pricing. Prefer [[openai-gpt-5-5-pro]] when the task involves frontier mathematics, multi-step multi-source web research, or scientific bioinformatics workflows and the \$180/1M output cost is acceptable. Prefer [[google-gemini-3-5-flash]] when the primary requirement is agentic task throughput at the lowest latency and cost in this comparison — vendor-claimed at 4x output speed and less than half the cost of comparable frontier models — and multi-agent coordination via MCP or Antigravity is within the deployment stack; note that all Gemini 3.5 Flash figures are vendor-reported and independently unverified.

## Evidence Notes

**Independent SWE-bench evaluation:** Vellum's LLM Leaderboard (April 2026) places Claude Opus 4.7 at 87.6% on SWE-bench — substantially above its vendor-reported SWE-Bench Pro figure of 64.3%. These are methodologically distinct evaluations; the Vellum figure should not be treated as a direct substitute for the SWE-Bench Pro figure in the table above. Source: [[2026-vellum-llm-leaderboard]].<br>
**Benchmark scope gaps:** OpenAI does not separately report GPT-5.5 Pro scores on ARC-AGI-2, Terminal-Bench 2.0, or Expert-SWE; the Pro variant's advantage appears concentrated in research-intensive and mathematics-heavy tasks. Claude Opus 4.7's ARC-AGI-2 score is not reported in available sources. Claude Opus 4.7 regresses from Opus 4.6 on BrowseComp (no absolute score reported).<br>
**Cross-model SWE-Bench Pro comparisons:** The Claude Opus 4.7 SWE-Bench Pro figure (64.3%) and the FrontierMath T4 Claude Opus 4.7 figure (22.9%) in the table above are drawn from OpenAI's release materials and should be evaluated as vendor-sourced comparative claims.<br>
**Gemini 3.5 Flash benchmark methodology:** All Gemini 3.5 Flash figures are drawn from Google's product blog announcement (vendor-reported) rather than the Vellum LLM Leaderboard used for the other three entities. Terminal-Bench 2.1 (Gemini, 76.2%) and Terminal-Bench 2.0 (GPT-5.5, 82.7%) are different benchmark versions and are not directly comparable; both appear in the "Agentic coding" row for contextual reference only. GDPval-AA and MCP Atlas scores have no equivalent figures available for the other models in this comparison's source set. Gemini 3.5 Flash pricing is vendor-stated as less than half the cost of comparable frontier models but specific per-token prices are not published in the available source.
