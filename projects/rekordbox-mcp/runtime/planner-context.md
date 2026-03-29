# Planner Context — Cycle 1

## Project: rekordbox-mcp
An MCP server for Rekordbox 6 library management, transitioning to a stable library engine.

## Current State
- Architecture: adapters/ → domain/ → services/ → mcp_tools/ (thin MCP layer)
- Enrichment pipeline: MusicBrainz → Claude cleanup → optional AcoustID/Discogs/Last.fm/Spotify
- Enrichment rerun in progress: 510 tracks processed, 51 batches completed
- **venv is MISSING** — `.venv/` doesn't exist, tests can't run

## Enrichment Stats (latest rerun)
- Processed: 510 tracks
- Updated: 154 (30%)
- Skipped: 166 (no_matching_genre)
- Not found: 182 (36%)
- API errors: 8
- Claude cleanup recoveries: 60
- AcoustID recoveries: 0 (evidence suggests removing from default)

## Roadmap Phases
### Phase 1: Stabilize The Current Engine (CURRENT)
- [ ] finish the current enrichment rerun
- [ ] evaluate the final source-tier and recovery-layer breakdown
- [ ] decide the default enrichment pipeline
- [ ] keep or remove AcoustID from the default path based on evidence
- [ ] commit the current reporting and analysis scripts as a new baseline

### Phase 2: Improve Review Workflows
- [ ] expand unresolved-track reviewer reports
- [ ] improve clustering and playlist-context reports
- [ ] create efficient manual review queues

### Phase 3-10: Future (app DB, FastAPI, web UI, Spotify import, etc.)

## Current Priority Order (from ROADMAP.md)
1. finish and evaluate the improved enrichment rerun
2. lock the enrichment defaults
3. commit the current reporting workflow
4. improve reviewer tooling
5. begin app DB design

## Scripts Available
- `scripts/batch_enrich_dry_run.py` — runs enrichment batches
- `scripts/build_unresolved_knowledge_tree.py` — builds knowledge tree
- `scripts/build_unresolved_review_report.py` — builds review report

## Reports Generated
- `reports/unresolved-knowledge-tree.json` (133KB)
- `reports/unresolved-review-report.json` (215KB)
- `reports/unresolved-by-playlist-context.json` (119KB)

## Issue: venv missing
The `.venv/` directory doesn't exist. This blocks:
- Running tests
- Running batch scripts properly
- Development workflow

## Your Task
Pick **ONE** concrete task that:
1. Can be completed in a single Codex session
2. Is valuable for Phase 1 or Phase 2
3. Doesn't require breaking changes to services/ or adapters/
4. Preferably additive (new files, new tests)

Consider:
- Should we first fix the venv setup?
- Should we add a script to evaluate enrichment results and recommend defaults?
- Should we add tests for the reporting scripts?
- Should we enhance the review report format?

Output format:
```
TASK: <one-line description>
RATIONALE: <why this is the highest value>
SCOPE: <specific files/areas to touch>
SUCCESS CRITERIA: <how to verify it's done>
```
