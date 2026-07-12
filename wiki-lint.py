#!/usr/bin/env python3
# **Last Updated:** 06/05/2026 21:49 EDT
"""
wiki-lint.py — Mechanical lint checks for the AI Effectiveness Wiki.

Run from the wiki repository root (the directory containing overview.md).

Usage:
    python3 wiki-lint.py [--verbose]

Output:
    raw/lint-findings.json  — structured findings for agent judgment pass
    stdout                  — human-readable summary

Exit codes:
    0 — completed (findings may exist)
    1 — fatal error (not run from wiki root, or findings file unwritable)

Environmental assumptions:
    - Python 3.6+ (f-strings, pathlib, datetime)
    - Standard library only — no external packages
    - Executed from the wiki repository root
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date, timedelta


# ─── Schema Constants ────────────────────────────────────────────────────────
# MAINTENANCE: Update these constants when the schema changes.
# See design/hybrid-lint-assessment.md Section 6 maintenance table.

# Credibility weights — CLAUDE.md Section 8 / OPERATIONS.md Section 11.1
# MAINTENANCE: Update if credibility tier weights change
CREDIBILITY_WEIGHTS = {
    "peer-reviewed": 3,
    "institutional": 2,
    "practitioner": 1,
    "community": 0,
}

# Support score decay — CLAUDE.md Section 6.1
# MAINTENANCE: Update DECAY_MULTIPLIER or DECAY_THRESHOLD_MONTHS if decay policy changes
DECAY_MULTIPLIER = 0.5
DECAY_THRESHOLD_MONTHS = 12

# Staleness thresholds — CLAUDE.md Section 5.2 / OPERATIONS.md Step L5
# MAINTENANCE: Update STALENESS_THRESHOLD_DAYS if 90-day window changes
STALENESS_THRESHOLD_DAYS = 90

# Nomination queue aging — OPERATIONS.md Step L1a
# MAINTENANCE: Update if nomination aging thresholds change (currently 90/180 days)
NOMINATION_STAGE1_DAYS = 90
NOMINATION_STAGE2_DAYS = 180

# Teaching Index completeness threshold — OPERATIONS.md Step L10
# MAINTENANCE: Update TEACHING_RATIO_THRESHOLD if 20% minimum changes
TEACHING_RATIO_THRESHOLD = 0.20

# Schema Signals aging — OPERATIONS.md Step L12d
# MAINTENANCE: Update SCHEMA_SIGNALS_AGE_DAYS if 60-day threshold changes
SCHEMA_SIGNALS_AGE_DAYS = 60

# Deferred ingest staleness — OPERATIONS.md Step L12b
# MAINTENANCE: Update DEFERRED_STALENESS_DAYS if 14-day threshold changes
DEFERRED_STALENESS_DAYS = 14

# Session stats count threshold — OPERATIONS.md Step L12a
# MAINTENANCE: Update SESSION_STATS_THRESHOLD if 50-entry threshold changes
SESSION_STATS_THRESHOLD = 50

# Contradiction override window — CLAUDE.md Section 8.4
# MAINTENANCE: Update OVERRIDE_WINDOW_DAYS if 7-day window changes
OVERRIDE_WINDOW_DAYS = 7

# Content directories — CLAUDE.md Section 2 directory tree
# MAINTENANCE: Add new content directories here when the schema adds them
CONTENT_DIRS = ["topics", "tools", "comparisons", "pitfalls", "sources", "teaching"]

# Teaching-relevant content directories (exclude sources and teaching from tagging checks)
TEACHING_CONTENT_DIRS = ["topics", "tools", "comparisons", "pitfalls"]

# Singleton files (excluded from orphan detection and other per-page checks)
SINGLETON_FILES = {
    "index.md", "overview.md", "log.md", "teaching-index.md",
    "wiki-lessons-learned.md", "CLAUDE.md", "OPERATIONS.md",
    "EXTRACTION-SKILL.md", "TAGGING-SKILL.md", "CONTRADICTION-SKILL.md",
}

# Skill files for L14 checks
SKILL_FILES = ["EXTRACTION-SKILL.md", "TAGGING-SKILL.md", "CONTRADICTION-SKILL.md"]

# Controlled vocabularies — CLAUDE.md Sections 7.1 and 7.2 / vocabulary.json (DM-127)
VOCABULARY_FILE = "vocabulary.json"

# Metric canonicalization — structured-data extraction (BL-W-02, DM-128)
# MAINTENANCE: generic suffix tokens are stripped from the end of a metric
# name only when at least one token remains afterward (the one-token-
# remaining guard — spec 4.3.1). Do not add tokens here that are themselves
# meaningful metric names.
METRIC_GENERIC_SUFFIXES = {
    "accuracy",
    "score",
    "scores",
    "benchmark",
    "performance",
    "result",
    "results",
    "rate",
}

# MAINTENANCE: canonical-form -> canonical-form rewrites for known
# cross-naming variants of the same metric. Empty at v1; entries are added
# from operational experience (L20 "alias candidates" informational finding,
# spec Section 6 failure mode F3). Single consumer today (L19/L20) — do not
# externalize to a data file unless a second consumer appears (the BL-W-01
# vocabulary.json precedent applies at two-plus consumers, not one).
METRIC_ALIASES = {}

# Value/unit parsing — structured-data extraction (BL-W-02, DM-128)
# MAINTENANCE: add new unit tokens here as new metric types are tracked in
# Data Records tables. Units not in this set parse as unrecognized (value
# still extracted; unit is None; the pair is treated as non-comparable
# wherever unit membership is required).
UNIT_TOKENS = {
    "%",
    "pp",
    "ms",
    "s",
    "sec",
    "seconds",
    "min",
    "tokens",
    "tok/s",
    "tokens/s",
    "$",
    "$/m",
    "$/1m",
    "x",
}

# MAINTENANCE: cross-naming normalization applied after a raw unit is
# matched against UNIT_TOKENS. "ms" is deliberately absent here — it is
# handled specially in parse_value() because converting it also rescales
# the numeric value (divide by 1000), not just the label.
UNIT_CONVERSIONS = {
    "sec": "s",
    "seconds": "s",
    "$/1m": "$/m",
}

# Divergence test thresholds — CLAUDE.md Section 6.6 / spec 4.3.3 (DM-128)
# MAINTENANCE: tuned exclusively via the spec Section 4.6 precision
# procedure — raise CLAIM_SIM_THRESHOLD first (0.4 -> 0.5), then
# REL_DIVERGENCE (0.02 -> 0.05), one change per lint run, re-measuring
# precision after each. Do not hand-tune these outside that procedure.
REL_DIVERGENCE = 0.02
ABS_DIVERGENCE_FLOOR = 0.1

# Class 1 (KC<->KC) entity-guard similarity threshold — spec 4.3.5
CLAIM_SIM_THRESHOLD = 0.4

# Class 3 (DR<->DR) conditions-comparability threshold — spec 4.3.6
CONDITIONS_SIM_THRESHOLD = 0.5

# Pre-screen candidate ceiling per lint run — spec 4.6
# MAINTENANCE: overflow candidates are deferred (stateless re-derivation on
# the next run), never dropped. Do not raise this to suppress a volume
# spike — that is what the precision/tuning procedure and the V-3 >50
# pre-ceiling pause are for.
MAX_PRESCREEN_CANDIDATES = 10


def load_vocabulary():
    """Load and validate vocabulary.json; exit fatally on any defect.

    Returns the parsed dict. Fail-fast rationale: an absent or malformed
    vocabulary file must never degrade into an empty allowlist that either
    flags every page (noise) or passes every value (silent schema erosion).

    Usage:
        VOCABULARY = load_vocabulary()
    """
    if not os.path.exists(VOCABULARY_FILE):
        sys.exit(f"FATAL: {VOCABULARY_FILE} not found at repo root. "
                 "It is the controlled-vocabulary source of truth (DM-127).")
    with open(VOCABULARY_FILE, encoding="utf-8") as f:
        try:
            vocab = json.load(f)
        except json.JSONDecodeError as exc:
            sys.exit(f"FATAL: {VOCABULARY_FILE} is not valid JSON: {exc}")
    for key in ("competency_domains", "professional_contexts"):
        entries = vocab.get(key)
        if not isinstance(entries, list) or not entries:
            sys.exit(f"FATAL: {VOCABULARY_FILE} key '{key}' missing or empty.")
        for entry in entries:
            if not re.fullmatch(r"[a-z0-9-]+", entry.get("id", "")):
                sys.exit(f"FATAL: {VOCABULARY_FILE} '{key}' entry has a missing "
                         f"or non-kebab-case id: {entry!r}")
            if not entry.get("label"):
                sys.exit(f"FATAL: {VOCABULARY_FILE} entry {entry.get('id')} "
                         "is missing a label.")
    return vocab


VOCABULARY = load_vocabulary()
VALID_COMPETENCY_DOMAINS = {e["id"] for e in VOCABULARY["competency_domains"]}
VALID_PROFESSIONAL_CONTEXTS = {e["id"] for e in VOCABULARY["professional_contexts"]}

# Valid status values by page type — CLAUDE.md Sections 5.2–5.6
# MAINTENANCE: Update when status vocabulary changes for any page type
VALID_STATUS = {
    "topic": {"stub", "developing", "current", "stale"},
    "tool": {"active", "emerging", "deprecated", "discontinued", "stub"},
    "source": {"active", "retracted", "ingested-in-error"},
    "comparison": {"current", "stale", "superseded"},
    "pitfalls": {"current", "stale"},
    "teaching-brief": {"current", "stale"},
}

# Required frontmatter fields by page type — CLAUDE.md Sections 5.1–5.10
# MAINTENANCE: Update when required fields are added or removed from any page type
REQUIRED_FIELDS = {
    "topic": ["type", "title", "created", "updated", "summary", "status", "source_count"],
    "tool": ["type", "title", "created", "updated", "summary", "status", "source_count"],
    "source": ["type", "title", "created", "updated", "status", "source_type",
               "ingested_date", "credibility_tier", "extraction_depth"],
    "comparison": ["type", "title", "created", "updated", "comparison_type",
                   "entities_compared", "use_case", "status", "source_count"],
    "pitfalls": ["type", "title", "created", "updated", "parent_entity",
                 "parent_type", "status"],
    "teaching-brief": ["type", "title", "created", "updated", "status",
                       "query_date", "derived_from", "competency_domains",
                       "professional_contexts", "teaching_relevance", "last_reviewed"],
}

# Mandatory body sections for pitfalls pages — CLAUDE.md Section 5.6
PITFALLS_MANDATORY_SECTIONS = [
    "## Technical Limitations",
    "## Usage Antipatterns",
    "## Alignment and Safety Concerns",
]

# CTRD pattern — CLAUDE.md Section 8.3
# MAINTENANCE: Update if CTRD-NNN format changes
CTRD_PATTERN = re.compile(r'CTRD-(\d+)')

# Wikilink pattern — CLAUDE.md Section 4
WIKILINK_PATTERN = re.compile(r'\[\[([^\]]+)\]\]')

# Key Claims table header pattern
KEY_CLAIMS_HEADER = re.compile(r'\|\s*Claim\s*\|\s*Source\s*\|\s*Date\s*\|\s*Status\s*\|\s*Support Score\s*\|\s*Decay Exempt\s*\|', re.IGNORECASE)

# Status-content thresholds for G5 consistency check
G5_STUB_MAX_CLAIMS = 3          # stub status suggests ≤3 Key Claims
G5_STUB_MAX_WORDS = 500         # stub status suggests <500 words prose
G5_CURRENT_MIN_CLAIMS = 3       # current status requires at least 3 Key Claims

# Script version — update when publishing new releases
SCRIPT_VERSION = "1.0.0"

TODAY = date.today()


# ─── Frontmatter Parser ───────────────────────────────────────────────────────

def _parse_scalar(val):
    """Convert a raw YAML scalar string to its Python type."""
    if val == "true":
        return True
    if val == "false":
        return False
    if val in ("null", "~", ""):
        return None
    # ISO date YYYY-MM-DD
    if re.match(r'^\d{4}-\d{2}-\d{2}$', val):
        try:
            return date.fromisoformat(val)
        except ValueError:
            pass
    # ISO date-time (truncate to date)
    m = re.match(r'^(\d{4}-\d{2}-\d{2})T', val)
    if m:
        try:
            return date.fromisoformat(m.group(1))
        except ValueError:
            pass
    # Integer
    if re.match(r'^\d+$', val):
        return int(val)
    return val


def parse_frontmatter(text):
    """
    Parse YAML frontmatter delimited by --- markers.

    Handles: scalars, booleans, integers, ISO dates, block lists (string items
    and dict items), and quoted wikilinks ("[[slug]]").

    Returns (frontmatter_dict, body_text).
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
    i = 0
    current_key = None
    current_list = None       # list being accumulated (string items)
    current_dict_list = None  # list of dicts being accumulated
    current_dict = None       # current dict within a dict-list

    while i < len(lines):
        line = lines[i]

        # Skip blank lines (they don't reset list context — only a new top-level key does)
        if not line.strip():
            i += 1
            continue

        # List item with dict-style sub-key: "  - key: value" or "  - key: " (start of dict)
        dict_list_start = re.match(r'^[ \t]+-[ \t]+([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)', line)
        # Continuation of dict item: "    key: value" (no leading dash)
        dict_continuation = re.match(r'^[ \t]{4}([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)', line)
        # Simple list item: "  - value" (no key:value pattern after dash)
        simple_list_item = re.match(r'^[ \t]+-[ \t]+(.*)', line)
        # Top-level key: "key: value" or "key:"
        top_key = re.match(r'^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)', line)

        if dict_list_start and current_key is not None:
            # New dict item in a dict-list
            sub_key = dict_list_start.group(1)
            sub_val = dict_list_start.group(2).strip().strip('"')
            current_dict = {sub_key: _parse_scalar(sub_val)}
            if current_dict_list is None:
                current_dict_list = []
                fm[current_key] = current_dict_list
                current_list = None
            current_dict_list.append(current_dict)
            i += 1
            continue

        if dict_continuation and current_dict is not None:
            # Continuation key-value inside a dict item
            sub_key = dict_continuation.group(1)
            sub_val = dict_continuation.group(2).strip().strip('"')
            current_dict[sub_key] = _parse_scalar(sub_val)
            i += 1
            continue

        if simple_list_item and current_key is not None and current_dict is None:
            # Check if this could be a dict-list item (doesn't match dict pattern above)
            item_val = simple_list_item.group(1).strip().strip('"')
            if current_list is None:
                current_list = []
                fm[current_key] = current_list
                current_dict_list = None
            current_list.append(_parse_scalar(item_val))
            i += 1
            continue

        if top_key:
            # New top-level key resets all list/dict context
            current_key = top_key.group(1)
            raw_val = top_key.group(2).strip().strip('"')
            current_list = None
            current_dict_list = None
            current_dict = None

            if raw_val == "":
                # Value will follow as block list or multi-line — set up for collection
                fm[current_key] = None  # placeholder, overwritten when items arrive
            else:
                fm[current_key] = _parse_scalar(raw_val)
            i += 1
            continue

        # Line doesn't match any pattern — reset dict context (not list context)
        current_dict = None
        i += 1

    return fm, body


# ─── Markdown Table Parser ────────────────────────────────────────────────────

def parse_markdown_table(text, section_header="## Key Claims"):
    """
    Extract rows from a markdown pipe-table under the given section header.

    Returns list of dicts keyed by column headers (lowercased, spaces→underscores).
    Returns [] if the section or table is not found.
    """
    if section_header not in text:
        return []

    start = text.find(section_header)
    section_text = text[start + len(section_header):]

    # Find the next H2 section to bound the search
    next_h2 = re.search(r'\n## ', section_text)
    if next_h2:
        section_text = section_text[:next_h2.start()]

    rows = []
    headers = None
    for line in section_text.split("\n"):
        line = line.strip()
        if not line.startswith("|"):
            continue
        # Skip separator rows (|---|---|...)
        if re.match(r'^\|[-| :]+\|$', line):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if headers is None:
            headers = [h.lower().replace(" ", "_") for h in cells]
            continue
        if len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))

    return rows


def parse_data_records_table(text):
    """
    Extract rows from a ## Data Records table.

    Returns list of dicts with keys: metric, value, conditions, measurement_date, source, status
    Returns [] if the section is not found.
    """
    return parse_markdown_table(text, "## Data Records")


# ─── Wikilink Utilities ───────────────────────────────────────────────────────

def extract_wikilinks(text):
    """Return all wikilink targets found in text as a list of strings."""
    return [m.group(1) for m in WIKILINK_PATTERN.finditer(text)]


def wikilink_to_slug(target):
    """
    Convert a wikilink target to its slug form.

    Handles:
    - "topics/some-page" -> "some-page" (strip directory prefix)
    - "some-page" -> "some-page"
    - "some-page|Label" -> "some-page" (strip display label)
    - "some-page [derived]" -> "some-page" (strip annotations)
    """
    # Strip display label
    target = target.split("|")[0].strip()
    # Strip path prefix
    if "/" in target:
        target = target.split("/")[-1]
    # Strip annotations like [derived], [minority view]
    target = re.sub(r'\s*\[.*?\]\s*$', '', target).strip()
    return target


def extract_source_slugs_from_claims(claims_rows):
    """
    Extract source slugs from Key Claims table rows.

    Handles multiple sources per row (comma-separated wikilinks),
    [derived] and [minority view] annotations.

    Returns list of (slug, is_minority_view) tuples.
    """
    results = []
    for row in claims_rows:
        source_cell = row.get("source", "")
        # Find all wikilinks in the source cell
        for m in WIKILINK_PATTERN.finditer(source_cell):
            raw_target = m.group(1)
            slug = wikilink_to_slug(raw_target)
            # Check if this specific wikilink has [minority view] annotation
            # by checking if [minority view] appears after the wikilink in the cell
            end_pos = m.end()
            remaining = source_cell[end_pos:end_pos + 30]
            is_minority = "[minority view]" in remaining
            results.append((slug, is_minority))
    return results


