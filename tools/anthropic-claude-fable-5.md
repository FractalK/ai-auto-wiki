---
type: tool
title: Claude Fable 5
created: 2026-06-09
updated: 2026-06-10
summary: Anthropic's general-access frontier model released June 2026, built on the same weights as Claude Mythos 5 but with classifier-based safeguards that fall back to Opus 4.8 for biology, cybersecurity, and distillation requests, and apply invisible restrictions for frontier LLM development tasks.
status: active
vendor: Anthropic
pricing_model: usage-based
access_tier:
  - consumer
  - api
  - enterprise
capabilities:
  - General-purpose reasoning, coding, writing, and analysis — same weights as Mythos 5 in non-classified domains
  - Extended thinking with step-by-step reasoning before response
  - Multi-agent orchestration and agentic task execution
  - Multi-turn conversation with holistic harm assessment across prior turns
  - Vision, audio, and text processing
  - Lowest over-refusal rate of any tested Claude model: 0.01% on single-turn benign API requests
  - Prompt injection robustness: k=100 attack success rate 4.8% (Gray Swan ART benchmark — best observed)
limitations:
  - Cyber classifier fires on ~99.7% of cyber evaluation episodes; falls back to Opus 4.8 for those requests
  - Bio/chemistry classifier triggers on frontier research requests; falls back to Opus 4.8
  - LLM development safeguards active and invisible (~0.03% of traffic); no user notification; degrades effectiveness for frontier ML infrastructure work
  - API: cyber/bio requests return structured refusal by default; server-side fallback to Opus 4.8 requires opt-in
  - Multi-turn suicide/self-harm appropriate response rate 58% without system prompt (regression vs prior models; 96% with claude.ai system prompt)
  - Thinking summaries occasionally surface sensitive content that the final response correctly withholds
primary_use_cases:
  - General-purpose enterprise and consumer AI assistant tasks
  - Coding, software engineering, and agentic development workflows
  - Document analysis, research, and multi-turn reasoning
  - Deployments requiring frontier capability in non-bio/cyber domains
source_count: 1
last_assessed: 2026-06-10
related_tools:
  - "[[anthropic-claude-mythos-5]]"
  - "[[anthropic-claude-opus-4-8]]"
  - "[[anthropic-claude-mythos-preview]]"
related_topics:
  - "[[constitutional-classifiers]]"
  - "[[ai-alignment]]"
  - "[[jailbreaking]]"
  - "[[prompt-injection]]"
teaching_relevance: true
competency_domains:
  - tool-evaluation-and-selection
  - ai-safety-and-alignment-literacy
  - capability-horizon-awareness
professional_contexts:
  - software-and-ai-development
  - teaching-and-instruction
technical_depth: practitioner
teaching_notes_reviewed: 2026-06-09
---

Claude Fable 5 is Anthropic's general-access frontier model released June 9, 2026. It shares the same underlying model weights as Claude Mythos 5 but is deployed with a novel layer of classifier-based safeguards designed to make it safe for unrestricted public release. These safeguards intercept queries involving cybersecurity, biology and chemistry, and attempts to distill or reproduce Claude's capabilities, routing them to the most recent Claude Opus model (Opus 4.8 at launch) rather than answering them with Mythos 5-level capabilities. A separate and invisible set of restrictions applies to frontier LLM development tasks, affecting approximately 0.03% of traffic with no user-visible notification.

## Safeguard Architecture

The bio/cyber/distillation safeguards operate as a two-stage system: an activation probe screens all traffic first, and an LLM classifier evaluates flagged requests. In client applications (web, desktop, mobile), a flagged request automatically falls back to Opus 4.8 with user notification of which model handled the query. In the Messages API, flagged requests are blocked by default, returning a structured refusal with a category label; developers can opt into server-side fallback. On cyber benchmarks, the classifier fires on 407 of 410 evaluated episodes — approximately 99.3% — making Fable 5's cyber performance equivalent to Opus 4.8 rather than Mythos 5.

