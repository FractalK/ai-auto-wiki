#!/usr/bin/env python3
# Last Updated: 06/27/2026 17:26 EDT
"""
PDF to Markdown Converter
========================

Converts multi-page PDFs to clean markdown using font-size-based heading classification
and smart text joining. Validated on Anthropic system cards, Nature articles, 
academic papers, and Anthropic Economic Index reports.

USAGE:
------
Option A — CLI, single line (most reliable — safe against shell paste artifacts):
    python3 pdf_to_markdown.py --input /path/to/file.pdf --output /path/to/out.md --title "# Document Title" --date "Month DD, YYYY" --org "Organization" --doi "https://doi.org/..."

Option A, multi-line form (readable, but fragile when pasted into some shells —
e.g. zsh treats each line as a separate command if a trailing space follows the
backslash, producing "command not found: --title"-style errors; verify no
trailing whitespace survives the paste before using this form):
    python3 pdf_to_markdown.py --input /path/to/file.pdf --output /path/to/out.md \\
        --title "# Document Title" --date "Month DD, YYYY" \\
        --org "Organization" --doi "https://doi.org/..."

Option B — Edit parameters below, then (recommended for repeated repo use,
since it has no shell-paste failure mode at all):
    python3 pdf_to_markdown.py

Diagnostic mode (inspect font sizes before converting):
    python3 pdf_to_markdown.py --diagnose [--input /path/to/file.pdf]

REQUIREMENTS:
- pymupdf: pip install pymupdf --break-system-packages -q
  (omit --break-system-packages outside a PEP 668 externally-managed
  environment, e.g. a plain pyenv/venv setup — it's a no-op there but some
  pip versions may not recognize it)

IMPORT NOTE — fitz/pymupdf namespace collision:
PyMuPDF's legacy import name is `fitz`, but there is also a separate,
unrelated, unmaintained PyPI package literally named `fitz` (last released
2017) that squats on the same import name. If that package was ever
`pip install`ed directly into this environment, `import fitz` resolves to
it instead of PyMuPDF, producing a confusing multi-frame ImportError several
layers deep (typically ending in "No module named 'frontend'" or a
StaticFiles directory error). This script avoids the collision entirely by
using `import pymupdf as fitz` below — the rest of the script's `fitz.*`
calls are unaffected, and this resolves correctly regardless of whether the
colliding `fitz` package is also installed, as long as `pymupdf` itself is.
If `pymupdf` is not installed at all, this import now fails with a clean
`ModuleNotFoundError: No module named 'pymupdf'` instead of the confusing
nested traceback.

OUTPUT:
- Markdown file with metadata header, h2/h3/h4/h5/h6 hierarchy, smart text joining
- Skips bare page numbers, pg. N footers, and unicode artifacts
- Skips repeated running headers/footers (e.g. document title repeated on every page)
- Detects and converts bullets (●, ○, and •)
- Detects exhibit/figure labels and renders as bold standalone lines
- Prevents excessive line breaks in body text
- Rejoins hyphenated line-breaks (academic column layouts)

TOC-ANCHORED HEADING EXTRACTION:
When the PDF contains an embedded outline (doc.get_toc() returns >= 10 entries),
the script uses the outline as a heading lookup table. Before font-size classification,
each line is checked against the normalized TOC index. On a match the heading level
comes from the outline (L1-L5 → ##/###/####/#####/######), bypassing font-size
thresholds entirely. This handles documents (e.g. Anthropic system cards) where
L4/L5 headings are visually indistinguishable from body text by font size alone.
TOC mode activates automatically; disable with --no-toc if it produces wrong output.

RUNNING HEADER/FOOTER DETECTION:
Many reports repeat the document title or section name on every page, at a font
size below all heading thresholds — these are page-position artifacts, not
content, and SKIP_PATTERNS (which only matches generic page-number shapes) does
not catch them because they are document-specific text, not a fixed pattern.
Before extraction, a pre-pass scans all pages and flags any line of text, at or
below RUNNING_HEADER_MAX_FONT_SIZE, that recurs verbatim on at least
RUNNING_HEADER_MIN_FRACTION of pages. Flagged text is skipped during extraction
instead of being concatenated into body paragraphs. Reported in --diagnose
output; disable with --no-header-strip if it produces a false positive (e.g. a
short phrase that is legitimately repeated content rather than a header/footer).

FONT SIZE THRESHOLDS (adjustable, used when TOC mode is off or no match found):
- h1 (##):  size >= 15.5
- h2 (###): size >= 13.5
- h3 (####): size >= 12.5
- h4 (#####): size >= 11.5 + bold
- body: default

If output is garbled, run with --diagnose to inspect actual font sizes and TOC entries.
"""