# ─── Date Utilities ───────────────────────────────────────────────────────────

def days_ago(d):
    """Return number of days between today and d (positive means d is in the past)."""
    if d is None:
        return None
    if isinstance(d, str):
        try:
            d = date.fromisoformat(d)
        except ValueError:
            return None
    return (TODAY - d).days


def months_ago(d):
    """Approximate months between today and d."""
    if d is None:
        return None
    days = days_ago(d)
    if days is None:
        return None
    return days / 30.44  # average days per month


def parse_ym_date(ym_str):
    """Parse YYYY-MM format to a date object (first day of month)."""
    if not ym_str:
        return None
    m = re.match(r'^(\d{4})-(\d{2})$', str(ym_str).strip())
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), 1)
        except ValueError:
            pass
    # Try full ISO date
    try:
        return date.fromisoformat(str(ym_str).strip())
    except ValueError:
        return None


# ─── Structured-Data Extraction — Normalization Utilities (BL-W-02, DM-128) ──
# Pure functions backing L19 (extraction/serialization) and L20 (pre-screen).
# See spec sections 4.3.1-4.3.6. Wiring into check_L19_*/check_L20_* happens
# separately; these functions have no side effects and do no I/O.

_METRIC_SPLIT_RE = re.compile(r"[^a-z0-9]+")

_NUMBER_TOKEN = r"[+-]?\d[\d,]*(?:\.\d+)?"
_RANGE_SPLIT_RE = re.compile(r"\s*(?:-|–|—|\bto\b)\s*", re.IGNORECASE)
_MULTIPLIER_RE = re.compile(r"^([KkMmBb])\b")
_MULTIPLIERS = {"k": 1e3, "m": 1e6, "b": 1e9}
_CURRENCY_PREFIX_RE = re.compile(r"^\\?\$")


def canonicalize_metric(raw):
    """
    Canonicalize a metric name to a stable slug for cross-page matching.

    Lowercases, collapses non-alphanumeric runs to single hyphens, strips
    trailing generic-suffix tokens (METRIC_GENERIC_SUFFIXES) one at a time
    unless doing so would remove the last remaining token, then applies
    METRIC_ALIASES as a final rewrite.

    Examples:
        >>> canonicalize_metric("MMLU accuracy")
        'mmlu'
        >>> canonicalize_metric("SWE-bench Verified")
        'swe-bench-verified'
        >>> canonicalize_metric("Hallucination Rate")
        'hallucination'
        >>> canonicalize_metric("Accuracy")
        'accuracy'
    """
    if not raw:
        return ""
    s = _METRIC_SPLIT_RE.sub("-", raw.strip().lower()).strip("-")
    tokens = s.split("-") if s else []
    while len(tokens) > 1 and tokens[-1] in METRIC_GENERIC_SUFFIXES:
        tokens = tokens[:-1]
    canonical = "-".join(tokens)
    return METRIC_ALIASES.get(canonical, canonical)


def _extract_currency_prefix(s):
    """Strip a leading escaped (\\$) or bare ($) currency sign from s."""
    m = _CURRENCY_PREFIX_RE.match(s)
    if m:
        return True, s[m.end() :]
    return False, s


def _extract_number_and_suffix(rest):
    """
    Parse a leading number (with optional K/M/B multiplier already applied)
    from `rest`. Returns (numeric, suffix) or (None, "") if no number found.
    """
    rest = rest.strip()
    m = re.match(rf"({_NUMBER_TOKEN})\s*(.*)$", rest)
    if not m:
        return None, ""
    num_str, suffix = m.group(1), m.group(2).strip()
    try:
        numeric = float(num_str.replace(",", ""))
    except ValueError:
        return None, ""
    mult_match = _MULTIPLIER_RE.match(suffix)
    if mult_match:
        numeric *= _MULTIPLIERS[mult_match.group(1).lower()]
        suffix = suffix[mult_match.end() :].strip()
    return numeric, suffix


def _normalize_suffix_unit(is_currency, suffix):
    """Build and validate a unit string from a currency flag and suffix text."""
    suffix_norm = suffix.strip().lower()
    if is_currency:
        if not suffix_norm:
            unit = "$"
        elif suffix_norm in ("/m", "/1m"):
            unit = "$" + suffix_norm
        else:
            return None
    else:
        if not suffix_norm:
            return None
        unit = suffix_norm
    if unit not in UNIT_TOKENS:
        return None
    return UNIT_CONVERSIONS.get(unit, unit)


def parse_value(raw):
    """
    Parse a Data Records / Key Claim value cell into (numeric, numeric_high, unit).

    Handles escaped/bare currency prefixes, K/M/B multipliers, ranges
    ("1.2-1.5s", "100 to 200 ms"), and the fixed UNIT_TOKENS vocabulary.
    "ms" values are converted to seconds (numeric / 1000) so all times
    compare in the same unit. Returns (None, None, None) for non-parsable
    values or unrecognized units.

    Examples:
        >>> parse_value("\\\\$15")
        (15.0, None, '$')
        >>> parse_value("1.2M")
        (1200000.0, None, None)
        >>> parse_value("87.5%")
        (87.5, None, '%')
        >>> parse_value("230ms")
        (0.23, None, 's')
        >>> parse_value("1.2-1.5s")
        (1.2, 1.5, 's')
        >>> parse_value("supported")
        (None, None, None)
    """
    if not raw or not raw.strip():
        return None, None, None
    raw = raw.strip()

    parts = _RANGE_SPLIT_RE.split(raw, maxsplit=1)
    if len(parts) == 2 and parts[0].strip() and parts[1].strip():
        low_currency, low_rest = _extract_currency_prefix(parts[0].strip())
        high_currency, high_rest = _extract_currency_prefix(parts[1].strip())
        low_num, low_suffix = _extract_number_and_suffix(low_rest)
        high_num, high_suffix = _extract_number_and_suffix(high_rest)
        if low_num is None or high_num is None:
            return None, None, None
        is_currency = low_currency or high_currency
        suffix = high_suffix if high_suffix else low_suffix
        unit = _normalize_suffix_unit(is_currency, suffix)
        if suffix.lower() == "ms" and not is_currency:
            low_num, high_num = low_num / 1000.0, high_num / 1000.0
            unit = "s"
        if low_num > high_num:
            low_num, high_num = high_num, low_num
        return low_num, high_num, unit

    is_currency, rest = _extract_currency_prefix(raw)
    numeric, suffix = _extract_number_and_suffix(rest)
    if numeric is None:
        return None, None, None
    unit = _normalize_suffix_unit(is_currency, suffix)
    if suffix.lower() == "ms" and not is_currency:
        numeric = numeric / 1000.0
        unit = "s"
    return numeric, None, unit


def divergence(a_low, a_high, unit_a, b_low, b_high, unit_b):
    """
    Determine whether two comparable values/ranges diverge (spec 4.3.3).

    Returns True if divergent, False if comparable but not divergent, or
    None if the pair is not comparable (a missing value or differing
    normalized units). Divergence requires BOTH the relative difference to
    exceed REL_DIVERGENCE AND the absolute difference to exceed
    ABS_DIVERGENCE_FLOOR, measured between the nearest endpoints of the two
    intervals (point values are treated as zero-width intervals).

    Examples:
        >>> divergence(87.5, None, "%", 82.0, None, "%")
        True
        >>> divergence(87.5, None, "%", 87.4, None, "%")
        False
        >>> divergence(50.0, None, "%", 15.0, None, "tok/s") is None
        True
        >>> divergence(10, 20, "%", 30, 40, "%")
        True
        >>> divergence(10, 20, "%", 15, 25, "%")
        False
        >>> divergence(90, None, "%", 80, 95, "%")
        False
    """
    if unit_a is None or unit_b is None or a_low is None or b_low is None:
        return None
    if unit_a != unit_b:
        return None

    a_hi = a_high if a_high is not None else a_low
    b_hi = b_high if b_high is not None else b_low

    gap_ref = _interval_gap_and_ref(a_low, a_hi, b_low, b_hi)
    if gap_ref is None:
        return False
    gap, ref = gap_ref

    rel = (gap / ref) if ref != 0 else float("inf")
    return rel > REL_DIVERGENCE and gap > ABS_DIVERGENCE_FLOOR


def _interval_gap_and_ref(a_low, a_hi, b_low, b_hi):
    """Return (gap, ref) between two intervals, or None if they overlap/touch."""
    if a_low <= b_hi and b_low <= a_hi:
        return None
    if a_hi < b_low:
        return b_low - a_hi, max(abs(a_hi), abs(b_low))
    return a_low - b_hi, max(abs(a_low), abs(b_hi))


def relative_divergence(a_low, a_high, unit_a, b_low, b_high, unit_b):
    """
    Return the relative divergence magnitude (gap/ref) for a comparable,
    divergent pair — the same computation divergence() uses internally to
    decide True/False — or None if the pair is non-comparable or not
    divergent. Used by L20 to rank pre-screen candidates (spec 4.6);
    divergence() itself only reports True/False/None.

    Examples:
        >>> relative_divergence(87.5, None, "%", 82.0, None, "%")
        0.06285714285714286
        >>> relative_divergence(87.5, None, "%", 87.4, None, "%") is None
        True
    """
    if not divergence(a_low, a_high, unit_a, b_low, b_high, unit_b):
        return None
    a_hi = a_high if a_high is not None else a_low
    b_hi = b_high if b_high is not None else b_low
    gap, ref = _interval_gap_and_ref(a_low, a_hi, b_low, b_hi)
    return gap / ref if ref != 0 else float("inf")


# Stopwords for claim_similarity's Jaccard comparison — deliberately includes
# generic assertion verbs ("scores", "achieves") that would otherwise inflate
# overlap between claims about different entities and defeat the entity
# guard (spec 4.3.5).
_CLAIM_SIM_STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "on",
    "in",
    "at",
    "of",
    "with",
    "for",
    "to",
    "is",
    "are",
    "was",
    "were",
    "its",
    "it",
    "that",
    "this",
    "which",
    "has",
    "have",
    "had",
    "under",
    "than",
    "compared",
    "vs",
    "versus",
    "scores",
    "score",
    "scored",
    "achieves",
    "achieved",
    "reaches",
    "reached",
    "shows",
    "showed",
    "reports",
    "reported",
    "measured",
    "measures",
    "leads",
    "leading",
}

_WORD_RE = re.compile(r"[a-z][a-z0-9/.\-]*")


def _content_tokens(text, metric_terms=()):
    """Lowercase content-token set: strips metric terms, units, numbers, stopwords."""
    metric_terms_norm = {m.lower() for m in metric_terms}
    tokens = set()
    for w in _WORD_RE.findall(text.lower()):
        if w in metric_terms_norm or w in UNIT_TOKENS or w in _CLAIM_SIM_STOPWORDS:
            continue
        tokens.add(w)
    return tokens


def claim_similarity(claim_a, claim_b, metric_terms=()):
    """
    Jaccard similarity between two claim texts after removing matched metric
    term(s), numeric/unit tokens, and stopwords (spec 4.3.5 — the entity
    guard for Class 1 KC<->KC matching).

    Examples:
        >>> claim_similarity(
        ...     "GPT-4o scores 86% on MMLU",
        ...     "Claude Opus scores 88% on MMLU",
        ...     metric_terms=["MMLU"],
        ... ) < CLAIM_SIM_THRESHOLD
        True
        >>> claim_similarity(
        ...     "GPT-4o scores 86% on MMLU under zero-shot evaluation",
        ...     "GPT-4o achieves 82% on MMLU in zero-shot evaluation",
        ...     metric_terms=["MMLU"],
        ... ) >= CLAIM_SIM_THRESHOLD
        True
    """
    a = _content_tokens(claim_a, metric_terms)
    b = _content_tokens(claim_b, metric_terms)
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def conditions_similarity(tokens_a, tokens_b):
    """
    Jaccard similarity between two already-tokenized Conditions cells
    (spec 4.3.6 — the Class 3 conditions-comparability gate). Two empty
    token sets compare as fully similar; one empty and one non-empty
    compares as fully dissimilar.

    Examples:
        >>> conditions_similarity(["zero-shot"], ["zero-shot", "standard"])
        0.5
        >>> conditions_similarity([], [])
        1.0
        >>> conditions_similarity([], ["zero-shot"])
        0.0
    """
    a, b = set(tokens_a), set(tokens_b)
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


# MAINTENANCE: stopwords dropped from Conditions-cell tokens (spec 4.2). Kept
# minimal and separate from _CLAIM_SIM_STOPWORDS — conditions text ("zero-shot,
# standard prompt") and claim prose serve different comparisons.
_CONDITIONS_STOPWORDS = {"a", "an", "the", "and", "or", "with", "in", "on", "of", "for"}


def _tokenize_conditions(raw):
    """
    Tokenize a Data Records Conditions cell: lowercase, split on commas,
    whitespace, and slashes; strip punctuation; drop stopwords (spec 4.2).

    Examples:
        >>> _tokenize_conditions("zero-shot, standard prompt")
        ['zero-shot', 'standard', 'prompt']
        >>> _tokenize_conditions("")
        []
    """
    if not raw:
        return []
    tokens = []
    for part in re.split(r"[,/\s]+", raw.lower()):
        cleaned = re.sub(r"[^a-z0-9\-]", "", part)
        if cleaned and cleaned not in _CONDITIONS_STOPWORDS:
            tokens.append(cleaned)
    return tokens


# Inline value scanner for Key Claim signature detection (spec 4.3.4).
# Requires a non-alphanumeric boundary on both sides so digits embedded in
# identifiers (e.g. the "4" in "gpt-4o") are not mistaken for a value. The
# second lookbehind additionally blocks a hyphen-attached trailing digit
# (e.g. the "2" in "ARC-AGI-2") — a plain 1-char boundary check doesn't see
# past the hyphen to the letter before it.
_INLINE_VALUE_RE = re.compile(
    r"(?<![A-Za-z0-9])(?<![A-Za-z0-9]-)(?:\\\$|\$)?[+-]?\d[\d,]*(?:\.\d+)?"
    r"(?:%|pp|ms|sec|seconds|min|tokens/s|tok/s|tokens|x)?(?![A-Za-z0-9])"
)

_METRIC_WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9\-]*")

# Matches the gap text between a value and a metric name in "VALUE on
# METRIC" / "VALUE at METRIC" / "VALUE in METRIC" phrasing — used by
# detect_claim_signatures as the strongest (unambiguous) association signal.
_VALUE_METRIC_CONNECTOR_RE = re.compile(r"^\s+(?:on|at|in)\s+$")


def _extract_inline_values(text):
    """
    Extract parsable numeric values (with optional unit) from claim prose,
    via parse_value — reused, not reimplemented (spec 4.3.2/4.3.4).

    Examples:
        >>> _extract_inline_values("GPT-4o scores 86% on MMLU")
        [{'numeric': 86.0, 'unit': '%', 'raw': '86%'}]
        >>> _extract_inline_values("No numbers here")
        []
    """
    values = []
    seen = set()
    for m in _INLINE_VALUE_RE.finditer(text):
        raw = m.group(0)
        if raw in seen:
            continue
        numeric, _high, unit = parse_value(raw)
        if numeric is None:
            continue
        seen.add(raw)
        values.append({"numeric": numeric, "unit": unit, "raw": raw})
    return values


def detect_claim_signatures(claim_text, metric_universe):
    """
    Detect quantitative-claim signatures (spec 4.3.4): a claim acquires one
    signature per metric in `metric_universe` whose canonical form matches
    an n-gram (<=4 tokens) of the claim text, provided the claim text also
    contains at least one parsable value. Returns a list of signature dicts
    (empty if no value is present or no metric matches).

    A claim citing several metrics in one sentence must not let one metric's
    value leak into another's signature. This wiki mixes several phrasings
    ("80.8% on SWE-bench Verified", "GPQA Diamond 89.9%", "SEC-bench Pro
    (69.8% vs 63.1%)") — no single ordering rule fits all of them. Each
    matched metric is paired with: (1) a value connected to it by an
    explicit "on"/"at"/"in" bridge ("VALUE on METRIC"), if one exists —
    the strongest, unambiguous signal; otherwise (2) the nearest value by
    plain character distance, in either direction. This is a mechanical
    proxy, not a semantic parse, and is expected to occasionally misattribute
    a value in unusual phrasings — CONTRADICTION-SKILL.md's existence check
    (Section 1.4) and the Section 4.6 precision-tuning procedure are the
    intended backstops, not a perfect parser.

    Examples:
        >>> detect_claim_signatures("GPT-4o scores 86% on MMLU", {"mmlu"})
        [{'metric_canonical': 'mmlu', 'metric_matched_text': 'MMLU', 'values': [{'numeric': 86.0, 'unit': '%', 'raw': '86%'}]}]
        >>> detect_claim_signatures("MMLU is a benchmark", {"mmlu"})
        []
        >>> sigs = detect_claim_signatures(
        ...     "80.8% on SWE-bench Verified, 68.8% on ARC-AGI-2, and 91.3% on GPQA Diamond",
        ...     {"swe-bench-verified", "arc-agi-2", "gpqa-diamond"},
        ... )
        >>> {s["metric_canonical"]: s["values"][0]["raw"] for s in sigs} == {
        ...     "swe-bench-verified": "80.8%", "arc-agi-2": "68.8%", "gpqa-diamond": "91.3%",
        ... }
        True
        >>> sigs2 = detect_claim_signatures(
        ...     "GPQA Diamond 89.9%, and ARC-AGI-2 60.42% (high effort)",
        ...     {"gpqa-diamond", "arc-agi-2"},
        ... )
        >>> {s["metric_canonical"]: s["values"][0]["raw"] for s in sigs2} == {
        ...     "gpqa-diamond": "89.9%", "arc-agi-2": "60.42%",
        ... }
        True
    """
    value_spans = []  # (start, end, value_dict)
    for m in _INLINE_VALUE_RE.finditer(claim_text):
        raw = m.group(0)
        numeric, _high, unit = parse_value(raw)
        if numeric is None:
            continue
        value_spans.append(
            (m.start(), m.end(), {"numeric": numeric, "unit": unit, "raw": raw})
        )
    if not value_spans:
        return []

    word_matches = list(_METRIC_WORD_RE.finditer(claim_text))
    metric_spans = {}  # canonical -> (start, end, longest matched phrase)
    for n in range(1, 5):
        for i in range(len(word_matches) - n + 1):
            span_start = word_matches[i].start()
            span_end = word_matches[i + n - 1].end()
            phrase = claim_text[span_start:span_end]
            canonical = canonicalize_metric(phrase)
            if canonical and canonical in metric_universe:
                existing = metric_spans.get(canonical)
                if existing is None or (span_end - span_start) > (
                    existing[1] - existing[0]
                ):
                    metric_spans[canonical] = (span_start, span_end, phrase)
    if not metric_spans:
        return []

    def _nearest_value(m_start, m_end):
        for vs in value_spans:
            v_start, v_end, _ = vs
            if v_end <= m_start and _VALUE_METRIC_CONNECTOR_RE.match(
                claim_text[v_end:m_start]
            ):
                return vs

        def _dist(vs):
            v_start, v_end, _ = vs
            if v_end <= m_start:
                return m_start - v_end
            if v_start >= m_end:
                return v_start - m_end
            return 0

        return min(value_spans, key=_dist)

    signatures = []
    for canonical, (m_start, m_end, matched_text) in metric_spans.items():
        nearest = _nearest_value(m_start, m_end)
        signatures.append(
            {
                "metric_canonical": canonical,
                "metric_matched_text": matched_text,
                "values": [nearest[2]],
            }
        )
    return signatures


