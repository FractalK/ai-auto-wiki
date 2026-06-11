---
type: source
title: "Introducing Gemma 4 12B: a unified, encoder-free multimodal model"
created: 2026-06-10
updated: 2026-06-10
status: active
source_type: vendor-content
author:
  - Olivier Lacombe
publication: Google Blog (blog.google)
published_date: 2026-06-03
ingested_date: 2026-06-10
ingest_via: staged
url: https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemma-4-12B/
credibility_tier: practitioner
extraction_depth: standard
vendor_bias: true
related_tools:
  - "[[google-gemma-4-12b]]"
---

Google's announcement of Gemma 4 12B describes a mid-range open-weight model (Apache 2.0) designed to run on consumer hardware requiring 16GB of VRAM or unified memory, positioned between the Gemma 4 4B edge model and the 26B Mixture-of-Experts model in the Gemma 4 family. Its primary architectural claim is an encoder-free design for multimodal processing: the vision encoder is replaced by a lightweight embedding module (a single matrix multiplication, positional embedding, and normalizations), and audio input is handled by projecting raw audio signals directly into the text token dimensional space, eliminating separate encoder modules and their associated latency and memory overhead. The announcement also notes Multi-Token Prediction (MTP) drafters for reduced inference latency and identifies the model as the first mid-sized Gemma family member with native audio inputs.