import argparse
import pymupdf as fitz
import re
import sys

# ══════════════════════════════════════════════════════════════════════════════
# PARAMETERS — EDIT THESE FOR EACH DOCUMENT (used when CLI args not supplied)
# ══════════════════════════════════════════════════════════════════════════════

INPUT_PDF = '/mnt/user-data/uploads/FILENAME.pdf'
OUTPUT_MD = '/mnt/user-data/outputs/FILENAME.md'
TITLE_LINE = '# Document Title Here'
PUB_DATE = 'Month DD, YYYY'

# Optional metadata (leave blank to skip)
ORGANIZATION = 'Organization Name'
DOI_OR_URL = ''
ADDITIONAL_METADATA = ''

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

FONT_SIZE_H1 = 15.5  # h2 in markdown (## Title)
FONT_SIZE_H2 = 13.5  # h3 in markdown (### Subtitle)
FONT_SIZE_H3 = 12.5  # h4 in markdown (#### Subsubtitle)
FONT_SIZE_H4 = 11.5  # h5 in markdown (##### Minor heading, requires bold)

# Skip patterns: bare page numbers and pg. N style footers
SKIP_PATTERNS = [
    r'^\d{1,4}$',          # bare page numbers: 1, 42, 1234
    r'^pg\.\s*\d+$',       # pg. N style footers (e.g. MIT NANDA report)
]

# Exhibit/figure label pattern: render as bold standalone line
EXHIBIT_LABEL_REGEX = r'^(Exhibit|Figure|Table|Chart):?\s'

# Running header/footer detection (P7): a line at or below this font size that
# recurs verbatim on at least this fraction of pages is treated as a repeated
# page header/footer and skipped, rather than concatenated into body text.
RUNNING_HEADER_MAX_FONT_SIZE = 10.0
RUNNING_HEADER_MIN_FRACTION = 0.4


# ══════════════════════════════════════════════════════════════════════════════
# FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def parse_args():
    """
    Parse CLI arguments. All are optional; unset args fall back to top-of-file
    parameter constants, preserving the edit-source workflow.

    Usage examples:
        python3 pdf_to_markdown.py --input doc.pdf --output out.md --title "# My Doc"
        python3 pdf_to_markdown.py --diagnose --input doc.pdf
        python3 pdf_to_markdown.py  # uses top-of-file constants
    """
    parser = argparse.ArgumentParser(
        description="Convert a PDF to clean wiki-ready markdown."
    )
    parser.add_argument("--input", help="Path to input PDF file")
    parser.add_argument("--output", help="Path to output markdown file")
    parser.add_argument("--title", help="Document title line (e.g. '# My Title')")
    parser.add_argument("--date", help="Publication date string")
    parser.add_argument("--org", help="Organization name")
    parser.add_argument("--doi", help="DOI or URL")
    parser.add_argument(
        "--diagnose",
        action="store_true",
        help="Print font sizes for the first N pages and exit",
    )
    parser.add_argument(
        "--no-toc",
        action="store_true",
        help="Disable TOC-anchored heading extraction even when an outline is present",
    )
    parser.add_argument(
        "--no-header-strip",
        action="store_true",
        help="Disable running header/footer detection (e.g. if it produces a false positive)",
    )
    parser.add_argument(
        "--sample-pages",
        type=int,
        default=5,
        help="Number of pages to sample in diagnostic/quality-check mode (default: 5)",
    )
    return parser.parse_args()


def classify(size, bold):
    """Map font size + bold flag to heading level or body."""
    if size >= FONT_SIZE_H1:
        return 'h1'
    if size >= FONT_SIZE_H2:
        return 'h2'
    if size >= FONT_SIZE_H3:
        return 'h3'
    if size >= FONT_SIZE_H4 and bold:
        return 'h4'
    return 'body'


