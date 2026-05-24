# wiki-dashboard-build-spec.md — Implementation Specification
**Last Updated:** 05/24/2026 15:30 EST

**Document status:** Design project output. Implementation artifact for Claude Code.
**Authority:** This document governs the implementation of `wiki-dashboard.py` and
`wiki-dashboard.html`. CLAUDE.md governs schema; OPERATIONS.md governs operational
procedures. Any conflict between this document and CLAUDE.md/OPERATIONS.md on schema
or procedural questions is a defect in this document.
**See also:** DM-107, test-harness.md Section 2.5.2, ingest-ui-implementation-plan.md
(implementation pattern reference).

---

## 1. Overview

### What gets built

`wiki-dashboard.py` — a standalone Python script at the wiki root that reads all wiki
files and generates `wiki-dashboard.html`, a self-contained local HTML file for operator
use. The dashboard serves two modes:

- **Health mode:** What needs maintenance attention? Pages by type and status, stale
  pages, open contradictions, recent activity, decay trajectory.
- **Insight mode:** What does the wiki know and how well? Best-evidenced positions,
  contested claims, evidence base quality, coverage gaps, teaching coverage, recently
  learned content.

The generated HTML is opened from the local filesystem (`open wiki-dashboard.html` on
macOS). It has no server dependency, no external asset references, and no CDN calls.

### Files created or modified

| File | Action | Description |
|---|---|---|
| `wiki-dashboard.py` | Create (committed) | Standalone generator script; standard library only |
| `wiki-dashboard.html` | Generated on demand (gitignored) | Self-contained dashboard; all data embedded |
| `.gitignore` | Modify | Add `wiki-dashboard.html` |
| `OPERATIONS.md` | Already modified | Step 10a added to Phase 3 (see DM-107) |
| `test-harness.md` | Already modified | Section 2.5.2 added (see DM-107) |

### Environmental assumptions

| Assumption | Risk if violated |
|---|---|
| Python 3.6+ available | f-strings, pathlib; script fails with syntax errors |
| Standard library only | No pip install required; script portable to any Python 3.6+ env |
| Run from wiki repository root (directory containing `CLAUDE.md`) | Script aborts at entrypoint guard |
| `wiki-dashboard.html` opened locally in a browser (not served) | No File System Access API; data must be fully embedded |
| Obsidian vault name configured in `OBSIDIAN_VAULT_NAME` constant | Deep links broken silently if empty (script warns) |

---

## 2. Script: wiki-dashboard.py

### 2.1 File structure

```
wiki-dashboard.py
│
├── Module docstring (usage, exit codes, environmental assumptions)
├── # ── Configuration and Schema Constants ──────────────────────────
│   └── All schema-coupled constants (labeled with # MAINTENANCE: comments)
├── # ── Data parsing ────────────────────────────────────────────────
│   ├── parse_frontmatter(text) → (dict, str)   [reuse from generate-teaching-index.py]
│   ├── parse_key_claims(body) → list[dict]
│   ├── parse_log_entries(text, n) → list[dict]
│   ├── parse_overview(path) → dict
│   └── parse_lint_findings(path) → dict | None
├── # ── Data collection ─────────────────────────────────────────────
│   └── collect_all_pages() → dict  (all panel data assembled here)
├── # ── Panel computation ───────────────────────────────────────────
│   ├── compute_h1_type_status(pages) → dict
│   ├── compute_h2_stale(pages) → list
│   ├── compute_h3_contradictions(pages, overview) → list
│   ├── compute_h4_recent_activity(log_entries) → list
│   ├── compute_h5_decay_trajectory(pages) → dict
│   ├── compute_i1_best_evidenced(pages) → list
│   ├── compute_i2_contested(pages) → list
│   ├── compute_i3_evidence_quality(sources) → dict
│   ├── compute_i4_coverage_gaps(pages, lint_findings) → dict
│   ├── compute_i5_heatmap(pages) → dict
│   └── compute_i6_recently_learned(pages) → list
├── # ── HTML rendering ──────────────────────────────────────────────
│   └── render_dashboard(data) → str   (returns full HTML as string)
└── # ── Entry point ─────────────────────────────────────────────────
    └── main()
```

### 2.2 Configuration and schema constants block

