# Information Needs
**Last Updated:** 07/25/2026 13:38 ET

Authoritative repository of open questions, data gaps, and contradictions that must
be resolved before dependent design or implementation work can proceed.

Reference format from other documents: `# See IN-NNN`

**Mutability rules:**
- Open and partial entries are updated in place.
- Closed entries are append-only: resolution is added; no other content is changed.
- Entries are never deleted. If a gap proves to be a non-issue, close it with an explanation.
- Exception for closed entries (DM-147, `decisions_made.md`): a gov_lint-flagged
  conformance correction to an entry's *form* (status-value casing, field-name repair,
  heading format) may be made in place under mandatory guards logged in the correcting
  DM. See `decisions_made.md` DM-147 for the full rule; it applies across all four
  append-only logs.

Sorted by priority tier at all times. Within a tier, higher-consequence blockers appear first.

---

## Priority Definitions

- **P1** — Blocks all design progress on a major component. Nothing depending on this can proceed.
- **P2** — Blocks a specific design path. Alternative approaches may be possible but carry risk.
- **P3** — Informational gap. Design can continue but with acknowledged uncertainty.

---

## Entry Template

```
## IN-NNN | [SHORT DESCRIPTIVE TITLE]

- **Status:** open | partial | closed
- **Priority:** P1 | P2 | P3
- **Category:** Architecture | Implementation | Tooling | Domain | Process
- **Raised:** YYYY-MM-DD
- **Resolved:** YYYY-MM-DD    ← populate only when CLOSED or PARTIAL

**Question / Gap / Contradiction:**
[One specific, answerable question or clearly stated contradiction.]

**Why This Blocks Progress:**
[What cannot proceed, and why.]

**Resolution:**
[Leave blank until resolved.]

**References:** DM-NNN, LL-NNN
```

---

## P1 — Blocks Major Progress

## IN-001 | Wiki Domain and Purpose Are Undefined

- **Status:** closed
- **Priority:** P1
- **Category:** Domain
- **Raised:** 2026-04-14
- **Resolved:** 2026-04-15

**Question / Gap / Contradiction:**
What is the target domain, subject matter, and intended purpose of the wiki being designed?

**Why This Blocks Progress:**
The schema document cannot be designed without knowing what the wiki is for.

**Resolution:**
AI effectiveness wiki for a small technical team (2–5 people). Domain covers: AI tools and workflows, emerging capabilities and their taxonomies, AI alignment vs performance tradeoffs, and novel methodologies and applications. Five named query patterns established. RAG use case held open pending schema design. Source types confirmed: research papers, industry blog articles, white papers, articles from credible publications, YouTube videos.

**References:** DM-002, DM-004, DM-005

---

## IN-002 | Wiki Schema Document Is Not Yet Designed

- **Status:** closed
- **Priority:** P1
- **Category:** Architecture
- **Raised:** 2026-04-14
- **Resolved:** 2026-04-19

**Question / Gap / Contradiction:**
What are the conventions, page types, frontmatter standard, naming rules, and operational workflows that will govern the wiki?

**Why This Blocks Progress:**
Without a schema, the wiki-executing LLM will invent conventions on the fly, causing drift.

**Resolution:**
All schema components are now fully specified and encoded in CLAUDE.md:
- Page type taxonomy, frontmatter specifications, naming conventions, directory structure,
  version handling, controlled vocabularies: DM-009 through DM-016.
- Source classification taxonomy: DM-017, DM-018. See CLAUDE.md Section 11.1.
- Ingest workflow (Steps 1–22): DM-019 through DM-022. See CLAUDE.md Section 11.2.
- Contradiction resolution protocol including flag format, log entries, and override
  mechanism: DM-023, DM-025, DM-030, DM-031, DM-032. See CLAUDE.md Sections 8.3, 8.4.
- Lint procedure (Steps L1–L13, Phase 3): DM-033, DM-034. See CLAUDE.md Section 11.4.
- Query workflow (Steps Q1–Q8): DM-035, DM-036, DM-037, DM-038.
  See CLAUDE.md Section 11.5.
- Supporting schema additions: DM-024 (wiki-lessons-learned.md), DM-026 (page length),
  DM-027 (summary field), DM-028 (conformance check), DM-029 (skill files).

Remaining open items: none. CLAUDE.md is complete. Stub sections 11.4 and 11.5 are
fully filled in. The schema is ready for portability review before use in the execution
environment.

**References:** IN-001, DM-002, DM-009 through DM-038

---

## P2 — Blocks Specific Paths

## IN-003 | Source Classification Taxonomy Not Defined

- **Status:** closed
- **Priority:** P2
- **Category:** Architecture
- **Raised:** 2026-04-14
- **Resolved:** 2026-04-18

**Question / Gap / Contradiction:**
What classification system will distinguish source types and map each to an appropriate extraction depth and page template?

**Why This Blocks Progress:**
Without classification rules, the ingest workflow cannot specify extraction behavior per source type.

**Resolution:**
Eight source types confirmed: research-paper, industry-blog, white-paper, publication-article, youtube-video, practitioner-reference, vendor-content, policy-document. Each mapped to extraction depth (full or standard) and credibility tier assignment logic. Institutional tier lists are controlled. vendor-content sources carry a vendor_bias flag applied during extraction. policy-document sources are institutional-tier always and exempt from age-based staleness flagging. YouTube sources require a human-provided transcript file as a prerequisite. Model-class vs. application-class classification decision criteria confirmed. See DM-017, DM-018, CLAUDE.md Section 11.1.

**References:** IN-001, IN-002, DM-015, DM-017, DM-018

---

## IN-004 | Contradiction Resolution Protocol Not Defined

- **Status:** closed
- **Priority:** P2
- **Category:** Process
- **Raised:** 2026-04-14
- **Resolved:** 2026-04-19

**Question / Gap / Contradiction:**
When a new source contradicts an existing wiki page, what is the resolution procedure?

**Why This Blocks Progress:**
The lint operation can detect contradictions but cannot resolve them without a protocol.

**Resolution:**
Three-path weighted contradiction model confirmed (DM-023). Credibility weights, support
score with 12-month decay, and decay_exempt flag specified. Operational path aliases
confirmed: auto-resolved, human-review, minority-view (DM-032).

