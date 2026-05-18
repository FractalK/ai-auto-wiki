---
type: comparison
title: Frontier LLM Benchmark Comparison
created: 2026-05-18
updated: 2026-05-18
comparison_type: tool-vs-tool
entities_compared:
  - "[[tools/anthropic-claude-opus-4-7]]"
  - "[[tools/openai-gpt-5-5]]"
  - "[[tools/openai-gpt-5-5-pro]]"
use_case: Selecting a frontier AI model for agentic coding, knowledge work, and scientific research as of April–May 2026
status: current
source_count: 4
related_topics:
  - "[[llm-fundamentals]]"
teaching_relevance: true
competency_domains:
  - tool-evaluation-and-selection
  - capability-horizon-awareness
professional_contexts:
  - teaching-and-instruction
  - professional-and-continuing-education
  - software-and-ai-development
---

Selecting among Claude Opus 4.7, GPT-5.5, and GPT-5.5 Pro for agentic coding, knowledge work, and scientific research reveals a clear capability stratification: Claude Opus 4.7 leads on production software engineering at the lowest output cost; GPT-5.5 leads on abstract reasoning and matches Claude's input pricing; and GPT-5.5 Pro extends GPT-5.5 for frontier mathematics and multi-source web research at a 6x price premium.

| Benchmark / Dimension | Claude Opus 4.7 | GPT-5.5 | GPT-5.5 Pro |
|---|---|---|---|
| Software engineering (SWE-Bench Pro) | 64.3% | 58.6% | — |
| Agentic coding | 70% CursorBench | 82.7% Terminal-Bench 2.0 | — |
| Abstract reasoning (ARC-AGI-2) | — | 85.0% | — |
| Frontier math (FrontierMath T4) | 22.9% | 35.4% | 39.6% |
| Web research (BrowseComp) | — | 84.4% | 90.1% |
| Interdisciplinary reasoning (HLE w/tools) | — | 52.2% | 57.2% |
| Scientific analysis (GeneBench) | — | — | 33.2% |
| API pricing (input/output per 1M tokens) | \$5/\$25 | \$5/\$30 | \$30/\$180 |
| Context window | — | 1M tokens | — |
| Safety assessment | "largely well-aligned, not fully ideal" (Anthropic) | "High" Preparedness Framework — cyber/bio (OpenAI) | — |

All benchmark figures are vendor-reported unless noted in Evidence Notes.

## Verdict

Prefer [[anthropic-claude-opus-4-7]] when the primary task is production software engineering and output cost must stay at or below \$25 per 1M tokens. Prefer [[openai-gpt-5-5]] when the task requires state-of-the-art abstract reasoning (ARC-AGI-2), a 1M-token context window, or general knowledge work at GPT-5.5 pricing. Prefer [[openai-gpt-5-5-pro]] when the task involves frontier mathematics, multi-step multi-source web research, or scientific bioinformatics workflows and the \$180/1M output cost is acceptable.

## Evidence Notes

**Independent SWE-bench evaluation:** Vellum's LLM Leaderboard (April 2026) places Claude Opus 4.7 at 87.6% on SWE-bench — substantially above its vendor-reported SWE-Bench Pro figure of 64.3%. These are methodologically distinct evaluations; the Vellum figure should not be treated as a direct substitute for the SWE-Bench Pro figure in the table above. Source: [[2026-vellum-llm-leaderboard]].<br>
**Benchmark scope gaps:** OpenAI does not separately report GPT-5.5 Pro scores on ARC-AGI-2, Terminal-Bench 2.0, or Expert-SWE; the Pro variant's advantage appears concentrated in research-intensive and mathematics-heavy tasks. Claude Opus 4.7's ARC-AGI-2 score is not reported in available sources. Claude Opus 4.7 regresses from Opus 4.6 on BrowseComp (no absolute score reported).<br>
**Cross-model SWE-Bench Pro comparisons:** The Claude Opus 4.7 SWE-Bench Pro figure (64.3%) and the FrontierMath T4 Claude Opus 4.7 figure (22.9%) in the table above are drawn from OpenAI's release materials and should be evaluated as vendor-sourced comparative claims.
