---
type: topic
title: Retrieval-Augmented Generation
created: 2026-04-28
updated: 2026-04-28
aliases:
  - RAG
summary: A technique in which a language model retrieves relevant documents from an external corpus at inference time to augment its response, reducing hallucination on knowledge-intensive tasks while introducing retrieval accuracy and authority selection challenges.
status: stub
source_count: 0
related_topics:
  - [[llm-wiki-pattern]]
  - [[legal-ai-hallucination]]
  - [[llm-position-bias]]
  - [[llm-fundamentals]]
related_tools:
  - [[lexisnexis-lexis-plus-ai]]
  - [[thomson-reuters-westlaw-ai]]
  - [[thomson-reuters-ask-practical-law-ai]]
---

Retrieval-Augmented Generation (RAG) is an inference-time augmentation technique in which a language model retrieves relevant documents from an external corpus and injects them into the context window before generating a response. Rather than relying solely on knowledge compressed into model parameters during pretraining, RAG grounds responses in retrieved material — reducing hallucination on factual and knowledge-intensive tasks while introducing new failure modes when retrieval precision is low, when retrieved authority is jurisdictionally or temporally inapplicable, or when position bias causes retrieved content to be underweighted based on its placement in the context window.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| RAG-based legal AI systems retrieve documents based on semantic similarity, which does not guarantee jurisdictional or temporal applicability, contributing to hallucination rates of 17–34% in independent benchmarking of leading legal AI tools. | [[legal-ai-hallucination]] [derived] | 2026-04-25 | current | derived | false |
| The LLM Wiki pattern differs from RAG architectures in that source synthesis occurs at ingest time rather than at query time, enabling pre-computed cross-references and contradiction detection without live document retrieval. | [[llm-wiki-pattern]] [derived] | 2026-04-22 | current | derived | false |
| Position bias in transformer models — causing underweighting of information placed in the middle of long input sequences — directly affects RAG systems, since retrieved passage placement within the context window influences which content effectively informs the model's response. | [[llm-position-bias]] [derived] | 2026-04-25 | current | derived | false |
