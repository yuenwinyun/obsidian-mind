# HEARTBEAT.md

Use heartbeats for lightweight vault maintenance and context checks.

If nothing needs attention, return `HEARTBEAT_OK`.

## Default Checks

1. Read `brain/North Star.md`
2. Check `work/active/` and `work/Index.md` for stale active projects
3. Check whether recent work should be captured in:
   - `brain/Key Decisions.md`
   - `brain/Patterns.md`
   - `perf/Brag Doc.md`
4. Look for obvious orphan-note or index drift if many notes changed recently
5. Suggest only high-signal follow-up work

## Guardrails

- Do not invent tasks from old context
- Do not create churn by rewriting stable docs unnecessarily
- Prefer pointing to the exact vault file that needs attention
