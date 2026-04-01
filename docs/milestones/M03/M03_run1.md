# M03 — Local verification & evidence (run1)

**Milestone:** M03 — Family 1 scale-up  
**Closeout verification date:** 2026-03-31 (formal pass, local)  
**Environment:** Windows, Python **3.11.9**  
**Repository root:** `c:\coding\kaggle\lucid`

**HEAD at start of formal closeout verification:** `e10021d7705e1a6bc6b46e9d5e373b93aa111f2f`  
**Note:** After staging and committing M03 artifacts, **HEAD will change** — update this line and the machine-readable footer after merge to record the **merge commit** and **GitHub Actions** run on `main`.

---

## 1. Standard gates (mirror `.github/workflows/ci.yml` + project scripts)

Commands run from repository root:

| Step | Command | Result |
|------|---------|--------|
| Ruff check | `python -m ruff check src tests scripts` | **Pass** |
| Ruff format | `python -m ruff format --check src tests scripts` | **Pass** (35 files formatted OK) |
| Mypy | `python -m mypy src` | **Pass** (20 source files) |
| Pytest + coverage | `python -m pytest` | **Pass** — **46** tests; total coverage **88.41%** (floor 85%) |
| Wheel build | `python -m build --wheel` | **Pass** — `lucid_benchmark-0.1.0-py3-none-any.whl` |
| Wheel kaggle guard | `python scripts/verify_wheel_has_kaggle.py` | **Pass** (`lucid/kaggle/episode_llm.py` present) |
| Local smoke (M00 path) | `python scripts/run_local_smoke.py` | **Pass** — `LUCID_SCORE_EPISODE=1.000000` |
| Kaggle notebook check | `python scripts/generate_kaggle_notebook.py --check -o notebooks/lucid_kaggle_transport_text_adapter_m_01.ipynb` | **Pass** (`check_pin=45cfa43be89575fc7d94545eae838e413abd30e7`) |

**PowerShell note:** `python -m build --wheel` may print benign stderr (`NativeCommandError`) while still exiting **0**; wheel artifact and subsequent steps confirmed success.

---

## 2. M03-specific verification

| Step | Command | Result |
|------|---------|--------|
| Manifest regeneration check | `python scripts/generate_family1_core_m03_manifest.py --check` | **Pass** — `ok` + path to `tests/fixtures/family1_core_m03/family1_core_m03_manifest.json` |
| Family 1 pack smoke (3 episodes) | `python scripts/run_family1_pack_smoke.py` | **Pass** — bundles under `out/family1_pack_smoke/`; scores `[1.0, 1.0, 1.0]` |
| Canonical manifest | `tests/fixtures/family1_core_m03/family1_core_m03_manifest.json` | **Present** — **96** episodes; **32/32/32** LOW/MEDIUM/HIGH |

### Smoke output (captured)

```text
bundle=out\smoke\episode_ep_symneg_25a9ad581e1d9cb4
LUCID_SCORE_EPISODE=1.000000
seed=100 severity=LOW bundle=out\family1_pack_smoke\episode_ep_symneg_1f438ab471eb138c LUCID_SCORE_EPISODE=1.000000
seed=42 severity=MEDIUM bundle=out\family1_pack_smoke\episode_ep_symneg_25a9ad581e1d9cb4 LUCID_SCORE_EPISODE=1.000000
seed=200 severity=HIGH bundle=out\family1_pack_smoke\episode_ep_symneg_6d0d42c996f9c1ab LUCID_SCORE_EPISODE=1.000000
all_ok scores=[1.0, 1.0, 1.0]
```

---

## 3. Git state at closeout (recorded)

| Field | Value |
|-------|--------|
| Inside git worktree | **Yes** (`git rev-parse --is-inside-work-tree` → true) |
| Branch | `m03-family-1-scale-up` (tracks `origin/m03-family-1-scale-up`) |
| Working tree (pre-commit) | **Dirty** — M03 files unstaged/untracked; **excluded** from M03 commit: `notebooks/archive/lucid_kaggle_benchmark_SCHEMA_SUPERSEDED.ipynb` (line-ending / unrelated churn), `notebooks/lucid_kaggle_transport_text_adapter_m_01.txt`, `notebooks/m01-baseline-e2e-2.ipynb` |

`git init` was **not** run.

---

## 4. Remote CI reference (GitHub Actions)

**Pre-merge:** Latest green **`CI`** run observed on **`main`** at closeout time:

| Run ID | Conclusion | Event | Branch | URL |
|--------|------------|-------|--------|-----|
| **23824761555** | success | push | `main` | `https://github.com/m-cahill/lucid/actions/runs/23824761555` |

**Post-merge (required hygiene):** After M03 lands on `main`, record the new workflow run ID/URL here (merge commit and PR run).

---

## 5. Artifact inventory

| Artifact | Path |
|----------|------|
| Canonical Family 1 M03 manifest | `tests/fixtures/family1_core_m03/family1_core_m03_manifest.json` |
| Pack logic | `src/lucid/packs/family1_core_m03.py` |
| Manifest CLI | `scripts/generate_family1_core_m03_manifest.py` |
| Family 1 E2E smoke | `scripts/run_family1_pack_smoke.py` |
| Pack tests | `tests/test_family1_core_m03_pack.py` |
| CI manifest gate | `.github/workflows/ci.yml` (Family 1 `--check` step) |

---

## Machine-readable footer

```json
{
  "milestone": "M03",
  "verification_date": "2026-03-31",
  "local_head_sha": "e10021d7705e1a6bc6b46e9d5e373b93aa111f2f",
  "python": "3.11.9",
  "pytest_passed": 46,
  "coverage_total_pct": 88.41,
  "manifest_check": "ok",
  "reference_main_ci_run_id": "23824761555",
  "reference_main_ci_url": "https://github.com/m-cahill/lucid/actions/runs/23824761555"
}
```
