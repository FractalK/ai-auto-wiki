# Ingest Decision Form — Implementation Plan
**Last Updated:** 01/05/2026 14:00

---

## 1. Overview

### What gets built

A self-contained HTML decision form that Claude Code generates at the end of every
pre-flight pass. The human opens it in a browser, clicks through choices, and copies
a single decision string to paste back into Claude Code. It replaces the current
text-block + manual-typing model.

### Files created or modified

| File | Action | Description |
|---|---|---|
| `ingest-ui-template.html` | Create (committed) | Persistent HTML/JS template; contains rendering logic and controlled vocabulary; Claude Code injects choices JSON at runtime |
| `ingest-decisions.html` | Generated per session (gitignored) | Session-specific form; produced by injecting choices JSON into template |
| `OPERATIONS.md` | Modify | Replace pre-flight report surfacing step with form-generation step; inline choices JSON schema |
| `.gitignore` | Modify | Add `ingest-decisions.html` |
| `quartz.config.ts` | Modify | Add `ingest-ui-implementation-plan.md` to `ignorePatterns` |

### Scope boundaries

**v1 covers:** All pre-flight forced choices (Steps 0, 2, 3, 5, 6, 7, 7a, 8, 9 of
the ingest workflow). These are the choices surfaced in the pre-flight report block
before Phase 2 begins.

**v1 defers:** Post-ingest forced choices (Step 12a/13b teaching notes assessments;
FRIC-031 Key Claims eviction when implemented). These fire after execution, not during
pre-flight, and require a separate design decision about when and how to present them.

---

## 2. Forced Choice Catalog

All pre-flight choices Claude Code must encode in the choices JSON, by choice type:

### single-select

Used when exactly one option from a small lettered set is required.

| Origin step | Description | Options | Recommended |
|---|---|---|---|
| Step 0 (N > 5) | Batch size selection | A=Process first 5 / B=Process first 10 / C=Process all N / D=I will specify (free text) / E=Defer | A |
| Step 2 | Duplicate URL detected | A=Abort / B=Enrich | determined by agent |
| Step 3 (ambiguous) | Source type classification | one option per applicable source type (see Section 3.2) | agent's best guess |
| Step 5 (ambiguous) | Model/application class | enumerated class values | agent's best guess |
| Step 7 | Comparison page proposal | A=Create / B=Skip | A |
| Step 7a | Pitfalls page proposal | A=Create or Update / B=Skip | A |
| Step 9 | decay_exempt proposal | A=Yes / B=No | A |

Step 0 option D is a special case: see `conditional-text` below.

### text-with-default

Used when the agent proposes a value the human can accept or override.

| Origin step | Description | Default value |
|---|---|---|
| Step 6 (new page) | Proposed slug for a new page | agent-generated slug |

### conditional-text

A single-select where one specific option reveals a free-text input.

| Origin step | Description | Trigger option |
|---|---|---|
| Step 0 option D | Specify which documents to process | D |

When option D is selected, a text area appears. Placeholder: `Enter filenames or URLs,
one per line`. Required before form can be submitted if D is selected.

### composite (teaching-relevance)

Unique card type for Step 8 teaching relevance proposals. Combines a boolean toggle
with two multi-select controlled vocabulary fields that activate conditionally.

| Sub-field | Control | Values |
|---|---|---|
| Accept teaching_relevance: true | Toggle (Accept / Decline) | boolean |
| competency_domains | Checkboxes | Section 7.1 vocabulary (7 values; see Section 3.1) |
| professional_contexts | Checkboxes | Section 7.2 vocabulary (13 values; see Section 3.1) |

Behaviour: when Accept is selected, domain and context checkboxes activate and are
pre-checked with the recommended values the agent proposes. When Decline is selected,
all checkboxes are disabled and greyed out. At least one domain and one context must
be checked when Accept is selected — form blocks submission otherwise.

---

## 3. Controlled Vocabulary Reference (Hardcoded in Template)

These values are baked into `ingest-ui-template.html` as a JavaScript constant.
They do not come from the choices JSON. If CLAUDE.md Sections 7.1–7.2 are updated,
the template must be updated to match.

### 3.1 competency_domains (Section 7.1)