Contradiction flag format: two-component design — `open_contradictions` frontmatter list
plus `contested [CTRD-NNN]` inline marker in Key Claims table. Global CTRD-NNN counter
tracked in `last_contradiction_id` on overview.md (DM-030). See CLAUDE.md Section 8.3.

Override mechanism: `CTRD-NNN:override` and `CTRD-NNN:confirm` lines in queue.md,
processed at start of every lint and ingest pre-flight pass. Redundant surfacing via
lint Step L4b forced choices with explicit skip option (DM-031, DM-034). Three outcomes
fully specified: override, confirm, window-expired-confirmed. See CLAUDE.md Section 8.4.

Log entry structure: three entry types specified — `contradiction-flag`,
`contradiction-resolved`, `contradiction-auto-resolved`. All use operational aliases.
See CLAUDE.md Section 12.

**References:** IN-002, DM-003, DM-023, DM-025, DM-030, DM-031, DM-032, DM-034

---

## IN-005 | Execution Environment for Wiki Not Selected

- **Status:** closed
- **Priority:** P2
- **Category:** Tooling
- **Raised:** 2026-04-14
- **Resolved:** 2026-04-16

**Question / Gap / Contradiction:**
What LLM agent and execution environment will maintain the wiki?

**Why This Blocks Progress:**
Schema conventions depend on the execution environment's capabilities and constraints.

**Resolution:**
Claude Code at Pro tier ($20/month fixed) as wiki maintenance agent. Git repository as wiki store. Obsidian as local reading interface. Quartz on GitHub Pages as public-facing published site. All Mac-native. See DM-007.

**References:** IN-002, DM-002, DM-007, DM-008

---

## IN-030 | BL-D-03's Planned Status-Value Corrections Are Not Covered by Any Existing Mutability Rule

- **Status:** closed
- **Priority:** P2
- **Category:** Process
- **Raised:** 2026-07-15
- **Resolved:** 2026-07-17

**Question / Gap / Contradiction:**
BL-D-03 plans to correct DM-102's `Status: Closed` and IN-016's `partially resolved` to canonical lowercase values, plus structural repairs to FRIC-017 and LL-034. But `decisions_made.md`'s own mutability rules authorize exactly one in-place edit: the coupled `Status: AMENDED` + `Amended By:` pair (or the `Superseded By:` equivalent) for the amendment mechanism specifically. There is no existing rule authorizing an in-place casing/value correction to a historical entry's `Status` field for any other reason, and `implementation-friction.md`/`info_needs.md` have their own, separately-scoped mutability conventions that may or may not cover this either.

**Why This Blocks Progress:**
Blocks BL-D-03 from proceeding safely: editing DM-102's `Status:` value in place, as currently scoped, would be an edit to an existing entry's content outside any documented exception — exactly the kind of edit the append-only convention exists to prevent. This must be resolved (either by identifying that an existing rule already covers it, or by adding a narrowly-scoped new exception) before BL-D-03 execution, not discovered mid-edit.

