---
type: tool
title: Westlaw AI-Assisted Research (Thomson Reuters)
created: 2026-04-25
updated: 2026-04-25
summary: Thomson Reuters's AI-assisted legal research product built on RAG over the Westlaw database, independently benchmarked at a greater than 34 percent hallucination rate — the highest of the three leading legal AI tools tested by Stanford RegLab in 2024.
status: active
vendor: Thomson Reuters
pricing_model: enterprise
access_tier:
  - enterprise
capabilities:
  - Legal case law research via retrieval-augmented generation over the Westlaw database
  - AI-assisted responses to open-ended legal research queries
  - Citation to legal authorities
limitations:
  - Greater than 34% error rate on open-ended legal queries per Stanford RegLab benchmark (2024) — highest of the tools tested
  - Sycophancy failures documented — system may agree with false legal premises rather than correcting them
  - No published systematic evaluation data from provider
source_count: 1
last_assessed: 2026-04-25
related_topics:
  - [[legal-ai-hallucination]]
related_tools:
  - [[lexisnexis-lexis-plus-ai]]
  - [[thomson-reuters-ask-practical-law-ai]]
---

Westlaw AI-Assisted Research is Thomson Reuters's generative AI feature within the Westlaw legal research platform, built on retrieval-augmented generation over the Westlaw database. Independent benchmarking by Stanford RegLab and HAI researchers in 2024 found an error rate exceeding 34 percent on a preregistered set of over 200 open-ended legal queries — the highest error rate of the three legal AI tools tested and more than double the rate for Lexis+ AI and Ask Practical Law AI. Thomson Reuters does not publish systematic evaluation results or provide researchers with access for independent testing. A documented failure example from the study shows the system reciting the overturned "undue burden" standard for abortion law as current law following Dobbs.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| Westlaw AI-Assisted Research hallucinated more than 34 percent of the time on a preregistered Stanford RegLab/HAI benchmark of over 200 open-ended legal queries — the highest error rate of the three legal AI tools tested and more than double that of Lexis+ AI. | [[2024-ai-trial-legal-models-hallucinate]] | 2024-05-23 | current | 0.5 | false |
| Westlaw AI-Assisted Research incorrectly recited the "undue burden" standard for abortion restrictions as current law in the Stanford benchmark, failing to reflect the Dobbs v. Jackson Women's Health Organization ruling. | [[2024-ai-trial-legal-models-hallucinate]] | 2024-05-23 | current | 0.5 | false |
