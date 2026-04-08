# M13 — Run 1 (public URL verification — deferred)

**Branch:** `m13-contingency-buffer`  
**Scope:** Truthful recording of Kaggle benchmark / task **public URL verification** posture per `docs/milestones/M12/M12_SUBMISSION_RUNBOOK.md`. **No** linkage regeneration; **no** fabricated URLs.

## M12 closure reference (unchanged)

| Field | Value |
|-------|--------|
| Authoritative green CI (PR #13) | Run ID **24108099234** — https://github.com/m-cahill/lucid/actions/runs/24108099234 |
| Final PR head | `513d230c0660f1e24b5995abf610e21116048a0f` |
| Merge to `main` | `6211b0c9b0197ab89ac5ddcc5350f3bc4d3840ed` |

## Verification attempt

| Item | Result |
|------|--------|
| Owner-view Kaggle UI (benchmark `michael1232/lucid-kaggle-community-benchmarks`, six attached tasks) | **Not performed** in this execution context — requires human operator with Kaggle owner access |
| Logged-out / incognito public visibility check | **Not performed** here |

## Current committed truth (unchanged)

Per `docs/milestones/M12/artifacts/m12_linkage_sources.json` and `m12_public_links.json`:

- `publication_status`: **`owner_visible_unverified`**
- `kaggle_benchmark_url`: **`null`**
- Per-task `task_url`: **`null`** for all six tasks (`lucid_main_task`, `lucid_family1_m04_task`, `lucid_m09_mature_evidence_task`, `lucid_m11_probe_p12_task`, `lucid_m11_probe_p24_task`, `lucid_m11_probe_p48_task`)

**Artifacts not modified:** `m12_linkage_sources.json`, `m12_submission_linkage.json`, `m12_submission_linkage.md`, `m12_public_links.json`. **No** `python scripts/generate_m12_submission_linkage.py --write` run.

## Working tree hygiene (this pass)

- **Notebooks:** Local modifications under `notebooks/` were **discarded** (`git restore`) so canonical generated notebooks match `main` / M12 closeout.
- **Stray duplicate CSV:** A duplicate untracked copy at `docs/milestones/M11/lucid_m11_probe_p12_task_costs.csv` (outside `artifacts/`) should be **deleted**; canonical path remains `docs/milestones/M11/artifacts/lucid_m11_probe_p12_task_costs.csv`. If deletion fails (file lock), close the file in the editor and remove it, then confirm `git status` is clean.

## Next step (when owner-view is available)

1. In Kaggle (owner account), confirm benchmark page URL and public visibility; confirm each task’s canonical URL.
2. If and only if verification supports it, update `m12_linkage_sources.json`, run `python scripts/generate_m12_submission_linkage.py --write` then `--check`, update `docs/lucid.md` blocker table, and record a new M13 run file.

## Local verification (post-doc commit)

Run the repo quality gates before push (see `.github/workflows/ci.yml` and `M12_SUBMISSION_RUNBOOK.md` §2). This pass changes **documentation only**; expected outcome: same as baseline `main` for code and generators.
