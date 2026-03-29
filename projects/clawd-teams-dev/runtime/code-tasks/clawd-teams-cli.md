Implement a `clawd-teams` CLI for the clawd-teams framework.

## Repository
Working directory: ~/code/clawd-teams

## Task
Create a shell script at `bin/clawd-teams` that provides a `new <project>` command to scaffold new projects.

## Requirements

### `bin/clawd-teams new <project-name>`
1. Check that `projects/.template/` exists (abort with helpful error if not)
2. Check that `projects/<project-name>/` does NOT already exist (abort if it does)
3. Copy `projects/.template/` to `projects/<project-name>/`
4. In the new `projects/<project-name>/EXECUTIVE.md`, replace `{{PROJECT_NAME}}` with the project name
5. Create `projects/<project-name>/state.json` with this content:
```json
{
  "cycle": 0,
  "last_cycle": null,
  "current_goals": [],
  "task_queue": [],
  "completed_tasks": [],
  "last_updated": null
}
```
6. Create `projects/<project-name>/log.md` with:
```
# <project-name> — Event Log

## Created
- Project scaffolded by clawd-teams CLI
```
7. Create `projects/<project-name>/runtime/` directory
8. Update `registry.json` in the repo root — add a new entry for the project using Python:
```python
import json, sys
with open('registry.json') as f: data = json.load(f)
data['projects']['<name>'] = {'path': 'projects/<name>', 'status': 'new', 'created': '<today>'}
with open('registry.json', 'w') as f: json.dump(data, f, indent=2)
```
9. Print a success message showing next steps

### `bin/clawd-teams help` (and default/no-args)
Print usage:
```
clawd-teams — multi-agent project framework

Commands:
  new <project>   Scaffold a new project from template
  help            Show this help

Examples:
  clawd-teams new trading-bot
  clawd-teams new news-digest-v2
```

### `bin/clawd-teams list`
List all projects in registry.json with their status.

## Notes
- Make the script executable: `chmod +x bin/clawd-teams`
- Use `#!/usr/bin/env bash` shebang
- Use `set -e` for safety
- Use Python (not jq) for JSON operations — more portable
- Also update `README.md` to include a "CLI" section showing usage

## Final steps (after implementation)
git add -A && git commit -m "feat: add clawd-teams CLI with new/help/list subcommands"

When completely done, run:
openclaw system event --text "CTO done: clawd-teams CLI implemented" --mode now