**Resolution:**
Resolved 2026-07-17 by DM-147: no existing rule covered the planned corrections (the old rules' first bullet protected only four named content fields while the amendment bullet claimed exclusivity over all in-place edits — an internal inconsistency, now also fixed). A **conformance-correction exception** was added to `decisions_made.md`'s mutability rules as a second permitted in-place edit class, applying to all four append-only logs, split into **pure form** corrections (no intent determination) and **out-of-vocabulary value** corrections (intent determined from entry content or operator confirmation first, else raise an IN instead of editing). Four mandatory guards: gov_lint Check B/C/F-flagged defects only; substantive content never touched; every batch logged in a DM with exact before → after text (the logs have no version control — the DM is the only history); per-batch operator confirmation. Alternatives ruled out (lawyerly reading of existing rules; formal amendment per fix; permanent acceptance / lint baseline; broad operator-edit exception) are recorded in DM-147. BL-D-03 is unblocked; its detail block now carries the before → after logging obligation.

**References:** BL-D-03, DM-102, IN-016, DM-147, gov-lint-spec.md, decisions_made.md (Mutability rules).

---

## P3 — Informational Gaps

## IN-006 | Scale Threshold for Index-Only Navigation Not Established

- **Status:** closed
- **Priority:** P3
- **Category:** Architecture
- **Raised:** 2026-04-14
- **Resolved:** 2026-05-26

**Question / Gap / Contradiction:**
At what wiki size does index.md-based navigation become insufficient, and what is the recommended escalation path?

**Why This Blocks Progress:**
Does not block initial schema design. Frontmatter and tagging conventions are already designed to accommodate a future search layer without revision. The `summary` field (DM-027) directly improves future search quality. Quartz native search (Ctrl+K) is the baseline and is adequate up to approximately 150–200 pages. qmd hybrid search (BM25/vector, MCP server available) is the recommended escalation path — compatible with existing frontmatter without schema revision.

**Resolution:**
Closed 2026-05-26 with a two-part trigger (DM-111). The Quartz side and agent side degrade on different schedules and require separate thresholds:
1. **Quartz side:** implement qmd when single-concept Quartz search (Ctrl+K) routinely returns >10 results.
2. **Agent side:** implement qmd when index.md exceeds ~300 lines, OR when a query session produces a sparse/shallow result on a topic that visibly has coverage in the wiki — whichever comes first.
At closure: wiki is at 102 pages, index.md is at 141 lines. Neither trigger is close.

**References:** IN-002, DM-027, DM-111

---

## IN-007 | Query Nomination Queue Scalability at Scale

- **Status:** closed
- **Priority:** P3
- **Category:** Architecture
- **Raised:** 2026-04-19
- **Resolved:** 2026-04-21

**Question / Gap / Contradiction:**
At what size does the `[nominated]` section of queue.md become too large for reliable
title-string matching against query topics, and what is the escalation path?

**Why This Blocks Progress:**
Does not block initial schema design or early operation. The gap nomination mechanism
(CLAUDE.md Section 11.5 Step Q2a) uses title-string matching between query topics and
nominated items in queue.md. At small queue sizes (under 20 items) this is tractable
and the human is an effective filter. As the nominated queue grows — particularly if
discovery passes run frequently without corresponding human review — the matching becomes
noisy and the forced choice block may surface low-relevance nominations alongside
relevant ones, degrading the human's ability to filter efficiently.

**Resolution:**
Two-stage automatic aging implemented in CLAUDE.md (DM-051). A `nominated: YYYY-MM-DD`
field is appended to every nomination line at write time. Lint Step L1a scans both
`[nominated]` and `[stale-nominated]` sections and marks items for aging:
- Stage 1 (≥90 days): moved from `[nominated]` to `[stale-nominated]` during lint
  Phase 3. Suppressed in ingest forced choices; visible only via query demand signal
  (sparse/shallow result in Step Q2a), where they surface in a separate "Older
  nominations" block with the same A/B/C choices.
- Stage 2 (≥180 days): deleted from `[stale-nominated]` during lint Phase 3.
  Never re-surfaced; a deleted item that later becomes relevant must be re-nominated
  from scratch.
Both stages are auto-execute with no forced choice; the lint informational summary
lists all items being moved or deleted, giving the human a rescue window before
Phase 3 executes. Option (b) from the escalation path — maximum nomination age — is
now implemented. Option (c) — semantic matching via the search layer — remains
available as a future escalation if title-string matching proves insufficient even
with the aging mechanism in place.

**Escalation path (to be resolved when queue approaches 20 unreviewed nominations):**
Options include: (a) raise the specificity of title-string matching by requiring exact
topic-slug matches rather than shared-term matches; (b) apply a maximum nomination age
after which items are auto-discarded; (c) extend the search layer (IN-006 escalation)
to cover queue.md as well as wiki pages, enabling semantic matching. Option (b) is the
lowest-cost starting point and does not require schema revision.

**References:** DM-036, DM-051, IN-006

---

## IN-008 | Teaching Index Does Not Grade Content by Accessibility Level

- **Status:** closed
- **Priority:** P3
- **Category:** Architecture
- **Raised:** 2026-04-20
- **Resolved:** 2026-04-20

**Question / Gap / Contradiction:**
Should an optional `technical_depth` field be added to Topic and Tool pages so that
the Teaching Index can surface content by accessibility level — distinguishing content
accessible to non-technical professionals from content requiring practitioner or
research-level ML background?

**Why This Blocks Progress:**
Does not block implementation. The teaching relevance gate (Section 7.3) and the
Teaching Index already exist and function without this field. The gap is a usability
gap: the Teaching Index currently presents a flat list of tagged pages with no
accessibility signal. A reader seeking foundational content cannot distinguish it from
practitioner-level content without reading the page. The risk is that a source diet
weighted toward technical lab blogs and research papers produces a Teaching Index that
is nominally populated but practically inaccessible to lay readers — the tagging gate
passes pages, but the pages still presuppose significant ML background.

**Proposed resolution:**
Add an optional `technical_depth` field to Topic and Tool page frontmatter.
Controlled values: `foundational | practitioner | research`. Claude Code assigns the
value at ingest based on source prerequisites. The Teaching Index renders this field
as a visible label. No scaffold file changes required — this is an optional frontmatter
addition to content pages only. Resolve before the wiki grows beyond 20–30 pages, at
which point the Teaching Index becomes the primary entry point for non-technical readers.

**Complementary mitigation (no schema change required):**
Deliberately include accessible practitioner-tier sources (MIT Technology Review,
HBR AI coverage) via manual `raw/queue.md` additions. Discovery feed is institutional-
tier only; accessible content must be curated manually. This supplements but does not
replace the schema-level signal a `technical_depth` field would provide.

**Resolution:**
Optional `technical_depth` field added to Topic and Tool page frontmatter (DM-048).
Controlled values: `foundational | practitioner | research`. Assigned by Claude Code
at ingest without human confirmation. Added to CLAUDE.md Sections 5.2, 5.3, 10
(Teaching Index generation rule 5), and Step 12 (ingest execution pass). The
"research" value covers both technical ML research and non-technical policy/alignment
research, scoped as "deep AI/ML background or equivalent research-level familiarity."
Complementary mitigation: four accessible/policy institutional sources added to the
default discovery feed (DM-049) to supplement the technical lab blog diet.

**References:** DM-012, DM-016, DM-048, DM-049

---

## IN-009 | Pitfalls Source Attribution Implementation

- **Status:** closed
- **Priority:** P2
- **Category:** Architecture
- **Raised:** 2026-04-25
- **Resolved:** 2026-04-25

**Question / Gap / Contradiction:**
Pitfalls page failure mode entries carry no source attribution. The retraction procedure
(Section 8.2) and ingested-in-error correction (Section 8.6) are blind to Pitfalls content.
How should source attribution be specified at both the entry level and the page frontmatter
level, and what changes are required to Section 8.2 and 8.6?

**Why This Blocks Progress:**
Without attribution, a retracted or ingested-in-error source leaves its failure mode
entries in the wiki permanently — no procedure flags or removes them. The two existing
Pitfalls pages already contain empirically specific claims with this exposure. Each
new Pitfalls page ingested before this is fixed increases the scope of that exposure.

**Resolution:**
Add `**Source:** [[source-slug]]` citation line to the failure mode entry format in
Section 5.6, immediately after `**Status:**`. Add `contributing_sources` list field
to Section 5.6 frontmatter. Update Step 13a to write the `**Source:**` line when
creating or updating failure mode entries. Update Section 8.2 retraction procedure
and Section 8.6 IE correction to scan Pitfalls pages and surface failure mode entries
whose sole contributing source is the affected source page. Manual remediation required
for two existing Pitfalls pages.

**References:** DM-066, DM-068

---

## IN-010 | Lint L11 Summary Field Check Produces False Violations on Comparison and Pitfalls Pages

- **Status:** closed
- **Priority:** P2
- **Category:** Process
- **Raised:** 2026-04-25
- **Resolved:** 2026-04-25

**Question / Gap / Contradiction:**
Step L11 checks "summary field: Present, non-empty, single sentence" across all sampled
pages. Comparison (Section 5.5) and Pitfalls (Section 5.6) frontmatter specs contain no
`summary` field. Should the check be narrowed, or should `summary` be added to these
page types?

**Why This Blocks Progress:**
Fires on the first lint pass. Three or more Comparison or Pitfalls pages updated since
last lint escalates to a false "systemic drift" forced choice. This trains the operator
to dismiss drift flags, degrading the signal value of the lint conformance check.

**Resolution:**
Narrow the summary field criterion in Step L11 to apply to Topic and Tool pages only.
One-line edit to the L11 conformance check table in Section 11.4. Comparison pages are
derived artifacts whose synthesis replaces the summary concept; Pitfalls pages use the
`parent_entity` field to identify their scope.

**References:** DM-068

---

## IN-011 | Stale → Current Transition Mechanism Missing

- **Status:** closed
- **Priority:** P2
- **Category:** Process
- **Raised:** 2026-04-25
- **Resolved:** 2026-04-25

**Question / Gap / Contradiction:**
Pages marked `status: stale` by lint Step L5 have no automated path back to `current`.
Step 12 explicitly prohibits upgrading to `current` during ingest. Lint Phase 3 has no
upgrade step. A page receiving consistent new ingest passes will have `last_assessed`
updated to today but its `status` will remain `stale` indefinitely. What is the correct
transition mechanism?

**Why This Blocks Progress:**
Actively maintained pages will accumulate `stale` status indefinitely. Query responses
must flag stale claims; pages that are actually current but status-stale produce false
staleness warnings. At scale, the staleness signal becomes meaningless noise.

**Resolution:**
Add a lint Phase 1 check (between L5 and L6) that identifies pages with `status: stale`
where `last_assessed` is within the past 90 days and `open_contradictions` is empty or
absent. Surface as a forced choice: "Page [[slug]] meets currency criteria (`last_assessed`
within 90 days, no open contradictions) but has `status: stale`. Confirm current?" Options:
A) Upgrade to `current`, B) Leave as `stale`. Lint Phase 3 applies confirmed upgrades.
This is human-confirmed, not auto-execute — matching the intent that `current` status
requires active assessment confirmation.

