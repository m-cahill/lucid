# LUCID Template Family Contract

**Project:** LUCID  
**Benchmark Version:** 1.0.1  
**Document Type:** Execution Contract (Layer B)  
**Authority:** Template family semantics  
**Status:** Frozen

---

## 1. Purpose

This contract defines what a template family is in LUCID and what it must declare.

Template families are the unit of scientific explanation, not just implementation convenience.

---

## 2. Required family fields

Every template family MUST declare:

- `family_id`
- `family_version`
- `rule_world_description`
- `allowed_rule_operators`
- `allowed_drift_operators`
- `output_domain`
- `ambiguity_contradiction_affordances`
- `difficulty_knobs`
- `family_scoring_notes`

---

## 3. Family scoring notes

`family_scoring_notes` is required.

It MUST explain any family-specific scoring expectations that are semantic but not meant to be rediscovered from code.

Example:

> In this family, ambiguity windows always begin immediately after drift onset and clarification is never offered.

This field exists to keep family-specific scoring assumptions explicit and auditable.

---

## 4. Invariants

- Families are the unit of scientific explanation and reporting.
- Families MUST NOT smuggle scoring semantics into undocumented generator code.
- Families MUST declare their scoring-relevant structure explicitly.

---

## 5. One-line summary

> In LUCID, a template family is a fully declared benchmark species: rule-world, drift affordances, difficulty knobs, and scoring notes included.
