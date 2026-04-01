# M05 — Verification and CI evidence

**Milestone:** M05 — Family 2 core pack (`contradiction_clarification_v1`)  
**Branch:** `m05-family-2-contradiction-clarification`  
**Environment (local):** Windows, Python 3.11  

---

## 1. Authoritative local verification (2026-04-01)

All commands completed with **exit code 0**.

| Command | Outcome |
|---------|---------|
| `python -m ruff check src tests scripts` | All checks passed |
| `python -m ruff format --check src tests scripts` | 46 files already formatted |
| `python -m mypy src` | Success: no issues in 23 source files |
| `python -m pytest` | 62 passed; coverage total **91.40%** (threshold 85%) |
| `python -m build --wheel` | Built `lucid_benchmark-0.1.0-py3-none-any.whl` |
| `python scripts/verify_wheel_has_kaggle.py` | OK: `lucid/kaggle/episode_llm.py` present in wheel |
| `python scripts/run_local_smoke.py` | `LUCID_SCORE_EPISODE=1.000000` |
| `python scripts/generate_family1_core_m03_manifest.py --check` | ok (manifest matches) |
| `python scripts/generate_kaggle_notebook.py --check -o notebooks/lucid_kaggle_transport_text_adapter_m_01.ipynb` | OK (matches generator) |
| `python scripts/generate_family1_m04_notebook.py --check -o notebooks/lucid_kaggle_family1_m04_analytics.ipynb` | OK (matches generator) |
| `python scripts/generate_family2_core_m05_manifest.py --check` | ok (manifest matches) |
| `python scripts/run_family2_pack_smoke.py` | `all_ok scores=[0.9, 1.0, 0.9, 1.0, 0.9, 1.0]` |

**Note:** `python -m pip install build` was used once before `python -m build --wheel` where the isolated build env was required; behavior matches CI (`pip install build` in workflow).

No command renames or path deviations vs the milestone plan.

---

## 2. Pull request

| Field | Value |
|-------|--------|
| **PR** | [#6](https://github.com/m-cahill/lucid/pull/6) |
| **PR URL** | https://github.com/m-cahill/lucid/pull/6 |
| **PR state** | *(update after merge — target: merged)* |
| **Final PR head SHA (pre-merge, CI-verified)** | `05045ea5d752a6ddd1525a16c3da050e05ff8923` |

---

## 3. GitHub Actions — PR (`pull_request`) workflow

Workflow file: `.github/workflows/ci.yml` (job: `lint-test` on `ubuntu-latest`, Python 3.11).

| Field | Value |
|-------|--------|
| **Workflow name** | CI |
| **Run ID** | `23829259120` |
| **Workflow URL** | https://github.com/m-cahill/lucid/actions/runs/23829259120 |
| **Conclusion** | **success** |
| **Event** | `pull_request` |
| **PR head SHA** | `05045ea5d752a6ddd1525a16c3da050e05ff8923` (matches §2) |

### 3.1 Workflow analysis (per `docs/prompts/workflowprompt.md`)

**Workflow identity**

* **Workflow:** CI (`.github/workflows/ci.yml`)
* **Trigger:** `pull_request` (and `push` to main/master)
* **Change context:** M05 — deterministic Family 2 offline pack, manifest `--check`, tests; benchmark **1.1.0** unchanged; no Kaggle platform claims.

**Step 1 — Job inventory (expected)**

| Job / Check | Merge-blocking | Purpose |
|-------------|----------------|---------|
| Ruff check | Yes | Lint |
| Ruff format | Yes | Format |
| Mypy | Yes | Types |
| Pytest + coverage | Yes | Tests + ≥85% on `lucid` |
| Build wheel + `verify_wheel_has_kaggle` | Yes | Packaging |
| `generate_kaggle_notebook.py --check` | Yes | M01 notebook drift |
| `generate_family1_m04_notebook.py --check` | Yes | M04 notebook drift |
| `generate_family1_core_m03_manifest.py --check` | Yes | Family 1 manifest |
| `generate_family2_core_m05_manifest.py --check` | Yes | Family 2 manifest |

No `continue-on-error` on required steps.

**Step 6 — Verdict**

**Verdict:** CI run `23829259120` completed **`success`** for head `05045ea5d752a6ddd1525a16c3da050e05ff8923` (includes M05_run1 evidence update). All merge-blocking steps executed (lint, format, mypy, pytest+coverage, wheel+kaggle verify, both notebook `--check` steps, Family 1 and Family 2 manifest `--check`). **Merge approved** per workflow prompt §6–7.

*(Earlier run `23829238083` on `a5aa401983ca419213c90abc8f1193dab6244d42` also succeeded for the initial feature commit.)*

**Annotation (informational):** GitHub surfaced a Node.js 20 deprecation notice for `actions/checkout@v4` / `actions/setup-python@v5` — does not fail the job; track for future workflow updates.

**Step 7 — Next actions:** Merge PR #6 to `main`; confirm post-merge `main` CI (§4).

---

## 4. Post-merge `main` workflow (if applicable)

| Field | Value |
|-------|--------|
| **Merge SHA** | *(fill after merge — `git rev-parse main` on updated clone)* |
| **Run ID** | *(push workflow on `main` after merge)* |
| **Workflow URL** | *(https://github.com/m-cahill/lucid/actions/runs/<ID>)* |
| **Conclusion** | *(success / failure)* |

---

## 5. Governance notes

* **M04:** Hosted-model CSV population for Family 1 remains deferred; not reopened.
* **M05:** No Kaggle platform proof; Family 2 verdict **retain provisionally** (offline pack only).
* **Benchmark:** **1.1.0** unchanged (no scorer/schema edits in this milestone).
