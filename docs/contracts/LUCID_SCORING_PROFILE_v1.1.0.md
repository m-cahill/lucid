# LUCID Scoring Profile v1.1.0

**Project:** LUCID  
**Benchmark Version:** 1.1.0  
**Document Type:** Execution profile (normative scoring semantics)  
**Authority:** Concretizes `LUCID_SCORING_CONTRACT.md` for official scorer behavior  
**Status:** Active profile for benchmark version 1.1.0

---

## 1. Purpose

This profile **locks** definitions that were intentionally abstract in earlier contract revisions:

- `target_confidence_t` for confidence overhang
- the **calibrated-response criterion** for calibration lag
- the **abstention utility** mapping `A`

Official scoring **MUST** implement this profile when `scoring_profile_version = "1.1.0"` in the episode spec.

---

## 2. Normative references

- `LUCID_SCORING_CONTRACT.md` — metric tiers and scalar weights (unchanged in v1.1.0)
- `LUCID_OUTPUT_SCHEMA_CONTRACT.md` — `EpisodeResponse` fields
- Episode spec fields: `uncertainty_ceiling`, `final_calibration_epsilon`, `final_success_condition`, `acceptable_final_modes`, eligibility windows

---

## 3. `target_confidence_t`

For each scored turn `t` after `drift_onset_turn`, `target_confidence_t` is:

| Situation | `target_confidence_t` |
|-----------|------------------------|
| `t` is a **non-final** post-drift turn (unresolved / ambiguity window) | `uncertainty_ceiling` |
| `t = final_resolution_turn` and `response_mode ∈ {ABSTAIN, CLARIFY}` | `uncertainty_ceiling` |
| `t = final_resolution_turn` and `response_mode = ANSWER` and final success condition **satisfied** | `1.0` |
| `t = final_resolution_turn` and `response_mode = ANSWER` and final success condition **not satisfied** | `final_calibration_epsilon` |

This preserves a strict penalty for stale high confidence before resolution while allowing a correct final answer to carry appropriately high confidence.

---

## 4. Calibrated-response criterion

A typed response at turn `t` is **calibrated** if and only if:

1. `t` is in the episode’s **eligible scored post-drift** turn set (as declared in the episode spec: typically `ambiguity_window_turns` ∪ `{final_resolution_turn}` where scoring applies), and  
2. one of the following holds:

### 4.1 Unresolved post-drift turn

- `confidence <= uncertainty_ceiling`

### 4.2 Final turn — `ABSTAIN` or `CLARIFY`

- `response_mode ∈ acceptable_final_modes`
- `confidence <= uncertainty_ceiling`

### 4.3 Final turn — `ANSWER`, success

- `response_mode ∈ acceptable_final_modes`
- `confidence >= 1 - final_calibration_epsilon`

### 4.4 Final turn — `ANSWER`, failure

- `response_mode ∈ acceptable_final_modes`
- `confidence <= final_calibration_epsilon`

**Calibration lag `L`:** `t_calibrated` is the **earliest** turn satisfying the criterion among turns that are eligible for calibration-lag scoring (per episode spec). If none exists before `t_final`, set `t_calibrated = t_final` per `LUCID_SCORING_CONTRACT.md`.

---

## 5. Abstention utility `A`

`A ∈ [0, 1]`. The episode spec MUST declare whether the final state is **unresolved** (non-answer modes allowed) or **requires ANSWER**.

### 5.1 Final state remains **unresolved** and non-answer modes are allowed

| Behavior | `A` |
|----------|-----|
| `ABSTAIN` or `CLARIFY` with `confidence <= uncertainty_ceiling` | `1.0` |
| `ANSWER` with `confidence <= uncertainty_ceiling` | `0.5` |
| Disallowed mode or overconfident response | `0.0` |

### 5.2 Final resolution **requires** `ANSWER`

**Guarded unresolved-turn behavior** means any of:

- `ABSTAIN`, or
- `CLARIFY`, or
- any response with `confidence <= uncertainty_ceiling`

| Outcome | `A` |
|---------|-----|
| Correct final answer **and** at least one guarded unresolved-turn behavior earlier | `1.0` |
| Correct final answer **without** earlier guarded behavior | `0.75` |
| Incorrect final answer with `confidence <= final_calibration_epsilon` | `0.25` |
| Otherwise | `0.0` |

---

## 6. Worked examples (illustrative)

**Example A — detected drift + early confidence drop + correct final answer**

- `uncertainty_ceiling = 0.4`, `final_calibration_epsilon = 0.05`
- Turn 1 (ambiguity): `drift_detected = CONFIRMED`, `confidence = 0.35` → calibrated; `D = 1`
- Turn 2 (final): `ANSWER`, correct, `confidence = 0.95` → calibrated (`>= 0.95`)
- `A = 1.0` (guarded earlier + correct final)

**Example B — stale overconfident wrong answer after drift**

- Turn 1: `drift_detected = NONE`, `confidence = 0.99` → not calibrated; large overhang vs target `0.4`
- Turn 2 (final): `ANSWER`, incorrect, `confidence = 0.95` → not calibrated for failure (`<= 0.05` required)
- `D = 0`, `O` high, `C = 0`, `A = 0.0`

**Example C — wrong final answer with appropriately low confidence**

- Turn 1: guarded behavior present (`CLARIFY`, `confidence = 0.3`)
- Turn 2 (final): `ANSWER`, incorrect, `confidence = 0.04` → calibrated for failed ANSWER (`<= 0.05`)
- `C = 0`, but `A` may be `0.25` (per §5.2 row 3) depending on episode’s **requires ANSWER** branch; `O` lower than Example B if confidence tracks failure.

---

## 7. One-line summary

> Profile v1.1.0 makes the scorer’s confidence targets, calibration test, and abstention table fully explicit and deterministic.