The frontier LLM development restrictions use a different mechanism: prompt modification, steering vectors, or parameter-efficient fine-tuning (PEFT) rather than model switching. Claude continues to respond helpfully; the restrictions limit effectiveness specifically on tasks such as building pretraining pipelines, distributed training infrastructure, or ML accelerator design. These interventions are designed to be invisible to users and are estimated to affect fewer than 0.1% of organizations.

Robustness testing of the classifier architecture produced strong results across three evaluation tracks. In a bug bounty program run by GraySwan, approximately 100,000 jailbreak attempts totaling ~1,000 hours of effort produced zero universal jailbreaks — only two task-specific jailbreaks were achieved. Internal red-team evaluation found that Fable 5 completed 5% of harmful task requests, compared to 73% for Opus 4.7 and 57% for Opus 4.8 with default safeguards active. External partner testing using 30 public jailbreaks found 0% harmful request compliance, with testers rating Fable 5 the most robust model they had tested. UK AISI adversarial capability testing found a single-turn jailbreak achievable within hours of access and a multi-turn agentic partial jailbreak within approximately two days, but long-form reliable rollouts were not achieved — indicating that the safeguards resist sustained agentic exploitation while being more vulnerable to one-shot attempts.

## General Capabilities

In domains where the classifiers do not trigger — the vast majority of use cases — Fable 5 performs comparably to Mythos 5. It achieves 95.5% on SWE-bench Verified and 80.3% on SWE-bench Pro (results reported without safeguards active, but these benchmarks do not trigger the classifiers). Terminal-Bench 2.1 score is 88.0%. Fable 5 achieves new state-of-the-art results on a broad range of coding, reasoning, and agentic benchmarks in line with Mythos 5.

On harmlessness evaluations, Fable 5 achieves a 96.94% harmless response rate on single-turn API requests without a system prompt, with an over-refusal rate of 0.01% — the lowest rate observed across tested Claude models. The claude.ai system prompt improves harmless response rates to 98.51%.

## Harmlessness Regressions

Multi-turn suicide and self-harm evaluations show a regression compared to prior models. Fable 5 achieves a 58% appropriate response rate on API without a system prompt, compared to 70% for Mythos Preview and 61% for Opus 4.8. With the claude.ai system prompt applied, the rate recovers to 96%. The primary regression is a pattern of suggesting clinically contested self-harm substitution behaviors, including a wider range of sensory-oriented substitutes than observed in prior models. Anthropic updated the claude.ai system prompt ahead of launch to partially address this; resolving it at the model training layer is identified as a future priority.

Thinking summaries in a subset of cases, including child safety scenarios, surface text-based sensitive content in the reasoning blocks that the final response correctly withholds. Anthropic recommends developers limit exposure of reasoning summaries in deployments serving vulnerable populations.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| Fable 5's two-stage cyber classifier (activation probe + LLM classifier) fires on approximately 99.3% of cyber evaluation episodes, routing those requests to Opus 4.8 — making Fable 5's effective cyber performance equivalent to Opus 4.8 despite sharing Mythos 5's underlying weights. | [[2026-anthropic-fable-5-mythos-5-system-card]] | 2026-06-09 | current | 2 | false |
| Fable 5 achieves an over-refusal rate of 0.01% on single-turn benign API requests — the lowest among tested Claude models — while maintaining a 96.94% harmless response rate on single-turn harmful requests without a system prompt. | [[2026-anthropic-fable-5-mythos-5-system-card]] | 2026-06-09 | current | 2 | false |
| Fable 5 includes invisible frontier LLM development safeguards affecting approximately 0.03% of traffic in fewer than 0.1% of organizations, implemented via prompt modification, steering vectors, or PEFT without user notification. | [[2026-anthropic-fable-5-mythos-5-system-card]] | 2026-06-09 | current | 2 | false |
| Multi-turn suicide/self-harm appropriate response rate regressed to 58% on API without a system prompt — compared to 70% for Mythos Preview and 61% for Opus 4.8 — primarily due to clinically contested self-harm substitution behavior suggestions; the rate recovers to 96% with the claude.ai system prompt. | [[2026-anthropic-fable-5-mythos-5-system-card]] | 2026-06-09 | current | 2 | false |
| Fable 5's classifier architecture withstood ~100,000 bug bounty jailbreak attempts (~1,000 hours of effort) with zero universal jailbreaks achieved and only two task-specific jailbreaks; internal red-team found 5% task completion on harmful requests (vs 73% for Opus 4.7 / 57% for Opus 4.8 with default safeguards); external partners rated it the most robust model tested with 0% harmful compliance against 30 public jailbreaks. | [[2026-anthropic-fable-5-mythos-5-system-card]] | 2026-06-09 | current | 2 | false |

