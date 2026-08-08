---
type: comparison
title: Frontier LLM Benchmark Comparison
created: 2026-05-18
updated: 2026-08-08
comparison_type: tool-vs-tool
entities_compared:
  - "[[tools/anthropic-claude-opus-5]]"
  - "[[tools/openai-gpt-5-5]]"
  - "[[tools/openai-gpt-5-5-pro]]"
  - "[[tools/google-gemini-3-5-flash]]"
use_case: Selecting a frontier AI model for agentic coding, knowledge work, and scientific research as of July 2026
status: current
source_count: 8
related_topics:
  - "[[llm-fundamentals]]"
---
> **Source note:** Benchmark data for Claude Opus 5 is drawn from the Anthropic system card (July 2026). Benchmark data for GPT-5.5 and GPT-5.5 Pro is derived from the Vellum LLM Leaderboard (2026), a vendor-operated aggregator, and is now a generation behind Claude's July 2026 comparison cohort.
> *(vendor-aggregated — benchmark selection, model inclusion, and methodology reflect
> commercial context; treat rankings and scores with caution)*
>
> **Gemini 3.5 Flash data is sourced exclusively from Google's product blog post (vendor-reported).
> All Gemini 3.5 Flash figures are self-reported and independently unverified in this comparison's
> source set.**

Selecting among Claude Opus 5, GPT-5.5, GPT-5.5 Pro, and Gemini 3.5 Flash for agentic coding, knowledge work, and scientific research as of July 2026 reveals a widened capability gap: Claude Opus 5 leads on production software engineering, professional task execution, web research, and abstract reasoning, having closed and reversed the ARC-AGI-2 gap that favored GPT-5.5 in the prior comparison cycle; GPT-5.5 retains its 1M-token context window as a distinguishing feature; GPT-5.5 Pro remains the only model in this set with a reported frontier-mathematics score (FrontierMath T4); and Gemini 3.5 Flash occupies a distinct position as the lowest-latency, lowest-cost option with vendor-claimed agentic throughput — though all Gemini performance figures are self-reported. GPT-5.5 and GPT-5.5 Pro figures are unchanged since the prior comparison and are now a full model generation behind Claude Opus 5's July 2026 release.

