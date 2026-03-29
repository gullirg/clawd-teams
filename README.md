# clawd-teams

A portable multi-agent team framework for autonomous project execution.

## Concept

```
Gulli
  └─► Clawd (meta-orchestrator)
        ├─► Executive: news-digest
        ├─► Executive: trading-agent
        └─► Executive: <any project>
              ├── Dev workers (Claude Code / Codex)
              ├── Research workers (isolated sub-agents)
              └── Ops workers (cron, monitoring, delivery)
```

You only ever talk to Clawd. Clawd routes to project executives. Executives manage their teams and report back.

## Structure

```
clawd-teams/
├── framework/
│   ├── EXECUTIVE_TEMPLATE.md   # Bootstrap briefing for any new executive
│   └── worker_contract.md      # Standard task/report interface
├── projects/
│   ├── .template/              # Copy this to start a new project
│   └── news-digest/            # First live project
└── registry.json               # Clawd's routing table
```

## Adding a new project

1. `cp -r projects/.template projects/<name>`
2. Fill in `projects/<name>/EXECUTIVE.md`
3. Fill in `projects/<name>/config.json`
4. Add entry to `registry.json`
5. Clawd spins up a persistent executive session

## CLI

Use the bundled CLI to scaffold and inspect projects:

```bash
bin/clawd-teams help
bin/clawd-teams list
bin/clawd-teams new trading-bot
```

`clawd-teams help` prints:

```text
clawd-teams — multi-agent project framework

Commands:
  new <project>   Scaffold a new project from template
  help            Show this help
  list            List projects in registry.json

Examples:
  clawd-teams new trading-bot
  clawd-teams new news-digest-v2
```

## Framework principles

- Executives are long-lived OpenClaw sessions with project context
- Workers are spawned on-demand (ACP sessions, cron jobs)
- All state is files — no databases required at framework level
- Git is the transport layer for remote execution
- Clawd is the single interface — humans never talk to workers directly
