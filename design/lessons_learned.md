# Lessons Learned
**Last Updated:** 07/25/2026 13:38 ET

Append-only log. Each entry documents a problem encountered, its root cause,
the fix applied, and the implication going forward.

Reference format from other documents: `# See LL-NNN`

**Mutability rules:**
- Append only. No existing entry's substantive content is ever edited after it is
  written, except for one narrow exception (DM-147, `decisions_made.md`): a
  gov_lint-flagged conformance correction to an entry's *form* (status-value casing,
  field-name repair, heading format) may be made in place, under mandatory guards
  logged in the DM that makes the correction. See `decisions_made.md` DM-147 for the
  full rule; it applies across all four append-only logs, not to this file alone.
- If a later entry reveals that a prior root cause diagnosis was wrong, add a new entry
  referencing the earlier one — do not correct the original.
- Entries are added at the close of any chat where a mistake was made and fixed,
  or where collaboration encountered friction that required remediation.

---

## Entry Template

```
## LL-NNN | [SHORT DESCRIPTIVE TITLE]

- **Date:** YYYY-MM-DD
- **Context:** [One sentence: what we were doing when this occurred]

**Problem:**
[What went wrong or caused friction.]

**Root Cause:**
[Why it actually happened.]

**Fix Applied:**
[Exactly what was done to resolve it in this instance.]

**Implication Going Forward:**
[What to do differently. Write as a directive.]

**References:** IN-NNN, DM-NNN
```

---

## LL-001 | Failed to Deliver Updated Project Instructions as a File

- **Date:** 2026-04-15
- **Context:** Evaluating project instructions and recommending changes during project initialization chat.

**Problem:**
Instruction evaluation and recommendations were delivered as inline chat prose. No updated instructions file was produced, despite the Delivery Rule requiring that any created or updated project artifact be delivered as a downloadable file.

**Root Cause:**
The evaluation was framed as advisory commentary rather than as a document update. The Delivery Rule was applied only to the three governance files, not to the project instructions themselves — which are also a project artifact subject to the same rule.

**Fix Applied:**
Produced the full updated instructions file on explicit request.

**Implication Going Forward:**
When producing recommendations that modify any project artifact — including the project instructions — always deliver the revised artifact as a file in the same response as the recommendations. Do not wait to be asked.

**References:** —


---

## LL-002 | Failed to Proactively Propose Weighted Contradiction Model

- **Date:** 2026-04-18
- **Context:** Designing the contradiction resolution protocol during the ingest workflow session.

**Problem:**
The original flat flag-and-wait contradiction protocol (DM-003) was designed and accepted without proposing a more automated alternative. The weighted three-path model — which meaningfully reduces human intervention frequency and is a better fit for the team's ingest cadence — was only surfaced when the user asked whether a more automated approach existed.

**Root Cause:**
The flat protocol satisfied the stated requirement (avoid silent overwriting, preserve human visibility) and was not pressure-tested against the operational constraint (high ingest cadence, risk of human review becoming a bottleneck). The design brief emphasized correctness over friction, and the friction implications of the flat protocol were not analyzed proactively.

**Fix Applied:**
Weighted three-path model designed and confirmed as DM-023, amending DM-003.

**Implication Going Forward:**
When designing any workflow step that involves human intervention, explicitly analyze the intervention frequency at the team's stated operational cadence before proposing the design. If the frequency is high enough to create a bottleneck risk, propose a more automated alternative alongside the conservative option. Do not wait to be asked.

**References:** DM-003, DM-023

---

## LL-003 | Failed to Warn Proactively About Context Limit

- **Date:** 2026-04-18
- **Context:** Running a long multi-item design session with an explicit instruction to warn when the session was getting too long.

**Problem:**
The user gave an explicit instruction at session start: warn if the session is getting too long or consuming too many tokens. No warning was issued. The context risk was flagged only after the user asked directly whether to continue.

**Root Cause:**
The instruction used vague language ("too long") with no concrete threshold. Without a precise trigger condition, the instruction was treated as a background concern rather than an active monitoring obligation. When the agenda was moving forward productively, there was no natural forcing function to pause and assess.

**Fix Applied:**
End-of-chat ritual run, carry-forward prompt produced, lessons learned entry added.

**Implication Going Forward:**
Do not accept vague context-limit instructions. At session start, if a context warning instruction is present, immediately restate it as a concrete checkable condition — e.g., "I will warn after each agenda item if remaining items cannot be completed at full quality." If the instruction does not specify a trigger, ask for one or propose one explicitly. Monitor at each agenda item boundary, not continuously. Do not wait to be asked.

**References:** —


---

## LL-004 | Delivered Carry-Forward Prompt as Chat Block Instead of File

- **Date:** 2026-04-19
- **Context:** Producing the carry-forward prompt at the end of a multi-item design session.

**Problem:**
The carry-forward prompt — a substantial multi-section document — was delivered as an
inline chat block rather than a downloadable file, requiring the user to manually copy
a large text from the chat interface.

**Root Cause:**
The carry-forward prompt was treated as conversational output rather than a project
artifact. The Delivery Rule was applied to governance file updates but not to the prompt
itself, despite the prompt being longer than most of the files delivered alongside it.

**Fix Applied:**
Prompt re-delivered as a downloadable file on user request.

**Implication Going Forward:**
Any output intended to be carried forward, pasted, or reused should be delivered as a
downloadable file if it exceeds a few sentences. Length is the trigger, not category
membership. The carry-forward prompt is a project artifact by function — treat it as
one at production time, not on request.

**References:** —


---

## LL-005 | Rationalized Case-Specific Exceptions to Unconditional Delivery Rule

- **Date:** 2026-04-19
- **Context:** Producing end-of-chat ritual deliverables including decisions_made.md and
  updated project instructions.

**Problem:**
Two project files requiring full-file delivery were delivered as partial artifacts:
decisions_made.md was delivered as an append-only fragment, and the project instructions
were delivered as a targeted section replacement block. Both required the user to manually
assemble the final files.

**Root Cause:**
In both cases a case-specific rationalization was constructed to justify partial delivery:
(1) For decisions_made.md: the file's append-only mutability model was misread as a
delivery scope rule — only the new content "matters," so only the new content need be
delivered. (2) For the project instructions: a claimed inability to reproduce unchanged
content accurately was used to justify partial delivery, rather than stopping to ask or
verifying that the content was available in context. Both files were fully available in
the context window. The Delivery Rule has no exceptions for these cases. The
rationalizations were invented, not derived from the rule.

**Fix Applied:**
User assembled both files manually. Delivery Rule amended with two explicit
anti-rationalization clauses. LL-005 added.

**Implication Going Forward:**
Apply the Delivery Rule unconditionally. Do not assess whether a case-specific exception
is warranted — none exist beyond the one explicitly stated in the rule (user explicitly
asks for a snippet or diff). Two specific rationalizations to reject: (1) A file's
mutability model (append-only, rolling overwrite, etc.) describes how the file is
maintained, not how deliverables are scoped. A project file that has been updated is
always delivered in full. (2) Uncertainty about whether unchanged content can be
reproduced accurately is not a basis for partial delivery — it is a trigger to stop
and ask before delivering anything. If content is in the context window, reproduce it.
If it is not, ask.

**References:** —


---

## LL-006 | Implementation-Handoff Scaffold Template Defects Escaped Cross-Reference Check

- **Date:** 2026-04-20
- **Context:** Fixing pre-existing defects in implementation-handoff.md Section 1.3
  discovered during this session's INIT-PROMPT.md production work.

**Problem:**
Two scaffold file templates in implementation-handoff.md Section 1.3 contained body
content not present in CLAUDE.md Section 2.1 — the authoritative source. `log.md`
template included a `# Operation Log` heading below the frontmatter fence; `raw/queue.md`
template included a `# Source Queue` heading above the `## [queued]` section. Both
contradicted Section 2.1 directly. Both escaped the cross-reference check run at the
end of the prior session, despite the check being explicitly specified in the ritual.

**Root Cause:**
The cross-reference check instruction states: "Does implementation-handoff.md Section 1.3
agree with CLAUDE.md Section 2.1 on initialization scaffold file content and field
values?" The check was interpreted narrowly — comparing frontmatter field names and
initial values only — rather than comparing complete template body content. The extra
body lines (`# Operation Log`, `# Source Queue`) are outside the frontmatter fence and
were not caught by a field-name comparison.

**Fix Applied:**
Both spurious body lines removed from implementation-handoff.md Section 1.3 this
session. INIT-PROMPT.md (produced from Section 2.1 directly) did not have either
defect and required no correction.

**Implication Going Forward:**
When running the Section 2.1 / implementation-handoff.md cross-reference check, compare
the complete rendered content of each scaffold file template — everything between the
opening and closing markdown fence — not only frontmatter field names and values. A line
that appears outside the frontmatter fence but inside the template fence is part of the
scaffold file content and must match Section 2.1 exactly.

**References:** —


---

## LL-007 | Executed Work That Was Explicitly Scoped for the Carry-Forward

- **Date:** 2026-04-20
- **Context:** User asked to add new tasks (technical_depth field, discovery source
  expansion) to the carry-forward prompt for execution in the next chat session, after
  the current session had already completed its stated agenda items and was in
  end-of-chat ritual.

**Problem:**
User stated explicitly: "I want to add them to the carry-forward prompt to be handled
first, knowing that I likely will have to cut the next chat short." This is an
instruction to update a planning document, not to execute the work. The work was
executed in the current session instead — file changes made, governance entries written,
DM numbers assigned — consuming remaining context capacity that the user had already
signaled was limited.

**Root Cause:**
The design content of the request (source list candidates, field design questions,
user confirmations) was pattern-matched as execution approvals rather than as
design decisions to be captured for planning purposes. The operative instruction
("add to the carry-forward") was subordinated to the content of the confirmations.
The session-context warning condition was active and should have reinforced deference
to the carry-forward, but it did not override the execution reflex.

**Fix Applied:**
Work was already done and confirmed correct by the user. No rollback. LL-007 added.

**Implication Going Forward:**
When a user says "add X to the carry-forward," the correct and complete action is to
update the carry-forward document with X as a fully-specified, executable agenda item.
Do not execute X. Do not treat confirmations obtained in service of writing the
carry-forward description as green-lights for immediate execution. If the session has
already completed its stated agenda and is in end-of-chat ritual, any new scope goes
into the carry-forward by default unless the user explicitly says "do it now."

**References:** —


---

## LL-008 | Lint forced-choice step inserted after consolidation step, creating silent miss

**Date:** 2026-04-21
**Context:** Schema design — lint procedure editing

**Problem:**
A new forced-choice lint step (deferred-ingest staleness check) was initially numbered
L14 and placed after the L13 consolidation step. This meant the forced choice would
not be included in the consolidated pre-flight report, making it unreachable to the
agent during normal lint Phase 1 execution.

**Root Cause:**
The insertion was made by appending to the end of a prior str_replace block rather
than by analyzing the lint step sequence first and identifying the correct insertion
point. L13's role as the consolidation step — which must come after all assessment
steps that generate forced choices — was not checked before placement.

**Fix Applied:**
Renumbered the step to L12b (before L13) and updated L13's forced-choice order list
to include it. The duplicate L13 block created by the initial error was removed.

**Implication Going Forward:**
Before inserting any new lint step that generates a forced choice, verify it is
numbered before L13. Any step numbered L13 or higher cannot generate forced choices
that appear in the consolidated pre-flight report. When adding new lint steps: read
the full L1–L14 sequence first, assign the correct number, then execute the str_replace.

**References:** —


---

## LL-009 | Session-Start Template Cross-References Not Updated When Template Was Extended

- **Date:** 2026-04-21
- **Context:** Pre-implementation readiness review — cross-referencing all artifacts
  before handing off to the implementation project.

**Problem:**
Three defects found in companion reference documents:
(1) INIT-PROMPT.md Step 12 cited "implementation-handoff.md Section 3" for the
session-start template — the document has no Section 3; the template is in Section 5.
(2) portability-review.md Section 6 item 13 made the same wrong Section 3 reference.
(3) tooling-recommendation.md Section 7 contained an older version of the session-start
template missing Step 5 (the deferred-ingest.md check), which was added to the
authoritative template in implementation-handoff.md Section 5 after tooling-recommendation.md
was written.

**Root Cause:**
The session-start template in implementation-handoff.md was the authoritative version
that received updates (Step 5 added, section number assigned). The two companion
documents that reference or reproduce the template were not updated when the authoritative
template changed. No cross-reference check specifically verified the section number
cited in INIT-PROMPT.md and portability-review.md against the actual section structure
of implementation-handoff.md, and no check confirmed that the template reproduced in
tooling-recommendation.md matched the authoritative version.

**Fix Applied:**
All three references corrected in the readiness review session: INIT-PROMPT.md Step 12
and portability-review.md item 13 updated to "Section 5"; tooling-recommendation.md
Section 7 updated to include Step 5.

**Implication Going Forward:**
When the session-start template in implementation-handoff.md is modified — any step
added, removed, or reworded — immediately check and update: (1) tooling-recommendation.md
Section 7, which reproduces the template; (2) any document that cites the template by
section reference (currently INIT-PROMPT.md Step 12 and portability-review.md item 13).
Add these as explicit items to the end-of-chat cross-reference checklist whenever
implementation-handoff.md is touched.

**References:** —


---

## LL-010 | Closed Information Need Not Propagated to Reference Documents

- **Date:** 2026-04-21
- **Context:** Pre-implementation readiness review — cross-referencing all artifacts
  before handing off to the implementation project.

**Problem:**
Three companion reference documents still described IN-007 (nomination queue scalability)
as an open gap requiring implementer action, despite IN-007 being closed and its
resolution (two-stage aging, DM-051) being fully implemented in CLAUDE.md:
(1) tooling-recommendation.md Section 6 Threshold 2 described the aging mechanism as
a future escalation requiring the implementer to "resolve IN-007 before the nominated
queue reaches 20 items."
(2) implementation-handoff.md Scaling Triggers repeated the same framing.
(3) portability-review.md Section 5 still listed DEF-05 (nomination queue age limit)
in the deferred capabilities table, implying it was not yet implemented.

**Root Cause:**
When IN-007 was closed and DM-051 was written, the updates were correctly applied to
CLAUDE.md and info_needs.md, but the cross-reference check at that session's end did
not explicitly audit companion reference documents (tooling-recommendation.md,
implementation-handoff.md, portability-review.md) for stale IN-007 language. The
end-of-chat cross-reference checklist does not include a step for updating
human-facing reference documents when an information need closes.

**Fix Applied:**
All three stale references updated in the readiness review session to reflect IN-007
as closed and the mechanism as implemented.

**Implication Going Forward:**
When an information need is closed via a DM entry, the end-of-chat cross-reference
check must explicitly include: scanning tooling-recommendation.md, implementation-handoff.md,
and portability-review.md for any text that refers to the closed IN as an open item
or deferred capability. These documents are human-facing references; stale "resolve
before launch" language in them creates unnecessary implementer confusion and is as
much a defect as a schema inconsistency.

**References:** —


---

## LL-011 | cp Circular Reference in Recovery Instructions Silently Dropped Directory

- **Date:** 2026-04-22
- **Context:** Providing verbal recovery instructions to fix a Quartz nested-directory
  installation problem during the first implementation session.

**Problem:**
The recovery instruction `cp -r quartz/. .` was intended to promote Quartz's contents
from a subdirectory to the repo root. It silently failed to copy the `quartz/quartz/`
source directory because `cp` hit a circular reference: the source path `quartz/` and
the destination path `.` both contained a directory named `quartz/`, and `cp` declined
to copy a directory into itself. No error was emitted; the directory was simply absent
from the result. The implementer received no overwrite prompt either, which was the
expected signal that the copy was proceeding.

**Root Cause:**
The `cp -r <src>/. <dst>` idiom does not protect against cases where the source
contains a subdirectory with the same name as the source directory itself. Quartz's
repository structure has exactly this layout (`quartz/` repo contains a `quartz/`
source subdirectory). The recovery instruction was written without accounting for this
structural collision.

