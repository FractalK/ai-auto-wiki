# vocabulary.json Single-Source Refactor — Execution Specification (BL-W-01)
**Last Updated:** 07/07/2026 18:12 EDT

**Status of this document:** Execution specification produced in the design project
(Fable 5 planning session, 2026-07-07, per DM-127). Executed by a Sonnet Claude Code
session in the wiki repository. Sections 1–7 govern that execution session. Section 8
governs the design-project follow-up batch after execution is confirmed. Section 9 states
environmental assumptions; Section 10 records deferred scope.

---

## 1. Purpose and Scope

Replace the five-site manual synchronization of the `competency_domains` and
`professional_contexts` controlled vocabularies with a single machine-readable source of
truth (`vocabulary.json`), runtime consumers, a generator for injected artifacts, and
mechanical lint enforcement of the one remaining human-maintained mirror.

In scope: the two teaching vocabularies only. Out of scope: `SOURCE_TYPES`, credibility
tier weights, and status vocabularies (see Section 10).

## 2. Current State

The vocabularies are replicated in five places, synchronized by ritual checklist (DM-107
as amended by DM-123; test-harness.md Section 2.5):

| # | Site | Form | Role today |
|---|------|------|-----------|
| 1 | CLAUDE.md Sections 7.1–7.2 | Markdown tables (7.1 carries a "Covers" column) | Authoritative control-document definition |
| 2 | TAGGING-SKILL.md Section 1 | Markdown tables (1.1 carries "Covers") | Self-contained skill-file copy |
| 3 | wiki-lint.py lines ~98–124 | `VALID_COMPETENCY_DOMAINS` / `VALID_PROFESSIONAL_CONTEXTS` sets | **Dead code — see audit finding below** |
| 4 | wiki-verify.sh check 14 | `VALID_CD` / `VALID_PC` bash arrays | Live: page frontmatter conformance check |
| 5 | ingest-ui-template.html lines ~331–355 | `COMPETENCY_DOMAINS` / `PROFESSIONAL_CONTEXTS` JS constants with display labels | Live: teaching-relevance composite card rendering |

All five sites were verified in exact agreement on ids on 2026-07-07 (design project
pre-flight for this spec). This is the migration baseline.

**Audit finding (planning session, 2026-07-07):** the wiki-lint.py constant sets are
referenced by no check in the script — grep confirms the two names appear only at their
definitions. The DM-107 "same delivery batch" hard requirement has been synchronizing
dead code. Page-level vocabulary conformance is enforced only by wiki-verify.sh check 14.
This spec fixes the latent gap by making the constants live (new lint step L17,
Section 4.2.3) rather than deleting them.

**Second observation:** ids are not the only replicated vocabulary. The template's
display labels and the "Covers" descriptions in CLAUDE.md 7.1 / TAGGING-SKILL 1.1 are
replicated too. A values-only JSON would leave labels and covers as a residual second
source. `vocabulary.json` therefore carries `id`, `label`, and (domains only) `covers`.

## 3. Target Architecture

```
vocabulary.json  (repo root — SOURCE OF TRUTH: id, label, covers)
    │
    ├─► wiki-lint.py          reads at startup (fail-fast); populates the two
    │                         VALID_* sets; new steps L17 (page conformance) and
    │                         L18 (artifact consistency)
    │
    ├─► wiki-verify.sh        check 14 reads it via POSIX awk (line-disciplined
    │                         format); new check 16 guards existence + format
    │
    ├─► generate-vocab-artifacts.py
    │       ├─► TAGGING-SKILL.md Section 1        (marker-delimited generated block)
    │       └─► ingest-ui-template.html constants (marker-delimited generated block)
    │
    └─► CLAUDE.md Sections 7.1–7.2   human-written MIRROR, not generated;
                                     exact agreement enforced by lint step L18a
```

