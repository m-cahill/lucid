# LUCID — competition alignment

**Project:** LUCID  
**Document type:** Alignment note (facts + scope boundaries + submission strategy)  
**Verification:** M00 = documentation only; **M01** = platform E2E proof; **M02** = competition charter & milestone arc (docs-only)  
**Last checked:** March 2026 (sources below)

---

## 1. Official competition

| Field | Value |
|-------|--------|
| **Name** | **Measuring Progress Toward AGI — Cognitive Abilities** |
| **Host / platform** | Kaggle |
| **Official competition URL** | https://www.kaggle.com/competitions/kaggle-measuring-agi |
| **Rules (authoritative for deadlines & requirements)** | https://www.kaggle.com/competitions/kaggle-measuring-agi/rules |

**Deadline and prize structure:** Kaggle’s **Rules** tab is authoritative; static mirrors and third-party articles may be wrong or stale. Open the Rules page directly before relying on any date.

---

## 2. Judged axes and win conditions

Partner and competition materials describe evaluation along multiple **cognitive** dimensions. Commonly referenced **five thematic tracks** include areas such as **learning**, **metacognition**, **attention**, **executive functions**, and **social cognition** — used to organize benchmark proposals and judging. **Exact labels and eligibility** can vary by phase; confirm on the **official competition Overview/Rules** pages.

For **benchmark construction** entries, practical judging emphasis is typically:

1. **Dataset quality & task construction** (highest leverage)
2. **Novelty / insights / discriminatory power** (does the benchmark reveal a meaningful behavioral gradient?)
3. **Writeup quality** (clarity, reproducibility, scientific framing)

**LUCID’s posture:** Each milestone should state **which axis** it primarily advances. The project does **not** try to win on breadth of unrelated cognitive tracks; it stays **one primary faculty**.

---

## 3. Why one track / one faculty

LUCID refuses **faculty sprawl** and **benchmark theater** (see `docs/LUCID_MOONSHOT.md`). A single, sharply isolated faculty produces:

- clearer task contracts and defensibility
- stronger dataset-quality narrative for judges
- measurable discriminatory signal instead of opaque multi-domain mixes

---

## 4. Why metacognition is the primary faculty

LUCID measures **metacognitive calibration under instructional drift**: whether a model **notices** when the governing rule changes, **adjusts confidence**, and **recovers** before stale confidence outruns correctness. That aligns with the competition’s **metacognition** pillar without claiming unrelated tracks.

Synthetic **rule-worlds** with explicit drift moments support **dataset defensibility**: exact ground truth, controlled stressors, and reduced contamination vs. hand-authored open-domain ambiguity.

---

## 5. Cognitive tracks (competition framing)

LUCID is intentionally scoped to **metacognitive calibration under instructional drift**, consistent with the **metacognition** pillar, without claiming coverage of unrelated tracks.

---

## 6. Kaggle Benchmarks / Community Benchmarks (platform)

| Resource | URL |
|----------|-----|
| **Kaggle Benchmarks documentation** (overview, tasks, leaderboards) | https://www.kaggle.com/docs/benchmarks |
| **Benchmarks hub** | https://www.kaggle.com/benchmarks |
| **Community Benchmarks** (same technical substrate as research benchmarks; different sourcing) | Described in official docs above |
| **Python SDK / examples** | https://github.com/Kaggle/kaggle-benchmarks |

Official docs state that **tasks** are Python-defined evaluations and **benchmarks** are collections of tasks composed in the UI; leaderboards can be downloaded (including via API). The platform emphasizes **robustness**, **reproducibility**, and **transparency**.

**Token / cost / latency:** Task notebooks and platform execution may surface model-call metrics; see current Kaggle Benchmarks documentation and task notebook patterns for what is recorded for a given run.

---

## 7. LUCID scope vs milestones

| Milestone | What is verified |
|-----------|------------------|
| **M00** | Repo, contracts, **local** deterministic smoke path, baseline CI, **documentation alignment** with official Kaggle URLs and Benchmarks docs |
| **M01** | **Kaggle Community Benchmarks end-to-end** — LUCID expressed and run through the platform without changing benchmark semantics; hosted-model score ledger |
| **M02** | **Competition charter lock** — submission strategy, M03–M13 planned arc, first three family priorities, promotion/retention rules (docs only; benchmark **1.1.0** unchanged) |
| **M03** | **Family 1 offline core pack** — 96-episode deterministic `symbolic_negation_v1` manifest (`family1_core_m03_v1`); M01 transport rows included; `--check` CI guard; benchmark **1.1.0** unchanged |
| **M04** | **Family 1 analytics** — structural difficulty ladder + deterministic baseline artifacts; **additive** Kaggle notebook on a **24-episode** stratified panel (`lucid_family1_m04_task`); Family 1 verdict **retain provisionally** pending populated hosted-model results (`docs/milestones/M04/artifacts/`); benchmark **1.1.0** unchanged |
| **M05** | **Family 2 offline core pack** — deterministic `contradiction_clarification_v1` manifest (`family2_core_m05_v1`, 72 episodes); `--check` CI guard; Family 2 verdict **retain provisionally**; no Kaggle Family 2 task in milestone scope; benchmark **1.1.0** unchanged |

