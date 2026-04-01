# M09 — Kaggle platform run manifest

**Panel ID:** `m09_mature_evidence_v1`  
**Task name (notebook):** `lucid_m09_mature_evidence_task`  
**Benchmark version:** 1.1.0  

---

## Run status (this repository revision)

**Platform execution:** **Not recorded for this milestone closeout.**

No hosted-model scores, Kaggle notebook URL, or benchmark/task URLs were supplied in the materials available when this document was written. Per project honesty rules, **no fabricated** notebook versions, roster entries, or scores appear in `m09_model_scores.csv` or related CSVs.

**Phase B (repo) is complete:** deterministic panel, `m09_model_panel.json`, generated notebook, CI `--check` for panel + notebook.

**Phase C–E (Kaggle platform proof + CSV ingestion)** remain **blocked** until a maintainer:

1. Pushes a branch whose **HEAD** commit contains `src/lucid/kaggle/m09_evidence_panel.py`.
2. Regenerates `notebooks/lucid_kaggle_m09_mature_evidence.ipynb` with `--pin-sha` set to that **same** HEAD SHA (so the GitHub ZIP install matches the code).
3. Uploads the notebook to Kaggle, defines task `lucid_m09_mature_evidence_task`, runs the tracked hosted-model roster.
4. Exports results and appends rows to:
   - `m09_model_scores.csv`
   - `m09_component_metrics.csv` (if the platform exposes D/L/O/A/C per episode)
   - `m09_family_breakdown.csv`
   - `m09_difficulty_breakdown.csv`
5. Updates **this manifest** with canonical links, roster, run date, and any failures/skips.

See `docs/milestones/M09/M09_KAGGLE_RUNBOOK.md`.

---

## Fields to fill after the first real run

| Field | Value (when known) |
|-------|---------------------|
| Notebook URL / Kaggle identifier | *TBD* |
| Notebook version (40-char repo SHA in banner) | *TBD — must match commit that ships `m09_evidence_panel`* |
| Benchmark / task linkage | *TBD* |
| Run date (UTC) | *TBD* |
| Hosted-model roster (actual) | *TBD* |
| Models skipped / failed | *TBD or “none”* |
| Run completeness | *TBD — complete / partial / blocked* |

---

## Proof-class note

**Kaggle platform proof** for M09 is **not** claimed in this ledger revision. **Local + GitHub CI proof** applies to generators and `--check` parity only.