Authority statement (goes into CLAUDE.md, Section 4.7 below): `vocabulary.json` is the
machine-readable source of truth for vocabulary *values, labels, and covers text*.
CLAUDE.md remains the source of truth for vocabulary *semantics and usage rules*
(thresholds, tagging criteria, expansion governance). The mirror tables exist so the
control document stays self-contained for human readers; lint guarantees they never lie.

Rationale for lint-checked mirror rather than generated CLAUDE.md tables: generating
content into the schema control document inverts authority — the document that governs
the agent would be partially written by a script the document specifies. Rejected.

## 4. Component Specifications

### 4.1 vocabulary.json

Location: wiki repository root. Committed. Initial content — byte-exact, including the
line discipline; this was validated in the design-project sandbox (JSON parses; awk
extraction yields 7 domains / 13 contexts):

```json
{
  "schema_version": 1,
  "comment": "Single source of truth for the controlled vocabularies in CLAUDE.md Sections 7.1-7.2. Edit here, update the CLAUDE.md mirror tables, then run: python3 generate-vocab-artifacts.py. Line discipline is load-bearing for wiki-verify.sh: one entry object per line, keys in order id/label/covers, double quotes, no backslashes or embedded quotes in values.",
  "competency_domains": [
    {"id": "tool-evaluation-and-selection", "label": "Tool Evaluation and Selection", "covers": "Assessing and choosing AI tools for specific use cases"},
    {"id": "practical-ai-use-and-interaction", "label": "Practical AI Use and Interaction", "covers": "Task-level use: prompting, iteration, output refinement"},
    {"id": "ai-integration-in-organizational-workflows", "label": "AI Integration in Organizational Workflows", "covers": "Embedding AI into multi-actor processes with accountability structures"},
    {"id": "output-verification-and-risk-assessment", "label": "Output Verification and Risk Assessment", "covers": "Checking outputs and evaluating workflow failure modes"},
    {"id": "ai-safety-and-alignment-literacy", "label": "AI Safety and Alignment Literacy", "covers": "Understanding alignment tradeoffs and safety-relevant behaviors"},
    {"id": "capability-horizon-awareness", "label": "Capability Horizon Awareness", "covers": "Tracking emerging capabilities and their taxonomies"},
    {"id": "attribution-ip-and-professional-integrity", "label": "Attribution, IP, and Professional Integrity", "covers": "Attribution norms, IP considerations, and disclosure practices across academic and professional contexts"}
  ],
  "professional_contexts": [
    {"id": "activism-and-civic-advocacy", "label": "Activism and Civic Advocacy"},
    {"id": "non-profit-and-ngo-work", "label": "Non-Profit and NGO Work"},
    {"id": "journalism-and-media", "label": "Journalism and Media"},
    {"id": "legal-practice", "label": "Legal Practice"},
    {"id": "domestic-civil-service-and-public-administration", "label": "Domestic Civil Service and Public Administration"},
    {"id": "foreign-service-and-diplomacy", "label": "Foreign Service and Diplomacy"},
    {"id": "organizational-leadership-and-change-management", "label": "Organizational Leadership and Change Management"},
    {"id": "project-and-program-management", "label": "Project and Program Management"},
    {"id": "teaching-and-instruction", "label": "Teaching and Instruction"},
    {"id": "graduate-and-doctoral-education", "label": "Graduate and Doctoral Education"},
    {"id": "professional-and-continuing-education", "label": "Professional and Continuing Education"},
    {"id": "entrepreneurship-and-startups", "label": "Entrepreneurship and Startups"},
    {"id": "software-and-ai-development", "label": "Software and AI Development"}
  ]
}
```

**Format discipline (normative — enforced by wiki-verify.sh check 16 and by the loader
validation in wiki-lint.py and the generator):**

- FD-1: One entry object per line; two-space top-level indent, four-space entry indent
  exactly as shown.
- FD-2: Keys in fixed order `id`, `label`, `covers`; `covers` present on
  `competency_domains` entries only.
- FD-3: `id` values match `^[a-z0-9-]+$` (kebab-case).
- FD-4: No backslashes and no embedded double quotes anywhere in `id`, `label`, or
  `covers` values. Consequence: covers text must be written without quotation marks.
