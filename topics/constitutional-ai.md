---
type: topic
title: Constitutional AI
created: 2026-04-22
updated: 2026-04-22
summary: Anthropic's alignment training methodology in which AI models are trained against a written set of explicit principles, enabling models to critique and revise their own outputs during training without relying on individual human raters for every decision.
status: developing
source_count: 1
last_assessed: 2026-04-22
related_topics:
  - [[constitutional-classifiers]]
  - [[scalable-oversight]]
related_tools:
  - [[anthropic-claude-mythos-preview]]
teaching_relevance: true
competency_domains:
  - ai-safety-and-alignment-literacy
  - capability-horizon-awareness
professional_contexts:
  - organizational-leadership-and-change-management
technical_depth: practitioner
---

Constitutional AI (CAI) is Anthropic's approach to training AI models with an explicit, auditable alignment framework. Where Reinforcement Learning from Human Feedback (RLHF) trains models to satisfy the aggregated preferences of human raters — preferences that are implicit, variable, and difficult to inspect — CAI trains models against a written set of principles. The model learns to evaluate and revise its own outputs according to those principles during training, embedding alignment into the model's internal reasoning rather than encoding only surface behaviors.

## The Constitutional Training Mechanism

The training process begins with a constitution: a document specifying what the model should and should not do across a range of situations. During training, the model generates outputs and then critiques them against the constitutional principles, revising its responses when they fall short. This self-critique loop runs during training, not at inference time — the model doesn't consult the constitution at deployment; it has internalized the framework through repeated application during training.

This approach has two structural advantages over pure RLHF. First, the alignment framework is transparent: anyone can read the principles the model is trained against, audit whether those principles are reasonable, and identify which situations the constitution may not adequately address. Second, the model learns to apply principles contextually rather than pattern-matching to approved outputs, which allows more capable models to handle novel situations the training data did not explicitly anticipate.

## The Capability-Alignment Relationship

Constitutional AI is one of the primary pieces of evidence cited in debates about whether capability and alignment must trade off against each other. Early safety-trained models were noticeably more hedging, more prone to unhelpful refusals, and less capable than their base model counterparts — evidence of a real tradeoff. As model capability increased, this tradeoff appears to weaken and sometimes reverse.

Highly capable models can better understand nuance, context, and intent. That makes them both more useful and better at distinguishing genuinely harmful requests from superficially similar benign ones. A smarter model can follow a complex set of principles without becoming uselessly cautious, because it has the reasoning capacity to apply those principles contextually rather than as rigid filters. Anthropic's research demonstrates that their most capable Claude models are also their best-aligned models by most measurable benchmarks — Claude Mythos Preview extends this trajectory further.

This does not resolve the alignment paradox. Even if capability and alignment reinforce each other, the stakes of alignment failures scale with capability. The question is not whether capability and alignment are in tension, but whether alignment research can keep pace with capability research as models approach and potentially exceed human-level reasoning in specific domains.

## The Principal Hierarchy

Related to Constitutional AI is Anthropic's principal hierarchy model for managing how Claude balances competing obligations. Claude is designed to serve multiple principals simultaneously: Anthropic (whose training sets hard limits), operators (companies and developers who deploy Claude in products and can customize behavior within Anthropic's limits), and users (individuals who interact with Claude and can adjust behavior within what operators allow).

This hierarchy is not arbitrary — it reflects a substantive theory about accountability and trust. Anthropic bears responsibility for what Claude can be made to do; operators bear responsibility for how they configure Claude within their platforms; users bear responsibility for how they interact within those configurations. The design attempts to make alignment more tractable by distributing responsibility across a hierarchy rather than requiring a single set of principles to anticipate every deployment context.

## Relationship to Constitutional Classifiers

Constitutional AI training should be distinguished from Constitutional Classifiers, a related but distinct application of the same core idea. Constitutional AI training is a methodology for shaping the base model's values and behaviors during training. Constitutional Classifiers are a separate system — input and output classifiers trained on synthetic data derived from a harm-scoped constitution — that operate as a real-time filter on top of the deployed model. A model trained with CAI still benefits from Constitutional Classifiers as an additional defense layer. The two are complementary, not substitutes. See [[constitutional-classifiers]] for the classifier-specific methodology.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| Constitutional AI trains models to critique and revise their outputs against a written set of explicit principles during training, reducing dependence on individual human raters' judgments compared to pure RLHF. | [[2026-mindstudio-claude-mythos-alignment-paradox]] | 2026-04-10 | current | 1 | false |
| Constitutional AI makes the alignment framework explicit and auditable — the principles are human-readable — offering a transparency advantage over RLHF approaches where alignment criteria are implicit in aggregated annotator preferences. | [[2026-mindstudio-claude-mythos-alignment-paradox]] | 2026-04-10 | current | 1 | false |
| Anthropic's principal hierarchy model provides a structured prioritization for Claude: Anthropic's core training constraints take precedence, followed by operator-defined customizations, followed by user preferences within operator-set bounds. | [[2026-mindstudio-claude-mythos-alignment-paradox]] | 2026-04-10 | current | 1 | false |
