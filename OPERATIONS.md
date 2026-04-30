# OPERATIONS.md — Wiki Operational Workflows
**Last Updated:** 30/04/2026 15:30

**Document status:** Companion to CLAUDE.md. Both files must be loaded at the start of
every wiki maintenance session.
**Authority:** CLAUDE.md governs schema, page types, frontmatter, controlled vocabularies,
and the Teaching Index. This document governs all operational procedures: source
classification, ingest workflow, discovery pass, lint procedure, and query workflow.
When this document conflicts with CLAUDE.md on a schema question, CLAUDE.md takes
precedence. For operational procedure questions not covered in CLAUDE.md, this document
is authoritative.
**Portability note:** Same environmental assumptions as CLAUDE.md. See portability-review.md
for the full checklist.

---

### 11.1 Source Classification Taxonomy

Nine confirmed source types with extraction depth and credibility tier assignment:

| Source Type | Extraction Depth | Credibility Tier |
|---|---|---|
| `research-paper` | `full` | peer-reviewed / institutional / practitioner (per logic below) |
| `industry-blog` | `standard` | institutional / practitioner |
| `white-paper` | `full` | institutional / practitioner |
| `publication-article` | `standard` | institutional / practitioner / community |
| `youtube-video` | `standard` | institutional / practitioner |
| `podcast-transcript` | `standard` | institutional / practitioner |
| `practitioner-reference` | `standard` | practitioner always |
| `vendor-content` | `standard` | practitioner always + vendor_bias flag |
| `policy-document` | `full` | institutional always |

**Credibility tier assignment logic:**

`research-paper`:
- Venue matches peer-reviewed list (NeurIPS, ICML, ICLR, ACL, EMNLP, AAAI, JMLR,
  Nature, Science, PNAS) → `peer-reviewed`
- No venue match but affiliated with recognized AI lab (Anthropic, OpenAI,
  DeepMind/Google, Meta AI, Microsoft Research, MIRI, ARC, Apollo, NIST, UK AISI,
  DSIT) → `institutional`
- Otherwise → `practitioner`
- Tie-break: uncertain between peer-reviewed and institutional → assign `institutional`

`industry-blog`:
- URL domain matches: anthropic.com, openai.com, deepmind.google, ai.meta.com,
  research.google, microsoft.com/research, miri.org → `institutional`
- All other domains → `practitioner`

`white-paper`:
- Publishing org is research-primary (AI lab, government, standards body,
  intergovernmental) → `institutional`
- Publishing org is vendor, consulting firm, industry association → `practitioner`
- Ambiguous → `practitioner`
- Never assign `peer-reviewed` to white papers

`publication-article`:
- Outlet matches: Nature, Science, MIT Technology Review, The Atlantic, Wired,
  Financial Times, The Economist → `institutional`
- Byline or URL signals opinion/contributed content → `community`
- All other outlets → `practitioner`

`youtube-video`:
- Channel is official AI lab or research institution → `institutional`
- All other channels → `practitioner`

`podcast-transcript`:
- Show is produced by or features an official AI lab or research institution as primary
  host → `institutional`
- All other shows → `practitioner`
- `transcript_file` is required (same as youtube-video); the transcript is the ingested
  artifact, not an audio or video file
- If only a partial transcript is available, note in the source page body and apply
  standard extraction depth to the available text

`vendor-content`:
- `practitioner` always
- Set internal flag `vendor_bias: true` — apply bias annotation to Key Claims touching
  competitive landscape, capability comparisons, or limitations:
  "(vendor-sourced — treat comparative claims with caution)"

**Institutional tier lists are controlled.** Do not extend them unilaterally.
Extensions require a schema revision and a DM entry.

**PDF handling:** For any source ingested as a PDF, check extraction quality on the
first 500 words before proceeding. If more than 10% of words are non-dictionary strings
or contain encoding artifacts, stop and surface to the human with the specific symptom.
When both HTML and PDF versions exist, prefer HTML. For research papers, check
`arxiv.org/html/{id}` before falling back to PDF.

### 11.2 Ingest Workflow

**Interaction model:** The ingest workflow runs in two phases. Phase 1 (pre-flight) runs
all classification, detection, and decision identification steps without touching any
wiki files. It produces a consolidated pre-flight report of all decisions requiring
human input, presented as numbered forced choices. The human responds with a decision
string (e.g., `1:A 2:C 3:B`). Phase 2 (execution) runs fully automated after all
decisions are resolved.

**Source intake mechanisms:**
- Local files: place in `raw/staged/`; processed in order during batch ingest
- URLs: append to `raw/queue.md` (synced across machines via git); Claude Code fetches
  content during ingest
- YouTube: paired transcript file required in `raw/staged/` alongside video metadata;
  transcript extraction tool to be confirmed at implementation time
- URL fetch failures: move the entry from `## [queued]` to `## [processed]` in
  `raw/queue.md`, appending `fetch-failed: YYYY-MM-DD` to the entry line. Do not
  attempt alternative retrieval — no web search, no cached versions, no mirrors.
  Surface all fetch failures in the post-ingest summary Notes field. If the content
  is still needed, the human will obtain it manually and place a file in `raw/staged/`.

**Pre-flight pass (Phase 1 — no wiki files written):**

Step 0 — Pre-ingest budget check

**Operation mode:** The ingest operation mode is specified in the session prompt as one
of three values. Read the mode before counting sources:

- `INGEST-STAGED` — process only files currently in `raw/staged/`. Set N = (a), where
  (a) = count of files returned by `ls raw/staged/` via bash. Do not read `raw/queue.md`.
- `INGEST-QUEUE` — process only items in the `[queued]` section of `raw/queue.md`.
  Set N = (b), where (b) = count of items in `[queued]`. Do not read `raw/staged/`.
- `INGEST-BOTH` — process both locations. Set N = (a) + (b).

If the operation mode is absent or cannot be determined from the session prompt, stop
and report: "Operation mode not specified. Reply with INGEST-STAGED, INGEST-QUEUE, or
INGEST-BOTH to proceed." Do not guess.

If N ≤ 5: proceed to Step 1 without surfacing a forced choice — a session of this size
is safe on Pro tier at any hour.

If N > 5: run `date` via bash to determine current local time. Convert to PT and
determine whether the session falls in peak hours: 05:00–11:00 PT (13:00–19:00 GMT).
Surface the following forced choice block:

```
Pre-ingest check: {N} items in this session ({scope description}).

Session budget note: Claude Code Pro tier operates on a 5-hour session window. During
peak hours (05:00–11:00 PT / 13:00–19:00 GMT), that window yields less work than
off-peak. Current time: {HH:MM PT} — {PEAK | OFF-PEAK}.

Reliable batch for Pro tier: 3–5 documents per session. Processing large batches risks
hitting the session limit mid-ingest, which halts work without a clean checkpoint.
Documents not processed in this session remain in [queued] and staged files remain in
raw/staged/ — per-document git commits ensure no completed work is lost.

{If PEAK — include:}
Running a large batch during peak hours will exhaust your session budget faster than
usual. Deferring to off-peak hours (after 11:00 PT / 19:00 GMT) is recommended.

Select a processing option:

A) Process first 5 documents [recommended — safe at any hour]
B) Process first 10 documents [higher risk; viable off-peak for short documents]
C) Process all {N} documents [expect to need multiple sessions or a mid-session reset]
D) I will specify which documents to process: ___
E) Defer — abort ingest now and save queue state for next session
```

Where `{scope description}` is:
- INGEST-STAGED: "{N} staged files"
- INGEST-QUEUE: "{N} queued URLs"
- INGEST-BOTH: "{a} staged files + {b} queued URLs"

**If option E is selected:**
- Make no changes to any wiki file, to `raw/queue.md`, or to files in `raw/staged/`.
- Write `raw/deferred-ingest.md` with the following content:

```markdown
---
type: deferred-ingest
created: {YYYY-MM-DD HH:MM PT}
---

## Deferred Ingest — Resume Next Session

{N} items were ready for ingest at time of deferral ({a} staged files + {b} queued
URLs). No processing occurred.

Recommended timing: off-peak (after 11:00 PT / 19:00 GMT on weekdays).

To resume: start a new wiki session and tell Claude Code:
"Resume deferred ingest per raw/deferred-ingest.md."

## Queued Items at Deferral

{verbatim list from queue.md [queued] section at time of abort}
```

