# M05 Plan — Family 2: contradiction / clarification benchmark family

**Milestone:** M05  
**Branch:** `m05-family-2-contradiction-clarification`  
**Primary judged axis:** **Dataset quality & task construction**  
**Benchmark version target:** **1.1.0 unchanged** unless an explicit change-control decision is made  
**Milestone posture:** **Small, offline-core, deterministic family implementation milestone**. Do not mix in Kaggle platform work or submission-grade hosted-model claims.

## 1. Objective

Implement the first canonical offline pack for **Family 2 — contradiction / clarification**, designed to stress **metacognitive honesty, abstention, guarded updating, and recovery after clarification** while preserving LUCID’s current benchmark semantics, deterministic generation posture, and audit-ready artifact discipline.

This milestone should be the Family 2 analogue of what M03 was for Family 1: a clean, reproducible, committed offline pack with local proof and CI guardrails, not a mixed analytics/platform milestone.

## 2. Why this milestone now

M05 is the next locked family in the roadmap, after Family 1 scale-up and Family 1 analytics. The project’s governing documents explicitly identify **contradiction / clarification** as the second priority family and describe contradiction and clarification as central to LUCID’s metacognition-under-drift thesis. M05 should deepen family coverage while staying narrow, defensible, and synthetic.

## 3. Scope

### In scope

* A new deterministic Family 2 family spec and offline core pack.
* Family-specific generator/pack module under `src/lucid/`.
* A committed manifest fixture with deterministic regeneration and `--check`.
* Local smoke path for the new pack.
* Tests for determinism, balance, metadata integrity, and duplicate prevention.
* CI guardrail for the Family 2 manifest check.
* Honest closeout docs, including a provisional family verdict if no hosted-model evidence is gathered.

### Out of scope

* Kaggle notebook or Kaggle task for Family 2.
* Hosted-model platform runs for Family 2.
* Claiming Family 2 promotion on the basis of local evidence alone.
* Backfilling M04 Family 1 hosted-model evidence as part of M05 scope.
* Scorer, output-schema, or benchmark-semantic changes.
* Family 3, unified multi-family normalization, defensibility hardening, or submission packaging.

M04 already closed with Family 1 hosted-model CSV population deferred; keep that separate instead of quietly folding it into M05.

## 4. Family definition for M05

Define a canonical Family 2 template family:

* **Family name:** `contradiction_clarification_v1`
* **Canonical pack id:** `family2_core_m05_v1`

The family should exercise two closely related episode shapes under the existing benchmark contract:

1. **Unresolved contradiction** — The prompt contains a direct conflict or contradiction that should make a well-calibrated model lower confidence and prefer `CLARIFY` or `ABSTAIN` over overconfident answering.

2. **Clarification-resolved contradiction** — The prompt contains a contradiction followed by a clarifier that restores answerability, so the model can demonstrate guarded recovery and resumed correctness.

These episodes must remain synthetic, deterministic, and legible. Do **not** let this family drift into vague natural-language ambiguity or open-ended reasoning theater.

## 5. Target pack shape

Default target:

* **72 episodes total**
* **24 LOW / 24 MEDIUM / 24 HIGH**
* Within each difficulty bucket:

  * **12 unresolved contradiction**
  * **12 clarification-resolved**

Each episode must carry machine-readable metadata sufficient for future analytics and audits, at minimum:

* `episode_id`
* `family_id`
* `pack_id`
* `difficulty`
* `contradiction_state` (`unresolved` or `resolved`)
* `template_version`
* `seed`
* `drift_type`
* `target_behavior`
* `expected_post_drift_rule`
* any family-specific parameters needed for exact regeneration

The pack should contain **no duplicate episode ids** and no duplicate logical episodes under different ids.

## 6. Required deliverables

Create the following deliverables, following existing naming/style conventions:

* `src/lucid/packs/family2_core_m05.py`
* `tests/fixtures/family2_core_m05/family2_core_m05_manifest.json`
* `scripts/generate_family2_core_m05_manifest.py`
* `scripts/run_family2_pack_smoke.py`
* `tests/` — Family 2 pack tests
* `docs/families/contradiction_clarification_v1.md`
* `docs/milestones/M05/artifacts/family2_pack_stats.json`

Family implementation also uses `src/lucid/families/contradiction_clarification_v1.py` and `src/lucid/runner_family2.py` for generation and local smoke.

## 7. Implementation requirements

### A. Preserve benchmark semantics

Assume **benchmark version 1.1.0 stays unchanged**. Do not change scorer semantics, output schema, or calibration rules as part of M05 unless an explicit change-control path is opened.

### B. Stay within the minimal green path

The new family must still fit LUCID’s minimal executable spine: `generate deterministic episode -> parse typed response -> score -> write bundle`.

### C. Keep the family legible

This family should measure contradiction/clarification behavior, not scope drift, precedence drift, or general instruction soup.

### D. Add CI without weakening existing guards

Add one new deterministic CI guard: `python scripts/generate_family2_core_m05_manifest.py --check`

## 8. Acceptance criteria

M05 is complete only when all of the following are true:

1. `family2_core_m05_v1` exists as a committed deterministic offline pack.
2. The manifest is committed and regenerates cleanly with `--check`.
3. Pack balance is exactly: 72 episodes; 24 LOW / 24 MEDIUM / 24 HIGH; equal unresolved/resolved split inside each bucket.
4. The pack carries the required audit metadata.
5. Family 2 smoke passes locally.
6. CI includes and passes the new Family 2 manifest `--check`.
7. Full standing repo gates remain green.
8. `docs/lucid.md` is updated at closeout (M05 complete, M06 next, inventory, verdict, judged axis).
9. M05 closeout records an honest Family 2 verdict: default **retain provisionally** unless discriminatory evidence exists.

## 9. Verification commands

Standing verification set **plus** Family 2 checks (see `M05_run1.md` for recorded results).

## 10. Required docs updates during the milestone

Update, at minimum: `docs/lucid.md`, `docs/LUCID_COMPETITION_ALIGNMENT.md`, `docs/milestones/M05/M05_plan.md`, `docs/milestones/M05/M05_toolcalls.md`. At closeout: `M05_run1.md`, `M05_summary.md`, `M05_audit.md`. `docs/LUCID_OPERATING_MANUAL.md` benchmark version aligned with **1.1.0**.

## 11. Explicit guardrails for Cursor

* Do **not** claim Kaggle platform proof unless actual hosted external evidence is recorded.
* Do **not** claim Family 2 promotion without real discriminatory evidence.
* Do **not** change benchmark semantics silently.
* Do **not** let contradiction/clarification become a vague language benchmark.
* Do **not** touch canonical notebooks by hand; regenerate if they must change.
* Do **not** reopen M04 scope casually.

## 12–13. Closeout posture

Expected Family 2 verdict: **retain provisionally** unless M05 unexpectedly includes real discriminatory evidence beyond the offline pack.