```python
# ── Configuration and Schema Constants ────────────────────────────────────────
# MAINTENANCE: When schema changes, update the constants below.
# See test-harness.md Section 2.5.2 for the full maintenance table.

CONTENT_DIRS = ["topics", "tools", "comparisons", "pitfalls"]
SOURCE_DIR = "sources"
OUTPUT_FILE = "wiki-dashboard.html"

# MAINTENANCE: Set to your Obsidian vault name. Empty string disables deep links.
OBSIDIAN_VAULT_NAME = ""

LINT_FINDINGS_PATH = "raw/lint-findings.json"

# MAINTENANCE: Must match wiki-lint.py STALENESS_THRESHOLD_DAYS and OPERATIONS.md Step L5.
STALENESS_THRESHOLD_DAYS = 90

# MAINTENANCE: Must match wiki-lint.py DECAY_THRESHOLD_MONTHS and OPERATIONS.md credibility weights.
CREDIBILITY_WEIGHTS = {
    "peer-reviewed": 3,
    "institutional": 2,
    "practitioner": 1,
    "community": 0,
}

# MAINTENANCE: Update when CLAUDE.md Section 3 page type vocabulary changes.
CONTENT_PAGE_TYPES = {"topic", "tool", "comparison", "pitfalls", "teaching-brief"}

# MAINTENANCE: Update when status vocabulary changes in CLAUDE.md Sections 5.2–5.6.
STALE_STATUSES = {"stale"}
EXCLUDED_FROM_STALENESS = {"stub", "deprecated", "discontinued"}

# MAINTENANCE: Update when CLAUDE.md Sections 7.1–7.2 vocabulary changes.
# Must also update wiki-lint.py VALID_COMPETENCY_DOMAINS/VALID_PROFESSIONAL_CONTEXTS
# and wiki-verify.sh VALID_CD/VALID_PC in the same batch.
COMPETENCY_DOMAINS = [
    "tool-evaluation-and-selection",
    "practical-ai-use-and-interaction",
    "ai-integration-in-organizational-workflows",
    "output-verification-and-risk-assessment",
    "ai-safety-and-alignment-literacy",
    "capability-horizon-awareness",
    "attribution-ip-and-professional-integrity",
]

PROFESSIONAL_CONTEXTS = [
    "activism-and-civic-advocacy",
    "non-profit-and-ngo-work",
    "journalism-and-media",
    "legal-practice",
    "domestic-civil-service-and-public-administration",
    "foreign-service-and-diplomacy",
    "organizational-leadership-and-change-management",
    "project-and-program-management",
    "teaching-and-instruction",
    "graduate-and-doctoral-education",
    "professional-and-continuing-education",
    "entrepreneurship-and-startups",
    "software-and-ai-development",
]

DASHBOARD_STALENESS_WARNING_DAYS = 7
RECENT_ACTIVITY_COUNT = 20
RECENTLY_LEARNED_DAYS = 30
TOP_EVIDENCED_COUNT = 10
```

### 2.3 Entrypoint guard

```python
def main():
    if not os.path.exists("CLAUDE.md"):
        print(
            "ABORT: CLAUDE.md not found in current directory. "
            "Run from the wiki repository root.",
            file=sys.stderr,
        )
        sys.exit(1)

    if OBSIDIAN_VAULT_NAME == "":
        print(
            "WARNING: OBSIDIAN_VAULT_NAME is empty — Obsidian deep links will be "
            "disabled. Set this constant in wiki-dashboard.py to enable them.",
            file=sys.stderr,
        )
```

### 2.4 Frontmatter parser

Copy `parse_frontmatter()` verbatim from `generate-teaching-index.py`. Do not rewrite
it. Add a module-level comment: `# Reused from generate-teaching-index.py — keep in sync`.
The two implementations must remain identical. If one is updated for a parser edge case,
update the other in the same commit.

### 2.5 Key Claims parser

```python
def parse_key_claims(body: str) -> list[dict]:
    """
    Parse the ## Key Claims table from a page body.

    Returns a list of claim dicts:
        {
            "claim": str,
            "source": str,          # raw Source field value
            "date": str,
            "status": str,          # "current" | "superseded" | "contested"
            "ctrd_ids": list[str],  # e.g. ["CTRD-003", "CTRD-004"]
            "support_score": float | str,  # numeric or "derived"
            "decay_exempt": bool,
            "is_minority_view": bool,   # True if source contains [minority view]
            "is_derived": bool,         # True if source contains [derived]
        }

    Returns empty list if:
    - No "## Key Claims" section found
    - Table header row not found or not parseable
    - Any parse error (log WARNING to stderr; do not raise)

    Edge cases handled:
    - contested [CTRD-NNN]: extract "contested" as status, parse CTRD IDs
    - [derived] in source field: set is_derived=True, support_score="derived"
    - [minority view] in source field: set is_minority_view=True
    - Multi-source cells (comma-separated wikilinks): kept as raw string
    - Missing columns: skip the row with a WARNING

    Example:
        claims = parse_key_claims(body)
        # [{"claim": "GPT-4 achieves ...", "status": "current",
        #   "support_score": 4.5, "decay_exempt": False, ...}, ...]
    """
```

