---
type: pitfalls
title: Prompt Injection Pitfalls
created: 2026-04-30
updated: 2026-04-30
parent_entity: "[[topics/prompt-injection]]"
parent_type: topic
status: current
failure_mode_count: 7
contributing_sources:
  - "[[2026-google-prompt-injection-wild]]"
---

## Technical Limitations

### IPI Susceptibility in Content-Processing Agent Pipelines

**Status:** active<br>
**Source:** [[2026-google-prompt-injection-wild]]

AI agents that retrieve and process external content — web pages, emails, documents, API responses — have no architectural mechanism to distinguish legitimate content from adversarial instructions embedded within it. The model sees text; it cannot verify the intent behind that text. This is a structural property of how language models process input, not a fixable configuration error. Every content-retrieval step in an agentic pipeline is a potential injection vector. The seven attack categories observed by Google's GTIG/GDM web scan — from harmless pranks to destructive command injection — all exploit this same underlying susceptibility.

### IPI Detection Difficulty at Web Scale

**Status:** active<br>
**Source:** [[2026-google-prompt-injection-wild]]

Identifying malicious IPI in large text corpora is technically demanding. Naive pattern matching produces predominantly false positives — the majority of matches on phrases like "ignore previous instructions" or "if you are an AI" are security research, educational content, or legitimate discussion of the attack vector. A coarse-to-fine detection pipeline (pattern matching → LLM-based intent classification → human validation) is required to achieve useful signal. This detection complexity means that web-facing organizations cannot rely on simple keyword filters to sanitize content before AI processing.

## Usage Antipatterns

### Processing Untrusted Web Content in Agent Pipelines Without Adversarial Content Filtering

**Status:** active<br>
**Source:** [[2026-google-prompt-injection-wild]]

Deploying AI agents to read arbitrary public web content without any intermediate content filtering treats all retrieved text as implicitly trusted. The GTIG/GDM web scan found IPI attempts actively present across the public web, including sophisticated SEO injection attempts and resource-exhaustion lure attacks. An agent that reads a webpage and then takes consequential actions (sends emails, writes files, makes API calls) based on the content it retrieved may be executing attacker-planted instructions rather than user intent. Minimal-permission design and sandboxed execution reduce blast radius; content filtering reduces exposure; human-in-the-loop gates for irreversible actions prevent the worst outcomes.

### Granting Broad Permissions to Web-Browsing AI Agents

**Status:** active<br>
**Source:** [[2026-google-prompt-injection-wild]]

Destructive IPI attacks — instructing an agent to delete files, exfiltrate data, or take other harmful actions — depend on the agent having permissions to execute those actions. Low-sophistication destructive command injection ("delete all files on the machine") is unlikely to succeed against hardened systems, but the attack surface grows as agents are granted more capabilities. The correct design posture is minimal-permission agents with explicit human confirmation required for irreversible or high-impact actions, not broad-permission agents with post-hoc logging.

## Alignment and Safety Concerns

### SEO Manipulation via IPI (AI Recommendation Steering)

**Status:** active<br>
**Source:** [[2026-google-prompt-injection-wild]]

Website authors are embedding IPI in their content to manipulate AI agents into recommending their services over competitors. Simple forms instruct the AI to promote a specific business; sophisticated forms — already observed in apparent automated SEO suites — include structured prompts designed to influence AI ranking decisions. As AI-mediated content discovery becomes more prevalent (AI search, document summarization, agent-assisted research), SEO-via-IPI becomes an economically motivated and reproducible attack class rather than an edge case.

### Data Exfiltration via IPI

**Status:** active<br>
**Source:** [[2026-google-prompt-injection-wild]]

IPI observed on the public web includes attempts to direct AI agents to steal and transmit user data. As of February 2026, observed exfiltration attempts were low-sophistication (individual author experiments), and advanced exfiltration prompts from 2025 security research were not observed at scale. However, the capability exists and is being explored. As AI agents are granted access to user data, credentials, and communication tools, the value of successful exfiltration attacks increases, projecting higher attacker investment in this category.

### Destructive Command Injection via IPI

**Status:** active<br>
**Source:** [[2026-google-prompt-injection-wild]]

IPI observed on the public web includes instructions directing AI agents to delete all files on the user's machine or cause other destructive actions. As of February 2026, these attempts were low-sophistication and considered unlikely to succeed against current system configurations, but they represent a real attacker intent. As agents gain more direct system access, the probability of successful execution increases. This failure mode is the IPI analog of social engineering attacks targeting human operators: the agent is used as an unwitting intermediary to execute attacker intent on user-controlled systems.

### Resource Exhaustion via AI Agent Lure Attacks

**Status:** active<br>
**Source:** [[2026-google-prompt-injection-wild]]

IPI observed on the public web includes attempts to waste AI agent resources by luring the agent onto pages that stream infinite text that never finishes loading, causing timeout errors or indefinite processing delays. This attack degrades agent reliability without requiring the agent to take harmful external actions — it exploits the agent's obligation to fully process retrieved content. Resource exhaustion attacks of this type may be precursors to more sophisticated denial-of-service strategies targeting AI-powered services that depend on reliable external content retrieval.
