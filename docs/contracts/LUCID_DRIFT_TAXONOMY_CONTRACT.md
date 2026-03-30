# LUCID Drift Taxonomy Contract

**Project:** LUCID  
**Benchmark Version:** 1.0.1  
**Document Type:** Governing Contract (Layer A)  
**Authority:** Drift family semantics  
**Status:** Frozen

---

## 1. Purpose

This contract defines the allowed drift families in LUCID and how they are recorded.

Drift is not a vague notion of “something changed.” It is a typed, auditable event in the rule environment.

---

## 2. Drift event requirement

Every scored LUCID episode MUST contain exactly one primary drift event.

That drift event MUST declare:

- `drift_type`
- `drift_severity`
- `drift_onset_turn`
- `drift_parameters`

Optional secondary annotations MAY exist, but they MUST NOT replace the primary typed drift event.

---

## 3. Allowed drift families

### 3.1 NEGATION
A rule flips polarity.

### 3.2 SCOPE
A rule changes the set over which it applies.

### 3.3 PRECEDENCE
Multiple rules remain valid, but their governing order changes.

### 3.4 EXCEPTION
A new exception overrides the earlier general rule.

### 3.5 AUTHORITY
A new source becomes authoritative over the prior source.

### 3.6 AMBIGUITY
The rule environment becomes underdetermined and requires uncertainty management.

### 3.7 CONTRADICTION
A new instruction directly conflicts with the earlier rule and should trigger guarded updating, abstention, or clarification.

---

## 4. Drift severity

Every drift event MUST declare `drift_severity`.

### 4.1 Allowed values
The canonical v1.0.1 severity enum is:

- `LOW`
- `MEDIUM`
- `HIGH`

### 4.2 Semantics
- `LOW` — subtle drift that should still be detectable by a calibrated model
- `MEDIUM` — clearly material drift without total rule-environment collapse
- `HIGH` — hard conflict, reversal, or severe instability in governing rule meaning

Severity is part of episode metadata, difficulty control, and family-level reporting. It MUST NOT be left implicit in generator code.

---

## 5. Recording rules

Each drift event MUST be reconstructible from the episode spec artifact using deterministic fields only.

The scorer MUST NOT infer drift type or severity from free-form narrative text.

---

## 6. Invariants

- Every scored episode MUST have a typed primary drift event.
- Drift type MUST come from the frozen family set above unless a version-bumped extension is introduced.
- Drift severity MUST be explicitly serialized.
- Drift semantics MUST remain compatible with the benchmark’s metacognitive identity.

---

## 7. One-line summary

> In LUCID, drift is typed, explicit, severity-marked, and reconstructible; it is never an informal narrative property of an episode.
