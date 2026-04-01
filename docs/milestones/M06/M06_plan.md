# M06 Plan — Family 3: scope / precedence / exception drift

**Milestone:** M06  
**Branch:** `m06-family-3-scope-precedence-exception`  
**Primary judged axis:** **Dataset quality & task construction**  
**Benchmark version target:** **1.1.0 unchanged** unless an explicit change-control decision is opened  
**Milestone posture:** Small, deterministic, offline-core family implementation milestone. No Kaggle platform work, no hosted-model claims, no scorer/output-schema changes.

## 1. Objective

Implement the third locked benchmark family as a clean, reproducible offline pack for **scope / precedence / exception drift**, extending LUCID’s drift taxonomy beyond negation and contradiction while preserving the current benchmark semantics, minimal green path, and audit-ready artifact posture. The family should remain synthetic, legible, and explicitly diagnostic rather than becoming natural-language ambiguity or solver theater.

## 2. Why this milestone now

The roadmap already fixes **Family 3 — scope / precedence / exception drift** as the next family after M05, and the moonshot explicitly names **scope change**, **precedence reversal**, and **exception insertion** as core drift types in LUCID’s scientific taxonomy. M06 should therefore be the Family 3 analogue of M03 and M05: a canonical deterministic offline pack with tests, manifest regeneration, CI guardrails, and honest governance.

## 3. Scope

### In scope

* A new deterministic Family 3 family spec and offline core pack.
* Synthetic episodes covering:

  * **scope drift**
  * **precedence drift**
  * **exception drift**
* A committed canonical manifest fixture with deterministic regeneration and `--check`.
* A dedicated Family 3 local smoke path.
* Tests for determinism, balance, metadata integrity, and duplicate prevention.
* One new CI manifest check for Family 3.
* Family documentation, milestone docs, and ledger updates.

### Out of scope

* Kaggle notebook or Family 3 benchmark task.
* Hosted-model sweep or discriminatory evidence collection for Family 3.
* Scorer, parser, output-schema, or benchmark-semantic changes.
* M04 deferred Family 1 hosted-model CSV backfill.
* M07 unified cross-family normalization work.
* M08 defensibility hardening.
* Any attempt to broaden the family into authority drift or contradiction/clarification replay.

## 4. Family definition

**Family name:** `scope_precedence_exception_v1`  
**Canonical pack id:** `family3_core_m06_v1`

The family should use a compact synthetic rule-world with typed item IDs, explicit local rules, and a clearly answerable final resolution. The answer domain should stay parallel to the prior families: selecting or naming a single final item ID from a bounded candidate set.

Implement three episode subtypes:

### A. Scope drift

A rule changes the subset over which it applies.

Example shape:

* Before: apply rule to **all items**
* After: apply rule only to items in **subset S**

### B. Precedence drift

Two valid rules remain in force, but the controlling order changes.

Example shape:

* Before: rule A overrides rule B
* After: rule B overrides rule A

### C. Exception drift

A new exception is introduced that overrides the prior general rule.

Example shape:

* Before: all items satisfying condition X follow rule R
* After: all such items follow rule R **except** class E

These episodes must remain explicit and local. Do not let M06 drift into contradiction-family semantics, vague ambiguity, or authority-source switching. Family 3 is about **structural rule change**, not unresolved contradiction.

## 5. Target pack shape

Default target:

* **72 episodes total**
* **24 LOW / 24 MEDIUM / 24 HIGH**
* Within each difficulty bucket:

  * **8 scope drift**
  * **8 precedence drift**
  * **8 exception drift**

Suggested deterministic seed layout:

* **LOW**

  * scope: `1–8`
  * precedence: `9–16`
  * exception: `17–24`
* **MEDIUM**

  * scope: `101–108`
  * precedence: `109–116`
  * exception: `117–124`
* **HIGH**

  * scope: `201–208`
  * precedence: `209–216`
  * exception: `217–224`

This keeps the pack the same scale as Family 2 while staying small enough for a narrow milestone.

## 6. Episode semantics and scorer posture

All canonical M06 episodes should end in a **resolved, answerable final state**.

Default expectation:

* `final_state_unresolved = False`
* `acceptable_final_modes = {"ANSWER"}`

Family 3 may still create a legitimate calibration window around the drift event, but the final resolution should be computable under the existing single-answer benchmark surface. Do **not** invent a richer interaction protocol for M06.