**Implementation notes:**
- Bound the Key Claims section: from `## Key Claims` to the next `##` heading (or EOF).
- Header row detection: match the pipe-delimited row containing "Claim", "Source",
  "Date", "Status", "Support Score", "Decay Exempt" as substrings (order matters;
  column count must be 6).
- Skip the separator row (`|---|---|...|`).
- For each data row: split on `|`; strip each cell; apply edge-case rules above.
- If the body contains `## Key Claims` but no valid table header is found: log
  `WARNING: {filepath} — Key Claims section found but table header not parseable` and
  return empty list. Do not raise.
- Status parsing: `raw_status = cell.strip()`. Extract CTRD IDs with regex
  `r'CTRD-\d+'`. If any IDs found, set status to "contested"; store IDs in `ctrd_ids`.
  Otherwise status is the raw cell value lowercased.
- Support score: strip whitespace; if "derived" → set `is_derived=True`,
  `support_score="derived"`; else attempt `float()`; if that fails, log WARNING and
  set `support_score=0.0`.

### 2.6 Log entry parser

```python
def parse_log_entries(text: str, n: int = 20) -> list[dict]:
    """
    Parse the most recent n log entries from log.md body.

    Matches entries with prefix: ## [YYYY-MM-DD] {operation} | {description}
    (CLAUDE.md Section 5.8 format)

    Returns list of dicts (newest first):
        {"date": "YYYY-MM-DD", "operation": str, "description": str}

    Returns empty list if no entries found (does not raise).

    Example:
        entries = parse_log_entries(open("log.md").read(), n=5)
        # [{"date": "2026-05-24", "operation": "ingest",
        #   "description": "Anthropic scaling laws post"}, ...]
    """
```

Match pattern: `r'^## \[(\d{4}-\d{2}-\d{2})\]\s+(\S+)\s*\|\s*(.+)$'` (multiline).
Return the most recent `n` matches sorted by date descending.

### 2.7 Panel computation specifications

**H1 — Pages by type and status:**
Count pages in CONTENT_DIRS by `type` and `status`. Return nested dict:
`{type: {status: count}}`. Exclude `raw/`, singletons, and skill files. Include a
`_total` key at the type level.

**H2 — Stale pages:**
All pages where `status` in `STALE_STATUSES`. For each: title, type, slug,
`last_assessed` (or None if absent), and `staleness_days` = today − `last_assessed`
(or "unknown"). Sort by `staleness_days` descending (unknown last).

**H3 — Open contradictions:**
All pages with ≥1 Key Claim where `status == "contested"`. For each matching claim:
page title, page slug, claim text (truncated to 120 chars), CTRD IDs. Also include
`overview_count` from `overview.md`. If the actual count of contested claims does not
match `overview.md`'s `open_contradictions`, add a warning flag to the panel data.

**H4 — Recent activity:**
Last `RECENT_ACTIVITY_COUNT` log entries from `log.md`, parsed by `parse_log_entries()`.
Display date, operation type (color-coded: ingest=blue, lint=purple, contradiction=amber,
query=teal, others=grey), and description.

**H5 — Decay trajectory:**
Pages not in `EXCLUDED_FROM_STALENESS` with `last_assessed` present. Compute
`days_until_stale = STALENESS_THRESHOLD_DAYS - (today - last_assessed).days`.
Exclude pages already stale (days_until_stale ≤ 0). Bucket:
- `≤30 days` — urgent (red)
- `31–60 days` — watch (amber)
- `61–90 days` — monitor (yellow)
Pages with `decay_exempt: true` on ALL Key Claims are excluded from this panel
(they do not go stale). Pages with no `last_assessed` are excluded (cannot compute).