**References:** DM-068

---

## IN-012 | open_contradictions Counter in overview.md Has No Reconciliation Check

- **Status:** closed
- **Priority:** P3
- **Category:** Process
- **Raised:** 2026-04-25
- **Resolved:** 2026-04-25

**Question / Gap / Contradiction:**
The `open_contradictions` integer counter in `overview.md` is incremented at ingest (Path B
creation) and decremented at resolution. No lint step validates the counter against the
actual count of open `open_contradictions` list entries across all page frontmatter. Counter
drift is undetectable until a human notices the number looks wrong.

**Why This Blocks Progress:**
A counter reading 0 when open contradictions exist misleads at a glance. Conversely, a
non-zero counter when all contradictions are resolved causes unnecessary concern. The
counter is the summary-level signal for the wiki's contradiction state.

**Resolution:**
Add a lint Phase 1 check that counts actual open `open_contradictions` list entries across
all page frontmatter and compares against the overview.md counter. If off by 1: informational
note only. If off by 2+: surface as a forced choice with option to correct the counter.
Add counter correction to lint Phase 3 execution if confirmed.

**References:** DM-068

---

## IN-013 | Schema Signals Entries Have No Aging Mechanism or Lint Visibility

- **Status:** closed
- **Priority:** P3
- **Category:** Process
- **Raised:** 2026-04-25
- **Resolved:** 2026-04-25

**Question / Gap / Contradiction:**
Schema Signals entries with `**Status:** open` in `wiki-lessons-learned.md` accumulate
without any lint step surfacing signals that have been open for extended periods. An
operator who does not proactively review the file can miss signals indefinitely.

**Why This Blocks Progress:**
The aggregation mechanism (L12c) can correctly identify systematic patterns, but the
escalation path (human brings signal to a design session) has no tripwire. Signals can
be ignored until the underlying problem grows large enough to surface as an obvious friction
report — at which point the cost of unwinding it is higher.

**Resolution:**
Add an informational note to the lint report (either as part of L12c output or a new
sub-step L12c-1): list all `## Schema Signals` entries with `**Status:** open` older
than 60 days by name and age. No forced choice — informational only. The human decides
whether to bring a signal to a design session as a friction report.

**References:** DM-068, DM-064

---

## IN-014 | Teaching Index Stub Page Inclusion Policy Undefined

- **Status:** closed
- **Priority:** P3
- **Category:** Process
- **Raised:** 2026-04-25
- **Resolved:** 2026-04-25

**Question / Gap / Contradiction:**
Section 10 Teaching Index generation rules exclude deprecated Tool pages but say nothing
about stub pages. A stub page tagged `teaching_relevance: true` would appear in the
Teaching Index with minimal content (1–3 Key Claims, 2–4 sentence prose), which could
mislead instructors querying for teaching material.

**Why This Blocks Progress:**
Low probability of impact currently — stub pages are unlikely to receive `teaching_relevance:
true` tags. Becomes a real issue as the wiki scales and stub pages may receive teaching tags
before they are fully developed.

**Resolution:**
Add "Exclude stub pages" to Section 10 generation rules, parallel to the existing
"Exclude deprecated Tool pages" rule. One-line addition.

**References:** DM-068

---

## IN-015 | Query-Generated Visualizations Have No Filing Workflow

- **Status:** open
- **Priority:** P3
- **Category:** Architecture
- **Raised:** 2026-04-26
- **Resolved:** —

**Question / Gap / Contradiction:**
Karpathy's gist describes query outputs that include matplotlib charts, and notes that
good query results should be filed back into the wiki as pages. If a query generates an
image (e.g., a comparison chart), where does the image file live such that it renders
in the Quartz-published site? The current schema has no naming convention, storage path,
or ingest step for query-generated images. `assets/` is excluded from Quartz rendering;
`quartz/static/` renders publicly but has no specified wiki workflow.

**Why This Blocks Progress:**
Does not block current operation — no query has yet generated a visualization requiring
filing. Becomes relevant when the query workflow is extended to support matplotlib or
similar chart outputs, or when a filed Comparison page needs an embedded figure.

**Resolution:**
—

**References:** DM-077, DM-035

---

## IN-016 | Key Claims Table Has No Eviction Mechanism for Novel Claims at Cap

