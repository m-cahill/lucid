# LUCID Contract Index

**Project:** LUCID  
**Benchmark Version:** 1.0.1  
**Document Type:** Contract Index and Authority Map  
**Authority:** Meta-governing index for the contract set  
**Status:** Frozen contract map

---

## 1. Purpose

This document defines the contract map for LUCID.

LUCID is a benchmark for metacognitive calibration under instructional drift. The purpose of this contract set is to lock:

- what LUCID is
- what LUCID measures
- how LUCID serializes and scores benchmark runs
- what changes require formal change control
- how results may be reported without overstating support

This index is the entry point for the frozen contract set. It does not replace the contracts; it defines how they fit together.

---

## 2. Authority hierarchy

When documents disagree, use the following order of precedence:

1. **`LUCID_MOONSHOT.md`**  
   Governs project identity, ambition, faculty targeting, and benchmark philosophy.

2. **Layer A governing contracts**  
   Define what LUCID is and what it refuses to become.

3. **Layer B execution contracts**  
   Define how episodes, outputs, scoring, and artifacts are represented and evaluated.

4. **`LUCID_SUBMISSION_DOCTRINE.md`**  
   Governs writeup, disclosure, and reporting posture; it does not change runtime semantics.

5. **Implementation code, notebooks, and CI wiring**  
   Must satisfy the contracts above. If code disagrees with the frozen contracts, treat it as an implementation defect or an explicit change-control event.

This index is authoritative about document relationships, not about benchmark semantics beyond those relationships.

---

## 3. Normative language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are used in their normal normative sense.

- **MUST / MUST NOT** — mandatory requirements
- **SHOULD / SHOULD NOT** — strong default, deviation requires justification
- **MAY** — allowed but optional

---

## 4. Contract layers

## Layer A — Governing contracts

These contracts define the benchmark's identity-level invariants.

### 4.1 `LUCID_BENCHMARK_IDENTITY_CONTRACT.md`
Locks that LUCID is a benchmark, not a solver, and that its primary faculty is metacognition under instructional drift.

### 4.2 `LUCID_DRIFT_TAXONOMY_CONTRACT.md`
Locks the allowed drift families, drift severity, their semantics, and how drift is recorded.

### 4.3 `LUCID_CONFIDENCE_CONTRACT.md`
Locks the meaning of confidence, where it is read from, and how it relates to typed outputs.

### 4.4 `LUCID_MINIMAL_GREEN_PATH_CONTRACT.md`
Locks the smallest end-to-end runnable benchmark path that every milestone must preserve.

### 4.5 `LUCID_REFUSAL_CONTRACT.md`
Locks what LUCID refuses to become, including solver drift, faculty sprawl, multimodal theater, and subjective human grading of core metrics.

### 4.6 `LUCID_CHANGE_CONTROL.md`
Locks versioning and defines what changes are benchmark-semantic and therefore require formal version bumps and changelog entries.

---

## Layer B — Execution contracts

These contracts define machine-operational behavior.

### 4.7 `LUCID_EPISODE_STRUCTURE_CONTRACT.md`
Defines the canonical episode state machine, required and optional phases, legal transitions, and scoring eligibility windows.

### 4.8 `LUCID_OUTPUT_SCHEMA_CONTRACT.md`
Defines the typed benchmark-facing response schema and forbids scoring from free-form text outside that schema.

### 4.9 `LUCID_DETERMINISTIC_GENERATION_CONTRACT.md`
Defines the reconstructibility tuple and the determinism guarantees for episode generation.

### 4.10 `LUCID_TEMPLATE_FAMILY_CONTRACT.md`
Defines what a template family is, what it must declare, including family scoring notes, and why families are the unit of scientific explanation.

### 4.11 `LUCID_SCORING_CONTRACT.md`
Defines official metric formulas, leaderboard versus diagnostic metrics, weighting, and scoring-profile versioning.

### 4.12 `LUCID_ARTIFACT_BUNDLE_CONTRACT.md`
Defines the episode spec artifact, episode result artifact, bundle manifest, and canonical hashing/serialization rules.

---

## Non-runtime doctrine

### 4.13 `LUCID_SUBMISSION_DOCTRINE.md`
Defines reporting discipline: what must be disclosed, how claims should be framed, and what counts as unsupported overreach.

---

## 5. Cross-document invariants

The following invariants apply across the entire contract set.

### 5.1 No scoring from free-form text
No official scoring logic may depend on free-form text outside the typed output schema defined in `LUCID_OUTPUT_SCHEMA_CONTRACT.md`.

Free text MAY be stored for qualitative analysis, but it is not an official scoring input.

### 5.2 No silent semantic change
No benchmark-facing semantic change is allowed without either:

- a formal version bump under `LUCID_CHANGE_CONTROL.md`, or
- an explicit statement that the change is non-semantic

“Small tweaks” are not exempt if they alter:

- output interpretation
- drift semantics
- scoring logic
- episode phase semantics
- eligibility window semantics
- artifact meaning

### 5.3 One primary faculty
LUCID MUST remain a benchmark for metacognitive calibration under instructional drift.

Secondary analyses MAY be reported, but they MUST NOT redefine the benchmark’s flagship faculty.

### 5.4 Typed outputs are the scoring boundary
All official scoring, auditing, and replay MUST be possible using:

- the episode spec artifact
- the typed episode response
- the scoring profile
- the result artifact

The scorer MUST NOT require access to hidden chain-of-thought or undocumented parser heuristics.

### 5.5 Layer A must not depend on Layer B semantics
Layer A contracts define identity-level truth. They MUST NOT depend on mutable execution-layer semantics, implementation-specific parsing behavior, or scoring formula details beyond what is necessary to preserve benchmark identity.

---

## 6. Adjacent frozen documents

The following documents are adjacent to the contract set and SHOULD be retained alongside it:

- `LUCID_MOONSHOT.md`
- `LUCID_BOUNDARIES.md`
- `LUCID_ASSUMED_GUARANTEES.md`
- `LUCID_STACK_INTERACTION.md`

These documents provide project identity, substrate posture, and scope boundaries. They should not duplicate the contract set, but the contract set should remain consistent with them.

---

## 7. Recommended reading order

For a new engineer, researcher, or AI agent, the recommended reading order is:

1. `LUCID_MOONSHOT.md`
2. `LUCID_BENCHMARK_IDENTITY_CONTRACT.md`
3. `LUCID_OUTPUT_SCHEMA_CONTRACT.md`
4. `LUCID_EPISODE_STRUCTURE_CONTRACT.md`
5. `LUCID_DRIFT_TAXONOMY_CONTRACT.md`
6. `LUCID_DETERMINISTIC_GENERATION_CONTRACT.md`
7. `LUCID_TEMPLATE_FAMILY_CONTRACT.md`
8. `LUCID_SCORING_CONTRACT.md`
9. `LUCID_ARTIFACT_BUNDLE_CONTRACT.md`
10. `LUCID_CHANGE_CONTROL.md`
11. `LUCID_SUBMISSION_DOCTRINE.md`

---

## 8. One-line summary

> LUCID is a metacognition-first benchmark. Layer A locks its identity; Layer B locks its execution semantics; change control prevents quiet benchmark drift.
