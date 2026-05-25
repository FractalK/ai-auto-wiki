# Hybrid Lint Architecture Assessment
**Last Updated:** 05/25/2026 20:00 EST

**Purpose:** Evaluate whether lint Phase 1 should be restructured as a hybrid
architecture — a Python script (`wiki-lint.py`) for mechanical checks, with the
LLM agent handling only judgment-requiring steps. This assessment responds to the
red-team finding immediately following DM-105: approximately 80% of Phase 1 steps
are fully mechanical, and the multi-session state file protocol may be solving the
wrong problem.

**Scope:** All six evaluation criteria from the carry-forward agenda, plus a lint
coverage gap analysis prompted by the architectural reconsideration.

---

## 1. Lint Coverage Gap Analysis

Before redesigning the lint architecture, this section identifies drift vectors the
current procedure does not cover. If any proposed checks are adopted, they flow into
the script scope (Section 3) and the mechanical-vs-judgment classification (Section 2).

### 1.1 Proposed New Checks

**Check G1 — Wikilink integrity (high value)**

No current lint step verifies that wikilinks in page prose and frontmatter point to
existing pages. A renamed, deleted, or mistyped wikilink produces a dead link on the
Quartz public site and a dimmed unresolved reference in Obsidian. This is the single
most visible drift vector to a site visitor.

Scope: scan all `[[...]]` patterns in non-source pages (prose and frontmatter). Build
a valid-slug set from the filesystem (all `.md` files in content directories, stripped
to slug form). Flag any wikilink whose target slug does not exist. Include structural
frontmatter fields (`entities_compared`, `derived_from`, `parent_entity`) — a broken
reference in these fields silently breaks lint cross-page checks (L5 comparison
staleness, L5 teaching-brief currency).

Classification: fully mechanical. Informational output — no forced choice, no
auto-execute. The human reviews broken links and decides whether to fix, redirect,
or remove.

Placement: Group C (cross-page analysis). Operates on a targeted grep scan, not full
page reads.

**Check G2 — Index.md ↔ filesystem parity (high value)**

L2 reads `index.md` as the authoritative catalog but does not cross-check against the
filesystem. `wiki-verify.sh` Group 5 checks `total_pages` count against the filesystem,
but count parity can mask offsetting errors (one page missing from index.md, one stale
entry in index.md for a deleted page — count matches, both defects invisible).

Scope: compare the set of page slugs in `index.md` against the set of `.md` files in
content directories. Flag pages on disk but absent from `index.md` (invisible to lint,
query, and Teaching Index). Flag entries in `index.md` with no corresponding file on
disk (stale catalog entries that produce broken links from the index page itself).

Classification: fully mechanical. Informational for missing-from-index (the page exists
and is functional, it is just invisible to catalog-based operations). Informational for
stale-entry (requires human decision on whether to delete the entry or restore the page).

Placement: enhances L2 (page inventory) — runs as part of Group A.

**Check G3 — Source reference integrity (high value)**

Each Key Claims table row contains a source wikilink. No current step verifies that
these wikilinks point to existing Source pages. A broken source reference means a Key
Claim cannot be traced to its evidence — a direct failure of the wiki's provenance
model. This is distinct from L6 (orphan detection, which finds pages with no inbound
links) and from G1 (which covers prose and frontmatter wikilinks generally but does
not specifically flag the provenance implication of a broken source reference).

Scope: for each Key Claims table row, extract the source wikilink(s). Verify each
points to an existing file in `sources/`. Flag broken references with the affected
page, claim text, and missing source slug.

Classification: fully mechanical. Informational — the human must decide whether to
locate the correct source, create a missing source page, or remove the claim.

Placement: Group B (per-page assessment) — runs during the single read of each
Topic/Tool page alongside L3.

**Check G4 — Overview.md counter accuracy (medium value)**

L4c verifies `open_contradictions` against the actual count. No step verifies
`total_pages` against L2 inventory or `last_contradiction_id` against the highest
CTRD-NNN in the wiki. `total_pages` drift is cosmetic in most cases but misleads the
human's sense of wiki size. `last_contradiction_id` drift is dangerous — if the counter
is lower than the actual highest CTRD-NNN, the next contradiction assignment will
produce a duplicate ID.

Scope: compare `overview.md` `total_pages` against L2 inventory count. Scan all
`open_contradictions` frontmatter entries and `log.md` `contradiction-flag` /
`contradiction-auto-resolved` entries for the highest CTRD-NNN; compare against
`overview.md` `last_contradiction_id`.

Classification: fully mechanical. `total_pages` drift: auto-correct (same as L4c ±1
pattern). `last_contradiction_id` drift: auto-correct upward only (correcting downward
would skip IDs, which is safe; correcting upward prevents duplicates). Flag as
informational if the counter needs correction.

Placement: Group C (uses data accumulated during Group B for contradiction IDs, plus
L2 inventory for total_pages).

**Check G5 — Status-content consistency (lower value)**

No current step flags pages where `status` contradicts content indicators. Examples:
`status: stub` with >3 Key Claims and >500 words of prose (page has grown past stub
but status was never updated). `status: current` with `last_assessed` absent (page has
never been evaluated but claims to be current). `status: current` with zero Key Claims
(empty content page marked as current).

Scope: for each page, compare `status` against content metrics (Key Claims count,
prose word count, `last_assessed` presence). Flag inconsistencies.

