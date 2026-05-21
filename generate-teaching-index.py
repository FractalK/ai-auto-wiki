#!/usr/bin/env python3
"""
generate-teaching-index.py — regenerate teaching-index.md from frontmatter tags.

Run from the wiki repository root (the directory containing CLAUDE.md).

Usage:
    python3 generate-teaching-index.py

Exit codes:
    0 — index written successfully (WARNING lines may have been emitted to stderr)
    1 — fatal error (CLAUDE.md not found, or teaching-index.md could not be written)

WARNING lines (stderr) are emitted for pages with teaching_relevance: true that are
missing competency_domains or professional_contexts. Those pages are excluded from the
index but do not cause a non-zero exit. Run wiki-verify.sh Check 15 to list them.

ABORT lines (stderr) indicate a fatal condition; exit code is 1.

Environmental assumptions:
    - Python 3.6+ (f-strings, pathlib)
    - Standard library only — no external packages
    - Executed from the wiki repository root
    - CLAUDE.md present in working directory (entrypoint guard)
"""

import os
import re
import sys
from collections import defaultdict
from datetime import date

# ── Configuration ─────────────────────────────────────────────────────────────

CONTENT_DIRS = ["topics", "tools", "comparisons", "pitfalls"]
OUTPUT_FILE = "teaching-index.md"
TODAY = date.today().strftime("%Y-%m-%d")


# ── Frontmatter parsing ───────────────────────────────────────────────────────

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


# ── Teaching Notes excerpt extraction ────────────────────────────────────────

def extract_teaching_notes_excerpt(body, page_type):
    """
    Extract one sentence from the appropriate Teaching Notes subsection.

    Topic/Tool pages: **Concept in plain terms** subsection.
    Pitfalls pages:   **What this failure mode teaches** subsection.

    Returns the first sentence found, stripped of wikilinks and bold markers.
    Returns None if the Teaching Notes section or the target subsection is absent.

    Example:
        excerpt = extract_teaching_notes_excerpt(body, "topic")
        # "Prompt injection exploits the model's inability to distinguish
        #  instruction from data." (first sentence only)
    """
    if "## Teaching Notes" not in body:
        return None

    tn_start = body.find("## Teaching Notes")
    tn_section = body[tn_start:]

    # Bound the section at the next H2 heading (if any)
    next_h2 = re.search(r'\n## ', tn_section[len("## Teaching Notes"):])
    if next_h2:
        cutoff = len("## Teaching Notes") + next_h2.start()
        tn_section = tn_section[:cutoff]

    target = (
        "**What this failure mode teaches**"
        if page_type == "pitfalls"
        else "**Concept in plain terms**"
    )

    if target not in tn_section:
        return None

    idx = tn_section.find(target)
    after = tn_section[idx + len(target):].strip()

    # Strip wikilinks: [[slug|label]] → label; [[slug]] → slug
    after = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\2', after)
    after = re.sub(r'\[\[([^\]]+)\]\]', r'\1', after)

    # Strip bold/italic markers
    after = re.sub(r'\*+', '', after)

    # Take the first sentence
    m = re.match(r'([^.!?]+[.!?])', after.strip())
    if m:
        return m.group(1).strip()

    return None


# ── Page collection ───────────────────────────────────────────────────────────

def collect_pages():
    """
    Scan CONTENT_DIRS for pages with teaching_relevance: true.

    Exclusions (CLAUDE.md Section 10 generation rules):
    - status: stub
    - status: deprecated
    - type: teaching-brief

    Pages with teaching_relevance: true but missing competency_domains or
    professional_contexts are warned and skipped (not a fatal error).

    Returns a list of page-entry dicts. Skipped-page count is printed to stderr.

    Example:
        pages = collect_pages()
        # [{"slug": "prompt-injection", "title": "Prompt Injection", ...}, ...]
    """
    pages = []
    skip_count = 0

    for directory in CONTENT_DIRS:
        if not os.path.isdir(directory):
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

            if fm.get("teaching_relevance") is not True:
                continue

            # Apply exclusions
            status = fm.get("status", "")
            page_type = fm.get("type", "")

            if status in ("stub", "deprecated"):
                continue
            if page_type == "teaching-brief":
                continue

            # Coerce list fields — handle scalar values from single-item lists
            competency_domains = fm.get("competency_domains", [])
            professional_contexts = fm.get("professional_contexts", [])

            if isinstance(competency_domains, str):
                competency_domains = [competency_domains] if competency_domains else []
            if isinstance(professional_contexts, str):
                professional_contexts = [professional_contexts] if professional_contexts else []

            # Required tagging fields — warn and skip if absent
            missing = []
            if not competency_domains:
                missing.append("competency_domains")
            if not professional_contexts:
                missing.append("professional_contexts")

            if missing:
                print(
                    f"WARNING: {fpath} — teaching_relevance: true but missing "
                    f"{', '.join(missing)}; page excluded from Teaching Index",
                    file=sys.stderr,
                )
                skip_count += 1
                continue

            slug = fname[:-3]  # strip .md
            title = fm.get("title", slug.replace("-", " ").title())
            summary = fm.get("summary", "")
            technical_depth = fm.get("technical_depth", "")
            excerpt = extract_teaching_notes_excerpt(body, page_type)

            pages.append({
                "slug": slug,
                "title": title,
                "type": page_type,
                "technical_depth": technical_depth,
                "summary": summary,
                "competency_domains": competency_domains,
                "professional_contexts": professional_contexts,
                "excerpt": excerpt,
            })

    if skip_count:
        print(
            f"WARNING: {skip_count} page(s) excluded from Teaching Index due to missing "
            f"tagging fields. Run wiki-verify.sh Check 15 to list affected files.",
            file=sys.stderr,
        )

    return pages


