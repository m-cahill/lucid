# LUCID Deterministic Generation Contract

**Project:** LUCID  
**Benchmark Version:** 1.0.1  
**Document Type:** Execution Contract (Layer B)  
**Authority:** Episode reconstructibility and determinism  
**Status:** Frozen

---

## 1. Purpose

This contract defines what it means for LUCID episode generation to be deterministic.

---

## 2. Required reconstructibility tuple

Every generated episode MUST be reproducible from the following tuple:

- `seed`
- `template_family`
- `template_version`
- `difficulty_profile`
- `drift_type`
- `drift_parameters`
- `scoring_profile_version`

Given this tuple, the generator MUST produce the same episode spec bit-for-bit.

---

## 3. No nondeterministic ambiguity resolution

Template families MUST NOT introduce nondeterministic ambiguity resolution.

If a family contains ambiguity branches, their realization MUST be fully determined by the reconstructibility tuple.

---

## 4. Generator invariants

- The same tuple MUST yield the same episode spec.
- Hidden randomness, clock time, and environment-dependent branching are forbidden.
- Any semantic change in interpretation of tuple fields requires change control.

---

## 5. One-line summary

> LUCID episodes are generated from a fixed reconstructibility tuple and may not contain hidden randomness, including hidden ambiguity resolution.
