# M07 — CI / verification run log

**Milestone:** M07 — Unified benchmark pack normalization across families  
**Status:** **Closed** — PR #8 merged to `main` (`07e349ef7ff68cad79be3c41bb94839045fe18b3`)  
**Branch (historical):** `m07-unified-benchmark-pack-normalization` (deleted on remote after merge)  
**Local environment:** Windows 10, Python 3.11, repo root `c:\coding\kaggle\lucid`

---

## 1. Local verification (authoritative set)

All commands run from repository root; **exit code 0** for each (2026-03-31).

| Step | Command | Exit |
|------|---------|------|
| 1 | `python -m ruff check src tests scripts` | 0 |
| 2 | `python -m ruff format --check src tests scripts` | 0 |
| 3 | `python -m mypy src` | 0 |
| 4 | `python -m pytest` | 0 (92 passed, coverage ≥85% on `lucid`) |
| 5 | `python -m build --wheel` | 0 |
| 6 | `python scripts/verify_wheel_has_kaggle.py` | 0 |
| 7 | `python scripts/run_local_smoke.py` | 0 |
| 8 | `python scripts/generate_family1_core_m03_manifest.py --check` | 0 |
| 9 | `python scripts/generate_kaggle_notebook.py --check -o notebooks/lucid_kaggle_transport_text_adapter_m_01.ipynb` | 0 |
| 10 | `python scripts/generate_family1_m04_notebook.py --check -o notebooks/lucid_kaggle_family1_m04_analytics.ipynb` | 0 |
| 11 | `python scripts/generate_family2_core_m05_manifest.py --check` | 0 |
| 12 | `python scripts/run_family2_pack_smoke.py` | 0 |
| 13 | `python scripts/generate_family3_core_m06_manifest.py --check` | 0 |
| 14 | `python scripts/run_family3_pack_smoke.py` | 0 |
| 15 | `python scripts/generate_unified_core_m07_manifest.py --check` | 0 |
| 16 | `python scripts/run_unified_pack_smoke.py` | 0 |

**Note:** `python -m build --wheel` may print stderr lines from the isolated build backend (hatchling); the process still completed successfully (exit 0).

Copy-paste block (bash / PowerShell):

```bash
python -m ruff check src tests scripts
python -m ruff format --check src tests scripts
python -m mypy src
python -m pytest
python -m build --wheel
python scripts/verify_wheel_has_kaggle.py
python scripts/run_local_smoke.py
python scripts/generate_family1_core_m03_manifest.py --check
python scripts/generate_kaggle_notebook.py --check -o notebooks/lucid_kaggle_transport_text_adapter_m_01.ipynb
python scripts/generate_family1_m04_notebook.py --check -o notebooks/lucid_kaggle_family1_m04_analytics.ipynb
python scripts/generate_family2_core_m05_manifest.py --check
python scripts/run_family2_pack_smoke.py
python scripts/generate_family3_core_m06_manifest.py --check
python scripts/run_family3_pack_smoke.py
python scripts/generate_unified_core_m07_manifest.py --check
python scripts/run_unified_pack_smoke.py
```

---

## 2. GitHub Actions

### 2.1 Pull request CI (authoritative)

| Field | Value |
|-------|--------|
| **PR URL** | https://github.com/m-cahill/lucid/pull/8 |
| **PR state** | **MERGED** |
| **PR head SHA** | `b5109f7de6f87039f3e671dad8c378fe64e05784` |
| **Workflow name** | `CI` (`.github/workflows/ci.yml`) |
| **Run ID** | `23831550017` |
| **Run URL** | https://github.com/m-cahill/lucid/actions/runs/23831550017 |
| **Conclusion** | **success** |

### 2.2 Post-merge `main` CI

| Field | Value |
|-------|--------|
| **Merge SHA** | `07e349ef7ff68cad79be3c41bb94839045fe18b3` |
| **Run ID** | `23831565243` |
| **Run URL** | https://github.com/m-cahill/lucid/actions/runs/23831565243 |
| **Conclusion** | **success** |

---

## 3. Workflow analysis (per `docs/prompts/workflowprompt.md`)

**Workflow identity:** GitHub Actions workflow **`CI`**, job **`lint-test`**, trigger **`pull_request`** / **`push`** to `main` after merge.

**Change context:** M07 adds unified pack code, manifest `--check`, tests, and docs; benchmark **1.1.0** unchanged; no scorer/parser contract edits.

**Baseline:** `main` at merge-parent prior to M07 PR.

### Step 1 — Workflow inventory

| Job / Check | Required? | Purpose | Pass/Fail | Notes |
|-------------|-----------|---------|-----------|--------|
| Checkout | Yes | Source tree | Pass | |
| Setup Python 3.11 | Yes | Toolchain | Pass | |
| pip install `-e ".[dev]"` | Yes | Dev deps | Pass | |
| Ruff check | Yes | Lint | Pass | |
| Ruff format --check | Yes | Format | Pass | |
| Mypy | Yes | Types | Pass | |
| Pytest + coverage | Yes | Tests + ≥85% `lucid` | Pass | |
| Build wheel + verify_kaggle | Yes | Package sanity | Pass | |
| Notebook `--check` (M01, M04) | Yes | Generated notebooks | Pass | |
| Family 1–3 manifest `--check` | Yes | Canonical family manifests | Pass | |
| **Unified M07 manifest `--check`** | Yes | **Canonical unified manifest** | Pass | **New in M07** |

No `continue-on-error` on required steps.

### Step 2 — Signal integrity

- **Tests:** Full `pytest` including `tests/test_unified_core_m07_pack.py`; integration coverage via existing suites.
- **Coverage:** Line coverage gate on `lucid` package (unchanged policy).
- **Static:** Ruff + mypy unchanged in intent.
- **New signal:** Unified manifest regeneration must match committed JSON (determinism).

### Step 6 — Verdict

> **Verdict:** PR run **`23831550017`** and post-merge **`main`** run **`23831565243`** both **succeeded**. Required jobs ran with **no** `continue-on-error` bypass. The change set is **dataset packaging + CI guard** only; signals match declared intent.

**✅ Merge approved** — executed (PR #8 merged).

### Step 7 — Next actions

- **M08:** Open defensibility / QA work from current `main` when prioritized (`docs/milestones/M08/M08_plan.md`).

---

## 4. Notes

- If the verification command set changes in a later commit, document the delta here per `M07_plan.md`.
- **M07** does not claim Kaggle platform proof; evidence class remains **local + CI** only.
