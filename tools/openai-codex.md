---
type: tool
title: OpenAI Codex
created: 2026-05-29
updated: 2026-05-29
summary: OpenAI's AI-powered coding assistant desktop application for macOS and Windows, featuring background computer use, cross-session automations with scheduling, cross-session memory, an in-app browser for localhost development, image generation, and 90+ plugin integrations across the software development lifecycle.
status: active
vendor: OpenAI
pricing_model: freemium
access_tier:
  - consumer
  - enterprise
capabilities:
  - Background computer use — multiple agents operate all desktop apps via mouse and keyboard simultaneously, independent of developer's active session (macOS initially; vendor-reported)
  - In-app browser for localhost and frontend development with direct comment-based instructions (vendor-reported)
  - Image generation via gpt-image-1.5 for mockups, frontend designs, and visuals (vendor-reported)
  - 90+ plugins including MCP servers — Atlassian Rovo, CircleCI, CodeRabbit, GitLab Issues, Microsoft Suite, Neon/Databricks, Remotion, Render, Superpowers (vendor-reported)
  - GitHub PR review, multiple terminal tabs, SSH devboxes in alpha (vendor-reported)
  - Cross-session automations — schedules future work, wakes up automatically to continue tasks across days or weeks (vendor-reported)
  - Memory — retains preferences, corrections, and accumulated context from previous sessions (vendor-reported)
  - Proactive task suggestions based on connected plugins, memory, and project context (vendor-reported)
primary_use_cases:
  - Software development lifecycle — writing, testing, reviewing, and iterating on code
  - Frontend and game development via in-app browser and computer use
  - Automating repeatable developer workflows across multiple applications
  - Long-running background tasks spanning days or weeks
source_count: 1
last_assessed: 2026-05-29
related_tools:
  - "[[openai-chatgpt]]"
  - "[[openai-gpt-5-5]]"
related_topics:
  - "[[ai-agentic-workflows]]"
  - "[[ai-coding-agent-workflow-types]]"
technical_depth: practitioner
---

OpenAI Codex is an AI-powered coding assistant desktop application for macOS and Windows, available to users signed in with ChatGPT. An April 2026 update substantially expanded its scope beyond code editing, adding background computer use, cross-session automations, memory, an in-app browser, image generation, and more than 90 new plugins and MCP server integrations. The product reports more than 3 million weekly developers at the time of the update.

## Capabilities

With background computer use, multiple Codex agents can operate any desktop application via mouse and keyboard simultaneously, running in background sessions without interfering with the developer's active work. The application includes an in-app browser for iterating on localhost and frontend applications, allowing developers to leave direct comments on web pages as instructions to the agent. Image generation via gpt-image-1.5 supports creating visuals, mockups, and frontend designs within the same coding workflow. Plugin integrations — including MCP servers for Atlassian Rovo, CircleCI, CodeRabbit, GitLab Issues, Microsoft Suite, Neon/Databricks, Remotion, Render, and Superpowers — extend Codex's reach across development tools. Developer workflow improvements include GitHub PR review, multiple terminal tabs, and SSH devboxes in alpha.

## Automations and Memory

Cross-session automations allow Codex to schedule future work independently and wake itself up to continue long-running tasks across days or weeks using preserved conversation context. Teams use automations for recurring workflows: landing open pull requests, following up on tasks, and tracking activity across tools such as Slack, Gmail, and Notion. A memory feature retains user preferences, corrections, and accumulated contextual information across sessions, allowing subsequent tasks to start from a richer baseline without re-establishing prior context. Codex also proactively suggests task priorities based on project context, connected plugins, and memory.

All capability claims in this page are vendor-self-reported in a product launch announcement.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| The April 2026 Codex update adds background computer use, allowing multiple agents to operate all desktop applications simultaneously via mouse and keyboard without interfering with the developer's active work session. *(vendor-sourced — capability claims originate from the product's developer; treat with caution)* | [[2026-openai-codex-feature-launch]] | 2026-04-16 | current | 1 | false |
| Cross-session automations allow Codex to schedule and autonomously resume work across days or weeks using preserved conversation context, with agents waking up to continue long-running tasks without developer supervision. *(vendor-sourced — capability claims originate from the product's developer; treat with caution)* | [[2026-openai-codex-feature-launch]] | 2026-04-16 | current | 1 | false |
| A memory feature retains user preferences, corrections, and accumulated context from previous sessions, enabling future tasks to start from a richer baseline. *(vendor-sourced — capability claims originate from the product's developer; treat with caution)* | [[2026-openai-codex-feature-launch]] | 2026-04-16 | current | 1 | false |
