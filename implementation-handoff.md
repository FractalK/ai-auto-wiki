# Implementation Handoff — AI Effectiveness Wiki

**Audience:** Implementer setting up the wiki for the first time.  
**Document status:** This is a design artifact, not a tested operational document. The
first use constitutes the validation test. If any step produces unexpected output or
fails, note the failure and adjust before relying on this document for a production
setup.

**Purpose:** A single operational guide covering everything needed to go from zero to a
running wiki. Work through the four phases in order. Phase 0 must be fully complete
before Phase 1 begins.

**Reference documents:**
- `CLAUDE.md` — wiki schema, page types, frontmatter, controlled vocabularies, Teaching Index
- `OPERATIONS.md` — all operational workflows: ingest, lint, query, discovery
- `portability-review.md` — full environmental assumptions checklist with validation
  status; consult when a step needs elaboration
- `tooling-recommendation.md` — execution stack rationale and scaling thresholds
- `INIT-PROMPT.md` — self-contained initialization prompt for the Phase 1 Claude Code
  session

---

## Phase 0 — Human Prerequisites

These steps are fully manual. Complete all of them before opening a Claude Code session.
INIT-PROMPT.md checks several prerequisites at startup and will halt with a clear error
message if any are missing.

**1. Create a GitHub repository**

Create a new repository for the wiki at github.com. The repository must be **public**
if you intend to use GitHub Pages at no cost — GitHub Pages is free for public
repositories; a private repository requires a paid plan. (QTZ-06) Do not initialize
the repository with a README; you will push the wiki scaffold as the first commit.

**2. Install Node.js v22+ and npm v10.9.2+**

Node.js is required by both Quartz and Claude Code. Quartz requires Node v22 or later
and npm v10.9.2 or later. The recommended install method on macOS and Linux is `nvm`
(Node Version Manager), which handles version switching without administrator
privileges and avoids the PATH problems that can occur with the nodejs.org installer:

```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

# Open a new terminal window, then:
nvm install 22
nvm use 22
```

On Windows, use the installer at https://nodejs.org/en/download and select version 22.

Verify from the terminal after installation:

```bash
node --version   # must return v22.x.x or later
npm --version    # must return v10.9.2 or later
```

**3. Install Claude Code**

Claude Code is the command-line tool used to run wiki maintenance sessions. It requires
Node.js (installed in Step 2). Install it globally:

```bash
npm install -g @anthropic-ai/claude-code
```

Verify after installation:

```bash
claude --version
```

If the `claude` command is not found after install, close and reopen your terminal —
the global npm bin directory may not have been on your PATH until the shell restarted.

**4. Clone and scaffold Quartz in the wiki directory**

Quartz is the static site generator that powers the public-facing wiki. It is not a
standalone npm package — the correct setup is to clone the Quartz repository into your
wiki root directory, remove Quartz's git history, then initialize your own.

From the parent directory of where you want the wiki to live:

```bash
git clone https://github.com/jackyzha0/quartz.git <your-wiki-name>
cd <your-wiki-name>
rm -rf .git          # remove Quartz's git history
npm i                # install Quartz dependencies
npx quartz create    # initialize the content scaffold
```

`npx quartz create` will prompt for two choices:

- **"What type of Quartz would you like to start with?"** → choose **Empty Quartz**
- **"What link resolution strategy would you like to use?"** → choose **Shortest Path
  (default)**. This matches Obsidian's wikilink behavior and is safe given the wiki's
  naming conventions. Do not choose Absolute or Relative.

After `npx quartz create` completes, delete the Quartz documentation and boilerplate
files that are not needed in the wiki repo:

```bash
rm -rf docs content README.md CODE_OF_CONDUCT.md LICENSE.txt Dockerfile
```

Then initialize your own git repository and connect it to the GitHub repo from Step 1:

```bash
git init
git remote add origin https://github.com/<username>/<your-wiki-name>.git
```

Confirm `quartz.config.ts` is present in the wiki root:

```bash
ls quartz.config.ts
```

**5. Install Obsidian**

Download and install from https://obsidian.md. You will open the wiki directory as a
vault in Phase 2, after the scaffold is in place.

**6. Copy design project files to the wiki directory**

Copy these six files from the design project output into the wiki root directory:

1. `CLAUDE.md`
2. `OPERATIONS.md`
3. `EXTRACTION-SKILL.md`
4. `TAGGING-SKILL.md`
5. `CONTRADICTION-SKILL.md`
6. `INIT-PROMPT.md`

