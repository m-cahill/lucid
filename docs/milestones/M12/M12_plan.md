# M12 Plan — Final benchmark / task / writeup linkage and authoritative submission pack

## Milestone identity

| Field | Value |
|-------|--------|
| **Milestone** | M12 |
| **Primary judged axis** | Writeup quality and submission readiness |
| **Secondary judged axis** | Novelty / insights / discriminatory power (presentation integrity only; no new semantic evidence claims) |
| **Benchmark version** | **1.1.0** locked; no scoring, parser, family, or benchmark-semantic changes in scope |
| **Default branch posture** | `m12-final-linkage` |
| **CI posture** | Green at milestone close |

## Why this milestone exists

M11 is closed, its authoritative closeout is green, and the ledger has already promoted **M12** to the active milestone for final benchmark / task / writeup linkage. The next step is to turn the current benchmark, notebooks, tasks, evidence, and judge-facing writeup into one authoritative competition-facing package without reopening benchmark semantics or the M11 probe program. Some uploaded M11 artifacts also appear internally inconsistent with the closed M11 summary/audit surface, so M12 must explicitly clean up the authoritative evidence surface before final linkage.

## Resolved scope decisions

1. **M12 is a linkage / packaging milestone, not a new evidence-generation milestone.** Do not change benchmark semantics, family composition, scoring profile, parser behavior, or notebook task logic except where a deterministic linkage/manifest fix is required.
2. **Do not reopen M11 probe execution by default.** Only add a narrow contingency lane for publication/visibility/metadata repairs or an explicitly authorized final hosted-model benchmark run if the competition surface truly requires it.
3. **Treat the M11 closeout surface as authoritative** (`M11_run2.md`, `M11_summary.md`, `M11_audit.md`, `docs/lucid.md`) when it conflicts with older or stale derived artifacts.
4. **Keep M12 small enough to close cleanly.** Any post-closeout polish that is not strictly required for final linkage goes to **M13** on a new branch.

## External rule assumptions to verify and encode

Before implementing, verify the current Kaggle competition-facing rules and record them inside M12 artifacts. As of the current public Kaggle surface, the competition requires a **Kaggle Benchmark** with underlying authored tasks, and the benchmark must be linked in the writeup as the project link. Current Kaggle benchmark documentation centers benchmark creation around creating a benchmark and adding tasks, and a competition discussion indicates a benchmark may comprise **one or more tasks**. Another current competition discussion recommends running all available models for a richer signal, but that reads as guidance rather than a hard rule. Capture these facts in the M12 run log with citations and do not rely on memory.

## Goals

1. Produce a **single authoritative linkage manifest** connecting benchmark **1.1.0**, final Kaggle benchmark object, included tasks, source notebooks and pins, final writeup artifact(s), public project link(s), and supporting M09/M10/M11 evidence artifacts.
2. Make the linkage **deterministic and CI-checkable** via a generated artifact and `--check` guardrail.
3. Clean up **authoritative evidence pointers** so the final submission pack does not mix closed M11 facts with stale pre-closeout placeholders.
4. Ship a **submission-facing runbook/checklist** so the final Kaggle linkage can be audited and repeated without improvisation.
5. Close M12 with green CI, explicit run records, summary, audit, and seeded M13 stub documents.

## Out of scope

* No benchmark version bump.
* No changes to `LUCID_SCORING_PROFILE v1.1.0` semantics.
* No new benchmark families.
* No parser rescue or prompt rescue for excluded M11 models.
* No broad rerun of M11 probes unless explicitly authorized and documented as an exception.
* No post-closeout doc-only commits on the M12 branch if they can reasonably wait for M13.

## Workstreams

### Workstream A — Authoritative inventory and evidence-surface cleanup

**Objective:** build a clean inventory of every competition-facing object and resolve internal pointer drift.

**Tasks**

1. Inventory all final-linkage surfaces and record exact current state.
2. Compare uploaded M11 analytical / allocation derivative files against the authoritative closeout docs and determine status: `authoritative_current`, `superseded_historical`, or `requires_regeneration`.
3. Add a machine-readable evidence-surface manifest.
4. Update `docs/lucid.md` so the M12 section points only to authoritative M11 closeout artifacts and the new M12 linkage artifacts.

