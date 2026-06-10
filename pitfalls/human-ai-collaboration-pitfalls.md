---
type: pitfalls
title: Human-AI Collaboration Pitfalls
created: 2026-06-10
updated: 2026-06-10
parent_entity: "[[topics/human-ai-collaboration]]"
parent_type: topic
status: current
failure_mode_count: 6
teaching_relevance: true
competency_domains:
  - output-verification-and-risk-assessment
  - practical-ai-use-and-interaction
professional_contexts:
  - teaching-and-instruction
  - organizational-leadership-and-change-management
  - professional-and-continuing-education
contributing_sources:
  - "[[2024-vaccaro-human-ai-synergy-meta-analysis]]"
teaching_notes_reviewed: 2026-06-10
---

## Technical Limitations

### Decision-Task Performance Deficit
**Status:** active<br>
**Source:** [[2024-vaccaro-human-ai-synergy-meta-analysis]]

In decision tasks — those in which participants choose among a predefined set of options — human-AI combinations consistently underperform the best individual performer (average Hedges' g = −0.27 across 344 effect sizes). This is a structural consequence of the dominant collaboration paradigm: both the human and AI evaluate the whole task, the human makes the final call, and the combination inherits the human's calibration errors on top of the AI's mistakes. Over 85% of the human-AI experiments in the 2024 meta-analysis used this full-task-overlap design. The deficit is not specific to any AI system quality level or explanation format — it is a property of the decision-task framing itself.

### AI Explanation and Confidence Features Do Not Improve Synergy
**Status:** active<br>
**Source:** [[2024-vaccaro-human-ai-synergy-meta-analysis]]

Adding explanations for AI recommendations or displaying AI confidence scores does not significantly improve human-AI synergy or augmentation, across 300+ experimental effect sizes. Both features have received substantial research and product investment on the premise that transparency improves trust calibration. Meta-analytic evidence contradicts this premise. The factors that actually moderate performance — task type and relative baseline performance — have received far less research attention and are rarely surfaced to end users.

## Usage Antipatterns

### Overreliance on AI Recommendations
**Status:** active<br>
**Source:** [[2024-vaccaro-human-ai-synergy-meta-analysis]]

Humans often apply AI suggestions as strong guidelines without independently seeking or processing additional information — especially when the AI has demonstrated generally high accuracy. When the AI outperforms the human overall, overreliance is most acute: the human correctly infers that the AI is generally better, then incorrectly extends that general accuracy to individual cases where the AI errs. Because the human lacks the domain expertise to identify those specific failure cases, their participation in the decision degrades overall performance below what the AI alone would achieve. Overreliance is not a bug in the AI system but a predictable consequence of deploying AI assistance to users less accurate than the AI on the relevant task.

### Underreliance on AI Recommendations
**Status:** active<br>
**Source:** [[2024-vaccaro-human-ai-synergy-meta-analysis]]

Humans sometimes ignore valid AI recommendations due to adverse attitudes toward automation, skepticism about AI reliability, or discomfort with algorithmic decision-making. Unlike overreliance, underreliance degrades even the augmentation benefit — humans fail to capture performance value the AI could provide, because they discount its output regardless of quality. Underreliance is more likely when humans have prior negative experiences with AI errors or when the AI's reasoning is opaque. Providing explanations does not reliably reduce underreliance, per the meta-analytic evidence.

### Benchmarking Human-AI Systems Only Against the Human Baseline
**Status:** active<br>
**Source:** [[2024-vaccaro-human-ai-synergy-meta-analysis]]

Evaluating whether a human-AI system is useful by comparing it only to humans alone — rather than also to AI alone — systematically misleads practitioners about whether the collaboration adds value. A system can outperform a human by a large margin while still underperforming what AI alone would achieve. The 2024 meta-analysis found substantial publication bias toward studies measuring the augmentation outcome (human-AI vs. human alone) and away from studies measuring the synergy outcome (human-AI vs. best of human or AI alone). This means the published literature overstates the case for human-AI collaboration as currently practiced.

## Alignment and Safety Concerns

### Trust Miscalibration Risk in High-Stakes Deployments
**Status:** active<br>
**Source:** [[2024-vaccaro-human-ai-synergy-meta-analysis]]

Meta-analytic evidence shows that human involvement in AI-assisted decision-making degrades performance specifically in domains where the AI outperforms the human — the cases where the human's trust calibration is least reliable. This creates a structural tension in high-stakes deployments (medical diagnosis, legal judgment, criminal risk assessment) where human oversight is mandated for ethical, legal, or regulatory reasons: the oversight mechanism itself introduces predictable performance losses when the AI is more capable than the human reviewer. Requiring human sign-off satisfies procedural accountability requirements while potentially increasing the rate of erroneous outcomes. This is not an argument against human oversight, but a warning that oversight effectiveness depends on the human having genuine domain expertise competitive with or superior to the AI on the specific task being reviewed.

## Teaching Notes

**What this failure mode teaches.** Human-AI collaboration fails in two opposite directions — overreliance and underreliance — because humans lack reliable signals for calibrating when to trust AI recommendations versus their own judgment. The calibration failure is sharpest when the AI outperforms the human overall: in precisely the conditions where deferring to AI would improve performance, humans are least equipped to identify which specific cases warrant that deference.

**Representative example.** A comparative study used three classification tasks with the same AI system achieving 73% accuracy on all three. In bird image classification, where humans alone scored 81%, the human-AI team reached 90% — genuine synergy. In fake hotel review detection, where humans alone scored 55%, the human-AI team scored only 69% — below the AI working alone at 73%. The AI's accuracy was identical across both tasks; the interface was the same; the participant pool was the same. What differed was whether the human had genuine domain expertise. For hotel reviews, the humans were less accurate than the AI overall, so their judgment about when to override the AI was also unreliable. They degraded the AI's 73% performance to 69% by intervening on cases where the AI was correct. For practitioners, the implication is direct: deploying AI assistance to workers who are less accurate than the AI on the relevant task is likely to hurt, not help — even when the AI's average recommendation is right.
