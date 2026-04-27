# implementation-friction.md
Last Updated: 2026-04-22

Persistent log of implementation friction issues encountered during setup and
operational shake-out. Created once; never deleted. Issues accumulate with open/closed
status. At session start, the agent reads this file and surfaces any open issues before
taking new reports. At end-of-chat batch write, applied fixes are marked closed.

Do not edit entries manually after they are written. The session agent maintains status
fields.

---

## Entry Template

```
## FRIC-NNN | [SHORT DESCRIPTIVE TITLE]

- **Date:** YYYY-MM-DD
- **Status:** open | closed
- **Phase:** Phase 0 | Phase 1 | Phase 2 | Phase 3 | Post-setup
- **Document implicated:** [filename, section]
- **Symptom:** [What the human encountered. One to three sentences.]
- **Verdict:** Confirmed weakness — [specific gap or error in the document]
- **Fix plan:** [What changes, where, and why. One to two sentences.]
- **Resolved:** YYYY-MM-DD | — [Date closed, or dash if still open]
```

---

## Issues

## FRIC-001 | Node/npm Version Spec Incorrect

- **Date:** 2026-04-22
- **Status:** closed
- **Phase:** Phase 0
- **Document implicated:** implementation-handoff.md Phase 0 Step 2; INIT-PROMPT.md Step 4
- **Symptom:** The documents required "Node.js 18 or later" and applied the same "18 or later" threshold to npm. npm v18 does not exist; current npm is v10.x–v11.x. Quartz's actual stated minimum is Node v22 and npm v10.9.2.
- **Verdict:** Confirmed weakness — incorrect version thresholds for both Node.js and npm; npm threshold is categorically wrong.
- **Fix plan:** Update both documents to state Node v22 or later and npm v10.9.2 or later, matching Quartz's published minimum.
- **Resolved:** 2026-04-22

---

## FRIC-002 | Quartz Install Method Wrong; Build Directory Gap

- **Date:** 2026-04-22
- **Status:** closed
- **Phase:** Phase 0
- **Document implicated:** implementation-handoff.md Phase 0 Step 3; INIT-PROMPT.md Steps 5 and 10
- **Symptom:** The instruction "from your intended wiki root directory, run `npx quartz create`" produced a nested directory structure with Quartz installed as a subdirectory rather than at the wiki root. Additionally, the GitHub Actions workflow used `npx quartz build` with no directory flag, which defaults to reading from `content/` — meaning all wiki pages at the repo root would be silently ignored during deployment.
- **Verdict:** Confirmed weakness — two distinct gaps: (1) `npx quartz create` is not a standalone bootstrapper; correct setup requires cloning the Quartz repository into the wiki root. (2) `npx quartz build` without `-d .` reads only from `content/`, silently producing an empty or near-empty published site.
- **Fix plan:** Rewrite Phase 0 Step 3 and INIT-PROMPT.md Step 5 to specify the correct clone-based setup. Add `-d .` to `npx quartz build` in the workflow template (Step 10) and add `docs/**` and `content/**` to `ignorePatterns` in Step 9 to suppress Quartz's own documentation and stub content directory from the published site.
- **Resolved:** 2026-04-22

---

## FRIC-003 | No nvm Install Guidance

- **Date:** 2026-04-22
- **Status:** closed
- **Phase:** Phase 0
- **Document implicated:** implementation-handoff.md Phase 0 Step 2; INIT-PROMPT.md Step 4
- **Symptom:** The only install guidance was "download from https://nodejs.org/en/download" — adequate for a developer audience but insufficient for an implementer with limited terminal experience. The nodejs.org installer can cause PATH and permissions problems on macOS and provides no version-switching path.
- **Verdict:** Confirmed weakness — usability gap; nvm is the standard and safer Node install method on macOS/Linux and should be the recommended path.
- **Fix plan:** Add a paragraph to Phase 0 Step 2 recommending nvm with install commands. Retain nodejs.org as the fallback for Windows. Mirror the guidance in INIT-PROMPT.md Step 4 error messages.
- **Resolved:** 2026-04-22

---

## FRIC-004 | Quartz Link Resolution Prompt Not Addressed