| Benchmark / Dimension | Claude Opus 5 | GPT-5.5 | GPT-5.5 Pro | Gemini 3.5 Flash |
|---|---|---|---|---|
| Software engineering (SWE-Bench Pro) | 79.2% | 58.6% | — | — |
| Agentic coding (Terminal-Bench 2.1 / FrontierBench v0.1) | 44.4% FrontierBench v0.1 (xhigh, mean reward) | 78.2% Terminal-Bench 2.0 | — | 76.2% Terminal-Bench 2.1 (vendor) |
| Abstract reasoning (ARC-AGI-2) | 90.4% | 85.0% | — | — |
| Frontier math (FrontierMath T4) | — | 35.4% | 39.6% | — |
| Web research (BrowseComp) | 90.8% | 84.4% | 90.1% | — |
| Professional task execution (GDPval-AA v2) | 1861 Elo (max effort) | 1769 Elo | — | — |
| Agentic evaluation (GDPval-AA) | — | — | — | 1656 Elo (vendor) |
| Multi-agent/MCP (MCP Atlas) | — | 75.3% | — | 83.6% (vendor) |
| Knowledge work (Humanity's Last Exam, with tools) | 64.7% | 52.2% | 57.2% | — |
| API pricing (input/output per 1M tokens) | not disclosed in system card | \$5/\$30 | \$30/\$180 | — |
| Context window | — | 1M tokens | — | — |
| Safety assessment | "very low" overall alignment risk, unchanged from Fable 5 (Anthropic system card) | "High" Preparedness Framework — cyber/bio (OpenAI) | — | "Frontier Safety Framework — improved cyber/CBRN" (Google, self-reported) |

All benchmark figures are vendor-reported unless noted in Evidence Notes.

## Verdict

Prefer [[anthropic-claude-opus-5]] when the primary task is production software engineering (SWE-Bench Pro 79.2% vs 58.6% for GPT-5.5), professional task execution across enterprise domains (GDPval-AA v2 1861 Elo vs 1769 for GPT-5.5), web research (BrowseComp 90.8% vs 90.1% for GPT-5.5 Pro), or abstract reasoning (ARC-AGI-2 90.4% vs 85.0% for GPT-5.5). Prefer [[openai-gpt-5-5]] when the task requires a 1M-token context window or general knowledge work at GPT-5.5 pricing, noting that GPT-5.5's disclosed benchmark figures are unchanged since May 2026 and no longer represent the current OpenAI frontier. Prefer [[openai-gpt-5-5-pro]] when the task involves frontier mathematics (FrontierMath T4 39.6%, the only reported score in this comparison) and the \$180/1M output cost is acceptable. Prefer [[google-gemini-3-5-flash]] when the primary requirement is agentic task throughput at the lowest latency and cost in this comparison — vendor-claimed at 4x output speed and less than half the cost of comparable frontier models — and multi-agent coordination via MCP or Antigravity is within the deployment stack; note that all Gemini 3.5 Flash figures are vendor-reported and independently unverified.

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
| SWE-bench Verified — Claude Opus 4.8 | 88.6% | Adaptive thinking, max effort; 5-trial average (prior generation baseline) | 2026-05 | [[2026-claude-opus-4-8-system-card]] | superseded |
| SWE-bench Pro — Claude Opus 4.8 | 69.2% | Adaptive thinking, max effort; 5-trial average (prior generation baseline) | 2026-05 | [[2026-claude-opus-4-8-system-card]] | superseded |
| Terminal-Bench 2.1 — Claude Opus 4.8 | 74.6% | High effort; Harbor scaffold, Terminus-2 harness; 5-trial mean over 89 tasks (prior generation; benchmark succeeded by FrontierBench v0.1) | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| GPQA Diamond — Claude Opus 4.8 | 93.6% | Adaptive thinking, max effort; 25-trial average (prior generation; not re-reported for Opus 5) | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| OSWorld-Verified — Claude Opus 4.8 | 83.4% | Adaptive thinking, max effort; 5-trial average; 1080p resolution (prior generation; benchmark succeeded by OSWorld 2.0) | 2026-05 | [[2026-claude-opus-4-8-system-card]] | current |
| BrowseComp (single-agent) — Claude Opus 4.8 | 84.3% | Adaptive thinking, max effort; 10M token limit; context compaction at 200k (prior generation baseline) | 2026-05 | [[2026-claude-opus-4-8-system-card]] | superseded |
| GDPval-AA — Claude Opus 4.8 | 1890 Elo | 220 tasks; Anthropic Elo rating; evaluated by Artificial Analysis (prior generation baseline) | 2026-05 | [[2026-claude-opus-4-8-system-card]] | superseded |
| HLE with tools — Claude Opus 4.8 | 57.9% | Adaptive thinking, max effort; web search + code execution; 1M token cap (prior generation baseline) | 2026-05 | [[2026-claude-opus-4-8-system-card]] | superseded |
| SWE-bench Verified — Claude Opus 5 | 96.0% | Adaptive thinking, max effort; 5-trial average | 2026-07 | [[2026-claude-opus-5-system-card]] | current |
| SWE-bench Pro — Claude Opus 5 | 79.2% | Adaptive thinking, max effort; 5-trial average | 2026-07 | [[2026-claude-opus-5-system-card]] | current |
| ARC-AGI-2 — Claude Opus 5 | 90.4% | — | 2026-07 | [[2026-claude-opus-5-system-card]] | current |
| BrowseComp — Claude Opus 5 | 90.8% | Adaptive thinking, max effort | 2026-07 | [[2026-claude-opus-5-system-card]] | current |
| GDPval-AA v2 — Claude Opus 5 | 1861 Elo (max effort) / 1827 Elo (xhigh) | 220 tasks, 44 occupations; independent eval by Artificial Analysis | 2026-07 | [[2026-claude-opus-5-system-card]] | current |
| HLE with tools — Claude Opus 5 | 64.7% | Adaptive thinking, max effort | 2026-07 | [[2026-claude-opus-5-system-card]] | current |
| FrontierBench v0.1 — Claude Opus 5 | 44.4% mean reward | xhigh effort; mini-SWE-agent harness; successor benchmark to Terminal-Bench 2.1; 74 tasks x 5 attempts | 2026-07 | [[2026-claude-opus-5-system-card]] | current |
| OSWorld 2.0 — Claude Opus 5 | 70.6% | Successor benchmark to OSWorld-Verified | 2026-07 | [[2026-claude-opus-5-system-card]] | current |
| AutomationBench — Claude Opus 5 | 26.0% | Max effort; Zapier private held-out eval set | 2026-07 | [[2026-claude-opus-5-system-card]] | current |

## Evidence Notes

**Claude Opus 5 system card benchmarks:** SWE-bench Verified, SWE-bench Pro, ARC-AGI-2, BrowseComp, GDPval-AA v2, HLE with tools, FrontierBench v0.1, OSWorld 2.0, and AutomationBench figures are from the Anthropic Claude Opus 5 System Card (July 2026). These supersede the prior Opus 4.8 baseline rows for the same metrics; GPQA Diamond, Terminal-Bench 2.1, and OSWorld-Verified are not re-reported for Opus 5 and remain current as the most recent disclosed figures for those specific benchmark versions.<br>
**Benchmark retirements:** Anthropic retired Terminal-Bench 2.1 for this release in favor of FrontierBench v0.1, developed by the same team with a larger emphasis on science and engineering tasks; the two are not directly comparable and appear on separate Data Records rows. OSWorld-Verified is similarly succeeded by OSWorld 2.0 in this system card.<br>
**GDPval-AA v2 methodology change:** Artificial Analysis's GDPval-AA v2 evaluation used for Opus 5 (1861 Elo at max effort) is reported as "v2" against the prior comparison's unversioned GDPval-AA figure for Opus 4.8 (1890 Elo); both are independently evaluated by Artificial Analysis using blind pairwise comparison, but a version change in the underlying benchmark means the two scores are not a strict apples-to-apples trend and the small decline should not be read as a capability regression.<br>
**GPT-5.5 / GPT-5.5 Pro / Gemini 3.5 Flash currency:** No new system card or benchmark disclosure for these three entities was ingested in this pass; their figures are unchanged from the May 2026 comparison and are now a full model generation behind Claude Opus 5's July 2026 release. This comparison's "current" status reflects the currency of the Claude figures only — a refresh incorporating GPT-5.6 and any newer Gemini release is recommended before this page is used for a cross-vendor purchasing decision.<br>
**Benchmark scope gaps:** OpenAI does not separately report GPT-5.5 Pro scores on several benchmarks; the Pro variant's advantage appears concentrated in research-intensive and mathematics-heavy tasks. FrontierMath T4 and MCP Atlas scores are not available for Claude Opus 5 in the ingested source; API pricing was not disclosed in the Opus 5 system card.<br>
**Terminal-Bench versioning:** Terminal-Bench 2.1 (Opus 4.8, 74.6%), FrontierBench v0.1 (Opus 5, 44.4%), and Terminal-Bench 2.0 (GPT-5.5, 78.2%) are three different benchmark versions and are not directly comparable; all appear in the "Agentic coding" row for contextual reference only.<br>
**Gemini 3.5 Flash benchmark methodology:** All Gemini 3.5 Flash figures are drawn from Google's product blog announcement (vendor-reported) rather than system card or independent evaluation. GDPval-AA (Gemini 3.5 Flash: 1656 Elo) uses a vendor-self-reported figure on the original, unversioned GDPval-AA benchmark. Gemini 3.5 Flash pricing is vendor-stated as less than half the cost of comparable frontier models but specific per-token prices are not published in the available source.
