# Decisions Made
**Last Updated:** 29/04/2026 14:30

Append-only log of non-obvious decisions made during this project.
"Non-obvious" means: a competent person could reasonably have chosen differently,
or the decision has meaningful consequences if reversed later.

Reference format from other documents: `# See DM-NNN`

**Mutability rules:**
- Append only. Never edit an existing entry's decision, rationale, context, or alternatives.
- If a decision is **amended** (modified but still directionally valid): add `Amended By: DM-NNN`
  to the original entry — this is the only permitted in-place edit — then create a new entry
  explaining what changed and why, referencing the original.
- If a decision is **superseded** (reversed or replaced entirely): add `Superseded By: DM-NNN`
  to the original entry, then create a new entry explaining the reversal and its rationale.
- Before any implementation-relevant chat: scan this file for entries that the proposed work
  might contradict. Surface conflicts before proceeding.

---

## Entry Template

```
## DM-NNN | [SHORT DESCRIPTIVE TITLE]

- **Date:** YYYY-MM-DD
- **Status:** ACTIVE | AMENDED | SUPERSEDED
- **Amended By:** DM-NNN       ← populate only if Status is AMENDED
- **Superseded By:** DM-NNN   ← populate only if Status is SUPERSEDED

**Decision:**
[One unambiguous statement of what was decided.]

**Context:**
[What problem or situation prompted this decision.]

**Rationale:**
[Why this option was chosen.]

**Alternatives Considered:**
- **[Option A]:** [Why ruled out]

**Consequences to Watch:**
[Observable conditions that would signal this decision needs revisiting.]

**References:** IN-NNN, LL-NNN
```

---

## DM-001 | Adopt Three-Document Governance Structure

- **Date:** 2026-04-14
- **Status:** ACTIVE

**Decision:**
This project will be governed by three persistent documents: `info_needs.md`, `decisions_made.md`, and `lessons_learned.md`. Each is maintained according to templates and update procedures agreed at project initialization.

**Context:**
This project spans multiple chat sessions with no persistent cross-session memory by default.

**Rationale:**
The three-document structure maps directly to three distinct failure modes: unresolved ambiguity, revisited decisions, and repeated mistakes. Each document has a mutability model matched to its purpose.

**Alternatives Considered:**
- **Single running notes document:** Undifferentiated; open questions and closed decisions intermingle.
- **Rely on Claude memory system:** Probabilistic and recency-biased; inadequate for authoritative tracking.
- **External project management tool:** Not accessible within this Claude Project without integration overhead.

**Consequences to Watch:**
- If documents grow too long to scan quickly, the end-of-chat ritual will be skipped in practice.
- If documents are not consulted at the start of implementation-relevant chats, the system provides no protection.

**References:** —

---

## DM-002 | This Project Is Design-Only, Not Implementation

- **Date:** 2026-04-14
- **Status:** ACTIVE

**Decision:**
This Claude Project is scoped to designing the wiki — producing schemas, workflows, specifications, and architectural guidance. It is not the execution environment for the wiki.

**Context:**
Clarified by the user after initial project setup.

**Rationale:**
Design and execution require different modes. Conflating them leads to designing-as-you-go, which is the primary driver of schema drift.

**Alternatives Considered:**
- **Design and execute in the same project:** Removes the forcing function to fully specify the schema before ingesting sources.

**Consequences to Watch:**
- Design artifacts must be portable to the eventual execution environment.
- Resist beginning source ingest before schema is stable.

**References:** IN-001, IN-002, IN-005

---

## DM-003 | Contradiction Resolution Protocol Direction

- **Date:** 2026-04-15
- **Status:** AMENDED
- **Amended By:** DM-023

**Decision:**
When a new source contradicts an existing wiki page, the LLM resolves the contradiction, updates the page, and flags the decision with explicit rationale. A 7-day human override window applies. Inaction auto-confirms.

**Context:**
The team ingests sources several times per week. A model requiring human approval before any wiki update would create a review backlog.

**Rationale:**
LLM-decides-with-flag threads the needle: the wiki always moves forward, but every contradiction resolution is visible and reversible.

**Alternatives Considered:**
- **LLM flags and waits:** Creates backlog, stalls wiki. Ruled out.
- **LLM overwrites silently:** Loses provenance trail. Ruled out.
- **Human always decides:** Too labor-intensive at this ingest cadence. Ruled out.

**Consequences to Watch:**
- High rate of auto-confirmations with no human review may signal window needs shortening.
- Frequent human overrides signal LLM resolution logic needs review.

**References:** IN-004

---

## DM-004 | Query Pattern Taxonomy Established

- **Date:** 2026-04-15
- **Status:** ACTIVE

**Decision:**
Five named query patterns: (1) landscape/comparison, (2) synthesis/evolution, (3) implementation details under tool constraints, (4) discovery/recommendation, (5) pitfalls/failure modes.

**Context:**
Query patterns are the primary driver of page type design and frontmatter structure.

**Rationale:**
Derived directly from stated team use cases. Pitfalls separated from synthesis because it has a distinct temporal spine.

**Alternatives Considered:**
- **Collapse pitfalls into synthesis:** Ruled out — different structural requirements.

**Consequences to Watch:**
- If a recurring query type emerges that does not map to any of the five patterns, add it and assess whether a new page type is required.

**References:** IN-001

---

## DM-005 | RAG Use Case Held Open

- **Date:** 2026-04-15
- **Status:** ACTIVE

**Decision:**
The use case of wiki pages as runtime agent input is held open. Schema design treats RAG as a live structural constraint.

**Context:**
Eliminating RAG reduces page structure constraints but trades away a named capability: competing methodologies programmatically.

**Rationale:**
Asymmetry favors keeping it open. Adding RAG back after schema design requires a revision.

**Alternatives Considered:**
- **Eliminate RAG now:** Loses methodology comparison at scale. Cannot be re-added without schema revision.
- **Commit to full RAG support now:** Premature. Cost unknown before schema design.

**Consequences to Watch:**
- If RAG support requires page structure so rigid it compromises human readability, revisit.
- If team does not use programmatic wiki queries within first six months, reconsider structural overhead.

**References:** IN-001, IN-002, IN-005

---

## DM-006 | Staleness Tracking via Key Claims Section

- **Date:** 2026-04-15
- **Status:** ACTIVE

**Decision:**
Wiki pages use a hybrid staleness model: narrative prose uses rolling overwrite; each page carries a Key Claims section containing 3–5 consequential claims each tagged with source and date.

**Context:**
Full claim-level annotation assessed as too burdensome. Page-level date alone assessed as too coarse.

**Rationale:**
Key Claims concentrates provenance effort where it has the highest value without requiring annotation of every sentence.

**Alternatives Considered:**
- **Full claim-level annotation:** Unsustainable at ingest cadence.
- **Page-level last-reviewed date only:** Too coarse for this domain's velocity.
- **Rolling overwrite with no provenance:** Loses ability to track claim evolution.

**Consequences to Watch:**
- If LLM consistently produces more or fewer than 3–5 Key Claims per page, tighten guidance.
- If Key Claims sections drift in format, the spec needs more prescriptive examples.

**References:** IN-001, IN-002, DM-005

---

## DM-007 | Execution Environment Stack Confirmed

- **Date:** 2026-04-16
- **Status:** ACTIVE

**Decision:**
Stack: Claude Code (Pro tier, $20/month) as wiki maintenance agent; git repository as wiki store; Obsidian as local reading interface; Quartz on GitHub Pages as public-facing published site.

**Context:**
Team needed fixed-cost execution with filesystem access, Obsidian compatibility, and a shareable URL without paid hosting.

**Rationale:**
Claude Code Pro is fixed-cost at the team's ingest cadence. Quartz is purpose-built for publishing Obsidian-style markdown wikis. GitHub Pages is free for public sites.

**Alternatives Considered:**
- **Claude.ai Projects:** No filesystem write access. Ruled out.
- **Custom API harness:** Variable cost, maintenance burden. Ruled out.
- **Private GitHub Pages:** Requires paid plan. Ruled out.

**Consequences to Watch:**
- If Claude Code Pro token limits are hit regularly, evaluate Max 5x or API pay-as-you-go.
- If wiki scale creates Quartz build time constraints, evaluate self-hosted deployment.

**References:** IN-005, DM-002

---

## DM-008 | Graphics Strategy: Mermaid First-Class, Assets Directory for Static Images

- **Date:** 2026-04-16
- **Status:** ACTIVE

**Decision:**
Mermaid diagrams are first-class. Static images stored in `assets/`. AI-generated imagery out of scope.

**Context:**
Three distinct categories of visual content with different answers.

**Rationale:**
Mermaid is text-based, version-controlled, renders natively in both Obsidian and Quartz.

**Alternatives Considered:**
- **External image URLs:** Brittle; URLs break over time.
- **AI image generation in workflow:** Claude Code cannot generate images.

**Consequences to Watch:**
- If Mermaid proves insufficient for a class of visual, assess lightweight diagramming tool with SVG export.
- If assets/ grows large, evaluate Git LFS.

**References:** IN-005

---

## DM-009 | Page Type Taxonomy Established

- **Date:** 2026-04-17
- **Status:** ACTIVE

**Decision:**
Seven named page types: Topic, Tool/Product, Source, Comparison, Pitfalls, Overview, Log.

**Context:**
Page type taxonomy is the foundational schema decision.

**Rationale:**
Seven types emerged from analysis of the five query patterns, the staleness model, and the RAG hold-open.

**Alternatives Considered:**
- **Merge Tool into Topic with tags:** Lifecycle metadata differs enough to justify distinct type.
- **Merge Source into Topic:** Destroys provenance chain.
- **Merge Pitfalls into Topic/Tool:** Pitfalls temporal structure incompatible with synthesis page design.

**Consequences to Watch:**
- If a recurring page need emerges that maps to no existing type, assess whether a new type is warranted.

**References:** IN-002, DM-004, DM-005, DM-006

---

## DM-010 | Teaching Index Structure: Professional Competency and Context Axes

- **Date:** 2026-04-17
- **Status:** ACTIVE

**Decision:**
Teaching Index is a derived artifact organized by professional competency domain (primary axis) and professional context (secondary axis). Both vocabularies are controlled and extensible only by schema revision.

**Context:**
Wiki serves a curriculum support use case: professors query it to inform teaching of non-technical students entering an AI-transformed workforce.

**Rationale:**
Organizing by professional competency rather than academic task makes the Teaching Index durable beyond the classroom.

**Alternatives Considered:**
- **Pitfalls-only teaching index:** Incomplete for workforce preparation framing.
- **Dedicated Teaching page type:** Creates parallel maintenance obligation and duplication.
- **Organize by academic task:** Frames AI competency as assignment-completion; becomes obsolete at graduation.

**Consequences to Watch:**
- If LLM applies teaching_relevance tags inconsistently, tighten schema tagging criteria.
- If competency domain vocabulary proves too coarse, expand during schema revision.

**References:** IN-002, DM-004, DM-009

---

## DM-011 | Pitfalls Page Category Structure

- **Date:** 2026-04-17
- **Status:** ACTIVE

**Decision:**
Three mandatory subsections: Technical Limitations, Usage Antipatterns, Alignment and Safety Concerns. Cross-cutting usage antipatterns belong on Topic-scoped Pitfalls pages. Each failure mode carries an explicit status field.

**Context:**
Without explicit category names, LLM defaults to technical limitations and underweights the other two.

**Rationale:**
Named subsections enforce coverage. Status field per failure mode required for the pitfalls query pattern.

**Alternatives Considered:**
- **Free-form pitfalls prose:** LLM defaults to technical framing; other categories underrepresented.
- **Pedagogical Considerations as fourth category:** A reframing of usage antipatterns, not a distinct category.

**Consequences to Watch:**
- If three-category structure produces consistently empty sections, assess whether category is optional for Tool-scoped pages.

**References:** IN-002, DM-004, DM-009, DM-010

---

## DM-012 | Controlled Vocabularies Locked

- **Date:** 2026-04-17
- **Status:** ACTIVE

**Decision:**
Two controlled vocabularies finalized: 7 Professional Competency Domains, 12 Professional Context Terms. Both extensible only by schema revision and amending DM entry.

**Context:**
Consistent tagging across hundreds of pages requires a stable, bounded set of terms.

**Rationale:**
Pre-defined vocabularies prevent tagging drift that makes the Teaching Index unreliable.

**Alternatives Considered:**
- **Keep Output Verification and Risk Assessment separate:** Distinction too fine for reliable tagger discrimination.
- **Keep compound education terms:** Graduate and CPE professionals have different AI competency profiles.

**Consequences to Watch:**
- If LLM applies competency domain tags inconsistently, tighten criteria with examples.
- If new professional contexts emerge that are materially distinct, add via schema revision.

**References:** DM-009, DM-010, IN-001, IN-002

---

## DM-013 | Frontmatter Specification Settled

- **Date:** 2026-04-17
- **Status:** ACTIVE

**Decision:**
Cross-cutting frontmatter decisions: `last_assessed` replaces `last_reviewed`; `credibility_tier` is LLM-assigned at ingest; RAG tension resolved as list-of-brief-strings now; full-path wikilinks in `entities_compared` and `parent_entity`.

**Context:**
IN-002 frontmatter design surfaced several ambiguities requiring explicit resolution.

**Rationale:**
`last_assessed` accurately describes the mechanism. LLM-assigned tier minimizes human intervention. List-of-brief-strings preserves partial RAG utility without premature rigidity.

**Alternatives Considered:**
- **`last_reviewed` as human-set field:** Does not scale past ~50 pages.
- **Human-assigned credibility_tier:** Creates mandatory human checkpoint at ingest.
- **Full YAML objects for capabilities/limitations now:** Cost unknown before RAG activation.

**Consequences to Watch:**
- If credibility_tier assignment produces inconsistent results, revisit logic during IN-003 design.
- If RAG use case is activated, revise capabilities/limitations to typed YAML objects.

**References:** DM-005, DM-006, IN-002, IN-003

---

## DM-014 | Naming Conventions and Directory Structure

- **Date:** 2026-04-17
- **Status:** ACTIVE

**Decision:**
All-lowercase kebab-case filenames. Type subdirectories at repo root. Per-type naming patterns established. Source slugs generated by Claude Code. Human does not set source filenames.

**Context:**
Naming conventions must satisfy Obsidian, Quartz, and Claude Code CLI simultaneously.

**Rationale:**
Kebab-case is the intersection of all three environment constraints. Mandatory vendor prefix prevents collision. Year prefix enables chronological sorting.

**Alternatives Considered:**
- **Spaces in filenames:** CLI quoting friction; %20 URLs in Quartz.
- **Uppercase permitted:** Silent collision risk on macOS; breaks on Linux CI.
- **Human-assigned source filenames:** Inconsistent at scale.

**Consequences to Watch:**
- If Quartz ignorePatterns not configured correctly, operational files render as wiki pages.
- If generated slugs collide, tighten slug generation rule.

**References:** DM-007, DM-008, IN-002, IN-005

---

## DM-015 | Version Handling for Tool/Product Pages

- **Date:** 2026-04-17
- **Status:** ACTIVE

**Decision:**
Model-class tools: one page per named active version, version identifier encoded in filename at creation. Application-class tools: rolling overwrite, single page.

**Context:**
Two distinct versioning patterns in the AI tool landscape require different handling.

**Rationale:**
Categorical split handles both patterns without namespace proliferation or loss of comparison precision.

**Alternatives Considered:**
- **Rolling overwrite for all tools:** Cannot represent simultaneously-active versions.
- **One page per version for all tools:** Unnecessary proliferation for application tools.
- **Family page plus version pages:** Comparison pages already serve that function.

**Consequences to Watch:**
- If model-class vs. application-class distinction is ambiguous at ingest, schema must provide examples.
- If deprecated page accumulation becomes a navigation problem, assess deprecated/ subdirectory.

**References:** DM-009, DM-013, DM-014, IN-003

---

## DM-016 | CLAUDE.md Added as Primary Design Artifact and Project File

- **Date:** 2026-04-17
- **Status:** ACTIVE

**Decision:**
A working CLAUDE.md draft is added as a fifth project file, maintained in place and updated at the end of any chat that confirms new design decisions.

**Context:**
As schema design progressed, the gap between governance records and the actual executable schema document widened.

**Rationale:**
A working draft is the synthesized output of design decisions. decisions_made.md serves future design sessions; CLAUDE.md serves the wiki-executing agent.

**Alternatives Considered:**
- **Rely on decisions_made.md:** Requires manual reconstruction of schema state.
- **Draft CLAUDE.md only at project end:** Defers highest-value synthesis; increases risk of gaps.

**Consequences to Watch:**
- If CLAUDE.md and decisions_made.md diverge on schema state, CLAUDE.md is wrong.
- If CLAUDE.md grows too long for a single context window, assess structural splitting.

**References:** IN-002, DM-002

---

## DM-017 | Source Classification Taxonomy Confirmed — Eight Types

- **Date:** 2026-04-18
- **Status:** ACTIVE

**Decision:**
Eight source types confirmed: research-paper, industry-blog, white-paper, publication-article, youtube-video, practitioner-reference, vendor-content, policy-document. Each mapped to extraction depth (full or standard) and credibility tier assignment logic. Institutional tier lists are controlled and extensible only by schema revision.

**Context:**
The initial five source types left three gaps identified through test cases: informally published reference documents (Karpathy gist), vendor-produced educational content (IBM Think), and government/regulatory documents (EU AI Act, NIST AI RMF).

**Rationale:**
`practitioner-reference` captures influential informal documents whose credibility derives from author reputation rather than editorial accountability. `vendor-content` captures vendor educational hubs with a mandatory bias flag on competitive claims. `policy-document` captures binding and quasi-binding governance documents with distinct staleness behavior.

**Alternatives Considered:**
- **Keep five types and force-fit:** practitioner-reference and policy-document have meaningfully different extraction and staleness behavior.
- **Social media threads:** Signal-to-noise too low; volatile artifacts. Excluded.
- **Podcast audio:** Covered by youtube-video type with transcript-first approach.
- **Book chapters:** Copyright constraints make systematic extraction inappropriate.
- **Product documentation:** Operational reference, not synthesis material.

**Consequences to Watch:**
- If a new source type emerges that does not map to any of the eight types, assess whether a new type is warranted and log an amending decision.
- If vendor_bias flag produces inconsistent annotation behavior, tighten the annotation instruction with examples in EXTRACTION-SKILL.md.

**References:** IN-003

---

## DM-018 | YouTube Ingest: Transcript-First Approach

- **Date:** 2026-04-18
- **Status:** ACTIVE

**Decision:**
YouTube video ingest requires a human-provided transcript file as a prerequisite. Claude Code ingests the transcript, not the video URL. The Source page records both the video URL and the transcript file path in a `transcript_file` frontmatter field.

**Context:**
Claude Code cannot watch video. Without a transcript, YouTube sources cannot be processed at standard extraction depth.

**Rationale:**
Transcript-first preserves extraction quality and keeps the ingest workflow consistent across source types.

**Alternatives Considered:**
- **Treat YouTube as out-of-scope for automated ingest:** Degrades extraction quality significantly for long technical talks. Ruled out.

**Consequences to Watch:**
- If the transcript extraction tool produces poor quality output for heavily technical content, assess alternative tools.
- If transcript-first creates friction that causes YouTube sources to be skipped, assess whether lightweight ingest path is warranted.

**References:** IN-003, DM-017

---

## DM-019 | queue.md as Universal Source Intake Mechanism

- **Date:** 2026-04-18
- **Status:** ACTIVE

**Decision:**
Source intake uses two mechanisms: (a) local files in `raw/staged/`; (b) `raw/queue.md` — a plain URL list in the git repo — for queuing sources from any machine. queue.md also carries CTRD-NNN override/confirm signals (see DM-031). Syncs across machines via git.

**Context:**
File-drop-to-directory only works when the human has access to that directory.

**Rationale:**
queue.md in the git repo is accessible from any machine with git access. The CTRD-NNN syntax is syntactically distinct from URL entries and cannot be mistaken for source queue items.

**Alternatives Considered:**
- **File-drop only:** Inaccessible from machines without local wiki directory access.
- **Email-to-queue:** Requires additional tooling and a monitored inbox.

**Consequences to Watch:**
- If Claude Code's URL fetch capability is blocked for certain domains, those sources must be provided as local files.
- If queue.md accumulates a large backlog of [fetch-failed] entries, assess whether a dedicated failed-queue review step is needed.

