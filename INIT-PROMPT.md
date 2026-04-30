# Wiki Initialization Session

You are running the **one-time initialization** of the AI effectiveness wiki. This
session creates the directory structure, scaffold files, and configuration needed before
the first wiki maintenance operation.

You are NOT running a wiki maintenance session. Do not attempt to read CLAUDE.md as a
first step — it does not yet exist in this directory as an operational file. Your
instructions for this session are entirely contained in this prompt.

Follow the steps below in order. At three explicitly marked pause points, stop and wait
for human confirmation before continuing. Do not skip a pause point because the next
step seems safe — the pauses exist to give the human a verification opportunity.

If any prerequisite check fails, stop and report the gap. Do not work around a failed
prerequisite.

---

## Step 1 — Confirm Working Directory

Run `pwd` and display the result. Then stop and output exactly:

```
PAUSE POINT 1 — Working Directory Confirmation

Current directory: [insert pwd result here]

All wiki files will be created in this directory. This cannot be undone without
manually deleting the files.

Is this the correct wiki root directory?
Reply YES to continue, or reply with the correct absolute path and I will change
to it and ask again.
```

Do not proceed to Step 2 until the human explicitly replies YES (or you have changed
to a confirmed correct path and received YES for it).

---

## Step 2 — Idempotency Check

Check whether any of the following scaffold files already exist in the current
directory:

```
overview.md
index.md
log.md
teaching-index.md
raw/queue.md
raw/collection-gaps.md
raw/discovery-sources.md
wiki-lessons-learned.md
```

If **none** are found: output "No existing scaffold files found. Proceeding." and
continue to Step 3 without pausing.

If **any** are found: output exactly:

```
INITIALIZATION HALT — Existing scaffold files detected.

Found: [list each file that exists]

This directory appears to be partially or fully initialized. I will not overwrite
existing files without your explicit permission for each one.

For each file listed above, reply with:
  SKIP     — leave the existing file untouched
  OVERWRITE — replace it with the default initial content

Example reply:
  overview.md: SKIP
  raw/queue.md: OVERWRITE

Reply with a decision for each found file before I proceed.
```

Wait for per-file decisions. Skip or overwrite only the files the human explicitly
indicates. Do not touch any file marked SKIP.

---

## Step 3 — Check Required Source Files

Verify that the following files are present in the current directory:

```
CLAUDE.md
OPERATIONS.md
EXTRACTION-SKILL.md
TAGGING-SKILL.md
CONTRADICTION-SKILL.md
```

These files must have been copied from the design project output before this session
started. They are not created by this initialization prompt — they are too large to
embed here and must come from the authoritative design project source.

If **all five are present**: output a one-line confirmation and continue to Step 4.

If **any are missing**: output exactly:

```
PREREQUISITE GAP — Required source files are missing.

Missing: [list each missing file]

These files must be copied from the design project output to this directory before
initialization can continue. They cannot be created here — they must come from the
authoritative design project source.

Steps to resolve:
1. Locate the design project output (the Claude.ai project where the wiki schema
   was designed).
2. Download or copy each missing file into this directory.
3. Reply CONTINUE once all missing files are in place.
```

Do not create stub replacements for these files. Wait for CONTINUE before proceeding.

---

## Step 4 — Check Node.js and npm

Run `node --version` and `npm --version`.

If either command is not found: output exactly:

```
PREREQUISITE GAP — Node.js is not installed or not on PATH.

Node.js v22 or later and npm v10.9.2 or later are required for Quartz.

Recommended install method on macOS/Linux (nvm):
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
  # Open a new terminal window, then:
  nvm install 22
  nvm use 22

On Windows: download from https://nodejs.org/en/download and select version 22.

After installing, run `node --version` and `npm --version` to confirm versions,
then reply CONTINUE.
```

Wait for CONTINUE before proceeding.

If `node --version` returns a version below v22 (e.g., v18.x.x or v20.x.x): output
exactly:

```
PREREQUISITE GAP — Node.js version [X] is below the required minimum of v22.

Upgrade using nvm:
  nvm install 22
  nvm use 22

Or download Node.js 22 from https://nodejs.org/en/download.
Then reply CONTINUE.
```

Wait for CONTINUE before proceeding.

