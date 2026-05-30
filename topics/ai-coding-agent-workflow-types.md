---
type: topic
title: AI Coding Agent Workflow Types
created: 2026-04-30
updated: 2026-05-29
summary: A taxonomy of AI coding agent interaction modes — IDE, terminal, pull request, and cloud — organized by deployment environment, autonomy level, and real-time control, used to match the right workflow type to the development task.
status: developing
source_count: 2
last_assessed: 2026-05-29
related_topics:
  - "[[ai-agentic-workflows]]"
  - "[[llm-fundamentals]]"
related_tools:
  - "[[anthropic-claude]]"
  - "[[openai-codex]]"
teaching_relevance: true
competency_domains:
  - tool-evaluation-and-selection
  - practical-ai-use-and-interaction
professional_contexts:
  - professional-and-continuing-education
  - organizational-leadership-and-change-management
  - software-and-ai-development
technical_depth: foundational
teaching_notes_reviewed: 2026-04-30
---

AI coding agents now span four distinct interaction modes — IDE, terminal, pull request, and cloud — each defined by where the agent operates and how much autonomy it exercises. Understanding this taxonomy matters more than selecting a "best" coding agent, because the same tool often supports multiple modes and the appropriate choice is task-dependent.

Before exploring the modes, it helps to understand what makes a coding tool agentic. Coding agents operate through a continuous loop: they read relevant files to form context, reason about necessary steps, act by editing files or running commands, then evaluate results and repeat. This loop continues until the task completes or the agent returns control to the developer — a structural distinction from autocomplete or one-shot chatbots, which generate single responses.

## IDE Agents

IDE agents live inside the code editor and work in real time. They suggest inline edits, display visual diffs, and let developers accept or reject changes without leaving the editing environment. Two variants exist: AI-native IDEs (Cursor, Windsurf, Kiro) built from the ground up around AI capabilities, and IDE integrations (GitHub Copilot extension, Claude Code in VS Code, Gemini Code Assist) that add agent features to existing editors. AI-native IDEs often support spec-driven workflows where a developer describes a task upfront; integrations tend toward file-targeted interactive editing. Both categories send code to external servers for inference when cloud-backed — a privacy implication teams with proprietary code policies must address before adoption.

## Terminal Agents

Terminal agents run in the shell. The developer describes a task; the agent reads files and proposes edits; the developer approves or rejects each step. This step-by-step approval model suits complex multi-file changes, large codebase navigation, and onboarding to unfamiliar code. Terminal agents — Claude Code, Aider, Gemini CLI, Codex CLI — integrate naturally with existing development workflows and can be chained with other CLI tools or run inside automation scripts. Some terminal agents support local model backends (Ollama, Continue), preserving code confidentiality when external API access is prohibited by policy.

## Pull Request Agents

Pull request agents are structurally asynchronous. Rather than working alongside a developer in real time, they trigger automatically when a pull request is opened or updated, run on their own schedule, then post review comments for human evaluation. They operate on shared branches visible to the whole team, not the developer's local workspace. The verification mechanism is human code review — the agent flags issues, but a reviewer decides whether to merge. CodeRabbit and GitHub Copilot code review are the primary examples. A key organizational note: PR agent access is often approved or blocked at the repository level by administrators, making it a team policy decision rather than an individual tool choice.

## Cloud Agents

