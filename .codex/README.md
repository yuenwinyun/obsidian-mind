# Codex Prompt Library

This folder contains Codex-facing workflow prompts for the core daily loops in Obsidian Mind.

These prompts are not magical runtime hooks. They are reusable instructions you can:

- paste into a Codex session
- point Codex at when you want a specific workflow
- use with `codex exec` from the vault root

Examples:

```bash
codex exec "$(cat .codex/prompts/standup.md)"
codex exec "$(cat .codex/prompts/wrap-up.md)"
```

For a freeform dump, paste the contents of `.codex/prompts/dump.md` and then append the material you want processed.

Advanced workflows remain under `.claude/commands/` for now. Codex can still follow those markdown instructions when asked, but only the core daily flows have been ported into `.codex/prompts/`.
