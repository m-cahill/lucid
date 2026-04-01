# Milestone Summary — M07: Unified benchmark pack normalization across families

**Project:** LUCID  
**Phase:** Benchmark construction (locked roadmap)  
**Milestone:** M07 — Unified offline pack (`unified_core_m07_v1`)  
**Timeframe:** 2026-03-31 → 2026-04-01 (repository record)  
**Status:** **Closed** — merged to `main` (`07e349ef7ff68cad79be3c41bb94839045fe18b3`)  
**Baseline reference:** `main` at pre-M07 (`ba4edeb6bb49cf3a05875a47fa080e966d7dd713`); PR #8 head `b5109f7de6f87039f3e671dad8c378fe64e05784`

---

## 1. Milestone Objective

Deliver the first **canonical unified offline benchmark pack** that composes the three existing family core packs (`family1_core_m03_v1`, `family2_core_m05_v1`, `family3_core_m06_v1`) into a single normalized, audit-ready artifact (**240** episodes) with deterministic ordering, explicit source lineage, per-episode `source_episode_spec_hash`, and CI-enforced manifest regeneration — **without** reauthoring episodes, changing scorer/parser contracts, or claiming Kaggle platform proof.

**Gap addressed:** After M06, families had strong standalone manifests but no single cross-family normalized pack suitable for downstream defensibility and evidence milestones.

---

## 2. Scope Definition

### In scope

- `src/lucid/packs/unified_core_m07.py` — composition, ordering, normalization helpers, smoke id panel, stats builder
- `src/lucid/runner_unified.py` — dispatch to existing family runners
- `scripts/generate_unified_core_m07_manifest.py` (`--write` / `--check`), `scripts/run_unified_pack_smoke.py`
- Committed manifest `tests/fixtures/unified_core_m07/unified_core_m07_manifest.json`
- Tests `tests/test_unified_core_m07_pack.py` (determinism, lineage, hashes, ordering, smoke, scorer regression)
- CI: unified manifest `--check` in `.github/workflows/ci.yml`
- Docs: `docs/benchmark_packs/unified_core_m07.md`, `docs/milestones/M07/artifacts/unified_pack_stats.json`, ledger updates (`docs/lucid.md`, `docs/LUCID_COMPETITION_ALIGNMENT.md`, `docs/LUCID_OPERATING_MANUAL.md`)
- M08 stubs: `docs/milestones/M08/` including `M08_run1.md`

### Out of scope

- New episode generation for Families 1–3; edits to source family manifests (except unrelated regeneration)
- Kaggle notebook/task or hosted-model evidence
- Scorer, parser, output schema, or benchmark version change (remains **1.1.0**)
- M04 deferred `family1_model_scores.csv` backfill
- Family verdict changes (all remain **retain provisionally**)

---

## 3. Work Executed

- **Implementation:** Unified pack module + runner; 240-row manifest; 18 new tests (pytest total **92**); additive CI step.
- **Docs:** Cross-family pack spec, unified inventory table with **source pack lineage**, M07 plan/run/summary/audit alignment, M08 seeded.
- **Mechanical vs semantic:** Packaging and metadata normalization only; **no** scoring-profile or benchmark semantic bump.

---

## 4. Validation & Evidence

- **Local:** Full command set in `M07_run1.md` §1 — all exit **0**; pytest with coverage gate **≥85%** on `lucid` (~92.5%).
- **CI (PR):** Run `23831550017` — **success** on head `b5109f7…`.
- **CI (`main`):** Run `23831565243` — **success** on merge `07e349e…`.

Failures: none.

---

## 5. CI / Automation Impact

- **Added:** `python scripts/generate_unified_core_m07_manifest.py --check` in `CI` workflow (`lint-test` job).
- **Unchanged:** Ruff, mypy, pytest+coverage, wheel verify, both Kaggle notebook generators, Family 1–3 manifest checks.

---

## 6. Issues & Exceptions

No new issues blocked completion.

---

## 7. Deferred Work

- **Family 1 hosted-model CSV:** Still deferred from M04 — not part of M07.
- **M08 defensibility / contamination:** Next planned milestone per `docs/lucid.md` §7.

---

## 8. Governance Outcomes

- **Provable:** Unified manifest regenerates deterministically; each `episode_spec` hash-audited; source episodes appear exactly once.
- **Ledger:** Unified pack inventory + M07 judged axis recorded; M08 listed as next; benchmark **1.1.0** unchanged.
- **Honest scope:** **Local + CI proof only** for M07 — no Kaggle platform claim.

---

## 9. Exit Criteria Evaluation

| Criterion | Met? | Evidence |
|-----------|------|----------|
| 240 episodes, full composition | Met | Pack module + tests + manifest |
| Manifest `--check` in CI | Met | `ci.yml`; runs `23831550017`, `23831565243` |
| Unified smoke (9 episodes) | Met | `run_unified_pack_smoke.py` |
| Lineage + nominal difficulty docs | Met | `unified_core_m07.md`, ledger |
| No Kaggle / no semantic bump | Met | Scope discipline |
| PR + main CI green | Met | `M07_run1.md` §2 |

---

## 10. Final Verdict

Milestone objectives met for **offline unified pack normalization and governance**. Merge completed with **green** GitHub Actions on PR head and on **`main`** post-merge.

---

## 11. Authorized Next Step

- **M08** — Defensibility, QA, and contamination-resistance hardening per `docs/milestones/M08/M08_plan.md`; work from `main` at `07e349e…` or later.

---

## 12. Canonical References

- **PR:** https://github.com/m-cahill/lucid/pull/8 (merged)
- **PR head SHA:** `b5109f7de6f87039f3e671dad8c378fe64e05784`
- **Merge commit (`main`):** `07e349ef7ff68cad79be3c41bb94839045fe18b3`
- **CI (PR):** https://github.com/m-cahill/lucid/actions/runs/23831550017
- **CI (`main`):** https://github.com/m-cahill/lucid/actions/runs/23831565243
- Plan: `docs/milestones/M07/M07_plan.md`
- Pack spec: `docs/benchmark_packs/unified_core_m07.md`
- Manifest: `tests/fixtures/unified_core_m07/unified_core_m07_manifest.json`
