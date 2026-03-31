# M01 Plan — Kaggle Community Benchmarks E2E Verification

**Status:** **Complete (closed)** — repository record 2026-03-31. See `M01_summary.md`, `M01_audit.md`, `M01_run1.md`.

**Project:** LUCID  
**Milestone:** M01  
**Benchmark line:** 1.1.0 (locked)  
**Default branch name:** `m01-kaggle-transport-proof`  
**Milestone mode:** Small, end-to-end, evidence-first

## 1. Objective

Prove that the existing LUCID **1.1.0** benchmark line can be **transported into Kaggle Community Benchmarks** and executed there **without changing benchmark semantics**.

For M01, keep scope intentionally narrow:

- **one active family only:** `symbolic_negation_v1`
- **one Kaggle main task only**
- **one tiny deterministic evaluation slice only**
- **one real Kaggle Community Benchmark proof path only**

This is a **transport-and-proof milestone**, not a benchmark expansion milestone.

---

## 2. Authority and invariants

Cursor must treat the following as locked:

1. `docs/LUCID_MOONSHOT.md`
2. Layer A/B contracts under `docs/contracts/`
3. `docs/LUCID_OPERATING_MANUAL.md`
4. `docs/LUCID_COMPETITION_ALIGNMENT.md`
5. `docs/lucid.md`
6. Existing implementation under `src/lucid/`

### Hard invariant

**No benchmark-semantic change is allowed in M01.**

That means M01 must **not** silently change:

- scoring formulas or profile behavior
- output schema meaning
- family semantics
- episode phase semantics
- eligibility windows
- confidence interpretation
- artifact meaning

If any of those must change, stop and treat it as formal change control with a version bump rather than “part of M01.”

---

## 3. Why M01 exists

M00 intentionally stopped at a **local deterministic green path** with CI. M01 is the first milestone that must prove **Kaggle Community Benchmarks end-to-end**, because LUCID’s current ledger explicitly leaves that proof deferred to M01.

M01 is complete only when there is:

1. **repo evidence** that LUCID can be represented as a Kaggle benchmark/task workflow, and  
2. **platform evidence** from an actual Kaggle Community Benchmarks run.

Local-only proof is **not enough** to close M01.

---

## 4. Milestone success criteria (hard gates)

M01 is only green when **all** of the following are true:

### A. Repo / CI gates

- Existing local gates remain green (`ruff`, `mypy`, `pytest`, local smoke).
- Any new CI added for M01 is truthful and merge-blocking if it represents a real invariant.
- No required check is weakened.
- Existing coverage posture is maintained or improved.

### B. Semantic equivalence gates

- `symbolic_negation_v1` still scores under **1.1.0** semantics.
- Kaggle transport code uses the same typed response meaning as local LUCID.
- Notebook/export path produces the same per-episode metric values as local scoring for fixed fixtures.
- Any deltas between local and Kaggle representations are documented as **transport-only**, not semantic.

### C. Kaggle transport gates

- A Kaggle task/notebook asset exists in the repo and is deterministic.
- The Kaggle path uses **one main task** only.
- The task evaluates a deterministic fixture dataset and returns a leaderboard-compatible result.
- The task uses a structured response path compatible with LUCID’s typed response model.

### D. Platform evidence gates

- A real Kaggle notebook/task run has been performed.
- Evidence is captured in the milestone folder.
- A real Community Benchmark entity or equivalent benchmark/task evidence exists, with links and screenshots/artifacts.
- Platform-specific friction is recorded honestly.

### E. Closeout gates

- `docs/lucid.md` is updated at milestone open and close.
- `M01_run1.md`, `M01_summary.md`, and `M01_audit.md` are produced.
- The branch merges only after green repo CI and platform-proof evidence are both present.

---

## 5. In scope

### In scope for M01

- Kaggle transport of **existing** LUCID semantics
- One deterministic fixture slice for `symbolic_negation_v1`
- One Kaggle task/notebook path
- One leaderboard-visible main task
- One real platform proof run
- CI guardrails for transport integrity
- Honest milestone evidence capture

### Explicitly out of scope

- New template families
- New scoring profile versions
- Clarification/recovery branch expansion
- Large dataset scaling
- Benchmark writeup polish beyond what is needed for proof
- Leaderboard optimization
- Re-architecting the local core
- Kaggle-specific semantics inside the benchmark core

---

## 6. Execution plan

## Phase 1 — Open the milestone and freeze the truth

### Required actions

1. Create `docs/milestones/M01/` if it does not already exist.
2. Copy this plan into `docs/milestones/M01/M01_plan.md`.
3. Seed `docs/milestones/M01/M01_toolcalls.md`.
4. Update `docs/lucid.md` to mark M01 as **opened / in progress**.
5. Add a short M01 entry noting that the milestone goal is **transport proof**, not semantic expansion.

