# TAGGING-SKILL.md — Teaching Relevance Tagging Skill File

**Purpose:** Read this file before any ingest operation that involves teaching relevance
tagging. It provides tagging rules, controlled vocabulary, decision procedure, and worked
examples. It is self-contained — you do not need to cross-reference CLAUDE.md Sections
7.1–7.3 to apply the vocabulary correctly.

**Scope:** `teaching_relevance` field, `competency_domains` field,
`professional_contexts` field on Topic, Tool/Product, and Pitfalls pages.

**Version:** Starter template. Sections marked TO BE ENRICHED require real operational
cases before they are complete. Treat this file as scaffolding, not finished guidance.

---

## 1. Controlled Vocabulary

These are the only permitted values for `competency_domains` and `professional_contexts`.
Do not use values outside these lists. Do not paraphrase or shorten them. If a concept
does not map to any existing term, surface the gap rather than inventing a new tag.

### 1.1 Professional Competency Domains

| Value (use exactly as shown) | Covers |
|---|---|
| `tool-evaluation-and-selection` | Assessing and choosing AI tools for specific use cases |
| `practical-ai-use-and-interaction` | Task-level use: prompting, iteration, output refinement |
| `ai-integration-in-organizational-workflows` | Embedding AI into multi-actor processes with accountability structures |
| `output-verification-and-risk-assessment` | Checking outputs and evaluating workflow failure modes |
| `ai-safety-and-alignment-literacy` | Understanding alignment tradeoffs and safety-relevant behaviors |
| `capability-horizon-awareness` | Tracking emerging capabilities and their taxonomies |
| `attribution-ip-and-professional-integrity` | Attribution norms, IP considerations, and disclosure practices across academic and professional contexts |

### 1.2 Professional Context Terms

| Value (use exactly as shown) |
|---|
| `activism-and-civic-advocacy` |
| `non-profit-and-ngo-work` |
| `journalism-and-media` |
| `legal-practice` |
| `domestic-civil-service-and-public-administration` |
| `foreign-service-and-diplomacy` |
| `organizational-leadership-and-change-management` |
| `project-and-program-management` |
| `teaching-and-instruction` |
| `graduate-and-doctoral-education` |
| `professional-and-continuing-education` |
| `entrepreneurship-and-startups` |

---

## 2. Tagging Decision Procedure

Execute these steps in order. Do not skip steps. Do not propose tags without completing
the full procedure.

**Step 1 — Check eligibility**

Do not propose `teaching_relevance: true` for pages with `status: stub`. Stub pages have
insufficient content to map reliably to competency domains. Wait until the page reaches
`status: developing` or higher. Record this in the pre-flight report as: "teaching
relevance deferred — page is a stub."

**Step 2 — Apply the two-criterion threshold**

Propose `teaching_relevance: true` only if the page meets at least one of:

- **Criterion A:** The page maps cleanly to two or more competency domains. "Cleanly"
  means the mapping is direct and obvious — you can point to a specific section or
  paragraph that covers the domain without any interpretive stretch.
- **Criterion B:** The page maps strongly to one competency domain with substantive
  coverage — multiple paragraphs, not a passing mention.

If neither criterion is met: do not propose the tag. The human can set it manually.
Do not adjust a domain definition to reach the threshold.

**Step 3 — Apply the clean-mapping test to each proposed domain**

For each domain you are considering proposing: identify the specific section or paragraph
that covers it. Ask: does a student or professional reading this domain definition and
this page section immediately see the connection, without inferring or bridging?

- If yes: include the domain.
- If no: exclude the domain. Record the near-miss in the forced choice if the human may
  want to make their own judgment (option B in the forced choice block).

**Step 4 — Assign professional contexts**

Professional contexts are secondary to competency domains. A context is appropriate when
the page's content has direct bearing on AI use in that specific professional setting —
not merely because that profession uses AI at all.

Apply the same clean-mapping test: does the page contain content specifically useful to
practitioners in that context? Useful means actionable or directly informative for
decisions that context faces. Do not tag by subject area overlap alone.

