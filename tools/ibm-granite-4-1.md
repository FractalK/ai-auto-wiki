---
type: tool
title: IBM Granite 4.1
created: 2026-05-27
updated: 2026-05-27
aliases:
  - Granite 4.1
summary: IBM open-weight model family spanning language (3B/8B/30B), vision, speech, safety moderation, and multilingual embedding; Apache 2.0; designed for enterprise instruction following and token efficiency over reasoning performance.
status: active
vendor: IBM
pricing_model: open-source
access_tier:
  - consumer
  - api
  - enterprise
capabilities:
  - Instruction following and tool calling (3B/8B/30B language models, 512K-token context)
  - Document understanding — table extraction, chart analysis, KVP extraction (Vision 4.1)
  - Multilingual speech recognition and translation with WER 5.33% (Speech 4.1 2B)
  - LLM input/output safety moderation across six risk categories (Guardian 4.1)
  - Multilingual semantic search across 200+ languages (Embedding R2, 97M parameters)
  - Air-gapped and on-premises deployment via Apache 2.0 license
limitations:
  - Non-reasoning architecture; not suited for tasks requiring explicit multi-step reasoning chains
  - All capability and benchmark claims are vendor-sourced; no independent verification available at publication
primary_use_cases:
  - Enterprise instruction following and workflow automation
  - Business document and record processing
  - AI output safety moderation pipelines
  - Multilingual transcription in constrained or edge environments
source_count: 1
last_assessed: 2026-05-27
related_topics:
  - "[[llm-fundamentals]]"
  - "[[ai-agentic-workflows]]"
technical_depth: practitioner
---

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| Granite 4.1 language models (3B/8B/30B) are dense decoder-only architectures with 512K-token context windows released under Apache 2.0, available on Hugging Face, Ollama, and IBM watsonx. [vendor-sourced] | [[2026-ibm-granite-4-1-models]] | 2026-04-29 | current | 1 | false |
| IBM claims the Granite 4.1 8B instruct model matches or outperforms the prior Granite 4.0 32B Mixture-of-Experts model on instruction-following and tool-calling benchmarks, presenting efficiency at reduced parameter count as the primary differentiator over reasoning-model architectures. [vendor-sourced — comparative claim] | [[2026-ibm-granite-4-1-models]] | 2026-04-29 | current | 1 | false |
| Granite Guardian 4.1 detects six safety categories — including hallucinations, prompt injection, and agentic risks — using IBM's AI Risk Atlas framework, and IBM reports it topped GuardBench in independent benchmarks. [vendor-sourced] | [[2026-ibm-granite-4-1-models]] | 2026-04-29 | current | 1 | false |
| Granite Speech 4.1 2B achieves 5.33% word-error rate on standard ASR evaluation and IBM reports top-tier ranking on the OpenASR Leaderboard; a non-autoregressive variant (2B NAR) trades transcription richness for higher throughput and GPU utilization. [vendor-sourced] | [[2026-ibm-granite-4-1-models]] | 2026-04-29 | current | 1 | false |
| Granite Vision 4.1 applies a feature injection architecture (inspired by DeepStack) for document understanding tasks, and Granite Embedding Multilingual R2 supports semantic search across 200+ languages in a 97M-parameter model. [vendor-sourced] | [[2026-ibm-granite-4-1-models]] | 2026-04-29 | current | 1 | false |

## Data Records

| Metric | Value | Conditions | Measurement Date | Source | Status |
|---|---|---|---|---|---|
| Word Error Rate | 5.33% | Standard ASR evaluation, Granite Speech 4.1 2B | 2026-04 | [[2026-ibm-granite-4-1-models]] | current |

## Overview

IBM Granite 4.1 is a family of open-weight AI models released under Apache 2.0 licensing in April 2026. The family spans five product lines: dense decoder-only language models in 3B, 8B, and 30B parameter tiers; Granite Vision 4.1 for business document analysis; Granite Speech 4.1 for multilingual transcription; Granite Guardian 4.1 for safety moderation; and Granite Embedding Multilingual R2 for cross-lingual semantic search. IBM's design philosophy centers on enterprise efficiency — optimizing for instruction following, tool calling, and token cost at scale — rather than frontier reasoning performance, positioning the family as complementary to rather than competitive with reasoning-specialized models.

## Language Models

The Granite 4.1 language models support context windows up to 512K tokens and are available in base and instruct variants across the three parameter tiers. IBM trained the models on approximately 15 trillion tokens across multiple staged refinement phases, with progressive annealing toward technical, scientific, and mathematical data, and a multi-stage reinforcement learning pipeline targeting instruction adherence, conversation quality, factual accuracy, and mathematical reasoning. IBM positions the non-reasoning design as intentional: reasoning-model overhead is costly for the majority of enterprise tasks where a correct instruction-following response is sufficient. IBM claims the 8B instruct variant matches or outperforms the prior Granite 4.0 32B Mixture-of-Experts model on instruction-following and tool-calling benchmarks; this comparative claim is vendor-sourced and has not been independently verified. The models are available through AnythingLLM, Hugging Face, LM Studio, Ollama, OpenRouter, Replicate, and IBM watsonx, optimized for vLLM, SGLang, and llama.cpp inference runtimes.

## Specialized Variants

**Granite Vision 4.1** is a vision-language model designed for business document processing: table extraction, chart analysis, and key-value pair extraction from invoices and similar records. Its architecture uses a feature injection scheme — inspired by the DeepStack approach — that distributes visual representations across language model layers rather than prepending image tokens. IBM trained it on real and synthetically generated data, including the million-scale ChartNet dataset built using code-guided augmentation.

**Granite Speech 4.1** offers multilingual speech recognition and translation in three 2B-parameter variants. The standard 2B model targets broad enterprise deployment; the 2B Plus variant adds richer transcription features; the 2B NAR model uses non-autoregressive generation for higher throughput and better GPU utilization. IBM partnered with Australia's Royal Flying Doctor Service to apply Speech 4.1 to clinical transcription in noisy aircraft environments. IBM reports 5.33% WER and top-tier ranking on the OpenASR Leaderboard; these claims are vendor-sourced.

**Granite Guardian 4.1** is a moderation model compatible with any language model, open or proprietary. It evaluates inputs and outputs against six safety categories from IBM's AI Risk Atlas: socially biased content, hateful language, abusive or profane speech, hallucinations, agentic risks, and prompt injection attempts. IBM reports Guardian 4.1 topped GuardBench; this claim is vendor-sourced.

**Granite Embedding Multilingual R2** covers 200+ languages in a 97M-parameter model, supporting semantic search across multilingual document collections.

## Deployment and Licensing

All Granite 4.1 models are released under Apache 2.0, permitting commercial use, modification, and redistribution without royalty obligations. Local deployment is supported through Ollama and llama.cpp; cloud or managed inference through watsonx and OpenRouter; research use through Hugging Face and Weights & Biases. IBM offers enterprise support via watsonx for organizations requiring managed SLAs.