**I1 — Best-evidenced positions:**
For each page in CONTENT_DIRS (excluding stub, deprecated, discontinued): compute
average support score across all numeric Key Claims (skip "derived" and 0.0 scores).
Require ≥2 numeric claims to qualify. Sort descending. Return top `TOP_EVIDENCED_COUNT`.
For each: title, slug, type, avg_score, claim_count, top claim text (highest individual
score; truncated to 100 chars), `last_assessed`.

Panel caveat string (hardcoded, displayed prominently under panel heading):
"Scores reflect source coverage within this wiki, not external validation. A
well-evidenced wrong claim ranks above a thinly-sourced correct one."

**I2 — Contested areas:**
All pages with ≥1 contested Key Claim. For each: page title, slug, contested claim
text (full, up to 200 chars), CTRD IDs, existing support score (from the claim row),
contesting source (from CTRD flag in frontmatter if parseable — optional, best-effort).

**I3 — Evidence base quality:**
Scan all source pages in `SOURCE_DIR`. Count by `credibility_tier`. Count
`vendor_bias` signals (source pages with `source_type: vendor-content`). Count by
`source_type`. Return: `{tier: count}`, `vendor_content_count`, `{source_type: count}`,
`total_sources`. Render as a horizontal bar chart (pure HTML/CSS, no JS library). Label:
"Sources contributing to wiki claims by credibility tier."

**I4 — Coverage gaps:**
Three sub-sources:
1. Pages with `status: stub` (from H1 data).
2. Pages with `source_count == 1` (thin coverage; parsed from frontmatter).
3. Collection gaps from `raw/lint-findings.json` if present and fresh — extract items
   of `type: "collection-gap"` from the findings array.
Return as three separate lists. If `lint-findings.json` is absent or stale, note
"Lint gap data unavailable — run wiki-lint.py to refresh."

**I5 — Teaching coverage and heatmap:**
Count pages with `teaching_relevance: true` (excluding stub, deprecated). Compute
ratio to total content pages (topics + tools + comparisons + pitfalls).

Heatmap data: `{(domain, context): count}` dict. A page with multiple domains and
contexts contributes to all matching cells (same logic as `generate-teaching-index.py`
`build_index()`). Cell value = page count. Zero cells rendered as white; max-count cell
rendered as deep blue; linear interpolation in between.

Layout: 13 rows (PROFESSIONAL_CONTEXTS) × 7 columns (COMPETENCY_DOMAINS). Column
headers: abbreviated labels (first 3 words max, truncated with "…" if needed). Row
headers: full context names. Minimum cell width: 40px; font-size: 11px.
Click handler: filter Layer 2 list to pages in that (domain, context) pair.

**I6 — Recently learned:**
Pages where `last_assessed` is within `RECENTLY_LEARNED_DAYS` days of today, OR where
`created` is within `RECENTLY_LEARNED_DAYS` days (new pages). Sort by date descending.
For each: title, slug, type, date, source contributing (from `related_topics`/
`related_tools` on the newest source page that references this page — best-effort,
omit if not resolvable without cross-referencing all sources). Credibility badge:
color-coded by the max credibility tier of sources in the page's Key Claims.

### 2.8 Data structure passed to renderer

```python
data = {
    "generated_date": "YYYY-MM-DD",
    "last_lint": "YYYY-MM-DD" | None,
    "total_pages": int,
    "total_sources": int,
    "obsidian_vault": str,          # empty = deep links disabled
    "dashboard_is_stale": bool,     # True if generated_date > DASHBOARD_STALENESS_WARNING_DAYS
    "pages": [                      # all content pages, all fields
        {
            "slug": str,
            "filepath": str,
            "title": str,
            "type": str,
            "status": str,
            "last_assessed": str | None,
            "source_count": int,
            "created": str,
            "updated": str,
            "summary": str,
            "teaching_relevance": bool,
            "competency_domains": list[str],
            "professional_contexts": list[str],
            "technical_depth": str,
            "key_claims": list[dict],   # from parse_key_claims()
            "avg_support_score": float | None,
            "has_contested_claims": bool,
            "days_until_stale": int | None,
        },
        ...
    ],
    "sources": [                    # all source page frontmatter
        {"slug": str, "credibility_tier": str, "source_type": str,
         "vendor_bias": bool, "ingested_date": str},
        ...
    ],
    "log_entries": list[dict],      # from parse_log_entries()
    "overview": dict,               # raw overview.md frontmatter
    "lint_findings": dict | None,   # None if absent or stale
    "panels": {
        "h1": dict, "h2": list, "h3": list, "h4": list, "h5": dict,
        "i1": list, "i2": list, "i3": dict, "i4": dict,
        "i5": {"ratio": float, "tagged_count": int, "heatmap": dict},
        "i6": list,
    }
}
```

