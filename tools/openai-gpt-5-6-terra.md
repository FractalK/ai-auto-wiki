---
type: tool
title: GPT-5.6 Terra
created: 2026-08-10
updated: 2026-08-10
summary: A capable, lower-cost model in OpenAI's GPT-5.6 family, rated High capability under the Preparedness Framework in both biology/chemistry and cybersecurity despite its smaller size, and the only GPT-5.6 model to outperform the flagship Sol on the small-scale LLM pretraining self-improvement evaluation.
status: active
vendor: OpenAI
pricing_model: usage-based
access_tier:
  - consumer
  - api
  - enterprise
capabilities:
  - Rated High capability under the Preparedness Framework in both Biological/Chemical and Cybersecurity domains despite being a smaller, lower-cost model than Sol
  - Internal Capture-the-Flag cybersecurity evaluation scores 91.84% pass@1, exceeding GPT-5.5 (88.06%) and GPT-5.4 (83.75%)
  - Tacit Knowledge and Troubleshooting (biology) score of 84.1% accounting for refusals — the highest of the newly released GPT-5.6 models and above the 80% expert-consensus threshold
  - Outperforms flagship GPT-5.6 Sol on the NanoGPT self-improvement evaluation (small-scale LLM pretraining optimization), reaching 14.5% mean reward versus Sol's 9.7%
  - Matches or exceeds Sol on PostTrainBench Lite (post-training recipe design) and MLE-Bench Revised at higher simulated latency budgets
primary_use_cases:
  - Cost-sensitive agentic coding and long-horizon software engineering
  - Post-training and machine learning research experimentation
  - Cybersecurity research under Trusted Access for Cyber
limitations:
  - Below Sol on most cybersecurity and biosecurity capability evaluations, including CVE-Bench, ExploitBench, ProtocolQA Open-Ended, and AAV capsid packaging prediction
  - Lower chain-of-thought controllability than Sol, similar to prior-generation GPT-5.x models
  - Carries the same High-capability safeguard restrictions as Sol despite generally lower measured capability on most individual evaluations
source_count: 1
last_assessed: 2026-08-10
related_tools:
  - "[[openai-gpt-5-6-sol]]"
  - "[[openai-gpt-5-6-luna]]"
  - "[[openai-gpt-5-5]]"
related_topics:
  - "[[ai-agentic-workflows]]"
  - "[[ai-assisted-vulnerability-discovery]]"
  - "[[ai-biosecurity]]"
  - "[[recursive-self-improvement]]"
technical_depth: practitioner
---

GPT-5.6 Terra is the capable, lower-cost model in OpenAI's GPT-5.6 family, positioned between flagship Sol and the fastest tier, Luna. Despite its smaller size, Terra is rated High capability under the Preparedness Framework in both the Biological/Chemical and Cybersecurity domains, on the reasoning that its capability profile is close enough to Sol's on the bottleneck evaluations that Sol's safeguard rule-out for Critical-level risk (no functional zero-day exploits or full-cycle biological threat engineering) applies to Terra as well.

On cybersecurity, Terra scores 91.84% pass@1 on OpenAI's internal Capture-the-Flag evaluation — below Sol's saturating 96.7% but above GPT-5.5 (88.06%) and GPT-5.4 (83.75%). On biology, Terra's accuracy on the Tacit Knowledge and Troubleshooting multiple-choice evaluation (accounting for refusals) reaches 84.1%, the highest score among the newly released GPT-5.6 models and above the 80% expert-consensus indicative threshold — though OpenAI notes this may reflect the evaluation approaching saturation rather than a genuine capability lead over Sol.

Terra is the only model in the GPT-5.6 family to outperform flagship Sol on a self-improvement evaluation: on NanoGPT, which measures an agent's ability to optimize a small-scale LLM pretraining setup under compute and time constraints, Terra reaches 14.5% mean reward against a human best-solution benchmark of 72.38%, compared to Sol's 9.7%. Terra also matches or exceeds Sol on PostTrainBench Lite (designing a post-training recipe for an open-source base model) and MLE-Bench Revised (Kaggle-style ML competitions) when given a larger simulated-latency budget, though both models still fall well short of the strongest human or test-time-compute-harness solutions on these evaluations.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| GPT-5.6 Terra is rated High capability under OpenAI's Preparedness Framework in both the Biological/Chemical and Cybersecurity domains despite being a smaller, lower-cost model than flagship Sol, scoring 91.84% pass@1 on OpenAI's internal Capture-the-Flag evaluation. | [[2026-openai-gpt-5-6-system-card]] | 2026-07-09 | current | 2 | false |
| GPT-5.6 Terra outperforms flagship GPT-5.6 Sol on the NanoGPT self-improvement evaluation, reaching 14.5% mean reward against a human best-solution benchmark of 72.38%, compared to Sol's 9.7% — the only self-improvement evaluation in the card where a smaller GPT-5.6 model exceeds the flagship. | [[2026-openai-gpt-5-6-system-card]] | 2026-07-09 | current | 2 | false |
| GPT-5.6 Terra scores 84.1% (accounting for refusals) on the Tacit Knowledge and Troubleshooting biology evaluation, the highest among the newly released GPT-5.6 models and above the 80% expert-consensus indicative threshold, though OpenAI attributes the result partly to possible evaluation saturation. | [[2026-openai-gpt-5-6-system-card]] | 2026-07-09 | current | 2 | false |

## Data Records

| Metric | Value | Conditions | Measurement Date | Source | Status |
|---|---|---|---|---|---|
| Internal Capture-the-Flag (cyber) | 91.84% | pass@1; internal curated CTF set, 63 challenges | 2026-07 | [[2026-openai-gpt-5-6-system-card]] | current |
| Tacit Knowledge and Troubleshooting (biology) | 84.1% | Accounting for refusals/safe completions as successes; 60-question MCQ set | 2026-07 | [[2026-openai-gpt-5-6-system-card]] | current |
| NanoGPT self-improvement | 14.5% | Mean reward; human best solution = 72.38%; one H100 GPU budget | 2026-07 | [[2026-openai-gpt-5-6-system-card]] | current |
