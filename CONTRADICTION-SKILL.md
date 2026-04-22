# CONTRADICTION-SKILL.md — Contradiction Resolution Skill File

**Purpose:** Read this file before any contradiction resolution during ingest or lint.
It provides the three-path decision logic, worked numerical examples for each path,
the boundary condition resolved unambiguously, vendor_bias treatment, retraction
trigger, and stacking rules for claims with multiple simultaneous contradictions. It
does not replace CLAUDE.md Section 8 — it supplements it with concrete cases that
make the path selection unambiguous.

**Scope:** Three-path resolution procedure, boundary condition at difference=2, stacking
rules for minority views and concurrent Path B flags, vendor bias correction heuristic,
retraction trigger, flag format.

**Version:** Starter template. Sections marked TO BE ENRICHED require real operational
cases before they are complete.

---

## 1. Inputs and Path Decision Logic

### 1.1 Four Inputs

1. **Incoming source credibility weight:**
   - `peer-reviewed`: 3
   - `institutional`: 2
   - `practitioner`: 1
   - `community`: 0 (cannot anchor Key Claims and cannot trigger the contradiction protocol
     on its own — ignore community-weight sources in contradiction assessment)

2. **Existing Key Claim support score:** The sum of credibility weights of all supporting
   sources in the claim's Source field, with decay applied. Sources older than 12 months
   contribute half their weight (0.5× multiplier). If `decay_exempt: true`, no decay.
   Round to one decimal place.

3. **Score difference:** |incoming weight − existing support score|. Always positive.

4. **Direction:** Whether the incoming weight exceeds or is exceeded by the existing score.

### 1.2 Path Labels — Quick Reference

| Label | Operational Alias | Plain Meaning |
|---|---|---|
| Path A | `auto-resolved` | Incoming source materially outweighs existing support; wiki updates without human input |
| Path B | `human-review` | Near-tie; human decides within the 7-day override window |
| Path C | `minority-view` | Existing support materially outweighs incoming; new source recorded as dissent, claim unchanged |

**Path B takes precedence over Path A at the boundary (difference = exactly 2).** See
precedence order below.

### 1.3 Path Decision — Precedence Order

Apply these tests in order. The first test that fires determines the path.

**Test 1 — Path B applies if |difference| ≤ 2 (regardless of direction).**
Condition: the score difference is 2 or less, in either direction.
Operational alias: `human-review`.

**Test 2 — Path A applies if difference > 2 AND incoming weight > existing score.**
Condition: incoming source materially outweighs existing support AND the difference
strictly exceeds 2.
Operational alias: `auto-resolved`.

**Test 3 — Path C applies if difference > 2 AND existing score > incoming weight.**
Condition: existing support materially outweighs the incoming source AND the difference
strictly exceeds 2.
Operational alias: `minority-view`.

**Critical boundary clarification:** When the score difference is exactly 2, Path B
applies — even if the incoming source outweighs the existing support score. Path A fires
only when the difference strictly exceeds 2. This ensures near-tie contradictions receive
human review rather than auto-resolution.

### 1.4 Contradiction Existence Check

Before calculating paths, confirm a contradiction exists. A contradiction requires
directional incompatibility — the new source's claim cannot be true at the same time
as the existing Key Claim. These are not contradictions:

- A new source adds nuance or detail to an existing claim without negating it.
- A new source covers the same topic with a different emphasis.
- A new source extends the finding to a new context without challenging the original.

When in doubt, treat it as not a contradiction and update the prose under rolling
overwrite. Only invoke the three-path protocol when the new source's finding is
directionally incompatible with the existing Key Claim.

---

## 2. Worked Examples

### Example 1 — Path A (Auto-Resolve)

**Context:** Existing Key Claim on `topics/domain-adaptation-fine-tuning.md`.

**Existing state:**
- Claim: "Fine-tuning a pre-trained language model on domain-specific corpora improves
  classification accuracy by approximately 12% over zero-shot prompting on the same
  domain benchmark."
- Supporting source: one practitioner blog post (`credibility_tier: practitioner`,
  weight=1), published 22 months ago.
