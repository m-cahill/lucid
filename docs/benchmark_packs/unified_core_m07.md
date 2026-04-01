# Unified benchmark pack — `unified_core_m07_v1`

**Project:** LUCID  
**Pack ID:** `unified_core_m07_v1`  
**Normalization version:** `1.0.0` (schema / process — not benchmark semantics)  
**Benchmark version:** **1.1.0** (unchanged)  
**Role:** First canonical **cross-family** offline benchmark artifact: normalized metadata and lineage over the three existing family core packs, without reauthoring episodes.

---

## 1. What this pack is

`unified_core_m07_v1` is a **faithful composition** of:

| Source pack | Family (`template_family`) | Episodes |
|-------------|------------------------------|----------|
| `family1_core_m03_v1` | `symbolic_negation_v1` | 96 |
| `family2_core_m05_v1` | `contradiction_clarification_v1` | 72 |
| `family3_core_m06_v1` | `scope_precedence_exception_v1` | 72 |
| **Total** | | **240** |

Every source episode appears **exactly once**. Nothing is omitted, duplicated, or semantically edited. The nested `episode_spec` in each unified row is the **full** source episode spec (deep-copied for the manifest).

---

## 2. Non-goals

- **No** new episode generation for Families 1–3.
- **No** Kaggle notebook, task, or platform proof.
- **No** scorer, parser, output-schema, or benchmark-version changes.
- **No** cross-family difficulty **equivalence** claim (see §6).
- **No** change to standing family verdicts (**retain provisionally** for all three).

---

## 3. Normalized row fields

Each episode row includes at least:

| Field | Description |
|-------|-------------|
| `unified_episode_id` | Deterministic ID: `u_<source_pack_id>__<source_episode_id>` |
| `family_id` | Template family id |
| `source_pack_id` | e.g. `family1_core_m03_v1` |
| `source_episode_id` | `episode_spec.episode_id` from the source pack |
| `difficulty` | `LOW` / `MEDIUM` / `HIGH` (from `difficulty_profile`) |
| `drift_type` | Primary drift enum (e.g. `NEGATION`, `CONTRADICTION`, …) |
| `family_variant` | Cross-family analytics tag (see §4) |
| `final_state_unresolved` | From `episode_spec` |
| `acceptable_final_modes` | From `episode_spec` |
| `target_behavior` | From `difficulty_profile` |
| `source_seed` | `generation_seed` |
| `source_template_version` | `template_version` |
| `source_episode_spec_hash` | SHA-256 of canonical JSON of **only** `episode_spec` |
| `episode_spec` | Full original source spec |
| `normalization_version` | `1.0.0` |

**Family 1 note:** Source M03 rows do not duplicate `family_id` / `drift_type` at the top level; unified normalization **reads** those from the nested `episode_spec`. Source family manifests are **not** modified in M07.

---

## 4. `family_variant` mapping (analytics only)

| Family | `family_variant` values |
|--------|-------------------------|
| Family 1 | `negation` |
| Family 2 | `unresolved`, `resolved` |
| Family 3 | `scope`, `precedence`, `exception` |

This does **not** replace `drift_type`; it supports packing and slicing only.

---

## 5. Canonical ordering

1. **Difficulty:** `LOW`, then `MEDIUM`, then `HIGH`.
2. **Within each difficulty:** Family **1**, then **2**, then **3**.
3. **Within each family block:** Same order as that family’s canonical manifest.

This yields **80 / 80 / 80** LOW / MEDIUM / HIGH overall.

---

## 6. Difficulty labels — nominal only

**LOW / MEDIUM / HIGH** are **normalized nominal labels** carried through consistently across families. M07 does **not** claim that e.g. LOW in Family 1 is psychometrically equivalent to LOW in Families 2 or 3. Treat cross-family difficulty comparisons as **structural**, not as calibrated human difficulty.

---

## 7. Artifacts and commands

| Artifact | Path |
|----------|------|
| Committed manifest | `tests/fixtures/unified_core_m07/unified_core_m07_manifest.json` |
| Pack module | `src/lucid/packs/unified_core_m07.py` |
| Manifest script | `scripts/generate_unified_core_m07_manifest.py` (`--write` / `--check`) |
| Unified smoke | `scripts/run_unified_pack_smoke.py` (9 episodes) |
| Structural stats | `docs/milestones/M07/artifacts/unified_pack_stats.json` |
| M08 defensibility audit artifacts | `docs/milestones/M08/artifacts/` (`m08_defensibility_audit.json`, `m08_duplicate_scan.json`, `m08_defensibility_summary.md`, `m08_contamination_posture.md`) |
| Defensibility standard | `docs/benchmark_quality/LUCID_DEFENSIBILITY_STANDARD.md` |

**Regenerate manifest (maintainers):**

```bash
python scripts/generate_unified_core_m07_manifest.py --write
```

**Verify (CI):**

```bash
python scripts/generate_unified_core_m07_manifest.py --check
```

**M08 defensibility audit (CI):**

```bash
python scripts/run_unified_defensibility_audit.py --write   # maintainers — refresh committed artifacts
python scripts/run_unified_defensibility_audit.py --check  # merge gate (matches committed artifacts)
```

---

## 8. Expected structure (audit)

- **240** episodes total.
- **Drift types:** `NEGATION` 96; `CONTRADICTION` 72; `SCOPE` / `PRECEDENCE` / `EXCEPTION` 24 each.
- **Final states:** 36 episodes with `final_state_unresolved` true (Family 2 unresolved rows); 204 resolved.

Full counts are summarized in `unified_pack_stats.json` and enforced in `tests/test_unified_core_m07_pack.py`.