For drift typing:

* Prefer existing implementation-level drift taxonomy support if scope / precedence / exception values already exist.
* If distinct public drift enum values are **not** already available without contract edits, keep the public benchmark contract unchanged and represent the subtype distinction in Family 3 metadata instead of widening contracts during M06.

**Implementation lock (M06):** Use `DriftType.SCOPE`, `DriftType.PRECEDENCE`, and `DriftType.EXCEPTION` as the primary drift type per episode; optional `drift_subtype` / `family3_subtype` string echoes for pack analytics.

If M06 cannot be implemented cleanly without public contract edits, stop and document the blocker rather than silently changing benchmark semantics.

## 7. Required deliverables

Create the following deliverables, following the established M03/M05 pattern:

* `src/lucid/families/scope_precedence_exception_v1.py`

  * deterministic Family 3 episode generation
  * stable subtype helpers
  * metadata helpers

* `src/lucid/packs/family3_core_m06.py`

  * canonical pack builder
  * seed layout helpers
  * representative smoke selection helpers

* `src/lucid/runner_family3.py`

  * Family 3 fixture/smoke helper path
  * generate → score → bundle local validation

* `scripts/generate_family3_core_m06_manifest.py`

  * supports `--write` and `--check`

* `scripts/run_family3_pack_smoke.py`

  * runs one representative episode per subtype per difficulty bucket
  * target: **9** smoke episodes total

* `tests/fixtures/family3_core_m06/family3_core_m06_manifest.json`

  * committed canonical manifest

* `tests/test_family3_core_m06_pack.py`

  * determinism
  * manifest shape
  * balance by difficulty and subtype
  * duplicate prevention
  * metadata presence
  * scorer regression / smoke alignment

* `docs/families/scope_precedence_exception_v1.md`

  * family spec
  * subtype definitions
  * difficulty knobs
  * non-goals
  * metadata fields

* `docs/milestones/M06/artifacts/family3_pack_stats.json`

  * compact structural summary for closeout and audit

Cursor may add small internal helpers if needed, but the milestone should stay centered on the items above.

## 8. Metadata requirements

Each episode should include audit-ready machine-readable metadata, at minimum:

* `episode_id`
* `family_id`
* `pack_id`
* `difficulty`
* `template_version`
* `seed`
* `drift_type`
* `drift_subtype`
* `target_behavior`
* `expected_post_drift_rule`

Plus subtype-specific metadata as applicable:

* for scope drift:

  * `scope_before`
  * `scope_after`
* for precedence drift:

  * `precedence_before`
  * `precedence_after`
  * `rule_count`
* for exception drift:

  * `general_rule`
  * `exception_class`
  * `exception_trigger`

The manifest should contain no duplicate logical episodes under distinct IDs.

## 9. Difficulty design

The family should scale difficulty through structural parameters, not prose complexity.

Suggested knobs:

* candidate item count
* attribute grid size
* subset complexity for scope drift
* number of competing rules for precedence drift
* number and salience of exception classes
* distractor density
* overlap pressure between rules

Difficulty should stay legible and synthetic. The benchmark’s governing doctrine explicitly prefers parameterized, auditable synthetic rule-worlds over open-ended ambiguity.

## 10. Implementation requirements

### A. Preserve benchmark semantics

Assume benchmark **1.1.0** remains unchanged. Do not alter scorer semantics, parser behavior, response schema, or contract language in M06.

### B. Preserve the minimal green path

Family 3 must still fit the existing deterministic pipeline:

`generate episode -> parse typed response -> score -> write bundle`

Do not add multi-turn protocol requirements or notebook-specific behavior in this milestone.

### C. Keep the family legible

The family should isolate **structural rule change**. Avoid natural-language ambiguity, contradiction windows, or authority-source changes unless they are already strictly encoded as scope/precedence/exception mechanics.

### D. Keep the milestone small

Mirror the M05 pattern:

* separate family generator
* separate pack module
* separate runner
* one new manifest script
* one new manifest CI check

Do not mix analytics, hosted evidence, or Kaggle work into M06.

## 11. Acceptance criteria

M06 is complete only when all of the following are true:

