---
type: tool
title: DeepSeek V4-Pro
created: 2026-06-04
updated: 2026-06-04
summary: DeepSeek's frontier open-weight model as of April 2026, a 1.6T-parameter Mixture-of-Experts model (49B active per token) with MIT license, 80.6% SWE-bench Verified score, and API pricing at approximately one-ninth of GPT-5.5 output token cost — text-only at launch.
status: active
vendor: DeepSeek
pricing_model: usage-based
access_tier:
  - api
capabilities:
  - 80.6% SWE-bench Verified (per model card, vendor-reported)
  - 1M token context window
  - MoE hybrid attention optimized for long-context inference FLOPs and KV cache reduction
  - MIT open weights deployable on self-hosted infrastructure with sufficient capacity
  - Agent tool integration (noted by DeepSeek as optimized for Claude Code, OpenClaw)
limitations:
  - Text-only at launch; multimodal capabilities stated as in progress
  - 1.6T total parameters require significant inference infrastructure for self-hosting
  - Launch discount (through 2026-05-05) may not reflect long-term pricing
primary_use_cases:
  - Agentic coding and software engineering tasks
  - High-volume API inference where output token cost is the binding constraint
  - Self-hosted deployment for organizations with large-scale infrastructure
source_count: 1
last_assessed: 2026-06-04
related_tools:
  - "[[deepseek-v4-flash]]"
  - "[[openai-gpt-5-5]]"
  - "[[anthropic-claude-opus-4-7]]"
technical_depth: practitioner
---

DeepSeek V4-Pro is DeepSeek's frontier open-weight model released April 24, 2026, positioned as a near-frontier alternative to closed-source premium models at a substantially lower API cost. It is available via the DeepSeek API and as open weights on Hugging Face under the MIT license, enabling commercial deployment without restrictions.

## Architecture

V4-Pro is a Mixture-of-Experts model with 1.6 trillion total parameters and 49 billion active parameters per token. Its hybrid attention scheme combines compressed sparse attention with heavily compressed attention, designed to reduce 1M-token inference FLOPs and KV cache size — enabling near-frontier benchmark performance while activating a small fraction of total weights per forward pass. This architectural efficiency is the primary driver of the cost differential with dense frontier models.

## Performance and Pricing

V4-Pro achieves 80.6% on SWE-bench Verified per the model card — within striking distance of leading closed-source frontier models — at an API list price of \$1.74 per million input tokens and \$3.48 per million output tokens. A launch discount applied through May 5, 2026. At list price, V4-Pro output tokens cost approximately one-ninth of GPT-5.5's \$30 per million output tokens. The 1M token context window matches the default context of OpenAI's and Anthropic's flagship models.

V4-Pro is text-only at launch. DeepSeek has stated that multimodal capabilities are in progress, but image and video reasoning are not currently supported. For workloads requiring multimodal input, V4-Pro is not a drop-in alternative to GPT-5.5 or Claude Opus 4.6.

## Hardware Context

Huawei announced on the same day as the V4 release that its Ascend supernodes offer full support for V4 inference. DeepSeek did not state whether V4-Pro was trained on Huawei Ascend hardware (in contrast to V4-Flash, which Huawei stated used Ascend chips for part of training). Prior DeepSeek models (V3, R1) ran on Nvidia hardware.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| DeepSeek V4-Pro is a Mixture-of-Experts model with 1.6 trillion total parameters and 49 billion active per token, achieving 80.6% on SWE-bench Verified per the model card — within striking distance of leading closed-source frontier models at approximately one-ninth the output token cost of GPT-5.5 at April 2026 list prices. *(vendor-sourced model card — treat benchmark with caution)* | [[2026-disappearing-ai-middle-class]] | 2026-04-26 | current | 1 | false |
| V4-Pro ships under the MIT license with full open weights on Hugging Face, making it commercially deployable without restrictions for any organization with sufficient infrastructure to host large MoE inference — including commercial products and fine-tuned derivatives. | [[2026-disappearing-ai-middle-class]] | 2026-04-26 | current | 1 | false |
| DeepSeek V4-Pro is text-only at launch with multimodal capabilities stated as in progress, making it incompatible with workloads requiring image or video reasoning and not a drop-in alternative to GPT-5.5 or Claude Opus 4.6 for multimodal tasks. | [[2026-disappearing-ai-middle-class]] | 2026-04-26 | current | 1 | false |

## Data Records

| Metric | Value | Conditions | Measurement Date | Source | Status |
|---|---|---|---|---|---|
| API input price | \$1.74 per 1M tokens | Standard list price; launch discount through 2026-05-05 not specified in this source | 2026-04 | [[2026-disappearing-ai-middle-class]] | current |
| API output price | \$3.48 per 1M tokens | Standard list price; launch discount through 2026-05-05 not specified in this source | 2026-04 | [[2026-disappearing-ai-middle-class]] | current |
| SWE-bench Verified | 80.6% | Per DeepSeek model card (vendor-reported); evaluation methodology not independently verified | 2026-04 | [[2026-disappearing-ai-middle-class]] | current |