A page about AI in legal research is not automatically relevant to `legal-practice`
unless it contains material about legal-specific considerations: privilege, admissibility,
citation standards, or ethics rules, for example.

**Step 5 — Select the minimum sufficient set of domains**

The `competency_domains` field is not a tag cloud. Over-tagging distributes the page
into Teaching Index bins where it does not add genuine value. Apply a maximum of three
competency domains per page. If more than three pass the clean-mapping test, select the
three with the most substantive coverage on this specific page.

**Step 6 — Format the forced choice**

```
[N] teaching_relevance proposed: [[page-slug]]
    Proposed domains: {domain-1}, {domain-2}
    A) Confirm — tag with proposed domains
    B) Confirm with edits — I will specify domains
    C) Decline
```

---

## 3. Worked Examples

### Example A — Clear Positive

**Page:** `topics/retrieval-augmented-generation.md`
**Content:** A 700-word developing-status page covering RAG architecture choices, retrieval
quality tradeoffs, chunking strategies, re-ranking methods, and documented failure modes
in enterprise deployment.

**Step 1:** Page status is `developing`. Eligible.

**Step 2:** Criterion A check.
- `tool-evaluation-and-selection`: The page covers how to evaluate RAG retrieval components
  (chunking strategies, re-ranking choices). Direct mapping — a section is dedicated to
  this. ✓
- `ai-integration-in-organizational-workflows`: The page covers enterprise deployment with
  discussion of accountability for retrieval errors in multi-actor pipelines. Direct
  mapping. ✓
- `output-verification-and-risk-assessment`: The failure modes section covers how to
  detect and handle retrieval failures. Direct mapping. ✓
- `practical-ai-use-and-interaction`: Chunking and prompting content exists. Near mapping —
  the page is not primarily about task-level prompting; it is about architecture. Borderline.

Criterion A is met (three clean domain mappings). Proceed to domain selection.

**Step 3:** Clean-mapping test applied above. `practical-ai-use-and-interaction` does not
pass cleanly — exclude it.

**Step 4:** Contexts. The content is actionable for teams embedding AI into knowledge
workflows — `project-and-program-management` and `organizational-leadership-and-change-management`
are supported by the enterprise deployment content.

**Step 5:** Three domains suffice. No reduction needed.

**Forced choice output:**
```
[N] teaching_relevance proposed: [[retrieval-augmented-generation]]
    Proposed domains: tool-evaluation-and-selection,
                      ai-integration-in-organizational-workflows,
                      output-verification-and-risk-assessment
    Proposed contexts: project-and-program-management,
                       organizational-leadership-and-change-management
    A) Confirm — tag with proposed domains and contexts
    B) Confirm with edits — I will specify domains/contexts
    C) Decline
```

---

### Example B — Clear Negative

**Page:** `tools/openai-whisper.md`
**Content:** A page about OpenAI Whisper, a speech-to-text model. Covers accuracy
benchmarks across languages, API integration steps, and error rates on technical speech.

**Step 1:** Page status is `developing`. Eligible.

**Step 2:** Criterion check.
- `tool-evaluation-and-selection`: The page covers benchmarks. However, it is a single
  tool's benchmarks, not evaluation methodology for selecting among tools. Near miss —
  does not pass the clean-mapping test.
- `practical-ai-use-and-interaction`: The API integration section covers task-level use.
  But it is a thin section — not substantive multi-paragraph coverage.
- `ai-integration-in-organizational-workflows`: Not covered.
- `output-verification-and-risk-assessment`: Error rates are mentioned but not as
  verification methodology — they appear as product characterization.
- `ai-safety-and-alignment-literacy`: Not covered.
- `capability-horizon-awareness`: The model exists. That alone is not coverage of the
  capability horizon tracking domain.
- `attribution-ip-and-professional-integrity`: Not covered.

Criterion A: No two clean domain mappings. Criterion B: No single domain with substantive
coverage. Neither criterion met.

**Decision:** Do not propose `teaching_relevance: true`. No forced choice generated.

---

### Example C — Borderline Case (Two-Domain Confidence Threshold)

