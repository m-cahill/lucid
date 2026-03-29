# LUCID Change Control

**Project:** LUCID  
**Benchmark Version:** 1.1.0  
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

## 5. Release classification (active)

### 5.1 Benchmark **1.1.0** (M00 — scoring semantic lock)

This **MINOR** benchmark release:

- introduces `LUCID_SCORING_PROFILE_v1.1.0.md` with fully specified `target_confidence_t`, calibrated-response criterion, and abstention utility `A`
- updates `LUCID_SCORING_CONTRACT.md` to reference the profile (official scorer behavior is no longer underspecified)
- does **not** change top-level scalar weights (`0.40/0.20/0.15/0.15/0.10`)
- does not widen the flagship faculty or change episode/artifact schemas beyond profile-linked semantics already implied by scoring

Historical contract exports may remain labeled **1.0.1** in the archive; the **active** benchmark line is **1.1.0** after M00.

### 5.2 Benchmark **1.0.1** (historical)

The 1.0.1 revision was a hardening pass over 1.0.0 that:

- adds drift severity
- clarifies legal state transitions
- tightens scientific and audit invariants

The concatenated export `docs/archive/LUCID_contracts_master_bundle_v1.0.1_ARCHIVED.md` captures the pre–profile-lock split contracts.

---

## 6. One-line summary

> In LUCID, any change that alters what an episode means, what a score means, or when a model is eligible to be rewarded is a semantic change and must be versioned.
