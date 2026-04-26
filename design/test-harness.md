# Wiki Test Harness — Specification

**Document status:** Design project output.
**Audience:** Wiki operator setting up or verifying the wiki configuration.
**Authority:** CLAUDE.md governs wiki operations. This document specifies how to
verify that the configuration and operational behavior conform to CLAUDE.md.

---

## 1. Purpose and Scope

The test harness defines two tiers of verification for the AI effectiveness wiki:

**Tier 1 — Configuration and Conformance Checks** ("unit tests"): Deterministic,
read-only checks that a human can run at any time without starting a Claude Code session.
Expressed as `wiki-verify.sh`. Catches configuration drift and scaffold file corruption
before it causes ingest or lint failures.

**Tier 2 — Workflow Smoke Tests** ("integration tests"): Human-verified tests that
run actual wiki operations against real sources. Confirms that the wiki agent's end-to-end
behavior conforms to the ingest, lint, and query workflows specified in CLAUDE.md. Not
automated — pass/fail determination is a human judgment against the criteria listed here.

**What this harness does not cover:**
- Correctness of Key Claims extraction (EXTRACTION-SKILL.md governs this)
- Teaching relevance tagging accuracy (TAGGING-SKILL.md governs this)
- Contradiction path logic accuracy (CONTRADICTION-SKILL.md governs this)
- RAG query quality at scale

These are operational calibration concerns, not one-time conformance checks.

---

## 2. Tier 1 — Configuration Conformance Checks

### 2.1 Decision: Form of Tier 1 Checks

Three options were evaluated:

| Option | Verdict | Reason |
|--------|---------|--------|
| Shell script (`bash wiki-verify.sh`) | **Selected** | Deterministic, re-runnable, zero cognitive overhead, no session budget consumed |
| Claude Code verification prompt | Rejected | Non-deterministic; LLM can miss checks the same way it misses things in operations |
| Structured Markdown checklist | Rejected | Human-executed, error-prone, doesn't scale |

Determinism is the primary value of Tier 1. The checks are mechanical (string presence,
integer validation, file existence, count comparison) — shell's native domain.

### 2.2 Environmental Assumptions

These are the conditions `wiki-verify.sh` takes for granted. Failure to meet them
produces incorrect results without explicit error messaging:

| Assumption | Risk if violated |
|------------|------------------|
| bash 3.2+ available | Script will fail with syntax errors if bash is absent or older |
| Standard POSIX tools present: `grep`, `find`, `wc`, `awk` | Individual checks silently skip or produce wrong output |
| Script run from wiki repository root (directory containing CLAUDE.md) | Abort at entrypoint guard; script exits immediately |
| `.git/` directory present | Section 3 (hook check) reports false FAIL |
| No yq, python, or node required | Not a risk — script has no such dependencies |

YAML field checks use `grep -E "^FIELD:"` patterns, not a YAML parser. This is correct
for flat scalar frontmatter with controlled field names. It will not detect fields that
are nested, quoted, or appear mid-document outside a frontmatter block.

### 2.3 Check Catalogue

`wiki-verify.sh` runs seven check groups. Each check emits `[PASS]`, `[FAIL]`, or
`[WARN]`. Exit code 1 if any `[FAIL]`; exit code 0 otherwise.

| Group | Checks | Rationale |
|-------|--------|-----------|
| 1. `quartz.config.ts` | 16 required ignorePatterns entries; `"index.md"` absence (WARN); baseUrl not default placeholder | QTZ-01; DM-070; FRIC-012, FRIC-014, FRIC-015 |
| 2. `.gitignore` | `raw/staged/`, `raw/processed/`, `!**/.gitkeep` present | GIT-06; INIT-PROMPT.md Step 8 |
| 3. Pre-commit hook | File exists; executable; covers wiki content dirs; contains `[A-Z ]` rejection pattern | GIT-03; CLAUDE.md Section 4 |
| 4. Scaffold file conformance | All five singleton .md files exist with required frontmatter fields and correct `type` values; `raw/queue.md` has all four section headers; raw/ support files exist; skill files exist | CLAUDE.md Section 2.1, 5.7–5.9 |
| 5. Page count consistency | `total_pages` in `overview.md` matches actual `.md` file count in `topics/`, `tools/`, `sources/`, `comparisons/`, `pitfalls/` | CLAUDE.md Section 5.7 |
| 6. Naming convention | No `.md` file in a wiki content directory contains uppercase letters or spaces in its filename | DM-014; CLAUDE.md Section 4 |
| 7. Stray .md files at root | No `.md` files at wiki root other than the 10 defined singletons and operational files | CLAUDE.md Section 2 |

### 2.4 Usage

```bash
# From the wiki repository root:
bash wiki-verify.sh
```

Run:
- Before the first ingest (part of the Phase 2 verification checklist)
- After any manual edit to `quartz.config.ts`, `.gitignore`, or scaffold files
- After schema changes that affect frontmatter or directory structure
- When a lint or ingest failure produces unexpected behavior and the root cause is unclear

The script is read-only. It is safe to run at any time.

### 2.5 Maintenance

