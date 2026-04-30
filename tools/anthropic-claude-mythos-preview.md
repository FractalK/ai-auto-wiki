---
type: tool
title: Claude Mythos Preview
created: 2026-04-22
updated: 2026-04-23
summary: Anthropic's unreleased frontier model demonstrating threshold-crossing capability in autonomous software vulnerability discovery and software engineering, available in limited research preview to Project Glasswing partners and open-source maintainers.
status: emerging
vendor: Anthropic
pricing_model: usage-based
access_tier:
  - enterprise
  - api
capabilities:
  - Autonomous zero-day vulnerability discovery across major operating systems and browsers
  - Multi-step exploit chain development without human steering
  - Software engineering at SOTA level (93.9% SWE-bench Verified)
  - Extended thinking with step-by-step reasoning before response
  - Vision, audio, and text processing
limitations:
  - Not generally available; restricted to Project Glasswing partners and approved open-source maintainers
  - Requires Cyber Verification Program approval for legitimate security researchers
  - Full public deployment requires new cybersecurity safeguards not yet released
  - Priced at $25/$125 per M input/output tokens after Anthropic usage credits expire
primary_use_cases:
  - Defensive vulnerability scanning in critical infrastructure
  - Autonomous security research and exploit analysis
  - Advanced software engineering and agentic coding tasks
source_count: 3
last_assessed: 2026-04-23
related_topics:
  - "[[ai-assisted-vulnerability-discovery]]"
  - "[[constitutional-ai]]"
related_tools:
  - "[[anthropic-claude-opus-4-7]]"
teaching_relevance: true
competency_domains:
  - capability-horizon-awareness
  - ai-safety-and-alignment-literacy
professional_contexts:
  - organizational-leadership-and-change-management
  - project-and-program-management
technical_depth: practitioner
teaching_notes_reviewed: 2026-04-30
---

Claude Mythos Preview is Anthropic's most capable model as of April 2026, currently available only to Project Glasswing partners and approved open-source security maintainers. It is not generally available and Anthropic has stated no plans to make it so without first developing and testing new cybersecurity safeguards. The model represents a documented capability threshold: it can autonomously find and exploit software vulnerabilities at a level surpassing all but the most skilled human security researchers.

## Cybersecurity Capabilities

The defining characteristic of Mythos Preview is its autonomous vulnerability discovery capability. In the weeks prior to the Project Glasswing announcement, Anthropic used the model to identify thousands of zero-day vulnerabilities — previously unknown flaws — across every major operating system and web browser. This included a 27-year-old vulnerability in OpenBSD, a 16-year-old vulnerability in FFmpeg that had been passed over by five million automated test runs, and a multi-step exploit chain in the Linux kernel enabling escalation from ordinary user access to full kernel control. All discoveries were made without human steering.

On CyberGym, Anthropic's vulnerability reproduction benchmark, Mythos Preview achieved 83.1% compared to 66.6% for Claude Opus 4.6 — a 16.5 percentage point gap. Anthropic describes this as a threshold event: the capabilities that enable defensive security at scale are the same capabilities that, in the wrong hands, enable sophisticated offensive operations. The defensive use case depends on the model being deployed by defenders first and faster than adversarial actors gain access.

## Software Engineering Performance

Mythos Preview's cybersecurity capabilities derive from underlying software engineering and reasoning strengths. On SWE-bench Verified, the model achieves 93.9% (vs. 80.8% for Opus 4.6). On SWE-bench Pro, it achieves 77.8% (vs. 53.4%). On Terminal-Bench 2.0, it achieves 82.0% (vs. 65.4%). These represent state-of-the-art results across software engineering benchmarks at the time of announcement.

The model also achieves 94.6% on GPQA Diamond (graduate-level science reasoning) and 86.9% on BrowseComp (web research). Notably, BrowseComp scores come while using 4.9× fewer tokens than Opus 4.6 for equivalent tasks.

An Anthropic internal survey cited a 4× acceleration in engineer productivity from Mythos Preview. However, the Opus 4.7 system card reveals the survey was opt-in based on interest rather than randomly sampled, and measured self-reported output volume — not quality or time savings. These limitations make the productivity figure illustrative rather than empirically precise. Separately, external security researchers (Vidok) found that other flagship models — including Opus 4.6 and GPT-5.4 — with appropriate scaffolding could reproduce many of the specific vulnerabilities Anthropic highlighted as Mythos-identified discoveries. Vidok's conclusion: Mythos changes the economics of vulnerability discovery rather than enabling capabilities categorically impossible for other frontier models. This does not challenge Mythos's benchmark advantage on CyberGym, which remains the primary quantitative evidence for its security edge.

