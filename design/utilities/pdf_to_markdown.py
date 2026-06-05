#!/usr/bin/env python3
"""
PDF to Markdown Converter
========================

Converts multi-page PDFs to clean markdown using font-size-based heading classification
and smart text joining. Validated on Anthropic system cards, Nature articles, and 
academic papers.

USAGE:
------
1. Edit parameters below (INPUT_PDF, OUTPUT_MD, TITLE_LINE, PUB_DATE)
2. Run: python3 pdf_to_markdown.py
3. Check output markdown in OUTPUT_MD

REQUIREMENTS:
- pymupdf (fitz): pip install pymupdf --break-system-packages -q

OUTPUT:
- Markdown file with metadata header, h2/h3/h4 hierarchy, smart text joining
- Skips bare page numbers and unicode artifacts
- Detects and converts bullets (● and ○)
- Prevents excessive line breaks in body text

FONT SIZE THRESHOLDS (adjustable):
- h1 (##):  size >= 15.5
- h2 (###): size >= 13.5
- h3 (####): size >= 12.5
- h4 (#####): size >= 11.5 + bold
- body: default

If output is garbled, run diagnostic_font_sizes() to inspect actual font sizes.
"""

import fitz
import re
import sys

# ══════════════════════════════════════════════════════════════════════════════
# PARAMETERS — EDIT THESE FOR EACH DOCUMENT
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

PAGE_NUMBER_REGEX = r'^\d{1,4}$'  # matches 1–4 digit bare page numbers


# ══════════════════════════════════════════════════════════════════════════════
# FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

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
    Heuristic: join flowing body text. Don't join bullets, sentence-ending lines,
    or text after headings.
    """
    if not last_line or last_line.startswith('#'):
        return False
    if last_line.endswith('\n') or new_text.startswith('- '):
        return False
    if any(last_line.endswith(char) for char in [':', '.', '%', ')']):
        return False
    return True


def extract_pdf(input_path, output_path, title_line, pub_date, org, doi, extra):
    """Main extraction pipeline."""
    try:
        doc = fitz.open(input_path)
    except Exception as e:
        print(f"ERROR: Cannot open PDF: {e}")
        sys.exit(1)

    page_count = len(doc)
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

                # Skip bare page numbers and empty lines
                if not text or re.match(PAGE_NUMBER_REGEX, text):
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
                    if prev_class in ('h1', 'h2', 'h3', 'h4'):
                        md_lines.append(text)
                    else:
                        # Smart joining for flowing body text
                        if md_lines and should_join_text(md_lines[-1], text):
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
    Run this if output appears garbled.
    """
    try:
        doc = fitz.open(input_path)
    except Exception as e:
        print(f"ERROR: Cannot open PDF: {e}")
        return

    print(f"\nDiagnostic: Font Sizes in {input_path}")
    print("=" * 80)

    for page_num in range(1, min(sample_pages + 1, len(doc))):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        print(f"\n--- Page {page_num + 1} ---")
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
    # Check for diagnostic flag
    if '--diagnose' in sys.argv:
        diagnostic_font_sizes(INPUT_PDF)
        sys.exit(0)

    # Validate parameters
    if INPUT_PDF == '/mnt/user-data/uploads/FILENAME.pdf':
        print("ERROR: INPUT_PDF parameter not set. Edit script and set INPUT_PDF path.")
        sys.exit(1)

    # Run extraction
    extract_pdf(
        input_path=INPUT_PDF,
        output_path=OUTPUT_MD,
        title_line=TITLE_LINE,
        pub_date=PUB_DATE,
        org=ORGANIZATION,
        doi=DOI_OR_URL,
        extra=ADDITIONAL_METADATA,
    )