Classification: fully mechanical (the conditions are all checkable from frontmatter and
word count). Informational only — no auto-execute, as the correct resolution depends on
whether the content or the status is wrong.

Placement: Group B (per-page assessment) — runs during the single read of each page.

### 1.2 Gap Summary

| ID | Check | Value | Mechanical? | Proposed Group |
|---|---|---|---|---|
| G1 | Wikilink integrity | High | Yes | C |
| G2 | Index ↔ filesystem parity | High | Yes | A (enhances L2) |
| G3 | Source reference integrity | High | Yes | B |
| G4 | Overview counter accuracy | Medium | Yes | C |
| G5 | Status-content consistency | Lower | Yes | B |

All five proposed checks are fully mechanical — they add no judgment load to the agent.
In the hybrid model, they are pure script work. G1, G2, and G3 are recommended for
immediate adoption. G4 and G5 are recommended as low-cost additions given that the
script infrastructure will exist anyway. None require forced choices; all produce
informational findings for human review.

---

## 2. Mechanical vs. Judgment Classification

Each Phase 1 step is classified into one of three categories:

- **M (Mechanical):** The script produces the complete finding, including its
  classification (auto-execute, forced-choice, or informational) and all contextual
  data. No agent involvement needed.
- **D (Data-assembly mechanical, judgment residue):** The script gathers all data and
  produces a partial finding with context. The agent reviews and completes a judgment
  element — typically the `recommended` value for a forced choice, or a classification
  decision the script cannot make.
- **J (Judgment-primary):** The agent must do the substantive work. The script may
  provide supporting data but cannot produce the finding.

### 2.1 Classification Table

| Step | Description | Category | Rationale |
|---|---|---|---|
| **L1** | queue.md CTRD-NNN scan | **M** | Regex pattern match + cross-reference against frontmatter `open_contradictions` by ID. All inputs are structured text. |
| **L1a** | Nomination queue aging | **M** | Date field parsing + arithmetic (age in days). Thresholds (90, 180) are constants. |
| **L2** | Page inventory | **M** | Read `index.md`, count entries by type. Pure parsing. |
| **L3** | Support score recalculation | **M** | Credibility weight lookup (3/2/1/0), decay multiplier (0.5×, 12-month threshold), sum, round. Requires cross-page read of source pages for `published_date` and `credibility_tier` — expensive for the agent, trivial for a script. |
| **L4a** | Contradiction flag expiry | **M** | Date comparison: `override_window_closes` vs. today. |
| **L4b** | Open contradiction surfacing | **D** | Detection is mechanical (same date comparison as L4a, opposite condition). Context assembly is mechanical (claim text, source, score, window date). **Judgment residue:** the `recommended` value (confirm/override/skip) requires assessing whether the contesting source's evidence is stronger — the agent must evaluate this. The script outputs the finding with `recommended: null`. |
| **L4c** | open_contradictions counter reconciliation | **M** | Count accumulated during Group B vs. `overview.md` value. ±1 vs. ±2+ threshold is arithmetic. |
| **L5** | Staleness checks (Topic/Tool) | **M** | `last_assessed` date vs. 90-day threshold. Date arithmetic. |
| **L5** | Staleness checks (Comparison) | **M** | Read `entities_compared`, follow wikilinks to entity pages, compare `last_assessed` (or fallback `updated`) against comparison `updated`. All date comparisons. |
| **L5** | Staleness checks (Teaching-brief) | **D** | Detection is mechanical (constituent page `last_assessed` vs. brief `last_reviewed`). Context assembly is mechanical. **Judgment residue:** `recommended` value. The default is A (regenerate), but the agent should confirm. Low judgment — script can set `recommended: "A"` and the agent can override. Borderline M/D — classified D for safety. |
| **L5a** | Stale → current upgrade check | **M** | Two conditions: `last_assessed` within 90 days (date arithmetic) + `open_contradictions` empty (frontmatter check). Both mechanical. Forced choice, but the recommendation is deterministic: if both conditions are met, recommend A. |
| **L5b** | Teaching notes currency check | **M** | Date comparison: `teaching_notes_reviewed` vs. `last_assessed`, 90-day gap. Informational only. |
| **L5c** | Data Records freshness check | **M** | Parse `## Data Records` table rows for `Measurement Date`, find most recent `current` row, compare against 90-day threshold. |
| **L6** | Orphan page detection | **M** | Wikilink grep across content directories. Set difference: all pages minus pages with inbound wikilinks. Informational only. |
| **L7** | Concept gap detection | **D** | Term frequency counting across prose sections is mechanical (the script can tokenize prose, exclude frontmatter/tables/headers, count term appearances across pages, and check against `index.md` for existing pages). **Judgment residue:** "exclude proper nouns already captured as Tool pages under a different slug" requires understanding that e.g., "GPT-4" maps to `openai-gpt-4`. The script outputs raw candidate terms with page references and appearance counts; the agent filters aliases and sets the forced choice type (A=stub Topic, B=stub Tool, C=dismiss). |
| **L8** | Pitfalls page maintenance | **M** | Count H3 headings with `**Status:**` field. Compare against `failure_mode_count`. Check for mandatory H2 section headings. All structural parsing. |
| **L9** | decay_exempt proposals | **D** | Conditions (b) and (c) are mechanical: (b) scan `log.md` for `contradiction-flag` entries referencing the page/claim; (c) count independent sources with `credibility_tier` peer-reviewed or institutional. **Judgment residue:** condition (a) — "the claim is definitional or foundational, not empirical" — is a semantic classification the script cannot make. The script identifies all claims passing (b) + (c) and outputs them with full context; the agent evaluates (a) and decides whether to surface each as a forced choice. |
| **L10** | Teaching Index completeness ratio | **M** | Ratio: `teaching_tagged_count` / (`topic_tool_count` - `topic_tool_deprecated_count`). Compare against 0.20 threshold. All arithmetic on counts accumulated during Group B. |
| **L11** | Schema conformance check | **D** | Most criteria are mechanical: Key Claims count (row count), prose length (word count), required frontmatter (field presence), summary field (presence + single-sentence heuristic), status vocabulary (value check against controlled set), mandatory sections (heading check), derived claim sourcing (annotation check), minority view sourcing (annotation check). **Judgment residue:** "Claim granularity — no topic labels" partially requires semantic judgment. The script can flag semicolons, question marks, and very short claims (< 6 words with no verb) mechanically. The "no topic labels" condition (e.g., a claim that is just "AI alignment" instead of an assertable sentence) requires the agent to review flagged candidates. The script outputs all mechanical violations as confirmed findings and candidate granularity violations as agent-review items. |
| **L12** | Collection gap analysis | **M** | Read `log.md` query entries, aggregate by `topic_tags` and `result_quality`. Cross-reference Source page `ingested_date` values. All structured data parsing and aggregation. |
| **L12a** | Session stats threshold check | **M** | Count `session-stats` entries in `log.md`. Compare against 50 threshold. If A selected, the inline analysis (rate of limit hits, source type mix) requires reading structured log data — this is mechanical aggregation, not judgment. |
| **L12b** | Deferred ingest staleness check | **M** | Check file existence + `created` date vs. 14-day threshold. |
| **L12c** | Override pattern detection | **D** | Extracting entries from `wiki-lessons-learned.md` within a 30-day window is mechanical. **Judgment residue:** categorizing each entry's `**What was wrong:**` text into one of five root cause categories (schema definition overlap, inference gap, human preference drift, vocabulary gap, source ambiguity) requires reading prose and making a classification judgment. The script extracts entries with their raw text; the agent categorizes. |
| **L12d** | Schema Signals age check | **M** | Date arithmetic on `## Schema Signals` entries with `**Status:** open`. |
| **L14** | Skill file enrichment staleness | **M** | Scan for "TO BE ENRICHED" sections + check for placeholder vs. real content + count `ingest` entries in `log.md`. All text pattern matching and counting. |
| **L15** | Teaching-tagged pages missing fields | **M** | Check `teaching_relevance: true` + missing `competency_domains` or `professional_contexts`. Frontmatter field presence check. |
| **L16** | Wikilink proliferation scan | **M** | Alias map construction from frontmatter + slug normalization + word-boundary regex match + topical proximity check (shared related_topics/related_tools or same directory). All mechanical. Outputs one batch forced-choice (Tier 1) and informational findings (Tier 2). |
| **L13** | Generate decision form | **D** | Assembling the choices JSON structure, serializing it, and injecting it into the HTML template is mechanical. **Judgment residue:** setting `recommended` values across all forced choices. For most forced choices, the recommendation is deterministic or follows from the data (L5a: always A; L10: always A; L12a: always B). For judgment-requiring choices (L4b, L7, L9), the agent must set recommendations. The script cannot produce the final form — it produces the data; the agent sets recommendations and generates the form. |

