#!/usr/bin/env python3
"""
record_session.py — Record a worker session for spend attribution.

Usage:
    python3 framework/record_session.py <project> <role> <session_id>

Example:
    python3 framework/record_session.py clawd-teams-dev cto abc123-def456
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECTS_DIR = Path(__file__).parent.parent / "projects"


def record_session(project: str, role: str, session_id: str) -> None:
    registry_path = PROJECTS_DIR / project / "runtime" / "session_registry.json"
    registry_path.parent.mkdir(parents=True, exist_ok=True)

    # Load existing registry
    if registry_path.exists():
        with open(registry_path) as f:
            registry = json.load(f)
    else:
        registry = []

    # Idempotency check
    existing_ids = {r["session_id"] for r in registry}
    if session_id in existing_ids:
        return  # already recorded

    record = {
        "session_id": session_id,
        "role": role,
        "spawned_at": datetime.now(timezone.utc).isoformat(),
        "accounted": False,
    }
    registry.append(record)

    tmp = registry_path.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(registry, f, indent=2)
    os.rename(tmp, registry_path)
    print(f"Recorded session {session_id[:8]}... for {project}/{role}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(f"Usage: python3 {sys.argv[0]} <project> <role> <session_id>")
        sys.exit(1)

    record_session(sys.argv[1], sys.argv[2], sys.argv[3])
