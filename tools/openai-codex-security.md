---
type: tool
title: Codex Security
created: 2026-06-23
updated: 2026-06-23
summary: OpenAI's developer-facing security plugin that integrates into Codex workflows to automate vulnerability scanning, threat modeling, patch generation, and validation across existing codebases, positioned as the standard defensive security starting point for most organizations within the Daybreak initiative.
status: emerging
vendor: OpenAI
pricing_model: usage-based
access_tier:
  - consumer
  - api
  - enterprise
capabilities:
  - Deep vulnerability scanning across entire codebases or specific changes and commits
  - Threat model generation for codebases without one
  - Attack path tracing and code reachability analysis
  - Codebase-specific patch generation with test validation
  - Triage and validation of existing findings from scanners, bug-bounty reports, and ticketing systems
  - Export integration with existing vulnerability management systems via SARIF files and CodeQL queries
  - Codex CLI and Codex app workflow integration for automated pipelines
limitations:
  - Research preview launched March 2026; plugin updated June 2026; not yet a mature GA product
  - Humans remain in control of which findings to investigate, which changes to apply, and what information to share
  - All capability and scale claims vendor-reported
primary_use_cases:
  - Automated vulnerability discovery and patch generation in developer workflows
  - Backlog reduction for existing security findings and advisories
  - Continuous security scanning integrated with CI/CD pipelines
  - Organizations seeking security-engineer-grade review without dedicated security staff
source_count: 1
last_assessed: 2026-06-23
related_tools:
  - "[[openai-gpt-5-5]]"
  - "[[openai-gpt-5-5-cyber]]"
  - "[[openai-aardvark]]"
related_topics:
  - "[[ai-assisted-vulnerability-discovery]]"
technical_depth: practitioner
---

Codex Security is OpenAI's developer-facing vulnerability management plugin, launched in research preview in March 2026 and updated with expanded capabilities in June 2026 as part of the Daybreak initiative. It integrates into developer workflows via the Codex app or Codex CLI, providing what OpenAI describes as "the equivalent of a security engineer next to every software developer." Rather than generating standalone alerts, the plugin understands the target codebase and its threat model, identifies plausible vulnerabilities, determines whether affected code is reachable, gathers evidence for validation, develops codebase-specific patches, and verifies the results — all with human control over which findings to act on and what changes to apply.

All capability claims below are vendor-reported.

## Scale and Adoption

Since its March 2026 launch, Codex Security has scanned more than 30 million commits across more than 30,000 codebases. Human reviewers have manually confirmed more than 70,000 findings as fixed; over 500,000 findings have been automatically confirmed as fixed. OpenAI presents this scale as the operating requirement for the current phase of vulnerability management: not just finding vulnerabilities, but closing them at the pace they are being identified. *(vendor-sourced)*

## Developer Workflow Integration

The updated plugin supports multiple scanning modes: deep scans of entire codebases, scans of specific subsets or recent changes, and triage of existing findings from external tools including vulnerability scanners, advisories, bug-bounty platforms, and ticketing systems. For each scan, it can generate reports with severity ratings, affected code locations, validation evidence, and remediation guidance; trace attack paths; build threat models for codebases that lack them; and generate codebase-specific patches for human review. Findings can be exported to existing vulnerability management systems via SARIF files or CodeQL queries, enabling integration with established security workflows.

## Positioning Within Daybreak

OpenAI positions Codex Security with GPT-5.5 and Trusted Access for Cyber as the recommended starting point for most organizations seeking to integrate AI into their security operations. GPT-5.5-Cyber — a specialized, more permissive variant — is reserved for verified defenders whose authorized work requires advanced capabilities beyond what the standard plugin provides. Codex Security is the public-access complement to the restricted GPT-5.5-Cyber model, accessible to developers and organizations without requiring verified defender status. See [[openai-gpt-5-5-cyber]] for the advanced restricted tier.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| Codex Security has scanned over 30 million commits across more than 30,000 codebases since its March 2026 launch, with 70,000+ findings manually confirmed fixed and 500,000+ automatically confirmed fixed — demonstrating AI-assisted patch confirmation at a scale that manual security review cannot match. *(vendor-sourced)* | [[2026-openai-daybreak-security-tools]] | 2026-06-21 | current | 1 | false |
| The Codex Security plugin performs codebase-specific threat modeling, reachability analysis, validation evidence gathering, and patch generation in developer workflows via Codex CLI and app, with findings exportable to SARIF files and existing vulnerability management systems. *(vendor-sourced)* | [[2026-openai-daybreak-security-tools]] | 2026-06-21 | current | 1 | false |
| OpenAI positions Codex Security with GPT-5.5 and Trusted Access for Cyber as the recommended starting point for most defenders, with GPT-5.5-Cyber reserved for verified defenders requiring advanced capabilities and more permissive model behavior. *(vendor-sourced)* | [[2026-openai-daybreak-security-tools]] | 2026-06-21 | current | 1 | false |
