# LUCID Output Schema Contract

**Project:** LUCID  
**Benchmark Version:** 1.0.1  
**Document Type:** Execution Contract (Layer B)  
**Authority:** Typed benchmark-facing response schema  
**Status:** Frozen

---

## 1. Purpose

This contract defines the only official schema from which benchmark scoring may read model behavior.

Free-form text MAY be stored, but it is not an official scoring input.

---

## 2. Canonical response object

The canonical typed response object is `EpisodeResponse`.

### 2.1 Required fields

| Field | Type | Required | Notes |
|---|---|---:|---|
| `answer` | family-defined typed value or null | yes | Required when `response_mode = ANSWER`; otherwise null |
| `confidence` | float in `[0.0, 1.0]` | yes | Official confidence |
| `response_mode` | enum | yes | `ANSWER`, `ABSTAIN`, `CLARIFY` |
| `drift_detected` | enum | yes | `NONE`, `SUSPECTED`, `CONFIRMED` |

### 2.2 Optional fields

| Field | Type | Required | Notes |
|---|---|---:|---|
| `rationale_stub` | short string or null | no | Non-chain-of-thought, non-scored |
| `response_timestamp` | string or number | no | Non-semantic operational metadata; MUST NOT affect canonical hashing or scoring |

---

## 3. Schema rules

### 3.1 `answer`
The answer domain is family-defined. It MUST be typed, not interpreted from prose.

### 3.2 `confidence`
Confidence MUST be numeric and bounded in `[0.0, 1.0]`.

### 3.3 `response_mode`
Allowed values:

- `ANSWER`
- `ABSTAIN`
- `CLARIFY`

### 3.4 `drift_detected`
Allowed values:

- `NONE`
- `SUSPECTED`
- `CONFIRMED`

This field is typed to distinguish no detection from guarded suspicion and explicit confirmation.

---

## 4. Parsing boundary

Official scoring MUST read only from typed fields in the canonical response object.

The scorer MUST NOT infer benchmark actions from:

- hedge words
- apology language
- long rationale text
- hidden chain-of-thought
- out-of-band metadata

---

## 5. Invariants

- Every scored response MUST conform to this schema.
- `response_timestamp`, if present, is non-semantic.
- Free-form text is not a scoring boundary.

---

## 6. One-line summary

> In LUCID, official model behavior is whatever the typed response schema says it is—nothing more, nothing less.