- **Date:** 2026-04-22
- **Status:** closed
- **Phase:** Phase 0
- **Document implicated:** implementation-handoff.md Phase 0 Step 3; INIT-PROMPT.md Step 5
- **Symptom:** `npx quartz create` prompts for a link resolution strategy (Shortest Path, Absolute, or Relative). The handoff gave no guidance on this choice, leaving the implementer to guess.
- **Verdict:** Confirmed weakness — implementer is forced to guess at a configuration choice with schema implications; Shortest Path is the correct answer and should be stated explicitly.
- **Fix plan:** Add a line to Phase 0 Step 3 and INIT-PROMPT.md Step 5 specifying "choose Shortest Path (the default)" with a one-sentence rationale (matches Obsidian wikilink behavior; safe given the wiki's flat-ish naming conventions).
- **Resolved:** 2026-04-22

---

## FRIC-005 | Claude Code Not Listed as a Phase 0 Prerequisite

- **Date:** 2026-04-22
- **Status:** closed
- **Phase:** Phase 0
- **Document implicated:** implementation-handoff.md Phase 0
- **Symptom:** Running `claude` in the terminal produced "command not found." Claude Code is not bundled with Node or npm and requires a separate install step. The handoff listed no step for installing it.
- **Verdict:** Confirmed weakness — missing prerequisite step; Claude Code installation must appear in Phase 0 before the readiness checklist.
- **Fix plan:** Add a Claude Code installation step to Phase 0 (after the Node/npm step, since npm is required) with the install command `npm install -g @anthropic-ai/claude-code` and a verify step. Add a corresponding item to the readiness checklist.
- **Resolved:** 2026-04-22

---

## FRIC-006 | "Unhandled Node Type: string" Warning Undocumented

- **Date:** 2026-04-22
- **Status:** closed
- **Phase:** Phase 1
- **Document implicated:** implementation-handoff.md Phase 1
- **Symptom:** Claude Code emitted "Unhandled node type: string" alongside bash tool output during Step 3. The implementer could not distinguish a cosmetic rendering warning from a genuine script failure.
- **Verdict:** Confirmed weakness — usability gap; the warning is cosmetic (Claude Code's display layer encountered a plain string it could not annotate) and does not indicate a script failure, but nothing in the documentation prepares the implementer for it.
- **Fix plan:** Add a one-paragraph callout to Phase 1 noting that Claude Code occasionally emits "Unhandled node type" rendering warnings alongside bash output; these are cosmetic and do not indicate script failure — if the bash command produced expected output, proceed.
- **Resolved:** 2026-04-22

---

## FRIC-007 | Obsidian Indexes node_modules and Quartz Source Files

- **Date:** 2026-04-22
- **Status:** closed
- **Phase:** Phase 2
- **Document implicated:** implementation-handoff.md Phase 2 Step 4
- **Symptom:** Opening the wiki root as an Obsidian vault produced a graph view with thousands of nodes — Obsidian had indexed node_modules, docs/, and Quartz source files. The vault was unusable for verification.
- **Verdict:** Confirmed weakness — the document instructed the implementer to verify the graph view without providing the exclusion configuration required to make it meaningful. node_modules will always be present in a Quartz-rooted wiki repo.
- **Fix plan:** Add an Obsidian exclusion configuration step to Phase 2 Step 4, before the graph view verification instruction, listing the exact paths to exclude: node_modules, docs, quartz, .github.
- **Resolved:** 2026-04-22

---

## FRIC-008 | GitHub Actions Workflow Uses Deprecated Node.js 20 Runtime

- **Date:** 2026-04-22
- **Status:** closed
- **Phase:** Phase 2
- **Document implicated:** INIT-PROMPT.md Step 10
- **Symptom:** The deployed workflow produced a GitHub Actions warning that actions/checkout@v4, actions/setup-node@v4, and actions/upload-pages-artifact@v3 run on Node.js 20, which will be forced to Node.js 24 on June 2, 2026 and removed September 16, 2026.
- **Verdict:** Confirmed weakness — the generated workflow will break before the wiki reaches meaningful size; the fix is to opt into Node.js 24 now via the FORCE_JAVASCRIPT_ACTIONS_TO_NODE24 environment variable, as recommended by GitHub.
- **Fix plan:** Add `env: FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true` at the top-level workflow scope in the deploy.yml template in INIT-PROMPT.md Step 10.
- **Resolved:** 2026-04-22

---

## FRIC-009 | Web Fetch Truncation Not Documented

- **Date:** 2026-04-22
- **Status:** closed
- **Phase:** Phase 3
- **Document implicated:** implementation-handoff.md Phase 3; implementation-handoff.md Section 5 customization notes
- **Symptom:** Several articles failed ingest during the first wiki session because web fetch truncated long pages. The implementer had no advance warning and no documented recovery path.
- **Verdict:** Confirmed weakness — web fetch has a token limit that will be hit on long articles; the fallback path (pre-clip to raw/staged/ using a browser extension) is correct per the schema but is not mentioned in Phase 3 or the session-start prompt customization notes.
- **Fix plan:** Add a note to Phase 3 that web fetch has a token limit and long articles should be pre-clipped to raw/staged/ before the session. Add a corresponding note to Section 5 customization notes.
- **Resolved:** 2026-04-22

---

## FRIC-010 | quartz.config.ts baseUrl Never Set During Initialization

- **Date:** 2026-04-22
- **Status:** closed
- **Phase:** Phase 2
- **Document implicated:** INIT-PROMPT.md Step 9; implementation-handoff.md Phase 2 Step 3
- **Symptom:** After a successful build and deploy, visiting the published GitHub Pages URL returned an RSS XML page instead of the Quartz wiki interface. The RSS `<link>` field showed `https://quartz.jzhao.xyz` — the Quartz default baseUrl, which was never changed during initialization.
- **Verdict:** Confirmed weakness — INIT-PROMPT.md Step 9 makes two targeted changes to quartz.config.ts (ignorePatterns and Plugin.Mermaid()) but never sets baseUrl. A first-time implementer has no reason to know this field exists, let alone that it defaults to the Quartz demo domain. A successful GitHub Actions build does not surface this error; the site deploys but renders only RSS.
- **Fix plan:** Add Change 3 to INIT-PROMPT.md Step 9 patching baseUrl to a placeholder (`"<your-github-username>.github.io/<your-repo-name>"`) with an explicit note that the human must replace the placeholder before committing. Add an HTML render verification step to implementation-handoff.md Phase 2 Step 3 so the implementer confirms the site serves HTML, not RSS, after the first successful build.
- **Resolved:** 2026-04-22

---

## FRIC-011 | FRIC Template Fix Did Not Propagate to Already-Generated deploy.yml

- **Date:** 2026-04-22
- **Status:** closed
- **Phase:** Phase 2
- **Document implicated:** implementation-handoff.md (FRIC resolution process)
- **Symptom:** FRIC-002 fixed the INIT-PROMPT.md Step 10 deploy.yml template to include `npx quartz build -d .`. However, the implementer's deploy.yml had already been generated from the pre-fix template. The FRIC-002 resolution did not include an instruction to the implementer to manually apply the `-d .` patch to their existing deploy.yml. The implementer continued using the broken file until the symptom (zero pages built) was diagnosed in this session.
- **Verdict:** Confirmed weakness — when a FRIC fix updates a template that generates a one-time configuration file (deploy.yml is written once during initialization, not regenerated), the resolution must include an explicit instruction to the implementer to manually apply the patch to the already-generated file. The FRIC-002 resolution omitted this.
- **Fix plan:** No doc change required — FRIC-002's template fix is correct and complete for future setups. Log as LL-012 to capture the process implication: when closing a FRIC that fixes a template generating a one-time file, always include an explicit "if you have already generated this file, apply the following patch manually" instruction in the resolution note.
- **Resolved:** 2026-04-22

---

## FRIC-012 | `node_modules` and `INIT-PROMPT.md` Published to Public Quartz Site

- **Date:** 2026-04-22
- **Status:** closed
- **Phase:** Post-setup
- **Document implicated:** INIT-PROMPT.md Step 9 Change 1; portability-review.md QTZ-01; CLAUDE.md Section 2 [ENV]
- **Symptom:** `node_modules` directory contents and `INIT-PROMPT.md` were visible on the public Quartz site. Both are present at the repo root; neither was in the ignorePatterns list installed by Step 9.
- **Verdict:** Confirmed weakness — `node_modules/**` and `"INIT-PROMPT.md"` were omitted from the ignorePatterns enumeration in INIT-PROMPT.md Step 9 and the corresponding pre-flight action in portability-review.md QTZ-01.
- **Fix plan:** Added `"node_modules/**"` and `"INIT-PROMPT.md"` to the ignorePatterns array in INIT-PROMPT.md Step 9 Change 1, portability-review.md QTZ-01, and CLAUDE.md Section 2 [ENV].
- **Resolved:** 2026-04-22

---

## FRIC-013 | Incorrect Diagnosis: public/ Believed Committed to Git

- **Date:** 2026-04-22
- **Status:** closed
- **Phase:** Post-setup
- **Document implicated:** None (diagnosis error; no doc change made)
- **Symptom:** CI build failed with `EEXIST: file already exists, mkdir 'public/public/tags'`. Initial diagnosis was that `public/` had been committed to git, and the fix `git rm -r --cached public/` was issued.
- **Verdict:** Diagnosis was wrong — `public/` was not committed. The `git rm` command returned "pathspec did not match any files." The actual root cause was FRIC-014. No document change was made based on this incorrect diagnosis.
- **Fix plan:** No doc change. Logged to record the diagnostic error. See FRIC-014 for the correct root cause and fix.
- **Resolved:** 2026-04-22

---

## FRIC-014 | Assets Emitter Processes Live Output Directory, Causing EEXIST

- **Date:** 2026-04-22
- **Status:** closed
- **Phase:** Post-setup
- **Document implicated:** INIT-PROMPT.md Step 9 Change 1; portability-review.md QTZ-01; CLAUDE.md Section 2 [ENV]
- **Symptom:** CI build failed with `EEXIST: file already exists, mkdir 'public/public/tags'`. The Quartz Assets emitter scans the source directory at emit time (not from the pre-parsed file list) and found `public/` — the output directory being populated by a concurrently running Tags emitter. It attempted to copy `public/` into `public/public/`, colliding with the already-created `public/tags/`.
- **Verdict:** Confirmed weakness — `public/**` was absent from ignorePatterns. The output directory must be excluded to prevent the Assets emitter from treating it as source material on subsequent or concurrent builds.
- **Fix plan:** Added `"public/**"` to the ignorePatterns array in INIT-PROMPT.md Step 9 Change 1, portability-review.md QTZ-01, and CLAUDE.md Section 2 [ENV].
- **Resolved:** 2026-04-22

---

## FRIC-015 | Singleton Scaffold Files overview.md and log.md Publishing to Public Site

- **Date:** 2026-04-22
- **Status:** closed
- **Phase:** Post-setup
- **Document implicated:** INIT-PROMPT.md Step 9 Change 1; portability-review.md QTZ-01; CLAUDE.md Section 2 [ENV]
- **Symptom:** `overview.md` and `log.md` appeared in the Quartz navigation bar. `overview.md` rendered as a blank page (frontmatter only, no body). Both are machine-maintained state files, not public content.
- **Verdict:** Confirmed weakness — the ignorePatterns design excluded operational infrastructure files (skill files, raw/, assets/) but did not address the singleton scaffold state files. Initial fix recommendation also incorrectly included `"index.md"`, which was retracted: Quartz requires index.md at the repo root to generate index.html; excluding it causes the site to serve index.xml (RSS) instead.
- **Fix plan:** Added `"overview.md"` and `"log.md"` to ignorePatterns in INIT-PROMPT.md Step 9 Change 1, portability-review.md QTZ-01, and CLAUDE.md Section 2 [ENV]. Added an explicit warning to all three locations that index.md must NOT be added.
- **Resolved:** 2026-04-22

---

## FRIC-016 | Phase 2 Obsidian Verification Step Implies overview.md Has Visible Content

- **Date:** 2026-04-22
- **Status:** closed
- **Phase:** Phase 2
- **Document implicated:** implementation-handoff.md Phase 2 Step 4
- **Symptom:** The Phase 2 Obsidian verification checklist contained "`overview.md` opens and renders correctly in reading view." Since overview.md has frontmatter only and no body, it renders as a blank page in Obsidian reading view. An implementer following the step sees a blank page and has no basis to determine whether this is correct or a failure.
- **Verdict:** Confirmed weakness — "renders correctly" implies visible content; the instruction should explicitly state the page is blank and that this is expected.
- **Fix plan:** Updated the checklist item to: "`overview.md` opens in reading view without error (the page body is blank — overview.md contains only YAML frontmatter, which Obsidian hides in reading view; this is expected)."
- **Resolved:** 2026-04-22

---

## FRIC-017

- **symptom:** Pre-flight budget forced choice check counts only `[queued]` items against the ≤5 threshold. Staged files (those ingested via the staged path rather than the queue URL path) are not counted. In practice, staged files are increasingly common because long sources fail on the queue path due to context limits — meaning staged sources tend to be longer in content, not shorter. The result: the budget check can approve a session with 2 queued items but 4 staged files (6 total, all potentially long) without triggering a forced choice.
- **implicated document:** CLAUDE.md — pre-flight check (Step 0) in the ingest workflow; budget forced choice logic; queue.md structure
- **verdict:** Confirmed weakness — Step 0 counted only `[queued]` items; staged files
  were excluded despite constituting real session work and tending to be the heaviest
  sources.
- **fix plan:** Step 0 now counts N = staged files (via `ls raw/staged/`) + queued
  items. Threshold unchanged at 5. Forced choice block template updated to show the
  breakdown (`{a} staged files + {b} queued URLs`). Deferral note template updated
  to record the breakdown at time of deferral.
- **status:** closed
- **reported:** 2026-04-22
- **resolved:** 2026-04-22

---

## FRIC-018 | Post-Ingest Summary Mixes Forced Choices and Informational Content

- **Date:** 2026-04-22
- **Status:** closed
- **Phase:** Post-setup
- **Document implicated:** CLAUDE.md — Step 21a (skill enrichment nomination format);
  Step 22 (post-ingest summary template)
- **Symptom:** The post-ingest summary output was an undifferentiated block mixing
  informational lines (pages created, tagging coverage, Teaching Index status) with
  forced choices (citation nominations, skill enrichment proposals). No consistent
  numbering scheme existed for post-ingest forced choices, requiring verbose responses
  to establish which answer mapped to which question.
- **Verdict:** Confirmed weakness — Step 22 template interleaved forced choices with
  informational output; no `PS-N` numbering or response format instruction existed for
  post-ingest decisions.
- **Fix plan:** Restructured Step 22 into Section A (informational) and Section B
  (forced choices, PS-N labeled, omitted when empty). Updated Step 21a to hold skill
  enrichment drafts until Step 22 assembly rather than outputting them mid-summary.
  Added response format instruction (`Respond with: PS-1:X PS-2:X ...`) opening
  Section B. PS-N namespace is distinct from pre-flight `N:X` namespace.
- **Resolved:** 2026-04-22

---

## FRIC-019 | No Sanctioned Path for Source Enrichment When Richer Version Available

- **Date:** 2026-04-22
- **Status:** closed
- **Phase:** Post-setup
- **Document implicated:** CLAUDE.md — Step 2 (duplicate detection); Section 5.4
  (source page frontmatter spec)
- **Symptom:** Step 2 hard-stopped on any exact URL match, regardless of why the
  duplicate was being submitted. A human who had a richer version of an already-ingested
  source (e.g., a full Obsidian clip replacing a truncated web fetch) had no sanctioned
  path to replace shallow extraction with deeper extraction. The only options were to
  abort or manually edit the source page outside the ingest workflow.
- **Verdict:** Confirmed schema gap — Step 2 had no differentiation between a true
  accidental duplicate (ingest error) and an intentional enrichment attempt. The hard
  stop was appropriate for the former but incorrectly blocked the latter.
- **Fix plan:** Step 2 now differentiates by the matched source page's status. For
  `status: retracted` or `ingested-in-error`, the hard stop is preserved. For
  `status: active`, a forced choice is surfaced (Abort / Enrich). Path B executes
  Step 2a: updates Source page frontmatter (`updated`, new `enriched` field), skips
  Steps 3–5 and Step 10, applies a downstream deduplication check before contradiction
  resolution in Steps 11–13, and uses a distinct commit message. The `enriched` field
  is added as an optional ISO 8601 date field to the source page frontmatter spec.
  Section 5.4 prose updated to list enrichment as the third exception to source page
  immutability.
- **Resolved:** 2026-04-22

---

## FRIC-020 | Source Page Summary Body Paragraph Undocumented

- **Date:** 2026-04-23
- **Status:** closed
- **Phase:** Post-setup
- **Document implicated:** CLAUDE.md — Section 5.4 (source page spec); Section 11.2 Step 10
- **Symptom:** Most source pages produced during ingest contain a prose summary paragraph below the frontmatter block. This behavior is not specified anywhere in CLAUDE.md — not in Section 5.4, not in Step 10. It is emergent LLM behavior that happens to be correct and consistent. A future model update or schema revision could silently regress it with no specification to catch the failure.
- **Verdict:** Confirmed weakness — undocumented emergent behavior. Not a gap in the sense of something missing that was intended, but a behavior that exists in practice and must be formally specified to prevent regression.
- **Fix plan:** Added a required body section to Section 5.4 immediately below the frontmatter block: one paragraph, 2–5 sentences, central argument and key findings, plain prose, present tense, immutable after creation except when Step 2a enrichment has been executed. Added to Step 10: "Write a summary paragraph immediately below the frontmatter block per Section 5.4." Updated Step 2a item 6 to include rewriting the summary paragraph from the richer extraction before moving the staged file. Two pre-schema anomalous pages (Stanford and Mollick, frontmatter-only) are now out of conformance; remediation is a human decision: manually write summaries, run Step 2a if richer files are available, or accept as pre-schema artifacts.
- **Resolved:** 2026-04-23

---

## FRIC-021 | No Ingest Provenance Field on Source Pages

- **Date:** 2026-04-23
- **Status:** closed
- **Phase:** Post-setup
- **Document implicated:** CLAUDE.md — Section 5.4 (source page frontmatter spec); Section 11.2 Step 10
- **Symptom:** Source pages record no information about how the source entered the system — whether Claude Code fetched the URL from the queue or processed a pre-staged local file. When source pages come out anomalous (e.g., frontmatter-only body), there is no basis for diagnosis. Two frontmatter-only pages (Stanford HAI and Mollick) could not be explained without this data.
- **Verdict:** Confirmed weakness — schema gap. Section 5.4 had no intake mechanism field. Section 11.2 describes two intake paths but neither is persisted to the source page.
- **Fix plan:** Added optional `ingest_via` field to Section 5.4 after the `enriched` field. Controlled vocabulary: `queue` (URL fetched from raw/queue.md [queued]) and `staged` (local file from raw/staged/). Set at Step 10; immutable after creation. `staged-url-fallback` deferred until the fallback mechanism is defined in the schema — adding a vocabulary value for undefined behavior is premature.
- **Resolved:** 2026-04-23

---

## FRIC-022 | Consumed Sources Deleted Rather Than Preserved

- **Date:** 2026-04-23
- **Status:** closed
- **Phase:** Post-setup
- **Document implicated:** CLAUDE.md — Section 2 (repo layout); Section 2.1 (queue.md scaffold); Section 11.2 Steps 2a and 22b; INIT-PROMPT.md Steps 6, 7, and 8
- **Symptom:** After successful ingest, staged files were removed from raw/staged/ and queue entries were consumed from raw/queue.md [queued] with no persistent record. Post-hoc diagnostics of past ingest sessions were impossible. Additionally, the normal ingest path (Steps 10–22a) contained no explicit staged file cleanup step at all — only the enrichment path (Step 2a) had a disposal instruction.
- **Verdict:** Confirmed weakness — two schema gaps: (1) raw/processed/ did not exist and staged files were deleted on ingest; (2) queue.md had no [processed] section and consumed entries disappeared entirely. A third gap was identified during fix planning: the normal ingest path had no staged file cleanup step, meaning the enrichment path's "Remove" instruction was the only disposal instruction in the schema.
- **Fix plan:** Added raw/processed/ to Section 2 repo layout (with gitignored note — same policy as raw/staged/; source files may be large or copyright-restricted). Added ## [processed] section to Section 2.1 queue.md scaffold with entry format (original entry + processed: YYYY-MM-DD) and a note that the human prunes it periodically. Added Step 22b (post-ingest housekeeping) to the execution pass: move staged files to raw/processed/ and move queue entries to ## [processed] for all successfully committed documents. Updated Step 2a item 6 from "Remove" to "Move to raw/processed/; rewrite summary paragraph first." Updated INIT-PROMPT.md Step 6 to create raw/processed/; updated Step 7 queue.md scaffold to include ## [processed] with format note; updated Step 8 .gitignore block to include raw/processed/ alongside raw/staged/. Note: portability-review.md GIT-06 still references only raw/staged/ in its .gitignore guidance — that entry requires a manual update by the human or a future session targeting portability-review.md. Retroactive patch for already-initialized wiki: run `mkdir raw/processed/` in repo root; append `## [processed]` to bottom of raw/queue.md; add `raw/processed/` to .gitignore.
- **Resolved:** 2026-04-23

---

## FRIC-023 | No podcast-transcript Source Type

- **Date:** 2026-04-25
- **Status:** closed
- **Phase:** Post-setup
- **Document implicated:** CLAUDE.md — Section 5.4 (source_type controlled vocabulary);
  Section 11.1 (source classification taxonomy)
- **Symptom:** A podcast transcript was submitted for ingest. No `podcast-transcript`
  source type existed in the controlled vocabulary. The human used `youtube-video` as a
  workaround. The classification was semantically wrong: the agent would see
  `source_type: youtube-video` with a `transcript_file` pointing to a podcast feed and
  no video URL, requiring rationalization with no schema basis.
- **Verdict:** Confirmed weakness — vocabulary gap in the source type taxonomy. The type
  did not exist; the workaround was semantically incorrect and would recur.
- **Fix plan:** Added `podcast-transcript` as the 9th source type: extraction depth
  `standard`, credibility tier `institutional` if official AI lab or research institution
  is primary host, `practitioner` otherwise. `transcript_file` required. Updated Section
  5.4 controlled vocabulary, Section 11.1 table and credibility logic, Step 3 reference
  ("nine-type decision tree"), and `transcript_file` conditional.
- **Resolved:** 2026-04-25

---

## FRIC-024 | Pitfalls Pages Never Created During Ingest

- **Date:** 2026-04-25
- **Status:** closed
- **Phase:** Post-setup
- **Document implicated:** CLAUDE.md — Section 11.2 (ingest workflow); Steps 7, 13, 16
- **Symptom:** Sources intentionally selected to build out the Pitfalls section were
  routed exclusively to Topic and Tool pages. No Pitfalls pages were ever proposed or
  created during ingest. The human had to manually override the agent's suggestions and
  force routing to Pitfalls pages, which is not intended behavior.
- **Verdict:** Confirmed structural gap — EXTRACTION-SKILL.md correctly identifies
  failure modes as "candidates for Pitfalls pages, not Key Claims," but no ingest step
  downstream of extraction acted on that routing. Steps 12 and 13 handle Topic and Tool
  pages; Step 15 handles Comparison pages. No equivalent pre-flight proposal or execution
  step existed for Pitfalls pages.
- **Fix plan:** Added Step 7a (pre-flight pitfalls proposal — fires when source contains
  at least one nameable failure mode meeting the substantive threshold: `### [Failure
  mode name]` entry with `**Status:**` designation; passing mentions do not qualify).
  Added Step 13a (execution — creates or updates Pitfalls page per Section 5.6 spec if
  Step 7a confirmed; routing rule applies). Updated Step 16 to include Pitfalls pages in
  index.md updates.
- **Resolved:** 2026-04-25

---

## FRIC-025 | PDF and PNG Files in assets/ Not Served by Quartz Public Site

- **Date:** 2026-04-25
- **Status:** closed
- **Phase:** Post-setup
- **Document implicated:** CLAUDE.md — Section 2 (repository structure, assets/ note)
- **Symptom:** A manually created methodology page referenced a PDF and a PNG stored in
  the `assets/` directory. Both files rendered correctly in Obsidian (reads directly from
  filesystem). Neither rendered on the Quartz-published public site — the browser received
  404s for both files.
- **Verdict:** Confirmed weakness — schema documentation conflated two distinct use cases
  for static files. `assets/` is listed in `ignorePatterns`, which correctly excludes its
  contents from Quartz page rendering but also prevents the Quartz Assets emitter from
  copying those files to `public/`. Files in `assets/` are therefore never served by the
  published site. Obsidian reads from the filesystem directly and is unaffected by
  ignorePatterns. Additionally, Quartz does not support inline PDF embedding via
  `![...]()` syntax — PDFs require an explicit `[text](url)` link or an HTML `<iframe>`
  block; Obsidian's native PDF viewer does not carry over to the web build.
- **Fix plan:** Updated Section 2 assets/ line to document the distinction: `assets/`
  is for operational images used by the LLM during maintenance; `quartz/static/` is the
  correct location for any file that must be served by the public Quartz site (images,
  PDFs, downloads). Files placed in `quartz/static/` are served at `/static/filename`
  and are not subject to ignorePatterns. PDF inline display requires explicit link syntax
  on the web even if Obsidian renders it natively.
- **Resolved:** 2026-04-25

---

## FRIC-026 | No Override Pattern Detection Mechanism

- **Date:** 2026-04-25
- **Status:** closed
- **Phase:** Post-setup
- **Document implicated:** CLAUDE.md — Section 11.4 (lint procedure, Phase 1); Section 5.9
  (wiki-lessons-learned spec)
- **Symptom:** No mechanism existed to detect when the human was consistently overriding
  the agent's decisions in a recurring category. Individual overrides were captured in
  wiki-lessons-learned.md per DM-024 but were never aggregated. A systematic definition
  problem, inference gap, or preference drift was indistinguishable from a one-time edge
  case without pattern detection.
- **Verdict:** Confirmed weakness — raw override data was being collected but never
  analyzed. Five distinct root causes identified: (1) schema definition overlap;
  (2) inference gap; (3) human preference drift; (4) vocabulary gap; (5) source ambiguity.
  Root causes 1–4 require design-session intervention; root cause 5 resolves via precedent
  entry. Without pattern detection, all five were invisible.
- **Fix plan:** Added lint Step L12c: reads wiki-lessons-learned.md ingest and lint
  sections, counts override entries by category over the past 30 days, auto-writes a
  `## Schema Signals` entry to wiki-lessons-learned.md if any category reaches 3+ overrides
  (no forced choice; informational only; one open signal per category maximum). Added
  `## Schema Signals` section to Section 5.9 with a distinct entry format naming all five
  root cause hypotheses. Added Schema Signals write step to Phase 3 execution pass.
  Updated L13 informational summary to report schema signal output. Human decides whether
  to bring a signal to a design session as a friction report.
- **Resolved:** 2026-04-25

---

## FRIC-027 | Agent Improvised Feature-Branch/PR Workflow; gh CLI Not Authenticated

- **Date:** 2026-04-27
- **Status:** open
- **Phase:** Post-setup
- **Document implicated:** CLAUDE.md — Section 11.2 (ingest workflow); implementation-handoff.md Phase 0; INIT-PROMPT.md
- **Symptom:** After an ingest operation, Claude Code attempted `gh pr create` and failed with "gh isn't authenticated in this environment." The agent had created a feature branch and was trying to open a pull request — behavior not prescribed by the schema. git push had succeeded (git and gh use independent authentication mechanisms); only the PR creation step failed.
- **Verdict:** Confirmed weakness — two distinct gaps. (1) CLAUDE.md's ingest workflow specifies per-document git commits but never prescribes the push strategy or explicitly prohibits feature-branch and PR workflows. This leaves the agent free to improvise a branching model, which conflicts with the deployment model: GitHub Actions deploys on push to main, so a feature branch blocks deployment until merged manually. (2) gh CLI installation and `gh auth login` are never mentioned in implementation-handoff.md Phase 0 or INIT-PROMPT.md. Even if the agent's PR behavior were intentional, authentication would silently fail on any new machine.
- **Fix plan:** Add an explicit commit-and-push instruction to CLAUDE.md Section 11.2, either as a sub-step of Step 22b or as a new Step 22c: commit all changes directly to main, run `git push origin main`, no feature branches, no `gh pr create`. The gh CLI is not required for any wiki operation. Remove any implicit affordance for branching by making the direct-to-main push instruction explicit. No change to INIT-PROMPT.md or implementation-handoff.md is required unless the push step is confirmed as a Phase 1 init-session item (it is not — first push is Phase 2).
- **Resolved:** —
