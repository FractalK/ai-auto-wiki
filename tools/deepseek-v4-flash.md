---
type: tool
title: DeepSeek V4-Flash
created: 2026-06-04
updated: 2026-06-04
summary: DeepSeek's low-cost open-weight model as of April 2026, a 284B-parameter MoE model (13B active per token) with MIT license and \$0.14/\$0.28 per million token pricing — self-hostable on mid-size team infrastructure and text-only at launch.
status: active
vendor: DeepSeek
pricing_model: usage-based
access_tier:
  - api
capabilities:
  - Ultra-low cost inference at \$0.14/\$0.28 per million input/output tokens
  - 1M token context window
  - MIT open weights deployable on multi-GPU clusters accessible to mid-size teams (13B active parameters)
  - Agent tool integration support (noted by DeepSeek)
limitations:
  - Text-only at launch; multimodal capabilities not yet supported
  - No independently published benchmark scores comparable to frontier models
  - Huawei Ascend hardware used for part of training — full training stack not disclosed
primary_use_cases:
  - Bulk-edit and high-volume inference steps in multi-model agent pipelines
  - Cost-sensitive deployments where token volume is the binding constraint
  - Self-hosted inference for organizations with multi-GPU infrastructure
source_count: 1
last_assessed: 2026-06-04
related_tools:
  - "[[deepseek-v4-pro]]"
  - "[[openai-gpt-5-5]]"
technical_depth: practitioner
---

DeepSeek V4-Flash is DeepSeek's cost-optimized open-weight model released April 24, 2026, alongside V4-Pro. It is available via the DeepSeek API and as open weights on Hugging Face under the MIT license. V4-Flash occupies a different market position from V4-Pro: where V4-Pro targets near-frontier performance at reduced cost, V4-Flash targets high-volume workloads where cost minimization takes priority over peak capability.

## Architecture and Self-Hosting

V4-Flash runs 284 billion total parameters with 13 billion active per token — an order of magnitude fewer active parameters than V4-Pro's 49 billion. This reduction enables inference on multi-GPU clusters accessible to mid-size engineering teams without hyperscaler-scale infrastructure. For organizations with sufficient compute, self-hosting V4-Flash trades the managed reliability of a cloud API for predictable inference costs and full model control.

DeepSeek's model card notes that at least part of V4-Flash's training was performed on Huawei Ascend AI chips, a disclosure acknowledged by Huawei in its concurrent announcement of Ascend supernode support for V4 inference. This makes V4-Flash the first frontier-tier model release for which non-Nvidia training hardware was publicly acknowledged, a significant signal about the Chinese AI hardware ecosystem. The full training stack was not disclosed; prior DeepSeek models ran on Nvidia hardware.

## Pricing and Positioning

At \$0.14 per million input tokens and \$0.28 per million output tokens, V4-Flash sits approximately one order of magnitude below V4-Pro and two orders of magnitude below GPT-5.5 on output token cost. This pricing makes it viable for bulk-edit steps in agent pipelines that use a higher-capability model (such as V4-Pro or GPT-5.5) for planning and a lower-cost model for high-volume execution. V4-Flash is text-only at launch; multimodal capabilities are not yet supported.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| DeepSeek V4-Flash uses 284 billion total parameters with 13 billion active per token, enabling inference on multi-GPU clusters accessible to mid-size teams at \$0.14/\$0.28 per million input/output tokens — an order-of-magnitude cost reduction below V4-Pro and roughly two orders of magnitude below GPT-5.5. | [[2026-disappearing-ai-middle-class]] | 2026-04-26 | current | 1 | false |
| V4-Flash ships under the MIT license with full open weights, enabling self-hosted deployment and allowing organizations to trade managed API reliability for predictable inference costs and full model control at the price of infrastructure investment. | [[2026-disappearing-ai-middle-class]] | 2026-04-26 | current | 1 | false |
| DeepSeek V4-Flash is text-only at launch, and Huawei has stated that its Ascend supernodes offer full support for V4 inference with at least part of V4-Flash's training performed on Huawei Ascend AI chips — the first publicly acknowledged frontier-tier model release with non-Nvidia training hardware involvement. | [[2026-disappearing-ai-middle-class]] | 2026-04-26 | current | 1 | false |

## Data Records

| Metric | Value | Conditions | Measurement Date | Source | Status |
|---|---|---|---|---|---|
| API input price | \$0.14 per 1M tokens | Standard list price, April 2026 | 2026-04 | [[2026-disappearing-ai-middle-class]] | current |
| API output price | \$0.28 per 1M tokens | Standard list price, April 2026 | 2026-04 | [[2026-disappearing-ai-middle-class]] | current |
