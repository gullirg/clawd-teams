# CEO Memory — clawd-teams-dev

## What this project is
Self-improving team that works on the clawd-teams framework itself.
The framework manages all of Gulli's autonomous agent projects.
Repo: ~/code/clawd-teams | GitHub: gullirg/clawd-teams

## Framework architecture
- Executives are persistent OpenClaw sessions per project
- Workers spawned on-demand (Codex for code, sub-agents for research)
- Routing table: ~/.openclaw/workspace/projects.json
- Registry: ~/code/clawd-teams/registry.json

## Active projects in the framework
1. clawd-teams-dev (this project — self-improvement)
2. rekordbox-mcp (DJ library MCP server)
3. news-digest (daily news to Telegram at 08:30)
4. clawd-voice (voice interface for Clawd)

## Completed today (2026-03-29)
- bin/clawd-teams CLI: `new`, `list`, `help` subcommands
- clawd-teams list shows project status, mode, last cycle

## Completed
- bin/clawd-teams CLI: `new`, `list`, `help` subcommands
- Real USD spend tracking: framework/budget_utils.py + session_registry sidecar system
  - session_cost() reads cost.total from JSONL (pre-computed, no token math needed)
  - record_session.py + sync_budget.py + backfill_sessions.py
  - bin/spending-report auto-syncs before displaying
  - Commit: 531c43c

## Current roadmap priority
1. Health checks: detect stale executives, budget overruns, failed workers
2. Improve EXECUTIVE_TEMPLATE.md based on real-world learnings
3. Add CONTRIBUTING.md and CHANGELOG.md
4. Make worker_contract.md executable (Python/shell base classes)

## Lessons learned
- JSONL cost field: message.usage.cost.total — already computed by OpenClaw
- When CTO (Claude Code) hits API limits, CEO can implement straightforward code tasks directly
- Planner is valuable for task decomposition even when CTO can't run

## Key rules
- Framework improvements must not break existing projects
- Test new CLI commands before committing
- Keep it simple — over-engineering is the main risk
- CEOs should use memory/ to track learnings across cycles

## Budget
- CEO: Opus, $0.50/day
- CTO: Codex, 10 tasks/day