### 2.2 Classification Summary

| Category | Steps | Count |
|---|---|---|
| **M** (fully mechanical) | L1, L1a, L2, L3, L4a, L4c, L5 (Topic/Tool), L5a, L5b, L5c, L6, L8, L10, L12, L12a, L12b, L12d, L14, L15, L16 | 20 |
| **D** (data-assembly + judgment residue) | L4b, L5 (Teaching-brief), L7, L9, L11, L12c, L13 | 7 |
| **J** (judgment-primary) | — | 0 |

No step is purely judgment with no mechanical component. Every step has a substantial
mechanical portion that the script handles. The 7 D-category steps have narrowly scoped
judgment residues — the agent reviews pre-assembled data and makes a specific decision,
rather than reading raw wiki pages from scratch.

### 2.3 Proposed New Checks Classification

| Check | Category | Rationale |
|---|---|---|
| G1 (Wikilink integrity) | **M** | Slug set construction + pattern matching. |
| G2 (Index ↔ filesystem parity) | **M** | Set comparison between `index.md` entries and filesystem. |
| G3 (Source reference integrity) | **M** | Key Claims table parsing + source slug existence check. |
| G4 (Overview counter accuracy) | **M** | Numeric comparison: `total_pages` vs L2 count; `last_contradiction_id` vs max CTRD-NNN. |
| G5 (Status-content consistency) | **M** | Status value vs. content metrics (claims count, word count, field presence). |

All proposed checks are fully mechanical — they increase the script's scope without
adding any agent judgment load.

---

## 3. Script Scope

### 3.1 What `wiki-lint.py` Does

The script runs from the wiki repository root. It reads all wiki files (pages,
singletons, `raw/` files, `log.md`, skill files) and performs every M-category check
plus the mechanical portion of every D-category check. It produces a structured findings
file (`raw/lint-findings.json`) and exits.

