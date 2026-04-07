# LUCID — Judge-facing submission narrative (M10)

**Benchmark version:** 1.1.0  
**Evidence scope:** M01–M09 closed; M09 mature-benchmark hosted evidence is **partial** (see limitations). **M11** adds nested probe-ladder hosted evidence (**31** active models; **2** exclusions — see §M11 addendum). **M12** packages deterministic **benchmark / task / writeup linkage** (`docs/milestones/M12/artifacts/m12_submission_linkage.json`).

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

## M11 addendum (hosted probe surface — bounded)

**M11** evaluates a deterministic **probe ladder** (P12 / P24 / partial P48; P72 comparable via M09 task rows) on the same mature substrate as M09. Closeout posture:

- **31** active tracked models; **2** exclusions with evidence-backed failure codes (`deepseek-r1-0528`, `gpt-oss-120b`) — see `docs/milestones/M11/artifacts/m11_roster_canonical.json`.
- **P24:** cost-aware **11-model** cohort (`m11_p24_candidate_set.md`).
- **P48:** partial; Gemma 3 12B documented operational ceiling (context length), not a benchmark defect.

No new scoring semantics; **no** parser/prompt rescue for excluded models in M11 scope.

---

## Competition-facing links (submission)

- **Primary project link (intended):** Kaggle **Community Benchmark** for slug `michael1232/lucid-kaggle-community-benchmarks` — fill the canonical benchmark URL in `docs/milestones/M12/artifacts/m12_linkage_sources.json` after owner-view confirms public visibility; regenerated linkage lives in `m12_submission_linkage.json`.
- **Secondary (implementation / source):** https://github.com/m-cahill/lucid
- **Competition hub:** https://www.kaggle.com/competitions/kaggle-measuring-agi

**Tasks (six)** wired in the repo: `lucid_main_task`, `lucid_family1_m04_task`, `lucid_m09_mature_evidence_task`, `lucid_m11_probe_p12_task`, `lucid_m11_probe_p24_task`, `lucid_m11_probe_p48_task` — see `docs/milestones/M12/artifacts/m12_submission_linkage.md`.

---

## Where to read next

- Claims ↔ evidence: `m10_claims_evidence_matrix.md`
- Limitations register: `m10_limitations_and_scope.md`
- Representative models (portfolio): `m10_representative_models.md`
- FAQ (judges): `m10_faq_for_judges.md`
