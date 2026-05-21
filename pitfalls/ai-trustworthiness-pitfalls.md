---
type: pitfalls
title: AI Trustworthiness Pitfalls
created: 2026-05-21
updated: 2026-05-21
parent_entity: "[[topics/ai-trustworthiness]]"
parent_type: topic
status: current
failure_mode_count: 7
contributing_sources:
  - "[[2024-afroogh-trust-ai-review]]"
---

## Technical Limitations

### Accuracy-Explainability Tradeoff
**Status:** active<br>
**Source:** [[2024-afroogh-trust-ai-review]]

High-accuracy AI models — particularly deep neural networks — are structurally less explainable than lower-accuracy interpretable models such as decision trees. Current Explainable AI (XAI) methods mitigate but do not eliminate this tradeoff; they add approximate local or global explanations to black-box models without restoring the causal transparency of simpler architectures. For high-stakes domains (healthcare, legal, financial) where both accuracy and explainability are required, this constraint forces a design tradeoff that cannot be optimized away with existing tools.

### Trust Calibration Failure
**Status:** active<br>
**Source:** [[2024-afroogh-trust-ai-review]]

Users systematically develop over-trust or under-trust in AI systems because perceived trustworthiness is formed from observable cues — interface quality, institutional endorsement, system confidence displays — rather than direct assessment of actual performance. Over-trust emerges when non-technical cues (good GUI, reputable vendor, fluent output) signal higher accuracy than the system achieves; under-trust emerges when lack of familiarity or opacity suppresses use of a genuinely accurate system. Adaptive trust calibration requires transparency mechanisms that connect observable output quality to measured performance, but most deployed systems do not provide this feedback.

## Usage Antipatterns

### Trust-Trustworthiness Conflation
**Status:** active<br>
**Source:** [[2024-afroogh-trust-ai-review]]

Treating the goals of building trust (user adoption, positive perception) and building trustworthiness (accuracy, safety, robustness) as identical, leading to misallocated effort. An organization that invests in polished documentation, compliance statements, and UI improvements expecting to produce a more reliable system, or that invests in model accuracy improvements expecting to produce higher user adoption, will be wrong in both cases. Trust and trustworthiness are entirely disentangled and require distinct improvement strategies.

### Context-Agnostic Transparency Provision
**Status:** active<br>
**Source:** [[2024-afroogh-trust-ai-review]]

Providing uniform transparency to all stakeholder classes rather than calibrating to different needs and cognitive loads. Developers need access to model internals, training data characteristics, and uncertainty metrics. Regulators need audit trails and compliance documentation. End users need task-specific justifications at the moment of decision. Providing excessive technical detail to end users reduces their trust rather than increasing it — behavioral research shows that too much transparency confuses users and degrades their confidence. Providing only high-level explanations to technical auditors fails to satisfy regulatory accountability requirements.

### Ethics-Washing
**Status:** active<br>
**Source:** [[2024-afroogh-trust-ai-review]]

Overstating ethical principles, safety claims, and trustworthiness commitments in marketing and public communications to preempt regulatory scrutiny, without aligning actual system behavior to those claims. When users eventually perceive the gap between stated ethical commitments and observed system behavior, trust damage is often more severe than it would have been without the prior claims. Ethics-washing also devalues legitimate trustworthiness certifications and governance frameworks by associating them with performative compliance rather than substantive accountability.

## Alignment and Safety Concerns

### Trust Equity Neglect
**Status:** active<br>
**Source:** [[2024-afroogh-trust-ai-review]]

Evaluating AI trust and adoption as aggregate population averages without disaggregating across demographic groups. Trust in AI is unevenly distributed: in healthcare, trust in AI diagnostics is higher than trust in female physicians for some populations but not higher than trust in male physicians, meaning AI adoption may disproportionately displace female doctors. In criminal justice, judges and lawyers who over-trust algorithmic recidivism scores cause differential harm to defendants from groups overrepresented in biased training data. Systems that achieve the "trusted" threshold on aggregate surveys can still embed and amplify systematic inequities through differential trust distributions.

### AI Accountability Gap
**Status:** active<br>
**Source:** [[2024-afroogh-trust-ai-review]]

Failing to develop direct accountability structures for AI systems on the grounds that AI lacks legal personhood and cannot be held responsible in the way human agents can. Without a clear theory of how accountability distributes among creators, deployers, and users, no party accepts full responsibility for outcomes. This creates a perverse incentive for each actor to point to the others when AI-driven decisions cause harm. The development of a robust framework that aligns explanation requirements, accountability obligations, and enforcement mechanisms at the level of human and organizational agents is an open governance challenge that current legal systems have not resolved.