**Do not** claim in writeups that Kaggle E2E is complete **before M01** closes.

---

## 8. Submission strategy (locked in M02)

- **Primary story:** Metacognition under **instructional drift** — detection, calibration, recovery — with **confidence-bearing outputs** and calibration-related signals (e.g. calibration lag) as first-class measurements.
- **Not a solver entry:** LUCID does not optimize for winning tasks as a reasoning system; it diagnoses behavior under drift.
- **M01** proved **transport** and **initial hosted-model spread**; **submission readiness** still requires family depth, defensibility, mature Kaggle evidence, and writeup packaging (see `docs/lucid.md` §6.4).
- **M03** delivered a **committed canonical Family 1 pack** (deterministic regeneration + manifest `--check`) so dataset construction is **auditable and drift-resistant** — the highest-leverage judged axis for benchmark entries. One-faculty posture and family priority order (**Family 1 first**) are unchanged.
- **M04** analytically evaluated Family 1 on that pack (structural ladder + local deterministic baseline + separate Kaggle analytics notebook). **Verdict:** **retain provisionally** — structural coherence is strong; **submission strategy** should treat hosted-model **spread evidence** on the M04 panel (or a documented fallback) as the next gate before claiming **promote** for Family 1. Populate `docs/milestones/M04/artifacts/family1_model_scores.csv` from Kaggle runs and revise the verdict when evidence warrants.
- **M05** added a **canonical Family 2 offline pack** (`family2_core_m05_v1`) for `contradiction_clarification_v1` with local proof and CI manifest verification. **Verdict:** **retain provisionally** — dataset construction advance; discriminatory hosted-model evidence for Family 2 is out of milestone scope.

---

## 9. Prioritized benchmark families (first three)

Order is locked for planning; implementation follows milestones **M03+**:

| Priority | Family theme | Rationale |
|----------|----------------|-----------|
| **1** | Symbolic negation / local rule reversal | Already proven at transport level in M01; fastest path to real dataset scale. |
| **2** | Contradiction / clarification | Exercises metacognitive honesty, abstention, and recovery. |
| **3** | Scope / precedence / exception drift | Broadens drift taxonomy while staying inside the same faculty thesis. |

---

## 10. Family promotion, retention, and drop

At each benchmark-family milestone closeout, record:

1. **Sample size**
2. **Hosted-model spread summary** (or equivalent discriminatory evidence)
3. **Verdict:** **promote** (carry forward as core), **retain provisionally** (needs more evidence), or **drop** (does not justify further investment)

This prevents unchecked expansion and keeps families tied to measurable signal.

---

## 11. Hosted-model sweep posture

- **Default:** Run **all** competition-available hosted models tracked in `docs/lucid.md` §6 on each major benchmark pass when practical — marginal cost is low and exhaustive coverage supports discriminatory claims.
- **Evidence:** Cite notebook / task / benchmark version in milestone run docs when claiming platform results.

---

## 12. Writeup asset checklist (standing)

For eventual submission packaging, plan to include:

- Problem framing and **single-faculty** claim (metacognition under drift)
- Task construction and **defensibility** (synthetic rule-worlds, drift taxonomy)
- **Reproducibility** (deterministic generation, scoring profile reference)
- Hosted-model **spread** and limitations (what the benchmark does / does not prove)
- Links to **Kaggle benchmark / task / rules** as required by the competition

---

## 13. Explicit non-goals

- **Solver drift:** Optimizing model task performance instead of diagnostic measurement.
- **Faculty sprawl:** Measuring many cognitive pillars shallowly.
- **Benchmark theater:** Clever-looking tasks without defensible construction or measurable gradient.
- **Casual semantic change:** Scoring, drift taxonomy, or profile changes without version bump and change control (`docs/contracts/LUCID_CHANGE_CONTROL.md`).

---

## 14. Supplementary context (non-Kaggle)

Google DeepMind’s public materials describe a **cognitive framework** for measuring progress toward AGI; these blog posts are useful **background** but do **not** replace Kaggle’s rules:

- https://deepmind.google/blog/measuring-progress-toward-agi-a-cognitive-framework/

---

## 15. One-line summary

> LUCID aligns with the **Measuring AGI — Cognitive Abilities** competition and **Kaggle Benchmarks** documentation as a **metacognition-first benchmark construction** entry; deadlines and rules come from Kaggle’s **Rules** tab; platform proof is **M01**; charter and planned arc through **M13** are **M02**.
