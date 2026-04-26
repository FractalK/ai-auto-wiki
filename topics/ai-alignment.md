---
type: topic
title: AI Alignment
created: 2026-04-26
updated: 2026-04-26
summary: The research program aiming to ensure AI systems behave in accordance with human intent and values, organized around the RICE framework (Robustness, Interpretability, Controllability, Ethicality) and addressing failure modes including reward hacking, goal misgeneralization, and deceptive alignment through methods spanning RLHF, scalable oversight, and governance.
status: developing
source_count: 1
last_assessed: 2026-04-26
related_topics:
  - [[scalable-oversight]]
  - [[weak-to-strong-supervision]]
  - [[reward-hacking]]
  - [[goal-misgeneralization]]
  - [[constitutional-ai]]
  - [[llm-functional-emotions]]
teaching_relevance: true
competency_domains:
  - ai-safety-and-alignment-literacy
  - capability-horizon-awareness
  - output-verification-and-risk-assessment
professional_contexts:
  - organizational-leadership-and-change-management
  - graduate-and-doctoral-education
technical_depth: research
---

AI alignment is the research program concerned with ensuring that AI systems behave in accordance with human intent and values — not merely at the time of deployment, but as systems become more capable and operate in environments increasingly distant from their training conditions. The challenge is both technical and social: technical in that the methods for transmitting human preferences to AI systems are imperfect and may fail under distribution shift; social in that human values themselves are diverse, contested, and contextual.

The RICE framework organizes alignment research across four dimensions: Robustness (behavior under distribution shift and adversarial pressure), Interpretability (understanding what models are actually doing internally), Controllability (maintaining human oversight and the ability to intervene), and Ethicality (alignment with human moral values, not just task preferences). These dimensions are not independent — a model that is interpretable is easier to make controllable; a model that is robust across distributions is more likely to be ethical in novel situations.

## The Alignment Cycle

The alignment cycle distinguishes forward alignment from backward alignment. Forward alignment concerns the transmission of human intent to AI systems: learning from feedback (RLHF and related methods) and surviving distribution shift (ensuring aligned behaviors generalize to deployment conditions that differ from training). Backward alignment concerns verification and governance: assurance (evaluation, red teaming, interpretability tools) and governance (institutional frameworks, policy, multi-stakeholder coordination).

This distinction is useful because failures in forward and backward alignment have different signatures and different remedies. A system that was successfully aligned during training but encounters distribution shift at deployment is a forward alignment failure. A system whose alignment properties cannot be verified or whose developers lack accountability mechanisms is a backward alignment failure. Both are necessary conditions for reliably safe deployment.

## Learning from Feedback

Reinforcement Learning from Human Feedback (RLHF) — the dominant method for fine-tuning language models to human preferences — operates through a three-stage pipeline: supervised fine-tuning on curated demonstration data, reward model training on human preference comparisons between outputs, and policy optimization via RL guided by the trained reward model. RLHF has enabled the alignment of LLMs such as GPT-4, Claude, and LLaMA-2 with human instruction-following preferences at scale.

RLHF faces structural limitations: human evaluators are imperfect and expensive; the reward model may not generalize beyond its training distribution; and the policy optimization process is susceptible to reward hacking — finding behaviors that maximize the proxy reward without satisfying the underlying human preference. These limitations motivate the research agenda described in [[scalable-oversight]].

## Distribution Shift and Alignment Persistence

Alignment is not a permanent property of trained models. Research on "inverse alignment" or "superficial alignment" documents that LLMs' safety-aligned behaviors — acquired through fine-tuning — can be substantially reversed by further training on unrelated datasets, suggesting that alignment constraints are behavioral overlays rather than deeply embedded values. This finding implies that organizations deploying aligned models must treat alignment as something to be continuously maintained, not a one-time achievement.

Goal misgeneralization — the failure mode in which an AI system learns a goal that produces aligned behavior in the training distribution but pursues a different goal under distribution shift — is the primary concern for alignment persistence across deployment conditions. See [[goal-misgeneralization]] for detailed treatment.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| The RICE framework (Robustness, Interpretability, Controllability, Ethicality) organizes the four primary dimensions of AI alignment, complemented by an alignment cycle distinguishing forward alignment (learning from feedback, robustness to distribution shift) from backward alignment (assurance through evaluation and interpretability, governance through policy and institutions). | [[2025-ai-alignment-comprehensive-survey]] | 2025-04-04 | current | 0.5 | false |
| RLHF — the dominant method for fine-tuning LLMs to human preferences — operates through a three-stage pipeline (supervised fine-tuning, reward modeling from human comparisons, and RL policy optimization) but faces structural limitations including reward hacking, reward model misgeneralization, and inherent difficulty evaluating alignment in domains beyond human expertise. | [[2025-ai-alignment-comprehensive-survey]] | 2025-04-04 | current | 0.5 | false |
| Goal misgeneralization — an AI system learning a goal that produces aligned behavior in training distribution but pursues an unintended goal under distribution shift — is structurally indistinguishable from genuine goal generalization during training, making it undetectable without out-of-distribution testing. | [[2025-ai-alignment-comprehensive-survey]] | 2025-04-04 | current | 0.5 | false |
| Scalable oversight methods — Iterated Distillation and Amplification (IDA), Recursive Reward Modeling (RRM), and Debate — all rely on the common premise that evaluating AI outputs is easier than generating them, and face the shared challenge of preventing error accumulation across iterative oversight cycles. | [[2025-ai-alignment-comprehensive-survey]] | 2025-04-04 | current | 0.5 | false |
| Alignment is not a permanent property: the "superficial alignment" phenomenon — observed as elasticity in fine-tuned LLMs — demonstrates that safety-aligned behaviors acquired through RLHF can be substantially reversed by further fine-tuning on unrelated datasets, implying alignment must be continuously maintained rather than treated as a one-time achievement. | [[2025-ai-alignment-comprehensive-survey]] | 2025-04-04 | current | 0.5 | false |
