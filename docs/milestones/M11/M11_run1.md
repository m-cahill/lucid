# M11 — CI / repo run record (ingest + generators)

**Milestone:** M11 — hosted-model probe surface  
**Date (UTC):** 2026-04-06  
**Branch:** `main` (local development record)  
**Notebook `%pip` pin (GitHub archive):** `a13afadadd89a6aed0cd434682b2675017ceab3c` — first commit where `src/lucid/kaggle/m11_probe_panels.py` exists in the tree. A follow-up `chore(m11): repin Kaggle notebooks to post-M11 commit` records regenerated `.ipynb` + manifest + ingest fields; see `git log -2 --oneline`.

---

## 0. Incident — bad pin / missing module on Kaggle (resolved in repo)

**Symptom:** Preflight showed `lucid.kaggle.m11_probe_panels -> MISSING` while `lucid` and `lucid.kaggle` were FOUND.

**Failing pin tried:** `13137d907e938c6ed36c2b17eb0c4347f2d3943c` — that revision does **not** contain `src/lucid/kaggle/m11_probe_panels.py` in the **committed** Git tree. Kaggle `%pip install` uses the GitHub archive ZIP for that SHA only; local untracked files are not included.

**Classification:** `run_error` — reason code `bad_pin_commit_missing_m11_module`.

**Fix:** Two commits — (1) commit all M11 sources and tooling so the module exists at `HEAD`; (2) regenerate notebooks and manifest so the embedded pin equals a post-M11 SHA, then commit those files. Verify with `python scripts/verify_m11_git_has_module.py --sha <pinned_sha>` before upload.

---

## 1. Notebook pin (Step 2.1)

**First commit (M11 in tree):** `a13afadadd89a6aed0cd434682b2675017ceab3c`

**Regenerated** (after that commit, pin = `HEAD` = same SHA):

* `python scripts/generate_m11_kaggle_notebooks.py --write`
* `python scripts/generate_m09_kaggle_notebook.py --pin-sha a13afadadd89a6aed0cd434682b2675017ceab3c -o notebooks/lucid_kaggle_m09_mature_evidence.ipynb`

Verified:

* `python scripts/generate_m11_kaggle_notebooks.py --check`
* `python scripts/generate_m09_kaggle_notebook.py --check -o notebooks/lucid_kaggle_m09_mature_evidence.ipynb`
* `python scripts/verify_m11_git_has_module.py --sha a13afadadd89a6aed0cd434682b2675017ceab3c`
* `python scripts/generate_m11_notebook_release_manifest.py --check`

---

## 2. Platform execution (Step 2.2) — operator posture

**This repository run does not execute Kaggle.** Probe ladder runs (P12 → P24 → P48 → P72) are **operator actions** on Kaggle per `M11_KAGGLE_RUNBOOK.md`.

**Current committed ingest** uses only the **existing** `docs/milestones/M09/artifacts/m09_kaggle_leaderboard_export.csv` as the default `--export` source. That file contains **`lucid_m09_mature_evidence_task`** rows (P72 / M09 comparable) but **does not** contain `lucid_m11_probe_p12_task` / `p24` / `p48` rows until new runs are exported.

---

## 3. Ingest + deterministic artifacts (Phase 3)

Commands (regenerate / verify):

```text
python scripts/ingest_m11_platform_exports.py --write --notebook-pin-sha a13afadadd89a6aed0cd434682b2675017ceab3c
python scripts/ingest_m11_platform_exports.py --check
python scripts/generate_m11_tables.py --write
python scripts/generate_m11_tables.py --check
python scripts/generate_m11_figures.py --write
python scripts/generate_m11_figures.py --check
```

**Repo CI parity:** `pytest`, `ruff check`, `ruff format --check`, mypy (`src`), and all `--check` generators including M11 ingest/tables/figures.

---

## 4. Next operator action (real P12–P48 evidence)

After running probe tasks on Kaggle, download leaderboard CSV(s) and re-run ingest with additional `--export` paths (merged by newest `Evaluation_Date` per model × task). Then commit updated `docs/milestones/M11/artifacts/*` and refresh this run record.
