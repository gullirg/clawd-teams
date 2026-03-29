# CEO Memory — rekordbox-mcp

## What this project is
MCP server connecting Rekordbox 6 DJ library to Claude Code. Gulli's DJ library tool.
Repo: ~/code/rekordbox-mcp | GitHub: gullirg/rekordbox-mcp (private)

## Architecture (confirmed clean)
adapter → domain → service → mcp_tools layers. Clean separation, good tests.
Old `tools/` shim layer is legacy — to deprecate eventually.

## Enrichment findings (2026-03-29 full run)
- 1,470 tracks processed: 17% updated, 64% not_found, 19% no_matching_genre
- AcoustID: 0 recoveries → remove from default pipeline
- Claude cleanup: 225 recoveries → keep enabled
- `evaluate_enrichment_results.py` committed (ea0b172) — analyses batch data

## Current roadmap priority
1. Lock enrichment defaults (disable AcoustID)
2. Expand genre normalization map (282 no_matching_genre tracks have mapping opportunities)
3. Build manual review queue for unresolved tracks (cluster by playlist context)
4. Phase 3: app-owned data model design

## Rules
- NO breaking changes to services/ or adapters/ — sensitive paths
- Run tests after any Codex work: `python -m pytest tests/ -x -q`
- Commit to main, push — Gulli reviews via GitHub

## Budget
- CEO: Opus, $0.50/day cap
- CTO: Codex, 10 tasks/day
- Daily cycle scheduled — work through roadmap in order
