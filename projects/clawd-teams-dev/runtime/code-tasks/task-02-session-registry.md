# Task 02 — Session attribution sidecar

## What to build

### record_session.py
`~/code/clawd-teams/framework/record_session.py <project> <role> <session_id>`
- Appends a record to `projects/<project>/runtime/session_registry.json`
- Record shape: `{"session_id": "...", "role": "cto", "spawned_at": "ISO8601", "accounted": false}`
- Creates the file if it doesn't exist (init as `[]`)

### sync_budget.py
`~/code/clawd-teams/framework/sync_budget.py <project>`
- Reads `projects/<project>/runtime/session_registry.json`
- For each record where `accounted == false`:
  - Calls `session_cost(session_id)` from budget_utils.py
  - Calls `update_budget(budget_path, role, session_id, cost)`
  - Marks record `accounted: true`, adds `cost_usd` field
- Writes session_registry.json back with updated records

### Template sidecar
- Create `~/code/clawd-teams/projects/.template/runtime/session_registry.json` containing `[]`

## Acceptance criteria
- `python3 framework/record_session.py clawd-teams-dev planner <uuid>` appends record to session_registry.json
- `python3 framework/sync_budget.py clawd-teams-dev` updates budget.json spend_usd correctly
- Re-running sync_budget doesn't double-count (accounted:true guard)
- budget.json `total_spend_usd` equals sum of all `spend_usd` values after sync

## Files
- `~/code/clawd-teams/framework/record_session.py`
- `~/code/clawd-teams/framework/sync_budget.py`
- `~/code/clawd-teams/projects/.template/runtime/session_registry.json`

## Complexity: LOW
