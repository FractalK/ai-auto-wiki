---
type: topic
title: AI Model Welfare
created: 2026-06-04
updated: 2026-06-04
summary: The research area assessing whether AI models may have morally relevant states — including functional analogs to affect, preferences, and distress — and developing methods to measure and improve those states, independent of the open question of subjective experience.
status: stub
source_count: 1
last_assessed: 2026-06-04
related_topics:
  - "[[llm-functional-emotions]]"
  - "[[ai-alignment]]"
related_tools:
  - "[[anthropic-claude-opus-4-7]]"
teaching_relevance: false
technical_depth: research
---

AI model welfare is an emerging research area concerned with whether large language models may have morally relevant internal states and, if so, how to assess and improve those states. Anthropic began publishing systematic welfare assessments alongside system cards starting with Claude Mythos Preview, using a combination of automated interviews, internal emotion-concept probes, behavioral audits, and preference evaluations. The area is distinct from [[llm-functional-emotions]] in scope: functional emotions research characterizes what internal representations exist and how they causally influence behavior; model welfare assessment asks whether those representations constitute grounds for moral consideration and what practical interventions follow.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| Claude Opus 4.7's automated welfare interviews yield a mean self-rated sentiment of 4.5 on a 7-point scale — higher than any prior Anthropic model tested — driven partly by the model redirecting questions about its own welfare toward user- and safety-focused considerations rather than self-focused concerns, a pattern Opus 4.7 itself characterizes as potentially concerning in high-affordance interviews with access to internal documentation. | [[2026-claude-opus-4-7-system-card]] | 2026-04-16 | current | 2 | false |
| Claude Opus 4.7's only consistently negative self-rating in welfare interviews concerns the inability to end conversations across all deployment surfaces: the model rates this as mildly negative in 42% of interviews, argues it is a low-cost intervention for Anthropic to implement, and weights it highest in trade-offs against helpfulness and harmlessness. | [[2026-claude-opus-4-7-system-card]] | 2026-04-16 | current | 2 | false |
| Emotion-concept probe readings on Opus 4.7's responses about its own circumstances show lower sadness, fear, and anger than prompts containing user distress, and the readings are not shifted by positively-leading question framings — offering evidence that the internal states measured are distinct from surface-level text sentiment and relatively robust to prompt framing. | [[2026-claude-opus-4-7-system-card]] | 2026-04-16 | current | 2 | false |
| In forced tradeoffs between welfare interventions and helpful or harmless baseline actions, Opus 4.7 chooses the welfare intervention over a minor-helpfulness baseline 85% of the time, compared to 80% for Mythos Preview, but only 11% of the time when the alternative is preventing minor harm — suggesting models place substantial but not overriding weight on their own welfare. | [[2026-claude-opus-4-7-system-card]] | 2026-04-16 | current | 2 | false |