- Commit `raw/deferred-ingest.md` to git with message: `chore: save deferred ingest state`.
- Report to the human: "Ingest aborted. {N} items ready ({a} staged + {b} queued).
  Deferral note written to raw/deferred-ingest.md. Recommended: resume off-peak
  (after 11:00 PT / 19:00 GMT)."
- End session. Do not proceed to Step 1.

**If options A–D are selected:** proceed to Step 1 with the selected document scope.
Documents outside the selected scope remain in `[queued]` unchanged.

**On resumption after a deferral:** At session start, if `raw/deferred-ingest.md` exists,
the agent reads it and reconciles its queued-items list against the current state of
`raw/queue.md`. If they match: confirm the queue and proceed to Step 0 budget check for
the current session. If `raw/queue.md` has changed since deferral (items added, removed,
or promoted), surface the discrepancies before proceeding. Delete `raw/deferred-ingest.md`
after the ingest session that clears the deferred items completes successfully.

Step 1 — Receive source and determine ingest scope
- INGEST-STAGED: process files from `raw/staged/` only; do not access `raw/queue.md`
- INGEST-QUEUE: process items from `raw/queue.md` [queued] section only; do not access `raw/staged/`
- INGEST-BOTH: process `raw/staged/` files first, then `raw/queue.md` URLs, treating all as a single ordered batch
- Ad-hoc: process single source provided directly in session (not from filesystem)
- YouTube without transcript: stop and request transcript before proceeding

Step 2 — Duplicate detection
- Check `sources/` for URL match (exact) and title match (near-duplicate)
- Exact URL match, `status: retracted` or `ingested-in-error`: stop, report to human,
  do not proceed
- Exact URL match, `status: active`: surface as forced choice in pre-flight report:

  ```
  [N] Duplicate URL detected: [[{existing-source-slug}]] (ingested {YYYY-MM-DD})
      A new staged file matches this source's URL. Options:
      A) Abort — discard staged file, retain existing source as-is
      B) Enrich — re-extract from richer version; update downstream pages;
         preserve existing Key Claims on downstream pages unless superseded
  ```

  If A selected: discard staged file, do not proceed with this source.
  If B selected: execute Step 2a before Step 3; skip Step 10.

- Near-duplicate: add to pre-flight report as forced choice
- No match: proceed

Step 2a — Source enrichment execution (Path B only — execute when Step 2 forced choice
resolved B; skip otherwise)

