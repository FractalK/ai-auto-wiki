#!/usr/bin/env python3
"""
generate-vocab-artifacts.py — regenerate the vocabulary blocks in
TAGGING-SKILL.md and ingest-ui-template.html from vocabulary.json.

Run from the wiki repository root (the directory containing vocabulary.json).

Usage:
    python3 generate-vocab-artifacts.py            # regenerate and write changed files
    python3 generate-vocab-artifacts.py --check     # compare only; write nothing

Exit codes:
    0 — default mode: files written (or already up to date).
        --check mode: both target files already match vocabulary.json.
    1 — --check mode only: at least one target file is out of sync.
    2 — fatal: vocabulary.json missing/invalid, or a marker pair is missing,
        duplicated, or out of order in a target file.

vocabulary.json (repo root) is the single source of truth for the
`competency_domains` and `professional_contexts` controlled vocabularies
(CLAUDE.md Sections 7.1-7.2, DM-127). This script is the only code that
renders that source into the generated blocks in TAGGING-SKILL.md and
ingest-ui-template.html — do not hand-edit content between the
BEGIN/END GENERATED VOCABULARY markers in either file.

Environmental assumptions:
    - Python 3.9+ (zoneinfo is stdlib from 3.9)
    - Standard library only — no external packages
    - Executed from the wiki repository root
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover - guarded by the 3.9+ environmental assumption
    ZoneInfo = None

VOCAB_FILE = "vocabulary.json"
TAGGING_SKILL_FILE = "TAGGING-SKILL.md"
INGEST_UI_FILE = "ingest-ui-template.html"

TAGGING_BEGIN_MARKER = (
    "<!-- BEGIN GENERATED VOCABULARY — source: vocabulary.json; "
    "do not edit by hand; run: python3 generate-vocab-artifacts.py -->"
)
TAGGING_END_MARKER = "<!-- END GENERATED VOCABULARY -->"

HTML_BEGIN_MARKER = (
    "// BEGIN GENERATED VOCABULARY — source: vocabulary.json; "
    "do not edit by hand; run: python3 generate-vocab-artifacts.py"
)
HTML_END_MARKER = "// END GENERATED VOCABULARY"

ID_PATTERN = re.compile(r"^[a-z0-9-]+$")


class VocabularyError(Exception):
    """Raised for any defect in vocabulary.json or a target file's marker block.

    Callers catch this at the top level, print the message to stderr, and
    exit 2 — the fail-fast contract shared with wiki-lint.py's loader.
    """


# ── vocabulary.json loading and validation ─────────────────────────────────


def load_and_validate_vocabulary(path=VOCAB_FILE):
    """
    Load, parse, and validate vocabulary.json.

    Validation rules (mirrors wiki-lint.py's load_vocabulary loader, plus two
    checks unique to this generator — FD-4 character prohibition and
    duplicate-id rejection — since this script is the last line of defense
    before those values are rendered into two other files):
      - file must exist and parse as JSON
      - competency_domains / professional_contexts must be present, non-empty lists
      - every entry must have a kebab-case id (^[a-z0-9-]+$) and a non-empty label
      - no backslash or embedded double-quote in id/label/covers (FD-4)
      - no duplicate ids within either list

    Returns the parsed dict on success. Raises VocabularyError on any defect.

    Example:
        >>> vocab = load_and_validate_vocabulary("vocabulary.json")
        >>> len(vocab["competency_domains"])
        7
    """
    if not os.path.exists(path):
        raise VocabularyError(
            f"{path} not found at repo root. It is the controlled-vocabulary "
            "source of truth (DM-127)."
        )

    with open(path, encoding="utf-8") as f:
        try:
            vocab = json.load(f)
        except json.JSONDecodeError as exc:
            raise VocabularyError(f"{path} is not valid JSON: {exc}") from exc

    for key in ("competency_domains", "professional_contexts"):
        entries = vocab.get(key)
        if not isinstance(entries, list) or not entries:
            raise VocabularyError(f"{path} key '{key}' missing or empty.")

        seen_ids = set()
        for entry in entries:
            entry_id = entry.get("id", "")
            label = entry.get("label", "")
            covers = entry.get("covers", "")

            if not ID_PATTERN.fullmatch(entry_id):
                raise VocabularyError(
                    f"{path} '{key}' entry has a missing or non-kebab-case id: {entry!r}"
                )
            if not label:
                raise VocabularyError(f"{path} entry {entry_id!r} is missing a label.")
            for field_name, value in (
                ("id", entry_id),
                ("label", label),
                ("covers", covers),
            ):
                if "\\" in value or '"' in value:
                    raise VocabularyError(
                        f"{path} entry {entry_id!r} field '{field_name}' contains a "
                        "backslash or embedded double quote (FD-4 violation)."
                    )
            if entry_id in seen_ids:
                raise VocabularyError(
                    f"{path} '{key}' contains duplicate id: {entry_id!r}"
                )
            seen_ids.add(entry_id)

    return vocab


# ── Rendering ────────────────────────────────────────────────────────────────


def render_tagging_skill_block(vocab):
    """
    Render the TAGGING-SKILL.md Section 1.1/1.2 vocabulary tables.

    Pure function of the vocabulary dict — no file I/O. Matches the table
    structure that predates this generator: domains carry a Covers column,
    contexts are a single-column list, both under "use exactly as shown"
    headers.

    Example:
        >>> vocab = {"competency_domains": [{"id": "a", "label": "A", "covers": "c"}],
        ...          "professional_contexts": [{"id": "b", "label": "B"}]}
        >>> print(render_tagging_skill_block(vocab))
        ### 1.1 Professional Competency Domains
        <BLANKLINE>
        | Value (use exactly as shown) | Covers |
        |---|---|
        | `a` | c |
        <BLANKLINE>
        ### 1.2 Professional Context Terms
        <BLANKLINE>
        | Value (use exactly as shown) |
        |---|
        | `b` |
    """
    lines = ["### 1.1 Professional Competency Domains", ""]
    lines.append("| Value (use exactly as shown) | Covers |")
    lines.append("|---|---|")
    for entry in vocab["competency_domains"]:
        lines.append(f"| `{entry['id']}` | {entry['covers']} |")
    lines.append("")
    lines.append("### 1.2 Professional Context Terms")
    lines.append("")
    lines.append("| Value (use exactly as shown) |")
    lines.append("|---|")
    for entry in vocab["professional_contexts"]:
        lines.append(f"| `{entry['id']}` |")
    return "\n".join(lines)


def render_ingest_ui_block(vocab):
    """
    Render the ingest-ui-template.html COMPETENCY_DOMAINS/PROFESSIONAL_CONTEXTS
    JS constant declarations.

    Pure function of the vocabulary dict — no file I/O. Emits {id, label}
    objects only (no `covers` — the form does not display it), one entry per
    line. SOURCE_TYPES and all other constants are untouched by this script
    (Section 10 of the spec — deferred scope).

    Example:
        >>> vocab = {"competency_domains": [{"id": "a", "label": "A", "covers": "c"}],
        ...          "professional_contexts": [{"id": "b", "label": "B"}]}
        >>> print(render_ingest_ui_block(vocab))
        const COMPETENCY_DOMAINS = [
          {id: "a", label: "A"}
        ];
        <BLANKLINE>
        const PROFESSIONAL_CONTEXTS = [
          {id: "b", label: "B"}
        ];
    """
    lines = ["const COMPETENCY_DOMAINS = ["]
    cd_rows = [
        f'  {{id: "{e["id"]}", label: "{e["label"]}"}}'
        for e in vocab["competency_domains"]
    ]
    lines.append(",\n".join(cd_rows))
    lines.append("];")
    lines.append("")
    lines.append("const PROFESSIONAL_CONTEXTS = [")
    pc_rows = [
        f'  {{id: "{e["id"]}", label: "{e["label"]}"}}'
        for e in vocab["professional_contexts"]
    ]
    lines.append(",\n".join(pc_rows))
    lines.append("];")
    return "\n".join(lines)


# ── Marker-delimited block replacement ──────────────────────────────────────


def locate_marker_block(text, begin_marker, end_marker, filename):
    """
    Validate that exactly one begin/end marker pair exists, in order.

    Raises VocabularyError if either marker is missing, either is duplicated,
    or the end marker precedes the begin marker. This is deliberately strict:
    guessing block bounds from a malformed marker pair risks silently
    clobbering hand-written content.

    Returns (begin_index, end_index) — the character offsets where each
    marker string starts in `text`.

    Example:
        >>> text = "a\\n<!-- BEGIN GENERATED VOCABULARY -->\\nx\\n<!-- END GENERATED VOCABULARY -->\\nb"
        >>> locate_marker_block(text, "<!-- BEGIN GENERATED VOCABULARY -->", "<!-- END GENERATED VOCABULARY -->", "f.md")
        (2, 40)
    """
    begin_count = text.count(begin_marker)
    end_count = text.count(end_marker)

    if begin_count == 0 or end_count == 0:
        raise VocabularyError(
            f"{filename}: generated-vocabulary marker pair not found "
            f"(begin found {begin_count} time(s), end found {end_count} time(s))."
        )
    if begin_count > 1 or end_count > 1:
        raise VocabularyError(
            f"{filename}: generated-vocabulary marker pair is duplicated "
            f"(begin found {begin_count} time(s), end found {end_count} time(s))."
        )

    begin_index = text.index(begin_marker)
    end_index = text.index(end_marker)

    if end_index < begin_index:
        raise VocabularyError(
            f"{filename}: END GENERATED VOCABULARY marker precedes the BEGIN marker."
        )

    return begin_index, end_index


def replace_marker_block(text, begin_marker, end_marker, new_inner, filename):
    """
    Replace the content between a validated begin/end marker pair.

    The replaced region runs from immediately after the BEGIN marker's line
    to immediately before the END marker's line — the marker lines themselves
    are preserved verbatim.

    Returns (new_text, changed) where `changed` is False if the existing
    inner content already equals `new_inner`.

    Example:
        >>> text = "<!-- BEGIN GENERATED VOCABULARY -->\\nold\\n<!-- END GENERATED VOCABULARY -->\\n"
        >>> new_text, changed = replace_marker_block(
        ...     text, "<!-- BEGIN GENERATED VOCABULARY -->",
        ...     "<!-- END GENERATED VOCABULARY -->", "new", "f.md")
        >>> changed
        True
        >>> new_text
        '<!-- BEGIN GENERATED VOCABULARY -->\\nnew\\n<!-- END GENERATED VOCABULARY -->\\n'
    """
    begin_index, _ = locate_marker_block(text, begin_marker, end_marker, filename)

    begin_line_end = text.index("\n", begin_index) + 1
    end_index = text.index(end_marker)
    end_line_start = text.rfind("\n", 0, end_index) + 1

    old_inner = text[begin_line_end:end_line_start]
    new_inner_block = new_inner + "\n"

    changed = old_inner != new_inner_block
    new_text = text[:begin_line_end] + new_inner_block + text[end_line_start:]
    return new_text, changed


# ── TAGGING-SKILL.md timestamp stamp ────────────────────────────────────────


def render_last_updated_stamp(now=None):
    """
    Render the current time in the project's MM/DD/YYYY HH:MM EST|EDT format,
    using America/New_York (spec Section 4.4 item 4).

    Example:
        >>> from datetime import datetime
        >>> from zoneinfo import ZoneInfo
        >>> render_last_updated_stamp(datetime(2026, 7, 11, 6, 27, tzinfo=ZoneInfo("America/New_York")))
        '07/11/2026 06:27 EDT'
    """
    if now is None:
        if ZoneInfo is None:
            raise VocabularyError(
                "zoneinfo is unavailable — Python 3.9+ is required (see environmental assumptions)."
            )
        now = datetime.now(ZoneInfo("America/New_York"))
    return now.strftime("%m/%d/%Y %H:%M %Z")


def update_last_updated_line(text, stamp):
    """
    Replace the '**Last Updated:** ...' line with a new stamp.

    Matches the single-line convention used across CLAUDE.md, OPERATIONS.md,
    and TAGGING-SKILL.md. Raises VocabularyError if no such line is found —
    fail fast rather than silently skipping the stamp update.

    Example:
        >>> update_last_updated_line("# T\\n**Last Updated:** old\\nbody", "new")
        '# T\\n**Last Updated:** new\\nbody'
    """
    new_text, count = re.subn(
        r"(?m)^\*\*Last Updated:\*\*.*$", f"**Last Updated:** {stamp}", text, count=1
    )
    if count == 0:
        raise VocabularyError(
            "TAGGING-SKILL.md: no '**Last Updated:**' line found to stamp."
        )
    return new_text


# ── Per-file processing ─────────────────────────────────────────────────────


def compute_updated_file(
    path, begin_marker, end_marker, render_fn, vocab, stamp_fn=None
):
    """
    Read `path`, render the expected block from `vocab`, and splice it in.

    Returns (new_text, changed). `stamp_fn`, if given, is applied to the
    spliced text whenever `changed` is True (used for the TAGGING-SKILL.md
    '**Last Updated:**' line).

    Raises VocabularyError if the file cannot be read or its marker pair is
    invalid (via replace_marker_block / locate_marker_block).

    Example:
        >>> import tempfile, os
        >>> fd, p = tempfile.mkstemp()
        >>> _ = os.write(fd, b"<!-- BEGIN GENERATED VOCABULARY -->\\n\\n<!-- END GENERATED VOCABULARY -->\\n")
        >>> os.close(fd)
        >>> vocab = {"competency_domains": [{"id": "a", "label": "A", "covers": "c"}],
        ...          "professional_contexts": [{"id": "b", "label": "B"}]}
        >>> _, changed = compute_updated_file(p, "<!-- BEGIN GENERATED VOCABULARY -->",
        ...     "<!-- END GENERATED VOCABULARY -->", render_ingest_ui_block, vocab)
        >>> changed
        True
        >>> os.remove(p)
    """
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError as exc:
        raise VocabularyError(f"cannot read {path}: {exc}") from exc

    new_inner = render_fn(vocab)
    new_text, changed = replace_marker_block(
        text, begin_marker, end_marker, new_inner, path
    )

    if changed and stamp_fn is not None:
        new_text = stamp_fn(new_text)

    return new_text, changed


# ── Entry point ──────────────────────────────────────────────────────────────


def main(argv=None):
    """
    CLI entry point.

    Default mode regenerates and writes both target files (only when their
    content actually changes) and prints 'unchanged' or 'regenerated' per
    file. --check mode renders and compares only, writing nothing, for use
    as wiki-lint.py's L18b subprocess check and for manual pre-commit use.

    Usage:
        python3 generate-vocab-artifacts.py
        python3 generate-vocab-artifacts.py --check
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Compare generated blocks to vocabulary.json; write nothing. "
        "Exit 0 if in sync, 1 if drifted, 2 on a fatal defect.",
    )
    args = parser.parse_args(argv)

    try:
        vocab = load_and_validate_vocabulary(VOCAB_FILE)

        tagging_text, tagging_changed = compute_updated_file(
            TAGGING_SKILL_FILE,
            TAGGING_BEGIN_MARKER,
            TAGGING_END_MARKER,
            render_tagging_skill_block,
            vocab,
            stamp_fn=lambda t: update_last_updated_line(t, render_last_updated_stamp()),
        )

        html_text, html_changed = compute_updated_file(
            INGEST_UI_FILE,
            HTML_BEGIN_MARKER,
            HTML_END_MARKER,
            render_ingest_ui_block,
            vocab,
        )
    except VocabularyError as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2

    if args.check:
        drifted = []
        if tagging_changed:
            drifted.append(TAGGING_SKILL_FILE)
        if html_changed:
            drifted.append(INGEST_UI_FILE)
        if drifted:
            print(f"DRIFT: out of sync with {VOCAB_FILE}: {', '.join(drifted)}")
            return 1
        print(f"OK: {TAGGING_SKILL_FILE} and {INGEST_UI_FILE} match {VOCAB_FILE}.")
        return 0

    for path, text, changed in (
        (TAGGING_SKILL_FILE, tagging_text, tagging_changed),
        (INGEST_UI_FILE, html_text, html_changed),
    ):
        if changed:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"regenerated: {path}")
        else:
            print(f"unchanged: {path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