---

## 3. HTML Output: wiki-dashboard.html

### 3.1 Structure

Single self-contained file. All CSS inline in `<style>`. All JS inline in `<script>`.
No external dependencies. No CDN calls. Data embedded as:

```html
<script>
const WIKI_DATA = {/* JSON-serialized data dict */};
</script>
```

File size at 100 pages: ~200–350 KB estimated. At 200 pages: ~400–700 KB. Both are
acceptable for a local file opened in a browser.

### 3.2 Status bar (always visible, top of page)

```
Generated: {date}  |  Last lint: {date or "never"}  |  {N} pages  |  {N} sources  |  Vault: {name or "deep links disabled"}
```

If `dashboard_is_stale`: status bar background `#f59e0b` (amber). Text: "Dashboard is
{N} days old — run `python3 wiki-dashboard.py` to refresh."

### 3.3 Regenerate button

Top-right of status bar. Label: "Regenerate ▾". Dropdown with two options:

| Label | Command copied to clipboard |
|---|---|
| Dashboard only | `python3 wiki-dashboard.py` |
| Lint + Dashboard | `python3 wiki-lint.py && python3 wiki-dashboard.py` |

On click: copy to clipboard using `navigator.clipboard.writeText()`. Show tooltip
"Copied — paste in terminal, then reload" for 2 seconds, then dismiss. If clipboard
API unavailable (non-HTTPS context without secure origin): show the command text in a
small modal for manual copy.

### 3.4 Navigation

Two top-level tabs: **Health** and **Insight**. Click switches the visible panel set.
Active tab underlined. Default: Health.

Within each tab: panel cards arranged in a two-column grid on wide viewports (≥1200px),
single-column below. Each panel card has: title, Layer 1 summary metric(s), and a "View
all →" link that expands to Layer 2.

### 3.5 Layer 1 summary cards

**Health tab:**
- H1: "{N} pages — {N} stale, {N} stub" with a mini horizontal bar chart (type breakdown)
- H2: "Stale: {N}" — click to expand
- H3: "Open contradictions: {N}" — click to expand; amber if N > 0
- H4: "Last activity: {N} days ago" — click to expand
- H5: "Approaching stale: {N≤30} urgent / {N31-60} watch / {N61-90} monitor"

**Insight tab:**
- I1: "Best-evidenced: {top title} (avg {score})" — click to see top 10
- I2: "Contested: {N} claim(s)" — click to expand; red if N > 0
- I3: "{N} sources — {top tier} dominant" — click for breakdown
- I4: "Gaps: {N} stubs, {N} thin pages" — click to expand
- I5: "Teaching: {N} pages tagged ({ratio}%)" — click for heatmap
- I6: "Recently learned: {N} pages in last {RECENTLY_LEARNED_DAYS} days"

### 3.6 Layer 2 panel tables

Standard table with sortable columns (JS sort, no library — implement manually).
Columns per panel:

| Panel | Columns |
|---|---|
| H2 | Title (link to Layer 3), Type, Status, Last Assessed, Stale for (days) |
| H3 | Page (link), Claim (truncated), CTRD IDs, Support Score |
| H4 | Date, Operation (colored badge), Description |
| H5 | Title (link), Type, Days Until Stale (colored), Last Assessed |
| I1 | Rank, Title (link), Type, Avg Score, Claims, Top Claim (truncated) |
| I2 | Page (link), Claim (truncated), CTRD IDs, Score |
| I3 | Tier, Count, % of total (bar visualization) |
| I4 | Category (stub/thin/gap), Title or Topic, Details |
| I5 | Heatmap view (see Section 3.7); table view tab showing tagged pages |
| I6 | Title (link), Type, Date, Credibility Badge |

### 3.7 Teaching heatmap (I5)

Pure HTML table. 14 rows (1 header + 13 context rows) × 8 columns (1 row-header +
7 domain columns). Each data cell:

```html
<td class="heatmap-cell" 
    data-count="{N}" 
    data-domain="{domain}" 
    data-context="{context}"
    style="background-color: {interpolated color}; cursor: pointer;"
    title="{N} pages: {domain} × {context}"
    onclick="filterLayer2('i5', '{domain}', '{context}')">
  {N}
</td>
```

