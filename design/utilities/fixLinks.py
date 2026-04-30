import pathlib, re, sys

DIRS = ["topics", "tools", "sources", "comparisons", "pitfalls", "teaching"]

# Matches: optional indent + "- " + unquoted [[...]]
BLOCK_ITEM = re.compile(r'^(\s*-\s+)(\[\[.*?\]\])(\s*.*)$')
# Matches: field-name: unquoted [[...]]
SINGLE_VALUE = re.compile(r'^(\s*[\w_]+:\s+)(\[\[.*?\]\])(\s*.*)$')

def fix_file(path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    result = []
    fm_delimiters = 0
    changed = False

    for line in lines:
        stripped = line.strip()
        if stripped == "---":
            fm_delimiters += 1
            result.append(line)
            continue

        # Only operate inside frontmatter (between delimiter 1 and 2)
        if fm_delimiters == 1:
            m = BLOCK_ITEM.match(line.rstrip('\n'))
            if m and not m.group(2).startswith('"'):
                line = m.group(1) + '"' + m.group(2) + '"' + m.group(3) + '\n'
                changed = True
            else:
                m2 = SINGLE_VALUE.match(line.rstrip('\n'))
                if m2 and not m2.group(2).startswith('"'):
                    line = m2.group(1) + '"' + m2.group(2) + '"' + m2.group(3) + '\n'
                    changed = True

        result.append(line)

    if changed:
        path.write_text("".join(result), encoding="utf-8")
        print(f"  fixed: {path}")
    return changed

fixed = []
for d in DIRS:
    for p in pathlib.Path(d).rglob("*.md"):
        if fix_file(p):
            fixed.append(str(p))

print(f"\n{len(fixed)} files updated.")