---
type: tool
title: Google Gemini 3.5 Flash
created: 2026-05-28
updated: 2026-08-14
summary: Google's frontier agentic model in the Flash speed tier, optimized for multi-step task execution, multi-agent coordination via the Antigravity harness, and coding workflows, with vendor-reported benchmark performance claimed to exceed Gemini 3.1 Pro and rival larger frontier models at lower latency and cost.
status: active
vendor: Google
pricing_model: usage-based
access_tier:
  - consumer
  - prosumer
  - enterprise
  - api
capabilities:
  - 'Multi-step agentic task planning and execution with long-horizon context'
  - 'Multi-agent coordination via Google Antigravity harness for parallel subagent deployment'
  - 'Code generation, codebase maintenance, and iterative software development'
  - 'Multimodal input and interactive web UI generation'
  - 'MCP integration for connecting to external tools and data sources'
  - 'Personal AI agent operations via Gemini Spark (24/7 autonomous action under user direction)'
limitations:
  - 'All benchmark scores are vendor-reported; no independent verification available in current sources'
  - 'Speed and cost claims (4x output speed, <50% cost vs. frontier models) are vendor-stated and unverified'
  - 'Frontier Safety Framework compliance is self-reported; CBRN and cyber safeguard effectiveness not independently assessed'
  - 'Gemini Spark was in limited beta (trusted testers only) as of May 2026'
primary_use_cases:
  - 'Agentic automation of complex multi-step and long-horizon workflows'
  - 'Enterprise coding at scale via Antigravity multi-agent coordination'
  - 'Financial document preparation and compliance workflow automation'
  - 'Consumer personal AI agent via Gemini app'
source_count: 1
last_assessed: 2026-05-28
related_tools:
  - "[[anthropic-claude-opus-4-7]]"
  - "[[openai-gpt-5-5]]"
---

Gemini 3.5 Flash is Google's first release in the Gemini 3.5 model family, announced May 19, 2026 at Google I/O. It is positioned as a model combining frontier intelligence with the speed and cost profile of the Flash tier — Google's designation for models optimized for high-throughput, low-latency deployment. According to Google, 3.5 Flash outperforms Gemini 3.1 Pro on agentic and coding benchmarks and is available to billions of users via the consumer Gemini app, Google AI Studio, Android Studio, and the Gemini Enterprise Agent Platform.

The model is designed for agentic workflows requiring multi-step reasoning and tool use at scale. When paired with Google's Antigravity harness, 3.5 Flash supports parallel deployment of collaborative subagents — enabling workflows that would previously require days of human effort to complete in a fraction of the time, according to vendor-reported case studies from Shopify and financial services clients. The model supports MCP for connectivity to external tools and data sources, aligning with the emerging agentic interoperability standards.

All performance claims are sourced from Google's product blog post (vendor-reported) and should be treated accordingly. No independent benchmark evaluation of Gemini 3.5 Flash performance is available in this wiki's current source set.

## Data Records

| Metric | Value | Conditions | Measurement Date | Source | Status |
|---|---|---|---|---|---|
| Terminal-Bench 2.1 | 76.2% | Vendor-reported; real terminal tasks; compared against Gemini 3.1 Pro as baseline | 2026-05 | [[2026-google-gemini-3-5-flash-announcement]] | current |
| GDPval-AA | 1656 Elo | Vendor-reported agentic task evaluation; compared against frontier models | 2026-05 | [[2026-google-gemini-3-5-flash-announcement]] | current |
| MCP Atlas | 83.6% | Vendor-reported multi-agent and MCP benchmark | 2026-05 | [[2026-google-gemini-3-5-flash-announcement]] | current |
| CharXiv Reasoning | 84.2% | Vendor-reported multimodal reasoning benchmark | 2026-05 | [[2026-google-gemini-3-5-flash-announcement]] | current |

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| Google reports Gemini 3.5 Flash outperforms Gemini 3.1 Pro on agentic and coding benchmarks including Terminal-Bench 2.1 (76.2%), MCP Atlas (83.6%), and CharXiv Reasoning (84.2%) — all vendor-measured with no independent corroboration in available sources. | [[2026-google-gemini-3-5-flash-announcement]] | 2026-05-19 | current | 1 | false |
| Google claims Gemini 3.5 Flash delivers output at 4x the tokens-per-second of "other frontier models" and completes agentic tasks at less than half the cost — vendor-stated speed and cost comparisons without identified comparison baselines or independent verification. | [[2026-google-gemini-3-5-flash-announcement]] | 2026-05-19 | current | 1 | false |
| Gemini 3.5 Flash supports collaborative multi-agent deployment via Google's Antigravity harness, enabling parallel subagent execution for complex long-horizon enterprise tasks. | [[2026-google-gemini-3-5-flash-announcement]] | 2026-05-19 | current | 1 | false |
| Gemini 3.5 Flash powers Gemini Spark, Google's personal AI agent designed to run 24/7 and take autonomous action in users' digital environments under user direction — in limited beta as of May 2026. | [[2026-google-gemini-3-5-flash-announcement]] | 2026-05-19 | current | 1 | false |
| Google reports that Gemini 3.5 Flash was developed under its Frontier Safety Framework with vendor-stated improvements to cyber and CBRN safeguards through interpretability tools applied to model reasoning before generating responses. | [[2026-google-gemini-3-5-flash-announcement]] | 2026-05-19 | current | 1 | false |
