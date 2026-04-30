---
type: comparison
title: Legal AI Tools Hallucination Rate Comparison
created: 2026-04-25
updated: 2026-04-25
comparison_type: tool-vs-tool
entities_compared:
  - "[[tools/lexisnexis-lexis-plus-ai]]"
  - "[[tools/thomson-reuters-westlaw-ai]]"
  - "[[tools/thomson-reuters-ask-practical-law-ai]]"
use_case: Evaluating leading legal AI research tools for hallucination rates and reliability before adopting for legal practice
status: current
source_count: 1
related_topics:
  - "[[legal-ai-hallucination]]"
---

*Based on: [[2024-ai-trial-legal-models-hallucinate]] — Stanford RegLab and HAI, May 2024. Study design: preregistered dataset of 200+ open-ended legal queries across four categories. Note: all three tools are practitioner-sourced self-descriptions; error rate data is from independent Stanford benchmarking.*

## Performance Comparison

| Dimension | Lexis+ AI (LexisNexis) | Westlaw AI-Assisted Research (TR) | Ask Practical Law AI (TR) |
|---|---|---|---|
| Provider claimed reliability | "Hallucination-free linked citations" | "Hallucination-free" | Not specified |
| Error rate — Stanford benchmark | >17% incorrect | >34% incorrect | >17% incorrect |
| Hallucination types | Incorrect answers + misgrounding | Incorrect answers + misgrounding | Incorrect answers + misgrounding |
| Sycophancy failures | Documented | Documented | Documented |
| Published evaluation data | None | None | None |
| Researcher access for testing | Restricted | Restricted | Restricted |

## Query Category Performance

The Stanford benchmark tested four query types. All three tools performed poorly on:

- **Jurisdiction-specific questions** — circuit splits and jurisdiction-dependent rules expose retrieval failures when semantically similar but inapplicable authority is returned
- **Time-specific questions** — recent changes in law (e.g., post-Dobbs abortion law) reveal failures to update or flag overturned precedent
- **False premise questions** — all three systems demonstrated sycophancy failures, agreeing with incorrect user premises rather than correcting them
- **General doctrine** — both correct answers and misgrounded citations observed across all tools; Westlaw showed the highest error rate in this category

## Hallucination Types

Both forms of legal hallucination appeared across all three tools:

1. **Outright incorrect** — the system states the law incorrectly or makes a factual error with no supporting citation
2. **Misgrounded** — the system cites a real, existing authority that does not in fact support the stated legal claim; this type passes a URL existence check and requires reading the cited authority to detect

The study authors argue that misgrounded citations may be more dangerous than outright errors because they create an appearance of authoritative support that attorneys and courts may not verify.

## Selection Guidance

Given the Stanford benchmark findings, no tested tool can be relied on as a primary research mechanism without systematic verification of citations and legal conclusions. Key considerations:

- Westlaw AI-Assisted Research showed the highest error rate (>34%), more than double the other two tools — users requiring the lowest possible error rate should prefer Lexis+ AI or Ask Practical Law AI pending updated benchmarking
- All three tools demonstrated sycophancy; practitioners should avoid framing queries with assumptions about legal conclusions and should explicitly instruct the tool to flag incorrect premises
- The absence of published evaluations from any provider means that error rates in the Stanford study may not reflect current tool performance; practitioners should treat the study as establishing a floor on reliability concern, not as current-state data

See [[legal-ai-hallucination-pitfalls]] for detailed failure mode documentation and mitigation guidance.