```javascript
const COMPETENCY_DOMAINS = [
  { id: "tool-evaluation-and-selection",
    label: "Tool Evaluation and Selection" },
  { id: "practical-ai-use-and-interaction",
    label: "Practical AI Use and Interaction" },
  { id: "ai-integration-in-organizational-workflows",
    label: "AI Integration in Organizational Workflows" },
  { id: "output-verification-and-risk-assessment",
    label: "Output Verification and Risk Assessment" },
  { id: "ai-safety-and-alignment-literacy",
    label: "AI Safety and Alignment Literacy" },
  { id: "capability-horizon-awareness",
    label: "Capability Horizon Awareness" },
  { id: "attribution-ip-and-professional-integrity",
    label: "Attribution, IP, and Professional Integrity" }
];
```

### 3.2 professional_contexts (Section 7.2)

```javascript
const PROFESSIONAL_CONTEXTS = [
  { id: "activism-and-civic-advocacy",       label: "Activism and Civic Advocacy" },
  { id: "non-profit-and-ngo-work",           label: "Non-Profit and NGO Work" },
  { id: "journalism-and-media",              label: "Journalism and Media" },
  { id: "legal-practice",                    label: "Legal Practice" },
  { id: "domestic-civil-service-and-public-administration",
    label: "Domestic Civil Service and Public Administration" },
  { id: "foreign-service-and-diplomacy",     label: "Foreign Service and Diplomacy" },
  { id: "organizational-leadership-and-change-management",
    label: "Organizational Leadership and Change Management" },
  { id: "project-and-program-management",    label: "Project and Program Management" },
  { id: "teaching-and-instruction",          label: "Teaching and Instruction" },
  { id: "graduate-and-doctoral-education",   label: "Graduate and Doctoral Education" },
  { id: "professional-and-continuing-education",
    label: "Professional and Continuing Education" },
  { id: "entrepreneurship-and-startups",     label: "Entrepreneurship and Startups" },
  { id: "software-and-ai-development",       label: "Software and AI Development" }
];
```

### 3.3 source_types (Section 11.1)

```javascript
const SOURCE_TYPES = [
  { id: "research-paper",         label: "Research Paper" },
  { id: "industry-blog",          label: "Industry Blog" },
  { id: "white-paper",            label: "White Paper" },
  { id: "publication-article",    label: "Publication Article" },
  { id: "youtube-video",          label: "YouTube Video" },
  { id: "podcast-transcript",     label: "Podcast Transcript" },
  { id: "practitioner-reference", label: "Practitioner Reference" },
  { id: "vendor-content",         label: "Vendor Content" },
  { id: "policy-document",        label: "Policy Document" }
];
```

---

## 4. Choices JSON Schema

**Authority note:** The choices JSON schema is reproduced inline in `OPERATIONS.md`
Section 11.2 and that copy is authoritative at runtime. Claude Code reads OPERATIONS.md
at every session start and must not depend on this file at runtime. The schema below is
the design record; OPERATIONS.md is the operational source of truth.

Claude Code writes this JSON as a `<script>` block injected into the template at
runtime. The injection point in the template is the string `%%CHOICES_JSON%%`.

### Top-level structure

```json
{
  "session_date": "YYYY-MM-DD",
  "source_title": "Descriptive source title for the form header",
  "choices": [ ...choice objects... ]
}
```

### Choice object — single-select

```json
{
  "id": 1,
  "type": "single-select",
  "context": "Full prose context as it would appear in the pre-flight report. One to four sentences.",
  "recommended": "A",
  "required": true,
  "options": [
    { "id": "A", "label": "Option text as it appears in the pre-flight report" },
    { "id": "B", "label": "..." }
  ]
}
```

`recommended`: the option id the agent would select if not overridden. Required on all
single-select choices. If the agent genuinely cannot recommend (true toss-up), set
`"recommended": null` — the form will flag this card as requiring active selection
before the string can be copied.

### Choice object — conditional-text (Step 0 option D)

```json
{
  "id": 1,
  "type": "single-select",
  "context": "...",
  "recommended": "A",
  "required": true,
  "options": [
    { "id": "A", "label": "Process first 5 documents — safe at any hour [recommended]" },
    { "id": "B", "label": "Process first 10 documents" },
    { "id": "C", "label": "Process all {N} documents" },
    { "id": "D", "label": "I will specify which documents to process",
      "reveals_text": true,
      "text_placeholder": "Enter filenames or URLs, one per line",
      "text_required": true },
    { "id": "E", "label": "Defer — abort ingest and save queue state for next session" }
  ]
}
```