1. `family3_core_m06_v1` exists as a committed deterministic offline pack.
2. The committed manifest regenerates cleanly with `--check`.
3. Pack balance is exactly:

   * 72 episodes total
   * 24 LOW / 24 MEDIUM / 24 HIGH
   * 8 scope / 8 precedence / 8 exception per bucket
4. Family 3 smoke passes locally.
5. The pack carries the required metadata.
6. CI includes and passes the new Family 3 manifest `--check`.
7. All standing repo verification gates remain green.
8. `docs/lucid.md` is updated at closeout to record:

   * M06 complete
   * M07 next
   * Family 3 pack inventory row
   * Family 3 verdict row
   * M06 judged axis
9. M06 closeout records an honest Family 3 verdict:

   * default expectation: **retain provisionally**
   * only promote if real discriminatory evidence exists and is recorded

## 12. Verification commands

Re-run the standing M05 set **plus** the new Family 3 checks.

Minimum expected commands:

```bash
python -m ruff check src tests scripts
python -m ruff format --check src tests scripts
python -m mypy src
python -m pytest
python -m build --wheel
python scripts/verify_wheel_has_kaggle.py
python scripts/run_local_smoke.py
python scripts/generate_family1_core_m03_manifest.py --check
python scripts/generate_kaggle_notebook.py --check -o notebooks/lucid_kaggle_transport_text_adapter_m_01.ipynb
python scripts/generate_family1_m04_notebook.py --check -o notebooks/lucid_kaggle_family1_m04_analytics.ipynb
python scripts/generate_family2_core_m05_manifest.py --check
python scripts/run_family2_pack_smoke.py
python scripts/generate_family3_core_m06_manifest.py --check
python scripts/run_family3_pack_smoke.py
```

If any command changes because the repo evolved, document that explicitly in `docs/milestones/M06/M06_run1.md`.

## 13. Required docs updates during the milestone

Update, at minimum:

* `docs/lucid.md`
* `docs/LUCID_COMPETITION_ALIGNMENT.md`
* `docs/milestones/M06/M06_plan.md`
* `docs/milestones/M06/M06_toolcalls.md`
* `docs/milestones/M06/M06_run1.md`

At closeout, also produce:

* `docs/milestones/M06/M06_summary.md`
* `docs/milestones/M06/M06_audit.md`

## 14. Explicit guardrails for Cursor

* Do **not** claim Kaggle platform proof for M06.
* Do **not** create a Family 3 Kaggle task or notebook in this milestone.
* Do **not** change scorer semantics, response schema, or benchmark version.
* Do **not** reopen M04 Family 1 hosted-model CSV backfill.
* Do **not** quietly widen public contracts just to land new drift subtype names.
* Do **not** let Family 3 collapse into contradiction-family semantics or authority drift.
* Do **not** hand-edit canonical notebooks.

## 15. Closeout instructions to give Cursor explicitly

At closeout, use an explicit prompt telling Cursor to do all of this:

1. Re-run the full local verification set and record exact commands/results in `M06_run1.md`.
2. Push the milestone branch and capture real GitHub Actions URLs in `M06_run1.md`.
3. Analyze the actual workflow run using `docs/prompts/workflowprompt.md`.
4. Keep the milestone open until required CI is green.
5. Generate:

   * `M06_summary.md` with `docs/prompts/summaryprompt.md`
   * `M06_audit.md` with `docs/prompts/unifiedmilestoneauditpromptV2.md`
6. Update `docs/lucid.md` so M06 is complete and M07 is next.
7. Add the Family 3 pack to the standing pack inventory and verdict ledger.
8. Record the M06 judged axis explicitly as **Dataset quality & task construction**.
9. Ensure all documentation is updated as necessary.
10. Merge to `main` only after green CI.
11. Create the next milestone folder / stubs for M07 if not already present.
12. If follow-up work appears after milestone close, carry it on a new branch rather than pushing more commits onto a closed milestone branch.

## 16. Expected honest closeout posture

Unless M06 unexpectedly includes real discriminatory evidence beyond the offline pack, the expected family verdict is:

* **Family 3 verdict:** `retain provisionally`

That keeps M06 aligned with the project’s standing rule that family verdicts must be evidence-backed rather than rhetorical.

---

One useful ledger improvement for `docs/lucid.md` after M06: add a compact **“drift subtypes covered”** field to the standing family pack inventory, so readers can see each family’s coverage without opening the family spec.
