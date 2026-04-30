---
type: pitfalls
title: AI Coding Agent Workflow Types Pitfalls
created: 2026-04-30
updated: 2026-04-30
parent_entity: "[[topics/ai-coding-agent-workflow-types]]"
parent_type: topic
status: current
failure_mode_count: 4
contributing_sources:
  - "[[2026-realpython-coding-agent-workflow-types]]"
---

## Technical Limitations

### Autonomy-Control Tradeoff as a Structural Constraint

**Status:** active<br>
**Source:** [[2026-realpython-coding-agent-workflow-types]]

Cloud and PR agents sacrifice real-time control in exchange for greater autonomy — they work asynchronously and return results that cannot be interrupted or redirected mid-execution. A cloud agent deployed for an exploratory debugging session produces a completed artifact to review later, not an interactive session to guide. PR agents post review comments after the work is done; they cannot flag an issue mid-implementation for the developer to redirect. The tradeoff is structural, not a configuration option: choosing a high-autonomy mode for a task that requires real-time feedback imposes a mismatch the tool cannot compensate for.

## Usage Antipatterns

### Assuming One Workflow Type Handles All Tasks

**Status:** active<br>
**Source:** [[2026-realpython-coding-agent-workflow-types]]

IDE agents excel at interactive editing and real-time inline changes; terminal agents handle complex multi-file coordination with step-by-step approval; PR agents catch issues asynchronously on shared branches; cloud agents execute well-scoped longer tasks without supervision. Applying the same agent mode to all tasks — particularly defaulting to the most autonomous cloud mode — produces mismatches between the tool's interaction model and the task's requirements. A developer trying to debug a runtime issue interactively with a cloud agent will receive a completed attempt to review, not the responsive feedback loop the task requires.

### Over-Automating Without Human Review

**Status:** active<br>
**Source:** [[2026-realpython-coding-agent-workflow-types]]

AI-generated code at any autonomy level requires human review before merging or deploying. The more autonomous the agent, the more important developer review becomes — cloud agents operating over long time horizons can diverge from intended direction and introduce bugs or patterns inconsistent with codebase conventions. A sound rule of thumb: never push or ship code that has not been reviewed by a developer who understands what it is supposed to do. The cost of a careful review is substantially less than the cost of a production failure.

## Alignment and Safety Concerns

### Sending Proprietary Code to Cloud-Backed Agents Without Compliance Verification

**Status:** active<br>
**Source:** [[2026-realpython-coding-agent-workflow-types]]

Cloud-backed IDE agents, terminal agents, and cloud agents with remote execution environments send code to external servers for processing. For teams with proprietary code, trade secrets, or compliance requirements (regulatory, contractual, or organizational policy), this constitutes a data boundary violation unless the specific agent's infrastructure is explicitly approved. Repository-level AI tool decisions are often made at the organizational level rather than by individual developers. Teams that need local processing can use agents that support local model backends (Ollama, Continue) or vendor-managed environments on controlled infrastructure (Cursor's My Machines) — but these options must be deliberately selected, not assumed to be the default.
