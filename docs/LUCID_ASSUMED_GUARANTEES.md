# LUCID assumed guarantees

**Project:** LUCID  
**Benchmark version:** 1.1.0 (active profile)  
**Document type:** Adjacent governance — substrate assumptions vs repo truth  
**Status:** Canonical

---

## 1. Purpose

This document states what the LUCID implementation **targets** and what is **actually proven in this repository** at a given time. It does **not** claim inherited certification from sibling codebases unless the same guarantees are **implemented and tested here**.

---

## 2. Three-way distinction

| Category | Meaning |
|----------|---------|
| **Assumed posture** | Design targets the benchmark commits to (may be partially implemented) |
| **Implemented in this repo** | Behavior enforced by code + tests + CI in **this** tree |
| **Not yet proven** | Planned or external; must not be asserted as done in writeups |

---

## 3. Assumed posture (targets)

- **Deterministic episode generation** from the reconstructibility tuple (seed, family, versions, drift params, scoring profile)
- **Canonical JSON** serialization for artifacts (stable keys, encoding, no NaN/Inf in canonical scoring payloads)
- **Reproducible hashing** of canonical files for audit trails
- **Typed output parsing** into `EpisodeResponse` with no scoring from raw model prose
- **Truthful CI** — automated checks reflect real failures; gates are not bypassed for convenience
- **No hidden evaluator dependence** — official metrics computable from spec + typed response + profile

---

## 4. Implemented in this repo

*Updated as milestones complete. M00 establishes the baseline.*

| Guarantee | M00 status |
|-----------|------------|
| Repository layout + packaging (`pyproject.toml`, `src/lucid`) | **Implemented** |
| Local minimal green path (one family, one bundle) | **Implemented** (`symbolic_negation_v1`, smoke script) |
| Scoring profile v1.1.0 semantics documented and encoded in scorer | **Implemented** |
| Baseline CI (lint, typecheck, tests) | **Implemented** (`.github/workflows/ci.yml`) |

---

## 5. Not yet proven (honest list)

- **Kaggle Community Benchmarks end-to-end** — deferred to **M01**; M00 does not validate platform execution
- **Certification or external audit** of this repo against third-party harnesses (unless explicitly added later)
- **Inherited guarantees** from RediAI, DARIA, Foundry, CLARITY, etc. — those projects inform **posture**; they are not automatically guarantees **of** LUCID unless ported and tested here

---

## 6. One-line summary

> LUCID documents assumed posture, distinguishes it from what this repo actually proves, and avoids certification theater borrowed from other systems.