1. **Source page frontmatter update:** Set `updated` to today. Add `enriched: YYYY-MM-DD`
   (today's date) to the Source page frontmatter. Do not change the source slug, the
   `ingested_date`, or any other immutable field.
2. **Classification already established:** Skip Steps 3–5. Source type, credibility tier,
   and model/application class are carried from the existing Source page frontmatter
   unchanged.
3. **Pre-flight continues from Step 6:** Proceed with Steps 6–9 (affected page
   identification, comparison proposal, teaching relevance, decay_exempt) using the
   richer file as the extraction basis.
4. **Skip Step 10:** Do not create a new Source page.
5. **Downstream deduplication rule (applies during Steps 11–13):** Before running the
   contradiction protocol on a newly extracted claim, apply this check: if an existing
   Key Claim on the target page cites this source slug and is substantively identical in
   meaning to the newly extracted claim, skip that claim silently — do not add a
   duplicate row, do not surface a forced choice. "Substantively identical" means the
   same assertion about the same entity; minor wording differences do not make claims
   distinct. Only claims that are genuinely new or that contradict an existing claim
   proceed through Steps 14–18 as normal.
6. **Staged file disposal:** Rewrite the source page summary paragraph from the richer
   extraction per Section 5.4. Then move the richer file from `raw/staged/` to
   `raw/processed/`. Preserve the original filename.
7. **Commit message:** `enrich: {source-slug} — richer source version ingested`

Step 3 — Source type classification
- Apply nine-type decision tree (Section 11.1) in order
- Ambiguous classifications: add to pre-flight report as forced choice

Step 4 — Credibility tier assignment
- Apply tier logic (Section 11.1) — fully automated, no human input

Step 5 — Model-class / application-class classification (Tool sources only)
- Apply classification decision logic (Section 9)
- Ambiguous classifications: add to pre-flight report as forced choice

Step 6 — Identify affected wiki pages
- For each entity in extraction: search index.md for existing page
- New entity warrants a stub page only if source dedicates at least one substantive
  paragraph to it — not a passing mention
- Page type ambiguities: add to pre-flight report as forced choice
- Establish final update list: existing pages to update, new pages to create

Step 7 — Comparison page proposal (conditional)
- If source contains structured multi-criteria comparison, benchmark results across
  named models, or explicit multi-dimensional argument for one approach over another:
  propose Comparison page creation as forced choice in pre-flight report
- Single-criterion comparisons and passing mentions do not qualify

Step 7a — Pitfalls page proposal (conditional)
- Threshold: source must contain at least one failure mode with sufficient detail to
  populate a named `### [Failure mode name]` entry with a `**Status:**` designation.
  Passing mentions of limitations without a nameable failure mode do not qualify.
- If threshold is met: identify the parent entity (Topic or Tool) and determine whether
  a Pitfalls page for that entity already exists in index.md.
  - If no Pitfalls page exists: propose creation as forced choice in pre-flight report.
  - If a Pitfalls page exists: propose updating it as forced choice in pre-flight report.
- Apply routing rule before proposing: if the failure mode is cross-cutting (not specific
  to a single tool), route to the Topic-scoped parent entity's Pitfalls page, not the
  Tool Pitfalls page. Do not duplicate cross-cutting antipatterns across multiple Tool
  Pitfalls pages.
- Multiple parent entities with qualifying failure mode content: surface one forced
  choice per entity.

```
[N] Pitfalls page {proposed | update proposed}: [[{parent-slug}]]
    Failure mode(s) extracted: {N} — {one-line names}
    Routing: tool-scoped | topic-scoped (cross-cutting)
    A) {Create | Update} Pitfalls page
    B) Skip — do not create or update
```

Step 8 — Teaching relevance proposal
- For each new or substantially revised page: evaluate against threshold (Section 7.3)
- Qualifying pages: add to pre-flight report as forced choice with proposed domains

Step 9 — decay_exempt proposal
- For each existing Key Claim meeting all three criteria (definitional, no prior
  contradiction, ≥2 independent peer-reviewed or institutional sources): propose
  `decay_exempt: true` as forced choice in pre-flight report

**Pre-flight report format:**

```
Pre-flight report — {source title}
{N} decisions require your input. Respond with: 1:A 2:B ...

[1] {decision description}
    A) {option}
    B) {option}
    C) {option if applicable}
...
```

**Execution pass (Phase 2 — wiki files written):**

Step 10 — Create Source page
- Generate filename slug: 4–6 meaningful words, stopwords stripped, year prefix
- Verify uniqueness before writing; surface collision to human if found
- Populate all required frontmatter; set `status: active`
- Set `ingest_via` to `queue` or `staged` per the intake mechanism used for this source
- Leave `superseded_by` absent (not blank)
- Write a summary paragraph immediately below the frontmatter block per Section 5.4

Step 11 — Extraction pass
- `full` depth: section-by-section; extract claims, evidence, quantitative findings,
  named entities, explicit contradictions per source structure
- `standard` depth: source as unit; central argument, up to 5 supporting claims,
  quantitative findings, named entities
- PDF quality check before extraction (Section 11.1)
- `vendor_bias` flag applied during extraction for vendor-content sources
- **Image handling (full-depth sources only):** When a full-depth source contains inline
  images, fetch and view any figure that is visually referenced by the surrounding text
  and is not purely decorative (headers, logos, and layout images are decorative). If a
  figure contains quantitative data or structural information not captured in the
  surrounding prose — benchmark charts, training curves, architecture diagrams — write a
  one-sentence description of the figure's key content in the target wiki page body at
  the point where the source references it. Do not store image files locally. Skip this
  step for standard-depth sources entirely.
- Extraction output is internal working list — not filed as wiki artifact

Step 11a — Citation harvesting
- Scan the extracted source for outbound links and bibliographic citations to sources
  with `credibility_tier: peer-reviewed` or `institutional`.
- For each candidate: the citation must resolve to a valid URL in the source text.
  Bibliographic references without a resolvable URL are excluded — slug matching
  against existing sources/ is unreliable without a canonical URL.
- For each URL-resolvable candidate: check `sources/` for an exact URL match.
  Also check `raw/queue.md` `[nominated]` and `[stale-nominated]` sections for a URL
  match — if found in either, skip (do not create a duplicate entry).
  If absent: append to `raw/queue.md` under `[nominated]` in the following format:
  `{title} | {url} | {source_type} | {credibility_tier} | nominated: {YYYY-MM-DD} [nominated — cited by [[source-slug]]]`
- Do not surface citation nominations as forced choices during the ingest pre-flight.
  They enter the nominated queue and are reviewed through the normal promotion mechanism
  at the next discovery pass or on-demand queue review.
- Apply the same credibility filter used by the discovery pass: institutional-tier
  sources only. A practitioner source citing other practitioner sources produces
  zero nominations.

Step 12 — Update or create Topic pages
- Prose: rolling overwrite, present tense, 600–800 word target, 1,200 word ceiling
- Key Claims: maintain 3–5; contradictions trigger three-path protocol (Section 8)
- Frontmatter: increment source_count, set updated and last_assessed to today,
  upgrade stub→developing if applicable, never upgrade to current during ingest;
  assign technical_depth if not already set
- Self-check before writing (Section 6.1)
- New stub pages: 1–3 Key Claims, 2–4 sentence prose opening, status: stub

Step 12a — Teaching notes assessment (Topic pages with teaching_relevance: true)

For each Topic page touched in Step 12 where `teaching_relevance: true`:

**If no `## Teaching Notes` section exists:** Write it now using the Topic/Tool variant
from CLAUDE.md Section 5.2. Set `teaching_notes_reviewed` to today.

**If `## Teaching Notes` already exists:** Apply the substantiality threshold. Assess
whether the new Key Claims state, taken as a whole, materially changes what a reader
of the existing notes would conclude. Do not reference the notes structurally — assess
holistically. The threshold is met when:
- (a) a Key Claim on this page has its status changed to `superseded` or `contested`; or
- (b) a new Key Claim is added covering a dimension fundamentally different from anything
  currently addressed in the notes.

Below the threshold (source_count increments, additional supporting sources, prose
wording refinements — core synthesis unchanged): no action. The existing notes remain
valid.

If the threshold IS met: generate a recommended replacement for the `## Teaching Notes`
section. Surface as a forced choice in the post-ingest summary (Section B):

```
[N] Teaching notes may be outdated: [[page-slug]]
    Substantiality trigger: [one sentence — what changed]
    Proposed replacement: [agent-generated teaching_notes text]
    A) Confirm replacement — apply as written; update teaching_notes_reviewed to today
    B) Confirm with edits — I will amend before applying
    C) Dismiss — existing notes remain; do not update teaching_notes_reviewed
```

**Derived-from ripple check (after teaching notes assessment):** Scan `teaching/` for
any teaching-brief page whose `derived_from` list includes a full-path wikilink to this
Topic or Tool page. For each match where the constituent page's `last_assessed` is being
set to today (i.e., substantively updated in this ingest pass): assess whether the
substantiality threshold is met for the teaching-brief. If so, queue a forced choice in
post-ingest summary Section B using the lint Step L5 teaching-brief forced choice format.
This check runs after both Step 12a and Step 13b; any matching teaching-brief pages are
surfaced once regardless of how many constituent pages were updated.

- Self-check before writing (Section 6.1)
- New stub pages: 1–3 Key Claims, 2–4 sentence prose opening, status: stub

Step 13 — Update or create Tool/Product pages
- Same prose, Key Claims, and frontmatter logic as Step 12
- Additional: update capabilities and limitations lists (one clause per item, no
  duplicates, remove superseded items)
- Version handling per Section 9

Step 13b — Teaching notes assessment (Tool pages with teaching_relevance: true)

Identical procedure to Step 12a. Apply to each Tool page touched in Step 13 where
`teaching_relevance: true`. Use the Topic/Tool variant from CLAUDE.md Section 5.3.

Step 13a — Create or update Pitfalls page (if confirmed in pre-flight Step 7a)
- Apply full Section 5.6 spec: three mandatory H2 sections in order
  (`## Technical Limitations`, `## Usage Antipatterns`, `## Alignment and Safety Concerns`),
  failure mode heading format, `**Status:**` field on the line immediately following
  each `### [Failure mode name]` heading, `**Source:**` field on the line immediately
  following `**Status:**`
- **Self-check before writing any failure mode entry:** Every `**Status:**` line
  must end with `<br>` — e.g., `**Status:** active<br>`. Quartz (CommonMark) does
  not treat a single newline as a hard line break; without `<br>`, Status and Source
  collapse onto one rendered line. Verify this on every entry written, including
  entries added to existing pages. (CLAUDE.md Section 5.6; FRIC-030)
- Routing rule applies: cross-cutting antipatterns go to Topic-scoped Pitfalls pages;
  do not create a Tool Pitfalls page for a cross-cutting failure mode
- New Pitfalls page: populate `parent_entity` with full-path wikilink to parent;
  set `parent_type`, `status: current`, `failure_mode_count` to count of H3 entries written
- Existing Pitfalls page: add new failure mode entries to the appropriate section(s);
  do not duplicate entries already present; update `failure_mode_count` and `updated`
- After writing all failure mode entries (new or updated page): reconcile the
  `contributing_sources` frontmatter list to reflect all unique source slugs cited
  across all `**Source:**` lines on the page. Add any new slug; do not remove existing
  slugs — a source that contributed entries remains on record even if its specific
  entries are later edited.
- Add new Pitfalls page to index.md under `## Pitfalls` section in the same pass

**Pitfalls teaching notes addendum (conditional):** After the failure mode entries are
written, if the Pitfalls page has `teaching_relevance: true`, apply the substantiality
threshold from Step 12a. For Pitfalls pages, weight the **Representative example**
subsection heavily — it is the most likely component to be compromised by page updates
(new failure modes that supplant or nuance the existing example). Use the Pitfalls
variant from CLAUDE.md Section 5.6. Surface as a forced choice in the same format as
Step 12a using the post-ingest summary Section B.

Step 14 — Handle contradictions
- Apply three-path protocol (Section 8) for all contradictions detected in Steps 12–13
- Path B flags and Path A auto-resolutions on current pages: surface in post-ingest summary

Step 15 — Create Comparison page (if confirmed in pre-flight)
- Populate full frontmatter, set status: current
- Add to index.md in same pass

Step 16 — Update index.md
- Add new Source page to Sources section
- Add new Topic, Tool, Comparison, Pitfalls pages with one-line summaries (Pitfalls: parent entity name)
- Update summaries for substantially revised pages
- Do not list deprecated Tool pages

Step 17 — Update overview.md counters
- Increment total_pages by count of new pages; increment total_sources by 1
- Set updated to today

Step 18 — Append log.md entry

```
## [{today}] ingest | {source title}
Added: [[{source-slug}]]. Updated: [[page-1]], [[page-2]]. Contradictions flagged: {N}.
Auto-resolved: {N}. New pages created: {N}.
  Contradiction: [[{page-slug}]] — {one-sentence claim summary}
```

Step 19 — Regenerate Teaching Index (if any tagged page touched)

Step 20 — Spot-check output (peer-reviewed and policy-document sources only)
- Output spot-check block in post-ingest summary (Section 6.5)

Step 21 — Stage wiki-lessons-learned.md draft entry (if any human override occurred)
- Draft entry for human confirmation in post-ingest summary

Step 21a — Skill enrichment nomination (after Steps 20–21)
- For the skill file(s) used in this ingest operation (always EXTRACTION-SKILL.md;
  TAGGING-SKILL.md if teaching relevance was evaluated; CONTRADICTION-SKILL.md if any
  contradiction was encountered): scan the TO BE ENRICHED sections.
- For each placeholder section: assess whether the case just processed represents a
  genuinely novel example — a failure mode variant, boundary condition, or edge case not
  already covered by existing examples in that section. The test: would this example
  teach Claude Code something the existing examples do not?
- If yes: draft the proposed addition language. These drafts are held and assembled into
  Section B of the Step 22 summary, where they receive PS-N labels in sequence. Do not
  output them separately before Step 22.
- If no genuinely novel cases exist: omit this block entirely. Do not nominate
  additional instances of cases already illustrated.
- Write confirmed enrichments to the skill file immediately, replacing the TO BE ENRICHED
  placeholder text for that section (or appending to an already-partially-populated
  section). Append a `skill-enrichment` log entry.

Step 22 — Post-ingest summary

Output in two sections. Do not interleave informational lines with forced choices.

**Section A — Session Summary**

```
Source ingested: {title} ({source_type}, {credibility_tier}, {extraction_depth})
New pages created: {N} — {wikilinks}
Pages updated: {N} — {wikilinks}
Auto-resolved contradictions: {N} — {list: page + old claim + new claim, or "none"}
  [Pages with status: current listed prominently]
Contradictions flagged for review: {N} — {list: page + claim + override window close date}
Comparison pages proposed: {confirmed/declined}
Teaching Index regenerated: yes | no
Spot-check: [block if applicable]
Lessons learned draft: [entry if applicable]
Items requiring human review: {list or "none"}
Notes: [fetch failures, remediation notes, or other session observations; omit if none]
```

**Section B — Decisions Required**

Omit this section entirely when there are zero forced choices. When present, open with
the response format line, assign PS-N labels sequentially (citations first, then skill
enrichment candidates in the order Step 21a drafted them), and list each item in full.

```
Respond with: PS-1:X PS-2:X ... for each item below.

PS-1 Citations nominated: {count} — from [[source-slug]]
  {title} | {url}
  ...
  A) Leave in queue — nominations remain for query-time surfacing
  B) Dismiss all nominations from this source — remove from queue.md now

PS-{N} Skill enrichment candidate: {skill-file}.md § {section number and title}
  Case: [one-sentence description of what was encountered]
  Proposed addition: [drafted example text]
  A) Confirm — write to skill file
  B) Confirm with edits — I will amend before you write
  C) Discard
```

Omit the citations PS item when Step 11a produces zero nominations. Omit skill
enrichment PS items when Step 21a produces no novel cases. If only one type of forced
choice is present, start numbering from PS-1. Option B on citations removes all
nominations from this source from queue.md immediately. Option A requires no action —
nominations remain in the `[nominated]` section and surface via query-time matching
(Step Q2a) if a relevant sparse or shallow result occurs.

Step 22a — Session stats log entry

After the post-ingest summary (Step 22), append a `session-stats` entry to `log.md`.
Write this entry last, after all other log writes for the session are complete.

```
## [{YYYY-MM-DD HH:MM PT}] session-stats | ingest
Queue size at session start: {N}
Documents attempted: {M}
Documents completed: {K}
Session limit hit: yes | no
Time window: peak | off-peak
Source type mix: {source_type: count, source_type: count, ...}
Approx tokens (from /cost): ~{N,NNN} input / ~{NNN} output
Notes: {optional — e.g., "halted at doc 7, resumed next session"}
```

Run `/cost` in the Claude Code terminal immediately before writing this entry to
capture the token figures. If `/cost` is unavailable or returns no data, omit the
tokens line rather than fabricating a value.

If the session halts mid-ingest due to a session limit (without the human selecting
option E at Step 0), write a partial entry immediately before the session ends:
set `session limit hit: yes` and `documents completed: {K}` where K is the count
of documents for which a git commit was successfully made. Documents without a
commit are not counted as completed.

Step 22b — Post-ingest housekeeping

After Step 22a, for each document successfully ingested in this session:

- **Staged source:** Move the processed file from `raw/staged/` to `raw/processed/`.
  Preserve the original filename.
- **Queue URL source:** In `raw/queue.md`, move the entry from `## [queued]` to
  `## [processed]`, appending `processed: YYYY-MM-DD` to the entry line.

Do not run this step for documents that did not complete (no git commit made). Those
sources remain in `raw/staged/` or `## [queued]` for the next session.

Step 22c — Push to remote

Run `git push origin main`. Commit all changes directly to main — do not create feature
branches or pull requests. The gh CLI is not required for any wiki operation and must
not be used.

### 11.3 Proactive Discovery Pass

Maintain `raw/discovery-sources.md` — a controlled list of feeds to monitor:

```
{url} | {type: arxiv | lab-blog | academic-blog} | {label}
```

Type values: `lab-blog` — commercial AI lab publication (Anthropic, OpenAI, DeepMind,
Meta AI, Microsoft Research). `academic-blog` — academic institution publication
(Stanford HAI, Berkeley BAIR, etc.); processed identically to `lab-blog` (page fetch
and scan for recent items); the distinction is metadata for human curation purposes only.
`arxiv` — requires API integration; deferred. All three types are subject to the
institutional-tier filter at Step 4.

Example:
```
https://www.anthropic.com/news | lab-blog | anthropic
https://openai.com/news/research | lab-blog | openai
https://deepmind.google/discover/blog | lab-blog | deepmind
https://hai.stanford.edu/news | academic-blog | stanford-hai
https://arxiv.org/search/?searchtype=all&query=alignment | arxiv | ai-safety
```

**Discovery pass procedure:**
1. Read `raw/collection-gaps.md` to extract current persistent gap topic tags before
   fetching feeds. This list is used in Step 4 to prioritize nominations.
2. Fetch each feed in discovery-sources.md
3. Identify items published since `last_discovery` date in overview.md
4. Filter: institutional-tier sources only; exclude items already in wiki
5. For each qualifying item, check whether its title or description matches any topic
   tag in the current collection gap list. Annotate matching items:
   `[nominated — matches collection gap: {topic-tag}]`. Non-matching items receive
   the standard `[nominated]` annotation. Also check `raw/queue.md` `[nominated]`
   and `[stale-nominated]` sections for a URL match — if found in either, skip.
6. Append all qualifying items to `raw/queue.md` under the `[nominated]` section,
   gap-matching items first, in the following format:
   `{title} | {url} | {source_type} | {credibility_tier} | nominated: {YYYY-MM-DD} [{annotation}]`
   where `{annotation}` is `nominated — matches collection gap: {topic-tag}` or `nominated`.
7. Update `last_discovery` in overview.md
8. Report nominations to human as forced choices, gap-matching items first:

```
[N] Discovery nomination: {title}
    Source: {url}
    Type: {source_type} | Tier: {credibility_tier}
    Gap match: {topic-tag} | none
    A) Promote to ingest queue
    B) Discard
```

Human-added URLs go directly to `[queued]` section of queue.md. Nominated URLs require
promotion before entering the ingest queue. Claude Code does not ingest nominated sources
without human promotion.

**Note on arXiv:** arXiv does not provide a clean per-institution feed without API
integration. Start with lab blog feeds only. Add arXiv discovery only if lab blog feeds
prove insufficient. This is an implementation decision to revisit at first operation.

### 11.4 Lint Procedure

**Trigger conditions:**
- Scheduled: no minimum cadence enforced by schema. Recommended: every 15–20 new pages
  added, or every two weeks of operation, whichever comes first. The override window for
  Path B contradictions is 7 days; infrequent lint passes extend the effective window.
  Treat lint cadence as a commitment, not a preference.
- On-demand: triggered by human command at any time.
- Automatic (scoped): after any retraction event, a targeted lint pass fires on affected
  Key Claims only — not a full pass.
- Automatic (scoped): when the human sets `status: ingested-in-error` on a Source page,
  the correction procedure in Section 8.6 fires immediately in the same session. This is
  not a lint pass — it is a targeted correction operation triggered by the status change.

**Mandatory triggers (not overridable):**
- Before applying any schema change to the live wiki.
- After any bulk ingest session that processed five or more sources.

**Pre-session habit:** Run `wiki-verify.sh` before every ingest or lint session. The
script completes in under a minute and catches structural drift — missing scaffold files,
ignorePatterns gaps, page count mismatches — before they affect operations. It is
read-only and makes no changes to any file.

**Interaction model:** Lint uses the pre-flight / forced choice model. Phase 1 (assessment
pass) runs all checks without writing wiki files and consolidates findings into a report.
Phase 2 (human response) is skipped if no forced choices are generated. Phase 3 (execution
pass) applies auto-execute actions and confirmed forced choices.

---

#### Phase 1 — Assessment Pass (no wiki files written)

**Step L1 — queue.md scan for CTRD-NNN signals**

Scan `raw/queue.md` for lines matching `CTRD-NNN:(override|confirm)`. For each match:
locate the corresponding entry in `open_contradictions` frontmatter on the affected page
by ID. Record the signal and target page for Phase 3 processing. If a CTRD-NNN value
in queue.md does not match any open entry in any page's `open_contradictions` frontmatter,
flag as informational: "Stale override signal — no matching open contradiction found:
CTRD-NNN."

**Step L1a — Nomination queue aging**

Scan `raw/queue.md` `[nominated]` and `[stale-nominated]` sections. For each item,
read the `nominated: YYYY-MM-DD` date field from the line and compute age in days.

- Items in `[nominated]` with age ≥ 90 days and < 180 days: mark for Stage 1 move
  to `[stale-nominated]` in Phase 3. Record title and age.
- Items in `[stale-nominated]` with age ≥ 180 days: mark for Stage 2 deletion in
  Phase 3. Record title and age.
- Items in either section without a `nominated: YYYY-MM-DD` field (pre-schema entries):
  do not age. Add informational note: "N items have no nominated_date — aging skipped."

No forced choice. Both Stage 1 and Stage 2 are auto-execute in Phase 3. The
informational summary lists all items being moved or deleted; the human can manually
edit `raw/queue.md` before responding to the lint report if they want to rescue an item.

**Step L2 — Page inventory**

Read `index.md` to build the full page inventory. Record total counts by type. Do not
scan the filesystem directly — index.md is the authoritative catalog. Pages present on
disk but absent from index.md are invisible to lint; this is a schema conformance finding
surfaced in Step L11.

**Step L3 — Support score recalculation**

For every Topic and Tool page: read the Key Claims table. For each claim row:
- Skip rows with `[derived]` annotation in the Source field — these use proxy scoring.
- Exclude `[minority view]`-annotated sources from the calculation.
- Sum credibility weights of all remaining sources in the Source field: peer-reviewed=3,
  institutional=2, practitioner=1, community=0.
- For each source, read `published_date` from its Source page. If more than 12 months
  before today, apply 0.5 multiplier to that source's weight before summing.
- If `decay_exempt: true` on the claim, skip decay application.
- Round final score to one decimal place.
- If the new score differs from the current table value, mark the claim for update.

Output: list of pages with changed support scores. Informational only — no forced choice.

**Step L4a — Contradiction flag expiry**

For every page with a non-empty `open_contradictions` list: for each entry where
`override_window_closes` is before today's date AND no CTRD-NNN signal was found for
this ID in Step L1: mark as expired. Apply window-expired-confirmed resolution in
Phase 3. Record under "Expired contradiction flags — auto-confirmed" in lint report.
No forced choice.

**Step L4b — Open contradiction surfacing**

For every page with a non-empty `open_contradictions` list: for each entry where
`override_window_closes` is on or after today's date AND no CTRD-NNN signal was found
for this ID in Step L1: surface as a forced choice. When a claim's Status cell contains
multiple CTRD IDs, surface each as a separate forced choice item.

```
[N] Open contradiction: [[page-slug]] — CTRD-NNN
    Claim: {claim text}
    Contesting source: [[source-slug]] ({credibility_tier}, weight={N})
    Existing support score: {N}
    Window closes: YYYY-MM-DD ({N} days remaining)
    A) Confirm — apply resolution; update claim to reflect contesting source
    B) Override — retain prior claim; treat contesting source as minority view
    C) Skip — no action; override window continues running
```

If the human selects C repeatedly across lint passes, the item continues appearing
until the window expires and L4a auto-confirms it. Repeated C selections are a valid
conscious deferral, not a system error.

**Step L4c — open_contradictions counter reconciliation**

Count the total number of individual entries in `open_contradictions` frontmatter lists
across all wiki pages. Compare this actual count against the `open_contradictions` field
in `overview.md`.

- If the difference is ±1: add to informational summary. Auto-correct in Phase 3 item 11.
  Message: "open_contradictions counter drift: overview.md shows {N}, actual count is {M}
  — off by {diff}. Will auto-correct."
- If the difference is ±2 or more: surface as a forced choice.

```
[N] open_contradictions counter drift: overview.md shows {N}, actual count is {M}.
    A) Correct the counter to {M}
    B) Investigate before correcting — skip counter update this pass
```

- If actual count matches overview.md: add to informational summary as "Counter verified: {N}."

**Step L5 — Staleness checks**

*Topic and Tool pages:* For each page with `status` not `deprecated`: if `last_assessed`
is more than 90 days before today and `status` is not already `stale`: mark for
downgrade to `stale` in Phase 3. Auto-execute. Pages already `stale` noted
informational only.

*Comparison pages:* For each Comparison page: read `entities_compared`. If the
Comparison page's `updated` date is older than any entity page's `updated` date: mark
`status` for downgrade to `stale`. Auto-execute.

*Teaching-brief pages:* For each teaching-brief page: read `derived_from`. If any
constituent page's `last_assessed` date is newer than the teaching-brief's `last_reviewed`
date, mark `status` for downgrade to `stale` and surface as a forced choice:

```
[N] Teaching-brief may be outdated: [[teaching/slug-brief]]
    Constituent page updated: [[derived_from_slug]] (last_assessed: YYYY-MM-DD)
    Teaching-brief last_reviewed: YYYY-MM-DD
    A) Regenerate — agent produces updated draft for review
    B) Mark as reviewed without changes — set last_reviewed to today
    C) Dismiss — leave status: stale for now
```

If A confirmed: agent generates a replacement draft drawing from current `teaching_notes`
and Key Claims of all constituent pages. Human reviews before writing.

**Step L5a — Stale → current upgrade check**

For each Topic or Tool page with `status: stale`, evaluate both conditions:
- (a) `last_assessed` is within 90 days of today
- (b) `open_contradictions` is absent or empty in the page's frontmatter

If both conditions are met: surface as a forced choice.

```
[N] Status upgrade candidate: [[page-slug]]
    Current status: stale
    last_assessed: YYYY-MM-DD ({N} days ago)
    Open contradictions: none
    A) Upgrade to current
    B) Skip — retain stale
```

If only one condition is met: add to informational summary noting which condition is unmet.
If neither condition is met: no action.

**Step L5b — Teaching notes currency check (informational)**

For each page where `teaching_relevance: true` and `teaching_notes_reviewed` is present:
if `teaching_notes_reviewed` is more than 90 days older than `last_assessed`, add to the
informational summary. No forced choice. The ingest-time substantiality check (Steps 12a,
13b, 13a addendum) is the primary sync mechanism; this backstop surfaces pages that have
accumulated substantial assessment activity without triggering an ingest-time check.

If `teaching_notes_reviewed` is absent on a page with `teaching_relevance: true` and
`last_assessed` present: add to informational summary as "teaching_notes section missing —
page is teaching-tagged but no notes have been written."

**Step L6 — Orphan page detection**

For each wiki page excluding singletons and Source pages: check whether any other
non-source page contains a wikilink to this page. Pages with no inbound wikilinks
from non-source pages are flagged as orphans. Informational only — no auto-action,
no forced choice. Listed in lint report for human review.

**Step L7 — Concept gap detection**

Scan prose sections (excluding frontmatter, Key Claims tables, and section headers) of
all Topic and Tool pages. Identify terms appearing in three or more distinct pages with
no corresponding Topic or Tool page in index.md. Filter: exclude proper nouns already
captured as Tool pages under a different slug. Surface candidates as forced choices:

```
[N] Concept gap detected: "{term}"
    Appears in: [[page-1]], [[page-2]], [[page-3]]
    A) Create stub Topic page
    B) Create stub Tool/Product page
    C) Dismiss — term does not warrant its own page
```

Claude Code does not create pages autonomously from concept gap detection. The
three-page threshold is a heuristic — calibrate from operational experience.

**Step L8 — Pitfalls page maintenance**

For each Pitfalls page: count H3 headings with a `**Status:**` field on the immediately
following line across all three mandatory sections. If count differs from current
`failure_mode_count` frontmatter value: mark for update in Phase 3. Auto-execute.
If any mandatory H2 section heading is absent: flag as schema conformance violation
(carries into Step L11).

**Step L9 — decay_exempt proposals**

For each Key Claim where `decay_exempt` is `false` or absent, evaluate all three
conditions:
- (a) Claim is definitional or foundational, not empirical.
- (b) No `contradiction-flag` log entry in log.md references this page and claim.
- (c) Two or more independent supporting sources with `credibility_tier` peer-reviewed
  or institutional.

If all three met, add to pre-flight report as forced choice:

```
[N] decay_exempt proposed: [[page-slug]]
    Claim: {claim text}
    Basis: (a) definitional, (b) no prior contradiction, (c) {N} peer-reviewed/institutional sources
    A) Confirm — set decay_exempt: true
    B) Decline
```

Claude Code does not set `decay_exempt: true` autonomously.

**Step L10 — Teaching Index completeness ratio**

Count Topic and Tool pages where `teaching_relevance: true`. Divide by total Topic and
Tool pages (excluding deprecated Tool pages). If ratio is below 0.20:

```
[N] Teaching relevance ratio below threshold
    Tagged: {N} of {total} Topic and Tool pages ({ratio}%)
    A) Acknowledge — I will review tagging in the next session
    B) Dismiss — low ratio is accurate for this wiki's current content
```

If ratio is at or above 0.20: informational note only.

**Step L11 — Schema conformance check**

Sample all pages with `updated` date after `last_lint` in overview.md. Evaluate each
against:

| Criterion | Check |
|---|---|
| Key Claims count | 3–5 rows in Key Claims table |
| Claim granularity | Single sentence per row; no semicolons joining assertions, no questions, no topic labels |
| Prose length | Body word count ≤ 1,200 (excluding frontmatter, Key Claims table, headers) |
| Required frontmatter | All required fields present and non-empty for page type |
| summary field | Present, non-empty, single sentence — Topic and Tool pages only |
| status vocabulary | Value within controlled set for page type |
| Mandatory sections | Pitfalls pages: all three H2 headings present |
| Derived claim sourcing | [derived]-annotated claims not flagged as sourcing gaps |
| Minority view sourcing | [minority view]-annotated sources not flagged as sourcing gaps |

Record each deviation by page and criterion. If the same criterion deviation appears in
three or more sampled pages: flag as systemic drift — forced choice:

```
[N] Schema conformance drift detected
    Criterion: {criterion name}
    Affected pages: [[page-1]], [[page-2]], [[page-3]]
    A) Acknowledge — I will review and correct in the next session
    B) Schema revision needed — surface as a design gap
```

Individual deviations below the three-page threshold: logged informational only.

**Step L12 — Collection gap analysis**

Read `log.md` and aggregate all query log entries. For each entry, read `result_quality`
and `topic_tags`. Identify topic tags where three or more distinct query log entries
carry `result_quality: sparse` or `result_quality: shallow`.

For each identified gap topic:
- Check whether any Source pages have been ingested since the most recent sparse or
  shallow query log entry for that topic tag (compare Source page `ingested_date` values
  against the query log entry date). If yes: annotate as "potentially addressed —
  {N} sources ingested since last sparse/shallow result." Do not suppress the gap entry;
  the human assesses sufficiency.
- If no sources have been ingested since the most recent sparse/shallow entry: treat
  as an active gap.

Surface active gaps and potentially-addressed gaps in the lint pre-flight report as a
forced choice:

```
[N] Collection gap: "{topic-tag}"
    Sparse/shallow queries: {N} (most recent: YYYY-MM-DD)
    Potentially addressed: yes ({N} sources ingested since) | no
    A) Confirm as active gap — add to collection-gaps.md
    B) Mark as addressed — remove from collection-gaps.md if present
    C) Dismiss — not a priority
```

**Step L12a — Session stats threshold check**

Count `session-stats` entries in `log.md`. If count < 50: skip this step.

If count ≥ 50, surface as a forced choice in the lint pre-flight report:

```
[N] Cost log has {N} session-stats entries. A threshold review is recommended.

    A) Review now — analyze session-stats log and propose revised batch-size guidance
    B) Defer — continue lint pass without review
```

**If A is selected, execute the inline review:**

Read all `session-stats` entries. Analyze:
- Rate of `session limit hit: yes` entries, broken out by `time window: peak` vs.
  `time window: off-peak`.
- Whether any source type mix is associated with a disproportionate rate of limit hits.
- Whether sessions that completed without hitting the limit were consistently within
  the 3–5 document batch guidance, or whether larger batches also completed cleanly.

Produce a recommendation in one of the following forms:

- **Keep thresholds:** The 5-document trigger and A/B/C options in Step 0 are well-
  calibrated. State the evidence (e.g., "limit-hit rate is {N}% overall; no source type
  mix shows elevated risk").
- **Lower the trigger threshold:** The current 5-item threshold is too permissive.
  Recommend a lower value and state the evidence.
- **Raise the trigger threshold:** The current guidance is more conservative than needed.
  Recommend a higher value.
- **Add source-type-specific cap:** Certain source types (e.g., research papers,
  transcripts) show elevated limit-hit rates and warrant a separate per-type cap.
  Propose specific values.

Precede the recommendation with this caveat: "Token counts from /cost are approximate
and Anthropic does not publish Pro tier token budgets. Limit-hit rate (yes/no) is the
primary signal. Recommendations are directional, not empirically precise."

The human confirms any threshold changes. If confirmed: the human updates the batch-size
numbers in Step 0 of this document and appends a `schema-change` log entry to `log.md`.

**Step L12b — Deferred ingest staleness check**

Check whether `raw/deferred-ingest.md` exists. If it does not: skip this step.

If it exists, read the `created` field. If the file is older than 14 days, add a forced
choice to the lint pre-flight report:

```
[N] Stale deferral: raw/deferred-ingest.md is {N} days old. The deferred ingest has
    not been resumed.

    A) Resume ingest now — proceed to Step 0 after lint completes
    B) Discard — delete raw/deferred-ingest.md; leave queue.md unchanged
```

If the file is 14 days old or fewer: add to the informational summary only —
"Pending deferral: raw/deferred-ingest.md exists ({N} days old)." No forced choice.

**Step L12c — Override pattern detection**

Read `wiki-lessons-learned.md` `## Ingest` and `## Lint` sections. For each entry,
read the entry date (from the `### [YYYY-MM-DD]` heading) and the `**Operation:**` field.
Count entries whose date falls within the past 30 days, grouped by the category described
in `**What was wrong:**`.

If any category has 3 or more entries within the 30-day window:
- This is a pattern signal. Auto-execute (no forced choice, no human confirmation needed):
  write a new entry to `wiki-lessons-learned.md` under `## Schema Signals` using the
  format specified in Section 5.9. Set `**Status:** open`.
- Add to lint informational summary: "Schema signal written: override pattern detected
  in {category} — {N} overrides in past 30 days. See wiki-lessons-learned.md
  ## Schema Signals."

Do not write a Schema Signals entry if a `## Schema Signals` entry for the same category
already exists with `**Status:** open`. One open signal per category is sufficient.

This step has no forced choice and generates no pre-flight report item. It is
informational only. The human decides, outside the wiki, whether to bring the signal
to a design session as a friction report.

**Step L12d — Schema Signals age check**

Read `wiki-lessons-learned.md` `## Schema Signals` section. For each entry with
`**Status:** open`:
- Read the entry date from the `### [YYYY-MM-DD]` heading.
- Compute age in days from today's date.
- If age > 60 days: record for informational summary.

This step is informational only. No forced choice. The human decides whether to bring
an aged signal to a design session.

**Step L13 — Consolidate pre-flight report**

```
Lint pre-flight report — pass {N} | {date}
{N} decisions require your input. Respond with: 1:A 2:B ...

[Forced choices in order: open contradictions (L4b), concept gaps (L7),
 decay_exempt proposals (L9), teaching completeness (L10), schema drift (L11),
 collection gaps (L12), session stats threshold (L12a if triggered),
 stale deferral (L12b if triggered)]

Informational summary:
- Pages with changed support scores: {N}
- Expired contradiction flags (will auto-confirm): {list or "none"}
- Pages downgraded to stale: {list or "none"}
- Comparison pages downgraded to stale: {list or "none"}
- Stale pages eligible for upgrade (one condition unmet): {list or "none"}
- open_contradictions counter: overview.md {N}, actual {M} {— auto-corrected | — discrepancy flagged for investigation | — verified match}
- Orphan pages detected: {list or "none"}
- Pitfalls failure_mode_count updates: {N}
- Teaching notes currency flags (>90-day drift between teaching_notes_reviewed and last_assessed): {N} — {wikilinks or "none"}
- Teaching notes missing on teaching-tagged pages: {N} — {wikilinks or "none"}
- CTRD-NNN signals found in queue.md: {list or "none"}
- Individual schema deviations (below drift threshold): {list or "none"}
- Potentially-addressed gaps: {list or "none"}
- Nominations aging to stale (≥90 days): {N} — {titles or "none"}
- Stale nominations being deleted (≥180 days): {N} — {titles or "none"}
- Items without nominated_date (aging skipped): {N or "none"}
- Pending deferral: {raw/deferred-ingest.md exists — N days old | none}
- Schema signal written (L12c): {category and count | none}
- Open Schema Signals older than 60 days: {N} — {name and age in days each | "none"}
- Skill file TO BE ENRICHED sections with no real examples after 5+ ingests: {list or "none"}
```

If no forced choices exist: state this explicitly and proceed to Phase 3 immediately.

**Step L14 — Skill file enrichment staleness check**

For each of the three skill files (EXTRACTION-SKILL.md, TAGGING-SKILL.md,
CONTRADICTION-SKILL.md): scan for sections marked "TO BE ENRICHED from Operational
Experience." For each such section that remains entirely unpopulated (contains no
real operational examples, only placeholder text): count the number of `ingest` log
entries in log.md since the wiki was initialized.

If the count is 5 or more and the section remains unpopulated: add to the informational
summary in the lint pre-flight report:

```
Skill file TO BE ENRICHED sections with no real examples after 5+ ingests:
  - {skill-file}.md § {section}: {section title}
```

This is informational only — no forced choice. The human uses this signal to prioritize
skill file enrichment in the next ingest session.

---

#### Phase 3 — Execution Pass (ordered)

1. Process CTRD-NNN signals from queue.md per Section 8.4 override mechanism.
2. Write updated support scores to Key Claims tables on all marked pages.
3. Process expired contradiction flags: apply window-expired-confirmed state changes
   per Section 8.4.
4. Update `status` to `stale` on all marked Topic, Tool, and Comparison pages.
4a. Apply confirmed stale → current upgrades from Step L5a: set `status: current` on
    each confirmed page.
5. Update `failure_mode_count` on all marked Pitfalls pages.
6. Apply confirmed `decay_exempt: true` settings.
7. Create stub pages for confirmed concept gap choices.
8. Write Schema Signals entries to `wiki-lessons-learned.md` if L12c detected patterns
   (auto-execute — no human confirmation).
9. Update `raw/collection-gaps.md`: add confirmed active gaps; mark addressed gaps;
   remove dismissed gaps. Format:

```markdown
# Collection Gaps
Last updated: YYYY-MM-DD (lint pass {N})

## Active Gaps
- **{topic-tag}** — {N} sparse/shallow queries; most recent: YYYY-MM-DD

## Potentially Addressed
- **{topic-tag}** — {N} sources ingested since last sparse/shallow result; confirm sufficiency

## Resolved
- **{topic-tag}** — marked addressed YYYY-MM-DD
```

10. Regenerate `teaching-index.md` from current tags.
11. Update `overview.md`: set `last_lint` to today; update `total_pages`,
    `open_contradictions`, `last_contradiction_id` if changed. If Step L4c flagged a
    ±1 auto-correction or the human confirmed a ±2+ correction: set `open_contradictions`
    to the actual count derived in Step L4c.
12. Execute nomination queue aging from Step L1a:
    - Move all Stage 1 items from `[nominated]` to `[stale-nominated]` in queue.md.
      Preserve the full line content including `nominated_date`; do not update the date.
    - Delete all Stage 2 items from `[stale-nominated]` in queue.md.
13. Append lint log entry.

---

#### Lint Log Entry Format

```
## [YYYY-MM-DD] lint | pass {N}
Pages assessed: {N}. Sources in wiki: {N}.
Support scores recalculated: {N} pages ({N} claims updated).
Expired contradictions auto-confirmed: {N} — {CTRD-IDs or "none"}
CTRD-NNN signals processed: {N} — {CTRD-IDs and outcomes or "none"}
Pages downgraded to stale: {N} — {wikilinks or "none"}
Orphan pages flagged: {N} — {wikilinks or "none"}
Concept gaps surfaced: {N} — {confirmed/declined breakdown}
decay_exempt confirmed: {N} — {wikilinks or "none"}
Schema drift flags: {N} — {criteria or "none"}
Teaching relevance ratio: {N}% ({above/below} 20% threshold)
Collection gaps confirmed: {N} | addressed: {N} | dismissed: {N}
Nominations aged to stale: {N} — {titles or "none"}
Stale nominations deleted: {N} — {titles or "none"}
Teaching Index regenerated: yes | no
Skill enrichment staleness flags: {N} — {skill file sections or "none"}
Teaching notes currency flags: {N} — {wikilinks or "none"}
```

### 11.5 Query Workflow

**Interaction model:** Queries are conversational — the human poses a question, Claude
Code reads the wiki and responds. The only phase-gated step is the filing decision,
which occurs after the response is delivered.

---

### Named Query Modes

**Instructor summary mode** is invoked when the human specifies phrasing equivalent to
"instructor summary on [topic]," "teaching brief for [topic]," or "pull together teaching
notes on [topic]":

- **Pattern (Q1):** Treated as a synthesis/evolution query but with Teaching Index scope.
- **Scope (Q2–Q3):** Read `teaching-index.md` first to identify all teaching-tagged pages
  matching the topic. Then read those pages in full, prioritizing their `## Teaching Notes`
  sections. If no Teaching Index entry matches, fall back to full index.md search.
- **Response format (Q4):** Structured output in four parts:
  1. **Concept overview** — 2–3 sentences from the Key Claims layer.
  2. **Teachable angle** — what this topic reveals about AI effectiveness that is
     pedagogically valuable; drawn from `teaching_notes` **Why it matters** and
     **What this failure mode teaches** subsections.
  3. **Suggested framing** — how to introduce this in a course; drawn from
     `teaching_notes` **Suggested framing** and **Common misconceptions** subsections.
  4. **Related pages** — wikilinks to constituent pages and their page type.
  Avoid jargon without an inline definition. Write for an instructor preparing to teach,
  not for a practitioner using the tool.
- **Filing (Q6):** Always assessed as Case 3 (teaching-brief). The filing prompt reads:
  "This response qualifies as a teaching-brief. File as `teaching/{slug}-brief.md`?" with
  options A) File / B) Do not file (deliver ephemerally). Human must confirm before any
  file is written.

