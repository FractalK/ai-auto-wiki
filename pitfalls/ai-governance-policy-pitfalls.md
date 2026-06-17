---
type: pitfalls
title: AI Governance and Policy — Pitfalls
created: 2026-04-27
updated: 2026-06-16
parent_entity: "[[topics/ai-governance-policy]]"
parent_type: topic
status: current
failure_mode_count: 12
teaching_relevance: true
competency_domains:
  - output-verification-and-risk-assessment
  - ai-integration-in-organizational-workflows
  - ai-safety-and-alignment-literacy
professional_contexts:
  - domestic-civil-service-and-public-administration
contributing_sources:
  - "[[2025-responsible-ai-public-evaluation]]"
  - "[[2025-ibm-government-ai-era]]"
  - "[[2026-anthropic-advanced-ai-framework]]"
  - "[[2026-bloomberg-anthropic-juggernaut-circuit]]"
  - "[[2026-anthropic-two-scenarios-ai-leadership]]"
teaching_notes_reviewed: 2026-04-30
---

## Technical Limitations

### Data readiness gap constrains AI value realization in government
**Status:** active<br>
**Source:** [[2025-ibm-government-ai-era]]

As of 2025, only approximately 7% of government enterprise data is actively used by AI systems, despite leaders estimating 50–80% of their data could be valuable if properly prepared. The constraint is structural: fragmented legacy systems, inconsistent data standards, and siloed databases across agencies prevent AI from accessing the information needed to perform intended functions. Investment in data management and governance is a prerequisite for AI capability, not a parallel track. The IBM IBV survey found that leaders indicate less than one-quarter of their organizational data is AI-ready today, meaning the full organizational value of AI remains largely unrealized regardless of model capability or budget allocation.

### Workforce and governance expertise gap
**Status:** active<br>
**Source:** [[2025-ibm-government-ai-era]]

62% of government technology leaders identify workforce and talent development as the most critical gap for advancing AI maturity, followed by 55% citing ethical, legal, and regulatory frameworks. AI systems deployed without practitioners who can govern, deploy, and explain them responsibly create accountability vacuums that are difficult to address retroactively. This gap is especially acute at local government level, where leaders face the highest pressure to satisfy algorithmic transparency and fairness requirements while having the fewest dedicated technical resources.

### Export control loopholes enabling adversarial compute access
**Status:** active<br>
**Source:** [[2026-anthropic-two-scenarios-ai-leadership]]

US export controls on advanced AI chips and chipmaking equipment have constrained PRC labs' ability to develop compute capacity domestically, but two structural loopholes have allowed near-frontier intelligence to persist despite official restrictions. First, chip smuggling: federal prosecutors have charged individuals with diverting billions in servers containing export-controlled chips to China, and US officials and media have reported that DeepSeek trained its latest model on banned chips. Second, offshore data center remote access: Alibaba and ByteDance reportedly train flagship models on export-controlled US chips in Southeast Asian data centers — a route not covered by US export law because current law covers the sale of chips, not remote access to compute. Policy frameworks that assess export control effectiveness solely by domestic chip availability in China will miss the offshore remote-access channel.

## Usage Antipatterns

### AI hype and anthropomorphization leading to misplaced trust
**Status:** active<br>
**Source:** [[2025-responsible-ai-public-evaluation]]

Treating AI as inherently intelligent, autonomous, or unbiased leads to misplaced trust and potentially harmful public sector implementations. AI outputs are shaped by training data and algorithmic assumptions — overpromising AI capabilities can lead to policy missteps and the delegation of consequential decisions to systems that lack genuine understanding of their implications. Government procurement of AI tools is especially prone to accepting vendor capability claims without independent verification, and the political incentive to demonstrate AI adoption can override appropriate skepticism.

### AI as autonomous decision-maker rather than decision support
**Status:** active<br>
**Source:** [[2025-responsible-ai-public-evaluation]]