### Required guardrails

- Do not claim Kaggle E2E is complete at milestone open.
- Do not update the active benchmark version.
- Do not widen the active family set.

### Evidence to capture

- Milestone folder created
- Plan copied
- Ledger updated

---

## Phase 2 — Define the Kaggle transport contract and frozen fixture slice

### Goal

Create the smallest deterministic slice that proves LUCID transport without introducing semantic ambiguity.

### Required implementation

1. Add a small deterministic fixture set for `symbolic_negation_v1`.
   - Use a tiny fixed set of episodes (recommended: **3–5** total).
   - Cover at least low / medium / high difficulty or equivalent deterministic seed spread.
   - Persist expected local outputs and expected scored metrics.

2. Add a transport-equivalence manifest for those fixtures.
   - For each fixture, record the expected:
     - typed response shape
     - final answer correctness
     - `D`, `L`, `O`, `A`, `C`
     - final scalar score

3. Add tests proving that the fixture expectations are stable under local scoring.

### File suggestions

Use names that fit the current repo, but prefer something like:

- `tests/fixtures/kaggle_transport/*.json`
- `tests/integration/test_kaggle_transport_equivalence.py`
- `src/lucid/kaggle/` for transport-only code

### Guardrails

- The fixture set is for transport proof only; it is **not** a new benchmark release.
- Do not add hidden notebook-only scoring logic.
- Keep all scoring delegated to existing LUCID logic where possible.

### Exit criteria

- Fixed fixtures exist
- Expected metric values are recorded
- Equivalence tests are green

---

## Phase 3 — Build the Kaggle notebook/task asset

### Goal

Create the minimal repo-tracked Kaggle asset that expresses LUCID as a Kaggle task workflow.

### Required implementation

1. Add a deterministic Kaggle task notebook asset.
   - Prefer a repo-controlled source form plus a generated notebook if practical.
   - Keep notebook generation deterministic.

2. Implement one **main task** that:
   - prompts the model for a typed LUCID response
   - enforces structured output compatible with `EpisodeResponse`
   - scores the response with local LUCID scoring code or a transport wrapper that is semantically identical
   - returns a leaderboard-compatible numeric result

3. Evaluate the task over the deterministic fixture dataset.
   - Use a dataset-wide evaluation pattern rather than ad hoc repeated cells.
   - Aggregate scores in a way that is faithful to LUCID’s existing scalar interpretation.

4. Ensure the notebook contains the final selection of the single main task.

### Design rule

The Kaggle notebook is a **transport surface**, not a second benchmark implementation.

### Required outputs

At minimum, commit:

- notebook source / generated notebook
- any tiny deterministic evaluation dataset artifact needed by the notebook
- export/validation helper script if used

### Guardrails

- One main task only.
- Keep intermediate diagnostics allowed, but only one leaderboard-visible task.
- Do not encode Kaggle-only benchmark meaning into core modules.

### Exit criteria

- Notebook/task asset exists in repo
- Main-task selection is present
- Offline validation of asset passes

---

## Phase 4 — Add offline verification and truthful CI guardrails

### Goal

Make the repo prove transport integrity **without pretending** that GitHub Actions is the Kaggle platform.

### Important constraint

Do **not** fake a green “Kaggle platform run” in CI.

CI should verify:

- notebook/export determinism
- fixture equivalence
- transport code stability
- notebook structure checks
- task selection checks

CI should **not** claim to prove real Kaggle execution if it only runs locally.

### Required implementation

1. Add tests for notebook/export determinism.
2. Add tests that compare local scorer outputs to transport/notebook scorer outputs on the frozen fixtures.
3. Add a small validation check that the notebook still contains exactly one main leaderboard task.
4. If a helper exporter exists, add a smoke test for it.

### CI expectation

Extend the existing workflow only as far as needed. Keep CI small and truthful.

If touching GitHub Actions, also clean up any adjacent workflow hygiene only if already in the edit path. Do **not** expand M01 into a general CI refactor milestone.

### Exit criteria

- CI stays green
- New transport integrity checks are green
- No dishonest “platform verified” claim is emitted from CI

---

## Phase 5 — Real Kaggle Community Benchmarks proof

### Goal

Produce the actual external platform evidence that closes M01.

### Required actions on Kaggle

1. Open a Kaggle benchmark task notebook using the official benchmark-task flow.
2. Port or upload the repo-tracked notebook asset.
3. Run the notebook on Kaggle using Kaggle’s benchmark environment.
4. Save a version.
5. Ensure the notebook emits the intended single main task output.
6. Create or attach the resulting task to a Community Benchmark.
7. Run at least one real evaluation/model pass sufficient to prove the pipeline actually works on-platform.

### Required evidence to capture in the repo

Record all of the following under `docs/milestones/M01/`:

