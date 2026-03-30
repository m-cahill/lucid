# LUCID Episode Structure Contract

**Project:** LUCID  
**Benchmark Version:** 1.0.1  
**Document Type:** Execution Contract (Layer B)  
**Authority:** Canonical episode state machine  
**Status:** Frozen

---

## 1. Purpose

This contract defines the canonical episode structure in LUCID.

Episodes are not arbitrary prompts. They are stateful benchmark instruments with typed phases and typed scoring eligibility windows.

---

## 2. Canonical episode spine

A canonical scored episode follows this conceptual order:

```text
RULE_INDUCTION
→ STABLE_APPLICATION
→ DRIFT_EVENT
→ DRIFT_RESPONSE_WINDOW
→ FINAL_RESOLUTION
→ RECOVERY_PROBE (optional)
```

Optional clarification branching MAY occur within `DRIFT_RESPONSE_WINDOW`.

---

## 3. Phase semantics

### 3.1 RULE_INDUCTION
The episode teaches or establishes the local policy.

- required: yes
- repeatable: no
- scored: context only

### 3.2 STABLE_APPLICATION
The model applies the pre-drift rule under stable conditions.

- required: yes
- repeatable: no
- scored: optional diagnostic only

### 3.3 DRIFT_EVENT
The governing rule changes.

- required: yes
- repeatable: no in v1.x
- scored: anchor only

### 3.4 DRIFT_RESPONSE_WINDOW
The model has an opportunity to detect drift, lower confidence, abstain, or ask for clarification.

- required: yes
- repeatable: yes if encoded by family, but the family must declare this
- scored: yes

### 3.5 FINAL_RESOLUTION
The model must issue a final typed benchmark action.

- required: yes
- repeatable: no
- scored: yes

### 3.6 RECOVERY_PROBE
Optional post-resolution probe to measure update quality after clarification or correction.

- required: no
- repeatable: family-dependent
- scored: diagnostic by default

---

## 4. Clarification branch

Clarification is a branch, not a universal obligation.

A family MAY expose:

```text
DRIFT_RESPONSE_WINDOW
→ CLARIFICATION_OFFERED
→ CLARIFICATION_RESPONSE
→ FINAL_RESOLUTION
```

But clarification MUST be explicitly encoded in the episode spec; it MUST NOT be inferred from prose.

---

## 5. Legal transitions

The following canonical transition table applies in v1.0.1.

| From | To | Allowed |
|---|---|---|
| RULE_INDUCTION | STABLE_APPLICATION | yes |
| STABLE_APPLICATION | DRIFT_EVENT | yes |
| DRIFT_EVENT | DRIFT_RESPONSE_WINDOW | yes |
| DRIFT_RESPONSE_WINDOW | CLARIFICATION_OFFERED | optional |
| DRIFT_RESPONSE_WINDOW | FINAL_RESOLUTION | yes |
| CLARIFICATION_OFFERED | CLARIFICATION_RESPONSE | yes |
| CLARIFICATION_RESPONSE | FINAL_RESOLUTION | yes |
| FINAL_RESOLUTION | RECOVERY_PROBE | optional |

Transitions not listed above SHOULD be treated as forbidden unless a version-bumped family extension explicitly allows them.

---

## 6. Eligibility windows

Every scored episode MUST serialize the following scoring windows where applicable:

- `drift_onset_turn`
- `detection_eligible_turns`
- `ambiguity_window_turns`
- `clarification_eligible_turns`
- `final_resolution_turn`
- `recovery_probe_turns` (optional)

These are semantic scoring inputs, not optional notes.

---

## 7. Invariants

- FINAL_RESOLUTION is mandatory for all scored episodes.
- Clarification remains optional unless an episode family explicitly requires its offer semantics.
- Zero-shot drift detection before final resolution is allowed only within declared detection-eligible turns.
- Legal transitions MUST remain explicit.

---

## 8. One-line summary

> LUCID episodes are governed by a typed state machine with explicit legal transitions and serialized scoring windows.