- FD-5: Array-open lines are exactly `  "competency_domains": [` and
  `  "professional_contexts": [`; array-close lines are `  ],` or `  ]`.
- FD-6: File is UTF-8, LF line endings, no trailing whitespace.

The discipline exists so a POSIX-awk reader in bash 3.2 can parse the file with zero
ambiguity and so any deviation fails loudly rather than silently shrinking an allowlist.

### 4.2 wiki-lint.py changes

#### 4.2.1 Loader (replaces the two hardcoded sets)

Delete the hardcoded `VALID_COMPETENCY_DOMAINS` and `VALID_PROFESSIONAL_CONTEXTS` set
literals (current lines ~98–124) and the associated MAINTENANCE comment. Replace with a
fail-fast loader near the top of the constants section:

```python
VOCABULARY_FILE = "vocabulary.json"


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
```

The set names are preserved so any future code referencing them needs no change.
Requires `import json` (verify present; add if not).

#### 4.2.2 Step numbering

Existing lint steps run through L16 (wikilink proliferation, DM-109). New steps are L17
and L18.

#### 4.2.3 L17 — page frontmatter vocabulary conformance (new; makes the constants live)

Mechanical, Phase 1, per the DM-106 hybrid architecture. For every page in the content
directories whose frontmatter carries `competency_domains` or `professional_contexts`,
every list value must be a member of the corresponding VALID_* set. This duplicates
wiki-verify.sh check 14 on the Python side deliberately: verify is the operator-side
guard; lint is the agent-session guard; before this spec, only verify performed the
check and the lint constants were dead.

Finding: category `forced-choice`, one finding per invalid value, payload
`{"page": slug, "field": field, "value": value, "criterion": "vocabulary_conformance"}`,
remediation options presented by the lint form: (A) correct to a valid value the agent
proposes, (B) operator supplies the correct value, (C) remove the value. Hook the check
into the per-page loop alongside `check_L15_teaching_tagged_missing_fields`.

#### 4.2.4 L18 — vocabulary artifact consistency (new)

Mechanical, Phase 1. Two sub-checks:

**L18a — CLAUDE.md mirror agreement.** Parse the CLAUDE.md Section 7.1 table rows
(pattern: `| \`id\` | covers |`) and Section 7.2 rows (`| \`id\` |`). Compare against
`vocabulary.json`: (a) id sets must be equal in both directions for both vocabularies;
(b) for each domain, the CLAUDE.md covers cell must string-equal the JSON `covers`
value. Any mismatch is one finding per discrepancy: category `informational`, payload
naming the id, the side that has it (or the differing covers text), and the remediation
"edit the CLAUDE.md Section 7.1/7.2 mirror table or vocabulary.json so they agree —
vocabulary.json is authoritative for values."

