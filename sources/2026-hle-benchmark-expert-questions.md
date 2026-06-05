---
type: source
title: "A Benchmark of Expert-Level Academic Questions to Assess AI Capabilities"
created: 2026-06-04
updated: 2026-06-04
status: active
source_type: research-paper
author:
  - Center for AI Safety
  - Scale AI
  - HLE Contributors Consortium
publication: "Nature, Vol 649, pp. 1139–1146"
published_date: 2026-01-28
ingested_date: 2026-06-04
ingest_via: staged
url: https://doi.org/10.1038/s41586-025-09962-4
credibility_tier: peer-reviewed
extraction_depth: full
related_topics:
  - "[[ai-capability-benchmarking]]"
related_tools:
  - "[[anthropic-claude-sonnet-4-6]]"
---

Phan, Hendrycks et al. (Center for AI Safety / Scale AI, 2026) introduce Humanity's Last Exam (HLE), a 2,500-question expert-level benchmark across over a hundred subjects, developed by ~1,000 subject-matter experts from 500+ institutions across 50 countries using a multi-stage review process that pre-validates questions against frontier models before submission. At release, all frontier models achieved low accuracy — GPT-4o 2.7%, Claude 3.5 Sonnet 4.1%, Gemini 1.5 Pro 4.6%, o1 8.0%, DeepSeek R1 8.5% — with post-release models (which had access to the public dataset) reaching Claude 4 Sonnet 7.8%, Gemini 2.5 Pro 21.6%, and GPT-5 25.3%. All models exhibited root mean square (RMS) calibration errors above 70%, providing incorrect answers with high confidence. Analysis of reasoning token output found log-linear accuracy gains up to approximately 2^14 tokens (~16,000), after which accuracy reverses across multiple frontier reasoning models — indicating that larger reasoning budgets are not always optimal. The benchmark includes a private held-out test set to assess model overfitting and gaming, and maintains a 15.4% expert disagreement rate comparable to other expert-grade evaluations.
