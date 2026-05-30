---
type: wiki-lessons-learned
title: Wiki Lessons Learned
created: 2026-04-22
updated: 2026-05-29
last_entry: 2026-05-29
entry_count: 1
---

## Ingest

### [2026-05-29] OpenAI product announcement: industry-blog vs vendor-content
**Operation:** ingest
**What happened:** A product announcement blog post from openai.com (Codex feature launch) was initially classified as industry-blog → institutional based on the openai.com domain match rule.
**What was wrong:** Content purpose (product launch, marketing) overrides domain tier for posts announcing or promoting the vendor's own products. Domain match applies to research-oriented posts, technical analysis, and safety commentary — not product announcements.
**Correct behavior:** Classify as vendor-content → practitioner when the content purpose is a product announcement, feature launch, or marketing piece, regardless of whether the domain matches the institutional lab list.
**Signal for future cases:** Before applying the industry-blog domain rule, test content purpose first: if the post announces a vendor's own product, apply the vendor-content boundary test. Domain match is a fallback for ambiguous cases, not an override of content-purpose classification.

## Contradiction

## Tagging

## Lint

## Query

## Schema Signals
