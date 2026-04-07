# M12 — CI / verification run 1

**Branch:** `m12-final-linkage`  
**Scope:** M12 linkage generator, M11 ingest path update (dual exports), evidence file moves, CI step for `generate_m12_submission_linkage.py --check`.

## Local verification (2026-04-07)

- `python -m ruff check src tests scripts` — pass  
- `python -m ruff format --check src tests scripts` — pass  
- `python -m mypy src` — pass  
- `python -m pytest` — pass (coverage ≥ 85%)  
- All generator `--check` commands in `.github/workflows/ci.yml`, including `python scripts/generate_m12_submission_linkage.py --check` — pass  

## GitHub Actions (PR #13)

**Pull request:** https://github.com/m-cahill/lucid/pull/13  

### Run A — initial validation (implementation + M13 seed)

| Field | Value |
|-------|--------|
| Run ID | **24107725335** |
| Workflow run URL | https://github.com/m-cahill/lucid/actions/runs/24107725335 |
| Head commit | `532a57c0c82f95821fa3e79972d771fca45a8753` |
| Conclusion | **success** |

### Run B — closing tip (authoritative green after closeout docs)

| Field | Value |
|-------|--------|
| Run ID | **24107886329** |
| Workflow run URL | https://github.com/m-cahill/lucid/actions/runs/24107886329 |
| Head commit | `72a6ca213813ad6bfc5c79fef5cb594550364b90` |
| Conclusion | **success** |

**Authoritative CI for M12 merge:** Run **B** (same tree as merge after PR merge).

## Merge to `main`

_Updated after merge — see table below._

| Field | Value |
|-------|--------|
| Merge commit SHA | _filled after merge_ |
| Merge method | _filled after merge_ |

## Notes

- M11 default ingest merges `docs/milestones/M09/artifacts/m09_kaggle_leaderboard_export.csv` with `docs/milestones/M11/artifacts/michael1232_lucid-kaggle-community-benchmarks_leaderboard.csv`, regenerating the committed response-surface artifacts so P12 rows are no longer `export_missing`.
