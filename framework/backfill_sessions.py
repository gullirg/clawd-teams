#!/usr/bin/env python3
"""
backfill_sessions.py — Seed session_registry.json for existing projects.

Seeds known historical session → role mappings from spend-tracker.py,
then syncs budget.json for each project.

Usage:
    python3 framework/backfill_sessions.py
"""

import sys
from pathlib import Path

FRAMEWORK_DIR = Path(__file__).parent
PROJECTS_DIR = FRAMEWORK_DIR.parent / "projects"

sys.path.insert(0, str(FRAMEWORK_DIR))
from record_session import record_session
from sync_budget import sync_budget

# Known session → (project, role) mappings from spend-tracker.py project_sessions dict
# Session IDs are 8-char prefixes; record_session handles prefix matching
KNOWN_SESSIONS = {
    # rekordbox-mcp — Codex/subagent CTO sessions
    "rekordbox-mcp": [
        ("5f3d2a07", "cto"),
        ("afa0400b", "cto"),
        ("fff0518e", "cto"),
        ("0396f584", "cto"),
    ],
    # clawd-voice — Codex/subagent CTO sessions
    "clawd-voice": [
        ("33f55010", "cto"),
        ("8efa559e", "cto"),
        ("9a9191c7", "cto"),
        ("c535c18c", "cto"),
    ],
    # clawd-teams-dev — CTO session
    "clawd-teams-dev": [
        ("1709626", "cto"),
    ],
}


def backfill():
    for project, sessions in KNOWN_SESSIONS.items():
        project_dir = PROJECTS_DIR / project
        if not project_dir.exists():
            print(f"Skipping {project} — directory not found")
            continue

        runtime_dir = project_dir / "runtime"
        runtime_dir.mkdir(exist_ok=True)

        print(f"\nBackfilling {project}...")
        for session_id, role in sessions:
            try:
                record_session(project, role, session_id)
            except Exception as e:
                print(f"  Warning: could not record {session_id[:8]}: {e}")

        try:
            sync_budget(project)
        except Exception as e:
            print(f"  Warning: sync_budget failed for {project}: {e}")

    print("\nBackfill complete.")


if __name__ == "__main__":
    backfill()
