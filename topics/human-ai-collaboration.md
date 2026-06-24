---
type: topic
title: Human-AI Collaboration
created: 2026-06-10
updated: 2026-06-23
summary: The empirical conditions under which combining humans and AI outperforms either alone, characterized by a key distinction between augmentation (beating the human baseline) and synergy (beating the best individual performer), with task type and relative baseline performance identified as the dominant moderators of whether collaboration helps or hurts.
status: developing
source_count: 3
last_assessed: 2026-06-23
related_topics:
  - "[[ai-workforce-complementarity]]"
  - "[[ai-agentic-workflows]]"
  - "[[llm-fundamentals]]"
related_tools:
  - "[[anthropic-claude-code]]"
  - "[[anthropic-claude-opus-4-7]]"
teaching_relevance: true
competency_domains:
  - practical-ai-use-and-interaction
  - output-verification-and-risk-assessment
  - tool-evaluation-and-selection
professional_contexts:
  - teaching-and-instruction
  - professional-and-continuing-education
  - organizational-leadership-and-change-management
technical_depth: practitioner
teaching_notes_reviewed: 2026-06-10
---

Measuring whether a human-AI system outperforms humans alone is a different question from measuring whether it outperforms the best of humans or AI alone. A 2024 preregistered meta-analysis from MIT's Center for Collective Intelligence quantifies this distinction with systematic evidence: human-AI combinations reliably beat humans working alone (augmentation), but on average fail to outperform either partner working independently (synergy). Across 106 experiments and 370 effect sizes from peer-reviewed publications spanning 2020–2023, the average human-AI system achieved augmentation (Hedges' g = 0.64, medium-to-large effect) while falling short of synergy (g = −0.23, small negative effect, p = 0.005). In practical terms, for most tasks studied it would have been more effective to use either a skilled human or a capable AI system alone rather than combining them.

## Data Records