Cloud agents offer the most autonomy. The developer describes a task; the agent works in a remote or managed environment; the agent later reports back with a branch, pull request, or prototype. This makes cloud agents suited for greenfield prototyping or work that takes longer than a developer would monitor live. Devin, Claude Code on the web, [[openai-codex|Codex web]], and Cursor's Cloud Agents fall into this category. Access channels include Slack, issue trackers, and web browsers. The tradeoff is that real-time control is absent — the code runs on infrastructure outside the developer's machine, sometimes vendor-managed (Anthropic for Claude Code on the web, GitHub Actions for GitHub Copilot cloud agent), sometimes on machines the developer controls (Cursor's My Machines). Where code executes matters for compliance verification.

An emerging variant within the high-autonomy category is background computer use in desktop applications — agents running locally on the developer's machine, operating all installed applications via mouse and keyboard in the background without interfering with the developer's active work. [[openai-codex]]'s April 2026 update introduced this capability (vendor-reported), supporting multiple parallel agents in background sessions. This modality shares the asynchrony and autonomy of cloud agents but differs on two dimensions: execution stays on the developer's machine rather than vendor infrastructure, and the agent has access to every locally installed application rather than a configured remote environment.

## Workflow Overlap and Selection

Tool overlap across categories is the norm. Claude Code, Cursor, and GitHub Copilot each span all four workflow types, which means the taxonomy describes interaction modes, not product categories. When selecting a coding agent workflow, the relevant question is what the task requires: real-time inline guidance (IDE), complex coordinated changes across a large codebase (terminal), asynchronous review on a shared branch (PR), or background execution of a well-scoped longer task (cloud). Using a high-autonomy cloud agent for a task requiring real-time iteration produces a completed artifact to review later — not the interactive feedback loop the task calls for.

## Key Claims

| Claim | Source | Date | Status | Support Score | Decay Exempt |
|---|---|---|---|---|---|
| AI coding agents operate through a continuous read-reason-act-evaluate loop, distinguishing them from autocomplete tools and one-shot chatbots by their capacity to autonomously navigate development workflows to task completion. | [[2026-realpython-coding-agent-workflow-types]] | 2026-04-29 | current | 1 | false |
| The same coding tool frequently spans multiple workflow types — Claude Code, Cursor, and GitHub Copilot each support IDE, terminal, PR, and cloud workflows — making workflow type a property of interaction mode rather than of the tool itself. | [[2026-realpython-coding-agent-workflow-types]] | 2026-04-29 | current | 1 | false |
| Cloud agents offer the highest autonomy by running in remote or managed environments and reporting back with branches or pull requests, but sacrifice real-time control and introduce code-leaves-machine privacy implications that require policy verification before use with proprietary code. | [[2026-realpython-coding-agent-workflow-types]] | 2026-04-29 | current | 1 | false |
| Pull request agents operate asynchronously on shared branches, triggering on PR open or update without developer supervision, functioning as a safety net before merging rather than a live steering tool. | [[2026-realpython-coding-agent-workflow-types]] | 2026-04-29 | current | 1 | false |
| Cloud-backed IDE and terminal agents send code to external servers for processing; local model options (Ollama, Continue) exist as alternatives for teams with proprietary code policies that prohibit external API access. | [[2026-realpython-coding-agent-workflow-types]] | 2026-04-29 | current | 1 | false |

## Teaching Notes

**Concept in plain terms.** AI coding agents come in four interaction modes — IDE (real-time in-editor assistance), terminal (shell-based with step-by-step approval), pull request (asynchronous code review), and cloud (remote autonomous execution) — each differing by where the agent runs, how much real-time control the developer retains, and what kind of task it handles best.

**Why it matters for instruction.** This taxonomy helps instructors counter the common assumption that AI coding tools are a single category. Practitioners who understand the four modes can match tool choice to task type, avoid misusing cloud agents for tasks requiring immediate feedback, and recognize that privacy and compliance implications vary significantly by mode — cloud agents and cloud-backed IDE agents send code to external servers, while local model setups do not.

**Common misconceptions.** Students often assume that the most autonomous agent (cloud) is the most capable for all tasks. Cloud agents sacrifice real-time control and require clear task scope — they produce branches or PRs to review later, not interactive guidance. For tasks requiring real-time iteration or complex multi-file coordination, terminal or IDE modes are more appropriate despite offering less autonomy.

**Suggested framing.** Introduce the four modes as a decision matrix: match real-time interactive editing to IDE, complex coordinated multi-file changes to terminal, asynchronous review to PR, and well-scoped background work to cloud. Ask students: which mode would you use if you needed to debug a subtle runtime error interactively? Which would you use if you needed to prototype a new feature over several hours without supervision?
