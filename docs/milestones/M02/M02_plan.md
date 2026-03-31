# M02 — Competition charter lock & milestone arc formalization

**Project:** LUCID  
**Milestone:** M02  
**Type:** Docs / governance / planning lock milestone  
**Status:** **Complete** (repository record)  
**Benchmark line:** **1.1.0** (unchanged; no semantic changes in M02)  
**Default branch name (convention):** `m02-competition-charter-lock`

---

## 1. Objective

Convert M02 from a stub into an auditable, competition-facing planning milestone that:

1. Locks the submission strategy around **metacognition under instructional drift**.
2. Formalizes the **planned milestone arc from M02 through M13**.
3. Records the **family priority order** for benchmark expansion (first three families).
4. Defines **promotion / retention / drop rules** for future families.
5. Updates **`docs/lucid.md`** as the authoritative living ledger for the planned arc.
6. Preserves M01 evidence and avoids accidental semantic or scope drift.

---

## 2. Why M02 exists

M01 proved transport and initial hosted-model discrimination but did **not** prove benchmark maturity. The competition rewards dataset quality and task construction most heavily, then novelty and discriminatory power, then writeup quality. LUCID’s moonshot already aligns to the metacognition track; M02 locks the winning posture and sequences work deliberately **before** large benchmark expansion spend.

---

## 3. Scope

### In scope

- Complete `docs/milestones/M02/M02_plan.md` (this file).
- Expand `docs/lucid.md` with competition-facing sections, full **M03–M13** planned arc, active milestone handoff, standing rules.
- Lock the first three benchmark-family priorities in writing.
- Define standing rules for future milestone promotion / drop decisions.
- Update `docs/LUCID_COMPETITION_ALIGNMENT.md` with submission strategy, judging implications, and family priorities.
- Optional M01 hygiene: CI run ID in `M02_toolcalls.md` or `M02_run1.md`; Kaggle permalinks in `M01_run1.md` **only if** already available without rerunning Kaggle.

### Out of scope

- No new benchmark-family implementation.
- No scorer semantics change.
- No notebook transport change.
- No Kaggle rerun required.
- No benchmark version bump (remains **1.1.0**).
- No family-contract authoring beyond planning-level prioritization.
- Do **not** create `docs/milestones/M04/` … `M13/` folders until those milestones open. **M03** may be seeded at formal closeout with **plan + toolcalls stubs only** (per project workflow).

---

## 4. Deliverables

| File | Role |
|------|------|
| `docs/milestones/M02/M02_plan.md` | This plan |
| `docs/milestones/M02/M02_toolcalls.md` | Tool / deliverable log |
| `docs/milestones/M02/M02_run1.md` | Local verification / CI evidence pointer |
| `docs/milestones/M02/M02_summary.md` | Closeout summary |
| `docs/milestones/M02/M02_audit.md` | Closeout audit |
| `docs/lucid.md` | Authoritative ledger update |
| `docs/LUCID_COMPETITION_ALIGNMENT.md` | Expanded alignment & strategy |

---

## 5. Benchmark family priorities (locked)

1. **Family 1:** Symbolic negation / local rule reversal — transport proved in M01; fastest path to scale.
2. **Family 2:** Contradiction / clarification — metacognitive honesty, abstention, recovery.
3. **Family 3:** Scope / precedence / exception drift — broadens drift taxonomy within the same faculty thesis.

---

## 6. Planned milestone arc (reference)

| Milestone | Goal |
|-----------|------|
| **M03** | Family 1 scale-up — symbolic negation / local rule-reversal dataset expansion |
| **M04** | Family 1 analytics — difficulty ladder, spread analysis, promotion decision |
| **M05** | Family 2 — contradiction / clarification benchmark family |
| **M06** | Family 3 — scope / precedence / exception drift family |
| **M07** | Unified benchmark pack normalization across families |
| **M08** | Defensibility, QA, contamination-resistance hardening |
| **M09** | Expanded Kaggle evidence run on mature benchmark |
| **M10** | Writeup evidence pack, figures, judge-facing narrative |
| **M11** | Submission lock — final benchmark freeze and checklist |
| **M12** | Contingency A — platform / benchmark replacement buffer |
| **M13** | Contingency B — final polish / writeup / evidence cleanup buffer |

---

## 7. Exit criteria

- `docs/lucid.md` updated with planned arc, §6 standing competition content, non-stub M02 historical / M03 next sections.
- `M02_plan.md` complete; `LUCID_COMPETITION_ALIGNMENT.md` updated.
- M01 hosted-model ledger in `docs/lucid.md` preserved.
- Local verification green: `ruff`, `mypy`, `pytest`, `scripts/run_local_smoke.py`, `scripts/generate_kaggle_notebook.py --check`.
- `M02_summary.md` and `M02_audit.md` produced.

---

## 8. Authority

Same hierarchy as M01: `docs/LUCID_MOONSHOT.md`, `docs/contracts/`, `docs/lucid.md`, `src/lucid/`.