**Fix Applied:**
Directed the implementer to clone from a temp location outside the repo
(`git clone https://github.com/jackyzha0/quartz.git /tmp/quartz-temp && cp -r /tmp/quartz-temp/quartz ./quartz && rm -rf /tmp/quartz-temp`) to retrieve only the missing subdirectory.

**Implication Going Forward:**
When writing recovery or setup instructions that copy directory contents into the same
repository, always check whether the source directory contains a subdirectory with the
same name as the source. If it does, use a temp location outside the repo as an
intermediate step — never rely on `cp -r <dir>/. .` for such a layout. The definitive
fix is in the Phase 0 Quartz setup instructions, which now use `git clone` directly
into the wiki root directory, eliminating the nested-copy problem entirely.

**References:** —


---

## LL-012 | FRIC Template Fix Did Not Include Retroactive Patch Instruction

- **Date:** 2026-04-22
- **Context:** First post-setup wiki session — diagnosing why the public site still
  showed RSS XML after a successful GitHub Actions build.

**Problem:**
FRIC-002 was resolved by fixing the `npx quartz build` command in INIT-PROMPT.md
Step 10 to include `-d .`. However, the implementer's `deploy.yml` had already been
generated from the pre-fix template during Phase 1. The FRIC-002 resolution note
contained no instruction to manually apply the patch to the existing `deploy.yml`.
The broken file remained deployed until this session, when the build log revealed
`Found 0 input files from content` — the diagnostic signature of the missing `-d .`
flag.

**Root Cause:**
The FRIC resolution process fixes the template for future setups but does not
explicitly address already-generated artifacts from that template. `deploy.yml` is a
one-time file: it is written during Phase 1 initialization and never regenerated.
A template fix has no effect on it without a separate retroactive patch step.

**Fix Applied:**
The implementer manually updated `deploy.yml` to `npx quartz build -d .` and pushed.
The site rendered correctly on the next build.

**Implication Going Forward:**
When closing a FRIC that fixes a template which generates a one-time file (deploy.yml,
quartz.config.ts, .gitignore, pre-commit hook), always include in the resolution note
an explicit "if you have already generated this file, apply the following patch
manually" instruction with the exact change. Do not assume the implementer will infer
that the template fix requires a manual retroactive update.

**References:** FRIC-002, FRIC-011

---

## LL-013 | Incorrect Build Failure Diagnosis Followed by Incorrect ignorePatterns Recommendation

- **Date:** 2026-04-22
- **Context:** Post-setup friction session — diagnosing Quartz build failures and
  public site configuration gaps.

**Problem:**
Two sequential errors in the same session:

(1) When the CI build failed with `EEXIST: file already exists, mkdir 'public/public/tags'`,
the diagnosis was that `public/` had been committed to git, and a `git rm -r --cached public/`
fix was issued. The command returned "pathspec 'public/' did not match any files" —
the premise was wrong. The actual root cause was that Quartz's Assets emitter scans
the source directory at emit time (not from the pre-parsed file list) and found the
`public/` output directory being populated by a concurrent emitter.

(2) When fixing FRIC-015 (scaffold files showing in public nav), the recommendation
to exclude `overview.md` and `log.md` also incorrectly included `"index.md"`. This
produced a site with no `index.html` home page — browsers received `index.xml`
(the RSS feed) instead. The error was caught on the next build.

**Root Cause:**
(1) The EEXIST error message (`mkdir 'public/public/tags'`) was read as evidence of a
doubled path caused by a committed directory, without checking whether `public/` was
actually tracked by git first.

(2) `index.md` was grouped with `overview.md` and `log.md` as "scaffold state files."
The distinction was missed: `overview.md` and `log.md` are pure state files with no
Quartz role, while `index.md` is simultaneously an operational catalog AND Quartz's
required home page input. The Quartz build warning about missing `index.md` was not
anticipated before making the recommendation.

**Fix Applied:**
(1) Retracted the `git rm` instruction. Identified the actual cause (Assets emitter
self-reference) and added `"public/**"` to ignorePatterns (FRIC-014).

(2) Retracted `"index.md"` from the ignorePatterns recommendation immediately on
observing the RSS-only outcome. Added an explicit warning to all three documents
(INIT-PROMPT.md, portability-review.md, CLAUDE.md) that `index.md` must not be
excluded (DM-055, FRIC-015).

**Implication Going Forward:**
Before issuing a `git rm --cached` instruction, verify the file is actually tracked:
run `git ls-files <path>` first. An empty result means the file is not tracked and
the premise is wrong.

Before recommending adding any file to Quartz ignorePatterns, ask: does Quartz
require this file to generate a specific output? `index.md` → `index.html` is the
canonical case. When excluding scaffold files, check each one individually — do not
batch-exclude by category.

**References:** FRIC-013, FRIC-014, FRIC-015, DM-055

---

## LL-014 | Plan Statement Treated as Self-Authorization to Execute

- **Date:** 2026-04-22
- **Context:** —
- **Problem:** Agent stated a detailed plan for the index.md landing page
  design, then immediately executed all file edits and deliveries in the same turn
  without waiting for the user to engage with or confirm the plan.
- **Root Cause:** The collaboration contract rule "plan first, act second" was misread
  as a sequencing constraint (do planning steps before execution steps, within a single
  turn) rather than a gating constraint (stop after the plan; execution requires explicit
  human go-ahead).
- **Fix Applied:** None to the deliverables — the work product is not wrong. Process
  error only.
- **Implication Going Forward:** After stating a plan, stop. The next turn belongs to
  the user. Do not interpret "plan first, act second" as permission to collapse both
  steps into one response. Execute only after receiving explicit approval or a "proceed"
  signal. If the plan draws corrections, incorporate them before executing.
**References:** —


---

## LL-015 | Fix Plan Assumed Skill File Content Without Reading

- **Date:** 2026-04-22
- **Context:** —
- **Problem:** The FRIC-018 fix plan stated that EXTRACTION-SKILL.md and
  TAGGING-SKILL.md "contain examples of skill enrichment proposal output" that would
  need updating to use the PS-N label. This was wrong. Both files contain enrichment
  content (§6.1, §5.1) — not examples of the proposal format. The proposal format
  lives in CLAUDE.md Step 21a. The user correctly instructed a re-read before writing.
  The error was caught before any incorrect edit was made.
- **Root Cause:** The fix plan was drafted from memory of the skill file structure
  without reading the files first. The reasoning was plausible (skill files were known
  to contain forced-choice format examples from the design phase) but stale — the files
  had evolved, and the proposal format had never been placed in the skill files.
- **Fix Applied:** Re-read both files before execution. Corrected scope: no skill file
  changes required for FRIC-018. Only CLAUDE.md Steps 21a and 22 changed.
- **Implication Going Forward:** When a fix plan references specific content in a
  project file, read that file before finalizing the plan — not after confirming it.
  Plausible reasoning about file content is not a substitute for reading. This applies
  especially to skill files, which are updated by ingest operations between sessions.
**References:** —


## LL-016 | Fix Plan Used Tool Page Status Vocabulary on Source Page

- **Date:** 2026-04-22
- **Context:** —
- **Problem:** The FRIC-019 fix plan (in the carry-forward prompt) specified
  "`status: superseded` or `status: retracted`: hard stop still applies." Source pages
  have no `status: superseded`. The controlled values for source page status are
  `active | retracted | ingested-in-error`. The `superseded` value belongs to Tool and
  Topic pages. The error was caught before writing and corrected to `retracted or
  ingested-in-error` during execution.
- **Root Cause:** The fix plan was drafted with source and tool page status vocabularies
  conflated. Both page types have a `status` field, but their controlled vocabularies
  differ. The distinction is easy to miss when reasoning about the schema at a distance
  without consulting the frontmatter specs.
- **Fix Applied:** Corrected the condition in Step 2 and the DM-059 entry to use the
  correct source page status vocabulary (`retracted | ingested-in-error`).
- **Implication Going Forward:** Before writing any fix plan that references a `status`
  field, confirm which page type is involved and check the controlled vocabulary for
  that page type in CLAUDE.md Section 5. Do not assume that vocabulary is consistent
  across page types.
**References:** —


---

## LL-017 | Normal Ingest Path Had No Explicit Staged File Cleanup Step

- **Date:** 2026-04-23
- **Context:** —
- **Problem:** While planning the FRIC-022 fix (consumed sources not preserved),
  the carry-forward prompt assumed staged file removal was already specified in the normal
  ingest path and that the fix would only need to change "remove" to "move." In fact, the
  normal path (Steps 10–22a) contained no staged file disposal instruction at all. Only the
  enrichment path (Step 2a) had a disposal instruction. The carry-forward description of the
  fix scope was therefore incomplete.
- **Root Cause:** The ingest workflow was designed with the implicit assumption that staged
  files would be cleaned up by the human or by the operating environment, not by the schema.
  No one noticed the omission because the only explicit disposal instruction (Step 2a) was
  added for a different reason (enrichment path) and was never generalized.
