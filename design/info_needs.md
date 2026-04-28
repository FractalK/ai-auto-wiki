# Information Needs

Authoritative repository of open questions, data gaps, and contradictions that must
be resolved before dependent design or implementation work can proceed.

Reference format from other documents: `# See IN-NNN`

**Mutability rules:**
- Open and partial entries are updated in place.
- Closed entries are append-only: resolution is added; no other content is changed.
- Entries are never deleted. If a gap proves to be a non-issue, close it with an explanation.

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

- **Status:** OPEN | PARTIAL | CLOSED
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

- **Status:** CLOSED
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

- **Status:** CLOSED
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

- **Status:** CLOSED
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

- **Status:** CLOSED
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

- **Status:** CLOSED
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

## P3 — Informational Gaps

## IN-006 | Scale Threshold for Index-Only Navigation Not Established

- **Status:** OPEN
- **Priority:** P3
- **Category:** Architecture
- **Raised:** 2026-04-14
- **Resolved:** —

**Question / Gap / Contradiction:**
At what wiki size does index.md-based navigation become insufficient, and what is the recommended escalation path?

**Why This Blocks Progress:**
Does not block initial schema design. Frontmatter and tagging conventions are already designed to accommodate a future search layer without revision. The `summary` field (DM-027) directly improves future search quality. Quartz native search (Ctrl+K) is the baseline and is adequate up to approximately 150–200 pages. qmd hybrid search (BM25/vector, MCP server available) is the recommended escalation path — compatible with existing frontmatter without schema revision. Resolve this entry before the wiki approaches 150 pages.

**Resolution:**
—

**References:** IN-002, DM-027

---

## IN-007 | Query Nomination Queue Scalability at Scale

- **Status:** CLOSED
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

- **Status:** CLOSED
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

- **Status:** CLOSED
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

- **Status:** CLOSED
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

- **Status:** CLOSED
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

- **Status:** CLOSED
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

- **Status:** CLOSED
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

- **Status:** CLOSED
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

- **Status:** OPEN
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
- **Status:** open
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
—

**References:** FRIC-031, DM-072
