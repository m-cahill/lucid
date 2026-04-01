# M04 Plan — Family 1 analytics — difficulty ladder, spread analysis, and promotion decision

**Project:** LUCID  
**Milestone:** M04  
**Title:** Family 1 analytics — difficulty ladder, spread analysis, and promotion decision  
**Branch:** `m04-family-1-analytics`  
**Status:** **Complete** (repository record)  
**Benchmark line:** **1.1.0** (unchanged)

## Objective

Use the **M03 canonical Family 1 pack** (`family1_core_m03_v1`) to decide whether `symbolic_negation_v1` should be **promoted**, **retained provisionally**, or **dropped** from the core competition path — with **decision-grade**, reproducible evidence.

## Pre-registered promotion criteria

Family 1 is **promote** only if **all** of the following hold:

1. **Pack quality** — no determinism drift; no material metadata gaps; no duplicate/malformed episodes; buckets balanced and coherent.  
2. **Difficulty ladder coherence** — LOW / MEDIUM / HIGH distinct in pack design; model performance does not collapse into an obviously flat ladder on hosted-model evidence.  
3. **Discriminatory power** — evaluated models show meaningful score spread; not near-all-perfect or near-all-zero; some component metrics show interpretable differences.  
4. **Competition usefulness** — supports metacognition-under-drift; judge-defensible; no obvious artifact shortcut.

If some but not all conditions are met → **retain provisionally**. If discriminatory power or defensibility fails badly → **drop**.

## Scope

### In scope

- Structural difficulty-ladder analysis from manifest + `symbolic_negation_v1` knobs.  
- Deterministic full-pack baseline (`fixture_turns` + official scorer) — pipeline coherence.  
- **M04 Kaggle analytics surface** — `notebooks/lucid_kaggle_family1_m04_analytics.ipynb` (generated; **not** the M01 transport notebook).  
- **Decision panel × stratified subset:** default **10 models** × **24 episodes** (8 LOW / 8 MEDIUM / 8 HIGH) via `m04_decision_eval_rows()`.  
- Machine-readable artifacts under `docs/milestones/M04/artifacts/`.  
- Targeted updates to `docs/lucid.md`, `docs/LUCID_COMPETITION_ALIGNMENT.md`.  
- M01 score ledger as **partial supporting** evidence only (three transport rows).

### Out of scope

- Family 2 / 3 implementation; benchmark version bump; scorer semantic change; M01 notebook contract rewrite; multi-family normalization.

## Execution notes

| Topic | Decision |
|--------|-----------|
| Hosted-model grid | **Not** 96×26 in-milestone; **panel + 24-episode subset** first; expand if operationally easy. |
| M01 notebook | **Preserved**; M04 uses separate task name `lucid_family1_m04_task`. |
| Verdict driver | **New** M04 evaluation evidence; M01 ledger alone insufficient. |

## Deliverables

- `M04_plan.md` (this file), `M04_toolcalls.md`, `M04_run1.md`, `M04_run2.md`, `M04_summary.md`, `M04_audit.md`  
- `scripts/analyze_family1_core_m03.py`, `scripts/summarize_family1_model_results.py`, `scripts/generate_family1_m04_notebook.py`  
- Artifacts: `family1_bucket_stats.json`, `family1_deterministic_baseline.csv`, `family1_model_scores.csv`, `family1_component_metrics.csv`, `family1_promotion_decision.md`, `m04_model_panel.json`

## Judged axis

**Novelty / insights / discriminatory power** (secondary competition axis), while preserving M03 dataset-quality positioning.
