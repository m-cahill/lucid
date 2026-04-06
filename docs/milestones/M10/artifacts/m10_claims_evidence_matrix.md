# M10 — Claims ↔ evidence matrix

**Benchmark version:** 1.1.0  
**Purpose:** Map major submission claims to **committed** artifacts and proof classes.

| Claim | Artifact / source | Proof class | Limitation |
|--------|---------------------|-------------|------------|
| LUCID targets **metacognition** (drift detection, calibration, recovery), not solver performance | `docs/LUCID_MOONSHOT.md`, `docs/lucid.md` §1 | Local / docs | — |
| Scoring semantics locked at **v1.1.0** | `docs/contracts/LUCID_SCORING_PROFILE_v1.1.0.md`, `docs/lucid.md` §5 | Local / docs | — |
| **Deterministic** synthetic episodes and manifests for core packs | `tests/fixtures/*_manifest.json`, `scripts/generate_*_manifest.py --check` | Local + **CI** | — |
| **Unified** 240-episode pack composes three families with lineage | `tests/fixtures/unified_core_m07/unified_core_m07_manifest.json`, `docs/benchmark_packs/unified_core_m07.md` | Local + **CI** | No cross-family psychometric equivalence claim |
| **M08** defensibility audit passes; hard checks block CI | `docs/milestones/M08/artifacts/m08_defensibility_summary.md`, `m08_defensibility_audit.json`, `scripts/run_unified_defensibility_audit.py --check` | Local + **CI** | Soft similarity findings are informational |
| **Contamination resistance** is structural (synthetic, auditable), not absolute | `docs/milestones/M08/artifacts/m08_contamination_posture.md` | Local / docs | Public repo visibility acknowledged |
| **M01** Kaggle Community Benchmarks **E2E** with hosted models | `docs/milestones/M01/M01_run1.md`, `docs/lucid.md` §6 score ledger | **Kaggle platform** | Ledger is **M01** slice; not the mature panel |
| **M09** mature panel definition (72 episodes) is repo-deterministic | `src/lucid/kaggle/m09_evidence_panel.py`, `docs/milestones/M09/artifacts/m09_model_panel.json` | Local + **CI** | — |
| **M09** hosted **aggregate** means ingested from platform export | `m09_kaggle_leaderboard_export.csv` → `m09_model_scores.csv` | **Kaggle platform** | **15**/33 numeric M09 means; **18** non-completions |
| **No** family/difficulty/component breakdown from export | `m09_family_breakdown.csv`, `m09_difficulty_breakdown.csv`, `m09_component_metrics.csv`, `m09_kaggle_run_manifest.md` | **Kaggle platform** | Placeholders / NA |
| Strongest code linkage for published notebook is path + task + benchmark slug + pin SHA | `m09_kaggle_run_manifest.md` | Docs | Exact Kaggle notebook URL/version **not** in export |
| **M10** figures/tables reproduce from committed inputs | `scripts/generate_m10_figures.py --check`, `scripts/generate_m10_tables.py --check` | Local + **CI** | PNG bytes tied to generator + matplotlib version |

**Proof class legend:** **Local** = machine/regenerator; **CI** = GitHub Actions; **Kaggle platform** = exported / hosted run records.
