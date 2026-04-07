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

## 4. Evidence sync (P12 + P24 + partial P48)

Leaderboard export with `lucid_main_task` and `lucid_m11_probe_p12_task` rows ingested via:

```text
python scripts/ingest_m11_platform_exports.py --write
python scripts/generate_m11_tables.py --write
python scripts/generate_m11_figures.py --write
```

Artifacts now include `m11_p12_vs_main_comparison.csv`, `m11_p12_cost_frontier.csv`, `m11_p24_candidate_set.md`, and `m11_fig_p12_delta_vs_cost.png`.

---

## 5. Excluded models — surface-compatibility failures

Two models were excluded from the active roster after retries. Exact failure payloads were later recovered from the P12 run:

### DeepSeek-R1 (`deepseek-r1-0528`)

- **status:** `run_error`
- **failure_reason_code:** `json_parse_failure_reasoning_wrapper`
- **evidence:** model emits `<think>...</think>` reasoning trace before JSON output; text adapter raises `ValueError: Confidence is not numeric: None`
- **classification:** structured-output / parser-compatibility failure; model reachable, benchmark task valid, parse failed before score

### gpt-oss-120b

- **status:** `run_error`
- **failure_reason_code:** `json_parse_failure_truncated_output`
- **evidence:** model initially returns valid JSON but later emits truncated malformed JSON; raises `ValueError: No JSON object found in model output`
- **classification:** structured-output / surface-compatibility failure; model reachable, benchmark task valid, parse failed before score

**M11 posture:** these failures reflect the current strict structured-output transport contract. M11 intentionally does **not** modify the parser, prompt, or notebook to rescue these runs. Both models remain excluded (`tracked: false`) with evidence-backed exclusion metadata in `m11_roster_canonical.json`. This preserves comparability with the 31 tracked models.

---

## 6. Closeout (formal)

**Closed (UTC):** 2026-04-07 — milestone complete from governance and evidence standpoint.

The evidence surface comprises:

- **P12:** 31 models completed with `lucid_main_task` comparator + operator cost CSV
- **P24:** 11 models from the cost-aware cohort
- **P48:** partial cohort (Gemma 3 12B hit context-window overflow at 32,768 tokens — logged as operational ceiling, not benchmark defect)
- **Excluded:** 2 models with exact surface-compatibility failure evidence (`json_parse_failure_reasoning_wrapper`, `json_parse_failure_truncated_output`)

No further M11 probing is planned. **M12** is the active follow-on milestone (`docs/milestones/M12/M12_plan.md`). Ledger: `docs/lucid.md` §9.

**CI authority (merge-blocking `main`):** See `M11_run2.md` for the **2026-04-07** corrective series. Tooling recovery reached **green** on run **24105189098** at commit **`c0f55ce7cdbc8d9b3feca7625379cb59211b0cd1`**. The formal **closeout** commit (31/2 roster + regenerated artifacts + ledger alignment) must also pass **`CI`** on `main`; the **latest** run ID is recorded in `M11_toolcalls.md`.