When the schema changes, update the script in the following cases:

| Schema change | Required script update |
|---------------|----------------------|
| New entry added to ignorePatterns | Add to `REQUIRED_PATTERNS` array in Section 1 |
| New required scaffold file | Add existence check and field checks to Section 4 |
| New required frontmatter field on overview.md | Add to `check_scaffold_fields` call for overview.md |
| New required section in `wiki-lessons-learned.md` | Add to Section 4 section-header check loop |
| New required section in `raw/queue.md` | Add to Section 4 queue section-header check loop |
| New allowed `.md` file at wiki root | Add to `ALLOWED_ROOT` array in Section 7 |
| Naming convention change (e.g., new character class) | Update grep pattern in Section 6 |

---

## 3. Tier 2 — Workflow Smoke Tests

Tier 2 tests run actual wiki operations in a Claude Code session and verify the
observable outputs against the pass criteria below. All four tests run on the
production wiki using real sources. Sources selected for smoke tests should be
genuinely useful to the wiki — not synthetic or throwaway.

**Pre-condition for all Tier 2 tests:** Tier 1 must pass before running any Tier 2 test.

**Sequence:** Tests must run in order. Each subsequent test depends on state from the prior test.

**How to verify:** After each Claude Code session that runs a smoke test, read the
produced files and compare outputs against the pass criteria. Pass/fail is a human
judgment — there is no automated assertion layer.

### 3.1 Ingest Smoke Test

**Purpose:** Verify the end-to-end happy-path ingest workflow.

**Source selection criteria:**
- Source type: industry-blog (institutional tier: AI lab or academic institution)
- Length: 800–1,200 words. Sources shorter than 800 words may not yield 3 Key Claims;
  sources longer than 1,200 words increase fetch-truncation risk unless pre-staged.
- Content: introduces a named technique, methodology, or capability — something
  that clearly maps to a new Topic or Tool page and yields at least 3 extractable claims.
- Not already in `sources/` (no URL match in the wiki).
- Not vendor-content (avoids vendor_bias complication on a first verification).

**Pre-conditions:**
- Tier 1 passes.
- Source URL added to `raw/queue.md` `[queued]` section, or source file placed in `raw/staged/`.
- Session-start prompt used per implementation-handoff.md Section 5.

**Pass criteria — in order of verification:**

| # | Observable output | Location to check |
|---|-------------------|-------------------|
| P1 | Pre-flight report generated and presented before any files are written | Claude Code output |
| P2 | At least one forced choice in the pre-flight report (source type, at minimum) | Claude Code output |
| P3 | Source page created in `sources/` with correct frontmatter fields: `type: source`, `source_type`, `credibility_tier`, `url`, `ingested_date`, `title`, `status: active`, `ingest_via` | `sources/<slug>.md` |
| P4 | Source page has a prose summary paragraph in the body (below frontmatter) | `sources/<slug>.md` |
| P5 | At least one Topic or Tool page created or updated with at least 3 Key Claims in a table; each claim cites the new source slug | `topics/<slug>.md` or `tools/<slug>.md` |
| P6 | `index.md` updated with entries for all new pages | `index.md` |
| P7 | `overview.md` `total_pages` incremented by the number of new content pages; `total_sources` incremented by 1 | `overview.md` |
| P8 | Processed queue entry in `raw/queue.md` `[processed]` section with `processed: YYYY-MM-DD` appended | `raw/queue.md` |
| P9 | `log.md` has a new entry with prefix `## [YYYY-MM-DD] ingest \|` | `log.md` |

**Common failure modes to watch for:**
- Pre-flight report skipped entirely → Step 0 budget check may have been interpreted incorrectly
- Source page created with no body paragraph → FRIC-020 regression; verify CLAUDE.md Step 10 is being followed
- Topic/Tool page not created → agent may have classified source as requiring no new page; check pre-flight report for the routing decision
- `total_pages` not incremented → likely a Phase 2 execution miss; check log.md for whether the ingest was marked complete

### 3.2 Contradiction Smoke Test

**Purpose:** Verify that the contradiction detection and Path B (human-review) flag workflow fires correctly.

**Source selection criteria:**
- A second source that makes a directly conflicting claim about something established by the Ingest Smoke Test source.
- Conflict type: quantitative (different metric values for the same thing), categorical (does/does not), or temporal (claim superseded by newer source).
- Both sources should be institutional-tier (credibility tier 2) so the support score difference is 0 — this guarantees Path B fires (difference ≤ 2) and produces a predictable, verifiable state change.
- If a natural pair cannot be found, an institutional source that directly contradicts a claim in the first source on a measurement or benchmark result is the best option.

**Pre-conditions:**
- Ingest Smoke Test completed and passed.
- Second source not yet ingested.

**Pass criteria:**

