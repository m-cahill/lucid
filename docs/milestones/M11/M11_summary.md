# Milestone Summary — M11: Hosted-model probe surface

**Project:** LUCID
**Milestone:** M11
**Status:** **Complete / closed** — P12/P24/partial-P48 evidence collected; exclusions evidence-backed; see `M11_audit.md`
**Benchmark version:** **1.1.0** (unchanged)

---

## 1. Objective

Deliver a **deterministic, auditable** pipeline from Kaggle leaderboard CSV(s) to normalized **model x probe_tier** rows, plus cost-aware allocation policy, P24 cohort, and completion figures, **without** benchmark semantic changes.

---

## 2. What shipped

| Area | Evidence |
|------|----------|
| Probe ladder code | `src/lucid/kaggle/m11_probe_panels.py` |
| Ladder + roster JSON | `m11_probe_ladder.json`, `m11_roster_canonical.json` (31 tracked, 2 excluded) |
| Probe notebooks | `lucid_kaggle_m11_probe_p12.ipynb`, `p24`, `p48` |
| Ingest | `ingest_m11_platform_exports.py`, `m11_ingest_common.py` |
| Response surface | `m11_model_response_surface.json` / `.csv` |
| Comparator + cost | `m11_p12_vs_main_comparison.csv`, `m11_p12_cost_frontier.csv` |
| P24 cohort | `m11_p24_candidate_set.md` |
| Allocation policy | `m11_allocation_policy.md` (cost-aware, `drop_from_consideration` action) |
| Analytical summary | `m11_analytical_summary.md` |
| Figures | `m11_fig_completion_by_tier.png`, `m11_fig_p12_delta_vs_cost.png` |
| Tests | `tests/test_m11_ingest.py` |
| Ledger | `docs/lucid.md`, `docs/LUCID_COMPETITION_ALIGNMENT.md` |

---

## 3. Evidence boundary

* **P12:** 31/31 tracked models completed against comparator `lucid_main_task` with operator cost CSV.
* **P24:** 11 models from cost-aware cohort (collapse, inversion, efficiency, anchors).
* **P48:** partial cohort; Gemma 3 12B hit context-window overflow (32,768 token input limit) — logged as operational ceiling (`input_token_limit_exceeded_32768`), not benchmark defect.
* **P72:** populated from committed M09 leaderboard export (15/33 `completed`, 18 `platform_limited`).

---

## 4. Excluded models — surface-compatibility failures

Two models are excluded from the 31-model active roster with exact failure evidence:

| model_slug | failure_reason_code | failure type |
|---|---|---|
| `deepseek-r1-0528` | `json_parse_failure_reasoning_wrapper` | `<think>` trace contaminates output; `ValueError: Confidence is not numeric: None` |
| `gpt-oss-120b` | `json_parse_failure_truncated_output` | Truncated malformed JSON; `ValueError: No JSON object found in model output` |

These are **structured-output / surface-compatibility failures**, not benchmark defects, not model-unavailable, and not score signals. M11 intentionally does **not** modify the parser or prompt to rescue them — doing so would change the evaluation surface and reduce comparability with the 31 tracked models.

---

## 5. Key M11 findings

1. **Collapse signals** — GLM-5 and GPT-5.4 mini showed persistent large negative delta vs `lucid_main_task` at P12 and P24.
2. **Inversion signals** — DeepSeek V3.1 and V3.2 showed large positive deltas that faded at P24.
3. **Efficiency anchor** — Qwen 3 Coder 480B: top-tier score-per-dollar at P12 and P24.
4. **Context-window ceiling** — P48 implicitly demands >32k input context; Gemma 3 12B hit this limit.
5. **Surface-compatibility limits** — DeepSeek-R1 (reasoning wrapper) and gpt-oss-120b (truncated JSON) exposed structured-output compatibility boundaries on the current strict transport contract.

---

## 6. Deferred

* **M12** — final benchmark / task / writeup linkage.
* **Future (post-M11):** structured-output robustness hardening, strict vs tolerant JSON extraction policy, reasoning-wrapper compatibility study. Not M11 scope.
