# Proposal: clawd-teams CLI

## Problem
Creating new clawd-teams projects requires manual copy+edit steps. A CLI command would make onboarding faster and less error-prone.

## Recommendation
Implement `bin/clawd-teams` as a bash script with a `new <project>` subcommand.

## Options Considered
1. **bash script** — zero deps, portable, simple (chosen)
2. **Node.js CLI** — more featureful but adds complexity
3. **Python** — good middle ground but less shell-native

## Implementation Plan
1. Create `bin/clawd-teams` executable shell script
2. `new <project>` subcommand:
   - Copies `projects/.template` → `projects/<name>`
   - Replaces `{{PROJECT_NAME}}` placeholder in EXECUTIVE.md
   - Creates minimal `state.json`, `log.md`, `config.json`
   - Adds entry to `registry.json` (use Python for JSON safety)
   - Prints next steps to stdout
3. Add `help` subcommand
4. README update with usage example

## Tradeoffs
- Shell: portable, fast, no install — but limited error handling
- Use Python one-liner for JSON to avoid jq dependency
