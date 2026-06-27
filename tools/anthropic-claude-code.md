---
type: tool
title: Anthropic Claude Code
created: 2026-06-16
updated: 2026-06-27
summary: Anthropic's CLI and desktop agentic coding tool, studied across approximately 400,000 sessions from 235,000 users (Oct 2025–Apr 2026), with consistent findings that domain expertise (not coding background) drives success, a natural human-planning/AI-execution task division, and approximately 27% growth in average session value over seven months as usage shifts toward higher-complexity work.
status: active
vendor: Anthropic
pricing_model: subscription
access_tier:
  - consumer
  - prosumer
capabilities:
  - Multi-step software development via CLI, Claude.ai, or desktop app
  - Nine work modes: building, fixing, testing, orchestrating, operating, understanding, planning, analyzing, communicating
  - Autonomous execution chains averaging 10 actions per user prompt, sometimes exceeding 100
  - Cross-session context via CLAUDE.md configuration files and memory
limitations:
  - Verified success rates 28–33% for expert sessions; 15% for novice sessions (strict measurement)
  - Novice users abandon approximately 19% of troubled sessions vs. 5–7% for experienced users
  - Study coverage excludes IDE extensions and headless/programmatic CLI usage
primary_use_cases:
  - Agentic software development and code generation
  - Debugging and code review
  - Data analysis and document generation
  - Orchestration of automated pipelines
source_count: 2
last_assessed: 2026-06-27
related_topics:
  - "[[ai-agentic-workflows]]"
  - "[[human-ai-collaboration]]"
  - "[[ai-workforce-complementarity]]"
  - "[[ai-economic-impact]]"
teaching_relevance: true
competency_domains:
  - practical-ai-use-and-interaction
  - ai-integration-in-organizational-workflows
  - capability-horizon-awareness
professional_contexts:
  - software-and-ai-development
  - professional-and-continuing-education
  - teaching-and-instruction
technical_depth: practitioner
teaching_notes_reviewed: 2026-06-16
---

Claude Code is Anthropic's agentic coding tool available as a CLI, Claude.ai interface, and desktop application, designed for directing an AI agent through multi-step software development tasks. Unlike traditional coding assistants that offer completions, Claude Code operates in a turn-based loop: the user sends a prompt and Claude autonomously reads files, writes code, runs commands, and verifies results — averaging 10 actions per turn and 2,400 words of output, before returning control to the user.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| In approximately 400,000 real-world Claude Code sessions, users make approximately 70% of planning decisions ('what to build') while Claude makes approximately 80% of execution decisions ('how to build it'), establishing task division — not capability substitution — as the dominant pattern in agentic coding practice. | [[2026-anthropic-agentic-coding-returns-expertise]] | 2026-06-16 | current | 2 | false |
| Domain expertise, not coding background, is the primary predictor of agentic coding session success: expert users generate 12 Claude actions per prompt versus 5 for novice users, and every major occupation succeeds in code-producing sessions at rates within 7 percentage points of software engineers — indicating agentic coding tools reward task-domain understanding over programming skill. | [[2026-anthropic-agentic-coding-returns-expertise]] | 2026-06-16 | current | 2 | false |
| Session composition shifted substantially over seven months (Oct 2025–Apr 2026): debugging fell from 33% to 19% of sessions while end-to-end agentic work (operating software, data analysis, writing) grew — indicating adoption is maturing from code-correction toward higher-complexity, higher-value work. | [[2026-anthropic-agentic-coding-returns-expertise]] | 2026-06-16 | current | 2 | false |
| The estimated value of the average Claude Code session rose approximately 27% from October 2025 to April 2026 (building +43%, operating +34%, fixing +32%), measured by comparison to freelance marketplace job postings, consistent with both model improvement and user expertise development over the study window. | [[2026-anthropic-agentic-coding-returns-expertise]] | 2026-06-16 | current | 2 | false |
| Novice-rated sessions are abandoned at 19% when hitting trouble (failed with zero code written), versus 5–7% for intermediate through expert sessions, while verified success rates are 15% for novice versus 28–33% for intermediate and expert — identifying domain expertise as both a quality amplifier and a failure recovery mechanism. | [[2026-anthropic-agentic-coding-returns-expertise]] | 2026-06-16 | current | 2 | false |

## Data Records

