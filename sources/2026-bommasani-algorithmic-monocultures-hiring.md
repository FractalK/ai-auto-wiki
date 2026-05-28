---
type: source
title: "Algorithmic Monocultures in Hiring"
created: 2026-05-28
updated: 2026-05-28
status: active
source_type: research-paper
author:
  - Rishi Bommasani
  - Sarah H. Bana
  - Kathleen A. Creel
  - Dan Jurafsky
  - Percy Liang
publication: "FAccT '26 (ACM Conference on Fairness, Accountability, and Transparency)"
published_date: 2026-05-26
ingested_date: 2026-05-28
ingest_via: staged
url: "https://doi.org/10.1145/3805689.3812400"
credibility_tier: practitioner
extraction_depth: full
related_topics:
  - "[[algorithmic-monoculture]]"
  - "[[llm-self-preference-bias]]"
---

This study provides the first large-scale empirical analysis of algorithmic monoculture in AI-mediated hiring, analyzing 4,197,168 applications submitted by 3,372,132 applicants to 1,746 positions screened by a single vendor (pymetrics) across 156 employers. The analysis finds clear racial disparities at the per-position level: 10.62% of positions demonstrate adverse impact against Black applicants under EEOC standards (covering 25.87% of all Black applications), and 5.32% demonstrate adverse impact against Asian applicants (covering 14.74% of all Asian applications) — disparities obscured when impact ratios are computed in aggregate, which meet the EEOC four-fifths threshold. The paper provides the first large-scale evidence of systemic rejection: 4% of applicants applying to 10 positions are rejected from all of them, a rate exceeding the baseline expected under chance independence, and counterfactual simulation shows applicants would need to submit 25 applications to reduce systemic rejection probability below 0.1%. The authors recommend per-position adverse impact measurement as the appropriate standard for vendor-mediated algorithmic hiring, along with market surveillance mechanisms and researcher access to enable independent auditing of deployed systems.
