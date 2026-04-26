# Portability Review — Environmental Assumptions Checklist

**Document status:** Design project output. Read before touching the wiki repository.  
**Audience:** Implementer setting up the execution environment.  
**Authority:** CLAUDE.md governs wiki operations. This document validates the assumptions
CLAUDE.md makes about the environment in which it will run. Where an assumption is
unverified, the pre-flight action must be completed before first ingest.

Validation statuses:
- **confirmed** — decided and recorded in decisions_made.md; no implementation test needed
- **unverified** — plausible but not tested; complete the pre-flight action before first use
- **requires implementation test** — cannot be validated without running the actual stack

---

## 1. Claude Code

| # | Assumption | Where Used in CLAUDE.md | Status | Pre-Flight Action |
|---|---|---|---|---|
| CC-01 | Claude Code has read/write filesystem access to the wiki repository directory | All ingest, lint, and query workflow steps that write files | confirmed (DM-007) | Verify working directory is set to wiki repo root at session start |
| CC-02 | Claude Code can fetch URLs over the network during ingest | Section 11.2 Step 1 — URL intake from queue.md | unverified | Test a URL fetch from a known institutional domain (e.g., anthropic.com/news) before first ingest session; confirm no proxy or network policy blocks egress |
| CC-03 | URL fetch failures are surfaced as errors, not silent nulls | Section 11.2 — "[fetch-failed]" tagging logic | requires implementation test | Attempt fetch of a known bad URL; verify Claude Code reports the failure explicitly rather than returning empty content |
| CC-04 | Claude Code's context window is large enough to hold CLAUDE.md plus active operation state in a single session | All operations — CLAUDE.md must be loaded alongside session content | unverified | Measure CLAUDE.md token count before first use. Current estimate: ~12,000–15,000 tokens. Claude Code Sonnet has a 200K token context window; this is not a near-term constraint, but monitor as CLAUDE.md grows. See DM-016 consequence. |
| CC-05 | Claude Code can read the full index.md in a single pass during query and lint operations | Section 11.4 Step L2, Section 11.5 Step Q2 | requires implementation test | At ~150 pages, index.md will be substantial. Test index.md read performance before the wiki reaches 100 pages. |
| CC-06 | Claude Code Pro tier ($20/month) provides sufficient token capacity at the team's ingest cadence (several ingests per week) | DM-007 — cost and tier decision | unverified | Monitor token consumption over the first four weeks of operation. If Pro limits are regularly hit, escalate to Max 5x per DM-007 consequence. |
| CC-07 | Claude Code can shell out to CLI tools (relevant to future qmd search integration) | Section 12 scale note — qmd as escalation path | unverified | Not required at launch. Validate before implementing IN-006 search escalation. |
| CC-08 | Skill files (EXTRACTION-SKILL.md, TAGGING-SKILL.md, CONTRADICTION-SKILL.md) are present in wiki root before operations begin | Section 1 — pre-operation read instructions | confirmed (DM-041) | Starter templates for all three skill files were produced in the design project (DM-041). Copy EXTRACTION-SKILL.md, TAGGING-SKILL.md, and CONTRADICTION-SKILL.md from design project output to wiki root before first ingest. Do not run ingest without EXTRACTION-SKILL.md at minimum. |
| CC-09 | wiki-lessons-learned.md exists and is organized by operation type before first operation | Section 1 — session start read instructions | unverified | Create wiki-lessons-learned.md with stub sections (## Ingest, ## Contradiction, ## Tagging, ## Lint, ## Query) before first ingest. |
| CC-10 | Claude Code reads CLAUDE.md at the start of every wiki maintenance session | Section 1 — stated requirement | requires implementation test | Claude Code does not load CLAUDE.md automatically. A session-start prompt template is a required implementation artifact — it must exist before the first wiki operation and must explicitly instruct Claude Code to read CLAUDE.md and the relevant skill file before proceeding. This template is separate from CLAUDE.md itself; it is the operational wrapper that invokes the schema. It must also instruct Claude Code to read the relevant section of wiki-lessons-learned.md before each operation type. Produce this template before first use. |
| CC-11 | YouTube transcript extraction tooling is available | Section 11.2 Step 1 — "transcript extraction tool to be confirmed at implementation time" | unverified | Before ingesting any youtube-video source: confirm a transcript tool (e.g., yt-dlp with --write-auto-subs, or a manual export workflow). Document the chosen tool in CLAUDE.md Section 11.2 before first YouTube ingest. Do not leave this as a runtime decision. |
| CC-12 | Four operational singletons (overview.md, index.md, log.md, teaching-index.md) and three raw/ files (queue.md, collection-gaps.md, discovery-sources.md) are human-initialized before the first Claude Code session | Section 2.1 — Initialization Scaffold; Section 5.7 — last_contradiction_id and counter initialization | unverified | Create all seven files with the exact initial content specified in CLAUDE.md Section 2.1 before opening the first Claude Code session. overview.md must have last_contradiction_id: 0 and open_contradictions: 0 or Claude Code will stop on the first contradiction with no valid state to read. See also implementation-handoff.md Section 1.3. |
| CC-13 | INIT-PROMPT.md exists and is current before the Phase 1 initialization session | DM-046 — semi-automated initialization; INIT-PROMPT.md as first-class artifact | unverified | Obtain INIT-PROMPT.md from design project output before starting the Claude Code initialization session. Verify it is the current version — its scaffold file content must match CLAUDE.md Section 2.1. Do not paste an outdated version; scaffold field mismatches will produce incorrect initial state. |

---

## 2. Git / Repository

| # | Assumption | Where Used in CLAUDE.md | Status | Pre-Flight Action |
|---|---|---|---|---|
| GIT-01 | The wiki lives in a git repository | Section 2 directory structure, DM-007 | confirmed (DM-007) | Initialize repository before any wiki files are written. |
| GIT-02 | queue.md syncs across machines via git | Section 8.4, Section 11.2 — queue.md as cross-machine intake | confirmed (DM-019) | Confirm git remote is set up and the team has push/pull access before relying on queue.md for cross-machine coordination. |
| GIT-03 | Filenames are all-lowercase kebab-case with no spaces | Section 4 — naming conventions rationale | confirmed (DM-014) | This is enforced by convention, not tooling. The consequence of violation is a silent collision on macOS that becomes a hard failure on Linux CI (GitHub Actions). Add a pre-commit hook or CI lint step to reject filenames with uppercase characters or spaces in the wiki directories. |
| GIT-04 | GitHub Actions builds Quartz on push | Section 2 — quartz.config.ts ignorePatterns; DM-007 | unverified | Configure GitHub Actions workflow for Quartz build before first push of content. Validate that ignorePatterns suppresses CLAUDE.md, skill files, and raw/ from the published output. |
| GIT-05 | raw/ directory is committed to git (not gitignored) | Section 2, Section 11.3 — queue.md and discovery-sources.md are in raw/ | unverified | Confirm raw/ is tracked in git. If raw/staged/ contains large or copyright-restricted source files, add raw/staged/ to .gitignore while keeping raw/*.md tracked. |
| GIT-06 | Source files in raw/staged/ and raw/processed/ are not committed to git | Implicit — source documents may be large or under copyright | unverified | Add `raw/staged/` and `raw/processed/` to .gitignore (on separate lines). Use explicit tracking for raw/queue.md, raw/discovery-sources.md, raw/collection-gaps.md. Confirm this does not conflict with GIT-05. |

---

## 3. Obsidian

| # | Assumption | Where Used in CLAUDE.md | Status | Pre-Flight Action |
|---|---|---|---|---|
| OBS-01 | Obsidian resolves wikilinks by shortest unique filename match | Section 4 — wikilink convention | confirmed (DM-014) | Short-form wikilinks in prose rely on Obsidian's shortest-unique-match resolution. If two pages share a filename across different directories, resolution is ambiguous. The naming convention and pre-creation uniqueness check (Section 4) are the controls. No Obsidian configuration required. |
| OBS-02 | Mermaid diagrams render natively in Obsidian | Section 6.4 | confirmed | Mermaid is native to Obsidian as of version 0.12. Verify installed version is 0.12 or later. |
| OBS-03 | YAML frontmatter is not rendered to readers in Obsidian reading view | Section 8.3 rationale — two-component contradiction flag design | confirmed | Obsidian hides frontmatter in reading view by default. The inline Key Claims marker (contested [CTRD-NNN]) is the human-visible component. No configuration required. |
| OBS-04 | Obsidian vault root is set to the wiki directory | Section 2 — operational note | unverified | Open the wiki directory (not a parent directory) as the Obsidian vault. If the vault root is above the wiki directory, graph view and wikilink resolution will include non-wiki files. |
| OBS-05 | Full-path wikilinks in frontmatter fields (entities_compared, parent_entity) resolve correctly in Obsidian graph view | Section 4 — wikilink exception rule | unverified | Test that [[tools/openai-gpt-4o]] in a YAML frontmatter field appears in Obsidian graph view. Obsidian may not render frontmatter wikilinks in graph view in all versions. This is a usability gap, not a correctness issue — the constraint exists for lint type enforcement, not navigation. |

---

## 4. Quartz

| # | Assumption | Where Used in CLAUDE.md | Status | Pre-Flight Action |
|---|---|---|---|---|
| QTZ-01 | quartz.config.ts ignorePatterns is configured before first build | Section 2 — explicit [ENV] marker | confirmed (FRIC-012, FRIC-014, FRIC-015) | Before first Quartz build, add to quartz.config.ts: `ignorePatterns: ["CLAUDE.md", "EXTRACTION-SKILL.md", "TAGGING-SKILL.md", "CONTRADICTION-SKILL.md", "wiki-lessons-learned.md", "assets/**", "raw/**", "docs/**", "content/**", "prompts/**", "node_modules/**", "INIT-PROMPT.md", "public/**", "overview.md", "log.md", "design/**"]`. Do NOT add `"index.md"` — Quartz requires it to generate the root `index.html` home page. Without the full list, operational files, build output, and scaffold state files render as wiki pages. |
| QTZ-02 | Quartz renders Obsidian-style wikilinks | Section 4, Section 6 | confirmed (DM-007) | Quartz natively supports Obsidian wikilink syntax. Confirm the Quartz version in use supports short-form wikilink resolution matching Obsidian's behavior. |
| QTZ-03 | Quartz renders Mermaid diagrams | Section 6.4 | unverified | Quartz supports Mermaid via an explicit plugin. Verify `Plugin.Mermaid()` is included in the quartz.config.ts transformers list. |
| QTZ-04 | YAML frontmatter fields are not exposed to public readers in the chosen Quartz theme | Section 8.3 rationale | unverified | Some Quartz themes render frontmatter fields as visible page metadata. Verify that open_contradictions entries are not exposed to public readers. If they are, assess whether a theme override is needed or whether this is acceptable. |
| QTZ-05 | Quartz native search (Ctrl+K) is adequate up to approximately 150–200 pages | Section 12 scale note | unverified (heuristic estimate) | This is a design-session estimate, not a tested threshold. Monitor search result quality as the wiki grows. Resolve IN-006 before reaching 150 pages. |
| QTZ-06 | GitHub Pages hosts the Quartz build output as a public site | DM-007 | confirmed (DM-007) | GitHub Pages is free for public repositories. Confirm the repository is public, or that a paid plan is in place if the wiki should remain private. DM-007 explicitly ruled out private GitHub Pages due to cost. |
| QTZ-07 | Quartz build does not fail on unrecognized YAML frontmatter fields | All page types with custom frontmatter fields | unverified | Quartz may warn or fail on unrecognized frontmatter keys depending on configuration. Run a test build with a page containing full Topic page frontmatter before first production ingest. |

---

## 5. Deferred / Out of Scope at Launch

The following capabilities are referenced in CLAUDE.md as future escalation paths. They are not required at launch. Each has a defined trigger condition; do not implement before the trigger is reached.

| # | Capability | Trigger Condition | Reference |
|---|---|---|---|
| DEF-01 | qmd hybrid search (BM25/vector, MCP server) | Wiki approaches 150 pages; Quartz native search degrades | IN-006, Section 12 |
| DEF-02 | arXiv API integration for discovery pass | Lab blog feeds prove insufficient for domain coverage | Section 11.3, DM-022 |
| DEF-03 | Git LFS for assets/ | assets/ directory grows large enough to affect clone/push performance | DM-008 consequence |
| DEF-04 | Batch size limits for ingest pre-flight reports | Pre-flight reports grow too long for a single review session | DM-020 consequence |

Note: The nomination queue aging mechanism (formerly DEF-05) is implemented in CLAUDE.md
(DM-051, IN-007 closed). Two-stage automatic aging (90-day move to `[stale-nominated]`,
180-day deletion) runs during every lint Phase 3 pass. No action required at launch.

---

## 6. Pre-Flight Sequence

Complete these in order before the first wiki operation.

1. Initialize git repository; confirm remote and team access (GIT-01, GIT-02)
2. Configure .gitignore: track raw/*.md, ignore raw/staged/ and raw/processed/ (GIT-05, GIT-06)
3. Configure quartz.config.ts ignorePatterns (QTZ-01)
4. Enable Mermaid plugin in quartz.config.ts (QTZ-03)
5. Run a test Quartz build with a sample page containing full Topic frontmatter (QTZ-07)
6. Configure and test GitHub Actions Quartz build workflow (GIT-04)
7. Open wiki directory as Obsidian vault root — not a parent directory (OBS-04)
8. Create wiki-lessons-learned.md with stub operation-type sections (CC-09)
9. Create the initialization scaffold: seven files with exact initial content per CLAUDE.md Section 2.1 — overview.md, index.md, log.md, teaching-index.md, raw/queue.md, raw/collection-gaps.md, raw/discovery-sources.md. Confirm overview.md has last_contradiction_id: 0 and open_contradictions: 0 before proceeding. (CC-12)
10. Copy EXTRACTION-SKILL.md, TAGGING-SKILL.md, and CONTRADICTION-SKILL.md starter templates from design project output to wiki root (CC-08)
11. Test URL fetch from a known domain; confirm network egress is not blocked (CC-02, CC-03)
12. Confirm YouTube transcript tooling and document in CLAUDE.md Section 11.2 before first YouTube ingest (CC-11)
13. Obtain INIT-PROMPT.md from design project output before the Phase 1 initialization session (CC-13). For all subsequent maintenance sessions, establish the session-start protocol using the prompt template in implementation-handoff.md Section 5. Confirm Claude Code reads CLAUDE.md in full before taking any action on the first maintenance session. (CC-10, CC-13)
14. Add filename casing pre-commit hook or CI check (GIT-03)
15. Run a test ingest with a single low-stakes source before batch ingesting (validates all CC, GIT, QTZ items end-to-end)
