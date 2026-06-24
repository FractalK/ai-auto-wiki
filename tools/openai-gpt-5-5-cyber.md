---
type: tool
title: GPT-5.5-Cyber
created: 2026-06-23
updated: 2026-06-23
summary: OpenAI's specialized cybersecurity variant of GPT-5.5, offering more permissive response behavior for authorized security work and state-of-the-art performance on vulnerability reproduction and exploitation benchmarks as of June 2026, released in continued limited access to verified defenders through the Daybreak initiative.
status: emerging
vendor: OpenAI
pricing_model: enterprise
access_tier:
  - api
capabilities:
  - Vulnerability reproduction at 85.6% on CyberGym — highest reported single-model score as of June 2026 (vendor-reported)
  - Exploit generation from known vulnerabilities at 39.5% on ExploitGym vs 25.95% for GPT-5.5 (vendor-reported)
  - Long-horizon vulnerability discovery and PoC generation at 69.8% on SEC-bench Pro vs 63.1% for GPT-5.5 (vendor-reported)
  - Deep analysis across large codebases: identifying security-relevant components, tracing code reachability, and validating issues in controlled environments
  - Full remediation loop support: discovery, validation, patch development, testing, and evidence preparation for human review
limitations:
  - Access limited to trusted defenders via continued limited release; not available for general API use
  - Intended for verified defenders with authorized security work requiring advanced capabilities and more permissive model behavior; most defenders should start with GPT-5.5 and Codex Security per OpenAI
  - All benchmark data vendor-reported; independent evaluation not available as of June 2026
primary_use_cases:
  - End-to-end vulnerability discovery and patch automation for authorized defenders
  - Large-scale codebase security analysis with remediation support
  - Authorized penetration testing and security research
source_count: 1
last_assessed: 2026-06-23
related_tools:
  - "[[openai-gpt-5-5]]"
  - "[[openai-codex-security]]"
related_topics:
  - "[[ai-assisted-vulnerability-discovery]]"
technical_depth: practitioner
---

GPT-5.5-Cyber is OpenAI's specialized cybersecurity variant of GPT-5.5, designed for authorized security work that benefits from more permissive model behavior than the standard GPT-5.5 profile. Following an initial limited release focused on reducing unnecessary refusals in specialized security workflows, OpenAI released an updated version in June 2026 through the Daybreak initiative with meaningfully stronger cybersecurity benchmark performance. The model is available through continued limited access to verified defenders and is not offered for general API use.

All benchmark claims below are vendor-reported and should be evaluated with caution.

## Benchmark Performance

On CyberGym — which measures whether an agent can reproduce known vulnerabilities in software environments — GPT-5.5-Cyber reached 85.6% in single-model evaluations, compared to 81.8% for GPT-5.5 and 78.8% for Claude Opus 4.8 (without safeguards). OpenAI describes this as the highest CyberGym score it has measured from a single model as of June 2026. *(vendor-sourced)*

On ExploitGym — which tests whether agents can turn known vulnerabilities into working exploits achieving unauthorized code execution — GPT-5.5-Cyber scored 39.5% compared to 25.95% for GPT-5.5. On SEC-bench Pro — evaluating long-horizon vulnerability discovery and proof-of-concept generation across complex software targets — it reached 69.8% compared to 63.1% for GPT-5.5. *(vendor-sourced)*

## Capability Profile

GPT-5.5-Cyber is designed to sustain deeper analysis across large codebases: identifying security-relevant components, tracing whether vulnerable code paths are reachable, validating likely issues in controlled environments, developing and testing patches, and preparing evidence for human review. The design goal is to help defenders move through the full remediation loop rather than simply generate more vulnerability findings.

For most defenders, OpenAI recommends GPT-5.5 with Trusted Access for Cyber and the Codex Security plugin as the starting point. GPT-5.5-Cyber is intended for verified defenders whose authorized work specifically requires the most advanced cybersecurity capabilities and more permissive model behavior, paired with stronger monitoring, scoped controls, and review requirements. See [[openai-codex-security]] for the developer-accessible defensive security layer within Daybreak.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| GPT-5.5-Cyber achieves 85.6% on CyberGym (single-model evaluation), compared to 81.8% for GPT-5.5 — described by OpenAI as the highest single-model CyberGym score it has measured as of June 2026. *(vendor-sourced)* | [[2026-openai-daybreak-security-tools]] | 2026-06-21 | current | 1 | false |
| GPT-5.5-Cyber outperforms GPT-5.5 on ExploitGym (39.5% vs 25.95%) and SEC-bench Pro (69.8% vs 63.1%), demonstrating stronger capability at both converting known vulnerabilities to working exploits and long-horizon vulnerability discovery across complex software targets. *(vendor-sourced)* | [[2026-openai-daybreak-security-tools]] | 2026-06-21 | current | 1 | false |
| GPT-5.5-Cyber is released in continued limited access to trusted defenders through the Daybreak initiative, with access paired with stronger verification, monitoring, and scoped controls; OpenAI positions GPT-5.5 with Codex Security as the recommended starting point for most defenders. *(vendor-sourced)* | [[2026-openai-daybreak-security-tools]] | 2026-06-21 | current | 1 | false |

## Data Records

| Metric | Value | Conditions | Measurement Date | Source | Status |
|---|---|---|---|---|---|
| CyberGym | 85.6% | Single-model evaluation; vulnerability reproduction benchmark; vendor-reported | 2026-06 | [[2026-openai-daybreak-security-tools]] | current |
| ExploitGym | 39.5% | Agent converts known vulnerabilities to working exploits achieving unauthorized code execution; vendor-reported | 2026-06 | [[2026-openai-daybreak-security-tools]] | current |
| SEC-bench Pro | 69.8% | Long-horizon vulnerability discovery and proof-of-concept generation across complex software targets; vendor-reported | 2026-06 | [[2026-openai-daybreak-security-tools]] | current |
