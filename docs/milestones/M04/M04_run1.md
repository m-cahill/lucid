# M04 — Run 1 — Local / analytics verification (authoritative closeout)

**Milestone:** M04  
**Recorded:** 2026-03-31 (closeout)  
**Branch:** `m04-family-1-analytics`  
**Environment:** Windows 10, Python 3.11.x (local); CI reference `ubuntu-latest` (see §6)

**Merge note:** At closeout, **`main` does not yet include M04** until the M04 PR is merged; pre-merge HEAD on this branch is recorded in §5.

---

## 1. Command matrix (truthful gates)

All commands below completed with **exit code 0** on the closeout verification pass (same tree as the M04 commit).

**Re-verification:** The full matrix was re-run immediately before pushing the closeout commit to `origin` (branch `m04-family-1-analytics`); all steps **PASS** on that tree.

| Step | Command | Result |
|------|---------|--------|
| Lint | `python -m ruff check src tests scripts` | **PASS** — All checks passed |
| Format | `python -m ruff format --check src tests scripts` | **PASS** — 40 files already formatted |
| Types | `python -m mypy src` | **PASS** — Success: no issues found in 20 source files |
| Tests | `python -m pytest` | **PASS** — 51 passed; total coverage **88.73%** (floor 85%) |
| Wheel | `python -m pip install build` then `python -m build --wheel` | **PASS** — `lucid_benchmark-0.1.0-py3-none-any.whl` built |
| Kaggle wheel | `python scripts/verify_wheel_has_kaggle.py` | **PASS** — `lucid/kaggle/episode_llm.py` present in wheel |
| Smoke | `python scripts/run_local_smoke.py` | **PASS** — `LUCID_SCORE_EPISODE=1.000000` |
| Manifest | `python scripts/generate_family1_core_m03_manifest.py --check` | **PASS** — manifest matches regeneration |
| M01 notebook | `python scripts/generate_kaggle_notebook.py --check -o notebooks/lucid_kaggle_transport_text_adapter_m_01.ipynb` | **PASS** — `check_pin=45cfa43be89575fc7d94545eae838e413abd30e7` |
| M04 notebook | `python scripts/generate_family1_m04_notebook.py --check -o notebooks/lucid_kaggle_family1_m04_analytics.ipynb` | **PASS** — `check_pin=0f82e1e1a2f8023d5896d72c0f67d46e8c984e33` |
| Analytics | `python scripts/analyze_family1_core_m03.py --json-out docs/milestones/M04/artifacts/family1_bucket_stats.json --baseline-csv docs/milestones/M04/artifacts/family1_deterministic_baseline.csv` | **PASS** — artifacts regenerated |

**Note:** On Windows, `python -m build --wheel` may print isolated-env messages to **stderr**; exit code remained **0**.

---

## 2. Benchmark / semantics

| Item | Value |
|------|--------|
| Benchmark version | **1.1.0** (unchanged) |
| Scoring semantics | Unchanged (M04 is analytics-only) |

---

## 3. Notebook generator pins (audit)

| Notebook | `--check` pin SHA (from committed `.ipynb`) |
|----------|-----------------------------------------------|
| M01 transport | `45cfa43be89575fc7d94545eae838e413abd30e7` |
| M04 Family 1 analytics | `0f82e1e1a2f8023d5896d72c0f67d46e8c984e33` (closeout commit; `%pip` ZIP pin) |

---

## 4. M04 analytics artifact regeneration

- `docs/milestones/M04/artifacts/family1_bucket_stats.json` — regenerates cleanly from canonical manifest path `tests/fixtures/family1_core_m03/family1_core_m03_manifest.json`.
- `docs/milestones/M04/artifacts/family1_deterministic_baseline.csv` — full 96-row deterministic baseline from `analyze_family1_core_m03.py`.

---

## 5. Repository HEAD and M04 notebook pin (audit)

| Role | Value |
|------|--------|
| **Branch tip (merge candidate)** | Run `git rev-parse HEAD` on `m04-family-1-analytics` after checkout (tip moves if you amend; do not rely on a frozen tip SHA inside amended commits). |
| **M04 notebook banner / `%pip` ZIP pin** | `0f82e1e1a2f8023d5896d72c0f67d46e8c984e33` |

**Parity note:** For any branch tip `T`, verify `git diff 0f82e1e1a2f8023d5896d72c0f67d46e8c984e33..T -- src/` is **empty** before claiming ZIP/tip equivalence — the installed `lucid` package must match. See `docs/kaggle/LUCID_KAGGLE_NOTEBOOK_CONTRACT.md` §5.1.

**Session closeout (2026-03-31):** immediately before the final single commit was finalized, `git rev-parse HEAD` read `1f2efb5a9ea369725beaca6c893cb98a126c6302` (recorded in `M04_toolcalls.md`; may differ after further amends).

---

## 6. GitHub Actions (authoritative CI)

**Pull request:** https://github.com/m-cahill/lucid/pull/5 (merged to `main`).

| Field | Value |
|-------|--------|
| Workflow | `CI` (`.github/workflows/ci.yml`) |
| PR / `pull_request` run (`m04-family-1-analytics`) | https://github.com/m-cahill/lucid/actions/runs/23827390034 — **success** |
| `main` / `push` run (merge commit) | https://github.com/m-cahill/lucid/actions/runs/23827404774 — **success** |

**Note:** GitHub may surface Node.js deprecation notices for `actions/checkout` / `actions/setup-python`; they do not change the correctness signal for this milestone.

---

## 7. Honesty — M04_run2

Hosted-model CSV population remains **optional / follow-up** per `M04_run2.md`. Family 1 verdict stays **retain provisionally** until real scores land in `family1_model_scores.csv`.