Specifically:

1. **Reads** (single pass through the filesystem):
   - All pages in `topics/`, `tools/`, `comparisons/`, `pitfalls/`, `sources/`, `teaching/`
   - Singletons: `overview.md`, `index.md`, `log.md`, `wiki-lessons-learned.md`
   - Raw files: `raw/queue.md`, `raw/deferred-ingest.md` (if present), `raw/collection-gaps.md`
   - Skill files: `EXTRACTION-SKILL.md`, `TAGGING-SKILL.md`, `CONTRADICTION-SKILL.md`

2. **Computes** (all M-category outputs):
   - Support scores for every Key Claim (L3)
   - Staleness flags for Topic, Tool, Comparison, Teaching-brief pages (L5)
   - Contradiction expiry and open contradiction detection (L4a, L4b)
   - Counter reconciliation (L4c, G4)
   - Nomination queue aging (L1a)
   - CTRD-NNN signal cross-reference (L1)
   - Page inventory with index-filesystem parity (L2, G2)
   - Orphan detection (L6)
   - Wikilink integrity (G1)
   - Source reference integrity (G3)
   - Pitfalls maintenance counts (L8)
   - Teaching completeness ratio (L10)
   - Collection gap aggregation (L12)
   - Session stats count (L12a)
   - Deferred ingest staleness (L12b)
   - Schema Signals aging (L12d)
   - Skill file enrichment staleness (L14)
   - Teaching-tagged missing fields (L15)
   - Status-content consistency (G5)
   - Schema conformance — mechanical criteria (L11 partial)

3. **Assembles data for agent judgment** (D-category partial outputs):
   - L4b: open contradiction context (claim, source, scores, window) with `recommended: null`
   - L5 (Teaching-brief): stale brief context with `recommended: "A"` (agent overrides if needed)
   - L7: candidate concept gap terms with page references and counts (agent filters aliases)
   - L9: claims passing conditions (b)+(c) with full context (agent evaluates condition (a))
   - L11: candidate claim granularity violations (agent confirms/dismisses)
   - L12c: override entries within 30-day window with raw `What was wrong` text (agent categorizes)

4. **Does not do:**
   - Write any wiki file
   - Generate the decision form (L13 — the agent does this after setting recommendations)
   - Make any semantic classification
   - Modify the repository in any way (read-only, same as `wiki-verify.sh`)

### 3.2 What the Script Does Not Replace

The script replaces the data-gathering phase of lint, not the judgment or execution
phases. The agent retains sole responsibility for:

- Setting `recommended` values on forced choices where judgment is required
- Filtering concept gap candidates for aliases (L7)
- Classifying claims as definitional vs. empirical (L9 condition (a))
- Categorizing override patterns (L12c)
- Reviewing candidate claim granularity violations (L11)
- Generating the decision form (L13) after completing its judgment work
- All of Phase 2 (human interaction) and Phase 3 (execution pass)

### 3.3 Runtime and Dependencies

- **Python 3.x** (already required for `generate-teaching-index.py`)
- **No external packages required.** YAML frontmatter is delimited by `---` markers;
  the script parses it with a lightweight built-in parser (split on `---`, parse
  key-value pairs). This avoids adding PyYAML as a dependency and matches the
  zero-external-dependency pattern of `wiki-verify.sh`. Markdown table parsing uses
  regex on pipe-delimited rows. Date arithmetic uses `datetime` from the standard
  library.
- **Read-only.** The script writes only `raw/lint-findings.json`. It does not modify
  any wiki page, singleton, or configuration file.
- **Runtime:** seconds, not minutes. The script processes all files in a single pass
  with no network I/O. At 100 pages, expect sub-second completion; at 500 pages,
  expect single-digit seconds.

---

## 4. Findings File Format

The script outputs `raw/lint-findings.json`. This file is the sole interface between
the script and the agent. The agent reads it at session start and operates on its
contents instead of reading 100+ wiki pages.

### 4.1 Top-Level Schema

```json
{
  "lint_date": "YYYY-MM-DD",
  "script_version": "1.0.0",
  "wiki_stats": {
    "total_pages": 100,
    "pages_by_type": {
      "topic": 42,
      "tool": 28,
      "source": 55,
      "comparison": 8,
      "pitfalls": 6,
      "teaching-brief": 4
    },
    "pages_by_directory": {
      "topics": 42,
      "tools": 28,
      "sources": 55,
      "comparisons": 8,
      "pitfalls": 6,
      "teaching": 4
    },
    "overview_fields": {
      "total_pages": 100,
      "total_sources": 55,
      "open_contradictions": 3,
      "last_contradiction_id": 12,
      "last_lint": "2026-05-01"
    }
  },
  "findings": [ ...finding objects... ],
  "agent_review": [ ...items requiring agent judgment... ]
}
```

### 4.2 Finding Object Schema

Each finding in the `findings` array is a complete, script-resolved result:

```json
{
  "step": "L3",
  "type": "auto-execute | forced-choice | informational",
  "page": "topics/some-page",
  "description": "Support score changed: 4.5 → 3.0",
  "data": { ...step-specific structured data... },
  "recommended": "A" | null
}
```