**L18b — generated-block agreement.** Run
`python3 generate-vocab-artifacts.py --check` as a subprocess. Exit-code contract
(Section 4.4): 0 = in sync (no finding); 1 = drift (finding: category `informational`,
remediation "run python3 generate-vocab-artifacts.py and commit the regenerated
files"); 2 = fatal (missing/duplicated markers or invalid vocabulary.json) — wiki-lint.py
exits fatally with the generator's stderr, mirroring the loader's fail-fast posture.

L18 findings are informational but carry mandatory remediation: the lint session must
not close with an open L18 finding. (OPERATIONS.md 11.4 wording change is in the
post-execution batch, Section 8.)

Both new steps update the script's step-count constants/summary output if any exist,
and both get docstrings with the CLAUDE.md/DM references per the coding standards.

### 4.3 wiki-verify.sh changes

#### 4.3.1 Check 14 rewrite — read the allowlists from vocabulary.json

Replace the hardcoded `VALID_CD=( ... )` and `VALID_PC=( ... )` array literals and their
MAINTENANCE comment with a reader. The following was prototyped and tested in the
design-project sandbox on 2026-07-07 (positive: 7/13 extracted; negative: corrupted
entry line produces a loud format FAIL; renamed key produces an empty-allowlist FAIL).
Bash 3.2-safe (indexed-assignment array append, no `mapfile`, no associative arrays) and
POSIX/BWK-awk-safe (no `gensub`):

```bash
# Allowlists are read from vocabulary.json (source of truth — DM-127).
# The format discipline (one entry per line, fixed key order, no backslashes
# or embedded quotes in values) is normative; see
# vocabulary-json-refactor-spec.md Section 4.1. Any line inside either array
# that does not match the entry pattern is a format violation (loud FAIL),
# never a silent skip.
VOCAB_FILE="vocabulary.json"
VALID_CD=()
VALID_PC=()
VJ_FAIL=0

if [ ! -f "$VOCAB_FILE" ]; then
    fail "vocabulary.json not found at repo root — controlled-vocabulary source of truth is missing"
    VJ_FAIL=1
else
    while IFS= read -r vj_line; do
        case "$vj_line" in
            cd:*)     VALID_CD[${#VALID_CD[@]}]="${vj_line#cd:}" ;;
            pc:*)     VALID_PC[${#VALID_PC[@]}]="${vj_line#pc:}" ;;
            FORMAT:*) fail "vocabulary.json format violation at line ${vj_line#FORMAT:} — see format discipline in vocabulary-json-refactor-spec.md"; VJ_FAIL=1 ;;
        esac
    done < <(awk '
        /^  "competency_domains": \[$/    { list = "cd"; next }
        /^  "professional_contexts": \[$/ { list = "pc"; next }
        /^  \],?$/                        { list = "";   next }
        list != "" {
            if ($0 ~ /^    \{"id": "[a-z0-9-]+", "label": "[^"\\]+"(, "covers": "[^"\\]+")?\},?$/) {
                id = $0
                sub(/^    \{"id": "/, "", id)
                sub(/".*$/, "", id)
                print list ":" id
            } else {
                print "FORMAT:" NR
            }
        }
    ' "$VOCAB_FILE")

    if [ "${#VALID_CD[@]}" -eq 0 ]; then
        fail "vocabulary.json yielded an empty competency_domains allowlist — refusing to run conformance with an empty allowlist"
        VJ_FAIL=1
    fi
    if [ "${#VALID_PC[@]}" -eq 0 ]; then
        fail "vocabulary.json yielded an empty professional_contexts allowlist — refusing to run conformance with an empty allowlist"
        VJ_FAIL=1
    fi
fi
```

If `VJ_FAIL=1`, check 14 skips the per-page loop (the allowlists are unusable) and the
FAILs already emitted carry the failure. If `VJ_FAIL=0`, the existing per-page loop and
`vc_in_list` helper run unchanged against the loaded arrays.

Update the header comment block: the "no yq, python, node" environmental assumption is
preserved; add "vocabulary.json present at repo root with the normative line
discipline" to the assumptions list, and note in Limitations that the JSON reader is a
format-disciplined line parser, not a JSON parser.

#### 4.3.2 New check 16 — vocabulary.json presence and format

Insert after check 15, before the Summary block. Content: (a) file exists at root —
FAIL if absent; (b) `schema_version` line present; (c) run the same awk pass in
format-guard mode: any `FORMAT:` line is a FAIL naming the line number; (d) extracted
counts are ≥ 1 for both lists — FAIL otherwise; (e) duplicate ids within a list — FAIL
(sort/uniq -d on the extracted ids). To avoid double execution cost and drift between
two copies of the awk program, factor the reader from 4.3.1 into a function
(`load_vocab_allowlists`) defined in the Utilities section and called once before
check 14; check 16 then reports on the recorded outcome (VJ_FAIL flag, counts,
duplicate scan). Checks 14 and 16 thus share one parse.

(Ordering note: the check-numbering follows file position; the shared loader runs at
check 14's position. If the executor prefers strict "existence before use" reporting
order, renumbering the new check as 13a instead of 16 is NOT permitted — keep appended
numbering, consistent with how checks have accreted historically.)

### 4.4 generate-vocab-artifacts.py (new)

Location: wiki repository root, alongside `generate-teaching-index.py` (naming keeps the
`generate-*` convention; the hyphenated name is deliberately non-importable — consumers
use the subprocess `--check` contract, keeping exactly one rendering implementation).

Behavior:

1. Load and validate `vocabulary.json` with the same validation rules as the
   wiki-lint.py loader (4.2.1), plus FD-4 enforcement (reject backslash or `"` in any
   value) and duplicate-id rejection. Any defect: print to stderr, exit 2.
2. Render two blocks (pure functions, unit-tested):
   - **TAGGING-SKILL.md block:** the Section 1.1 and 1.2 tables, byte-deterministic,
     matching the current table structure (`| Value (use exactly as shown) | Covers |`
     for domains; single-column for contexts), preceded by the sentence "These are the
     only permitted values..." exactly as currently present within the block bounds
     chosen at migration (Step 3, Section 5).
   - **ingest-ui-template.html block:** the two JS `const` declarations,
     `COMPETENCY_DOMAINS` as `{id, label}` objects and `PROFESSIONAL_CONTEXTS` as
     `{id, label}` objects, formatted one entry per line. (`covers` is not emitted —
     the form does not display it.)
3. Locate marker pairs in each target file:
   - TAGGING-SKILL.md:
     `<!-- BEGIN GENERATED VOCABULARY — source: vocabulary.json; do not edit by hand; run: python3 generate-vocab-artifacts.py -->`
     / `<!-- END GENERATED VOCABULARY -->`
   - ingest-ui-template.html (inside the script element):
     `// BEGIN GENERATED VOCABULARY — source: vocabulary.json; do not edit by hand; run: python3 generate-vocab-artifacts.py`
     / `// END GENERATED VOCABULARY`
   A missing, duplicated, or out-of-order marker pair: stderr + exit 2 (fail fast; do
   not guess block bounds).
4. Default mode: replace block contents; write only if changed; on writing
   TAGGING-SKILL.md, update its line-2 `**Last Updated:**` stamp using
   `zoneinfo.ZoneInfo("America/New_York")` in the project's `MM/DD/YYYY HH:MM EST|EDT`
   format. Print a one-line summary per file: `unchanged` or `regenerated`. Exit 0.
5. `--check` mode: render, compare, write nothing. Exit 0 if both files match; exit 1
   if either differs (print which); exit 2 on any fatal defect. This is the L18b
   contract (4.2.4) and is also suitable for manual pre-commit use.

Style: Black, fail-fast, docstrings with usage examples, tests written and run in the
execution session before wiring L18b (coding standards).

### 4.5 TAGGING-SKILL.md changes

Insert the marker pair around Section 1's vocabulary tables (Sections 1.1 and 1.2,
including the "These are the only permitted values..." preamble if the executor elects
to include it inside the block — decide once, then the generator renders it; the
migration gate in Section 5 Step 3 requires the post-generation file to be
id/label/covers-identical to the pre-migration file either way). Add one sentence
immediately before the BEGIN marker: "The tables below are generated from
vocabulary.json. Do not edit them here." The rest of the file (decision procedure,
worked examples) is untouched and remains hand-maintained.

