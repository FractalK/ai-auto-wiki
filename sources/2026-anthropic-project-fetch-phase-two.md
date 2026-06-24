---
type: source
title: "Project Fetch: Phase Two"
created: 2026-06-23
updated: 2026-06-23
status: active
source_type: industry-blog
author:
  - "Michael Ilie"
  - "C. Daniel Freeman"
  - "Kevin K. Troy"
publication: Anthropic Research Blog
published_date: 2026-06-18
ingested_date: 2026-06-23
ingest_via: staged
url: https://www.anthropic.com/research/project-fetch-phase-two
credibility_tier: institutional
extraction_depth: standard
related_topics:
  - "[[human-ai-collaboration]]"
  - "[[ai-agentic-workflows]]"
related_tools:
  - "[[anthropic-claude-opus-4-7]]"
---

Anthropic researchers report that Claude Opus 4.7, operating autonomously in Claude Code without human assistance, completed robotics setup and programming tasks for an off-the-shelf robotic quadruped 37x faster than a human team without AI and 18x faster than a human team that used Claude in August 2024, while producing 1,045 lines of code compared to the Claude-assisted team's 10,309. The autonomous model's code was effective on the first try across most tasks and showed low within-task variance in completion time across three trials. The model failed at closed-loop physical control — precisely positioning a beach ball using the robot — a task that practiced human teams could accomplish manually, indicating the autonomous AI threshold has been crossed for structured programming and sensor integration tasks but not yet for real-time perception-feedback control. The authors note that these robotics capability improvements emerged from general-purpose model scaling rather than robotics-specific training, framing the result as the beginning of the physical agentic AI era, following the same trajectory seen earlier in software agentic AI.
