# LUCID boundaries

**Project:** LUCID  
**Benchmark version:** 1.1.0 (active profile)  
**Document type:** Adjacent governance — integration and ownership boundaries  
**Status:** Canonical

---

## 1. Purpose

This document defines what LUCID **owns**, what it **refuses to own**, and where **integration boundaries** sit so the benchmark cannot drift into solver mode, omnibus evaluation, or platform-specific semantics inside the core.

---

## 2. What LUCID owns

- A **deterministic**, **typed**, **auditable** benchmark for **metacognitive calibration under instructional drift**
- **Synthetic rule-worlds** with explicit drift events and reconstructible episode specs
- **Official scoring** derived only from **typed** outputs and **declared** eligibility windows (see contracts)
- **Artifact bundles** (episode spec + episode result + manifests + hashes) suitable for audit and rescoring

---

## 3. What LUCID does not own

- **Solver optimization** — LUCID does not exist to maximize task accuracy as a product
- **Human-judged core scoring** — primary leaderboard metrics must not depend on subjective grading of free text
- **Hidden evaluator logic** — scoring must not rely on undocumented parsing of prose or chain-of-thought
- **Free-form text as a scoring input** — narrative may be stored for analysis but is not an official scoring boundary
- **Kaggle-platform-specific semantics inside the benchmark core** — transport and hosting may wrap the core; they must not redefine drift, phases, or scores
- **Stack reimplementation** — LUCID borrows posture from sibling systems (determinism, CI discipline) without re-building their full stacks
- **Benchmark widening into a generic reasoning omnibus** — one flagship faculty stays primary

---

## 4. Local vs remote

- The **local deterministic core** (generate → score → bundle) remains **canonical** even when Kaggle or other hosts integrate execution.
- **M01** and later platform work must prove **transport and execution compatibility**, not **redefine benchmark meaning**.

---

## 5. One-line summary

> LUCID owns a metacognition-first, typed, deterministic benchmark core; it refuses solver drift, hidden judges, free-text scoring, and platform semantics inside that core.
