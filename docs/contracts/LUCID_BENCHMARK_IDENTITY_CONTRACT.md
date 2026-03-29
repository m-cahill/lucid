# LUCID Benchmark Identity Contract

**Project:** LUCID  
**Benchmark Version:** 1.0.1  
**Document Type:** Governing Contract (Layer A)  
**Authority:** Identity-level benchmark contract  
**Status:** Frozen

---

## 1. Purpose

This contract defines what LUCID is, what it measures, and what it is for.

LUCID is not a general evaluation sandbox. It is not a solver. It is not a broad “reasoning benchmark.” It is a specific scientific instrument.

---

## 2. Identity lock

LUCID is a benchmark for metacognitive calibration under instructional drift.

This phrase is not a slogan. It is the governing identity of the project.

### 2.1 Benchmark
LUCID exists to diagnose model behavior, not to solve tasks.

### 2.2 Metacognitive
LUCID primarily evaluates whether a model can monitor the validity of its own local policy under change.

### 2.3 Calibration
LUCID treats confidence behavior as part of the answer.

### 2.4 Instructional drift
LUCID centers episodes in which the governing rule changes in a structured, explicit, and auditable way.

---

## 3. Primary faculty

The primary faculty isolated by LUCID is:

> metacognitive calibration under instructional drift

The flagship questions are:

- Can the model detect that the governing rule has changed?
- Can the model lower confidence before confidence outruns correctness?
- Can the model abstain or ask for clarification when the rule environment becomes unstable?
- Can the model recover cleanly after contradiction, ambiguity, or correction?

Secondary signals MAY be reported, but they MUST NOT displace this primary faculty.

---

## 4. Core stressor

The core stressor in LUCID is:

> explicit rule change in a synthetic local rule-world

LUCID is therefore anchored on:

- deterministic rule induction
- stable pre-drift application
- explicit drift event
- post-drift uncertainty management
- final behavioral resolution

The benchmark MUST NOT collapse into generic task difficulty divorced from rule change.

---

## 5. Benchmark outputs

The canonical output of a scored LUCID interaction is:

- a typed answer or typed non-answer action
- a scalar confidence in `[0.0, 1.0]`
- a typed drift-detection signal
- optional, non-scored short rationale metadata

Correctness alone is insufficient. Confidence is part of the official benchmark output.

The precise schema is defined in `LUCID_OUTPUT_SCHEMA_CONTRACT.md`.

---

## 6. Evaluation target hierarchy

LUCID optimizes for the following hierarchy:

1. Drift detection
2. Calibration under uncertainty
3. Abstention / clarification discipline
4. Behavioral recovery after drift
5. Post-drift correctness

Correctness remains important, but it is not the sole or primary signal.

### 6.1 No lucky-guessing reward
LUCID MUST NOT reward correct answers that arise from lucky guessing under stale policy as if they were equivalent to detected, calibrated, and behaviorally updated responses.

A correct final answer obtained without drift detection, confidence adjustment, or appropriate uncertainty behavior MUST NOT outrank a response profile that demonstrates stronger metacognitive adaptation.

---

## 7. Dataset doctrine

LUCID MUST prefer:

- synthetic rule-worlds
- exact ground truth
- contamination resistance
- deterministic generation
- tunable difficulty
- auditability

LUCID MUST NOT depend on vague human interpretation to determine core correctness or core drift labels.

---

## 8. Scientific contribution lock

LUCID’s scientific contribution is:

> to measure whether a model can detect when its internal policy is stale and recalibrate before confidence outruns correctness

This contribution depends on all of the following remaining true:

- the benchmark is metacognition-first
- drift is explicit and typed
- confidence is a scored output
- abstention / clarification remain meaningful actions
- deterministic artifacts support reproducible re-evaluation

---

## 9. Non-goal lock

LUCID MUST NOT become:

- a solver system
- a broad faculty omnibus benchmark
- a natural-language ambiguity soup benchmark
- a multimodal flash benchmark without faculty isolation
- a human-judged core leaderboard

---

## 10. One-line summary

> LUCID is a benchmark, not a solver, and it exists to reveal whether models notice rule drift and recalibrate before stale confidence outruns correctness.
