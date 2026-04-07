# M12 — Evidence surface notes (M11 alignment)

**Purpose:** Explain how M12 classifies M11-era files so judges and operators do not mix **closed M11 closeout** facts with **stale placeholders** or **local-only** files.

## Authority order (unchanged)

1. `docs/lucid.md`
2. `docs/milestones/M11/M11_run2.md` (when CI recovery context matters)
3. `docs/milestones/M11/M11_summary.md`
4. `docs/milestones/M11/M11_audit.md`
5. Machine-readable artifacts explicitly referenced by the ledger and ingest manifests

## Authoritative ingest and operator sources (committed)

| File | Role |
|------|------|
| `docs/milestones/M11/artifacts/michael1232_lucid-kaggle-community-benchmarks_leaderboard.csv` | Full-benchmark Kaggle leaderboard export; merged with M09 export in `ingest_m11_platform_exports.py` |
| `docs/milestones/M11/artifacts/lucid_m11_probe_p12_task_costs.csv` | Operator cost table for P12 (and P24 columns where present) |
| `docs/milestones/M11/artifacts/ci/M11_ci_failure_snippet_run24058104201.txt` | Snippet supporting M11 CI recovery narrative (`M11_run2.md`) |

## Local / non-canonical

| Item | Classification |
|------|------------------|
| `.cursor-ci-runs.json` (repo root, if present) | Local operator cache — **not** authoritative evidence |

## Duplicate path hygiene

If a legacy copy of `lucid_m11_probe_p12_task_costs.csv` remains outside `artifacts/` (for example after a move while a file handle was open), delete the stray copy once unlocked so only the `artifacts/` path remains.