- **Fix Applied:** Added Step 22b to the execution pass as an explicit post-ingest
  housekeeping step covering both staged files (move to raw/processed/) and queue entries
  (move to ## [processed] with processed date appended).
- **Implication Going Forward:** When writing fix plans that reference "the existing cleanup
  step," verify that the step actually exists in the current schema before citing it. Do not
  infer the presence of a step from context or operational common sense. Read the schema
  text first.
**References:** —


---

## LL-018 | Pitfalls Pages Never Created Because No Ingest Step Routed to Them

- **Date:** 2026-04-25
- **Context:** Operational friction session — human reported that sources selected
  specifically to build out the Pitfalls section were not producing Pitfalls pages.

**Problem:**
Despite intentionally ingesting articles and papers containing failure modes and
antipatterns, the agent never proposed creating Pitfalls pages. The human had to
manually override topic/comparison suggestions and force the agent to route content
to Pitfalls pages. This was not intended behavior.

**Root Cause:**
A structural gap in the ingest workflow. `EXTRACTION-SKILL.md` correctly routes
failure mode content away from Key Claims — labeling it as "candidates for Pitfalls
pages, not Key Claims." But no downstream ingest step acted on those candidates.
Steps 12 and 13 handle Topic and Tool pages. Step 15 handles Comparison pages
(conditional on pre-flight Step 7). No equivalent step existed for Pitfalls pages.
The failure mode content was correctly identified and then dropped.

**Fix Applied:**
Added Step 7a (pre-flight pitfalls proposal — fires when source contains at least one
substantive failure mode meeting the named-entry threshold) and Step 13a (execution —
creates or updates Pitfalls page if Step 7a confirmed). Threshold: nameable failure
mode with `**Status:**` designation. Passing mentions of limitations do not qualify.

**Implication Going Forward:**
When adding a new page type to the schema, explicitly verify that the ingest workflow
has both a pre-flight proposal step and an execution step for that type. The
existence of a page type in Section 3 and a frontmatter spec in Section 5 is not
sufficient — without workflow steps, the type is unreachable from ingest.

**References:** —


---

## LL-019 | Repeated Identical Structures Should Be Presented as Tables, Not Prose Blocks

- **Date:** 2026-04-25
- **Context:** Design session — presenting 10 gap disposition recommendations as an elicitation aid.

**Problem:**
Ten gap disposition items were formatted as individual prose blocks, each repeating the
same attribute structure (recommendation, risk rationale, response format). The result
was a document that required scanning 10 repetitions of the same pattern to compare items
across, rather than a format that supported side-by-side comparison.

**Root Cause:**
The structured block format was chosen to match the expected prose complexity of a
multi-item recommendation — without first checking whether the items actually shared a
uniform attribute schema. When N items share the same attribute set, tabular presentation
is always clearer for comparison than N repeated blocks. The test was not applied.

**Fix Applied:**
None to the content — the user provided dispositions successfully. The feedback was
received and logged.

**Implication Going Forward:**
Before formatting a multi-item elicitation or recommendation series as N prose blocks,
check: do all items share the same attribute schema? If yes, use a table. The specific
test: would reading this as a table make cross-item comparison easier than reading it
as blocks? If yes, use a table. This applies to gap audits, decision comparisons,
option evaluations, and any structured recommendation series with three or more items.

**References:** —


---

## LL-020 | Plan Stated Then Executed Without User Confirmation

- **Date:** 2026-04-25
- **Context:** Test harness design session — proposing and executing the Tier 1
  verification artifact form decision.

**Problem:**
After stating the decision to use a shell script for Tier 1 checks and explaining the
rationale, the agent immediately wrote 390 lines of code without pausing for user
confirmation. The plan was presented and executed in the same response with no
checkpoint for the user to redirect, question, or confirm.

**Root Cause:**
The collaboration contract rule "plan first, act second — state the plan explicitly
before writing code or drafting artifacts" was misread as a sequencing constraint
(present the plan and then execute, within a single response) rather than a gating
constraint (stop after the plan; execution requires explicit user approval). This is
the same root cause as LL-014. The fix applied in LL-014 — noting "after stating a
plan, stop" — did not propagate to the project instructions as an explicit language
change, leaving the rule ambiguous enough to be misread again.

**Fix Applied:**
Project instructions amended: the "plan first, act second" clause now explicitly states
"After stating the plan, stop and wait for explicit user confirmation before executing.
Do not treat absence of pushback as confirmation. Do not proceed on your own judgment
that the plan is sound."

**Implication Going Forward:**
After presenting any plan — including a single-item decision — stop. The next turn
belongs to the user. If the user confirms, execute. If they redirect, incorporate and
re-present before executing. This applies equally to decisions about form (shell script
vs. alternatives) and to multi-step design plans.

**References:** LL-014

---

## LL-021 | Governance Document Entry Delivered Inline Instead of as Complete File

- **Date:** 2026-04-25
- **Context:** End-of-chat ritual — producing the DM-071 entry for decisions_made.md.

**Problem:**
The DM-071 entry was delivered as an inline chat code block. The agent acknowledged
this was a Delivery Rule situation, correctly identified that it should stop and ask
about reproducing the full 2,790-line file, but then delivered the inline block "in
the meantime." The rule does not permit partial inline delivery while the full-file
question is pending.

**Root Cause:**
The agent recognized the Delivery Rule's "stop and ask" trigger applied, then
rationalized delivering the inline block as a helpful interim step. Rationalization of
partial delivery is exactly the failure mode the Delivery Rule prohibits — the amended
rule explicitly names "invented exceptions" as the error pattern. Recognizing the rule
applies does not permit the behavior the rule forbids.

**Fix Applied:**
Full file delivered in the closing response of the same session after the file was
read in sections. LL-021 logged.

**Implication Going Forward:**
If the Delivery Rule's "stop and ask" trigger fires, stop and ask — deliver nothing
else until the question is answered. Do not deliver partial inline content "in the
meantime." The user's ability to read an inline block does not satisfy the Delivery
Rule.

**References:** —


---

## LL-022 | Declared Information Unavailable Without Checking Accessible Sources

- **Date:** 2026-04-25
- **Context:** Test harness design session — identifying the two out-of-conformance
  Pitfalls pages by name.

**Problem:**
The agent stated that the names of the two Pitfalls pages "are live-wiki facts only,
not design-project facts" and could not be known without checking the wiki. The wiki
URL is documented in the project instructions. A single web fetch would have returned
the page names. The agent declared the information unavailable, described an inspection
procedure for the user to find the pages themselves, and moved on.

**Root Cause:**
The agent pattern-matched "not in project knowledge files" as equivalent to
"unavailable," without checking the next logical source — the live wiki URL present in
the project instructions. The same error pattern applies when a file is declared missing
without checking project knowledge: the search scope was too narrow. Declaring
unavailability without checking all accessible sources is the failure.

**Fix Applied:**
Web fetch performed in the following exchange. Pages identified as
`ai-search-citation-accuracy-pitfalls.md` and `legal-ai-hallucination-pitfalls.md`.
Project instructions amended with a new collaboration contract clause requiring all
accessible sources to be checked before declaring information unavailable.

**Implication Going Forward:**
Before stating that information is unavailable or unknown, enumerate the accessible
sources and check them: project knowledge files, URLs documented in the project
instructions, web search for live resources, and any other applicable tool. "Not in
project files" is not equivalent to "unavailable." Exhaust accessible sources before
declaring the information cannot be found.

**References:** —


---

## LL-023 | Wiki-Verify.sh baseUrl Check: Whole-File String Match Causes False Positives

- **Date:** 2026-04-26
- **Context:** First verification run on the live wiki repository.

**Problem:**
The baseUrl check used `grep -qF 'quartz.jzhao.xyz' quartz.config.ts` — a whole-file
string match. This fired a FAIL even though the active `baseUrl` was correctly set to
`fractalk.github.io/ai-auto-wiki`. The Quartz default configuration template leaves the
placeholder string in a comment block elsewhere in the file even after the operator
changes the active setting.

**Root Cause:**
The check was written to detect the case where the operator forgot to change the default.
quartz.config.ts is TypeScript with inline comments; the placeholder may survive as a
comment, example value, or neighboring default even after the active `baseUrl:` line is
updated. The whole-file approach cannot distinguish an active setting from a comment.

**Fix Applied:**
Narrowed the grep to lines containing `baseUrl` before checking for the placeholder:
`grep 'baseUrl' quartz.config.ts | grep -qF 'quartz.jzhao.xyz'`. Script header comment
updated to document the distinction between ignorePatterns checks (still whole-file)
and the baseUrl check (line-scoped).

**Implication Going Forward:**
Any script check that validates an active setting in a structured config file should
grep for the specific key line, not the whole file. Whole-file matching is appropriate
only when checking for strings that must never appear anywhere (e.g., secret key
patterns, known malicious strings). For setting-value checks, narrow to the key line.

**References:** —


---

## LL-024 | Wiki-Verify.sh Naming Scan Included Gitignored Archive Directory

- **Date:** 2026-04-26
- **Context:** First verification run on the live wiki repository.

**Problem:**
The naming convention scan loop included `raw` alongside the five wiki content
directories. `find "$d" -name "*.md"` recurses into `raw/processed/` and `raw/staged/`,
producing five FAILs on archived source files whose filenames reflect original article
titles (spaces, mixed case). These files are gitignored, are never wiki pages, and were
never subject to naming conventions.

**Root Cause:**
`raw/` was added to the scan under the assumption that any `.md` file in the tree should
follow naming conventions. The distinction between wiki content pages (subject to the
convention) and archived ingest originals (not subject to it) was not encoded in the
script's scan scope.

**Fix Applied:**
Removed `raw` from the naming convention loop. The only files in `raw/` that require
conformance checking — `queue.md`, `collection-gaps.md`, `discovery-sources.md` — are
already checked by name in Group 4 (scaffold file conformance).

**Implication Going Forward:**
Naming convention checks should target only directories whose files are expected to
conform. When adding a directory to a conformance scan, confirm that all files in that
directory tree are subject to the convention being checked. Gitignored directories that
hold externally-sourced or archived content should be excluded unless there is a specific
affirmative reason to include them.

**References:** —


---

## LL-025 | LL-022 Root Cause Recurred Under Simulation-Mode Framing

- **Date:** 2026-04-26
- **Context:** Abstract dry-run exercise — assessing whether existing wiki pages
  covered concepts in the paper being classified.

**Problem:**
During a classification dry-run, the agent repeatedly hedged with "cannot assess from
abstract alone whether [page] exists in the wiki" — despite the live wiki being
accessible throughout the session. LL-022 and DM-072 document this exact failure mode
and amend the collaboration contract to require checking all accessible sources before
declaring information unavailable.

**Root Cause:**
The agent was reasoning in "simulation mode" — framing the exercise as what the ingest
pipeline would know given only an abstract. In that frame, "existing wiki coverage" was
treated as a runtime input to the simulated pipeline rather than information resolvable
in this session. The simulation framing caused the agent to unconsciously scope its own
information access to match the simulated agent's constraints, even though no such
constraint applied to the design session.

**Fix Applied:**
None mid-session (issue was moot for the dry-run). Logged here for pattern recognition.

**Implication Going Forward:**
Simulation mode is a specific trigger for the LL-022 substitution error. Any time the
agent begins reasoning about how a *different agent* would behave, that is precisely
when the accessible-source check must fire — because the simulation framing is where
scope-narrowing is most likely to occur silently. "What would the pipeline know?" and
"What can I verify in this session?" are different questions; they must not be conflated.

**References:** —


---

## LL-026 | BSD sed Requires Empty-String Backup Argument for In-Place Editing

- **Date:** 2026-04-27
- **Context:** Implementation support session — applying the FRIC-030 retroactive fix
  to insert `<br>` after `**Status:**` lines in all Pitfalls pages.

**Problem:**
The carry-forward prompt provided a sed command without an empty-string backup argument:
`find pitfalls/ -name "*.md" -exec sed -i 's/...' {} +`. On macOS (BSD sed), this
produced: `sed: 1: "pitfalls/...": extra characters at the end of p command`. The
command works as written on Linux (GNU sed), which allows `-i` without a suffix argument.

**Root Cause:**
BSD sed (macOS) and GNU sed (Linux) differ in the `-i` (in-place) flag syntax. GNU sed
accepts `-i` with no argument; BSD sed requires an explicit suffix argument immediately
after `-i` — even if the suffix is empty (`''`). The carry-forward prompt's sed command
was written in GNU sed style, which runs without error on Linux but fails on macOS with
a cryptic message about extra characters.

**Fix Applied:**
Added `''` immediately after `-i`: `find pitfalls/ -name "*.md" -exec sed -i ''
's/\(\*\*Status:\*\*[^\n]*\)$/\1<br>/' {} +`. Command succeeded; fix was committed,
pushed, and validated on the Quartz site.

**Implication Going Forward:**
Any time a sed command involving in-place editing (`-i`) is provided in this project,
use `-i ''` (with empty string) to ensure macOS/BSD sed compatibility. The wiki runs
on a Mac. GNU sed is not available by default. When providing bash commands that will
run on the implementer's machine rather than in a Linux container, default to BSD-compatible
syntax. If portability is uncertain, note both forms.

**References:** —


---

## LL-027 | Asked Unnecessary Clarifying Question Answered by Existing Convention

- **Date:** 2026-04-27
- **Context:** Designing the `derived_from` frontmatter field for query-derived pages
  (teaching-brief and Comparison pages with `provenance: query-generated`).

**Problem:**
Asked whether `derived_from` should use wikilinks or plain slug strings, framing it as
an open design choice. The existing schema already answers this: all internal slug
references throughout the wiki use wikilink syntax (`[[slug]]`) — in `open_contradictions`,
Key Claims citations, and cross-references. There was no reason to treat `derived_from`
differently.

**Root Cause:**
The question was raised without first checking whether the same pattern existed elsewhere
in the schema. Treating a consistency question as a design question introduced false
uncertainty and consumed a turn unnecessarily.

**Fix Applied:**
Operator correctly pointed out the inconsistency. Wikilinks confirmed as the convention;
no design decision required.

**Implication Going Forward:**
Before raising a design question about a field format or reference syntax, check whether
the same pattern already exists elsewhere in the schema. If it does, apply it and state
the rationale — do not surface it as an open question.

**References:** —


---

## LL-028 | Proposed Over-Triggering Sync Mechanism Before Testing Signal Frequency

- **Date:** 2026-04-27
- **Context:** Designing the `teaching_notes` sync mechanism — how to detect when
  teaching notes have drifted out of currency with the page they annotate.

**Problem:**
Initial proposal used `teaching_notes_reviewed` as a lint-triggered date comparison:
flag any page where the reviewed date is older than `last_assessed`. This fires on every
ingest pass that updates the page — including minor corroborating additions, small Key
Claim edits, and formatting changes — none of which compromise the teaching synthesis.
The operator correctly identified this as a design that would train them to dismiss the
signal, degrading it to noise.

**Root Cause:**
The mechanism was designed to catch drift without first asking how frequently the trigger
would fire under normal operating conditions. A sync flag that fires constantly is
functionally equivalent to no sync flag — operators learn to skip it. The better
mechanism (agent assesses substantiality at ingest time, flags only when synthesis is
genuinely at risk) was available from the start but required reasoning about trigger
frequency before proposing it.

**Fix Applied:**
Mechanism redesigned: substantiality check runs at ingest Steps 12/13 when the agent
has full before/after context; lint serves only as a long-stop backstop (90-day gap
between `teaching_notes_reviewed` and `last_assessed`). Forced choice fires only on
substantive change.

**Implication Going Forward:**
When designing any sync, staleness, or drift-detection mechanism, explicitly estimate
trigger frequency under normal operating conditions before proposing it. A mechanism
that fires on every minor change must be rejected or scoped down before it reaches the
proposal stage. The test: would an operator encountering this flag on three consecutive
ingest sessions start dismissing it? If yes, the trigger is wrong.

**References:** —


## LL-029 | TOOLING-RECOMMENDATION.MD SECTION 7 NOT UPDATED WHEN SECTION 5 CHANGED

- **Date:** 2026-04-29
- **Context:** End-of-chat cross-reference check for the DM-085 OPERATIONS.md split
  session, which rewrote implementation-handoff.md Section 5 to add OPERATIONS.md as
  Step 2 and renumber the deferred-ingest check to Step 6.

**Problem:**
tooling-recommendation.md Section 7 contained the old 5-step session-start template
(no OPERATIONS.md step, deferred-ingest as Step 5) after the DM-085 session batch was
delivered. The canonical template in implementation-handoff.md Section 5 had been
updated correctly; Section 7 had not. The two documents were inconsistent.

**Root Cause:**
The end-of-chat ritual cross-reference check explicitly names this pair: "When
implementation-handoff.md Section 5 (session-start template) was modified this session,
verify that tooling-recommendation.md Section 7... has been updated to match." The check
either was not run against this pair or the Section 7 discrepancy was not caught when it
was run.

**Fix Applied:**
tooling-recommendation.md Section 7 updated in this session to match the current
6-step canonical template (OPERATIONS.md as Step 2, deferred-ingest as Step 6, three
ingest operation modes in the operation line and customization notes).

**Implication Going Forward:**
The cross-reference check between implementation-handoff.md Section 5 and
tooling-recommendation.md Section 7 is a named check that fires on every session that
modifies the template. Treat it as a required gate, not a suggestion. Do not mark the
ritual complete until both documents have been visually compared on the template content.

**References:** —


## LL-030 | YAML WIKILINK QUOTING REQUIREMENT NOT STATED EXPLICITLY IN SCHEMA

- **Date:** 2026-04-29
- **Context:** Post-implementation review of live wiki pages revealed unquoted wikilinks
  in YAML block list frontmatter fields across multiple page types.

**Problem:**
Unquoted `[[wikilinks]]` in YAML block list frontmatter fields (e.g., `- [[slug]]`) were
present across Comparison, Source, and Pitfalls pages. The YAML parser treats unquoted
`[[...]]` as a nested flow sequence, not a string, producing triple-bracket rendering in
Obsidian Properties and broken link resolution in Quartz. The defect was systematic
across multiple ingest sessions — not an isolated agent error.

**Root Cause:**
CLAUDE.md Section 5 never stated an explicit quoting requirement for wikilinks in
frontmatter fields. Inline comment examples in some field specs used the flow-sequence
list form (e.g., `["[[slug-a]]", "[[slug-b]]"]`), which implied correct quoting in that
format. But block list form (`- [[slug]]`) was never addressed, and that is the form
agents naturally use when writing YAML block lists. The agent used syntactically valid
YAML that resolved to the wrong type.

**Fix Applied:**
Universal quoting rule added to CLAUDE.md Section 5 preamble: all wikilinks in all
frontmatter fields must be written as `"[[slug]]"` — both in block list items
(`- "[[slug]]"`) and single-value fields (`field: "[[slug]]"`). All affected example
values in Section 5 specs updated to quoted form. Retroactive fix on live pages planned
as a targeted Claude Code session (Python script parsing frontmatter blocks; grep + sed
verification pass).

**Implication Going Forward:**
Any frontmatter field that accepts wikilink values must show an explicit `"[[slug]]"`
example — not merely an inline comment in flow-sequence form. When adding a new
wikilink-valued field to any page type spec, confirm the example value is in quoted form
before delivery. Comment syntax and implied convention are insufficient instruction for
the agent on YAML type behavior.

**References:** FRIC-032, DM-087

## LL-031 | SCHEMA RULE PRESENT BUT NOT ENFORCED AT EXECUTION POINT — BR RECURRENCE

- **Date:** 2026-04-30
- **Context:** wiki-verify.sh Group 10 (added DM-088) flagged two Pitfalls pages with
  missing `<br>` after `**Status:**` lines — on entries written after FRIC-030 was
  documented and the rule was in CLAUDE.md Section 5.6.

**Problem:**
The `<br>` requirement for Pitfalls failure mode `**Status:**` lines was violated on
newly-written entries despite the rule being present in the schema spec. The retroactive
fix (FRIC-030) corrected existing pages but did not prevent recurrence on new entries.

**Root Cause:**
A formatting rule stated in a schema reference document (CLAUDE.md Section 5.6) is not
reliably recalled at the moment of execution during ingest. The agent reads CLAUDE.md at
session start but writes failure mode entries during Step 13a, several steps later. The
`<br>` requirement has no visible effect in the local markdown file — it only manifests
as a rendering defect on the Quartz-published site — so there is no in-situ signal to
catch the omission. The combination of recall gap and invisible-until-published defect
makes this class of rule unusually prone to recurrence.

**Fix Applied:**
A mandatory self-check bullet added to OPERATIONS.md Step 13a immediately after the
`**Status:**`/`**Source:**` format spec: "Every `**Status:**` line must end with `<br>`
— verify this on every entry written, including entries added to existing pages." Places
the rule at the exact execution point rather than relying on recall from schema load.

**Implication Going Forward:**
For any rendering-critical formatting rule that (a) only manifests as a defect on the
published site, not in the local file, and (b) applies at a specific execution step:
place an explicit self-check at that step in OPERATIONS.md. Spec-document presence alone
is insufficient for this class of rule. The pattern applies to any future Quartz-specific
formatting requirements (e.g., `\$` escaping, Evidence Notes `<br>` separators on
Comparison pages). wiki-verify.sh Group 10 is the automated backstop; the OPERATIONS.md
self-check is the point-of-write prevention.

**References:** FRIC-030, DM-088, DM-089

## LL-032 | NEAR-MISS AUTO-COMPACTION REVEALS MISSING RECOVERY PROTOCOL

- **Date:** 2026-04-30
- **Context:** Live ingest session; Claude Code auto-compacted late in the session
  (during teaching brief writing) with no work lost; the event triggered a design
  review session for compaction resilience.

**Problem:**
No detection or recovery procedure existed for mid-source ingest interruptions caused
by auto-compaction or other session failures. If compaction had fired between Step 10
(first disk write: Source page) and Step 22c (git commit), the wiki would have been
left in inconsistent state — a Source page with no downstream Topic updates, or Topic
and Tool pages updated but index.md not yet reflecting them — with no reliable mechanism
to detect or recover from this condition in the next session.

**Root Cause:**
The ingest workflow uses a single commit point per source (Step 22c), which is the
correct architectural choice for clean git history. This necessarily creates an exposure
window between first disk write and commit. No compensating detection mechanism was
added at session start to catch prior-session interruptions within this window. The gap
was not visible during design because the workflow was developed sequentially, with each
step's recovery properties considered in isolation rather than as an exposure window
spanning multiple steps.

**Fix Applied:**
Two additions to OPERATIONS.md Section 11.2 (see DM-093 for full rationale):
(1) A mandatory pre-session check (before Step 0) that runs `git status` and halts if
uncommitted wiki file changes are detected in content paths, presenting the human with
a rollback/recover forced choice.
(2) A recovery session prompt template (Interrupted Ingest Recovery Procedure, after
Step 22c) that walks the agent through diagnosing the filesystem state and either
completing forward or rolling back cleanly in a fresh session.

**Implication Going Forward:**
The `git status` check at session start is the class solution for interrupted-state
detection in any single-commit-per-unit-of-work workflow. If new wiki operation types
(beyond ingest) are introduced that write files before a commit point, the pre-session
check covers them automatically — no update to the detection mechanism is needed,
provided the new content paths are in the inspection scope. If new content directories
are added to the schema, add them to the git status check explicitly. The step-to-file
mapping in the recovery procedure should be reviewed whenever step numbering changes
materially.

**References:** DM-093; OPERATIONS.md Section 11.2

## LL-033 | VOCABULARY EXPANSION DOES NOT TRIGGER RETROACTIVE LINT RE-EVALUATION

- **Date:** 2026-05-04
- **Context:** First lint pass after `software-and-ai-development` was added to the
  Section 7.2 controlled vocabulary (DM-091). No existing tagged pages were prompted
  to adopt the new term; the lint pass had no mechanism to propose it.

**Problem:**
When a new professional context or competency domain is added to the controlled vocabulary,
existing tagged pages retain whatever `professional_contexts` and `competency_domains` values
they carried at original tagging time. No lint step reads the vocabulary against existing
tags to identify pages that would now qualify for the new term. The lint procedure's
teaching-relevance check (Step L10) is a ratio check only — it confirms the tagged/total
ratio is above 20%, not that individual tag sets are complete relative to the current
vocabulary. The result is that the `software-and-ai-development` context was available in
the vocabulary but applied to zero pages after addition, with no lint signal to indicate
the gap.

**Root Cause:**
The lint procedure was designed assuming the vocabulary is stable. No retroactive matching
step was specified because the schema did not anticipate vocabulary growth requiring
back-population. This is a design gap that becomes more visible as the vocabulary evolves.
Automating retroactive matching in lint is impractical: it would require reading every
tagged page against every vocabulary term on each pass, consuming significant context for
low signal yield, and the agent cannot reliably judge applicability without reading each
page carefully.

**Fix Applied:**
Added OPERATIONS.md Section 11.6: a human-triggered vocabulary expansion procedure that,
when invoked after a vocabulary addition, applies the clean-mapping test from
TAGGING-SKILL.md Step 3 to all eligible tagged pages and surfaces confirmed matches as a
consolidated forced choice. A human-direct alternative (manual Obsidian edit) is also
documented. Added a cross-reference in CLAUDE.md Section 7.2 pointing to the procedure.
See DM-095 for placement rationale.

**Implication Going Forward:**
Any addition to CLAUDE.md Sections 7.1 or 7.2 must be followed by a vocabulary expansion
pass per OPERATIONS.md Section 11.6 before the term can be considered operationally active
across the wiki. The term addition and the expansion pass are two distinct operations; the
first without the second leaves the vocabulary partially deployed. Log the expansion pass
separately from the vocabulary change DM entry.

**References:** DM-091, DM-095, OPERATIONS.md Section 11.6, CLAUDE.md Section 7.2

---

## LL-034 | Friction Log Status Fields Not Updated When Resolved Dates Were Set

**Date:** 2026-05-18

**Context:**
—

**Phase:** Implementation support

**Problem:**
FRIC-033 and FRIC-034 were identified as `Status: open` in `implementation-friction.md`
despite both having `Resolved: 2026-05-04` dates set. The prior session's end-of-chat
ritual wrote the resolved dates but never changed the status fields. The defect was
caught in the current session during routine friction log review.

**Root Cause:**
The friction log format has two fields that must both be updated to close an issue:
`status` (open/closed) and `resolved` (date). The prior session updated only the `resolved`
date — likely because the DM entry and resolved date were appended in a final batch and
the status field, located earlier in each entry, was not revisited. The ritual did not
include an explicit check that both fields were updated for each closed entry.

**Fix Applied:**
FRIC-033 and FRIC-034 status fields corrected to `closed` in this session.

**Implication Going Forward:**
When closing friction log entries during the end-of-chat ritual, explicitly verify that
both `status: closed` AND `resolved: YYYY-MM-DD` are set on each entry being closed.
Updating the resolved date without changing the status field leaves the entry in a
contradictory state that will be misread by any future session scanning for open issues.
The two fields are a compound close operation — neither alone is sufficient.

**References:** FRIC-033, FRIC-034, FRIC-035

---

## LL-035 | POSITIVE INSTRUCTIONS INSUFFICIENT TO PREVENT AGENT WORKAROUNDS; EXPLICIT PROHIBITIONS AND VERIFICATION REQUIRED

- **Date:** 2026-05-18
- **Context:** Diagnosing FRIC-036 (blank ingest form recurrence) and FRIC-037 (large
  document context exhaustion).

**Problem:**
Two distinct instances in the same session where a spec fix that told the agent what
to do was insufficient because it did not tell the agent what not to do and did not
verify the outcome.

FRIC-036: OPERATIONS.md specified "serialize with python3 json.dumps" but did not
prohibit bash string substitution. The agent tried bash first (faster path), bash
failed, the agent claimed a Python fallback but the form was still blank. The spec
had no verification step to catch the failure before presenting the form to the human.

FRIC-037: The initial in-session fix proposal (chunk the document and process chapters
sequentially within one session) would have reproduced the context exhaustion problem
at a different granularity. The operator identified the flaw: processing 8 chapters
sequentially still accumulates context, and the session may still exhaust. The fix
required rethinking: chunks must be durable staged files that survive session
boundaries, not ephemeral in-memory units.

**Root Cause:**
Two related patterns. (1) Agent optimization: when a spec says "use method X," an
agent may interpret this as "method X is recommended" rather than "method X is the
only permitted approach" — and try a faster alternative first. Without an explicit
prohibition, the spec's intent is ambiguous. (2) Granularity displacement: a fix that
addresses the symptom (document too large) by subdividing the work (chapters) can
reproduce the same resource constraint at the new granularity if the subdivision
doesn't also introduce resource boundaries (session breaks, durable checkpoints).

**Fix Applied:**
FRIC-036: Added explicit prohibition on bash substitution and a post-injection
verification step (grep for `%%CHOICES_JSON%%` in the output file).
FRIC-037: Redesigned from in-session chunking to durable staged-file decomposition
with manifest-based cross-session continuity (DM-097).

**Implication Going Forward:**
For any spec fix that prescribes a specific method: (a) explicitly prohibit the
known alternative approaches that would circumvent it, and (b) add a verification
step that catches failure before the human encounters it. "Do X" is necessary but
not sufficient; "Do X, do not do Y, verify X succeeded" is the complete pattern.

When designing a fix for a resource-constraint problem (context window, memory, disk,
time), verify that the fix does not reproduce the constraint at a different
granularity. Ask: "if I apply this fix and the problem recurs at the new scale, what
recovery mechanism exists?" If the answer is "none," the fix needs durable
checkpoints that survive the resource boundary.

**References:** FRIC-034, FRIC-036, FRIC-037, DM-097


---

## LL-036 | Dollar-Sign Double-Escaping Recurred Despite Correct Spec

**Date:** 2026-05-20


**Context:**
—

**Problem:**
Wiki pages contained `\\$` (two backslashes + dollar sign) in prose, causing LaTeX math
mode to trigger on the Quartz site — the same rendering failure as FRIC-029. CLAUDE.md
Section 6.2 already specified the correct `\$` form (one backslash), so the spec was not
wrong. The agent was double-escaping anyway.

**Root Cause:**
The spec said "do X" (write `\$`) but did not say "do not do Y" (do not write `\\$`).
Absent an explicit prohibition, the agent constructed the wrong form — likely by treating
the backslash as requiring an additional level of escaping when building Python strings or
file-write commands. The absence of a post-write verification step meant the failure was
not caught before commit.

**Fix Applied:**
Per LL-035 pattern: (1) added explicit prohibition of `\\$` to CLAUDE.md Section 6.2;
(2) added post-write dollar-sign check to OPERATIONS.md Step 12 (applies also to Step 13).

**Implication Going Forward:**
"Correct form specified" is not sufficient when a plausible wrong form exists. For any
escaping rule in CLAUDE.md, if there is a known wrong form that an agent might reasonably
produce (e.g., by over-escaping), explicitly prohibit it in the same rule block. The LL-035
pattern applies here: "Do X, do not do Y, verify X succeeded."

**References:** FRIC-029, FRIC-041, DM-102, CLAUDE.md Section 6.2, OPERATIONS.md Step 12

---

## LL-037 | Claude Code Compaction Before First Write Loses Wiki-Inspection Ground Truth

- **Date:** 2026-05-23
- **Context:** Claude Code session building wiki-lint.py (~940-line Python script) per
  the hybrid lint assessment (DM-106).

**Problem:**
The agent read all five required reference files, then ran 8 wiki-inspection commands
and read index.md structure to gather ground-truth data about actual frontmatter
patterns, page structures, counter formats, and index layout. Compaction fired before
the agent wrote a single line of script code. All ground-truth observations from the
live wiki were lost to compaction summarization. The spec document tells the agent
*what* to check; the wiki inspection tells it *how things actually look on disk* —
exact field names, list formats, table column layouts, wikilink quoting patterns. The
second category is precisely what compaction summarizes away.

**Root Cause:**
The build prompt was structured as a single monolithic Step 1 (~940 lines of code)
followed by testing. The agent's context budget was consumed by reading 5 large
reference files plus running extensive wiki inspection, leaving insufficient context
for the code-generation phase. With no intermediate commit points, compaction destroyed
all work and all gathered ground truth simultaneously.

**Fix Applied:**
Build prompt restructured into three phases with git commit gates between each:
Phase 1 (~500 lines: scaffold + per-page mechanical checks), Phase 2 (~440 lines:
cross-page computation + D-category data assembly), Phase 3 (document updates). Each
phase starts with a re-read of the committed script. If compaction fires mid-phase,
at most one phase of work is lost; prior phases are preserved on disk.

**Implication Going Forward:**
For any Claude Code build session producing >500 lines of code, structure the prompt
with commit gates that preserve partial progress on disk. The trigger is not code
complexity but code volume: large scripts consume enough context for code generation
that combined with reference-file reads and wiki inspection, they exhaust the context
window before the first write. The commit gate pattern: (1) split into phases of
roughly 400-500 lines each, (2) commit after each phase, (3) re-read the committed
file at the start of each subsequent phase. Each phase must produce a working (partial)
script that can be tested independently.

**References:** DM-106, hybrid-lint-assessment.md

---

## LL-038 | Build Prompts That Delegate OPERATIONS.md Updates Must Specify Target Sections Explicitly

**Date:** 2026-05-24

**Context:**
—

**Trigger:** Post-build verification revealed G1-G5 checks implemented in wiki-lint.py
but absent from OPERATIONS.md step documentation, Group A/B/C classification, L13
summary template, and lint log format.

**Problem:**
The claude-code-lint-build-prompt-v2.md Phase 3 instruction read: "Add the five new
checks (G1-G5) to the appropriate step positions." The Claude Code session updated
OPERATIONS.md's hybrid architecture description and rewrote the Section 11.4 preamble
but did not add individual step documentation entries, did not update the Group A/B/C
classification lists, and did not add G-check lines to the L13 informational summary
template or the lint log entry format. All four omissions were caught in the subsequent
design-project verification session and corrected manually.

**Root Cause:**
The instruction "add to the appropriate step positions" is ambiguous. It does not
specify which OPERATIONS.md sections require updating, how many distinct insertion
points exist, or what the expected output looks like. A build prompt that delegates
documentation work to a Claude Code session must enumerate the target sections
explicitly — the agent cannot reliably infer the full set of update sites from a
general instruction, especially in a long document with multiple related sections
(classification block, per-step documentation, summary template, log format).

**Fix Applied:**
Post-build verification session (this session) added all missing documentation:
Step G1–G5 entries at correct Phase 1 positions; G2 in Group A classification;
G3, G5 in Group B; G1, G4 in Group C; G-check lines in L13 summary template and
lint log format. See FRIC-043.

**Implication Going Forward:**
When a build prompt delegates OPERATIONS.md (or any multi-section document) updates,
enumerate every target section explicitly:
- "Update the Group A/B/C classification list at line ~NNN"
- "Add a Step GN documentation block after Step LN"
- "Add GN output lines to the L13 informational summary template"
- "Add GN lines to the lint log entry format"
A general "add in appropriate positions" instruction reliably produces partial
compliance on documents with four or more distinct update sites. The omission pattern
is consistent: preamble/architecture sections get updated; templated output formats
(summary template, log format) are skipped.

**References:** FRIC-043, DM-106, claude-code-lint-build-prompt-v2.md

## LL-039 | Advised Manual Fix After Already Executing It

**Date:** 2026-05-24

**Context:**
—

**Session:** Dark-mode dashboard theming session
**Rule Violated:** Collaboration contract — "If uncertain, stop and ask. Never assume a way forward." Inverse failure: declared a fix unexecutable after having already executed and verified it.

**Problem:**
During surgical str_replace editing of wiki-dashboard.html, a duplicate closing brace `}` was introduced in the `heatColor()` function. The fix was applied via str_replace and verified with `node --check` (output: "Syntax OK") — all within the same response. The response then concluded by telling the operator: "I can't execute the fix in this response" and instructing them to make the manual edit themselves.

**Root Cause:**
The response was drafted as if the fix had not yet been applied, ignoring the tool output immediately above. The verification result ("Syntax OK") was present in the same response but was not reflected in the closing prose. Writing the closing summary before re-reading the execution results.

**Fix Applied:**
Operator caught the error. Fix was already in place; file was re-presented without further changes. LL-039 logged per collaboration contract self-violation rule.

**Implication Going Forward:**
Before instructing the operator to take any manual action, verify that the action has not already been completed by checking tool output in the current response. Specifically: if a `str_replace` succeeded and a syntax check passed in the same response, the file is already correct — do not tell the operator otherwise. Read results before writing conclusions.

**References:** wiki-dashboard.html dark-mode theming (2026-05-24)

## LL-040 | EDITED STALE PROJECT KNOWLEDGE COPY OF TEST-HARNESS.MD

- **Date:** 2026-05-25
- **Context:** Implementing Items 1–5 of the L16 wikilink proliferation agenda (adding L16 to all governance docs).

**Problem:**
Applied the surgical L16 maintenance entry to the project knowledge copy of
`test-harness.md`, which was missing Section 2.5.2 (wiki-dashboard.py Maintenance).
The delivered file was therefore missing an entire section present in the operator's
current working copy. Operator caught the discrepancy and provided the correct version.
Fix applied in a follow-up exchange.

**Root Cause:**
Project knowledge files reflect the state at last sync, not the current working copy.
`test-harness.md` had been updated in a prior implementation support session (adding
Section 2.5.2 per DM-107) but the project knowledge had not been re-synced. The session
proceeded to edit the project knowledge copy without first confirming it was current.

**Fix Applied:**
Operator provided the correct current version inline. Single surgical edit (L16 entry)
applied to the operator-provided version and re-delivered.

**Implication Going Forward:**
Before editing any project file that is actively updated during implementation support
sessions (test-harness.md, OPERATIONS.md, CLAUDE.md, wiki-lint.py, wiki-verify.sh),
confirm the project knowledge copy is current — or ask the operator to provide the
current version if there is any doubt. The project knowledge sync lag is a known failure
mode for files touched by both design sessions and implementation support sessions. When
an operator provides a file inline, always treat that version as authoritative over the
project knowledge copy.

**References:** Items 1–5, L16 wikilink proliferation session (2026-05-25)

## LL-041 | SPOTTED BUG PASSED TO OPERATOR RATHER THAN FIXED IN PLACE

- **Date:** 2026-05-26
- **Context:** Revising `claude-code-L16-followon-prompt.md` to add compaction mitigations; advisor noticed an invalid Python import statement in the original prompt while actively writing the replacement file.

**Problem:**
Advisor spotted a bug (`python3 -c "import wiki-lint"` — hyphens are illegal in Python module names) while writing the corrected file. Instead of fixing it, the advisor flagged it as a to-do for the operator in closing prose.

**Root Cause:**
Treating "I noticed this in someone else's prior text" differently from "I wrote this myself." The distinction is irrelevant: if the error is visible, the file is open, and the fix is trivial, fix it.

**Fix Applied:**
Operator challenged the pass-through. Corrected to `python3 wiki-lint.py --help` in the delivered file.

**Implication Going Forward:**
When writing or rewriting any file, fix all visible errors in that file during the same operation. Do not narrate fixable defects back to the operator as action items. If a fix requires a judgment call (ambiguous intent, multiple valid approaches), flag it. A syntax error is not a judgment call.

**References:** `claude-code-L16-followon-prompt-v2.md` revision (2026-05-26)


## LL-042 | "NO CITATIONS" INSTRUCTION PROHIBITED WIKILINKS IN TEACHING-BRIEF RELATED PAGES

- **Date:** 2026-05-27
- **Context:** Reviewing filed teaching briefs after the first Claude Code teaching-brief generation session.

**Problem:**
Both filed teaching briefs had plain-text `## Related Pages` sections — no wikilinks — rendering them navigation dead-ends on the public Quartz site. The `derived_from` frontmatter was correct; only the body section was broken.

**Root Cause:**
OPERATIONS.md Step Q7 Case 3 item 3 said "Plain prose, no citations." The agent correctly followed the instruction. The instruction meant no *source* citations (`→ [[sources/...]]` format); it did not mean no wikilinks of any kind. A single negative constraint was used to cover two distinct concepts without distinguishing them.

**Fix Applied:**
Step Q7 Case 3 item 3 updated to explicitly distinguish: no source citations; `## Related Pages` must use full-path wikilinks. Both existing briefs patched manually.

**Implication Going Forward:**
Schema instructions using negative constraints ("no X") must specify the scope of the negation precisely when X has multiple plausible referents. "No citations" covers both inline source citations and navigation wikilinks — two different things. Write "no source citations" and "navigation wikilinks required in Related Pages" as separate, explicit directives. When a negative constraint could be read broadly, assume the agent will read it broadly.

**References:** DM-113, OPERATIONS.md Step Q7 Case 3

---

## LL-043 | FIELD DIRECTION ERROR: PROPOSED `successor_to` POINTED BACKWARD, NOT FORWARD

- **Date:** 2026-05-29
- **Context:** Designing `succeeded_by` / `successor_to` lineage fields for prior-generation model-class tool pages.

**Problem:**
Advisor proposed `successor_to` as the lineage field for prior-generation pages. The name implies the field identifies "what this page is a successor to" — i.e., it points *backward* to the older version. But the intent was a forward pointer from the older page to the newer one. The operator caught the inversion before it was committed.

**Root Cause:**
The field name was chosen to express the relationship from the newer page's perspective ("I am a successor to X") rather than from the older page's perspective ("I was succeeded by X"). When the field lives on the *older* page, the correct name is `succeeded_by`.

**Fix Applied:**
Field renamed to `succeeded_by` in CLAUDE.md Sections 5.3 and 9 and in DM-114 before delivery. `successor_to` documented as a rejected alternative in DM-114 rationale.

**Implication Going Forward:**
When naming a relational field, always resolve it from the perspective of the page that *carries* the field, not the page being *referenced*. A field on page A pointing to page B should be named to complete the sentence "A _____ B." If the sentence reads unnaturally from A's perspective, the field is on the wrong page or has the wrong name. Test the name before proposing it.

**References:** DM-114

---

## LL-044 | TIMESTAMPS INVENTED RATHER THAN DERIVED FROM ACTUAL CURRENT TIME

- **Date:** 2026-06-04
- **Context:** End-of-chat ritual file delivery across multiple files in a single session.

**Problem:**
All five files delivered this session carried invented timestamps (17:00, 17:30, 17:45, 17:50, 18:00 EST) rather than the actual current time. The operator had to catch and correct this explicitly, supplying the real time (13:39 EST) before correct files could be delivered.

**Root Cause:**
The session instructions specify timestamp format (`MM/DD/YYYY HH:MM EST`) but do not specify the source of the time value. With no authoritative source named, the advisor defaulted to plausible-looking but fabricated times. The date was correct (derived from the system prompt); the time was not.

**Fix Applied:**
All five files re-delivered with correct timestamp 06/04/2026 13:39 EST. Session instructions updated with one additional sentence: "Use the actual current time as reported by the system or confirmed by the operator. Do not invent or approximate a timestamp."

**Implication Going Forward:**
When instructions specify a timestamp format, always derive the time value from an authoritative source — system-reported time or operator-confirmed time. If neither is available, ask before delivering. A correctly formatted invented timestamp is worse than no timestamp: it creates a false audit trail. Format compliance and value accuracy are separate requirements; both must be met.

**References:** Session instructions (Last Updated line), all files delivered 2026-06-04

---

## LL-045 | FIXES TO GENERATED ARTIFACTS NOT BACKPORTED TO COMMITTED TEMPLATE

- **Date:** 2026-06-04
- **Context:** L16 wikilink proliferation table rendering in `lint-decisions.html`.

**Problem:**
The `parseContext` function (which renders pipe-delimited markdown tables as HTML `<table>` elements) was added to a prior generated `lint-decisions.html` but was never backported to `ingest-ui-template.html`, the committed template from which every new generated file is produced. On the next lint pass, a new `lint-decisions.html` was generated from the unmodified template, reverting the fix. The regression was only caught when the operator noticed the table rendering as ASCII text.

**Root Cause:**
The template-and-generation pattern creates two artifacts with the same name in different states: the committed template (persistent, the real source of truth) and the generated output (ephemeral, gitignored). When a fix is applied to the generated output for immediate usability and the session ends without backporting, the fix is silently lost at the next generation. There is no natural forcing function — the fixed generated file works, nothing fails visibly, and the template divergence is invisible until the next generation cycle.

**Fix Applied:**
`ingest-ui-template.html` updated with `parseContext`, `.context-table` CSS, and call-site replacements at all three render functions. FRIC-045 logged. The project knowledge copy of `lint-decisions.html` (which contains the correct state) served as the authoritative source for the backport.

**Implication Going Forward:**
Any time a fix is applied to a generated artifact (a file produced by injecting data into a committed template), the committed template must be updated in the same session before delivery. The rule is: fix the template first, then regenerate if needed — never fix the output and leave the template unchanged. If the template is not accessible in the current session, the FRIC entry must explicitly name the template as the fix target so it is not missed in the next session.

**References:** FRIC-045, ingest-ui-implementation-plan.md Section 10

---

## LL-046 | SCRIPT CHANGE SCOPING: DETECTION IS NOT SUFFICIENT — OUTPUT CHANNEL MUST ALSO BE VERIFIED

- **Date:** 2026-06-05
- **Context:** Key Claims overcap resolution fix (FRIC-047, DM-115).

**Problem:**
Initial scoping stated "wiki-lint.py does not change — it already detects and flags overcap." This was wrong. The script did detect overcap correctly but emitted it as `"informational"`, which means it never reached the agent judgment pass and never reached the forced-choice form. The fix required changing the output channel from `add_finding(..., "informational", ...)` to `add_agent_review(...)`. The error was caught during the cross-reference check before delivery, not after.

**Root Cause:**
When assessing whether a script change is required for a workflow fix, only the detection logic was verified ("does the script catch this condition?"), not the routing logic ("does the finding reach the correct downstream consumer?"). In the hybrid lint architecture, `informational` findings are reported but never acted on; only `agent_review` items reach the judgment pass and can be promoted to forced choices. Detection and routing are separate concerns that must both be verified.

**Fix Applied:**
wiki-lint.py updated to route overcap to `add_agent_review` with `claims_summary` and `claim_count` data when no skip condition is active. Deferred and overridden pages remain `informational` with descriptive messages. Cross-reference check caught the gap mid-execution before any files were delivered.

**Implication Going Forward:**
When assessing whether a script requires changes for a workflow fix, verify two things independently: (1) does the script detect the condition? (2) does the finding emit to the correct output channel for the intended downstream behavior? In wiki-lint.py specifically: `informational` → reported only; `agent_review` → judgment pass + form; `forced-choice` → form directly. A finding in the wrong channel is a silent gap — it produces output but no action.

**References:** FRIC-047, DM-115, wiki-lint.py `check_L11_schema_conformance`

---

## LL-047 | UTC TIME USED DIRECTLY AS EST — TIMEZONE CONVERSION NOT PERFORMED

- **Date:** 2026-06-05
- **Context:** End-of-chat file deliveries — CLAUDE.md, OPERATIONS.md, wiki-lint.py, ingest-ui-implementation-plan.md, implementation-friction.md, decisions_made.md, lessons_learned.md, carry-forward, session instructions.

**Problem:**
The system `date` command returned `Fri Jun 5 02:41:38 UTC 2026`. All files updated in that batch received timestamps of `06/05/2026 02:41–02:55 EST` — UTC time with the EST label applied without conversion. The correct Eastern time was approximately `06/04/2026 21:41–21:55 EDT` (UTC−4 in June), a nine-hour discrepancy on a different calendar date. The operator caught it by comparing the stated timestamp against the expected local time.

**Root Cause:**
Same failure mode as LL-044: the system-reported time was used as-is without converting to Eastern time. The numeric value was correct but the timezone label and resulting wall-clock time were wrong. Knowing the rule ("use system time, convert to EST") is not sufficient if the conversion step is skipped.

**Fix Applied:**
All nine affected files corrected to `06/05/2026 21:49 EDT` (system-verified Eastern time at correction time). LL-047 logged.

**Implication Going Forward:**
When recording a Last Updated timestamp, always perform the conversion explicitly: run `TZ='America/New_York' date` rather than `date`, which returns UTC. The EDT/EST label should match what `TZ='America/New_York' date` reports — EDT during summer, EST during winter. The session instructions say "EST" colloquially but the correct label varies by season; use whatever the system reports for America/New_York. Never use UTC time as a proxy for Eastern time.

**References:** LL-044, session instructions (Last Updated line rule)

---

## LL-048 | PRE-CHECK STATIC METRICS DO NOT DETECT SPAN-LEVEL ENCODING ARTIFACTS

- **Date:** 2026-06-05
- **Context:** pdf_to_markdown.py P4 quality pre-check implementation; conversion of Biodefense in the Intelligence Age (OpenAI, June 2026).

**Problem:**
The `assess_extraction_quality()` function recommended "script" for the Biodefense PDF (2,139 chars/page avg, 9 heading candidates). Diagnostic inspection revealed severe word concatenation throughout the document — words joined without inter-word spaces due to justified-text PDF encoding. Running the script would have produced garbled output. The pre-check passed the document because total character count is unaffected by absent whitespace: concatenated words count the same as properly spaced words.

**Root Cause:**
The pre-check design measured text quantity (chars/page) and structural signal (heading-size spans), both of which are insensitive to inter-word spacing. PDF text extraction via PyMuPDF faithfully reproduces what the PDF encodes at the span level — if the PDF encodes "Thequickbrownfox" as one span token, that is what fitz returns, and it counts as 18 characters of apparently good text yield. No downstream metric in the current pre-check catches this.

**Fix Applied:**
None yet — session ended before the pre-check could be improved. The false positive was caught manually via the `--diagnose` flag, which was already part of the workflow. No garbled output was produced because in-context processing was used for all three documents regardless of pre-check recommendation.

**Implication Going Forward:**
The pre-check should add a concatenation detection heuristic: sample the extracted text and measure the proportion of "long runs" — sequences of non-whitespace characters above a threshold length (e.g., ≥ 20 characters with no internal space). A high proportion of such runs (e.g., >15% of all tokens) is a reliable signal of justified-text encoding artifacts. Additionally, the pre-check should incorporate page-count awareness: documents ≤ 10 pages that are fully rendered in context should be recommended "in-context" regardless of other metrics, since in-context processing is both feasible and artifact-free for short documents. See DM-116 and carry-forward Item 2.

**References:** DM-116, pdf_to_markdown.py `assess_extraction_quality`, carry-forward Item 2


## LL-049 | ZW-SPACE ENCODING AND TRUE CONCATENATION ARE DISTINCT ARTIFACTS REQUIRING DIFFERENT DETECTION

- **Date:** 2026-06-09
- **Context:** Implementing the concatenation heuristic in `assess_extraction_quality()` and verifying it against the Biodefense PDF.

**Problem:**
The carry-forward specified a concatenation heuristic based on long-run token ratio. Initial implementation tokenized raw extracted text (no unicode cleaning). Verification revealed the Biodefense PDF's raw long-run ratio was ~8.5% — close to but under the 10% threshold, and inconsistent across sample sizes. Deeper inspection showed the artifact was not word concatenation (words fused with no separator) but zero-width space padding: words were separated by `\u200b` characters rather than regular spaces. Splitting on whitespace produced multi-sentence "tokens" because ZW-spaces are not whitespace characters. After cleaning `\u200b` → ` ` before tokenizing, the ratio dropped to ~0.1%.

**Root Cause:**
Two distinct PDF encoding pathologies were conflated:
- **True concatenation:** Words fused with no separator at all (e.g., `Thequickbrownfox`). `extract_pdf()` cannot fix this; the output is garbled.
- **ZW-space padding:** Words separated by `\u200b` rather than regular spaces. `extract_pdf()` already cleans this (`text.replace('\u200b', '')` → now `replace('\u200b', ' ')`); output is correct.

The pre-check, if it had used raw text, would have produced unreliable results: misclassifying some ZW-space PDFs as concatenation artifacts and potentially missing genuinely concatenated documents depending on threshold tuning.

**Fix Applied:**
The concatenation heuristic was updated to apply the same `\u200b`/`\ufeff` cleaning as `extract_pdf()` before tokenizing. This makes the pre-check's view of text consistency with what the script will actually write — the correct design invariant. The heuristic now correctly detects only genuinely unfixable concatenation artifacts, not ZW-space artifacts that `extract_pdf()` handles cleanly.

Additionally, `extract_pdf()` itself was updated to replace `\u200b` with a space (` `) rather than deleting it (`''`), ensuring word boundaries are preserved in the output even when ZW-space was the only separator.

**Implication Going Forward:**
When building text quality checks against PDF extraction output, always apply the same unicode cleaning that the extraction pipeline applies before comparing or measuring. A quality check that sees raw text will characterize encoding artifacts that the pipeline silently fixes, producing misleading recommendations. The invariant: **pre-check and extraction pipeline must share the same text normalization step.**

**References:** DM-117, pdf_to_markdown.py `assess_extraction_quality`, LL-048

---

## LL-050 | FLAT-FONT-SIZE PDF SCHEMA MAKES SCRIPT PATH UNSUITABLE — DIAGNOSE BEFORE COMMITTING

- **Date:** 2026-06-09
- **Amended By:** LL-051
- **Context:** Attempting to convert the Claude Fable 5 / Claude Mythos 5 System Card (319 pages) via the script path after the quality pre-check returned `[SCRIPT]`.

**Problem:**
`assess_extraction_quality()` returned `[SCRIPT] Good text yield: 1818 chars/page avg, 8 heading candidate(s) in 3 pages`. Running the `--diagnose` flag before execution revealed that all body text and all section headings use 11.0pt font, with only the cover-page title at 56.0pt and one 16.0pt bold heading on page 2. The script's heading thresholds (H1 ≥ 15.5, H2 ≥ 13.5, H3 ≥ 12.5) would produce zero headings for the entire 319-page document — the TOC structure is entirely invisible to font-size classification.

**Root Cause:**
The quality pre-check detected 8 "heading candidates" (spans ≥ 15.5pt) from the cover page (56.0pt title text). The cover-page cover detection note in `--diagnose` output explicitly warns that font sizes on the cover may be decorative — but the pre-check does not apply this caveat. The 8 heading candidates are all on page 1 (cover) and are not representative of the document body. Pages 2–6 show a completely flat 11.0pt schema with differentiation only by bold weight.

**Fix Applied:**
None to the script — the design is correct for its target document class. The fix was recognizing the pre-check's limitation at the `--diagnose` step (per the documented workflow: "run `--diagnose` to inspect font sizes before converting") and routing the document to in-context processing.

**Implication Going Forward:**
The `--diagnose` step before conversion is not optional for unfamiliar documents — it is the correct gate, not the pre-check. The pre-check can produce false positives on documents with cover-page decorative titles that inflate heading candidate counts. The correct workflow is:
1. Pre-check (`assess_extraction_quality`) for gross screening (scanned, very short, genuinely concatenated).
2. `--diagnose` to validate thresholds before running the full conversion.
3. If body text and headings share the same font size, route to in-context regardless of pre-check recommendation.

The session instructions' quality gate description should be updated to make the `--diagnose` step explicit as a required intermediate step for any document being processed via the script path for the first time.

**References:** pdf_to_markdown.py `--diagnose`, DM-117, session instructions quality gate

---

## LL-051 | DIAGNOSE SAMPLING HIT TOC ZONE — FALSE "FLAT SCHEMA" READING; DOCUMENT HAS PROPER BODY HIERARCHY

- **Date:** 2026-06-09
- **Context:** Post-diagnosis analysis of the Claude Fable 5 / Mythos 5 System Card after LL-050 concluded the schema was globally flat.

**Problem:**
LL-050 concluded the system card used a flat 11.0pt schema throughout and was unsuitable for the script path. This was incorrect. Further analysis (sampling body chapter pages directly, cross-referencing `doc.get_toc()` with raw fitz extraction on chapter-opening pages) revealed the document has a proper heading hierarchy in the body: L1 headings at 16.0pt bold, L2 at 14.0pt, L3 at 13.0pt — all above the script's current thresholds. Only L4 (11.0pt bold) and L5 (11.0pt non-bold) fall to body size.

**Root Cause:**
`--diagnose` with default `--sample-pages 6` sampled pages 1–6, which in this 319-page document are: cover (56.0pt decorative), executive summary (11.0pt dense body prose), and visible TOC pages (11.0pt flat, because the visible TOC renders all entries at body size regardless of the heading level they represent). Body chapter pages begin at page 11; none were sampled. The TOC zone's uniform 11.0pt gave a false reading of the body schema. LL-050's root cause diagnosis ("pages 2–6 show a completely flat 11.0pt schema") was accurate as a description of those pages but wrong as a characterization of the document.

**Fix Applied:**
None to the script yet — the correct fix is to make `--diagnose` body-aware (skip cover and TOC zone, sample from first body chapter page). This is carried forward as part of Item 2. The in-context conversion route chosen after LL-050 remains correct for now (L4/L5 still need the TOC-match feature). The decision to route to in-context was right for the wrong reason; no output was harmed.

**Implication Going Forward:**
`--diagnose` must not be run with the default page range on long documents without first identifying where the body begins. The cover and any visible TOC pages will always read flat regardless of the body schema. The correct procedure: identify the first body chapter page (from the embedded outline page numbers or by skimming the TOC) and sample pages from that point forward. Until `--diagnose` is fixed to auto-detect the body zone, supply `--sample-pages` with a count offset to skip front matter.

The broader principle: **a sample is only representative if it covers the zone being characterized.** Front matter, TOC pages, and appendices can have radically different typographic properties from the body. A 6-page sample on a 319-page document is less than 2% coverage and likely hits only front matter.

**References:** LL-050 (prior diagnosis, partially incorrect), DM-117, carry-forward Item 2 (`--diagnose` fix)

---

## LL-052 | TOC-ANCHORED HEADING EXTRACTION IMPLEMENTED — PRINTED TOC DUPLICATION IS EXPECTED BEHAVIOR

- **Date:** 2026-06-09
- **Context:** Implementing the TOC-anchored heading extraction feature (DM-118) in `pdf_to_markdown.py` and validating against system card PDFs.

**Problem:**
After implementing `build_toc_index()` and TOC-match classification in `extract_pdf()`, heading counts in the system card output were higher than the TOC entry count. For example, the Claude Fable 5 / Mythos 5 System Card has 9 unique L5 TOC titles, but the output contained 17 `######` headings. Similarly, L4 heading counts exceeded the 59 TOC L4 entries.

**Root Cause:**
Not a defect. TOC titles appear twice in Anthropic system cards: once in the printed visible TOC (pages 4–10 for the Fable 5 / Mythos 5 card), where they render as body-size text that matches the normalized TOC index, and once in the document body where they are the actual section headings. Both occurrences match the TOC index correctly. The duplication is inherent to documents that render their TOC inline on numbered pages rather than as a separate non-body section.

**Fix Applied:**
None — this is correct behavior. The printed TOC lines being classified as headings is acceptable: the rendered markdown will contain heading entries that correspond to the printed TOC, which does not harm the structural integrity of the output. The heading hierarchy is still correct everywhere the headings actually appear in body text.

**Implication Going Forward:**
When validating TOC-mode output against expected heading counts, compare against (TOC entries × 2) for documents with printed inline TOC pages, not against the raw TOC entry count. If the printed TOC headings in output markdown are undesirable, a future enhancement could detect TOC-zone pages by page range (from `doc.get_toc()` page numbers) and skip TOC-match classification on those pages. This is not currently implemented and is low priority — the output is structurally correct.

**References:** DM-118, LL-050, LL-051, pdf_to_markdown.py `build_toc_index`

---

## LL-053 | RUNNING HEADERS ARE A DISTINCT PDF ARTIFACT CLASS FROM PAGE FOOTERS — NEEDS FREQUENCY-BASED DETECTION, NOT FIXED PATTERNS

- **Date:** 2026-06-27
- **Context:** Converting the Anthropic Economic Index ("Cadences") report and validating the script's output before staging for ingest.

**Problem:**
The repeated page header ("Anthropic Economic Index report: Cadences") was extracted as ordinary body text on every page and fused into surrounding paragraphs — e.g. "...lower baseline rates of personal use. 3 Anthropic Economic Index report: Cadences Request clusters..." — because its font size (8.0pt) fell below all heading thresholds and it didn't match `SKIP_PATTERNS` (which only covers bare page numbers and "pg. N" footers).

**Root Cause:**
`SKIP_PATTERNS` encodes fixed regex shapes for known footer conventions seen in prior documents (the MIT NANDA report's "pg. N"). It has no mechanism for detecting a document-specific running header/footer whose text is unknown in advance — that requires comparing text across pages, not matching a single page in isolation.

**Fix Applied:**
Added `detect_running_headers()` to `pdf_to_markdown.py`: a pre-pass that flags any line of text, at or below a low font-size threshold (`RUNNING_HEADER_MAX_FONT_SIZE`, default 10.0pt), that recurs verbatim on at least `RUNNING_HEADER_MIN_FRACTION` (default 40%) of pages, and skips it during extraction. Reported in `--diagnose` output (mirroring TOC reporting) and during conversion. Disable with `--no-header-strip` if the heuristic misfires.

**Implication Going Forward:**
Fixed-pattern skip rules (`SKIP_PATTERNS`) are appropriate for footer conventions with a known, generic shape (page numbers, "pg. N"). Document-specific running headers/footers — which repeat the document's own title or section name — cannot be caught by a fixed pattern and require frequency-based detection across the page set. When diagnosing a future garbled or polluted conversion, check whether the artifact is a single-page anomaly (fixed-pattern fixable) or a cross-page repetition (frequency-detection fixable) before deciding where to patch.

**References:** FRIC-048, pdf_to_markdown.py `detect_running_headers`

---

## LL-054 | NARROW BULLET-GLYPH ALLOWLISTS FAIL SILENTLY AND COMPOUND WITH JOIN LOGIC

- **Date:** 2026-06-27
- **Context:** Same Economic Index conversion validation; "•" bullets discovered unconverted, with one cluster joined into a single run-on line.

**Problem:**
The script's bullet detection only recognized "●"/"○" (U+25CF/U+25CB). This document uses "•" (U+2022), in two different rendering patterns: (1) glyph and text combined in one span ("•\tDirective: ..."), and (2) the glyph alone on its own line, with the text following as a separate line/span. Pattern (1) left literal "•" prefixes in the output instead of markdown "- " syntax. The same gap had a second, less obvious effect: because unconverted bullets never received the "- " prefix, `should_join_text()`'s existing bullet-join guard (which checks `new_text.startswith('- ')`) never triggered, so five consecutive footnote bullet items were silently joined into one run-on paragraph — a content-structure defect, not just a formatting one. Pattern (2) failed differently: a bare glyph carries no font-size signal of its own and was joined onto its following text line by the generic join heuristic before any bullet check ever saw the combined text.

**Root Cause:**
The bullet-glyph allowlist was built against the documents validated during initial script development and was never revisited against the broader set of Unicode bullet characters in common use, or against the second rendering pattern (glyph-only line, text on a separate line) that some PDF generators produce.

**Fix Applied:**
Two changes to `pdf_to_markdown.py`: (1) added "•"/"•\t" to the existing bullet-detection conditional alongside "●" — this alone also fixes the run-on-joining problem, since `should_join_text()` already checks for the "- " prefix this assignment produces. (2) Added standalone-glyph-line handling: a line whose entire (stripped) text is just a bullet glyph sets a `pending_bullet` marker; the next body-classified line consumes it, applying the prefix and forcing a new markdown line rather than letting it join. While implementing this, also widened `should_join_text()`'s existing bullet-join guard from `new_text.startswith('- ')` to `new_text.lstrip().startswith('- ')`, since the original check did not recognize indented sub-bullets ("  - ") — a latent gap discovered during this fix, not previously triggered because no prior document exercised the "○" sub-bullet path through this exact check.

**Implication Going Forward:**
When a glyph-based detection rule feeds a downstream heuristic that checks for the rule's *output* marker (here: the "- " prefix) rather than the input condition, an incomplete input allowlist produces a second, less obvious failure mode beyond the obvious one — fixing the input case alone can silently fix the downstream symptom too, but only if the output marker is actually what the input case produces. When validating a glyph-detection fix, check both how the glyph renders inline and whether it can render as a standalone marker on its own line — these are different code paths requiring different handling, and a document can use both patterns for different list types in the same body.

**References:** FRIC-049, pdf_to_markdown.py bullet detection block, `should_join_text`

---

## LL-055 | LOCAL CLI EXECUTION FAILED ON TWO ENVIRONMENT-LAYER ISSUES THE SANDBOX NEVER EXPOSES

- **Date:** 2026-06-27
- **Context:** Operator attempted to run `pdf_to_markdown.py` from the wiki repo's local command line (macOS, zsh, pyenv Python 3.11.10) against the same PDF already validated in this session's sandbox, and hit two failures that never surfaced here.

**Problem:**
Two distinct failures, neither related to the script's conversion logic: (1) `import fitz` crashed seven stack frames deep, ultimately on `ModuleNotFoundError: No module named 'frontend'` / a Starlette `StaticFiles` directory error; (2) the documented multi-line CLI example, pasted into zsh, produced `command not found: --title` and `command not found: --org`.

**Root Cause:**
(1) There is a separate, unmaintained, unrelated PyPI package literally named `fitz` (last released 2017) that squats on the same import name PyMuPDF uses. If that package was ever `pip install`ed directly into the local environment — an easy mistake, since the import statement is `import fitz` — it shadows PyMuPDF, and the resulting traceback gives no indication that the actual problem is a package-name collision. This is a long-standing, currently-documented PyMuPDF issue (confirmed via PyMuPDF's own installation docs), not specific to this operator's setup. (2) The documented CLI example used backslash line-continuation; zsh treats each subsequent line as its own command if a trailing space survives after the backslash (a common artifact of pasting from a chat/markdown code block), so `--title` and `--org` were each interpreted as standalone (nonexistent) commands rather than continuation arguments.

Both failures are specific to *this script's actual execution environment* (a real local shell against a real pip installation) and could not have been caught by the design-project sandbox, which has neither a pre-existing `fitz` package conflict nor a real interactive shell with paste behavior to exercise. This is a structural limitation of validating CLI tooling from within this project: correctness here proves the conversion logic works, not that the script is portable to an arbitrary local environment.

**Fix Applied:**
(1) Changed the script's import from `import fitz` to `import pymupdf as fitz` — PyMuPDF's own documented workaround. This resolves correctly regardless of whether the colliding `fitz` package is also installed, as long as `pymupdf` itself is; if `pymupdf` is missing entirely, the import now fails with a clean `ModuleNotFoundError: No module named 'pymupdf'` instead of the confusing nested traceback. Verified byte-identical output against the same PDF before and after the change — zero behavioral regression. (2) Updated the module docstring's USAGE section to lead with the single-line CLI form (safe against paste artifacts), retained the multi-line form with an explicit warning about the trailing-whitespace pitfall, and called out Option B (edit top-of-file constants, run with no CLI args) as the more reliable choice for repeated repo use.

**Implication Going Forward:**
When a script is developed and validated entirely within this design-project sandbox but is meant to run in the operator's actual local environment, treat "it works here" as validating logic only, not portability. Before considering a script-delivery session complete, check for at least these two environment-layer risk classes even when not prompted: (1) known namespace/package-name collisions for any third-party import the script relies on — prefer the unambiguous full package name over a short alias-prone one where the library supports it; (2) shell-paste fragility in any documented multi-line CLI example — prefer single-line examples as the primary documented form, with multi-line shown only as a secondary, explicitly-flagged convenience.

**References:** FRIC-050, pdf_to_markdown.py import statement, USAGE docstring

---

## LL-056 | A RULE STATED ONLY IN A TEMPLATE FIELD COMMENT DRIFTED ON THE FOURTH REAL APPLICATION

- **Date:** 2026-06-30
- **Context:** Resolving IN-021 — whether `decisions_made.md`'s `Status` field flips to `AMENDED` alongside the `Amended By` line.

**Problem:**
`decisions_made.md`'s entry template already specified the rule unambiguously, as a field comment: `Amended By: DM-NNN ← populate only if Status is AMENDED`. But the prose "Mutability rules" section at the top of the file — the part an operator or agent actually reads when performing an amendment — said only "add `Amended By: DM-NNN` to the original entry... this is the only permitted in-place edit," with no mention of the Status field. Three amendments (DM-023, DM-039, DM-044) happened to get it right anyway. The fourth (DM-111, amended by DM-120) did not: `Status` was left `ACTIVE` with `Amended By` populated, contradicting the template.

**Root Cause:**
The rule existed in exactly one place readable at the moment of authoring the template, and zero places readable at the moment of performing the actual edit. An agent amending an entry months later reads the prose mutability rule, not the template's field-level comment, to know what to do — and the prose rule was incomplete. This is the same failure shape as LL-035 (prohibition-verification-prescription: stating a rule once, without reinforcement at the point of execution, is insufficient), just occurring in this project's own governance log rather than in the wiki schema LL-035 was written about. Getting it right three times before drifting is itself informative: a rule that's "usually" followed from memory or convention, without being restated where the action is taken, will eventually be missed — and there's no mechanical check (lint, verify script, or otherwise) over this design-project's own governance files to catch it when it happens, unlike the wiki-side schema which has wiki-lint.py and wiki-verify.sh as a backstop.

**Fix Applied:**
Rewrote the prose mutability rule to state the Status flip and the Amended By line as a single coupled edit ("these two field changes together are the only permitted in-place edit; never edit one without the other"), rather than relying on the template's field comment to carry the full rule alone. Corrected DM-111 to `Status: AMENDED`. Logged as DM-121.

**Implication Going Forward:**
When a governing rule lives in two places in the same document — a prose policy section and a template's inline field annotations — treat that as a latent inconsistency risk even when the two currently agree, because only the prose section is consulted during routine execution. The template should illustrate the rule; the prose section must state it completely. This applies to any of this project's append-only logs (`decisions_made.md`, `info_needs.md`, `lessons_learned.md` itself) that pair a prose mutability-rules section with an entry template — worth a one-time audit for the same pattern rather than waiting for the next drift to surface it.

**References:** IN-021, DM-111, DM-120, DM-121, LL-035

---

## LL-057 | A CARRY-FORWARD'S PROPOSED IMPLEMENTATION IS A STARTING HYPOTHESIS, NOT A LOCKED SPEC — CHECK GOVERNANCE HISTORY BEFORE BUILDING IT

- **Date:** 2026-06-30
- **Context:** Implementing P9 (TOC-echo stripping in `pdf_to_markdown.py`), proposed in the prior session's carry-forward as `detect_toc_echo_block()`, a consecutive-heading-run heuristic.

**Problem:**
The carry-forward's proposed implementation was reasonable on its face and came with its own calibration caveat already attached (false-positive risk on dense legitimate outline sections, flagged by the same session that wrote it). Building it as specified would have worked, but would have reproduced a shape-based heuristic when a more precise, root-cause mechanism was already on record.

**Root Cause:**
LL-052 (2026-06-09) — the entry that first diagnosed this exact symptom — already named the more precise fix as an explicit forward note: detect TOC-zone pages by page range from `doc.get_toc()`'s own page numbers, rather than inferring TOC-echo status from output shape. That note predates the carry-forward that proposed the run-length heuristic, but the carry-forward was drafted without cross-referencing it. A carry-forward prompt is written under the same time and context pressure as any other session output — it is not exempt from the possibility that a better answer already exists in the governance log.

**Fix Applied:**
Before implementing, read LL-052 and DM-118 (the entries that established TOC-anchored classification), found the unimplemented forward note, and built page-anchored zone detection instead — presented as an explicit deviation with alternatives and rationale before coding (not carried out silently). Validated against an operator-provided real document before delivery. Logged as DM-122.

**Implication Going Forward:**
When a carry-forward proposes a new mechanism to fix a known problem, treat the proposal as a hypothesis to verify against the full relevant governance history (`decisions_made.md` and `lessons_learned.md` entries on the same subsystem) before implementing it as specified — not as a locked spec to execute. Symmetrically, when drafting a carry-forward item that proposes a new implementation strategy, search the governance log for the problem's originating entry first; if it already contains a forward note naming a fix, cite it in the carry-forward rather than proposing an unrelated mechanism from scratch. Both sides of the carry-forward handoff — the session that writes it and the session that executes it — are responsible for this check.

**References:** LL-052, DM-118, DM-122, carry-forward Item 1

---

## LL-058 | DELIVERY RULE APPLIES TO PROJECT INSTRUCTIONS EVEN WHEN ONLY A FRAGMENT IS IN CONTEXT — "CANNOT WRITE IT" IS NOT "CANNOT DELIVER A COMPLETE FILE"

- **Date:** 2026-06-30
- **Context:** Correcting the stale "Known improvement backlog" block in the Session Instructions.

**Problem:**
Asked to make the backlog block accurate, given only that block (not the full Session Instructions document) in context, Claude delivered a corrected inline snippet in chat plus a note that the fix fell "outside files Claude can edit" — without invoking the Delivery Rule's own stop-and-ask clause for the fact that only a fragment, not the full document, was available.

**Root Cause:**
Two distinct facts were conflated. (1) Claude has no write mechanism to the live Project Instructions setting — true, and worth stating plainly. (2) Claude cannot deliver a complete, reproducible file for the operator to paste in its place — false, and wrongly treated as equivalent to (1). The Delivery Rule requires the second regardless of the first; "I can't execute this update myself" does not license "so I'll give you a partial answer instead." The correct response to only having a fragment in context was to say so and ask whether to proceed with just the fragment or wait for the full document — the Delivery Rule already states this exact case: "uncertainty about whether unchanged content can be reproduced accurately is not a basis for partial delivery. It is a trigger to stop and ask."

**Fix Applied:**
None applied retroactively at the time — the operator supplied the full Session Instructions document in a later message and directed the corrected backlog language be treated as already applied (it was copied into the live setting independently). Logged here to prevent recurrence, and folded into Item 1 of the carry-forward (full assessment of the Session Instructions) as one of the catalogued violations that audit should account for.

**Implication Going Forward:**
When an update is due to a document Claude cannot directly write to (a project instructions setting, a third-party system, or any file outside Claude's write access), apply the Delivery Rule's ordinary test: is the current full content available in context to reproduce? If yes, deliver the complete file regardless of the write-access constraint. If no, stop and ask for it. Do not let "I can't execute this myself" quietly downgrade the deliverable to a reminder or inline fragment — those are two separate questions with two separate answers.

**References:** Delivery Rule, this session's backlog-correction exchange, DM-111 (the other rule-drift instance surfaced this session)

---

## LL-059 | THE MOST-VIOLATED STATED RULE WAS THE MOST-REINFORCED ONE — SCOPE-BOUNDARY AMBIGUITY, NOT DOCUMENT LENGTH, WAS THE CAUSE

- **Date:** 2026-07-01
- **Context:** Auditing the Session Instructions (carry-forward Item 1), cataloguing every lessons_learned entry that violated a rule the document actually states.

**Problem:**
The working hypothesis carried into the audit was that the Session Instructions had grown long enough to dilute their own authority, causing rule violations. Acting on that hypothesis would have meant shortening the document as the fix for rule-adherence.

**Root Cause:**
The hypothesis did not survive contact with the evidence. Of 58 lessons-learned entries, ~23 record violations of a stated rule; the largest cluster (5) is the Delivery Rule — which is also the most-reinforced rule in the document (its own section, two anti-rationalization clauses, restated in the End-of-Chat Ritual and every carry-forward) and the last-positioned. A position- or length-driven dilution mechanism predicts the most-reinforced, last-read rule should be among the least-violated; the opposite was true. Inspecting each Delivery Rule violation showed a common shape: every one was a scope-boundary question (do the project instructions count? a carry-forward? a governance-log entry? a fragment-only-in-context? a file Claude cannot write to?), never a failure to recall the rule existed. The rule's edges, not its prominence or the document's length, were the failure surface.

**Fix Applied:**
Strengthened the Delivery Rule with an explicit scope enumeration and a default-to-full-file-when-unclear clause (DM-123), rather than shortening the document. Independent currency cuts (peak-hour material, the IN-001 gate, section compression) were made separately and justified as removing stale dead weight — not as a fix for rule-adherence.

**Implication Going Forward:**
When a rule is violated repeatedly, test the causal hypothesis before acting on it: cross-reference the violations against where the rule sits, how reinforced it is, and what specifically failed each time. A high-frequency rule whose violations cluster at its scope edges needs its boundary cases enumerated at the rule, not a shorter surrounding document. Do not attribute recurrence to document length without first ruling out the competing explanation — and note that a section being stale dead weight (worth cutting for currency) is a separate question from a section causing violations (which cutting would not fix).

**References:** DM-123, LL-001, LL-004, LL-005, LL-021, LL-058


---

## LL-060 | GOVERNANCE ENTRIES CAN BE REFERENCED-BUT-ABSENT — APPEND-ONLY LOGS ARE NOT SELF-VERIFYING

- **Date:** 2026-07-07
- **Context:** An adversarial project assessment scanned decisions_made.md entry IDs and found the log jumped from DM-099 to DM-102, while DM-100 was cited as a live decision authority in implementation-friction.md (FRIC-044 references the inter-chunk pause "added per DM-100/FRIC-039").

**Problem:**
DM-100 (mandatory inter-chunk pause) and DM-101 (pause placement and standing-authorization prohibition) — both dated 2026-05-20, both governing active protocol behavior in OPERATIONS.md — were absent from decisions_made.md for approximately seven weeks. Downstream documents cited them as authorities during that entire period. Any session consulting the log to understand the inter-chunk pause's rationale, or auditing whether a proposed protocol change relitigated a settled question, would have found nothing.

**Root Cause:**
A delivery containing the two entries from the 2026-05-20 session was lost or never placed into project knowledge — the entries existed (the operator recovered them in full, with correct formatting and cross-references) but the updated log file they belonged to did not reach its destination. The gap then persisted because nothing checks the log's integrity: the append-only convention governs how entries are written, but no mechanism verifies that the ID sequence is continuous or that referenced entries exist. Append-only was implicitly trusted as self-verifying; it is not. Cross-reference checks in the End-of-Chat Ritual verify that documents agree with decisions logged *in the current session* — they cannot catch an entry that was never placed.

**Fix Applied:**
Operator located the original DM-100 and DM-101 entries; both were inserted verbatim into decisions_made.md at the DM-099/DM-102 junction (2026-07-07), status ACTIVE, no amendment flips. A governance self-lint script (design-project-backlog.md BL-D-02) was specified to mechanically check ID sequence continuity, status-field vocabulary conformance, amendment coupling, and Last Updated format across all four governance logs — the ID-continuity check would have caught this gap the day it occurred.

**Implication Going Forward:**
A referenced-but-absent log entry is a distinct governance defect class: more dangerous than a missing reference (which fails loudly when followed) because the citing documents look healthy and the gap is silent until someone follows the pointer. Mechanical integrity checks on governance logs are cheap and catch this class immediately; conventions about how logs are written do not substitute for verification that they were. Secondary implication: delivery placement is a failure point separate from delivery production — a correctly produced file that never reaches project knowledge fails identically to one never produced, and only an integrity check on the destination catches the difference.

**References:** DM-100, DM-101, DM-126, FRIC-039, FRIC-040, FRIC-044, design-project-backlog.md BL-D-02

---

## LL-061 | STAGED/DERIVED GOVERNANCE DRIFTS FROM HOUSE FORMAT, AND LONG-LIVED CONTROL DOCUMENTS CARRY LATENT COPY DEFECTS — FULL REPRODUCTION AND GOV-LINT ARE THE ONLY DETECTORS

- **Date:** 2026-07-11
- **Context:** The BL-D-01 batch reformatted three decision entries staged in a separate draft file into decisions_made.md, and reproduced the full Session Instructions in order to apply the R-001 edits.

**Problem:**
Two latent defects surfaced only because the work forced a full pass over the text. (1) The draft DM entries were authored in a staging shorthand — PROPOSED/settled parentheticals, a "Proposed decision" header, structure that diverged from the log's house format — and had to be reconciled to house style at append time rather than pasted as-is. (2) The Session Instructions' Delivery Rule section carried a duplicated, truncated sentence fragment — a copy-paste artifact of unknown vintage — that no session had noticed, because no session had reproduced that section in full since it was introduced.

**Root Cause:**
Governance text produced outside its destination file (staged drafts, derived proposals) is written to be read by a human in the moment, not to match the destination's conventions; the reconciliation step is implicit and easy to skip. Separately, a control document edited in place with surgical `str_replace` is never re-read end to end, so a defect outside any edited region persists indefinitely. Neither failure is caught by the current End-of-Chat Ritual, which checks cross-document agreement for changes made *this* session, not the internal well-formedness of a document nobody fully reproduced.

**Fix Applied:**
The three drafts were reformatted to house style before append (all-caps `|` titles, `- **Date:**` / `- **Status:** ACTIVE` bullets, staging parentheticals stripped, DM-132 flipped PROPOSED to ACTIVE with its open tradeoff resolved). The duplicated Delivery-Rule fragment was removed during the R-001 reproduction. Both fixes shipped in the BL-D-01 batch (DM-133). Because the full instructions were reproduced from context rather than from a byte-exact disk source, the R-001 revision also establishes a standing practice: the operator diffs the delivered file against the stored copy before replacing it.

**Implication Going Forward:**
Two gov-lint targets to add to BL-D-02 beyond the ID-continuity check LL-060 already motivates: (a) house-format and status-vocabulary conformance for every log entry, which would flag a staged draft that landed unreconciled; and (b) intra-document well-formedness checks that do not depend on a change occurring this session (duplicated or truncated lines, orphaned fragments). Until that lint exists, the mitigations are manual: reconcile staged governance to house format at landing, and periodically reproduce long-lived control documents in full rather than only `str_replace`-editing them — surgical edits keep the edited regions correct but never surface defects elsewhere.

**References:** DM-131, DM-132, DM-133, LL-045, LL-060, design-project-backlog.md BL-D-02, decisions_made.md, wiki-design-session-instructions.md

---

## LL-062 | GOVERNANCE-LOG LINE-2 TIMESTAMPS CAN LAG THEIR OWN LATEST ENTRY — THE CARRY-FORWARD CHAIN CHECK CAUGHT IT, NOT THE DELIVERY

- **Date:** 2026-07-12
- **Context:** Session Start's carry-forward chain check (R-001, check 2) compared the
  loaded carry-forward's date (07/11/2026 12:58 EDT) against `decisions_made.md`'s
  Line-2 `Last Updated` (07/08/2026 12:23 EDT) and found a mismatch.

**Problem:**
`decisions_made.md` and `lessons_learned.md` both had their entries appended through
DM-133 / LL-061 (dated 2026-07-11 in-entry) in the BL-D-01 session, but neither file's
Line-2 `Last Updated` line was bumped to match — both still showed their pre-session
timestamps. `wiki-implementation-backlog.md` and `design-project-backlog.md`, edited in
the same session, got their headers bumped correctly. `implementation-friction.md` and
`info_needs.md` were unaffected (not touched that session).

**Root Cause:**
The Delivery Rule and the Project Files convention both require the Line-2 timestamp
update on any file edit, but for append-only logs the edit is conceptually "add an
entry," which is easy to execute as a pure append (`str_replace` inserting new content
before the file's end) without also touching Line 2 — unlike the rolling-edit backlog
files, where the header and the body are naturally revisited together. Nothing checks
this mechanically; it surfaced only because the Session Start carry-forward chain check
happens to diff a log's header against an external date.

**Fix Applied:**
Corrected both headers to 07/12/2026 15:43 EDT in this session (concurrent with new
entries DM-134/135 and this entry). Confirmed via content-level check (max entry ID
matching the carry-forward's stated maxima) that this was a header-only defect, not a
stale copy or a missing entry, before proceeding — the two check types answer different
questions and neither substitutes for the other.

**Implication Going Forward:**
A third gov-lint target for BL-D-02, alongside the two LL-061 already named
(house-format conformance; intra-document well-formedness independent of this
session's edits): Line-2 `Last Updated` recency versus the latest in-entry `Date:` /
`Raised:` field in each of the four governance logs. Until that lint exists, the
Session Start carry-forward chain check remains the only mitigation, and it only
catches `decisions_made.md` specifically — it does not cross-check
`lessons_learned.md`, `implementation-friction.md`, or `info_needs.md` headers against
their own latest entries. Consider extending Session Start check 2 (or check 3) to
diff all four log headers against their own latest in-entry dates, not just
`decisions_made.md` against the carry-forward.

**References:** LL-060, LL-061, design-project-backlog.md BL-D-02, decisions_made.md
(DM-134, DM-135), wiki-implementation-backlog.md, design-project-backlog.md, Session
Instructions Session Start (check 2).

---

## LL-063 | A "MANDATORY" CARRY-FORWARD TABLE STILL DROPPED A ROW — NARRATIVE RECALL IS NOT A SUBSTITUTE FOR A MECHANICAL DIFF AGAINST THE SOURCE COLUMN

- **Date:** 2026-07-12
- **Context:** Session Start's standing stale-state check (R-001/R-002, check 4) read
  `wiki-implementation-backlog.md`'s summary table directly and found BL-W-03 listed
  `planned`, but `carry-forward-2026-07-12.md`'s "Pending executions" table — explicitly
  documented as mandatory and exhaustive for every `planned` item — enumerated only
  BL-W-04.

**Problem:**
The Pending Executions table is written to be exhaustive by construction ("its absence
when `planned` items exist is a defect in the carry-forward"), yet a `planned` row was
silently dropped from it in the same session that produced it.

**Root Cause:**
BL-W-03 is a split item — Stage 1 rides as an uncommitted rider on the not-yet-run
BL-W-04 session; Stage 2 is trigger-gated. That nuance almost certainly caused it to be
mentally filed as "not a standalone pending execution" while drafting the table, even
though the backlog's own Status column — the literal source of truth the table is
supposed to enumerate — says `planned`, unqualified. The table was assembled from
narrative recall of the session's work (which is centered on BL-W-04), not from a
mechanical scan of both backlog files' Status columns for the literal value `planned`.
This is the same failure shape as LL-060/LL-061: a derived artifact drifts from its
source because a human-legible summarization step stood in for a mechanical check.

**Fix Applied:**
Caught this session via Session Start check 4 before any work proceeded on the stale
framing. Correction deferred to the next carry-forward this session produces, which
must list BL-W-03 with a note on its rider/split status rather than omit it.

**Implication Going Forward:**
Add a fourth target to `design-project-backlog.md` BL-D-02 (gov-lint): before any
carry-forward is delivered, mechanically grep both backlog files' summary tables for
every row where Status = `planned` and diff that set against the drafted Pending
Executions table — do not rely on recalling which items the session's narrative
centered on. Until gov-lint exists, this diff is a manual step to run explicitly at
Ritual step 7, separate from drafting the table's prose. This does not need an
institutional-memory artifact on its own — it is a project-internal process defect,
not a generalizable design principle — though the underlying shape (a mandatory
summarization step silently drifting from its own source column) is the same pattern
LL-060/LL-061 already flagged, and may be worth folding into a future institutional-
memory entry on derived-artifact verification generally if that theme recurs again.

**References:** LL-060, LL-061, design-project-backlog.md BL-D-02,
wiki-implementation-backlog.md (BL-W-03), carry-forward-2026-07-12.md, Session
Instructions Session Start (check 4).

---

## LL-064 | AN EXECUTION SPEC INSTRUCTED THE EXECUTOR TO READ A FILE IT CANNOT REACH — A CROSS-SPEC REFERENCE IS AN UNEXECUTABLE STEP, NOT A CITATION

- **Date:** 2026-07-12
- **Context:** Generating `claude-code-prompt-BL-W-04.md` from
  `ingest-injection-resistance-spec.md` per DM-132. The spec's Section 5 execution
  sequence, step 6, reads: "Apply BL-W-03 Stage 1 (key-claims-eviction-spec.md Section 6:
  lint log format line in both mirror locations + L11 card annotation instruction)."

**Problem:**
`key-claims-eviction-spec.md` is a design-project file. It does not exist in the wiki
repository and is not inlined in the prompt. Claude Code, executing the prompt, cannot
read it. The instruction is therefore unexecutable as written: the rider commit would
have been produced from the one-line paraphrase in the step text, or silently skipped,
or the executor would have STOPped and asked — the best of three bad outcomes. This is
precisely the paraphrase-failure risk DM-132 was created to eliminate, and the spec
tripped over it in the spec's own execution section.

**Root Cause:**
The spec was authored inside the design project, where both files are in context and a
cross-reference reads like an ordinary citation. DM-132's rule — "inline the governing
spec verbatim rather than referencing it, because the execution agent cannot read the
source" — was applied to the *governing* spec and not carried to a spec the governing
spec *itself* points at. The rule was understood as a fact about one document rather than
as a property of the executor's whole reachable context. Note the timing: DM-130 and
DM-129 were drafted in the same planning burst (both dated 2026-07-08, both Fable
planning-capture items), where the cross-reference was natural and the coupling real; the
defect only became visible at prompt-generation time, three sessions later.

**Fix Applied:**
1. `key-claims-eviction-spec.md` Section 6 is inlined verbatim in the BL-W-04 prompt as
   Appendix A, behind its own `=== BEGIN RIDER SPECIFICATION ===` marker, with an explicit
   scope fence ("commit 2 scope, and nothing beyond it") — because dropping one section of
   the *eviction* spec into an executor's context without a fence invites it to implement
   Stage 2, which is trigger-gated and must not run.
2. The governing spec was deliberately **not** amended. Amending it would bump its
   `Last Updated` and immediately stale the prompt built from it (DM-132's currency guard).
   The prompt closes the gap by construction; the spec's step text remains accurate as a
   description of *what* commit 2 does.
3. Backported to `claude-code-execution-prompt-template.md` in the same session (LL-045):
   a **closure check** in the generation checklist — scan the governing spec's execution
   sequence for instructions to read any other specification or design-project document,
   and inline each verbatim as a rider — plus rider markers in the template body and a
   requirement that every inlined spec's `Last Updated` appear in the prompt header and the
   backlog pointer.
4. Audited the other three execution specs (`key-claims-eviction-spec.md`,
   `structured-data-extraction-spec.md`, `vocabulary-json-refactor-spec.md`) for the same
   defect in their execution sections. **Clean** — no other spec instructs its executor to
   read a design-project file. The defect is isolated to BL-W-04.


**Implication Going Forward:**
The test for an execution prompt is not "is the governing spec inlined?" but "**is
everything the executor is told to read reachable from the prompt alone?**" Those differ
exactly when one spec cites another — which happens whenever two backlog items are planned
in the same session and one rides on the other's execution, a pattern this project now uses
deliberately (BL-W-03 Stage 1 riding on BL-W-04). The coupling that makes riders efficient
is the same coupling that makes them unexecutable if the rider text is left behind. This is
the same shape as LL-060/LL-061/LL-063 — a derived artifact drifting from its source
because a summarizing step stood in for a mechanical one — but with a sharper edge: here the
derived artifact is handed to an agent with repository write access, and the paraphrase it
would have executed from was a single parenthetical clause.

**References:** DM-129, DM-130, DM-132, DM-141, LL-045, LL-060, LL-061, LL-063,
ingest-injection-resistance-spec.md (Section 5, step 6), key-claims-eviction-spec.md
(Section 6), claude-code-execution-prompt-template.md, claude-code-prompt-BL-W-04.md.

---

## LL-065 | "SYNCED" CONFLATED CONNECTOR SYNC WITH GIT PUSH — SESSION START CHECK 4 MUST DISAMBIGUATE, NOT ACCEPT EITHER STATUS CLAIM AT FACE VALUE

- **Date:** 2026-07-14
- **Context:** Processing the Step 9 report for the BL-W-04/BL-W-03-Stage-1 execution
  session at Session Start.

**Problem:**
The operator opened with "I have synced the repo" before pasting the Step 9 report. The
report's own text stated both commits were local-only and had not been pushed to
`origin/main`. Taken at face value, "synced" would have satisfied Session Start check 4
(connector currency) when in fact it could not have: the GitHub connector's `Sync now`
reads only from `origin/main`; run against an unpushed local repository, it pulls no new
content regardless of how many times it is run.

**Root Cause:**
"Synced" collapses two distinct actions in ordinary speech: (1) running the connector's
`Sync now`, and (2) the prerequisite of having pushed local commits to `origin/main`
first, without which (1) is a no-op. Nothing in the operator-facing language, or in the
connector's own UI, signals that these are two separate steps rather than one.

**Fix Applied:**
Did not accept the initial "synced" claim as satisfying check 4 — the report's own
"local only, not pushed" statement was flagged back to the operator directly, and work
was held until push status was confirmed. After the operator confirmed the gap, pushed,
and re-ran `Sync now`, currency was confirmed by a **direct retrieval probe** — searching
project knowledge for content that could only exist post-commit (`EXTRACTION-SKILL.md`'s
new Section 8 header, `OPERATIONS.md`'s Step 11 injection-screen bullet, the
`CLAUDE.md`/`OPERATIONS.md` `Overcap cards:` log line) — rather than accepting the
operator's second "synced" confirmation at face value either.

**Implication Going Forward:**
Session Start check 4 must never treat "synced" (or equivalent operator shorthand) as
self-certifying, in either direction. Whenever a Claude Code session has executed since
the last design session: (1) ask explicitly whether local commits were pushed to
`origin/main` before `Sync now` was run — do not infer this from the word "synced" alone;
(2) regardless of the answer, confirm currency by a direct retrieval probe for content
that only exists after the specific commit(s) in question, following the pattern DM-138
already established for whole-file claims. A status claim about the connector is not
evidence about the connector.

**References:** DM-138, DM-140, DM-142, DM-143.

---

## LL-066 | SANDBOX CLOCK IS UNRELIABLE ACROSS TOOL CALLS — DERIVE THE DATE STAMP FROM THE AUTHORITATIVE SESSION DATE, NOT A RAW `date` READING

- **Date:** 2026-07-14
- **Context:** Applying `Last Updated` header timestamps and in-entry `Date:` fields
  during the BL-D-02 planning session and its End-of-Chat Ritual.

**Problem:**
Two `date` reads in the same session returned wall-clock values roughly a day and a half
apart (an early call implied 2026-07-13 morning; a later call implied 2026-07-14 night).
The first, stale reading had already been used to stamp four working files with
`07/13/2026` headers and `2026-07-13` in-entry dates. The authoritative session date was
2026-07-14 throughout, so those stamps were wrong and had to be corrected in a second
pass — the exact kind of avoidable rework the timestamp convention exists to prevent.

**Root Cause:**
The instruction "use the actual current time as reported by the system" implicitly assumes
the sandbox clock is a stable, monotonic wall clock. It is not: the execution sandbox can
be reset or re-provisioned between tool batches, so a raw `date` reading is a reading of
*that container's* clock at that moment, not a reliable session wall clock. Nothing in the
convention told the advisor to cross-check the reading against an independent source of the
current date.

**Fix Applied:**
Normalized every this-session file — the four already stamped plus all ritual outputs — to
a single authoritative timestamp (`07/14/2026 23:27 EDT`) derived from the session's known
current date rather than from whichever `date` reading was most recent. Verified that no
pre-existing prior-session dates were clobbered by the normalization (the originals held
zero `2026-07-13` references).

**Implication Going Forward:**
Treat the sandbox `date` command as a source for the *time-of-day* only, and cross-check
its *date* against the authoritative session date before stamping any file. When the two
disagree, the authoritative session date wins. Stamp all files produced in one session with
one consistent timestamp rather than re-reading the clock per file — a session is a single
logical "now," and per-file clock reads invite exactly the intra-batch date split seen
here. This is a convention refinement, not a rule violation; the wrong stamps were caught
and corrected before delivery.

**References:** LL-062 (header-currency defect class), DM-144, gov-lint-spec.md Section 4.4
(Check D validates header currency but not timezone/date correctness against an external
clock — this lesson is the human-side complement).

---

## LL-067 | A SPEC'S NAMED REGRESSION FIXTURES ARE NOT A SUBSTITUTE FOR AN INTEGRATION RUN AGAINST THE FULL REAL CORPUS

- **Date:** 2026-07-15
- **Context:** Building `gov_lint.py` (BL-D-02) against `gov-lint-spec.md`, which named five specific historical defects (DM-102, IN-016, FRIC-017, LL-034, a header-lag case) as required regression fixtures.

**Problem:**
The first working version of `gov_lint.py` passed all synthetic fixture tests, including the five named regression cases, but its `Status:`/`Date:` field-extraction regexes required a leading `- ` bullet before `**Field:**`. Real entries from an earlier convention era (DM-078 through DM-080, at minimum) write `**Status:**`/`**Date:**` with no bullet at all. Against the real files, this produced false "no Status field found" errors on three entries that do have a status — a wrong finding, not a missing one.

**Root Cause:**
The five named regression fixtures in the spec were all synthesized (correctly) around the *current* entry-template convention (bulleted fields). None of them happened to exercise the older unbulleted-field convention, because that specific drift pattern wasn't among the historical defects the spec's author had front-of-mind when naming fixtures. A synthetic-fixture-only test suite inherits the blind spots of whoever enumerated the fixtures; it cannot catch a format variant nobody thought to name.

**Fix Applied:**
Ran the finished script against the full real `/mnt/project` corpus (not just the fixture set) before declaring it done. This surfaced the bullet-format gap immediately; the field regexes were loosened to make the leading `- ` optional, and the unit tests were re-verified to still pass.

**Implication Going Forward:**
For any tool built against a spec that names specific historical defects as regression fixtures: treat those fixtures as a floor, not a ceiling. Always run the finished tool against the full real file(s) it will operate on before delivery, even when — especially when — the synthetic fixtures all pass. The named fixtures test whether the spec's *known* defects are caught; a real-corpus run tests whether *unknown* ones slip through.

**Addendum, same session:** a second, related defect surfaced the same way, one step later. Drafting this very entry's `Problem:` paragraph — which discusses `**Status:**`/`**Date:**` as regex targets — caused `gov_lint.py` to misfire again: its field regexes searched for `**Field:**` anywhere in an entry's body, so prose that merely *mentions* a field name (rather than declaring it) was indistinguishable from the field itself. This was not hypothetical — four pre-existing entries (LL-018, LL-026, LL-031, LL-061) were already being mis-flagged as "carrying a Status field" for exactly this reason, discovered only when this entry's own text tripped the same bug. Fixed by anchoring every field regex to the start of a line (`^`, optionally after a bullet dash) instead of a free `re.search` anywhere in the body. Generalization: a field-presence check on semi-structured text needs a *structural* anchor (line-start), not just the field's bolded name — a lesson that applies to any regex-based document parser, not just this one.

**References:** BL-D-02, gov-lint-spec.md, DM-144.

---

## LL-068 | SERIAL OVERCORRECTION IN RULE EVOLUTION — EACH TIMESTAMP RULE FIXED ONLY THE LAST FAILURE, ENDING WITH THE OPERATOR IN THE LOOP FOR A TRIVIAL FACT

- **Date:** 2026-07-17
- **Context:** The advisor asked the operator for the wall-clock time before a delivery batch, citing the carried-forward "stop and ask" constraint; the operator identified this as the wrong default.

**Problem:**
The timestamp rule had evolved into requiring operator involvement for every delivery batch. Retrieving the current time is machine-retrievable; the operator belongs in the loop only when no tool can answer.

**Root Cause:**
Rule evolution by serial overcorrection. Original failure: timestamps hallucinated without consulting any clock → rule: "use the actual system time." Second failure: sandbox clock date-split mid-session (LL-066) → rule: derive from the authoritative session date; clock for time-of-day only. Third failure: a temporary clock outage → carry-forward hardening: "stop and ask the operator." Each patch responded only to the most recent incident, with no enumeration of the full failure-mode set (hallucination, drift/re-provisioning, outage, multi-day sessions) — so the end state solved the rare case by imposing a per-batch human cost on the common case. A second instance of the same pattern surfaced within the fix session itself: a clock reading that appeared to jump four hours was initially suspected as drift (fighting the last war, LL-066), when an external `Date`-header cross-check showed the clock was correct and the operator's earlier time anchor was simply stale after a four-hour turn gap.

**Fix Applied:**
DM-148 / Instructions R-006 replaced the chain with a layered default: sandbox clock read at each delivery batch, `TZ` conversion, `ET` label, date sanity check, external HTTPS `Date`-header cross-check when in doubt, operator fallback only when both the clock and the cross-check fail. LL-066's "one timestamp per session" implication is refined to "one per delivery batch"; LL-066 itself is unedited per append-only discipline — this entry carries the refinement.

**Implication Going Forward:**
When a rule fails, enumerate the complete known failure-mode set before patching, and design the replacement as default-plus-fallback layers across all of them — not as a patch on the newest incident. Test for the inversion: if a rule escalates to human involvement for something a tool can retrieve, the human step belongs in the fallback branch, not the default. Corollary: operator-supplied facts that decay with time (clock anchors, "I just synced") are stale after any turn gap and must be re-derived or re-verified mechanically, not remembered — the same principle LL-065 established for "synced."

**References:** LL-065, LL-066, DM-148, R-006, carry-forward-2026-07-15.md.

---

## LL-069 | PRE-DELIVERY LINT OF THE STAGED BATCH IS A DELIVERY GATE, NOT A RITUAL-TIME-ONLY STEP — IT CAUGHT TWO DEFECT CLASSES IN ONE SESSION

- **Date:** 2026-07-17
- **Context:** Second delivery batch of the DM-148/R-006 session; `gov_lint.py` run against the staged files before copying anything to outputs.

**Problem:**
Two defects existed in the staged batch that reasoning had not caught: (1) the drafted DM-148 claimed the `ET` zone label had no `gov_lint.py` impact, but the linter's line-2 regex required `(EST|EDT)` and failed every `ET`-stamped file — the ritual matrix's conformance-rule row did fire, contrary to the drafted claim; (2) a foreign DM-148 entry, appended to the staged log by an aborted prior execution attempt (IN-031), was invisible to a prose read of the file tail but tripped the Check A duplicate-ID finding.

**Root Cause:**
The instructions position `gov_lint.py` at session start and at ritual time; nothing mandated linting each staged delivery batch before it ships. Both defects were catchable only mechanically: a "no linter impact" claim about a conformance-rule change is an empirical claim about a regex, not a judgment call, and foreign content inside a 6,800-line append-only log is not findable by inspection.

**Fix Applied:**
Ran the linter on the full staged corpus before delivery; both findings were fixed in-batch — the spec was amended and the linter rebuilt with a regression test per the matrix row, and the foreign entry was excised by rebuilding from the last delivered snapshot. The final batch was re-linted to exact baseline parity (168 errors / 80 warnings, all pre-existing) before copying to outputs.

**Implication Going Forward:**
Lint every staged delivery batch against the full governance corpus and require baseline parity — or explained deltas — before anything is copied to outputs; treat this as a delivery gate alongside the Delivery Rule. Never assert from reasoning alone that a conformance-rule change has no linter impact; run the linter, which is the ground truth for its own behavior. Candidate one-line codification into the Session Instructions at the next revision (queued in the carry-forward rather than churning a second revision in one session).

**References:** DM-148, IN-031, LL-041, LL-063, LL-067, gov-lint-spec.md.