- `step`: the lint step ID (L1, L1a, L2, ..., G1, G2, ...).
- `type`: the finding's classification per OPERATIONS.md.
- `page`: the affected page slug (null for cross-page or singleton findings).
- `description`: human-readable summary for the informational report.
- `data`: step-specific structured data (support score details, dates, counts, etc.).
- `recommended`: for forced-choice findings, the script's recommendation. Set to the
  deterministic value when one exists (L5a: always `"A"`), or `null` when judgment is
  required (the agent fills this in).

### 4.3 Agent Review Object Schema

Each item in the `agent_review` array requires the agent to complete a judgment step:

```json
{
  "step": "L9",
  "review_type": "definitional_classification",
  "page": "topics/some-page",
  "description": "Claim passes conditions (b)+(c) for decay_exempt. Agent must evaluate condition (a): is this claim definitional or empirical?",
  "claim_text": "Transformer attention scales quadratically with sequence length",
  "supporting_sources": [
    {"slug": "source-1", "tier": "peer-reviewed", "published": "2024-01-15"},
    {"slug": "source-2", "tier": "institutional", "published": "2023-08-20"}
  ],
  "context": { ...additional data the agent needs... }
}
```

Review types:
- `contradiction_recommendation` (L4b): agent sets recommended value
- `teaching_brief_recommendation` (L5): agent confirms or overrides default recommendation
- `concept_gap_filter` (L7): agent filters alias terms and sets stub type
- `definitional_classification` (L9): agent evaluates condition (a)
- `claim_granularity_review` (L11): agent confirms or dismisses candidate violations
- `override_categorization` (L12c): agent categorizes override entries

### 4.4 File Lifecycle

- Created by `wiki-lint.py` at lint start.
- Read by the agent at session start.
- Not committed to git. Added to `.gitignore` alongside `lint-decisions.html`.
- Deleted by Phase 3 cleanup (replaces the `raw/lint-state.md` deletion step from
  DM-105).

---

## 5. Agent Workflow in the Hybrid Model

### 5.1 Session Structure

A lint session in the hybrid model follows this sequence:

1. **Pre-session (human, outside Claude Code):**
   - Run `wiki-verify.sh` (pre-session habit, unchanged).
   - Run `python3 wiki-lint.py` from the wiki root. Takes seconds.
   - Start Claude Code session with the lint prompt.

2. **Agent session start:**
   - Read `CLAUDE.md` and `OPERATIONS.md` (unchanged — both required at session start).
   - Read `raw/lint-findings.json`.
   - Report script summary to human: total findings by type, any errors or warnings
     from the script.

3. **Agent judgment pass (replaces multi-session Phase 1 page reading):**
   - Process `agent_review` items:
     - **L4b** (open contradictions): read the pre-assembled context for each. Set
       `recommended` based on evidence quality assessment. This may require reading
       the specific wiki pages involved — but only the 0–5 pages with open
       contradictions, not all 100+ pages.
     - **L7** (concept gaps): review candidate terms. Filter aliases. For surviving
       candidates, set stub type (Topic or Tool). Requires checking `index.md` for
       existing pages (already in the findings file) and making a judgment about
       whether a term is a synonym.
     - **L9** (decay_exempt): for each candidate claim, evaluate whether it is
       definitional/foundational or empirical. Read the claim text and source context
       from the findings file. No page read required — all context is in the findings.
     - **L11** (claim granularity): review flagged candidates. Confirm or dismiss.
       Claim text is in the findings file.
     - **L12c** (override categorization): read the extracted override entry texts.
       Categorize into the five root cause bins. If any category reaches 3+, mark for
       Schema Signals entry in Phase 3.
   - Merge judgment results back into the findings: set `recommended` values, promote
     confirmed D-category items to findings, dismiss false positives.

4. **L13 — Generate decision form:**
   - Assemble the choices JSON from the merged findings (script findings +
     agent-completed judgments).
   - Serialize and inject into the HTML template (unchanged process).
   - Present to human.

5. **Phase 2 — Human response (unchanged).**

6. **Phase 3 — Execution pass (unchanged).** Apply auto-execute actions and confirmed
   forced choices. Delete `raw/lint-findings.json` at the end.

### 5.2 Context Window Impact

The critical improvement: the agent reads `raw/lint-findings.json` (estimated 5–20 KB
depending on finding count) instead of reading 100+ wiki pages (estimated 300–500 KB
of frontmatter and prose). The agent only reads specific wiki pages when a judgment step
requires it — and only the 0–10 pages implicated in judgment-requiring findings, not
the full corpus.

At 100 pages, this reduces the agent's Phase 1 context consumption by approximately
90–95%. At 200 pages, the reduction is even more dramatic because the script's runtime
is linear and sub-second regardless of scale, while the agent's per-page context cost
is constant.

### 5.3 Fallback for Context Pressure

If the agent's judgment pass plus Phase 3 execution still approach context limits
(unlikely at current scale, but possible if the wiki reaches 300+ pages with many
findings), the DM-105 state file mechanism can be adapted as a fallback: the agent
writes its judgment results to a file, commits, and the next session reads the file
and proceeds to L13. This is a contingency, not a design requirement — it exists only
to acknowledge that the DM-105 pattern has a residual role as an emergency valve.

The more likely scenario: at 300+ pages with many findings, the script's findings file
grows, but the agent's judgment work remains bounded by the number of D-category items
(which scales with the number of active contradictions, concept gaps, and override
patterns — not with total page count). The agent's context consumption in the hybrid
model scales with judgment-requiring items, not with wiki size. This is the fundamental
architectural improvement.

