# M12 — CI / verification run 1

**Branch:** `m12-final-linkage`  
**Scope:** M12 linkage generator, M11 ingest path update (dual exports), evidence file moves, CI step for `generate_m12_submission_linkage.py --check`.

## Local verification (2026-04-07)

- `python -m ruff check src tests scripts` — pass  
- `python -m ruff format --check src tests scripts` — pass  
- `python -m mypy src` — pass  
- `python -m pytest` — pass (coverage ≥ 85%)  
- All generator `--check` commands in `.github/workflows/ci.yml`, including `python scripts/generate_m12_submission_linkage.py --check` — pass  

## GitHub Actions

_Record the authoritative green workflow run URL and commit SHA for the closing M12 merge after the PR is pushed._

| Field | Value |
|-------|--------|
| Workflow run URL | _pending — fill after CI on merge tip_ |
| Commit SHA | _pending_ |
| Verdict | _pending_ |

## Notes

- M11 default ingest now merges `docs/milestones/M09/artifacts/m09_kaggle_leaderboard_export.csv` with `docs/milestones/M11/artifacts/michael1232_lucid-kaggle-community-benchmarks_leaderboard.csv`, regenerating the committed response-surface artifacts so P12 rows are no longer `export_missing`.