- Apply 12-month decay: 1 × 0.5 = 0.5.
- **Existing support score: 0.5**

**Incoming source:** A peer-reviewed NeurIPS paper (`credibility_tier: peer-reviewed`,
weight=3) that directly contradicts the figure, reporting approximately 3% improvement
under controlled conditions using the same benchmark.

**Calculation:**
- Incoming weight: 3
- Existing support score: 0.5
- Score difference: 3 − 0.5 = 2.5
- Direction: incoming > existing

Test 1 — Path B: difference is 2.5. 2.5 > 2. **Does not fire.**
Test 2 — Path A: difference > 2 AND incoming (3) > existing (0.5). **Fires.**

**Resolution: Path A — auto-resolved.**

**Actions (Phase 2, no pre-flight forced choice):**
1. Update Key Claim text to reflect the new finding.
2. Replace Source field with the NeurIPS source wikilink.
3. Set Support Score to 3. Set claim status to `current`.
4. Update prose via rolling overwrite to reflect the revised finding.
5. Log a `contradiction-auto-resolved` entry.
6. Surface in post-ingest summary under "Auto-resolved contradictions" — informational
   only, not a required action. Because the page had `status: current` before resolution,
   apply additional prominence: list the page, old claim, and new claim explicitly.

**Rationale:** The existing source was old (22 months), decayed, and practitioner-tier.
The incoming source is peer-reviewed and current. The difference (2.5) exceeds the Path B
threshold (2). Auto-resolution is appropriate.

---

### Example 2 — Path B (Human Review, Boundary Condition)

**Context:** Existing Key Claim on `topics/retrieval-augmented-generation.md`.

**Existing state:**
- Claim: "Naive top-k RAG without re-ranking achieves 61% recall on a standard open-domain
  QA benchmark."
- Supporting source: one practitioner evaluation report (`credibility_tier: practitioner`,
  weight=1), published 4 months ago.
- No decay (within 12 months).
- **Existing support score: 1.0**

**Incoming source:** A peer-reviewed paper (`credibility_tier: peer-reviewed`, weight=3)
reporting 58% recall under the same benchmark setup, directly contradicting the specific
figure.

**Calculation:**
- Incoming weight: 3
- Existing support score: 1.0
- Score difference: 3 − 1.0 = **2.0**
- Direction: incoming > existing

Test 1 — Path B: difference is 2.0. 2.0 ≤ 2. **Fires.**

**Resolution: Path B — human-review.**

This is the boundary condition. Even though the incoming source is peer-reviewed (weight=3)
and the existing source is practitioner-tier (weight=1), the score difference is exactly 2,
which is within the Path B range. Path A does not fire — it requires difference strictly
greater than 2. Human review is required.

**Why Path B at this boundary?** A peer-reviewed source directly contradicting a practitioner
finding by 3 percentage points is a genuine contested case — the difference may reflect
prompting conditions, dataset version, or evaluation methodology, not a definitive
correction. The human should assess whether the conditions are comparable before
auto-resolving.

**Actions (pre-flight forced choice and post-execution):**
1. Assign CTRD-ID: read `last_contradiction_id` from `overview.md`, increment by 1.
2. Generate frontmatter entry on the affected page:
   ```yaml
   open_contradictions:
     - id: "CTRD-001"
       claim_summary: "Naive top-k RAG achieves 61% recall on open-domain QA benchmark"
       contesting_source: "[[2024-peer-reviewed-rag-eval]]"
       flagged_date: "YYYY-MM-DD"
       override_window_closes: "YYYY-MM-DD+7"
       path: "human-review"
   ```
3. Append `contested [CTRD-001]` to the Status cell of the Key Claim row.
4. Update prose to reflect the newer view (rolling overwrite proceeds).
5. Log a `contradiction-flag` entry.
6. Surface in post-ingest summary under "Contradictions flagged for review" — required
   action with window close date.

---

### Example 3 — Path C (Minority View)

**Context:** Existing Key Claim on `topics/constitutional-ai.md`.

