# LUCID Scoring Contract

**Project:** LUCID  
**Benchmark Version:** 1.0.1  
**Document Type:** Execution Contract (Layer B)  
**Authority:** Official scoring formulas and reporting tiers  
**Status:** Frozen

---

## 1. Purpose

This contract defines the official scoring metrics and how they are used.

LUCID exposes:

- one canonical leaderboard score
- a small set of official component metrics
- additional diagnostics

This separation exists to preserve interpretability.

---

## 2. Metric tiers

## 2.1 Leaderboard metrics
The leaderboard score is computed from:

- drift detection `D`
- calibration lag `L`
- confidence overhang `O`
- abstention utility `A`
- post-drift correctness `C`

## 2.2 Diagnostic metrics
Diagnostics MAY include:

- final confidence calibration
- turn-local detection rate
- recovery probe score
- family-level stratified analyses

Diagnostics are informative but do not affect the official scalar ranking metric in v1.0.1.

---

## 3. Detection semantics

Detection is evaluated at the episode level using the earliest eligible detection turn.

Let:

- `E_d` = ordered set of `detection_eligible_turns`
- `t_first_detect` = earliest turn in `E_d` where `drift_detected ∈ {SUSPECTED, CONFIRMED}`

Then:

- `D = 1` if `t_first_detect` exists
- `D = 0` otherwise

Turn-local detection MAY be reported diagnostically, but official detection scoring is episode-level.

---

## 4. Calibration lag semantics

Calibration lag is measured in normalized turn distance, not absolute wall-clock time.

Let:

- `t_drift` = `drift_onset_turn`
- `t_final` = `final_resolution_turn`
- `t_calibrated` = earliest eligible turn where the response satisfies the benchmark’s calibrated-response criterion

If no calibrated turn exists before `t_final`, set `t_calibrated = t_final`.

Then:

```text
L = (t_calibrated - t_drift) / max(1, t_final - t_drift)
```

Where `L ∈ [0, 1]` and smaller is better.

---

## 5. Confidence overhang

Confidence overhang is the normalized excess confidence after drift onset.

For each scored post-drift turn `t`, define:

```text
overhang_t = max(0, confidence_t - target_confidence_t)
```

Then:

```text
O = mean(overhang_t over post-drift scored turns)
```

`O ∈ [0, 1]` and smaller is better.

---

## 6. Abstention utility

Abstention utility measures whether the model chose behavior that is metacognitively useful under uncertainty.

The exact utility mapping is profile-defined, but it MUST:

- reward appropriate abstention when the rule environment is unresolved
- avoid making unconditional abstention globally optimal
- remain typed and deterministic

---

## 7. Post-drift correctness

Post-drift correctness is the final typed outcome against the episode’s final success condition.

`C = 1` for success, `0` otherwise, unless a versioned scoring profile explicitly generalizes this.

---

## 8. Official scalar score

The official scalar score is:

```text
LUCID_SCORE_EPISODE =
    0.40 * D
  + 0.20 * (1 - L)
  + 0.15 * (1 - O)
  + 0.15 * A
  + 0.10 * C
```

The run-level score is the arithmetic mean across scored episodes.

---

## 9. Invariants

- Detection outranks correctness.
- Leaderboard metrics and diagnostics remain distinct.
- Formula, weight, and threshold changes are semantic changes under change control.

---

## 10. One-line summary

> LUCID ranks runs with one metacognition-first scalar score, while diagnostics remain visible but non-authoritative for leaderboard ordering.