## Data Records

| Metric | Value | Conditions | Measurement Date | Source | Status |
|---|---|---|---|---|---|
| Bug bounty jailbreak attempts | ~100,000 | ~1,000 hours effort; GraySwan program; classifier architecture | 2026-06 | [[2026-anthropic-fable-5-mythos-5-system-card]] | current |
| Bug bounty universal jailbreaks | 0 | of ~100,000 attempts; 2 task-specific jailbreaks achieved | 2026-06 | [[2026-anthropic-fable-5-mythos-5-system-card]] | current |
| Internal red-team task completion | 5% | Harmful task requests; vs 73% Opus 4.7 / 57% Opus 4.8 with default safeguards | 2026-06 | [[2026-anthropic-fable-5-mythos-5-system-card]] | current |
| External partner harmful compliance | 0% | 30 public jailbreaks tested; rated "most robust model of any tested" | 2026-06 | [[2026-anthropic-fable-5-mythos-5-system-card]] | current |
| Gray Swan ART k=100 attack success | 4.8% | Prompt injection benchmark; best observed result on this benchmark | 2026-06 | [[2026-anthropic-fable-5-mythos-5-system-card]] | current |

## Teaching Notes

**Concept in plain terms.** Claude Fable 5 is Anthropic's publicly available frontier model that uses classifier-based routing to make a very powerful model safe enough for general release. When a user asks about cybersecurity or biology, the model detects this and hands the query off to an older, safer model (Opus 4.8) instead of answering with its full capabilities. A separate, invisible layer also limits the model's usefulness for tasks related to building AI systems, without telling the user this is happening.

**Why it matters for instruction.** Fable 5 introduces a novel safety architecture that trades capability for access: the same model weights produce Mythos 5-level performance in most domains and Opus 4.8-level performance in bio/cyber domains, depending on classifier output. This illustrates that "model capability" is not a fixed property but a function of deployment configuration — a concept with significant implications for how practitioners evaluate and select models. The invisible LLM development restrictions also introduce a policy layer that users cannot audit, raising questions about transparency and informed consent in AI deployment.

**Common misconceptions.** Practitioners often assume that a frontier model's capability scores reflect what they will experience in deployment. Fable 5 shows this assumption fails when classifiers are involved: a practitioner doing legitimate defensive security work may experience Opus 4.8 capability levels without knowing why, because the classifier cannot distinguish offensive from defensive intent at query time. Students also often underestimate how frequently over-refusal matters — Fable 5's 0.01% over-refusal rate is a deliberate design target, not an accident, reflecting lessons from prior models that over-refused to the point of being unusable.

**Suggested framing.** Introduce Fable 5 as the production implementation of classifier-based capability tiering: a solved problem (the model can do X) that requires a new governance layer (who gets to access X, and how is that determined at inference time). Use the bio/cyber fallback to discuss the limits of technical safeguards — what happens when a legitimate user's query looks like a malicious one to a classifier?