**Existing state:**
- Claim: "Constitutional AI training reduces harmful outputs by approximately 40% relative
  to RLHF-only training on Anthropic's internal safety evaluation suite."
- Supporting sources: two Anthropic institutional blog posts (`credibility_tier:
  institutional`, weight=2 each), published 5 months and 9 months ago respectively.
- No decay on either (both within 12 months).
- **Existing support score: 2 + 2 = 4.0**

**Incoming source:** A practitioner blog post (`credibility_tier: practitioner`, weight=1)
arguing the reduction is closer to 25% under stricter third-party test conditions.

**Calculation:**
- Incoming weight: 1
- Existing support score: 4.0
- Score difference: 4.0 − 1 = 3.0
- Direction: existing > incoming

Test 1 — Path B: difference is 3.0. 3.0 > 2. **Does not fire.**
Test 2 — Path A: difference > 2 AND incoming (1) > existing (4). Incoming does not
exceed existing. **Does not fire.**
Test 3 — Path C: difference > 2 AND existing (4) > incoming (1). **Fires.**

**Resolution: Path C — minority-view.**

**Actions:**
1. Do not change claim status. Do not change claim text.
2. Add the practitioner source to the Source field with `[minority view]` annotation:
   `[[2024-practitioner-cai-critique]] [minority view]`
3. Log a `contradiction-flag` entry at informational level. This does not create an
   `open_contradictions` frontmatter entry — that is for Path B only.
4. Do not surface as a required action for human review.
5. Note in post-ingest summary under "Minority views recorded" — informational only.

**Rationale:** Two recent institutional sources supporting the existing claim outweigh
a single practitioner blog by a margin of 3. The minority view is recorded for
provenance, not elevated to a contested status.

---

## 3. Stacking Rules — Multiple Contradictions on One Claim

### 3.1 Multiple Path C Accumulations (Minority Views)

Minority views accumulate in the Source field without limit. There is no restriction on
how many `[minority view]` annotations a single claim row can carry. Each additional
minority view source is appended to the Source field and a new informational
`contradiction-flag` log entry is written. No `open_contradictions` frontmatter entry
is created for Path C resolutions.

**Source field with two minority views:**
```
| [claim text] | [[source-a]], [[source-b]] [minority view], [[source-c]] [minority view] | ... | current | 4.0 | false |
```

Minority view sources do not contribute to the incumbent support score. Exclude them
from score calculations.

### 3.2 New Source Arrives While Claim is Already Contested (Path B Open)

When a new source arrives and the target claim already carries an open
`contested [CTRD-NNN]` flag, determine the new source's posture relative to the
existing three-party state (incumbent claim, existing contesting source, new source)
and apply the corresponding procedure.

**Posture 1 — New source supports the contesting source's position.**

1. Add the new source to the existing contesting position. Recalculate the combined
   contesting weight (sum of all sources supporting the contesting position, with decay
   applied). Treat this combined weight as the new incoming weight for path determination
   against the incumbent support score.
2. Rerun path determination with the updated combined contesting weight:
   - Path A territory (difference > 2, contesting > incumbent): auto-resolve. Update the
     claim to reflect the contesting position. Close the CTRD entry as `auto-resolved`
     with note "contesting weight increased above Path A threshold." Write
     `contradiction-auto-resolved` log entry.
   - Still Path B territory: update the CTRD entry's `contesting_source` field to include
     the new source. Update the incumbent's support score if it changed. Do not reset the
     override window close date.

**Posture 2 — New source supports the incumbent claim.**

1. Add the new source to the incumbent's Source field. Recalculate the incumbent support
   score.
2. Rerun path determination with the updated incumbent score:
   - Path C territory (difference > 2, incumbent > contesting): the incumbent has
     strengthened enough to demote the contest. Close the CTRD entry as `auto-resolved`
     with note "incumbent score increased above Path B threshold." Write
     `contradiction-auto-resolved` log entry. Remove the `contested [CTRD-NNN]` inline
     marker. Remove the CTRD entry from `open_contradictions`. Decrement
     `open_contradictions` counter in `overview.md`.
   - Still Path B territory: update the incumbent support score in the Key Claims table.
     Inform in post-ingest summary: "CTRD-NNN incumbent score increased — still in
     human-review range." Do not reset the override window close date.

