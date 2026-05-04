# Lessons Learned
**Last Updated:** 04/05/2026 21:00

Append-only log. Each entry documents a problem encountered, its root cause,
the fix applied, and the implication going forward.

Reference format from other documents: `# See LL-NNN`

**Mutability rules:**
- Append only. No existing entry is ever edited after it is written.
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

---

## LL-008 | Lint forced-choice step inserted after consolidation step, creating silent miss

**Date:** 2026-04-21
**Operation:** Schema design — lint procedure editing

**Problem Encountered:**
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
- **Problem encountered:** Agent stated a detailed plan for the index.md landing page
  design, then immediately executed all file edits and deliveries in the same turn
  without waiting for the user to engage with or confirm the plan.
- **Root cause:** The collaboration contract rule "plan first, act second" was misread
  as a sequencing constraint (do planning steps before execution steps, within a single
  turn) rather than a gating constraint (stop after the plan; execution requires explicit
  human go-ahead).
- **Fix applied:** None to the deliverables — the work product is not wrong. Process
  error only.
- **Implication going forward:** After stating a plan, stop. The next turn belongs to
  the user. Do not interpret "plan first, act second" as permission to collapse both
  steps into one response. Execute only after receiving explicit approval or a "proceed"
  signal. If the plan draws corrections, incorporate them before executing.

---

## LL-015 | Fix Plan Assumed Skill File Content Without Reading

- **Date:** 2026-04-22
- **Problem encountered:** The FRIC-018 fix plan stated that EXTRACTION-SKILL.md and
  TAGGING-SKILL.md "contain examples of skill enrichment proposal output" that would
  need updating to use the PS-N label. This was wrong. Both files contain enrichment
  content (§6.1, §5.1) — not examples of the proposal format. The proposal format
  lives in CLAUDE.md Step 21a. The user correctly instructed a re-read before writing.
  The error was caught before any incorrect edit was made.
- **Root cause:** The fix plan was drafted from memory of the skill file structure
  without reading the files first. The reasoning was plausible (skill files were known
  to contain forced-choice format examples from the design phase) but stale — the files
  had evolved, and the proposal format had never been placed in the skill files.
- **Fix applied:** Re-read both files before execution. Corrected scope: no skill file
  changes required for FRIC-018. Only CLAUDE.md Steps 21a and 22 changed.
- **Implication going forward:** When a fix plan references specific content in a
  project file, read that file before finalizing the plan — not after confirming it.
  Plausible reasoning about file content is not a substitute for reading. This applies
  especially to skill files, which are updated by ingest operations between sessions.

## LL-016 | Fix Plan Used Tool Page Status Vocabulary on Source Page

- **Date:** 2026-04-22
- **Problem encountered:** The FRIC-019 fix plan (in the carry-forward prompt) specified
  "`status: superseded` or `status: retracted`: hard stop still applies." Source pages
  have no `status: superseded`. The controlled values for source page status are
  `active | retracted | ingested-in-error`. The `superseded` value belongs to Tool and
  Topic pages. The error was caught before writing and corrected to `retracted or
  ingested-in-error` during execution.
- **Root cause:** The fix plan was drafted with source and tool page status vocabularies
  conflated. Both page types have a `status` field, but their controlled vocabularies
  differ. The distinction is easy to miss when reasoning about the schema at a distance
  without consulting the frontmatter specs.
- **Fix applied:** Corrected the condition in Step 2 and the DM-059 entry to use the
  correct source page status vocabulary (`retracted | ingested-in-error`).
- **Implication going forward:** Before writing any fix plan that references a `status`
  field, confirm which page type is involved and check the controlled vocabulary for
  that page type in CLAUDE.md Section 5. Do not assume that vocabulary is consistent
  across page types.

---

## LL-017 | Normal Ingest Path Had No Explicit Staged File Cleanup Step

- **Date:** 2026-04-23
- **Problem encountered:** While planning the FRIC-022 fix (consumed sources not preserved),
  the carry-forward prompt assumed staged file removal was already specified in the normal
  ingest path and that the fix would only need to change "remove" to "move." In fact, the
  normal path (Steps 10–22a) contained no staged file disposal instruction at all. Only the
  enrichment path (Step 2a) had a disposal instruction. The carry-forward description of the
  fix scope was therefore incomplete.
- **Root cause:** The ingest workflow was designed with the implicit assumption that staged
  files would be cleaned up by the human or by the operating environment, not by the schema.
  No one noticed the omission because the only explicit disposal instruction (Step 2a) was
  added for a different reason (enrichment path) and was never generalized.
- **Fix applied:** Added Step 22b to the execution pass as an explicit post-ingest
  housekeeping step covering both staged files (move to raw/processed/) and queue entries
  (move to ## [processed] with processed date appended).
- **Implication going forward:** When writing fix plans that reference "the existing cleanup
  step," verify that the step actually exists in the current schema before citing it. Do not
  infer the presence of a step from context or operational common sense. Read the schema
  text first.

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

**Fix applied:**
Added Step 7a (pre-flight pitfalls proposal — fires when source contains at least one
substantive failure mode meeting the named-entry threshold) and Step 13a (execution —
creates or updates Pitfalls page if Step 7a confirmed). Threshold: nameable failure
mode with `**Status:**` designation. Passing mentions of limitations do not qualify.

**Implication going forward:**
When adding a new page type to the schema, explicitly verify that the ingest workflow
has both a pre-flight proposal step and an execution step for that type. The
existence of a page type in Section 3 and a frontmatter spec in Section 5 is not
sufficient — without workflow steps, the type is unreachable from ingest.

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
