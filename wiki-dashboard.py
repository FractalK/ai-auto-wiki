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
    Phase 2 placeholder — implemented in Phase 2.
    Phase 1 uses inline placeholder HTML in main().
    """
    pass


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
    html_template = """<html><body>
<script>const WIKI_DATA = %%WIKI_DATA%%;</script>
<p>Data injected. Phase 1 complete.</p>
</body></html>"""

    json_str = json.dumps(data, ensure_ascii=False, default=str)
    html = html_template.replace("%%WIKI_DATA%%", json_str)

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