### 4.6 ingest-ui-template.html changes

Insert the marker pair around the `COMPETENCY_DOMAINS` and `PROFESSIONAL_CONTEXTS`
constants only. `SOURCE_TYPES` and all other constants stay outside the block
(Section 10). No rendering-logic changes.

### 4.7 CLAUDE.md changes (control-document text)

**Section 2 tree:** add two lines to the repository structure listing, adjacent to
`wiki-lint.py`:

```
├── vocabulary.json              ← controlled-vocabulary source of truth (Sections 7.1–7.2); read by wiki-lint.py and wiki-verify.sh; input to generate-vocab-artifacts.py
├── generate-vocab-artifacts.py  ← regenerates the vocabulary blocks in TAGGING-SKILL.md and ingest-ui-template.html from vocabulary.json
```

**Section 7 preamble:** replace the current two-paragraph preamble with:

```
Both vocabularies are controlled. Do not use values outside these lists during ingest
or tagging. If a concept does not map to any existing term, surface the gap rather than
inventing a new tag.

vocabulary.json at the repository root is the machine-readable source of truth for
vocabulary values, display labels, and covers text. The tables in Sections 7.1 and 7.2
are a human-readable mirror of that file; lint enforces exact agreement between them
(step L18). The vocabulary blocks in TAGGING-SKILL.md and ingest-ui-template.html are
generated from vocabulary.json by generate-vocab-artifacts.py — never edit those blocks
by hand.

Additions to either vocabulary require a schema revision and a DM entry in the design
project governance log, and are applied via the vocabulary expansion procedure in
OPERATIONS.md Section 11.6: edit vocabulary.json, update the mirror tables in this
section, run the generator, and confirm lint steps L17/L18 pass.
```