Color interpolation: white (`#ffffff`) at count=0 → `#1d4ed8` (deep blue) at
max-count. Linear interpolation on RGB channels. Zero cells show no count text.

Column headers: abbreviated domain labels. Full label shown in `title` attribute
(hover tooltip). Abbreviations:

| Full | Abbrev |
|---|---|
| tool-evaluation-and-selection | Tool Eval |
| practical-ai-use-and-interaction | Practical AI |
| ai-integration-in-organizational-workflows | AI in Workflows |
| output-verification-and-risk-assessment | Output Verify |
| ai-safety-and-alignment-literacy | AI Safety |
| capability-horizon-awareness | Capability |
| attribution-ip-and-professional-integrity | Attribution |

Row headers: full context names, font-size 11px, max-width 180px, overflow ellipsis.

Below the heatmap: a toggle "Show page list" that opens a filterable table of all
teaching-tagged pages (same structure as the Layer 2 table). Click a heatmap cell
pre-filters this table to that (domain, context) pair.

### 3.8 Layer 3 page health card

Triggered by clicking any page title link in Layer 2 tables. Renders as a modal overlay
(or a side panel — implementer choice; modal is simpler).

Content:
```
[Type badge]  [Status badge]  {Title}
────────────────────────────────────────────────────────
Summary: {summary field}

Last assessed: {date or "never"}  |  Source count: {N}  |  Created: {date}
Technical depth: {value or "—"}

Key Claims
─────────────────────────────────────────────────────────
[Table: Claim | Source | Date | Status (colored) | Score | Decay Exempt]
  - current: green background
  - contested: amber background + CTRD badge
  - superseded: grey text

Teaching: {Yes / No}
  Domains: {list}
  Contexts: {list}

[Open in Obsidian →]   [Close]
```

Status badge colors:
- `current` / `active` / `emerging`: green
- `stale`: amber
- `stub`: grey
- `deprecated` / `discontinued`: dark grey
- `contested`: red

Obsidian deep link (if `OBSIDIAN_VAULT_NAME` is set):
`obsidian://open?vault={OBSIDIAN_VAULT_NAME}&file={filepath}`
where `filepath` is the relative path (e.g., `topics/prompt-injection.md`), URL-encoded.

### 3.9 JavaScript architecture

No framework, no external libraries. Vanilla JS only.

```javascript
// Data source (injected by wiki-dashboard.py)
const WIKI_DATA = { ... };

// On load: render all panels from WIKI_DATA
document.addEventListener('DOMContentLoaded', () => {
    renderStatusBar(WIKI_DATA);
    renderPanels(WIKI_DATA);
});

// State: current tab, current Layer 2 view, current Layer 3 page
let state = { tab: 'health', layer2Panel: null, layer2Filter: null, layer3Slug: null };

// Functions:
// switchTab(tab)
// expandPanel(panelId)
// filterLayer2(panelId, domain, context)
// showLayer3(slug)
// closeLayer3()
// sortTable(tableId, colIndex)
// copyToClipboard(text)
```

Keep all JS in a single `<script>` block. No module syntax. Keep functions short
(single-responsibility per the project coding standards). Total JS target: ≤500 lines.

---

## 4. Key Claims Parser Edge Case Reference

All edge cases must be handled without crashing. For each, the fallback behavior is
specified.

| Edge case | Example raw cell value | Required behavior |
|---|---|---|
| Contested with single CTRD | `contested [CTRD-003]` | status="contested", ctrd_ids=["CTRD-003"] |
| Contested with multiple CTRDs | `contested [CTRD-003] [CTRD-004]` | status="contested", ctrd_ids=["CTRD-003", "CTRD-004"] |
| Derived claim | `[[topic-slug]] [derived]` | is_derived=True, support_score="derived" |
| Minority view | `[[source-slug]] [minority view]` | is_minority_view=True; excluded from avg score |
| Multi-source | `[[src-a]], [[src-b]]` | source=raw string; score calculated externally |
| Support score "derived" literal | `derived` | support_score="derived"; is_derived=True |
| Support score non-numeric | `n/a` or empty | log WARNING; support_score=0.0 |
| Missing table entirely | (no `## Key Claims` in body) | return [] |
| Malformed header | columns not recognized | log WARNING; return [] |
| Extra whitespace in cells | `  current  ` | strip all cells before parsing |
| Backslash-dollar in claim text | `costs \$20` | preserve as-is; do not unescape |

