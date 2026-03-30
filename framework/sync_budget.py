#!/usr/bin/env python3
"""
sync_budget.py — Sync unaccounted sessions into budget.json.

Usage:
    python3 framework/sync_budget.py <project>

Example:
    python3 framework/sync_budget.py clawd-teams-dev
"""

import json
import os
import sys
from pathlib import Path

FRAMEWORK_DIR = Path(__file__).parent
PROJECTS_DIR = FRAMEWORK_DIR.parent / "projects"

sys.path.insert(0, str(FRAMEWORK_DIR))
from budget_utils import session_cost, update_budget


def sync_budget(project: str) -> None:
    registry_path = PROJECTS_DIR / project / "runtime" / "session_registry.json"
    budget_path = PROJECTS_DIR / project / "runtime" / "budget.json"

    if not registry_path.exists():
        print(f"No session_registry.json for {project} — skipping")
        return

    if not budget_path.exists():
        print(f"No budget.json for {project} — skipping")
        return

    with open(registry_path) as f:
        registry = json.load(f)

    total_synced = 0
    total_cost = 0.0

    for record in registry:
        if record.get("accounted"):
            continue

        sid = record["session_id"]
        role = record["role"]
        cost = session_cost(sid)

        update_budget(str(budget_path), role, sid, cost)
        record["accounted"] = True
        record["cost_usd"] = round(cost, 6)

        total_synced += 1
        total_cost += cost

    # Write back updated registry
    tmp = registry_path.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(registry, f, indent=2)
    os.rename(tmp, registry_path)

    if total_synced > 0:
        print(f"Synced {total_synced} sessions for {project}: ${total_cost:.4f}")
    else:
        print(f"Nothing to sync for {project}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <project>")
        sys.exit(1)

    sync_budget(sys.argv[1])
