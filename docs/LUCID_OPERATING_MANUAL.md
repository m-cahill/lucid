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

### Offline core packs (canonical manifests)

As of **M07**, committed deterministic packs (regenerate with `--check` in CI) include the three per-family core packs plus one **unified** cross-family pack (full composition, normalized metadata):

| Pack ID | Family (`template_family`) | Manifest check script |
|---------|----------------------------|------------------------|
| `family1_core_m03_v1` | `symbolic_negation_v1` | `scripts/generate_family1_core_m03_manifest.py` |
| `family2_core_m05_v1` | `contradiction_clarification_v1` | `scripts/generate_family2_core_m05_manifest.py` |
| `family3_core_m06_v1` | `scope_precedence_exception_v1` | `scripts/generate_family3_core_m06_manifest.py` |
| `unified_core_m07_v1` | *(multi-family composition)* | `scripts/generate_unified_core_m07_manifest.py` |

**M08 — defensibility audit (CI):** After manifests match generators, CI runs `python scripts/run_unified_defensibility_audit.py --check`, which verifies lineage, duplicate posture, hash integrity, and regenerable artifacts under `docs/milestones/M08/artifacts/`. Policy: `docs/benchmark_quality/LUCID_DEFENSIBILITY_STANDARD.md`. This is **local + CI proof** only — not Kaggle execution evidence.

**M09 — Kaggle evidence panel (repo, Phase B):** The **mature-benchmark** evaluation slice is defined in `src/lucid/kaggle/m09_evidence_panel.py` (72 episodes on `unified_core_m07_v1`, not a pack expansion). The committed panel artifact is `docs/milestones/M09/artifacts/m09_model_panel.json` (`scripts/generate_m09_panel_artifact.py --write` / `--check`). The generated notebook is `notebooks/lucid_kaggle_m09_mature_evidence.ipynb` (`scripts/generate_m09_kaggle_notebook.py`), task **`lucid_m09_mature_evidence_task`**. Hosted-model runs and exported CSVs are **platform evidence** (Phase C+), not CI.

**Benchmark version** for scoring and episode generation remains **1.1.0** unless change control bumps it. The unified pack does **not** change episode semantics; see `docs/benchmark_packs/unified_core_m07.md`.

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
