# TOOLS.md

OpenClaw tool notes for this vault.

## Preferred Tools

- `obsidian` CLI when Obsidian is running
- `qmd` for semantic or hybrid vault search
- `rg` for fast filename and text search
- `git` for recent context and history

## Working Order

1. `qmd query` or `qmd vsearch` when looking for related notes
2. `obsidian read`, `obsidian search`, `obsidian backlinks`, `obsidian tasks daily todo`
3. direct filesystem reads only when the CLI is unavailable

## Examples

```bash
qmd query "redis migration decision"
obsidian read file="North Star"
obsidian backlinks file="Auth Refactor"
rg -n "\\[\\[" .
git log --oneline --since="48 hours ago" --no-merges
```