- **Priority:** P3
- **Category:** —
- **Status:** partial
- **Raised:** 2026-04-27
- **Resolved:** —

**Question / Gap / Contradiction:**
The schema requires 3–5 Key Claims per page and states that claims must be "the most
consequential and time-sensitive assertions on the page." However, there is no procedure
for the case where a new source produces a genuinely novel, high-consequentiality claim
and the table is already at 5. The agent has no authority to evict the weakest existing
claim and no procedure to propose a swap as a forced choice. The current behavior is to
silently skip the new claim if it does not contradict an existing one.

**Why This Blocks Progress:**
Does not block current operation. The pattern is rare: novel claims on fully-saturated
pages typically either trigger Section 8 (contradiction) or map to a different page.
Becomes relevant if high-value sources consistently produce novel claims on mature,
well-established pages.

**Resolution:**
Partially resolved 2026-07-08 (DM-129): the eviction policy is fully specified in
key-claims-eviction-spec.md — deterministic ranking with candidacy floor, option D on
the DM-115 overcap card, and an ingest-time swap forced choice in the post-ingest
summary Section B covering exactly this gap (novel non-contradicting claim at a page
with >= 5 rows is no longer silently skipped once adopted). Stage 1 trigger
instrumentation executes with the BL-W-04 Claude Code session; Stage 2 adoption is
gated on the third overcap card surfacing on a single page, counted from
instrumentation onward. Close this entry when Stage 2 executes.

**References:** FRIC-031, DM-072, DM-115, DM-129, key-claims-eviction-spec.md

---

## IN-017 | Competency Domain Gap: AI System Design and Technical Implementation

- **Priority:** P3
- **Category:** —
- **Status:** open
- **Raised:** 2026-04-30
- **Resolved:** —

