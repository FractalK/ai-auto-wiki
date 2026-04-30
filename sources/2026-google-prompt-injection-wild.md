---
type: source
title: "AI threats in the wild: The current state of prompt injections on the web"
created: 2026-04-30
updated: 2026-04-30
status: active
source_type: industry-blog
author:
  - Thomas Brunner
  - Yu-Han Liu
  - Moni Pande
publication: Google Security Blog
published_date: 2026-04-23
ingested_date: 2026-04-30
ingest_via: staged
url: https://security.googleblog.com/2026/04/ai-threats-in-wild-current-state-of.html
credibility_tier: institutional
extraction_depth: standard
related_topics:
  - "[[prompt-injection]]"
  - "[[llm-fundamentals]]"
---

Google's Threat Intelligence Group (GTIG) and Google DeepMind (GDM) conducted a broad scan of Common Crawl — a publicly available archive of 2–3 billion web pages — to characterize the actual state of indirect prompt injection (IPI) on the public web. Using a coarse-to-fine detection methodology (pattern matching, LLM-based intent classification via Gemini, human validation), they identified IPI attempts in seven categories ranging from harmless pranks to data exfiltration and destructive command injection. The majority of observed attempts were low-sophistication experiments; advanced exfiltration techniques from 2025 security research were not observed at scale. However, the malicious IPI category increased 32% between November 2025 and February 2026 across successive Common Crawl snapshots, indicating a maturing threat trajectory as AI agents grow more capable and more widely deployed.
