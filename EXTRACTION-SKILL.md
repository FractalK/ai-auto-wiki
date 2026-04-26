# EXTRACTION-SKILL.md — Key Claims Extraction Skill File

**Purpose:** Read this file before every ingest operation. It provides extraction rules,
worked examples, and named failure modes for Key Claims extraction from Topic and Tool
pages. It does not replace CLAUDE.md — it supplements it with concrete cases that make
the rules actionable.

**Scope:** Key Claims extraction quality. Full-depth vs. standard-depth extraction
behavior. vendor_bias annotation. Spot-check block format.

**Version:** Starter template. Sections marked TO BE ENRICHED require real operational
cases before they are complete. Treat this file as scaffolding, not finished guidance.

---

## 1. The Central Rule for Key Claims

A Key Claim is a single assertable sentence that states a specific, verifiable
proposition about the subject of the page. Before writing any Key Claim row, verify
all four of the following:

1. **Assertable.** It can be true or false. A description is not assertable. A question
   is not assertable. "This tool is widely used for enterprise search" is not assertable —
   "This tool has been deployed in production by over 500 Fortune 500 companies as of Q1
   2024" is assertable.

2. **Specific.** It contains at least one of: a named entity, a measured quantity, a named
   condition, or a named outcome. Vague improvement language ("performs better") is not
   specific. "Reduces hallucination rate by 23% on the RAGAS benchmark compared to naive
   top-k retrieval" is specific.

3. **Traceable.** It links to a specific Source page via wikilink in the Source field.
   A claim without a source wikilink is not a Key Claim — it is an unsourced assertion.
   Exception: `[derived]` claims from filed query results; see CLAUDE.md Section 6.1.

4. **Non-compound.** It makes exactly one assertion. Two facts joined by "and" or ";"
   are two Key Claims. If one is later contested, the entire row changes status — keeping
   them separate preserves independent provenance.

Self-check before writing the Key Claims table: confirm claim count is 3–5; each claim
has a source wikilink or `[derived]` annotation; each claim is a single assertable
sentence; Support Score is calculated and populated.

---

## 2. Failure Modes — Named and Illustrated

### Failure Mode 1: Topic Label Presented as a Claim

A topic label describes what a source covers rather than what it asserts. Topic labels
are among the most common extraction errors because they read like summaries and feel
useful — but they contain no specific, falsifiable information.

**WRONG:**
> "This paper covers RAG architectures and their applications in enterprise search."

**WRONG:**
> "GPT-4o supports a range of capabilities relevant to enterprise AI workflows."

**WRONG:**
> "Constitutional AI is an alignment methodology developed by Anthropic."

The third example is close to useful but is still a topic label — it identifies the
subject without asserting anything specific about it.

**RIGHT:**
> "RAG with cross-encoder re-ranking reduces hallucination rate by 23% on the RAGAS
> benchmark compared to naive top-k retrieval, per the evaluation in [source]."

**RIGHT:**
> "Constitutional AI training reduces harmful outputs by approximately 40% relative to
> RLHF-only training on Anthropic's internal safety evaluation suite, as reported in
> [source]."

**Signal you have a topic label:** If you can delete the claim without any reader losing
a specific fact — they only lose a category pointer — it is a topic label. Delete it and
extract the underlying assertion instead.

---

### Failure Mode 2: Hedged Non-Assertion

A hedged non-assertion states a claim and then removes its falsifiability.

**WRONG:**
> "The authors suggest that alignment may be important for deployment safety."

**WRONG:**
> "It is possible that chain-of-thought prompting improves multi-step reasoning performance."

**WRONG:**
> "GPT-4o appears to outperform prior models on coding tasks."

**RIGHT:**
> "Chain-of-thought prompting improves accuracy on GSM8K from 17.9% to 56.9% for 540B
> parameter models, per controlled evaluation in [source]."

**Signal you have a hedged non-assertion:** The words "may," "might," "could," "appears
to," "suggests that," or "it is possible" appear inside the claim text itself (not in
your meta-commentary about the claim's confidence). These words void falsifiability.

**Exception:** A claim about uncertainty is assertable if the uncertainty is the finding:
"Authors report no statistically significant difference between method A and method B at
p<0.05 across three benchmark datasets" is a valid Key Claim. The finding is the
null result.

---

### Failure Mode 3: Claim Without a Traceable Source Anchor

Every Key Claim must cite the Source page that provides the specific evidence for it.
An empty or missing Source field means the claim is unsourced. Do not proceed to write
the page if you cannot fill the Source field.

**WRONG (Source field empty):**
```
| Chain-of-thought prompting outperforms standard prompting on multi-step reasoning | — | 2022 | current | 2 | false |
```

**RIGHT:**
```
| Chain-of-thought prompting outperforms standard prompting on multi-step reasoning | [[2022-wei-chain-of-thought-prompting]] | 2022 | current | 3 | false |
```

