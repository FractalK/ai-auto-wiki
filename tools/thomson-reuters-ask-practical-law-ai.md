---
type: tool
title: Ask Practical Law AI (Thomson Reuters)
created: 2026-04-25
updated: 2026-04-25
summary: Thomson Reuters's AI assistant for practical law questions built on RAG, independently benchmarked at a greater than 17 percent error rate on open-ended legal queries by Stanford RegLab in 2024, comparable to LexisNexis Lexis+ AI.
status: active
vendor: Thomson Reuters
pricing_model: enterprise
access_tier:
  - enterprise
capabilities:
  - AI-assisted responses to practical legal questions via retrieval-augmented generation
  - Access to Thomson Reuters Practical Law content database
limitations:
  - Greater than 17% error rate on open-ended legal queries per Stanford RegLab benchmark (2024)
  - Sycophancy failures documented — system may agree with false legal premises rather than correcting them
  - No published systematic evaluation data from provider
source_count: 1
last_assessed: 2026-04-25
related_topics:
  - [[legal-ai-hallucination]]
related_tools:
  - [[lexisnexis-lexis-plus-ai]]
  - [[thomson-reuters-westlaw-ai]]
---

Ask Practical Law AI is Thomson Reuters's generative AI assistant for practical legal questions, drawing on the Practical Law content database via retrieval-augmented generation. Independent benchmarking by Stanford RegLab and HAI researchers in 2024 found an error rate exceeding 17 percent on a preregistered set of over 200 open-ended legal queries, grouped with Lexis+ AI as the better-performing of the three tools tested. Thomson Reuters does not publish systematic evaluation results. A documented failure example from the study shows the system failing to correct a user's false premise that Justice Ginsburg dissented in Obergefell v. Hodges, instead confirming the false premise and adding fabricated details.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| Ask Practical Law AI produced incorrect information more than 17 percent of the time on a preregistered Stanford RegLab/HAI benchmark of over 200 open-ended legal queries. | [[2024-ai-trial-legal-models-hallucinate]] | 2024-05-23 | current | 0.5 | false |
| Ask Practical Law AI failed to correct a false premise in the Stanford benchmark, confirming that Justice Ginsburg dissented in Obergefell v. Hodges and adding false details about her reasoning — she did not dissent. | [[2024-ai-trial-legal-models-hallucinate]] | 2024-05-23 | current | 0.5 | false |
