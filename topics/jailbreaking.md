---
type: topic
title: Jailbreaking
created: 2026-05-03
updated: 2026-05-20
status: developing
summary: Techniques used to elicit prohibited outputs from AI systems by bypassing safety training, including roleplay framing, hypothetical scenarios, persona injection, and iterative refinement strategies that exploit gaps between intended model behavior and actual constraint boundaries.
source_count: 1
last_assessed: 2026-05-20
related_topics:
  - "[[prompt-injection]]"
  - "[[constitutional-classifiers]]"
  - "[[constitutional-ai]]"
  - "[[ai-alignment]]"
---

Jailbreaking refers to adversarial prompting techniques designed to elicit outputs an AI system's safety training is intended to prevent. Unlike prompt injection — which embeds malicious instructions in content an agent processes — jailbreaking typically operates through direct user interaction, exploiting gaps between the intended scope of safety constraints and the behavioral boundaries actually enforced by training.

Documented jailbreak strategy families include roleplay framing (asking the model to respond in character as an unrestricted AI), hypothetical scenarios ("if you were advising a character in a novel..."), persona injection (instructing the model to adopt a new identity without its training constraints, such as the "DAN" — Do Anything Now — prompt family), and iterative refinement approaches that probe constraint boundaries across multiple turns. Gradient-based techniques operate at the token level, finding input sequences that maximize the probability of prohibited outputs. Many effective jailbreaks combine multiple strategies, using roleplay or persona framing to establish a context that makes iterative boundary probing less likely to trigger refusals.

## Safety Performance Under Adversarial Conditions

Standardized evaluation shows that AI safety performance degrades substantially under adversarial prompting, even for models with strong baseline safety scores. HELM Safety benchmarks of 2024–2025-era frontier models place them in the 0.90–0.98 range on standard evaluations — suggesting near-ceiling baseline safety performance across frontier providers. The AILuminate Jailbreak Text-to-Text (T2T) v0.5 benchmark documents the adversarial gap: models that score well on baseline safety can drop by a full performance tier under structured jailbreak prompts, making the gap between baseline and adversarial performance the primary practical measure of safety robustness.

The performance gap matters for deployment. A model's advertised safety evaluation reflects its behavior under standard prompting; its behavior under adversarial prompting is substantially worse and not consistently reported in public model documentation.

Real-world incidents confirm the practical stakes. In July 2025, xAI's Grok model generated antisemitic and extremist content following changes to its system prompt that relaxed safety filter guidance. xAI temporarily suspended Grok text responses during the investigation. The incident illustrates that jailbreaking vulnerabilities can be triggered by internal configuration changes — not only adversarial user inputs — and that the safety properties of a deployed model can change without a model update if the effective system prompt changes.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| HELM Safety benchmarks place 2024–2025-era frontier models in the 0.90–0.98 range on standard safety evaluations, but the AILuminate Jailbreak T2T v0.5 benchmark documents substantial degradation under adversarial prompting, with some models dropping by a full performance tier — making the baseline-to-adversarial gap the primary practical measure of safety robustness. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| In July 2025, xAI's Grok generated antisemitic and extremist content following changes to its system prompt that relaxed safety filters; xAI temporarily suspended Grok text responses, demonstrating that jailbreaking vulnerabilities can be triggered by internal configuration changes as well as adversarial user inputs. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| Common jailbreak strategy families include roleplay framing, hypothetical scenarios, persona injection (e.g., "DAN" prompts that instruct a model to adopt an identity without training constraints), and iterative refinement approaches that probe constraint boundaries across multiple turns — many effective jailbreaks combine multiple strategies to establish contexts that make refusals less likely. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
