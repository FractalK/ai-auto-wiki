---
type: source
title: "Mind Your Tone: Investigating How Prompt Politeness Affects LLM Accuracy"
created: 2026-05-26
updated: 2026-05-26
status: active
source_type: research-paper
author:
  - "Om Dobariya"
  - "Akhil Kumar"
publication: arXiv (Pennsylvania State University)
published_date: 2025-10
ingested_date: 2026-05-26
ingest_via: staged
url: https://arxiv.org/abs/2510.04950
credibility_tier: institutional
extraction_depth: full
related_topics:
  - "[[prompt-engineering]]"
---

This short paper investigates whether and how prompt politeness level affects LLM accuracy on multiple-choice questions. The authors created 250 prompts by rewriting 50 base MCQ questions across mathematics, science, and history into five politeness variants (Very Polite through Very Rude), then evaluated ChatGPT-4o across 10 runs per condition using paired t-tests to assess statistical significance. Contrary to prior findings on older models (GPT-3.5, Llama2-70B), very rude prompts produced the highest accuracy (84.8%) while very polite prompts produced the lowest (80.8%), with differences confirmed statistically significant by paired t-tests (p < 0.05 for all politeness–rudeness pairs). The authors propose that RLHF updates in newer models may alter how tone is processed, but note the causal mechanism remains unresolved and that the study is limited by a small dataset (50 base questions), reliance on a single model family, and MCQ-only format.