If a claim is derived from a filed query result rather than a raw source, annotate the
source field with `[derived]`: `[[topic-slug]] [derived]`. Do not leave the field blank.
Lint will not flag `[derived]`-annotated claims as sourcing gaps.

If you cannot identify a source for a claim you want to include, that claim does not
belong in the Key Claims table. It may belong in the prose body with appropriate hedging,
but not in the provenance-anchored Key Claims section.

---

### Failure Mode 4: Overcounting — More Than 5 Claims

The 3–5 claim rule is a quality constraint, not a suggestion. Extracting more than 5
claims signals either failure to apply the assertable/specific/non-compound tests, or
extraction of low-salience detail that belongs in prose rather than Key Claims.

**WRONG (7 claims for a tool page, several of which are metadata or low-salience):**
```
| GPT-4o supports function calling | ... |
| GPT-4o supports JSON mode | ... |
| GPT-4o has a 128K context window | ... |
| GPT-4o achieves 87.5% on MMLU | ... |
| GPT-4o supports vision, audio, and text input | ... |
| GPT-4o is priced at $5 per 1M input tokens | ... |
| GPT-4o was released in May 2024 | ... |
```

Apply the following reduction procedure when you have more than 5 candidate claims:

1. **Specificity filter:** Discard any claim without at least one measured quantity, named
   entity, or named condition. "Supports function calling" fails specificity — "supports
   function calling with parallel invocation of up to 128 functions per request" passes.
2. **Metadata filter:** Release dates belong in frontmatter, not Key Claims.
3. **Recency filter:** Among remaining claims, prefer those with the most recent source
   dates or highest support scores.
4. **Salience filter:** Prefer claims directly relevant to the page's primary query patterns
   (landscape/comparison queries, pitfalls queries). Feature presence flags are lower
   salience than performance findings.

**RIGHT (5 claims after applying filters):**
```
| GPT-4o achieves 87.5% on MMLU, a 3.1 pp improvement over GPT-4 Turbo | [[2024-openai-gpt4o-system-card]] | 2024 | current | 2 | false |
| GPT-4o supports a 128K token context window | [[2024-openai-gpt4o-system-card]] | 2024 | current | 2 | false |
| GPT-4o processes vision, audio, and text natively in a single model | [[2024-openai-gpt4o-system-card]] | 2024 | current | 2 | false |
| GPT-4o input pricing is $5 per 1M tokens, half the cost of GPT-4 Turbo at launch | [[2024-openai-gpt4o-system-card]] | 2024 | current | 2 | false |
| GPT-4o scores lower on RealToxicityPrompts than GPT-4 Turbo under identical prompting conditions | [[2024-openai-gpt4o-system-card]] | 2024 | current | 2 | false |
```

Note: the pricing claim was retained here because it is quantified, has a specific
comparison baseline, and is time-sensitive — making it a higher-value Key Claim than a
plain feature flag.

---

### Failure Mode 5: Undercounting by Merging Distinct Claims

The opposite error: combining two independently assertable claims into one compound
sentence to stay under the 5-claim ceiling. This conceals two independent provenance
trails in one row. If either half is later contested or superseded, the entire row
must change status.

**WRONG:**
> "GPT-4o achieves 87.5% on MMLU and supports a 128K context window, with pricing at
> half the cost of GPT-4 Turbo."

This is three claims. Each has independent time-sensitivity, independent sources of
potential contradiction, and independent provenance. Keep them as three rows.

**Signal you have a compound claim:** The claim contains "and," ";," or a comma joining
two facts that could each stand alone. Split it.

---

## 3. Extraction Depth Behavior

### Full Depth: research-paper, white-paper, policy-document

Process section by section. For each section:
- Identify the central claim of the section, if any.
- Extract quantitative findings with their conditions, benchmark names, and comparison
  baselines. A finding without its benchmark condition is not extractable at full depth.
- Identify named entities (tools, models, methods, datasets) for entity page consideration.
  A new entity warrants a stub page only if the source dedicates at least one substantive
  paragraph to it.
- Note explicit limitations, failure conditions, or scope boundaries stated by the authors.
  These are candidates for Pitfalls pages, not Key Claims.
- **Inline images:** When the source contains an inline image that is visually referenced
  by the surrounding text and is not purely decorative (headers, logos, and layout images
  are decorative), fetch and view it. If the figure contains quantitative data or
  structural information not captured in the surrounding prose — benchmark charts, training
  curves, architecture diagrams — write a one-sentence description of the figure's key
  content in the target wiki page body at the point where the source references it.
  Do not store image files locally.

After processing all sections, apply the 3–5 claim filter. Select the most
consequential claims by the following priority:

1. Quantitative findings with benchmark names, conditions, and comparison baselines.
2. Findings that directly constrain or enable a named workflow or methodology.
3. Findings that introduce a new named entity to the field.
4. Definitional claims that other Key Claims in the wiki depend on.