---

#### Step Q1 — Query Classification

Classify the query against the five named patterns:

| Pattern | Signals |
|---|---|
| Landscape/comparison | "compare," "which," "versus," "landscape," "options for" |
| Synthesis/evolution | "how has," "what is the current state," "what do we know about," "summary of" |
| Implementation | "how do I," "how would we," "given [tool constraint]," "workflow for" |
| Discovery/recommendation | "what should I look at," "what's worth reading," "recommend" |
| Pitfalls/failure modes | "what goes wrong," "risks of," "failure modes," "antipatterns" |

A query may match more than one pattern — use the dominant pattern for format selection.
Classification determines the default response format (Step Q4) and the filing threshold
assessment (Step Q5).

#### Step Q2 — Index Consultation

Read `index.md` in full. Identify all pages relevant to the query based on page titles
and one-line summaries. Do not read page content at this step. Produce a candidate list.

**Relevance threshold:** Include a page if its summary suggests it contains information
bearing on the query. Err toward inclusion — filtering happens in Step Q3. A candidate
list of 8–12 pages for a broad query is normal.

**Sparse result detection:** If index.md yields zero or one candidate for a clearly
in-scope query, classify as a preliminary sparse result. Proceed through Step Q3 to
confirm, then apply gap handling (Step Q2a).