Sections 7.1/7.2 tables and Section 7.3 are unchanged. Update CLAUDE.md's line-2
timestamp on delivery.

### 4.8 OPERATIONS.md Section 11.6 changes

Insert a new step 0 block before the current step 1, and renumber or (preferred,
smaller diff) title it "Value registration" ahead of the existing numbered procedure:

```
**Value registration (perform before the retroactive pass below):**

a. Add the new entry to vocabulary.json (id, label, and — for competency domains —
   covers), preserving the file's line discipline.
b. Add the matching row to the CLAUDE.md Section 7.1 or 7.2 mirror table.
c. Run `python3 generate-vocab-artifacts.py`; commit the regenerated TAGGING-SKILL.md
   and/or ingest-ui-template.html together with vocabulary.json and CLAUDE.md.
d. Run `python3 wiki-lint.py` and confirm no L17/L18 findings, and `bash
   wiki-verify.sh` and confirm checks 14 and 16 pass.
```

The existing trigger line changes from "has been added to CLAUDE.md Section 7.1 or
7.2" to "has been added to vocabulary.json and the CLAUDE.md Section 7.1 or 7.2 mirror
(see Value registration below)". The retroactive tagging pass (steps 1–6) is unchanged.
Update OPERATIONS.md's line-2 timestamp on delivery.

## 5. Migration Sequence (single Claude Code execution session)

No commit until Step 8's gates pass; the working tree is the rollback mechanism. The
session pauses at each STOP for operator confirmation per the project's plan-then-pause
convention.

- **Step 0 — pre-flight agreement check.** Extract the ids from all five current sites
  (script the extraction; do not eyeball) and diff. Any divergence: STOP and surface —
  reconcile under the old sync rule before migrating. Also verify `import json` and
  `import re` are present in wiki-lint.py.
- **Step 1 — create vocabulary.json** with the byte-exact content in 4.1. Gate:
  `python3 -m json.tool vocabulary.json` succeeds; the awk reader extracts exactly 7
  and 13 ids.
- **Step 2 — create generate-vocab-artifacts.py** with unit tests for the render
  functions, validation rejections (bad id, embedded quote, duplicate id), marker
  fault-handling (missing/duplicated), and `--check` exit codes. Gate: tests pass.
- **Step 3 — insert markers and generate.** Add marker pairs to TAGGING-SKILL.md and
  ingest-ui-template.html; run the generator. Gate: a scripted comparison shows the
  post-generation id/label/covers content is identical to pre-migration content
  (formatting inside the blocks may normalize; values may not change). Then
  `--check` exits 0.
- **Step 4 — wiki-lint.py**: loader (4.2.1), L17 (4.2.3), L18 (4.2.4). Gate: full lint
  run against the live wiki completes with zero L17/L18 findings and no fatal exit;
  negative tests — temporarily corrupt a scratch copy of vocabulary.json and confirm
  fatal exit; temporarily hand-edit a generated block in a scratch copy and confirm an
  L18b finding.