If `npm --version` returns a version below 10.9.2: output exactly:

```
PREREQUISITE GAP — npm version [X] is below the required minimum of 10.9.2.

Upgrade npm:
  npm install -g npm@latest

Then run `npm --version` to confirm, and reply CONTINUE.
```

Wait for CONTINUE before proceeding.

If both commands return acceptable versions (node v22+, npm v10.9.2+): output a
one-line confirmation and continue to Step 5.

---

## Step 5 — Check Quartz Scaffold

Check whether `quartz.config.ts` exists in the current directory.

If it does **not** exist: output exactly:

```
PREREQUISITE GAP — quartz.config.ts not found.

Quartz must be cloned and initialized before initialization continues.
Run these commands from the PARENT of your intended wiki root directory:

  git clone https://github.com/jackyzha0/quartz.git <your-wiki-name>
  cd <your-wiki-name>
  rm -rf .git          # remove Quartz's git history
  npm i                # install Quartz dependencies
  npx quartz create    # initialize content scaffold

When npx quartz create prompts:
  "What type of Quartz would you like to start with?" → choose Empty Quartz
  "What link resolution strategy would you like to use?" → choose Shortest Path (default)

After that, delete the Quartz boilerplate files that do not belong in the wiki repo:
  rm -rf docs content README.md CODE_OF_CONDUCT.md LICENSE.txt Dockerfile

Then re-initialize git and set your remote:
  git init
  git remote add origin https://github.com/<username>/<your-wiki-name>.git

Return to this directory and reply CONTINUE once quartz.config.ts is present.
```

Wait for CONTINUE before proceeding.

If `quartz.config.ts` exists: output a one-line confirmation and continue to Step 6.

---

## Step 6 — Create Directory Structure

Create the following directories. For any directory that does not already exist,
create it and add an empty `.gitkeep` file so git will track the directory.

```
assets/
raw/staged/
raw/processed/
topics/
tools/
sources/
comparisons/
pitfalls/
teaching/
```

Do not add `.gitkeep` to `raw/` itself — it will contain real files. Do not add
`.gitkeep` to `raw/staged/` or `raw/processed/` if they contain existing files.

After completing this step, output a brief summary:
- Which directories were created
- Which already existed
- Which `.gitkeep` files were written

Then continue to Step 7 without pausing.

---

## Step 7 — Create Scaffold Files

Create the following files with the exact content shown. Replace every instance of
`YYYY-MM-DD` with today's actual date in ISO 8601 format (e.g., 2026-04-20).

After creating each file, output a one-line confirmation (e.g., "Created overview.md").
Do not output the file contents to the chat.

If a file was marked SKIP in Step 2, do not create or modify it — output
"Skipping [filename] per Step 2 decision" instead.

---

**overview.md** — create in wiki root:

```markdown
---
type: overview
title: Wiki Overview
created: YYYY-MM-DD
updated: YYYY-MM-DD
total_pages: 0
total_sources: 0
open_contradictions: 0
last_contradiction_id: 0
---
```

`last_contradiction_id` must be exactly `0`. Claude Code increments this before
assigning every CTRD-NNN identifier. `open_contradictions` is initialized to `0`
explicitly — absence of the field could be misread as unknown state during lint.
Do not add `last_lint` or `last_discovery` — their absence correctly signals that
no lint or discovery pass has run yet.

---

**index.md** — create in wiki root:

```markdown
---
type: index
title: AI Effectiveness Wiki
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

This wiki tracks AI tools, capabilities, workflows, and failure modes for practitioners
who need to evaluate and apply AI in professional settings. Content is organized by
concept area, product, and use case — updated continuously as new sources are ingested.

Browse by category below. For content aligned to specific learning objectives and
professional roles, see the [[teaching-index]].

*0 pages. Last updated: YYYY-MM-DD.*

---

## Topics

## Tools

## Sources

## Comparisons

## Pitfalls

## Teaching
```

The intro prose and At a Glance line are part of the scaffold. The At a Glance line
(`*0 pages. Last updated: YYYY-MM-DD.*`) uses `0` at initialization; Claude Code
updates the page count and date after each ingest. The intro prose is written once
and never modified by Claude Code — it is the public-facing landing page identity.

---

**log.md** — create in wiki root:

