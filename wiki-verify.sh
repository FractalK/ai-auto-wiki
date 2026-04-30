#!/usr/bin/env bash
# Last Updated: 30/04/2026 15:00
# wiki-verify.sh — Tier 1 configuration, conformance, and content-level checks
# AI Effectiveness Wiki — see test-harness.md for specification
#
# Usage:
#   bash wiki-verify.sh
#
# Run from the wiki repository root (the directory containing CLAUDE.md).
# Read-only: this script makes no changes to any file.
#
# Exit codes:
#   0 — all checks passed (PASS or WARN only)
#   1 — at least one check failed (FAIL)
#
# Environmental assumptions:
#   - bash 3.2+ (macOS system bash compatible; no bash 4+ features used)
#   - Standard POSIX tools: grep, find, wc, awk, ls (no yq, python, node)
#   - Executed from the wiki repository root (directory containing CLAUDE.md)
#   - .git/ directory present (initialized git repository)
#
# Limitations:
#   - YAML field checks use grep, not a YAML parser. Field presence is
#     confirmed; type validation for integers uses a numeric regex only.
#   - quartz.config.ts ignorePatterns checks confirm string presence anywhere in the
#     file, not specifically within the ignorePatterns array. The baseUrl check is
#     narrowed to lines containing "baseUrl" to avoid false positives from commented-out
#     examples elsewhere in the file.
#   - "index.md" absence check emits WARN (not FAIL) because the string may
#     legitimately appear in a comment explaining NOT to add it.
#   - Pre-commit hook is inspected for expected content, not executed.

# ─── Output helpers ──────────────────────────────────────────────────────────
PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

pass() { printf "[PASS] %s\n" "$1"; PASS_COUNT=$((PASS_COUNT + 1)); }
fail() { printf "[FAIL] %s\n" "$1"; FAIL_COUNT=$((FAIL_COUNT + 1)); }
warn() { printf "[WARN] %s\n" "$1"; WARN_COUNT=$((WARN_COUNT + 1)); }

# ─── Utilities ───────────────────────────────────────────────────────────────
# yaml_field_present FILE FIELD — true if "FIELD:" appears as a top-level key
yaml_field_present() {
    grep -qE "^$2:" "$1" 2>/dev/null
}

# yaml_value FILE FIELD — print the scalar value after "FIELD:"
yaml_value() {
    grep -E "^$2:" "$1" 2>/dev/null | awk '{print $2}' | head -1
}

# is_integer VALUE — true if VALUE is a non-negative integer
is_integer() {
    echo "$1" | grep -qE '^[0-9]+$'
}

# check_scaffold_fields FILE FIELD... — PASS/FAIL each required frontmatter field
check_scaffold_fields() {
    local file="$1"; shift
    for field in "$@"; do
        if yaml_field_present "$file" "$field"; then
            pass "$file: field '$field' present"
        else
            fail "$file: missing required field '$field'"
        fi
    done
}

# check_integer_field FILE FIELD — confirm field is a non-negative integer
check_integer_field() {
    local file="$1" field="$2"
    local val
    val=$(yaml_value "$file" "$field")
    if is_integer "$val"; then
        pass "$file: $field is integer ($val)"
    else
        fail "$file: $field is not a valid integer (got: '$val')"
    fi
}

# check_yaml_value FILE FIELD EXPECTED — confirm field has an exact expected value
check_yaml_value() {
    local file="$1" field="$2" expected="$3"
    local val
    val=$(yaml_value "$file" "$field")
    if [ "$val" = "$expected" ]; then
        pass "$file: $field = $expected"
    else
        fail "$file: $field = '$val', expected '$expected'"
    fi
}

# ─── Entrypoint guard ────────────────────────────────────────────────────────
printf "\n=== Wiki Conformance Check — %s ===\n" "$(date '+%Y-%m-%d %H:%M:%S')"
printf "Working directory: %s\n\n" "$(pwd)"