- **Step 5 — wiki-verify.sh**: check 14 rewrite + check 16 + header updates (4.3).
  Gate: `bash wiki-verify.sh` all-PASS on the live repo; negative tests as prototyped
  (corrupted entry line → format FAIL; renamed array key → empty-allowlist FAIL).
  If a bash 3.2 binary is unavailable in the execution environment, run under
  `bash --posix` and flag LL-055 residual portability risk in the session report for
  operator verification on macOS.
- **Step 6 — control documents**: CLAUDE.md (4.7) and OPERATIONS.md (4.8) edits. Gate:
  L18a passes against the updated CLAUDE.md (proves the mirror parser works against
  the real document).
- **Step 7 — execution-time verifications** (Section 7 items). Gate: both resolved and
  recorded in the session report.
- **Step 8 — full re-run of wiki-lint.py and wiki-verify.sh**, then one atomic commit
  containing: vocabulary.json, generate-vocab-artifacts.py (+ tests),
  wiki-lint.py, wiki-verify.sh, TAGGING-SKILL.md, ingest-ui-template.html, CLAUDE.md,
  OPERATIONS.md. Commit message references DM-127 and this spec. Partial-migration
  states are never committed.
- **Step 9 — report back** to the design project: gates passed, verification outcomes,
  any deviations. This report is the trigger for the Section 8 batch.

## 6. Failure Modes and Mitigations

| Failure mode | Mechanism | Mitigation |
|---|---|---|
| Partial migration | Some consumers on JSON, others hardcoded; next vocab change diverges silently | Atomic single commit (Step 8); Step 0 agreement gate; DM-107-as-amended sync rule remains in force until execution is confirmed (DM-127) |
| Empty allowlist | Malformed JSON silently yields zero valid values | Python side: fail-fast loader. Bash side: format-guard FAIL on any nonconforming line + explicit empty-allowlist FAIL; check 14 skips rather than runs with empty arrays. Failure direction is loud in both tools (validated in sandbox) |
| Generator drift (hand edit of a generated block) | Edit between generator runs goes live | L18b `--check` comparison every lint run; do-not-edit marker text |
| Generator not run after JSON edit | JSON updated, artifacts stale | Same L18b comparison — expected content is recomputed from JSON each run |
| Mirror drift (CLAUDE.md tables) | Human edits one side only | L18a set-and-covers comparison every lint run |
| Escaped/embedded quotes in values | Breaks the awk entry pattern | FD-4 prohibition, enforced at three points: generator validation, lint loader, check 16 format guard |
| macOS awk incompatibility | gawk-only constructs | Reader uses only POSIX match/sub/gsub (no gensub); prototyped against the same constructs the existing script already relies on |
| vocabulary.json served by the public site | Root JSON exposed via GitHub Pages | Verified at execution (Section 7). Exposure is nil regardless — every value already appears in published page frontmatter |
| Fresh wiki init lacks vocabulary.json | Lint/verify fail on a new repo | Loud by design (loader fatal, check 16 FAIL); INIT-PROMPT.md gains the creation step in the Section 8 batch |

## 7. Execution-Time Verification Items

- **V-1: generate-teaching-index.py vocabulary independence.** Confirm the script does
  not hardcode either vocabulary (expected: it groups by values found in frontmatter).
  If it does hardcode, STOP and report — it becomes a sixth consumer and this spec is
  amended before commit.
- **V-2: Quartz handling of root JSON.** After the next site build, confirm
  vocabulary.json is not rendered as a page (expected: Quartz processes markdown only).
  Whether GitHub Pages serves the raw file is immaterial (values are already public);
  record the observed behavior in the session report. Do not modify ignorePatterns for
  this — keeping the [ENV] block stable avoids INIT-PROMPT churn.

## 8. Post-Execution Design-Project Batch (gated on the Step 9 report)

