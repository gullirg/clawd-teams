# Task 01 — Create framework/budget_utils.py

## What to build
Standalone Python utility at `~/code/clawd-teams/framework/budget_utils.py` with:

1. `session_cost(session_id: str) -> float`
   - Reads `~/.openclaw/agents/main/sessions/<session_id>.jsonl`
   - Sums `cost.total` from every event that has it (already computed, no token maths needed)
   - Returns total float USD

2. `update_budget(budget_path: str, role: str, session_id: str, cost: float) -> None`
   - Atomically reads budget.json
   - Adds cost to `spend_usd[role]` and `total_spend_usd`
   - Increments `calls[role]`
   - Adds session_id to a `seen_sessions` list (idempotency guard — skip if already present)
   - Writes back atomically (write to temp, rename)

3. CLI: `python3 budget_utils.py <session_id>` — prints cost in $X.XXXX format

## Acceptance criteria
- `python3 framework/budget_utils.py <valid-session-id>` prints a non-zero dollar amount
- `update_budget()` correctly increments `spend_usd[role]` and `total_spend_usd`
- Re-running with same session_id doesn't double-count
- Module importable: `from budget_utils import session_cost, update_budget`

## File
`~/code/clawd-teams/framework/budget_utils.py`

## Complexity: LOW
