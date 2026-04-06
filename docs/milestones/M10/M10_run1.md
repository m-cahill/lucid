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

### 1.3 Figure / table byte stability (local)

- **`generate_m10_tables.py --check`:** Text artifacts match generator — **stable** on this machine.
- **`generate_m10_figures.py --check`:** PNG bytes match regenerated buffer — **stable** on Windows after `--write`.
- **Linux vs Windows matplotlib risk:** PNG output is compared as **exact bytes** in `--check`. Different OS/font/ Agg builds *can* diverge. **Mitigation:** CI runs on **`ubuntu-latest`**; if the committed PNGs were produced on Windows, the **first** Linux CI run is the authoritative test. If CI fails on figure parity, regenerate with `python scripts/generate_m10_figures.py --write` on Linux (or in a Linux container), commit, and re-run — document any such fix below.
- **Pins:** `matplotlib>=3.8.0` in `dev` deps; no tighter pin unless CI proves instability. Residual risk remains **documented**, not eliminated by version pinning alone.

---

## 2. Pull request — record when created

| Field | Value |
|-------|--------|
| Branch | `m10-writeup-pack` |
| Base | `main` |
| PR URL | *(filled after `gh pr create`)* |
| PR head SHA | *(filled at merge time)* |

---

## 3. PR CI analysis (authoritative `pull_request` runs)

*Filled after PR exists and CI completes. Format follows `docs/prompts/workflowprompt.md` (workflow identity, jobs, conclusions, merge-blocking checks).*

| Field | Value |
|-------|--------|
| Workflow name | `CI` (`.github/workflows/ci.yml`) |
| PR CI run ID(s) | *(see below)* |
| Conclusion | *(success / failure)* |
| Merge-blocking | All jobs in `lint-test` (Ruff, Mypy, Pytest, wheel, notebook checks, manifests, M08 audit, **M10 table/figure checks**) |
| `generate_m10_tables.py --check` | *(pass/fail)* |
| `generate_m10_figures.py --check` | *(pass/fail)* |

### CI narrative

*(PR head SHA, run URL(s), whether green on authoritative head, any fixes/reruns.)*

---

## 4. Merge and post-merge `main` CI

| Field | Value |
|-------|--------|
| Merge commit SHA | *(after merge)* |
| Post-merge `main` workflow run ID | *(after merge)* |
| Post-merge run URL | *(after merge)* |
| Conclusion | *(success / failure)* |

---

## 5. Resolutions / follow-ups

- If PNG parity required a Linux-regenerated commit, describe the commit SHA and reason here.
- Docs-only follow-ups after merge (if any): list here.
