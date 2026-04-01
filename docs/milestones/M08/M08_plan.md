# M08 Plan — Defensibility, QA, and contamination-resistance hardening

**Project:** LUCID  
**Milestone:** M08  
**Title:** Defensibility, QA, and contamination-resistance hardening  
**Status:** **Complete** (repository record)  
**Primary judged axis:** **Dataset quality & task construction**  
**Benchmark posture:** **No Kaggle platform proof claim in this milestone**  
**Benchmark version target:** **Remain at 1.1.0** unless a material semantic defect is discovered and handled through formal change control.

---

## 1. Goal

Turn the unified benchmark from “deterministic and normalized” into “defensible and audit-ready” by adding a deterministic QA / defensibility layer over `unified_core_m07_v1` and its source family packs.

This milestone produces a **blocking, repeatable audit** that answers:

- Is the unified pack lineage-preserving and duplication-clean?
- Are benchmark artifacts structurally defensible and metadata-complete?
- Are ambiguity / contradiction / drift signals represented coherently enough to support judge-facing claims?
- Can LUCID make a stronger contamination-resistance argument based on synthetic generation and committed provenance?

---

## 2. Why this milestone now

M07 completed the unified pack and explicitly did **not** attempt Kaggle or hosted-model evidence. The ledger named **defensibility / ambiguity audit** as a submission blocker. M08 stays narrow: remove that blocker for **automated, CI-enforced** defensibility — without conflating it with Kaggle proof.

---

## 3. In scope

- Deterministic **defensibility audit** code for the unified pack and source packs.
- Structural **QA checks** runnable locally and in CI.
- Exact-duplicate, lineage, provenance, and metadata completeness checks.
- Soft **near-duplicate / repetitive-surface heuristics** as informational output (not flaky merge blockers).
- A written **contamination-resistance posture** grounded in LUCID’s synthetic generation approach (honest scope).
- CI enforcement for the new blocking audit.
- Updates to `docs/lucid.md` and related docs so the ledger remains the living authority.
- Full milestone evidence paths: plan, run log, summary, audit, toolcalls, artifact outputs (see closeout workflow).

---

## 4. Out of scope

- Kaggle notebook / task work.
- Hosted-model runs or backfilling `family1_model_scores.csv`.
- New family generation or major pack expansion.
- Scorer / parser / output-schema semantic changes.
- Psychometric rebalancing across families.
- Any claim that M08 alone delivers submission readiness.

---

## 5. Deliverables (as implemented)

| Area | Location |
|------|----------|
| Audit engine | `src/lucid/audits/defensibility.py`, `src/lucid/audits/__init__.py` |
| CLI | `scripts/run_unified_defensibility_audit.py` (`--write` / `--check`) |
| Artifacts | `docs/milestones/M08/artifacts/m08_defensibility_audit.json`, `m08_duplicate_scan.json`, `m08_defensibility_summary.md`, `m08_contamination_posture.md`, `m08_exact_duplicate_allowlist.json` |
| Canonical standard | `docs/benchmark_quality/LUCID_DEFENSIBILITY_STANDARD.md` |
| Tests | `tests/test_unified_defensibility_audit.py` |
| CI | `.github/workflows/ci.yml` — `run_unified_defensibility_audit.py --check` |

---

## 6. Hard vs soft checks (summary)

**Hard-fail:** rebuild parity with `build_manifest_dict()`, unique `unified_episode_id`, bijective lineage to source manifests, source `episode_spec` equality, `source_episode_spec_hash` correctness, required row metadata, valid difficulty / drift / family variant, distribution summaries, unapproved exact-duplicate groups (allowlist default empty).

**Soft (informational):** token-set Jaccard, character n-gram overlap, prompt-skeleton repetition bands, ambiguity-window shape heuristics — capped and deterministic for auditability.

---

## 7. Acceptance criteria mapping

1. `python scripts/run_unified_defensibility_audit.py --check` passes locally and in CI.  
2. Audit artifacts are deterministic and committed (regenerate via `--write`).  
3. Unified pack has **no unapproved exact duplicates** or lineage collisions.  
4. Every unified row passes required provenance and metadata completeness checks.  
5. Soft findings surfaced in artifacts and summary.  
6. Existing pack checks, smoke paths, and repo CI remain green.  
7. `docs/lucid.md` reflects M08 artifacts, judged axis, and updated blocker posture.  
8. **No** Kaggle platform proof claim and **no** benchmark version bump claim unless documented semantic change.

---

## 8. Verification commands (suggested)

```bash
python scripts/generate_family1_core_m03_manifest.py --check
python scripts/generate_family2_core_m05_manifest.py --check
python scripts/generate_family3_core_m06_manifest.py --check
python scripts/generate_unified_core_m07_manifest.py --check
python scripts/run_unified_pack_smoke.py
python scripts/run_unified_defensibility_audit.py --check
pytest
```

---

## 9. Authority

`docs/LUCID_MOONSHOT.md`, `docs/contracts/`, `docs/lucid.md`, `docs/benchmark_quality/LUCID_DEFENSIBILITY_STANDARD.md`, `src/lucid/`.