---

## 5. Error Handling

Follow the project coding standard: fail fast for preconditions; degrade gracefully
for per-page errors.

| Situation | Behavior |
|---|---|
| CLAUDE.md not found | `print ABORT to stderr; sys.exit(1)` |
| A content directory does not exist | Skip with `WARNING: {dir}/ not found — skipping` |
| A page file cannot be read | `WARNING: cannot read {path}: {exc}` — skip the page |
| Frontmatter missing or malformed | Use empty dict; page still included in health panels with available fields |
| Key Claims table malformed | `WARNING: {path} — Key Claims parse error`; page included in all panels except Key Claims-dependent ones (I1, I2) |
| `overview.md` not found | `WARNING: overview.md not found — some panels will be incomplete`; continue |
| `log.md` not found | H4 and I6 panels show "Log not found" |
| `lint-findings.json` absent | I4 gap data unavailable — note in I4 panel |
| `lint-findings.json` stale (> 7 days) | Include data with staleness warning in I4 panel |
| Output file cannot be written | `print ABORT to stderr; sys.exit(1)` |
| Any per-panel computation error | Catch exception; mark panel as "Computation error — {exc}" in output; continue other panels |

---

## 6. Output file: wiki-dashboard.html

### 6.1 Serialization

The `data` dict is serialized to JSON for embedding in the HTML. Use `json.dumps(data)`
with `ensure_ascii=False`. The embedded block:

```html
<script>
const WIKI_DATA = JSON_OUTPUT_HERE;
</script>
```

Use Python to generate this:
```python
import json
json_str = json.dumps(data, ensure_ascii=False, default=str)
html = html_template.replace("%%WIKI_DATA%%", json_str)
```

`default=str` handles `datetime.date` objects and any other non-serializable types
gracefully.

### 6.2 Post-generation verification

After writing `wiki-dashboard.html`:
```python
# Verify the placeholder was replaced
with open(OUTPUT_FILE) as f:
    content = f.read()
if "%%WIKI_DATA%%" in content:
    print("ABORT: JSON injection failed — placeholder not replaced.", file=sys.stderr)
    sys.exit(1)
```

### 6.3 Usage note printed to stdout on success

```
Wiki dashboard written: wiki-dashboard.html
({N} pages, {N} sources, {N} stale, {N} contested)
Open with: open wiki-dashboard.html
```

---

## 7. .gitignore Entry

Add to `.gitignore`:
```
wiki-dashboard.html
```

Verify: `grep wiki-dashboard .gitignore` must return the line.

---

## 8. Implementation Notes

### 8.1 Date arithmetic

Use `datetime.date.today()` throughout. Parse `last_assessed`, `created`, `updated`,
`ingested_date` fields with:
```python
from datetime import date
def parse_date(s):
    try:
        return date.fromisoformat(s)
    except (ValueError, TypeError):
        return None
```
All date arithmetic produces `timedelta` objects; use `.days` for integer comparisons.

### 8.2 Support score averaging

For I1 (best-evidenced positions):
- Only include claims where `support_score` is numeric (not "derived", not 0.0 from
  an error).
- Exclude `is_minority_view=True` claims (consistent with how the wiki calculates
  support scores — minority views are not counted toward incumbent score).
- `decay_exempt=True` claims: include in average without decay (they have their
  canonical score).
- Minimum 2 numeric claims required to qualify a page for I1.

### 8.3 Obsidian deep-link construction

```python
import urllib.parse

def make_obsidian_link(vault_name: str, filepath: str) -> str | None:
    if not vault_name:
        return None
    encoded_vault = urllib.parse.quote(vault_name)
    encoded_file = urllib.parse.quote(filepath)
    return f"obsidian://open?vault={encoded_vault}&file={encoded_file}"
```

`filepath` is the path relative to the wiki root (e.g., `topics/prompt-injection.md`).

### 8.4 lint-findings.json staleness check

```python
import json
from datetime import date

def parse_lint_findings(path: str) -> dict | None:
    if not os.path.exists(path):
        return None
    try:
        with open(path) as f:
            data = json.load(f)
        lint_date = parse_date(data.get("lint_date", ""))
        if lint_date is None:
            return None
        age = (date.today() - lint_date).days
        data["_age_days"] = age
        data["_is_stale"] = age > DASHBOARD_STALENESS_WARNING_DAYS
        return data
    except (json.JSONDecodeError, OSError) as e:
        print(f"WARNING: cannot read {path}: {e}", file=sys.stderr)
        return None
```