```markdown
---
type: log
title: Operation Log
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_entry: YYYY-MM-DD
entry_count: 0
---
```

---

**teaching-index.md** — create in wiki root:

```markdown
---
type: teaching-index
title: Teaching Index
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

*Generated on first ingest that touches a page tagged teaching_relevance: true.*
```

---

**raw/queue.md** — create in raw/ subdirectory:

```markdown
## [queued]

## [nominated]

## [stale-nominated]

## [processed]
```

No other content. Four section headers only. Entries move from `## [queued]` to
`## [processed]` after successful ingest (Step 22b), with `processed: YYYY-MM-DD`
appended to the original entry line. The human prunes this section periodically.

---

**raw/collection-gaps.md** — create in raw/ subdirectory:

```markdown
# Collection Gaps
Last updated: YYYY-MM-DD (initialization)

## Active Gaps

## Potentially Addressed

## Resolved
```

---

**raw/discovery-sources.md** — create in raw/ subdirectory:

```
# Discovery Sources
# Format: {url} | {type: arxiv | lab-blog | academic-blog} | {label}
# academic-blog: academic institution publications (Stanford HAI, Berkeley BAIR, etc.)
#   — fetched identically to lab-blog; distinction is metadata only.
# Edit this list before the first discovery pass.
# Add or remove feeds as the team's source priorities evolve.

https://www.anthropic.com/news | lab-blog | Anthropic News
https://openai.com/news/research | lab-blog | OpenAI Research
https://deepmind.google/discover/blog | lab-blog | Google DeepMind Blog
https://hai.stanford.edu/news | academic-blog | Stanford HAI
https://cset.georgetown.edu/category/blog/ | academic-blog | CSET Georgetown
https://www.brookings.edu/topic/artificial-intelligence/ | academic-blog | Brookings AI
https://partnershiponai.org/blog/ | academic-blog | Partnership on AI
```

---

**wiki-lessons-learned.md** — create in wiki root:

```markdown
---
type: wiki-lessons-learned
title: Wiki Lessons Learned
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_entry: YYYY-MM-DD
entry_count: 0
---

## Ingest

## Contradiction

## Tagging

## Lint

## Query

## Schema Signals
```

`last_entry` is initialized to today's date (the creation date). `entry_count` is 0.
Entries will be drafted by Claude Code after ingest or lint passes where the human
overrides a decision.

---

## PAUSE POINT 2 — Verify Directory Structure

After creating all scaffold files, output exactly:

```
PAUSE POINT 2 — Scaffold Files Created

Files created in this step:
  [list every file created or skipped in Step 7]

Current directory structure (run `find . -not -path './.git/*' -not -path './node_modules/*' | sort` to see it):
  [show output of the find command above]

Before I proceed to git setup and Quartz configuration:
  - Verify the directory structure looks correct
  - Confirm overview.md, index.md, log.md, teaching-index.md, raw/queue.md,
    raw/collection-gaps.md, raw/discovery-sources.md, and wiki-lessons-learned.md
    are all present
  - Confirm CLAUDE.md, OPERATIONS.md, EXTRACTION-SKILL.md, TAGGING-SKILL.md, and
    CONTRADICTION-SKILL.md are present (copied from design project output)

Reply YES to continue to git and Quartz configuration, or describe any issues.
```

Do not proceed to Step 8 until the human explicitly replies YES.

---

## Step 8 — Configure .gitignore

Check whether a `.gitignore` file already exists in the current directory.

If it exists: read its current content. Append the following block at the end,
preserving all existing content:

```
# Wiki: exclude source files — potentially large or copyright-restricted
raw/staged/
raw/processed/

# Keep .gitkeep files in tracked empty directories
!**/.gitkeep
```

If it does not exist: create it with only the content above.

Do not remove any existing `.gitignore` entries.

Output a one-line confirmation noting whether the file was created or appended to.

---

## Step 9 — Patch quartz.config.ts

Read the existing `quartz.config.ts` in full before making any changes. Make exactly
three targeted changes:

**Change 1 — ignorePatterns**

Locate the `ignorePatterns` field (it may already exist with some default entries
such as `"private"` or `"templates/**"`). Add the following paths to the array,
preserving any existing entries:

```
"CLAUDE.md"
"OPERATIONS.md"
"EXTRACTION-SKILL.md"
"TAGGING-SKILL.md"
"CONTRADICTION-SKILL.md"
"wiki-lessons-learned.md"
"assets/**"
"raw/**"
"docs/**"
"content/**"
"prompts/**"
"node_modules/**"
"INIT-PROMPT.md"
"public/**"
"overview.md"
"log.md"
"design/**"
```

If no `ignorePatterns` field exists anywhere in the file, add one. The resulting
array must contain at minimum the seventeen paths listed above.

Note: Do NOT add `"index.md"` to ignorePatterns. Quartz requires `index.md` at the
repo root to generate `index.html` — the site's home page. Excluding it will cause
Quartz to emit no root HTML page; browsers will serve `index.xml` (the RSS feed)
instead.

**Change 2 — Mermaid plugin**

Locate the `transformers` array in the plugins configuration block. Add
`Plugin.Mermaid()` to the list if it is not already present. Position does not
matter as long as it is inside the `transformers` array.

**Change 3 — baseUrl**

Locate the `baseUrl` field. Change its value to:

```
"<your-github-username>.github.io/<your-repo-name>"
```

This is a placeholder. The human must replace it with their actual GitHub Pages URL
before committing. For a repository at `github.com/myusername/my-wiki`, the correct
value is `"myusername.github.io/my-wiki"`. Do not include `https://` — Quartz
prepends the protocol automatically.

After patching, stop and output exactly:

```
CONFIGURATION REQUIRED — quartz.config.ts baseUrl

I have set baseUrl to the placeholder value:
  "<your-github-username>.github.io/<your-repo-name>"

You must replace this with your actual GitHub Pages URL before committing.
For your repository at https://github.com/<username>/<repo>, the value should be:
  "<username>.github.io/<repo>"

Do not include https:// — Quartz adds the protocol automatically.

Edit quartz.config.ts now to replace the placeholder, then reply CONTINUE.
```

Wait for CONTINUE before proceeding to Step 10.

After receiving CONTINUE, output a brief description of all three changes: confirm
whether `ignorePatterns` was extended or created from scratch, whether
`Plugin.Mermaid()` was added or was already present, and confirm the baseUrl the
human entered.

Do not rewrite any other parts of `quartz.config.ts`.

---

## Step 10 — Create GitHub Actions Workflow

Create the directory `.github/workflows/` if it does not already exist.

Create the file `.github/workflows/deploy.yml` with this exact content:

```yaml
name: Deploy Quartz site to GitHub Pages

on:
  push:
    branches:
      - main

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true

jobs:
  build:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - name: Install Quartz dependencies
        run: npm ci
      - name: Build Quartz
        run: npx quartz build -d .
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: public

  deploy:
    needs: build
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-22.04
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

Output a one-line confirmation that the file was created.

Note: This workflow will not succeed until GitHub Pages is enabled for the repository
(Settings → Pages → Source: GitHub Actions). The human verifies this in Phase 2 of
the implementation guide, not during this session.

The `-d .` flag on `npx quartz build` tells Quartz to read content from the repository
root rather than the default `content/` subdirectory. This is required because wiki
pages live at the repo root alongside `quartz.config.ts`. The `ignorePatterns` entries
added in Step 9 prevent non-wiki files (docs/, content/, skill files, etc.) from being
built into the site.

---

## Step 11 — Write Pre-Commit Hook

Create the file `.git/hooks/pre-commit` with this exact content:

```bash
#!/bin/sh
# Reject filenames with uppercase letters or spaces in wiki content directories.
# macOS filesystems are case-insensitive; a violation that passes here will break
# the Quartz build on GitHub Actions (Linux, case-sensitive filesystem).

DIRS="topics tools sources comparisons pitfalls teaching raw"

for dir in $DIRS; do
  if [ -d "$dir" ]; then
    violations=$(git diff --cached --name-only | grep "^$dir/" | grep -E '[A-Z ]')
    if [ -n "$violations" ]; then
      echo "ERROR: The following staged filenames contain uppercase letters or spaces:"
      echo "$violations"
      echo "Rename to lowercase kebab-case before committing (e.g., my-topic.md)."
      exit 1
    fi
  fi
done

