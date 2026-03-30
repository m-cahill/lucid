# LUCID terminology guide (LLM-focused)

**Project:** LUCID  
**Audience:** Cursor, agents, and human authors writing about LUCID  
**Status:** Canonical writing aid (non-normative for benchmark semantics)

---

## 1. Purpose

Keep public and internal prose aligned with LUCID’s scientific identity: **metacognitive calibration under instructional drift**, not generic “AGI hype” or solver framing.

---

## 2. Preferred terms

| Term | Use |
|------|-----|
| benchmark | LUCID evaluates models; it does not “solve the world.” |
| cognitive ability | Safer than “faculty” in competition-facing copy. |
| metacognitive calibration | The flagship construct LUCID targets. |
| instructional drift | Define as an **explicit, typed rule change** in the episode spec. |
| explicit rule change | Reinforces determinism and auditability. |
| typed response | Official behavior is whatever `EpisodeResponse` fields say. |
| deterministic episode | Same tuple → same spec; no hidden randomness. |
| artifact bundle | Audit trail: spec + result + manifests + hashes. |

---

## 3. Terms needing caution

| Term | Caution |
|------|---------|
| latent | LUCID’s acronym uses “Latent” historically; do **not** imply latent-space interpretability unless that is explicitly in scope. |
| policy | Prefer “local rule” or “governing rule” unless discussing internal model behavior carefully. |
| faculty | Fine technically; prefer **cognitive ability** in outward-facing text. |
| drift | Always tie to **typed drift family** + episode metadata, not vague “prompt changed.” |
| calibration | Means **confidence vs correctness / uncertainty state**, not “sounds humble.” |
| episode | A full benchmark instance with phases and eligibility windows—not a single chat turn by default. |

---

## 4. Public-writeup translation

- Say **“cognitive ability”** more often than **“faculty”** in competition copy.
- Define **instructional drift** once as an explicit rule-change event with a drift label.
- Describe **confidence** as **part of the benchmark output**, not decorative metadata.
- Present LUCID as **metacognition-first**, not as a broad reasoning showcase.

---

## 5. Forbidden phrasing

- “LUCID solves …”
- “LUCID is an AGI system”
- “LUCID proves general intelligence”
- “LUCID measures everything important about reasoning”

---

## 6. One-line summary

> Write LUCID as a deterministic, typed, drift-aware benchmark—not as a solver, miracle, or omnibus IQ test.
