# M13 — Run 2 (observed Kaggle benchmark state + M09 restoration posture)

**Branch:** `m13-contingency-buffer`  
**Scope:** Truthful documentation of **observed** Kaggle Community Benchmarks surface vs **M12-intended** linkage; narrow **M09 repair** posture per `docs/milestones/M12/artifacts/m12_contingency_matrix.md`. **No** creation of `lucid_family1_m04_task`. **No** benchmark semantic changes.

## M12 closure reference (unchanged)

| Field | Value |
|-------|--------|
| Authoritative green CI (PR #13) | Run ID **24108099234** — https://github.com/m-cahill/lucid/actions/runs/24108099234 |
| Final PR head | `513d230c0660f1e24b5995abf610e21116048a0f` |
| Merge to `main` | `6211b0c9b0197ab89ac5ddcc5350f3bc4d3840ed` |

---

## A. Intended vs observed (two truths)

### Repo-intended linkage surface (M12 — unchanged in this pass)

`docs/milestones/M12/artifacts/m12_linkage_sources.json` lists **six** LUCID tasks as the submission linkage target:

| Task | Role in repo |
|------|----------------|
| `lucid_main_task` | M01 transport |
| `lucid_family1_m04_task` | M04 Family 1 analytics (notebook generated; **M04 platform run template was never filled** — see `docs/milestones/M04/M04_run2.md`) |
| `lucid_m09_mature_evidence_task` | M09 mature evidence — **prior platform evidence** in `docs/milestones/M09/artifacts/` |
| `lucid_m11_probe_p12_task` | M11 probe |
| `lucid_m11_probe_p24_task` | M11 probe |
| `lucid_m11_probe_p48_task` | M11 probe |

**This pass does not** revise `m12_linkage_sources.json` or regenerate M12 linkage artifacts — deliberate per milestone plan: document platform mismatch; preserve M12 as the **intended** canonical linkage record until a separate decision to formally shrink the linkage target.

### Observed Kaggle benchmark state (operator report — pre-action)

**Benchmark slug:** `michael1232/lucid-kaggle-community-benchmarks`

**Attached (observed):**

- `lucid_main_task`
- `lucid_m11_probe_p12_task`
- `lucid_m11_probe_p24_task`
- `lucid_m11_probe_p48_task`

**Missing from benchmark (observed):**

- `lucid_m09_mature_evidence_task` — treat as **benchmark drift / repairable** (M09 Phase C exports and manifest prove this task existed on-platform historically).
- `lucid_family1_m04_task` — treat as **not evidenced as ever created on Kaggle** (`M04_run2.md` remained TBD); **do not** create in M13.

### Distinction (audit)

| Task | Classification | M13 default |
|------|----------------|-------------|
| `lucid_m09_mature_evidence_task` | Prior platform evidence → **drift** | **Re-attach** in Kaggle owner UI if the task object still exists |
| `lucid_family1_m04_task` | Repo-intended only; no committed platform IDs | **Do not create** in M13 |

---

## B. Platform actions (this repository session)

| Action | Result |
|--------|--------|
| Kaggle owner UI: reattach `lucid_m09_mature_evidence_task` | **Not executed here** — Cursor / CI cannot drive Community Benchmarks UI |
| Public URL / `public_verified` | **Not verified** — URLs remain `null`; `publication_status` unchanged in `m12_linkage_sources.json` |

**Post-action benchmark state:** Same as **Observed pre-action** until the **account owner** completes reattachment in Kaggle and updates this file or a follow-up run log.

---

## C. Operator checklist — restore M09 only (Kaggle)

1. Sign in as benchmark owner (`michael1232`).
2. Open Community Benchmarks for **Measuring Progress Toward AGI**; open benchmark **`michael1232/lucid-kaggle-community-benchmarks`**.
3. Confirm whether **`lucid_m09_mature_evidence_task`** still exists as a task (may be detached vs deleted).
4. If the task exists: **attach** it to this benchmark (do not add default template tasks).
5. If the task was deleted: recreating it is a **new platform object** — document explicitly; do not conflate with “restore” without a decision.
6. **Do not** create or publish **`lucid_family1_m04_task`** as part of this M13 lane.
7. After any change: re-verify attached task list; optionally fill `m12_linkage_sources.json` URLs only when owner-view / logged-out verification supports `public_verified` per `M12_SUBMISSION_RUNBOOK.md`.

Canonical notebook for M09: `notebooks/lucid_kaggle_m09_mature_evidence.ipynb` (regenerate from repo per `docs/lucid.md` §8).

---

## D. Linkage artifacts

| File | Changed in M13 run 2? |
|------|------------------------|
| `m12_linkage_sources.json` | **No** |
| `m12_submission_linkage.json` / `.md` | **No** |
| `m12_public_links.json` | **No** |

Rationale: preserve M12 six-task **intent**; observed platform gap is **documented** here, not silently rewritten into a five-task canonical manifest without explicit product decision.

---

## E. Local verification (this commit)

Documentation-only delta expected; run full gates before push per `M12_SUBMISSION_RUNBOOK.md` §2.