if [ ! -f "CLAUDE.md" ]; then
    printf "[ABORT] CLAUDE.md not found in current directory.\n"
    printf "        Run this script from the wiki repository root.\n"
    exit 1
fi

# ─── 1. quartz.config.ts ────────────────────────────────────────────────────
printf "--- 1. quartz.config.ts ---\n"

if [ ! -f "quartz.config.ts" ]; then
    fail "quartz.config.ts not found"
else
    pass "quartz.config.ts exists"

    # All 17 required ignorePatterns entries (CLAUDE.md Section 2 [ENV])
    REQUIRED_PATTERNS=(
        '"CLAUDE.md"'
        '"EXTRACTION-SKILL.md"'
        '"TAGGING-SKILL.md"'
        '"CONTRADICTION-SKILL.md"'
        '"wiki-lessons-learned.md"'
        '"assets/**"'
        '"raw/**"'
        '"docs/**"'
        '"content/**"'
        '"prompts/**"'
        '"node_modules/**"'
        '"INIT-PROMPT.md"'
        '"public/**"'
        '"overview.md"'
        '"log.md"'
        '"design/**"'
        '"OPERATIONS.md"'
    )

    for pat in "${REQUIRED_PATTERNS[@]}"; do
        if grep -qF "$pat" quartz.config.ts; then
            pass "ignorePatterns contains $pat"
        else
            fail "ignorePatterns missing $pat"
        fi
    done

    # "index.md" must NOT be excluded — Quartz requires it for index.html
    # Use WARN: the string may appear in a comment explaining not to add it
    if grep -qF '"index.md"' quartz.config.ts; then
        warn '"index.md" appears in quartz.config.ts — confirm it is in a comment only, NOT in ignorePatterns (excluding it replaces index.html with index.xml)'
    else
        pass '"index.md" not present as an excluded path'
    fi

    # baseUrl must not be the default Quartz placeholder.
    # Narrow to lines containing "baseUrl" to avoid matching commented-out
    # examples or other strings elsewhere in the file.
    if grep 'baseUrl' quartz.config.ts | grep -qF 'quartz.jzhao.xyz'; then
        fail 'baseUrl still contains default placeholder "quartz.jzhao.xyz" — set to your GitHub Pages URL before publishing'
    else
        pass 'baseUrl does not contain default Quartz placeholder'
    fi
fi

# ─── 2. .gitignore ──────────────────────────────────────────────────────────
printf "\n--- 2. .gitignore ---\n"

if [ ! -f ".gitignore" ]; then
    fail ".gitignore not found"
else
    pass ".gitignore exists"

    # Required entries per INIT-PROMPT.md Step 8 and portability-review.md GIT-06
    for entry in "raw/staged/" "raw/processed/" "!**/.gitkeep"; do
        if grep -qF "$entry" .gitignore; then
            pass ".gitignore contains: $entry"
        else
            fail ".gitignore missing: $entry"
        fi
    done
fi

# ─── 3. Pre-commit hook ─────────────────────────────────────────────────────
printf "\n--- 3. Pre-commit hook ---\n"

HOOK=".git/hooks/pre-commit"

if [ ! -f "$HOOK" ]; then
    fail "Pre-commit hook not found: $HOOK"
else
    pass "Pre-commit hook file exists"

    if [ -x "$HOOK" ]; then
        pass "Pre-commit hook is executable"
    else
        fail "Pre-commit hook is not executable (fix: chmod +x $HOOK)"
    fi

    # Hook should cover all wiki content directories including teaching/
    if grep -qF "topics tools sources comparisons pitfalls teaching" "$HOOK"; then
        pass "Pre-commit hook targets all wiki content directories"
    else
        warn "Pre-commit hook may not cover all wiki content directories — expected: topics tools sources comparisons pitfalls teaching"
    fi

    # Hook should contain the uppercase/space rejection pattern [A-Z ]
    if grep -qF '[A-Z ]' "$HOOK"; then
        pass "Pre-commit hook contains uppercase/space rejection pattern"
    else
        warn "Pre-commit hook does not appear to contain [A-Z ] rejection pattern"
    fi