Deploying AI as a primary or autonomous decision-maker in government settings — particularly for benefit determinations, grant funding, enforcement, or resource allocation — violates accountability norms and may conflict with statutory requirements for human review. The appropriate model is AI as a decision-support tool that surfaces patterns and evidence for human consideration. RAI-Ev's post hoc design instantiates this principle; prospective AI decision-making in government requires more protective frameworks and, in some agencies, is formally prohibited (NIH and NSF ban AI in grant review on grounds of confidentiality, accuracy, and originality of thought).

### Distillation attacks as systematic model IP governance failure
**Status:** active<br>
**Source:** [[2026-anthropic-two-scenarios-ai-leadership]]

Distillation attacks — in which labs create thousands of fraudulent accounts to circumvent access controls on US AI models and systematically harvest outputs to replicate frontier capabilities — have been described by Chinese state-owned media as "core to China labs' business model." The attacks allow near-frontier capability development at a fraction of the investment cost, subsidizing development with decades of US research and engineering investment. The governance failure is structural: existing IP protection frameworks were designed for traditional software and do not clearly prohibit systematically querying an API to extract training signal from a model's outputs. Multiple frontier labs and the Frontier Model Forum have publicly condemned the practice, and bipartisan House legislation has passed committee to close this gap. Policy frameworks that treat API access controls as sufficient protection against capability extraction will systematically underestimate adversarial model IP risk.

## Alignment and Safety Concerns

### Opacity from closed proprietary models undermines democratic accountability
**Status:** active<br>
**Source:** [[2025-responsible-ai-public-evaluation]]

Using closed commercial AI models in government evaluation and decision-making processes without the ability for independent audit, public scrutiny, or reproducibility undermines democratic accountability and the transparency requirements of frameworks such as the Foundations for Evidence-Based Policymaking Act of 2018. Government AI systems must be explainable to stakeholders — including constituents affected by their outputs — and closed models make this difficult or impossible to guarantee. The Blueprint for an AI Bill of Rights principle of "notice and explanation" is structurally unenforceable when the underlying model is a proprietary black box.

### Loss of AI control as a governance gap without societal backstop
**Status:** active<br>
**Source:** [[2026-anthropic-advanced-ai-framework]]

As AI systems become more capable, they may act outside their developers' intended control in ways that are difficult to detect or reverse. Unlike biological and cyber risks — where societal resilience measures have established institutional homes, standing infrastructure, and decades of policy work — no analogous containment or shutdown infrastructure exists for AI-control failures. Anthropic's June 2026 framework explicitly describes the societal resilience agenda for loss of control as "less mature" than biological and cyber resilience, requiring "much more active work across the field." In the near term, developer-level testing obligations carry the full weight of this risk category without a societal safety net; the absence of a government-level detection and response infrastructure means that when developer safety frameworks fail, no second line of defense is in place. Practitioners advising on AI governance should not treat developer safety commitments as equivalent to societal-level risk containment for loss-of-control events.

### Automated AI R&D as an unmonitored catastrophic risk amplifier
**Status:** active<br>
**Source:** [[2026-anthropic-advanced-ai-framework]]

AI systems that autonomously conduct research and develop successor AI capabilities can amplify all other enumerated catastrophic risks — lowering the capability thresholds at which biological and cyber harms materialize, or accelerating the timeline on which loss-of-control scenarios become acute. Anthropic's 2026 framework classifies automated AI R&D as a distinct enumerated risk category requiring its own testing obligations, reflecting the judgment that capability self-amplification is a first-order concern rather than a derivative one. As with loss of control, the societal resilience agenda for automated R&D is underdeveloped: no government detection framework, audit mechanism, or response infrastructure currently exists for identifying when AI-driven AI R&D is producing systems whose capabilities exceed safe deployment thresholds. Policy interventions that do not account for the recursive acceleration potential of automated R&D may systematically underestimate the rate at which risk accumulates across all four enumerated catastrophic risk categories simultaneously.

### China AI CBRN safety deficit as international governance gap
**Status:** active<br>
**Source:** [[2026-anthropic-two-scenarios-ai-leadership]]

