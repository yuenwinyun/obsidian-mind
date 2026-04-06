# Obsidian Mind for Codex

This repository is an Obsidian vault template. For Codex, this file is the primary operating manual.

The durable system is the vault itself:
- goals live in `brain/North Star.md`
- memory lives in `brain/`
- active work lives in `work/active/`
- people and org context live in `org/`
- performance evidence lives in `perf/`

Claude-specific automation still exists under `.claude/`. Codex can reuse those files as references, but should not assume Claude hooks or slash commands run automatically.

## Session Start

Before substantial work:

1. Read `Home.md`
2. Read `brain/North Star.md`
3. Read `work/Index.md`
4. Scan `brain/Memories.md`, then open the relevant topic notes
5. Check recent changes with `git log --oneline --since="48 hours ago" --no-merges`
6. If Obsidian CLI is available, prefer it for note reads, backlinks, tasks, and property updates

If the user asks for a morning kickoff or says "start session", follow `.codex/prompts/standup.md`.

## Core Rules

### Search Before Create

- Prefer `qmd query`, `qmd search`, or `qmd vsearch` before reading many files
- If QMD is unavailable, use Obsidian CLI search or `rg`
- Before creating a note, check whether the information belongs in an existing note

### Vault-First Memory

- Durable knowledge belongs in the vault, not in external scratch files
- `brain/` is the long-term memory system
- `work/`, `org/`, and `perf/` hold the evidence trail

### Note Hygiene

Every substantive note should have:
- YAML frontmatter with `date`, `description`, and `tags`
- the correct folder placement
- at least one `[[wikilink]]` to another note

A note without links is a bug.

### Folder Placement

- current projects: `work/active/`
- archived projects: `work/archive/YYYY/`
- incidents: `work/incidents/`
- 1:1s: `work/1-1/`
- people: `org/people/`
- teams: `org/teams/`
- competency evidence and review artifacts: `perf/`
- durable operating knowledge: `brain/`
- scratch thinking: `thinking/`

### Index Maintenance

When creating or materially changing notes, update the relevant indexes:
- `work/Index.md`
- `brain/Memories.md`
- `org/People & Context.md`
- `perf/Brag Doc.md`

## Codex Prompt Library

Core Codex workflows live in `.codex/prompts/`:

- `standup.md` — morning orientation
- `dump.md` — freeform capture and routing
- `wrap-up.md` — end-of-session review

Use them as reusable prompt text or operational checklists. For advanced workflows that are still Claude-first, consult `.claude/commands/`.

## Natural-Language Routing

When the user says something like:

- "start session", "standup", or "what should I focus on today"
  - follow `.codex/prompts/standup.md`
- provides a large unstructured update, meeting recap, or decision dump
  - follow `.codex/prompts/dump.md`
- "wrap up", "let's wrap", or asks for an end-of-day review
  - follow `.codex/prompts/wrap-up.md`

## Obsidian CLI

When Obsidian is running, prefer CLI over raw filesystem:

```bash
obsidian read file="North Star"
obsidian search query="redis migration"
obsidian backlinks file="Auth Refactor"
obsidian tasks daily todo
obsidian property:set name="status" value="completed" file="Auth Refactor"
```

Fall back to direct file reads only when the CLI is unavailable.

## Compatibility Notes

- `CLAUDE.md` remains the detailed manual for Claude Code
- `.claude/commands/`, `.claude/agents/`, and `.claude/scripts/` remain supported for Claude users
- Codex should treat those files as source material, not as automatically active runtime features
