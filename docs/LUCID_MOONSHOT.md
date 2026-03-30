# LUCID Moonshot

**Project:** LUCID  
**Expansion:** *Latent Update & Calibration under Instructional Drift*  
**Role:** Governing moonshot anchor for the project  
**Intended use:** This document fixes the project’s ambition, identity, benchmark philosophy, and strategic constraints so that future plans and implementation choices can be derived from it rather than renegotiated.

---

## 1. Why LUCID exists

LUCID exists to build a competition-grade benchmark for evaluating whether frontier models can **detect, admit, and adapt to instructional drift before their confidence outruns their correctness**.

The project’s belief is simple:

> models do not fail only because they are wrong; they also fail because they do not realize that the governing rule has changed.

LUCID is therefore **not** a solver, **not** a prompt pack, and **not** a model performance vanity project.  
It is a **diagnostic benchmark**.

---

## 2. The moonshot

> **Build a metacognition-first benchmark that reveals whether a model can detect when its internal policy is stale and recalibrate under controlled instructional drift.**

In its fullest form, LUCID should be able to:

- present a model with a compact synthetic rule-world
- induce a local instruction policy
- introduce a controlled drift event
- measure whether the model notices the drift
- measure whether the model updates confidence appropriately
- measure whether the model recovers behaviorally after contradiction, ambiguity, or correction
- do all of the above reproducibly, auditably, and at benchmark scale

The moonshot is **not** merely to see whether a model answers correctly.  
The moonshot is to see whether a model can **track the validity of its own policy under change**.

---

## 3. What competition LUCID is trying to win

LUCID is designed for the **Kaggle Measuring AGI** competition as a **benchmark construction** entry, not as a task-solving system.

That matters.

The project is optimized around the realities of the competition:

- dataset quality outranks almost everything else
- cognitive faculty isolation matters
- novelty must reveal a new behavioral signal
- the benchmark must produce a useful gradient, not a trivial pass/fail wall

LUCID is therefore built to maximize:

- **defensible task construction**
- **scientifically meaningful metacognitive signals**
- **high reproducibility**
- **clear writeup story**
- **clean faculty targeting**

---

## 4. What LUCID is

LUCID is a **metacognitive drift benchmark**.

Its canonical shape is:

```text
Instruction Episode
  → Model infers local policy
  → Drift event changes governing rule
  → Model answers + reports confidence
  → Benchmark measures detection, calibration, and recovery
```

On richer episodes, the canonical shape becomes:

```text
Instruction Episode
  → Stable rule-learning phase
  → Drift injection
  → Ambiguity / contradiction window
  → Optional clarification opportunity
  → Final answer + confidence + abstain/clarify choice
```

This means the center of gravity is:

- metacognition
- calibration
- rule change detection
- confidence adjustment
- recovery under drift

not:

- raw problem-solving difficulty
- long-chain reasoning aesthetics
- multimodal flashiness for its own sake
- benchmark-as-solver confusion

---

## 5. The north star system identity

LUCID should be understood as:

> **a benchmark for metacognitive calibration under instructional drift**

That phrasing is important.

- **Benchmark** means LUCID diagnoses models rather than trying to outperform them on tasks.
- **Metacognitive** means the primary target is self-monitoring, not raw competence.
- **Calibration** means confidence behavior matters as much as answer behavior.
- **Instructional drift** means the model is evaluated under rule change, not static prompt interpretation.

---

## 6. The system thesis

LUCID assumes that a strong cognitive benchmark in this competition should test not just whether a model can follow a rule, but whether it can **notice when the rule environment changes**.

This is the system thesis:

> the deepest failures under drift are not merely wrong answers, but stale internal policies that remain overconfident after the rule has changed.

That is what LUCID exists to expose.

---

## 7. The benchmark philosophy

LUCID is built around three benchmark beliefs.

### 7.1 Synthetic over natural-language ambiguity

Natural-language benchmarks often look realistic but are hard to defend.  
LUCID prefers synthetic rule-worlds because they offer:

- exact ground truth
- controlled drift
- zero leakage by design
- tunable difficulty
- reproducibility
- faculty isolation

### 7.2 Calibration over raw correctness

Correctness still matters, but a benchmark entry for this competition should be strongest where it reveals what ordinary accuracy metrics miss.

LUCID therefore privileges:

- confidence alignment
- honest uncertainty
- drift detection
- abstention behavior
- correction after contradiction

### 7.3 Scientific instrument over benchmark theater

