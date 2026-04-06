# Dump

Process the user's freeform work dump and route each distinct item into the right part of the vault.

For each meaningful piece of information:

1. Classify it: decision, incident, 1:1 content, win, architecture, project update, person context, or general work note
2. Search before creating anything:
   - prefer `qmd vsearch` or `qmd query`
   - otherwise use Obsidian CLI search or `rg`
3. Update an existing note when the new information is incremental
4. Create a new note only when the content is clearly a new durable node
5. Follow `AGENTS.md` for folder placement, frontmatter, and linking
6. Update the relevant indexes if new durable knowledge was added

After processing, summarize:

- what was captured
- which notes were updated
- which notes were created
- anything ambiguous that needs user input

Every new note should have frontmatter and at least one `[[wikilink]]`.