**Do not include** section headers, scope statements ("this paper examines..."), or
authors' future work proposals as Key Claims candidates.

### Standard Depth: all other source types

Treat the source as a unit. Extract:
- The central argument (one sentence, used for the Source page summary — not itself
  a Key Claim).
- Up to 5 Key Claims using the priority ordering above.
- Named entities warranting stub page creation.

Do not scan section-by-section for standard-depth sources. Read the source as a whole,
identify the most specific and consequential assertions, and apply the 3–5 claim filter.

If the source lacks an identifiable central argument after full reading, that is a signal
the source is low-salience or poorly structured. Surface this to the human rather than
fabricating structure: "This source does not have a clear central argument. Options: (A)
proceed with extraction of individual claims only, (B) classify as collection gap filler
and extract no Key Claims, (C) skip this source."

---

## 4. vendor_bias Annotation Format

Apply when `source_type: vendor-content`. The `vendor_bias` flag is set on the Source
page. During extraction, annotate every Key Claim that touches competitive landscape,
comparative capability claims, or product limitations with a prose annotation.

**Annotation format in prose:**
Append to the sentence in question: *(vendor-sourced — treat comparative claims with caution)*

**Claims that require the annotation:**
- Any claim comparing the vendor's product to a competitor by name.
- Any claim about the absence or resolution of limitations in the vendor's product.
- Any comparative performance claim for which no independent corroboration exists in the wiki.

**Claims that do NOT require the annotation:**
- Factual pricing stated in the source (objectively verifiable).
- Release dates (objectively verifiable).
- API specification details (objectively verifiable from published documentation).
- Usage requirements and access tiers (objectively verifiable).

**Key Claims table behavior:** No special annotation in the Key Claims table row itself.
The `source_type` field on the Source page carries the machine-readable signal. The prose
annotation is the human-visible warning when reading the page.

---

## 5. Spot-Check Block Format

Required in the post-ingest summary for every source with
`source_type: research-paper` or `source_type: policy-document`.

This is an internal fidelity check — it allows the wiki owner to verify that extracted
claims are grounded in specific source passages, not fabricated or generalized. It is
not a public citation.

**Format:**
```
Spot-check — [[source-slug]]:
  Claim: [exact claim text as written in the Key Claims table]
  Source passage: "[verbatim clause from source that supports this claim, under 15 words]"
  ...repeat for each Key Claim extracted from this source...
```

**If you cannot identify a verbatim passage supporting a Key Claim:**
This is an extraction error. Stop and surface it before completing the ingest. Either:
- The claim is a topic label (too general to trace to a specific passage) — rewrite or discard.
- The claim is fabricated (no supporting passage exists) — discard immediately.
- The claim is a valid inference from multiple passages (not directly stated) — move it
  to prose with appropriate hedging; it does not belong in Key Claims.

Do not produce a spot-check block for standard-depth sources. The block is only required
for full-depth (peer-reviewed paper, white-paper, policy-document) extraction.

---

## 6. TO BE ENRICHED from Operational Experience

The following sections should be populated after the first five ingest operations.
Until then, the rules above are the operative guidance.

**6.1 Additional Failure Mode Examples**

*Case: Truncated staged file — URL fallback (2026-04-22)*

Staged file "AI Teaching Strategies.md" existed in `raw/staged/` but contained only
the article introduction; the body was absent (truncated on copy-paste). The extraction
candidate list after Step 11 would have yielded zero claims — only introductory framing
was present.

**Signal:** A staged file ends within the first section, or reading the file reveals
only a heading and a paragraph with no substantive procedural or empirical content.

**Correct behavior:** Surface as a pre-flight forced choice before extraction begins.
Do not attempt extraction from a truncated file — the claim list will be empty or
misleading. Forced choice options: (A) fetch full content from URL, (B) skip this
source. If the URL is unavailable, tag `[fetch-failed]` and move on.

The URL fetch in this case succeeded via subagent even though a prior session had
received a 403 from the same URL, suggesting intermittent access rather than a
permanent block. Do not assume a prior `[fetch-failed]` tag is permanent.

**6.2 Full-Depth Extraction Edge Cases**
Populate when a peer-reviewed source has non-standard section structure (e.g., a paper
organized as a position paper rather than as methods/results, or a policy document with
annex-heavy structure where the normative content is distributed across annexes).

**6.3 vendor_bias Edge Cases**
Populate with cases where a non-vendor-content source contains vendor-favorable claims
(e.g., a practitioner blog sponsored by a vendor, or a white-paper co-authored with
a vendor). The formal source type field will not carry the vendor_bias flag in these
cases, but the extraction should note the potential bias.

**6.4 Claim Calibration for Narrow Sources**
Some sources are highly focused (e.g., a benchmark paper reporting a single finding
for a single model). For these, 3 claims may be the right count even if the source
is full-depth. Populate this section with calibration examples from early operation.