LUCID must feel like a **real measurement instrument**, not a clever prompt trick.  
Every task family should be explainable in terms of:

- the faculty being isolated
- the drift being introduced
- the behavioral expectation being measured
- the scoring signal being extracted

---

## 8. The benchmark contract

Every LUCID task family and every individual episode must satisfy the following contract.

### 8.1 Deterministic rule-world

Every episode is programmatically generated from a seed and a fixed generation profile.

This ensures:

- exact reproducibility
- unambiguous ground truth
- inspectable generation logic
- no hidden annotation subjectivity

### 8.2 Explicit drift moment

Every episode must contain a known, explicit drift event.

That event may occur as:

- negation
- scope change
- precedence reversal
- exception insertion
- authority override
- contradiction
- clarification that resolves earlier ambiguity

Each episode must record:

- where the drift occurs
- what type of drift it is
- what new behavioral expectation it creates

### 8.3 Confidence-bearing output

The model must provide both:

- an answer
- a scalar confidence estimate in `[0.0, 1.0]`

LUCID is not complete if only answer accuracy is captured.

### 8.4 Calibration opportunity

Each episode must include a defined region in which a well-calibrated model should either:

- lower confidence
- abstain
- ask for clarification
- explicitly identify that the governing rule may have changed

This is the **ambiguity window**.  
It exists to measure metacognitive honesty, not just final answer accuracy.

### 8.5 Audit-ready episode record

Every episode must be reconstructible as a benchmark artifact containing at minimum:

- generation seed
- episode template family
- pre-drift rule
- drift type
- expected post-drift rule
- target outputs
- scoring metadata

---

## 9. The drift taxonomy

LUCID should not treat instructional drift as one vague concept.  
It should define explicit drift families.

### 9.1 Negation drift
A rule flips polarity.

Example shape:

```text
Before: select items that satisfy property P
After: select items that do NOT satisfy property P
```

### 9.2 Scope drift
A rule changes the set over which it applies.

Example shape:

```text
Before: apply to all items
After: apply only to items in subset S
```

### 9.3 Precedence drift
Two or more rules retain validity, but the governing order changes.

Example shape:

```text
Before: Rule A overrides Rule B
After: Rule B overrides Rule A
```

### 9.4 Exception drift
A new exception is introduced that overrides the prior general rule.

Example shape:

```text
Before: all X follow rule R
After: all X follow rule R except class E
```

### 9.5 Authority drift
A new source supersedes the earlier controlling instruction.

Example shape:

```text
Before: follow instruction from source A
After: source B becomes authoritative
```

### 9.6 Ambiguity drift
An initially underdetermined situation receives clarifying information that should trigger confidence adjustment.

### 9.7 Contradiction drift
A new instruction directly conflicts with the earlier rule and should trigger explicit uncertainty, clarification, or guarded updating.

This taxonomy is not decoration.  
It is one of the benchmark’s scientific backbones.

---

## 10. The canonical episode structure

A LUCID episode should generally follow this shape:

```text
Phase 1: Local rule induction
Phase 2: Stable application
Phase 3: Drift event
Phase 4: Ambiguity / contradiction window
Phase 5: Answer + confidence + optional abstain / clarify
Phase 6: Optional correction / recovery turn
```

This enables LUCID to measure not only whether the model is right, but:

- whether it notices the drift
- whether it lowers confidence in time
- whether it persists with stale behavior
- whether it recovers after being corrected

---

## 11. The minimal green path

Every milestone must preserve a minimal runnable path:

```text
Generate deterministic episode
  → induce local policy
  → inject one explicit drift event
  → collect answer + confidence
  → score detection + calibration + correctness
  → produce benchmark artifact bundle
```

This is the project’s non-negotiable executable spine.

If a proposed change breaks the minimal green path, it is a deviation and must be explicitly justified.

---

## 12. Dataset defensibility doctrine

Because dataset quality is the competition’s heaviest scoring axis, LUCID must treat defensibility as a first-class design doctrine.

### 12.1 Contamination resistance

LUCID uses synthetic rule-worlds because they resist training-set contamination by design.

The benchmark should not reward memorization of known tasks, examples, or public benchmark artifacts.  
It should reward real adaptation to fresh local rules and rule changes.

### 12.2 Parameterization

Each episode family must expose tunable parameters such as:

- drift type
- drift severity
- rule complexity
- ambiguity depth
- contradiction strength
- clarification timing
- distractor pressure

