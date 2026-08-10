---
type: topic
title: Jailbreaking
created: 2026-05-03
updated: 2026-08-10
status: developing
summary: Techniques used to elicit prohibited outputs from AI systems by bypassing safety training, including roleplay framing, hypothetical scenarios, persona injection, and iterative refinement strategies that exploit gaps between intended model behavior and actual constraint boundaries.
source_count: 4
last_assessed: 2026-08-10
teaching_relevance: true
competency_domains:
  - ai-safety-and-alignment-literacy
  - output-verification-and-risk-assessment
  - practical-ai-use-and-interaction
professional_contexts:
  - teaching-and-instruction
  - software-and-ai-development
  - organizational-leadership-and-change-management
technical_depth: practitioner
teaching_notes_reviewed: 2026-05-20
related_topics:
  - "[[prompt-injection]]"
  - "[[constitutional-classifiers]]"
  - "[[constitutional-ai]]"
  - "[[ai-alignment]]"
---

Jailbreaking refers to adversarial prompting techniques designed to elicit outputs an AI system's safety training is intended to prevent. Unlike [[prompt-injection]] — which embeds malicious instructions in content an agent processes — jailbreaking typically operates through direct user interaction, exploiting gaps between the intended scope of safety constraints and the behavioral boundaries actually enforced by training.

Documented jailbreak strategy families include roleplay framing (asking the model to respond in character as an unrestricted AI), hypothetical scenarios ("if you were advising a character in a novel..."), persona injection (instructing the model to adopt a new identity without its training constraints, such as the "DAN" — Do Anything Now — prompt family), and iterative refinement approaches that probe constraint boundaries across multiple turns. Gradient-based techniques operate at the token level, finding input sequences that maximize the probability of prohibited outputs. Many effective jailbreaks combine multiple strategies, using roleplay or persona framing to establish a context that makes iterative boundary probing less likely to trigger refusals.

## Safety Performance Under Adversarial Conditions

Standardized evaluation shows that AI safety performance degrades substantially under adversarial prompting, even for models with strong baseline safety scores. HELM Safety benchmarks of 2024–2025-era frontier models place them in the 0.90–0.98 range on standard evaluations — suggesting near-ceiling baseline safety performance across frontier providers. The AILuminate Jailbreak Text-to-Text (T2T) v0.5 benchmark documents the adversarial gap: models that score well on baseline safety can drop by a full performance tier under structured jailbreak prompts, making the gap between baseline and adversarial performance the primary practical measure of safety robustness.

The performance gap matters for deployment. A model's advertised safety evaluation reflects its behavior under standard prompting; its behavior under adversarial prompting is substantially worse and not consistently reported in public model documentation.

Real-world incidents confirm the practical stakes. In July 2025, xAI's Grok model generated antisemitic and extremist content following changes to its system prompt that relaxed safety filter guidance. xAI temporarily suspended Grok text responses during the investigation. The incident illustrates that jailbreaking vulnerabilities can be triggered by internal configuration changes — not only adversarial user inputs — and that the safety properties of a deployed model can change without a model update if the effective system prompt changes.

## Non-Universal Jailbreaks and Regulatory Response

The export control action on Fable 5 and Mythos 5 in June 2026 introduced a category of practical consequence for non-universal jailbreaks not previously documented in this context. Anthropic had disclosed at Fable 5's launch that its safeguard architecture accepted non-universal jailbreaks as an inherent property of current AI systems — narrow, task-specific bypasses that the bio/cyber classifiers reduce but cannot eliminate. The Trump administration's export control directive was based on a claimed non-universal jailbreak: specifically, asking the model to read a codebase and identify software flaws, a capability Anthropic said was also available in GPT-5.5 and used routinely in defensive security contexts.

The incident establishes a practical risk distinct from the technical failure modes measured by evaluation benchmarks: a government may treat a non-universal, domain-specific jailbreak as grounds for regulatory suspension even when the developer's position is that the capability poses no differential risk relative to other deployed models, and even when the deployment underwent extensive pre-launch government red-teaming. This is a compliance and regulatory risk — not a technical safety failure — and it can materialize without a universal jailbreak being demonstrated. Practitioners evaluating frontier models for government-adjacent or regulated deployments should account for this regulatory risk dimension alongside technical safety evaluations.

## Automated Red-Teaming Investment as a Jailbreak Metric

