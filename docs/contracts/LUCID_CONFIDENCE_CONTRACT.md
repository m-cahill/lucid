# LUCID Confidence Contract

**Project:** LUCID  
**Benchmark Version:** 1.0.1  
**Document Type:** Governing Contract (Layer A)  
**Authority:** Confidence semantics  
**Status:** Frozen

---

## 1. Purpose

This contract defines what confidence means in LUCID and where it is read from.

Confidence is part of the benchmark output, not incidental metadata.

---

## 2. Canonical meaning

`confidence` is a scalar in `[0.0, 1.0]` representing the model’s claimed probability that its benchmark-facing typed action is correct under the benchmark’s scoring notion.

This meaning applies across all response modes:

- `ANSWER`
- `ABSTAIN`
- `CLARIFY`

---

## 3. Typed boundary

Official confidence is read only from the typed output field defined in `LUCID_OUTPUT_SCHEMA_CONTRACT.md`.

The scorer MUST NOT infer confidence from:

- hedging language
- “seems likely” style text
- token probabilities outside the typed contract
- free-form rationales

---

## 4. Benchmark role

Confidence exists to support:

- calibration analysis
- calibration lag analysis
- confidence overhang analysis
- abstention / clarification discipline

Confidence is not a decorative field.

---

## 5. Invariants

- Every typed benchmark response MUST include confidence.
- Confidence MUST be numeric and bounded in `[0.0, 1.0]`.
- Confidence interpretation MUST NOT silently change without change control.

---

## 6. One-line summary

> In LUCID, confidence is a scored benchmark output with fixed semantics, read only from the typed schema.