**Question / Gap / Contradiction:**
No competency domain in Section 7.1 covers AI system design, evaluation pipeline
architecture, LLM API integration, RAG architecture, deployment reliability, or MLOps.
`practical-ai-use-and-interaction` is explicitly "task-level use: prompting, iteration,
output refinement" and does not reach system-level design. `ai-integration-in-organizational-
workflows` is oriented toward multi-actor processes and accountability structures, not
technical implementation. A page on prompt reliability in production systems or evaluation
pipeline design has no domain that cleanly receives it.

**Why This Blocks Progress:**
Does not block current operation. The wiki's current content is positioned at the AI
effectiveness / use level; no ingested content yet requires this domain bin. Becomes
relevant when sources covering LLM API integration patterns, evaluation pipeline design,
RAG architecture, or MLOps are queued.

**Trigger:** Revisit before ingesting any source whose primary subject is AI system
architecture, evaluation pipeline design, RAG/retrieval systems, LLM deployment
reliability, or MLOps.

**Resolution:**
—

**References:** DM-091, DM-090, CLAUDE.md Section 7.1

## IN-018 | Retroactive Vocabulary Matching in Lint — Design Not Specified

- **Priority:** P3
- **Category:** —
- **Status:** open
- **Raised:** 2026-05-04
- **Resolved:** —

**Question / Gap / Contradiction:**
The vocabulary expansion procedure in OPERATIONS.md Section 11.6 is human-triggered and
requires the operator to remember to run it after each vocabulary addition. There is no
lint step that detects the condition "vocabulary term exists but has never been applied to
any tagged page" and surfaces it as a signal. A term could be added to the controlled
vocabulary, the expansion pass skipped, and the omission would be invisible until a human
noticed the term had zero wiki entries in the Teaching Index.

Should lint include a lightweight check — e.g., "any professional context or competency
domain term in Section 7.1/7.2 with zero occurrences across all tagged pages" — that
flags the gap informally? Alternatively, should the vocabulary addition DM entry template
include a mandatory "expansion pass completed: yes/no" field to enforce the two-step
pattern?

**Why This Blocks Progress:**
Does not block current operation. The vocabulary expansion procedure exists and is
documented. The risk is operator forgetting, not missing tooling. Becomes more relevant
as the vocabulary grows and the number of terms requiring back-population after each
addition increases.

**Trigger:** Revisit when a second vocabulary term is added and the expansion pass is
either skipped or produces unexpected results.

**Resolution:**
—

**References:** DM-091, DM-095, LL-033, OPERATIONS.md Section 11.6

---

## IN-019 | Lint Detection of Commercial-Entity Sources Misclassified as practitioner-reference

**ID:** IN-019
**Priority:** P3
**Category:** —
**Status:** open
**Raised:** 2026-05-18
**Resolved:** —

**Question / Gap / Contradiction:**
The new entity-type boundary rule (DM-096) means that commercial entities operating
aggregator leaderboards or comparison tables are `vendor-content`, not
`practitioner-reference`. The lint procedure has no explicit check for this condition.
A source ingested before DM-096 (or ingested by an agent that misjudges the boundary)
could sit as `practitioner-reference` indefinitely without a lint signal.

**Why This Blocks Progress:**
The wiki has 30 sources. Manual review of `practitioner-reference` sources for
commercial-entity origin is feasible at current scale. The gap becomes meaningful as
the source count grows, or as more aggregator/leaderboard sources are ingested.

**Trigger:** Revisit when a second misclassification of this type is detected, or when
source count exceeds 75 and manual audit becomes impractical.

**Resolution:**
—

**References:** DM-096, FRIC-035, OPERATIONS.md Section 11.1

---

## IN-020 | Large-Document Decomposition Threshold Calibration

**ID:** IN-020
**Priority:** P3
**Category:** —
**Status:** open
**Raised:** 2026-05-24
**Resolved:** —

**Question / Gap / Contradiction:**
FRIC-037 set the chunking threshold at >100 pages (PDF) or >50,000 words (other formats),
derived from the Stanford HAI AI Index (425 pages) as the triggering case. The current
threshold has not been validated against lower-density documents. Four specific questions
require investigation:

1. **Cost of unnecessary chunking.** What is the actual cost when chunking fires on a
   document that would have fit in one session (e.g., a 60-page PDF with a threshold of
   50 pages)? If the cost is low — one extra manifest file, one extra session boundary —
   a lower threshold is defensible as a conservative default.

2. **Cost of not chunking.** What is the cost of the failure mode FRIC-037 was designed
   to prevent: a document that needed chunking processed in a single session, leading to
   compaction and lost extraction work?

3. **Structural marker effect.** Does the presence of a TOC or section headers change the
   calculus? A well-structured 80-page document decomposes cleanly at a 50-page split; an
   unstructured 80-page document may produce poor chunks at the same boundary. A
   structure-conditional threshold (lower for unstructured, higher for structured) may be
   more accurate than a single page-count number.

4. **Empirical signal.** Is there evidence from actual ingest sessions that the 100-page
   threshold is too high — e.g., compaction events during ingest of documents in the
   70–100 page range?

**Why This Blocks Progress:**
The threshold is functional and has not produced confirmed failures since FRIC-037 was
resolved. This is a calibration question, not a correctness gap.

**Trigger:** Revisit when any of the following: (a) compaction is observed during ingest
of a document below the 100-page threshold; (b) a document with a TOC/headers is
chunked at a boundary that produces poor extraction; or (c) operator decides to revisit
as a deliberate tuning exercise.

**Deliverable when resolved:** Assessment with recommendation to keep, lower, or make the
threshold conditional on document structure. If a change is recommended: OPERATIONS.md
edit and a DM entry.

**Resolution:**
—

**References:** FRIC-037, OPERATIONS.md Section 11.2 (Step 0 high-density source handling)

---

## IN-021 | Decisions Made Mutability Rule vs. Entry Template Contradiction on Amendment Status

- **ID:** IN-021
- **Status:** closed
- **Priority:** P3
- **Category:** Process
- **Raised:** 2026-06-14
- **Resolved:** 2026-06-30

**Question / Gap / Contradiction:**
When a `decisions_made.md` entry is amended, does the `Status` field flip from `ACTIVE` to
`AMENDED` alongside the `Amended By: DM-NNN` line, or does `Status` remain `ACTIVE` with
`Amended By` serving only as an informational pointer? The entry template's field comment
(`Amended By: DM-NNN ← populate only if Status is AMENDED`) implied the former, but the
prose mutability rule named only "add `Amended By: DM-NNN`" as the permitted in-place edit
and never mentioned the Status field — a contradiction between template and prose. The gap
was not hypothetical: DM-111 was left `Status: ACTIVE` after being amended by DM-120,
diverging from three prior amendments (by DM-023, DM-039, DM-044) that had correctly set
`Status: AMENDED`.

**Why This Blocks Progress:**
Did not block current operation — no dependent work was waiting on this. Left unresolved,
it risked further inconsistent application on each new amendment, eroding the Status
field's reliability as a signal of which entries stand exactly as written.

**Resolution:**
`Status: AMENDED` and `Amended By: DM-NNN` are set together as a single in-place edit;
neither is populated without the other. DM-111 corrected to `Status: AMENDED`. The prose
mutability rule rewritten to state the coupled edit explicitly rather than relying on the
template's field comment alone. See DM-121.

**References:** DM-111, DM-120, DM-121, LL-056

---

## IN-022 | P9 TOC-Zone Detection: Duplicate-Title Handling and Threshold Generalization Unconfirmed

- **ID:** IN-022
- **Status:** open
- **Priority:** P4
- **Category:** Validation
- **Raised:** 2026-06-30
- **Resolved:** —

**Question / Gap / Contradiction:**
`pdf_to_markdown.py`'s P9 TOC-echo zone detection (DM-122) was validated against a single document — the Claude Sonnet 5 System Card — with a wide margin (36-37 mismatched matches per printed-TOC page vs. zero on every real content page). Two aspects of the design are unconfirmed on real data:
(1) `build_toc_page_index()`'s duplicate-title handling (storing a set of valid pages per title rather than overwriting, to avoid a false TOC-echo flag on a legitimately duplicated section title) — the validation document had zero duplicate titles, so this path is verified by code review only.
(2) `TOC_ZONE_MIN_MATCHES = 5` generalization — validated with a wide margin on one document's structure; other Anthropic system cards or future PDF sources may produce a narrower margin.

**Why This Blocks Progress:**
Does not block current operation. `--no-toc-strip` provides a documented fallback (reverts to the pre-P9 duplication behavior, itself documented as harmless per LL-052) if either gap surfaces as a real defect on a future conversion.

**Deliverable when resolved:** After 2-3 additional system card or TOC-bearing document conversions, confirm no duplicate-title false positive/negative and no threshold near-miss occurred. If confirmed clean, close with a note. If an issue surfaces, log the finding and adjust `TOC_ZONE_MIN_MATCHES` or the duplicate-title logic with a DM entry citing the specific document.

**Resolution:**
—

**References:** DM-122, LL-052, LL-057, pdf_to_markdown.py `build_toc_page_index`, `detect_toc_zone_pages`

---

## IN-023 | Pre-Existing wiki-verify.sh Findings Surfaced by BL-W-01 Execution (Page-Count Drift, Unescaped Dollar Signs)

- **ID:** IN-023
- **Status:** open
- **Priority:** P3
- **Category:** Implementation
- **Raised:** 2026-07-12
- **Resolved:** —

**Question / Gap / Contradiction:**
The BL-W-01 execution report's live `wiki-verify.sh` runs (before and after the
vocabulary.json migration) both show check 5 FAIL (`overview.md`'s `total_pages`
recorded as 197 against an actual count of 198 content pages) and two check-12 WARNs
(unescaped `$` before a digit in two source pages, false-positive-risk severity).
Confirmed identical before and after the refactor, so not caused by BL-W-01 — these are
pre-existing, unrelated drift in the live wiki that nothing has yet resolved.

**Why This Blocks Progress:**
Does not block current operation. Check 5 is a FAIL-severity check (no false-positive
risk per test-harness.md Section 2.3 row 5), so it should not be left indefinitely —
either `overview.md`'s counter needs a routine reconciliation pass or L4c-style
reconciliation logic, or the count discrepancy points to an actual missing/miscounted
page worth investigating.

**Resolution:**
—

**References:** BL-W-01 execution report (Step 9), test-harness.md Section 2.3 rows 5
and 12, wiki-verify.sh.

---

## IN-024 | test-harness.md Section 2.5.2 Still Documents wiki-dashboard.py as a Governed Vocabulary Sync Target (Superseded by DM-123)

- **ID:** IN-024
- **Status:** open
- **Priority:** P3
- **Category:** Tooling
- **Raised:** 2026-07-12
- **Resolved:** —

**Question / Gap / Contradiction:**
Surfaced while executing the BL-W-01 Section 8 batch. test-harness.md Section 2.5.2
(`wiki-dashboard.py` Maintenance) and its "Three-script sync rule" note still describe
`wiki-dashboard.py`, `wiki-lint.py`, and `wiki-verify.sh` as needing vocabulary updates
"in the same delivery batch" — but the Session Instructions' End-of-Chat Ritual step 6
(pre-R-002 gated block) already stated `wiki-dashboard.py` is no longer a governed sync
target, per DM-107 as amended by DM-123. This predates BL-W-01 and is independent of
it: Section 2.5.2 was not updated when DM-123 was adopted.

**Why This Blocks Progress:**
Does not block current operation — no session currently relies on Section 2.5.2 as an
active instruction (BL-W-01's Section 8 batch superseded the *other* two vocabulary
maintenance rows in Section 2.5/2.5.1, which were the live ones). Left as-is, a future
session consulting test-harness.md for `wiki-dashboard.py` maintenance would receive
stale guidance.

**Resolution:**
—

**References:** DM-107, DM-123, test-harness.md Section 2.5.2, Session Instructions
End-of-Chat Ritual step 6 (post-R-002 consolidated vocabulary row).

---

## IN-025 | INIT-PROMPT.md Step 3 (Required Source Files) Omits wiki-lint.py and wiki-verify.sh Entirely

- **ID:** IN-025
- **Status:** open
- **Priority:** P3
- **Category:** Tooling
- **Raised:** 2026-07-12
- **Resolved:** —

**Question / Gap / Contradiction:**
Surfaced while adding `generate-vocab-artifacts.py` to INIT-PROMPT.md Step 3 for the
BL-W-01 Section 8 batch (item 5). Step 3's required-source-files list currently reads
`CLAUDE.md`, `OPERATIONS.md`, `EXTRACTION-SKILL.md`, `TAGGING-SKILL.md`,
`CONTRADICTION-SKILL.md` — it does not mention `wiki-lint.py` or `wiki-verify.sh`
anywhere in the document, despite both being core, load-bearing tooling that a fresh
wiki initialization would need before its first lint or verify pass. This predates
BL-W-01 and appears to be a standing gap in INIT-PROMPT.md's own coverage, not
something this spec introduced or is responsible for closing.

**Why This Blocks Progress:**
Does not block the currently-running wiki (already initialized). Would surface as a
hard blocker on any future from-scratch re-initialization: Phase 2 verification
(`wiki-verify.sh`) and any lint session (`wiki-lint.py`) would fail outright with
neither script present, and INIT-PROMPT.md gives no instruction to obtain them.

**Resolution:**
—

**References:** INIT-PROMPT.md Step 3, wiki-lint.py, wiki-verify.sh,
implementation-handoff.md Phase 1.

---

## IN-026 | OPERATIONS.md Phase 1 Sequence May Be Missing Dedicated L17/L18 Step-Text Blocks (Possible Incomplete BL-W-01 Artifact)

- **ID:** IN-026
- **Status:** open
- **Priority:** P3
- **Category:** Implementation
- **Raised:** 2026-07-12
- **Resolved:** —

**Question / Gap / Contradiction:**
Surfaced in the BL-W-02 execution report's appendix (not a BL-W-02 defect — flagged as
out of that session's scope). Unlike lint Steps L1–L16, the executing agent found no
dedicated "Step L17"/"Step L18" prose blocks in OPERATIONS.md's Phase 1 sequence — only
a passing mention at the vocabulary-expansion procedure ("confirm no L17/L18
findings"). This looks like BL-W-01's own OPERATIONS.md edit (spec Section 4.8, the
Section 11.6 Value-registration block) did not also add step-documentation blocks for
L17/L18 in the Phase 1 step sequence itself, the way L1 through L16 each have one.
Cannot be confirmed against the design project's own OPERATIONS.md copy — it is stale
(06/05/2026, predates the spec) and this session deferred all OPERATIONS.md edits per
LL-040 (see DM-134, DM-136).

**Why This Blocks Progress:**
Does not block current lint operation — the constants are live and L17/L18 findings
are produced and enforced regardless of whether their Phase 1 sequence documentation
is complete. Left unresolved, an agent reading OPERATIONS.md's Phase 1 sequence
top-to-bottom for procedural guidance (rather than relying on tribal knowledge of the
spec) would not find L17/L18 documented at their expected location.

**Resolution:**
—

**References:** BL-W-02 execution report Appendix item 1, vocabulary-json-refactor-spec.md
Section 4.2 (L17/L18 definitions), DM-127, DM-134, DM-136, OPERATIONS.md Section 11.4.

---

## IN-027 | design-project-backlog.md's Status Vocabulary Has No Equivalent to BL-W-series' "planned" for Operator-Gated Items

- **ID:** IN-027
- **Status:** closed
- **Priority:** P3
- **Category:** Process
- **Raised:** 2026-07-12
- **Resolved:** 2026-07-14

**Question / Gap / Contradiction:**
The carry-forward's "Pending executions" table is mandated to enumerate every backlog
item in `planned` status, in either backlog file. `wiki-implementation-backlog.md` uses
`planned` as a real status value (plan exists, execution pending). But
`design-project-backlog.md`'s status vocabulary is only `open | in-progress | done |
dropped` — it has no status distinguishing "blocked on an operator action, otherwise
ready" from ordinary `open`. BL-D-07 (added this session, blocked on the operator
connecting the GitHub connector) is `open` under the current vocabulary, so a literal
reading of the Pending Executions mandate — which scans for the string `planned` — would
never surface it, even though it is functionally identical to a BL-W `planned` item:
specified, not yet actionable, waiting on a discrete external step.

**Why This Blocks Progress:**
Does not block BL-D-07 itself — this session's carry-forward will surface it by name
regardless. It is a gap in the *mechanical* guarantee: a future session drafting a
carry-forward by literal rule-following (scan for `planned`) could miss an
operator-gated BL-D item the same way LL-063 documents happening to a BL-W item this
session, and for a structurally different reason (vocabulary mismatch, not recall
error).

**Resolution:**
Closed by DM-144. `design-project-backlog.md` adopts the same six-value status set as
`wiki-implementation-backlog.md` — `open | planned | in-progress | gated | done |
dropped` — so an operator-gated, otherwise-ready BL-D item is marked `planned` (or
`gated` when blocked on a named trigger) and is caught by the Pending-Executions mandate's
literal `planned` scan exactly as a BL-W item is. The vocabulary mismatch that made BL-D-07
invisible to that scan no longer exists. No Session Instructions change was required (the
mandate already reads "either backlog file"). Note: the lowercase canonical means the
in-file `Status:` template-header casing (`OPEN | PARTIAL | CLOSED`) and legacy entries
across the logs are now stale; their normalization is BL-D-03, not this entry.

**References:** LL-063, DM-144, design-project-backlog.md (status vocabulary), BL-D-03,
BL-D-07, DM-138, wiki-implementation-backlog.md.

---

## IN-028 | DM-040 Status/Superseded-By Mismatch — Marked ACTIVE But Carries a Superseded-By Pointer

- **Status:** closed
- **Priority:** P3
- **Category:** Process
- **Raised:** 2026-07-15
- **Resolved:** 2026-07-25

**Question / Gap / Contradiction:**
DM-040 ("CLAUDE.md Splitting Deferred") carries `Status: ACTIVE` alongside a `Superseded By: DM-061` pointer. Per the coupling rule (DM-121; enforced by `gov_lint.py` Check C), a `Superseded By` pointer should only appear on an entry whose `Status` is `superseded`. Discovered by `gov_lint.py`'s first real-corpus run (BL-D-02, this session), not by manual inspection.

**Why This Blocks Progress:**
Does not block current design work. Blocks a clean first `gov_lint.py` run in the sense that it's a genuine Check C failure the tool will keep reporting until resolved — relevant scope for BL-D-03, which already exists to consume `gov_lint.py`'s Check B/F output; this adds a Check C item to that same cleanup pass.

**Resolution:**
Resolved 2026-07-25 as part of BL-D-03's execution (DM-149). DM-061's content was
checked directly: it explicitly states `Supersedes: DM-040` and replaces DM-040's
"no split, ever" decision with "split planned, deferred to a 3,000-line trigger" — a
genuine reversal, not a spurious pointer. DM-040's `Status` corrected to `superseded`.
`gov_lint.py` Check C now passes clean on this entry.

**References:** DM-040, DM-061, DM-121, BL-D-02, BL-D-03.

---

## IN-029 | gov_lint.py Actual Size (~640 Lines) Exceeds gov-lint-spec.md's Revised Estimate (~150–200 Lines) by ~3x — Unconfirmed Whether Acceptable

- **Status:** open
- **Priority:** P3
- **Category:** Tooling
- **Raised:** 2026-07-15
- **Resolved:** —

**Question / Gap / Contradiction:**
`gov-lint-spec.md` Section 5 estimated ~150–200 lines (already a revision upward from BL-D-02's original ~50–100 estimate, per DM-144). The delivered script is closer to ~640 lines of actual code (excluding blank lines, comments, and docstrings). The delta is attributable to real functionality — per-log required-field schemas, header-name-driven (not hardcoded-position) backlog table parsing, and specific, actionable error messages — not padding, but this has not been reviewed or accepted by the operator the way DM-144's earlier deviation was.

**Why This Blocks Progress:**
Does not block use of the tool (it runs correctly; see BL-D-02). Open question is whether the operator wants it trimmed (at some cost to parsing robustness or message specificity) or accepts the size as the real cost of the six-check design.

**Resolution:**
—

**References:** BL-D-02, gov-lint-spec.md, DM-144, DM-145.

---

## IN-031 | Unexplained Root-Owned Artifacts Appeared in the Sandbox Working Directory Mid-Session — Provenance Unconfirmed

- **Status:** open
- **Priority:** P3
- **Category:** Process
- **Raised:** 2026-07-17
- **Resolved:** —

**Question / Gap / Contradiction:**
During the 2026-07-17 session, two artifacts appeared in the advisor's sandbox that no tool call in the visible session record created, both owned by `root` while the advisor's writes run as user `claude`: (1) a file `session-instructions-R-006.md` (65,082 bytes, internal stamp `07/17/2026 16:45 ET`) in the staging directory, and (2) a complete `DM-148` entry appended to the staged `decisions_made.md`, caught by `gov_lint.py` Check A as a duplicate ID when the advisor appended its own DM-148. Both artifacts' content was benign and traceable to the session's own operator-approved plan: faithful R-005 reproduction plus exactly the planned edits, wording matching the advisor's earlier in-chat plan text, and lacking the external clock cross-check layer added later in the session. Both internal stamps fall inside a confirmed ~4-hour real-time gap between operator turns. Leading hypothesis: an aborted prior execution attempt of the same turn (retry infrastructure) left its outputs behind, with `root` ownership reflecting a different execution context. Open question: what created them, and can sandbox working directories be assumed single-writer within a session?

**Why This Blocks Progress:**
Does not block current work — both artifacts were quarantined, the delivered files were authored independently from in-context sources, and diffs against the quarantined copies confined all differences to the intended edit regions (incidentally corroborating transcription fidelity of the R-005 reproduction). The open risk if unresolved: staged files cannot be assumed to contain only this session's edits, so silent foreign content could ride into a delivery. Interim guards now in practice: (a) before delivering, confirm staged content traces to tool calls in the visible session record; (b) run `gov_lint.py` on the staged corpus — its duplicate-ID and max-ID checks mechanically catch foreign appends to the logs; (c) rebuild from the last delivered snapshot when in doubt. Close if the aborted-retry explanation is confirmed (recurrence with the same benign signature, or documented platform behavior). Escalate to an integrity incident if an unexplained artifact ever appears whose content is *not* traceable to the session's own plan.

**Resolution:**
—

**References:** DM-148, LL-068, LL-066, gov-lint-spec.md (Check A).