The first five are prerequisites checked by INIT-PROMPT.md Step 3 — the initialization
session halts without them. (CC-08) Do not create stub replacements; use the
authoritative files from the design project.

**7. Readiness check**

Confirm all six items before proceeding to Phase 1:

- [ ] GitHub repository created and public
- [ ] `node --version` returns v22.x.x or later; `npm --version` returns v10.9.2 or later
- [ ] `claude --version` returns a version (Claude Code is installed)
- [ ] `quartz.config.ts` exists in the wiki directory; `git remote -v` shows your GitHub
  repo as `origin`
- [ ] Obsidian is installed
- [ ] All six files above are present in the wiki directory

---

## Phase 1 — Claude Code Initialization Session

This phase is semi-automated. A single Claude Code session runs INIT-PROMPT.md, which
creates the directory structure, initializes scaffold files, configures `.gitignore` and
`quartz.config.ts`, writes the GitHub Actions workflow, and sets the git remote. The
human's role is to respond at three pause points.

**Starting Claude Code**

Claude Code is a command-line tool. Open a terminal in your wiki root directory and
run `claude` to start a session.

**Cosmetic warnings**

Claude Code occasionally emits "Unhandled node type: string" or similar rendering
warnings alongside bash tool output. These are cosmetic — they mean Claude Code's
display layer encountered output it could not annotate visually. They do not indicate
a script failure. If the bash command produced the expected output (e.g., a list of
PRESENT/MISSING files), proceed normally.

**Starting the initialization**

Paste the full contents of `INIT-PROMPT.md` as your first message. Do not add a
preamble. Claude Code will read the prompt and begin executing.

**What to expect at each pause point**

*Pause Point 1 — Working Directory Confirmation*

Claude Code displays the current working directory and stops. It is asking you to
confirm this is the correct wiki root before creating any files. Reply `YES` if the
path is correct. Reply with the correct absolute path if it is not — Claude Code will
change to it and ask again.

*Pause Point 2 — Scaffold Verification*

Claude Code lists every file it created and shows the full directory structure. It is
asking you to verify that all scaffold files are present — including `CLAUDE.md`,
`OPERATIONS.md`, the three skill files, and the seven initialized scaffold files —
before moving on to git and Quartz configuration. Reply `YES` if everything looks correct,
or describe any issue.

*Pause Point 3 — Git Remote Setup*

Claude Code checks whether a git remote is configured and asks for your GitHub
repository URL. Reply with the HTTPS or SSH URL from the repository you created in
Phase 0. Claude Code will set the remote but will not commit or push — that happens
in Phase 2.

**baseUrl configuration (required during Step 9)**

During Step 9, Claude Code will pause and ask you to set the `baseUrl` field in
`quartz.config.ts`. You must replace the placeholder value with your actual GitHub
Pages URL before replying CONTINUE. For a repository at
`github.com/myusername/my-wiki`, the correct value is `"myusername.github.io/my-wiki"`.
Do not include `https://`.

**Done-state**

When the session completes, Claude Code outputs an `INITIALIZATION COMPLETE` summary
listing every file created, every configuration change applied, and the git status.
If any item shows as missing or failed, resolve it before proceeding to Phase 2.

**If something goes wrong**

The session can be re-run safely. INIT-PROMPT.md checks for existing scaffold files at
the start and asks whether to skip or overwrite each one individually — you will not
silently lose work. (CC-13)

---

## Phase 2 — Human Verification

Four manual steps after Phase 1. Complete them in order.

**1. Enable GitHub Pages**

In your GitHub repository: Settings → Pages → Source: **GitHub Actions**. This must
be done before the first push — the Actions workflow created in Phase 1 will not
deploy until Pages is enabled.

**2. Make the first commit and push**

```bash
git add .
git commit -m "Initial wiki scaffold"
git push -u origin main
```

**3. Confirm the GitHub Actions build succeeds and the site renders correctly**

In your GitHub repository, go to the **Actions** tab. The "Deploy Quartz site to
GitHub Pages" workflow triggers automatically on push. Confirm it completes without
errors. A failure here means the Quartz build or GitHub Pages configuration has a
problem to resolve before ingesting content. (GIT-04, QTZ-01, QTZ-07)