def _atomic_write_json(path, obj):
    """Write JSON to `path` atomically: temp file in the same directory, then os.replace."""
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, default=str)
    os.replace(tmp_path, path)


# ─── Findings Management ─────────────────────────────────────────────────────

findings = []
agent_review = []


def add_finding(step, ftype, page, description, data=None, recommended=None):
    """Append a finding to the findings list."""
    findings.append({
        "step": step,
        "type": ftype,
        "page": page,
        "description": description,
        "data": data or {},
        "recommended": recommended,
    })


def add_agent_review(step, review_type, page, description, **kwargs):
    """Append an agent-review item."""
    item = {
        "step": step,
        "review_type": review_type,
        "page": page,
        "description": description,
    }
    item.update(kwargs)
    agent_review.append(item)


# ─── Valid Slug Set ───────────────────────────────────────────────────────────

def build_valid_slug_set():
    """
    Build the set of all valid page slugs from the filesystem.

    Returns a set of slug strings (filename without .md extension).
    Also returns a dict mapping slug -> relative path for reference.
    """
    slugs = set()
    slug_to_path = {}
    for d in CONTENT_DIRS:
        if not os.path.isdir(d):
            continue
        for fname in os.listdir(d):
            if fname.endswith(".md"):
                slug = fname[:-3]
                slugs.add(slug)
                slug_to_path[slug] = os.path.join(d, fname)
    # Also add singleton slugs for wikilink resolution
    for fname in SINGLETON_FILES:
        slug = fname.replace(".md", "")
        slugs.add(slug)
    return slugs, slug_to_path


# ─── Index.md Parser ─────────────────────────────────────────────────────────

def parse_index_entries(index_text):
    """
    Extract page slugs from index.md.

    Returns dict: {"topics": [...slugs...], "tools": [...], ...}
    Also returns flat set of all slugs.
    """
    entries_by_type = defaultdict(list)
    all_slugs = set()

    current_section = None
    section_map = {
        "## Topics": "topics",
        "## Tools": "tools",
        "## Sources": "sources",
        "## Comparisons": "comparisons",
        "## Pitfalls": "pitfalls",
        "## Teaching": "teaching",
    }

    for line in index_text.split("\n"):
        line = line.strip()
        if line in section_map:
            current_section = section_map[line]
            continue
        if line.startswith("## "):
            current_section = None
            continue
        if current_section and line.startswith("- [["):
            m = WIKILINK_PATTERN.search(line)
            if m:
                raw = m.group(1)
                # Strip directory prefix and display labels
                slug = wikilink_to_slug(raw)
                entries_by_type[current_section].append(slug)
                all_slugs.add(slug)

    return dict(entries_by_type), all_slugs


# ─── Prose Word Count ─────────────────────────────────────────────────────────

def count_prose_words(body):
    """
    Count words in prose body, excluding frontmatter (already stripped),
    Key Claims table, Data Records table, section headers, and code blocks.
    """
    lines = body.split("\n")
    in_code_block = False
    in_table = False
    word_count = 0
    in_key_claims = False
    in_data_records = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if stripped.startswith("#"):
            if "Key Claims" in stripped:
                in_key_claims = True
                in_data_records = False
            elif "Data Records" in stripped:
                in_data_records = True
                in_key_claims = False
            elif stripped.startswith("## "):
                in_key_claims = False
                in_data_records = False
            continue
        if stripped.startswith("|"):
            continue  # Skip table rows entirely
        if in_key_claims or in_data_records:
            continue

        words = len(stripped.split())
        word_count += words

    return word_count


def strip_non_prose(body):
    """
    Return only the prose lines from a page body, stripping structures that
    would contaminate term-frequency analysis.

    Excluded:
    - Section headers (# / ## / ###)
    - Key Claims table rows and content beneath the ## Key Claims heading
    - Data Records table rows and content beneath the ## Data Records heading
    - Teaching Notes section (## Teaching Notes through the next ## heading)
    - All markdown pipe-table rows (| … |) including separator rows
    - Fenced code blocks (``` … ```)

    Used by check_L7_concept_gaps to ensure only real prose is tokenized.
    """
    lines = body.split("\n")
    prose_lines = []
    in_code_block = False
    in_key_claims = False
    in_data_records = False
    in_teaching_notes = False

    for line in lines:
        stripped = line.strip()

        # Code block toggle
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Section heading — update state flags, always skip the heading line itself
        if stripped.startswith("#"):
            if "## " in stripped or stripped.startswith("## "):
                # Top-level section transitions reset all structural flags
                in_key_claims = False
                in_data_records = False
                in_teaching_notes = False
                if "Key Claims" in stripped:
                    in_key_claims = True
                elif "Data Records" in stripped:
                    in_data_records = True
                elif "Teaching Notes" in stripped:
                    in_teaching_notes = True
            # Always skip header lines
            continue

        # Skip content under structural sections
        if in_key_claims or in_data_records or in_teaching_notes:
            continue

        # Skip all table rows (pipe-delimited lines, including separator rows)
        if stripped.startswith("|"):
            continue

        prose_lines.append(line)

    return "\n".join(prose_lines)


# ─── Group A: Singleton Checks ────────────────────────────────────────────────

def check_L1_ctrd_signals(queue_text):
    """
    L1: Scan queue.md for CTRD-NNN:(override|confirm) signals.
    Returns dict mapping ctrd_id -> signal_type.
    """
    signals = {}
    pattern = re.compile(r'(CTRD-\d+):(override|confirm)', re.IGNORECASE)
    for m in pattern.finditer(queue_text):
        ctrd_id = m.group(1).upper()
        signal_type = m.group(2).lower()
        signals[ctrd_id] = signal_type
        add_finding(
            "L1", "informational", None,
            f"CTRD signal in queue.md: {ctrd_id}:{signal_type}",
            {"ctrd_id": ctrd_id, "signal_type": signal_type},
        )
    if not signals:
        add_finding("L1", "informational", None, "No CTRD signals found in queue.md.")
    return signals


def check_L1a_nomination_aging(queue_text):
    """
    L1a: Scan nominated and stale-nominated sections for aged items.
    Returns (stage1_items, stage2_items) for Phase 3 processing.
    """
    stage1 = []  # nominated items ≥90 days → move to stale-nominated
    stage2 = []  # stale-nominated items ≥180 days → delete

    nominated_section = False
    stale_section = False
    no_date_count = 0

    date_pattern = re.compile(r'nominated:\s*(\d{4}-\d{2}-\d{2})')

    for line in queue_text.split("\n"):
        stripped = line.strip()
        if stripped == "## [nominated]":
            nominated_section = True
            stale_section = False
            continue
        if stripped == "## [stale-nominated]":
            stale_section = True
            nominated_section = False
            continue
        if stripped.startswith("## ["):
            nominated_section = False
            stale_section = False
            continue

        if not stripped:
            continue

        if nominated_section or stale_section:
            m = date_pattern.search(stripped)
            if not m:
                no_date_count += 1
                continue
            nom_date = _parse_scalar(m.group(1))
            if not isinstance(nom_date, date):
                continue
            age = days_ago(nom_date)
            title = stripped.split("|")[0].strip()[:80]

            if nominated_section and age >= NOMINATION_STAGE2_DAYS:
                # In nominated but somehow very old — treat as stage2
                stage2.append({"title": title, "age_days": age, "source": "nominated"})
            elif nominated_section and age >= NOMINATION_STAGE1_DAYS:
                stage1.append({"title": title, "age_days": age})
                add_finding(
                    "L1a", "informational", None,
                    f"Nominated item aging to stale ({age} days): {title}",
                    {"title": title, "age_days": age, "stage": 1},
                )
            elif stale_section and age >= NOMINATION_STAGE2_DAYS:
                stage2.append({"title": title, "age_days": age, "source": "stale-nominated"})
                add_finding(
                    "L1a", "informational", None,
                    f"Stale nomination eligible for deletion ({age} days): {title}",
                    {"title": title, "age_days": age, "stage": 2},
                )

    if no_date_count > 0:
        add_finding(
            "L1a", "informational", None,
            f"{no_date_count} nomination(s) have no nominated_date — aging skipped.",
            {"no_date_count": no_date_count},
        )

    return stage1, stage2


def check_L2_and_G2_page_inventory(index_text, valid_slug_set, slug_to_path):
    """
    L2: Build page inventory from index.md.
    G2: Cross-check index.md entries against filesystem.
    Returns index_entries_by_type, index_slug_set.
    """
    entries_by_type, index_slugs = parse_index_entries(index_text)

    # Count by type
    counts = {k: len(v) for k, v in entries_by_type.items()}
    total_indexed = sum(counts.values())

    add_finding(
        "L2", "informational", None,
        f"Page inventory from index.md: {total_indexed} total",
        {"counts_by_type": counts, "total": total_indexed},
    )

    # G2: pages on disk but absent from index.md
    content_slugs = set()
    for d in CONTENT_DIRS:
        if not os.path.isdir(d):
            continue
        for fname in os.listdir(d):
            if fname.endswith(".md"):
                content_slugs.add(fname[:-3])

    missing_from_index = content_slugs - index_slugs
    stale_in_index = index_slugs - content_slugs

    for slug in sorted(missing_from_index):
        add_finding(
            "G2", "informational", slug,
            f"Page on disk but absent from index.md: {slug}",
            {"slug": slug, "issue": "missing_from_index"},
        )

    for slug in sorted(stale_in_index):
        add_finding(
            "G2", "informational", slug,
            f"index.md entry has no corresponding file on disk: {slug}",
            {"slug": slug, "issue": "stale_index_entry"},
        )

    if not missing_from_index and not stale_in_index:
        add_finding("G2", "informational", None, "index.md ↔ filesystem parity: verified.")

    return entries_by_type, index_slugs


# ─── Group B: Per-Page Checks ─────────────────────────────────────────────────

def check_L4a_contradiction_expiry(fm, page_slug, ctrd_signals):
    """
    L4a: Check open_contradictions for expired override windows.
    Returns list of expired CTRD IDs.
    """
    expired = []
    open_contradictions = fm.get("open_contradictions")
    if not open_contradictions:
        return expired

    if not isinstance(open_contradictions, list):
        return expired

    for entry in open_contradictions:
        if not isinstance(entry, dict):
            continue
        ctrd_id = entry.get("id", "")
        if not ctrd_id:
            continue
        # Skip if a signal was found in queue.md for this ID
        if ctrd_id in ctrd_signals:
            continue
        window_closes = entry.get("override_window_closes")
        if isinstance(window_closes, date) and window_closes < TODAY:
            age = days_ago(window_closes)
            expired.append(ctrd_id)
            add_finding(
                "L4a", "auto-execute", page_slug,
                f"Contradiction flag expired: {ctrd_id} on {page_slug} (window closed {window_closes})",
                {
                    "ctrd_id": ctrd_id,
                    "page": page_slug,
                    "override_window_closes": str(window_closes),
                    "days_past_window": age,
                    "claim_summary": entry.get("claim_summary", ""),
                    "contesting_source": entry.get("contesting_source", ""),
                },
            )

    return expired


def check_L4b_open_contradictions(fm, page_slug, ctrd_signals):
    """
    L4b: Surface open contradictions within their override window.
    D-category: outputs to agent_review with recommended: null.
    """
    open_contradictions = fm.get("open_contradictions")
    if not open_contradictions or not isinstance(open_contradictions, list):
        return

    for entry in open_contradictions:
        if not isinstance(entry, dict):
            continue
        ctrd_id = entry.get("id", "")
        if not ctrd_id:
            continue
        if ctrd_id in ctrd_signals:
            continue
        window_closes = entry.get("override_window_closes")
        if isinstance(window_closes, date) and window_closes >= TODAY:
            days_remaining = (window_closes - TODAY).days
            add_agent_review(
                "L4b", "contradiction_recommendation", page_slug,
                f"Open contradiction {ctrd_id} on {page_slug}: review and set recommended value",
                ctrd_id=ctrd_id,
                claim_summary=entry.get("claim_summary", ""),
                contesting_source=entry.get("contesting_source", ""),
                flagged_date=str(entry.get("flagged_date", "")),
                override_window_closes=str(window_closes),
                days_remaining=days_remaining,
                path=entry.get("path", "human-review"),
                options=["A", "B", "C"],
                options_labels={
                    "A": "Confirm — apply resolution; update claim to reflect contesting source",
                    "B": "Override — retain prior claim; treat contesting source as minority view",
                    "C": "Skip — no action; override window continues running",
                },
                recommended=None,
            )


def check_L5_staleness(fm, page_slug, page_type, entity_pages_fm=None):
    """
    L5: Staleness check for Topic, Tool, Comparison, and Teaching-brief pages.
    entity_pages_fm: dict of slug -> fm for resolving entities_compared (Comparison)
    Returns downgrade_needed bool and relevant context.
    """
    if page_type not in ("topic", "tool", "comparison", "teaching-brief"):
        return False

    if page_type in ("topic", "tool"):
        status = fm.get("status", "")
        if status == "deprecated":
            return False
        last_assessed = fm.get("last_assessed")
        if last_assessed is None:
            return False
        age = days_ago(last_assessed)
        if age is None:
            return False
        if age > STALENESS_THRESHOLD_DAYS and status != "stale":
            add_finding(
                "L5", "auto-execute", page_slug,
                f"Page is stale: last_assessed {last_assessed} ({age} days ago) — downgrade to stale",
                {
                    "page": page_slug,
                    "page_type": page_type,
                    "last_assessed": str(last_assessed),
                    "age_days": age,
                    "current_status": status,
                    "action": "set_status_stale",
                },
                recommended="A",
            )
            return True
        if age > STALENESS_THRESHOLD_DAYS and status == "stale":
            add_finding(
                "L5", "informational", page_slug,
                f"Page already stale: last_assessed {last_assessed} ({age} days ago)",
                {"page": page_slug, "last_assessed": str(last_assessed), "age_days": age},
            )
        return False

    if page_type == "comparison":
        comp_updated = fm.get("updated")
        entities = fm.get("entities_compared", [])
        if not isinstance(entities, list):
            return False
        stale_trigger = None
        for entity_ref in entities:
            slug = wikilink_to_slug(str(entity_ref))
            if entity_pages_fm and slug in entity_pages_fm:
                efm = entity_pages_fm[slug]
                signal = efm.get("last_assessed") or efm.get("updated")
                if signal and comp_updated and isinstance(signal, date) and isinstance(comp_updated, date):
                    if signal > comp_updated:
                        stale_trigger = (slug, signal)
                        break

        if stale_trigger:
            current_status = fm.get("status", "")
            if current_status != "stale":
                add_finding(
                    "L5", "auto-execute", page_slug,
                    f"Comparison page stale: entity {stale_trigger[0]} last_assessed {stale_trigger[1]} "
                    f"is newer than comparison updated {comp_updated}",
                    {
                        "page": page_slug,
                        "trigger_entity": stale_trigger[0],
                        "entity_signal_date": str(stale_trigger[1]),
                        "comparison_updated": str(comp_updated),
                        "action": "set_status_stale",
                    },
                    recommended="A",
                )
                return True
        return False

    if page_type == "teaching-brief":
        last_reviewed = fm.get("last_reviewed")
        derived_from = fm.get("derived_from", [])
        if not isinstance(derived_from, list):
            return False

        stale_trigger = None
        for ref in derived_from:
            slug = wikilink_to_slug(str(ref))
            if entity_pages_fm and slug in entity_pages_fm:
                efm = entity_pages_fm[slug]
                const_assessed = efm.get("last_assessed")
                if (const_assessed and last_reviewed
                        and isinstance(const_assessed, date)
                        and isinstance(last_reviewed, date)
                        and const_assessed > last_reviewed):
                    stale_trigger = (slug, const_assessed)
                    break

        if stale_trigger:
            add_agent_review(
                "L5", "teaching_brief_recommendation", page_slug,
                f"Teaching-brief may be outdated: constituent {stale_trigger[0]} "
                f"last_assessed {stale_trigger[1]} > brief last_reviewed {last_reviewed}",
                constituent_slug=stale_trigger[0],
                constituent_last_assessed=str(stale_trigger[1]),
                brief_last_reviewed=str(last_reviewed) if last_reviewed else None,
                options=["A", "B", "C"],
                options_labels={
                    "A": "Regenerate — agent produces updated draft for review",
                    "B": "Mark as reviewed without changes — set last_reviewed to today",
                    "C": "Dismiss — leave status: stale for now",
                },
                recommended="A",
            )
            return True
        return False