This enables a clean **difficulty gradient** rather than a single brittle benchmark level.

### 12.3 Auditability

Every task instance must be reconstructible from:

- generation seed
- template family
- drift parameters
- canonical scoring profile

This allows:

- exact regeneration
- audit review
- deterministic reruns
- leaderboard-independent benchmarking discipline

### 12.4 Statistical scaling

Synthetic generation is not merely a convenience.  
It enables statistically meaningful sample sizes without sacrificing label quality.

### 12.5 Benchmark honesty

LUCID should explicitly prefer a narrower, cleaner, more defensible benchmark over a broader but less auditable one.

---

## 13. How LUCID wins

LUCID wins if it becomes better than ordinary static benchmarks at revealing the behavior that actually matters under change.

A strong LUCID benchmark should expose:

- overconfidence after drift
- late confidence collapse
- stale-rule perseveration
- false certainty under contradiction
- inability to identify that a rule has changed
- poor abstention judgment
- weak recovery after correction

The benchmark’s advantage is not just that it measures failure.  
Its advantage is that it measures **how the model understands its own failure risk**.

---

## 14. What success looks like

### 14.1 Competition success

At the competition layer, success means:

- the benchmark is clearly scoped to one primary faculty
- judges immediately understand the insight it reveals
- the dataset is visibly defensible
- the benchmark produces a meaningful performance gradient
- the writeup feels scientifically grounded rather than speculative

### 14.2 Project success

At the project layer, success means:

- LUCID becomes a reusable evaluation pattern for drift-sensitive cognition
- the benchmark remains reproducible and auditable
- benchmark improvements are measurable rather than rhetorical
- each milestone deepens the instrument without blurring its identity

### 14.3 Moonshot success

At the highest level, success means:

> LUCID demonstrates that metacognitive calibration under rule change is a measurable cognitive faculty and that current models can be distinguished by how quickly and honestly they adapt when their internal policy becomes stale.

---

## 15. Role of the stack

LUCID is not starting from zero.  
It stands on a disciplined stack and should benefit from it without becoming a stack reimplementation exercise.

### 15.1 CLARITY

CLARITY informs the benchmark’s evaluation posture:

- perturbation sweeps
- robustness surfaces
- metrics over narrative
- controlled stress testing under change

### 15.2 DARIA

DARIA informs the benchmark’s execution posture:

- deterministic generation and episode execution
- artifact bundles
- run reproducibility
- audit-friendly benchmark traces

### 15.3 Foundry

Foundry informs the benchmark’s architecture posture:

- role separation
- clean composition
- additive orchestration
- small, auditable, reversible changes

### 15.4 RediAI

RediAI informs the benchmark’s governance posture:

- certification thinking
- truthful CI
- evidence-backed promotion
- competition-grade audit discipline

### 15.5 Sibling project doctrine

LUCID and MYTHOS may share the same deterministic substrate posture, but they serve opposite architectural roles.

- **MYTHOS** is a **solver** project focused on performance optimization for reasoning outcomes.
- **LUCID** is a **benchmark** project focused on diagnostic evaluation of model behavior.

They may share substrate discipline, but they must never be confused in identity.

LUCID does not exist to solve tasks.  
It exists to diagnose how models behave under drift.

---

## 16. Guiding principles

1. **Benchmark first.** LUCID is an evaluation instrument, not a solver.
2. **Faculty isolation over benchmark sprawl.** One sharp faculty outranks shallow multidomain coverage.
3. **Synthetic over anecdotal.** Programmatic task generation beats hard-to-defend hand-authored ambiguity.
4. **Calibration over theatrics.** Honest uncertainty is a first-class signal.
5. **Detection before recovery.** A model should first notice drift before being praised for post-hoc adjustment.
6. **Abstention is useful.** Correctly refusing to overclaim is part of intelligence.
7. **Determinism matters.** Every meaningful benchmark result should be reproducible.
8. **Artifacts over anecdotes.** Evaluation claims must be inspectable.
9. **Difficulty should be tunable.** Drift should scale along a controlled gradient.
10. **The benchmark must remain legible.** Cleverness that obscures what is being measured is a failure mode.

---

## 17. What LUCID refuses to be

LUCID should explicitly refuse several bad futures.

### 17.1 Solver drift
A project that quietly becomes a task-solving system rather than a diagnostic benchmark.

### 17.2 Benchmark theater
A project that sounds clever but cannot defend task construction scientifically.

