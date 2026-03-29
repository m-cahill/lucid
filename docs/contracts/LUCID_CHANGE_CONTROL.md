# LUCID Change Control

**Project:** LUCID  
**Benchmark Version:** 1.0.1  
**Document Type:** Governing Contract (Layer A)  
**Authority:** Semantic versioning and contract-affecting changes  
**Status:** Frozen

---

## 1. Purpose

This contract defines how LUCID changes without silently changing meaning.

LUCID is a benchmark instrument. Benchmark-semantic changes require explicit versioning and documentation.

---

## 2. Versioning model

LUCID uses semantic-style benchmark versioning:

- **MAJOR** — breaking changes to benchmark meaning
- **MINOR** — additive but benchmark-semantic changes
- **PATCH** — clarifying or hardening changes that do not alter benchmark semantics

---

## 3. Contract-affecting changes

The following changes are benchmark-semantic and require formal change control:

- output schema changes
- scoring formula changes
- scoring weights or thresholds
- drift family definition changes
- drift severity semantics changes
- episode phase semantics changes
- eligibility window semantics changes
- artifact field meaning changes
- confidence interpretation changes
- template family semantics changes

---

## 4. Eligibility windows are semantic

Changes to detection, ambiguity, clarification, recovery, or final-resolution eligibility windows are semantic changes.

They MUST NOT be treated as innocuous implementation tweaks.

---

## 5. Current change classification

This 1.0.1 revision is a hardening pass over 1.0.0 that:

- adds drift severity
- clarifies legal state transitions
- tightens scientific and audit invariants
- does not widen the flagship faculty or change the benchmark’s core identity

It is intended as a non-breaking refinement of the frozen contract set.

---

## 6. One-line summary

> In LUCID, any change that alters what an episode means, what a score means, or when a model is eligible to be rewarded is a semantic change and must be versioned.
