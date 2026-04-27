---
type: pitfalls
title: AI Governance and Policy — Pitfalls
created: 2026-04-27
updated: 2026-04-27
parent_entity: [[topics/ai-governance-policy]]
parent_type: topic
status: current
failure_mode_count: 5
teaching_relevance: true
competency_domains:
  - output-verification-and-risk-assessment
  - ai-integration-in-organizational-workflows
professional_contexts:
  - domestic-civil-service-and-public-administration
contributing_sources:
  - [[2025-responsible-ai-public-evaluation]]
  - [[2025-ibm-government-ai-era]]
---

## Technical Limitations

### Data readiness gap constrains AI value realization in government
**Status:** active
**Source:** [[2025-ibm-government-ai-era]]

As of 2025, only approximately 7% of government enterprise data is actively used by AI systems, despite leaders estimating 50–80% of their data could be valuable if properly prepared. The constraint is structural: fragmented legacy systems, inconsistent data standards, and siloed databases across agencies prevent AI from accessing the information needed to perform intended functions. Investment in data management and governance is a prerequisite for AI capability, not a parallel track. The IBM IBV survey found that leaders indicate less than one-quarter of their organizational data is AI-ready today, meaning the full organizational value of AI remains largely unrealized regardless of model capability or budget allocation.

### Workforce and governance expertise gap
**Status:** active
**Source:** [[2025-ibm-government-ai-era]]

62% of government technology leaders identify workforce and talent development as the most critical gap for advancing AI maturity, followed by 55% citing ethical, legal, and regulatory frameworks. AI systems deployed without practitioners who can govern, deploy, and explain them responsibly create accountability vacuums that are difficult to address retroactively. This gap is especially acute at local government level, where leaders face the highest pressure to satisfy algorithmic transparency and fairness requirements while having the fewest dedicated technical resources.

## Usage Antipatterns

### AI hype and anthropomorphization leading to misplaced trust
**Status:** active
**Source:** [[2025-responsible-ai-public-evaluation]]

Treating AI as inherently intelligent, autonomous, or unbiased leads to misplaced trust and potentially harmful public sector implementations. AI outputs are shaped by training data and algorithmic assumptions — overpromising AI capabilities can lead to policy missteps and the delegation of consequential decisions to systems that lack genuine understanding of their implications. Government procurement of AI tools is especially prone to accepting vendor capability claims without independent verification, and the political incentive to demonstrate AI adoption can override appropriate skepticism.

### AI as autonomous decision-maker rather than decision support
**Status:** active
**Source:** [[2025-responsible-ai-public-evaluation]]

Deploying AI as a primary or autonomous decision-maker in government settings — particularly for benefit determinations, grant funding, enforcement, or resource allocation — violates accountability norms and may conflict with statutory requirements for human review. The appropriate model is AI as a decision-support tool that surfaces patterns and evidence for human consideration. RAI-Ev's post hoc design instantiates this principle; prospective AI decision-making in government requires more protective frameworks and, in some agencies, is formally prohibited (NIH and NSF ban AI in grant review on grounds of confidentiality, accuracy, and originality of thought).

## Alignment and Safety Concerns

### Opacity from closed proprietary models undermines democratic accountability
**Status:** active
**Source:** [[2025-responsible-ai-public-evaluation]]

Using closed commercial AI models in government evaluation and decision-making processes without the ability for independent audit, public scrutiny, or reproducibility undermines democratic accountability and the transparency requirements of frameworks such as the Foundations for Evidence-Based Policymaking Act of 2018. Government AI systems must be explainable to stakeholders — including constituents affected by their outputs — and closed models make this difficult or impossible to guarantee. The Blueprint for an AI Bill of Rights principle of "notice and explanation" is structurally unenforceable when the underlying model is a proprietary black box.
