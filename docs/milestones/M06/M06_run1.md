# M06 — CI / verification run log

**Milestone:** M06 — Family 3 — scope / precedence / exception drift  
**Branch:** `m06-family-3-scope-precedence-exception`  
**Status:** Local verification recorded below; **GitHub Actions URLs and PR merge evidence** — add after push to remote.

---

## 1. Local verification (Windows / PowerShell, repo root)

Commands run after implementation; all completed with **exit code 0** unless noted.

| Command | Result |
|---------|--------|
| `python -m ruff check src tests scripts` | OK |
| `python -m ruff format --check src tests scripts` | OK |
| `python -m mypy src` | OK |
| `python -m pytest` | OK (coverage ≥85% on `lucid`) |
| `python -m pip install build` + `python -m build --wheel` | Wheel built |
| `python scripts/verify_wheel_has_kaggle.py` | OK |
| `python scripts/run_local_smoke.py` | OK (`LUCID_SCORE_EPISODE=1.000000`) |
| `python scripts/generate_family1_core_m03_manifest.py --check` | OK |
| `python scripts/generate_kaggle_notebook.py --check -o notebooks/lucid_kaggle_transport_text_adapter_m_01.ipynb` | OK |
| `python scripts/generate_family1_m04_notebook.py --check -o notebooks/lucid_kaggle_family1_m04_analytics.ipynb` | OK |
| `python scripts/generate_family2_core_m05_manifest.py --check` | OK |
| `python scripts/run_family2_pack_smoke.py` | OK |
| `python scripts/generate_family3_core_m06_manifest.py --check` | OK |
| `python scripts/run_family3_pack_smoke.py` | OK (9 episodes, scores all 1.0) |

---

## 2. Pull request

- **PR URL:** _(add after opening PR to `main`)_
- **Head SHA:** _(add)_

---

## 3. GitHub Actions

- **Workflow:** `CI` (`.github/workflows/ci.yml`)
- **Run URL / ID:** _(add after push)_
- **Conclusion:** _(add)_

---

## 4. Post-merge (optional)

- **Main branch run:** _(optional)_
