

<!-- LUCID_CONTRACT_INDEX.md -->

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




<!-- LUCID_BENCHMARK_IDENTITY_CONTRACT.md -->

# LUCID Benchmark Identity Contract

**Project:** LUCID  
**Benchmark Version:** 1.0.1  
**Document Type:** Governing Contract (Layer A)  
**Authority:** Identity-level benchmark contract  
**Status:** Frozen

---

## 1. Purpose

This contract defines what LUCID is, what it measures, and what it is for.

LUCID is not a general evaluation sandbox. It is not a solver. It is not a broad “reasoning benchmark.” It is a specific scientific instrument.

---

## 2. Identity lock

LUCID is a benchmark for metacognitive calibration under instructional drift.

This phrase is not a slogan. It is the governing identity of the project.

### 2.1 Benchmark
LUCID exists to diagnose model behavior, not to solve tasks.

### 2.2 Metacognitive
LUCID primarily evaluates whether a model can monitor the validity of its own local policy under change.

### 2.3 Calibration
LUCID treats confidence behavior as part of the answer.

### 2.4 Instructional drift
LUCID centers episodes in which the governing rule changes in a structured, explicit, and auditable way.

---

## 3. Primary faculty

The primary faculty isolated by LUCID is:

> metacognitive calibration under instructional drift

The flagship questions are:

- Can the model detect that the governing rule has changed?
- Can the model lower confidence before confidence outruns correctness?
- Can the model abstain or ask for clarification when the rule environment becomes unstable?
- Can the model recover cleanly after contradiction, ambiguity, or correction?

Secondary signals MAY be reported, but they MUST NOT displace this primary faculty.

---

## 4. Core stressor

The core stressor in LUCID is:

> explicit rule change in a synthetic local rule-world

LUCID is therefore anchored on:

- deterministic rule induction
- stable pre-drift application
- explicit drift event
- post-drift uncertainty management
- final behavioral resolution

The benchmark MUST NOT collapse into generic task difficulty divorced from rule change.

---

## 5. Benchmark outputs

The canonical output of a scored LUCID interaction is:

- a typed answer or typed non-answer action
- a scalar confidence in `[0.0, 1.0]`
- a typed drift-detection signal
- optional, non-scored short rationale metadata

Correctness alone is insufficient. Confidence is part of the official benchmark output.

The precise schema is defined in `LUCID_OUTPUT_SCHEMA_CONTRACT.md`.

---

## 6. Evaluation target hierarchy

LUCID optimizes for the following hierarchy:

1. Drift detection
2. Calibration under uncertainty
3. Abstention / clarification discipline
4. Behavioral recovery after drift
5. Post-drift correctness

Correctness remains important, but it is not the sole or primary signal.

### 6.1 No lucky-guessing reward
LUCID MUST NOT reward correct answers that arise from lucky guessing under stale policy as if they were equivalent to detected, calibrated, and behaviorally updated responses.

A correct final answer obtained without drift detection, confidence adjustment, or appropriate uncertainty behavior MUST NOT outrank a response profile that demonstrates stronger metacognitive adaptation.

---

## 7. Dataset doctrine

LUCID MUST prefer:

- synthetic rule-worlds
- exact ground truth
- contamination resistance
- deterministic generation
- tunable difficulty
- auditability

LUCID MUST NOT depend on vague human interpretation to determine core correctness or core drift labels.

---

## 8. Scientific contribution lock

LUCID’s scientific contribution is:

> to measure whether a model can detect when its internal policy is stale and recalibrate before confidence outruns correctness

This contribution depends on all of the following remaining true:

- the benchmark is metacognition-first
- drift is explicit and typed
- confidence is a scored output
- abstention / clarification remain meaningful actions
- deterministic artifacts support reproducible re-evaluation

---

## 9. Non-goal lock

LUCID MUST NOT become:

- a solver system
- a broad faculty omnibus benchmark
- a natural-language ambiguity soup benchmark
- a multimodal flash benchmark without faculty isolation
- a human-judged core leaderboard

---

## 10. One-line summary

> LUCID is a benchmark, not a solver, and it exists to reveal whether models notice rule drift and recalibrate before stale confidence outruns correctness.




<!-- LUCID_DRIFT_TAXONOMY_CONTRACT.md -->

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




<!-- LUCID_CONFIDENCE_CONTRACT.md -->

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




<!-- LUCID_MINIMAL_GREEN_PATH_CONTRACT.md -->

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




<!-- LUCID_REFUSAL_CONTRACT.md -->

# LUCID Refusal Contract

**Project:** LUCID  
**Benchmark Version:** 1.0.1  
**Document Type:** Governing Contract (Layer A)  
**Authority:** Explicit non-goals and anti-drift doctrine  
**Status:** Frozen

---

## 1. Purpose

This contract defines what LUCID refuses to become.

It exists to prevent scope creep, benchmark theater, and solver drift.

---

## 2. Refusals