### 8.5 Color interpolation for heatmap

```python
def interpolate_color(count: int, max_count: int) -> str:
    """
    Interpolate between white (count=0) and deep blue (count=max_count).
    Returns a CSS color string: "rgb(R, G, B)".
    """
    if max_count == 0 or count == 0:
        return "#ffffff"
    t = count / max_count  # 0.0 to 1.0
    # white: (255, 255, 255) → deep blue: (29, 78, 216)
    r = round(255 + t * (29 - 255))
    g = round(255 + t * (78 - 255))
    b = round(255 + t * (216 - 255))
    return f"rgb({r}, {g}, {b})"
```

---

## 9. Implementation Sequence (Claude Code session)

**Step 1 — Read this spec, CLAUDE.md Section 6.1, OPERATIONS.md Step L5, and
`generate-teaching-index.py` before writing any code.**

**Step 2 — Write and test parsing functions first.**
Implement `parse_frontmatter()` (copy from `generate-teaching-index.py`),
`parse_key_claims()`, `parse_log_entries()`, `parse_overview()`, and
`parse_lint_findings()`. Test each against real wiki files before proceeding.
One function, one test. Do not proceed to the next function until the current one passes.

**Step 3 — Implement panel computation.**
Implement all `compute_*()` functions. For each panel, test against real wiki data and
verify the output matches the spec. Pay particular attention to Key Claims edge cases
(Section 4).

**Step 4 — Implement HTML rendering.**
Build the HTML template with all structural elements (status bar, tabs, panel cards,
Layer 2 tables, Layer 3 modal, heatmap). Use placeholder data first; wire to `WIKI_DATA`
after the structure renders correctly.

**Step 5 — Integration and verification.**
Run the full script from the wiki root. Verify:
- `wiki-dashboard.html` is written without error
- `grep -c '%%WIKI_DATA%%' wiki-dashboard.html` returns 0
- `open wiki-dashboard.html` loads without JS console errors
- All panels render with real data
- Layer 2 drill-down works for at least H2 and I1
- Layer 3 modal opens for at least one page
- Heatmap cells render with correct counts
- Regenerate button copies to clipboard

**Step 6 — Update .gitignore.**
Append `wiki-dashboard.html`. Verify with `grep wiki-dashboard .gitignore`.

**Step 7 — Commit.**
```
feat: add wiki-dashboard.py (dual-mode operator dashboard)
```
Include: `wiki-dashboard.py`, `.gitignore`.
Do not commit `wiki-dashboard.html`.

**Step 8 — Report to human.**
Confirm completion and provide:
- Where `wiki-dashboard.py` lives and how to run it
- How to set `OBSIDIAN_VAULT_NAME` for deep links
- How the Phase 3 optional step works
- That `wiki-dashboard.html` is gitignored and opened locally

---

## 10. Maintenance Notes

**When CLAUDE.md Sections 7.1 or 7.2 (controlled vocabulary) change:**
Update `COMPETENCY_DOMAINS` and `PROFESSIONAL_CONTEXTS` lists in `wiki-dashboard.py`.
Also update `wiki-verify.sh` `VALID_CD`/`VALID_PC` and `wiki-lint.py`
`VALID_COMPETENCY_DOMAINS`/`VALID_PROFESSIONAL_CONTEXTS`. Three-script sync required.
See test-harness.md Section 2.5.2.

**When `STALENESS_THRESHOLD_DAYS` changes:**
Update in `wiki-dashboard.py` AND `wiki-lint.py`. Both must use the same value.

**When a new page type is added to CLAUDE.md Section 3:**
Update `CONTENT_PAGE_TYPES` set. Update H1 panel grouping. Assess whether the new
type has a staleness signal that differs from the default — if so, update
`compute_h2_stale()` and H5 accordingly.

**When Key Claims column structure changes (CLAUDE.md Section 6.1):**
Update `parse_key_claims()`. The parser is the single point of Key Claims data
ingestion — all panels that use Key Claims data depend on it.

**When `generate-teaching-index.py` `parse_frontmatter()` is updated:**
Copy the updated function to `wiki-dashboard.py`. The two implementations must remain
identical. Add a commit note.
