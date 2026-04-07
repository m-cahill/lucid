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

### Run B — closeout docs (summary / audit / `M12_run1` first pass)

| Field | Value |
|-------|--------|
| Run ID | **24107886329** |
| Workflow run URL | https://github.com/m-cahill/lucid/actions/runs/24107886329 |
| Head commit | `72a6ca213813ad6bfc5c79fef5cb594550364b90` |
| Conclusion | **success** |

### Run C — alignment pass (CI ref churn)

| Field | Value |
|-------|--------|
| Run ID | **24107986535** |
| Workflow run URL | https://github.com/m-cahill/lucid/actions/runs/24107986535 |
| Head commit | `57dd8a6215856d7fbbe61febc6b0da6f7d74b5ee` |
| Conclusion | **success** |

### Run D — final PR head (authoritative green before merge)

| Field | Value |
|-------|--------|
| Run ID | **24108099234** |
| Workflow run URL | https://github.com/m-cahill/lucid/actions/runs/24108099234 |
| Head commit | `513d230c0660f1e24b5995abf610e21116048a0f` |
| Conclusion | **success** |

**Authoritative CI for M12 merge:** Run **D** — last green `pull_request` workflow on the PR branch before merge to `main`.

## Merge to `main`

| Field | Value |
|-------|--------|
| Merge commit SHA | `6211b0c9b0197ab89ac5ddcc5350f3bc4d3840ed` |
| Merge method | merge commit (`Merge branch 'm12-final-linkage' (M12 closeout)`) |
| PR | https://github.com/m-cahill/lucid/pull/13 |

## Notes

- M11 default ingest merges `docs/milestones/M09/artifacts/m09_kaggle_leaderboard_export.csv` with `docs/milestones/M11/artifacts/michael1232_lucid-kaggle-community-benchmarks_leaderboard.csv`, regenerating the committed response-surface artifacts so P12 rows are no longer `export_missing`.
