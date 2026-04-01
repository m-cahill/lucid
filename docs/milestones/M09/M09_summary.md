# Milestone Summary — M09: Expanded Kaggle evidence on the mature benchmark

**Project:** LUCID  
**Phase:** Benchmark construction  
**Milestone:** M09 — Expanded Kaggle evidence on the mature benchmark  
**Timeframe:** 2026-04-01 → *open* (platform phase pending)  
**Status:** **Open** — Phase B (repo) complete; Phase C–E (Kaggle platform run + score ingestion) **pending**  

---

## 1. Milestone Objective

Add **deterministic, auditable** infrastructure for **hosted-model evidence** on the **mature unified** benchmark (`unified_core_m07_v1`) without changing scoring semantics, and record **real** Kaggle platform results when available.

Without M09, the project would lack a **defined 72-episode** cross-family panel and **generated** notebook path aligned to the post-M08 substrate.

---

## 2. Scope Definition

### In scope (delivered in repo)

- `src/lucid/kaggle/m09_evidence_panel.py` — panel `m09_mature_evidence_v1` (72 rows; Family 1 = exact M04 decision continuity).
- `docs/milestones/M09/artifacts/m09_model_panel.json` — reproducible via `scripts/generate_m09_panel_artifact.py`.
- `scripts/generate_m09_kaggle_notebook.py` → `notebooks/lucid_kaggle_m09_mature_evidence.ipynb`; task **`lucid_m09_mature_evidence_task`**.
- CI `--check` for panel artifact + notebook.
- Tests: `tests/test_m09_evidence_panel.py`.
- Governance docs: `docs/lucid.md`, `docs/LUCID_COMPETITION_ALIGNMENT.md`, `docs/LUCID_OPERATING_MANUAL.md`, runbook, disposition/promotion stubs.
- **Honest** Phase C placeholders: header-only CSVs + `m09_kaggle_run_manifest.md` stating **no platform run** recorded yet.

### Out of scope

- Fabricated Kaggle scores or URLs.
- Benchmark version bump (remains **1.1.0**).
- M10 writeup pack implementation.
- Full 240-episode hosted sweep.

---

## 3. Work Executed

- Implemented deterministic panel selectors (F2/F3 balanced; F1 = M04 keys).
- Added notebook generator (dedicated cell pipeline, not M01/M04 index patches).
- Committed panel JSON; wired CI; added tests; documentation and external evidence index updates.
- Recorded **M04 blocker disposition**: **superseded by M09** as the successor evidence surface, with **operational** hosted closure still pending scored CSV rows (`m09_m04_blocker_disposition.md`).

---

## 4. Validation & Evidence

| Proof class | Status |
|-------------|--------|
| **Local proof** | **Yes** — generators, smoke, pytest, panel/notebook `--check` |
| **GitHub CI proof** | **Pending PR** — record run ID in `M09_run1.md` after `pull_request` CI |
| **Kaggle platform proof** | **No** — not available in this closeout; manifest documents gap |

**Benchmark version:** **1.1.0** (unchanged).

---

## 5. Judged Axis

**Novelty / insights / discriminatory power** — **partially advanced**: repo delivers the **evaluation panel + notebook** required for discriminatory sweeps; **insight from hosted spread** awaits platform CSV population.

---

## 6. M04 Hosted-Model Evidence

**Disposition:** **Superseded by M09** as the canonical **mature-benchmark** hosted evidence path (M04 Family 1 rows embedded in M09 panel). **Direct population** of `family1_model_scores.csv` was **not** performed; **full closure** of the discriminatory evidence gap requires **`m09_model_scores.csv`** rows from a real run (`m09_m04_blocker_disposition.md`).

---

## 7. Artifact Surfaces

| Artifact | Role |
|----------|------|
| `src/lucid/kaggle/m09_evidence_panel.py` | Panel logic |
| `docs/milestones/M09/artifacts/m09_model_panel.json` | Committed panel |
| `notebooks/lucid_kaggle_m09_mature_evidence.ipynb` | Generated notebook |
| `docs/milestones/M09/artifacts/m09_kaggle_run_manifest.md` | Platform run record (pending) |
| `docs/milestones/M09/artifacts/m09_model_scores.csv` | Scores (header-only until run) |
| `docs/milestones/M09/artifacts/m09_component_metrics.csv` | Components if exported |
| `docs/milestones/M09/artifacts/m09_family_breakdown.csv` | Per-family breakdown |
| `docs/milestones/M09/artifacts/m09_difficulty_breakdown.csv` | Per-difficulty breakdown |
| `docs/milestones/M09/artifacts/m09_promotion_decision.md` | Provisional posture |
| `docs/milestones/M09/artifacts/m09_m04_blocker_disposition.md` | M04 gap disposition |

---

## 8. Exit Criteria (milestone)

Original acceptance criteria required **at least one authoritative Kaggle platform proof run**. That criterion is **not met** in this revision. **Phase B** exit criteria **are met**. **M09 remains open** until platform evidence is recorded.

---

## 9. Authorized Next Step

1. Push PR; confirm green CI.  
2. Run Kaggle per `M09_KAGGLE_RUNBOOK.md`; regenerate notebook with `--pin-sha` = PR head.  
3. Populate CSVs and update `m09_kaggle_run_manifest.md`.  
4. Re-close summary or add `M09_run2.md` when platform evidence exists.

**M10** — **not** seeded until M09 is **fully** closed per project rules.