fi

# ─── 4. Scaffold file conformance ───────────────────────────────────────────
printf "\n--- 4. Scaffold file conformance ---\n"

# overview.md
if [ ! -f "overview.md" ]; then
    fail "overview.md not found"
else
    pass "overview.md exists"
    check_yaml_value "overview.md" "type" "overview"
    check_scaffold_fields "overview.md" title created updated \
        total_pages total_sources open_contradictions last_contradiction_id
    check_integer_field "overview.md" "total_pages"
    check_integer_field "overview.md" "total_sources"
    check_integer_field "overview.md" "open_contradictions"
    check_integer_field "overview.md" "last_contradiction_id"
fi

# log.md
if [ ! -f "log.md" ]; then
    fail "log.md not found"
else
    pass "log.md exists"
    check_yaml_value "log.md" "type" "log"
    check_scaffold_fields "log.md" title created updated last_entry entry_count
    check_integer_field "log.md" "entry_count"
fi

# index.md
if [ ! -f "index.md" ]; then
    fail "index.md not found"
else
    pass "index.md exists"
    check_yaml_value "index.md" "type" "index"
    check_scaffold_fields "index.md" title created updated
fi

# teaching-index.md
if [ ! -f "teaching-index.md" ]; then
    fail "teaching-index.md not found"
else
    pass "teaching-index.md exists"
    check_yaml_value "teaching-index.md" "type" "teaching-index"
    check_scaffold_fields "teaching-index.md" title created updated
fi

# wiki-lessons-learned.md
if [ ! -f "wiki-lessons-learned.md" ]; then
    fail "wiki-lessons-learned.md not found"
else
    pass "wiki-lessons-learned.md exists"
    check_yaml_value "wiki-lessons-learned.md" "type" "wiki-lessons-learned"
    check_scaffold_fields "wiki-lessons-learned.md" title created updated last_entry entry_count
    check_integer_field "wiki-lessons-learned.md" "entry_count"
    # Required operation-type section headers (CLAUDE.md Section 5.9)
    for section in "## Ingest" "## Contradiction" "## Tagging" "## Lint" "## Query" "## Schema Signals"; do
        if grep -qF "$section" wiki-lessons-learned.md; then
            pass "wiki-lessons-learned.md contains section: $section"
        else
            fail "wiki-lessons-learned.md missing section: $section"
        fi
    done
fi

# raw/queue.md — required sections (CLAUDE.md Section 2.1)
if [ ! -f "raw/queue.md" ]; then
    fail "raw/queue.md not found"
else
    pass "raw/queue.md exists"
    for section in "## [queued]" "## [nominated]" "## [stale-nominated]" "## [processed]"; do
        if grep -qF "$section" raw/queue.md; then
            pass "raw/queue.md contains section: $section"
        else
            fail "raw/queue.md missing section: $section"
        fi
    done
fi

# raw/collection-gaps.md and raw/discovery-sources.md — existence only
for rawfile in "raw/collection-gaps.md" "raw/discovery-sources.md"; do
    if [ -f "$rawfile" ]; then
        pass "$rawfile exists"
    else
        fail "$rawfile not found"
    fi
done

# Operational skill files — existence only
for skillfile in "EXTRACTION-SKILL.md" "TAGGING-SKILL.md" "CONTRADICTION-SKILL.md" "INIT-PROMPT.md" "OPERATIONS.md"; do
    if [ -f "$skillfile" ]; then
        pass "$skillfile exists"
    else
        fail "$skillfile not found"
    fi
done

# ─── 5. Page count consistency ──────────────────────────────────────────────
printf "\n--- 5. Page count consistency ---\n"

