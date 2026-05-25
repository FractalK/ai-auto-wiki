#!/usr/bin/env python3
"""
wiki-dashboard.py — generate wiki-dashboard.html from wiki state.

Run from the wiki repository root (the directory containing CLAUDE.md).

Usage:
    python3 wiki-dashboard.py

Exit codes:
    0 — dashboard written successfully (WARNING lines may have been emitted to stderr)
    1 — fatal error (CLAUDE.md not found, output file cannot be written)

WARNING lines (stderr) indicate per-page parse failures or missing optional files.
Those pages/panels are excluded or degraded but do not cause a non-zero exit.

ABORT lines (stderr) indicate a fatal condition; exit code is 1.

Environmental assumptions:
    - Python 3.6+ (f-strings, pathlib, datetime.date.fromisoformat)
    - Standard library only — no external packages
    - Executed from the wiki repository root (directory containing CLAUDE.md)
    - wiki-dashboard.html opened locally in a browser (data fully embedded; no server required)
    - Set OBSIDIAN_VAULT_NAME constant below to enable Obsidian deep links
"""

import json
import os
import re
import sys
import urllib.parse
from collections import defaultdict
from datetime import date

# Reused from generate-teaching-index.py — keep in sync

# ── Configuration and Schema Constants ────────────────────────────────────────
# MAINTENANCE: When schema changes, update the constants below.
# See test-harness.md Section 2.5.2 for the full maintenance table.

CONTENT_DIRS = ["topics", "tools", "comparisons", "pitfalls"]
SOURCE_DIR = "sources"
OUTPUT_FILE = "wiki-dashboard.html"

# MAINTENANCE: Set to your Obsidian vault name. Empty string disables deep links.
OBSIDIAN_VAULT_NAME = "ai-auto-wiki"

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

# Credibility tier ordering for max-tier computation (higher index = better)
CREDIBILITY_TIER_ORDER = ["community", "practitioner", "institutional", "peer-reviewed"]


# ── Data parsing ──────────────────────────────────────────────────────────────

def parse_frontmatter(text):
    """
    Parse YAML frontmatter from a markdown file.

    Returns (frontmatter_dict, body_text).

    Handles: scalar string values, boolean true/false, and block-list values
    (YAML sequences using the '  - item' format). Flow sequences on a single
    line (e.g. competency_domains: [a, b]) are not supported — wiki frontmatter
    uses block-list format exclusively.

    Example:
        fm, body = parse_frontmatter(open("topics/foo.md").read())
        fm["teaching_relevance"]   # True
        fm["competency_domains"]   # ["tool-evaluation-and-selection"]
    """
    if not text.startswith("---"):
        return {}, text

    end = text.find("\n---", 3)
    if end == -1:
        return {}, text

    fm_text = text[4:end]
    body = text[end + 4:].lstrip("\n")

    fm = {}
    lines = fm_text.split("\n")
    current_key = None
    current_list = None  # non-None only while parsing a block-list value

    for line in lines:
        # Block-list item: two-space indent or leading dash
        if re.match(r'^[ \t]+-[ \t]', line):
            if current_key is not None and current_list is not None:
                val = re.sub(r'^[ \t]+-[ \t]', '', line).strip().strip('"')
                current_list.append(val)
            continue

        # Key: value
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)', line)
        if m:
            current_key = m.group(1)
            raw_val = m.group(2).strip().strip('"')

            if raw_val == "":
                # Empty value — likely the start of a block list
                current_list = []
                fm[current_key] = current_list
            elif raw_val == "true":
                fm[current_key] = True
                current_list = None
            elif raw_val == "false":
                fm[current_key] = False
                current_list = None
            else:
                fm[current_key] = raw_val
                current_list = None
        else:
            # Non-matching line (blank line, comment, etc.) — reset list context
            # only if the line is clearly not a continuation
            if line.strip() and not line.startswith(" "):
                current_list = None

    return fm, body


def parse_date(s):
    """Parse an ISO 8601 date string. Returns date or None on failure."""
    try:
        return date.fromisoformat(str(s))
    except (ValueError, TypeError):
        return None