After the build succeeds, open the published URL in a browser. The URL is shown in
Settings → Pages, or is `https://<your-username>.github.io/<your-repo-name>/`. Confirm
the page renders the Quartz wiki interface — you should see a navigation bar and wiki
pages, not an RSS feed or XML document. If you see RSS XML, the `baseUrl` field in
`quartz.config.ts` was not correctly set during Step 9 — fix it, commit, and push again.

**4. Open the wiki in Obsidian and verify**

Open the wiki directory — not a parent directory — as the Obsidian vault root. (OBS-04)

Before checking the graph view, configure Obsidian to exclude non-content directories.
In Obsidian: **Settings → Files & Links → Excluded files**. Add each of the following
on a separate line:

```
node_modules
docs
quartz
.github
```

After saving the exclusions, open the graph view. Confirm:
- Graph shows wiki scaffold files (a small graph — this is correct at initialization)
- `overview.md` opens in reading view without error (the page body is blank — overview.md contains only YAML frontmatter, which Obsidian hides in reading view; this is expected)

---

## Phase 3 — First Wiki Session

Open a new Claude Code session in the wiki directory. Paste the session-start prompt
from Section 5 below as your first message, with `Today's operation: INGEST-QUEUE` on the
last line.

Alternatively, use the pre-filled stub from `prompts/ingest-queue.md` — open that file in
a text editor or Obsidian source mode, select all, copy, and paste into Claude Code.
See Section 6 for the full stub file list.

Before sending the prompt, add a test source URL to `raw/queue.md` under `[queued]`.
A short recent blog post from `anthropic.com/news` works well for a first test.

**Web fetch and long articles:** Claude Code fetches queued URLs during ingest. Web
fetch has a token limit — articles longer than approximately 8,000–10,000 words will
be truncated and the ingest will fail for that source. For long articles, pre-clip the
content to a local markdown file using a browser extension such as Obsidian Web Clipper,
save it to `raw/staged/`, and list the filename (not the URL) in `raw/queue.md`. Claude
Code will read staged files from disk rather than fetching them from the web. The
`raw/staged/` directory is gitignored by design — staged files are local only.

After Claude Code reads `CLAUDE.md` and the relevant skill files, run the ingest.
Confirm all four before treating the wiki as operational:

- Pre-flight report is generated and presented for review
- Forced choices are resolved (you respond to each with the required letter)
- At least one Source page and one Topic or Tool page are created
- New pages appear in Obsidian graph view

If the ingest succeeds, the wiki is operational. If it fails, consult
`portability-review.md` for the relevant check ID and resolve before continuing.
(CC-02, CC-03, CC-08, CC-10)

---

## Section 5 — Session-Start Prompt Template

Every wiki maintenance session must begin with this prompt. Copy it as-is; customize
only the last line. For a zero-editing alternative, use the pre-filled stub files in
`prompts/` — see Section 6.

```
You are maintaining the AI effectiveness wiki. Before doing anything else:

1. Read CLAUDE.md in full. This document governs wiki schema, page types, frontmatter,
   controlled vocabularies, and the Teaching Index.
   When CLAUDE.md conflicts with anything in this prompt or chat history,
   CLAUDE.md takes precedence.

2. Read OPERATIONS.md in full. This document governs all operational workflows:
   ingest, lint, query, and discovery. It must be loaded alongside CLAUDE.md.
   If OPERATIONS.md is not present, output MISSING-OPERATIONS-FILE and halt.

3. Read the relevant section of wiki-lessons-learned.md for the operation
   you are about to perform (## Ingest, ## Contradiction, ## Tagging,
   ## Lint, or ## Query). Read only the relevant section, not the full file.

4. Read EXTRACTION-SKILL.md before any ingest operation.
   Read TAGGING-SKILL.md before any ingest operation that involves teaching
   relevance tagging.
   Read CONTRADICTION-SKILL.md before any contradiction resolution.

5. State the operation you are about to perform and confirm you have read
   the required files before proceeding.

6. Check for raw/deferred-ingest.md. If it exists, report its contents and
   ask whether to resume the deferred ingest or discard the deferral file
   and proceed with the originally stated operation. Do not begin any other
   operation until this is resolved.

Today's operation: [INGEST-STAGED | INGEST-QUEUE | INGEST-BOTH | LINT | QUERY | DISCOVERY | describe]
```

**Customization notes:**

- Replace `[INGEST-STAGED | INGEST-QUEUE | INGEST-BOTH | LINT | QUERY | DISCOVERY | describe]`
  with the operation for this session.