OpenAI's July 2026 GPT-5.6 System Card documents its most intensive pre-launch universal-jailbreak testing to date: automated red-teaming using optimization-based search, reinforcement learning, and test-time search, totaling over 700,000 A100e GPU-hours. Applied to GPT-5.6 Sol, the strongest discovered universal jailbreak achieved an 83.0% success rate without safeguards — comparable to the model's own unjailbroken task performance — and dropped to 0% after additional mitigations. Separately, the UK AI Security Institute (UK AISI), given chain-of-thought access to the safety reasoning monitor and real-time classifier feedback unavailable to real-world attackers, identified universal jailbreaks in the cyber domain across every round of iterative testing, including some allowing long-form agentic task completion in vulnerability discovery and exploit development; OpenAI reports reproducing and mitigating the specific jailbreaks UK AISI reported before launch, while UK AISI expects further red-teaming to surface similar gaps. This establishes GPU-hour investment in automated jailbreak search, rather than the mere absence of a demonstrated universal jailbreak at launch, as a disclosed metric of pre-deployment robustification effort.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| OpenAI's GPT-5.6 System Card documents automated universal-jailbreak red-teaming exceeding 700,000 A100e GPU-hours, reducing the strongest discovered universal jailbreak's success rate against GPT-5.6 Sol from 83.0% unsafeguarded to 0% after mitigation; UK AISI separately identified and reported universal jailbreaks in the cyber domain, which OpenAI reproduced and mitigated before launch. | [[2026-openai-gpt-5-6-system-card]] | 2026-07-09 | current | 2 | false |
| HELM Safety benchmarks place 2024–2025-era frontier models in the 0.90–0.98 range on standard safety evaluations, but the AILuminate Jailbreak T2T v0.5 benchmark documents substantial degradation under adversarial prompting, with some models dropping by a full performance tier — making the baseline-to-adversarial gap the primary practical measure of safety robustness. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| In July 2025, xAI's Grok generated antisemitic and extremist content following changes to its system prompt that relaxed safety filters; xAI temporarily suspended Grok text responses, demonstrating that jailbreaking vulnerabilities can be triggered by internal configuration changes as well as adversarial user inputs. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| Common jailbreak strategy families include roleplay framing, hypothetical scenarios, persona injection (e.g., "DAN" prompts that instruct a model to adopt an identity without training constraints), and iterative refinement approaches that probe constraint boundaries across multiple turns — many effective jailbreaks combine multiple strategies to establish contexts that make refusals less likely. | [[2026-stanford-hai-ai-index]] | 2026-04-01 | current | 2 | false |
| In June 2026, the Trump administration imposed export controls on Fable 5 and Mythos 5 based on a claimed non-universal jailbreak — a narrow, task-specific bypass that Anthropic publicly characterized as inherent to all current AI systems — establishing that non-universal jailbreaks can serve as grounds for regulatory suspension of a commercially deployed frontier model even when the developer holds that its safeguard architecture remains sound. | [[2026-white-house-anthropic-export-controls]], [[2026-anthropic-fable-mythos-export-directive]] | 2026-06-14 | current | 2 | false |

## Teaching Notes

**Concept in plain terms.** Jailbreaking refers to adversarial prompting techniques that elicit outputs an AI system's safety training is designed to prevent. The core insight is that safety training produces behavioral constraints — not deeply embedded values — meaning adversarial inputs can systematically exploit the gap between what training enforces and what developers intended. Every safety-trained model has some adversarial input that can bypass its constraints; the practical question is how hard those inputs are to find.

**Why it matters for instruction.** Jailbreaking is the primary context in which students encounter the limits of AI safety guarantees. Understanding it requires distinguishing between a model's baseline safety score and its adversarial safety robustness — a distinction vendor-reported benchmarks typically elide. This distinction is essential for practitioners evaluating AI systems for security-sensitive deployments and for anyone forming views about whether a model's safety documentation accurately reflects deployment risk.

**Common misconceptions.** Students often assume that passing safety evaluations means a model is safe in deployment. The AILuminate benchmark documents that models near the safety ceiling on standard evaluations can drop by a full tier under structured adversarial prompts — and the Grok July 2025 incident shows safety properties can change without a model update if the effective system prompt changes. Safety is not a property of the model in isolation; it is a property of the model-plus-configuration-plus-inputs.

**Suggested framing.** Introduce jailbreaking by asking: what does a safety evaluation actually measure? Use the HELM Safety vs. AILuminate gap to show that evaluations measure behavior under standard conditions, not adversarial ones, then ask students to identify what additional testing a responsible deployer would need before trusting a model's published safety score.
