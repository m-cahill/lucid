# M09 — Kaggle platform run manifest

**Panel ID:** `m09_mature_evidence_v1`  
**Task name:** `lucid_m09_mature_evidence_task`  
**Benchmark slug:** `michael1232/lucid-kaggle-community-benchmarks`  
**Benchmark version (semantics):** 1.1.0  

---

## Repository linkage (closeout)

| Field | Value |
|-------|--------|
| Generated notebook (this repo) | `notebooks/lucid_kaggle_m09_mature_evidence.ipynb` |
| Notebook ZIP install pin (embedded in notebook) | `3a0f774d6f7ed069ed088364ab7d9c175b079b01` |
| **Exact Kaggle notebook URL / version** | **Not recorded** — not present in the leaderboard export or attached materials for this closeout. Strongest available linkage: benchmark slug + task name + notebook path + pin SHA above. |

The pin SHA is the **authoritative** code state referenced by the shipped notebook’s `%pip install` cell. It may differ from the **documentation / ledger** commit on `main` at the time of this closeout; reconcile by regenerating the notebook with `--pin-sha` matching the intended release commit when publishing a new Kaggle revision.

---

## Raw source evidence

| Artifact | Path |
|----------|------|
| Raw leaderboard export (audit trail) | `docs/milestones/M09/artifacts/m09_kaggle_leaderboard_export.csv` |

---

## Ingested run summary (from export)

| Metric | Value |
|--------|--------|
| Models in roster (M09 task rows) | **33** |
| **Completed** M09 runs (numeric `Numerical_Result` on `lucid_m09_mature_evidence_task`) | **15** |
| **Non-completions** (no M09 numeric score; `Boolean_Result=False` on failed rows in export) | **18** |

**Non-completion posture:** The **18** models without M09 numeric scores are classified as **`failed_platform_limited`** in `m09_model_scores.csv`. The honest interpretation is **non-completion under platform / token / cost constraints** on the larger M09 panel — **not** a claim that the benchmark is defective. This limits **evidence breadth**, not benchmark correctness.

---

## Derived milestone artifacts

| Artifact | Role |
|----------|------|
| `m09_model_scores.csv` | One row per model: M01 mean (`lucid_main_task`), M09 mean (`lucid_m09_mature_evidence_task` where present), delta, status, evaluation timestamp |
| `m09_family_breakdown.csv` | **NA** — see file header / note (not sliceable from export) |
| `m09_difficulty_breakdown.csv` | **NA** — see file header / note (not sliceable from export) |
| `m09_component_metrics.csv` | **NA** — D/L/O/A/C not in export; see file rows |

**Limitation:** The export provides **per-task aggregate means** only. **No** per-episode scores, **no** component (D/L/O/A/C) breakdown, and **no** family or difficulty slices — so those CSVs are explicit **not available from export** placeholders (no inferred metrics).

---

## Proof class

**Kaggle platform proof** for M09 is **claimed for the ingested export**: real task names, benchmark slug, timestamps, and numeric aggregates where the platform returned them. **CI** continues to validate generators and `--check` parity only.