def build_toc_index(doc):
    """
    Build a normalized heading lookup table from the PDF's embedded outline.

    Reads doc.get_toc(), filters blank/whitespace-only entries, and normalizes
    each title (strip leading/trailing whitespace, collapse internal whitespace,
    replace zero-width spaces with regular spaces — mirroring extract_pdf
    unicode cleaning). Returns a dict mapping normalized_title → toc_level (1–5).

    Returns an empty dict when:
      - The document has no embedded outline (get_toc() returns []).
      - Fewer than 10 non-blank entries remain after filtering (avoids false
        activation on documents with only chapter-level bookmarks).

    Args:
        doc: An open fitz.Document object.

    Returns:
        dict[str, int]: Normalized title → TOC level (1–5). Empty if not usable.

    Usage example:
        doc = fitz.open("system_card.pdf")
        toc_index = build_toc_index(doc)
        if toc_index:
            level = toc_index.get("2.1.2.1 On autonomy risks")
    """
    raw = doc.get_toc()
    if not raw:
        return {}

    index = {}
    for entry in raw:
        lvl, raw_title, _page = entry
        # Normalize: zero-width space → space, collapse whitespace, strip ends
        norm = raw_title.replace('\u200b', ' ').replace('\ufeff', '')
        norm = re.sub(r'\s+', ' ', norm).strip()
        if norm:
            index[norm] = lvl  # last entry wins on duplicate titles (rare)

    if len(index) < 10:
        return {}

    return index


# TOC level → markdown heading prefix (L1=##, L2=###, L3=####, L4=#####, L5=######)
_TOC_LEVEL_PREFIX = {1: '##', 2: '###', 3: '####', 4: '#####', 5: '######'}


def detect_running_headers(doc, min_fraction=RUNNING_HEADER_MIN_FRACTION,
                            max_font_size=RUNNING_HEADER_MAX_FONT_SIZE):
    """
    Detect repeated running headers/footers: low-font-size lines that recur
    verbatim across a large fraction of pages.

    Running headers/footers (e.g. a document title repeated on every page)
    are page-position artifacts, not content. SKIP_PATTERNS cannot catch them
    because their text is document-specific, not a fixed shape like a page
    number — detecting them requires comparing text *across* pages rather
    than matching a single page in isolation.

    Each page contributes at most one count per distinct text (a header
    that happens to render as two adjacent spans on one page is not double
    counted), so the fraction reflects page coverage, not raw occurrences.

    Args:
        doc:           An open fitz.Document object.
        min_fraction:  Minimum fraction of pages a line must appear on
                       (verbatim, after the same unicode cleaning extract_pdf
                       applies) to be flagged as a running header/footer.
        max_font_size: Only lines at or below this font size are eligible —
                       this excludes repeated body content (e.g. a section
                       title that legitimately recurs) which is typically
                       set at body size or larger, not header/footer size.

    Returns:
        set[str]: Normalized line texts to skip during extraction. Empty if
        no text meets the recurrence threshold.

    Usage example:
        doc = fitz.open("report.pdf")
        running_headers = detect_running_headers(doc)
        if running_headers:
            print(f"Will skip: {running_headers}")
    """
    page_count = len(doc)
    counts = {}

    for page in doc:
        seen_this_page = set()
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if b.get("type") != 0:
                continue
            for line in b.get("lines", []):
                spans = line.get("spans", [])
                if not spans:
                    continue
                text = ' '.join(s['text'] for s in spans)
                # Mirror the main loop's exact cleaning (empty-string deletion,
                # not space substitution) so this set matches what `text` will
                # actually equal at the `text in running_headers` check below.
                text = text.replace('\u200b', '').replace('\ufeff', '').strip()
                if not text or text in seen_this_page:
                    continue
                max_size = max(s['size'] for s in spans)
                if max_size <= max_font_size:
                    counts[text] = counts.get(text, 0) + 1
                    seen_this_page.add(text)

    threshold = max(2, int(page_count * min_fraction))
    return {text for text, count in counts.items() if count >= threshold}


