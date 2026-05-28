---
type: tool
title: IBM Defense Model
created: 2026-05-27
updated: 2026-05-27
aliases:
  - IBM Janes Defense Model
summary: IBM Granite-based LLM fine-tuned on Janes open-source defense intelligence data for air-gapped, classified, and edge deployment; decision-support for operational planning and defense industrial base strategy.
status: emerging
vendor: IBM
pricing_model: subscription
access_tier:
  - enterprise
  - api
capabilities:
  - Defense terminology, equipment, and mission context comprehension
  - Operational planning and intelligence decision support
  - Defense industrial base corporate strategy and equipment planning assistance
  - Real-time data queries via secure scheduled feeds from Janes intelligence
  - Air-gapped, classified, and edge environment deployment via API
limitations:
  - No benchmark data available; capability claims sourced from a single trade publication
  - Decision-support only; not designed for autonomous decision-making
  - Excludes internet training data by design; knowledge bounded by Janes subscription coverage
primary_use_cases:
  - Defense intelligence analysis and operational planning
  - Equipment specification and military order-of-battle research
  - Defense industrial base strategy support
source_count: 1
last_assessed: 2026-05-27
related_tools:
  - "[[ibm-granite-4-1]]"
technical_depth: practitioner
---

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| The IBM Defense Model is a Granite-based LLM trained on Janes' curated open-source defense intelligence data — covering equipment specifications, government statements, and field documentation — and is deployable in air-gapped, classified, and edge environments via API integration. | [[2025-ibm-llm-defense-applications]] | 2025-10-29 | current | 1 | false |
| The model queries live Janes data via secure scheduled feeds rather than encoding static training knowledge, enabling real-time defense intelligence updates without model retraining; internet training data is deliberately excluded to avoid the military information inaccuracies common in public sources. | [[2025-ibm-llm-defense-applications]] | 2025-10-29 | current | 1 | false |
| IBM and Janes developed the model for operational planning, intelligence functions, and defense industrial base strategy use cases, positioning it explicitly as decision-support rather than autonomous decision-making. | [[2025-ibm-llm-defense-applications]] | 2025-10-29 | current | 1 | false |

## Overview

The IBM Defense Model is a large language model developed jointly by IBM and Janes, the defense intelligence data provider. It combines IBM's Granite foundation model architecture with Janes' proprietary collection of open-source defense intelligence — manufacturer specifications, government statements, and field documentation covering militaries worldwide. IBM was selected as the technology partner because of its ability to account for the provenance of all training data, which Janes identified as a requirement for data integrity assurance in defense contexts.

The model differs from general-purpose LLMs in two design choices: it excludes internet training data (to avoid military misinformation common in public sources), and it queries live Janes data via secure scheduled feeds rather than relying on memorized training knowledge. This architecture allows the intelligence corpus to be updated continuously without retraining the underlying model.

As of October 2025, the model was offered on a subscription basis with flexible terms and had not yet been publicly deployed or independently benchmarked. IBM and Janes have described target applications including operational planning support, defense industrial base strategy, and equipment research, and the model is positioned as compatible with classified and CJADC2-adjacent environments.