def check_L5a_stale_upgrade(fm, page_slug, page_type):
    """
    L5a: For stale pages, check if both upgrade conditions are met.
    Condition (a): last_assessed within 90 days.
    Condition (b): no open contradictions.
    """
    if page_type not in ("topic", "tool"):
        return
    if fm.get("status") != "stale":
        return

    last_assessed = fm.get("last_assessed")
    open_contradictions = fm.get("open_contradictions")
    has_open = bool(open_contradictions and isinstance(open_contradictions, list)
                    and len(open_contradictions) > 0)

    if last_assessed is None:
        return

    age = days_ago(last_assessed)
    if age is None:
        return

    condition_a = age <= STALENESS_THRESHOLD_DAYS
    condition_b = not has_open

    if condition_a and condition_b:
        add_finding(
            "L5a", "forced-choice", page_slug,
            f"Stale page eligible for upgrade to current: {page_slug}",
            {
                "page": page_slug,
                "last_assessed": str(last_assessed),
                "age_days": age,
                "open_contradictions": 0,
                "options": {
                    "A": "Upgrade to current",
                    "B": "Skip — retain stale",
                },
            },
            recommended="A",
        )
    elif condition_a and not condition_b:
        add_finding(
            "L5a", "informational", page_slug,
            f"Stale page: last_assessed within 90 days but has open contradictions — cannot upgrade",
            {"page": page_slug, "condition_b_unmet": True},
        )
    elif not condition_a and condition_b:
        add_finding(
            "L5a", "informational", page_slug,
            f"Stale page: no open contradictions but last_assessed is {age} days ago — cannot upgrade",
            {"page": page_slug, "condition_a_unmet": True, "age_days": age},
        )


def check_L5b_teaching_notes_currency(fm, page_slug):
    """
    L5b: Check teaching notes currency (informational only).
    """
    if fm.get("teaching_relevance") is not True:
        return

    teaching_notes_reviewed = fm.get("teaching_notes_reviewed")
    last_assessed = fm.get("last_assessed")

    if teaching_notes_reviewed is None:
        if last_assessed is not None:
            add_finding(
                "L5b", "informational", page_slug,
                f"teaching_notes section missing — page is teaching-tagged but no notes have been written: {page_slug}",
                {"page": page_slug, "issue": "no_teaching_notes"},
            )
        return

    if not isinstance(teaching_notes_reviewed, date) or not isinstance(last_assessed, date):
        return

    gap = (last_assessed - teaching_notes_reviewed).days
    if gap > STALENESS_THRESHOLD_DAYS:
        add_finding(
            "L5b", "informational", page_slug,
            f"Teaching notes currency: teaching_notes_reviewed is {gap} days before last_assessed on {page_slug}",
            {
                "page": page_slug,
                "teaching_notes_reviewed": str(teaching_notes_reviewed),
                "last_assessed": str(last_assessed),
                "gap_days": gap,
            },
        )


def check_L5c_data_records_freshness(body, page_slug):
    """
    L5c: Check Data Records freshness (informational only).
    """
    rows = parse_data_records_table(body)
    if not rows:
        return

    current_dates = []
    for row in rows:
        if row.get("status", "").lower() == "current":
            mdate = parse_ym_date(row.get("measurement_date", ""))
            if mdate:
                current_dates.append(mdate)

    if not current_dates:
        return

    most_recent = max(current_dates)
    age = days_ago(most_recent)
    if age is not None and age > STALENESS_THRESHOLD_DAYS:
        add_finding(
            "L5c", "informational", page_slug,
            f"Data records may be stale on {page_slug}: last measurement {most_recent.strftime('%Y-%m')} ({age} days ago)",
            {
                "page": page_slug,
                "last_measurement": most_recent.strftime("%Y-%m"),
                "age_days": age,
            },
        )


def check_L8_pitfalls_maintenance(fm, body, page_slug):
    """
    L8: Check pitfalls page failure_mode_count and mandatory H2 sections.
    """
    if fm.get("type") != "pitfalls":
        return

    # Count H3 headings that have **Status:** on the next non-blank line
    lines = body.split("\n")
    h3_with_status = 0
    for idx, line in enumerate(lines):
        if line.strip().startswith("### "):
            # Look ahead for **Status:**
            for j in range(idx + 1, min(idx + 4, len(lines))):
                if lines[j].strip():
                    if lines[j].strip().startswith("**Status:**"):
                        h3_with_status += 1
                    break

    current_count = fm.get("failure_mode_count")

    if current_count is not None and isinstance(current_count, int):
        if h3_with_status != current_count:
            add_finding(
                "L8", "auto-execute", page_slug,
                f"failure_mode_count mismatch on {page_slug}: frontmatter={current_count}, actual={h3_with_status}",
                {
                    "page": page_slug,
                    "frontmatter_count": current_count,
                    "actual_count": h3_with_status,
                    "action": "update_failure_mode_count",
                },
                recommended="A",
            )

    # Check mandatory H2 sections
    for section in PITFALLS_MANDATORY_SECTIONS:
        if section not in body:
            add_finding(
                "L8", "informational", page_slug,
                f"Missing mandatory section on pitfalls page {page_slug}: {section}",
                {"page": page_slug, "missing_section": section},
            )


def check_L11_schema_conformance(fm, body, page_slug, page_type, claims_rows, last_lint_date):
    """
    L11: Schema conformance checks (mechanical criteria).
    D-category items (claim granularity candidates) go to agent_review.
    """
    if page_type not in ("topic", "tool"):
        return

    # Only check pages updated after last_lint
    updated = fm.get("updated")
    if last_lint_date and isinstance(updated, date) and isinstance(last_lint_date, date):
        if updated <= last_lint_date:
            return

    # Key Claims count
    if claims_rows is not None:
        claim_count = len(claims_rows)
        if claim_count < 3:
            add_finding(
                "L11", "informational", page_slug,
                f"Key Claims count below minimum: {page_slug} has {claim_count} claims (minimum 3)",
                {"page": page_slug, "claim_count": claim_count, "criterion": "key_claims_count_low"},
            )
        elif claim_count > 5:
            # Check skip conditions: deferred or overridden in frontmatter.
            cap_deferred = fm.get("claims_cap_deferred", 0)
            cap_override = fm.get("claims_cap_override", False)
            if cap_override:
                # Permanently overridden — informational only.
                add_finding(
                    "L11", "informational", page_slug,
                    f"Key Claims overcap on {page_slug}: {claim_count} claims (cap override active)",
                    {"page": page_slug, "claim_count": claim_count, "criterion": "key_claims_count_high_override"},
                )
            elif cap_deferred and int(cap_deferred) > 0:
                # Deferred — informational only; Phase 3 will decrement counter.
                add_finding(
                    "L11", "informational", page_slug,
                    f"Key Claims overcap on {page_slug}: {claim_count} claims (deferred, {cap_deferred} passes remaining)",
                    {"page": page_slug, "claim_count": claim_count, "criterion": "key_claims_count_high_deferred",
                     "cap_deferred": int(cap_deferred)},
                )
            else:
                # No skip condition — route to agent_review for consolidation candidate
                # identification and forced-choice promotion.
                # Serialise claims_rows for the agent: include claim text, source, date,
                # and status only (support score and decay_exempt not needed for consolidation).
                claims_summary = [
                    {
                        "claim": r.get("claim", ""),
                        "source": r.get("source", ""),
                        "date": r.get("date", ""),
                        "status": r.get("status", ""),
                    }
                    for r in claims_rows
                ]
                add_agent_review(
                    "L11", "key_claims_overcap", page_slug,
                    f"Key Claims overcap: {page_slug} has {claim_count} claims (cap: 5)",
                    claim_count=claim_count,
                    claims_summary=claims_summary,
                )

    # Prose length
    word_count = count_prose_words(body)
    if word_count > 1200:
        add_finding(
            "L11", "informational", page_slug,
            f"Prose length exceeds 1200 words on {page_slug}: {word_count} words",
            {"page": page_slug, "word_count": word_count, "criterion": "prose_length"},
        )

    # Required frontmatter
    required = REQUIRED_FIELDS.get(page_type, [])
    for field in required:
        if field not in fm or fm[field] is None:
            add_finding(
                "L11", "informational", page_slug,
                f"Missing required field '{field}' on {page_slug}",
                {"page": page_slug, "missing_field": field, "criterion": "required_frontmatter"},
            )

    # Summary field: single sentence check (heuristic)
    summary = fm.get("summary", "")
    if isinstance(summary, str) and summary:
        sentence_count = len(re.findall(r'[.!?](?:\s|$)', summary))
        if sentence_count > 1:
            add_finding(
                "L11", "informational", page_slug,
                f"Summary field may contain multiple sentences on {page_slug}",
                {"page": page_slug, "criterion": "summary_single_sentence"},
            )

    # Status vocabulary
    valid_statuses = VALID_STATUS.get(page_type, set())
    status = fm.get("status", "")
    if status and status not in valid_statuses:
        add_finding(
            "L11", "informational", page_slug,
            f"Invalid status '{status}' for {page_type} page {page_slug}",
            {"page": page_slug, "status": status, "criterion": "status_vocabulary"},
        )

    # Claim granularity candidates (D-category) — mechanical signals only
    if claims_rows:
        for row in claims_rows:
            claim_text = row.get("claim", "")
            issues = []
            if ";" in claim_text:
                issues.append("contains semicolon (may join multiple assertions)")
            if claim_text.endswith("?"):
                issues.append("ends with question mark (should be an assertion)")
            word_count_claim = len(claim_text.split())
            if word_count_claim < 6:
                issues.append(f"very short ({word_count_claim} words) — may be a topic label, not an assertion")

            if issues:
                add_agent_review(
                    "L11", "claim_granularity_review", page_slug,
                    f"Candidate claim granularity violation on {page_slug}: {'; '.join(issues)}",
                    claim_text=claim_text,
                    issues=issues,
                    source=row.get("source", ""),
                    status=row.get("status", ""),
                )


def check_L15_teaching_tagged_missing_fields(fm, page_slug, page_type):
    """
    L15: Teaching-tagged pages missing required tagging fields.
    """
    if fm.get("teaching_relevance") is not True:
        return
    if fm.get("status") in ("stub", "deprecated"):
        return
    if page_type == "teaching-brief":
        return

    missing = []
    competency_domains = fm.get("competency_domains")
    professional_contexts = fm.get("professional_contexts")

    if not competency_domains or (isinstance(competency_domains, list) and len(competency_domains) == 0):
        missing.append("competency_domains")
    if not professional_contexts or (isinstance(professional_contexts, list) and len(professional_contexts) == 0):
        missing.append("professional_contexts")

    if missing:
        add_finding(
            "L15", "forced-choice", page_slug,
            f"Teaching-tagged page missing required field(s): {page_slug} — missing: {', '.join(missing)}",
            {
                "page": page_slug,
                "page_type": page_type,
                "status": fm.get("status", ""),
                "missing_fields": missing,
                "options": {
                    "A": "Tag now — agent proposes domains/contexts; human confirms before writing",
                    "B": "Defer — page excluded from Teaching Index until manually tagged",
                },
            },
            recommended="A",
        )


def check_L17_vocabulary_conformance(fm, page_slug):
    """
    L17: page frontmatter vocabulary conformance (CLAUDE.md Sections 7.1-7.2, DM-127).

    Every value in a page's competency_domains or professional_contexts field
    must be a member of VALID_COMPETENCY_DOMAINS / VALID_PROFESSIONAL_CONTEXTS
    (loaded from vocabulary.json). This duplicates wiki-verify.sh check 14 on
    the Python side deliberately — verify is the operator-side guard, lint is
    the agent-session guard.
    """
    for field, valid_set in (
        ("competency_domains", VALID_COMPETENCY_DOMAINS),
        ("professional_contexts", VALID_PROFESSIONAL_CONTEXTS),
    ):
        values = fm.get(field)
        if not values:
            continue
        if isinstance(values, str):
            values = [values]

        for value in values:
            if value not in valid_set:
                add_finding(
                    "L17", "forced-choice", page_slug,
                    f"Invalid {field} value '{value}' on {page_slug}",
                    {
                        "page": page_slug,
                        "field": field,
                        "value": value,
                        "criterion": "vocabulary_conformance",
                        "options": {
                            "A": "Correct to a valid value — agent proposes replacement",
                            "B": "Operator supplies the correct value",
                            "C": "Remove the value",
                        },
                    },
                )


def check_G1_wikilink_integrity(text, page_slug, valid_slugs):
    """
    G1: Check all wikilinks in page text against valid slug set.
    Returns set of outbound slugs (for orphan detection).
    """
    outbound = set()
    for m in WIKILINK_PATTERN.finditer(text):
        raw = m.group(1)
        slug = wikilink_to_slug(raw)
        if not slug:
            continue
        outbound.add(slug)
        if slug not in valid_slugs:
            add_finding(
                "G1", "informational", page_slug,
                f"Broken wikilink [[{raw}]] on {page_slug}: target '{slug}' not found",
                {
                    "page": page_slug,
                    "raw_target": raw,
                    "slug": slug,
                    "issue": "broken_wikilink",
                },
            )
    return outbound


def check_G3_source_reference_integrity(claims_rows, page_slug, source_slugs):
    """
    G3: Verify Key Claims source wikilinks point to existing source pages.
    source_slugs: set of slugs in sources/ directory.
    """
    for row in claims_rows:
        source_cell = row.get("source", "")
        if not source_cell:
            continue
        # Skip [derived] claims
        if "[derived]" in source_cell:
            continue
        for m in WIKILINK_PATTERN.finditer(source_cell):
            raw = m.group(1)
            slug = wikilink_to_slug(raw)
            if not slug:
                continue
            if "[minority view]" in source_cell[m.end():m.end() + 20]:
                continue
            if slug not in source_slugs:
                add_finding(
                    "G3", "informational", page_slug,
                    f"Broken source reference [[{raw}]] in Key Claims on {page_slug}: "
                    f"no file in sources/",
                    {
                        "page": page_slug,
                        "source_slug": slug,
                        "claim_text": row.get("claim", "")[:100],
                        "issue": "missing_source_page",
                    },
                )


def check_G5_status_content_consistency(fm, body, page_slug, page_type, claims_rows):
    """
    G5: Flag status values that contradict content indicators.
    """
    if page_type not in ("topic", "tool"):
        return

    status = fm.get("status", "")
    last_assessed = fm.get("last_assessed")
    claim_count = len(claims_rows) if claims_rows else 0
    word_count = count_prose_words(body)

    if status == "stub" and claim_count > G5_STUB_MAX_CLAIMS:
        add_finding(
            "G5", "informational", page_slug,
            f"Status stub but has {claim_count} Key Claims (>{G5_STUB_MAX_CLAIMS}) on {page_slug}",
            {"page": page_slug, "status": status, "claim_count": claim_count, "issue": "stub_too_many_claims"},
        )
    if status == "stub" and word_count > G5_STUB_MAX_WORDS:
        add_finding(
            "G5", "informational", page_slug,
            f"Status stub but has {word_count} prose words (>{G5_STUB_MAX_WORDS}) on {page_slug}",
            {"page": page_slug, "status": status, "word_count": word_count, "issue": "stub_too_much_prose"},
        )
    if status == "current" and last_assessed is None:
        add_finding(
            "G5", "informational", page_slug,
            f"Status current but last_assessed is absent on {page_slug}",
            {"page": page_slug, "status": status, "issue": "current_no_last_assessed"},
        )
    if status == "current" and claim_count == 0:
        add_finding(
            "G5", "informational", page_slug,
            f"Status current but has 0 Key Claims on {page_slug}",
            {"page": page_slug, "status": status, "issue": "current_no_claims"},
        )


# ─── Group C: Cross-Page Computation ─────────────────────────────────────────

def build_source_info():
    """
    Read all source pages to collect credibility_tier and published_date.
    Returns dict: source_slug -> {"tier": str, "published": date|None}
    """
    info = {}
    if not os.path.isdir("sources"):
        return info
    for fname in os.listdir("sources"):
        if not fname.endswith(".md"):
            continue
        slug = fname[:-3]
        try:
            with open(os.path.join("sources", fname), encoding="utf-8") as f:
                text = f.read()
        except OSError:
            continue
        fm, _ = parse_frontmatter(text)
        tier = fm.get("credibility_tier", "")
        published = fm.get("published_date")
        info[slug] = {
            "tier": tier,
            "published": published if isinstance(published, date) else None,
            "status": fm.get("status", "active"),
        }
    return info


