# M07 Plan — Unified benchmark pack normalization across families

**Milestone:** M07  
**Branch:** `m07-unified-benchmark-pack-normalization`  
**Primary judged axis:** **Dataset quality & task construction**  
**Benchmark version target:** **1.1.0** unchanged unless an explicit change-control path is opened  
**Milestone posture:** Small, deterministic, offline packaging and normalization milestone. No Kaggle platform work, no hosted-model claims, no scorer/output-schema changes.

## 1. Objective

Create the first **canonical unified benchmark pack** that composes the three existing offline family packs into one normalized, audit-ready benchmark artifact, without changing any episode semantics or family-level contracts.

**Families composed:**

- **Family 1:** `symbolic_negation_v1` — `family1_core_m03_v1` (96)
- **Family 2:** `contradiction_clarification_v1` — `family2_core_m05_v1` (72)
- **Family 3:** `scope_precedence_exception_v1` — `family3_core_m06_v1` (72)

**Unified pack name:** `unified_core_m07_v1` — **240** episodes total.

## 2. Implementation locks (Cursor)

- **`unified_episode_id`:** `u_<source_pack_id>__<source_episode_id>` (do not reuse source id as unified id).
- **`source_episode_spec_hash`:** SHA-256 of canonical JSON of **`episode_spec` only** (`lucid.canonical_json.dumps_canonical`).
- **`normalization_version`:** `1.0.0` (normalization schema/process; not benchmark version).
- **Family 1:** Extract missing top-level fields from nested `episode_spec`; **do not** mutate Family 1 source manifest.
- **CI:** Add `python scripts/generate_unified_core_m07_manifest.py --check` to existing workflow (same pattern as Families 1–3).
- **Docs:** `docs/benchmark_packs/unified_core_m07.md` in new `docs/benchmark_packs/`.
- **No renumbering or rebalancing** — full 96 + 72 + 72 composition only.
- **Difficulty:** Document **nominal** normalization only — not psychometric cross-family equivalence.

## 3. Deliverables (checklist)

- [x] `src/lucid/packs/unified_core_m07.py`
- [x] `src/lucid/runner_unified.py`
- [x] `scripts/generate_unified_core_m07_manifest.py` (`--write` / `--check`)
- [x] `scripts/run_unified_pack_smoke.py`
- [x] `tests/fixtures/unified_core_m07/unified_core_m07_manifest.json`
- [x] `tests/test_unified_core_m07_pack.py`
- [x] `docs/benchmark_packs/unified_core_m07.md`
- [x] `docs/milestones/M07/artifacts/unified_pack_stats.json`
- [x] CI manifest check
- [x] Ledger / alignment / operating manual updates
- [x] `M07_summary.md`, `M07_audit.md`, `M07_run1.md` (PR + CI evidence)

## 4. Ordering rule

1. Difficulty: `LOW`, `MEDIUM`, `HIGH`  
2. Family priority: 1 → 2 → 3  
3. Source pack local order within each family block  

## 5. Unified smoke

**9 episodes:** all three families; all three difficulty buckets; Family 2 `unresolved` + `resolved`; Family 3 `scope` / `precedence` / `exception`.

## 6. Verification commands

See `docs/milestones/M07/M07_run1.md` (full local + CI record at closeout).

Minimum set includes: ruff, pytest, wheel verify, all family manifest `--check` scripts, unified `generate_unified_core_m07_manifest.py --check`, `run_unified_pack_smoke.py`, and existing notebook generators.

## 7. Out of scope

New episode logic; edits to family semantics; Kaggle; hosted-model sweeps; M04 CSV backfill; family verdict changes; benchmark version bump.

## 8. Closeout (post-merge)

Generate `M07_summary.md`, `M07_audit.md`, record CI URLs in `M07_run1.md`, update `docs/lucid.md` (M07 complete, M08 next, inventory row), honest posture: **pack normalization only** — no Kaggle proof, no submission-readiness claim.
