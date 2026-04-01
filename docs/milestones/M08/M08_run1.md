# M08 — Run record (local + PR CI + main CI)

**Project:** LUCID  
**Milestone:** M08 — Defensibility, QA, and contamination-resistance hardening  
**Repository:** https://github.com/m-cahill/lucid  

---

## 1. Local verification (Windows, repository root)

Commands executed in order (all **exit code 0** unless noted):

| Command | Result | Notes |
|---------|--------|--------|
| `python scripts/run_unified_defensibility_audit.py --check` | Pass | Verifies committed JSON/MD artifacts match deterministic audit |
| `python scripts/generate_unified_core_m07_manifest.py --check` | Pass | Unified manifest regeneration parity |
| `python scripts/generate_family1_core_m03_manifest.py --check` | Pass | |
| `python scripts/generate_family2_core_m05_manifest.py --check` | Pass | |
| `python scripts/generate_family3_core_m06_manifest.py --check` | Pass | |
| `python scripts/run_unified_pack_smoke.py` | Pass | 9 episodes; `all_ok n=9` |
| `python -m pytest` | Pass | Full suite; coverage gate **≥85%** met (~**87%** on `lucid`) |

**Benchmark version:** **1.1.0** (unchanged; no semantic bump in M08).  
**Notable warnings:** None from pytest; smoke prints expected episode scores.

---

## 2. Pull request (authoritative green head)

| Field | Value |
|-------|--------|
| **PR** | https://github.com/m-cahill/lucid/pull/9 |
| **Title** | M08: Defensibility, QA, and contamination-resistance hardening |
| **Base branch** | `main` @ `c29212acef18b0005613237fdca29d29eaeb7381` |
| **PR head SHA (authoritative green)** | `4e4fb2c8b5bece0cf5bcf6233c16a4f5decdc90e` |

### Superseded / failed runs (not PR head)

| Run ID | Trigger | Conclusion | Cause |
|--------|---------|------------|--------|
| `23866385840` | `pull_request` | **failure** | Ruff **format** on `src/lucid/audits/defensibility.py` — fixed in `a89352c` |
| `23866410564` | `pull_request` | **failure** | Pytest `test_defensibility_script_check_exits_zero`: audit JSON **path** fields were absolute; Linux CI drift vs committed artifacts — fixed in `4e4fb2c` (`_repo_relative_posix` in audit output) |

### Authoritative PR CI run (merge-blocking)

| Field | Value |
|-------|--------|
| **Workflow** | `CI` (`.github/workflows/ci.yml`) |
| **Run ID** | `23866649886` |
| **URL** | https://github.com/m-cahill/lucid/actions/runs/23866649886 |
| **Trigger** | `pull_request` |
| **Branch** | `m08-defensibility` |
| **Commit** | `4e4fb2c8b5bece0cf5bcf6233c16a4f5decdc90e` |
| **Conclusion** | **success** |
| **Job** | `lint-test` (single job; all steps required) |

**Merge-blocking checks:** The `CI` workflow’s `lint-test` job (Ruff check, Ruff format, Mypy, Pytest + coverage ≥85%, wheel + Kaggle verify, both Kaggle notebook `--check` generators, Family 1–3 manifest `--check`, unified manifest `--check`, **M08** `run_unified_defensibility_audit.py --check`). No `continue-on-error` on these steps.

**Informational:** GitHub annotation on Node.js 20 deprecation for `actions/checkout@v4` / `actions/setup-python@v5` (upstream runner notice; does not fail the job).

---

## 3. Workflow analysis (workflowprompt.md structure)

**Workflow identity:** `CI`, run `23866649886`, trigger `pull_request`, branch `m08-defensibility`, commit `4e4fb2c8b5bece0cf5bcf6233c16a4f5decdc90e`.

**Change context:** M08 — defensibility audit module, CI gate, committed artifacts, ledger updates; no benchmark semantic change.

**Baseline:** `main` at `c29212a…` pre-merge.

**Step 1 — Inventory:** All checks in one job `lint-test`; each step is merge-blocking for this repo’s workflow.

**Step 2 — Signal integrity:** Tests include unit + integration; coverage enforced on `lucid` with `--cov-fail-under=85`. Static gates: Ruff, Mypy strict on `src`. New M08 step exercises the same audit as local `--check`.

**Step 3 — Delta:** Touches `src/lucid/audits/`, `scripts/`, `tests/`, `docs/`, `.github/workflows/ci.yml`. No contract edits under `docs/contracts/`.

**Step 4 — Failures:** Two earlier PR runs failed for fixable reasons (format + cross-platform JSON); both resolved before merge.

**Step 5 — Invariants:** Required checks enforced; no scope leakage; benchmark version unchanged.

**Step 6 — Verdict:** This run is **safe to merge** with respect to repo CI policy.

**Step 7 — Next actions:** Merge completed; post-merge `main` CI verified (§4).

---

## 4. Post-merge `main` CI

| Field | Value |
|-------|--------|
| **Merge commit** | `2ceca1f979c1b8de68827786184d742223d15043` |
| **PR** | #9 merged into `main` |
| **Workflow** | `CI` |
| **Run ID** | `23866754720` |
| **URL** | https://github.com/m-cahill/lucid/actions/runs/23866754720 |
| **Trigger** | `push` to `main` |
| **Conclusion** | **success** |

### 4.1 Docs closeout commit on `main` (after merge)

| Field | Value |
|-------|--------|
| **Commit** | `7fbd7416fa2987c9f9ad45df66f54f5914a8beec` |
| **Message** | `docs(m08): closeout run1, summary, audit, and tool log` |
| **CI run** | `23866907808` |
| **URL** | https://github.com/m-cahill/lucid/actions/runs/23866907808 |
| **Conclusion** | **success** |

---

## 5. Commit chain on PR branch (reference)

| SHA | Description |
|-----|-------------|
| `e05a926` | feat(m08): defensibility audit, CI gate, artifacts, and ledger |
| `a89352c` | style(m08): ruff format defensibility audit module |
| `4e4fb2c` | fix(m08): repo-relative paths in audit JSON for cross-platform CI --check |

---

## 6. Benchmark version

**1.1.0** — unchanged for M08 (no `LUCID_CHANGE_CONTROL` semantic bump).
