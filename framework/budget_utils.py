#!/usr/bin/env python3
"""
budget_utils.py — Shared spend tracking utilities for clawd-teams.

Functions:
    session_cost(session_id) -> float   Read USD cost from a JSONL session file
    update_budget(budget_path, role, session_id, cost) -> None  Atomically update budget.json

CLI:
    python3 budget_utils.py <session_id>
"""

import json
import os
import sys
import tempfile
from pathlib import Path

SESSIONS_DIR = Path.home() / ".openclaw/agents/main/sessions"


def session_cost(session_id: str) -> float:
    """
    Read the total USD cost for a session from its JSONL file.
    Sums cost.total from every event that has it (message.usage.cost.total).
    Returns 0.0 if file not found or no cost data present.
    """
    path = SESSIONS_DIR / f"{session_id}.jsonl"
    if not path.exists():
        # Try partial match (first 8 chars)
        matches = list(SESSIONS_DIR.glob(f"{session_id}*.jsonl"))
        if not matches:
            return 0.0
        path = matches[0]

    total = 0.0
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                # Cost can be nested in message.usage.cost.total
                msg = d.get("message", d)
                usage = msg.get("usage", {})
                cost = usage.get("cost", {})
                if isinstance(cost, dict):
                    t = cost.get("total", 0.0)
                    if t:
                        total += float(t)
            except (json.JSONDecodeError, TypeError, ValueError):
                pass
    return total


def update_budget(budget_path: str, role: str, session_id: str, cost: float) -> None:
    """
    Atomically update budget.json with cost for a role's session.
    Idempotent: skips if session_id already in seen_sessions.
    """
    budget_path = Path(budget_path)
    if not budget_path.exists():
        return

    with open(budget_path) as f:
        data = json.load(f)

    # Idempotency guard
    seen = data.setdefault("seen_sessions", [])
    if session_id in seen:
        return

    # Update spend
    spend = data.setdefault("spend_usd", {})
    spend[role] = round(spend.get(role, 0.0) + cost, 6)

    data["total_spend_usd"] = round(sum(spend.values()), 6)

    # Increment call count
    calls = data.setdefault("calls", {})
    calls[role] = calls.get(role, 0) + 1

    # Mark seen
    seen.append(session_id)

    # Atomic write
    tmp = budget_path.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    os.rename(tmp, budget_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <session_id>")
        sys.exit(1)

    sid = sys.argv[1]
    cost = session_cost(sid)
    print(f"${cost:.4f}")
