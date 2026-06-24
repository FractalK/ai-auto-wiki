---
type: wiki-lessons-learned
title: Wiki Lessons Learned
created: 2026-04-22
updated: 2026-06-23
last_entry: 2026-06-23
entry_count: 2
---

## Ingest

### [2026-05-29] OpenAI product announcement: industry-blog vs vendor-content
**Operation:** ingest
**What happened:** A product announcement blog post from openai.com (Codex feature launch) was initially classified as industry-blog → institutional based on the openai.com domain match rule.
**What was wrong:** Content purpose (product launch, marketing) overrides domain tier for posts announcing or promoting the vendor's own products. Domain match applies to research-oriented posts, technical analysis, and safety commentary — not product announcements.
**Correct behavior:** Classify as vendor-content → practitioner when the content purpose is a product announcement, feature launch, or marketing piece, regardless of whether the domain matches the institutional lab list.
**Signal for future cases:** Before applying the industry-blog domain rule, test content purpose first: if the post announces a vendor's own product, apply the vendor-content boundary test. Domain match is a fallback for ambiguous cases, not an override of content-purpose classification.

### [2026-06-23] Pre-flight missed existing page: anthropic-claude-opus-4-7
**Operation:** ingest
**What happened:** The pre-flight form generated decision 6 as a new tool page creation for `anthropic-claude-opus-4-7`. The page already existed at `tools/anthropic-claude-opus-4-7.md`. The human had to override in the decision string with an explicit note that the page exists.
**What was wrong:** Pre-flight did not check whether a tool page slug derived from a source's `related_tools` field already existed before presenting it as a creation decision.
**Correct behavior:** At pre-flight Step 3 (page decisions), for every tool or topic slug that would be a new page creation, check whether that file already exists in the wiki. If it does, present it as an update decision rather than a creation decision.
**Signal for future cases:** Before generating any page-creation decision in pre-flight, run a file-existence check on the derived slug path. If the file exists, route to update; if absent, route to create. Never present a creation decision for a page that already exists.

## Contradiction

## Tagging

## Lint

## Query

## Schema Signals