**Outputs**

* `docs/milestones/M12/artifacts/m12_evidence_surface_manifest.json`
* `docs/milestones/M12/artifacts/m12_evidence_surface_notes.md`

### Workstream B — Deterministic submission-linkage manifest + CI guardrail

**Objective:** create a single source of truth for benchmark/task/writeup linkage.

**Tasks**

1. Implement `scripts/generate_m12_submission_linkage.py --write` / `--check`.
2. Emit machine-readable JSON and human-readable Markdown from the same build.
3. Capture benchmark version, benchmark slug/URLs/status, task names, notebook pins, manifest hashes, writeup paths, evidence pointers, and pending publication fields.
4. Add tests and CI `--check` gating.

**Outputs**

* `scripts/generate_m12_submission_linkage.py`
* `tests/test_m12_submission_linkage.py`
* `docs/milestones/M12/artifacts/m12_submission_linkage.json`
* `docs/milestones/M12/artifacts/m12_submission_linkage.md`

### Workstream C — Final competition-facing writeup linkage

**Objective:** make the final submission artifacts point to the exact benchmark object and task set.

**Tasks**

1. Update the judge-facing narrative pack only where needed for links and naming.
2. Create a concise final-linkage note (checklist + public links JSON).
3. Ensure every external URL used in final-linkage docs appears in the machine-readable linkage manifest (or is explicitly null with honest publication status).

**Outputs**

* `docs/milestones/M12/artifacts/m12_submission_checklist.md`
* `docs/milestones/M12/artifacts/m12_public_links.json`
* Minimal targeted edits to the M10 narrative pack and `docs/lucid.md`

### Workstream D — Runbook, verification, and contingency lane

**Outputs**

* `docs/milestones/M12/M12_SUBMISSION_RUNBOOK.md`
* `docs/milestones/M12/artifacts/m12_contingency_matrix.md`

## CI / verification requirements

1. Existing repo quality gates (`ruff`, `pytest`, generator `--check`, notebook checks, etc.).
2. New `generate_m12_submission_linkage.py --check` step.
3. Tests for M12 linkage logic.
4. Generated docs/artifacts reproducible and checked in CI.

## Deliverables (minimum)

* `docs/milestones/M12/M12_plan.md` (this file)
* `docs/milestones/M12/M12_run1.md`
* `docs/milestones/M12/M12_summary.md`
* `docs/milestones/M12/M12_audit.md`
* `docs/milestones/M12/M12_toolcalls.md`
* `docs/milestones/M12/M12_SUBMISSION_RUNBOOK.md`
* `docs/milestones/M12/artifacts/m12_submission_linkage.json`
* `docs/milestones/M12/artifacts/m12_submission_linkage.md`
* `docs/milestones/M12/artifacts/m12_evidence_surface_manifest.json`
* `docs/milestones/M12/artifacts/m12_submission_checklist.md`
* Minimal targeted updates to `docs/lucid.md` and the M10 narrative pack

## Acceptance criteria

1. Benchmark semantics unchanged; version **1.1.0**.
2. Single authoritative linkage source exists (generated, checked-in manifest).
3. No fake external IDs or URLs; unpublished items marked pending or owner-unverified.
4. Competition-facing link path is explicit (Kaggle benchmark primary; GitHub secondary).
5. Authoritative evidence surface cleaned up vs superseded M11 placeholders.
6. CI green on closing commit.
7. Closeout docs complete; ledger marks M12 closed / M13 active.
8. M13 seeded with stub plan and toolcalls on a new branch if follow-up work remains.

## Decision rule if ambiguity remains

If ambiguity about whether a file is authoritative remains, prefer:

1. `docs/lucid.md`
2. `M11_run2.md`
3. `M11_summary.md`
4. `M11_audit.md`
5. Generated machine-readable artifacts explicitly referenced by the ledger
