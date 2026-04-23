---
type: tool
title: Claude (Anthropic)
created: 2026-04-22
updated: 2026-04-22
summary: Anthropic's general-purpose AI assistant, available as a web app, desktop application, and API, with differentiated access tiers and a distinct agentic operating mode (Cowork) enabling autonomous multi-step task execution on local file systems.
status: active
vendor: Anthropic
pricing_model: freemium
access_tier:
  - consumer
  - prosumer
  - api
capabilities:
  - Long document processing (up to 200 pages per session)
  - Local file access via desktop application
  - Autonomous multi-step task execution via Cowork mode
  - Writing, editing, and voice adaptation from examples
  - Document summarization with page references
  - File creation and export (spreadsheets, presentations, PDFs) via Cowork
  - Step-by-step reasoning on complex multi-part problems
limitations:
  - No native image generation
  - No real-time information access without explicit search tool activation
  - Unreliable for precise calculations not executed through code
  - Context window fills in long conversations, degrading response quality
  - Voice interaction inferior to ChatGPT per practitioner evaluation (April 2026)
primary_use_cases:
  - Long document analysis and summarization
  - Writing, drafting, and voice adaptation
  - Autonomous file processing workflows via Cowork
  - Structured reasoning and decision support
source_count: 1
last_assessed: 2026-04-22
related_tools:
  - [[anthropic-claude-opus-4-7]]
  - [[openai-chatgpt]]
  - [[google-notebooklm]]
related_topics:
  - [[ai-agentic-workflows]]
teaching_relevance: true
competency_domains:
  - tool-evaluation-and-selection
  - practical-ai-use-and-interaction
professional_contexts:
  - professional-and-continuing-education
  - entrepreneurship-and-startups
  - teaching-and-instruction
technical_depth: foundational
---

Claude is Anthropic's general-purpose AI assistant, accessed through a browser interface, a desktop application (Mac and Windows), and an API. It operates through statistical pattern matching over large training datasets — predicting text continuations rather than retrieving facts — which means it produces confident-sounding output that may be incorrect, fabricated, or outdated. Understanding this underlying mechanism is the first step toward using Claude effectively.

## Access and Pricing

Three consumer tiers are available as of April 2026. The **Free** tier provides browser-only access with daily message limits and access to Claude's standard models — suitable for initial evaluation. The **Pro** tier ($20/month) provides access to the best available Claude model (Opus), Cowork, Claude Code, and Projects, with substantially higher usage limits; it is the recommended starting point for practitioners who plan to use Claude more than a few times per week. The **Max** tier ($100–200/month) provides heavy usage across all features without hitting limits, suited for daily intensive use. Team and Enterprise plans are available for organizational deployment.

A key decision point is mode of access: the browser interface provides a standard chatbot experience, while the desktop application unlocks Cowork and local file system access. Both Cowork and local file access require a paid plan and the desktop app.

## Operating Modes

**Browser (claude.ai):** Standard prompt-response chatbot. Works on the free plan and across all paid tiers. Suitable for drafting, summarizing, and one-off reasoning tasks.

**Desktop application:** Same account as the browser interface, installed locally. Enables local file access — Claude can read files in specified directories — and unlocks three modes: Chat, Cowork, and Code.

**Cowork:** Claude's agentic operating mode. The user specifies a task and a target folder; Claude plans steps, reads relevant files, produces output files (PDFs, spreadsheets, presentations, HTML), and asks clarifying questions autonomously over minutes to hours. Designed for non-developers — no coding required. Effectiveness increases when the target folder includes context about the user's work style, prior outputs, and reusable templates.

**Claude Code:** A terminal-based mode for developers to write, execute, and debug code. Not required for non-developers; Cowork covers the majority of file-handling use cases without it.

## Capabilities and Limitations

Claude's documented practitioner advantages include processing long documents (up to approximately 200 pages per session) without losing context, accessing local files directly via the desktop application, and executing multi-step autonomous tasks via Cowork without requiring custom technical setup.

Claude's documented limitations include the absence of native image generation (use ChatGPT or Gemini for image creation), unreliable real-time information access without activating the built-in web search tool, and degraded response quality in long conversations as the context window fills. The recommended practice when quality degrades is to start a fresh conversation and paste only the relevant context. Claude is also unreliable for precise arithmetic unless it runs code to compute the answer.

## Effective Use Practices

Prompting quality determines output quality more than model selection. Five practitioner principles: (1) specificity over generality — provide exactly the format, length, and context you need, not a vague goal; (2) examples over instructions — pasting a sample of desired output teaches Claude faster than describing it; (3) positive framing — specify what you want, not only what to avoid; (4) iterative refinement — start short, review, then add detail; (5) fresh conversations when quality degrades — restart with clean context rather than continuing a degraded session.

For Cowork, effectiveness increases with structured folder organization: an `about-me` subfolder with context about the user's role and preferences, an `outputs` subfolder for prior Cowork results, and a `templates` subfolder with examples of desired output formats.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| Anthropic's Claude is available in three consumer pricing tiers as of April 2026: Free (browser-only, limited messages), Pro ($20/month, includes Cowork and access to Opus), and Max ($100–200/month, heavy usage without limits). | [[2026-hassid-claude-beginners-guide]] | 2026-04-17 | current | 1 | false |
| Claude's Cowork mode enables autonomous task execution for minutes to hours, reading local files and producing output files (PDFs, spreadsheets, presentations) directly on the user's computer, accessible only via the paid desktop application. | [[2026-hassid-claude-beginners-guide]] | 2026-04-17 | current | 1 | false |
| Claude cannot generate images natively; it can analyze images but image creation requires external tools such as ChatGPT or Gemini. | [[2026-hassid-claude-beginners-guide]] | 2026-04-17 | current | 1 | false |
| Practitioner evaluation identifies Claude's primary advantages over ChatGPT as long document processing (up to 200 pages per session), local file system access via the desktop app, and multi-step autonomous task execution via Cowork. | [[2026-hassid-claude-beginners-guide]] | 2026-04-17 | current | 1 | false |
| Claude's context window fills with conversational history over long sessions, degrading response relevance; starting fresh conversations with pasted context is recommended when quality degrades. | [[2026-hassid-claude-beginners-guide]] | 2026-04-17 | current | 1 | false |