---

## 6. Maintenance Table

The script hardcodes schema knowledge. When the schema changes, the script must be
updated. This table defines the mapping — modeled on `test-harness.md` Section 2.5.

| Schema Change | Required Script Update |
|---|---|
| Credibility weight values changed (3/2/1/0) | Update `CREDIBILITY_WEIGHTS` constant |
| Decay multiplier changed (0.5×) | Update `DECAY_MULTIPLIER` constant |
| Decay threshold changed (12 months) | Update `DECAY_THRESHOLD_MONTHS` constant |
| Staleness threshold changed (90 days for Topic/Tool) | Update `STALENESS_THRESHOLD_DAYS` constant |
| Comparison staleness signal field changed (`last_assessed` → other) | Update comparison staleness logic |
| Nomination aging thresholds changed (90/180 days) | Update `NOMINATION_STAGE1_DAYS`, `NOMINATION_STAGE2_DAYS` constants |
| Teaching ratio threshold changed (0.20) | Update `TEACHING_RATIO_THRESHOLD` constant |
| Schema Signals aging threshold changed (60 days) | Update `SCHEMA_SIGNALS_AGE_DAYS` constant |
| Deferred ingest staleness threshold changed (14 days) | Update `DEFERRED_STALENESS_DAYS` constant |
| Session stats count threshold changed (50) | Update `SESSION_STATS_THRESHOLD` constant |
| New content directory added | Add to `CONTENT_DIRS` list |
| New page type with required frontmatter fields | Add field checks to per-page assessment |
| Required frontmatter field added to existing page type | Add to field-presence check for that type |
| Controlled vocabulary values changed (Sections 7.1–7.2) | Update `VALID_COMPETENCY_DOMAINS`, `VALID_PROFESSIONAL_CONTEXTS` arrays |
| Key Claims table column structure changed | Update markdown table parser |
| CTRD-NNN format changed | Update regex pattern |
| New singleton file with required fields | Add to singleton checks |
| New lint step (M-category) added | Implement check in script; add to findings output |
| New lint step (D-category) added | Implement data-assembly in script; add to `agent_review` output |
| override_window default changed (7 days) | Update `OVERRIDE_WINDOW_DAYS` constant |
| Status vocabulary changed | Update `VALID_STATUS` constant per page type |
| L12a inline analysis criteria changed | Update session stats aggregation logic |
| `wiki-verify.sh` vocabulary allowlists changed | Ensure `wiki-lint.py` uses the same allowlists (or shares a constants file) |

### 6.1 Maintenance Coupling Comparison

`wiki-verify.sh` (709 lines, bash): 12 rows in its Section 2.5 maintenance table.
`wiki-lint.py` (estimated 800–1000 lines, Python): 23 rows in the table above.

The script has roughly double the maintenance surface of `wiki-verify.sh`. This is
expected — the lint script does substantially more work (support score calculation,
cross-page reference following, date-based staleness logic, log aggregation) than the
verify script (structural presence checks, naming conventions, field existence).

The coupling is manageable because:
- Most rows are constant-value updates (change one number). These are the most common
  schema changes and the easiest to maintain.
- The script's constants can be grouped in a single `# --- Schema Constants ---`
  section at the top of the file, making them easy to find and update.
- The maintenance table serves the same purpose as `test-harness.md` Section 2.5 — it
  is a gate that the design session checks before delivering any schema change.

### 6.2 Shared Constants Opportunity

Several constants appear in both `wiki-verify.sh` and `wiki-lint.py` (controlled
vocabulary values, content directory list, allowed root files). A shared constants
file (e.g., `wiki-constants.json`) could eliminate duplication, but introduces a new
dependency and coupling point. The recommendation is to defer this until a maintenance
error caused by inconsistent constants between the two scripts actually occurs. Until
then, explicit duplication with a maintenance table row calling it out is simpler.

---

## 7. Build Cost Assessment

### 7.1 Complexity Estimate

| Component | Estimated Lines | Notes |
|---|---|---|
| Frontmatter parser | ~80 | Split on `---`, parse key-value pairs, handle lists. No PyYAML dependency. |
| Markdown table parser | ~60 | Regex on pipe-delimited rows. Handle Key Claims table specifically. |
| Page reader (orchestrator) | ~80 | Walk content dirs, read each page, dispatch to per-page checks. |
| Support score calculator (L3) | ~80 | Weight lookup, decay arithmetic, cross-page source resolution. |
| Staleness checks (L5, L5a, L5b, L5c) | ~70 | Date arithmetic, comparison staleness signal logic. |
| Contradiction checks (L1, L4a, L4b, L4c) | ~70 | CTRD pattern matching, window comparison, counter reconciliation. |
| Queue/nomination checks (L1a, L12b) | ~40 | Date parsing, aging thresholds. |
| Wikilink checks (L6, G1, G3) | ~60 | Slug set construction, pattern extraction, set difference. |
| Schema conformance — mechanical (L11 partial) | ~70 | Field presence, word count, vocabulary check, heading check. |
| Index parity (G2) | ~30 | Filesystem walk vs. index.md entry set. |
| Log.md reader + aggregation (L12, L12a) | ~60 | Parse log entries, aggregate by topic_tags + result_quality. |
| Override/signals extraction (L12c, L12d) | ~40 | Parse wiki-lessons-learned.md, extract entries within date window. |
| Teaching checks (L10, L15) | ~30 | Ratio calculation, field presence. |
| Skill file + misc checks (L14, L8, G4, G5) | ~50 | Pattern matching, counting, field comparison. |
| Concept gap term extraction (L7 mechanical portion) | ~50 | Tokenize prose, count term frequency, check against index.md. |
| Findings file writer (JSON) | ~40 | Serialize findings and agent_review items. |
| CLI + main entry point | ~30 | argparse, directory validation, error handling. |
| **Total** | **~940** | |