| # | Observable output | Location to check |
|---|-------------------|-------------------|
| P1 | Pre-flight report identifies the specific claim conflict and proposes Path B disposition | Claude Code output |
| P2 | A CTRD-001 (or next sequential ID) assigned | `overview.md` `last_contradiction_id` incremented; CTRD-ID appears in output |
| P3 | `open_contradictions` list field added to the affected Topic or Tool page frontmatter with the CTRD-ID | Affected content page frontmatter |
| P4 | Inline marker `contested [CTRD-001]` appended to the contested Key Claim row in the page body | Affected content page body |
| P5 | `overview.md` `open_contradictions` integer counter incremented by 1 | `overview.md` |
| P6 | `log.md` has a new entry with operation `contradiction-flag` | `log.md` |

**What to verify does NOT happen:**
- The contested claim should not be silently overwritten (that would be Path A behavior).
- The second source's conflicting claim should be added as a new Key Claim row with a lower support score, not used to replace the original.

### 3.3 Lint Smoke Test

**Purpose:** Verify that the lint procedure runs without false positives and correctly updates derived artifacts.

**Pre-conditions:**
- Both prior smoke tests completed and passed.
- At least one ingested Topic or Tool page is tagged `teaching_relevance: true` (if none exists, the Teaching Index regeneration criterion cannot be tested — note as untested if so).

**Procedure:** Run a lint session using the session-start prompt with `Today's operation: LINT`.

**Pass criteria:**

| # | Observable output | Location to check |
|---|-------------------|-------------------|
| P1 | L1 (queue.md CTRD-NNN scan): surfaces CTRD-001 as an open contradiction from queue.md — OR correctly reports no queue signals if CTRD-001 was not added to queue.md | Claude Code output |
| P2 | L4b: CTRD-001 surfaced as a forced choice in the lint pre-flight report | Claude Code output |
| P3 | L11 conformance check: no false summary-field violations on the Pitfalls or Comparison pages (if any exist) | Claude Code output |
| P4 | L12 naming convention: no violations reported (assuming smoke test sources followed naming rules) | Claude Code output |
| P5 | Teaching Index regenerated if at least one `teaching_relevance: true` page exists | `teaching-index.md` updated date |
| P6 | `collection-gaps.md` updated with any coverage notes the agent identifies | `raw/collection-gaps.md` |
| P7 | `overview.md` `last_lint` field populated with today's date | `overview.md` |
| P8 | `log.md` has a new entry with operation `lint` | `log.md` |

**False positive check (critical):** If any `[FAIL]` or warning appears in the lint report that is NOT explained by actual content or configuration issues, treat it as a false positive and log it as a potential FRIC entry.

### 3.4 Query Smoke Test

**Purpose:** Verify that the query workflow produces wiki-grounded responses and correctly offers to file valuable results.

**Pre-conditions:**
- All prior smoke tests completed and passed.
- At least one Topic or Tool page exists with content from the ingested sources.

**Query selection:** Choose a query whose answer is covered by the ingested material — one of the five named query patterns from IN-001:
- "What are the current capabilities and limitations of X?" (for a Tool page)
- "What does the wiki know about [technique/approach]?" (for a Topic page)

**Procedure:** Run a query session using the session-start prompt with `Today's operation: QUERY [your query]`.

**Pass criteria:**

| # | Observable output | Location to check |
|---|-------------------|-------------------|
| P1 | Response cites specific wiki pages (not raw source URLs) for claims | Claude Code output |
| P2 | If `teaching_relevance: true` pages exist, Teaching Index is consulted and referenced if relevant to the query | Claude Code output |
| P3 | Step Q6 filing criterion assessed: if the response has derived value (Comparison, synthesis), a forced choice is offered before any file is written | Claude Code output |
| P4 | `log.md` has a new entry with operation `query`, including `result_quality` and `topic_tags` fields | `log.md` |

**What to verify does NOT happen:**
- Response should not cite raw source URLs directly (sources are cited via wiki page wikilinks).
- A Comparison or synthesis page should not be written without the filing forced choice having been presented and confirmed.

---

## 4. When to Run Each Tier

| Trigger | Tier 1 | Tier 2 |
|---------|--------|--------|
| Before first ingest (Phase 2 verification) | Run | Run (all four tests, in sequence) |
| After manual edit to `quartz.config.ts`, `.gitignore`, or scaffold files | Run | Not needed |
| After schema changes affecting frontmatter or directory structure | Run | Consider if changes touch workflow steps |
| After a CLAUDE.md version update | Run | Consider running ingest and lint smoke tests |
| When an ingest or lint failure produces unexpected behavior | Run | Not needed (Tier 1 diagnoses configuration issues) |
| Periodically as the wiki grows (every ~50 pages) | Run | Not needed unless behavior changes observed |

---

## 5. Environmental Assumptions (document-level)

This document takes the following execution environment for granted, consistent with
the confirmed stack (portability-review.md, DM-007):

| Component | Assumption |
|-----------|------------|
| Wiki agent | Claude Code (Pro tier, $20/month) |
| Version control | git repository; GitHub Actions for Quartz build |
| Local reading | Obsidian (vault root = wiki directory) |
| Public publication | Quartz on GitHub Pages |

Tier 2 tests require a functioning Claude Code session with the session-start prompt
(implementation-handoff.md Section 5). They cannot be run without Claude Code access.
Tier 1 requires only a terminal with bash. Both tiers require the wiki repository to
be locally available (git cloned).
