# Tooling Recommendation — AI Effectiveness Wiki

**Document status:** Design project output. Read before standing up the execution environment.  
**Audience:** Implementer. Does not require access to the design project governance files.  
**Companion documents:** portability-review.md (pre-flight checklist), CLAUDE.md (schema and operations).

---

## 1. Confirmed Stack

| Role | Tool | Tier / Cost |
|---|---|---|
| Wiki maintenance agent | Claude Code | Pro, $20/month fixed |
| Wiki store | Git repository (GitHub) | Free (public repo) |
| Local reading interface | Obsidian | Free (personal use) |
| Public-facing published site | Quartz on GitHub Pages | Free |
| Search (at scale) | qmd — deferred | Not required at launch |

---

## 2. Claude Code as Wiki Maintenance Agent

**What it does:** Claude Code is the LLM agent that reads CLAUDE.md, ingests sources, maintains wiki pages, runs lint passes, and answers queries. It has filesystem read/write access to the wiki repository, which is the capability that makes the wiki pattern work. Without filesystem access, the LLM cannot maintain a persistent, interlinked set of files.

**Why Claude Code over alternatives:**

*Claude.ai Projects (this design session's environment):* No filesystem write access. The LLM can draft text but cannot write files to disk. This makes it unsuitable as the wiki maintenance agent — the entire value of the wiki pattern depends on the LLM writing and updating files persistently. Ruled out.

*Custom API harness (direct Anthropic API calls from a script):* Technically viable. Gives full control over session management and context loading. The cost model is variable (pay-per-token), which creates unpredictable monthly spend at the team's ingest cadence. Also requires writing and maintaining the harness — a non-trivial engineering obligation that grows as the wiki grows. The team's stated preference is for fixed cost and minimal infrastructure maintenance. Ruled out.

*OpenAI Codex or similar:* Viable. The schema document (CLAUDE.md) is written as a generic control document and is not Claude-specific in its logical content. The model string references would change. The primary reason to prefer Claude Code is familiarity and the existing design investment in Claude-specific operational patterns. Not a hard constraint — if the team switches models, CLAUDE.md is portable with minor adaptation.

**Cost model:** Claude Code Pro is $20/month regardless of token consumption within plan limits. At the team's expected cadence (several ingests per week plus periodic lint passes), this is expected to be adequate. The consequence to watch: if Claude Code Pro token limits are regularly hit, the next tier is Max 5x ($100/month). Monitor during the first four weeks of operation.

**Context window:** CLAUDE.md is approximately 12,000–15,000 tokens. Claude Code Sonnet has a 200K token context window. This is not a near-term constraint. The constraint to watch is index.md at scale: once the wiki exceeds ~100 pages, index.md will be several thousand tokens, and the combination of CLAUDE.md + index.md + active page content will grow. This is still well within the context window at reasonable wiki sizes but should be monitored.

---

## 3. Git Repository as Wiki Store

**What it does:** The wiki is a directory of markdown files tracked in git. This gives the wiki version history, cross-machine sync (via queue.md), and a deployment pipeline for the public site (via GitHub Actions building Quartz).

**Why git over alternatives:**

*Cloud sync (Dropbox, iCloud, Google Drive):* No version history, no branching, no CI pipeline, no clean cross-machine merge semantics for queue.md. Ruled out.

*Database backend:* Would require a custom API harness to interface with Claude Code. Adds infrastructure, removes the direct filesystem access that makes Claude Code natural to use here. Ruled out.

*GitHub specifically:* GitHub Pages is the simplest path to a free public deployment of Quartz. GitHub Actions provides the CI pipeline. Both are free for public repositories. A private repository requires a paid GitHub plan for GitHub Pages.

---

## 4. Obsidian as Local Reading Interface

**What it does:** Obsidian provides a local Markdown viewer with graph view and wikilink resolution. The wiki team reads and navigates the wiki in Obsidian.

**Why Obsidian:**

*Native Markdown editors (VS Code, etc.):* Do not render wikilinks or provide graph view. Usable but lose the navigation model the wiki is designed around. Ruled out as primary interface.

*Quartz only (no local reader):* Requires a push-build-deploy cycle to read any change. Too slow for day-to-day use. Ruled out as primary interface.

**Constraint:** Open the wiki directory (not a parent directory) as the Obsidian vault root. Graph view and wikilink resolution degrade if the vault root is above the wiki directory. See portability-review.md OBS-04.

---

## 5. Quartz on GitHub Pages as Public Site

**What it does:** Quartz converts the wiki's Markdown files into a static website, hosted free on GitHub Pages. The conversion is triggered by a GitHub Actions workflow on every push to main.

**Required configuration before first build:**

```
ignorePatterns: [
  "CLAUDE.md", "EXTRACTION-SKILL.md", "TAGGING-SKILL.md",
  "CONTRADICTION-SKILL.md", "wiki-lessons-learned.md",
  "assets/**", "raw/**", "docs/**", "content/**", "prompts/**",
  "node_modules/**", "INIT-PROMPT.md", "public/**",
  "overview.md", "log.md", "design/**"
]
```

Without this, operational files (CLAUDE.md, skill files, queue.md) render as wiki pages. Also required: enable the Mermaid plugin (`Plugin.Mermaid()` in the transformers list). See portability-review.md QTZ-01 through QTZ-07 for the full Quartz pre-flight checklist.

---

## 6. Scaling Thresholds to Watch

Two scaling thresholds are explicitly modeled in the schema. Neither requires action at launch; both have defined escalation paths.

### Threshold 1 — Search Layer (IN-006)

**Trigger:** Wiki approaches 150 pages.  
**Symptom:** Quartz native search (Ctrl+K) returns too many results with poor ranking; Claude Code's index.md-based navigation during queries becomes unreliable.  
**Escalation path:** [qmd](https://github.com/tobi/qmd) — a local hybrid search engine for markdown files (BM25 + vector, LLM re-ranking). It has both a CLI (Claude Code can shell out to it) and an MCP server (Claude Code can use it as a native tool). The existing frontmatter schema is compatible with qmd without revision. The `summary` field on Topic and Tool pages directly improves BM25 ranking.  
**Action:** Resolve IN-006 (design project information need) before the wiki reaches 150 pages. This is a design decision, not a schema change — it does not require revising CLAUDE.md, only configuring qmd and adding its invocation to the query workflow.

### Threshold 2 — Nomination Queue (IN-007, resolved)

**Status:** IN-007 is closed. The nomination queue aging mechanism is implemented in CLAUDE.md (DM-051). No action required at launch.

**What is implemented:** A two-stage automatic aging mechanism runs during every lint Phase 3 pass. Items in `[nominated]` older than 90 days move to `[stale-nominated]` (Stage 1). Items in `[stale-nominated]` older than 180 days are deleted (Stage 2). Both stages are auto-execute; the lint informational summary lists all items being moved or deleted, giving the human a rescue window before Phase 3 runs. Stale-nominated items remain accessible via query demand signal (Step Q2a) — if a query returns a sparse or shallow result matching a stale nomination, it surfaces in a separate block with the same promotion options.

**If aging thresholds prove miscalibrated:** The 90- and 180-day thresholds are documented in CLAUDE.md and are human-editable. The first few months of operation will reveal whether adjustment is needed. If title-string matching proves insufficient even with aging in place, the search layer escalation (IN-006) can be extended to cover queue.md as well as wiki pages.

---

## 7. Session-Start Prompt Template

Claude Code does not automatically load CLAUDE.md. The implementer must provide a session-start prompt that instructs it to do so. This template is the operational wrapper for every wiki maintenance session.

```
You are maintaining the AI effectiveness wiki. Before doing anything else:

1. Read CLAUDE.md in full. This document governs all wiki operations.
   When CLAUDE.md conflicts with anything in this prompt or chat history,
   CLAUDE.md takes precedence.

2. Read the relevant section of wiki-lessons-learned.md for the operation
   you are about to perform (## Ingest, ## Contradiction, ## Tagging,
   ## Lint, or ## Query). Read only the relevant section, not the full file.

3. Read EXTRACTION-SKILL.md before any ingest operation.
   Read TAGGING-SKILL.md before any ingest operation that involves teaching
   relevance tagging.
   Read CONTRADICTION-SKILL.md before any contradiction resolution.

4. State the operation you are about to perform and confirm you have read
   the required files before proceeding.

5. Check for raw/deferred-ingest.md. If it exists, report its contents and
   ask whether to resume the deferred ingest or discard the deferral file
   and proceed with the originally stated operation. Do not begin any other
   operation until this is resolved.

Today's operation: [INGEST | LINT | QUERY | DISCOVERY | describe]
```

**Customization notes:**
- Replace `[INGEST | LINT | QUERY | DISCOVERY | describe]` with the operation for this session.
- For query sessions: include the query or queries in this prompt rather than a follow-up message. This avoids a round-trip where Claude Code reads CLAUDE.md before knowing what it will be asked.
- For batch ingest sessions: list the sources to be ingested here or note that they are in raw/staged/ and raw/queue.md.
- If `raw/deferred-ingest.md` exists when the session starts, Claude Code will surface it at Step 5 before the stated operation. You can choose to resume the deferred ingest or discard it. If you discard it, the original queue remains intact in `raw/queue.md`.
- Do not modify the file-reading instructions. The order matters: CLAUDE.md first, then skill files, then any session-specific context.