def parse_key_claims(body, filepath=""):
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
            "is_minority_view": bool,
            "is_derived": bool,
        }

    Returns empty list if:
    - No "## Key Claims" section found
    - Table header row not found or not parseable
    - Any parse error (logs WARNING to stderr; does not raise)

    Edge cases handled (CLAUDE.md Section 6.1 and spec Section 4):
    - contested [CTRD-NNN]: extract "contested" as status, parse CTRD IDs
    - contested [CTRD-NNN] [CTRD-NNN+1]: multiple IDs in one cell
    - [derived] in source field: set is_derived=True, support_score="derived"
    - [minority view] in source field: set is_minority_view=True
    - Multi-source cells (comma-separated wikilinks): kept as raw string
    - Support score "derived" literal: support_score="derived", is_derived=True
    - Support score non-numeric (n/a, empty): log WARNING; support_score=0.0
    - Missing table entirely: return []
    - Malformed header (columns not recognized): log WARNING; return []
    - Missing columns in data row: log WARNING; skip the row
    - Extra whitespace in cells: strip all cells before parsing
    - Backslash-dollar in claim text (costs \\$20): preserved as-is

    Example:
        claims = parse_key_claims(body)
        # [{"claim": "GPT-4 achieves ...", "status": "current",
        #   "support_score": 2.0, "decay_exempt": False, ...}, ...]
    """
    if "## Key Claims" not in body:
        return []

    kc_start = body.find("## Key Claims")
    kc_section = body[kc_start:]

    # Bound to next ## heading
    next_h2 = re.search(r'\n## ', kc_section[len("## Key Claims"):])
    if next_h2:
        cutoff = len("## Key Claims") + next_h2.start()
        kc_section = kc_section[:cutoff]

    lines = kc_section.split('\n')

    # Find header row: must contain all six expected column names
    required_cols = ["Claim", "Source", "Date", "Status", "Support Score", "Decay Exempt"]
    header_idx = None
    for i, line in enumerate(lines):
        if all(col in line for col in required_cols):
            header_idx = i
            break

    if header_idx is None:
        label = f"{filepath} — " if filepath else ""
        print(
            f"WARNING: {label}Key Claims section found but table header not parseable",
            file=sys.stderr,
        )
        return []

    claims = []
    # Skip header row and separator row
    for line in lines[header_idx + 2:]:
        line_stripped = line.strip()
        if not line_stripped.startswith('|'):
            continue
        # Skip separator rows like |---|---|...|
        if re.match(r'^\|[-|: ]+\|$', line_stripped):
            continue

        parts = line_stripped.split('|')
        # Strip leading/trailing empty strings from pipe-delimited row
        if len(parts) >= 2:
            cells = [p.strip() for p in parts[1:-1]]
        else:
            continue

        if len(cells) < 6:
            label = f"{filepath} — " if filepath else ""
            print(
                f"WARNING: {label}Key Claims row has {len(cells)} column(s) (expected 6); skipping row",
                file=sys.stderr,
            )
            continue

        claim_text = cells[0]
        source_raw = cells[1]
        date_str = cells[2]
        status_raw = cells[3]
        score_raw = cells[4]
        decay_raw = cells[5]

        # Status: extract CTRD IDs
        ctrd_ids = re.findall(r'CTRD-\d+', status_raw)
        if ctrd_ids:
            status = "contested"
        else:
            status = status_raw.lower().strip()

        # Source: check for [derived] and [minority view]
        is_derived = "[derived]" in source_raw
        is_minority_view = "[minority view]" in source_raw

        # Support score
        score_lower = score_raw.lower().strip()
        if is_derived or score_lower == "derived":
            support_score = "derived"
            is_derived = True
        elif score_raw == "":
            support_score = 0.0
        else:
            try:
                support_score = float(score_raw)
            except (ValueError, TypeError):
                label = f"{filepath} — " if filepath else ""
                print(
                    f"WARNING: {label}non-numeric support score '{score_raw}'; using 0.0",
                    file=sys.stderr,
                )
                support_score = 0.0

        # Decay exempt
        decay_exempt = decay_raw.lower().strip() == "true"

        claims.append({
            "claim": claim_text,
            "source": source_raw,
            "date": date_str,
            "status": status,
            "ctrd_ids": ctrd_ids,
            "support_score": support_score,
            "decay_exempt": decay_exempt,
            "is_minority_view": is_minority_view,
            "is_derived": is_derived,
        })

    return claims


def parse_log_entries(text, n=20):
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
    pattern = re.compile(
        r'^## \[(\d{4}-\d{2}-\d{2})\]\s+(\S+)\s*\|\s*(.+)$',
        re.MULTILINE,
    )
    matches = pattern.findall(text)
    # matches is list of (date, operation, description)
    entries = [
        {"date": m[0], "operation": m[1], "description": m[2].strip()}
        for m in matches
    ]
    # Sort newest first
    entries.sort(key=lambda e: e["date"], reverse=True)
    return entries[:n]


def parse_overview(path):
    """
    Read overview.md frontmatter. Returns dict. Returns empty dict if file absent.

    Example:
        overview = parse_overview("overview.md")
        overview["total_pages"]    # "102"
        overview["open_contradictions"]  # "0"
    """
    if not os.path.exists(path):
        print(
            f"WARNING: {path} not found — some panels will be incomplete",
            file=sys.stderr,
        )
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        fm, _ = parse_frontmatter(text)
        return fm
    except OSError as exc:
        print(f"WARNING: cannot read {path}: {exc}", file=sys.stderr)
        return {}


def parse_lint_findings(path):
    """
    Read and validate lint-findings.json. Returns dict with added _age_days and
    _is_stale keys, or None if absent/unreadable/no valid lint_date.

    Staleness threshold: DASHBOARD_STALENESS_WARNING_DAYS.

    Example:
        findings = parse_lint_findings("raw/lint-findings.json")
        findings["_age_days"]    # 2
        findings["_is_stale"]    # False
    """
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        lint_date = parse_date(data.get("lint_date", ""))
        if lint_date is None:
            return None
        age = (date.today() - lint_date).days
        data["_age_days"] = age
        data["_is_stale"] = age > DASHBOARD_STALENESS_WARNING_DAYS
        return data
    except (json.JSONDecodeError, OSError) as exc:
        print(f"WARNING: cannot read {path}: {exc}", file=sys.stderr)
        return None


# ── Data collection ───────────────────────────────────────────────────────────

def _coerce_list(val):
    """Coerce a frontmatter value to a list of strings."""
    if isinstance(val, list):
        return val
    if isinstance(val, str) and val:
        return [val]
    return []


def _extract_source_slugs(source_raw):
    """
    Extract source slugs from a raw Key Claims source field.
    Handles single and multi-source fields, short-form and full-path wikilinks.
    Returns list of slug strings (filename stem only, no directory prefix).
    """
    slugs = []
    for match in re.finditer(r'\[\[([^\]|]+)', source_raw):
        slug = match.group(1).strip()
        # Strip directory prefix (e.g. "sources/2024-slug" → "2024-slug")
        slug = slug.split('/')[-1]
        if slug:
            slugs.append(slug)
    return slugs


def collect_all_pages():
    """
    Walk CONTENT_DIRS and SOURCE_DIR to collect all page data.

    Returns a dict:
        {
            "pages": list[dict],    # content pages with computed fields
            "sources": list[dict],  # source page metadata
        }

    Per-page errors are logged as WARNINGs and the page is skipped.

    Example:
        raw = collect_all_pages()
        raw["pages"][0]["avg_support_score"]   # 2.5
        raw["sources"][0]["credibility_tier"]  # "practitioner"
    """
    today = date.today()
    pages = []
    sources = []

    # ── Pass 1: collect source pages ─────────────────────────────────────────
    if not os.path.isdir(SOURCE_DIR):
        print(f"WARNING: {SOURCE_DIR}/ not found — skipping", file=sys.stderr)
    else:
        for fname in sorted(os.listdir(SOURCE_DIR)):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(SOURCE_DIR, fname)
            try:
                with open(fpath, encoding="utf-8") as f:
                    text = f.read()
            except OSError as exc:
                print(f"WARNING: cannot read {fpath}: {exc}", file=sys.stderr)
                continue
            fm, _ = parse_frontmatter(text)
            slug = fname[:-3]
            sources.append({
                "slug": slug,
                "credibility_tier": fm.get("credibility_tier", ""),
                "source_type": fm.get("source_type", ""),
                "vendor_bias": fm.get("source_type", "") == "vendor-content",
                "ingested_date": fm.get("ingested_date", ""),
            })

    # Build slug → credibility_tier lookup for Key Claims cross-reference
    source_tier_map = {s["slug"]: s["credibility_tier"] for s in sources}

    # ── Pass 2: collect content pages ────────────────────────────────────────
    for directory in CONTENT_DIRS:
        if not os.path.isdir(directory):
            print(f"WARNING: {directory}/ not found — skipping", file=sys.stderr)
            continue

        for fname in sorted(os.listdir(directory)):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(directory, fname)
            try:
                with open(fpath, encoding="utf-8") as f:
                    text = f.read()
            except OSError as exc:
                print(f"WARNING: cannot read {fpath}: {exc}", file=sys.stderr)
                continue

            fm, body = parse_frontmatter(text)

            slug = fname[:-3]
            title = fm.get("title", slug.replace("-", " ").title())
            page_type = fm.get("type", "")
            status = fm.get("status", "")
            last_assessed_raw = fm.get("last_assessed", None)
            last_assessed = last_assessed_raw if last_assessed_raw else None

            try:
                source_count = int(fm.get("source_count", 0))
            except (ValueError, TypeError):
                source_count = 0

            competency_domains = _coerce_list(fm.get("competency_domains", []))
            professional_contexts = _coerce_list(fm.get("professional_contexts", []))

            # Parse Key Claims
            try:
                key_claims = parse_key_claims(body, filepath=fpath)
            except Exception as exc:
                print(f"WARNING: {fpath} — Key Claims parse error: {exc}", file=sys.stderr)
                key_claims = []

            # Compute avg_support_score (numeric, non-derived, non-minority-view)
            numeric_scores = [
                c["support_score"] for c in key_claims
                if isinstance(c["support_score"], (int, float))
                and not c["is_minority_view"]
            ]
            avg_support_score = (
                sum(numeric_scores) / len(numeric_scores) if numeric_scores else None
            )

            has_contested_claims = any(c["status"] == "contested" for c in key_claims)

            # Compute days_until_stale
            days_until_stale = None
            if status not in EXCLUDED_FROM_STALENESS and last_assessed:
                d = parse_date(last_assessed)
                if d is not None:
                    days_since = (today - d).days
                    days_until_stale = STALENESS_THRESHOLD_DAYS - days_since

            # Max credibility tier from Key Claims sources (for I6 badge)
            max_tier = ""
            for claim in key_claims:
                if claim["is_minority_view"] or claim["is_derived"]:
                    continue
                for slug_ref in _extract_source_slugs(claim["source"]):
                    tier = source_tier_map.get(slug_ref, "")
                    if tier in CREDIBILITY_TIER_ORDER:
                        if not max_tier or CREDIBILITY_TIER_ORDER.index(tier) > CREDIBILITY_TIER_ORDER.index(max_tier):
                            max_tier = tier

            pages.append({
                "slug": slug,
                "filepath": fpath,
                "title": title,
                "type": page_type,
                "status": status,
                "last_assessed": last_assessed,
                "source_count": source_count,
                "created": fm.get("created", ""),
                "updated": fm.get("updated", ""),
                "summary": fm.get("summary", ""),
                "teaching_relevance": fm.get("teaching_relevance", False) is True,
                "competency_domains": competency_domains,
                "professional_contexts": professional_contexts,
                "technical_depth": fm.get("technical_depth", ""),
                "key_claims": key_claims,
                "avg_support_score": avg_support_score,
                "has_contested_claims": has_contested_claims,
                "days_until_stale": days_until_stale,
                "max_credibility_tier": max_tier,
            })

    return {"pages": pages, "sources": sources}


# ── Panel computation ─────────────────────────────────────────────────────────

def compute_h1_type_status(pages):
    """
    H1 — Pages by type and status.
    Returns {type: {status: count, "_total": count}}.

    Example:
        h1 = compute_h1_type_status(pages)
        h1["topic"]["current"]   # 12
        h1["topic"]["_total"]    # 20
    """
    counts = defaultdict(lambda: defaultdict(int))
    for page in pages:
        t = page["type"] or "unknown"
        s = page["status"] or "unknown"
        counts[t][s] += 1
        counts[t]["_total"] += 1
    return {t: dict(v) for t, v in counts.items()}


def compute_h2_stale(pages):
    """
    H2 — Stale pages.
    Returns list sorted by staleness_days descending (unknown last).

    Example:
        h2 = compute_h2_stale(pages)
        h2[0]["staleness_days"]   # 120
    """
    today = date.today()
    stale = []
    for page in pages:
        if page["status"] not in STALE_STATUSES:
            continue
        last_assessed = page["last_assessed"]
        if last_assessed:
            d = parse_date(last_assessed)
            staleness_days = (today - d).days if d else None
        else:
            staleness_days = None

        stale.append({
            "slug": page["slug"],
            "filepath": page["filepath"],
            "title": page["title"],
            "type": page["type"],
            "status": page["status"],
            "last_assessed": last_assessed,
            "staleness_days": staleness_days,
        })

    # Sort: known days descending, unknowns at end
    stale.sort(key=lambda x: (x["staleness_days"] is None, -(x["staleness_days"] or 0)))
    return stale


def compute_h3_contradictions(pages, overview):
    """
    H3 — Open contradictions.
    Returns list of contested claim dicts plus overview_count and mismatch_warning.

    Example:
        h3 = compute_h3_contradictions(pages, overview)
        h3[0]["claim"][:40]   # "Model X achieves state-of-the-art on..."
    """
    contested_items = []
    all_ctrd_ids = set()

    for page in pages:
        for claim in page.get("key_claims", []):
            if claim["status"] != "contested":
                continue
            for cid in claim["ctrd_ids"]:
                all_ctrd_ids.add(cid)
            contested_items.append({
                "page_title": page["title"],
                "page_slug": page["slug"],
                "filepath": page["filepath"],
                "claim": claim["claim"][:120],
                "ctrd_ids": claim["ctrd_ids"],
                "support_score": claim["support_score"],
            })

    try:
        overview_count = int(overview.get("open_contradictions", 0))
    except (ValueError, TypeError):
        overview_count = 0

    actual_count = len(all_ctrd_ids)
    mismatch_warning = (actual_count != overview_count) and overview_count != 0

    # Attach summary fields (not in list items)
    return {
        "items": contested_items,
        "overview_count": overview_count,
        "actual_ctrd_count": actual_count,
        "mismatch_warning": mismatch_warning,
    }


def compute_h4_recent_activity(log_entries):
    """
    H4 — Recent activity.
    Returns the last RECENT_ACTIVITY_COUNT log entries (already sorted newest first).

    Example:
        h4 = compute_h4_recent_activity(entries)
        h4[0]["operation"]   # "ingest"
    """
    return log_entries[:RECENT_ACTIVITY_COUNT]


def compute_h5_decay_trajectory(pages):
    """
    H5 — Decay trajectory.
    Returns buckets: urgent (≤30 days), watch (31–60), monitor (61–90).

    Excludes: EXCLUDED_FROM_STALENESS statuses, missing last_assessed,
    already stale (days_until_stale ≤ 0), all-decay-exempt pages.

    Example:
        h5 = compute_h5_decay_trajectory(pages)
        len(h5["urgent"])   # 3
    """
    urgent = []
    watch = []
    monitor = []

    for page in pages:
        if page["status"] in EXCLUDED_FROM_STALENESS:
            continue
        if not page["last_assessed"]:
            continue
        days_until = page["days_until_stale"]
        if days_until is None or days_until <= 0:
            continue

        # Skip pages where ALL key claims are decay-exempt
        key_claims = page.get("key_claims", [])
        if key_claims and all(c["decay_exempt"] for c in key_claims):
            continue

        entry = {
            "slug": page["slug"],
            "filepath": page["filepath"],
            "title": page["title"],
            "type": page["type"],
            "last_assessed": page["last_assessed"],
            "days_until_stale": days_until,
        }

        if days_until <= 30:
            urgent.append(entry)
        elif days_until <= 60:
            watch.append(entry)
        elif days_until <= 90:
            monitor.append(entry)

    # Sort each bucket by days_until_stale ascending (most urgent first)
    for bucket in (urgent, watch, monitor):
        bucket.sort(key=lambda x: x["days_until_stale"])

    return {"urgent": urgent, "watch": watch, "monitor": monitor}


def compute_i1_best_evidenced(pages):
    """
    I1 — Best-evidenced positions.
    Top TOP_EVIDENCED_COUNT pages by average support score (≥2 qualifying claims).

    Qualifying claims: numeric score > 0, not derived, not minority view.

    Caveat (must be displayed prominently in UI):
    "Scores reflect source coverage within this wiki, not external validation.
    A well-evidenced wrong claim ranks above a thinly-sourced correct one."

    Example:
        i1 = compute_i1_best_evidenced(pages)
        i1[0]["avg_score"]   # 2.5
    """
    candidates = []

    for page in pages:
        if page["status"] in {"stub", "deprecated", "discontinued"}:
            continue

        qualifying = [
            c for c in page.get("key_claims", [])
            if isinstance(c["support_score"], (int, float))
            and c["support_score"] > 0
            and not c["is_minority_view"]
            and not c["is_derived"]
        ]

        if len(qualifying) < 2:
            continue

        avg_score = sum(c["support_score"] for c in qualifying) / len(qualifying)

        # Top claim = highest individual score (first on tie)
        top_claim = max(qualifying, key=lambda c: c["support_score"])

        candidates.append({
            "slug": page["slug"],
            "filepath": page["filepath"],
            "title": page["title"],
            "type": page["type"],
            "avg_score": round(avg_score, 2),
            "claim_count": len(qualifying),
            "top_claim": top_claim["claim"][:100],
            "last_assessed": page["last_assessed"],
        })

    candidates.sort(key=lambda x: x["avg_score"], reverse=True)
    return candidates[:TOP_EVIDENCED_COUNT]


def compute_i2_contested(pages):
    """
    I2 — Contested areas.
    All pages with ≥1 contested Key Claim.

    Example:
        i2 = compute_i2_contested(pages)
        i2[0]["ctrd_ids"]   # ["CTRD-003"]
    """
    items = []
    for page in pages:
        for claim in page.get("key_claims", []):
            if claim["status"] != "contested":
                continue
            items.append({
                "page_title": page["title"],
                "page_slug": page["slug"],
                "filepath": page["filepath"],
                "claim": claim["claim"][:200],
                "ctrd_ids": claim["ctrd_ids"],
                "support_score": claim["support_score"],
            })
    return items


def compute_i3_evidence_quality(sources):
    """
    I3 — Evidence base quality.
    Returns tier counts, source type counts, vendor content count, total.

    Example:
        i3 = compute_i3_evidence_quality(sources)
        i3["tier_counts"]["practitioner"]   # 18
        i3["total_sources"]                 # 35
    """
    tier_counts = defaultdict(int)
    type_counts = defaultdict(int)
    vendor_content_count = 0

    for src in sources:
        tier = src.get("credibility_tier", "") or "unknown"
        tier_counts[tier] += 1

        stype = src.get("source_type", "") or "unknown"
        type_counts[stype] += 1

        if src.get("vendor_bias"):
            vendor_content_count += 1

    total = len(sources)
    # Find dominant tier (highest credibility weight, then count)
    dominant_tier = ""
    if tier_counts:
        dominant_tier = max(
            [t for t in tier_counts if t in CREDIBILITY_WEIGHTS],
            key=lambda t: (CREDIBILITY_WEIGHTS[t], tier_counts[t]),
            default="",
        ) or max(tier_counts, key=lambda t: tier_counts[t])

    return {
        "tier_counts": dict(tier_counts),
        "type_counts": dict(type_counts),
        "vendor_content_count": vendor_content_count,
        "total_sources": total,
        "dominant_tier": dominant_tier,
    }


def compute_i4_coverage_gaps(pages, lint_findings):
    """
    I4 — Coverage gaps.
    Returns three lists: stubs, thin_pages, collection_gaps.

    collection_gaps sourced from lint-findings.json if present and fresh.

    Example:
        i4 = compute_i4_coverage_gaps(pages, lint_findings)
        len(i4["stubs"])   # 5
    """
    stubs = []
    thin_pages = []

    for page in pages:
        entry = {
            "slug": page["slug"],
            "filepath": page["filepath"],
            "title": page["title"],
            "type": page["type"],
            "source_count": page["source_count"],
        }
        if page["status"] == "stub":
            stubs.append(entry)
        elif page["source_count"] == 1:
            thin_pages.append(entry)

    # Collection gaps from lint-findings.json
    collection_gaps = []
    lint_note = ""
    if lint_findings is None:
        lint_note = "Lint gap data unavailable — run wiki-lint.py to refresh."
    else:
        if lint_findings.get("_is_stale"):
            age = lint_findings.get("_age_days", "?")
            lint_note = f"Lint gap data is {age} days old — run wiki-lint.py to refresh."
        for item in lint_findings.get("findings", []):
            if item.get("type") == "collection-gap":
                collection_gaps.append({
                    "topic": item.get("topic", ""),
                    "details": item.get("details", ""),
                })

    return {
        "stubs": stubs,
        "thin_pages": thin_pages,
        "collection_gaps": collection_gaps,
        "lint_note": lint_note,
    }


def compute_i5_heatmap(pages):
    """
    I5 — Teaching coverage and heatmap.
    Returns ratio, tagged_count, and nested heatmap {domain: {context: count}}.

    A page with multiple domains/contexts contributes to all matching cells.

    Example:
        i5 = compute_i5_heatmap(pages)
        i5["ratio"]   # 0.45
        i5["heatmap"]["tool-evaluation-and-selection"]["teaching-and-instruction"]  # 3
    """
    excluded_statuses = {"stub", "deprecated", "discontinued"}
    content_total = sum(
        1 for p in pages
        if p["type"] in {"topic", "tool", "comparison", "pitfalls"}
        and p["status"] not in excluded_statuses
    )

    tagged = [
        p for p in pages
        if p.get("teaching_relevance") is True
        and p["status"] not in excluded_statuses
        and p["type"] != "teaching-brief"
    ]

    # Build nested heatmap dict
    heatmap = {}
    for domain in COMPETENCY_DOMAINS:
        heatmap[domain] = {}
        for context in PROFESSIONAL_CONTEXTS:
            heatmap[domain][context] = 0

    for page in tagged:
        for domain in page["competency_domains"]:
            if domain not in heatmap:
                continue
            for context in page["professional_contexts"]:
                if context in heatmap[domain]:
                    heatmap[domain][context] += 1

    ratio = len(tagged) / content_total if content_total > 0 else 0.0

    return {
        "ratio": round(ratio, 3),
        "tagged_count": len(tagged),
        "total_content": content_total,
        "heatmap": heatmap,
        "tagged_pages": [
            {
                "slug": p["slug"],
                "filepath": p["filepath"],
                "title": p["title"],
                "type": p["type"],
                "competency_domains": p["competency_domains"],
                "professional_contexts": p["professional_contexts"],
                "technical_depth": p["technical_depth"],
                "summary": p["summary"],
            }
            for p in tagged
        ],
    }


def compute_i6_recently_learned(pages, sources):
    """
    I6 — Recently learned.
    Pages with last_assessed or created within RECENTLY_LEARNED_DAYS days.

    Credibility badge: max credibility tier of sources in page's Key Claims.

    Example:
        i6 = compute_i6_recently_learned(pages, sources)
        i6[0]["credibility_badge"]   # "institutional"
    """
    today = date.today()
    cutoff = today.toordinal() - RECENTLY_LEARNED_DAYS
    results = []

    for page in pages:
        # Check last_assessed
        d_assessed = parse_date(page["last_assessed"]) if page["last_assessed"] else None
        # Check created
        d_created = parse_date(page["created"]) if page["created"] else None

        recent_date = None
        if d_assessed and d_assessed.toordinal() >= cutoff:
            recent_date = d_assessed
        elif d_created and d_created.toordinal() >= cutoff:
            recent_date = d_created

        if recent_date is None:
            continue

        results.append({
            "slug": page["slug"],
            "filepath": page["filepath"],
            "title": page["title"],
            "type": page["type"],
            "date": recent_date.isoformat(),
            "credibility_badge": page.get("max_credibility_tier", ""),
        })

    results.sort(key=lambda x: x["date"], reverse=True)
    return results


# ── HTML rendering ─────────────────────────────────────────────────────────────

def render_dashboard(data):
    """
    Return complete self-contained HTML for the wiki dashboard.

    Embeds all data as JSON, all CSS in <style>, all JS in <script>.
    No external dependencies. Data serialized with json.dumps default=str.

    Spec: wiki-dashboard-build-spec.md Sections 3.1–3.9.

    Example:
        html = render_dashboard(data)
        open("wiki-dashboard.html", "w").write(html)
    """
    json_str = json.dumps(data, ensure_ascii=False, default=str)

    css = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14px;color:#1f2937;background:#f9fafb;min-height:100vh}
.status-bar{background:#1e293b;color:#f8fafc;padding:8px 16px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:50;flex-wrap:wrap;gap:8px}
.status-bar.stale{background:#f59e0b;color:#1f2937}
.stale-msg{display:none;font-weight:600;font-size:12px;margin-top:2px}
.tabs{display:flex;border-bottom:2px solid #e5e7eb;background:white;padding:0 16px;position:sticky;top:40px;z-index:40}
.tab{padding:11px 20px;cursor:pointer;color:#6b7280;border-bottom:3px solid transparent;font-size:14px}
.tab.active{color:#1d4ed8;border-bottom-color:#1d4ed8;font-weight:600}
.panel-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;padding:16px;max-width:1440px;margin:0 auto}
@media(max-width:1200px){.panel-grid{grid-template-columns:1fr}}
.panel-card{background:white;border:1px solid #e5e7eb;border-radius:8px;padding:16px;cursor:pointer;transition:box-shadow .15s}
.panel-card:hover{box-shadow:0 2px 8px rgba(0,0,0,.1)}
.panel-title{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.07em;color:#6b7280;margin-bottom:10px}
.panel-metric{font-size:30px;font-weight:700;color:#1f2937;line-height:1.1}
.panel-sub{font-size:12px;color:#6b7280;margin-top:4px}
.badge{display:inline-block;padding:2px 7px;border-radius:4px;font-size:11px;font-weight:600;text-transform:uppercase;white-space:nowrap}
.badge-green{background:#dcfce7;color:#15803d}
.badge-amber{background:#fef3c7;color:#d97706}
.badge-red{background:#fee2e2;color:#dc2626}
.badge-grey{background:#f3f4f6;color:#6b7280}
.badge-blue{background:#dbeafe;color:#1d4ed8}
.badge-darkgrey{background:#e5e7eb;color:#374151}
.layer2{display:none;margin-top:14px;padding-top:14px;border-top:1px solid #e5e7eb;max-height:440px;overflow-y:auto}
.layer2.active{display:block}
.data-table{width:100%;border-collapse:collapse;font-size:12px}
.data-table th{background:#f8fafc;font-weight:600;padding:7px 10px;text-align:left;cursor:pointer;user-select:none;border-bottom:2px solid #e5e7eb;white-space:nowrap;font-size:11px}
.data-table th:hover{background:#f1f5f9}
.data-table td{padding:7px 10px;border-bottom:1px solid #f3f4f6;vertical-align:top}
.data-table tr:hover td{background:#fafafa}
.sort-asc::after{content:" ↑"}.sort-desc::after{content:" ↓"}
.modal-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:200;align-items:flex-start;justify-content:center;padding-top:5vh}
.modal-overlay.active{display:flex}
.modal{background:white;border-radius:8px;padding:24px;max-width:820px;width:92%;max-height:88vh;overflow-y:auto;position:relative}
.modal-close{position:absolute;top:12px;right:14px;cursor:pointer;font-size:22px;color:#9ca3af;background:none;border:none;line-height:1}
.modal-close:hover{color:#374151}
.heatmap-table{border-collapse:collapse;font-size:11px}
.heatmap-cell{min-width:40px;text-align:center;padding:4px 2px;cursor:pointer;border:1px solid #e5e7eb}
.heatmap-cell:hover{opacity:.82;outline:2px solid #1d4ed8}
.hm-col-hdr{font-weight:600;padding:4px 6px;background:#f8fafc;font-size:10px;max-width:72px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;text-align:center;border:1px solid #e5e7eb}
.hm-row-hdr{font-size:10px;padding:4px 8px;text-align:right;max-width:170px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#4b5563;border:1px solid #e5e7eb}
.claim-current{background:#f0fdf4}
.claim-contested{background:#fffbeb}
.claim-superseded td{color:#9ca3af}
.regen-wrap{position:relative}
.regen-btn{background:#374151;color:white;border:none;padding:5px 11px;border-radius:4px;cursor:pointer;font-size:12px}
.regen-btn:hover{background:#4b5563}
.regen-dropdown{display:none;position:absolute;right:0;top:calc(100% + 4px);background:white;border:1px solid #e5e7eb;border-radius:6px;box-shadow:0 4px 12px rgba(0,0,0,.15);min-width:235px;z-index:100}
.regen-dropdown.active{display:block}
.regen-option{padding:9px 14px;cursor:pointer;color:#1f2937;font-size:12px}
.regen-option:hover{background:#f8fafc}
.regen-tooltip{position:absolute;right:0;top:calc(100% + 4px);background:#1e293b;color:white;padding:6px 12px;border-radius:4px;font-size:11px;white-space:nowrap;display:none;z-index:101}
.regen-tooltip.active{display:block}
.copy-modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:300;align-items:center;justify-content:center}
.copy-modal.active{display:flex}
.copy-modal-inner{background:white;padding:24px;border-radius:8px;max-width:500px;width:92%}
.copy-cmd{font-family:"SF Mono",Menlo,monospace;background:#f8fafc;border:1px solid #e5e7eb;padding:10px 12px;border-radius:4px;font-size:12px;word-break:break-all;margin:10px 0;color:#1f2937}
.op-ingest{background:#dbeafe;color:#1d4ed8}
.op-lint{background:#ede9fe;color:#7c3aed}
.op-contradiction{background:#fef3c7;color:#d97706}
.op-query{background:#d1fae5;color:#065f46}
.op-other{background:#f3f4f6;color:#6b7280}
a.page-link{color:#1d4ed8;text-decoration:none}
a.page-link:hover{text-decoration:underline}
details summary{cursor:pointer;outline:none;font-size:12px;color:#6b7280}
.view-toggle{font-size:12px;color:#1d4ed8;cursor:pointer;background:none;border:none;padding:0;margin-top:8px}
"""

    body_html = """
<div id="status-bar" class="status-bar">
  <div>
    <span id="status-text" style="font-size:13px"></span>
    <div id="stale-msg" class="stale-msg"></div>
  </div>
  <div class="regen-wrap">
    <button class="regen-btn" onclick="toggleRegenDropdown(event)">Regenerate &#9662;</button>
    <div id="regen-dropdown" class="regen-dropdown">
      <div class="regen-option" onclick="copyCommand('python3 wiki-dashboard.py')">Dashboard only</div>
      <div class="regen-option" onclick="copyCommand('python3 wiki-lint.py &amp;&amp; python3 wiki-dashboard.py')">Lint + Dashboard</div>
    </div>
    <div id="regen-tooltip" class="regen-tooltip">Copied &#8212; paste in terminal, then reload</div>
  </div>
</div>
<div class="tabs">
  <div class="tab active" id="tab-health" onclick="switchTab('health')">Health</div>
  <div class="tab" id="tab-insight" onclick="switchTab('insight')">Insight</div>
</div>
<div id="health-panels" class="panel-grid"></div>
<div id="insight-panels" class="panel-grid" style="display:none"></div>
<div id="modal-overlay" class="modal-overlay" onclick="if(event.target===this)closeLayer3()">
  <div class="modal">
    <button class="modal-close" onclick="closeLayer3()">&#x2715;</button>
    <div id="modal-body"></div>
  </div>
</div>
<div id="copy-modal" class="copy-modal" onclick="if(event.target===this)closeCopyModal()">
  <div class="copy-modal-inner">
    <strong>Copy this command and paste in terminal:</strong>
    <div id="copy-cmd-text" class="copy-cmd"></div>
    <button onclick="closeCopyModal()" style="font-size:13px;padding:6px 14px;border:1px solid #e5e7eb;border-radius:4px;cursor:pointer;background:white">Close</button>
  </div>
</div>
"""

    js = r"""
// ── State ─────────────────────────────────────────────────────────────────
let state = {tab:'health', activeLayer2:null};
let pageIndex = {};

// ── Init ──────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
    (WIKI_DATA.pages || []).forEach(function(p){ pageIndex[p.slug] = p; });
    checkStaleness();
    renderStatusBar();
    document.getElementById('health-panels').innerHTML = renderHealthPanels();
    document.getElementById('insight-panels').innerHTML = renderInsightPanels();
});

function checkStaleness() {
    var genDate = new Date(WIKI_DATA.generated_date);
    var ageDays = Math.floor((Date.now() - genDate.getTime()) / 86400000);
    if (ageDays > 7) {
        document.getElementById('status-bar').classList.add('stale');
        var msg = document.getElementById('stale-msg');
        msg.style.display = '';
        msg.textContent = 'Dashboard is ' + ageDays + ' days old — run `python3 wiki-dashboard.py` to refresh.';
    }
}

function renderStatusBar() {
    var lastLint = WIKI_DATA.last_lint || 'never';
    var vault = WIKI_DATA.obsidian_vault || 'deep links disabled';
    document.getElementById('status-text').innerHTML =
        'Generated: ' + escH(WIKI_DATA.generated_date) + ' &nbsp;|&nbsp; ' +
        'Last lint: ' + escH(lastLint) + ' &nbsp;|&nbsp; ' +
        WIKI_DATA.total_pages + ' pages &nbsp;|&nbsp; ' +
        WIKI_DATA.total_sources + ' sources &nbsp;|&nbsp; ' +
        'Vault: ' + escH(vault);
}

// ── Tab switching ─────────────────────────────────────────────────────────
function switchTab(tab) {
    state.tab = tab;
    document.getElementById('health-panels').style.display = tab === 'health' ? 'grid' : 'none';
    document.getElementById('insight-panels').style.display = tab === 'insight' ? 'grid' : 'none';
    document.getElementById('tab-health').className = 'tab' + (tab === 'health' ? ' active' : '');
    document.getElementById('tab-insight').className = 'tab' + (tab === 'insight' ? ' active' : '');
}

// ── Layer 2 toggle ────────────────────────────────────────────────────────
function togglePanel(id) {
    var el = document.getElementById('l2-' + id);
    if (!el) return;
    var isOpen = el.classList.contains('active');
    if (state.activeLayer2 && state.activeLayer2 !== id) {
        var prev = document.getElementById('l2-' + state.activeLayer2);
        if (prev) prev.classList.remove('active');
    }
    if (!isOpen) { el.classList.add('active'); state.activeLayer2 = id; }
    else { el.classList.remove('active'); state.activeLayer2 = null; }
}

// ── Layer 3 modal ─────────────────────────────────────────────────────────
function showLayer3(slug) {
    var page = pageIndex[slug];
    if (!page) return;
    document.getElementById('modal-body').innerHTML = buildLayer3(page);
    document.getElementById('modal-overlay').classList.add('active');
}

function closeLayer3() {
    document.getElementById('modal-overlay').classList.remove('active');
}

function buildLayer3(page) {
    var sc = {current:'#dcfce7:#15803d',active:'#dcfce7:#15803d',emerging:'#dcfce7:#15803d',
              developing:'#dbeafe:#1d4ed8',stale:'#fef3c7:#d97706',stub:'#f3f4f6:#6b7280',
              deprecated:'#e5e7eb:#374151',discontinued:'#e5e7eb:#374151',contested:'#fee2e2:#dc2626'};
    var h = '<div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;flex-wrap:wrap">' +
        typeBadge(page.type) + ' ' + statusBadge(page.status) +
        ' <span style="font-size:18px;font-weight:700">' + escH(page.title) + '</span></div>';
    if (page.summary) {
        h += '<p style="color:#4b5563;margin-bottom:12px;line-height:1.5;font-size:13px">' + escH(page.summary) + '</p>';
    }
    h += '<div style="display:flex;gap:16px;flex-wrap:wrap;font-size:12px;color:#6b7280;margin-bottom:16px">' +
        '<span>Last assessed: ' + (page.last_assessed || 'never') + '</span>' +
        '<span>Source count: ' + page.source_count + '</span>' +
        '<span>Created: ' + (page.created || '—') + '</span>' +
        (page.technical_depth ? '<span>Depth: ' + escH(page.technical_depth) + '</span>' : '') +
        '</div>';

    if (page.key_claims && page.key_claims.length > 0) {
        h += '<h4 style="font-weight:600;margin-bottom:8px;color:#374151;font-size:13px">Key Claims</h4>';
        h += '<div style="overflow-x:auto"><table class="data-table" style="font-size:11px"><thead><tr>' +
            '<th>Claim</th><th>Source</th><th>Date</th><th>Status</th><th>Score</th><th>Exempt</th>' +
            '</tr></thead><tbody>';
        for (var i = 0; i < page.key_claims.length; i++) {
            var c = page.key_claims[i];
            var rowCls = c.status === 'current' ? 'claim-current' :
                         c.status === 'contested' ? 'claim-contested' :
                         c.status === 'superseded' ? 'claim-superseded' : '';
            var stCell = (c.ctrd_ids && c.ctrd_ids.length > 0)
                ? '<span class="badge badge-amber">contested</span> ' +
                  c.ctrd_ids.map(function(id){return '<span style="font-size:10px;color:#d97706">'+id+'</span>';}).join(' ')
                : '<span>' + escH(c.status) + '</span>';
            h += '<tr class="' + rowCls + '">' +
                '<td style="max-width:260px;word-break:break-word">' + escH(c.claim) + '</td>' +
                '<td style="color:#6b7280;font-size:10px">' + escH(c.source) + '</td>' +
                '<td style="white-space:nowrap">' + escH(c.date) + '</td>' +
                '<td>' + stCell + '</td>' +
                '<td>' + (typeof c.support_score === 'number' ? c.support_score.toFixed ? c.support_score.toFixed(1) : c.support_score : escH(String(c.support_score))) + '</td>' +
                '<td>' + (c.decay_exempt ? '✓' : '') + '</td></tr>';
        }
        h += '</tbody></table></div>';
    } else {
        h += '<p style="color:#9ca3af;font-style:italic;font-size:12px;margin-top:8px">No Key Claims found.</p>';
    }

    if (page.teaching_relevance) {
        h += '<div style="margin-top:16px"><span style="font-weight:600;font-size:13px">Teaching:</span> <span class="badge badge-green">Yes</span>';
        if (page.competency_domains && page.competency_domains.length)
            h += '<div style="margin-top:5px;font-size:12px;color:#4b5563">Domains: ' + escH(page.competency_domains.join(', ')) + '</div>';
        if (page.professional_contexts && page.professional_contexts.length)
            h += '<div style="margin-top:3px;font-size:12px;color:#4b5563">Contexts: ' + escH(page.professional_contexts.join(', ')) + '</div>';
        h += '</div>';
    }

    if (WIKI_DATA.obsidian_vault) {
        var link = 'obsidian://open?vault=' + encodeURIComponent(WIKI_DATA.obsidian_vault) + '&file=' + encodeURIComponent(page.filepath);
        h += '<div style="margin-top:16px;padding-top:16px;border-top:1px solid #e5e7eb">' +
            '<a href="' + link + '" style="color:#1d4ed8;font-size:13px">Open in Obsidian →</a></div>';
    }
    return h;
}

// ── Regenerate button ─────────────────────────────────────────────────────
function toggleRegenDropdown(e) {
    e.stopPropagation();
    var d = document.getElementById('regen-dropdown');
    d.classList.toggle('active');
    if (d.classList.contains('active')) {
        document.addEventListener('click', function handler(ev) {
            if (!d.contains(ev.target)) { d.classList.remove('active'); }
            document.removeEventListener('click', handler);
        });
    }
}

function copyCommand(cmd) {
    document.getElementById('regen-dropdown').classList.remove('active');
    // Unescape the HTML entity in the command
    cmd = cmd.replace(/&amp;/g, '&');
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(cmd).then(function() {
            var tip = document.getElementById('regen-tooltip');
            tip.classList.add('active');
            setTimeout(function(){ tip.classList.remove('active'); }, 2000);
        });
    } else {
        document.getElementById('copy-cmd-text').textContent = cmd;
        document.getElementById('copy-modal').classList.add('active');
    }
}

function closeCopyModal() { document.getElementById('copy-modal').classList.remove('active'); }

// ── Table sorting ─────────────────────────────────────────────────────────
function sortTable(tableId, col) {
    var table = document.getElementById(tableId);
    if (!table) return;
    var tbody = table.querySelector('tbody');
    var rows = Array.prototype.slice.call(tbody.querySelectorAll('tr'));
    var th = table.querySelectorAll('th')[col];
    var asc = th.dataset.sort !== 'asc';
    table.querySelectorAll('th').forEach(function(t){ t.className = ''; delete t.dataset.sort; });
    th.dataset.sort = asc ? 'asc' : 'desc';
    th.className = asc ? 'sort-asc' : 'sort-desc';
    rows.sort(function(a, b) {
        var av = a.cells[col] ? a.cells[col].textContent.trim() : '';
        var bv = b.cells[col] ? b.cells[col].textContent.trim() : '';
        var an = parseFloat(av), bn = parseFloat(bv);
        var cmp = (!isNaN(an) && !isNaN(bn)) ? (an - bn) : av.localeCompare(bv);
        return asc ? cmp : -cmp;
    });
    rows.forEach(function(r){ tbody.appendChild(r); });
}

// ── Heatmap filter ────────────────────────────────────────────────────────
function filterI5(domain, ctx) {
    document.querySelectorAll('#i5-page-table tbody tr').forEach(function(row) {
        var rd = row.dataset.domains || '', rc = row.dataset.contexts || '';
        row.style.display = (rd.indexOf(domain) >= 0 && rc.indexOf(ctx) >= 0) ? '' : 'none';
    });
    document.querySelectorAll('.heatmap-cell').forEach(function(c){ c.style.outline = ''; });
    var cell = document.querySelector('.heatmap-cell[data-domain="'+domain+'"][data-context="'+ctx+'"]');
    if (cell) cell.style.outline = '2px solid #dc2626';
    var list = document.getElementById('i5-page-list');
    if (list) { list.style.display = ''; list.scrollIntoView({behavior:'smooth',block:'nearest'}); }
}

function clearI5Filter() {
    document.querySelectorAll('#i5-page-table tbody tr').forEach(function(r){ r.style.display = ''; });
    document.querySelectorAll('.heatmap-cell').forEach(function(c){ c.style.outline = ''; });
}

// ── Helpers ───────────────────────────────────────────────────────────────
function escH(s) {
    if (s === null || s === undefined) return '';
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function typeBadge(type) {
    var map = {topic:'#dbeafe:#1d4ed8',tool:'#dcfce7:#15803d',comparison:'#ede9fe:#7c3aed',
               pitfalls:'#fef3c7:#d97706','teaching-brief':'#d1fae5:#065f46'};
    var p = (map[type] || '#f3f4f6:#6b7280').split(':');
    return '<span class="badge" style="background:'+p[0]+';color:'+p[1]+'">' + escH(type) + '</span>';
}

function statusBadge(status) {
    var map = {current:'#dcfce7:#15803d',active:'#dcfce7:#15803d',emerging:'#dcfce7:#15803d',
               developing:'#dbeafe:#1d4ed8',stale:'#fef3c7:#d97706',stub:'#f3f4f6:#6b7280',
               deprecated:'#e5e7eb:#374151',discontinued:'#e5e7eb:#374151',contested:'#fee2e2:#dc2626'};
    var p = (map[status] || '#f3f4f6:#6b7280').split(':');
    return '<span class="badge" style="background:'+p[0]+';color:'+p[1]+'">' + escH(status) + '</span>';
}

function credBadge(tier) {
    if (!tier) return '';
    var map = {'peer-reviewed':'#dbeafe:#1d4ed8',institutional:'#ede9fe:#7c3aed',
               practitioner:'#dcfce7:#15803d',community:'#f3f4f6:#6b7280'};
    var p = (map[tier] || '#f3f4f6:#6b7280').split(':');
    return '<span class="badge" style="background:'+p[0]+';color:'+p[1]+';font-size:10px">' + escH(tier) + '</span>';
}

function opBadge(op) {
    var cls = {ingest:'op-ingest',lint:'op-lint',query:'op-query',
               'contradiction-flag':'op-contradiction','contradiction-resolved':'op-contradiction',
               'contradiction-auto-resolved':'op-contradiction'}[op] || 'op-other';
    return '<span class="badge ' + cls + '">' + escH(op) + '</span>';
}

function pageLink(slug, title) {
    return '<a class="page-link" href="javascript:void(0)" onclick="showLayer3(\'' + escH(slug) + '\')">' + escH(title) + '</a>';
}

function heatColor(count, max) {
    if (max === 0 || count === 0) return '#ffffff';
    var t = count / max;
    var r = Math.round(255 + t*(29-255)), g = Math.round(255 + t*(78-255)), b = Math.round(255 + t*(216-255));
    return 'rgb('+r+','+g+','+b+')';
}

function sTh(label, col, tid) {
    return '<th onclick="sortTable(\''+tid+'\','+col+')">' + escH(label) + '</th>';
}

function panel(id, title, summary, layer2) {
    return '<div class="panel-card" onclick="togglePanel(\''+id+'\')">' +
        '<div class="panel-title">'+title+'</div>' +
        '<div onclick="event.stopPropagation()">'+summary+'</div>' +
        '<div id="l2-'+id+'" class="layer2" onclick="event.stopPropagation()">'+layer2+'</div>' +
        '</div>';
}

// ── Panel renderers ───────────────────────────────────────────────────────
function renderHealthPanels() { return renderH1()+renderH2()+renderH3()+renderH4()+renderH5(); }
function renderInsightPanels() { return renderI1()+renderI2()+renderI3()+renderI4()+renderI5()+renderI6(); }

function renderH1() {
    var h1 = WIKI_DATA.panels.h1 || {};
    var h2 = WIKI_DATA.panels.h2 || [];
    var stubCount = 0;
    Object.values(h1).forEach(function(v){ stubCount += (v.stub||0); });
    var types = Object.entries(h1);
    var maxT = Math.max.apply(null, types.map(function(e){ return e[1]._total||0; }).concat([1]));
    var bars = '<div style="margin-top:10px">';
    types.forEach(function(entry){
        var t = entry[0], v = entry[1];
        var pct = Math.round(((v._total||0)/maxT)*100);
        bars += '<div style="display:flex;align-items:center;gap:6px;margin-bottom:3px">' +
            '<span style="font-size:10px;width:70px;color:#6b7280;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'+escH(t)+'</span>' +
            '<div style="flex:1;background:#f3f4f6;height:10px;border-radius:2px;overflow:hidden">' +
            '<div style="width:'+pct+'%;height:100%;background:#1d4ed8;opacity:0.7"></div></div>' +
            '<span style="font-size:10px;color:#374151;width:22px;text-align:right">'+(v._total||0)+'</span></div>';
    });
    bars += '</div>';
    var summary = '<div class="panel-metric">'+WIKI_DATA.total_pages+'</div>' +
        '<div class="panel-sub">'+h2.length+' stale &nbsp;&middot;&nbsp; '+stubCount+' stub</div>'+bars;

    var rows = '';
    types.forEach(function(entry){
        var t = entry[0], v = entry[1];
        Object.entries(v).forEach(function(se){
            if (se[0]==='_total') return;
            rows += '<tr><td>'+typeBadge(t)+'</td><td>'+statusBadge(se[0])+'</td><td>'+se[1]+'</td></tr>';
        });
    });
    var tbl = '<table class="data-table" id="tbl-h1"><thead><tr>'+sTh('Type',0,'tbl-h1')+sTh('Status',1,'tbl-h1')+sTh('Count',2,'tbl-h1')+'</tr></thead><tbody>'+rows+'</tbody></table>';
    return panel('h1','H1 · Pages',summary,tbl);
}

function renderH2() {
    var h2 = WIKI_DATA.panels.h2 || [];
    var summary = '<div class="panel-metric" style="color:'+(h2.length>0?'#d97706':'#1f2937')+'">'+h2.length+'</div>' +
        '<div class="panel-sub">stale pages</div>';
    var inner = h2.length === 0 ? '<p style="color:#15803d;padding:8px 0">No stale pages.</p>' : '';
    if (h2.length > 0) {
        var rows = h2.map(function(r){
            return '<tr><td>'+pageLink(r.slug,r.title)+'</td><td>'+typeBadge(r.type)+'</td>' +
                '<td>'+(r.last_assessed||'—')+'</td><td>'+(r.staleness_days!==null?r.staleness_days:'?')+'</td></tr>';
        }).join('');
        inner = '<table class="data-table" id="tbl-h2"><thead><tr>'+sTh('Title',0,'tbl-h2')+sTh('Type',1,'tbl-h2')+sTh('Last Assessed',2,'tbl-h2')+sTh('Stale for (days)',3,'tbl-h2')+'</tr></thead><tbody>'+rows+'</tbody></table>';
    }
    return panel('h2','H2 · Stale Pages',summary,inner);
}

function renderH3() {
    var h3 = WIKI_DATA.panels.h3 || {};
    var items = h3.items || [];
    var warn = h3.mismatch_warning ? '<div style="background:#fef3c7;border:1px solid #f59e0b;border-radius:4px;padding:5px 10px;font-size:11px;margin-bottom:8px">⚠ Count mismatch: '+items.length+' CTRD IDs found; overview.md reports '+escH(String(h3.overview_count))+'</div>' : '';
    var summary = '<div class="panel-metric" style="color:'+(items.length>0?'#d97706':'#1f2937')+'">'+items.length+'</div>' +
        '<div class="panel-sub">contested claim'+(items.length!==1?'s':'')+'</div>';
    var inner = warn + (items.length === 0 ? '<p style="color:#15803d;padding:8px 0">No contested claims.</p>' : '');
    if (items.length > 0) {
        var rows = items.map(function(r){
            return '<tr><td>'+pageLink(r.page_slug,r.page_title)+'</td>' +
                '<td style="max-width:280px;font-size:11px">'+escH(r.claim)+'</td>' +
                '<td style="font-size:11px">'+(r.ctrd_ids||[]).join(', ')+'</td>' +
                '<td>'+escH(String(r.support_score))+'</td></tr>';
        }).join('');
        inner = warn + '<table class="data-table" id="tbl-h3"><thead><tr>'+sTh('Page',0,'tbl-h3')+sTh('Claim',1,'tbl-h3')+sTh('CTRD IDs',2,'tbl-h3')+sTh('Score',3,'tbl-h3')+'</tr></thead><tbody>'+rows+'</tbody></table>';
    }
    return panel('h3','H3 · Contradictions',summary,inner);
}

function renderH4() {
    var h4 = WIKI_DATA.panels.h4 || [];
    var lastStr = '—';
    if (h4.length > 0) {
        var d = Math.floor((Date.now()-new Date(h4[0].date).getTime())/86400000);
        lastStr = d === 0 ? 'today' : d+' day'+(d!==1?'s':'')+' ago';
    }
    var summary = '<div class="panel-metric">'+lastStr+'</div><div class="panel-sub">last log entry &middot; '+h4.length+' shown</div>';
    var inner = h4.length === 0 ? '<p style="color:#9ca3af;padding:8px 0">No log entries.</p>' : '';
    if (h4.length > 0) {
        var rows = h4.map(function(r){
            return '<tr><td style="white-space:nowrap">'+escH(r.date)+'</td><td>'+opBadge(r.operation)+'</td>' +
                '<td style="font-size:11px;color:#4b5563;max-width:340px">'+escH(r.description)+'</td></tr>';
        }).join('');
        inner = '<table class="data-table" id="tbl-h4"><thead><tr>'+sTh('Date',0,'tbl-h4')+sTh('Operation',1,'tbl-h4')+sTh('Description',2,'tbl-h4')+'</tr></thead><tbody>'+rows+'</tbody></table>';
    }
    return panel('h4','H4 · Recent Activity',summary,inner);
}

function renderH5() {
    var h5 = WIKI_DATA.panels.h5 || {};
    var urg = (h5.urgent||[]).length, wtch = (h5.watch||[]).length, mon = (h5.monitor||[]).length;
    var summary = '<div style="display:flex;gap:14px;flex-wrap:wrap">' +
        '<div><span style="color:#dc2626;font-size:24px;font-weight:700">'+urg+'</span><span style="font-size:11px;color:#dc2626;margin-left:4px">≤30d urgent</span></div>' +
        '<div><span style="color:#d97706;font-size:24px;font-weight:700">'+wtch+'</span><span style="font-size:11px;color:#d97706;margin-left:4px">31–60d watch</span></div>' +
        '<div><span style="color:#ca8a04;font-size:24px;font-weight:700">'+mon+'</span><span style="font-size:11px;color:#ca8a04;margin-left:4px">61–90d monitor</span></div>' +
        '</div>';
    var all = (h5.urgent||[]).concat(h5.watch||[]).concat(h5.monitor||[]);
    var inner = all.length === 0 ? '<p style="color:#15803d;padding:8px 0">No pages approaching stale.</p>' : '';
    if (all.length > 0) {
        var rows = all.map(function(r){
            var d = r.days_until_stale, clr = d<=30?'#dc2626':d<=60?'#d97706':'#ca8a04';
            return '<tr><td>'+pageLink(r.slug,r.title)+'</td><td>'+typeBadge(r.type)+'</td>' +
                '<td style="color:'+clr+';font-weight:600">'+d+'</td>' +
                '<td>'+(r.last_assessed||'—')+'</td></tr>';
        }).join('');
        inner = '<table class="data-table" id="tbl-h5"><thead><tr>'+sTh('Title',0,'tbl-h5')+sTh('Type',1,'tbl-h5')+sTh('Days Until Stale',2,'tbl-h5')+sTh('Last Assessed',3,'tbl-h5')+'</tr></thead><tbody>'+rows+'</tbody></table>';
    }
    return panel('h5','H5 · Decay Trajectory',summary,inner);
}

function renderI1() {
    var i1 = WIKI_DATA.panels.i1 || [];
    var top = i1[0];
    var summary = top
        ? '<div class="panel-metric" style="font-size:18px;line-height:1.3">'+escH(top.title.substring(0,35))+'</div>' +
          '<div class="panel-sub">avg score '+top.avg_score+' &middot; top '+i1.length+' shown</div>'
        : '<div class="panel-metric">—</div><div class="panel-sub">No qualifying pages</div>';
    var caveat = '<p style="font-size:10px;color:#9ca3af;margin-bottom:8px;font-style:italic">Scores reflect source coverage within this wiki, not external validation. A well-evidenced wrong claim ranks above a thinly-sourced correct one.</p>';
    var inner = caveat;
    if (i1.length === 0) {
        inner += '<p style="color:#9ca3af">No pages with ≥2 qualifying claims.</p>';
    } else {
        var rows = i1.map(function(r,i){
            return '<tr><td style="color:#9ca3af">'+(i+1)+'</td><td>'+pageLink(r.slug,r.title)+'</td>' +
                '<td>'+typeBadge(r.type)+'</td>' +
                '<td style="font-weight:600">'+r.avg_score+'</td>' +
                '<td>'+r.claim_count+'</td>' +
                '<td style="font-size:10px;color:#4b5563;max-width:220px">'+escH(r.top_claim)+'</td></tr>';
        }).join('');
        inner += '<table class="data-table" id="tbl-i1"><thead><tr>'+sTh('#',0,'tbl-i1')+sTh('Title',1,'tbl-i1')+sTh('Type',2,'tbl-i1')+sTh('Avg Score',3,'tbl-i1')+sTh('Claims',4,'tbl-i1')+sTh('Top Claim',5,'tbl-i1')+'</tr></thead><tbody>'+rows+'</tbody></table>';
    }
    return panel('i1','I1 · Best-Evidenced',summary,inner);
}

function renderI2() {
    var i2 = WIKI_DATA.panels.i2 || [];
    var summary = '<div class="panel-metric" style="color:'+(i2.length>0?'#dc2626':'#1f2937')+'">'+i2.length+'</div>' +
        '<div class="panel-sub">contested claim'+(i2.length!==1?'s':'')+'</div>';
    var inner = i2.length === 0 ? '<p style="color:#15803d;padding:8px 0">No contested claims.</p>' : '';
    if (i2.length > 0) {
        var rows = i2.map(function(r){
            return '<tr><td>'+pageLink(r.page_slug,r.page_title)+'</td>' +
                '<td style="font-size:11px;max-width:290px">'+escH(r.claim)+'</td>' +
                '<td style="font-size:11px">'+(r.ctrd_ids||[]).join(', ')+'</td>' +
                '<td>'+escH(String(r.support_score))+'</td></tr>';
        }).join('');
        inner = '<table class="data-table" id="tbl-i2"><thead><tr>'+sTh('Page',0,'tbl-i2')+sTh('Claim',1,'tbl-i2')+sTh('CTRD IDs',2,'tbl-i2')+sTh('Score',3,'tbl-i2')+'</tr></thead><tbody>'+rows+'</tbody></table>';
    }
    return panel('i2','I2 · Contested Areas',summary,inner);
}

function renderI3() {
    var i3 = WIKI_DATA.panels.i3 || {};
    var tiers = i3.tier_counts || {}, total = i3.total_sources || 0;
    var summary = '<div class="panel-metric">'+total+'</div>' +
        '<div class="panel-sub">'+escH(i3.dominant_tier||'—')+' dominant</div>';
    var order = ['peer-reviewed','institutional','practitioner','community'];
    var colors = {'peer-reviewed':'#1d4ed8',institutional:'#7c3aed',practitioner:'#15803d',community:'#9ca3af'};
    var bars = '<div style="margin-top:8px">';
    order.forEach(function(tier){
        var cnt = tiers[tier]||0; if (!cnt) return;
        var pct = total>0?Math.round(cnt/total*100):0;
        bars += '<div style="display:flex;align-items:center;gap:6px;margin-bottom:5px">' +
            '<span style="font-size:11px;width:100px;color:#374151">'+escH(tier)+'</span>' +
            '<div style="flex:1;background:#f3f4f6;height:14px;border-radius:3px;overflow:hidden">' +
            '<div style="width:'+pct+'%;height:100%;background:'+(colors[tier]||'#6b7280')+'"></div></div>' +
            '<span style="font-size:11px;width:55px;text-align:right;color:#4b5563">'+cnt+' ('+pct+'%)</span></div>';
    });
    bars += '</div>';
    if (i3.vendor_content_count > 0)
        bars += '<p style="font-size:12px;color:#d97706;margin-top:6px">⚠ '+i3.vendor_content_count+' vendor-content source'+(i3.vendor_content_count!==1?'s':'')+'</p>';
    var typeRows = Object.entries(i3.type_counts||{}).sort(function(a,b){return b[1]-a[1];}).map(function(e){
        return '<tr><td>'+escH(e[0])+'</td><td>'+e[1]+'</td></tr>';
    }).join('');
    var tblHtml = typeRows ? '<details style="margin-top:10px"><summary>Source types</summary>' +
        '<table class="data-table" id="tbl-i3" style="margin-top:6px"><thead><tr>'+sTh('Type',0,'tbl-i3')+sTh('Count',1,'tbl-i3')+'</tr></thead><tbody>'+typeRows+'</tbody></table></details>' : '';
    return panel('i3','I3 · Evidence Quality',summary,bars+tblHtml);
}

function renderI4() {
    var i4 = WIKI_DATA.panels.i4 || {};
    var stubs = i4.stubs||[], thin = i4.thin_pages||[], gaps = i4.collection_gaps||[];
    var summary = '<div class="panel-metric">'+(stubs.length+thin.length)+'</div>' +
        '<div class="panel-sub">'+stubs.length+' stubs &middot; '+thin.length+' thin &middot; '+gaps.length+' gap hints</div>';
    var note = i4.lint_note ? '<p style="font-size:11px;color:#9ca3af;margin-bottom:8px">'+escH(i4.lint_note)+'</p>' : '';
    var rows = '';
    stubs.forEach(function(r){ rows += '<tr><td><span class="badge badge-grey">stub</span></td><td>'+pageLink(r.slug,r.title)+'</td><td>'+typeBadge(r.type)+'</td></tr>'; });
    thin.forEach(function(r){ rows += '<tr><td><span class="badge badge-amber">thin</span></td><td>'+pageLink(r.slug,r.title)+'</td><td>'+typeBadge(r.type)+'</td></tr>'; });
    gaps.forEach(function(g){ rows += '<tr><td><span class="badge badge-blue">gap</span></td><td>'+escH(g.topic||'—')+'</td><td style="font-size:11px">'+escH(g.details||'')+'</td></tr>'; });
    if (!rows) rows = '<tr><td colspan="3" style="color:#15803d;padding:8px">No coverage gaps detected.</td></tr>';
    var tbl = note + '<table class="data-table" id="tbl-i4"><thead><tr>'+sTh('Category',0,'tbl-i4')+sTh('Title',1,'tbl-i4')+sTh('Detail',2,'tbl-i4')+'</tr></thead><tbody>'+rows+'</tbody></table>';
    return panel('i4','I4 · Coverage Gaps',summary,tbl);
}

function renderI5() {
    var i5 = WIKI_DATA.panels.i5 || {};
    var tagged = i5.tagged_count||0, ratio = i5.ratio||0;
    var summary = '<div class="panel-metric">'+tagged+'</div>' +
        '<div class="panel-sub">pages tagged ('+(ratio*100).toFixed(0)+'%)</div>';

    var heatmap = i5.heatmap || {};
    var ABBREVS = {'tool-evaluation-and-selection':'Tool Eval','practical-ai-use-and-interaction':'Practical AI',
        'ai-integration-in-organizational-workflows':'AI in Workflows','output-verification-and-risk-assessment':'Output Verify',
        'ai-safety-and-alignment-literacy':'AI Safety','capability-horizon-awareness':'Capability',
        'attribution-ip-and-professional-integrity':'Attribution'};
    var domains = Object.keys(heatmap);
    var contexts = domains.length > 0 ? Object.keys(heatmap[domains[0]]||{}) : [];
    var maxC = 0;
    domains.forEach(function(d){ contexts.forEach(function(c){ maxC = Math.max(maxC, (heatmap[d]&&heatmap[d][c])||0); }); });

    var hm = '<div style="overflow-x:auto;margin-bottom:8px"><table class="heatmap-table"><thead><tr>' +
        '<th class="hm-row-hdr" style="text-align:right;background:#f8fafc">Context \\ Domain</th>';
    domains.forEach(function(d){ hm += '<th class="hm-col-hdr" title="'+escH(d)+'">'+escH(ABBREVS[d]||d)+'</th>'; });
    hm += '</tr></thead><tbody>';
    contexts.forEach(function(ctx){
        hm += '<tr><td class="hm-row-hdr">'+escH(ctx)+'</td>';
        domains.forEach(function(d){
            var cnt = (heatmap[d]&&heatmap[d][ctx])||0;
            var bg = heatColor(cnt, maxC);
            var fg = cnt/Math.max(maxC,1) > 0.5 ? '#ffffff' : '#1f2937';
            hm += '<td class="heatmap-cell" data-count="'+cnt+'" data-domain="'+escH(d)+'" data-context="'+escH(ctx)+'"' +
                ' style="background:'+bg+';color:'+(cnt>0?fg:'#e5e7eb')+'"' +
                ' title="'+cnt+' pages: '+escH(d)+' \xd7 '+escH(ctx)+'"' +
                ' onclick="filterI5(\''+escH(d)+'\',\''+escH(ctx)+'\')">'+  (cnt>0?cnt:'') +'</td>';
        });
        hm += '</tr>';
    });
    hm += '</tbody></table></div>';
    hm += '<button class="view-toggle" onclick="clearI5Filter()" style="margin-bottom:8px">Clear filter</button>';

    var taggedPages = i5.tagged_pages || [];
    var pRows = taggedPages.map(function(p){
        return '<tr data-domains="'+escH((p.competency_domains||[]).join('|'))+'" data-contexts="'+escH((p.professional_contexts||[]).join('|'))+'">' +
            '<td>'+pageLink(p.slug,p.title)+'</td><td>'+typeBadge(p.type)+'</td>' +
            '<td style="font-size:11px;color:#6b7280">'+escH(p.technical_depth||'—')+'</td></tr>';
    }).join('');
    var pTbl = '<div id="i5-page-list" style="margin-top:8px">' +
        '<table class="data-table" id="i5-page-table"><thead><tr>'+sTh('Title',0,'i5-page-table')+sTh('Type',1,'i5-page-table')+sTh('Depth',2,'i5-page-table')+'</tr></thead>' +
        '<tbody>'+pRows+'</tbody></table></div>';

    return panel('i5','I5 · Teaching Coverage',summary,hm+pTbl);
}

function renderI6() {
    var i6 = WIKI_DATA.panels.i6 || [];
    var summary = '<div class="panel-metric">'+i6.length+'</div>' +
        '<div class="panel-sub">pages in last 30 days</div>';
    var inner = i6.length === 0 ? '<p style="color:#9ca3af;padding:8px 0">No pages assessed or created in the last 30 days.</p>' : '';
    if (i6.length > 0) {
        var rows = i6.map(function(r){
            return '<tr><td>'+pageLink(r.slug,r.title)+'</td><td>'+typeBadge(r.type)+'</td>' +
                '<td style="white-space:nowrap">'+escH(r.date)+'</td>' +
                '<td>'+credBadge(r.credibility_badge)+'</td></tr>';
        }).join('');
        inner = '<table class="data-table" id="tbl-i6"><thead><tr>'+sTh('Title',0,'tbl-i6')+sTh('Type',1,'tbl-i6')+sTh('Date',2,'tbl-i6')+sTh('Credibility',3,'tbl-i6')+'</tr></thead><tbody>'+rows+'</tbody></table>';
    }
    return panel('i6','I6 · Recently Learned',summary,inner);
}
"""

    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
        "<meta charset=\"UTF-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
        "<title>Wiki Dashboard</title>\n"
        "<style>" + css + "</style>\n"
        "</head>\n<body>\n" + body_html + "\n"
        "<script>\nconst WIKI_DATA = " + json_str + ";\n" + js + "\n</script>\n"
        "</body>\n</html>"
    )


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    """
    Main entry point. Entrypoint guard, data collection, panel computation,
    HTML generation with JSON injection, post-generation verification.

    Usage:
        python3 wiki-dashboard.py
    """
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

    # ── Collect raw data ──────────────────────────────────────────────────────
    raw_data = collect_all_pages()
    pages = raw_data["pages"]
    sources = raw_data["sources"]

    # Parse log.md
    log_entries = []
    if os.path.exists("log.md"):
        try:
            with open("log.md", encoding="utf-8") as f:
                log_text = f.read()
            _, log_body = parse_frontmatter(log_text)
            log_entries = parse_log_entries(log_body, RECENT_ACTIVITY_COUNT)
        except OSError as exc:
            print(f"WARNING: cannot read log.md: {exc}", file=sys.stderr)
    else:
        print("WARNING: log.md not found — H4 and I6 activity data unavailable", file=sys.stderr)

    overview = parse_overview("overview.md")
    lint_findings = parse_lint_findings(LINT_FINDINGS_PATH)

    # ── Derive summary values ─────────────────────────────────────────────────
    today = date.today()
    generated_date = today.isoformat()
    last_lint = overview.get("last_lint", None) or None

    try:
        total_pages = int(overview.get("total_pages", len(pages)))
    except (ValueError, TypeError):
        total_pages = len(pages)

    try:
        total_sources = int(overview.get("total_sources", len(sources)))
    except (ValueError, TypeError):
        total_sources = len(sources)

    # dashboard_is_stale: computed dynamically in JS from generated_date;
    # always False here (dashboard was just generated).
    dashboard_is_stale = False

    # ── Compute panels ────────────────────────────────────────────────────────
    def safe_compute(fn, *args, panel_id="?"):
        try:
            return fn(*args)
        except Exception as exc:
            print(f"WARNING: {panel_id} panel computation error: {exc}", file=sys.stderr)
            return {"_error": str(exc)}

    h1 = safe_compute(compute_h1_type_status, pages, panel_id="H1")
    h2 = safe_compute(compute_h2_stale, pages, panel_id="H2")
    h3 = safe_compute(compute_h3_contradictions, pages, overview, panel_id="H3")
    h4 = safe_compute(compute_h4_recent_activity, log_entries, panel_id="H4")
    h5 = safe_compute(compute_h5_decay_trajectory, pages, panel_id="H5")
    i1 = safe_compute(compute_i1_best_evidenced, pages, panel_id="I1")
    i2 = safe_compute(compute_i2_contested, pages, panel_id="I2")
    i3 = safe_compute(compute_i3_evidence_quality, sources, panel_id="I3")
    i4 = safe_compute(compute_i4_coverage_gaps, pages, lint_findings, panel_id="I4")
    i5 = safe_compute(compute_i5_heatmap, pages, panel_id="I5")
    i6 = safe_compute(compute_i6_recently_learned, pages, sources, panel_id="I6")

    # ── Assemble data dict ────────────────────────────────────────────────────
    data = {
        "generated_date": generated_date,
        "last_lint": last_lint,
        "total_pages": total_pages,
        "total_sources": total_sources,
        "obsidian_vault": OBSIDIAN_VAULT_NAME,
        "dashboard_is_stale": dashboard_is_stale,
        "pages": pages,
        "sources": sources,
        "log_entries": log_entries,
        "overview": {k: str(v) for k, v in overview.items()},
        "lint_findings": lint_findings,
        "panels": {
            "h1": h1,
            "h2": h2,
            "h3": h3,
            "h4": h4,
            "h5": h5,
            "i1": i1,
            "i2": i2,
            "i3": i3,
            "i4": i4,
            "i5": i5,
            "i6": i6,
        },
    }

    # ── Write HTML ────────────────────────────────────────────────────────────
    html = render_dashboard(data)

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(html)
    except OSError as exc:
        print(f"ABORT: could not write {OUTPUT_FILE}: {exc}", file=sys.stderr)
        sys.exit(1)

    # Post-generation verification
    with open(OUTPUT_FILE, encoding="utf-8") as f:
        content = f.read()
    if "%%WIKI_DATA%%" in content:
        print("ABORT: JSON injection failed — placeholder not replaced.", file=sys.stderr)
        sys.exit(1)

    # ── Usage summary ─────────────────────────────────────────────────────────
    stale_count = len(h2) if isinstance(h2, list) else 0
    contested_count = len(i2) if isinstance(i2, list) else 0

    print(f"Wiki dashboard written: {OUTPUT_FILE}")
    print(f"({total_pages} pages, {total_sources} sources, {stale_count} stale, {contested_count} contested)")
    print(f"Open with: open {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