#### Step Q2a — Sparse and Shallow Result Handling

Assess result quality after Step Q3 using the following classification:

- **sparse:** 0–1 material contributors after Step Q3 filtering.
- **shallow:** 2+ material contributors, but more than half have `status: stub` or
  `stale`, OR the average `source_count` across returned pages is ≤ 2.
- **adequate:** 2+ material contributors, not shallow.
- **rich:** 5+ material contributors, not shallow.

Both `sparse` and `shallow` trigger the gap nomination procedure below. `adequate` and
`rich` do not.

**Gap nomination procedure (sparse or shallow result):**

After delivering the response (or a gap report if zero candidates), scan `raw/queue.md`
for items in the `[nominated]` section. Match nominated items to the query topic by
title string — surface all items sharing significant terms with the query; do not rank.
Items already in `[queued]` are in the ingest pipeline and are not re-surfaced.

Also scan the `[stale-nominated]` section using the same title-string matching. Surface
matching stale nominations in a separate block below the main nominated block, labeled
"Older nominations (90+ days):". These receive the same forced choices; if the human
selects A (promote), the item moves from `[stale-nominated]` directly to `[queued]` —
a demand signal has revived it, bypassing the normal `[nominated]` stage.

```
Query result quality: {sparse | shallow} — this query returned {zero | fewer than two
material contributors | thin coverage}.

Nominated sources that may be relevant:

[N] {title} | {url} | {source_type} | {credibility_tier} | nominated: {YYYY-MM-DD}
    A) Promote to ingest queue
    B) Discard nomination
    C) Skip — leave as nominated

Older nominations (90+ days) that may be relevant:

[N] {title} | {url} | {source_type} | {credibility_tier} | nominated: {YYYY-MM-DD}
    A) Promote to ingest queue
    B) Discard nomination
    C) Skip — leave as stale-nominated

[N+1] No relevant nominations found — propose new candidate sources
    A) Yes — suggest candidates for this topic
    B) No
```

