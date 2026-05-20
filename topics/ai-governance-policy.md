---
type: topic
title: AI Governance and Policy
created: 2026-04-23
updated: 2026-05-20
summary: The emerging regulatory and policy landscape for AI, encompassing liability frameworks, age-gating proposals, international coordination mechanisms, and analogies to prior technology governance efforts including nuclear arms control and environmental treaties.
status: developing
source_count: 4
last_assessed: 2026-05-20
related_topics:
  - "[[ai-companion-risks]]"
  - "[[constitutional-ai]]"
  - "[[ai-assisted-vulnerability-discovery]]"
  - "[[responsible-ai-government-evaluation]]"
teaching_relevance: true
competency_domains:
  - ai-integration-in-organizational-workflows
  - ai-safety-and-alignment-literacy
professional_contexts:
  - domestic-civil-service-and-public-administration
  - organizational-leadership-and-change-management
technical_depth: practitioner
teaching_notes_reviewed: 2026-04-30
---

AI governance encompasses the institutional, legal, and international mechanisms through which AI development and deployment are regulated, made accountable, and bounded. As of 2026, no comprehensive national or international AI governance framework is in force. The US federal policy landscape has undergone sharp reversals between administrations; international coordination remains aspirational on most questions; and government AI adoption is accelerating faster than the regulatory structures intended to shape it.

## International Coordination

The most developed framework for international AI governance comes from advocates of preemptive limits on systems capable of causing civilizational harm. Analyst Tristan Harris proposes four regulatory red lines: mass labor displacement without transition infrastructure, AI-enabled surveillance states that permanently erode privacy, engagement-maximizing AI companions for minors, and deployment of uncontrollable superintelligent systems. These are proposed as the minimum scope for international coordination, analogous to the nuclear Non-Proliferation Treaty and the Montreal Protocol on ozone-depleting chemicals — precedents where adversarial countries nonetheless coordinated on shared existential risks.

Enforcing AI governance agreements faces a fundamental monitoring challenge: unlike nuclear detonations, AI training runs are not externally observable by default. Researchers cited as the "AI-27 authors" argue that monitoring approximately 95% of global compute — through satellite heat-emission monitoring, electrical signal tracking, and shared data center mapping — would be sufficient for treaties to be enforceable, because only actors with substantial compute fractions can build the most dangerous systems. A precedent exists: at China's request, the 2023–2024 Biden-Xi meetings produced an initial agreement preventing AI use in nuclear command and control systems, establishing that adversarial powers can coordinate on AI safety when mutual existential stakes are mutually recognized.

The 2025 Paris AI Action Summit represented the most significant multilateral AI governance event to date by signatory count. More than 100 countries participated; 64 — including the EU and the African Union — signed the Statement on Inclusive and Sustainable AI, which committed signatories to responsible AI development principles. The United States and United Kingdom declined to sign, signaling divergence between the two historically closest AI governance partners. The Paris summit built on the 2023 Bletchley Park AI Safety Summit and Japan's 2024 Hiroshima AI Process, constituting a series of multilateral forums that have so far produced statements and process commitments rather than binding treaties.

National AI Safety Institutes have emerged as a parallel institutional mechanism for governance without treaty. As of 2025, AI Safety Institutes are operational in the United Kingdom (the founding institution, established 2023), the United States (housed within NIST), Japan, Singapore, and Israel. India and France launched new institutes in 2025; a second wave is under development in Canada, South Korea, Germany, and Brazil. These institutions focus primarily on capability evaluation, safety research, and inter-governmental coordination rather than regulatory enforcement.

## US Federal Policy Evolution

At the federal level, AI governance has been marked by sharp reversals. The Biden administration built a substantial executive framework including Executive Order 13960 (Promoting the Use of Trustworthy Artificial Intelligence in the Federal Government) and the White House Blueprint for an AI Bill of Rights (2022), which articulated five principles: safe and effective systems, algorithmic discrimination protections, data privacy, notice and explanation, and human alternatives and fallback. In January 2025, the Trump Administration revoked many of these orders, directing agencies to revise or rescind all AI policies from the prior administration on the grounds that they imposed "onerous and unnecessary government control over the development of AI." The White House's America's AI Action Plan (July 2025) signaled a shift toward promoting AI workforce development through public-private collaboration rather than protective regulation.

Following the federal rollback, many state and local government bodies have continued promoting responsible AI practices independently, maintaining transparency and privacy requirements even where federal mandates were withdrawn.

## Government AI Acceleration

Despite regulatory uncertainty, government AI adoption is accelerating. A 2025 IBM IBV survey of 100 senior government technology executives found that 69% acknowledge the potential productivity gains from AI automation are so large they must accept significant risk to keep pace, with nearly 90% planning to accelerate transformation despite uncertainty. Governments currently allocate an average of approximately 8% of IT budgets to AI — projected to exceed 13% by 2030 — with spending expected to shift from data infrastructure and traditional AI toward generative and agentic applications.

The data and workforce constraints behind this ambition are significant. Only approximately 7% of government enterprise data is currently being used by AI systems, despite leaders estimating 50–80% of their data could be valuable if properly prepared. The primary barriers to AI maturity are talent and governance, not technology: 62% of government technology leaders identify workforce and talent development as their most critical need, followed by 55% citing ethical, legal, and regulatory frameworks.

## AI Incident Trends and Responsible AI Gap