**Page:** `topics/prompt-injection.md`
**Content:** A 650-word developing-status page covering prompt injection attack types
(direct, indirect), documented real-world exploitation cases, and defensive strategies
(input sanitization, sandboxed execution, system prompt hardening).

**Step 1:** Page status is `developing`. Eligible.

**Step 2:** Criterion check.
- `ai-safety-and-alignment-literacy`: The page directly addresses safety-relevant
  adversarial behaviors and their real-world consequences. Multiple substantive paragraphs.
  Criterion B is met by this domain alone.
- `output-verification-and-risk-assessment`: The defenses section covers detection and
  mitigation. This is a near-clean mapping — but the page's primary focus is the attack
  mechanism, not a verification methodology. The defenses are described as countermeasures,
  not as a systematic verification practice.

**Step 3:** Clean-mapping test for `output-verification-and-risk-assessment`. Can a student
reading the domain definition ("Checking outputs and evaluating workflow failure modes")
and the page's defenses section immediately see the connection? The defenses section
describes how to reduce attack surface, not how to evaluate output correctness. The
mapping requires a bridging step: "defenses against injection → this is a form of risk
assessment." That bridging step fails the clean-mapping test.

**Step 4:** Contexts. Prompt injection is directly relevant to practitioners responsible
for deploying AI-integrated systems: `project-and-program-management`. Organizations
deploying AI agents face this as a concrete operational risk: `organizational-leadership-and-change-management`.

**Step 5:** One confirmed domain plus contexts.

**Forced choice output:**
```
[N] teaching_relevance proposed: [[prompt-injection]]
    Proposed domains: ai-safety-and-alignment-literacy
    Proposed contexts: project-and-program-management,
                       organizational-leadership-and-change-management
    A) Confirm — tag with proposed domains and contexts
    B) Confirm with edits — I will specify domains/contexts
    C) Decline
```

Note on the borderline domain: if you believe `output-verification-and-risk-assessment`
is defensible for this page, option B in the forced choice allows the human to add it.
Do not add it yourself — the clean-mapping test failed.

---

## 4. Common Tagging Errors

**Error 1: Tagging by subject relevance, not domain coverage**
A page about AI tool adoption in nonprofit organizations does not automatically warrant
`non-profit-and-ngo-work` in `professional_contexts`. It must contain content specifically
useful to non-profit practitioners — e.g., budget constraint considerations, volunteer
management constraints, grant reporting implications of AI outputs. Subject matter overlap
is not sufficient.

**Error 2: Applying all plausible domains**
Applying five competency domains when three pass the clean-mapping test distributes the
page across five Teaching Index bins. In two of those bins, the page will appear alongside
pages that substantively cover the domain — and this page will be the weakest entry. That
degrades the Teaching Index quality. Apply the minimum sufficient set.

**Error 3: Tagging stub pages**
A stub page has 1–3 Key Claims and a 2–4 sentence prose opening. This is not enough
content to map reliably to competency domains. The tagging will be revised when the page
develops, wasting a forced choice. Defer and note the deferral.

**Error 4: Proposing `teaching_relevance: true` for Source pages**
Source pages are ingestion records, not synthesis pages. They document provenance, not
actionable knowledge. Never propose teaching relevance tagging for Source pages.

**Error 5: Using domains as synonyms**
`practical-ai-use-and-interaction` (task-level prompting, iteration) and
`ai-integration-in-organizational-workflows` (multi-actor processes, accountability
structures) are distinct. A page about effective prompting techniques is not about
organizational integration. A page about AI governance in enterprise workflows is not
primarily about task-level prompting. Apply each only to the specific scope it covers.

---

## 5. TO BE ENRICHED from Operational Experience

**5.1 Tool Page Examples**

*Case: teaching_relevance gated by source quality, not topic (2026-04-22)*

Two tool pages created in the same session required opposite `teaching_relevance`
decisions, illustrating that the decision gates on source quality as much as topic fit.