Executed in the design project in the session that receives execution confirmation.
Every item delivers the complete updated file per the Delivery Rule.

1. **Session Instructions:** activate the gated ritual step 6 replacement (the gated
   block was placed in the instructions on 2026-07-07): remove the three superseded
   bullets — (a) TAGGING-SKILL.md/CLAUDE.md 7.1–7.3 exact agreement, (b)
   wiki-lint.py/wiki-verify.sh same-batch vocabulary sync, (c)
   ingest-ui-implementation-plan.md Section 3 constants sync — and enact the
   replacement bullet text carried in the gate. Add vocabulary.json and
   generate-vocab-artifacts.py to the LL-040 currency-note file list.
2. **test-harness.md Section 2.5:** replace the two vocabulary hard-requirement rows
   (wiki-lint.py sets; wiki-verify.sh VALID_CD/VALID_PC arrays) with one row:
   "Controlled vocabulary values changed → edit vocabulary.json + CLAUDE.md mirror,
   run generate-vocab-artifacts.py; no script edits (scripts read vocabulary.json at
   runtime). wiki-verify.sh check 16 and lint L17/L18 enforce." Add a check-catalogue
   entry (Section 2.3) for check 16.
3. **hybrid-lint-assessment.md:** add L17 and L18 rows to the Section 2.1
   classification table (both mechanical/script) and Appendix A (script output and
   agent role: L17 forced-choice remediation; L18 informational with mandatory
   remediation).
4. **ingest-ui-implementation-plan.md Section 3:** replace the hardcoded-constants
   framing with: constants are generated from vocabulary.json between markers; the
   Section 11 maintenance note changes from "update template constants" to "run
   generate-vocab-artifacts.py".
5. **INIT-PROMPT.md:** add a step creating vocabulary.json (content from the
   repository's committed copy) and generate-vocab-artifacts.py during Phase 1. Not a
   CLAUDE.md 2.1 scaffold entry (it is tooling/config, like wiki-lint.py), so the
   Step 7 scaffold sync rule's scope does not expand.
6. **DM-127 status:** append the execution-confirmation note per governance convention
   (a References/consequences follow-up, not an amendment — DM-126 misleads-alone
   test).
7. **wiki-implementation-backlog.md:** BL-W-01 → `done`.

## 9. Environmental Assumptions

- Confirmed execution stack per DM-007: Claude Code (Pro), git repo as wiki store,
  Obsidian local, Quartz on GitHub Pages.
- wiki-verify.sh contract preserved: bash 3.2+, POSIX tools only (grep, find, wc, awk,
  ls), explicitly no yq/python/node; BWK awk compatible (macOS system awk).
- python3 ≥ 3.9 available where wiki-lint.py and the generator run (zoneinfo is
  stdlib from 3.9). Already an environmental assumption of the existing stack
  (wiki-lint.py, generate-teaching-index.py).
- Scripts execute from the wiki repository root.
- In-sandbox validation performed here (JSON content, awk reader, negative tests)
  establishes the logic, not local portability (LL-055); Step 5 carries the residual
  macOS verification note.

## 10. Deferred Scope (flagged, not planned)

- **SOURCE_TYPES:** replicated in ingest-ui-template.html and the OPERATIONS.md 11.1
  taxonomy (two sites; no lint/verify consumer). Candidate for a schema_version-2
  vocabulary.json section plus generator coverage. Not in BL-W-01; raise as a backlog
  item only if the taxonomy changes or a third consumer appears.
- **Credibility tier weights:** replicated in wiki-lint.py `CREDIBILITY_WEIGHTS` and
  CLAUDE.md Section 8. Same single-source pattern applies but touches the
  contradiction protocol's control text; treat as its own item with
  CONTRADICTION-SKILL.md in the blast radius if pursued.
- **Status vocabularies** (`VALID_STATUS` in wiki-lint.py vs. CLAUDE.md Sections
  5.2–5.6): same pattern, lower churn; not planned.