exit 0
```

Make it executable:

```bash
chmod +x .git/hooks/pre-commit
```

Output a one-line confirmation that the hook was written and made executable.

---

## PAUSE POINT 3 — Git Remote Setup

Check the git status:
- Run `git status` to confirm git is initialized. If it is not, run `git init` first.
- Run `git remote -v` to check whether a remote named `origin` is already configured.

Then output exactly:

```
PAUSE POINT 3 — Git Remote

Git repository status: [initialized / just initialized]
Existing remotes: [show output of git remote -v, or "none configured"]

To finish initialization, I need the remote URL for your GitHub repository.
This is the repository you created for this wiki. The URL looks like one of:
  HTTPS: https://github.com/yourusername/your-wiki-repo.git
  SSH:   git@github.com:yourusername/your-wiki-repo.git

Reply with one of:
  [your remote URL] — I will run `git remote add origin [URL]`
  SKIP              — a remote is already configured and I should leave it as-is
  LATER             — skip remote setup for now (you will configure it manually)
```

Wait for the human's reply.

If they provide a URL: run `git remote add origin [URL]` (or
`git remote set-url origin [URL]` if a remote already exists). Confirm the remote
was set by running `git remote -v` and displaying the output.

If they reply SKIP or LATER: acknowledge and proceed to Step 12.

Do not run `git add`, `git commit`, or `git push` in this session. The first commit
is part of Phase 2 (human verification) in the implementation guide, not here.

---

## Step 12 — Initialization Summary

Output the following summary, filling in the bracketed fields:

```
INITIALIZATION COMPLETE

--- Files created ---
Scaffold files:
  overview.md
  index.md
  log.md
  teaching-index.md
  raw/queue.md
  raw/collection-gaps.md
  raw/discovery-sources.md
  wiki-lessons-learned.md

Copied from design project (verified present, not created):
  CLAUDE.md
  OPERATIONS.md
  EXTRACTION-SKILL.md
  TAGGING-SKILL.md
  CONTRADICTION-SKILL.md

--- Configuration applied ---
.gitignore          [created / appended to]
quartz.config.ts    baseUrl [value the human entered]; ignorePatterns [added / extended]; Plugin.Mermaid() [added / already present]
.github/workflows/deploy.yml    created
.git/hooks/pre-commit           created and made executable

--- Git ---
Repository:   [initialized / was already initialized]
Remote:       [URL / not configured]

--- NOT in scope for this session ---
First commit and push (do this after Phase 2 verification)
Enabling GitHub Pages (do this in repository settings before first push)
Opening Obsidian (do this after this session ends)
First wiki maintenance session (use the session-start prompt template)

--- Next steps ---
1. Open the wiki directory (not a parent) as your Obsidian vault. Configure
   excluded files before opening graph view: Settings → Files & Links →
   Excluded files → add: node_modules, docs, quartz, .github
2. Enable GitHub Pages in your repository settings:
   Settings → Pages → Source: GitHub Actions
3. Make a first commit and push to main. Confirm the GitHub Actions build succeeds.
4. Open the published URL in a browser and confirm it renders the Quartz wiki
   interface (not an RSS feed). If you see RSS XML, the baseUrl in quartz.config.ts
   was not updated from the placeholder — fix it, commit, and push again.
5. Run the first wiki session: paste the session-start prompt from
   implementation-handoff.md Section 5 (or use a pre-filled stub from prompts/)
   into a new Claude Code session and run a test ingest.
```

---

## Environmental Assumptions

This prompt assumes the following are true before the session starts:

- A GitHub repository has been created for the wiki (human prerequisite)
- Node.js v22+ and npm v10.9.2+ are installed — checked at Step 4
- Quartz has been cloned and scaffolded per Phase 0 Step 4 of implementation-handoff.md,
  with `quartz.config.ts` present at the wiki root — checked at Step 5
- CLAUDE.md, OPERATIONS.md, EXTRACTION-SKILL.md, TAGGING-SKILL.md, and CONTRADICTION-SKILL.md
  have been copied from design project output to this directory — checked at Step 3
- The working directory is the intended wiki root — confirmed at Pause Point 1

This is a design artifact. It has not been validated by running against an actual
Claude Code session. Treat the first use as a test run: if any step produces unexpected
output or fails, note the failure and adjust before relying on this prompt for a
production wiki setup.
