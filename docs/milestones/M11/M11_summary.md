# Milestone Summary — M11: Hosted-model probe surface (repo + ingest)

**Project:** LUCID  
**Milestone:** M11  
**Status:** **Repo + ingest complete**; **P12 / P24 / P48** leaderboard rows still **pending** new Kaggle exports  
**Benchmark version:** **1.1.0** (unchanged)  
**Notebook pin SHA:** `13137d907e938c6ed36c2b17eb0c4347f2d3943c`

---

## 1. Objective (definition of done for this increment)

Deliver a **deterministic, auditable** pipeline from Kaggle leaderboard CSV(s) to normalized **model × probe_tier** rows, plus allocation policy and a completion-by-tier figure, **without** benchmark semantic changes.

---

## 2. What shipped

| Area | Evidence |
|------|------------|
| Probe ladder code | `src/lucid/kaggle/m11_probe_panels.py` |
| Ladder + roster JSON | `docs/milestones/M11/artifacts/m11_probe_ladder.json`, `m11_roster_canonical.json` |
| Probe notebooks | `notebooks/lucid_kaggle_m11_probe_p12.ipynb`, `p24`, `p48` |
| Ingest | `scripts/ingest_m11_platform_exports.py`, `scripts/m11_ingest_common.py` |
| Response surface | `m11_model_response_surface.json` / `.csv` |
| Completion frontier | `m11_completion_frontier.csv` |
| Taxonomy + manifest | `m11_failure_taxonomy.md`, `m11_probe_run_manifest.md` |
| Allocation policy | `m11_allocation_policy.md` |
| Analytical summary | `m11_analytical_summary.md` (`scripts/generate_m11_tables.py`) |
| Figure | `docs/milestones/M11/artifacts/figures/m11_fig_completion_by_tier.png` |
| Tests | `tests/test_m11_ingest.py` |
| Ledger | `docs/lucid.md`, `docs/LUCID_COMPETITION_ALIGNMENT.md` |

---

## 3. Honest evidence boundary

* **P72:** Populated from committed M09 leaderboard export — **15** / **33** `completed`, **18** `platform_limited` (same story as M09 closeout).
* **P12 / P24 / P48:** **No** task rows in the default committed export → all **33** models show `export_missing` for those tiers until new CSVs are merged.
* **Cost / latency:** Not present in CSV columns used → `NA` in normalized surface with explicit fields.

---

## 4. Deferred

* **M12** — final benchmark / task / writeup linkage (`docs/milestones/M12/M12_plan.md`).

---

## 5. Operator follow-up

Run probe ladder on Kaggle; add exports; `ingest_m11_platform_exports.py --write` with `--export` pointed at new file(s); commit artifacts.