def compute_support_score(source_cell, decay_exempt, source_info):
    """
    Compute a Key Claim's support score from its Source cell text
    (CLAUDE.md Section 6.1). Shared by L3 (recalculation check) and L19
    (claims.json serialization) so support-score arithmetic has a single
    implementation.

    Returns (score, detail_lines): score is a float rounded to one decimal
    place; detail_lines describes each contributing/excluded source.
    """
    total_score = 0.0
    detail_lines = []

    for m in WIKILINK_PATTERN.finditer(source_cell):
        raw = m.group(1)
        slug = wikilink_to_slug(raw)
        # Check if [minority view] follows this wikilink
        tail = source_cell[m.end() : m.end() + 30]
        if "[minority view]" in tail:
            detail_lines.append(f"  {slug}: minority view — excluded")
            continue

        sinfo = source_info.get(slug, {})
        tier = sinfo.get("tier", "")
        weight = CREDIBILITY_WEIGHTS.get(tier, 0)
        pub_date = sinfo.get("published")

        # Apply decay if not exempt
        if not decay_exempt and pub_date:
            age_months = months_ago(pub_date)
            if age_months is not None and age_months > DECAY_THRESHOLD_MONTHS:
                weight *= DECAY_MULTIPLIER

        total_score += weight
        detail_lines.append(f"  {slug}: tier={tier}, weight={weight:.1f}, " f"pub={pub_date}")

    return round(total_score, 1), detail_lines


def check_L3_support_scores(page_claims, source_info, verbose):
    """
    L3: Recalculate support scores for every Key Claim on Topic and Tool pages.
    Reports differences. Informational only.
    """
    for page_slug, claims_rows in page_claims.items():
        for row in claims_rows:
            source_cell = row.get("source", "")
            status_cell = row.get("status", "")
            decay_exempt_val = row.get("decay_exempt", "false").strip().lower() == "true"
            current_score_str = row.get("support_score", "").strip()

            # Skip [derived] claims
            if "[derived]" in source_cell:
                continue

            computed, detail_lines = compute_support_score(
                source_cell, decay_exempt_val, source_info
            )

            if verbose:
                print(f"  [L3] {page_slug} claim '{row.get('claim','')[:50]}...' "
                      f"computed={computed}")
                for dl in detail_lines:
                    print(f"    {dl}")

            # Compare to table value
            try:
                table_score = float(current_score_str)
            except (ValueError, TypeError):
                table_score = None

            if table_score is not None and abs(computed - table_score) >= 0.05:
                add_finding(
                    "L3", "informational", page_slug,
                    f"Support score changed on {page_slug}: table={table_score}, "
                    f"computed={computed} (claim: '{row.get('claim','')[:60]}')",
                    {
                        "page": page_slug,
                        "claim_text": row.get("claim", ""),
                        "table_score": table_score,
                        "computed_score": computed,
                        "detail": detail_lines,
                    },
                )
            elif table_score is None and current_score_str not in ("", "derived"):
                add_finding(
                    "L3", "informational", page_slug,
                    f"Support score unparseable on {page_slug}: '{current_score_str}'",
                    {"page": page_slug, "raw_score": current_score_str},
                )


def check_L4c_and_G4_counters(open_contradictions_count, all_ctrd_ids,
                               overview_fm, total_indexed):
    """
    L4c: Reconcile open_contradictions counter.
    G4: Verify total_pages and last_contradiction_id in overview.md.
    """
    # L4c: open_contradictions
    overview_open = overview_fm.get("open_contradictions", 0) or 0
    if isinstance(overview_open, str):
        try:
            overview_open = int(overview_open)
        except ValueError:
            overview_open = 0

    diff = abs(open_contradictions_count - overview_open)
    if diff == 0:
        add_finding(
            "L4c", "informational", None,
            f"open_contradictions counter verified: {overview_open}",
            {"actual": open_contradictions_count, "overview": overview_open},
        )
    elif diff <= 1:
        add_finding(
            "L4c", "informational", None,
            f"open_contradictions counter drift ±1: overview.md={overview_open}, "
            f"actual={open_contradictions_count} — will auto-correct",
            {
                "overview_value": overview_open,
                "actual_count": open_contradictions_count,
                "action": "auto-correct",
            },
        )
    else:
        add_finding(
            "L4c", "forced-choice", None,
            f"open_contradictions counter drift ±{diff}: overview.md={overview_open}, "
            f"actual={open_contradictions_count}",
            {
                "overview_value": overview_open,
                "actual_count": open_contradictions_count,
                "diff": diff,
                "options": {
                    "A": f"Correct the counter to {open_contradictions_count}",
                    "B": "Investigate before correcting — skip counter update this pass",
                },
            },
            recommended="A",
        )

    # G4: total_pages
    overview_total = overview_fm.get("total_pages", 0) or 0
    if isinstance(overview_total, str):
        try:
            overview_total = int(overview_total)
        except ValueError:
            overview_total = 0

    if overview_total != total_indexed:
        add_finding(
            "G4", "informational", None,
            f"total_pages drift: overview.md={overview_total}, index.md={total_indexed}",
            {"overview_value": overview_total, "indexed_count": total_indexed},
        )
    else:
        add_finding(
            "G4", "informational", None,
            f"total_pages verified: {overview_total}",
            {"verified": True},
        )

    # G4: last_contradiction_id
    overview_last_id = overview_fm.get("last_contradiction_id", 0) or 0
    if isinstance(overview_last_id, str):
        try:
            overview_last_id = int(overview_last_id)
        except ValueError:
            overview_last_id = 0

    max_ctrd_num = 0
    for cid in all_ctrd_ids:
        m = CTRD_PATTERN.match(cid)
        if m:
            max_ctrd_num = max(max_ctrd_num, int(m.group(1)))

    if max_ctrd_num > overview_last_id:
        add_finding(
            "G4", "informational", None,
            f"last_contradiction_id is lower than highest CTRD found: "
            f"overview.md={overview_last_id}, highest found={max_ctrd_num}",
            {
                "overview_value": overview_last_id,
                "highest_found": max_ctrd_num,
                "action": "auto-correct-upward",
            },
        )
    else:
        add_finding(
            "G4", "informational", None,
            f"last_contradiction_id verified: {overview_last_id}",
            {"verified": True},
        )


def check_L10_teaching_ratio(teaching_tagged_count, topic_tool_count,
                              topic_tool_deprecated_count):
    """
    L10: Teaching Index completeness ratio.
    """
    denominator = topic_tool_count - topic_tool_deprecated_count
    if denominator == 0:
        add_finding("L10", "informational", None,
                    "No eligible topic/tool pages for teaching ratio calculation.", {})
        return

    ratio = teaching_tagged_count / denominator
    ratio_pct = round(ratio * 100, 1)

    if ratio < TEACHING_RATIO_THRESHOLD:
        add_finding(
            "L10", "forced-choice", None,
            f"Teaching relevance ratio below {int(TEACHING_RATIO_THRESHOLD*100)}% threshold: "
            f"{teaching_tagged_count}/{denominator} = {ratio_pct}%",
            {
                "tagged_count": teaching_tagged_count,
                "eligible_count": denominator,
                "ratio": ratio,
                "threshold": TEACHING_RATIO_THRESHOLD,
                "options": {
                    "A": "Acknowledge — I will review tagging in the next session",
                    "B": "Dismiss — low ratio is accurate for this wiki's current content",
                },
            },
            recommended="A",
        )
    else:
        add_finding(
            "L10", "informational", None,
            f"Teaching relevance ratio: {teaching_tagged_count}/{denominator} = {ratio_pct}% "
            f"(threshold: {int(TEACHING_RATIO_THRESHOLD*100)}%)",
            {"tagged_count": teaching_tagged_count, "eligible_count": denominator,
             "ratio": ratio},
        )


def _parse_log_entries(log_text):
    """Parse log.md into a list of entry dicts with keys: date, operation, description, body."""
    entries = []
    current = None
    header_pat = re.compile(
        r'^## \[(\d{4}-\d{2}-\d{2}[^\]]*)\]\s+(\S+)\s*\|(.*)'
    )
    for line in log_text.split("\n"):
        m = header_pat.match(line.strip())
        if m:
            if current:
                entries.append(current)
            op = m.group(2).strip()
            current = {
                "date_str": m.group(1).strip()[:10],
                "operation": op,
                "description": m.group(3).strip(),
                "body": [],
                "topic_tags": [],
                "result_quality": "",
            }
        elif current and line.strip():
            current["body"].append(line.strip())
            # Extract topic_tags and result_quality from query entries
            if current["operation"] == "query":
                tt = re.match(r'^Topic tags:\s+(.+)', line.strip())
                if tt:
                    current["topic_tags"] = [t.strip() for t in tt.group(1).split(",")]
                rq = re.match(r'^Result quality:\s+(\S+)', line.strip())
                if rq:
                    current["result_quality"] = rq.group(1).strip()
    if current:
        entries.append(current)
    return entries


def check_L12_collection_gaps(log_text, collection_gaps_text):
    """
    L12: Collection gap analysis from log.md query entries.
    """
    entries = _parse_log_entries(log_text)
    query_entries = [e for e in entries if e["operation"] == "query"]

    # Aggregate sparse/shallow by topic_tag
    tag_events = defaultdict(list)  # tag -> list of {"date", "quality"}
    for e in query_entries:
        quality = e["result_quality"]
        if quality in ("sparse", "shallow"):
            entry_date = _parse_scalar(e["date_str"])
            for tag in e["topic_tags"]:
                if tag:
                    tag_events[tag].append({"date": entry_date, "quality": quality})

    # Find tags with 3+ sparse/shallow entries
    for tag, events in sorted(tag_events.items()):
        if len(events) < 3:
            continue

        most_recent = max(
            (e["date"] for e in events if isinstance(e["date"], date)),
            default=None
        )
        # Check if sources ingested since most_recent
        potentially_addressed = False
        if most_recent:
            ingest_entries = [e for e in entries
                              if e["operation"] == "ingest"
                              and isinstance(_parse_scalar(e["date_str"]), date)
                              and isinstance(most_recent, date)
                              and _parse_scalar(e["date_str"]) > most_recent]
            potentially_addressed = len(ingest_entries) > 0

        add_finding(
            "L12", "forced-choice", None,
            f"Collection gap: '{tag}' — {len(events)} sparse/shallow queries, "
            f"most recent: {most_recent}",
            {
                "topic_tag": tag,
                "query_count": len(events),
                "most_recent": str(most_recent) if most_recent else None,
                "potentially_addressed": potentially_addressed,
                "options": {
                    "A": "Confirm as active gap — add to collection-gaps.md",
                    "B": "Mark as addressed — remove from collection-gaps.md if present",
                    "C": "Dismiss — not a priority",
                },
            },
            recommended=None,
        )


def check_L12a_session_stats(log_text):
    """
    L12a: Session stats threshold check.
    """
    entries = _parse_log_entries(log_text)
    stats_entries = [e for e in entries if e["operation"] == "session-stats"]
    count = len(stats_entries)

    if count < SESSION_STATS_THRESHOLD:
        add_finding(
            "L12a", "informational", None,
            f"Session stats count: {count} entries (threshold: {SESSION_STATS_THRESHOLD})",
            {"count": count, "threshold": SESSION_STATS_THRESHOLD},
        )
        return

    add_finding(
        "L12a", "forced-choice", None,
        f"Cost log has {count} session-stats entries. A threshold review is recommended.",
        {
            "count": count,
            "threshold": SESSION_STATS_THRESHOLD,
            "options": {
                "A": "Review now — analyze session-stats log and propose revised batch-size guidance",
                "B": "Defer — continue lint pass without review",
            },
        },
        recommended="B",
    )


def check_L12b_deferred_ingest():
    """
    L12b: Deferred ingest staleness check.
    """
    path = os.path.join("raw", "deferred-ingest.md")
    if not os.path.exists(path):
        return
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return
    fm, _ = parse_frontmatter(text)
    created = fm.get("created")
    if not created:
        add_finding("L12b", "informational", None,
                    "raw/deferred-ingest.md exists but has no created date.", {})
        return
    # Parse date from potentially datetime string
    if isinstance(created, str):
        created = _parse_scalar(created[:10])
    if not isinstance(created, date):
        return
    age = days_ago(created)
    if age is None:
        return

    if age > DEFERRED_STALENESS_DAYS:
        add_finding(
            "L12b", "forced-choice", None,
            f"Stale deferral: raw/deferred-ingest.md is {age} days old. "
            "The deferred ingest has not been resumed.",
            {
                "created": str(created),
                "age_days": age,
                "options": {
                    "A": "Resume ingest now — proceed to Step 0 after lint completes",
                    "B": "Discard — delete raw/deferred-ingest.md; leave queue.md unchanged",
                },
            },
            recommended="A",
        )
    else:
        add_finding(
            "L12b", "informational", None,
            f"Pending deferral: raw/deferred-ingest.md exists ({age} days old).",
            {"created": str(created), "age_days": age},
        )


def check_L12c_override_patterns(wll_text):
    """
    L12c: Override pattern detection in wiki-lessons-learned.md.
    D-category: extract entries in 30-day window, send to agent_review for categorization.
    """
    cutoff = TODAY - timedelta(days=30)
    entry_pat = re.compile(r'^### \[(\d{4}-\d{2}-\d{2})\]\s+(.+)', re.MULTILINE)
    op_pat = re.compile(r'\*\*Operation:\*\*\s+(\S+)')
    wrong_pat = re.compile(r'\*\*What was wrong:\*\*\s+(.+)')

    sections_of_interest = []
    current_section = None
    current_entry = None
    recent_entries = []

    for line in wll_text.split("\n"):
        if line.startswith("## "):
            current_section = line[3:].strip()
            continue
        if current_section in ("Ingest", "Lint"):
            m = entry_pat.match(line)
            if m:
                entry_date = _parse_scalar(m.group(1))
                if isinstance(entry_date, date) and entry_date >= cutoff:
                    current_entry = {
                        "date": entry_date,
                        "title": m.group(2),
                        "section": current_section,
                        "what_was_wrong": "",
                        "operation": "",
                    }
                    recent_entries.append(current_entry)
                else:
                    current_entry = None
                continue
            if current_entry:
                om = op_pat.match(line.strip())
                if om:
                    current_entry["operation"] = om.group(1)
                wm = wrong_pat.match(line.strip())
                if wm:
                    current_entry["what_was_wrong"] = wm.group(1)

    if len(recent_entries) >= 3:
        add_agent_review(
            "L12c", "override_categorization", None,
            f"Override pattern detection: {len(recent_entries)} entries in past 30 days — "
            "categorize into root cause bins to determine if Schema Signals entry is needed",
            entries=recent_entries,
            categories=[
                "schema definition overlap",
                "inference gap",
                "human preference drift",
                "vocabulary gap",
                "source ambiguity",
            ],
            threshold=3,
        )
    else:
        add_finding(
            "L12c", "informational", None,
            f"Override pattern check: {len(recent_entries)} entries in past 30 days "
            "(below 3-entry pattern threshold)",
            {"count": len(recent_entries)},
        )


def check_L12d_schema_signals_age(wll_text):
    """
    L12d: Schema Signals age check — flag open signals older than 60 days.
    """
    in_signals = False
    current_entry_date = None
    current_entry_title = None
    is_open = False

    for line in wll_text.split("\n"):
        if line.startswith("## Schema Signals"):
            in_signals = True
            continue
        if line.startswith("## ") and in_signals:
            in_signals = False
            continue
        if not in_signals:
            continue

        m = re.match(r'^### \[(\d{4}-\d{2}-\d{2})\]\s+(.+)', line)
        if m:
            # Save previous entry if open
            if current_entry_date and is_open:
                age = days_ago(current_entry_date)
                if age is not None and age > SCHEMA_SIGNALS_AGE_DAYS:
                    add_finding(
                        "L12d", "informational", None,
                        f"Open Schema Signal is {age} days old: {current_entry_title}",
                        {
                            "entry_title": current_entry_title,
                            "entry_date": str(current_entry_date),
                            "age_days": age,
                        },
                    )
            current_entry_date = _parse_scalar(m.group(1))
            current_entry_title = m.group(2)
            is_open = False
            continue

        if "**Status:** open" in line:
            is_open = True
        elif "**Status:** resolved" in line:
            is_open = False

    # Handle last entry
    if current_entry_date and is_open:
        age = days_ago(current_entry_date)
        if age is not None and age > SCHEMA_SIGNALS_AGE_DAYS:
            add_finding(
                "L12d", "informational", None,
                f"Open Schema Signal is {age} days old: {current_entry_title}",
                {
                    "entry_title": current_entry_title,
                    "entry_date": str(current_entry_date),
                    "age_days": age,
                },
            )


def check_L14_skill_enrichment(log_text):
    """
    L14: Skill file enrichment staleness.
    """
    entries = _parse_log_entries(log_text)
    ingest_count = sum(1 for e in entries if e["operation"] == "ingest")

    if ingest_count < 5:
        return

    for skill_file in SKILL_FILES:
        if not os.path.exists(skill_file):
            continue
        try:
            with open(skill_file, encoding="utf-8") as f:
                content = f.read()
        except OSError:
            continue

        # Find "TO BE ENRICHED" sections
        enriched_pattern = re.compile(
            r'#+\s+.*?TO BE ENRICHED.*?(?=^#+|\Z)', re.MULTILINE | re.DOTALL | re.IGNORECASE
        )
        for m in enriched_pattern.finditer(content):
            section_text = m.group(0)
            # Check if section is unpopulated (only placeholder text)
            lines = [l.strip() for l in section_text.split("\n") if l.strip()]
            # A populated section has more than just the heading and placeholder
            heading_lines = [l for l in lines if l.startswith("#")]
            non_heading = [l for l in lines if not l.startswith("#")
                           and "TO BE ENRICHED" not in l.upper()
                           and "operational experience" not in l.lower()
                           and l != "---"]
            if len(non_heading) == 0:
                section_heading = heading_lines[0] if heading_lines else "unknown section"
                add_finding(
                    "L14", "informational", None,
                    f"Skill file TO BE ENRICHED section with no examples after {ingest_count} ingests: "
                    f"{skill_file} — {section_heading}",
                    {
                        "skill_file": skill_file,
                        "section": section_heading,
                        "ingest_count": ingest_count,
                    },
                )