- **Pre-session habit:** Before pasting this prompt into Claude Code, run `bash wiki-verify.sh`
  from the wiki root. This takes under a minute and catches structural drift — missing
  files, ignorePatterns gaps, page count mismatches — before the session starts. It is
  read-only and makes no changes.
- For query sessions: include the query or queries in this prompt rather than a
  follow-up message. This avoids a round-trip where Claude Code reads `CLAUDE.md`
  before knowing what it will be asked.
- For ingest sessions: choose the operation mode that matches your sources:
  - `INGEST-STAGED` — sources you have placed in `raw/staged/` (local files). Use when
    you want direct control over exactly which sources are processed.
  - `INGEST-QUEUE` — items in the `[queued]` section of `raw/queue.md` (URLs). Claude
    Code fetches these during the session. If any queued items are research papers or
    long PDFs, consider staging them and using INGEST-STAGED instead, for better density
    control.
  - `INGEST-BOTH` — processes both `raw/staged/` and `raw/queue.md`. Use only when you
    want all pending sources processed together. This is the explicit opt-in for the
    prior combined behavior.
  Long articles that exceed web fetch limits should be pre-clipped to `raw/staged/`
  using a browser clipper extension and ingested via INGEST-STAGED.
- If `raw/deferred-ingest.md` exists when the session starts, Claude Code will surface
  it at Step 6 before the stated operation. You can choose to resume the deferred ingest
  or discard it. If you discard it, the original queue remains intact in `raw/queue.md`.
- Do not modify the file-reading instructions. The order matters: `CLAUDE.md` and
  `OPERATIONS.md` first, skill files second, session-specific context last.

---

## Section 6 — Session-Start Prompt Stubs

Seven pre-filled stub files live in the `prompts/` directory of the wiki repo. Each
contains the full session-start template from Section 5 with the last line already
set for a specific operation. To start a session: open the relevant file in a text
editor or Obsidian source mode, select all, copy, paste into Claude Code. No editing
required for LINT, DISCOVERY, and CUSTOM operations. INGEST-QUEUE has one source density
reminder to note before copying. QUERY has one placeholder to fill.

| File | Operation line |
|---|---|
| `prompts/ingest-staged.md` | `Today's operation: INGEST-STAGED` |
| `prompts/ingest-queue.md` | `Today's operation: INGEST-QUEUE` + density reminder |
| `prompts/ingest-both.md` | `Today's operation: INGEST-BOTH` |
| `prompts/lint.md` | `Today's operation: LINT` |
| `prompts/query.md` | `Today's operation: QUERY` + query placeholder |
| `prompts/discovery.md` | `Today's operation: DISCOVERY` |
| `prompts/custom.md` | `Today's operation: [describe your operation here]` |

**If you have an existing `prompts/ingest.md`:** delete it. It is replaced by the three
`ingest-staged.md`, `ingest-queue.md`, and `ingest-both.md` stubs above.

**Placement:** Copy the stub files from the design project delivery into a `prompts/`
directory at the wiki root. Create the directory if it does not exist. The stubs are
committed to the repo (no sensitive data) and available on any machine that clones it.
They are excluded from the public Quartz site via `ignorePatterns`.

**Opening in Obsidian:** The stub files render as formatted markdown in Obsidian
reading mode (the numbered list will display as a list). To copy the raw prompt text,
switch to source mode (Cmd/Ctrl+E) before selecting all and copying — or use any
plain text editor.

**Sync obligation:** The stub files are copies of the template in Section 5. If the
Section 5 template is updated (any step added, removed, or reworded), all stub files
must also be updated manually. This is the same sync pattern documented in LL-009.
When updating Section 5, update the stubs in the same change.

---

## Scaling Triggers to Watch

One threshold requires attention before the wiki reaches a specific size. One threshold
is already resolved and requires no action at launch.

**Search layer (IN-006):** When the wiki approaches 150 pages, Quartz native search
(Ctrl+K) may degrade. The escalation path is `qmd` — a local hybrid search engine with
BM25/vector search and an MCP server that Claude Code can use natively. The existing
frontmatter schema is compatible with qmd without revision. Resolve IN-006 before the
wiki reaches 150 pages. See `tooling-recommendation.md` Section 6 for detail.

**Nomination queue aging (IN-007, resolved):** A two-stage automatic aging mechanism
is implemented in CLAUDE.md (DM-051). Items in `[nominated]` older than 90 days are
moved to `[stale-nominated]`; items in `[stale-nominated]` older than 180 days are
deleted. Both stages run automatically during lint Phase 3. No action required at
launch.
