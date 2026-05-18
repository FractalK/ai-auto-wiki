---
type: topic
title: LLM Hallucination
created: 2026-05-03
updated: 2026-05-18
status: developing
summary: The tendency of large language models to generate plausible-sounding but factually incorrect or fabricated content — including nonexistent citations, invented entities, and confidently stated errors — as a structural consequence of next-token prediction without factual verification, with persistent and measurable epistemic reliability failures even in frontier models.
source_count: 1
last_assessed: 2026-05-18
related_topics:
  - "[[retrieval-augmented-generation]]"
  - "[[legal-ai-hallucination]]"
  - "[[llm-fundamentals]]"
  - "[[ai-search-citation-accuracy]]"
---

LLM hallucination — the generation of plausible-sounding but factually incorrect or fabricated content — is a structural property of next-token prediction systems. Language models generate statistically likely continuations of text, not verified factual statements. Hallucinated outputs are indistinguishable from accurate outputs at the surface level: they are fluent, specific, and confidently phrased, with no internal signal that the output is wrong. The practical implication is that every LLM output touching matters of fact requires independent verification before use in academic, professional, or consequential contexts.

Hallucination takes several overlapping forms: factual errors stated with confidence, citation of nonexistent sources (documented extensively in legal AI tools and academic AI search), invention of names, events, or statistics that were never recorded, and — a more specific and recently benchmarked variant — failure to distinguish between what is known and what is merely believed. The last form, called epistemic reliability, is particularly consequential in professional contexts.

## Epistemic Reliability

The KaBLE benchmark (Suzgun et al., 2025) evaluates whether AI models can distinguish knowledge from belief — a property termed epistemic reliability. The distinction matters in practice: a model supporting a medical diagnosis based on a patient's stated but mistaken belief, rather than established clinical fact, can reinforce an inaccurate treatment plan. A model summarizing legal testimony that cannot flag the difference between witness knowledge and witness belief creates misrepresentation risk.

Evaluated across 26 leading AI models using 13,000 questions spanning verification, confirmation, and recursive knowledge tasks, KaBLE documents hallucination rates ranging from 22% to 94% depending on model and task framing. The failure is not random: models handle third-person false beliefs considerably better than first-person ones. GPT-4o achieves 98.2% accuracy on true-belief verification tasks but drops to 64.4% when the same false statement is framed as something the user personally believes. DeepSeek R1 shows an even sharper decline, from over 90% to 14.4%. Newer models outperform older ones on first-person false-belief tasks (62.6% versus 52.5%), but none reliably distinguishes the epistemic status of first-person claims across all task types.

The benchmark results suggest that current models have not consistently learned the distinction between knowledge and belief — that while a belief can be held without it being true, knowledge requires truth. Recent models that perform well on recursive knowledge tasks may be relying on pattern matching rather than genuine epistemic understanding.

## Reporting Gap

Hallucination and factuality benchmarking is systematically underreported relative to capability benchmarking. The Stanford HAI AI Index 2026 documents that almost all frontier model developers report results on MMLU, SWE-bench, and coding evaluations, while reporting on responsible AI benchmarks — including factuality and hallucination evaluations — remains sparse. This creates a public record dense with capability claims but thin on reliability evidence. The practical consequence: organizational decisions about AI deployment are made against a backdrop of well-documented capability metrics and poorly documented factual reliability.

The share of organizations that consider inaccuracy a relevant AI risk rose from 60% to 74% between 2024 and 2025, and the share actively mitigating inaccuracy risks rose from 55% to 71% — suggesting that practitioners are encountering the failure mode at scale even in the absence of systematic public benchmarking.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| The KaBLE epistemic reliability benchmark (13,000 questions across 26 AI models) documents hallucination rates from 22% to 94%, with models demonstrating a structural failure to distinguish knowledge from belief: GPT-4o drops from 98.2% accuracy on true-belief tasks to 64.4% on first-person false-belief tasks, and DeepSeek R1 falls from over 90% to 14.4%. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| AI models handle third-person false beliefs considerably better than first-person ones: newer models achieve 95% accuracy on third-person false-belief tasks versus 62.6% on first-person tasks, and older models 79% versus 52.5% — indicating that epistemic failure is patterned rather than random and worsens when models process claims framed from the user's own perspective. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| Frontier AI model developers almost universally report performance on capability benchmarks but rarely report results on factuality or hallucination evaluations, creating a systematic gap between publicly documented AI capabilities and publicly documented factual reliability; the share of organizations citing inaccuracy as a relevant AI risk rose from 60% to 74% between 2024 and 2025. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
