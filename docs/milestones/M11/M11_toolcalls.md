# M11 — Tool call log

**Milestone:** M11 — Hosted-model probe ladder + response surface  
**Status:** Active — repo + ingest shipped; Kaggle probe runs pending.

---

| Timestamp (UTC) | Tool | Purpose | Files / target | Status |
|-----------------|------|---------|----------------|--------|
| 2026-04-06 | — | Stub seeded at M10 closeout | this file | seeded |
| 2026-04-06 | implementation | M11 Phase 1: `m11_probe_panels.py`, artifacts, notebooks, stubs, CI, ledger | `src/lucid/kaggle/m11_probe_panels.py`, `scripts/generate_m11_*.py`, `docs/lucid.md`, `docs/LUCID_COMPETITION_ALIGNMENT.md`, `.github/workflows/ci.yml` | complete |
| 2026-04-06 | implementation | M11 Phase 3: full ingest, tables, figures; pin `13137d9`; `M11_run1/summary/audit` | `scripts/m11_ingest_common.py`, `ingest_m11_platform_exports.py`, `generate_m11_tables.py`, `generate_m11_figures.py`, `docs/milestones/M11/artifacts/` | complete |
| 2026-04-06 | implementation | Publication policy hardening: manifest generator, runbook retry rules, ledger policy section | `scripts/generate_m11_notebook_release_manifest.py`, `docs/lucid.md`, `M11_KAGGLE_RUNBOOK.md`, `M11_toolcalls.md`, `.github/workflows/ci.yml` | complete |
| 2026-04-06 | implementation | Kaggle pin + packaging: wheel guard for `m11_probe_panels`, git-HEAD verify, import tests, preflight cell | `scripts/verify_wheel_has_kaggle.py`, `scripts/verify_m11_git_has_module.py`, `tests/test_m11_package_visibility.py`, `generate_m11_kaggle_notebooks.py`, `pyproject.toml`, CI | complete |
| 2026-04-06 | incident | Kaggle preflight `m11_probe_panels` MISSING: pin `13137d907e938c6ed36c2b17eb0c4347f2d3943c` has no `m11_probe_panels.py` in tree; GitHub ZIP = committed tree only, not local untracked files | outcome `run_error`, reason `bad_pin_commit_missing_m11_module` | resolved by two-commit workflow (see `M11_run1.md`) |

---

## Operator note template (copy per Kaggle upload / run)

```text
### Kaggle run: <task_name> — <date UTC>

- Notebook pin SHA: <40-char-sha>
- Generator --check: PASS / FAIL
- Notebook SHA-256: <from m11_notebook_release_manifest.json>
- Kaggle notebook URL: <url or "not yet published">
- Kaggle notebook version: <version number or "initial">
- Upload type: fresh_upload / rerun / retry_after_platform_failure
- Outcome: completed / platform_limited / run_error / ...
- Failure reason (if any): <reason code, e.g. platform_dns_failure>
- Leaderboard CSV exported: yes / no
- Notes: <free text>
```
