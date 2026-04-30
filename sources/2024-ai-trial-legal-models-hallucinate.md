---
type: source
title: "AI on Trial: Legal Models Hallucinate in 1 out of 6 (or More) Benchmarking Queries"
created: 2026-04-25
updated: 2026-04-25
status: active
source_type: publication-article
author:
  - Varun Magesh
  - Faiz Surani
  - Matthew Dahl
  - Mirac Suzgun
  - Christopher D. Manning
  - Daniel E. Ho
publication: Stanford HAI News
published_date: 2024-05-23
ingested_date: 2026-04-25
ingest_via: staged
url: https://hai.stanford.edu/news/ai-trial-legal-models-hallucinate-1-out-6-or-more-benchmarking-queries
credibility_tier: practitioner
extraction_depth: standard
related_topics:
  - "[[legal-ai-hallucination]]"
related_tools:
  - "[[lexisnexis-lexis-plus-ai]]"
  - "[[thomson-reuters-westlaw-ai]]"
  - "[[thomson-reuters-ask-practical-law-ai]]"
---

Stanford RegLab and HAI researchers benchmarked three leading legal AI research tools — LexisNexis Lexis+ AI, Thomson Reuters Westlaw AI-Assisted Research, and Thomson Reuters Ask Practical Law AI — on a preregistered dataset of over 200 open-ended legal queries, finding hallucination rates of more than 17 percent for Lexis+ AI and Ask Practical Law AI and more than 34 percent for Westlaw AI-Assisted Research. The study identified three failure mechanisms specific to RAG-based legal AI: the difficulty of identifying binding authority among semantically similar but jurisdictionally inapposite documents, the failure to detect when retrieved precedent has been overturned, and sycophancy toward false legal premises. As of May 2024, none of the major providers published systematic evaluation results or provided researchers with access to test their tools, making independent reliability assessment impossible without conducting bespoke studies.