ACTUAL_COUNT=0
for d in topics tools sources comparisons pitfalls teaching; do
    if [ -d "$d" ]; then
        count=$(find "$d" -maxdepth 1 -name "*.md" | wc -l | tr -d '[:space:]')
        ACTUAL_COUNT=$((ACTUAL_COUNT + count))
    fi
done

if [ -f "overview.md" ]; then
    RECORDED=$(yaml_value "overview.md" "total_pages")
    if [ "$RECORDED" = "$ACTUAL_COUNT" ]; then
        pass "total_pages consistent: overview.md=$RECORDED, actual count in content dirs=$ACTUAL_COUNT"
    else
        fail "total_pages mismatch: overview.md=$RECORDED, actual count in content dirs=$ACTUAL_COUNT"
    fi
else
    warn "Cannot check page count — overview.md not found (already reported above)"
fi

# ─── 6. Naming convention ───────────────────────────────────────────────────
printf "\n--- 6. Naming convention (no uppercase or spaces in content dir filenames) ---\n"

NAMING_FAIL=0
for d in topics tools sources comparisons pitfalls teaching; do
    if [ -d "$d" ]; then
        # Find .md files in this dir with uppercase letters or spaces in the basename
        while IFS= read -r filepath; do
            basename_only=$(basename "$filepath")
            if echo "$basename_only" | grep -qE '[A-Z ]'; then
                fail "Filename convention violation: $filepath"
                NAMING_FAIL=1
            fi
        done < <(find "$d" -name "*.md" 2>/dev/null)
    fi
done

if [ "$NAMING_FAIL" = "0" ]; then
    pass "No naming convention violations found in content directories"
fi

# ─── 7. No stray .md files at wiki root ─────────────────────────────────────
printf "\n--- 7. Stray .md files at wiki root ---\n"

# The complete list of .md files permitted at the wiki root
ALLOWED_ROOT=(
    "CLAUDE.md"
    "OPERATIONS.md"
    "EXTRACTION-SKILL.md"
    "TAGGING-SKILL.md"
    "CONTRADICTION-SKILL.md"
    "wiki-lessons-learned.md"
    "INIT-PROMPT.md"
    "index.md"
    "overview.md"
    "log.md"
    "teaching-index.md"
)

STRAY_FAIL=0
while IFS= read -r filepath; do
    fname=$(basename "$filepath")
    allowed=0
    for a in "${ALLOWED_ROOT[@]}"; do
        if [ "$fname" = "$a" ]; then
            allowed=1
            break
        fi
    done
    if [ "$allowed" = "0" ]; then
        fail "Stray .md file at wiki root: $fname"
        STRAY_FAIL=1
    fi
done < <(find . -maxdepth 1 -name "*.md" 2>/dev/null | sed 's|^\./||' | sort)

if [ "$STRAY_FAIL" = "0" ]; then
    pass "No stray .md files at wiki root"
fi

# ─── 8. Teaching-brief page conformance ─────────────────────────────────────
printf "\n--- 8. Teaching-brief page conformance ---\n"
# Every file in teaching/ must be type: teaching-brief with all required
# frontmatter fields (Section 5.10). teaching_relevance is hardcoded true.

if [ ! -d "teaching" ]; then
    warn "teaching/ directory not found — no teaching-brief pages to check"
else
    TB_COUNT=0
    while IFS= read -r filepath; do
        TB_COUNT=$((TB_COUNT + 1))
        check_yaml_value   "$filepath" "type"               "teaching-brief"
        check_yaml_value   "$filepath" "teaching_relevance" "true"
        check_scaffold_fields "$filepath" \
            title created updated status query_date derived_from \
            last_reviewed competency_domains professional_contexts
    done < <(find "teaching" -maxdepth 1 -name "*.md" 2>/dev/null)

    if [ "$TB_COUNT" = "0" ]; then
        pass "teaching/ directory is empty — no teaching-brief pages to check"
    fi
