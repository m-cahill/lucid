# M04 hosted-model evidence — M09 disposition

**Decision (organizational):** **Superseded by M09** (with explicit limits below).

---

## Rationale

The open gap referenced in `docs/lucid.md` and M04 closeout was **populated hosted-model spread** on the **M04 Family 1** 24-episode panel (`family1_model_scores.csv`).

M09 defines a **deterministic 72-episode** evidence panel (`m09_mature_evidence_v1`) on the **mature unified** benchmark (`unified_core_m07_v1`), whose **Family 1 slice is exactly the M04 decision rows** (same seeds and severities, mapped to `unified_episode_id`). That makes M09 the **authoritative successor surface** for hosted-model discriminatory evidence on the mature pack: **chasing a separate M04-only CSV** is no longer the right default; evidence lands under **`docs/milestones/M09/artifacts/`**.

---

## Operational closure (M09 closeout)

- **`m09_model_scores.csv`** is **populated** from the ingested leaderboard export (`m09_kaggle_leaderboard_export.csv`): **15** completing models + **18** non-completions documented with explicit status (see `m09_kaggle_run_manifest.md`).
- **`family1_model_scores.csv`** is **still not backfilled** — M09 closeout does **not** duplicate rows into the M04 artifact; the **mature** evidence path is authoritative for new analysis.

**Full discriminatory closure** (numeric score for **every** tracked hosted model on the M09 task) is **not** claimed: **18** models lack M09 numeric means in the export. That is an **evidence breadth** limit, not proof of a benchmark bug.

---

## Silence check

This is **not** a silent rewrite of M04 history. M04 artifacts and narrative remain; M09 states explicitly where evidence must land next.
