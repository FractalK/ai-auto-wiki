---
type: tool
title: GPT-5.5 Pro
created: 2026-04-30
updated: 2026-04-30
summary: OpenAI's highest-capability variant of GPT-5.5, differentiated by stronger performance on web research, frontier mathematics, and scientific benchmarks at substantially higher pricing, available to Pro, Business, and Enterprise users.
status: active
vendor: OpenAI
pricing_model: usage-based
access_tier:
  - prosumer
  - api
  - enterprise
capabilities:
  - BrowseComp at 90.1% (highest in reported evaluation, vendor-reported)
  - FrontierMath Tier 4 at 39.6%, Tier 1-3 at 52.4% (vendor-reported)
  - GeneBench at 33.2% (highest in reported evaluation, vendor-reported)
  - Humanity's Last Exam at 57.2% with tools (vendor-reported)
  - GPQA Diamond at 93.6% (vendor-reported)
limitations:
  - Priced at \$30 per 1M input tokens and \$180 per 1M output tokens (6x GPT-5.5 standard input and output pricing)
  - Available only to Pro, Business, and Enterprise ChatGPT users; not available on Plus or consumer tiers
primary_use_cases:
  - Advanced research and frontier mathematics
  - Complex multi-source web research and information synthesis
  - Scientific data analysis requiring highest accuracy
source_count: 1
last_assessed: 2026-04-30
related_tools:
  - "[[openai-gpt-5-5]]"
  - "[[openai-chatgpt]]"
technical_depth: practitioner
---

GPT-5.5 Pro is OpenAI's highest-capability variant of GPT-5.5, differentiated from the base model by stronger performance on frontier mathematics, multi-source web research, and scientific benchmarks, at a substantially higher price point. It is available to Pro, Business, and Enterprise users in ChatGPT, and through the OpenAI API. The base model [[openai-gpt-5-5]] is available more broadly including Plus and consumer tiers.

All benchmark comparisons below are from OpenAI's own release materials and should be evaluated as vendor-sourced claims.

## Differentiated Capabilities

GPT-5.5 Pro achieves 90.1% on BrowseComp — the highest result in OpenAI's reported evaluation table, ahead of GPT-5.4 Pro (89.3%), GPT-5.5 (84.4%), and Gemini 3.1 Pro (85.9%). On FrontierMath Tier 4 (the most difficult tier of advanced mathematics problems), it scores 39.6% compared to GPT-5.5's 35.4% and Claude Opus 4.7's 22.9%. On Humanity's Last Exam with tools, it achieves 57.2%, above GPT-5.5's 52.2%. On GeneBench (multi-stage genetic data analysis), it achieves 33.2%, the highest result reported for any model in OpenAI's evaluation. *(vendor-sourced — treat comparative claims with caution)*

The differentiation between GPT-5.5 and GPT-5.5 Pro is most pronounced on benchmarks requiring extended search, synthesis across multiple sources, or frontier mathematical reasoning. On benchmarks favoring raw reasoning speed or general coding (such as ARC-AGI-2, Terminal-Bench 2.0, and Expert-SWE), OpenAI does not report separate GPT-5.5 Pro scores, suggesting the Pro variant's advantage is concentrated in research-intensive and mathematics-heavy tasks.

## Pricing

GPT-5.5 Pro is priced at \$30 per 1M input tokens and \$180 per 1M output tokens in the API — 6x the input cost and 6x the output cost of standard GPT-5.5 (\$5/\$30). Batch processing is available at half the standard rate.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| GPT-5.5 Pro achieves 90.1% on BrowseComp, the highest result in OpenAI's reported evaluation, ahead of GPT-5.4 Pro (89.3%), Gemini 3.1 Pro (85.9%), and GPT-5.5 (84.4%), per OpenAI's April 2026 evaluation. *(vendor-sourced — treat comparative claims with caution)* | [[2026-openai-gpt-5-5-announcement]] | 2026-04-28 | current | 1 | false |
| GPT-5.5 Pro is priced at \$30 per 1M input tokens and \$180 per 1M output tokens in the API, 6x the input and 6x the output cost of standard GPT-5.5; batch processing is available at half the standard rate. | [[2026-openai-gpt-5-5-announcement]] | 2026-04-28 | current | 1 | false |
| GPT-5.5 Pro achieves 39.6% on FrontierMath Tier 4 and 52.4% on Tier 1–3, exceeding GPT-5.5 (35.4%, 51.7%), Claude Opus 4.7 (22.9%, 43.8%), and Gemini 3.1 Pro (16.7%, 36.9%) on this benchmark per OpenAI's evaluation. *(vendor-sourced — treat comparative claims with caution)* | [[2026-openai-gpt-5-5-announcement]] | 2026-04-28 | current | 1 | false |
| GPT-5.5 Pro achieves 57.2% on Humanity's Last Exam (with tools) and 33.2% on GeneBench, the highest results for these benchmarks in OpenAI's reported evaluation table, per OpenAI's April 2026 evaluation. *(vendor-sourced — treat comparative claims with caution)* | [[2026-openai-gpt-5-5-announcement]] | 2026-04-28 | current | 1 | false |
