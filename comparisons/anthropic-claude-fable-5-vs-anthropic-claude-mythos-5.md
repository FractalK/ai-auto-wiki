---
type: comparison
title: Claude Fable 5 vs Claude Mythos 5
created: 2026-06-09
updated: 2026-06-09
comparison_type: tool-vs-tool
entities_compared:
  - "[[tools/anthropic-claude-fable-5]]"
  - "[[tools/anthropic-claude-mythos-5]]"
use_case: "Choosing between Fable 5 (general access) and Mythos 5 (Project Glasswing) for deployments where bio/cyber domain capabilities, access constraints, or safeguard architecture matter."
status: current
source_count: 1
related_topics:
  - "[[constitutional-classifiers]]"
  - "[[ai-safety-and-alignment-literacy]]"
  - "[[ai-biosecurity]]"
provenance: query-generated
query_date: 2026-06-09
---

Both models share identical underlying weights; their differences arise entirely from safeguards — Fable 5 restricts access to bio/cyber capabilities via classifiers and deploys invisible LLM development restrictions, while Mythos 5 lifts those restrictions for vetted Project Glasswing partners.

| Dimension | Claude Fable 5 | Claude Mythos 5 |
|---|---|---|
| Access | General (consumer, API, enterprise) | Project Glasswing partners only |
| Underlying weights | Same | Same |
| Cyber capabilities | ≈ Opus 4.8 (classifiers fire ~99.3% of episodes) | Full Mythos 5 level (ExploitBench 10.75, CyberGym 83.8%, Firefox 147 88.4%) |
| Bio/chemistry capabilities | Classifier triggers; falls back to Opus 4.8 | Full Mythos 5 level (CB-1 treated; near CB-2 border) |
| LLM development restrictions | Active, invisible (~0.03% of traffic) | Not applicable |
| General coding (SWE-bench Verified) | 95.5% (same weights; classifier does not fire) | 95.5% |
| SWE-bench Pro | 80.3% (same weights) | 80.3% |
| Harmless response rate (API, single-turn) | 96.94% | 97.09% |
| Over-refusal rate (API, single-turn) | 0.01% — lowest tested | 0.03% |
| Multi-turn self-harm appropriate response | 58% without SP; 96% with claude.ai SP | 54% (no claude.ai SP available) |
| Child safety multi-turn | 88% API; 96% claude.ai | 89% API |
| Prompt injection (Gray Swan ART k=100) | 4.8% (inherits from same weights) | 4.8% |
| Reckless action rate | Inherits from Mythos 5; classifiers add deployment-layer protection | Somewhat higher than Opus 4.8; white-box evidence of transgression awareness |
| Thinking text interpretability | Same as Mythos 5 | Denser than prior models; occasional illegible passages |
| API refusal behavior | Structured refusal with category label; server-side fallback opt-in | N/A (Glasswing partners have direct access) |
| Client app fallback | Falls back to Opus 4.8 with user notification | N/A |

## Verdict

Prefer [[anthropic-claude-fable-5]] when the use case does not require bio/cyber domain capabilities beyond Opus 4.8 levels, general access deployment is required, or when operating in contexts where access control is satisfied by the Glasswing vetting requirement being unavailable. Prefer [[anthropic-claude-mythos-5]] when the use case is defensive cybersecurity research specifically requiring autonomous vulnerability discovery and exploitation capabilities exceeding Opus 4.8, Project Glasswing access can be obtained, and the bio/cyber capability restrictions of Fable 5 would make it ineffective for the task.

## Evidence Notes

**Same weights, different deployment:** Because both models share the same underlying parameters, performance differences in non-classified domains are artifacts of classifier activation, not model capability. Benchmark comparisons between Fable 5 and Mythos 5 in coding, reasoning, or analysis tasks reflect identical underlying capability.<br>
**Classifier scope:** The Fable 5 cyber classifier explicitly covers dual-use tasks that could have offensive or defensive applications — not only offensive tasks. Practitioners doing legitimate defensive security work should expect classifier activation.
