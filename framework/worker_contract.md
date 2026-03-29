# Worker Contract

All workers in the clawd-teams framework communicate using this standard interface.

## Task Request

When an executive spawns a worker, it passes a task in this shape:

```json
{
  "task_id": "unique-id",
  "type": "research | dev | ops | analysis",
  "project": "project-name",
  "instructions": "Clear, specific instructions for this task",
  "context": {
    "relevant_files": [],
    "relevant_state": {},
    "deadline": null
  },
  "report_back": "How and where to deliver results (file path, session, etc.)"
}
```

## Task Result

Workers always produce a result in this shape:

```json
{
  "task_id": "unique-id",
  "status": "ok | error | partial | blocked",
  "summary": "One paragraph human-readable summary",
  "artifacts": ["list of files created or modified"],
  "blockers": ["list of things preventing completion, if any"],
  "next_steps": ["suggested follow-up actions"]
}
```

## Worker Types

### Research Worker
- Input: topic, depth, output format
- Tools: web_search, web_fetch, read
- Output: markdown report written to a file

### Dev Worker
- Input: task description, repo path, constraints
- Tools: ACP coding session (Claude Code / Codex)
- Output: code changes committed to git

### Ops Worker
- Input: script/command to run, delivery target
- Tools: exec, cron, sessions_send
- Output: execution result + delivery confirmation

### Analysis Worker
- Input: data files or queries, analysis goal
- Tools: exec (Python/SQL), read, write
- Output: analysis report + structured findings

## Communication Pattern

```
Executive
  │
  ├── sessions_spawn(task) → Worker
  │         │
  │         └── works autonomously
  │                   │
  │                   └── writes result to shared state file
  │                             │
  └── reads result, updates state.json, reports to Clawd
```

## State File Convention

Each project maintains `state.json`:

```json
{
  "active_workers": [
    {"task_id": "x", "type": "research", "spawned_at": "ISO", "status": "running"}
  ],
  "completed_tasks": [...],
  "pending_tasks": [...],
  "last_updated": "ISO timestamp"
}
```
