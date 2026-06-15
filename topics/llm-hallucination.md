---
type: topic
title: LLM Hallucination
created: 2026-05-03
updated: 2026-06-14
status: developing
summary: The tendency of large language models to generate plausible-sounding but factually incorrect or fabricated content — including nonexistent citations, invented entities, confidently stated errors, and context-grounding failures where models rely on parametric knowledge instead of provided documents — as a structural consequence of next-token prediction without factual verification.
source_count: 3
last_assessed: 2026-06-14
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

## Context Grounding Failure

A distinct form of hallucination involves ignoring provided context and generating from parametric (training-time) knowledge instead. In legal AI benchmarks, this failure mode is well-documented: CaseLaw v2 evaluates models against recent US and Canadian court decisions dated after training cutoffs, specifically to force document-grounded reasoning. Despite this design, a recurring failure pattern is models relying on general legal knowledge rather than the supplied documents, even when explicitly instructed to do so. The consequence is outputs that are legally fluent but not grounded in the case materials actually provided — a structurally equivalent failure to citation hallucination, with the additional problem that the model's confident tone provides no signal of the deviation.

Context grounding failure is practically significant in any [[retrieval-augmented-generation]] or document-assisted workflow: a model that ignores retrieved context and generates from internal knowledge reproduces exactly the accuracy and currency gaps that RAG architectures are designed to avoid. Measuring context grounding fidelity — how consistently a model anchors its output in provided documents versus its internal knowledge — is not yet standard practice in frontier model evaluation.

## Reporting Gap

Hallucination and factuality benchmarking is systematically underreported relative to capability benchmarking. The Stanford HAI AI Index 2026 documents that almost all frontier model developers report results on MMLU, SWE-bench, and coding evaluations, while reporting on responsible AI benchmarks — including factuality and hallucination evaluations — remains sparse. This creates a public record dense with capability claims but thin on reliability evidence. The practical consequence: organizational decisions about AI deployment are made against a backdrop of well-documented capability metrics and poorly documented factual reliability.

The share of organizations that consider inaccuracy a relevant AI risk rose from 60% to 74% between 2024 and 2025, and the share actively mitigating inaccuracy risks rose from 55% to 71% — suggesting that practitioners are encountering the failure mode at scale even in the absence of systematic public benchmarking.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| The KaBLE epistemic reliability benchmark (13,000 questions across 26 AI models) documents hallucination rates from 22% to 94%, with models demonstrating a structural failure to distinguish knowledge from belief: GPT-4o drops from 98.2% accuracy on true-belief tasks to 64.4% on first-person false-belief tasks, and DeepSeek R1 falls from over 90% to 14.4%. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| AI models handle third-person false beliefs considerably better than first-person ones: newer models achieve 95% accuracy on third-person false-belief tasks versus 62.6% on first-person tasks, and older models 79% versus 52.5% — indicating that epistemic failure is patterned rather than random and worsens when models process claims framed from the user's own perspective. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| Frontier AI model developers almost universally report performance on capability benchmarks but rarely report results on factuality or hallucination evaluations, creating a systematic gap between publicly documented AI capabilities and publicly documented factual reliability; the share of organizations citing inaccuracy as a relevant AI risk rose from 60% to 74% between 2024 and 2025. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| In legal AI benchmarks (CaseLaw v2), a recurring failure pattern is models relying on general parametric knowledge rather than the supplied case documents — even when explicitly instructed to use them — producing legally fluent but document-ungrounded outputs that reproduce the accuracy and currency gaps that retrieval-augmented architectures are designed to prevent. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| Munich Regional Court ruled in June 2026 that Google is liable for false statements in AI Overviews because the AI produced new synthetic associations between plaintiffs and fraudulent practices not present in any linked source document — establishing that hallucination-by-synthesis (generating new claims by combining source material rather than directly fabricating text) carries legal liability and cannot invoke safe-harbor protections available to link aggregators. | [[2026-google-ai-overviews-liability]] | 2026-06-13 | current | 2 | false |

## Legal Accountability

In June 2026, the Munich Regional Court ruled that Google is liable for false statements generated by its AI Overviews search feature — specifically, associations between publishers and fraudulent practices not present in any linked source document. The court's analysis distinguished generative AI search from traditional link aggregation: where a link-based search engine curates third-party statements, AI Overviews generates new statements via synthesis, making the developer the author of record for any resulting false claims. User-facing disclaimers acknowledging AI error potential were found insufficient to transfer liability to users, since the third parties falsely associated by the AI had never made the statements at issue — there is no third party to pursue.

The ruling introduces a legal framing of hallucination that may prove consequential beyond the search context. The standard industry defense — that users should verify AI outputs because the model may contain errors — does not protect against liability when the AI generates new synthetic claims not traceable to any source. For practitioners deploying AI in contexts where synthesized output could associate named individuals, organizations, or products with actions they never took, the Munich ruling establishes that the verification burden cannot be fully transferred to end users via disclaimer language.
