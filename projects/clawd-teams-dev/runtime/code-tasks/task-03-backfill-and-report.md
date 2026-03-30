# Task 03 — Backfill + spending-report update

## What to build

### backfill_sessions.py
`~/code/clawd-teams/framework/backfill_sessions.py`
- Contains known session→role mappings for existing projects (seed from spend-tracker.py's project_sessions dict)
- For each project, calls record_session logic to populate session_registry.json
- Skips sessions already in session_registry.json (idempotent)
- Then calls sync_budget.py logic for each project to populate real spend

Seed data to include (copy from ~/.openclaw/workspace/spend-tracker.py):
- Run: `cat ~/.openclaw/workspace/spend-tracker.py` to find the `project_sessions` dict

### Update bin/spending-report
- At the top of the main logic, call `python3 framework/sync_budget.py <project>` for each project before reading budget.json
- This ensures report always shows live data

## Acceptance criteria
- After running backfill, `projects/rekordbox-mcp/runtime/budget.json` has non-zero spend_usd for roles that actually ran
- `bin/spending-report` shows non-zero USD figures for clawd-teams-dev and rekordbox-mcp
- spending-report runs in <5 seconds
- Commit with message: `feat: wire up real USD spend tracking via session_registry`

## Files
- `~/code/clawd-teams/framework/backfill_sessions.py`
- `~/code/clawd-teams/bin/spending-report`
- `~/code/clawd-teams/projects/rekordbox-mcp/runtime/session_registry.json` (created by backfill)
- `~/code/clawd-teams/projects/clawd-teams-dev/runtime/session_registry.json` (created by backfill)

## Complexity: MEDIUM