### 7.2 Comparison

| Script | Lines | Language | Maintenance rows | External deps |
|---|---|---|---|---|
| `wiki-verify.sh` | 709 | bash | 12 | None (POSIX tools) |
| `wiki-lint.py` (est.) | ~940 | Python 3 | 23 | None (stdlib only) |
| `generate-teaching-index.py` | ~150 (est.) | Python 3 | per DM-103 | None |

The lint script is ~30% larger than `wiki-verify.sh` but written in Python, which is
substantially more maintainable for this level of complexity. Bash with grep/awk
heuristics for YAML parsing (wiki-verify.sh's approach) would not scale to support
score calculation, cross-page reference resolution, or structured JSON output.

### 7.3 Build Effort

The script is a straightforward data-processing program with no external dependencies,
no network I/O, and no concurrency. A Claude Code session should be able to produce the
initial implementation in 1–2 sessions. Testing can use the existing wiki as a test
fixture — run the script, verify findings against known state.

### 7.4 Shared Utilities with `generate-teaching-index.py`

Both scripts read wiki pages and parse frontmatter. If `generate-teaching-index.py`
already has a frontmatter parser, the lint script could import it. If not, the lint
script's parser can be written as a standalone module importable by both scripts. This
is an implementation detail — note it for the Claude Code session but do not block
the design on it.

---

## 8. DM-105 Disposition

### 8.1 What DM-105 Introduced

- Persistent state file (`raw/lint-state.md`) for multi-session Phase 1
- Group A/B/C step classification
- 30-page hard ceiling with directory-aware batching
- State file lifecycle (created at lint start, deleted after Phase 3)
- Staleness guard (>7 days: warn; >14 days: recommend restart)
- Corruption guard
- Abandoned-pass detection

### 8.2 What Survives in the Hybrid Model

**Preserved conceptually:**
- **Group A/B/C classification.** The three-group model correctly identifies the
  dependency structure of lint steps (singleton reads → per-page assessment →
  cross-page analysis). The script's internal architecture will reflect this ordering
  even though it executes in a single pass. The classification remains useful for
  documentation and maintenance.
- **Staleness guard concept.** Applied to `raw/lint-findings.json` instead of
  `raw/lint-state.md`. If the findings file is more than 7 days old when the agent
  session starts, warn — the wiki may have changed since the script ran. If more
  than 14 days, recommend re-running the script. Same thresholds, different file.

**Superseded:**
- **State file protocol.** No longer needed — the script produces findings in seconds,
  not across multiple sessions.
- **30-page ceiling.** No longer needed — the script reads all pages in one pass
  outside the context window.
- **Directory-aware batching.** No longer needed — the script processes all directories
  in one run.
- **Multi-session resume logic.** No longer needed — there is no multi-session Phase 1.
- **Corruption guard and abandoned-pass detection.** No longer needed for the same
  reason.

### 8.3 Transition Path

DM-105 was committed to OPERATIONS.md and CLAUDE.md two days ago. The transition is:

1. Build `wiki-lint.py` (Claude Code session).
2. Run it against the live wiki and verify findings match expected state.
3. Update OPERATIONS.md: replace the chunked-session protocol with the hybrid model.
   Remove `raw/lint-state.md` references. Add `raw/lint-findings.json` lifecycle.
   Update Phase 1 to describe the script-then-agent sequence.
4. Update CLAUDE.md Section 2: remove `raw/lint-state.md` from the directory tree.
   Add `wiki-lint.py` to the allowed root files. Add `raw/lint-findings.json` (ephemeral,
   not committed).
5. Log DM-106 superseding DM-105.
6. The state file protocol from DM-105 has no residual operational role. It is
   preserved only as a design record in `decisions_made.md`.

---

## 9. Recommendation

**Build now.**

Reasoning:

1. **Operational tax is real and immediate.** At 100 pages, lint Phase 1 requires
   approximately 4 sessions under DM-105's 30-page ceiling. The wiki will only grow.
   At 200 pages, it requires 7+ sessions. The hybrid model completes Phase 1 data
   gathering in seconds and reduces the agent session to judgment work + Phase 3
   execution — reliably one session.

2. **Sunk cost is minimal.** DM-105 was committed two days ago. No multi-session lint
   pass has been executed under the new protocol. The state file format has never been
   generated in production. There is no operational habit to unlearn.

3. **The script provides durable infrastructure.** Unlike the state file protocol
   (which manages the symptom of context exhaustion), the script eliminates the cause
   (reading 100+ pages in the context window). It scales to 500+ pages without any
   further architectural changes.

4. **Maintenance coupling is manageable.** The 23-row maintenance table is larger than
   `wiki-verify.sh`'s 12 rows, but the same governance pattern (check the table before
   delivering schema changes) already works. No new process is needed.