def should_join_text(last_line, new_text):
    """
    Heuristic: determine how to join flowing body text.

    Returns:
        'hyphen'  — last_line ends with a mid-word hyphen; join without space
        'join'    — normal flowing text; join with a space
        False     — do not join; start a new line

    Does NOT join across: bullets, sentence-ending lines, headings.
    """
    if not last_line or last_line.startswith('#'):
        return False
    if last_line.endswith('\n') or new_text.lstrip().startswith('- '):
        return False
    if any(last_line.endswith(char) for char in [':', '.', '%', ')']):
        return False

    # Detect trailing hyphen indicating a mid-word line break (P3).
    # Exclude "- " bullet markers and standalone dashes.
    stripped = last_line.rstrip()
    if stripped.endswith('-') and len(stripped) > 1 and stripped[-2] != ' ':
        return 'hyphen'

    return 'join'


def assess_extraction_quality(input_path, sample_pages=3, page_count=None):
    """
    Quick quality pre-check: sample the first N pages to determine whether
    the script path or in-context processing is more appropriate.

    Checks run in order from cheapest to most expensive:
      1. Page-count check — short documents are always routed to in-context,
         which avoids any encoding artifacts without text extraction.
      2. Concatenation check — detects justified-text encoding artifacts where
         words are fused without inter-word spaces (long-run token heuristic).
      3. Yield check — detects scanned/image-based PDFs with low text yield.

    Args:
        input_path:   Path to the PDF file.
        sample_pages: Number of pages to sample for quality checks (default: 3).
        page_count:   Total page count of the already-open document, if known.
                      When provided, the page-count check runs without opening
                      the file a second time. Pass None to skip this check.

    Returns:
        tuple[str, str]: ("script"|"in-context", reason string)

    Usage example:
        recommendation, reason = assess_extraction_quality("paper.pdf", page_count=9)
        print(f"Recommended: {recommendation} — {reason}")
    """
    # Check 1: Page-count awareness (cheapest — no file I/O if page_count provided).
    # Short documents are fully renderable in context and artifact-free; route them
    # to in-context regardless of other metrics.
    if page_count is not None and page_count <= 10:
        return (
            "in-context",
            f"Document is {page_count} pages — short enough for in-context processing, "
            f"which avoids any encoding artifacts.",
        )

    try:
        doc = fitz.open(input_path)
    except Exception as e:
        return ("in-context", f"Cannot open PDF: {e}")

    total_chars = 0
    heading_candidates = 0
    all_tokens = []  # For concatenation check (Check 2)
    pages_sampled = min(sample_pages, len(doc))

    for page_num in range(0, pages_sampled):  # Start from page 0 (cover included)
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if b.get("type") != 0:
                continue
            for line in b.get("lines", []):
                spans = line.get("spans", [])
                if not spans:
                    continue
                text = ' '.join(s['text'] for s in spans)
                # Mirror extract_pdf unicode cleaning so the concatenation check
                # reflects what the script will actually write, not raw encoding.
                text = text.replace('\u200b', ' ').replace('\ufeff', '').strip()
                total_chars += len(text)
                all_tokens.extend(text.split())
                max_size = max(s['size'] for s in spans)
                if max_size >= FONT_SIZE_H1:
                    heading_candidates += 1

    doc.close()

    # Check 2: Concatenation detection.
    # Text is cleaned of zero-width spaces (mirroring extract_pdf) before
    # tokenizing, so this check targets documents where words are genuinely
    # fused with no separator at all — a different encoding failure from
    # zero-width-space padding. Long-run token ratio > 10% indicates that
    # extraction will produce garbled concatenated output even after cleanup.
    # Threshold values: min token length = 20 chars, ratio = 0.10.
    total_tokens = len(all_tokens)
    if total_tokens > 0:
        long_run_count = sum(1 for t in all_tokens if len(t) >= 20)
        long_run_ratio = long_run_count / total_tokens
        if long_run_ratio > 0.10:
            return (
                "in-context",
                f"Possible word concatenation: {long_run_ratio:.0%} of tokens exceed "
                f"20 chars (threshold: 10%). PDF may use justified-text encoding.",
            )

    # Check 3: Yield check.
    avg_chars = total_chars / pages_sampled if pages_sampled > 0 else 0

    if avg_chars < 200:
        return (
            "in-context",
            f"Low text yield: {avg_chars:.0f} chars/page avg on {pages_sampled} pages "
            f"(threshold: 200). PDF may be scanned or image-based.",
        )
    if heading_candidates == 0:
        return (
            "script",
            f"No heading-size text found in {pages_sampled} pages — "
            f"headings may use body-size fonts. Script will run but consider "
            f"adjusting FONT_SIZE_H1/H2/H3 thresholds after --diagnose.",
        )
    return (
        "script",
        f"Good text yield: {avg_chars:.0f} chars/page avg, "
        f"{heading_candidates} heading candidate(s) in {pages_sampled} pages.",
    )