# ── Index assembly ────────────────────────────────────────────────────────────

def build_index(pages):
    """
    Organise pages into a nested dict: domain → context → [page_dicts].

    A page with multiple competency domains appears under each domain.
    A page with multiple professional contexts appears under each context
    within each of its domain sections.

    Example:
        index = build_index(pages)
        index["tool-evaluation-and-selection"]["teaching-and-instruction"]
        # [{"slug": "...", "title": "...", ...}, ...]
    """
    index = defaultdict(lambda: defaultdict(list))

    for page in pages:
        for domain in page["competency_domains"]:
            for context in page["professional_contexts"]:
                index[domain][context].append(page)

    return index


def read_created_date():
    """
    Read the existing `created` date from teaching-index.md if it exists.
    Falls back to TODAY if the file is absent or unparseable.
    """
    if not os.path.exists(OUTPUT_FILE):
        return TODAY
    try:
        with open(OUTPUT_FILE, encoding="utf-8") as f:
            text = f.read()
        fm, _ = parse_frontmatter(text)
        return fm.get("created", TODAY)
    except OSError:
        return TODAY


# ── Rendering ─────────────────────────────────────────────────────────────────

def render_index(index, pages, created):
    """
    Render the full teaching-index.md content as a string.

    Structure:
        ---
        type: teaching-index
        title: Teaching Index
        created: YYYY-MM-DD
        updated: YYYY-MM-DD
        ---

        # Teaching Index
        {summary line}

        ## {competency_domain}
        ### {professional_context}
        - [[slug|Title]] (type · depth) — summary
          *excerpt*
    """
    lines = []

    # Frontmatter
    lines += [
        "---",
        "type: teaching-index",
        "title: Teaching Index",
        f"created: {created}",
        f"updated: {TODAY}",
        "---",
        "",
    ]

    # Header
    domain_count = len(index)
    lines += [
        "# Teaching Index",
        "",
        f"Auto-generated from frontmatter tags. {len(pages)} page(s) indexed across "
        f"{domain_count} competency domain(s).",
        f"Last regenerated: {TODAY}. "
        f"To regenerate: `python3 generate-teaching-index.py`.",
        "",
    ]

    if not index:
        lines.append("*No teaching-tagged pages found.*")
        lines.append("")
        return "\n".join(lines)

    for domain in sorted(index.keys()):
        lines.append(f"## {domain}")
        lines.append("")

        for context in sorted(index[domain].keys()):
            lines.append(f"### {context}")
            lines.append("")

            # Deduplicate within this domain/context cell
            seen = set()
            for page in sorted(index[domain][context], key=lambda p: p["title"]):
                if page["slug"] in seen:
                    continue
                seen.add(page["slug"])

                depth_part = f" · {page['technical_depth']}" if page["technical_depth"] else ""
                entry = (
                    f"- [[{page['slug']}|{page['title']}]] "
                    f"({page['type']}{depth_part})"
                )

                if page["summary"]:
                    entry += f" — {page['summary']}"

                lines.append(entry)

                if page["excerpt"]:
                    lines.append(f"  *{page['excerpt']}*")

            lines.append("")

    return "\n".join(lines)


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    """
    Main entry point. Guards, collects, builds, renders, writes.

    Usage:
        python3 generate-teaching-index.py
    """
    if not os.path.exists("CLAUDE.md"):
        print(
            "ABORT: CLAUDE.md not found in current directory. "
            "Run from the wiki repository root.",
            file=sys.stderr,
        )
        sys.exit(1)

    created = read_created_date()
    pages = collect_pages()
    index = build_index(pages)
    content = render_index(index, pages, created)

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(content)
    except OSError as exc:
        print(f"ABORT: could not write {OUTPUT_FILE}: {exc}", file=sys.stderr)
        sys.exit(1)

    print(
        f"Teaching Index written: {OUTPUT_FILE} "
        f"({len(pages)} page(s) indexed, {len(index)} domain(s))."
    )


if __name__ == "__main__":
    main()
