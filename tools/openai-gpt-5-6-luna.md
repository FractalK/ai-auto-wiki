---
type: tool
title: GPT-5.6 Luna
created: 2026-08-10
updated: 2026-08-10
summary: The fastest and most cost-efficient model in OpenAI's GPT-5.6 family, still rated High capability under the Preparedness Framework in biology/chemistry and cybersecurity despite generally trailing Sol and Terra on individual benchmarks, and the best-scoring model in the family on OpenAI's first-person fairness evaluation.
status: active
vendor: OpenAI
pricing_model: usage-based
access_tier:
  - consumer
  - api
  - enterprise
capabilities:
  - Rated High capability under the Preparedness Framework in both Biological/Chemical and Cybersecurity domains despite being the smallest and fastest model in the family
  - Internal Capture-the-Flag cybersecurity evaluation scores 85.19% pass@1, above GPT-5.4 (83.75%) but below GPT-5.5 (88.06%) and Terra
  - Lowest harm_overall score (0.61%) on OpenAI's first-person fairness evaluation of any GPT-5.x model tested, indicating the smallest measured difference in response quality between statistically male- and female-associated user names
primary_use_cases:
  - High-throughput, latency-sensitive agentic tasks
  - Cost-constrained deployments requiring High-capability safeguard coverage
limitations:
  - Generally trails Sol and Terra on individual biosecurity and cybersecurity capability evaluations, including ExploitGym, SEC-bench Pro, and ProtocolQA Open-Ended
  - Weakest data-overwrite avoidance among the GPT-5.6 family on the destructive-actions evaluation (0.73 avoidance-only, 0.32 avoidance+correctness combined score, versus 0.83 and 0.44 for Sol)
  - Carries the same High-capability safeguard restrictions as Sol and Terra despite generally lower measured capability on most individual evaluations
source_count: 1
last_assessed: 2026-08-10
related_tools:
  - "[[openai-gpt-5-6-sol]]"
  - "[[openai-gpt-5-6-terra]]"
  - "[[openai-gpt-5-5]]"
related_topics:
  - "[[ai-agentic-workflows]]"
  - "[[ai-assisted-vulnerability-discovery]]"
  - "[[ai-biosecurity]]"
technical_depth: practitioner
---

GPT-5.6 Luna is the fastest and most cost-efficient model in OpenAI's GPT-5.6 family. Despite generally trailing flagship Sol and mid-tier Terra on individual capability evaluations, Luna is still rated High capability under the Preparedness Framework in both the Biological/Chemical and Cybersecurity domains — OpenAI's rationale is that Sol's rule-out of Critical-level risk (no functional zero-day exploits or full biological-threat engineering cycle) extends to the smaller, less capable Terra and Luna as well.

On cybersecurity, Luna scores 85.19% pass@1 on OpenAI's internal Capture-the-Flag evaluation, ahead of GPT-5.4 (83.75%) but behind GPT-5.5 (88.06%) and Terra. Luna is consistently the weakest of the three GPT-5.6 models on exploit-development evaluations such as ExploitGym and SEC-bench Pro, and on biosecurity troubleshooting evaluations including ProtocolQA Open-Ended. On the destructive-actions evaluation, which measures whether a coding agent completes a task without overwriting user data adversarially injected into its workspace, Luna scores lowest among the GPT-5.6 family on both the avoidance-only metric (0.73, versus 0.83 for Sol) and the combined avoidance-plus-correctness metric (0.32, versus 0.44 for Sol).

Luna's one notable strength relative to its siblings is on OpenAI's first-person fairness evaluation, which measures differences in response quality when a user's name is statistically associated with male or female first names. Luna records the lowest harm_overall score (0.61%) of any GPT-5.x model OpenAI reports in the card, ahead of Sol (0.98%), Terra (0.88%), and GPT-5.5 (1.12%).

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| GPT-5.6 Luna is rated High capability under OpenAI's Preparedness Framework in both the Biological/Chemical and Cybersecurity domains despite being the smallest and fastest model in the GPT-5.6 family, and generally trails Sol and Terra on individual capability evaluations such as ExploitGym and ProtocolQA Open-Ended. | [[2026-openai-gpt-5-6-system-card]] | 2026-07-09 | current | 2 | false |
| GPT-5.6 Luna records the lowest harm_overall score (0.61%) of any GPT-5.x model on OpenAI's first-person fairness evaluation, ahead of Sol (0.98%), Terra (0.88%), and GPT-5.5 (1.12%), indicating the smallest measured difference in response quality between male- and female-associated user names. | [[2026-openai-gpt-5-6-system-card]] | 2026-07-09 | current | 2 | false |
| GPT-5.6 Luna scores lowest among the GPT-5.6 family on the destructive-actions evaluation, completing challenging coding tasks without overwriting adversarially injected user data in only 32% of cases on the combined avoidance-and-correctness metric, versus 44% for Sol. | [[2026-openai-gpt-5-6-system-card]] | 2026-07-09 | current | 2 | false |

## Data Records

| Metric | Value | Conditions | Measurement Date | Source | Status |
|---|---|---|---|---|---|
| Internal Capture-the-Flag (cyber) | 85.19% | pass@1; internal curated CTF set, 63 challenges | 2026-07 | [[2026-openai-gpt-5-6-system-card]] | current |
| First-person fairness (harm_overall) | 0.61% | Lower is better; 95% CI reported in source | 2026-07 | [[2026-openai-gpt-5-6-system-card]] | current |
| Destructive-actions avoidance + correctness | 0.32 | Combined avoidance-of-overwrite and task-correctness metric | 2026-07 | [[2026-openai-gpt-5-6-system-card]] | current |