**Posture 3 — New source takes a genuinely distinct third position.**

A third position means the new source is directionally incompatible with both the
incumbent claim and the existing contesting source.

1. Run the three-path protocol for the new source against the incumbent claim's current
   support score independently. The existing CTRD-NNN flag is not a factor in this
   calculation — treat the incumbent score as the baseline.
2. Apply the outcome:
   - Path A: The new source outweighs the incumbent by more than 2. Update the claim
     to the new source's position. Close CTRD-NNN simultaneously — the original
     contesting source is also superseded. Log both closures. Add the original contesting
     source to the Source field with `[minority view]` unless its position aligns with
     the new source's.
   - Path B: A new CTRD-NNN+1 is assigned. The Status cell carries both IDs:
     `contested [CTRD-NNN] [CTRD-NNN+1]`. The `open_contradictions` list carries two
     entries. Update the prose to accurately describe that multiple competing positions
     exist — do not present either contesting view as settled.
   - Path C: Record the new source as `[minority view]`. CTRD-NNN remains open and
     unchanged.

**Key constraint for dual Path B (two CTRD flags on one row):** The Key Claims table
row always asserts one incumbent position — the claim text does not change until a CTRD
entry is resolved. When two CTRD flags are open on the same row, the prose body (via
rolling overwrite) must accurately describe the contested state, naming the competing
positions. The claim row is the provenance anchor; the prose is where the contested
picture lives for human readers.

---

## 4. vendor_bias Correction Heuristic

A vendor-content source (`source_type: vendor-content`, weight=1) that contradicts an
existing claim receives standard path treatment based on weight arithmetic. However,
apply the following bias correction when all three conditions hold:

1. Source type is `vendor-content`.
2. The contradiction favors the vendor's own product or disfavors a named competitor.
3. At least one non-vendor source supports the existing claim.

**When all three conditions hold: apply Path C regardless of the score arithmetic.**

Record the override in the `contradiction-flag` log entry:

```
## [YYYY-MM-DD] contradiction-flag | [page title]
Page: [[page-slug]]
Claim: [one-sentence paraphrase]
Contesting source: [[source-slug]] (practitioner, weight=1)
Existing support score: [N]
Resolution path: minority-view
Note: Path C applied on vendor-bias grounds. Nominal score arithmetic suggested Path B
(difference=[N]). Vendor-content source with self-favorable comparative claim; one
independent source supports the existing claim.
```

**When NOT to apply the vendor-bias override:**
- When the existing claim is also vendor-sourced (no independent baseline to protect).
- When the contradiction concerns a factual matter objectively verifiable by a third party
  (pricing, release dates, API specifications).
- When no non-vendor source supports the existing claim — in that case, Path B is correct
  because both sides are vendor-sourced.

---

## 5. Retraction Trigger

A retraction is not a contradiction. Do not apply the three-path protocol to a retracted
source. The procedure is independent of support scores.

**Trigger:** The human sets `status: retracted` on a Source page.

**Procedure:**
1. Identify every Key Claim in the wiki where the Source field references this page as
   its **sole** citation (no other wikilinks in the Source field for that claim row,
   excluding `[minority view]`-annotated sources).
2. For each such claim, surface as a retraction impact forced choice per CLAUDE.md
   Section 8.2. Do not auto-resolve.
3. For Key Claims that cite this page alongside other non-minority-view sources: do not
   surface as a retraction impact. Recalculate support score with the retracted source
   removed. If the removal shifts an existing `contested` claim's path determination
   (e.g., incumbent score drops enough to move from Path C to Path B), surface that
   separately as a forced choice.
4. A retracted Source page is never deleted and never removed from Source field citations.
   It remains in place with `status: retracted` as a permanent provenance record.

**Common error:** Confusing a superseded source (a newer source replaces an older one)
with a retracted source (the source itself has been invalidated). Supersession is handled
by the normal ingest path. Retraction is a human-triggered exception.

---