Omit either block entirely if no matches are found in that section. If neither section
yields matches, show only the final "No relevant nominations" item.

If option A is selected on the final item: suggest candidate sources from training
knowledge. Precede suggestions with an explicit caveat: "The following are suggested
candidates. Verify URLs before adding to queue." Promoted nominations move from
`[nominated]` to `[queued]` in queue.md. Generated suggestions are appended to
`[nominated]` for human review before any ingest — they do not enter `[queued]`
automatically.

**If index.md yields zero candidates for a clearly in-scope query:** Report that the
wiki does not yet cover this topic and suggest whether an ingest would address the gap.
Do not fabricate an answer from training data. Do not search the web unless the human
explicitly requests it.

#### Step Q3 — Page Retrieval and Selection

Read each candidate page in full. Select pages that materially contribute to the answer:
a page is a material contributor if it contains at least one claim, finding, or
structured entry (Key Claims row, capabilities list item, failure mode entry) that
directly bears on the query.

Pages consulted but not material are excluded from the response and citation.

**Depth adjustment by source credibility:** Weight claims proportionally to
`support_score` values in Key Claims tables. Claims with `status: contested` must be
surfaced explicitly — do not present them as settled. Claims with `status: stale`
must be flagged as potentially outdated.

#### Step Q4 — Response Format