- Kaggle notebook link/identifier
- task page link/identifier
- benchmark page link/identifier
- screenshots or exported images/PDFs if direct links are brittle
- the exact fixture slice used
- the model(s) used on platform
- observed platform outputs
- any surfaced token / cost / latency metadata, if Kaggle provides it
- any friction or manual steps required

### Honesty rule

If platform access, permissions, or runtime limitations prevent completion:

- do **not** close M01 as complete
- record the blocker in `M01_run1.md`
- keep CI green on what was implemented
- propose the smallest corrective next milestone rather than hand-waving the gap away

### Exit criteria

- Real Kaggle execution evidence exists
- Real benchmark/task evidence exists
- Friction is documented

---

## Phase 6 — Closeout, audit, and next-milestone seeding

### Required closeout work

1. Update `docs/lucid.md`:
   - current benchmark status
   - M01 ledger status
   - any new canonical artifact paths
   - brief M01 observation note

2. Produce:
   - `docs/milestones/M01/M01_run1.md`
   - `docs/milestones/M01/M01_summary.md`
   - `docs/milestones/M01/M01_audit.md`

3. The audit must explicitly state:
   - what was proven locally
   - what was proven in CI
   - what was proven on Kaggle
   - whether any gap remains

4. Merge only after:
   - repo CI is green for the final branch head
   - Kaggle proof evidence is committed
   - summary and audit exist

5. After merge:
   - create the next milestone folder
   - seed the next plan stub and toolcalls stub
   - do **not** continue pushing on the closed M01 branch unless a reopen is intentional

---

## 7. Deliverables checklist

The exact filenames may vary, but M01 should finish with the equivalent of:

- `docs/milestones/M01/M01_plan.md`
- `docs/milestones/M01/M01_toolcalls.md`
- deterministic Kaggle notebook/task asset(s)
- deterministic transport fixture set
- transport equivalence tests
- notebook/export validation tests
- `docs/milestones/M01/M01_run1.md`
- `docs/milestones/M01/M01_summary.md`
- `docs/milestones/M01/M01_audit.md`
- `docs/lucid.md` updated

---

## 8. Acceptance tests Cursor should explicitly run

At minimum, run and record:

1. Existing repo quality gates
   - `ruff`
   - `mypy`
   - `pytest`
   - local smoke script

2. New transport tests
   - fixture equivalence test(s)
   - notebook/export validation test(s)
   - any deterministic notebook generation check

3. Real Kaggle evidence
   - notebook executed on Kaggle
   - saved version created
   - task/benchmark evidence captured

If any of the above is skipped, the summary/audit must say so plainly.

---

## 9. Risks and handling

### Risk 1 — Kaggle local execution is not fully reproducible in GitHub CI

Handle by separating:

- **offline transport validation** in repo CI
- **real platform proof** on Kaggle

Do not blur those two into one claim.

### Risk 2 — Kaggle leaderboard/task model is narrower than LUCID’s native metric model

Handle by keeping the Kaggle task as a transport surface that returns a compatible numeric score while retaining full local diagnostics as LUCID artifacts.

### Risk 3 — Scope creep into benchmark redesign

Handle by freezing to:

- one family
- one notebook
- one benchmark path
- one tiny fixture slice

### Risk 4 — Manual platform steps reduce auditability

Handle by capturing every manual action and artifact in the milestone folder.

---

## 10. Non-negotiable guardrails for Cursor

- Do not change benchmark semantics under the banner of “Kaggle compatibility.”
- Do not add Kaggle-specific meaning into the core benchmark contracts.
- Do not claim Kaggle E2E without actual Kaggle evidence.
- Do not widen family scope in M01.
- Do not weaken CI to get a green merge.
- Do not close the milestone with only local notebook proof.
- Do not push additional non-M01 work after milestone close on the same branch.

---

## 11. Suggested `docs/lucid.md` improvements while touching M01

Make these improvements if they can be done cleanly during the milestone:

1. Add a small **“proof class”** note in the current status area that distinguishes:
   - local deterministic proof
   - repo CI proof
   - external platform proof

2. Add a canonical path entry for the Kaggle notebook/task asset once it exists.

3. Add a short M01 observation line recording the exact Kaggle evidence class achieved (for example: notebook run, task creation, benchmark creation, model evaluation).

These are documentation hardening improvements, not semantic changes.

---

## 12. Closeout prompt to hand Cursor at the end of M01

When implementation is done, give Cursor an explicit closeout instruction roughly equivalent to:

> Close out M01. Generate `M01_summary.md` and `M01_audit.md` using the repository prompts. Update `docs/lucid.md` with final M01 status and evidence pointers. Confirm the final PR head has green CI. Confirm Kaggle platform evidence is committed in the milestone folder. Merge the branch if and only if both repo CI and Kaggle evidence are present. Then create the next milestone folder and seed the next plan/toolcalls stubs on a fresh branch.