def check_L7_concept_gaps(page_prose, index_slugs, valid_slugs):
    """
    L7 (mechanical portion): Tokenize prose of Topic/Tool pages, find terms
    appearing in 3+ pages not covered by an existing page.
    D-category: outputs to agent_review.

    Calls strip_non_prose() before tokenizing to exclude Key Claims tables,
    Data Records tables, Teaching Notes sections, section headers, and code
    blocks. Without this filter the candidate list is dominated by schema
    column headers and structural boilerplate, producing zero signal.
    """
    term_pages = defaultdict(set)  # term -> set of page slugs

    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "up", "is", "are", "was", "were", "be",
        "been", "being", "have", "has", "had", "do", "does", "did", "will",
        "would", "could", "should", "may", "might", "can", "this", "that",
        "these", "those", "it", "its", "not", "no", "more", "also", "as",
        "if", "when", "which", "who", "where", "how", "than", "then", "so",
        "such", "their", "they", "them", "we", "our", "i", "you", "your",
        "ai", "llm", "model", "models", "system", "systems", "data", "based",
        "use", "used", "using", "new", "well", "while", "between", "through",
        "each", "most", "other", "about", "across", "human", "into", "over",
        "under", "any", "all", "both", "even", "often", "however", "while",
        "within", "without", "after", "before", "during", "since", "there",
        "what", "per", "key", "approach", "work", "tasks", "task", "tool",
        "tools", "time", "users", "user", "output", "outputs", "input",
        "inputs", "content", "text", "language", "see", "example", "one",
        "two", "three", "four", "five", "first", "second", "third",
    }

    for page_slug, prose in page_prose.items():
        words = re.findall(r'\b[a-z][a-z-]{3,}\b', strip_non_prose(prose).lower())
        for word in words:
            if word not in stop_words and len(word) > 4:
                term_pages[word].add(page_slug)

    # Find terms appearing in 3+ pages with no corresponding page
    candidates = []
    for term, pages in sorted(term_pages.items(), key=lambda x: -len(x[1])):
        if len(pages) < 3:
            continue
        # Check if a page exists for this term
        if term in valid_slugs or term in index_slugs:
            continue
        # Filter out terms that are substrings of existing slugs
        if any(term in slug for slug in valid_slugs):
            continue
        candidates.append({
            "term": term,
            "page_count": len(pages),
            "pages": sorted(pages)[:10],  # cap at 10 for output size
        })

    if candidates:
        add_agent_review(
            "L7", "concept_gap_filter", None,
            f"Concept gap candidates: {len(candidates)} terms appear in 3+ pages with "
            "no corresponding page. Agent filters aliases and sets stub type.",
            candidates=candidates[:30],  # cap total candidates
            instructions=(
                "For each candidate: (1) Filter out aliases/synonyms for existing pages. "
                "(2) For surviving terms, set stub_type: 'Topic' or 'Tool'. "
                "(3) Dismiss terms that are not meaningful standalone concepts."
            ),
        )
    else:
        add_finding("L7", "informational", None,
                    "Concept gap check: no terms found in 3+ pages without a corresponding page.",
                    {})


def check_L9_decay_exempt(page_claims, source_info, log_text):
    """
    L9: Identify Key Claims where conditions (b) and (c) are met for decay_exempt.
    D-category: outputs to agent_review for evaluation of condition (a).
    """
    # Build set of pages with contradiction-flag log entries
    entries = _parse_log_entries(log_text)
    flagged_pages = set()
    for e in entries:
        if e["operation"] == "contradiction-flag":
            # Extract page slug from description line body
            for line in e["body"]:
                m = re.match(r'^Page:\s+\[\[([^\]]+)\]\]', line)
                if m:
                    flagged_pages.add(wikilink_to_slug(m.group(1)))

    for page_slug, claims_rows in page_claims.items():
        for row in claims_rows:
            decay_exempt_val = row.get("decay_exempt", "false").strip().lower()
            if decay_exempt_val == "true":
                continue  # Already exempt

            source_cell = row.get("source", "")
            if "[derived]" in source_cell:
                continue

            # Condition (b): no contradiction-flag entry for this page
            if page_slug in flagged_pages:
                continue

            # Condition (c): 2+ independent peer-reviewed or institutional sources
            qualifying_sources = []
            for m in WIKILINK_PATTERN.finditer(source_cell):
                raw = m.group(1)
                slug = wikilink_to_slug(raw)
                tail = source_cell[m.end():m.end() + 30]
                if "[minority view]" in tail:
                    continue
                sinfo = source_info.get(slug, {})
                tier = sinfo.get("tier", "")
                if tier in ("peer-reviewed", "institutional"):
                    qualifying_sources.append({"slug": slug, "tier": tier})

            if len(qualifying_sources) >= 2:
                add_agent_review(
                    "L9", "definitional_classification", page_slug,
                    f"Claim passes conditions (b)+(c) for decay_exempt on {page_slug}. "
                    "Agent must evaluate condition (a): is this claim definitional or empirical?",
                    claim_text=row.get("claim", ""),
                    supporting_sources=qualifying_sources,
                    current_support_score=row.get("support_score", ""),
                    condition_b_met=True,
                    condition_c_met=True,
                    options={"A": "Confirm — set decay_exempt: true", "B": "Decline"},
                    recommended=None,
                )


# ─── Page Reader Orchestrator ─────────────────────────────────────────────────

def read_and_check_all_pages(valid_slugs, slug_to_path, ctrd_signals, last_lint_date, verbose):
    """
    Walk all content directories, read each page once, run all per-page checks.

    Returns:
    - entity_pages_fm: dict slug -> fm (for cross-page staleness checks)
    - inbound_links: dict slug -> set of slugs that link to it (for orphan detection)
    - open_contradictions_count: total open contradiction entries across all pages
    - teaching_tagged_count: count of pages with teaching_relevance: true
    - topic_tool_count: count of topic+tool pages
    - topic_tool_deprecated_count: count of deprecated tool pages
    - source_slugs: set of slugs in sources/
    - all_ctrd_ids: set of all CTRD-NNN IDs found across the wiki
    - page_data_records: dict slug -> list of Data Records rows (for L19; topic/tool/comparison)
    - page_meta: dict slug -> {"directory": str, "page_type": str} (for L19 page-path construction)
    """
    entity_pages_fm = {}  # slug -> fm for non-source pages
    inbound_links = defaultdict(set)  # target_slug -> {source_slugs}
    open_contradictions_count = 0
    teaching_tagged_count = 0
    topic_tool_count = 0
    topic_tool_deprecated_count = 0
    source_slugs = set()
    all_ctrd_ids = set()
    page_claims = {}   # topic/tool slug -> list of claim rows (for L3, L9, L19)
    page_prose = {}    # slug -> prose body text (topic/tool for L7; all in-scope types for L16)
    page_data_records = {}  # topic/tool/comparison slug -> Data Records rows (for L19)
    page_meta = {}  # slug -> {"directory": str, "page_type": str} (for L19)

    # Build source slug set first (for G3)
    if os.path.isdir("sources"):
        for fname in os.listdir("sources"):
            if fname.endswith(".md"):
                source_slugs.add(fname[:-3])

    for directory in CONTENT_DIRS:
        if not os.path.isdir(directory):
            continue

        for fname in sorted(os.listdir(directory)):
            if not fname.endswith(".md"):
                continue

            page_slug = fname[:-3]
            fpath = os.path.join(directory, fname)

            try:
                with open(fpath, encoding="utf-8") as f:
                    text = f.read()
            except OSError as exc:
                add_finding("error", "informational", page_slug,
                            f"Cannot read {fpath}: {exc}", {})
                continue

            fm, body = parse_frontmatter(text)
            page_type = fm.get("type", "")
            page_meta[page_slug] = {"directory": directory, "page_type": page_type}

            # Store fm for cross-page checks
            if page_type in ("topic", "tool", "comparison", "teaching-brief", "pitfalls"):
                entity_pages_fm[page_slug] = fm

            # Accumulate counters
            if page_type in ("topic", "tool"):
                topic_tool_count += 1
                if fm.get("status") == "deprecated":
                    topic_tool_deprecated_count += 1
            if fm.get("teaching_relevance") is True:
                teaching_tagged_count += 1

            # Count open contradictions
            open_ctrd = fm.get("open_contradictions")
            if open_ctrd and isinstance(open_ctrd, list):
                open_contradictions_count += len(open_ctrd)
                for entry in open_ctrd:
                    if isinstance(entry, dict):
                        cid = entry.get("id", "")
                        if cid:
                            all_ctrd_ids.add(cid)

            # Find all CTRD-NNN references in the file (for G4 max-id scan)
            for m in CTRD_PATTERN.finditer(text):
                all_ctrd_ids.add(f"CTRD-{m.group(1)}")

            # Parse Key Claims table (for L3, L9, L11, G3, L19)
            claims_rows = []
            if page_type in ("topic", "tool"):
                claims_rows = parse_markdown_table(body, "## Key Claims")
                page_claims[page_slug] = claims_rows
            # Parse Data Records table (for L5c freshness, L19 serialization)
            if page_type in ("topic", "tool", "comparison"):
                dr_rows = parse_data_records_table(body)
                if dr_rows:
                    page_data_records[page_slug] = dr_rows
            # Accumulate prose body for L7 (topic/tool) and L16 (all in-scope types)
            if page_type in ("topic", "tool", "comparison", "pitfalls", "teaching-brief"):
                page_prose[page_slug] = body

            # G1: Wikilink integrity (extract outbound links)
            outbound = check_G1_wikilink_integrity(text, page_slug, valid_slugs)
            for target in outbound:
                inbound_links[target].add(page_slug)

            if verbose and page_type in ("topic", "tool"):
                print(f"  [verbose] Checking: {fpath}")

            # Run per-page checks
            check_L4a_contradiction_expiry(fm, page_slug, ctrd_signals)
            check_L4b_open_contradictions(fm, page_slug, ctrd_signals)
            check_L5_staleness(fm, page_slug, page_type)  # entity_pages_fm filled in second pass
            check_L5a_stale_upgrade(fm, page_slug, page_type)
            check_L5b_teaching_notes_currency(fm, page_slug)
            check_L5c_data_records_freshness(body, page_slug)
            check_L8_pitfalls_maintenance(fm, body, page_slug)
            check_L15_teaching_tagged_missing_fields(fm, page_slug, page_type)
            check_L17_vocabulary_conformance(fm, page_slug)
            check_G5_status_content_consistency(fm, body, page_slug, page_type, claims_rows)
            check_L11_schema_conformance(fm, body, page_slug, page_type, claims_rows, last_lint_date)

            if page_type in ("topic", "tool") and claims_rows:
                check_G3_source_reference_integrity(claims_rows, page_slug, source_slugs)

    # L6: Orphan page detection (after all pages read)
    check_L6_orphan_detection(entity_pages_fm, inbound_links)

    # L5 comparison/teaching-brief staleness (now that entity_pages_fm is populated)
    for directory in ["comparisons", "teaching"]:
        if not os.path.isdir(directory):
            continue
        for fname in sorted(os.listdir(directory)):
            if not fname.endswith(".md"):
                continue
            page_slug = fname[:-3]
            if page_slug not in entity_pages_fm:
                continue
            fm = entity_pages_fm[page_slug]
            page_type = fm.get("type", "")
            if page_type in ("comparison", "teaching-brief"):
                check_L5_staleness(fm, page_slug, page_type, entity_pages_fm)

    return (
        entity_pages_fm,
        inbound_links,
        open_contradictions_count,
        teaching_tagged_count,
        topic_tool_count,
        topic_tool_deprecated_count,
        source_slugs,
        all_ctrd_ids,
        page_claims,
        page_prose,
        page_data_records,
        page_meta,
    )


# Required Data Records columns — CLAUDE.md Section 6.6 / spec 4.2
REQUIRED_DATA_RECORD_KEYS = (
    "metric",
    "value",
    "conditions",
    "measurement_date",
    "source",
    "status",
)


def check_L19_extraction_and_serialization(
    page_claims, page_data_records, page_meta, source_info
):
    """
    L19 (Group C — serialization): build raw/claims.json and
    raw/data-records.json from the Key Claims and Data Records rows
    accumulated during Group B (spec Section 4.4). Reuses parse_markdown_table
    / parse_data_records_table output already accumulated — no page is
    re-read. Writes both artifacts atomically (temp file + os.replace);
    a write failure is a fatal script error (spec 4.4 — the artifacts are
    L20's input and silent absence would disable it invisibly).

    Data Records are serialized first so their canonical metrics define the
    "metric universe" (spec 4.3.4) used for Key Claim signature detection.

    Returns (claims_list, records_list) for L20 to consume in the same run
    without re-parsing anything.
    """
    # ---- Data Records first: defines the metric universe ----
    records_list = []
    malformed_rows = 0
    dr_metrics = set()

    for page_slug, rows in page_data_records.items():
        meta = page_meta.get(page_slug, {})
        page_path = f"{meta.get('directory', '')}/{page_slug}"
        for row in rows:
            if not all(k in row for k in REQUIRED_DATA_RECORD_KEYS):
                malformed_rows += 1
                add_finding(
                    "L19",
                    "informational",
                    page_slug,
                    f"Data Records row skipped: malformed (missing required column) on {page_slug}",
                    {"page": page_path, "row_keys": sorted(row.keys())},
                )
                continue

            metric_canonical = canonicalize_metric(row["metric"])
            value_numeric, value_numeric_high, unit = parse_value(row["value"])
            sources = [
                wikilink_to_slug(m.group(1))
                for m in WIKILINK_PATTERN.finditer(row["source"])
            ]

            records_list.append(
                {
                    "page": page_path,
                    "page_type": meta.get("page_type", ""),
                    "metric_raw": row["metric"],
                    "metric_canonical": metric_canonical,
                    "value_raw": row["value"],
                    "value_numeric": value_numeric,
                    "value_numeric_high": value_numeric_high,
                    "unit": unit,
                    "conditions_raw": row["conditions"],
                    "conditions_tokens": _tokenize_conditions(row["conditions"]),
                    "measurement_date": row["measurement_date"].strip(),
                    "sources": sources,
                    "status": row["status"].strip(),
                }
            )
            if metric_canonical:
                dr_metrics.add(metric_canonical)

    metric_universe = (
        dr_metrics | set(METRIC_ALIASES.keys()) | set(METRIC_ALIASES.values())
    )

    # ---- Claims: signature detection depends on metric_universe above ----
    claims_list = []
    claims_with_signature = 0

    for page_slug, claims_rows in page_claims.items():
        meta = page_meta.get(page_slug, {})
        page_path = f"{meta.get('directory', '')}/{page_slug}"

        for row_index, row in enumerate(claims_rows, start=1):
            source_cell = row.get("source", "")
            status_cell = row.get("status", "")
            claim_text = row.get("claim", "")
            derived = "[derived]" in source_cell
            decay_exempt = row.get("decay_exempt", "false").strip().lower() == "true"

            sources = []
            source_annotations = {}
            for slug, is_minority in extract_source_slugs_from_claims([row]):
                sources.append(slug)
                if is_minority:
                    source_annotations[slug] = "minority view"

            ctrd_ids = [f"CTRD-{n}" for n in CTRD_PATTERN.findall(status_cell)]
            status_clean = re.sub(r"\s*\[CTRD-\d+\]", "", status_cell).strip()

            if derived:
                support_score = "derived"
            else:
                support_score, _detail = compute_support_score(
                    source_cell, decay_exempt, source_info
                )

            sigs = detect_claim_signatures(claim_text, metric_universe)
            if not sigs:
                signature = None
            elif len(sigs) == 1:
                signature = sigs[0]
                claims_with_signature += 1
            else:
                signature = sigs
                claims_with_signature += 1

            claims_list.append(
                {
                    "page": page_path,
                    "page_type": meta.get("page_type", ""),
                    "row_index": row_index,
                    "claim": claim_text,
                    "sources": sources,
                    "source_annotations": source_annotations,
                    "derived": derived,
                    "date": row.get("date", "").strip(),
                    "status": status_clean,
                    "ctrd_ids": ctrd_ids,
                    "support_score": support_score,
                    "decay_exempt": decay_exempt,
                    "signature": signature,
                }
            )

    # ---- Write both artifacts atomically ----
    claims_artifact = {
        "generated": TODAY.isoformat(),
        "script_version": SCRIPT_VERSION,
        "claims": claims_list,
    }
    records_artifact = {
        "generated": TODAY.isoformat(),
        "script_version": SCRIPT_VERSION,
        "records": records_list,
    }
    try:
        os.makedirs("raw", exist_ok=True)
        _atomic_write_json(os.path.join("raw", "claims.json"), claims_artifact)
        _atomic_write_json(os.path.join("raw", "data-records.json"), records_artifact)
    except (OSError, TypeError) as exc:
        sys.exit(
            f"FATAL: L19 could not write structured-data extraction artifacts: {exc}"
        )

    pages_contributing = len(set(page_claims.keys()) | set(page_data_records.keys()))
    add_finding(
        "L19",
        "informational",
        None,
        f"Structured-data extraction: {pages_contributing} pages contributing, "
        f"{len(claims_list)} claims serialized, {len(records_list)} records serialized, "
        f"{malformed_rows} Data Records rows skipped as malformed, "
        f"{claims_with_signature} claims carrying a quantitative signature.",
        {
            "pages_contributing": pages_contributing,
            "claims_serialized": len(claims_list),
            "records_serialized": len(records_list),
            "malformed_rows_skipped": malformed_rows,
            "claims_with_signature": claims_with_signature,
        },
    )

    return claims_list, records_list


# ─── L20: Contradiction Pre-Screen (BL-W-02, DM-128, spec Section 4.5) ───────


def _sig_list(signature):
    """Normalize a claims.json 'signature' field (None/dict/list) to a list."""
    if signature is None:
        return []
    if isinstance(signature, list):
        return signature
    return [signature]


