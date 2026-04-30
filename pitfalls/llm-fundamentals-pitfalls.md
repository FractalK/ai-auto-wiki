---
type: pitfalls
title: LLM Fundamentals Pitfalls
created: 2026-04-26
updated: 2026-04-30
parent_entity: "[[topics/llm-fundamentals]]"
parent_type: topic
status: current
failure_mode_count: 7
teaching_relevance: true
competency_domains:
  - output-verification-and-risk-assessment
  - practical-ai-use-and-interaction
professional_contexts:
  - teaching-and-instruction
  - organizational-leadership-and-change-management
  - professional-and-continuing-education
contributing_sources:
  - "[[2023-karpathy-intro-large-language-models]]"
  - "[[2026-google-prompt-injection-wild]]"
teaching_notes_reviewed: 2026-04-30
---

## Technical Limitations

### System 1 Reasoning Ceiling
**Status:** active<br>
**Source:** [[2023-karpathy-intro-large-language-models]]

LLMs generate responses through a single forward pass with no mechanism for deliberate search, backtracking, or work verification. Tasks requiring extended proof construction, precise arithmetic, or long-horizon planning expose this ceiling: the model produces a plausible-sounding completion rather than a verified result. Users relying on LLM outputs for complex reasoning chains without independent verification are operating outside the model's reliable performance envelope.

### Context Window Amnesia
**Status:** active<br>
**Source:** [[2023-karpathy-intro-large-language-models]]

LLMs have no persistent memory across context windows. Each conversation starts from a blank state unless external memory is explicitly architected into the deployment. For workflows that depend on accumulated context — multi-session projects, longitudinal case management, ongoing knowledge synthesis — relying on the model's in-session state without external persistence creates silent information loss.

### Base Model vs. Fine-Tuned Model Confusion
**Status:** active<br>
**Source:** [[2023-karpathy-intro-large-language-models]]

Base models (pretrained but not instruction-tuned) are not assistants and have no safety constraints. Deploying base models without fine-tuning safety layers exposes raw pretraining behavior. Separately, users and developers who believe fine-tuned safety behavior is a deep architectural property rather than a behavioral overlay may underestimate the vulnerability surface that jailbreaks exploit.

## Usage Antipatterns

### Treating Outputs as Verified Facts
**Status:** active<br>
**Source:** [[2023-karpathy-intro-large-language-models]]

LLMs produce statistically plausible continuations; they do not retrieve and verify ground truth. Arithmetic errors, outdated factual claims, and hallucinated citations are structural properties of the generation process, not rare edge cases. Workflows that route LLM outputs directly to external systems, documents, or stakeholders without human review at domain-critical points introduce systematic quality risk.

### Unchecked Agentic Tool Use
**Status:** active<br>
**Source:** [[2023-karpathy-intro-large-language-models]]

Giving LLMs access to external tools — web browsing, code execution, file system access, API calls — without human review gates enables cascading errors and opens the pipeline to prompt injection attacks through retrieved content. The LLM-as-OS architecture amplifies what models can accomplish; it also amplifies the blast radius of both model errors and adversarial exploitation.

## Alignment and Safety Concerns

### Jailbreaks Bypassing Fine-Tuned Safety
**Status:** active<br>
**Source:** [[2023-karpathy-intro-large-language-models]]

Jailbreaks use social engineering, fictional framing, or structural manipulation to bypass the behavioral constraints installed during fine-tuning. Because the safety layer is a trained behavioral overlay rather than a hardcoded constraint, sufficiently creative prompts can route around it, restoring access to base model outputs that include no safety conditioning. No complete defensive solution existed as of late 2023, and the attack surface expands with model capability.

### Prompt Injection via External Content
**Status:** active<br>
**Source:** [[2023-karpathy-intro-large-language-models]], [[2026-google-prompt-injection-wild]]

When an LLM agent retrieves and processes external content — web pages, documents, emails — that content may contain adversarial instructions designed to redirect the agent's behavior. Unlike jailbreaks, which require user interaction, prompt injection can occur silently in automated pipelines without the user's knowledge. A 2026 Google Threat Intelligence scan of Common Crawl (2–3 billion web pages) confirmed that indirect prompt injection attempts are actively present on the public web across seven attack categories, with malicious attempts growing 32% between November 2025 and February 2026. The attack surface scales with LLM adoption in agentic workflows and has no comprehensive architectural mitigation. For a dedicated treatment of the attack taxonomy and detection challenges, see [[prompt-injection]]. Cross-cutting: see also [[constitutional-classifiers]] for partial jailbreak mitigations.

## Teaching Notes

**What this failure mode teaches.** LLM fundamentals pitfalls reveal that statistically plausible text and factually accurate text look identical from the outside — there is no surface signal distinguishing a correct LLM output from a confident hallucination. This is not a temporary limitation to be corrected in a future model version; it is a structural property of how these systems generate text. Recognizing this changes how practitioners should design any workflow that incorporates LLM outputs.

**Representative example.** The "treating outputs as verified facts" antipattern is the most broadly applicable classroom case. LLMs predict statistically likely continuations of text; they do not retrieve and verify ground truth before stating it. A user who asks an LLM for a citation, a calculation, or a historical date receives an output that looks exactly like a correct answer — fluent, specific, confidently phrased — whether or not it is accurate. There is no error indicator, no confidence score, and no internal mechanism that prevents the model from producing a plausible-sounding wrong answer. In a workflow where that output routes directly to a document, a client communication, or an automated downstream system without a human review step, systematic quality errors accumulate invisibly. The appropriate practitioner mental model is to treat every LLM output as a draft that requires domain-appropriate verification before use, not as a retrieved fact. The System 1 analogy reinforces this: LLMs are fast, intuitive, and confident by design — they produce their best guess, not a checked answer. Designing workflows to account for this is not a workaround; it is the correct way to use the technology.