`reveals_text: true` on an option object causes a text area to appear below that
option's button when it is selected.

### Choice object — text-with-default (slug)

```json
{
  "id": 3,
  "type": "text-with-default",
  "context": "A new page must be created. Proposed slug:",
  "recommended": "2026-attention-mechanisms",
  "required": true
}
```

The text field is pre-filled with `recommended`. The human edits in place or accepts.
No option buttons — just the text field and a label.

### Choice object — composite (teaching-relevance)

```json
{
  "id": 7,
  "type": "teaching-relevance",
  "context": "[[page-slug]] qualifies for teaching relevance tagging. Proposed domains: ...",
  "recommended": {
    "accept": true,
    "competency_domains": ["tool-evaluation-and-selection", "practical-ai-use-and-interaction"],
    "professional_contexts": ["teaching-and-instruction", "professional-and-continuing-education"]
  },
  "required": true
}
```

The template hardcodes the full vocabulary lists (Section 3 above) and pre-checks
whichever values appear in `recommended.competency_domains` and
`recommended.professional_contexts`.

---

## 5. Decision String Format

The form assembles a single-line string plus an optional DOCUMENTS block.

### Standard line

```
1:A 2:research-paper 3:B 4:true:tool-evaluation-and-selection,practical-ai-use-and-interaction:teaching-and-instruction,professional-and-continuing-education 5:2026-my-proposed-slug
```

Rules by choice type:

| Type | Format | Example |
|---|---|---|
| single-select | `N:option-id` | `1:A` |
| single-select where D selected (no free text) | `N:D` | `1:D` |
| text-with-default | `N:slug-value` | `5:2026-attention-mechanisms` |
| teaching-relevance (accept) | `N:true:domain1,domain2:context1,context2` | `7:true:tool-evaluation-and-selection:teaching-and-instruction` |
| teaching-relevance (decline) | `N:false` | `7:false` |

### DOCUMENTS block (Step 0 option D only)

When option D is selected, append a labelled block after the decision line:

```
1:A 2:B 3:D 4:B

DOCUMENTS:
2026-some-paper.pdf
https://example.com/article
raw-notes.md
```

The DOCUMENTS block is omitted entirely when option D is not selected.

### Copy button behaviour

The form displays the assembled decision string in a prominent read-only text box
that updates live as selections change. A "Copy to clipboard" button copies the
complete string (decision line + DOCUMENTS block if present). The button label
changes to "Copied!" for 1.5 seconds after copy.

---

## 6. HTML Template Behaviour Specification

### Load state

On load: every choice is in its recommended state. The decision string is already
assembled and copyable. A user who agrees with all recommendations can copy and paste
without clicking anything.

### Deviation tracking

Any card where the current selection differs from `recommended` receives a visible
"Modified" indicator (e.g., a coloured left border or a small pill badge). This is
computed live on every change event.

### Review panel

A sticky panel (fixed to the right side on wide screens, or below the form on narrow
screens) that lists only the choices currently differing from recommendations, as a
compact summary. When all choices match recommendations, the panel shows:
"All recommended values selected."

### Restore controls

- **Per-card restore:** Each modified card shows a small "Reset to recommended" link
  below the controls. Clicking it restores that card's selection to `recommended` and
  removes the "Modified" indicator. The link is hidden when the card is unmodified.
