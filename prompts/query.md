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

Today's operation: QUERY

Query: [describe your query here]
