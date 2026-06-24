---
type: tool
title: OpenAI Aardvark
created: 2026-06-09
updated: 2026-06-23
summary: OpenAI's agentic security researcher that autonomously scans codebases for vulnerabilities, proposes patches, and identifies novel CVEs by reasoning over entire codebases, currently in private beta with planned free coverage for non-commercial open-source repositories.
status: emerging
vendor: OpenAI
access_tier:
  - enterprise
capabilities:
  - Autonomous codebase scanning for security vulnerabilities
  - Patch proposal for discovered vulnerabilities, ready for maintainer adoption
  - Novel CVE identification in open-source software via whole-codebase reasoning
source_count: 2
last_assessed: 2026-06-23
related_topics:
  - "[[ai-assisted-vulnerability-discovery]]"
related_tools:
  - "[[openai-codex-security]]"
  - "[[openai-gpt-5-5-cyber]]"
---

OpenAI Aardvark is an agentic security research tool in private beta as of December 2025. It autonomously scans codebases for vulnerabilities and proposes patches that security maintainers can adopt quickly. According to OpenAI, Aardvark has already identified novel CVEs in open-source software by reasoning over entire codebases, rather than operating on isolated function calls or code snippets. OpenAI plans to offer free coverage to select non-commercial open-source repositories to support supply chain security. Access is currently by application through a private beta program targeting developers and security teams working on cyberdefense.

OpenAI's June 2026 Daybreak announcement introduced two publicly accessible products in the same cybersecurity ecosystem: Codex Security, a developer-facing plugin for scanning and patching vulnerabilities in the deployer's own codebase, and the Patch the Planet initiative, through which OpenAI-funded expert security researchers work directly with open-source maintainers using Codex Security and advanced models. These expand the open-source vulnerability management mission Aardvark was originally launched to serve. The Daybreak announcement does not reference Aardvark by name, suggesting Aardvark's private beta continues as a separate research instrument while Codex Security and Patch the Planet provide the public-facing layer. See [[openai-codex-security]] for the developer-accessible security layer.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| OpenAI Aardvark is an agentic security researcher in private beta that autonomously scans entire codebases for vulnerabilities, proposes patches for maintainers to adopt, and has already identified novel CVEs in open-source software through whole-codebase reasoning. | [[2025-openai-cyber-resilience-safeguards]] | 2025-12-10 | current | 1 | false |
| OpenAI plans to offer free Aardvark coverage to select non-commercial open-source repositories to address supply chain security, with a private beta application process targeting developers and security teams working on cyberdefense. | [[2025-openai-cyber-resilience-safeguards]] | 2025-12-10 | current | 1 | false |
| Aardvark is positioned as part of OpenAI's defense-in-depth ecosystem strategy alongside a Frontier Risk Council and trusted access program, framing it as a building block toward a more resilient open-source and enterprise security ecosystem rather than a standalone product. | [[2025-openai-cyber-resilience-safeguards]] | 2025-12-10 | current | 1 | false |