def extract_pdf(input_path, output_path, title_line, pub_date, org, doi, extra,
                 no_toc=False, no_header_strip=False):
    """Main extraction pipeline.

    Args:
        input_path:      Path to the input PDF file.
        output_path:     Path to write the output markdown file.
        title_line:      Document title line (e.g. '# My Title').
        pub_date:        Publication date string.
        org:             Organization name (optional).
        doi:             DOI or URL (optional).
        extra:           Additional metadata lines (optional).
        no_toc:          If True, disable TOC-anchored heading extraction even
                         when the document has a usable embedded outline
                         (default: False).
        no_header_strip: If True, disable running header/footer detection
                         (default: False).
    """

    try:
        doc = fitz.open(input_path)
    except Exception as e:
        print(f"ERROR: Cannot open PDF: {e}")
        sys.exit(1)

    page_count = len(doc)

    # P4 — Quality pre-check advisory (non-blocking).
    # Pass page_count so the cheapest check (page-count) runs without re-opening.
    recommendation, reason = assess_extraction_quality(input_path, page_count=page_count)
    print(f"Quality pre-check: [{recommendation.upper()}] {reason}")
    if recommendation == "in-context":
        print("  Note: consider using in-context processing instead of this script.")
    print(f"Pages: {page_count}")

    # TOC-anchored heading extraction: build index from embedded outline.
    # Auto-activates when the document has >= 10 non-blank TOC entries and
    # --no-toc is not set. L4/L5 headings that are indistinguishable from body
    # text by font size alone are classified via TOC match only.
    if no_toc:
        toc_index = {}
        print("TOC mode: DISABLED (--no-toc)")
    else:
        toc_index = build_toc_index(doc)
        if toc_index:
            print(f"TOC mode: ACTIVE ({len(toc_index)} entries in index)")
        else:
            print("TOC mode: OFF (no usable embedded outline)")

    # Running header/footer detection (P7): flag repeated low-font-size lines
    # that recur across pages so they're skipped rather than concatenated
    # into body text. Runs unless --no-header-strip is set.
    if no_header_strip:
        running_headers = set()
        print("Header-strip mode: DISABLED (--no-header-strip)")
    else:
        running_headers = detect_running_headers(doc)
        if running_headers:
            preview = list(running_headers)[:3]
            print(f"Header-strip mode: ACTIVE ({len(running_headers)} pattern(s) "
                  f"detected): {preview}")
        else:
            print("Header-strip mode: OFF (no repeated header/footer text found)")

    md_lines = []
    prev_class = None
    pending_bullet = None  # P8b: set when a bullet glyph rendered as its own
                            # line/span, with the bullet's text following as
                            # a separate line — see detection block below.

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if b.get("type") != 0:
                continue
            for line in b.get("lines", []):
                spans = line.get("spans", [])
                if not spans:
                    continue

                # Extract text and clean unicode artifacts
                text = ' '.join(s['text'] for s in spans)
                text = text.replace('\u200b', '').replace('\ufeff', '').strip()

                # Skip empty lines and matched skip patterns (P2: pg. N footers)
                if not text:
                    continue
                if any(re.match(pattern, text) for pattern in SKIP_PATTERNS):
                    continue
                # Skip detected running headers/footers (P7)
                if running_headers and text in running_headers:
                    continue

                # Standalone bullet-glyph line (P8b): some PDFs render the
                # bullet glyph as its own line/span, with the bullet's text
                # following as a separate line — a distinct pattern from the
                # inline "•\tlabel: text" spans handled below. A bare glyph
                # carries no font-size signal of its own, so this must be
                # caught before classification; the next non-empty line
                # consumes the pending marker (see below).
                if text in ('•', '●'):
                    pending_bullet = '- '
                    continue
                if text == '○':
                    pending_bullet = '  - '
                    continue

                # Classify by font size and bold
                max_size = max(s['size'] for s in spans)
                is_bold = any('Bold' in s.get('font', '') for s in spans)

                # TOC-anchored classification: check normalized line text against
                # the embedded outline index before falling back to font-size.
                # On a match, the TOC level overrides font-size classification.
                # L1-L5 TOC levels map to ##/###/####/#####/######.
                if toc_index:
                    norm_text = re.sub(r'\s+', ' ', text).strip()
                    toc_level = toc_index.get(norm_text)
                    if toc_level is not None:
                        prefix = _TOC_LEVEL_PREFIX.get(toc_level, '######')
                        md_lines.append(f'\n{prefix} {text}\n')
                        prev_class = f'h{toc_level}'
                        continue

                cls = classify(max_size, is_bold)

                # Convert bullets (P8: "•" added alongside "●" — this also
                # prevents run-on joining, since should_join_text's existing
                # guard checks for the "- " prefix this assigns)
                if (text.startswith('● ') or text.startswith('●\t')
                        or text.startswith('• ') or text.startswith('•\t')):
                    text = '- ' + text[2:].strip()
                    cls = 'bullet'
                elif text.startswith('○ ') or text.startswith('○\t'):
                    text = '  - ' + text[2:].strip()
                    cls = 'bullet'
                elif pending_bullet and cls == 'body':
                    # P8b: this line is the content half of a standalone
                    # bullet-glyph marker seen on the previous line — apply
                    # the prefix now and force a new markdown line.
                    text = pending_bullet + text
                    cls = 'bullet'
                elif pending_bullet:
                    # The line following a bare bullet glyph turned out to be
                    # a heading, not body text — almost certainly malformed
                    # source structure. Drop the stale marker rather than
                    # carrying it forward onto unrelated later content.
                    pending_bullet = None

                if cls == 'bullet':
                    pending_bullet = None

                # Build markdown
                if cls == 'h1':
                    md_lines.append(f'\n## {text}\n')
                elif cls == 'h2':
                    md_lines.append(f'\n### {text}\n')
                elif cls == 'h3':
                    md_lines.append(f'\n#### {text}\n')
                elif cls == 'h4':
                    md_lines.append(f'\n##### {text}\n')
                elif cls in ('body', 'bullet'):
                    # P5 — Exhibit/figure label: render as bold standalone line
                    if re.match(EXHIBIT_LABEL_REGEX, text):
                        md_lines.append(f'\n**{text}**\n')
                        prev_class = 'exhibit'
                        continue

                    if prev_class in ('h1', 'h2', 'h3', 'h4', 'exhibit'):
                        md_lines.append(text)
                    else:
                        # P3 — Smart joining with hyphen-break detection
                        join_result = should_join_text(
                            md_lines[-1] if md_lines else '', text
                        )
                        if join_result == 'hyphen':
                            # Strip trailing hyphen and join without space
                            md_lines[-1] = md_lines[-1].rstrip()[:-1] + text
                        elif join_result == 'join':
                            md_lines[-1] = md_lines[-1] + ' ' + text
                        else:
                            md_lines.append(text)

                prev_class = cls

    doc.close()

    # Join lines and normalize whitespace
    full_md = '\n'.join(md_lines)
    full_md = re.sub(r'\n{3,}', '\n\n', full_md)

    # Build metadata header
    header = f"""{title_line}

**Published:** {pub_date}
"""
    if org:
        header += f"**Organization:** {org}\n"
    if doi:
        header += f"**DOI/URL:** {doi}\n"
    if extra:
        header += f"{extra}\n"
    header += "\n"

    full_md = header + full_md

    # Write output
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_md)
    except Exception as e:
        print(f"ERROR: Cannot write output: {e}")
        sys.exit(1)

    # Report
    char_count = len(full_md)
    line_count = full_md.count('\n')
    print(f"Written: {char_count:,} chars, {line_count:,} lines")
    print(f"\n--- FIRST 1000 CHARS (spot check) ---")
    print(full_md[:1000])
    print("\n✓ Conversion complete")


