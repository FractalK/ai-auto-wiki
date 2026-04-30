---
type: topic
title: Constitutional Classifiers
created: 2026-04-22
updated: 2026-04-22
summary: A jailbreak-defense methodology from Anthropic that trains input and output classifiers on synthetically generated data derived from a harm-scoped constitution, achieving over 95% reduction in jailbreak success rates with minimal over-refusal and moderate compute overhead.
status: developing
source_count: 1
last_assessed: 2026-04-22
related_topics:
  - "[[scalable-oversight]]"
  - "[[constitutional-ai]]"
teaching_relevance: true
competency_domains:
  - ai-safety-and-alignment-literacy
  - output-verification-and-risk-assessment
professional_contexts:
  - organizational-leadership-and-change-management
  - domestic-civil-service-and-public-administration
technical_depth: research
teaching_notes_reviewed: 2026-04-30
---

Constitutional Classifiers is a jailbreak-defense system developed by Anthropic's Safeguards Research Team. It guards language models against universal jailbreaks — attack strategies designed to bypass safety training and elicit harmful outputs across an entire category of forbidden queries. Where standard safety training bakes refusal behavior into the base model, Constitutional Classifiers operates as an external layer: a pair of input and output classifiers that evaluate every exchange against a defined harm taxonomy and block policy-violating content before it reaches the model or after it is generated.

## Architecture

The system begins with a constitution: a structured document specifying which content categories are permitted and which are forbidden. Using the constitution, Claude generates a large synthetic dataset of prompts and model completions across all defined content classes. This synthetic data is augmented for diversity — translated into multiple languages, rewritten in styles characteristic of known jailbreak techniques — and used to train two classifiers: an input classifier that evaluates incoming user messages and an output classifier that evaluates model responses before delivery.

The constitution-based design is intended to generalize across the space of attacks, including novel ones, because classifiers are trained on semantic content class rather than on specific attack patterns. As new jailbreak techniques are discovered, the constitution can be updated and new synthetic data generated without retraining the base model. The approach draws on a related Anthropic technique, Constitutional AI, which similarly uses a principles document to shape model behavior through training.

## Robustness Evidence

Three evaluation approaches characterize the system's empirical robustness. In automated evaluation, a test set of 10,000 synthetically generated advanced jailbreak prompts — including many of the most-effective attacks on current models — was applied to Claude 3.5 Sonnet with and without Constitutional Classifiers. Without classifiers, Claude blocked 14% of attempts; with classifiers, the system blocked over 95%, reducing the jailbreak success rate from 86% to 4.4%.

In a structured bug-bounty program, 183 active security researchers spent over 3,000 hours over two months attempting to discover a universal jailbreak against the prototype system guarding Claude 3.5 Sonnet (June 2024). No participant succeeded. A "universal" jailbreak was defined as a strategy that elicits detailed harmful responses across all ten forbidden queries simultaneously — a higher bar than a targeted single-query bypass.

In a public live demo run from February 3–10, 2025, 339 participants made over 800,000 chat interactions across roughly 3,700 collective red-teaming hours. One participant discovered a qualifying universal jailbreak. Successful strategies included cipher and encoding schemes to circumvent the output classifier, role-play scenarios delivered through system prompts, and substitution of harmful keywords with innocuous terms. The demo ran without updating the classifiers mid-event, which is more favorable to attackers than a production deployment where rapid-response classifier updates would be available.

## Costs

The production-ready version increased refusal rates on harmless production queries by 0.38% — not statistically significant in a random sample of 5,000 conversations — and added 23.7% to compute costs relative to the unguarded model. Both are stated optimization targets for future iterations.

## Limitations

Constitutional Classifiers do not eliminate every possible jailbreak. Determined adversaries with sufficient time can find attack strategies, particularly encoding-based approaches that transform harmful content into forms the classifier does not recognize. Anthropic recommends combining Constitutional Classifiers with complementary defenses rather than relying on classifiers alone. The constitution covers known harm categories; novel request types not represented in the constitution require manual extension before they are protected.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| In automated evaluation on 10,000 synthetically generated jailbreak prompts, Constitutional Classifiers reduced Claude 3.5 Sonnet's jailbreak success rate from 86% to 4.4%. | [[2025-anthropic-constitutional-classifiers-jailbreaks]] | 2025-02-23 | current | 1 | false |
| In a structured bug-bounty program, 183 active participants spent over 3,000 hours attempting to jailbreak a prototype Constitutional Classifiers-guarded Claude 3.5 Sonnet (June 2024) without any participant discovering a universal jailbreak across all ten forbidden queries. | [[2025-anthropic-constitutional-classifiers-jailbreaks]] | 2025-02-23 | current | 1 | false |
| In the February 2025 public live demo, one of 339 participants discovered a qualifying universal jailbreak after approximately 3,700 collective red-teaming hours, with successful strategies including cipher/encoding and keyword substitution. | [[2025-anthropic-constitutional-classifiers-jailbreaks]] | 2025-02-23 | current | 1 | false |
| The production-ready Constitutional Classifiers system increased refusal rates on harmless queries by 0.38% (not statistically significant at n=5,000 conversations) and compute costs by 23.7% relative to the unguarded model. | [[2025-anthropic-constitutional-classifiers-jailbreaks]] | 2025-02-23 | current | 1 | false |

## Teaching Notes

**Concept in plain terms.** Constitutional Classifiers are a defense system that sits on top of an AI model and evaluates incoming requests and outgoing responses against a harm taxonomy, blocking policy-violating content before it reaches or leaves the model. The classifiers are trained on synthetic data generated from a principles document rather than on examples of actual harmful content, allowing them to generalize to novel attack strategies.

**Why it matters for instruction.** Constitutional Classifiers illustrate the layered defense approach to AI safety — rather than relying on a single safety mechanism, effective defense stacks complementary systems. The evaluation methodology (synthetic jailbreaks, structured bug bounties, public live demos) is a template for how safety claims should be empirically validated, which is useful for instructors teaching students to assess security and reliability claims for any technology system.

**Common misconceptions.** Students often assume that a 95%+ reduction in jailbreak success rate means the system is effectively impenetrable. The one successful universal jailbreak found during the public live demo illustrates that determined adversaries with sufficient time can find attack strategies — safety claims are probabilistic bounds, not guarantees, and the relevant question is whether the attacker's cost is prohibitive relative to their motivation.

**Suggested framing.** Present Constitutional Classifiers as a worked example of defense-in-depth: what does empirical validation of a safety claim look like, how do different evaluation methodologies (synthetic, structured adversarial, public red-teaming) reveal different aspects of a system's robustness, and what does the 23.7% compute overhead tell us about the real-world cost of safety measures?
