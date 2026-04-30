---
type: comparison
title: Legal AI Tools Hallucination Rate Comparison
created: 2026-04-25
updated: 2026-04-29
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

All three leading legal AI research tools demonstrated meaningful hallucination rates in independent benchmarking — none can substitute for per-citation human verification of cited authorities in legal practice.

| Dimension | Lexis+ AI (LexisNexis) | Westlaw AI-Assisted Research (TR) | Ask Practical Law AI (TR) |
|---|---|---|---|
| Provider claimed reliability | "Hallucination-free linked citations" | "Hallucination-free" | Not specified |
| Error rate — Stanford benchmark | >17% incorrect | >34% incorrect | >17% incorrect |
| Hallucination types | Incorrect answers + misgrounding | Incorrect answers + misgrounding | Incorrect answers + misgrounding |
| Sycophancy failures | Documented | Documented | Documented |
| Published evaluation data | None | None | None |
| Researcher access for testing | Restricted | Restricted | Restricted |

## Verdict

Prefer [[lexisnexis-lexis-plus-ai]] or [[thomson-reuters-ask-practical-law-ai]] when error rate minimization is the primary criterion — both benchmarked at comparable rates (>17%) that are less than half of Westlaw AI's rate. Avoid [[thomson-reuters-westlaw-ai]] for error-sensitive tasks; it benchmarked at >34%, more than double the other two tools in the same study, with a documented failure to reflect post-Dobbs law on abortion restrictions.

See [[legal-ai-hallucination-pitfalls]] for detailed failure mode documentation and mitigation guidance.

## Evidence Notes

**Study design:** Stanford RegLab and HAI, May 2024; preregistered dataset of 200+ open-ended queries across four categories: jurisdiction-specific, time-specific, false premise, and general doctrine.<br>
**Data currency:** Tool versions are not disclosed by providers; error rates reflect May 2024 benchmarking and may not reflect current performance — treat as establishing a reliability floor, not current-state data.<br>
**Hallucination types:** Two distinct forms documented — outright incorrect (states the law wrong) and misgrounded (cites a real authority that does not support the stated claim); misgrounded citations pass URL existence checks and require reading the cited authority to detect.<br>
**Sycophancy:** All three tools confirmed false legal premises rather than correcting them; practitioners should explicitly instruct tools to flag incorrect premises and avoid framing queries with embedded legal conclusions.<br>
**Researcher access:** All three providers restrict independent testing access and publish no systematic evaluation data; vendor "hallucination-free" claims are not supported by the independent benchmark.