def _truncate_ym(date_str):
    """Truncate a YYYY-MM-DD or YYYY-MM string to its YYYY-MM prefix."""
    return (date_str or "")[:7]


def _best_matching_divergence(values_a, values_b):
    """
    Find the most-divergent comparable pair between two claims' inline
    value lists (spec 4.5 Class 1). A claim's signature carries every
    parsable value in its text, not just the one tied to the matched
    metric, so candidate pairs are compared across the full cross product
    and the strongest divergent match wins — a v1 design choice the spec
    does not pin down further. Returns (relative_divergence, value_a,
    value_b) for the best divergent pair, or None if none diverges.
    """
    best = None
    for va in values_a:
        if va.get("numeric") is None or va.get("unit") is None:
            continue
        for vb in values_b:
            if vb.get("numeric") is None or vb.get("unit") is None:
                continue
            rel = relative_divergence(
                va["numeric"], None, va["unit"], vb["numeric"], None, vb["unit"]
            )
            if rel is not None and (best is None or rel > best[0]):
                best = (rel, va, vb)
    return best


def _claim_vs_record_divergence(values_a, record_low, record_high, record_unit):
    """
    Find the most-divergent comparable pair between a claim's inline value
    list and a single Data Record value/range (spec 4.5 Class 2). Same
    multi-value design note as _best_matching_divergence. Returns
    (relative_divergence, value_a) for the best divergent match, or None.
    """
    best = None
    for va in values_a:
        if va.get("numeric") is None or va.get("unit") is None:
            continue
        rel = relative_divergence(
            va["numeric"], None, va["unit"], record_low, record_high, record_unit
        )
        if rel is not None and (best is None or rel > best[0]):
            best = (rel, va)
    return best


def _designate_class1_sides(claim_a, claim_b):
    """
    Determine (contested, contesting) for a Class 1 KC<->KC candidate: the
    contested side has the lower support score, tie-broken by older date,
    tie-broken by alphabetical page slug (spec 4.5). Both claims must
    already have numeric (non-"derived") support scores.
    """
    key_a = (claim_a["support_score"], claim_a["date"], claim_a["page"])
    key_b = (claim_b["support_score"], claim_b["date"], claim_b["page"])
    # Lower score first; older date first; alphabetically-first page first.
    if (key_a[0], key_a[1], key_a[2]) <= (key_b[0], key_b[1], key_b[2]):
        return claim_a, claim_b
    return claim_b, claim_a


def _eligible_claims_by_metric(claims_list):
    """
    Group (claim, signature) pairs eligible for Class 1/2 matching by
    metric_canonical: status current, not derived (support_score must be
    numeric for the contested-side tie-break), and no open CTRD flag
    (already in protocol — spec 4.5 Class 1; applied to Class 2 too for
    consistency, since a claim under an open contradiction shouldn't gain a
    second pre-screen flag through a different channel).
    """
    by_metric = defaultdict(list)
    for claim in claims_list:
        if claim["status"] != "current" or claim["derived"] or claim["ctrd_ids"]:
            continue
        for sig in _sig_list(claim["signature"]):
            by_metric[sig["metric_canonical"]].append((claim, sig))
    return by_metric


def _records_by_metric(records_list):
    """Group Data Records by metric_canonical."""
    by_metric = defaultdict(list)
    for record in records_list:
        by_metric[record["metric_canonical"]].append(record)
    return by_metric


def _class1_candidates(claims_by_metric):
    """Class 1 — KC<->KC cross-page divergence candidates (spec 4.5)."""
    candidates = []
    for metric_canonical, entries in claims_by_metric.items():
        for i in range(len(entries)):
            claim_a, sig_a = entries[i]
            for j in range(i + 1, len(entries)):
                claim_b, sig_b = entries[j]
                if claim_a["page"] == claim_b["page"]:
                    continue  # same-page KC<->KC is out of scope (Section 10)
                sim = claim_similarity(
                    claim_a["claim"],
                    claim_b["claim"],
                    metric_terms=[
                        sig_a["metric_matched_text"],
                        sig_b["metric_matched_text"],
                    ],
                )
                if sim < CLAIM_SIM_THRESHOLD:
                    continue
                match = _best_matching_divergence(sig_a["values"], sig_b["values"])
                if match is None:
                    continue
                rel, va, vb = match
                contested, contesting = _designate_class1_sides(claim_a, claim_b)
                candidates.append(
                    {
                        "class": "kc-kc",
                        "metric_canonical": metric_canonical,
                        "relative_divergence": rel,
                        "claim_similarity": sim,
                        "side_a": {
                            "page": contested["page"],
                            "kind": "claim",
                            "text": contested["claim"],
                            "sources": contested["sources"],
                            "date": contested["date"],
                            "support_score": contested["support_score"],
                            "value": va["raw"] if contested is claim_a else vb["raw"],
                        },
                        "side_b": {
                            "page": contesting["page"],
                            "kind": "claim",
                            "text_or_metric": contesting["claim"],
                            "sources": contesting["sources"],
                            "date": contesting["date"],
                            "support_score": contesting["support_score"],
                            "value": vb["raw"] if contested is claim_a else va["raw"],
                        },
                        "description": (
                            f"Pre-screen divergence candidate: {metric_canonical}, "
                            f"{va['raw']} vs {vb['raw']}"
                        ),
                    }
                )
    return candidates


def _class2_candidates(claims_by_metric, records_by_metric):
    """Class 2 — DR<->KC same-page divergence candidates (spec 4.5)."""
    candidates = []
    for metric_canonical, entries in claims_by_metric.items():
        for record in records_by_metric.get(metric_canonical, []):
            if record["status"] != "current":
                continue
            for claim, sig in entries:
                if claim["page"] != record["page"]:
                    continue  # Class 2 is same-page only; cross-page is deferred scope
                if _truncate_ym(record["measurement_date"]) < _truncate_ym(
                    claim["date"]
                ):
                    continue  # record must postdate (or match) the claim
                match = _claim_vs_record_divergence(
                    sig["values"],
                    record["value_numeric"],
                    record["value_numeric_high"],
                    record["unit"],
                )
                if match is None:
                    continue
                rel, va = match
                candidates.append(
                    {
                        "class": "dr-kc",
                        "metric_canonical": metric_canonical,
                        "relative_divergence": rel,
                        "claim_similarity": None,
                        "side_a": {
                            "page": claim["page"],
                            "kind": "claim",
                            "text": claim["claim"],
                            "sources": claim["sources"],
                            "date": claim["date"],
                            "support_score": claim["support_score"],
                            "value": va["raw"],
                        },
                        "side_b": {
                            "page": record["page"],
                            "kind": "record",
                            "text_or_metric": record["metric_raw"],
                            "sources": record["sources"],
                            "date": record["measurement_date"],
                            "support_score": None,
                            "value": record["value_raw"],
                        },
                        "description": (
                            f"Pre-screen divergence candidate: {metric_canonical}, "
                            f"{va['raw']} vs {record['value_raw']}"
                        ),
                    }
                )
    return candidates


def _class3a_findings(records_by_metric):
    """Class 3a — DR<->DR inconsistent replication (informational only, spec 4.5)."""
    findings = []
    for metric_canonical, records in records_by_metric.items():
        for i in range(len(records)):
            rec_a = records[i]
            if rec_a["status"] != "current":
                continue
            for j in range(i + 1, len(records)):
                rec_b = records[j]
                if rec_b["status"] != "current" or rec_a["page"] == rec_b["page"]:
                    continue
                if rec_a["measurement_date"] != rec_b["measurement_date"]:
                    continue
                if not (set(rec_a["sources"]) & set(rec_b["sources"])):
                    continue
                if (
                    conditions_similarity(
                        rec_a["conditions_tokens"], rec_b["conditions_tokens"]
                    )
                    < CONDITIONS_SIM_THRESHOLD
                ):
                    continue
                if not divergence(
                    rec_a["value_numeric"],
                    rec_a["value_numeric_high"],
                    rec_a["unit"],
                    rec_b["value_numeric"],
                    rec_b["value_numeric_high"],
                    rec_b["unit"],
                ):
                    continue
                findings.append(
                    f"Class 3a inconsistent replication: {metric_canonical} — "
                    f"[[{rec_a['page']}]] reports {rec_a['value_raw']}, "
                    f"[[{rec_b['page']}]] reports {rec_b['value_raw']} for the same "
                    f"{rec_a['measurement_date']} measurement, shared source(s) "
                    f"{sorted(set(rec_a['sources']) & set(rec_b['sources']))}."
                )
    return findings


def _class3b_findings(records_by_metric):
    """Class 3b — DR<->DR supersession asymmetry (informational only, spec 4.5)."""
    findings = []
    for metric_canonical, records in records_by_metric.items():
        by_page = defaultdict(list)
        for rec in records:
            by_page[rec["page"]].append(rec)
        pages = sorted(by_page.keys())
        for page_a in pages:
            for rec_a in by_page[page_a]:
                if rec_a["status"] != "current":
                    continue
                for page_b in pages:
                    if page_b == page_a:
                        continue
                    candidates = [
                        rec_b
                        for rec_b in by_page[page_b]
                        if (set(rec_a["sources"]) & set(rec_b["sources"]))
                        and conditions_similarity(
                            rec_a["conditions_tokens"], rec_b["conditions_tokens"]
                        )
                        >= CONDITIONS_SIM_THRESHOLD
                    ]
                    if not candidates:
                        continue
                    best_b = max(candidates, key=lambda r: r["measurement_date"])
                    if best_b["measurement_date"] < rec_a["measurement_date"]:
                        findings.append(
                            f"Class 3b supersession asymmetry: {metric_canonical} — "
                            f"[[{page_a}]] has a current measurement dated "
                            f"{rec_a['measurement_date']}, but [[{page_b}]]'s most "
                            f"recent matching measurement is dated "
                            f"{best_b['measurement_date']} — it may have missed an append."
                        )
    return findings


def check_L20_contradiction_prescreen(claims_list, records_list):
    """
    L20 (Group C — pre-screen): match quantitative assertions across the
    claims.json/data-records.json structures L19 built (no page re-reads)
    and surface divergence candidates for the agent's existing
    CONTRADICTION-SKILL.md Section 1.4 existence check (spec Section 4.5).

    Classes 1-2 produce agent_review items (review_type:
    contradiction_prescreen); Classes 3a-3b produce informational findings
    only and are structurally incapable of promotion to a contradiction
    review item (spec F5). Class 1+2 candidates are capped at
    MAX_PRESCREEN_CANDIDATES per run, ranked Class 2 before Class 1, then by
    descending relative divergence, then descending claim similarity;
    overflow is deferred (stateless re-derivation next run), not dropped.
    """
    claims_by_metric = _eligible_claims_by_metric(claims_list)
    records_by_metric = _records_by_metric(records_list)

    class1 = _class1_candidates(claims_by_metric)
    class2 = _class2_candidates(claims_by_metric, records_by_metric)

    all_candidates = class2 + class1  # Class 2 ranked before Class 1 (spec 4.6)
    all_candidates.sort(
        key=lambda c: (
            0 if c["class"] == "dr-kc" else 1,
            -c["relative_divergence"],
            -(c["claim_similarity"] or 0.0),
        )
    )

    surfaced = all_candidates[:MAX_PRESCREEN_CANDIDATES]
    deferred = all_candidates[MAX_PRESCREEN_CANDIDATES:]

    for cand in surfaced:
        add_agent_review(
            "L20",
            "contradiction_prescreen",
            None,
            cand["description"],
            **{k: v for k, v in cand.items() if k != "description"},
        )

    if deferred:
        add_finding(
            "L20",
            "informational",
            None,
            f"Pre-screen: {len(deferred)} Class 1/2 candidate(s) deferred to next "
            f"lint pass (ceiling {MAX_PRESCREEN_CANDIDATES} reached).",
            {"deferred_count": len(deferred)},
        )

    class3a = _class3a_findings(records_by_metric)
    class3b = _class3b_findings(records_by_metric)

    for msg in class3a[:20]:
        add_finding("L20", "informational", None, msg, {})
    if len(class3a) > 20:
        add_finding(
            "L20",
            "informational",
            None,
            f"Class 3a: {len(class3a) - 20} more inconsistent-replication findings not shown.",
            {},
        )
    for msg in class3b[:20]:
        add_finding("L20", "informational", None, msg, {})
    if len(class3b) > 20:
        add_finding(
            "L20",
            "informational",
            None,
            f"Class 3b: {len(class3b) - 20} more supersession-asymmetry findings not shown.",
            {},
        )

    add_finding(
        "L20",
        "informational",
        None,
        f"Contradiction pre-screen: Class 1 candidates={len(class1)}, "
        f"Class 2 candidates={len(class2)} (pre-ceiling), surfaced={len(surfaced)}, "
        f"deferred={len(deferred)}, Class 3a={len(class3a)}, Class 3b={len(class3b)}.",
        {
            "class1_count": len(class1),
            "class2_count": len(class2),
            "surfaced_count": len(surfaced),
            "deferred_count": len(deferred),
            "class3a_count": len(class3a),
            "class3b_count": len(class3b),
        },
    )
def check_L6_orphan_detection(entity_pages_fm, inbound_links):
    """
    L6: Detect pages with no inbound wikilinks from non-source pages.
    Informational only.
    """
    for slug in sorted(entity_pages_fm.keys()):
        fm = entity_pages_fm[slug]
        page_type = fm.get("type", "")
        # Only check non-source pages
        if page_type == "source":
            continue
        if slug not in inbound_links or len(inbound_links[slug]) == 0:
            add_finding(
                "L6", "informational", slug,
                f"Orphan page: {slug} has no inbound wikilinks from non-source pages",
                {"page": slug, "page_type": page_type},
            )


