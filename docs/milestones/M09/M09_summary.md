# Milestone Summary — M09: Expanded Kaggle evidence on the mature benchmark

**Project:** LUCID  
**Phase:** Benchmark construction  
**Milestone:** M09 — Expanded Kaggle evidence on the mature benchmark  
**Timeframe:** 2026-04-01 → **closed** (2026-04-05 repository record — evidence ingest PR)  
**Status:** **Complete** — Phase B (repo) + Phase C (platform export ingest + derived CSVs + manifest)

---

## 1. Milestone Objective

Add **deterministic, auditable** infrastructure for **hosted-model evidence** on the **mature unified** benchmark (`unified_core_m07_v1`) without changing scoring semantics, and record **real** Kaggle platform results when available.

---

## 2. Scope Definition

### In scope (delivered)

- `src/lucid/kaggle/m09_evidence_panel.py` — panel `m09_mature_evidence_v1` (72 rows; Family 1 = exact M04 decision continuity).
- `docs/milestones/M09/artifacts/m09_model_panel.json` — reproducible via `scripts/generate_m09_panel_artifact.py`.
- `scripts/generate_m09_kaggle_notebook.py` → `notebooks/lucid_kaggle_m09_mature_evidence.ipynb`; task **`lucid_m09_mature_evidence_task`**.
- CI `--check` for panel artifact + notebook.
- **Phase C:** Raw leaderboard export + **`m09_model_scores.csv`** (15 successes, 18 non-completions) + NA breakdown/component CSVs where export cannot support slices + updated **`m09_kaggle_run_manifest.md`**.

### Out of scope

- Fabricated metrics beyond the export.
- Benchmark version bump (remains **1.1.0**).
- M10 writeup pack implementation.
- Full 240-episode hosted sweep or re-running the panel to “fill” the 18 non-completions.

---

## 3. Work Executed

- Phase B: panel, notebook generator, tests, CI, M04 disposition docs (PR #10, merged earlier).
- Phase C: Ingest **`m09_kaggle_leaderboard_export.csv`**; derive scores; document limitations (no family/difficulty/component inference); classify non-completions as **`failed_platform_limited`**; refresh promotion + ledger alignment.

---

## 4. Validation & Evidence

| Proof class | Status |
|-------------|--------|
| **Local proof** | **Yes** — generators, smoke, pytest, panel/notebook `--check` |
| **GitHub CI proof** | **Yes** — see `M09_run1.md` for Phase B PR #10 and **Phase C closeout PR** (recorded when merged) |
| **Kaggle platform proof** | **Yes (partial roster)** — ingested export with **15** numeric M09 means + **18** documented non-completions |

**Benchmark version:** **1.1.0** (unchanged).

---

## 5. Judged Axis

**Novelty / insights / discriminatory power** — **advanced** with **honest limits**: mature-panel **instrument + notebook + scored subset**; full hosted roster **not** completed.

---

## 6. M04 Hosted-Model Evidence

**Disposition:** **Superseded by M09** as the canonical **mature-benchmark** hosted evidence path. **`m09_model_scores.csv`** is populated; **`family1_model_scores.csv`** was **not** backfilled by design.

---

## 7. Artifact Surfaces

| Artifact | Role |
|----------|------|
| `docs/milestones/M09/artifacts/m09_kaggle_leaderboard_export.csv` | Raw platform export (audit trail) |
| `docs/milestones/M09/artifacts/m09_model_scores.csv` | Derived per-model M01 / M09 means and status |
| `docs/milestones/M09/artifacts/m09_kaggle_run_manifest.md` | Linkage, counts, limitations |
| `docs/milestones/M09/artifacts/m09_*_breakdown.csv`, `m09_component_metrics.csv` | Explicit NA where export cannot support slices |
| `docs/milestones/M09/artifacts/m09_promotion_decision.md` | Provisional posture |
| `docs/milestones/M09/artifacts/m09_m04_blocker_disposition.md` | M04 vs M09 operational notes |

---

## 8. Exit Criteria

**Met:** At least one **authoritative** Kaggle-linked evidence ingest with **real** task/benchmark identifiers and **non-fabricated** numeric rows for the completing subset, plus explicit accounting for non-completions.

---

## 9. Authorized Next Step

**M10** — writeup evidence pack, figures, faculty framing, M01→M09 comparison, defensibility / contamination narrative, judge-facing packaging (see `docs/milestones/M10/M10_plan.md`).