## Alignment Approach

Mythos Preview is trained using an evolved version of Anthropic's Constitutional AI framework, with more sophisticated reasoning about competing principles and edge cases than prior models. It is also the first Claude model trained with direct feedback from mechanistic interpretability research: Anthropic researchers identified specific circuits and attention patterns associated with problematic behaviors during training and used those findings to shape the model's development. Extended thinking — the ability to reason through problems step-by-step before producing a final output — is supported and functions as a form of self-monitoring that reduces impulsive harmful outputs.

Despite these advances, Anthropic characterizes the alignment challenge of Mythos Preview as unresolved. The model's most dangerous capabilities require safeguards that have not yet been deployed at scale. The planned path is to test new cybersecurity safeguards with an upcoming Claude Opus model before enabling Mythos-class capabilities for broad deployment.

## Access and Pricing

Project Glasswing partners receive access through the Claude API, Amazon Bedrock, Google Cloud Vertex AI, and Microsoft Foundry. Anthropic has committed up to \$100M in usage credits. After the research preview period, access is priced at \$25/\$125 per million input/output tokens. Open-source software maintainers can apply through the Claude for Open Source program. Security researchers whose legitimate work is affected by cybersecurity safeguards can apply to an upcoming Cyber Verification Program.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| Mythos Preview achieved 83.1% on CyberGym (vulnerability reproduction benchmark) compared to 66.6% for Opus 4.6, the largest recorded capability gap on a cybersecurity benchmark between two consecutive Anthropic models. | [[2026-anthropic-project-glasswing]] | 2026-04-07 | current | 2 | false |
| Mythos Preview autonomously identified zero-day vulnerabilities in every major operating system and web browser, including a 27-year-old OpenBSD flaw and a 16-year-old FFmpeg vulnerability missed by five million automated test runs, without human steering. | [[2026-anthropic-project-glasswing]] | 2026-04-07 | current | 2 | false |
| Mythos Preview achieved 93.9% on SWE-bench Verified, a 13.1 percentage point improvement over Opus 4.6, with the performance margin holding after excluding problems showing signs of memorization. | [[2026-anthropic-project-glasswing]] | 2026-04-07 | current | 2 | false |
| Anthropic trained Claude Mythos Preview with direct feedback from mechanistic interpretability findings, using identified circuit-level patterns associated with problematic behaviors to shape the model during training. | [[2026-mindstudio-claude-mythos-alignment-paradox]] | 2026-04-10 | current | 1 | false |
| Anthropic does not plan to make Mythos Preview generally available; public deployment requires new cybersecurity safeguards that Anthropic plans to test first on an upcoming Claude Opus model. | [[2026-anthropic-project-glasswing]] | 2026-04-07 | current | 2 | false |

## Teaching Notes

**Concept in plain terms.** Claude Mythos Preview is Anthropic's frontier AI model as of April 2026, available only to a restricted set of security research partners. Its defining capability is autonomous software vulnerability discovery — it can find and chain security flaws in major operating systems and browsers without human guidance at any intermediate step.

**Why it matters for instruction.** Mythos Preview represents a documented capability threshold event that makes the dual-use problem immediate and concrete. Instructors covering AI safety or capability horizons can use it to illustrate that the same AI advances enabling large-scale defensive security work also lower the barrier to sophisticated offensive attacks — the technology itself does not distinguish intended use, and access control and alignment are partial mitigations, not solutions.

**Common misconceptions.** Students often assume that restricting access to dangerous AI capabilities is sufficient to prevent misuse, or that safety training eliminates offensive capability. Mythos Preview illustrates that access control and alignment reduce risk at the margin — the capability threshold crossed is not reversible, and the window between vulnerability discovery and exploitation has compressed for any actor with access to comparable models.

**Suggested framing.** Introduce Mythos Preview as a case study in capability threshold-crossing — a specific, documented moment when AI moved from assisting human security experts to exceeding them in a consequential domain — and use it to ground discussion of dual-use governance challenges.
