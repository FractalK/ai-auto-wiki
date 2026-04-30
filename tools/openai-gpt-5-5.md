---
type: tool
title: GPT-5.5
created: 2026-04-30
updated: 2026-04-30
summary: OpenAI's flagship agentic model as of April 2026, with state-of-the-art results on agentic coding and abstract reasoning benchmarks at GPT-5.4 latency, rated "High" under OpenAI's Preparedness Framework for cybersecurity and biosecurity capabilities.
status: active
vendor: OpenAI
pricing_model: usage-based
access_tier:
  - consumer
  - api
  - enterprise
capabilities:
  - Agentic coding at 82.7% Terminal-Bench 2.0 and 73.1% Expert-SWE (internal benchmark, vendor-reported)
  - SWE-Bench Pro at 58.6% (Public, vendor-reported)
  - Computer use at 78.7% OSWorld-Verified (vendor-reported)
  - Knowledge work at 84.9% GDPval across 44 occupations (vendor-reported)
  - Abstract reasoning at 85.0% ARC-AGI-2 and 95.0% ARC-AGI-1 (vendor-reported)
  - Scientific data analysis (GeneBench, BixBench); bioinformatics workflows
  - 1M token context window in API
  - Fast mode in Codex at 1.5x token generation speed for 2.5x the cost
limitations:
  - Cybersecurity and biological/chemical capabilities rated "High" under Preparedness Framework; advanced cyber use requires Trusted Access verification
  - SWE-Bench Pro (58.6%) below Claude Opus 4.7 (64.3%) per OpenAI's own evaluation *(vendor-sourced — treat comparative claims with caution)*
  - Priced higher than GPT-5.4; token efficiency gains in Codex partially offset higher cost per OpenAI
primary_use_cases:
  - Agentic software engineering and long-horizon coding tasks
  - Knowledge work automation across professional domains
  - Scientific data analysis and research assistance
  - Computer use and multi-tool workflow automation
source_count: 1
last_assessed: 2026-04-30
related_tools:
  - "[[openai-gpt-5-5-pro]]"
  - "[[anthropic-claude-opus-4-7]]"
  - "[[openai-chatgpt]]"
technical_depth: practitioner
---

GPT-5.5 is OpenAI's flagship model as of April 2026, positioned as a substantial advance over GPT-5.4 in agentic coding, knowledge work, computer use, and scientific research. It is available in ChatGPT (Plus, Pro, Business, Enterprise) and Codex, and through the OpenAI API with a 1M token context window. A higher-capability variant, GPT-5.5 Pro, is available to Pro, Business, and Enterprise users — see [[openai-gpt-5-5-pro]].

All benchmark comparisons below are from OpenAI's own release materials and should be evaluated as vendor-sourced claims.

## Agentic Coding

GPT-5.5's headline advance is in agentic coding. On Terminal-Bench 2.0 — which tests complex command-line workflows requiring planning, iteration, and tool coordination — it achieves 82.7%, a 7.6 percentage point improvement over GPT-5.4 (75.1%). On Expert-SWE, an internal benchmark for long-horizon coding tasks with a median estimated 20-hour human completion time, GPT-5.5 also outperforms GPT-5.4. On SWE-Bench Pro (Public), it scores 58.6% compared to GPT-5.4's 57.7%, though this places it below Claude Opus 4.7's 64.3% on the same benchmark; OpenAI notes that Anthropic has cited evidence of memorization in Claude's SWE-Bench Pro score. *(vendor-sourced — treat comparative claims with caution)*

A key design claim is that GPT-5.5 matches GPT-5.4's per-token serving latency despite higher capability. In Codex, the model uses significantly fewer tokens for equivalent tasks — an efficiency claim that partially offsets the higher base pricing.

## Knowledge Work and Computer Use

GPT-5.5 achieves 84.9% on GDPval (testing agents across 44 professional occupations), 78.7% on OSWorld-Verified (measuring computer use in real environments), and 98.0% on Tau2-bench Telecom (complex customer service workflows without prompt tuning). OpenAI reports that over 85% of its own staff use Codex weekly, using GPT-5.5 for workflows including financial document analysis (24,771 K-1 tax forms totaling 71,637 pages) and automated business report generation. *(vendor-sourced — treat comparative claims with caution)*

## Abstract Reasoning and Science

On ARC-AGI-2 (Verified), GPT-5.5 achieves 85.0%, an 11.7 percentage point improvement over GPT-5.4's 73.3%. On ARC-AGI-1 (Verified), it achieves 95.0%. Scientific benchmarks include GeneBench (25.0%, multi-stage genetic data analysis) and BixBench (80.5%, bioinformatics). OpenAI reports that an internal version of GPT-5.5 contributed a new proof about Ramsey numbers in combinatorics, subsequently verified in Lean — cited as an example of AI contributing a genuinely novel mathematical argument rather than explanation or code. *(vendor-sourced — treat comparative claims with caution)*

## Safety and Preparedness

OpenAI rates GPT-5.5's cybersecurity and biological/chemical capabilities as "High" under its Preparedness Framework — the highest level before Critical. This triggers tiered deployment restrictions: stricter classifiers for high-risk cyber activity and additional safeguards developed with external experts over several months. A Trusted Access program provides verified defenders with expanded access to advanced cybersecurity capabilities with fewer restrictions. OpenAI notes that while GPT-5.5 did not reach Critical on cybersecurity capability, its abilities represent a step up from GPT-5.4.

## Serving Infrastructure

OpenAI states that GPT-5.5 was co-designed and trained with NVIDIA GB200 and GB300 NVL72 systems. Achieving GPT-5.4 latency required integrated inference optimization rather than isolated improvements. One optimization — dynamic load-balancing heuristics developed using Codex analyzing production traffic patterns — increased token generation speeds by over 20%.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| GPT-5.5 achieves 82.7% on Terminal-Bench 2.0, a 7.6 percentage point improvement over GPT-5.4 (75.1%), representing a state-of-the-art result on complex agentic coding workflows as of April 2026, per OpenAI's evaluation. *(vendor-sourced — treat comparative claims with caution)* | [[2026-openai-gpt-5-5-announcement]] | 2026-04-28 | current | 1 | false |
| GPT-5.5 is priced at \$5 per 1M input tokens and \$30 per 1M output tokens in the API with a 1M token context window; batch processing is available at half the standard rate and priority processing at 2.5x the standard rate. | [[2026-openai-gpt-5-5-announcement]] | 2026-04-28 | current | 1 | false |
| OpenAI rates GPT-5.5's cybersecurity and biological/chemical capabilities as "High" under its Preparedness Framework — the highest level before Critical — triggering stricter deployment classifiers and a Trusted Access program for verified defenders. | [[2026-openai-gpt-5-5-announcement]] | 2026-04-28 | current | 1 | false |
| GPT-5.5 achieves 85.0% on ARC-AGI-2 (Verified), an 11.7 percentage point improvement over GPT-5.4's 73.3%, and 95.0% on ARC-AGI-1, per OpenAI's April 2026 evaluation. *(vendor-sourced — treat comparative claims with caution)* | [[2026-openai-gpt-5-5-announcement]] | 2026-04-28 | current | 1 | false |
| GPT-5.5 scores 58.6% on SWE-Bench Pro (Public), below Claude Opus 4.7's 64.3% on the same benchmark; OpenAI notes that Anthropic has cited evidence of memorization in Claude's score on this evaluation. *(vendor-sourced — treat comparative claims with caution)* | [[2026-openai-gpt-5-5-announcement]] | 2026-04-28 | current | 1 | false |