| Metric | Value | Conditions | Measurement Date | Source | Status |
|---|---|---|---|---|---|
| Human-AI synergy — overall | g = −0.23 (95% CI −0.39 to −0.07) | 106 experiments, 370 effect sizes; preregistered; peer-reviewed publications 2020–2023; baseline = best of human or AI alone | 2024-10 | [[2024-vaccaro-human-ai-synergy-meta-analysis]] | current |
| Human augmentation — overall | g = 0.64 (95% CI 0.53 to 0.74) | Same sample; baseline = human alone | 2024-10 | [[2024-vaccaro-human-ai-synergy-meta-analysis]] | current |
| Human-AI synergy — decision tasks | g = −0.27 (95% CI −0.44 to −0.10) | n = 344 effect sizes; tasks involving choice among finite options | 2024-10 | [[2024-vaccaro-human-ai-synergy-meta-analysis]] | current |
| Human-AI synergy — creation tasks | g = 0.19 (95% CI −0.09 to 0.48, ns) | n = 34 effect sizes; open-ended response tasks; not statistically significant | 2024-10 | [[2024-vaccaro-human-ai-synergy-meta-analysis]] | current |
| Human-AI synergy — human outperforms AI alone | g = 0.46 (95% CI 0.28 to 0.66) | n = 127 effect sizes; cases where human alone > AI alone | 2024-10 | [[2024-vaccaro-human-ai-synergy-meta-analysis]] | current |
| Human-AI synergy — AI outperforms human alone | g = −0.54 (95% CI −0.71 to −0.37) | n = 251 effect sizes; cases where AI alone > human alone | 2024-10 | [[2024-vaccaro-human-ai-synergy-meta-analysis]] | current |
| Planning decisions made by user (agentic coding) | ~70% | Average across ~400,000 Claude Code sessions; Oct 2025–Apr 2026 | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Execution decisions made by Claude (agentic coding) | ~80% | Average across sessions | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Claude actions per prompt — expert users | 12 | Geometric mean; agentic coding sessions | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Claude actions per prompt — novice users | 5 | Geometric mean; same methodology | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Verified success rate — novice sessions | 15% | Judged successful + at least one hard verifiable signal | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Verified success rate — intermediate through expert sessions | 28–33% | Same methodology | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Abandoned session rate — novice (when hitting trouble) | 19% | Failed + zero lines of code written | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Abandoned session rate — intermediate through expert (when hitting trouble) | 5–7% | Same methodology | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Task time — 4 robotics tasks, Claude Opus 4.7 (autonomous) | 9 min 35 sec | Claude Code; adaptive thinking, max effort; 3-trial average; Project Fetch Phase 2 | 2026-06 | [[2026-anthropic-project-fetch-phase-two]] | current |
| Task time — 4 robotics tasks, Team Claude | 181 min | Human team with Claude access; August 2024 baseline; Project Fetch Phase 1 | 2024-08 | [[2026-anthropic-project-fetch-phase-two]] | current |
| Task time — 4 robotics tasks, Team Claude-less | 361 min | Human team without AI; August 2024 baseline; Project Fetch Phase 1 | 2024-08 | [[2026-anthropic-project-fetch-phase-two]] | current |
| Code volume — Claude Opus 4.7 (autonomous) | 1,045 lines | Project Fetch Phase 2; comparable or better task success than human teams | 2026-06 | [[2026-anthropic-project-fetch-phase-two]] | current |
| Code volume — Team Claude | 10,309 lines | Project Fetch Phase 1 (August 2024); Claude-assisted human team | 2024-08 | [[2026-anthropic-project-fetch-phase-two]] | current |

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| A preregistered meta-analysis of 106 experimental studies (370 effect sizes, 2020–2023) found human-AI combinations outperform humans alone on average (Hedges' g = 0.64) but perform significantly worse than the best of humans or AI alone (g = −0.23), meaning most human-AI systems achieve augmentation but not synergy — and for most studied tasks it would have been more effective to use either partner alone. | [[2024-vaccaro-human-ai-synergy-meta-analysis]] | 2024-10-28 | current | 1.5 | false |
| Task type significantly moderates human-AI synergy (p = 0.006): decision tasks — the dominant paradigm in the human-AI literature — produce consistent performance losses (g = −0.27), while creation tasks trend toward gains (g = 0.19), with the difference between task types statistically significant despite the small creation-task sample size. | [[2024-vaccaro-human-ai-synergy-meta-analysis]] | 2024-10-28 | current | 1.5 | false |
| Relative baseline performance is the strongest moderator of human-AI synergy (F = 81.79, p < 0.001): when humans outperform AI alone, combinations achieve substantial synergy (g = 0.46); when AI outperforms humans alone, combinations produce significant losses (g = −0.54), indicating humans accurately calibrate trust only when they are the more capable performer. | [[2024-vaccaro-human-ai-synergy-meta-analysis]] | 2024-10-28 | current | 1.5 | false |
| AI explanations and AI confidence scores do not significantly moderate human-AI synergy or augmentation across 300+ experimental effect sizes, challenging the widespread assumption in the explainable AI field that transparency features improve human-AI system performance. | [[2024-vaccaro-human-ai-synergy-meta-analysis]] | 2024-10-28 | current | 1.5 | false |
| Task division — explicitly assigning different subtasks to the human or AI partner based on relative capability — shows positive average synergy (g = 0.22) in limited experiments (3 of 106+ studies); large-scale agentic coding data from 400,000 real sessions corroborates this, showing the natural division is human planning (~70% of planning decisions) with AI execution (~80% of execution decisions), and that domain expertise determines how much autonomous work the AI does per instruction. | [[2024-vaccaro-human-ai-synergy-meta-analysis]], [[2026-anthropic-agentic-coding-returns-expertise]] | 2026-06-16 | current | 3.5 | false |
| In a June 2026 controlled experiment (Project Fetch Phase 2), Claude Opus 4.7 autonomously completed robotics programming and sensor integration tasks 37x faster than a human team without AI and 18x faster than a human team with Claude assistance, producing 1,045 lines of code versus the Claude-assisted team's 10,309 — while failing at closed-loop physical control tasks (autonomous beach ball retrieval) that practiced humans could perform — illustrating that the autonomous AI threshold has been crossed for structured programming tasks but not yet for real-time perception-feedback-action loops. | [[2026-anthropic-project-fetch-phase-two]] | 2026-06-18 | current | 2 | false |

## What Drives Synergy — and What Doesn't

**Task type is a significant moderator.** Human-AI combinations show consistent performance losses on decision tasks — those in which participants choose among a finite set of options — and trend toward gains on creation tasks involving open-ended responses. The framing that dominates the research literature, in which AI provides a recommendation and humans make the final call, consistently underperforms AI working alone when the AI is more capable. Creation tasks (about 10% of the effect sizes studied) show the opposite pattern, pointing to generative AI collaboration as an underexplored avenue for achieving true synergy.

**Relative baseline performance is the strongest moderator.** When humans outperform AI alone, combinations achieve substantial synergy. When AI outperforms humans, combinations produce significant losses. The proposed mechanism is trust calibration: humans who are overall more accurate than the AI are also better at identifying which specific cases warrant relying on the algorithm versus their own judgment. When AI is more capable overall, humans lack the domain expertise to recognize when the AI is wrong — their participation degrades performance.

**AI explanations and confidence scores do not improve performance.** Both factors have received substantial research attention on the premise that transparency helps humans calibrate trust. Across 300+ effect sizes, neither explanations nor confidence indicators significantly moderated human-AI synergy or augmentation. This finding suggests the field may be overinvesting in explainability features relative to the higher-impact design variables — task type and relative performance — which have received less research attention.

## Behavioral Failure Modes

Two behavioral failure modes explain much of the performance loss pattern:

**Overreliance** occurs when humans use AI suggestions as strong guidelines without seeking or processing additional information, even in cases where the AI is wrong. This is especially acute when the AI outperforms the human overall — because the human correctly learns that the AI is generally better, they incorrectly extend that general accuracy to individual cases where the AI errs.

**Underreliance** occurs when humans ignore valid AI recommendations due to adverse attitudes toward automation. Unlike overreliance, this pattern reduces even the augmentation benefit — humans fail to capture value the AI could provide because they discount its output regardless of quality.

Both failure modes are calibration problems rather than directional biases. The challenge is not that humans systematically over- or underweight AI, but that they lack reliable signals for knowing when to defer and when to override. See [[human-ai-collaboration-pitfalls]] for failure mode entries and mitigation guidance.

## Process Design as the Underexplored Lever

Only 3 of 106+ experiments in the meta-analysis studied task division — the explicit assignment of different subtasks to the human or AI based on which partner performs better at each. These experiments found positive average synergy (g = 0.22), though the result was not statistically significant given the small sample. The authors argue that designing innovative processes for how to combine humans and AI may be as important as the technology itself: synergy requires that humans be better at some parts of the task, AI be better at other parts, and the system correctly allocate subtasks to the stronger partner.

Large-scale agentic coding data from approximately 400,000 real Claude Code sessions (Hitzig et al. 2026) provides the most direct real-world evidence for this mechanism. The natural division that emerges in practice — users making approximately 70% of planning decisions and Claude making approximately 80% of execution decisions — shows that task division structures itself spontaneously when users bring domain expertise. Domain expertise amplifies the benefit: expert users generate 12 Claude actions per prompt versus 5 for novice users, consistent with the prediction that synergy scales with the human's relative competence at strategic and planning work. Every major occupation succeeds within 7 percentage points of software engineers in code-producing sessions, indicating the benefit is available across domains rather than restricted to technical users. See [[anthropic-claude-code]] for the full session dataset.

## Scope and Limitations

The meta-analysis is limited to published experiments reporting performance for human-only, AI-only, and human-AI conditions — excluding tasks that neither partner can perform alone. Potential publication bias exists for the augmentation measure (studies showing human-AI combinations beating humans alone may be more likely to be published), though tests show no evidence of publication bias for the synergy measure. High heterogeneity (I² = 97.7% for synergy) means the average effect conceals substantial variation: specific combinations of task type, baseline performance, and process design produce results well above and below the average. The literature also under-represents creation tasks and structured task-division designs, limiting generalizability to the most promising collaboration architectures.

## Teaching Notes

**Concept in plain terms.** Adding AI assistance to human work is not the same as combining the best of both. Most human-AI systems improve on what the human could do alone, but fail to outperform what the AI could do alone — or what the human alone could do when the human is the stronger performer. Whether combining helps or hurts depends primarily on which partner is better at the task and what kind of task it is.

**Why it matters for instruction.** The prevailing narrative frames AI collaboration as uniformly beneficial. This meta-analysis shows that framing is empirically wrong for decision tasks and especially wrong when humans are the weaker performer. Instructors helping learners develop AI workflow skills need to teach calibrated adoption: match the collaboration design to the task type, and be explicit about which partner has superior accuracy on which subtasks.

**Common misconceptions.** Learners assume AI explanations and confidence scores help them calibrate trust. Experimental evidence shows neither factor significantly improves performance. What matters is whether the human brings genuine expertise to the task, and whether the workflow assigns different subtasks to the better-suited partner rather than having both perform the whole task.

**Suggested framing.** Open with the synergy/augmentation distinction. Ask learners to identify one task where they outperform the AI, and one where the AI outperforms them — then trace what the evidence predicts for each collaboration scenario, and what that implies for how to design the workflow.