| Metric | Value | Conditions | Measurement Date | Source | Status |
|---|---|---|---|---|---|
| Claude actions per prompt — average | ~10 | Agentic coding sessions; Oct 2025–Apr 2026; geometric mean | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Claude actions per prompt — expert users | 12 | Geometric mean; expert-rated sessions | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Claude actions per prompt — novice users | 5 | Geometric mean; novice-rated sessions | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Claude output words per prompt — expert users | ~3,200 | Geometric mean | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Claude output words per prompt — novice users | ~600 | Geometric mean | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Verified success rate — novice sessions | 15% | Judged successful + at least one hard verifiable signal | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Verified success rate — intermediate through expert sessions | 28–33% | Same methodology | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Abandoned session rate — novice (when hitting trouble) | 19% | Failed + zero lines of code written; trouble = failure signal > 3 | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Abandoned session rate — intermediate through expert (when hitting trouble) | 5–7% | Same methodology | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Share of sessions — debugging (fixing) | 19% | April 2026; down from 33% in October 2025 | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Share of sessions — operating software | 21% | April 2026; up from 14% in October 2025 | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Average session value growth | +27% | Oct 2025 to Apr 2026; estimated from freelance job posting comparison | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Session value growth — building tasks | +43% | Same methodology | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Session value growth — operating tasks | +34% | Same methodology | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Session value growth — fixing tasks | +32% | Same methodology | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Verified success gap — software vs. other occupations | 5pp | 34% (software) vs. 29% (non-software); code-producing sessions; every occupation within 7pp | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| Average Claude Code usage | 20 hours/week | Hours Claude Code actively running; not hands-on time; ~235,000 users | 2026-04 | [[2026-anthropic-agentic-coding-returns-expertise]] | current |
| AI autonomy gap — Claude Code vs. chat/Cowork (average) | 0.37 points | 1–5 autonomy scale; 26 of 31 output types; Apr–Jun 2026; chat & Cowork vs. Claude Code surface | 2026-06 | [[2026-anthropic-economic-index-cadences]] | current |
| AI autonomy gap — Sonnet-model-controlled (Claude Code vs. chat/Cowork) | 0.26 points | Same scale; subset of Sonnet-served conversations only; demonstrates surface effect independent of model choice | 2026-06 | [[2026-anthropic-economic-index-cadences]] | current |
| Opus serving share — Claude Code | 54% | Share of Claude Code conversations served by Opus; Apr–Jun 2026 | 2026-06 | [[2026-anthropic-economic-index-cadences]] | current |
| Opus serving share — chat/Cowork | 10% | Share of chat and Cowork conversations served by Opus; same period | 2026-06 | [[2026-anthropic-economic-index-cadences]] | current |
| Median human prompts per blog/article — Claude Code | 1 | Conversations producing blog post or article output; median human turns; Apr–Jun 2026 | 2026-06 | [[2026-anthropic-economic-index-cadences]] | current |
| Median human prompts per blog/article — chat/Cowork | 13 | Same output type; chat or Cowork surface; same period | 2026-06 | [[2026-anthropic-economic-index-cadences]] | current |

## The Division of Labor in Practice

The most consistent finding across the 400,000-session study is a stable natural division of labor: humans direct planning (approximately 70% of planning decisions) and Claude handles execution (approximately 80% of execution decisions). This division is not enforced by the tool's design — it emerges from how users and the agent interact. Users set goals, define scope, and evaluate outcomes; Claude selects files to edit, writes code, chooses commands, and iterates toward the user's specification.

Domain expertise amplifies this division. Expert users issue more precise instructions, enabling Claude to operate with longer autonomous chains before requiring course correction. The result is higher output per prompt (12 actions and 3,200 words for expert versus 5 actions and 600 words for novice), not because the expert works more slowly, but because their precision allows Claude to confidently extend its execution chains. This pattern holds within every work mode and every task value band, ruling out task selection as a confound.

A June 2026 companion analysis from the Anthropic Economic Index compares autonomy levels across product surfaces, finding that Claude Code elicits higher AI autonomy than chat or Cowork across 26 of 31 output types — an average 0.37-point gap on the 1–5 autonomy scale. The gap persists at 0.26 points when controlling for model (comparing only Sonnet-served conversations), indicating that the product surface itself — not the underlying model — is the primary driver. The mechanism is both compositional and behavioral: a blog post produced on chat involves a median of 13 rounds of back-and-forth, while the same output on Claude Code involves a median of 1 human prompt. Claude Code's structural design as an agentic tool fundamentally changes the degree to which users delegate, independent of which Claude model underlies the session.

## Work Mode Evolution

The composition of Claude Code sessions changed substantially between October 2025 and April 2026. The most significant shift is the halving of debugging sessions (33% to 19%), replaced by growth in operating software (14% to 21%) and in writing and data analysis (combined roughly doubling from 10% to 20%). This shift is consistent with models improving at debugging over the study window, shifting that work earlier in the development cycle and freeing session time for more complex activities.

The fastest-growing non-software occupation groups are management, sales, and legal — indicating expansion into professional domains with strong task-domain expertise but no coding background. This corroborates the occupation-agnostic success rate finding: the tool's value is increasingly accessed by professionals whose expertise is in their domain, not in programming.

## Teaching Notes

**Concept in plain terms.** Claude Code is Anthropic's command-line and desktop tool for directing an AI agent through software development tasks. Users describe what to build; Claude decides how and executes autonomously — reading files, writing code, running commands — until the task is complete or it needs guidance. The key finding from large-scale study is that domain expertise, not coding skill, determines how well this works.

**Why it matters for instruction.** Claude Code is the most extensively studied real-world agentic coding tool, with 400,000 sessions providing direct empirical evidence about who uses AI coding agents, how, and with what success. For instructors teaching AI-augmented knowledge work, it provides concrete data for key pedagogical claims: that domain expertise matters more than technical background, that occupation is less predictive of success than task-domain understanding, and that the economic value of work done with AI tools is growing rapidly as models improve.

**Common misconceptions.** Instructors often assume agentic coding tools primarily benefit software engineers. The data show that management, legal, business, and science occupations all succeed at rates within 7 percentage points of software engineers — the tool is substantially occupation-agnostic. A second misconception is that more sophisticated users simply 'use AI more'; the actual mechanism is that experts issue higher-quality instructions, enabling Claude to do more work per prompt and recover from errors more effectively without user intervention.

**Suggested framing.** Introduce Claude Code as a case study in the human-planning/AI-execution division of labor: humans provide task-domain knowledge and define what to build, Claude handles implementation decisions. Use the novice/expert success differential (15% vs. 28–33% verified) to ground the argument that AI tools amplify expertise rather than substitute for it — and the occupation-success data to challenge the assumption that software engineers have a structural advantage in using these tools.
