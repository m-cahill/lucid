# M11 — Hosted-model probe surface, cost/results frontier, and internal response model

**Milestone identity:** M11 — deterministic probe ladder on the mature M09 substrate; transparent empirical response model for hosted models.

**Primary judged axis:** Novelty / insights / discriminatory power  
**Secondary value:** Operational intelligence for final run allocation and submission strategy  
**Benchmark version target:** **1.1.0** (unchanged — no scorer/parser/schema/contract edits)

**Status:** **Repo + ingest pipeline complete** (deterministic `--check` for ladder, roster, notebooks, ingest, tables, figures). **P12 / P24 / P48** platform rows still require new Kaggle runs + leaderboard exports merged via `ingest_m11_platform_exports.py --export ...`. **M12** owns final benchmark/task/writeup linkage.

---

## Objective

Spend the remaining competition run budget on a **deterministic, auditable internal model** of hosted-model behavior on LUCID by measuring, for each **tracked** model (33-authoritative roster from M09-normalized artifacts):

* completion vs non-completion by probe tier
* score behavior as panel size increases (P12 → P24 → P48 → P72)
* repeatability on the **P12 repeat lane** (same episodes as P12)
* opportunistic cost/latency metadata when the platform exposes fields; otherwise `NA` + reason code
* explicit failure taxonomy when fields are absent

**Out of scope:** Inferring family/difficulty/component claims from aggregate M09 exports; benchmark semantic changes; benchmark version bump; fabricating Phase 2–4 evidence in-repo.

---

## Probe ladder (nested)

All tiers are **subsets of** the M09 mature 72-episode panel (`m09_mature_evidence_v1`), selected **within each M09 family block** by difficulty bucket (first *N* by sorted `unified_episode_id`), then reordered to **M09 block order**.

| Tier | Episodes | Per-family allocation (difficulty) |
|------|----------|--------------------------------------|
| **P12** | 12 | LOW 1, MEDIUM 2, HIGH 1 (4 per family); MEDIUM +1 vs 3×3 base |
| **P24** | 24 | LOW 2, MEDIUM 3, HIGH 3 (8 per family) |
| **P48** | 48 | LOW 5, MEDIUM 6, HIGH 5 (16 per family) |
| **P72** | 72 | Identical to M09 (`m09_eval_rows()`) |

**Repeat lane:** `P12_repeat = P12` (same `unified_episode_id` set and notebook/task surface for P12).

**Code:** `src/lucid/kaggle/m11_probe_panels.py`  
**Artifacts:** `docs/milestones/M11/artifacts/m11_probe_ladder.json`, `m11_roster_canonical.json`

---

## Kaggle surfaces (Phase 1 repo)

| Notebook (generated) | Task name |
|----------------------|-----------|
| `notebooks/lucid_kaggle_m11_probe_p12.ipynb` | `lucid_m11_probe_p12_task` |
| `notebooks/lucid_kaggle_m11_probe_p24.ipynb` | `lucid_m11_probe_p24_task` |
| `notebooks/lucid_kaggle_m11_probe_p48.ipynb` | `lucid_m11_probe_p48_task` |
| `notebooks/lucid_kaggle_m09_mature_evidence.ipynb` | `lucid_m09_mature_evidence_task` (P72 / M09 comparable) |

**Generator:** `scripts/generate_m11_kaggle_notebooks.py` (`--write` / `--check`)

---

## Phases

| Phase | Scope |
|-------|--------|
| **1** | Charter, probe code, ladder + roster JSON, probe notebooks, CI `--check`, runbook scaffolding, ingest/table/figure script stubs |
| **2** | Ten-day Kaggle execution cadence (see `M11_KAGGLE_RUNBOOK.md`); platform runs only |
| **3** | `ingest_m11_platform_exports.py`, `generate_m11_tables.py`, optional figures; normalized CSV/JSON + policy docs under `docs/milestones/M11/artifacts/` |
| **4** | Closeout docs (`M11_run1.md`, `M11_summary.md`, `M11_audit.md`); ledger; seed **M12** (linkage + contingency) |

---

## Deferred to M12

**Final Kaggle benchmark / task / writeup linkage** per competition rules — moved from the old M11 “submission lock” stub to **M12** (`docs/milestones/M12/M12_plan.md`).

---

## Acceptance criteria (full milestone)

See user charter: green CI; benchmark 1.1.0 unchanged; nested panels committed and `--check`-verified; every tracked model has ≥1 normalized M11 row with status + provenance; response-surface + allocation policy; `docs/lucid.md` + `LUCID_COMPETITION_ALIGNMENT.md` updated; audit posture explicit on deferrals.