**`google-notebooklm` — tagged `teaching_relevance: true`**
Source: practitioner blog (industry-blog, practitioner tier). The page describes the
tool's behavior and use cases clearly; Key Claims are observable product behaviors,
not vendor assertions. Tags assigned: `practical-ai-use-and-interaction` +
`tool-evaluation-and-selection`. Professional contexts: `teaching-and-instruction`,
`graduate-and-doctoral-education`, `journalism-and-media`. Technical depth: foundational.
The tool warrants both domains because it covers task-level use (how to interact with it)
and selection criteria (when to choose it over alternatives).

**`mindstudio` — no `teaching_relevance` tag (deferred)**
Source: vendor-content (vendor_bias: true). Every Key Claim on the page carries
a vendor-bias hedge ("vendor-sourced — treat comparative claims with caution"). A student
or instructor using this page would be unable to trust capability or comparison claims
without independent verification. Tagging it as teaching-relevant would mislead users
about the page's evidential standing.

**Rule:** When a tool page's only source is `vendor-content` and all Key Claims carry
vendor-bias annotations, defer `teaching_relevance` regardless of topic fit. Re-evaluate
after a non-vendor source is ingested for that tool.

**5.2 Pitfalls Page Examples**

*Case: Pitfalls page domain mapping varies by parent topic — not uniform across all Pitfalls pages (2026-04-26)*

Three Pitfalls pages created in the same session had different domain profiles, illustrating that the mapping is driven by the content of the failure modes, not by the fact that a page is a Pitfalls page.

**`llm-fundamentals-pitfalls`** (parent: Topic — foundational LLM mechanics)
Domains: `practical-ai-use-and-interaction` + `output-verification-and-risk-assessment`
Not tagged: `ai-safety-and-alignment-literacy` — the failure modes are operational
(context window limits, System 1 reasoning ceiling, unchecked agentic tool use, prompt
injection). These are misuse and limitation patterns, not alignment-theoretic failures.
Tagging alignment literacy here would overclaim the page's scope.

**`ai-alignment-pitfalls`** (parent: Topic — alignment research)
Domains: `ai-safety-and-alignment-literacy` + `output-verification-and-risk-assessment`
Not tagged: `practical-ai-use-and-interaction` — the failure modes are alignment-theoretic
(deceptive alignment, outer/inner alignment gap, RLHF-as-alignment substitution error).
These are research-level failure modes, not task-level use patterns.

**`llm-self-preference-bias-pitfalls`** (parent: Topic — evaluator bias in hiring contexts)
Domains: `output-verification-and-risk-assessment` + `ai-integration-in-organizational-workflows`
Not tagged: `ai-safety-and-alignment-literacy` — the failure modes are workflow design
errors (AI-generates-AI-evaluates without bias controls, treating automation as
neutrality). The compounding bias in training loops entry carries `speculative` status
and does not alone justify the alignment domain.

**Rule:** Do not default to `ai-safety-and-alignment-literacy` for all Pitfalls pages.
Read the actual failure modes and ask: are these alignment-theoretic failures (deceptive
alignment, reward hacking, goal misgeneralization, sycophancy under pressure) or
operational misuse patterns (unchecked outputs, workflow design errors, context limits,
tool integration risks)? Alignment-theoretic failures warrant `ai-safety-and-alignment-literacy`.
Operational patterns do not — `output-verification-and-risk-assessment` is sufficient.

Alignment-theoretic → include `ai-safety-and-alignment-literacy`.
Operational → `output-verification-and-risk-assessment` is sufficient.

Speculative alignment entries that are one of six failure modes do not tip the balance.

Note: the original placeholder for this section stated both domains "frequently" apply
to Pitfalls pages. That was incorrect. Only `output-verification-and-risk-assessment`
is routine; `ai-safety-and-alignment-literacy` is conditional on failure mode type.

**5.3 Calibration for Less-Obvious Domain Mappings**
`attribution-ip-and-professional-integrity` and `capability-horizon-awareness` are the
two domains most likely to produce borderline cases in this wiki's domain. Populate with
calibration examples after the first ten ingest operations.

**5.4 Systematic Under-Tagging Detection**
If the lint teaching relevance ratio check (CLAUDE.md Section 10) fires below 20%,
review recent decisions against these examples to determine whether the clean-mapping
test is being applied too conservatively. Document the calibration adjustment here.