**References:** IN-003, DM-007, DM-031

---

## DM-020 | Pre-Flight Pass Model for Human Decision Consolidation

- **Date:** 2026-04-18
- **Status:** ACTIVE

**Decision:**
The ingest workflow runs in two phases. Phase 1 (pre-flight): all classification, detection, and decision identification steps run without touching any wiki files, producing a consolidated report of all decisions requiring human input. Phase 2 (execution): fully automated after all decisions are resolved.

**Context:**
Scattering human decision points throughout a sequential workflow creates an interrupt-driven interaction model where Claude Code blocks mid-ingest waiting for responses.

**Rationale:**
Consolidating decisions into a single review block per session transforms the interaction model from interrupt-driven to review-then-execute.

**Alternatives Considered:**
- **Sequential interrupt-driven model:** Creates the bottleneck pattern that degrades system utility.
- **Fully automated with no human input:** Removes human quality gate on classification and page creation decisions.

**Consequences to Watch:**
- If pre-flight reports grow too long for a single review session, assess whether batch size limits are needed.

**References:** IN-003, DM-019

---

## DM-021 | Forced Choice Interface for All Human Decisions

- **Date:** 2026-04-18
- **Status:** ACTIVE

**Decision:**
Every human decision point uses a forced choice format: numbered items with lettered options. Human responds with a single decision string (e.g., `1:A 2:C 3:B`). No prose required.

**Context:**
Human review becoming a chore and then a bottleneck was identified as a primary risk to system utility.

**Rationale:**
Forced choices with single-character responses are the lowest-friction human interaction that still preserves meaningful choice.

**Alternatives Considered:**
- **Prose responses:** High friction; invites over-specification and back-and-forth.
- **Binary yes/no only:** Insufficient for multi-option decisions.

**Consequences to Watch:**
- If the forced choice format is used for decisions with too many options (>4), cap options at 4.

**References:** DM-020

---

## DM-022 | Proactive Discovery Pass

- **Date:** 2026-04-18
- **Status:** AMENDED
- **Amended By:** DM-039

**Decision:**
A discovery pass maintains `raw/discovery-sources.md` — a controlled feed list of institutional-tier sources to monitor. Claude Code fetches feeds, identifies items published since `last_discovery`, filters for institutional-tier sources not already in the wiki, and appends qualifying nominations to a `[nominated]` section of queue.md. Human promotes or discards nominations before they enter the ingest queue. Discovery pass is now gap-aware: nominations matching persistent gap topics are annotated and listed first (see DM-038).

**Context:**
The wiki owner does not monitor all relevant institutional sources continuously.

**Rationale:**
Scoping to institutional-tier only keeps the signal-to-noise ratio high. Separating nominated from queued prevents surprise items entering the ingest queue.

**Alternatives Considered:**
- **Include practitioner and opinion content in discovery:** Too broad; produces noise.
- **Fully automatic ingest of discovered sources:** Removes human quality gate.

**Consequences to Watch:**
- arXiv discovery requires API integration. Start with lab blog feeds only.
- If discovery nominations accumulate without human review, consider a maximum nomination age for auto-discard.

**References:** DM-019, DM-020, DM-021, DM-038

---

## DM-023 | Weighted Three-Path Contradiction Model with Score Decay

- **Date:** 2026-04-18
- **Status:** ACTIVE

**Decision:**
Contradiction resolution uses a weighted three-path model. Credibility weights: peer-reviewed=3, institutional=2, practitioner=1, community=0. Each Key Claim carries a `support_score`. Path A (auto-resolve): incoming weight exceeds existing support score by more than 2 (difference > 2, incoming > existing). Path B (flag for human review): absolute difference ≤ 2 in either direction — tested first. Path C (minority view): existing score exceeds incoming weight by more than 2. Score decay threshold: 12 months (half weight). Operational aliases: auto-resolved, human-review, minority-view.

**Context:**
The original flat flag-and-wait contradiction protocol (DM-003) required excessive human intervention at the team's ingest cadence. The Path A/B boundary was subsequently clarified: Path B takes precedence at difference=2, and Path A fires only when difference strictly exceeds 2.

**Rationale:**
Credibility-weighted evidence balance is a better proxy for epistemic quality than source count. Score decay prevents historical accumulation from suppressing correct newer claims. The Path B-first test prevents auto-resolution at near-tie boundaries where human judgment adds the most value.

**Alternatives Considered:**
- **Vote-count model:** Produces false stability — consensus that looks robust but is stale.
- **Flat flag-and-wait (DM-003 original):** Too many human touchpoints.
- **Fully automated without human review path:** Removes judgment from genuinely ambiguous cases.

**Consequences to Watch:**
- Source independence assumption: five sources citing the same upstream paper are not five independent data points.
- Credibility tier mis-assignment compounds into support score errors.
- If 12-month decay threshold produces excessive noise, adjust in CLAUDE.md and run full lint recalculation.

**References:** DM-003, IN-004

---

## DM-024 | wiki-lessons-learned.md Operational Singleton

- **Date:** 2026-04-18
- **Status:** ACTIVE

**Decision:**
`wiki-lessons-learned.md` is added as a new operational singleton — append-only, excluded from Quartz rendering, organized by operation type. Claude Code reads only the relevant section at the start of the corresponding operation. Claude Code drafts a new entry after any pass where the human overrode its decision; the human confirms or discards.

**Context:**
CLAUDE.md encodes rules but not precedents. Ambiguous cases are not covered by rules alone.

**Rationale:**
Rules + examples (skill files) + precedents (lessons learned) is the strongest consistency stack available within the confirmed environment.

**Alternatives Considered:**
- **No precedent log:** Drift accumulates silently.
- **Append to log.md:** log.md is operational; lessons learned is interpretive. Different purposes.

**Consequences to Watch:**
- If wiki-lessons-learned.md grows large, organize by operation type to enable selective reading. Already in the design.

**References:** DM-016

---

## DM-025 | Source Retraction Handling

- **Date:** 2026-04-18
- **Status:** ACTIVE

**Decision:**
Source pages carry a `status` field: `active` or `retracted`. `retracted` is set only by human manual action. When set, an immediate scoped lint pass fires on all Key Claims whose Source field references the retracted page as sole non-minority-view citation. Path B contradiction protocol applies regardless of score.

**Context:**
Retractions are infrequent but consequential. A retracted source is actively invalidated, not merely outdated.

**Rationale:**
A dedicated status field with an immediate lint trigger is the minimum necessary addition. Human-only trigger is correct — retraction is consequential enough to require explicit human awareness.

**Alternatives Considered:**
- **Rely on superseded_by:** Models succession, not invalidation.
- **Auto-detect retractions from new sources:** Claude Code cannot reliably identify retraction notices.

**Consequences to Watch:**
- If the retraction immediate lint pass is slow on a large wiki, assess whether a paginated approach is needed.

**References:** DM-023, IN-004

---

## DM-026 | Page Length Guidelines and Split Protocol

- **Date:** 2026-04-18
- **Status:** ACTIVE

**Decision:**
Topic and Tool page prose body target: 600–800 words. Hard ceiling: 1,200 words. When exceeded, Claude Code proposes a split as a forced choice. Splits require human confirmation. Section-targeted updates used for minimal-impact passes.

**Context:**
Rolling overwrite keeps content current but does not inherently keep it short.

**Rationale:**
A hard ceiling with a split protocol creates a mechanical backstop against page length creep. Human confirmation required because the wikilink graph changes when pages are split.

**Alternatives Considered:**
- **No length constraint:** Page length creep is a known failure mode at scale.
- **Auto-split without human confirmation:** Wikilink graph changes without human awareness.

**Consequences to Watch:**
- If the 1,200 word ceiling is hit frequently in early operation, the target guidance may need tightening.

**References:** IN-002

---

## DM-027 | summary Frontmatter Field on Topic and Tool Pages

- **Date:** 2026-04-18
- **Status:** ACTIVE

**Decision:**
Topic and Tool pages carry a required `summary` field: a single sentence written by Claude Code at page creation and updated on any pass that substantially revises the page.

**Context:**
Quartz native search uses page content for snippets. Summary quality directly affects search result usefulness at scale.

**Rationale:**
Minimal cost at creation; significant payoff at 200+ pages for both human navigation and any future search layer.

**Alternatives Considered:**
- **Derive summaries from page content at search time:** Less reliable; depends on search tool's extraction quality.

**Consequences to Watch:**
- If Claude Code generates summaries that are too generic or too specific, add examples to EXTRACTION-SKILL.md.

**References:** IN-006

---

## DM-028 | Schema Conformance Check in Lint

- **Date:** 2026-04-18
- **Status:** ACTIVE

**Decision:**
The lint procedure includes a schema conformance check: Claude Code samples recently updated pages and evaluates them against explicit criteria. Deviations are logged. Same deviation across three or more pages signals behavioral drift and surfaces a schema revision question.

**Context:**
Claude Code will be invoked in many separate sessions over months. Without a feedback mechanism, behavioral drift accumulates silently.

**Rationale:**
A conformance check creates the feedback loop the design otherwise lacks. It detects drift, which is the prerequisite for correction.

**Alternatives Considered:**
- **Trust CLAUDE.md rules alone:** No detection mechanism for drift.

**Consequences to Watch:**
- If the conformance check consistently flags the same deviation without schema revision addressing it, the schema instruction needs tightening with examples.

**References:** DM-016, DM-024

---

## DM-029 | Skill Files for Ingest Consistency

- **Date:** 2026-04-18
- **Status:** ACTIVE

**Decision:**
Three skill files added to wiki root: `EXTRACTION-SKILL.md`, `TAGGING-SKILL.md`, `CONTRADICTION-SKILL.md`. All excluded from Quartz rendering. Authored from early operation experience — do not exist at initial implementation.

**Context:**
CLAUDE.md encodes rules. Skill files encode examples. Concrete examples reduce variance more effectively than rules alone for judgment tasks.

**Rationale:**
Rules + examples + precedents is the strongest consistency stack available within the confirmed environment.

**Alternatives Considered:**
- **Embed examples in CLAUDE.md:** Pushes it beyond practical single-session context size.
- **Fine-tuning:** Outside the confirmed stack and cost constraints.

**Consequences to Watch:**
- If skill files are not authored from early operation, their absence degrades the consistency benefit. Prioritize EXTRACTION-SKILL.md first.

**References:** DM-024, DM-028

---

## DM-030 | Contradiction Flag Format: Frontmatter List Plus Inline Key Claims Marker

- **Date:** 2026-04-19
- **Status:** ACTIVE

**Decision:**
A Path B contradiction flag has two required components: (1) an entry in an `open_contradictions` frontmatter list on the affected page, and (2) a `contested [CTRD-NNN]` inline marker appended to the Status cell of the contested Key Claim row. Both components are required. The frontmatter entry is machine-readable by Claude Code during lint without prose scanning. The inline marker is visible to a human reading the page in Obsidian or Quartz. IDs are globally unique, zero-padded integers (`CTRD-NNN`), tracked in a new `last_contradiction_id` field on `overview.md`. Multiple CTRD IDs on a single Status cell are space-separated: `contested [CTRD-003] [CTRD-004]`.

**Context:**
The flag format needed to satisfy three constraints simultaneously: human-visible in Quartz reading view, machine-readable by Claude Code during lint, and non-disruptive to page structure.

**Rationale:**
A dedicated section on the page creates ambiguity about whether it is canonical content and requires structural surgery to remove on resolution. Frontmatter-only is invisible to Quartz readers by default. The two-component approach serves both audiences without redundant prose sections.

**Alternatives Considered:**
- **Dedicated `## Open Contradictions` section:** Higher removal risk; ambiguous canonical status.
- **Frontmatter only:** Invisible to human readers in Quartz reading view.
- **Inline marker only:** Not aggregable by lint without full-text search across every page.

**Consequences to Watch:**
- If `last_contradiction_id` on overview.md is not incremented correctly, ID collisions will occur.
- If Quartz frontmatter rendering changes to expose YAML fields, the two-component design may become redundant — one component could be dropped.

**References:** IN-004, DM-023

---

## DM-031 | Override Mechanism: queue.md CTRD-NNN Syntax with Lint Redundancy

- **Date:** 2026-04-19
- **Status:** ACTIVE

**Decision:**
The human signals contradiction override or confirmation by adding a `CTRD-NNN:override` or `CTRD-NNN:confirm` line to `raw/queue.md`. These lines are processed at the start of every lint and ingest pre-flight pass. As a redundant mechanism, open contradictions within their window are also surfaced as forced choices during lint (Step L4b) with an explicit skip option. The human need not remember the queue.md mechanism; lint will surface open items regardless.

**Context:**
A mechanism relying solely on the human remembering to act in queue.md creates a brittle single point of failure. The lint redundancy ensures open contradictions are always surfaced for human disposition.

**Rationale:**
Two mechanisms with complementary trigger points: proactive (queue.md, any time) and reactive (lint, at scheduled pass). Neither requires the other to function. Repeated skip selections in lint are valid conscious deferrals, not errors.

**Alternatives Considered:**
- **Dedicated raw/overrides.md file:** Adds a file the human must remember to check and edit. queue.md is already in the workflow.
- **Lint-only mechanism:** Requires the human to wait for lint to act on a contradiction they want to resolve immediately.
- **queue.md only:** Brittle; if the human forgets, the item only auto-confirms at window expiry.

**Consequences to Watch:**
- If queue.md accumulates many CTRD-NNN lines without lint processing them, assess whether a queue.md health check step is needed at ingest pre-flight.

**References:** DM-023, DM-030, IN-004

---

## DM-032 | Operational Aliases for Contradiction Path Labels

- **Date:** 2026-04-19
- **Status:** ACTIVE

**Decision:**
Path A/B/C labels from the design session are replaced by operational aliases in all machine-readable and human-readable field values: `auto-resolved` (Path A), `human-review` (Path B), `minority-view` (Path C). The A/B/C labels are retained as structural labels in CLAUDE.md Section 8.2 prose for explanatory purposes only. No field value in the wiki uses the letter labels.

**Context:**
Path letter labels are design-session shorthand. A maintainer reading a contradiction flag in frontmatter or a log entry during operations should not need to look up what "Path B" means.

**Rationale:**
Operational aliases are self-describing at read time. The mapping between letter labels and aliases is documented once in CLAUDE.md; the aliases carry the meaning everywhere they appear.

**Alternatives Considered:**
- **Retain letter labels in all fields:** Requires cross-referencing CLAUDE.md to interpret any flag.
- **Replace letter labels in CLAUDE.md prose too:** The structural labels aid comprehension of the three-path logic; removing them degrades the schema document's readability.

**Consequences to Watch:**
- If a new contradiction path is added, both the letter label and the operational alias must be assigned simultaneously to avoid ambiguity.

**References:** DM-023, DM-030

---

## DM-033 | Lint Procedure: Full Specification

- **Date:** 2026-04-19
- **Status:** ACTIVE

**Decision:**
Lint runs in three phases: assessment pass (L1–L14, no files written), optional human response to forced choices, execution pass. Fourteen assessment steps cover: queue.md CTRD-NNN signals, page inventory, support score recalculation, contradiction expiry (L4a), open contradiction surfacing as forced choices (L4b), staleness checks, orphan detection, concept gap detection, pitfalls maintenance, decay_exempt proposals, teaching index completeness, schema conformance, collection gap analysis, and skill file enrichment staleness check (L14). Execution pass applies all auto-execute actions and confirmed forced choices, updates collection-gaps.md, regenerates teaching index, updates overview.md, and appends log entry.

**Context:**
CLAUDE.md Section 11.4 was a stub list of known rules without executable procedure.

**Rationale:**
Each step is specified with its criterion, classification (auto-execute vs. forced choice vs. informational), and Phase 3 action. The ordered structure ensures that CTRD-NNN signals are processed before contradiction expiry checks, avoiding double-processing.

**Alternatives Considered:**
- **Unordered lint checks:** Step ordering matters — CTRD-NNN signals must precede expiry detection to avoid applying window-expired-confirmed to an entry the human just acted on.

**Consequences to Watch:**
- The concept gap detection heuristic (three-page threshold) is noisy. Calibrate from operational experience; adjust threshold if signal-to-noise is poor.
- If lint passes grow too slow on a large wiki, assess whether support score recalculation can be scoped to pages updated since last lint.

**References:** IN-002, IN-004, DM-023, DM-031

---

## DM-034 | L4b: Lint Surfaces Open Contradictions as Forced Choices

- **Date:** 2026-04-19
- **Status:** ACTIVE

**Decision:**
Lint Step L4b surfaces all open Path B contradiction flags whose override window has not yet expired as forced choices in the lint pre-flight report, with an explicit skip option (C). When a claim's Status cell carries multiple CTRD IDs, each is surfaced as a separate forced choice item. This is a redundant mechanism alongside queue.md signals — the two operate independently and complement each other.

**Context:**
The queue.md mechanism requires the human to remember to act. Surfacing open contradictions at lint ensures they are put in front of the human even if they forgot to use queue.md.

**Rationale:**
The redundancy is the point. Repeated C selections are a valid conscious deferral — the item keeps appearing until the window expires and L4a auto-confirms it.

**Alternatives Considered:**
- **Lint informational only (no forced choice):** Reduces friction but removes the forcing function. Items can be overlooked in an informational list.

**Consequences to Watch:**
- If the human consistently skips all open contradictions at every lint pass, assess whether the 7-day window is appropriately calibrated.

**References:** DM-031, DM-033

---

## DM-035 | Query Workflow: Full Specification

- **Date:** 2026-04-19
- **Status:** ACTIVE

**Decision:**
Query workflow: classify query (Q1), consult index.md for candidates (Q2), assess result quality and apply gap handling (Q2a), retrieve and select material contributors (Q3), format response by pattern (Q4), cite wiki pages not raw sources (Q5), assess filing criterion (Q6), create page if confirmed (Q7), append log entry with result_quality and topic_tags fields (Q8). Filing is never automatic. Derived Key Claims use `[derived]` annotation and are exempt from lint sourcing gap checks.

**Context:**
CLAUDE.md Section 11.5 was a stub.

**Rationale:**
The query workflow closes the loop between reading the wiki and improving it: valuable query results can be filed back as Comparison or Topic pages, and sparse/shallow results trigger gap nomination. The result_quality and topic_tags fields on query log entries enable lint to aggregate query history for collection gap analysis.

**Alternatives Considered:**
- **Cite raw sources directly in query responses:** Bypasses the wiki as the synthesis layer; undermines the wiki's value as a compiled knowledge base.
- **Auto-file valuable query results:** Removes human quality gate on what becomes a permanent wiki page.

**Consequences to Watch:**
- The `[derived]` annotation convention is new. If lint conformance checks flag derived claims as sourcing gaps, tighten the exception rule in EXTRACTION-SKILL.md.
- Topic tag quality for query log entries degrades for wholly novel topics not yet in index.md. Addition 1 (gap nomination) is the better handler for these cases.

**References:** IN-002, DM-004, DM-006

---

## DM-036 | Source Nomination at Query Time for Sparse and Shallow Results

- **Date:** 2026-04-19
- **Status:** ACTIVE

**Decision:**
When a query returns a sparse or shallow result, Claude Code scans `raw/queue.md` for nominated items matching the query topic and surfaces them as forced choices. A final option in the forced choice block allows the human to request Claude Code-generated candidate sources when no relevant nominations exist. Generated suggestions are appended to `[nominated]` for human review — they do not enter `[queued]` automatically. Generated suggestions carry an explicit caveat to verify URLs before use.

**Context:**
Sparse and shallow query results were dead ends in the prior design — they communicated a gap but offered no path to close it within the same session.

**Rationale:**
Surfacing nominations at query time exploits the moment when the gap is most front-of-mind. The generation option handles the case where the nomination queue has nothing relevant. The caveat on generated suggestions is mandatory because URL hallucination is a known LLM failure mode.

**Alternatives Considered:**
- **Surface all nominated items regardless of relevance:** Too noisy; the human must filter a potentially long list.
- **Auto-promote relevant nominations without forced choice:** Removes human judgment on whether a nomination is actually relevant.
- **No generated suggestions:** Leaves the case where queue.md has nothing useful as a dead end.

**Consequences to Watch:**
- Title-based matching of nominations to query topics is noisy at scale. If the nominated queue exceeds 20 items, this step becomes unreliable. Log as P3 gap for search-layer escalation.
- If generated URL suggestions are frequently wrong, add a stronger caveat or disable the generation option.

**References:** DM-035, DM-033

---

