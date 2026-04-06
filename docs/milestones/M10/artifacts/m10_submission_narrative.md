# LUCID — Judge-facing submission narrative (M10)

**Benchmark version:** 1.1.0  
**Evidence scope:** M01–M09 closed; M09 mature-benchmark hosted evidence is **partial** (see limitations).

---

## What LUCID measures

LUCID (*Latent Update & Calibration under Instructional Drift*) is a **metacognition-first diagnostic benchmark**. It asks whether a model can **detect instructional drift**, **calibrate confidence** after a governing rule changes, and **recover** before stale confidence outruns correctness. It is **not** a solver entry and **not** a generic reasoning contest.

Outputs are **answer + scalar confidence**; scoring encodes detection, calibration, and related signals under a fixed profile (`LUCID_SCORING_PROFILE_v1.1.0`).

---

## Why metacognition under drift matters

Many failures under change are not “wrong answer” failures alone—they are **stale-policy failures**: the model keeps behaving as if the earlier instruction still governs the task. LUCID stresses **rule change** in compact synthetic environments so that **not noticing drift** and **remaining overconfident** are measurable, not anecdotal.

---

## How the benchmark is constructed

- **Synthetic deterministic rule-worlds** — episodes are generated from seeds and template families with explicit drift types (e.g. negation, contradiction, scope / precedence / exception). Ground truth and lineage are inspectable (`unified_core_m07_v1`, 240 episodes; M09 evaluates a deterministic **72-episode** mature panel on that unified substrate).
- **Unified pack normalization (M07)** — cross-family composition with metadata normalization; difficulty labels are **nominally** aligned across families, **not** psychometrically equated across families.
- **Defensibility layer (M08)** — automated audit (`run_unified_defensibility_audit.py`) with committed artifacts; **contamination resistance** is framed as structural auditability, not absolute immunity (`m08_contamination_posture.md`).

---

## What M01 → M09 proves (progression)

| Stage | Proof class | Core claim |
|--------|-------------|------------|
| **M01** | **Kaggle platform** | Community Benchmarks **E2E**: transport, task wiring, hosted models with numeric scores on an acceptance slice (historical ledger in `docs/lucid.md` §6). |
| **M03–M06** | **Local + CI** | Canonical per-family offline packs; deterministic manifests with `--check`. |
| **M07** | **Local + CI** | Single **unified** offline pack (`unified_core_m07_v1`) composing all three families. |
| **M08** | **Local + CI** | Defensibility audit **blocking** in CI; duplicate and lineage posture documented. |
| **M09** | **Kaggle platform (partial roster)** | **Mature-panel** notebook task on unified substrate; **ingested** leaderboard export → `m09_model_scores.csv` (**15** completions, **18** non-completions documented). |

**M04** Family-1 analytics and its Kaggle surface are **superseded for mature hosted evidence** by M09 (`m09_m04_blocker_disposition.md`); the **M01 score table** remains **historical M01 evidence** and is not overwritten.

---

## What M09’s evidence subset shows

On the **15 models** with numeric M09 means:

- There is a **meaningful spread** on the mature task (`lucid_m09_mature_evidence_task`).
- **M01 → M09 deltas** are not uniform: some models **improve** on the mature panel, others **lose ground** sharply—consistent with a benchmark that **reorders** models when the evaluation slice moves from the transport acceptance task to the **72-episode** cross-family panel.

Figures and tables derived from committed CSVs: `docs/milestones/M10/artifacts/figures/`, `docs/milestones/M10/artifacts/tables/`, manifest `m10_figure_manifest.json`.

**Honest boundary:** The export does **not** support per-family, per-difficulty, or component (D/L/O/A/C) slices; those are **not** claimed from aggregate exports. **33** roster rows are tracked; **18** did not yield an M09 numeric in the export (`failed_platform_limited`).

---

## Where to read next

- Claims ↔ evidence: `m10_claims_evidence_matrix.md`
- Limitations register: `m10_limitations_and_scope.md`
- Representative models (portfolio): `m10_representative_models.md`
- FAQ (judges): `m10_faq_for_judges.md`
