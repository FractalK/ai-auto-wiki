#!/usr/bin/env python3
# Last Updated: 06/07/2026 20:13 EDT
"""
PDF to Markdown Converter
========================

Converts multi-page PDFs to clean markdown using font-size-based heading classification
and smart text joining. Validated on Anthropic system cards, Nature articles, and 
academic papers.

USAGE:
------
Option A — CLI (preferred):
    python3 pdf_to_markdown.py --input /path/to/file.pdf --output /path/to/out.md \\
        --title "# Document Title" --date "Month DD, YYYY" \\
        --org "Organization" --doi "https://doi.org/..."

Option B — Edit parameters below, then:
    python3 pdf_to_markdown.py

Diagnostic mode (inspect font sizes before converting):
    python3 pdf_to_markdown.py --diagnose [--input /path/to/file.pdf]

REQUIREMENTS:
- pymupdf (fitz): pip install pymupdf --break-system-packages -q

OUTPUT:
- Markdown file with metadata header, h2/h3/h4 hierarchy, smart text joining
- Skips bare page numbers, pg. N footers, and unicode artifacts
- Detects and converts bullets (● and ○)
- Detects exhibit/figure labels and renders as bold standalone lines
- Prevents excessive line breaks in body text
- Rejoins hyphenated line-breaks (academic column layouts)

FONT SIZE THRESHOLDS (adjustable):
- h1 (##):  size >= 15.5
- h2 (###): size >= 13.5
- h3 (####): size >= 12.5
- h4 (#####): size >= 11.5 + bold
- body: default

If output is garbled, run with --diagnose to inspect actual font sizes.
"""

import argparse
import fitz
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
    if last_line.endswith('\n') or new_text.startswith('- '):
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


def extract_pdf(input_path, output_path, title_line, pub_date, org, doi, extra):
    """Main extraction pipeline."""

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

    md_lines = []
    prev_class = None

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

                # Classify by font size and bold
                max_size = max(s['size'] for s in spans)
                is_bold = any('Bold' in s.get('font', '') for s in spans)
                cls = classify(max_size, is_bold)

                # Convert bullets
                if text.startswith('● ') or text.startswith('●\t'):
                    text = '- ' + text[2:].strip()
                    cls = 'bullet'
                elif text.startswith('○ ') or text.startswith('○\t'):
                    text = '  - ' + text[2:].strip()
                    cls = 'bullet'

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
    """
    try:
        doc = fitz.open(input_path)
    except Exception as e:
        print(f"ERROR: Cannot open PDF: {e}")
        return

    print(f"\nDiagnostic: Font Sizes in {input_path}")
    print("=" * 80)

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
    )
