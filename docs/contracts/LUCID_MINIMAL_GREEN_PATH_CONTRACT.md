# LUCID Minimal Green Path Contract

**Project:** LUCID  
**Benchmark Version:** 1.0.1  
**Document Type:** Governing Contract (Layer A)  
**Authority:** Minimal runnable benchmark spine  
**Status:** Frozen

---

## 1. Purpose

This contract defines the smallest end-to-end path that every milestone, implementation branch, and notebook proof must preserve.

---

## 2. Canonical minimal path

```text
Generate deterministic episode
→ induce local policy
→ inject one explicit drift event
→ collect typed answer + confidence + response mode
→ score detection + calibration + correctness
→ write audit-ready episode bundle
```

This is the non-negotiable executable spine of LUCID.

---

## 3. Invariants

### 3.1 Minimal path must remain runnable
At all times, the benchmark MUST retain at least one family and one scoring path that satisfy the canonical minimal path.

### 3.2 Optional branches must remain optional
The minimal green path MUST NOT depend on optional clarification or recovery probes.

Clarification and recovery MAY be present in richer families, but the benchmark’s minimal viability MUST not depend on them.

### 3.3 Typed output only
The minimal path MUST terminate in typed benchmark output and typed scoring artifacts.

---

## 4. One-line summary

> LUCID’s minimal green path is a deterministic, drift-bearing, typed, scored, artifact-writing end-to-end run that does not depend on optional branches.
