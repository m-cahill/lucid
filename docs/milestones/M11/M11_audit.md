# Milestone Audit — M11 (closeout)

**Milestone:** M11 — Hosted-model probe surface
**Mode:** **DELTA** — ingest scripts, artifacts, docs, CI; **no** scorer/parser/schema/family edits
**Audit verdict:** **Green** — evidence collected, exclusions evidence-backed, closeout ready.

---

## 1. Executive summary

**Intent:** Transparent response-surface pipeline from Kaggle leaderboard CSVs to normalized artifacts, with cost-aware allocation, P24 cohort, and honest failure taxonomy. Benchmark **1.1.0** unchanged; **31-model** active roster (2 excluded with exact failure evidence).

**Blast radius**

* **Added/modified:** `scripts/m11_ingest_common.py`, `ingest_m11_platform_exports.py`, `generate_m11_tables.py`, `generate_m11_figures.py`, `generate_m11_probe_artifacts.py`, `docs/milestones/M11/artifacts/*`.
* **Not touched:** `src/lucid/` scorer/parser/schema semantics (no benchmark surface change).

---

## 2. Governance alignment

| Invariant | Status |
|-----------|--------|
| Benchmark version **1.1.0** | **Held** |
| Semantic benchmark change | **None** |
| Roster authority (33 listed, 31 tracked) | **Held** via `m11_roster_canonical.json` |
| No parser/prompt/notebook changes for excluded models | **Held** |
| No M09 aggregate slice invention | **Held** — ingest uses task-level rows only |

---

## 3. Evidence posture

| Claim | Supported by |
|-------|--------------|
| P12 completion (31 models) | `docs/milestones/M11/artifacts/michael1232_lucid-kaggle-community-benchmarks_leaderboard.csv` (ingested) |
| P12 cost data | `docs/milestones/M11/artifacts/lucid_m11_probe_p12_task_costs.csv` (operator CSV, per-model totals) |
| P24 cohort (11 models) | Operator P24 run evidence (cost-aware selection) |
| P48 partial | Operator P48 runs; Gemma 3 12B context overflow documented |
| P72 from M09 export | `m09_kaggle_leaderboard_export.csv` (15/33 completed) |
| DeepSeek-R1 exclusion | `json_parse_failure_reasoning_wrapper` — exact error payload |
| gpt-oss-120b exclusion | `json_parse_failure_truncated_output` — exact error payload |

---

## 4. Excluded model findings

These are **operational findings**, not benchmark defects:

1. **DeepSeek-R1** (`deepseek-r1-0528`): model emits `<think>...</think>` reasoning trace before JSON. The current strict text adapter does not strip reasoning wrappers. This is a known surface-compatibility boundary. M11 records it honestly and does not attempt rescue.

2. **gpt-oss-120b**: model emits truncated malformed JSON on later turns. The current strict JSON extraction fails. M11 records it honestly and does not attempt rescue.

The correct framing: the current strict structured-output surface is part of the benchmark transport contract. These models did not satisfy it cleanly enough for M11 scoring. We are recording that honestly.

---

## 5. CI / reproducibility

* **Authoritative green CI (tooling recovery, 2026-04-07):** run **24105189098** on commit **`c0f55ce7cdbc8d9b3feca7625379cb59211b0cd1`** — https://github.com/m-cahill/lucid/actions/runs/24105189098 — after fixes for notebook-manifest newline hashing, repo-relative ingest `export_paths`, and LF-normalized CSV hashing in probe manifest tables.
* **Formal closeout commit** (roster 31/2 + regenerated artifacts + ledger): run **24105499612** on commit **`861aa19f03b0a12ef2ef41ff23ebb5c4151cc0f0`** — https://github.com/m-cahill/lucid/actions/runs/24105499612 — **success**.
* All `--check` generators pass deterministically on that tip.
* `pytest` full suite green with ≥85% coverage.
* `ruff check` clean on touched scripts.
* PNG figure checks use pixel tolerance consistent with prior milestones.

---

## 6. Deferred (future, not M11 scope)

* Structured-output robustness hardening (strict vs tolerant JSON extraction)
* Reasoning-wrapper compatibility study (`<think>` stripping, chain-of-thought extraction)
* These are potential work items for M12+ or later; they are **not** unfinished M11 execution debt

---

## 7. Machine-readable appendix

```json
{
  "milestone": "M11",
  "mode": "delta_audit",
  "verdict": "green_closeout",
  "benchmark_version": "1.1.0",
  "semantic_changes": false,
  "tracked_models": 31,
  "excluded_models": 2,
  "exclusion_evidence_backed": true,
  "p12_complete": true,
  "p24_cohort_run": true,
  "p48_partial": true,
  "parser_changes": false,
  "prompt_changes": false,
  "notebook_changes": false,
  "m12_linkage_deferred": true
}
```