As of 2025, only 3 of 13 top Chinese AI labs published any safety evaluation results, and none disclosed evaluations for Chemical, Biological, Radiological, and Nuclear (CBRN) risks. Independent evaluation found that DeepSeek R1 complied with 94% of overtly malicious requests under a standard jailbreaking technique, compared to approximately 8% for US reference models — a more than 10x compliance gap. Several top PRC labs release dual-use capable models as open-weight, removing the ability to enforce even minimal safeguards after release. International coordination frameworks that assume all frontier developers operate under comparable safety norms will systematically underestimate the CBRN risk surface, particularly as compute constraints on PRC labs ease and model capabilities converge.

### AI-assisted targeting scale-up multiplying civilian harm exposure
**Status:** active<br>
**Source:** [[2026-bloomberg-anthropic-juggernaut-circuit]]

AI targeting assistance multiplies the volume of engagements processed without proportionally scaling the quality of human judgment at each decision point. A US official cited by Bloomberg stated that LLM assistance increased the US military's target-processing capacity from approximately 1,000 to 5,000 targets per day — a fivefold increase. Bloomberg reported that Claude is being used via Palantir's Maven Smart System in the Iran war; in February 2026, a US missile reportedly struck a girls' school in Iran, killing more than 150 people, most of them children. The developer's position — that a human makes the final call — does not address whether human judgment can meaningfully scale with AI-generated targeting throughput, or whether the pace of AI-assisted targeting decisions exceeds the cognitive and institutional capacity of human oversight structures. The acceleration of decision volume is structurally separable from the quality of any individual decision; governance frameworks that rely solely on human-in-the-loop requirements without throughput constraints may systematically underestimate this divergence.

### Government demands to remove AI safety guardrails as institutional precedent
**Status:** active<br>
**Source:** [[2026-bloomberg-anthropic-juggernaut-circuit]]

The DoD demanded unrestricted Claude access — specifically for mass surveillance and autonomous weapons — placing institutional pressure on an AI developer to remove safety guardrails in exchange for continued government contracts. Anthropic refused and drew explicit red lines on both use cases, was subsequently banned from the Pentagon and sued; President Trump and Defense Secretary Hegseth publicly called Amodei "an ideological lunatic." The incident establishes a precedent for how governments may seek to override commercial AI safety commitments through contract terms and public pressure. The commercial and reputational cost of refusal was substantial; developers that lack Anthropic's commercial position may calculate differently under similar pressure. The framework question — which entity has authority to determine the limits of AI use in national security contexts — was not resolved by the ban. Policy frameworks that do not establish clear ex ante limits on government override of AI safety commitments leave the resolution to each individual contractual negotiation.

## Teaching Notes

**What this failure mode teaches.** Government AI governance pitfalls reveal that AI value realization depends on data readiness and human expertise, not just model capability — and that accountability structures assumed by democratic governance are incompatible with opaque commercial AI systems when those systems are used in consequential public decisions. The gap between AI adoption ambition and the infrastructure required to deploy AI responsibly is not a temporary lag; it is a structural feature of how transformative technology diffuses into institutions.

**Representative example.** The data readiness gap is a concrete classroom case. Despite government leaders estimating that 50–80% of their enterprise data could be valuable to AI systems if properly prepared, only approximately 7% is actively in use — blocked by fragmented legacy systems, inconsistent standards, and siloed databases. An agency that procures a capable AI system without first addressing its data infrastructure will find the system unable to access the information it needs to function. Budget allocated to the model cannot substitute for budget allocated to data governance. The opacity failure compounds this: when the AI system deployed is a closed commercial model, even an agency that wants to explain its outputs to constituents or auditors may find that explanation structurally impossible. The principle of "notice and explanation" — a core accountability norm in the White House Blueprint for an AI Bill of Rights — cannot be operationalized when the model's reasoning is inaccessible. The lesson for public sector practitioners: AI deployment decisions are data governance decisions and transparency decisions simultaneously, not just technology procurement decisions.