- **Global restore:** A "Restore all recommendations" button above the decision string
  output. Clicking it shows a confirmation message ("This will reset all your changes.
  Continue?") with Confirm / Cancel buttons. On Confirm: all cards reset to recommended,
  review panel clears.

### Required-but-no-recommendation cards

If a choice has `recommended: null`, the card is visually flagged as "Required —
please select." The copy button is disabled until all such cards have a selection.
When the last required card receives a selection, the copy button enables automatically.

### Teaching-relevance card

The card renders as:
1. A two-button toggle at the top: **Accept** / **Decline** (pre-selected per
   `recommended.accept`)
2. When Accept is selected: two multi-column checkbox grids appear below — one for
   competency_domains, one for professional_contexts — pre-checked per recommended
   values. Minimum one selection in each grid is enforced; if the user unchecks all
   boxes in either grid, a validation message appears and the copy button disables.
3. When Decline is selected: both checkbox grids are hidden.

### Option D text area (Step 0)

When option D is selected from the button group, a text area slides in below the
buttons. The text area is empty (no default). The form cannot be submitted (copy
button disabled) while D is selected and the text area is empty.

### Form width and typography

Design for readability over aesthetics. Each card is a distinct visual block. Context
text renders as readable prose (not monospace). Option buttons are large enough to click
comfortably without precision. The decision string output uses monospace to signal
"this is code to paste."

No external CSS or JS dependencies. Everything inline in the HTML file.

---

## 7. OPERATIONS.md Change

### Location

The change replaces the pre-flight report surfacing step, which currently reads:

```
**Pre-flight report format:**

Pre-flight report — {source title}
{N} decisions require your input. Respond with: 1:A 2:B ...
...
```

This block is removed and replaced with the Form Generation Step below.

### New text to insert

Replace the `**Pre-flight report format:**` block in its entirety with the following:

---

**Pre-flight report — form generation**

After completing all pre-flight analysis steps (Steps 0 through 9), serialize all
identified decisions to a choices JSON object conforming to the schema below. Then:

[Choices JSON schema inlined here — see OPERATIONS.md Section 11.2 for the
authoritative runtime copy. See `ingest-ui-implementation-plan.md` Section 4 for
the design record.]

1. Read `ingest-ui-template.html` from the wiki root.
2. Replace the string `%%CHOICES_JSON%%` with the serialized choices JSON.
3. Write the result to `ingest-decisions.html` at the wiki root.
4. Report to the human:

```
Pre-flight complete. {N} decisions identified for [[{source-title}]].

Open ingest-decisions.html in your browser:
  open ingest-decisions.html

Make your selections. When satisfied, copy the decision string and paste it here.
```

Do not proceed to Phase 2 until the human pastes a decision string. Parse the
decision string by matching each `N:value` token to choice id `N` in the choices
JSON. For teaching-relevance choices, decode the colon-delimited sub-fields. For
option-D text, read the DOCUMENTS block below the decision line. Execute Phase 2 with
all decisions resolved.

---

**Note on the text pre-flight summary:** Claude Code should still produce a brief
internal working summary of all pre-flight findings (source classification, affected
pages, proposed decisions) as session output for context and auditability. This is not
surfaced to the human as a decision prompt — it is background record-keeping. The form
is the sole human input mechanism for pre-flight decisions.

---

## 8. .gitignore Addition

Append the following line to `.gitignore` in the wiki root:

```
ingest-decisions.html
```

Place it in the same block as other generated/temporary files. No other change to
`.gitignore` is required.

---

## 9. Claude Code Session Plan

Execute in this exact order. Do not proceed to a step without completing the prior one.

**Step 1 — Read the schema files**

Read `CLAUDE.md` Sections 7.1 and 7.2 to confirm vocabulary values match Section 3
of this plan. Read `OPERATIONS.md` Section 11.2 to confirm the pre-flight step
sequence and forced choice formats match the catalog in Section 2 of this plan.
Surface any discrepancy to the human before writing any code.

**Step 2 — Write `ingest-ui-template.html`**

Implement the template per Sections 3–6 of this plan. The template must:
- Be entirely self-contained: no external CSS, fonts, or JS dependencies
- Contain the hardcoded vocabulary constants from Section 3 (COMPETENCY_DOMAINS,
  PROFESSIONAL_CONTEXTS, SOURCE_TYPES)
- Contain the `%%CHOICES_JSON%%` injection placeholder as a JavaScript variable
  assignment: `const CHOICES = %%CHOICES_JSON%%;`
- Implement all four choice types: single-select, text-with-default, conditional-text
  (via `reveals_text` on option), and composite teaching-relevance
- Implement pre-selection, deviation tracking, review panel, per-card restore, and
  global restore as specified in Section 6
- Implement decision string assembly and copy button
- Implement required-but-no-recommendation validation
- Not write any files (browsers cannot write to the local filesystem from file:// URLs)
- Open correctly when launched as a file:// URL on macOS (no server required)

After writing the template, generate a minimal smoke-test choices JSON (covering at
least one of each choice type) and inject it manually to verify the form renders and
the decision string assembles correctly. Run `open ingest-decisions-test.html` to
verify in the browser. Report the result. Do not proceed to Step 3 until the test
passes.

**Step 3 — Update `OPERATIONS.md`**

Apply the change specified in Section 7 of this plan. Replace the
`**Pre-flight report format:**` block with the Form Generation Step text, including
the inlined choices JSON schema. No other changes to `OPERATIONS.md`. Verify the
surrounding section structure is intact after the edit.

**Step 4 — Update `.gitignore`**

Append `ingest-decisions.html` per Section 8 of this plan. Verify the line is present
with `grep ingest-decisions .gitignore`.

**Step 5 — Commit**

Commit all changes with message:
`feat: add ingest decision form (ingest-ui-template.html)`

Include in the commit:
- `ingest-ui-template.html`
- `.gitignore`
- `OPERATIONS.md`

Do not commit `ingest-decisions.html` (it will be gitignored). Verify with
`git status` that it does not appear as staged.

**Step 6 — Report to human**

Confirm completion and provide usage instructions:
- Where `ingest-ui-template.html` lives and what it is
- How the form appears in the ingest workflow (when Claude Code will generate it)
- How to open it: `open ingest-decisions.html` on macOS
- What the copy-paste interaction looks like

---

## 10. Design Decisions and Rationale

**Why self-contained HTML instead of a TUI**

The spatial layout requirement — seeing all choices simultaneously before committing —
cannot be satisfied well in a linear terminal UI. A browser form is the only model that
supports spatial layout without a server. The copy-paste return path is one interaction
and is not materially worse than any alternative.

**Why a persistent template rather than full generation each session**

A persistent template separates the rendering logic (stable, rarely changes) from the
session data (changes every ingest). Full regeneration each session is wasteful (Claude
Code spending tokens on boilerplate HTML/JS) and makes UI bugs harder to isolate.
The template is a committed file with a clear maintenance boundary: controlled
vocabulary changes require a template update; adding new choice types requires a
template update; changing the layout or visual design requires a template update.
Adding a new forced choice to the workflow does not require a template update — the
JSON drives that.

**Why option ids instead of letters for enumerated choices**

Using the actual controlled vocabulary value (e.g., `research-paper`) in the decision
string rather than a letter (`A`) eliminates the need for Claude Code to maintain a
mapping between letter and value during Phase 2 parsing. It also makes the decision
string human-readable, which simplifies debugging.

**Why the DOCUMENTS block format for option D**

Free-text document lists may contain spaces, commas, and other characters that would
break a compact `N:D:val1,val2` encoding. A separate labelled block below the decision
line is unambiguous and handles arbitrary document names without escaping.

**Why post-ingest choices are deferred**

Post-ingest choices (teaching notes assessments) fire after Phase 2 execution and
require the agent to have written page content before the choices can be formulated.
They cannot be folded into the pre-flight form without changing the two-phase model.
A v2 could generate a second form at the end of Phase 2, but that is a separate design
problem with different constraints.

**Why the schema is inlined in OPERATIONS.md rather than referenced by filename**

OPERATIONS.md is loaded at every wiki session start. Inlining the schema there makes
it available to Claude Code without requiring a secondary file read. The plan document
(`ingest-ui-implementation-plan.md`) is a design artifact, not an operational document,
and Claude Code should not depend on it at runtime. The plan retains the schema as a
design record; OPERATIONS.md is authoritative.

---

## 11. Maintenance Notes

**When CLAUDE.md Sections 7.1 or 7.2 change:**
Update the vocabulary constants in `ingest-ui-template.html` and the JavaScript
constants in the template file. These must remain in exact agreement with CLAUDE.md.
Also update Section 3 of this plan to keep the design record current.

**When a new pre-flight forced choice type is added to OPERATIONS.md:**
If the new choice maps to an existing JSON type (single-select, text-with-default,
teaching-relevance), no template change is required — Claude Code adds the new choice
object to the JSON. If the new choice requires a new control type, add the type to the
template before deploying. Update Section 2 of this plan to add the new choice to the
catalog.

**When FRIC-031 is implemented (Key Claims eviction):**
The eviction forced choice fires during Phase 2, not pre-flight. It belongs in the
post-ingest form if v2 is ever built. Do not add it to the pre-flight form.

**When the decision string format is extended:**
Update Section 5 of this plan and the OPERATIONS.md inlined schema (Section 11.2).
The template's assembler function must be updated to match any format change.

**Publishing exclusion:**
`ingest-ui-implementation-plan.md` is excluded from Quartz publishing via
`ignorePatterns` in `quartz.config.ts`. It is a design artifact, not wiki content.
Do not remove this exclusion.
