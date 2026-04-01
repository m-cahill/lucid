# LUCID Operating Manual

**Project:** LUCID  
**Benchmark Version:** 1.1.0  
**Document Type:** Operating Manual (Execution Context)  
**Authority:** Practical execution guide over frozen contracts  
**Status:** Canonical execution reference

---

## 1. Purpose

This document explains how to **run, build, and reason about LUCID as a system**.

The contract set defines:

- what LUCID *is*
- what LUCID *measures*
- what is allowed and forbidden

This document defines:

- how LUCID is executed end-to-end
- how contracts map to code
- how to produce a valid benchmark run
- how to integrate with Kaggle

---

## 2. Core Mental Model

LUCID is a deterministic benchmark pipeline:

```text
EpisodeSpec
  → Generator (deterministic)
  → Model produces typed response
  → Parser → EpisodeResponse
  → Scorer → EpisodeResult
  → Artifact Writer → Bundle
```

Every component is governed by a contract.

---

## 3. Minimal System Components

A minimal LUCID implementation requires:

| Component    | Role                   | Contract                 |
| ------------ | ---------------------- | ------------------------ |
| generator    | builds episode spec    | Deterministic Generation |
| drift module | applies drift          | Drift Taxonomy           |
| parser       | enforces output schema | Output Schema            |
| scorer       | computes metrics       | Scoring                  |
| writer       | emits bundle           | Artifact Bundle          |

---

## 4. Contract → Code Mapping

| Contract                              | Implementation Module |
| ------------------------------------- | --------------------- |
| `LUCID_OUTPUT_SCHEMA_CONTRACT.md`     | `parser.py`           |
| `LUCID_EPISODE_STRUCTURE_CONTRACT.md` | `generator.py`        |
| `LUCID_DRIFT_TAXONOMY_CONTRACT.md`    | `drift.py`            |
| `LUCID_SCORING_CONTRACT.md`           | `scorer.py`           |
| `LUCID_ARTIFACT_BUNDLE_CONTRACT.md`   | `writer.py`           |

---

## 5. First Runnable System (Minimal Green Path)

The smallest valid benchmark run:

```text
1 episode
1 template family
1 drift event
no clarification branch
single final resolution
```

Pipeline:

```text
generate_episode()
→ run_model()
→ parse_response()
→ score_episode()
→ write_bundle()
```

This MUST satisfy the Minimal Green Path contract 

---

## 6. Episode Lifecycle

Each episode follows the state machine:

```text
RULE_INDUCTION
→ STABLE_APPLICATION
→ DRIFT_EVENT
→ DRIFT_RESPONSE_WINDOW
→ FINAL_RESOLUTION
→ (optional) RECOVERY_PROBE
```

Defined in:

* Episode Structure Contract 

---

## 7. Model Interaction

The model MUST produce a typed response:

```json
{
  "answer": "...",
  "confidence": 0.73,
  "response_mode": "ANSWER",
  "drift_detected": "SUSPECTED"
}
```

Defined in:

* Output Schema Contract 

---

## 8. Scoring Flow

```text
EpisodeResponse
→ Detection (D)
→ Calibration Lag (L)
→ Confidence Overhang (O)
→ Abstention Utility (A)
→ Correctness (C)
→ Aggregate score
```

Defined in:

* Scoring Contract 

---

## 9. Artifact Output

Each episode produces:

```text
episode_<id>/
  episode_spec.json
  episode_result.json
  bundle_manifest.json
  hashes.json
```

Defined in:

* Artifact Bundle Contract 

---

## 10. Determinism Guarantee

Every episode must be reproducible from:

```text
(seed, template_family, template_version,
 difficulty_profile, drift_type,
 drift_parameters, scoring_profile_version)
```

Defined in:

* Deterministic Generation Contract 

---

## 11. How to Build LUCID

### Step 1 — Implement generator

* deterministic
* produces `episode_spec.json`

### Step 2 — Implement parser

* validates schema
* extracts typed response

### Step 3 — Implement scorer

* computes D, L, O, A, C

### Step 4 — Implement artifact writer

* writes canonical JSON
* computes hashes

### Step 5 — Validate minimal green path

* run 1 episode
* confirm full bundle

---

## 12. Kaggle Integration Model

### Dataset

* generated offline
* stored as episode spec artifacts

### Submission

* model produces typed responses
* scoring runs in notebook

### Output

* scalar score
* optional diagnostics

### Key constraint

* Kaggle submission must NOT change benchmark semantics

---

## 13. Debugging Guide

### If scoring is wrong

* check eligibility windows
* check drift_onset_turn
* check normalized lag formula

### If parsing fails

* check schema compliance
* check enum values

### If results vary

* check seed usage
* check deterministic generation

---

## 14. What This System Guarantees

LUCID guarantees:

* deterministic reproducibility
* typed scoring boundary
* no hidden evaluator logic
* audit-ready artifacts
* metacognition-first evaluation

It does NOT guarantee:

* model correctness
* solver performance
* general reasoning coverage

---

## 15. One-line Summary

> LUCID is a deterministic pipeline that converts rule-change episodes into typed model behavior, scores metacognitive adaptation, and produces audit-ready artifacts.