5. **Build cost is low.** An estimated 940-line Python script with no external
   dependencies, buildable in 1–2 Claude Code sessions. The wiki itself serves as the
   test fixture.

6. **Agent judgment is preserved.** The 7 D-category steps retain meaningful agent
   contribution. The agent is not rubber-stamping script output — it is making the
   semantic assessments (definitional vs. empirical, alias recognition, evidence
   quality) that are the lint procedure's primary value-add over `wiki-verify.sh`.

7. **The fallback exists if needed.** If a future scenario arises where the agent's
   judgment pass plus Phase 3 exceeds context limits (300+ pages with many findings),
   a simplified version of DM-105's state file pattern can be adapted for the judgment
   results. This is a contingency, not a design requirement.

**What "build now" means in practice:**

- This design session produces the assessment (this document) and the DM entry.
- A subsequent Claude Code session builds the script, tests it against the live wiki,
  and updates OPERATIONS.md and CLAUDE.md.
- The OPERATIONS.md revision replaces the chunked-session protocol (DM-105) with the
  hybrid model. This is a net simplification of the document — the multi-session
  protocol is longer and more complex than the hybrid model's description.

---

## 10. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Script has a bug in support score calculation | Medium (first release) | Incorrect findings → wrong forced choices | Verify against manual calculation on 5+ pages before trusting. Add `--verbose` mode that shows per-claim calculation details. |
| Schema change made without updating script | Medium (ongoing) | Script produces stale or incorrect findings | Maintenance table is the gate. Add to project instructions cross-reference checks: "When CLAUDE.md changes touch [list], check wiki-lint.py maintenance table." |
| Frontmatter parser fails on edge cases | Low | Script crashes or produces wrong findings | The parser handles the subset of YAML the wiki uses (scalars, lists, dates). No need for full YAML spec compliance. Test against all existing pages. |
| Agent reads stale findings file | Low | Findings do not reflect current wiki state | Staleness guard (7-day warn, 14-day recommend restart) — carried forward from DM-105. The human runs the script immediately before starting the agent session. |
| Findings file grows very large (500+ pages, many findings) | Low (future) | Agent context consumption increases | The file grows linearly with findings, not with page count. Most pages produce zero findings. At 500 pages, expect 20–50 KB — well within context limits. |

---

## 11. Open Questions for Implementation Session

These are noted for the Claude Code session that builds the script, not for resolution
in this design session:

1. Can `generate-teaching-index.py`'s frontmatter parser be reused, or should the
   lint script have its own? Check the existing script's parser implementation.
2. Should the script have a `--check-only` mode that exits with a non-zero code if any
   forced-choice findings exist (useful for CI/pre-commit integration in the future)?
3. Should the script output a human-readable summary to stdout in addition to the JSON
   findings file (useful for the human to see results before starting the agent session)?
4. For L7 (concept gap term extraction), what tokenization approach produces the best
   candidate terms? Simple whitespace splitting will miss multi-word terms; n-gram
   extraction may produce too many candidates. Start simple (single words + known
   compound terms from index.md slugs) and iterate.

---

## Appendix A — Step-to-Script Mapping Quick Reference

For use during the Claude Code implementation session.

| Step | Script produces | Agent does |
|---|---|---|
| L1 | Complete CTRD signal list | Nothing |
| L1a | Complete aging list | Nothing |
| L2 + G2 | Page inventory + parity findings | Nothing |
| L3 | Complete support score recalculations | Nothing |
| L4a | Complete expiry list | Nothing |
| L4b | Open contradiction findings with `recommended: null` | Sets recommendations |
| L4c + G4 | Counter reconciliation findings | Nothing |
| L5 (Topic/Tool) | Complete staleness findings | Nothing |
| L5 (Comparison) | Complete staleness findings | Nothing |
| L5 (Teaching-brief) | Stale brief findings with `recommended: "A"` | Confirms or overrides |
| L5a | Complete upgrade candidates | Nothing |
| L5b | Complete currency check findings | Nothing |
| L5c | Complete Data Records freshness findings | Nothing |
| L6 | Complete orphan list | Nothing |
| L7 | Candidate terms with counts and page refs | Filters aliases, sets stub type |
| L8 | Complete Pitfalls maintenance findings | Nothing |
| L9 | Claims passing (b)+(c) with context | Evaluates condition (a) |
| L10 | Complete ratio finding | Nothing |
| L11 | Mechanical violations + candidate granularity flags | Reviews granularity candidates |
| L12 | Complete collection gap aggregation | Nothing |
| L12a | Complete session stats count | Nothing (if A selected, inline analysis is data aggregation — could be script or agent) |
| L12b | Complete deferred staleness finding | Nothing |
| L12c | Override entries with raw text | Categorizes entries |
| L12d | Complete Schema Signals age findings | Nothing |
| L14 | Complete skill enrichment staleness findings | Nothing |
| L15 | Complete missing-field findings | Nothing |
| L16 | Batch forced-choice with numbered-row candidate table (Tier 1); informational findings (Tier 2) | Sets recommended (C for first run, A for subsequent) |
| G1 | Complete broken wikilink list | Nothing |
| G3 | Complete broken source reference list | Nothing |
| G5 | Complete status-content inconsistencies | Nothing |
| L13 | — (agent generates form) | Assembles JSON, sets remaining recommendations, serializes, injects |
