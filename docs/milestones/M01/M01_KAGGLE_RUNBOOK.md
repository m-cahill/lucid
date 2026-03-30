# M01 — Kaggle Community Benchmarks handoff runbook

**Milestone:** M01 — transport proof for benchmark line **1.1.0**  
**Purpose:** Execute the **real Kaggle platform** steps after repo-side assets are merged. This document is **not** a substitute for the [Kaggle Benchmarks cookbook](https://github.com/Kaggle/kaggle-benchmarks/blob/ci/cookbook.md).

---

## 1. Repo-side prerequisites (offline)

- Branch contains `notebooks/lucid_kaggle_benchmark.ipynb` with **one** `%choose` selecting **`lucid_main_task`**.
- Deterministic slice matches `tests/fixtures/kaggle_transport/transport_manifest.json` (seeds **100/LOW**, **42/MEDIUM**, **200/HIGH**).
- Local gates green: `ruff`, `mypy`, `pytest`, `python scripts/run_local_smoke.py`.

---

## 2. Kaggle notebook setup

1. Create or open a Kaggle notebook in the **Community Benchmarks** flow (see competition / platform UI for the current entry point).
2. **Add input:** install LUCID from GitHub (pin a commit SHA or tag once M01 merges), e.g.  
   `pip install -q "git+https://github.com/m-cahill/lucid.git@<ref>"`  
   Use the first code cell in `notebooks/lucid_kaggle_benchmark.ipynb` as the template (uncomment / adjust ref).
3. Copy the remaining cells from the repo notebook so task names and `%choose` stay aligned.
4. **Model:** prefer a **Kaggle-hosted** model (e.g. examples in the upstream cookbook). One model is enough for the acceptance run; add a second only after the first proof is green.
5. **Save Version** after a successful run.

---

## 3. Leaderboard / main task

- The notebook must expose **exactly one** main leaderboard task via `%choose` in the **final** code cell (see cookbook: [Publishing Your Task to the Leaderboard](https://github.com/Kaggle/kaggle-benchmarks/blob/ci/cookbook.md)).
- Dataset evaluation uses `.evaluate(...)` over the fixed three-row slice; the main task aggregates per-row scores (see notebook implementation).

---

## 4. Evidence capture (commit back to `docs/milestones/M01/`)

Fill `M01_KAGGLE_EVIDENCE_TEMPLATE.md` (or rename to `M01_run1.md` once populated) with:

- Notebook URL / version identifier
- Task and Community Benchmark identifiers (as shown in the UI)
- Model identifier used on platform
- Screenshots or exports if links are brittle
- Any manual steps, friction, or permission blockers

**Honesty rule:** If a full platform run cannot be completed, **do not** claim M01 E2E complete; record the blocker and keep CI green on offline transport checks only.

---

## 5. Semantic freeze

- **No** change to scoring profile **1.1.0**, output meaning, or family semantics under the banner of “Kaggle compatibility.” Transport-only differences must be documented as such.