def diagnostic_font_sizes(input_path, sample_pages=5):
    """
    Inspect font sizes in PDF to diagnose classification issues.
    Run this if output appears garbled (via --diagnose flag).
    Also reports embedded outline (TOC) entry count and level distribution.
    """
    try:
        doc = fitz.open(input_path)
    except Exception as e:
        print(f"ERROR: Cannot open PDF: {e}")
        return

    print(f"\nDiagnostic: Font Sizes in {input_path}")
    print("=" * 80)

    # Report TOC structure first so operator knows whether TOC mode will activate
    toc_index = build_toc_index(doc)
    raw_toc = doc.get_toc()
    if not raw_toc:
        print(f"\nTOC: No embedded outline found — TOC mode will be OFF")
    else:
        non_blank = sum(1 for e in raw_toc if re.sub(r'\s+', ' ', e[1].replace('\u200b', ' ')).strip())
        level_dist = {}
        for e in raw_toc:
            norm = re.sub(r'\s+', ' ', e[1].replace('\u200b', ' ')).strip()
            if norm:
                level_dist[e[0]] = level_dist.get(e[0], 0) + 1
        status = f"ACTIVE ({len(toc_index)} entries in index)" if toc_index else f"OFF ({non_blank} non-blank entries < 10 threshold)"
        print(f"\nTOC: {len(raw_toc)} total entries, {non_blank} non-blank — mode will be {status}")
        print(f"     Level distribution: {dict(sorted(level_dist.items()))}")
        # Show a sample of L4/L5 entries if present
        l4l5 = [(e[0], re.sub(r'\s+', ' ', e[1].replace('\u200b', ' ')).strip())
                 for e in raw_toc if e[0] in (4, 5) and re.sub(r'\s+', ' ', e[1].replace('\u200b', ' ')).strip()]
        if l4l5:
            print(f"     L4/L5 sample (first 5):")
            for lvl, title in l4l5[:5]:
                print(f"       L{lvl}: {repr(title[:70])}")

    # Report running header/footer detection so operator can sanity-check
    # before conversion (mirrors TOC reporting above).
    running_headers = detect_running_headers(doc)
    if running_headers:
        print(f"\nRunning headers/footers: {len(running_headers)} pattern(s) detected "
              f"(will be skipped during extraction):")
        for h in list(running_headers)[:5]:
            print(f"     {repr(h[:80])}")
    else:
        print(f"\nRunning headers/footers: none detected")

    # P6 — Start from page 0 (cover page); note decorative font sizes expected
    for page_num in range(0, min(sample_pages, len(doc))):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        note = " [cover — font sizes may be decorative]" if page_num == 0 else ""
        print(f"\n--- Page {page_num + 1}{note} ---")
        for b in blocks:
            if b.get("type") != 0:
                continue
            for line in b.get("lines", []):
                spans = line.get("spans", [])
                if not spans:
                    continue
                text = ' '.join(s['text'] for s in spans).replace('\u200b', '').strip()
                if not text or text.isdigit():
                    continue
                max_size = max(s['size'] for s in spans)
                is_bold = any('Bold' in s.get('font', '') for s in spans)
                print(f"  [{max_size:5.1f}{'B' if is_bold else ' '}] {text[:75]}")

    doc.close()
    print("\n" + "=" * 80)
    print("Review output above and adjust FONT_SIZE_H1/H2/H3/H4 if needed.")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    args = parse_args()

    # Resolve effective parameters: CLI args override top-of-file constants
    effective_input = args.input or INPUT_PDF
    effective_output = args.output or OUTPUT_MD
    effective_title = args.title or TITLE_LINE
    effective_date = args.date or PUB_DATE
    effective_org = args.org or ORGANIZATION
    effective_doi = args.doi or DOI_OR_URL

    # Diagnostic mode
    if args.diagnose:
        diagnostic_font_sizes(effective_input, sample_pages=args.sample_pages)
        sys.exit(0)

    # Validate: fail fast if INPUT_PDF placeholder was not overridden
    if effective_input == '/mnt/user-data/uploads/FILENAME.pdf':
        print("ERROR: INPUT_PDF parameter not set. Use --input or edit INPUT_PDF in script.")
        sys.exit(1)

    # Run extraction
    extract_pdf(
        input_path=effective_input,
        output_path=effective_output,
        title_line=effective_title,
        pub_date=effective_date,
        org=effective_org,
        doi=effective_doi,
        extra=ADDITIONAL_METADATA,
        no_toc=args.no_toc,
        no_header_strip=args.no_header_strip,
    )