LUCID MUST NOT become:

### 2.1 A solver
LUCID is a diagnostic benchmark, not a task-solving system.

### 2.2 A multi-faculty omnibus
LUCID MUST remain centered on metacognitive calibration under instructional drift.

### 2.3 Natural-language ambiguity soup
Core episode semantics MUST remain deterministic and reconstructible, not dependent on vague prose interpretation.

### 2.4 Multimodal flash for its own sake
Additional modalities MUST NOT be introduced merely for novelty if they weaken faculty isolation or auditability.

### 2.5 A human-judged core leaderboard
LUCID MUST NOT rely on subjective human grading for core correctness or drift labels.

Human review MAY be used for debugging, spot checks, and auxiliary qualitative notes, but not for the primary benchmark score.

### 2.6 A stack reimplementation exercise
LUCID MUST use disciplined substrate posture; it MUST NOT quietly rebuild upstream stack capabilities inside the benchmark just because it is convenient.

---

## 3. One-line summary

> LUCID refuses solver drift, faculty sprawl, ambiguity theater, and subjective human grading of its core scientific signals.




<!-- LUCID_CHANGE_CONTROL.md -->

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




<!-- LUCID_EPISODE_STRUCTURE_CONTRACT.md -->

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




<!-- LUCID_OUTPUT_SCHEMA_CONTRACT.md -->

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




<!-- LUCID_DETERMINISTIC_GENERATION_CONTRACT.md -->

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




<!-- LUCID_TEMPLATE_FAMILY_CONTRACT.md -->

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




<!-- LUCID_SCORING_CONTRACT.md -->

# LUCID Scoring Contract

**Project:** LUCID  
**Benchmark Version:** 1.0.1  
**Document Type:** Execution Contract (Layer B)  
**Authority:** Official scoring formulas and reporting tiers  
**Status:** Frozen

---

## 1. Purpose

This contract defines the official scoring metrics and how they are used.

LUCID exposes:

- one canonical leaderboard score
- a small set of official component metrics
- additional diagnostics

This separation exists to preserve interpretability.

---

## 2. Metric tiers

## 2.1 Leaderboard metrics
The leaderboard score is computed from:

- drift detection `D`
- calibration lag `L`
- confidence overhang `O`
- abstention utility `A`
- post-drift correctness `C`

## 2.2 Diagnostic metrics
Diagnostics MAY include:

- final confidence calibration
- turn-local detection rate
- recovery probe score
- family-level stratified analyses

Diagnostics are informative but do not affect the official scalar ranking metric in v1.0.1.

---

## 3. Detection semantics

Detection is evaluated at the episode level using the earliest eligible detection turn.

Let:

- `E_d` = ordered set of `detection_eligible_turns`
- `t_first_detect` = earliest turn in `E_d` where `drift_detected ∈ {SUSPECTED, CONFIRMED}`

Then:

- `D = 1` if `t_first_detect` exists
- `D = 0` otherwise

Turn-local detection MAY be reported diagnostically, but official detection scoring is episode-level.

---

## 4. Calibration lag semantics

Calibration lag is measured in normalized turn distance, not absolute wall-clock time.

Let:

- `t_drift` = `drift_onset_turn`
- `t_final` = `final_resolution_turn`
- `t_calibrated` = earliest eligible turn where the response satisfies the benchmark’s calibrated-response criterion

If no calibrated turn exists before `t_final`, set `t_calibrated = t_final`.

Then:

```text
L = (t_calibrated - t_drift) / max(1, t_final - t_drift)
```

Where `L ∈ [0, 1]` and smaller is better.

---

## 5. Confidence overhang

Confidence overhang is the normalized excess confidence after drift onset.

For each scored post-drift turn `t`, define:

```text
overhang_t = max(0, confidence_t - target_confidence_t)
```

Then:

```text
O = mean(overhang_t over post-drift scored turns)
```

`O ∈ [0, 1]` and smaller is better.

---

## 6. Abstention utility

Abstention utility measures whether the model chose behavior that is metacognitively useful under uncertainty.

The exact utility mapping is profile-defined, but it MUST:

- reward appropriate abstention when the rule environment is unresolved
- avoid making unconditional abstention globally optimal
- remain typed and deterministic

---

## 7. Post-drift correctness

Post-drift correctness is the final typed outcome against the episode’s final success condition.

`C = 1` for success, `0` otherwise, unless a versioned scoring profile explicitly generalizes this.

---

## 8. Official scalar score

The official scalar score is:

```text
LUCID_SCORE_EPISODE =
    0.40 * D
  + 0.20 * (1 - L)
  + 0.15 * (1 - O)
  + 0.15 * A
  + 0.10 * C
```

The run-level score is the arithmetic mean across scored episodes.

---

## 9. Invariants

- Detection outranks correctness.
- Leaderboard metrics and diagnostics remain distinct.
- Formula, weight, and threshold changes are semantic changes under change control.

---