Documented AI incidents rose sharply in 2025, reaching 362 globally — up 55% from 233 in 2024, with the OECD AIM dashboard recording a peak of 435 incidents in a single month (January 2026). Responsible AI benchmark reporting by frontier model developers remains inconsistent: nearly all leading developers report results on capability benchmarks, but reporting on responsible AI benchmarks is substantially spottier. Compounding the challenge, empirical research documented that improving one responsible AI dimension — such as safety — can degrade another, such as accuracy, creating systematic optimization tradeoffs that make comprehensive responsible AI compliance harder to achieve simultaneously.

Organizational RAI maturity lags the incident growth rate. The 2026 AI Index documents a global average RAI maturity score of 2.3 out of 4 across surveyed organizations. Governance role creation is accelerating — AI-specific governance positions grew 17% in 2025 — and the share of organizations with no RAI policies fell from 24% to 11% over the past year. The primary barriers to RAI adoption are knowledge gaps (cited by 59% of organizations), budget constraints (48%), and regulatory uncertainty (41%). Among organizations deploying agentic AI specifically, security and risk concerns were cited by 62% as the top barrier. Regulatory standards adoption is uneven: ISO/IEC 42001 (the AI management system standard) was adopted by 36% of surveyed organizations, and the NIST AI Risk Management Framework by 33%.

## AI Sovereignty and Public Trust

AI sovereignty emerged as a central organizing principle in national AI policy in 2025. More than half of newly adopted national AI strategies came from developing countries entering the policy landscape for the first time, with state-backed investments in AI supercomputing rising in parallel — a sign of growing ambitions for domestic control over AI ecosystems. Open-source AI development is beginning to redistribute global participation, with GitHub contributions from outside the U.S. and Europe now outpacing the EU and approaching the United States, fueling more linguistically diverse models and benchmarks.

Public trust in AI governance institutions is fragmented and asymmetric. Globally, the EU is trusted more than the United States or China to regulate AI effectively. Among surveyed countries, the United States reported the lowest level of trust in its own government to regulate AI, at 31%. A pronounced expert-public divide also characterizes governance attitudes: 73% of AI experts expect a positive impact from AI on how people do their jobs, compared with just 23% of the public — a 50-point gap that shapes the political feasibility of AI governance interventions.

## Data Records

| Metric | Value | Conditions | Measurement Date | Source | Status |
|---|---|---|---|---|---|
| Documented AI incidents globally | 362 | Annual count per AI Index methodology | 2025-12 | [[2026-stanford-hai-ai-index]] | current |
| Documented AI incidents globally | 233 | Annual count per AI Index methodology | 2024-12 | [[2026-stanford-hai-ai-index]] | superseded |
| Trust in government to regulate AI — United States | 31% | Public survey; lowest among surveyed countries | 2025 | [[2026-stanford-hai-ai-index]] | current |

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| Harris proposes four regulatory red lines for AI governance: mass labor displacement without transition infrastructure; AI-enabled surveillance states; engagement-maximizing AI companions for minors; and deployment of uncontrollable superintelligent systems. | [[2025-pivot-harris-ai-dilemma]] | 2025-12-22 | current | 1 | false |
| Harris cites a China-initiated agreement at the 2023–2024 Biden-Xi meetings to prevent AI use in nuclear command and control systems as evidence that adversarial nations can coordinate on AI safety when existential stakes are mutually recognized. | [[2025-pivot-harris-ai-dilemma]] | 2025-12-22 | current | 1 | false |
| Harris cites AI-27 authors arguing that monitoring approximately 95% of global compute — via satellite heat-emission data, electrical signal tracking, and shared data center mapping — is the threshold needed for international AI governance treaties to be enforceable against the most dangerous AI development. | [[2025-pivot-harris-ai-dilemma]] | 2025-12-22 | current | 1 | false |
| The Trump Administration revoked many prior AI executive orders in January 2025, directing agencies to revise or rescind all AI policies from the prior administration; many state and local governments continue promoting responsible AI practices independently. | [[2025-responsible-ai-public-evaluation]] | 2025-12-01 | current | 1 | false |
| A 2025 IBM IBV survey of 100 senior government technology executives found that 69% acknowledge potential AI productivity gains are so large they must accept significant risk to keep pace, with nearly 90% planning to accelerate AI transformation despite uncertainty. | [[2025-ibm-government-ai-era]] | 2025-12-01 | current | 1 | false |

## Teaching Notes

**Concept in plain terms.** AI governance and policy refers to the legal, regulatory, and international mechanisms being developed to manage AI development and deployment. As of 2026, no comprehensive framework is in force anywhere; the US has undergone sharp policy reversals between administrations; and government AI adoption is accelerating faster than governance frameworks can keep up.

**Why it matters for instruction.** AI governance illustrates how governance of transformative technologies typically lags behind adoption — and how the absence of governance creates risks for users, affected populations, and institutions. Understanding the current policy landscape helps practitioners working in or with government understand what constraints apply, what gaps remain, and what institutional risks they are assuming.

**Common misconceptions.** Students often assume that government AI adoption is cautious and well-regulated relative to private sector adoption. The IBM data showing 90% of government technology leaders planning to accelerate AI transformation despite regulatory uncertainty reveals the opposite — adoption pressure in the public sector is significant, and governance structures are playing catch-up rather than setting the pace.

**Suggested framing.** Introduce AI governance as a race between adoption and accountability — framing current policy gaps not as permanent features but as the temporary consequence of transformative technology diffusing faster than institutions can adapt, and using the US federal reversal between administrations as a case study in how political transitions affect the stability of AI governance frameworks.
