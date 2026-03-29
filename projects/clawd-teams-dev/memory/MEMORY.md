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

## Current roadmap priority
1. Wire up real USD spend tracking in budget.json files (currently zeros)
2. Health checks: detect stale executives, budget overruns
3. Improve EXECUTIVE_TEMPLATE.md based on real-world learnings
4. Make worker_contract.md executable (Python/shell base classes)

## Key rules
- Framework improvements must not break existing projects
- Test new CLI commands before committing
- Keep it simple — over-engineering is the main risk
- CEOs should use memory/ to track learnings across cycles

## Budget
- CEO: Opus, $0.50/day
- CTO: Codex, 10 tasks/day
