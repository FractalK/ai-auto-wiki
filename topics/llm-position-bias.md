---
type: topic
title: LLM Position Bias
created: 2026-04-25
updated: 2026-04-25
summary: The structural tendency of transformer language models to overweight information at the beginning and end of input sequences while neglecting the middle, caused by causal masking and amplified by model depth, with implications for information retrieval, long-context reasoning, and RAG systems.
status: stub
source_count: 1
last_assessed: 2026-04-25
technical_depth: research
---

Position bias is the tendency of transformer language models to overweight information at the beginning and end of input sequences while neglecting the middle — a structural consequence of how attention mechanisms distribute influence across positions. An ICML 2025 paper by MIT researchers (Wu, Wang, Jegelka, Jadbabaie) provides the first formal theoretical account of this phenomenon, tracing it to the interaction of causal masking, positional encoding schemes, and model depth. The framework establishes that causal masking alone is sufficient to produce beginning-of-sequence bias, while positional encodings such as RoPE extend the bias to both ends — producing the U-shaped accuracy pattern ("lost-in-the-middle") observed in practice.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| Causal masking in transformer architectures causes the probability that any token attends to the first token to approach 1 with exponential convergence as model depth increases, independent of the actual importance of early tokens to the task (formally proven at ICML 2025). | [[2025-emergence-position-bias-transformers]] | 2025-07-18 | current | 3.0 | false |
| Transformer models exhibit a "lost-in-the-middle" phenomenon in information retrieval: accuracy follows a U-shaped pattern, highest when correct content is at the beginning or end of an input sequence and lowest when it is in the middle, as validated experimentally by Wu et al. (ICML 2025). | [[2025-emergence-position-bias-transformers]] | 2025-07-18 | current | 3.0 | false |
| Position bias toward earlier inputs is amplified with increasing transformer model depth regardless of the positional encoding scheme used, because additional attention layers compound the cumulative importance of early tokens across layers. | [[2025-emergence-position-bias-transformers]] | 2025-07-18 | current | 3.0 | false |