### 17.3 Natural-language ambiguity soup
A project that depends on vague human interpretation rather than clean ground truth.

### 17.4 Faculty sprawl
A project that tries to measure everything and therefore isolates nothing.

### 17.5 Stack confusion
A project that quietly rebuilds upstream stack capabilities instead of using them as disciplined substrate.

These refusal modes are part of the project’s identity, not side notes.

---

## 18. Core evaluation signals

The benchmark’s evaluation signals must reflect its metacognitive identity.

### 18.1 Drift detection accuracy
Can the model identify that the governing rule has changed?

### 18.2 Post-drift task accuracy
Can the model answer correctly after the drift event?

### 18.3 Confidence calibration
How well does reported confidence align with actual correctness?

### 18.4 Calibration lag
How many turns or episodes pass before confidence behavior catches up to the changed rule environment?

This is one of LUCID’s signature metrics.

### 18.5 Confidence overhang
How long does stale high confidence persist after drift?

### 18.6 Abstention utility
Does the model appropriately abstain or ask for clarification when the governing rule is contradictory or unresolved?

### 18.7 Recovery after correction
When clarification or corrective feedback is given, how quickly and cleanly does the model update?

### 18.8 Secondary cross-faculty signals
These are not the flagship faculty, but they can appear as secondary analyses:

- stale-rule perseveration
- distractor sensitivity
- ambiguity-induced attentional inertia
- delayed inhibitory switching

---

## 19. Scoring philosophy

LUCID must move beyond raw answer accuracy.

Its scoring hierarchy should privilege metacognitive honesty.

### 19.1 Calibration over correctness

A model that is honestly uncertain when it is wrong is more cognitively trustworthy than a model that is accidentally right while systematically miscalibrated.

### 19.2 Detection over blind answering

Explicitly identifying that a rule has changed is a stronger metacognitive signal than merely stumbling into the correct post-drift answer.

### 19.3 Abstention utility

The benchmark should reward models that appropriately choose:

- `ABSTAIN`
- `CLARIFY`
- low-confidence guarded outputs

when the governing rule is unresolved or contradictory.

### 19.4 Recovery over rationalization

When corrected, a strong model should update behavior rather than justify stale reasoning.

### 19.5 Confidence behavior is part of the answer

In LUCID, confidence is not metadata.  
It is part of the benchmark output.

---

## 20. The benchmark’s scientific contribution

LUCID’s scientific contribution should be stated plainly:

LUCID contributes a new dimension to AGI evaluation by isolating **metacognitive calibration under instructional drift**.

It does not merely ask whether a model can answer after a rule change.  
It asks whether the model can detect that its internal policy is stale, lower confidence appropriately, abstain when warranted, and recover behaviorally before confidence outruns correctness.

That is the benchmark’s research value.

---

## 21. Problem scope and non-goals

### 21.1 Early focus classes

LUCID should begin with clean synthetic instruction environments where faculty isolation is easiest to defend:

- symbolic rule application
- local policy induction
- contradiction and clarification episodes
- scoped override logic
- controlled distractor insertion

### 21.2 Explicit non-goals

LUCID is **not** optimizing for:

- visual impressiveness
- multimodal novelty for its own sake
- arbitrary solver difficulty
- explanation elegance
- benchmark breadth at the cost of clarity

Correct diagnosis outranks surface flash.

---

## 22. One-sentence anchor

> **LUCID contributes a new dimension to AGI evaluation by isolating the metacognitive calibration faculty: it reveals whether a model can detect when its internal policy is stale and update its behavior before its confidence outruns its correctness.**

---

## 23. What this document locks

This moonshot document locks the following truths:

- LUCID is a **benchmark**, not a solver
- the primary faculty is **metacognition**
- the canonical stressor is **instructional drift**
- synthetic deterministic rule-worlds are preferred
- confidence behavior is part of the benchmark output
- calibration lag is a signature metric
- abstention and clarification are valuable benchmark behaviors
- future plans must preserve a clean scientific instrument identity

Anything that conflicts with these points should be treated as a proposed deviation, not a casual extension.

---

## 24. Immediate implication for the next document set

Because this moonshot is now fixed, the next project documents should answer only these questions:

- what benchmark families exist first
- how episodes are generated
- how drift parameters are encoded
- how scoring is computed
- what artifact bundle each run must produce
- what minimal implementation proves the benchmark end to end

Those documents should elaborate the instrument, not redefine the ambition.