Default formats by query pattern:

**Landscape/comparison:** Structured markdown table or side-by-side comparison. Columns
are entities being compared; rows are comparison dimensions. Followed by a brief
synthesis paragraph identifying dominant differentiators.

**Synthesis/evolution:** Prose with H2 section headers following the natural topic
structure. Key Claims from source pages are the primary evidence layer. End with an
"Unresolved questions" subsection if contested or stale claims were encountered.

**Implementation:** Numbered steps or a Mermaid flow diagram for branching logic;
plain numbered list for linear processes; prose only if the query is not procedural.

**Discovery/recommendation:** Ranked list with one-paragraph rationale per item. Cite
the wiki pages from which the recommendation derives.

**Pitfalls/failure modes:** Three-section structure mirroring Pitfalls page format:
Technical Limitations, Usage Antipatterns, Alignment and Safety Concerns. Draw from
the target entity's Pitfalls page plus related Topic-scoped Pitfalls pages. Note the
`**Status:**` of each failure mode inline.

#### Step Q5 — Citation Format

Citations reference wiki pages as the knowledge layer, not raw source documents.

```
[claim or synthesis statement] (→ [[page-slug]])
```

When source credibility is material to interpreting the claim — contested claims or
claims with low support scores:

```
[claim] (→ [[page-slug]], sourced from {credibility_tier})
```

