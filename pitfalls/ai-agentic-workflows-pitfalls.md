---
type: pitfalls
title: AI Agentic Workflows Pitfalls
created: 2026-05-21
updated: 2026-05-21
parent_entity: "[[topics/ai-agentic-workflows]]"
parent_type: topic
status: current
failure_mode_count: 7
contributing_sources:
  - "[[2026-mollick-management-ai-superpower]]"
  - "[[2026-stanford-hai-ai-index]]"
  - "[[2025-mit-sloan-bcg-agentic-ai-management]]"
  - "[[2026-oecd-agentic-ai-landscape]]"
teaching_relevance: true
competency_domains:
  - output-verification-and-risk-assessment
  - ai-integration-in-organizational-workflows
  - practical-ai-use-and-interaction
professional_contexts:
  - organizational-leadership-and-change-management
  - project-and-program-management
  - entrepreneurship-and-startups
technical_depth: practitioner
teaching_notes_reviewed: 2026-05-21
---

## Technical Limitations

### Task Reliability Gap
**Status:** active<br>
**Source:** [[2026-stanford-hai-ai-index]]

Even top-performing agentic models fail approximately one in three attempts on structured computer-use benchmarks (OSWorld: ~66% accuracy vs. 72% human baseline as of 2025). Tasks requiring near-perfect success rates — audit trails, compliance documentation, sequential multi-step workflows with compounding dependencies — cannot yet rely on agentic AI for unsupervised execution. Published benchmark accuracy systematically overstates reliability on novel tasks outside the benchmark distribution.

### Verification Overhead Underestimation
**Status:** active<br>
**Source:** [[2026-mollick-management-ai-superpower]]

Users consistently underestimate the cumulative cost of evaluation cycles when Probability of Success is moderate or low. The Equation of Agentic Work makes the math explicit: when a task takes seven hours manually and the AI succeeds 70% of the time with one hour of evaluation overhead per attempt, expected net savings are approximately two hours — but with high variance. Tasks the AI fails cost *more* time than doing them manually. Organizations that delegate broadly without assessing task-level success rates discover negative ROI after deployment rather than before.

## Usage Antipatterns

### Specification Vagueness
**Status:** active<br>
**Source:** [[2026-mollick-management-ai-superpower]]

Delegating tasks without defining the goal rationale, scope of authority, definition of "done," required outputs, and quality self-checks produces AI outputs that technically complete the surface task but miss the actual intent. AI agents have no context beyond what is explicitly provided; they cannot infer unstated requirements, organizational norms, or judgment calls the way an experienced human colleague would. Multi-page structured prompts matching the format of human delegation documents (PRDs, Five Paragraph Orders, engagement scopes) consistently outperform brief or vague instructions.

### Domain Expertise Substitution Fallacy
**Status:** active<br>
**Source:** [[2026-mollick-management-ai-superpower]]

Treating AI agents as a substitute for domain expertise rather than an amplifier of it. Domain expertise has three roles in agentic workflows: specifying what to ask for, recognizing quality problems in output, and providing targeted correction when the first attempt misses. People without domain expertise receive less value from the same AI tools because they write weaker specifications and accept lower-quality outputs they cannot identify as such. The common expectation that AI lowers the bar for effective task delegation inverts the actual dynamic.

### Management Framework Application Without Explicit Rules
**Status:** active<br>
**Source:** [[2025-mit-sloan-bcg-agentic-ai-management]], [[2026-oecd-agentic-ai-landscape]]

Applying human delegation frameworks to agentic AI without translating implicit rules, organizational norms, and judgment thresholds into explicit parameters. Human workers navigate permissible decision scopes, ethical boundaries, escalation triggers, and confidence thresholds through tacit knowledge accumulated over time. AI agents require these constraints to be explicitly defined as threshold values, permissible action sets, and defined escalation conditions. Organizations that deploy agentic AI under standard management frameworks, without explicit rule translation, create undetected governance gaps: the agent operates as if it has the implicit judgment it lacks.

## Alignment and Safety Concerns

### AI Offspring Governance Gap
**Status:** active<br>
**Source:** [[2025-mit-sloan-bcg-agentic-ai-management]]

Failing to account for AI systems autonomously created or modified by other AI systems. As agentic AI capabilities expand, some systems can generate sub-agents, modify their own configurations, or create specialized AI tools for subtasks. These "AI offspring" may fall entirely outside existing management scope: they were not provisioned by a human, have no human-assigned accountability owner, and may operate with permissions inherited from their parent system. Standard governance audits that track only human-provisioned AI deployments will systematically miss this category.

### Accountability Void via AI Exceptionalism
**Status:** active<br>
**Source:** [[2025-mit-sloan-bcg-agentic-ai-management]]

Treating the novel properties of agentic AI — its opacity, speed, and autonomy — as grounds for exempting AI-driven outcomes from standard accountability structures. AI lacks legal personhood and cannot be held directly liable for outcomes; accountability must therefore be explicitly distributed across creators, deployers, and users. Organizations that frame agentic AI governance as a new paradigm requiring new institutions, without first clearly assigning accountability for outcomes under existing frameworks, create a vacuum that no actor fills. The 25% minority in the MIT Sloan/BCG expert panel who argued against new management frameworks were making this point: clear human accountability should be the starting point, not the aspirational endpoint of governance design.

## Teaching Notes

**What this failure mode teaches.** Agentic workflow failures reveal a structural difference between delegating to humans and delegating to AI: human workers accumulate implicit knowledge of organizational norms, ethical boundaries, and escalation triggers over time; AI agents only know what they are explicitly given. When those implicit rules remain unspecified, the AI operates as though it has broader authority than intended — not through any intentional breach, but because boundary knowledge was never encoded. This failure mode teaches that effective AI delegation is as much a governance design task as a prompting task.

**Representative example.** A project manager at a consulting firm deploys an agentic AI system to conduct preliminary client research, assuming the same informal guidelines that govern junior analyst work will apply: be thorough, avoid sensitive topics, flag anything unusual. The AI agent retrieves and summarizes competitor intelligence that would normally require partner-level approval before inclusion in a client deliverable — because "requires partner-level approval" was never encoded as an explicit permission boundary. The output was accurate and useful by ordinary quality standards, but violated a firm norm the manager assumed was obvious. The correct approach: before deploying an agentic system, enumerate every implicit escalation trigger, permission boundary, and ethical threshold that a new employee would learn informally — then encode each as an explicit parameter. The AI has no informal orientation period and will not infer what "common sense" means in your organizational context.