fi

# ─── 9. YAML wikilink quoting ────────────────────────────────────────────────
printf "\n--- 9. YAML wikilink quoting (FRIC-032 regression) ---\n"
# All [[wikilinks]] in YAML frontmatter must be quoted as "[[slug]]".
# Unquoted wikilinks parse as nested YAML flow sequences, breaking Obsidian
# Properties rendering and Quartz link resolution (CLAUDE.md Section 5 preamble).
# Uses awk to limit scanning to the frontmatter block (between the first and
# second --- delimiters), avoiding false positives from prose body bullets.
# Two patterns:
#   block-list items:  - [[slug]]      (should be: - "[[slug]]")
#   single-value fields: field: [[slug]]  (should be: field: "[[slug]]")
# Known limitation: a file using --- inside a YAML string value may mis-scope
# the frontmatter boundary. Not a realistic risk given wiki frontmatter structure.

WL_FAIL=0
for d in topics tools sources comparisons pitfalls teaching; do
    [ -d "$d" ] || continue
    while IFS= read -r filepath; do
        result=$(awk '
            /^---/ { delim++; next }
            delim == 1 && /^[[:space:]]*-[[:space:]]+\[\[/ { print NR": "$0 }
            delim == 1 && /^[a-z_]+:[[:space:]]+\[\[/     { print NR": "$0 }
        ' "$filepath")
        if [ -n "$result" ]; then
            fail "Unquoted wikilink in YAML frontmatter: $filepath"
            while IFS= read -r wl_line; do
                printf "         %s\n" "$wl_line"
            done <<< "$result"
            WL_FAIL=1
        fi
    done < <(find "$d" -maxdepth 1 -name "*.md" 2>/dev/null)
done

if [ "$WL_FAIL" = "0" ]; then
    pass "No unquoted wikilinks found in YAML frontmatter"
fi

# ─── 10. Pitfalls <br> conformance ──────────────────────────────────────────
printf "\n--- 10. Pitfalls <br> conformance (FRIC-030 regression) ---\n"
# Quartz (CommonMark) does not treat a single newline as a hard line break.
# Every **Status:** line in a Pitfalls failure mode entry must end with <br>
# (CLAUDE.md Section 5.6). grep pattern matches the bold body label only —
# the YAML 'status:' frontmatter field uses no asterisks and is not matched.

if [ ! -d "pitfalls" ]; then
    pass "pitfalls/ directory not found — no pitfalls pages to check"
else
    BR_FAIL=0
    while IFS= read -r filepath; do
        result=$(grep -n '\*\*Status:\*\*' "$filepath" 2>/dev/null | grep -v '<br>')
        if [ -n "$result" ]; then
            fail "Missing <br> after **Status:** in pitfalls page: $filepath"
            while IFS= read -r br_line; do
                printf "         %s\n" "$br_line"
            done <<< "$result"
            BR_FAIL=1
        fi
    done < <(find "pitfalls" -maxdepth 1 -name "*.md" 2>/dev/null)

    if [ "$BR_FAIL" = "0" ]; then
        pass "All **Status:** lines in pitfalls pages include <br>"
    fi
fi

# ─── 11. Comparison Verdict section ─────────────────────────────────────────
printf "\n--- 11. Comparison Verdict section (DM-087) ---\n"
# Every Comparison page must contain a ## Verdict section (CLAUDE.md Section 5.5,
# DM-087). The Verdict is always producible from Key Claims; its absence signals
# an incomplete or pre-DM-087 page that was not retroactively fixed.

if [ ! -d "comparisons" ]; then
    pass "comparisons/ directory not found — no comparison pages to check"
else
    VD_FAIL=0
    while IFS= read -r filepath; do
        if ! grep -qF '## Verdict' "$filepath" 2>/dev/null; then
            fail "Comparison page missing required ## Verdict section: $filepath"
            VD_FAIL=1
        fi
    done < <(find "comparisons" -maxdepth 1 -name "*.md" 2>/dev/null)

    if [ "$VD_FAIL" = "0" ]; then
        pass "All comparison pages contain ## Verdict section"
    fi
fi

# ─── 12. Dollar sign escaping ────────────────────────────────────────────────
printf "\n--- 12. Dollar sign escaping (FRIC-029 regression) ---\n"
# Quartz renders \$...\$ as LaTeX inline math. All bare dollar signs before
# digits must be escaped as \$ in wiki content (CLAUDE.md Section 6.2).
# Step 1: grep for lines containing a literal $ followed by a digit.
# Step 2: filter out lines that already contain \$ (the correctly escaped form).
# Severity: WARN — dollar signs in code blocks may produce false positives.
# Known limitation: a line containing both \$20 (escaped) and $30 (unescaped)
# may be excluded by the filter on the escaped match. Review all flagged lines.

DS_WARN=0
for d in topics tools sources comparisons pitfalls teaching; do
    [ -d "$d" ] || continue
    while IFS= read -r filepath; do
        result=$(grep -nE '\$[0-9]' "$filepath" 2>/dev/null | grep -v '\\\$')
        if [ -n "$result" ]; then
            warn "Possible unescaped dollar sign (use \\$ per Section 6.2): $filepath"
            while IFS= read -r ds_line; do
                printf "         %s\n" "$ds_line"
            done <<< "$result"
            DS_WARN=1
        fi
    done < <(find "$d" -maxdepth 1 -name "*.md" 2>/dev/null)
done

if [ "$DS_WARN" = "0" ]; then
    pass "No bare dollar signs before digits found in content pages"
fi

# ─── 13. teaching_notes_reviewed field presence ──────────────────────────────
printf "\n--- 13. teaching_notes_reviewed field presence (Section 5.2/5.3) ---\n"
# Topic and Tool pages with teaching_relevance: true that contain a
# ## Teaching Notes body section must also have teaching_notes_reviewed in
# frontmatter (CLAUDE.md Sections 5.2/5.3). Severity: WARN — lint Step L5b
# is the authoritative backstop; this check provides an earlier warning signal.
# Note: grep -qF '## Teaching Notes' matches the body section header only;
# this string does not appear in YAML frontmatter.

TNR_WARN=0
for d in topics tools; do
    [ -d "$d" ] || continue
    while IFS= read -r filepath; do
        tr_val=$(yaml_value "$filepath" "teaching_relevance")
        if [ "$tr_val" = "true" ]; then
            if grep -qF '## Teaching Notes' "$filepath" 2>/dev/null; then
                if ! yaml_field_present "$filepath" "teaching_notes_reviewed"; then
                    warn "Teaching-tagged page has ## Teaching Notes but missing 'teaching_notes_reviewed' frontmatter field: $filepath"
                    TNR_WARN=1
                fi
            fi
        fi
    done < <(find "$d" -maxdepth 1 -name "*.md" 2>/dev/null)
done

if [ "$TNR_WARN" = "0" ]; then
    pass "All teaching-tagged pages with ## Teaching Notes have teaching_notes_reviewed field"
fi

# ─── Summary ─────────────────────────────────────────────────────────────────
printf "\n=== Summary ===\n"
printf "PASS: %d   FAIL: %d   WARN: %d\n" "$PASS_COUNT" "$FAIL_COUNT" "$WARN_COUNT"

if [ "$FAIL_COUNT" -gt 0 ]; then
    printf "\nResult: FAIL — %d check(s) failed. Resolve before first ingest.\n" "$FAIL_COUNT"
    exit 1
elif [ "$WARN_COUNT" -gt 0 ]; then
    printf "\nResult: WARN — all hard checks passed; %d warning(s) require review.\n" "$WARN_COUNT"
    exit 0
else
    printf "\nResult: PASS — all checks passed.\n"
    exit 0
fi
