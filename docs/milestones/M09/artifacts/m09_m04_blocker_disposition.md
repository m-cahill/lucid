# M04 hosted-model evidence — M09 disposition

**Decision (organizational):** **Superseded by M09** (with explicit limits below).

---

## Rationale

The open gap referenced in `docs/lucid.md` and M04 closeout was **populated hosted-model spread** on the **M04 Family 1** 24-episode panel (`family1_model_scores.csv`).

M09 defines a **deterministic 72-episode** evidence panel (`m09_mature_evidence_v1`) on the **mature unified** benchmark (`unified_core_m07_v1`), whose **Family 1 slice is exactly the M04 decision rows** (same seeds and severities, mapped to `unified_episode_id`). That makes M09 the **authoritative successor surface** for hosted-model discriminatory evidence on the mature pack: **chasing a separate M04-only CSV** is no longer the right default; evidence should be recorded under **`docs/milestones/M09/artifacts/`** once platform runs exist.

---

## What is *not* claimed here

- **`family1_model_scores.csv` is not backfilled** in this milestone.
- **Full discriminatory closure** (hosted scores in repo) is **not** achieved until **`m09_model_scores.csv`** contains real platform rows (see `m09_kaggle_run_manifest.md`).

So: **M04-specific artifact** gap is **superseded in intent** by M09; **operational closure** of the **hosted-model evidence blocker** still requires a **completed M09 Kaggle run** and committed scores.

---

## Silence check

This is **not** a silent rewrite of M04 history. M04 artifacts and narrative remain; M09 states explicitly where evidence must land next.