## DM-037 | Collection Gap Recommendations from Query History

- **Date:** 2026-04-19
- **Status:** ACTIVE

**Decision:**
Query log entries carry two new structured fields: `result_quality` (sparse | shallow | adequate | rich, set by Claude Code at query time) and `topic_tags` (kebab-case terms drawn from index.md slugs where possible). Lint Step L12 aggregates query log entries by topic tag and identifies topics with three or more sparse or shallow results as active collection gaps. Gaps are written to `raw/collection-gaps.md` — a persistent planning artifact updated by lint. Lint also checks whether sources have been ingested since the most recent sparse/shallow entry for each gap topic; if yes, the gap is annotated as potentially addressed rather than suppressed. The discovery pass reads collection-gaps.md to prioritize and annotate gap-matching nominations.

**Context:**
The design needed a mechanism for usage patterns and results to inform collection needs over time, not just at the moment of a sparse result.

**Rationale:**
The result_quality and topic_tags fields on log entries are the minimum addition needed to enable retrospective aggregation. collection-gaps.md as a persistent artifact makes gap recommendations available between lint passes. The potentially-addressed annotation prevents stale gap flags after relevant sources are ingested.

**Alternatives Considered:**
- **Aggregate from natural-language log descriptions:** Not reliably aggregable without a semantic layer.
- **Lint informational output only, no persistent file:** Gap recommendations disappear into log history. The human has no standing view of collection priorities.

**Consequences to Watch:**
- `result_quality: shallow` requires Claude Code to assess page status and source_count across returned pages — more work than a simple count. If shallow detection produces inconsistent results, tighten the criteria in CLAUDE.md.
- Topic tag quality degrades for wholly novel topics. This is a known limitation; Addition 1 (gap nomination at query time) handles novel topics better.

**References:** DM-033, DM-035, DM-036

---

## DM-038 | Red-Team Additions: Shallow Coverage, Discovery Pass Gap Prioritization, Gap Closure Check

- **Date:** 2026-04-19
- **Status:** ACTIVE

**Decision:**
Three additions confirmed from red-teaming the collection gap design: (1) A `shallow` result quality value (distinct from `sparse`) is added — 2+ material contributors but majority stub/stale or average source_count ≤ 2. Shallow triggers the same gap nomination behavior as sparse. (2) The discovery pass reads `raw/collection-gaps.md` before fetching feeds and annotates gap-matching nominations, listing them first in the nomination report. (3) Lint Step L12 checks whether sources have been ingested since the most recent sparse/shallow query entry for each gap topic; gaps with subsequent ingests are annotated as potentially addressed rather than suppressed.

**Context:**
Red-teaming identified three failure modes in the collection gap design: (a) shallow coverage is not detected by a page-count-only result quality metric; (b) the discovery pass and query history are disconnected; (c) there is no loop closure to verify that an ingested source actually addressed a gap.

**Rationale:**
These additions close the most significant feedback loop gaps without requiring new data structures or new interaction model components. All three reuse existing infrastructure.

**Alternatives Considered:**
- **Declined filing as a gap signal:** Too noisy; declines happen for many reasons unrelated to coverage gaps.
- **Semantic topic tag matching for discovery pass:** Out of scope for confirmed stack; title-string matching is sufficient for initial implementation.
- **Automatic gap closure confirmation after ingest:** Cannot be done reliably without a re-query to test whether the new source actually answers the gap question.

**Consequences to Watch:**
- The shallow detection criteria (majority stub/stale or avg source_count ≤ 2) are heuristics. Calibrate from operational experience.
- If discovery pass gap annotation produces more noise than signal (many false matches), raise the match specificity threshold.
- The gap closure check is advisory only — the human assesses sufficiency of potentially-addressed gaps. Do not auto-close gaps.

---

## DM-039 | Citation Harvesting During Ingest

- **Date:** 2026-04-19
- **Status:** AMENDED
- **Amended By:** DM-044

**Decision:**
During the ingest execution pass, Step 11a scans the extracted source for outbound
links and citations to peer-reviewed or institutional sources that resolve to a valid
URL. Candidates not already present in `sources/` by exact URL match are appended to
`raw/queue.md` under `[nominated]` with a `[nominated — cited by [[source-slug]]]`
annotation. Nominations are not surfaced as forced choices during ingest — they enter
the normal promoted queue reviewed at the next discovery pass or on-demand. The same
institutional-tier filter used by the discovery pass applies.

**Context:**
The discovery pass monitors feeds forward in time. Citation harvesting works backward
through citation chains. Practitioner and vendor sources regularly cite peer-reviewed
papers and institutional research that the team would not encounter directly. Without
this mechanism, that signal is lost at ingest time.

**Rationale:**
Complexity cost is low — the extraction pass already reads the source in full, and
cited sources are present in the text. The credibility filter (institutional-tier only)
keeps nominations signal-rich: a practitioner blog citing other practitioner blogs
produces zero nominations. The URL-resolvable constraint prevents unreliable slug
matching against ambiguous bibliographic references. Deferring to the nominated queue
rather than interrupting the ingest pre-flight preserves the batch review model.

**Alternatives Considered:**
- **Surface as ingest pre-flight forced choices:** Interrupts the batch review model
  with citation nominations mid-session. Ruled out.
- **Include practitioner citations:** Degrades nomination signal-to-noise. Ruled out.
- **Accept bibliographic references without URLs:** Slug matching against sources/
  is unreliable without a canonical URL. Ruled out.

**Consequences to Watch:**
- If a source cites many institutional papers (e.g., a literature review), the
  nomination queue may receive a large batch at once. If this becomes a pattern,
  assess a per-ingest nomination cap.
- If URL resolution fails at ingest time for a valid citation, the source is silently
  skipped. If missed citations become a pattern, assess adding a `[citation-unresolved]`
  log annotation for human follow-up.

**References:** DM-022, DM-019

---

## DM-040 | CLAUDE.md Splitting Deferred — Not Warranted at Current Size

- **Date:** 2026-04-19
- **Status:** ACTIVE
- **Superseded By:** DM-061

**Decision:**
CLAUDE.md will not be split into multiple files at current size (~12,000–15,000 tokens).
Reassess if the document grows to 2–3x its current size through schema revision.

**Context:**
DM-016 flagged "if CLAUDE.md grows too long for a single context window, assess structural
splitting" as a consequence to watch. The document has grown substantially since that entry
was written. This session assessed whether the trigger had been reached.

**Rationale:**
The context window concern is not live: CLAUDE.md occupies roughly 7–8% of Claude Code
Sonnet's 200K context window. The instruction-reliability concern — the more substantive
risk — is already mitigated by the existing architecture: the session-start prompt directs
Claude Code to specific sections by operation type; skill files offload examples;
wiki-lessons-learned.md offloads precedents. The natural split (schema spec vs. operational
workflows) would require the session-start prompt to name multiple files, introducing a new
failure mode (forgetting to load a required file) worse than the problem it solves. The
current single-document design is robust because "read CLAUDE.md" is one unambiguous
instruction.

**Alternatives Considered:**
- **Split into schema spec + operational workflows:** The most natural structural boundary.
  Ruled out because it requires the session-start prompt to coordinate multiple file loads,
  and the failure mode of forgetting one file is worse than the cost of a longer single file.
- **Split by operation type (ingest, lint, query as separate files):** Higher granularity,
  lower per-operation context load. Ruled out as premature — the operations are
  interdependent (ingest references lint protocol, query references gap nomination) and
  splitting would require extensive cross-references that degrade maintainability.

**Consequences to Watch:**
- If CLAUDE.md grows to 2–3x current size through schema revision, reassess splitting.
- If instruction-following quality degrades on specific sections in early operation,
  that is a signal to extract those sections to skill files rather than split the document.

**References:** DM-016, DM-029

---

## DM-041 | Skill File Starter Templates Produced in Design Project

- **Date:** 2026-04-19
- **Status:** ACTIVE

**Decision:**
Starter templates for EXTRACTION-SKILL.md, TAGGING-SKILL.md, and CONTRADICTION-SKILL.md
will be produced in this design project rather than deferred entirely to early operational
experience. Templates use synthetic worked examples and explicit "TO BE ENRICHED" markers
for sections requiring real operational cases.

**Context:**
DM-029 specified that skill files should be "authored from early operation experience,"
which could be read as deferring them entirely. This session assessed whether starter
templates would reduce early operational drift enough to warrant producing them now.

**Rationale:**
The primary value of a starter template is establishing document structure and naming
common failure modes before the first ingest runs — not the richness of its examples.
An agent reading a stub EXTRACTION-SKILL.md with two synthetic examples and a named
failure mode ("Key Claims must be assertable sentences, not topic labels") is measurably
better calibrated than reading nothing. The first ingest runs cold without any skill file.
The controlled vocabulary in CLAUDE.md (Sections 7.1, 7.2) makes TAGGING-SKILL.md fully
derivable from the schema. CONTRADICTION-SKILL.md borderline cases (incoming weight within
one tier step of existing support score) are the most likely source of drift and benefit
most from a worked example before any contradictions are encountered.

**Alternatives Considered:**
- **Defer all three entirely:** Consistent with literal reading of DM-029. Ruled out
  because it leaves the first ingest without any extraction guidance, which is the highest
  variance operation.
- **Produce EXTRACTION-SKILL.md only:** Reasonable fallback. Ruled out in favor of
  producing all three because TAGGING-SKILL.md and CONTRADICTION-SKILL.md are fully
  derivable from schema content already designed, and the marginal effort is low.

**Consequences to Watch:**
- Synthetic examples in starter templates may not cover the actual edge cases encountered
  in the team's specific source material. Prioritize enriching EXTRACTION-SKILL.md after
  the first five ingests.
- If starter templates are treated as complete rather than as scaffolding, operational
  drift detection may be delayed. The "TO BE ENRICHED" markers must be prominent.

**References:** DM-029, DM-028

---

## DM-042 | Skill Enrichment Nomination Mechanism

- **Date:** 2026-04-19
- **Status:** ACTIVE

**Decision:**
Claude Code nominates skill file enrichments at two trigger points: (1) after each ingest
operation (Step 21a), by scanning TO BE ENRICHED sections of skill files used during that
ingest and assessing whether the case just processed represents a genuinely novel example
not already covered; (2) at each lint pass (Step L14), by checking whether any TO BE
ENRICHED section remains entirely unpopulated after five or more ingests and surfacing
this as an informational flag. Nominations use the forced choice format (confirm / confirm
with edits / discard). Confirmed enrichments are written to the skill file immediately.
A `skill-enrichment` log entry type records confirmations.

**Context:**
Skill files contain TO BE ENRICHED placeholder sections that require real operational
cases. Without a structured nomination mechanism, populating these sections depends on
the human remembering to do it — which is the same failure mode that makes all
maintenance tasks accumulate into backlogs.