def check_L16_wikilink_proliferation(entity_pages_fm, valid_slugs, slug_to_path, page_prose):
    """
    L16: Wikilink proliferation scan.

    Scans prose sections of Topic, Tool, Comparison, Pitfalls, and Teaching-brief
    pages for text that matches an existing wiki entity slug or alias but is not yet
    enclosed in a wikilink. Emits one batch forced-choice finding (Tier 1) covering all
    candidates, plus individual informational findings (Tier 2).

    Tier 1 requires all three conditions:
      (a) Exact match: candidate term matches a slug (kebab→space) or aliases entry.
      (b) Standalone noun phrase: word-boundary check (no substring of a larger term).
      (c) Topical proximity: shared related_topics/related_tools, OR target appears in
          containing page's Key Claims source refs, OR same content directory.

    Tier 2: condition (a) met but (b) or (c) fails — informational only.

    Usage example:
        check_L16_wikilink_proliferation(
            entity_pages_fm, valid_slugs, slug_to_path, page_prose
        )
    """
    # In-scope source page types for this scan (Source pages and singletons excluded)
    L16_SCOPE_TYPES = {"topic", "tool", "comparison", "pitfalls", "teaching-brief"}

    # Build alias map: normalized_alias -> target_slug
    # Also build slug_to_dir map for condition (c) same-directory check
    alias_map = {}   # lowercase alias text -> target_slug
    slug_to_dir = {} # slug -> content directory name

    for slug, fpath in slug_to_path.items():
        # Infer directory from path (first component)
        parts = fpath.replace("\\", "/").split("/")
        if parts:
            slug_to_dir[slug] = parts[0]

    for slug, fm in entity_pages_fm.items():
        aliases = fm.get("aliases") or []
        if isinstance(aliases, list):
            for alias in aliases:
                if isinstance(alias, str):
                    alias_map[alias.lower()] = slug

    # Build set of all candidate target slugs (exclude singletons, keep only entity pages)
    target_slugs = {
        s for s in entity_pages_fm
        if entity_pages_fm[s].get("type") in L16_SCOPE_TYPES
    }

    # Helper: normalize slug to space-separated words for text matching
    def slug_to_phrase(slug):
        return slug.replace("-", " ")

    # Helper: build regex pattern matching the phrase at word boundaries
    def make_word_boundary_pattern(phrase):
        return re.compile(
            r'(?<![A-Za-z0-9-])' + re.escape(phrase) + r'(?![A-Za-z0-9-])',
            re.IGNORECASE,
        )

    # Helper: extract ~60-char context snippet centred on the match
    def extract_snippet(text, match_start, match_end, window=60):
        half = window // 2
        start = max(0, match_start - half)
        end = min(len(text), match_end + half)
        snippet = text[start:end].replace("\n", " ")
        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."
        return snippet

    # Helper: strip prose of sections that should not be scanned
    # Returns prose lines only (no Key Claims, Data Records, headers, code blocks)
    def extract_scannable_prose(body):
        lines = body.split("\n")
        result = []
        in_code_block = False
        in_excluded_section = False

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            if stripped.startswith("#"):
                # Track exclusion sections; any new ## resets
                if re.match(r'^#+\s', stripped):
                    low = stripped.lower()
                    if "key claims" in low or "data records" in low:
                        in_excluded_section = True
                    else:
                        in_excluded_section = False
                continue  # Always skip header lines themselves
            if stripped.startswith("|"):
                continue  # Skip table rows
            if in_excluded_section:
                continue
            result.append(line)
        return "\n".join(result)

    # Helper: check topical proximity (condition c)
    def has_topical_proximity(source_slug, source_fm, target_slug):
        # Shared related_topics or related_tools
        src_rt = set(source_fm.get("related_topics") or [])
        src_rt_tools = set(source_fm.get("related_tools") or [])

        # Normalise wikilink targets in these lists to bare slugs
        def normalise_set(s):
            return {wikilink_to_slug(v) for v in s}

        src_rt = normalise_set(src_rt)
        src_rt_tools = normalise_set(src_rt_tools)

        if target_slug in src_rt or target_slug in src_rt_tools:
            return True

        # Target appears in source page's related sets (reciprocal)
        target_fm = entity_pages_fm.get(target_slug, {})
        tgt_rt = normalise_set(set(target_fm.get("related_topics") or []))
        tgt_rt_tools = normalise_set(set(target_fm.get("related_tools") or []))
        if source_slug in tgt_rt or source_slug in tgt_rt_tools:
            return True

        # Same content directory
        src_dir = slug_to_dir.get(source_slug)
        tgt_dir = slug_to_dir.get(target_slug)
        if src_dir and tgt_dir and src_dir == tgt_dir:
            return True

        return False

    # ── Main scan loop ─────────────────────────────────────────────────────────
    # Collect all Tier 1 candidates for the single batch finding
    tier1_rows = []   # list of dicts: {row, target_slug, source_page, snippet}
    row_number = 0

    for source_slug in sorted(page_prose.keys()):
        source_fm = entity_pages_fm.get(source_slug, {})
        page_type = source_fm.get("type", "")
        if page_type not in L16_SCOPE_TYPES:
            continue

        body = page_prose[source_slug]
        scannable = extract_scannable_prose(body)

        # Build set of slugs already wikilinked in this page's prose
        already_linked = set()
        for wl_target in extract_wikilinks(scannable):
            already_linked.add(wikilink_to_slug(wl_target))
        # Also check frontmatter wikilinks
        full_text_wikilinks = extract_wikilinks(body)
        for wl_target in full_text_wikilinks:
            already_linked.add(wikilink_to_slug(wl_target))

        # Track which target slugs we've already surfaced for this page (first-occurrence rule)
        surfaced_for_page = set()

        for target_slug in sorted(target_slugs):
            # Skip self-reference
            if target_slug == source_slug:
                continue
            # Skip if already wikilinked
            if target_slug in already_linked:
                continue
            # Skip if already surfaced as a candidate for this page
            if target_slug in surfaced_for_page:
                continue

            # Build candidate phrases: slug-as-words and all aliases
            candidate_phrases = [slug_to_phrase(target_slug)]
            target_fm = entity_pages_fm.get(target_slug, {})
            for alias in (target_fm.get("aliases") or []):
                if isinstance(alias, str):
                    candidate_phrases.append(alias)

            for phrase in candidate_phrases:
                pattern = make_word_boundary_pattern(phrase)
                match = pattern.search(scannable)
                if not match:
                    continue

                # Condition (a) satisfied — exact match found
                # Condition (b): word-boundary satisfied by pattern (already enforced)
                cond_b = True  # regex enforces word-boundary

                # Condition (c): topical proximity
                cond_c = has_topical_proximity(source_slug, source_fm, target_slug)

                snippet = extract_snippet(scannable, match.start(), match.end())

                if cond_b and cond_c:
                    # Tier 1 — actionable
                    row_number += 1
                    tier1_rows.append({
                        "row": row_number,
                        "target_slug": target_slug,
                        "source_page": source_slug,
                        "snippet": snippet,
                        "phrase_matched": phrase,
                    })
                    surfaced_for_page.add(target_slug)
                else:
                    # Tier 2 — informational
                    reason = []
                    if not cond_c:
                        reason.append("no topical proximity")
                    add_finding(
                        "L16", "informational", source_slug,
                        (f"L16 Tier 2: '{phrase}' in [[{source_slug}]] matches "
                         f"[[{target_slug}]] but {' and '.join(reason)} — not linked"),
                        {
                            "target_slug": target_slug,
                            "source_page": source_slug,
                            "phrase": phrase,
                            "reason": reason,
                            "tier": 2,
                        },
                    )
                    surfaced_for_page.add(target_slug)
                break  # First matching phrase for this target is sufficient

    # Emit single batch forced-choice for all Tier 1 candidates
    if tier1_rows:
        # Build human-readable table for description field
        header = (
            f"Wikilink proliferation — {len(tier1_rows)} candidates across "
            f"{len({r['source_page'] for r in tier1_rows})} pages\n\n"
            "Row | Target slug | Source page | Context snippet\n"
            "----|-------------|-------------|----------------"
        )
        rows_text = "\n".join(
            f"{r['row']:3} | [[{r['target_slug']}]] | {r['source_page']} | "
            f"\"{r['snippet']}\""
            for r in tier1_rows
        )
        description = (
            f"{header}\n{rows_text}\n\n"
            "A) Apply all  B) Apply subset (range notation, e.g. 1-5,9)  "
            "C) Review by page  D) Skip"
        )
        add_finding(
            "L16", "forced-choice", None,
            description,
            {
                "candidates": tier1_rows,
                "total_candidates": len(tier1_rows),
                "affected_pages": sorted({r["source_page"] for r in tier1_rows}),
                "options": ["A", "B", "C", "D"],
                "option_b_subtype": "subset-select",
                "first_run_recommended": "C",
                "subsequent_recommended": "A",
            },
            recommended="C",  # Default for first run; agent should override to A on subsequent passes
        )


def check_L18a_claude_md_mirror_agreement(claude_md_text):
    """
    L18a: CLAUDE.md Sections 7.1/7.2 mirror agreement with vocabulary.json.

    vocabulary.json is authoritative for vocabulary values, labels, and covers
    text (DM-127). CLAUDE.md Sections 7.1-7.2 are a human-maintained mirror
    kept for control-document readability — this check verifies exact
    agreement in both directions: (a) id sets equal for both vocabularies;
    (b) for competency_domains, the CLAUDE.md covers cell string-equals the
    vocabulary.json covers value. Any mismatch is one informational finding.
    """
    if not claude_md_text:
        add_finding(
            "L18a", "informational", None,
            "CLAUDE.md not found or unreadable — cannot verify vocabulary mirror agreement.",
            {},
        )
        return

    cd_section = re.search(
        r"### 7\.1 Professional Competency Domains(.*?)### 7\.2 Professional Context Terms",
        claude_md_text, re.DOTALL,
    )
    pc_section = re.search(
        r"### 7\.2 Professional Context Terms(.*?)(?:### 7\.3|\Z)",
        claude_md_text, re.DOTALL,
    )
    if not cd_section or not pc_section:
        add_finding(
            "L18a", "informational", None,
            "CLAUDE.md Sections 7.1/7.2 not found in expected structure — "
            "cannot verify vocabulary mirror agreement.",
            {},
        )
        return

    remediation = (
        "edit the CLAUDE.md Section 7.1/7.2 mirror table or vocabulary.json so "
        "they agree — vocabulary.json is authoritative for values."
    )

    claude_cd = dict(re.findall(r"\|\s*`([a-z0-9-]+)`\s*\|\s*([^|]+?)\s*\|", cd_section.group(1)))
    claude_pc_ids = set(re.findall(r"\|\s*`([a-z0-9-]+)`\s*\|", pc_section.group(1)))

    vocab_cd = {e["id"]: e["covers"] for e in VOCABULARY["competency_domains"]}
    vocab_pc_ids = {e["id"] for e in VOCABULARY["professional_contexts"]}

    for missing_id in sorted(set(claude_cd) - set(vocab_cd)):
        add_finding(
            "L18a", "informational", None,
            f"competency_domains id '{missing_id}' present in CLAUDE.md Section 7.1 "
            "but not in vocabulary.json",
            {"id": missing_id, "field": "competency_domains", "side": "claude_md_only",
             "remediation": remediation},
        )
    for missing_id in sorted(set(vocab_cd) - set(claude_cd)):
        add_finding(
            "L18a", "informational", None,
            f"competency_domains id '{missing_id}' present in vocabulary.json "
            "but not in CLAUDE.md Section 7.1",
            {"id": missing_id, "field": "competency_domains", "side": "vocabulary_json_only",
             "remediation": remediation},
        )
    for shared_id in sorted(set(claude_cd) & set(vocab_cd)):
        if claude_cd[shared_id] != vocab_cd[shared_id]:
            add_finding(
                "L18a", "informational", None,
                f"competency_domains '{shared_id}' covers text differs between "
                "CLAUDE.md Section 7.1 and vocabulary.json",
                {"id": shared_id, "field": "covers",
                 "claude_md_value": claude_cd[shared_id],
                 "vocabulary_json_value": vocab_cd[shared_id],
                 "remediation": remediation},
            )

    for missing_id in sorted(claude_pc_ids - vocab_pc_ids):
        add_finding(
            "L18a", "informational", None,
            f"professional_contexts id '{missing_id}' present in CLAUDE.md Section 7.2 "
            "but not in vocabulary.json",
            {"id": missing_id, "field": "professional_contexts", "side": "claude_md_only",
             "remediation": remediation},
        )
    for missing_id in sorted(vocab_pc_ids - claude_pc_ids):
        add_finding(
            "L18a", "informational", None,
            f"professional_contexts id '{missing_id}' present in vocabulary.json "
            "but not in CLAUDE.md Section 7.2",
            {"id": missing_id, "field": "professional_contexts", "side": "vocabulary_json_only",
             "remediation": remediation},
        )


def check_L18b_generated_artifact_consistency():
    """
    L18b: generated-block agreement with vocabulary.json, via
    `python3 generate-vocab-artifacts.py --check`.

    Exit-code contract (vocabulary-json-refactor-spec.md Section 4.4 item 5):
      0 — in sync: no finding.
      1 — drift: informational finding with mandatory remediation.
      2 — fatal: wiki-lint.py itself exits fatally, mirroring the loader's
          fail-fast posture (missing/duplicated markers or invalid vocabulary.json).
    """
    script = "generate-vocab-artifacts.py"
    if not os.path.exists(script):
        sys.exit(
            f"FATAL: {script} not found at repo root — cannot verify generated "
            "vocabulary artifact consistency (DM-127)."
        )

    try:
        result = subprocess.run(
            [sys.executable, script, "--check"],
            capture_output=True, text=True,
        )
    except OSError as exc:
        sys.exit(f"FATAL: could not run {script} --check: {exc}")

    if result.returncode == 0:
        return
    if result.returncode == 1:
        add_finding(
            "L18b", "informational", None,
            "Generated vocabulary artifacts are out of sync with vocabulary.json.",
            {
                "stdout": result.stdout.strip(),
                "remediation": "run python3 generate-vocab-artifacts.py and commit the regenerated files",
            },
        )
        return
    sys.exit(
        f"FATAL: {script} --check exited {result.returncode} — vocabulary.json "
        f"or a generated-block marker is invalid.\n{result.stderr.strip()}"
    )


# ─── Findings File Writer ─────────────────────────────────────────────────────

def write_findings_file(wiki_stats):
    """Serialize findings and agent_review to raw/lint-findings.json."""
    os.makedirs("raw", exist_ok=True)
    output = {
        "lint_date": TODAY.isoformat(),
        "script_version": SCRIPT_VERSION,
        "wiki_stats": wiki_stats,
        "findings": findings,
        "agent_review": agent_review,
    }
    path = os.path.join("raw", "lint-findings.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, default=str)
    return path


# ─── Summary Output ───────────────────────────────────────────────────────────

def print_summary():
    """Print human-readable summary to stdout."""
    by_type = defaultdict(lambda: defaultdict(int))
    for f in findings:
        by_type[f["type"]][f["step"]] += 1

    total = len(findings)
    forced = sum(1 for f in findings if f["type"] == "forced-choice")
    auto = sum(1 for f in findings if f["type"] == "auto-execute")
    info = sum(1 for f in findings if f["type"] == "informational")
    errors = sum(1 for f in findings if f["type"] == "error")

    print(f"\n=== wiki-lint.py — {TODAY} ===")
    print(f"Total findings: {total}  (forced-choice: {forced}, auto-execute: {auto}, "
          f"informational: {info}, errors: {errors})")
    print(f"Agent-review items: {len(agent_review)}")

    if forced > 0:
        print("\nForced-choice findings by step:")
        for f in findings:
            if f["type"] == "forced-choice":
                print(f"  [{f['step']}] {f['description'][:100]}")

    if auto > 0:
        print("\nAuto-execute findings by step:")
        for f in findings:
            if f["type"] == "auto-execute":
                print(f"  [{f['step']}] {f['description'][:100]}")

    if errors > 0:
        print("\nErrors:")
        for f in findings:
            if f["type"] == "error":
                print(f"  [{f['step']}] {f['description']}")

    print(f"\nFindings written to: raw/lint-findings.json")


# ─── Main Entry Point ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="wiki-lint.py — mechanical lint checks for the AI Effectiveness Wiki"
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Print per-page processing details and support score calculation",
    )
    args = parser.parse_args()

    # Entrypoint guard
    if not os.path.exists("overview.md"):
        print("ABORT: overview.md not found in current directory. "
              "Run from the wiki repository root.", file=sys.stderr)
        sys.exit(1)

    verbose = args.verbose

    # ── Pre-computation: build valid slug set ──────────────────────────────
    valid_slugs, slug_to_path = build_valid_slug_set()

    # ── Read singletons ────────────────────────────────────────────────────
    def read_file(path):
        try:
            with open(path, encoding="utf-8") as f:
                return f.read()
        except OSError:
            return ""

    overview_text = read_file("overview.md")
    index_text = read_file("index.md")
    queue_text = read_file("raw/queue.md")
    log_text = read_file("log.md")
    wll_text = read_file("wiki-lessons-learned.md")
    claude_md_text = read_file("CLAUDE.md")

    overview_fm, _ = parse_frontmatter(overview_text)
    last_lint_raw = overview_fm.get("last_lint")
    last_lint_date = last_lint_raw if isinstance(last_lint_raw, date) else None

    # ── Group A ────────────────────────────────────────────────────────────
    if verbose:
        print("\n[Group A] Singleton checks...")

    ctrd_signals = check_L1_ctrd_signals(queue_text)
    check_L1a_nomination_aging(queue_text)
    entries_by_type, index_slugs = check_L2_and_G2_page_inventory(
        index_text, valid_slugs, slug_to_path
    )

    # ── Group B ────────────────────────────────────────────────────────────
    if verbose:
        print("\n[Group B] Per-page checks...")

    (
        entity_pages_fm,
        inbound_links,
        open_contradictions_count,
        teaching_tagged_count,
        topic_tool_count,
        topic_tool_deprecated_count,
        source_slugs,
        all_ctrd_ids,
        page_claims,
        page_prose,
        page_data_records,
        page_meta,
    ) = read_and_check_all_pages(
        valid_slugs, slug_to_path, ctrd_signals, last_lint_date, verbose
    )

    # ── Verify CTRD signals from L1 match open contradictions ─────────────
    for ctrd_id, signal_type in ctrd_signals.items():
        found = any(
            any(isinstance(e, dict) and e.get("id") == ctrd_id
                for e in (fm.get("open_contradictions") or []))
            for fm in entity_pages_fm.values()
        )
        if not found:
            add_finding(
                "L1", "informational", None,
                f"Stale override signal — no matching open contradiction found: {ctrd_id}",
                {"ctrd_id": ctrd_id, "signal_type": signal_type, "issue": "stale_signal"},
            )

    # ── Group C ────────────────────────────────────────────────────────────────
    if verbose:
        print("\n[Group C] Cross-page computation...")

    source_info = build_source_info()
    counts_by_type = entries_by_type
    total_indexed = sum(len(v) for v in counts_by_type.values())

    claims_list, records_list = check_L19_extraction_and_serialization(
        page_claims, page_data_records, page_meta, source_info
    )
    check_L20_contradiction_prescreen(claims_list, records_list)
    check_L3_support_scores(page_claims, source_info, verbose)
    check_L4c_and_G4_counters(
        open_contradictions_count, all_ctrd_ids, overview_fm, total_indexed
    )
    check_L10_teaching_ratio(
        teaching_tagged_count, topic_tool_count, topic_tool_deprecated_count
    )
    check_L12_collection_gaps(log_text, read_file("raw/collection-gaps.md"))
    check_L12a_session_stats(log_text)
    check_L12b_deferred_ingest()
    check_L12c_override_patterns(wll_text)
    check_L12d_schema_signals_age(wll_text)
    check_L14_skill_enrichment(log_text)
    check_L7_concept_gaps(page_prose, index_slugs, valid_slugs)
    check_L9_decay_exempt(page_claims, source_info, log_text)
    check_L16_wikilink_proliferation(entity_pages_fm, valid_slugs, slug_to_path, page_prose)
    check_L18a_claude_md_mirror_agreement(claude_md_text)
    check_L18b_generated_artifact_consistency()

    # ── Build wiki_stats for findings file ─────────────────────────────────
    # (counts_by_type and total_indexed already computed above)
    pages_by_directory = {}
    for d in CONTENT_DIRS:
        if os.path.isdir(d):
            pages_by_directory[d] = sum(1 for f in os.listdir(d) if f.endswith(".md"))
        else:
            pages_by_directory[d] = 0

    wiki_stats = {
        "total_pages": total_indexed,
        "pages_by_type": {k: len(v) for k, v in counts_by_type.items()},
        "pages_by_directory": pages_by_directory,
        "overview_fields": {
            "total_pages": overview_fm.get("total_pages"),
            "total_sources": overview_fm.get("total_sources"),
            "open_contradictions": overview_fm.get("open_contradictions"),
            "last_contradiction_id": overview_fm.get("last_contradiction_id"),
            "last_lint": str(last_lint_date) if last_lint_date else None,
        },
        "accumulated": {
            "open_contradictions_count": open_contradictions_count,
            "teaching_tagged_count": teaching_tagged_count,
            "topic_tool_count": topic_tool_count,
            "topic_tool_deprecated_count": topic_tool_deprecated_count,
            "all_ctrd_ids": sorted(all_ctrd_ids),
        },
    }

    # ── Write findings file ────────────────────────────────────────────────
    path = write_findings_file(wiki_stats)

    # ── Print summary ──────────────────────────────────────────────────────
    print_summary()

    return 0


if __name__ == "__main__":
    sys.exit(main())
