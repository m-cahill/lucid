# M09 Plan — Expanded Kaggle evidence on the mature benchmark

**Project:** LUCID  
**Milestone:** M09  
**Title:** Expanded Kaggle evidence on the mature benchmark  
**Primary judged axis:** **Novelty / insights / discriminatory power**  
**Benchmark version target:** **1.1.0** unless a genuine semantic defect is discovered and handled through change control  
**Branch name:** `m09-kaggle-evidence`

## Goal

Produce the first **authoritative Kaggle platform evidence** on the **mature, post-M08 benchmark surface**, using a deterministic **72-episode** evaluation panel: **24 Family 1** (exact M04 decision rows) + **24 Family 2** + **24 Family 3**, layered on `unified_core_m07_v1` without pack expansion.

## Phase B (repo) — complete

- **Panel:** `src/lucid/kaggle/m09_evidence_panel.py` — `M09_PANEL_ID` = `m09_mature_evidence_v1`, selector version `1.0.0`.
- **Artifact:** `docs/milestones/M09/artifacts/m09_model_panel.json` — `scripts/generate_m09_panel_artifact.py` (`--write` / `--check`; CI: `--check`).
- **Notebook:** `scripts/generate_m09_kaggle_notebook.py` → `notebooks/lucid_kaggle_m09_mature_evidence.ipynb`; task **`lucid_m09_mature_evidence_task`**.
- **Tests:** `tests/test_m09_evidence_panel.py`.
- **CI:** Panel + notebook `--check` in `.github/workflows/ci.yml`.

## Phase C–E — pending (platform + closeout)

Kaggle upload/run, hosted-model CSV exports, full ledger updates once scores exist. Handoff: **`M09_KAGGLE_RUNBOOK.md`**.

**Current repo state:** Phase B complete; **`m09_kaggle_run_manifest.md`** documents that **no platform run** is recorded yet; CSVs are header-only. **Do not** merge claims of full M09 closeout until real Kaggle evidence is committed.

## Verification (local / CI)

```bash
python scripts/generate_unified_core_m07_manifest.py --check
python scripts/run_unified_defensibility_audit.py --check
python scripts/run_unified_pack_smoke.py
pytest
python scripts/generate_m09_panel_artifact.py --check
python scripts/generate_m09_kaggle_notebook.py --check -o notebooks/lucid_kaggle_m09_mature_evidence.ipynb
```

## Authority

`docs/LUCID_MOONSHOT.md`, `docs/contracts/`, `docs/lucid.md`, `src/lucid/`.