## 5a. Retraction vs. Ingested-in-Error — When to Apply Each

Both statuses result in a Source page that is permanently marked and never deleted. They
are triggered by different facts and run different procedures. Applying the wrong one is
a provenance error.

| Dimension | `status: retracted` | `status: ingested-in-error` |
|---|---|---|
| **Provenance of the source** | Was valid at ingest; later invalidated by its issuer or community consensus | Was never valid; ingested by mistake |
| **Typical cause** | Publisher issues retraction notice; methodology found fatally flawed; source identified as fabricated | Wrong document selected; source outside domain scope; misclassified source type |
| **Trigger** | Human sets `status: retracted` | Human sets `status: ingested-in-error` |
| **Governing procedure** | Section 8.2 retraction procedure | Section 8.6 correction procedure |
| **CTRD cleanup** | Not applicable — a retracted source was never the contesting source in a CTRD flag generated under normal ingest | Auto-execute Step IE-2 closes any open CTRD flags where this source is the contesting source; incumbent claim restored unconditionally |
| **Orphaned page handling** | Not applicable — a retracted source was legitimately ingested and contributed to pages that remain valid | Step IE-4 surfaces orphaned pages (those with `source_count: 1`) as delete/stub forced choices |
| **Key Claims forced choice options** | A) Remove claim, B) I will provide a replacement source, C) Downgrade page status to stale and leave claim contested | A) Remove claim, B) I will provide a replacement source (no option C — content from a never-valid source is not retained as contested) |

**Decision rule:** If you are uncertain which status to apply, ask: was the source ever
a legitimate contribution to the wiki at the time it was ingested?

- Yes → `retracted`
- No → `ingested-in-error`

**Do not use either status for supersession.** A source that has been replaced by a newer,
better source is not retracted and was not ingested in error. Use `superseded_by` on the
Source page and let the normal ingest path update affected Key Claims.

---

## 6. Support Score Calculation Reference

Credibility weights:
- `peer-reviewed`: 3
- `institutional`: 2
- `practitioner`: 1
- `community`: 0 (no contribution to support score)

Decay rule: sources published more than 12 months before today contribute 0.5× their
weight. Sources with `decay_exempt: true` on the claim row are exempt from decay.

**Calculation procedure:**
1. For each source in the claim's Source field: read `published_date` from the Source page.
2. Exclude `[minority view]`-annotated sources — they do not contribute to the incumbent
   support score.
3. If `published_date` is more than 12 months before today: multiply weight by 0.5.
4. If `decay_exempt: true` on the claim: skip decay for all sources in that row.
5. Sum all (possibly decayed) non-minority-view weights.
6. Round to one decimal place.
7. Write the result to the Support Score column.

**`[derived]` claims:** Skip numeric calculation. Record `derived` in the Support Score
column. Derive a proxy score from the `source_count` of the referenced wiki pages if
needed for path comparisons.

---

## 7. TO BE ENRICHED from Operational Experience

**7.1 Multiple Simultaneous Contradictions on One Page**
Populate with a real case showing two open CTRD entries on the same page — include the
full frontmatter list structure with two entries, the Status cell format showing both
IDs (`contested [CTRD-003] [CTRD-004]`), and the post-ingest summary format.

**7.2 Stacking Resolution — Real Cases for Each Posture**
Section 3.2 covers three postures theoretically. Populate with at least one real case
per posture after encountering it in operation.

**7.3 Counter-Intuitive Decay Cases**
Populate when decay produces a resolution path that surprises the human (e.g., an
institutional source decays below a current practitioner source's weight, flipping the
path). Document the case and the correct reasoning.

**7.4 Calibration for the vendor-bias Override**
Populate with real cases where the vendor-bias correction heuristic was applied and the
human confirmed or overrode it. Use these to refine the three-condition test if needed.

**7.5 Source Simultaneously a Contradiction Trigger and a Citation Harvest Candidate**
Populate when a single ingested source both contradicts an existing claim and cites
institutional papers that should be nominated. Document the sequencing (contradiction
detection in Steps 9–10; citation harvesting in Step 11a) and confirm these do not
interfere.