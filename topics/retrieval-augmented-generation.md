---
type: topic
title: Retrieval-Augmented Generation
created: 2026-04-28
updated: 2026-05-20
aliases:
  - RAG
summary: A technique in which a language model retrieves relevant documents from an external corpus at inference time to augment its response, reducing hallucination on knowledge-intensive tasks while facing architectural evolution toward graph-structured retrieval, long-context integration tradeoffs, and persistent gaps between accepted context window size and effective deep comprehension.
status: developing
source_count: 1
last_assessed: 2026-05-20
related_topics:
  - "[[llm-wiki-pattern]]"
  - "[[legal-ai-hallucination]]"
  - "[[llm-position-bias]]"
  - "[[llm-fundamentals]]"
  - "[[ai-capability-benchmarking]]"
related_tools:
  - "[[lexisnexis-lexis-plus-ai]]"
  - "[[thomson-reuters-westlaw-ai]]"
  - "[[thomson-reuters-ask-practical-law-ai]]"
technical_depth: practitioner
---

Retrieval-Augmented Generation (RAG) is an inference-time augmentation technique in which a language model retrieves relevant documents from an external corpus and injects them into the context window before generating a response. Rather than relying solely on knowledge compressed into model parameters during pretraining, RAG grounds responses in retrieved material — reducing hallucination on factual and knowledge-intensive tasks while introducing new failure modes when retrieval precision is low, when retrieved authority is jurisdictionally or temporally inapplicable, or when position bias causes retrieved content to be underweighted based on its placement in the context window.

## Retrieval Architectures and Their Tradeoffs

Standard RAG pipelines retrieve individual text chunks based on query similarity. This works well for single-document lookups but struggles when answers require synthesizing information across multiple documents or understanding high-level thematic relationships. In 2024, Microsoft Research introduced Graph RAG, which structures source material into a knowledge graph and generates community summaries capturing high-level themes — enabling more effective responses to queries requiring cross-document synthesis. Other architectural variants focus on multistep retrieval (iterative expansion of the query context) or passage reranking before generation.

All RAG architectures involve tradeoffs between answer quality, retrieval latency, and cost. Graph RAG improves synthesis quality on complex queries but requires upfront graph construction and imposes higher query overhead. Standard chunk-based RAG is faster and cheaper but degrades on questions that cannot be answered by a single retrieved passage. Choosing among architectures requires knowledge of the query distribution the system will face in deployment.

## Context Windows and Deep Comprehension

Context windows — the amount of text a model can process in a single input — have grown by approximately 30× per year since mid-2023, with leading models now accepting 1 million or more tokens. This expansion has direct implications for RAG systems: wider context windows can accommodate more retrieved material without truncation. However, the relationship between accepted context length and effective comprehension is not linear.

Research on LongBench v2, an expert-level long-context benchmark, documents this gap directly: human experts scored 53.7% accuracy under a 15-minute time limit, and the best model scored 57.7% — a narrow margin that contrasts with the large human-AI gaps on structured benchmarks. Models that reason step-by-step through long documents outperform those answering immediately, suggesting that how a model processes long input matters as much as the volume it can accept. Separately, models handle simple lookups well but degrade on tasks requiring multiple pieces of matching information or condition application across a very long document. Longer inputs also impose practical costs: slower response times, higher operating expense, and reduced accuracy for content appearing late in the input sequence.

For RAG practitioners, this means that increasing context window size is not a substitute for retrieval precision. Flooding the context window with loosely relevant passages does not guarantee that the model will attend to the right material. Retrieval quality — returning the most relevant passages rather than the most text — remains the critical determinant of RAG output quality in long-context settings.

## Text Embedding Benchmarking

Text embedding models underpin retrieval in RAG systems by encoding documents and queries into a shared vector space where similarity search identifies relevant passages. The Massive Text Embedding Benchmark (MTEB), which evaluates embedding models across 50+ datasets spanning 8 task categories, shows steady improvement: the top average score on MTEB (English v2) reached approximately 76 in 2025, up ~11 points since 2023. However, no model approaches a perfect score, and performance varies substantially across task types. Embedding quality differences between models directly affect retrieval recall in RAG deployments.

## Data Records

| Metric | Value | Conditions | Measurement Date | Source | Status |
|---|---|---|---|---|---|
| Context window growth rate | ~30× per year | Approximate doubling rate since mid-2023; models now accepting 1M+ tokens | 2025 | [[2026-stanford-hai-ai-index]] | current |
| LongBench v2 — best model | 57.7% | Expert-level long-context benchmark; human experts score 53.7% under 15-minute time limit; step-by-step reasoning improves performance | 2025 | [[2026-stanford-hai-ai-index]] | current |
| MTEB (English v2) top score | 75.97 | Best embedding model; 50+ datasets, 8 task categories; up ~11 points since 2023 | 2025 | [[2026-stanford-hai-ai-index]] | current |

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| RAG-based legal AI systems retrieve documents based on semantic similarity, which does not guarantee jurisdictional or temporal applicability, contributing to hallucination rates of 17–34% in independent benchmarking of leading legal AI tools. | [[legal-ai-hallucination]] [derived] | 2026-04-25 | current | derived | false |
| The LLM Wiki pattern differs from RAG architectures in that source synthesis occurs at ingest time rather than at query time, enabling pre-computed cross-references and contradiction detection without live document retrieval. | [[llm-wiki-pattern]] [derived] | 2026-04-22 | current | derived | false |
| Position bias in transformer models — causing underweighting of information placed in the middle of long input sequences — directly affects RAG systems, since retrieved passage placement within the context window influences which content effectively informs the model's response. | [[llm-position-bias]] [derived] | 2026-04-25 | current | derived | false |
| Context windows have grown ~30× per year since mid-2023, but the gap between accepted context length and effective comprehension remains wide: models degrade on multi-needle retrieval tasks, and best-model performance on LongBench v2 (57.7%) only narrowly exceeds human expert performance (53.7%) — confirming that retrieval precision, not context window size, is the limiting factor in RAG quality. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| Graph RAG, introduced by Microsoft Research in 2024, addresses standard RAG's weakness on cross-document synthesis by structuring source material into a knowledge graph with community summaries, enabling more effective responses to complex queries at the cost of higher construction overhead and query latency. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
