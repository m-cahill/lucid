# M10 — CI / verification run log

**Milestone:** M10 — Writeup evidence pack, figures, and judge-facing narrative  
**Environment:** Local (Windows, Python 3.11) + **`ubuntu-latest`** GitHub Actions (authoritative for merge)

---

## 1. Local verification (pre-PR)

Commands run from repository root unless noted.

### 1.1 CI-equivalent gates (match `.github/workflows/ci.yml`)

| Command | Result |
|---------|--------|
| `python -m pytest` | **PASS** — 106 tests; coverage ≥ 85% |
| `python -m ruff check src tests scripts` | **PASS** |
| `python -m ruff format --check src tests scripts` | **PASS** |
| `python scripts/generate_m10_tables.py --check` | **PASS** |
| `python scripts/generate_m10_figures.py --check` | **PASS** |

Additional parity checks (same as CI bundle):

| Command | Result |
|---------|--------|
| `python scripts/generate_unified_core_m07_manifest.py --check` | **PASS** |
| `python scripts/run_unified_defensibility_audit.py --check` | **PASS** |

### 1.2 Broader `ruff` invocation (informational)

| Command | Result |
|---------|--------|
| `python -m ruff check .` | **FAIL** — reports issues inside generated/legacy **notebook** JSON under `notebooks/` (e.g. E501, E402, E741). This is **not** the CI scope; workflow uses `ruff check src tests scripts` only. |
| `python -m ruff format --check .` | **Would reformat** several `.ipynb` files — again **not** CI scope. |

**Conclusion:** Merge-blocking style gates are **`src` / `tests` / `scripts`** only; M10 did not expand Ruff scope to notebooks.

### 1.3 Figure / table stability and cross-platform PNG policy

- **`generate_m10_tables.py --check`:** Text artifacts match generator — **stable** (exact text match).
- **`generate_m10_figures.py --check`:** After **PR #12** iteration, `--check` accepts either **exact byte** equality or **RGBA pixel-wise** match within **atol=2** per channel (`numpy.allclose` on `PIL`/`RGBA` arrays). This addresses **Linux CI vs Windows dev** rasterization differences without dropping committed PNGs from the repo.
- **First PR CI attempt** failed on **exact** PNG bytes (`generate_m10_figures.py --check`) on `ubuntu-latest` while committed PNGs were produced on Windows. **Fix:** commit `556e97e` (`fix(m10): PNG --check tolerates OS/matplotlib raster variance (RGBA atol=2)`).
- **Pins:** `matplotlib>=3.8.0` in `dev` deps; no extra pin was required once tolerance was applied. **Residual risk:** large font/backend changes could still exceed tolerance; if so, widen tolerance slightly or regenerate PNGs on Linux (e.g. Docker) and recommit.

---

## 2. Pull request

| Field | Value |
|-------|--------|
| Branch | `m10-writeup-pack` |
| Base | `main` |
| PR | **#12** — https://github.com/m-cahill/lucid/pull/12 |
| **Final PR head SHA** (merged) | `556e97e` |

### Commit series on the PR branch

| SHA | Description |
|-----|-------------|
| `888ab39` | M10: writeup pack, deterministic figures/tables, CI checks |
| `556e97e` | fix(m10): PNG `--check` tolerates OS/matplotlib raster variance (RGBA atol=2) |

---

## 3. PR CI analysis (authoritative `pull_request` runs)

**Workflow identity:** `CI` (`.github/workflows/ci.yml`)  
**Trigger:** `pull_request`  
**Merge-blocking:** single job **`lint-test`** (all steps must pass).

### Run A — failed (superseded)

| Field | Value |
|-------|--------|
| Run ID | `24016147118` |
| PR head | `888ab39` |
| Conclusion | **failure** |
| Failing step | **Verify M10 figures match generator** — exact PNG bytes differed Linux vs Windows. |

### Run B — green (authoritative for merge)

| Field | Value |
|-------|--------|
| Run ID | `24016213848` |
| PR head | `556e97e` |
| URL | https://github.com/m-cahill/lucid/actions/runs/24016213848 |
| Conclusion | **success** |
| `generate_m10_tables.py --check` | **PASS** |
| `generate_m10_figures.py --check` | **PASS** |

**Inventory (all passed on Run B):** Ruff check/format, Mypy, Pytest+coverage, wheel verify, M01/M04/M09 notebook `--check`, manifests M03–M07, M08 defensibility `--check`, **M10 tables + figures** `--check`.

---

## 4. Merge and post-merge `main` CI

| Field | Value |
|-------|--------|
| Merge commit SHA | `4a3fe92` — *Merge pull request #12 from m-cahill/m10-writeup-pack* |
| Post-merge `main` workflow run ID | `24016267389` |
| Post-merge run URL | https://github.com/m-cahill/lucid/actions/runs/24016267389 |
| Conclusion | **success** |
| Trigger | `push` to `main` (merge) |

### Docs-only closeout commit (final `M10_run1` / summary / audit / toolcalls)

| Field | Value |
|-------|--------|
| Commit SHA | `fd2fd92` |
| Post-merge CI run ID | `24016329033` |
| URL | https://github.com/m-cahill/lucid/actions/runs/24016329033 |
| Conclusion | **success** |
| Trigger | `push` to `main` (docs finalize after PR merge) |

---

## 5. Resolutions / follow-ups

- **PNG CI fix:** `556e97e` — relaxed `--check` to pixel tolerance; no Linux-regenerated PNG commit required.
- **Node.js deprecation annotation** on GitHub Actions (Node 20) — informational only; **not** a merge blocker for M10.
- **M11:** stub only; no implementation in this milestone.