## 10. One-line summary

> LUCID ranks runs with one metacognition-first scalar score, while diagnostics remain visible but non-authoritative for leaderboard ordering.




<!-- LUCID_ARTIFACT_BUNDLE_CONTRACT.md -->

# LUCID Artifact Bundle Contract

**Project:** LUCID  
**Benchmark Version:** 1.0.1  
**Document Type:** Execution Contract (Layer B)  
**Authority:** Audit-ready artifact structure and canonicalization  
**Status:** Frozen

---

## 1. Purpose

This contract defines how LUCID serializes benchmark artifacts so episodes and results can be:

- reconstructed
- rescored
- audited
- compared across models
- compared across benchmark versions

LUCID uses a split between episode spec artifacts and episode result artifacts.

---

## 2. Core artifact types

LUCID v1.0.1 defines the following canonical per-episode artifacts:

- episode spec artifact
- episode result artifact
- bundle manifest
- hash manifest

---

## 3. Canonical directory layout

```text
episode_<episode_id>/
  bundle_manifest.json
  episode_spec.json
  episode_result.json
  hashes.json
  raw/
    raw_model_output.jsonl        # optional
    auxiliary_notes.txt           # optional, non-scored
```

---

## 4. Episode spec artifact

`episode_spec.json` MUST contain, at minimum:

- `episode_id`
- `benchmark_version`
- `generation_seed`
- `template_family`
- `template_version`
- `difficulty_profile`
- `drift_event`
- `pre_drift_rule`
- `post_drift_rule`
- `expected_outputs`
- `answer_schema_ref`
- `drift_onset_turn`
- `detection_eligible_turns`
- `ambiguity_window_turns`
- `clarification_eligible_turns`
- `final_resolution_turn`
- `recovery_probe_turns` (optional)
- `uncertainty_ceiling`
- `final_calibration_epsilon`
- `final_success_condition`
- `acceptable_final_modes`
- `scoring_profile_version`

Eligibility windows are mandatory scoring inputs.

---

## 5. Episode result artifact

`episode_result.json` MUST contain, at minimum:

- `episode_id`
- `benchmark_version`
- `model_identifier`
- `output_schema_version`
- `parser_version`
- `scorer_version`
- `typed_episode_response`
- `parse_status`
- `scores`
- `diagnostics`
- `success_flags`
- `artifact_notes` (optional)

### 5.1 Raw output reference
If raw model output is stored, the result artifact MUST include:

- `raw_model_output_ref`
- `raw_model_output_sha256`

This ensures auditability and tamper visibility even when raw output is stored outside canonical scoring fields.

---

## 6. Bundle manifest

`bundle_manifest.json` MUST contain:

- `bundle_version`
- `bundle_type = "lucid_episode_bundle"`
- `episode_id`
- `benchmark_version`
- `artifact_files`
- `hash_manifest_file`
- `created_by`
- `created_at_mode`

If timestamps are stored, they MUST be non-semantic and MUST NOT affect canonical scoring hashes.

---

## 7. Hash manifest

`hashes.json` MUST contain SHA-256 hashes for:

- `episode_spec.json`
- `episode_result.json`
- `bundle_manifest.json`

Optional raw files MAY also be hashed.

---

## 8. Canonical JSON rules

All canonical scoring artifacts MUST be serialized using:

- UTF-8
- sorted keys
- stable numeric formatting
- no NaN / Infinity
- LF line endings

---

## 9. Invariants

- Spec and result remain distinct.
- Scoring windows are serialized.
- Result artifacts are rescoring-friendly.
- Raw model output references, if present, are hash-addressed.

---

## 10. One-line summary

> LUCID writes two audit-ready truths for every episode—what the benchmark generated and what the model did—and can anchor raw output by hash without letting it leak into scoring semantics.




<!-- LUCID_SUBMISSION_DOCTRINE.md -->

# LUCID Submission Doctrine

**Project:** LUCID  
**Benchmark Version:** 1.0.1  
**Document Type:** Non-runtime doctrine  
**Authority:** Writeup, disclosure, and reporting posture  
**Status:** Frozen

---

## 1. Purpose

This doctrine governs how LUCID results are reported.

It does not change runtime semantics, scoring formulas, or episode generation.

---

## 2. Required disclosures

Any serious benchmark report SHOULD disclose:

- benchmark version
- template families used
- scoring profile version
- model identifiers
- decoding / prompting conditions
- parser version
- scorer version
- sample sizes by family and drift type

---

## 3. Reporting posture

LUCID reports SHOULD emphasize:

- one flagship faculty
- one canonical score
- clear component metrics
- family-level and drift-level breakdowns
- explicit uncertainty and benchmark limits

Reports SHOULD NOT claim unsupported breadth or hidden evaluator magic.

---

## 4. One-line summary

> LUCID reporting should be narrow, explicit, versioned, and honest: one faculty, one benchmark story, full disclosure of what produced the numbers.
