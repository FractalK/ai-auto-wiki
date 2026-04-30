---
type: source
title: "On the Emergence of Position Bias in Transformers"
created: 2026-04-25
updated: 2026-04-25
status: active
source_type: research-paper
author:
  - Xinyi Wu
  - Yifei Wang
  - Stefanie Jegelka
  - Ali Jadbabaie
publication: International Conference on Machine Learning (ICML 2025)
published_date: 2025-07-18
ingested_date: 2026-04-25
ingest_via: staged
url: https://arxiv.org/abs/2502.01951
credibility_tier: peer-reviewed
extraction_depth: full
related_topics:
  - "[[llm-position-bias]]"
---

MIT researchers (Wu, Wang, Jegelka, Jadbabaie) develop a graph-theoretic framework to analyze how architectural choices in transformer models — particularly causal masking and positional encoding schemes — produce systematic position bias. The paper proves formally (Theorem 4.1) that causal masking is sufficient to cause attention toward the first token to approach certainty with exponential convergence as model depth increases, independent of the importance of early tokens to the task, and demonstrates through experiments that this produces a U-shaped accuracy pattern ("lost-in-the-middle") in information retrieval tasks where models perform worst when relevant content is in the middle of a sequence. The analysis further shows that training data with positional structure independently contributes to position bias, and that architectural mitigations (positional encodings, alternative masking schemes) interact with depth in ways that may dilute or amplify the effect across layers.