**Rationale:**
The analogy to wiki-lessons-learned.md drafting is exact: Claude Code encounters a case,
drafts the proposed enrichment language, surfaces it as a low-friction decision, human
confirms or discards. The novelty filter ("would this example teach Claude Code something
the existing examples do not?") prevents noise from accumulating in skill files through
redundant instances of already-covered cases. The lint staleness check (L14) is
informational only — it signals under-enrichment without creating forced choice pressure
at every pass.

**Alternatives Considered:**
- **Human-initiated enrichment only:** Relies on the human noticing and remembering.
  The same maintenance burden that leads to skill file neglect.
- **Nominate every case encountered:** Produces noise; skill files accumulate redundant
  examples that dilute the signal from genuinely novel cases.
- **Dedicated enrichment review session:** Creates a separate workflow step with its own
  scheduling burden. The per-ingest nomination integrates enrichment into existing flow
  at near-zero marginal cost.

**Consequences to Watch:**
- If the novelty filter is applied too conservatively, genuine edge cases are not
  nominated. If applied too liberally, skill files accumulate redundant examples.
  Calibrate from the first ten ingest operations.
- If nominated enrichment language is consistently revised by the human (option B in the
  forced choice), tighten the drafting guidance in this entry's consequences or in
  wiki-lessons-learned.md.

**References:** DM-029, DM-041

---

## DM-043 | Contradiction Stacking Rules and Path A/B Boundary Clarification

- **Date:** 2026-04-19
- **Status:** ACTIVE

**Decision:**
Two additions to the contradiction resolution schema: (1) Path A/B boundary clarified —
Path B takes precedence whenever |difference| ≤ 2; Path A fires only when difference
strictly exceeds 2. This resolves an ambiguity in the prior wording where "incoming
weight exceeds existing Support Score" could fire at difference=2 simultaneously with
Path B. (2) Stacking rules specified for two cases: (a) multiple Path C accumulations —
minority views accumulate in the Source field without limit; each is excluded from the
incumbent Support Score; no frontmatter entry is created; (b) new source arrives while
claim is already contested — three postures specified (supports contesting position;
supports incumbent; distinct third position) with path recalculation logic for each.
Dual CTRD IDs in a single Status cell are valid syntax: `contested [CTRD-003] [CTRD-004]`.
Lint Step L4b handles multiple IDs per row as separate forced choice items.

**Context:**
The Path A/B boundary was implicitly ambiguous in the prior CLAUDE.md wording. The
stacking cases were unspecified. Both gaps were surfaced during skill file drafting when
the CONTRADICTION-SKILL.md worked examples required unambiguous path determination at
the boundary condition, and when the question of multiple simultaneous contradictions
on one claim was raised.

**Rationale:**
Path B-first testing at the boundary is the conservative choice — it sends near-tie cases
to human review rather than auto-resolving them. This is consistent with the design intent
of the weighted model, which placed human review precisely at the boundary of evidence
balance. For stacking: minority views are purely additive to the Source field and require
no new structural machinery. The three-posture model for contested-claim stacking handles
all cases reachable by the path logic without introducing new path types. The dual-CTRD
syntax is a minimal extension of the existing inline marker convention.

**Alternatives Considered:**
- **Path A-first at boundary:** Auto-resolves cases where incoming outweighs existing,
  even at difference=2. Ruled out — the boundary is exactly where a practitioner source
  may reasonably contest a decayed institutional source, and human judgment adds value.
- **New page section for contested claims with multiple flags:** Higher structural cost;
  creates ambiguity about whether the section is canonical content. Ruled out in favor
  of extending the existing Status cell syntax.
- **Cap on minority views per claim:** No operational justification for a cap; minority
  views are low-cost to record and high-value for provenance. Ruled out.

**Consequences to Watch:**
- Dual CTRD IDs in a Status cell increase the complexity of lint L4b parsing. If lint
  incorrectly handles multi-ID cells in early operation, add a worked example to
  CONTRADICTION-SKILL.md Section 7.1.
- The three-posture stacking logic for Posture 3 (third position) is the most complex
  case. If Claude Code produces incorrect path calculations for this posture, add a
  worked numerical example to CONTRADICTION-SKILL.md Section 7.2.

**References:** DM-023, DM-030, DM-033, DM-034

---

## DM-044 | Citation Harvesting Nomination Cap Deferred; Step 22 Batch Dismiss Added

- **Date:** 2026-04-19
- **Status:** ACTIVE

**Decision:**
No per-ingest nomination cap is added to Step 11a at schema design time. The consequence
language in DM-039 is replaced with a specific observable trigger: if a single ingest
deposits more than 10 nominations to the `[nominated]` queue, assess whether a cap or
source-type exclusion is warranted. Separately, the post-ingest summary (Step 22) is
extended with a "Citations nominated" block that gives the human a two-option forced
choice: leave nominations in queue for passive query-time surfacing (option A), or
dismiss all nominations from this source immediately (option B). The block is omitted
when Step 11a produces zero nominations.

**Context:**
DM-039 flagged a consequence to watch: a literature review or survey could deposit a
large nomination batch in a single ingest. Two questions were open: (1) whether a hard
cap was warranted at design time, and (2) whether the human had any mechanism to manage
nomination batches without manually editing queue.md. Analysis showed the cap was not
warranted, but the second question revealed a real gap — the human had no batch dismiss
path for citation-harvested nominations.

**Rationale:**
The cap risk is speculative and source-mix dependent. Lab blog posts, research papers,
and practitioner articles — the typical source types for this wiki — cite 2–5
institutional sources each, not 20–30. A cap applied speculatively would discard valid
nominations before the human can assess relevance. The human promotion gate in queue.md
is already the effective throttle on what enters the ingest pipeline. The Step 22 batch
dismiss option provides the missing control mechanism at zero structural cost: it is a
two-option forced choice in the existing summary format, removing queue.md entries that
the human decides immediately are not worth pursuing. Option A (leave in queue) requires
no action, preserving passive surfacing via query-time matching.

**Alternatives Considered:**
- **Hard cap at design time (e.g., 10 nominations per ingest):** Discards valid
  nominations silently before human review. Ruled out — cost is concrete, risk is
  speculative.
- **No batch dismiss, no cap:** Leaves nominations accumulating with no lightweight
  removal path. Ruled out — the gap is real even if the risk is not acute.
- **Separate nomination review session:** Creates a new workflow step with its own
  scheduling burden. Ruled out in favor of integrating into the existing Step 22 summary.

**Consequences to Watch:**
- If a single ingest consistently deposits more than 10 nominations (the trigger
  condition), assess whether a source-type exclusion (e.g., skip citation harvesting
  for literature reviews) or a per-ingest cap is warranted at that point.
- If the human consistently selects option B (dismiss all) for citation-harvested
  nominations, that is a signal that citation harvesting is producing low-value
  nominations and the institutional-tier credibility filter may need tightening.

**References:** DM-039, DM-019

---

## DM-045 | SINGLETON INITIALIZATION IS HUMAN RESPONSIBILITY; LAST_CONTRADICTION_ID INITIALIZES TO 0

- **Date:** 2026-04-20
- **Status:** ACTIVE

**Decision:**
The four operational singletons (`overview.md`, `index.md`, `log.md`, `teaching-index.md`)
and three `raw/` files (`queue.md`, `collection-gaps.md`, `discovery-sources.md`) must be
created by the human before the first Claude Code session, using exact initial content
specified in the schema. `last_contradiction_id` initializes to `0` in `overview.md`.
`open_contradictions` initializes to `0`. `last_lint` and `last_discovery` are omitted at
initialization. CLAUDE.md updated with Section 2.1 (Initialization Scaffold) and an
initialization values note in Section 5.7.

**Context:**
Implementation handoff work surfaced that CLAUDE.md did not specify who creates singleton
files or what their initial field values should be. Claude Code reads `last_contradiction_id`
before assigning every CTRD-NNN — if the file is absent or the field is uninitialized,
Claude Code must either fail hard or improvise defaults, both of which the schema prohibits.
The schema's stated rule (Section 1: "stop and surface the gap rather than improvising a
convention") means an absent overview.md with no specified behavior produces a hard stop on
the first contradiction encountered. Specifying initialization in the schema eliminates the
ambiguity.

**Rationale:**
`last_contradiction_id: 0` is unambiguous: read 0, increment to 1, assign CTRD-001. Any
other initialization value would create a gap between the counter state and the first
assigned ID. Omitting `last_lint` and `last_discovery` at initialization is correct because
their absence is a valid state (no lint or discovery has run yet) — initializing them to
dummy dates would create false signals in the lint staleness checks and discovery pass.
Initializing `open_contradictions: 0` (optional field) explicitly avoids a lint edge case
where absence of the field could be misread as an unknown state rather than zero.

**Alternatives Considered:**
- **Claude Code creates overview.md on first run if absent:** Requires Claude Code to
  handle missing required state as a special case. Inconsistent with the schema's
  fail-on-gap rule. Ruled out.
- **Leave initialization unspecified, resolve at implementation time:** Defers the ambiguity
  without resolving it. Ruled out — the answer is deterministic and should be in the schema.

**Consequences to Watch:**
- If the wiki schema is ever migrated to a new execution environment, the initialization
  scaffold content in Section 2.1 must be updated to reflect any new required fields.
- Section 2.1 is the authoritative initialization specification. The implementation handoff
  document reproduces it for implementer convenience; any divergence between the two is a
  defect in the handoff document, not in the schema.

**References:** CC-08, CC-09, CC-12 (portability-review.md)

---

## DM-046 | SEMI-AUTOMATED INITIALIZATION ADOPTED; INIT-PROMPT.MD AS FIRST-CLASS ARTIFACT; IMPLEMENTATION GUIDE RESTRUCTURED AROUND EXECUTOR PHASES

- **Date:** 2026-04-20
- **Status:** ACTIVE

**Decision:**
The implementation guide (item 4 of the agenda) will center on a Claude Code
initialization session rather than a manual step-by-step walkthrough. A new artifact,
`INIT-PROMPT.md`, is a hard prerequisite for the guide — it is the initialization
prompt the human pastes into Claude Code to start the automated setup session.
`implementation-handoff.md` is restructured around four executor phases rather than
technical dependency order. Approximately 65% of the pre-flight steps are automatable
by Claude Code; ~20% are guided (Claude Code does the work, human provides one input);
~15% are human-only.

**Context:**
Review of implementation-handoff.md against the execution environment revealed that
most initialization tasks — creating directory structure, writing scaffold files with
exact YAML content, patching quartz.config.ts, writing .gitignore, writing the
pre-commit hook — are mechanical file writes Claude Code handles more reliably than a
human copying from a document. The primary barrier to automation is a bootstrapping
conflict: the standard session-start prompt instructs Claude Code to read CLAUDE.md
first, but during initialization CLAUDE.md does not yet exist in the wiki directory.
A separate initialization prompt that is self-contained (not dependent on reading
CLAUDE.md from the wiki directory) resolves this conflict.

**INIT-PROMPT.md Design Requirements:**

The initialization prompt must satisfy all of the following:

1. **Self-contained.** Embeds all file content specifications Claude Code needs for the
   scaffold. Does not reference CLAUDE.md in the wiki directory — it does not exist yet.
   Instead, it includes the content of CLAUDE.md Section 2.1 directly.

2. **Working directory confirmation first.** Before writing any files, Claude Code must
   display the current working directory and confirm with the human that it is the
   intended wiki root. This is the first action, before any mkdir or file write.

3. **Idempotency check.** Before creating any scaffold file, Claude Code checks whether
   the file already exists. If any scaffold files are found, Claude Code surfaces the
   list and stops — it does not overwrite without explicit human confirmation per file.
   This protects against re-running initialization on a partially-initialized directory.

4. **Quartz prerequisite check.** Early in the session, Claude Code runs `node --version`
   and `npm --version`. If either fails or returns a version below Node 18, Claude Code
   stops and reports the gap with the specific install instruction before proceeding to
   any Quartz-related step.

5. **Defined pause points.** Claude Code pauses and waits for explicit human confirmation
   at three points: (a) after working directory confirmation; (b) after scaffold files
   are written and before git operations, so the human can verify the directory structure
   visually; (c) after git remote is set, so the human can confirm the remote URL is
   correct before any push.

6. **Defined done-state.** The initialization session ends when: all scaffold files are
   written, git is initialized with remote set, .gitignore is configured, quartz.config.ts
   is patched, the pre-commit hook is written, and Claude Code has reported a summary of
   what was created. The first wiki maintenance session (test ingest) is explicitly out
   of scope for the initialization session.

7. **First-time Claude Code UX annotations.** At each pause point and at each major
   action, the prompt instructs Claude Code to explain in plain language what it just
   did and what the human should expect to see. This is a UX requirement, not a
   functional one — it exists because the implementer is a first-time Claude Code user
   who needs to build a mental model of what Claude Code is doing.

**Implementation Guide Structure (executor-phase order):**

- **Phase 0 — Human Prerequisites** (~4 steps): Create GitHub repo, install Node.js
  18+ and npm, install Quartz scaffold (`npx quartz create`), install Obsidian. These
  must be complete before Claude Code session starts. Includes verification commands
  the human runs to confirm readiness.

- **Phase 1 — Claude Code Initialization Session** (~10 automated steps, 3 pause
  points): Human pastes INIT-PROMPT.md into Claude Code. Claude Code handles all file
  creation and configuration. Human acts only at the three pause points. Guide describes
  what each pause point looks like in Claude Code's output and what the human must do.

- **Phase 2 — Human Verification** (~3 steps): Open wiki directory as Obsidian vault,
  verify a test page renders, confirm GitHub Actions build succeeds. These require GUI
  interaction that Claude Code cannot perform.

- **Phase 3 — First Wiki Session** (1 step): Paste the standard session-start prompt
  from tooling-recommendation.md Section 7 and run a test ingest with a single
  low-stakes source. This is the handoff from initialization to operation.

**Artifacts required (new):**
- `INIT-PROMPT.md` — initialization prompt, designed before the guide is written
- Revised `implementation-handoff.md` — restructured around Phase 0–3 executor order

**Artifacts requiring updates (deferred to next session):**
- `portability-review.md` — new CC assumption entry for INIT-PROMPT.md as required
  pre-session artifact (analogous to CC-10 for session-start prompt)

**Alternatives Considered:**
- **Manual step-by-step guide with no Claude Code automation:** More tedious for the
  implementer, higher error rate on YAML content, no structural advantage. Ruled out.
- **Fully automated with no pause points:** Creates risk of Claude Code operating in
  the wrong directory or with wrong configuration without human awareness. Ruled out.
- **Single combined artifact (guide + init prompt in one file):** The init prompt must
  be pasteable directly into Claude Code without the surrounding guide content. Keeping
  them separate preserves this property. Ruled out.

**Consequences to Watch:**
- INIT-PROMPT.md embeds CLAUDE.md Section 2.1 content. If Section 2.1 changes, both
  files must be updated. This is an explicit synchronization dependency.
- The implementation guide must be validated against the actual Claude Code UX by a
  user with comparable experience to the intended implementer before being treated as
  final. It is a design artifact, not a tested operational document.

---

## DM-047 | ACADEMIC-BLOG ADDED AS THIRD DISCOVERY SOURCE TYPE

- **Date:** 2026-04-20
- **Status:** ACTIVE

**Decision:**
`academic-blog` added as a third valid type value in `raw/discovery-sources.md`.
Format string updated from `{type: arxiv | lab-blog}` to
`{type: arxiv | lab-blog | academic-blog}` in CLAUDE.md Sections 2.1 and 11.3,
implementation-handoff.md Section 1.3, and INIT-PROMPT.md Step 7.
`academic-blog` is processed identically to `lab-blog` (page fetch and scan for
recent items); the distinction is metadata for human curation purposes only.
All three types remain subject to the institutional-tier filter at discovery Step 4.

**Context:**
The original two-value format (`arxiv | lab-blog`) did not accommodate academic
institution publications such as Stanford HAI or Berkeley BAIR, which are institutional-
tier and relevant to the wiki domain but are neither commercial lab blogs nor arXiv feeds.
The absence of a third type forced a false choice between misclassifying them as `lab-blog`
or excluding them from the discovery feed.

**Rationale:**
Adding a distinct type label costs nothing operationally (identical fetch behavior) and
correctly represents the distinction between commercial lab publications and academic
institution publications. The label aids human curation when reviewing the feed list.
Keeping the type distinct from `lab-blog` preserves the ability to add type-specific
behavior later if warranted (e.g., different scan heuristics for academic publication
pages vs. lab news feeds) without a breaking format change.

**Alternatives Considered:**
- **Use `lab-blog` for academic sources too:** Operationally equivalent but semantically
  incorrect. Complicates future type-specific behavior. Ruled out.
- **Create `institutional-blog` covering both labs and academics:** Loses the
  lab-vs-academic distinction that may matter for credibility-tier assignment heuristics.
  Ruled out.

**Consequences to Watch:**
- If Stanford HAI or similar academic sources are added and the discovery pass
  consistently nominates irrelevant items from them, consider whether academic
  institution blogs warrant a tighter institutional-tier filter than lab blogs.
- If the `academic-blog` vs `lab-blog` behavioral distinction ever needs to be
  implemented (e.g., different page-structure scan heuristics), update CLAUDE.md
  Section 11.3 to describe the difference. The type label is already in place.

---

## DM-048 | TECHNICAL_DEPTH FIELD ADDED TO TOPIC AND TOOL PAGES

- **Date:** 2026-04-20
- **Status:** ACTIVE

**Decision:**
An optional `technical_depth` field is added to Topic and Tool page frontmatter.
Controlled values: `foundational | practitioner | research`. Assigned by Claude Code
at ingest without human confirmation. Added to CLAUDE.md Sections 5.2 and 5.3
(frontmatter specs), Section 10 (Teaching Index generation rule 5), and Step 12
(ingest execution pass frontmatter logic). Step 13 inherits via its reference to
Step 12.

Value definitions:
- `foundational` — no AI/ML background required; concepts explained from first
  principles; accessible to non-technical professionals
- `practitioner` — requires familiarity with AI/ML concepts; suitable for developers,
  product managers, data scientists
- `research` — assumes deep AI/ML background or equivalent research-level familiarity
  with the subject area; covers novel methods, theoretical results, empirical
  evaluations, or advanced alignment and policy analysis

**Context:**
The Teaching Index surfaced a usability gap: it presents a flat list of tagged pages
with no accessibility signal. A non-technical reader cannot distinguish foundational
content from research-level content without reading the page. The gap is compounded by
a source diet weighted toward technical lab blogs and research papers, which risks
producing a Teaching Index that is nominally populated but practically inaccessible
to lay readers. See IN-008.

**Rationale:**
Three-level scale is the minimum that meaningfully distinguishes the target audiences
(lay professional, practitioner, researcher). A binary (accessible/technical) loses
the practitioner segment entirely. More than three levels introduces assignment
ambiguity without commensurate benefit. Auto-assignment without forced choice is
correct: `technical_depth` is a factual judgment about prerequisites, not a
policy decision requiring human input. It can be revised on re-assessment.

**Alternatives Considered:**
- **Binary accessible/technical:** Loses the practitioner-level segment. Ruled out.
- **Five-level scale:** Assignment ambiguity increases significantly at boundaries
  (e.g., practitioner-high vs. research-low). Ruled out.
- **Human-assigned via forced choice:** Adds a forced choice per page per ingest.
  The field is a factual prerequisite judgment, not a policy decision. Ruled out.

**Consequences to Watch:**
- If Claude Code consistently misassigns depth (e.g., marks practitioner content as
  research), add a calibration note to EXTRACTION-SKILL.md or TAGGING-SKILL.md with
  worked examples.
- The "research" value spans both technical ML research and non-technical policy
  research. If these require materially different assignment logic in practice, split
  into `research-technical` and `research-policy`. Not warranted at launch.

**References:** IN-008

---

## DM-049 | DISCOVERY SOURCE FEED EXPANDED WITH FOUR INSTITUTIONAL SOURCES

- **Date:** 2026-04-20
- **Status:** ACTIVE

**Decision:**
Four sources added to the default `raw/discovery-sources.md` feed, all typed as
`academic-blog`:
- `https://hai.stanford.edu/news` | Stanford HAI — safety, policy, human-AI
  interaction, economic impacts
- `https://cset.georgetown.edu/category/blog/` | CSET Georgetown — AI policy,
  US-China competition, export controls, government AI adoption
- `https://www.brookings.edu/topic/artificial-intelligence/` | Brookings AI —
  AI governance, regulation, economic policy; accessible writing style
- `https://partnershiponai.org/blog/` | Partnership on AI — responsible AI
  deployment, fairness, accountability

Updated in CLAUDE.md Section 11.3 example, INIT-PROMPT.md Step 7 default content,
and implementation-handoff.md Section 1.3 template.

**Context:**
The original three defaults (Anthropic, OpenAI, DeepMind) are all commercial lab
blogs. A feed composed exclusively of lab blogs is biased toward technical capability
announcements and training results, underrepresenting alignment, safety, governance,
regulation, and accessible practitioner content. The four additions were chosen to
correct this bias while remaining institutional-tier.

**Rationale:**
Stanford HAI and CSET Georgetown are academic research centers with clear
institutional-tier status. Brookings Institution is a major policy think tank
(nonprofit, non-partisan) with strong AI governance coverage and accessible prose
that directly supports the teaching use case. Partnership on AI addresses responsible
deployment — a gap in the lab blog diet. All four were reviewed against the
institutional-tier filter criteria (editorial accountability, institutional affiliation,
peer review or editorial review process). RAND and NIST were deferred: RAND is more
narrowly focused on defense/national security; NIST publishes at too low a cadence
for a discovery feed and is better treated as a manual queue addition.

**Alternatives Considered:**
- **Include RAND:** More narrowly scoped than Brookings; less relevant unless wiki
  scope expands to defense/national security AI. Deferred.
- **Include NIST AI page:** Cadence too low for a discovery feed; publishes major
  frameworks (AI RMF) as one-time documents. Better as manual queue addition. Deferred.

**Consequences to Watch:**
- If Brookings or Partnership on AI nominations are consistently discarded by the
  human as off-domain, remove from the feed and replace with a narrower source.
- Academic institution blog pages may have different HTML structure than lab news
  pages; if the discovery pass fails to identify recent items from academic-blog
  sources, add a structure note to CLAUDE.md Section 11.3.

---

## DM-050 | SESSION BUDGET MANAGEMENT: STEP 0 PRE-INGEST CHECK, DEFERRED-INGEST, SESSION-STATS LOG, COST REVIEW PROCEDURE

- **Date:** 2026-04-21
- **Status:** ACTIVE

**Decision:**
Four inter-related schema additions address Claude Code Pro tier session budget risk
during large ingest operations:

1. **Step 0 pre-ingest budget check:** Fires when `[queued]` count exceeds 5. Reads
   system time via bash, determines peak/off-peak status (peak: 05:00–11:00 PT /
   13:00–19:00 GMT per Anthropic's March 2026 capacity policy), and surfaces a
   five-option forced choice: process first 5 (recommended), process first 10, process
   all, specify a custom subset, or defer. Threshold of 5 chosen as safe for Pro tier
   at any hour; not configurable at runtime — requires human schema edit to change.

2. **deferred-ingest.md:** Ephemeral file written to `raw/` when the human selects
   option E (defer) at Step 0. Records the queued items list at time of abort and
   recommended timing. Committed to git on creation. Deleted on successful resumption.
   Lint step L14 surfaces a forced choice if the file is older than 14 days.

3. **session-stats log entry (Step 22a):** Appended to `log.md` at the end of every
   ingest session. Records queue size, documents attempted and completed, whether the
   session limit was hit, time window (peak/off-peak), source type mix, and approximate
   token counts from `/cost`. Write-heavy, read-rarely — the agent reads the log only
   during an explicit cost review, not at session start.

4. **Cost log review procedure (Step L12a):** Fires during lint when `session-stats`
   entry count reaches 50. Surfaces a forced choice: review now or defer. If review now:
   agent reads all session-stats entries, analyzes limit-hit rates by time window and
   source type mix, and produces a directional recommendation to keep, lower, raise, or
   add source-type-specific batch thresholds. Recommendation is preceded by an explicit
   caveat that token counts are approximate and limit-hit rate is the primary signal.
   Human confirms any threshold changes; agent appends `schema-change` log entry.

**Context:**
Anthropic's March 2026 capacity policy introduced elastic peak-hour throttling:
5-hour session windows yield less work during peak hours (05:00–11:00 PT) without
changing weekly totals. Pro tier sessions have approximately 44,000 tokens per window
at off-peak, less during peak. Anthropic does not publish exact figures. A 20-document
ingest on Pro tier risks exhausting the window before completion, halting work without
a clean checkpoint. Per-document git commits (existing requirement) ensure completed
work is not lost, but a mid-session halt is still disruptive.

The goal is not to prevent large batches — the "process all" option remains available
— but to ensure the user makes that choice with full awareness of the risk, and to
accumulate operational data to refine guidance over time.

**Rationale:**
- Five-option forced choice (including abort) gives the user full agency. The schema
  does not impose a hard cap.
- Abort (option E) was added at user request: the user may start a session not knowing
  how large the queue has grown, and needs a clean exit path.
- Time-of-day guidance is grounded in Anthropic's published capacity policy, not
  speculation. Off-peak scheduling is a confirmed lever.
- session-stats log is write-heavy and read-rarely to minimize per-session overhead
  (~200–400 tokens to write; reads only at explicit review trigger).
- 50-entry threshold for review gives approximately 3–6 months of data at normal
  operating cadence before the first recalibration is suggested.

**Alternatives Considered:**
- **Hard batch cap (no override):** Removes user agency; ruled out.
- **Separate cost-tracking file:** Adds structural overhead with no benefit over
  extending log.md. Ruled out.
- **Read session-stats at every session start:** Token overhead on every session for
  data that is only actionable quarterly. Ruled out.
- **No cost review procedure:** Leaves the heuristic permanently uncalibrated.
  Ruled out.

**Consequences to Watch:**
- If the 5-item threshold fires too frequently in normal operation (e.g., user
  routinely queues 6–7 short articles), lower friction by raising the threshold.
  The first cost review at 50 entries will surface this signal.
- If `/cost` is unavailable or returns no data in Claude Code, the tokens line is
  omitted from session-stats entries. The limit-hit signal remains usable without it.
- The peak/off-peak window is based on Anthropic's March 2026 policy announcement.
  If Anthropic changes this policy, the Step 0 guidance becomes stale. No automated
  mechanism detects this — periodic manual review of Anthropic's capacity policy is
  the only mitigation.

**References:** IN-007 (partially addressed — queue aging aspect remains open)

---

## DM-051 | TWO-STAGE NOMINATION QUEUE AGING: NOMINATED_DATE FIELD, [STALE-NOMINATED] SECTION, LINT AGING PASS

- **Date:** 2026-04-21
- **Status:** ACTIVE

**Decision:**
Nomination queue aging is implemented as a two-stage automatic process:

- **Stage 1 (90 days):** Item moves from `[nominated]` to `[stale-nominated]` in
  queue.md during the next lint pass. Suppressed in ingest Step 11a forced choices.
  Visible in query Step Q2a via a demand-signal resurface (separate "Older nominations"
  block, same A/B/C choices).
- **Stage 2 (180 days):** Item is deleted from `[stale-nominated]` during the next lint
  pass. Never re-surfaced. If a query produces a demand signal for a deleted item, the
  normal gap nomination path creates a fresh nomination.

A `nominated: YYYY-MM-DD` field is appended to every nomination line at write time by
both citation harvesting (Step 11a) and the discovery pass (Section 11.3). Pre-schema
entries without this field are skipped by the aging pass with an informational note.

Both Stage 1 and Stage 2 are auto-execute in lint Phase 3 — no forced choice. The
informational summary lists all items being moved or deleted; the human can manually
edit queue.md before lint Phase 3 executes to rescue an item.

Promotion via query demand signal (option A on a stale-nominated item) moves the item
directly to `[queued]`, bypassing the `[nominated]` stage. The `nominated_date` is
retained on the line as metadata; the aging clock does not apply to `[queued]` items.

Both Step 11a and the discovery pass now check `[nominated]` and `[stale-nominated]`
for URL duplicates before writing, preventing re-nomination of an item already in either
section.

**Context:**
IN-007 identified that a `[nominated]` queue exceeding ~20 items degrades title-string
matching quality during query Step Q2a. The escalation path described in IN-007 noted
that option (b) — a maximum nomination age with auto-discard — was the lowest-cost
starting point. This decision implements that path with the two-stage refinement
requested during design review.

**Rationale:**
A hard single-stage deletion was too blunt. Stage 1 preserves demand-signal resurface
capability for items that may have become relevant since nomination. Stage 2 removes
genuinely dead items after a longer window. The demand signal (sparse/shallow query
result) is the most reliable proxy for "this item has become relevant" — it fires when
the wiki actually fails to answer a question, not as a speculative relevance guess.

Auto-execute for both stages is correct: the human confirmed the aging design implicitly
by adopting it, and the informational summary provides a list of items being acted on,
giving a rescue window before Phase 3 runs.

90 and 180 days are starting thresholds. The first few months of operation will reveal
whether these need adjustment. They are human-editable in the schema.

**Alternatives Considered:**
- **Single-stage hard delete at 90 days:** Too aggressive; discards items that a future
  query might need. Ruled out.
- **Forced choice per deleted item:** Creates the exact friction the aging mechanism was
  meant to eliminate. Ruled out.
- **Semantic matching (IN-007 option c):** Requires search layer (IN-006) to be in place.
  Out of scope until that escalation trigger is reached.

**Consequences to Watch:**
- If `[stale-nominated]` regularly accumulates many items that are then deleted without
  ever being revived, the 180-day Stage 2 window may be too long — shorten to 120 days.
- If items are frequently rescued from `[stale-nominated]` via query demand signals,
  the 90-day Stage 1 threshold may be too aggressive — lengthen to 120 days.
- Items added before this schema change have no `nominated_date`. The aging pass skips
  them with an informational note. The human should manually add `nominated: YYYY-MM-DD`
  to pre-schema items during the first lint pass, or accept that they will never age out.

**References:** IN-007 (closes), DM-036

---

## DM-052 | Ingested-in-Error Correction Procedure: Binary Forced Choice, Tool Page stub Status

- **Date:** 2026-04-21
- **Status:** ACTIVE

**Decision:**
A new `status: ingested-in-error` value is added to the Source page controlled vocabulary,
distinct from `status: retracted`. A new Section 8.6 governs the correction procedure.
A new `stub` value is added to the Tool page `status` controlled vocabulary (mirroring
the existing Topic page `stub` value). The orphaned page forced choice is binary (delete
or retain as stub) — no "retain unchanged" option.

**Context:**
The retraction procedure (DM-025) covers sources that were valid at ingest and later
invalidated. It does not cover sources that were never valid — wrong documents, out-of-scope
material, misclassified types. That gap required a distinct procedure with three extensions
beyond retraction: (1) CTRD cleanup for flags where the bad source was the contesting
source; (2) orphaned page detection and disposition for pages created solely from the bad
source; (3) a new `stub` status for Tool pages to parallel the existing Topic page `stub`.

**Rationale:**
Keeping `retracted` and `ingested-in-error` as distinct status values preserves accurate
provenance semantics: "was valid, now invalidated" vs. "was never valid." Merging them
would conflate meaningfully different epistemic states. The binary forced choice for
orphaned pages (delete vs. retain as stub) was chosen over a three-option version that
included "retain unchanged." The argument for no third option: running the correction
procedure is a commitment to correction. Allowing "retain unchanged" permits the human to
declare a source a mistake and then keep all its content intact — which defeats the
procedure's purpose. The stub option already provides what "retain unchanged" appears to
offer (content preserved, page accessible) while correctly signaling that the page needs
re-sourcing. If the human wants to keep content without any correction, the correct
action is not to run the procedure at all. The `stub` addition to Tool pages was a
necessary corollary: without it, "retain as stub" is meaningful for Topic pages but
undefined for Tool pages, creating behavioral divergence.

The CTRD cleanup step (IE-2) is auto-execute because no human judgment is needed: if a
contradiction flag was generated by a source that was never valid, the incumbent claim
is restored unconditionally. There is nothing to weigh.

**Alternatives Considered:**
- **Merge with retracted status:** Conflates "never valid" with "was valid, now
  invalidated." Degrades provenance accuracy. Ruled out.
- **Retain unchanged as third option for orphaned pages:** Lets the human declare a
  mistake without correcting it. Undermines the procedure. Ruled out.
- **Manual CTRD cleanup (no auto-execute IE-2):** CTRD flags from an invalid contesting
  source require no human judgment — restoring the incumbent is the only correct outcome.
  Manual forced choice would add friction for zero epistemic benefit. Ruled out.
- **Reuse retraction forced choice format verbatim (including option C):** Option C
  ("Downgrade page status to stale and leave claim contested") makes no sense for a source
  that was never valid. Ruled out. The ingested-in-error forced choice has no option C.

**Consequences to Watch:**
- If the human frequently sets `status: ingested-in-error` on sources that were actually
  legitimate (confusing ingested-in-error with superseded), the provenance record will
  accumulate incorrect tombstones. The CONTRADICTION-SKILL.md Section 5a decision rule
  should catch this; monitor for misuse.
- If a correction pass reveals more than 20 affected Key Claims regularly, assess whether
  the ingest pre-flight classification steps (Steps 3–5) need tightening to prevent
  bad-source ingests at intake.
- The `stub` Tool page status interacts with lint Step L5 only through the `last_assessed`
  field being cleared on stub creation. If lint is ever revised to check `status: stub`
  directly, this implicit behavior must be made explicit.

**References:** DM-025, CLAUDE.md Sections 5.3, 5.4, 8.6; CONTRADICTION-SKILL.md Section 5a

---

## DM-053 | quartz.config.ts baseUrl Must Be Set During Initialization

- **Date:** 2026-04-22
- **Status:** ACTIVE

**Decision:**
INIT-PROMPT.md Step 9 must set `baseUrl` in `quartz.config.ts` as a required third
change (Change 3), prompting the human to replace a placeholder value with their actual
GitHub Pages URL before the first commit. The placeholder format is
`"<your-github-username>.github.io/<your-repo-name>"`. Claude Code pauses at this step
and waits for CONTINUE after the human makes the substitution.

**Context:**
After a successful Phase 1 initialization and Phase 2 build/deploy, the public site at
`fractalk.github.io/ai-auto-wiki` returned an RSS XML page instead of the Quartz wiki
interface. The RSS `<link>` field showed `https://quartz.jzhao.xyz` — the Quartz
default `baseUrl`. INIT-PROMPT.md Step 9 made two targeted changes to `quartz.config.ts`
(ignorePatterns and Plugin.Mermaid()) but did not touch `baseUrl`. The build succeeded
and GitHub Actions reported green; the misconfiguration was undetectable until the
published URL was visited.

**Rationale:**
`baseUrl` is a required personalization field: it cannot be automated (the repo name is
unknown to the initialization session), and its default value (`quartz.jzhao.xyz`) will
silently produce a broken site. A pause-and-confirm pattern at Step 9 is appropriate
because this is a single, explicit human-replacement step with a concrete format
constraint (no `https://` prefix). Embedding it in the initialization session rather
than in Phase 0 human prerequisites keeps it adjacent to the quartz.config.ts edits
being made in the same step.

**Alternatives Considered:**
- **Phase 0 prerequisite (human edits quartz.config.ts before Phase 1):** Valid, but
  removes the ability for Claude Code to verify the field was set and to guide the
  format. Ruled out in favor of the in-session pause pattern.
- **Phase 2 manual step (human fixes baseUrl before first push):** Places the step
  at the wrong abstraction level — quartz.config.ts configuration belongs in
  initialization, not in post-initialization verification. Ruled out.
- **Automate via quartz.config.ts template generation:** INIT-PROMPT.md is a one-time
  prompt that cannot know the human's GitHub username or repo name at authoring time.
  Automation is not possible without adding a prerequisite data-collection step.
  Ruled out as adding unnecessary complexity.

**Consequences to Watch:**
- If Quartz changes how `baseUrl` is specified (e.g., separates host from path, or
  adds a `pathPrefix` field), INIT-PROMPT.md Step 9 Change 3 will need updating.
- The pause-and-confirm pattern at Step 9 adds a human interaction not present in the
  original three-pause structure. If implementation feedback indicates the extra pause
  creates friction, consider combining it with Pause Point 3 (git remote setup).

**References:** FRIC-010, LL-012

---

## DM-054 | Operation-Specific Prompt Stubs in prompts/ Directory

- **Date:** 2026-04-22
- **Status:** ACTIVE

**Decision:**
Five pre-filled session-start prompt stub files are created in a `prompts/`
subdirectory at the wiki root: `ingest.md`, `lint.md`, `query.md`, `discovery.md`,
and `custom.md`. Each contains the full session-start template from
implementation-handoff.md Section 5 with the last line pre-filled for the relevant
operation. The stubs are committed to the repo (not gitignored). The `prompts/`
directory is added to `ignorePatterns` in `quartz.config.ts` so stubs are not
published to the public site. The stubs are not created by INIT-PROMPT.md — they are
delivered as separate files and placed manually by the implementer.

**Context:**
Starting a wiki session required five manual steps: open the handoff document, locate
Section 5, copy the template, edit the last line, paste into Claude Code. The edit
step is a friction point — a typo in the operation name produces an ambiguous or
incorrect session start.

**Rationale:**
Pre-filled stubs reduce the session-start sequence to: open file, select all, copy,
paste — zero editing required for LINT, DISCOVERY, and CUSTOM operations. INGEST
and QUERY retain one placeholder each (source list and query, respectively) because
those values are session-specific and cannot be pre-filled. Committing the stubs to
the repo makes them available on any machine without requiring the implementer to
re-create them from the handoff document. The `prompts/` directory does not require
Obsidian exclusion — stub files are harmless in the graph and visible in the vault
as a useful reference.

The "minimal stub" alternative (operation line only, with instruction to prepend
the canonical template) was considered and rejected: it requires two copy-paste steps
and still requires the human to locate the canonical template, defeating the purpose.

The sync obligation — stubs must be updated when Section 5 changes — is documented
in implementation-handoff.md Section 6 and parallels the LL-009 pattern. It is an
accepted trade-off: the consequence of drift is reduced human convenience, not a
functional failure (CLAUDE.md governs session behavior, not the stub header).

**Alternatives Considered:**
- **Minimal stubs (operation line only):** Two copy-paste steps; still requires
  locating the canonical template. Ruled out.
- **Wiki root placement (no subdirectory):** Adds noise to the root alongside
  quartz.config.ts, CLAUDE.md, and scaffold files. Ruled out in favor of
  `prompts/` subdirectory.
- **raw/ placement:** raw/ implies ingest pipeline involvement. Semantically
  incorrect. Ruled out.
- **Gitignored (local only):** Removes cross-machine portability. No sensitive data
  in stubs that would justify gitignoring. Ruled out.

**Consequences to Watch:**
- When implementation-handoff.md Section 5 template is updated, all five stub files
  must be updated in the same change. Failure to do so will cause stubs to drift.
  Monitor after any session that modifies the template.
- If the `prompts/` directory grows beyond the five canonical stubs (e.g., custom
  per-topic stubs), consider whether ignorePatterns or Obsidian exclusion needs
  updating.

**References:** LL-009, implementation-handoff.md Section 6

---

## DM-055 | Singleton Scaffold Files overview.md and log.md Excluded from Public Quartz Site; index.md Must Remain Public

- **Date:** 2026-04-22
- **Status:** ACTIVE

**Decision:**
`overview.md` and `log.md` are added to `quartz.config.ts` ignorePatterns and are
excluded from the public Quartz site. `index.md` is explicitly NOT excluded and must
remain in Quartz's input set.

**Rationale:**
`overview.md` (wiki state counters) and `log.md` (append-only operation log) are
machine-maintained internal files. Neither has a markdown body — both contain only
YAML frontmatter — so they render as blank pages. Exposing them leaks operational
metadata (page counts, contradiction IDs, operation timestamps) to public readers
with no benefit.

`index.md` must not be added to ignorePatterns. Quartz requires a root-level
`index.md` to emit `index.html` — the site's home page. When `index.md` is excluded,
Quartz emits no root HTML file; browsers receive `index.xml` (the RSS feed) instead
of the site interface. This was confirmed by accidental exclusion during FRIC-015
resolution.

**Alternatives Considered:**
- **Exclude index.md too:** Ruled out. Quartz cannot serve a home page without it.
  Confirmed by production failure (see FRIC-015, LL-013).
- **Give overview.md and log.md markdown bodies:** Possible but not implemented.
  These are operational state files; adding public-facing prose bodies would create
  a maintenance obligation (keeping prose in sync with automated state) for no clear
  reader benefit.
- **Keep all scaffold files public:** Produces blank pages in navigation and exposes
  operational metadata. Ruled out.

**Consequences to Watch:**
- `index.md` has only frontmatter and no markdown body. The public home page renders
  blank. This is a known gap; index.md should eventually receive a markdown body that
  serves as a meaningful landing page for public readers. See carry-forward agenda.
- `teaching-index.md` is intentionally kept public — it is a human-readable derived
  artifact, not a state file.

**References:** FRIC-015, LL-013

---

## DM-056 | index.md Landing Page Design: Static Prose + Generated At a Glance Line

- **Date:** 2026-04-22
- **Status:** ACTIVE

**Decision:**
`index.md` receives a two-paragraph static intro zone, a single generated "At a Glance"
line, and a horizontal rule separator above the existing catalog sections. The YAML
`title` field is changed from `"Wiki Index"` to `"AI Effectiveness Wiki"`. Claude Code
updates the At a Glance line on every ingest; the intro zone is written once by the
wiki owner and never modified by Claude Code.

**Context:**
`index.md` had only YAML frontmatter and section headers. The public home page at
the Quartz site rendered blank. DM-055 documented this as a known gap. This decision
resolves it.

**Rationale:**
The intro prose gives first-time visitors immediate context on the wiki's scope and
audience. It is written once because prose framing is a value judgment — Claude Code
should not regenerate it, as automated rewriting could subtly shift the framing without
the owner noticing. The At a Glance line (page count + last updated date) is the only
part that benefits from automated maintenance; it derives entirely from fields Claude
Code already maintains in `overview.md`. Keeping the generated element minimal limits
the surface area of the ingest-step change. The title change from "Wiki Index" to
"AI Effectiveness Wiki" is required because Quartz renders the `title` frontmatter
field as the page H1 — "Wiki Index" is an operational label, not a public identity.

**Alternatives Considered:**
- **"Recently Added" section:** Redundant with the existing catalog sections (which
  already list all pages). Adds a new ingest step for minimal reader gain. Ruled out.
- **Teaching-indexed count in At a Glance:** Requires a new `overview.md` field or a
  scan of `teaching-index.md` to count entries. Disproportionate schema change for one
  statistic; the wikilink to `[[teaching-index]]` in the intro prose serves the same
  discovery purpose. Ruled out.
- **Quartz theming/layout customization:** Would require changes to `quartz.config.ts`
  outside CLAUDE.md's authority. Out of scope. Ruled out.
- **Full dynamic regeneration of intro prose:** Automated rewriting could shift framing
  without the owner noticing. Prose is a one-time human judgment. Ruled out.

**Consequences to Watch:**
- The intro prose references `[[teaching-index]]` via wikilink. If the teaching-index
  is excluded from the Quartz site (currently it is not in ignorePatterns — this is
  intentional per DM-055), the link renders correctly. If the teaching-index is ever
  excluded, this wikilink becomes broken on the public site.
- The At a Glance page count reads from `overview.md:total_pages`. If Claude Code ever
  writes index.md before incrementing `total_pages` in a given ingest session, the
  count will be one behind. The Section 12 generation rule specifies "after incrementing"
  to prevent this.
- CLAUDE.md is now at approximately 2,405 lines. DM-040 split-assessment trigger is
  2,500 lines. Monitor in the next session.

**References:** DM-055, FRIC-015

---

## DM-057 | Budget Forced Choice Counts Staged Files and Queued URLs Equally

- **Date:** 2026-04-22
- **Status:** ACTIVE

**Decision:**
Step 0 budget check counts N = (staged files in `raw/staged/`) + (items in the
`[queued]` section of `raw/queue.md`). Both sources count as 1 item each. The
threshold (≤5 = no forced choice) is unchanged. The forced choice block template
now shows the breakdown: `{a} staged files + {b} queued URLs = {N} total items`.

**Context:**
FRIC-017 identified that the prior Step 0 counted only `[queued]` items. A session
with 2 queued URLs and 4 staged files was approved as a 2-item session. Staged files
are systematically heavier sources (they exist on the staged path precisely because
they are too long for the URL fetch path), making this undercount structurally biased.

**Rationale:**
Equal weighting (1:1) is the defensible default without empirical data on relative
session costs. Staged files do tend to be longer, but the variability within each
category is high enough that a fixed weight multiplier would be arbitrary. The
threshold stays at 5 because that calibration was based on session experience and
changing it requires its own empirical justification. IN-007 (P3) is the correct
vehicle for threshold revision when data is available.

**Alternatives Considered:**
- **Weight staged files at 1.5x:** Arbitrary without data. Ruled out.
- **Separate thresholds for staged and queued:** Adds complexity; the human should
  see one number when deciding how much to process. Ruled out.
- **Lower threshold to 4:** No empirical basis. Ruled out.

**Consequences to Watch:**
- If the combined count triggers the forced choice more often than expected, assess
  whether the threshold needs upward adjustment (IN-007).
- The deferral note (`raw/deferred-ingest.md`) now records the breakdown at time
  of deferral, keeping the count auditable.

**References:** FRIC-017, IN-007

---

## DM-058 | Post-Ingest Summary Split into Section A (Informational) and Section B (Forced Choices)

- **Date:** 2026-04-22
- **Status:** ACTIVE

**Decision:**
Step 22 post-ingest summary is restructured into two explicit sections. Section A
contains all informational output. Section B contains all forced choices, each labeled
PS-N in sequence (citations first, then skill enrichment candidates). Section B is
omitted entirely when there are no forced choices. The response format instruction
(`Respond with: PS-1:X PS-2:X ...`) opens Section B. The PS-N namespace is distinct
from the pre-flight `N:X` namespace.

**Context:**
FRIC-018 identified that the prior Step 22 template interleaved forced choices with
informational lines. Without a consistent numbering scheme, the human was required to
write verbose answers to establish which response mapped to which question.

**Rationale:**
Separating informational content from decisions reduces cognitive load and enables
the compact `PS-N:X` response format. Two namespaces (pre-flight `N:X`, post-ingest
`PS-N:X`) are intentionally distinct: pre-flight choices are resolved before execution
begins; post-ingest choices are resolved after all writes are complete. Conflating
them would require renumbering across phases without benefit. Citations are assigned
lower PS-N numbers than skill enrichment proposals because they are structurally
simpler (A/B only) and benefit from appearing first.

**Alternatives Considered:**
- **Numbering only, no section split:** Reduces verbosity of responses but does not
  resolve the cognitive overhead of scanning a mixed block. Ruled out in favor of
  the section split.
- **Extend pre-flight numbering into post-ingest:** Requires the agent to track a
  running counter across two phases with no execution interleaved. Error-prone.
  Ruled out.

**Consequences to Watch:**
- If future forced choice types are added to the post-ingest summary, they must be
  assigned PS-N positions and documented in Step 22 with their ordering rule.
- Step 21a skill enrichment draft items are held until Step 22 assembly — the agent
  must not output them mid-session before the summary.

**References:** FRIC-018

## DM-059 | Source Enrichment Path: Step 2a and enriched Frontmatter Field

- **Date:** 2026-04-22
- **Status:** ACTIVE

**Decision:**
Step 2 duplicate detection now differentiates between accidental duplicates and
intentional enrichment attempts. For an exact URL match where the existing source page
has `status: active`, a forced choice is surfaced (Abort / Enrich). Path B executes a
new Step 2a that updates the source page's `updated` and `enriched` frontmatter fields,
skips classification Steps 3–5 and source page creation Step 10, applies a downstream
deduplication check before contradiction resolution in Steps 11–13, and uses a distinct
commit message (`enrich: {slug}`). A new optional `enriched` ISO 8601 date field is
added to the source page frontmatter spec. Section 5.4 prose is updated to list
enrichment as the third exception to source page immutability (alongside `superseded_by`
population and `status` correction). Hard stop on exact URL match is preserved for
`status: retracted` and `ingested-in-error` pages.

**Context:**
FRIC-019 identified that Step 2 had a single response to all exact URL matches: stop.
This correctly handles accidental re-ingest but incorrectly blocks the valid case where
a human has a richer version of an already-ingested source — most commonly a full
Obsidian browser clip replacing a web-fetch-truncated extraction. The pattern becomes
more common as the wiki grows, because long sources increasingly require the staged
path, and staged sources are sometimes clipped more completely on a second attempt.

**Rationale:**
The enrichment path is a meaningful operational case that should be handled by the
schema rather than forcing the human to manually edit source pages outside the workflow.
Conditioning the forced choice on `status: active` preserves the intent of the hard
stop (do not re-open retracted or erroneously-ingested sources) while enabling the
enrichment case. The deduplication check in Step 2a prevents contradiction resolution
noise from claims that are substantively identical to what is already on downstream
pages — without it, every enriched ingest would surface spurious Path A auto-resolutions
for claims that haven't actually changed.

**Corrections applied during execution** (departures from the carry-forward fix plan):
1. `status: superseded` replaced with `status: ingested-in-error` — source pages have
   no `superseded` status; the controlled values are `active | retracted |
   ingested-in-error`. The carry-forward used Tool page vocabulary by mistake.
2. "Overwrite source page body and Key Claims section" removed — source pages contain
   only frontmatter; they have no body section and no Key Claims section. The enrichment
   operation updates source page frontmatter only; downstream Key Claims live on Topic
   and Tool pages and are handled by Steps 11–13 with the deduplication check.

**Alternatives Considered:**
- **Permanent hard stop on all URL matches:** Simple but blocks a legitimate and
  increasingly common operational case. Ruled out.
- **Allow re-ingest freely without deduplication check:** Creates contradiction
  resolution noise for substantively identical claims. Ruled out.
- **Separate enrichment command outside the ingest flow:** Adds operational complexity
  without benefit; the ingest flow already has all the required machinery. Ruled out.

**Consequences to Watch:**
- CLAUDE.md is now at 2,468 lines — 32 lines from the DM-040 split-assessment trigger
  of 2,500. The next change that adds significant content should include a line-count
  assessment before writing.
- If enrichment is performed a second time on the same source, the `enriched` field
  is overwritten with the new date. The prior enrichment date is not preserved. If
  enrichment history becomes operationally important, a list-valued `enriched` field
  should be considered at that time.

**References:** FRIC-019, DM-040

## DM-060 | SOURCE PAGE BODY, INGEST PROVENANCE, AND PROCESSED ARCHIVE (FRIC-020/021/022)

- **Date:** 2026-04-23
- **Status:** ACTIVE

**Decision:**
Three schema additions made together: (1) source page body paragraph is now a required
specified element (Section 5.4); (2) `ingest_via` field added to source page frontmatter
(Section 5.4, Step 10); (3) `raw/processed/` archive and `## [processed]` queue section
added (Section 2, Section 2.1, Step 22b).

**Context:**
Investigation of two frontmatter-only source pages revealed three distinct schema gaps:
the summary paragraph was emergent/unspecified; no intake mechanism was persisted to source
pages; and consumed sources were deleted rather than archived. These gaps blocked retroactive
diagnosis and left correct behavior unprotected against regression.

**Rationale:**
All three fixes address permanent structural weaknesses rather than one-off operational
problems. Specifying the body prevents silent regression. `ingest_via` makes future anomaly
diagnosis tractable. The processed archive preserves audit trail without requiring any
additional tooling — git already tracks the move.

**Alternatives Considered:**
- **Defer ingest_via until anomaly recurs:** Ruled out — the whole point of a provenance
  field is to capture data prospectively. Retroactive diagnosis is impossible by definition.
- **Delete rather than move to processed/:** Current behavior. Ruled out — loses all audit
  trail. The archive imposes no operational cost beyond human pruning.
- **staged-url-fallback as third ingest_via value:** Deferred. The fallback mechanism is
  undefined in the schema; a vocabulary value for undefined behavior is premature.

**Consequences to Watch:**
- CLAUDE.md is now at 2,503 lines, 3 over the DM-040 split-assessment threshold.
  Section 11 → OPERATIONS.md split is the planned remediation; execute before the next
  substantive addition.
- Two pre-schema source pages (Stanford HAI and Mollick) are now out of conformance on
  the body paragraph requirement. Human must decide on remediation.
- `staged-url-fallback` vocabulary value deferred; add to `ingest_via` spec when the
  fallback mechanism is defined.

**References:** FRIC-020, FRIC-021, FRIC-022

---

## DM-061 | CLAUDE.md Split Architecture: Option 2 (OPERATIONS.md + Hard Gate), Deferred to 3,000-Line Trigger

- **Date:** 2026-04-23
- **Status:** ACTIVE
- **Supersedes:** DM-040

**Decision:**
The agreed long-term split architecture is Option 2: extract Section 11 (operational
workflows) verbatim into a peer document `OPERATIONS.md`, with a hard gate instruction
at the top of CLAUDE.md Section 1. The hard gate reads: "If OPERATIONS.md is not present
in this context, output the string MISSING-OPERATIONS-FILE and halt before taking any
other action." The split is not executed now. It executes when CLAUDE.md reaches 3,000
lines OR when a procedural error attributable to document depth is confirmed — whichever
comes first.

**Context:**
DM-040 deferred splitting on the grounds that a peer document split requires the
session-start prompt to coordinate multiple file loads, and that forgetting to load a
required file silently produces wrong behavior. DM-040's trigger for reassessment was
"2–3x current size through schema revision." CLAUDE.md is now at 2,503 lines (~20K
tokens) with no observed instruction-following degradation on Section 11 content.
The question "what is the sustainable architecture as CLAUDE.md grows to 3,000, 4,000,
5,000 lines?" was assessed with two distinct risks in view: Risk A (context window
exhaustion — not live for a long time at current growth rates) and Risk B
(instruction-following degradation as operational procedures drift deeper into context).

**Rationale:**
Option 2 with a hard gate addresses DM-040's core concern directly. The gate is a
simple binary instruction placed at the top of CLAUDE.md, the most reliably followed
position in a long document. A hard halt converts a silent failure into a loud one. The
failure mode DM-040 worried about — an improvised ingest procedure because a file was
not loaded — is blocked. Option 3 (per-operation skill files) was evaluated and ruled
out on two grounds: (a) it blurs the semantic distinction between authoritative procedure
files and teaching/example files, making it unclear to a future maintainer which files
govern behavior; (b) it requires three files to update when a cross-cutting schema change
is made, versus two for Option 2. Option 4 (decide architecture now, execute at a
concrete trigger) was selected as the timing wrapper because no functional failure has
been observed and clean execution under a planned trigger is preferable to reactive
splitting under pressure.

**Alternatives Considered:**
- **Option 1 (no split, DM-040 status quo):** Ruled out. DM-040's consequence clause
  was "reassess at 2–3x current size." Current size is within that range. Deciding the
  architecture now avoids re-litigating the question under time pressure.
- **Option 3 (per-operation procedure files):** Ruled out. See rationale above.
- **Execute the split now (Option 2, immediate):** Ruled out. No functional failure
  justifies the complexity cost today. The 2,503-line breach is 3 lines over a soft
  cosmetic threshold. Execute at the trigger.

**Execution Obligations at Trigger:**
When CLAUDE.md reaches 3,000 lines or a procedural error attributable to document depth
is confirmed:
1. Move Section 11 (11.1–11.5) verbatim to OPERATIONS.md at wiki root.
2. Add hard gate to CLAUDE.md Section 1: "If OPERATIONS.md is not present in this
   context, output MISSING-OPERATIONS-FILE and halt before taking any other action."
3. Update CLAUDE.md Section 1 to reference OPERATIONS.md explicitly.
4. Update all session-start prompt stubs in prompts/ to name both CLAUDE.md and
   OPERATIONS.md.
5. Update implementation-handoff.md session-start template (Section 5).
6. Update INIT-PROMPT.md to scaffold OPERATIONS.md and include it in verification.
7. Audit EXTRACTION-SKILL.md, TAGGING-SKILL.md, CONTRADICTION-SKILL.md for
   "Section 11.x" cross-references; update to "OPERATIONS.md Section 11.x".
8. Update portability-review.md entries that cite "Section 11.x".
9. Add a DM entry recording the split execution and confirming all obligations met.

**Consequences to Watch:**
- Schema-to-operations cross-references (Section 5 frontmatter fields, Section 7
  controlled vocabularies, Section 8 contradiction logic) cross a file boundary after
  the split. A change to any referenced section requires auditing OPERATIONS.md as well
  as CLAUDE.md. This is manageable with the existing cross-reference check discipline
  but is a new ongoing obligation to register.
- If instruction-following degradation on Section 11 content is observed before 3,000
  lines, execute the split immediately rather than waiting for the line count trigger.

**References:** DM-040, FRIC-020/021/022, DM-060

---

## DM-062 | PODCAST-TRANSCRIPT ADDED AS 9TH SOURCE TYPE

- **Date:** 2026-04-25
- **Status:** ACTIVE

**Decision:**
`podcast-transcript` added as the 9th source type. Extraction depth: `standard`. Credibility
tier: `institutional` if the show is produced by or features an official AI lab or research
institution as primary host; `practitioner` otherwise. `transcript_file` required (same as
`youtube-video`). Partial transcripts accepted with a note in the source page body.

**Context:**
A podcast transcript was submitted for ingest. No `podcast-transcript` source type existed.
The human used `youtube-video` as a workaround. The classification was semantically wrong
and would generate noise at ingest (agent would see `source_type: youtube-video` with a
transcript from a podcast feed and no video URL).

**Rationale:**
The type gap was real and would recur. Luminary elevation (treating select individuals'
informal content at a higher credibility tier) was evaluated and rejected: it introduces
a person-list maintenance burden, breaks the automation property, creates political
subjectivity, and ages badly. The corroboration mechanism is the correct long-term
answer for informal content that later proves influential. Adding the source type fixes
the classification gap without any of the elevation risks.

**Alternatives Considered:**
- **Keep `youtube-video` as the workaround:** Semantically wrong; generates ingest noise;
  does not scale cleanly to transcripts without video URLs. Ruled out.
- **Add luminary elevation / `influential` flag:** Evaluated at length. Rejected on grounds
  of subjectivity, maintenance burden, broken automation, list-aging, and suppression of
  legitimate contradictions. See session discussion for full red-team.

**Consequences to Watch:**
- Credibility tier for podcasts: the institutional test (official AI lab or research
  institution as primary host) is tighter than some shows that carry genuine weight.
  Monitor whether this produces systematic under-weighting of high-signal shows that
  don't meet the institutional host bar.

**References:** FRIC-023

---

## DM-063 | PITFALLS PAGE CREATION GAP IN INGEST WORKFLOW FIXED

- **Date:** 2026-04-25
- **Status:** ACTIVE

**Decision:**
Two additions to the ingest workflow: (1) Step 7a — a conditional pre-flight trigger
that proposes Pitfalls page creation or update when a source contains at least one
substantive failure mode (nameable `### [Failure mode name]` entry with `**Status:**`
designation); (2) Step 13a — the corresponding execution step that creates or updates
the Pitfalls page if confirmed. The routing rule (cross-cutting antipatterns to
Topic-scoped pages, not Tool pages) applies at both steps.

**Context:**
Sources intentionally selected to build out the Pitfalls section were being routed
exclusively to Topic and Tool pages. No ingest step existed to route failure mode
content to Pitfalls pages. The human had to override the agent's suggestions manually
to get content into Pitfalls pages — the correct behavior, but not intended behavior.
`EXTRACTION-SKILL.md` correctly identifies failure modes as "candidates for Pitfalls
pages, not Key Claims" during extraction, but that routing was never picked up by any
downstream ingest step.

**Rationale:**
The pre-flight/execution split mirrors the existing Comparison page mechanism (Step 7 /
Step 15), which is the established pattern for conditional page creation at ingest. The
substantive threshold (nameable failure mode, not passing mention) prevents noise from
sources that mention limitations incidentally. Routing rule enforcement at pre-flight
prevents cross-cutting antipatterns from being incorrectly scoped to Tool pages.

**Alternatives Considered:**
- **Auto-create Pitfalls pages without pre-flight proposal:** Removes human confirmation
  from a page creation decision. Ruled out — consistent with the principle that page
  creation is never automatic.
- **Lower threshold (any limitation mention qualifies):** Too noisy; most sources
  mention limitations in passing. Ruled out.

**Consequences to Watch:**
- If Pitfalls pages are still rarely created despite Step 7a being in place, assess
  whether the substantive threshold is calibrated correctly.
- Step 13a's routing rule (cross-cutting → Topic page) requires the agent to make a
  scoping judgment during pre-flight. This may produce forced choices when scoping is
  ambiguous — monitor for excessive friction.

**References:** FRIC-024

---

## DM-064 | OVERRIDE PATTERN DETECTION AND SCHEMA SIGNALS ESCALATION PATH

- **Date:** 2026-04-25
- **Status:** ACTIVE

**Decision:**
Two additions: (1) Lint Step L12c — reads `wiki-lessons-learned.md` ingest and lint
sections, counts override entries by category over the past 30 days, auto-writes a
`## Schema Signals` entry if any category reaches 3+ overrides, no forced choice;
(2) `## Schema Signals` section added to `wiki-lessons-learned.md` with a distinct
entry format that names five root cause hypotheses explicitly. Schema Signals entries
accumulate as an open backlog. The human decides whether to bring a signal to a design
session as a friction report. Root cause identification and resolution are design-session
work, not wiki-agent work.

**Context:**
No mechanism existed to detect systematic override patterns. Individual overrides were
captured in `wiki-lessons-learned.md` per DM-024, but nothing aggregated them. Without
aggregation, a recurring definition problem looks identical to a one-time edge case.
The five root causes identified: (1) schema definition overlap; (2) inference gap; (3)
human preference drift; (4) vocabulary gap; (5) source ambiguity. Root causes 1–4
require design-session intervention; root cause 5 resolves via wiki-lessons-learned.md
precedent entry without escalation.

**Rationale:**
Time-windowed threshold (30 days, 3+ overrides) chosen over cumulative-since-schema-change
for simplicity — the more semantically correct option requires linking override entries
to schema change dates. The simpler approach is adequate: a pattern that fires and
resolves within 30 days will stop firing naturally; a persistent pattern will keep
signaling. Auto-execute (no forced choice) is correct because the signal itself requires
no human decision — only the downstream design-session response does.

**Alternatives Considered:**
- **Cumulative-since-schema-change threshold:** More semantically correct; requires
  cross-linking override entries to DM entries with dates. Too complex for marginal
  benefit. Ruled out.
- **Agent proposes schema fix directly:** Agent modifying its own governing document
  is a different and riskier operation than surfacing a signal. Ruled out.
- **Named-person tier elevation as the fix:** Evaluated and rejected separately (DM-062).

**Consequences to Watch:**
- If the 30-day window produces too many false positives (brief clusters that resolve
  themselves), consider raising the threshold to 5 or extending the window to 60 days.
- If Schema Signals entries accumulate without resolution (human never brings them to
  a design session), the backlog becomes noise. Monitor at first lint pass that fires
  the signal.

**References:** FRIC-026

## DM-065 | PITFALLS PAGES CONFIRMED AS ENTITY-SCOPED SYNTHESIS DESIGN

- **Date:** 2026-04-25
- **Status:** ACTIVE

**Decision:**
Pitfalls pages are entity-scoped — one page per parent Tool or Topic entity. Multiple
sources contributing failure modes for the same entity compound into a single Pitfalls
page via the Step 13a update path. The current appearance of isolated per-source documents
reflects sample size (one source per entity), not a design flaw. The alternative of three
cross-category synthesis pages (one per failure mode category across all entities) was
evaluated and rejected.

**Context:**
Post-implementation review showed two Pitfalls pages, both created under manual override
before Steps 7a and 13a existed. The human questioned whether the design intent was
per-source isolation or cross-source synthesis, and whether the section would grow as
independent per-source documents rather than compounding per-entity documents.

**Rationale:**
Entity-scoped design correctly answers the primary Pitfalls query pattern ("what are
the pitfalls of GPT-4o?") with a focused, navigable result. Cross-cutting antipatterns
are handled separately via the routing rule directing them to Topic-scoped Pitfalls pages.
Three cross-category synthesis pages would become unmaintainably large, lose entity
context, fail the primary query pattern, and make contradiction detection and source
attribution intractable.

**Alternatives Considered:**
- **Three cross-category synthesis pages:** Fails the primary "pitfalls of X" query
  pattern; strips entity context from failure modes; no tractable unit of work for
  contradiction detection or source attribution. Ruled out.

**Consequences to Watch:**
- When the same entity accumulates multiple source ingests, the Pitfalls page will
  compound visibly. Sample size is the current limiting factor, not the design.
- If a Pitfalls page for a single entity grows very long (many failure modes from many
  sources), assess whether a page split is warranted — the same 1,200-word ceiling
  does not apply directly to Pitfalls pages, but very long pages degrade query
  response readability.

**References:** FRIC-024, DM-063

---

## DM-066 | PITFALLS FAILURE MODE ENTRIES REQUIRE SOURCE ATTRIBUTION

- **Date:** 2026-04-25
- **Status:** ACTIVE

**Decision:**
Each `### [Failure mode name]` entry in a Pitfalls page must include a `**Source:**`
citation line immediately after the `**Status:**` line, referencing the contributing
source page via short-form wikilink. A `contributing_sources` list field is added to the
Pitfalls page frontmatter spec (Section 5.6), tracking source page wikilinks for all
sources that have contributed failure mode entries to the page. The retraction procedure
(Section 8.2) and ingested-in-error correction (Section 8.6) must be updated to scan
Pitfalls pages and surface failure mode entries whose sole contributing source is the
affected source page.

**Context:**
The two existing Pitfalls pages contain empirically specific claims traceable to named
benchmarks and studies (e.g., Tow Center benchmark figures, Stanford RegLab error rates),
but carry no source attribution at the failure mode entry level. The retraction and
ingested-in-error procedures were entirely blind to Pitfalls content. The failure mode
entries have no freshness mechanism independent of source page status.

**Rationale:**
Pitfalls will be explicitly queried, and query outputs will surface specific failure mode
claims to end users. The evolution of failure modes over time — a stated design goal, since
what goes wrong with models in 2024 differs from 2027 — requires knowing which sources
established each failure mode and which later sources superseded or mitigated them. Without
attribution, retraction events leave invalid failure mode entries in the wiki permanently.

**Alternatives Considered:**
- **Treat Pitfalls as documentary content outside retraction scope:** Simpler, but
  creates a class of wiki content that cannot be cleaned up when its evidentiary basis
  is invalidated. Ruled out — the wiki's integrity model should be uniform.
- **Page-level attribution only (contributing_sources frontmatter, no per-entry citation):**
  Enables retraction detection but does not identify which specific failure mode entries
  came from which source. Insufficient when multiple sources contribute and only one is
  retracted. Ruled out in favor of per-entry attribution.

**Consequences to Watch:**
- Step 13a update path must be updated to write the `**Source:**` line when adding new
  failure mode entries to an existing Pitfalls page.
- The retraction and correction procedures will become more complex — they now have three
  types of content to handle: Key Claims rows, orphaned pages, and failure mode entries.
- The two existing Pitfalls pages are retroactively out of conformance on this requirement.
  Human must manually add `**Source:**` lines to existing entries or re-ingest under the
  updated Step 13a.

**References:** GAP-001, IN-009

---

## DM-067 | DESIGN GOVERNANCE FILES RECOMMENDED FOR WIKI REPO STORAGE IN design/ DIRECTORY

- **Date:** 2026-04-25
- **Status:** ACTIVE

**Decision:**
The design project governance files (decisions_made.md, lessons_learned.md, info_needs.md,
CLAUDE.md, implementation-friction.md, portability-review.md, tooling-recommendation.md,
implementation-handoff.md, INIT-PROMPT.md, EXTRACTION-SKILL.md, TAGGING-SKILL.md,
CONTRADICTION-SKILL.md, and related artifacts) are recommended to be stored in a `design/`
subdirectory in the wiki git repository. Nothing else about the current workflow changes:
files continue to be iterated in this Claude.ai design project and downloaded at session
end; the human commits them to `design/` after download. The `design/` directory is added
to Quartz `ignorePatterns` so its contents are never published to the public site.

**Context:**
User asked whether consolidating the design project into Claude Code was feasible and
whether it would simplify the workflow. The full consolidation was evaluated as a distinct
question from storage location.

**Rationale:**
Git version control on the governance files provides history, cross-machine access, and a
single canonical location at zero operational cost beyond the human's existing commit habit.
The full consolidation of design sessions into Claude Code was evaluated and rejected:
design mode (skeptical, advisory, push back on weak reasoning) and execution mode
(imperative, no improvisation, stop and surface gaps) are different operational postures
that benefit from separate contexts. Merging them risks modal contamination — an agent
evaluating its own schema changes while also executing them. The current separation has
produced 65+ decisions and 19 lessons learned with good discipline. The `design/` storage
recommendation captures most of the version-control benefit without blurring the
design/execution boundary.

**Alternatives Considered:**
- **Full consolidation into Claude Code:** Feasible technically; rejected on grounds of
  modal contamination risk and loss of the separation discipline that has worked well.
- **External git repo separate from wiki:** Adds a second repo to manage; the wiki repo
  is already the canonical artifact home. Ruled out.
- **Current state (no git storage):** Loses version history and requires manual file
  tracking across sessions. Ruled out.

**Consequences to Watch:**
- `design/` must be added to Quartz `ignorePatterns` before first publish after this
  directory is created, or governance files will appear as public wiki pages.
- If Claude Code is ever asked to read governance files during a wiki maintenance session,
  the `design/` path must be confirmed (not assumed to match project file names exactly).

**References:** DM-002

---

## DM-068 | SPEC AUDIT GAP DISPOSITIONS — GAPS 001–010

- **Date:** 2026-04-25
- **Status:** ACTIVE

**Decision:**
Following a thorough spec audit identifying ten structural gaps in CLAUDE.md, the
following dispositions were confirmed by the human:

| Gap | Description | Disposition | Tracking |
|-----|-------------|-------------|----------|
| GAP-001 | Pitfalls source attribution missing | Actionable | IN-009 |
| GAP-002 | Lint L11 false summary violations | Actionable | IN-010 |
| GAP-003 | Stale → current transition missing | Actionable | IN-011 |
| GAP-004 | Comparison pages undocumented as derived artifacts | Informational | CLAUDE.md §5.5 |
| GAP-005 | vendor_bias algorithmic effect undocumented | Informational | CLAUDE.md §8 |
| GAP-006 | open_contradictions counter drift undetected | Actionable | IN-012 |
| GAP-007 | Discovery pass cadence and lint trigger absent | Deferred | — |
| GAP-008 | Schema Signals entries have no aging mechanism | Actionable | IN-013 |
| GAP-009 | Teaching Index stub page inclusion undocumented | Actionable | IN-014 |
| GAP-010 | No ingest-time signal for Comparison page staleness | Deferred | — |

**Context:**
Spec audit conducted after user observed that two sources ingested to populate the Pitfalls
section produced isolated per-entity pages rather than a synthesized cross-source view. This
was confirmed as intended behavior (DM-065), but prompted a broader audit for structurally
similar gaps where data was captured but not acted on, checks were performed but not producing
output, or workflows were defined but had incomplete thread-through.

**Rationale:**
The I-disposition items (GAP-004 and GAP-005) require minor CLAUDE.md additions — one
sentence each — but no structural changes or new procedures. The D-disposition items
(GAP-007 and GAP-010) have existing mitigation (GAP-007: human-triggered pass;
GAP-010: lint L5 catches staleness) and low urgency relative to the A items.

**Consequences to Watch:**
- CLAUDE.md will grow by an estimated 80–150 lines from A and I gap implementations.
  Combined with current count (2,598 lines), the OPERATIONS.md split trigger (3,000 lines
  per DM-061) may be reached within this set of changes. Sequence gap implementations
  before the split decision point — do not execute the split mid-gap-fix session.
- The two existing Pitfalls pages are retroactively out of conformance on GAP-001.
  Manual remediation required (add `**Source:**` lines to all existing failure mode entries).

**References:** DM-061, DM-065, DM-066, IN-009, IN-010, IN-011, IN-012, IN-013, IN-014

---

## DM-069 | GAP IMPLEMENTATIONS — IN-009 THROUGH IN-014 AND GAP-004/GAP-005

- **Date:** 2026-04-25
- **Status:** ACTIVE

**Decision:**
All six actionable gaps (IN-009 through IN-014) and both informational additions
(GAP-004, GAP-005) from the DM-068 spec audit were implemented in CLAUDE.md in a
single batch session. The following changes were made:

| Item | Change | Section(s) |
|------|--------|------------|
| IN-009 | Added `**Source:**` line to failure mode entry format; added `contributing_sources` frontmatter field; extended Step 13a; extended Section 8.2 retraction and Section 8.6 IE-3 to scan Pitfalls pages | 5.6, 8.2, 8.6, Step 13a |
| IN-010 | Narrowed summary field check to Topic and Tool pages only | Step L11 |
| IN-011 | Added Step L5a (stale→current forced choice) and Phase 3 item 4a | Steps L5a, Phase 3 |
| IN-012 | Added Step L4c (counter reconciliation) and extended Phase 3 item 11 and L13 summary | Steps L4c, Phase 3, L13 |
| IN-013 | Added Step L12d (Schema Signals age check) and L13 summary line | Steps L12d, L13 |
| IN-014 | Extended Section 10 generation rule 2 to exclude stub pages | Section 10 |
| GAP-004 | Added derived artifact note to Section 5.5 | Section 5.5 |
| GAP-005 | Added vendor_bias annotation note after credibility weights | Section 8.2 |

**Context:**
These were the six actionable and two informational gaps identified in the DM-068 spec
audit. All had confirmed dispositions and resolution text in info_needs.md before
implementation began.

**Rationale:**
Batch execution in a single pass minimizes inconsistency risk — all related changes land
together. Sequencing from simplest to most complex reduced the chance that an early error
would corrupt the anchor text for later changes.

**Alternatives Considered:**
- **Incremental delivery across sessions:** Higher risk of partial consistency states
  where some gaps are closed and others are open on the same schema version. Ruled out.

**Consequences to Watch:**
- CLAUDE.md is now at 2,702 lines. OPERATIONS.md split trigger is 3,000 lines. Approximately
  298 lines of headroom remain before the split must execute. Monitor on next substantive
  schema addition.
- Two existing Pitfalls pages are retroactively out of conformance on IN-009 (no `**Source:**`
  lines on failure mode entries, no `contributing_sources` frontmatter). Manual remediation
  required by the human before next ingest.
- IN-006 remains open P3. Resolve before wiki reaches 150 pages.

**References:** IN-009, IN-010, IN-011, IN-012, IN-013, IN-014, DM-068

---
## DM-070 | Design Project Governance Files Versioned in wiki/design/ with Quartz Exclusion

- **Date:** 2026-04-25
- **Status:** ACTIVE

**Decision:**
Design project governance files (info_needs.md, decisions_made.md, lessons_learned.md,
portability-review.md, tooling-recommendation.md, implementation-handoff.md,
INIT-PROMPT.md, LLM_Wiki_by_Karpathy.md) are stored in a `design/` subdirectory at
the wiki repository root for version control purposes. `"design/**"` is added to
`quartz.config.ts` ignorePatterns so the directory is excluded from the public site.
The wiki agent (Claude Code) is explicitly prohibited from reading, creating, or
modifying any file in `design/`.

**Context:**
The design project files are authoritative governance artifacts produced in a Claude.ai
design project, which has no independent version history. Storing them in the wiki repo
provides durable backup and change history for a set of files that govern the wiki's
behavior.

**Rationale:**
Version control benefit is worth the agent proximity risk given: (1) the files are
distinctly named and do not follow wiki naming conventions, making misidentification
unlikely; (2) an explicit CLAUDE.md prohibition provides a clear behavioral boundary;
(3) the alternative (separate repo or no versioning) adds friction or eliminates the
backup entirely.

**Alternatives Considered:**
- **Separate repository:** Cleaner separation but adds friction for a single-owner
  project. Ruled out.
- **Gitignore design/ (local only):** Defeats the version control benefit. Ruled out.
- **No version control for design files:** Relies solely on Claude.ai project chat
  history, which is not independently versioned. Ruled out.

**Consequences to Watch:**
- If the wiki agent performs broad file operations (e.g., `find .` during lint) it will
  encounter `design/` contents. The CLAUDE.md prohibition is the sole guard. Monitor
  for agent behavior that disregards it.
- CLAUDE.md, EXTRACTION-SKILL.md, TAGGING-SKILL.md, and CONTRADICTION-SKILL.md are
  operational wiki files that live in the wiki root — NOT in `design/`. Two copies of
  these files must not exist in the repo.

**References:** CLAUDE.md Section 2

---

## DM-071 | WIKI TEST HARNESS — TIER 1 SHELL SCRIPT ONLY; TIER 2 DROPPED

- **Date:** 2026-04-25
- **Status:** ACTIVE

**Decision:**
The wiki test harness consists of a single Tier 1 configuration and conformance check
script (`wiki-verify.sh`). Tier 2 workflow smoke tests were designed but then dropped
before adoption. Behavioral conformance relies on real operations serving as their own
tests, with anomalies surfacing as FRIC entries through the existing escalation path
(Option C).

**Context:**
Two tiers of verification were initially designed: Tier 1 (shell script, deterministic
configuration checks) and Tier 2 (four Claude Code smoke test sessions covering ingest,
contradiction, lint, and query workflows). On review, the cost of dedicated Tier 2
sessions was identified as equivalent to the cost of running real wiki operations, which
additionally produce residual value (actual wiki content). Three options were evaluated
for behavioral assurance: Option A (post-operation conformance summaries embedded in
CLAUDE.md workflows), Option B (human spot-check list after first ingest), Option C
(no dedicated verification layer; operations are their own tests). Option C was selected.

**Rationale:**
Tier 1 is worth its cost: it is deterministic, read-only, re-runnable at near-zero
overhead, and catches configuration drift that cannot be detected by running operations.
Tier 2 is not worth its cost: a smoke test session produces no wiki content, consumes
the same token budget as a real ingest, and does not catch failure modes that real
operations with real sources would catch. The existing FRIC escalation path (anomalies
surfaced as friction reports, logged, resolved in design sessions) already provides the
behavioral oversight function that Tier 2 was intended to serve. Adding a parallel
oversight layer duplicates that function at material cost.

**Alternatives Considered:**
- **Option A (conformance summaries per operation):** Marginal token cost, potentially
  useful signal. Not selected because it adds schema complexity and the FRIC path already
  covers the same ground.
- **Option B (spot-check list):** Zero token cost, adequate for first-run verification.
  Not selected as a standalone mechanism because it is one-time and not re-runnable.
- **Tier 2 as originally designed:** Token cost equivalent to real operations; no
  residual value. Ruled out.

**Consequences to Watch:**
- `wiki-verify.sh` must be updated when CLAUDE.md adds new required ignorePatterns
  entries, scaffold files, or required frontmatter fields. See test-harness.md Section
  2.5 (maintenance table) for the specific trigger conditions.
- If a behavioral failure mode emerges that `wiki-verify.sh` cannot detect and the FRIC
  path does not catch quickly enough, reconsider Option A (conformance summaries).

**References:** LL-020, LL-021, LL-022

---

## DM-072 | PROJECT INSTRUCTIONS AMENDED: PLAN-THEN-PAUSE, ACCESSIBLE-SOURCE CHECK, SELF-VIOLATION LOGGING REQUIREMENT

- **Date:** 2026-04-25
- **Status:** ACTIVE

**Decision:**
Three amendments to the project instructions governing this design session:

1. **Plan-then-pause requirement (Collaboration Contract).** The "plan first, act second"
   clause is amended to require an explicit stop after stating any plan, pending user
   confirmation. The prior text ("state the plan explicitly before writing code or
   drafting artifacts") was read as permission to plan-and-execute in a single response.
   The amended text adds: "After stating the plan, stop and wait for explicit user
   confirmation before executing. Do not treat absence of pushback as confirmation. Do
   not proceed on your own judgment that the plan is sound."

2. **Accessible-source check before declaring unavailability (Collaboration Contract).**
   A new bullet is added: "Before stating that information is unavailable or unknown,
   check all accessible sources: project knowledge files, web fetch of URLs documented
   in the project instructions, and any other tool appropriate to the query. Declaring
   information unavailable without first checking the sources that would contain it is
   a collaboration failure — this applies equally to project files, live URLs, and any
   other accessible resource."

3. **Self-violation logging requirement (End-of-Chat Ritual item 2).** The existing
   lessons-learned trigger is amended to explicitly cover violations of the project
   instructions themselves: "This includes violations of this document's own rules.
   Any session in which a rule from these project instructions was broken must produce
   a `lessons_learned.md` entry regardless of whether the violation was caught
   mid-session or in retrospect."

**Context:**
Three collaboration failures occurred in a single session: (1) a plan was stated and
immediately executed without user confirmation, repeating the root cause of LL-014
despite that entry existing in the log; (2) a governance document entry was delivered
inline instead of as a complete file; (3) the names of two Pitfalls pages were declared
unavailable without checking the live wiki URL present in the project instructions.
None of these failures were logged as lessons learned until the user raised them
explicitly, which is itself a violation of the end-of-chat ritual.

**Rationale:**
Amendment 1 makes the plan-then-pause requirement unambiguous. LL-014 identified the
same root cause; the prior fix ("after stating a plan, stop") was not encoded in the
project instructions, only in lessons_learned.md. Encoding it in the instructions closes
the gap. Amendment 2 addresses a pattern that appeared in two forms in the same session:
declaring a project file missing without checking project knowledge (a prior session
pattern), and declaring live-wiki information unavailable without checking the URL in
the instructions. Both are the same failure: incomplete search scope before declaring
unavailability. Amendment 3 addresses the failure to self-report. The ritual already
requires logging process errors, but prior sessions have shown that the agent does not
reliably apply this to its own rule violations. Making the self-violation case explicit
removes any ambiguity.

**Alternatives Considered:**
- **Rely on existing LL-014 and lessons_learned.md:** Did not prevent recurrence of the
  same root cause. Ruled out — the fix must be in the instructions, not only in the log.
- **Add a mandatory pre-execution pause prompt:** More explicit but adds mechanical
  overhead to every plan presentation. The language amendment is sufficient given that
  the failure was interpretation, not forgetfulness.

**Consequences to Watch:**
- Amendment 1 applies to every plan, including single-item decisions about artifact form.
  There is no threshold below which a plan can be executed without confirmation.
- If the accessible-source check (Amendment 2) adds friction to straightforward responses
  where information is obviously unavailable, the clause can be tightened with examples.

**References:** LL-014, LL-020, LL-021, LL-022

---

## DM-073 | ABOUT/ DIRECTORY ESTABLISHED FOR SCHEMA-EXEMPT PUBLIC PAGES

- **Date:** 2026-04-26
- **Status:** ACTIVE

**Decision:**
A dedicated `about/` directory is established for human-authored, schema-exempt pages
intended for public readers. Pages in `about/` are rendered by Quartz (not in
ignorePatterns) but are never created, modified, or linted by Claude Code. The directory
is documented in CLAUDE.md Section 2 with an explicit agent-exclusion note alongside
the existing `design/` note.

**Context:**
`how-this-wiki-works.md` was manually created at the wiki root to explain the wiki's
auto-generation concept to public readers. It does not conform to the wiki schema and
triggered a FAIL in wiki-verify.sh Group 7 (stray root file check).

**Rationale:**
Root placement fails the stray-root conformance check. Adding the file to the
`ALLOWED_ROOT` array is a point solution that does not scale to future schema-exempt
pages. Adding it to ignorePatterns prevents Quartz from rendering it, defeating its
purpose. A dedicated directory handles the category cleanly: Quartz-rendered but
agent-invisible, physically separated from schema-governed content directories.

**Alternatives Considered:**
- **Add to `ALLOWED_ROOT` in wiki-verify.sh:** Does not scale; each new schema-exempt
  file requires another script edit. Ruled out.
- **Add to ignorePatterns:** Prevents public rendering. Ruled out.

**Consequences to Watch:**
- CLAUDE.md Section 2 updated with directory entry and agent-exclusion note.
- wiki-verify.sh requires no update — the stray-root check (Group 7) only fires on
  files at the wiki root; files inside `about/` are not at root level. The naming
  convention check (Group 6) does not scan `about/`. No script changes needed for
  this directory to be invisible to conformance checks.
- If a future schema-exempt file is added to `about/`, no additional configuration
  is required.

---

## DM-074 | WIKI-VERIFY.SH SCRIPT FIXES: BASEURL CHECK AND NAMING SCAN SCOPE

- **Date:** 2026-04-26
- **Status:** ACTIVE

**Decision:**
Two targeted fixes applied to wiki-verify.sh. (1) The baseUrl check is narrowed from
a whole-file string match to lines containing `baseUrl` before checking for the
placeholder string, preventing false positives from commented-out examples elsewhere
in quartz.config.ts. (2) The naming convention scan loop is narrowed from
`topics tools sources comparisons pitfalls raw` to `topics tools sources comparisons
pitfalls`, removing `raw/` from scope to avoid false positives on gitignored archive
files in `raw/staged/` and `raw/processed/`.

**Context:**
First verification run produced two categories of false positive: (1) a baseUrl FAIL
despite the active setting being correctly configured (`fractalk.github.io/ai-auto-wiki`),
caused by a commented Quartz default still containing `quartz.jzhao.xyz` elsewhere in
the file; (2) five naming FAILs from archived source files in `raw/processed/` that
were never wiki pages and were never subject to naming conventions.

**Rationale:**
Both false positives were script design errors, not configuration errors. The
whole-file grep approach for baseUrl matches comments, not just the active setting.
The `raw/` directory contains gitignored archives whose filenames reflect original
source titles — they were never intended to conform to wiki naming conventions.
Files in `raw/` that require conformance checking (`queue.md`, `collection-gaps.md`,
`discovery-sources.md`) are already checked by name in Group 4.

**Consequences to Watch:**
- wiki-verify.sh header comment updated to accurately describe the narrowed scope
  of the baseUrl check.
- test-harness.md Section 2.3 check catalogue descriptions remain accurate;
  no table updates required.

---

## DM-075 | TIER 2 SMOKE TESTS ANNOTATED AS NOT ADOPTED IN TEST-HARNESS.MD

- **Date:** 2026-04-26
- **Status:** ACTIVE

**Decision:**
test-harness.md Section 1, Section 3, and Section 4 are updated to reflect that Tier 2
smoke tests were designed but not adopted (DM-071). The test content is preserved as
reference. Section 3 receives a prominent notice block. Section 1's Tier 2 description
gains a parenthetical. Section 4's "When to Run" table replaces Tier 2 "Run"
recommendations with "Not adopted (DM-071)."

**Context:**
test-harness.md presented Tier 2 as an active practice. A future operator — or a future
agent instance — reading Section 3 would have no way to know the tests were never run
and are not part of current practice. DM-071 dropped Tier 2 before adoption; this
decision had not been reflected in the document.

**Rationale:**
Deletion would lose the pass criteria and design rationale, which have reference value
for diagnosing FRIC entries. Annotation preserves the record while preventing a future
reader from acting on instructions that describe a procedure that will not be followed.

**Consequences to Watch:**
- If operational experience ever produces a class of behavioral failures not detectable
  by Tier 1 or FRIC entries, the Tier 2 pass criteria provide a ready-made starting
  point for a structured re-evaluation. The not-adopted notice would need to be revisited.

**References:** DM-071

---

## DM-076 | TEST-HARNESS.MD AND WIKI-VERIFY.SH ADDED TO PROJECT INSTRUCTIONS

- **Date:** 2026-04-26
- **Status:** ACTIVE

**Decision:**
Entries for test-harness.md and wiki-verify.sh added to the "Project Files — Consult
Before Proceeding" section of the project instructions. test-harness.md is the reference
for when schema changes require script updates (Section 2.5 maintenance table).
wiki-verify.sh is an execution artifact, not a design-session reference document.

**Context:**
Both files existed in the project without any guidance on when to consult them. The
project instructions govern session behavior for every project file; their omission
meant no defined trigger for consulting the maintenance table before delivering a
CLAUDE.md update that changes directory structure, frontmatter fields, or ignorePatterns.

**Consequences to Watch:**
- The Section 2.5 maintenance table in test-harness.md must be kept current as the
  schema evolves. Any CLAUDE.md change that touches directory structure, required
  frontmatter fields, scaffold files, allowed root files, or ignorePatterns should be
  cross-checked against Section 2.5 before delivery.

**References:** DM-073, DM-074

---

## DM-077 | INGEST STEP 11: IMAGE HANDLING FOR FULL-DEPTH SOURCES

- **Date:** 2026-04-26
- **Status:** ACTIVE

**Decision:**
For full-depth source types (`research-paper`, `white-paper`) that contain inline images:
during the Step 11 extraction pass, fetch and view any figure that is visually referenced
by the surrounding text and is not purely decorative. If the figure contains quantitative
data or structural information not captured in the surrounding prose (benchmark charts,
training curves, architecture diagrams), write a one-sentence description of the figure's
key content in the target wiki page body at the point where the source references it.
Do not store image files locally. Standard-depth sources are excluded from this step
entirely. CLAUDE.md Step 11 and EXTRACTION-SKILL.md Section 3 updated to reflect this.

**Context:**
Karpathy's gist describes downloading images locally so the LLM can reference them
during extraction. The rationale is that benchmark charts and architecture diagrams
frequently contain quantitative data not captured in the surrounding text — text-only
extraction loses this. The local-storage approach (Obsidian Web Clipper hotkey to
`raw/assets/`) has material maintenance costs: storage growth, copyright exposure for
stored third-party images, and no automated cleanup. `assets/` is also excluded from
Quartz rendering, making stored images unavailable in the public wiki.

**Rationale:**
The prose-description approach captures the same extraction value (LLM views the figure
and integrates its content) without storage overhead or copyright exposure. The one-sentence
figure description in the wiki page body survives link rot and is immediately useful to
readers. The Obsidian Web Clipper local-download path remains available for ad hoc human
use when a specific figure warrants preservation, using the existing `assets/` directory.

**Alternatives Considered:**
- **Status quo (drop all images):** Zero cost; loses quantitative data visible only in
  figures. Ruled out as a meaningful and fixable gap for full-depth sources.
- **Local storage via Web Clipper hotkey:** Preserves images for future reference but
  adds storage growth, periodic pruning, and copyright exposure. Not adopted as a
  workflow step; remains available for ad hoc human use.
- **URL fetch with no prose capture:** LLM views the image but writes nothing. Loses
  the extraction value after the session ends.

**Consequences to Watch:**
- "Purely decorative" is a judgment call. If the agent systematically over-fetches
  (logos, layout images), add a negative-example list to EXTRACTION-SKILL.md Section 3
  from operational experience.
- If HTML versions of arXiv papers render figures differently than PDF (e.g., figures
  not inline in HTML), revisit whether HTML-first fetching adequately exposes figures.

**References:** IN-003 (Karpathy gist), DM-008 (assets/ directory)

---

## DM-078 | URL FETCH FAILURE: NO FALLBACK RETRIEVAL; ENTRY MOVES TO [PROCESSED]

**Date:** 2026-04-27
**Status:** confirmed

**Decision:** When a queued URL fails to fetch (bot protection, network error, or any
other cause), the agent moves the entry from `## [queued]` to `## [processed]` in
`raw/queue.md` with a `fetch-failed: YYYY-MM-DD` annotation. No fallback retrieval is
attempted — no web search, no cached versions, no mirrors. All failures surface in the
post-ingest summary Notes field. If the content is still needed, the human obtains it
manually and places a file in `raw/staged/`.

**Rationale:** Prior behavior (FRIC-028): agent improvised web search fallbacks on fetch
failure, consuming significant tokens without authorization. The absence of a "stop here"
instruction was interpreted as permission to try alternatives. Explicit prohibition closes
the gap. Moving to `[processed]` (rather than a new `[fetch-failed]` section) avoids
changes to wiki-verify.sh or Section 2.1 scaffold.

**Consequences:** Fetch-failed entries are findable in `[processed]` via the
`fetch-failed:` annotation. Duplicate detection (Step 2) checks `sources/` by URL, not
`queue.md`, so a manually staged file from a previously fetch-failed URL will not
trigger a false positive.

---

## DM-079 | DOLLAR SIGNS MUST BE ESCAPED AS \$ IN ALL WIKI PAGE CONTENT

**Date:** 2026-04-27
**Status:** confirmed

**Decision:** All bare dollar signs in wiki page content — prose sections, Key Claims
table cells, and frontmatter string fields — must be written as `\$`. Rule added to
CLAUDE.md Section 6.2.

**Rationale:** Quartz uses remark/MDX which parses `$...$` as inline LaTeX math
delimiters. A bare `$20/month` in prose opened a math block; the next `$` closed it,
rendering everything between as compressed math notation. Obsidian does not implement
this behavior by default, masking the issue locally. Escaping is the correct fix;
removing LaTeX support from Quartz config would be a larger change with broader
implications not examined.

**Consequences:** All future wiki writes must use `\$` for currency. Existing pages
required a one-time retroactive fix (applied manually by human on 2026-04-27).

---

## DM-080 | PITFALLS STATUS/SOURCE LINES REQUIRE <br> FOR QUARTZ RENDERING

**Date:** 2026-04-27
**Status:** confirmed

**Decision:** The `**Status:**` line in Pitfalls failure mode entries must be followed
by `<br>` to force a line break in Quartz. Schema format updated in CLAUDE.md Section
5.6. All existing Pitfalls pages require a retroactive fix (deferred to next wiki
session, to be applied via a targeted bash/sed pass).

**Rationale:** Quartz uses CommonMark, which does not treat a single newline as a hard
line break. Without `<br>`, `**Status:**` and `**Source:**` collapse onto one line in
the published site. Obsidian defaults to treating single newlines as line breaks, masking
the issue locally. `<br>` is the minimal fix; blank lines between the two fields would
introduce unwanted paragraph spacing.

**Consequences:** All future Pitfalls page writes use the updated format. Existing pages
need retroactive `<br>` insertion — approach is a Claude Code bash/sed pass across
`pitfalls/` at next wiki session start.

---

## DM-081 | DERIVED-PAGE RIPPLE RULE: THRESHOLD-BASED, NOT AUTO-REWRITE PROHIBITION

- **Date:** 2026-04-27
- **Status:** ACTIVE

**Decision:**
The auto-rewrite prohibition for derived pages (Comparison pages and teaching-brief pages) is replaced with a threshold-based rule. Below the Step 12/13 substantiality threshold, the agent auto-applies updates and logs the action in the commit message. At or above the threshold, the agent surfaces a forced choice with an agent-generated draft. The same threshold governs teaching_notes sync and derived-page ripple checks.

**Context:**
Prior design left the ripple behavior for derived pages undefined. An absolute prohibition on auto-rewrite would prevent any automated maintenance. The threshold-based approach preserves human oversight where it matters (substantive content changes) without creating friction for minor updates.

**Rationale:**
Threshold-based rules are consistent with the existing Path A/B/C contradiction protocol design philosophy: automate the unambiguous cases, surface the judgment calls. The substantiality threshold (Key Claim superseded/contested, or new fundamentally different claim added) is operationally verifiable.

**Alternatives Considered:**
- **Auto-rewrite prohibition (always surface):** Ruled out — creates forced choice noise for corroborating updates that do not change the synthesis.
- **Always auto-apply (no threshold):** Ruled out — derived pages contain curated synthesis; silent overwrites of significant content changes undermine the value of human-reviewed notes.

**Consequences to Watch:**
If agents systematically misclassify substantive changes as below-threshold, teaching notes and Comparison pages will silently drift from their constituent pages. Monitor teaching_notes_reviewed vs. last_assessed gaps during lint.

**References:** LL-026

---

## DM-082 | TEACHING NOTES: STRUCTURED ANNOTATION ON TEACHING-TAGGED PAGES

- **Date:** 2026-04-28
- **Status:** ACTIVE

**Decision:**
Add a conditional `## Teaching Notes` body section to all pages with `teaching_relevance: true`. Two variants: Topic/Tool variant (concept in plain terms, why it matters, common misconceptions, suggested framing; ~150–200 words) and Pitfalls variant (what this failure mode teaches, representative example; ~150–200 words). A new `teaching_notes_reviewed` frontmatter field tracks currency. Sync mechanism: ingest-time substantiality check in Steps 12a, 13b, 13a. Lint backstop: flag pages where `teaching_notes_reviewed` is >90 days older than `last_assessed`.

**Context:**
The Teaching Index currently surfaces page summaries only. Instructors preparing to teach need richer pedagogical framing — accessible explanations, common misconceptions, and classroom-ready examples — without having to re-derive them from Key Claims on each use.

**Rationale:**
Embedding structured notes directly in each page keeps the pedagogical context co-located with the content it annotates. The instructor summary query mode can then synthesize from these notes rather than from raw Key Claims, producing significantly better instructor-facing output. The ingest-time substantiality check prevents stale notes from accumulating silently.

**Alternatives Considered:**
- **Separate teaching notes file per page:** Ruled out — adds file management overhead and breaks co-location.
- **Freeform prose in summary field:** Ruled out — summary field is a single sentence used for index entries and search snippets; it cannot carry pedagogical depth.
- **Teaching Index only (no page-level notes):** Ruled out — the Teaching Index is a derived aggregation artifact; it cannot carry page-specific pedagogical context without duplicating it from somewhere.

**Consequences to Watch:**
Pages ingested before this schema change have no `teaching_notes` section. The lint Step L5b backstop will surface these as "teaching notes missing" — an expected accumulating signal as existing teaching-tagged pages are touched by future ingests. Retroactive population is at operator discretion.

**References:** DM-081

---

## DM-083 | QUERY FILE-BACK PATH: THREE CASES + TEACHING-BRIEF PAGE TYPE + INSTRUCTOR SUMMARY MODE

- **Date:** 2026-04-28
- **Status:** ACTIVE

**Decision:**
Add a structured file-back procedure to OPERATIONS.md Section 11.5 covering three cases: (1) new cross-topic synthesis files as a Comparison page with `provenance: query-generated` and `query_date` fields; (2) refinement of an existing page is handled as a normal targeted ingest update with provenance noted in the commit message only; (3) instructor summary outputs file as a new `teaching-brief` page type in `teaching/`. Add a named instructor summary query mode that synthesizes from `teaching_notes` fields first, Key Claims second. Query outputs are not sources — they do not enter the ingest source classification taxonomy. Teaching-brief pages use full-path wikilinks in `derived_from` (same convention as `entities_compared` and `parent_entity`) for lint type enforcement. Teaching-brief pages are excluded from the Teaching Index (they are outputs, not source entries).

**Context:**
Query results previously disappeared into session history. Cross-topic synthesis valuable enough to persist had no structured filing path. The Teaching Index was useful for finding teaching-relevant content but produced no instructor-facing output format.

**Rationale:**
Three-case structure reflects the three meaningfully different filing contexts a query result can produce. Case 2 avoids creating a new page when the insight belongs on an existing one — the most common outcome for refinement queries. Case 3 creates a lightweight, human-reviewed format suitable for direct instructor use. Full-path wikilinks in `derived_from` are consistent with all other structural frontmatter fields used for lint enforcement; short-form is reserved for convenience navigation fields.

**Alternatives Considered:**
- **Single filing path (always Comparison page):** Ruled out — most synthesis queries produce refinements, not stand-alone comparisons.
- **Short-form wikilinks in derived_from:** Ruled out — without full-path, lint cannot reliably determine the referenced page's type for directory consistency checks.
- **Teaching-brief pages included in Teaching Index:** Ruled out — creates circular self-reference; the Teaching Index is a source index, not an output index.

**Consequences to Watch:**
The `teaching/` directory is new. The pre-commit hook, wiki-verify.sh, and INIT-PROMPT.md all needed updates in the same batch to prevent a window where the hook does not cover the new directory. Atomic delivery of these changes is required — do not apply CLAUDE.md changes to a live wiki without also updating wiki-verify.sh and regenerating the pre-commit hook.

**References:** DM-082

---

## DM-084 | LINT CADENCE GUIDELINE: 15–20 PAGES OR TWO WEEKS, MANDATORY TRIGGERS

- **Date:** 2026-04-28
- **Status:** ACTIVE

**Decision:**
Replace the informal "recommended: weekly" lint cadence with a concrete guideline: run lint every 15–20 new pages added, or every two weeks of operation, whichever comes first. Mandatory triggers (not overridable): before any schema change applied to the live wiki; after any bulk ingest session of five or more sources. Add a pre-session habit: run `wiki-verify.sh` before every ingest or lint session.

**Context:**
First lint pass (Pass 1) ran after 63 pages — significantly later than optimal. A concrete cadence guideline prevents unbounded drift. The 7-day Path B contradiction override window creates a natural pressure to run lint at least weekly during active ingest periods, but this was not encoded in the schema.

**Rationale:**
15–20 pages is calibrated to the current ingest velocity (~8–10 pages per session). At that rate, lint runs approximately every 2–3 sessions — often enough to catch staleness and schema drift before it compounds, not so often that it becomes operational overhead. The two-week ceiling prevents indefinite deferral during low-ingest periods. Mandatory triggers address the two highest-risk moments: schema changes (where pre-change lint confirms baseline state) and bulk ingests (where post-ingest lint validates structural integrity).

**Alternatives Considered:**
- **Weekly mandatory schedule:** Ruled out — too prescriptive for variable ingest cadences; would create forced lint passes on days with no new content.
- **No cadence guideline (on-demand only):** Ruled out — operationally demonstrated to produce unbounded drift (63-page gap before first pass).

**Consequences to Watch:**
The `wiki-verify.sh` pre-session habit is documented in OPERATIONS.md and implementation-handoff.md Section 5 customization notes but is not enforced by the schema. If operators consistently skip it, structural drift will accumulate silently. Monitor FRIC log for structural issues that a pre-session verify would have caught.

---

## DM-085 | OPERATIONS.MD SPLIT EXECUTED: SECTION 11 EXTRACTED FROM CLAUDE.MD

- **Date:** 2026-04-28
- **Status:** ACTIVE

**Decision:**
Executed the OPERATIONS.md split per DM-061. All of CLAUDE.md Section 11 (11.1 source classification taxonomy, 11.2 ingest workflow, 11.3 discovery pass, 11.4 lint procedure, 11.5 query workflow) moved verbatim to a new peer file `OPERATIONS.md` at the wiki root. A hard gate instruction added to CLAUDE.md Section 1: if OPERATIONS.md is not present in context, output `MISSING-OPERATIONS-FILE` and halt. CLAUDE.md post-split: ~1,590 lines. OPERATIONS.md: ~1,497 lines. Combined: ~3,087 lines — above the 3,000-line trigger in DM-061.

**Context:**
DM-061 set the 3,000-line trigger. This session's three confirmed additions (teaching notes, file-back path, lint cadence) plus the OPERATIONS.md split content itself pushed the projected combined total above 3,000. The split was executed in the same session as the schema additions, incorporating all new operational content directly into OPERATIONS.md.

**Rationale:**
Splitting at the natural Section 11 boundary is clean — all schema definitions (types, frontmatter, vocabularies, contradiction protocol, version handling) stay in CLAUDE.md; all operational procedures stay in OPERATIONS.md. The hard gate prevents silent partial-load failures. Both files must be in the session-start prompt template.

**Execution obligations completed per DM-061:**
1. Section 11 moved verbatim to OPERATIONS.md — done
2. Hard gate added to CLAUDE.md Section 1 — done
3. CLAUDE.md Section 1 references OPERATIONS.md explicitly — done
4. Session-start prompt template updated (implementation-handoff.md Section 5) — done
5. INIT-PROMPT.md updated: OPERATIONS.md in prerequisite check, directory creation, scaffold verification, Step 12 summary — done
6. EXTRACTION-SKILL.md, TAGGING-SKILL.md, CONTRADICTION-SKILL.md: no Section 11.x cross-references found — no update required
7. portability-review.md: all Section 11.x references updated to OPERATIONS.md Section 11.x — done
8. DM entry recorded — this entry

**Note for live wiki:** OPERATIONS.md must be created in the wiki root as a schema-change operation. The agent should log a `schema-change` log entry when OPERATIONS.md is added to the live wiki. The session-start prompt stubs in `prompts/` must also be regenerated from the updated template in implementation-handoff.md Section 5 — the old stubs reference only CLAUDE.md and must be replaced.

**Consequences to Watch:**
Schema-to-operations cross-references (Section 5 frontmatter fields, Section 7 controlled vocabularies, Section 8 contradiction logic) now cross a file boundary. Any change to a referenced section in CLAUDE.md requires auditing OPERATIONS.md for consistency. This is manageable with the existing cross-reference check discipline but is a new ongoing obligation.

**References:** DM-061

## DM-086 | INGEST OPERATION MODE SEPARATION: INGEST-STAGED / INGEST-QUEUE / INGEST-BOTH

- **Date:** 2026-04-29
- **Status:** ACTIVE

**Decision:**
Replace the single INGEST operation with three named modes: `INGEST-STAGED` (staged
files only), `INGEST-QUEUE` (queued URLs only), and `INGEST-BOTH` (both locations,
explicit opt-in). OPERATIONS.md Step 0 branches on the declared mode before counting
sources. Step 1 routes based on the same mode. The agent halts and requests
clarification if the mode is absent or ambiguous.

**Context:**
OPERATIONS.md Step 0 previously counted staged files + queued URLs together and Step 1
processed both in every batch ingest. This was designed-in behavior — operator prompt
phrasing instructing "staged only" was overridden by the spec. The result: sessions
inadvertently combined both locations, inflating source counts and consuming more
session budget than expected, with no trimming opportunity before extraction began.

**Rationale:**
Explicit modes eliminate the combining behavior at zero runtime cost — no added round
trips, no pre-flight manifest step. The operator declares intent at prompt time via the
stub file. INGEST-BOTH preserves the prior combined behavior for cases where it is
genuinely wanted. For density control, INGEST-STAGED is the right default for research
papers and long PDFs — the operator controls `raw/staged/` contents before starting the
session.

**Alternatives Considered:**
- **Pre-ingest source manifest pause (Fix 2):** Add a step where the agent lists all
  candidate sources before extracting, letting the operator trim. Ruled out — the
  per-session round-trip cost amortizes poorly for a disciplined operator who already
  controls the staged directory. Fix 1 solves the stated problem without runtime
  overhead.
- **Effort-adjusted source cap (Fix 3):** Count full-extraction sources as 2 toward
  the N ≤ 5 threshold. Ruled out as redundant given Fix 1 — INGEST-STAGED gives direct
  density control without requiring source-type classification at Step 0.

**Consequences to Watch:**
The `prompts/ingest.md` stub is replaced by three stubs (`ingest-staged.md`,
`ingest-queue.md`, `ingest-both.md`). Any wiki repo with a pre-existing `prompts/ingest.md`
must have it deleted and the three new stubs added. The step-6-7 Claude Code prompt
must be updated to regenerate the correct set of seven stubs.

**References:** LL-029

---

## DM-087 | COMPARISON PAGE BODY TEMPLATE: FOUR-PART STRUCTURE WITH CONSTRAINED VERDICT

- **Date:** 2026-04-29
- **Status:** ACTIVE

**Decision:**
Comparison pages use a four-part body structure: (1) opening sentence — required, no
heading, one sentence derived from `use_case`, written as prose (not a verbatim restate);
(2) comparison table — required, no heading; (3) `## Verdict` — required, constrained
format: "Prefer [[X]] when [condition]." one sentence per compared entity, conditions
must be specific and falsifiable against the comparison table, no hedging language; for
five or more entities, group into tiers; (4) `## Evidence Notes` — optional, labeled
attributes separated by `<br>`, omitted entirely when nothing meaningful to add, no
placeholder heading. Verdict updates follow the DM-081 threshold rule: auto-apply below
threshold; surface as forced choice in post-ingest summary Section B when a Key Claim
changes which conditions apply.

**Context:**
CLAUDE.md Section 5.5 specified the frontmatter schema for Comparison pages but left the
body structure entirely unspecified. Agents improvised — producing inconsistent heading
hierarchies, unconstrained prose verdicts, and inline evidence blocks that collapsed to
single lines on Quartz (the CommonMark single-newline rendering problem documented in
FRIC-030). Three existing comparison pages require retroactive restructuring.

**Rationale:**
The Verdict section is always producible from the comparison table and Key Claims — it
requires no information not already on the page, so there is no empty-section risk for
that heading. Constraining its format to "Prefer [[X]] when [condition]" limits judgment
drift: conditions must be falsifiable, hedging language is prohibited, and the format
degrades gracefully to tier groupings for large entity counts. Evidence Notes are optional
so the agent omits the heading entirely when nothing meaningful is available — the
empty-heading pollution problem that motivated option B's rejection. The `<br>` separator
mirrors the FRIC-030 fix for Pitfalls pages: same Quartz/CommonMark rendering constraint,
same solution.

**Alternatives Considered:**
- **Option A — Status quo (no body spec):** Ruled out — demonstrated to produce
  structural inconsistency across existing comparison pages.
- **Option B — Comparison table only, no Verdict or Evidence Notes:** Ruled out —
  comparison without a recommendation is incomplete for the wiki's decision-support use
  case; the table alone answers "how do they differ" but not "which to choose."
- **Option C — Unconstrained Verdict prose:** Ruled out — without format constraints,
  agents produce hedged, non-falsifiable prose ("generally better when...") that cannot
  be meaningfully updated on re-ingest.
- **Option D — Constrained Verdict, Evidence Notes optional (chosen):** Provides
  necessary structure without over-specifying; omit-when-empty rule prevents placeholder
  pollution; `<br>` separator is a proven Quartz fix.
- **Option E — Forced-choice Verdict on every write:** Ruled out — Verdict is fully
  derivable from Key Claims; requiring human confirmation on every comparison page write
  adds overhead without value. DM-081 threshold logic already governs when a forced
  choice is warranted.

**Consequences to Watch:**
Verdict updates must respect the DM-081 threshold rule: when a Key Claim changes which
conditions apply, the update is a forced choice, not auto-apply. Evidence Notes can go
stale when a new source with substantially different methodology is ingested without
triggering a comparison staleness flag; the lint staleness check (Comparison page
`updated` vs. `entities_compared` page `updated`) is the backstop, but methodological
shifts may not surface as Key Claim changes — they may appear only in a new Source
page's body. No lint rule currently detects this; defer until operationally observed.

**References:** DM-081, FRIC-030, FRIC-032