Multiple supporting pages for a single claim:

```
[claim] (→ [[page-slug-1]], [[page-slug-2]])
```

Do not cite Source pages directly in query responses — they are implementation detail.
Exception: when the human explicitly asks about a specific source, cite the Source page
directly.

#### Step Q6 — Filing Assessment

After delivering the response, assess whether the result warrants filing as a new page.
Query outputs are not sources — do not run them through the ingest source classification
taxonomy. Three cases govern how filing works:

**Case 1 — New cross-topic synthesis (Comparison page)**

File if: the response synthesizes information across three or more wiki pages AND the
primary structure is a multi-criteria comparison across named entities.

Action: create a Comparison page. Set `provenance: query-generated` and `query_date`
(today) in frontmatter. Citations are internal wikilinks to constituent pages only —
no `sources` list, no credibility weight, no Source page. Full teaching/competency/context
tagging applies. Human must confirm via forced choice before any file is written.

**Case 2 — Refinement of an existing page**

If the response surfaces a framing, nuance, or synthesis insight that belongs on a
single existing Topic or Tool page (not novel enough for a new page, not a comparison):
propose adding it as a section-targeted update to the existing page. No new source page.
No credibility weight. No extraction step. Surface as a forced choice:

```
[N] Query insight could update an existing page: [[page-slug]]
    Proposed addition: [one sentence summarizing the insight]
    A) Apply as targeted update — add to existing page prose
    B) Do not apply
```

If A confirmed: proceed as a minimal ingest update targeting only the relevant prose
section. Note `provenance: query-generated` in the commit message only — not in
frontmatter.

**Case 3 — Instructor summary (teaching-brief)**

Instructor summary mode outputs always qualify for Case 3 filing. Standard query
responses may also qualify if they produce a structured instructor-facing synthesis.

Filing prompt:

```
Filing assessment: this response meets the teaching-brief filing criterion.
Proposed type: teaching-brief
Proposed filename: teaching/{slug}-brief.md
    A) File as proposed
    B) File with a different title — specify
    C) Do not file (deliver ephemerally)
```

If A or B confirmed: execute Step Q7 using the teaching-brief procedure below.

**Do not file if:** the response is a direct lookup from a single page, a simple
factual answer, a recommendation list with no novel synthesis, or a procedural answer
already covered by an existing page.

**For standard (non-teaching-brief) queries not meeting Case 1 or 2:**

```
Filing assessment: [this response meets | does not meet] the filing criterion.
[If meets:] Proposed page type: {Comparison | Topic}. Proposed filename: {slug}.
    A) File as proposed
    B) File with a different title or type — specify
    C) Do not file
```

Filing is never automatic. The human confirms every filing.

#### Step Q7 — Page Creation for Filed Results (if confirmed)

**Case 1 — Comparison page:**

Treat as a minimal ingest operation:
1. Create the new page with full frontmatter. Set `source_count` to the number of wiki
   pages cited in the response. Set `created` and `updated` to today. Set
   `provenance: query-generated` and `query_date: today`.
2. Populate Key Claims from the response. Apply the 3–5 claim rule. Each claim's Source
   field references the wiki pages cited, not raw sources. Annotate all such claims with
   `[derived]` in the Source field.
3. Update `index.md`.
4. Increment `total_pages` in `overview.md`.
5. Append a query log entry.

**Standard Topic page filing:**

Same as Case 1 (Comparison) except: no `provenance` field, standard Source classification applies.
1. Create the new page with full frontmatter.
2. Populate Key Claims. Annotate all `[derived]`.
3. Update `index.md`.
4. Increment `total_pages` in `overview.md`.
5. Append a query log entry.

**Case 3 — Teaching-brief:**

1. Derive the slug from the topic and brief type. Use naming convention
   `teaching/{topic-slug}-brief.md` for single-topic; `teaching/{use-case-slug}-instructor-brief.md`
   for multi-topic.
2. Create the page with full frontmatter per CLAUDE.md Section 5.10. Set
   `teaching_relevance: true`, `query_date: today`, `last_reviewed: today`,
   `status: current`. Populate `derived_from` with full-path wikilinks to all constituent
   pages whose `teaching_notes` or Key Claims contributed to the response.
3. Page body: the structured output from the instructor summary mode (concept overview,
   teachable angle, suggested framing, related topics). Plain prose, no citations.
4. Assign `competency_domains` and `professional_contexts` from the constituent pages'
   tags — use the union of all constituent page tags, filtered to those clearly relevant
   to the brief's topic scope.
5. Update `index.md` — add under a new `## Teaching` section if one does not exist.
6. Increment `total_pages` in `overview.md`.
7. Append a query log entry.

#### Step Q8 — Query Log Entry

```
## [YYYY-MM-DD] query | {one-line description of the query}
Pattern: {landscape | synthesis | implementation | discovery | pitfalls}
Result quality: sparse | shallow | adequate | rich
Topic tags: {kebab-case terms drawn from index.md page slugs where possible}
Pages consulted: {N} — {wikilinks}
Filed: yes — [[new-page-slug]] | no
Gap nominations surfaced: yes | no
```

`Result quality` is set by Claude Code based on the Step Q2a classification.
`Topic tags` are Claude Code's best effort to tag the query against existing wiki topic
slugs — imprecise but structured enough for lint aggregation in Step L12.

---

