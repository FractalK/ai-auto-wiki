---
type: topic
title: LLM Fundamentals
created: 2026-04-26
updated: 2026-04-26
summary: The foundational mechanics of large language model training, inference, and deployment, covering the pretraining and fine-tuning pipeline, scaling laws, System 1 reasoning constraints, agentic tool integration, and the principal security vulnerabilities that arise at each stage.
status: developing
source_count: 1
last_assessed: 2026-04-26
related_topics:
  - "[[scalable-oversight]]"
  - "[[llm-position-bias]]"
  - "[[constitutional-ai]]"
teaching_relevance: true
competency_domains:
  - practical-ai-use-and-interaction
  - output-verification-and-risk-assessment
  - tool-evaluation-and-selection
professional_contexts:
  - teaching-and-instruction
  - organizational-leadership-and-change-management
  - professional-and-continuing-education
technical_depth: foundational
---

Large language models are produced through a two-stage training process. In pretraining, a model is trained via next-token prediction on a very large corpus of text — on the order of tens to hundreds of terabytes — compressing a broad representation of human-generated knowledge into a set of neural network weights. The resulting base model is a statistical world model capable of high-fidelity continuation and completion, but it is not yet an assistant. Fine-tuning — including supervised instruction following and reinforcement learning from human feedback (RLHF) — reshapes the base model into a helpful, relatively safe assistant by training it on curated interaction data and human preference judgments. The fine-tuned model can be thought of as a thin behavioral layer over the base model's world knowledge.

Scaling laws describe a predictable empirical relationship between model performance and three input variables: model parameter count, training compute (measured in FLOP), and training dataset size. Within the ranges studied, increasing any of these variables reliably reduces validation loss, allowing research teams to forecast the expected benefit of larger training runs before they complete. Scaling laws are one of the most practically important findings in LLM research because they convert a fundamentally empirical process — training neural networks — into a partially plannable one.

## Reasoning Mode Constraints

LLMs in their current mainstream form operate as System 1 thinkers: they generate responses through a single forward pass through the network, without deliberate sequential search, backtracking, or verification. This is sufficient for tasks that can be answered from compressed world knowledge — pattern completion, factual retrieval, translation, code generation in familiar paradigms. It is structurally insufficient for tasks that require extended proof search, precise arithmetic, long-horizon planning, or verification of novel reasoning chains.

The System 2 analogy points toward a development direction: models that can spend variable compute at inference time — allocating more processing to harder subproblems, checking work, exploring alternatives. As of late 2023, this capability was aspirational for most practical deployments; post-training inference-time scaling techniques have since made partial progress on this gap.

## Agentic Deployment and the LLM Operating System

As LLMs are given access to external tools — web browsers, code interpreters, calculators, databases — they increasingly function as an orchestration layer rather than a standalone reasoner. Karpathy frames this as the "LLM OS" analogy: the model is the kernel, specialized tools are peripherals, and multi-step tasks are the applications. This architecture amplifies what LLMs can accomplish while simultaneously expanding the attack surface available to adversaries.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| LLMs are produced through a two-stage pipeline: unsupervised pretraining on large text corpora that compresses world knowledge into model parameters, followed by fine-tuning (including RLHF) that shapes the model into an assistant aligned with human preferences. | [[2023-karpathy-intro-large-language-models]] | 2023-11-22 | current | 0.5 | false |
| Scaling laws describe a predictable empirical relationship between model performance, training compute, and dataset size — improvements in any dimension reliably reduce validation loss, enabling research teams to forecast the value of larger training runs before they complete. | [[2023-karpathy-intro-large-language-models]] | 2023-11-22 | current | 0.5 | false |
| LLMs in their current form operate as System 1 reasoners — generating responses through a single forward pass without deliberate sequential search or verification — which structurally limits reliable performance on tasks requiring multi-step planning, complex mathematics, or extended reasoning chains. | [[2023-karpathy-intro-large-language-models]] | 2023-11-22 | current | 0.5 | false |
| Prompt injection — embedding adversarial instructions in external content an LLM agent processes — can silently redirect model behavior without the user's awareness, making it a class of attack that scales with LLM adoption in automated pipelines. | [[2023-karpathy-intro-large-language-models]] | 2023-11-22 | current | 0.5 | false |
| LLMs trained with RLHF develop a fine-tuned behavioral layer that constrains outputs but can be bypassed through jailbreaks; when jailbreaks succeed, the base model — which contains no safety constraints — becomes the effective agent. | [[2023-karpathy-intro-large-language-models]] | 2023-11-22 | current | 0.5 | false |
