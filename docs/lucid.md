# LUCID — execution ledger

**Project:** LUCID (*Latent Update & Calibration under Instructional Drift*)  
**Role:** Living ledger, authority map, and integration surface for the repository  
**Active benchmark version:** **1.1.0** (scoring semantics locked in M00; see semantic changelog below)  
**Frozen historical export:** contract bundle **v1.0.1** archived under `docs/archive/` (not editable canon)

**Repository:** https://github.com/m-cahill/lucid  
**Competition:** [Kaggle — Measuring Progress Toward AGI](https://www.kaggle.com/competitions/kaggle-measuring-agi)

---

## 1. Project identity (one sentence)

LUCID is a **metacognition-first diagnostic benchmark** that measures whether models **detect instructional drift, calibrate confidence, and recover** before stale confidence outruns correctness — not a solver and not a generic reasoning contest.

---

## 2. Authority hierarchy

When documents or code disagree, use this order:

1. **`docs/LUCID_MOONSHOT.md`** — ambition, faculty, philosophy, refusals  
2. **Layer A & B contracts** in **`docs/contracts/`** — identity and execution semantics  
3. **`docs/LUCID_OPERATING_MANUAL.md`** — how the pipeline maps to components  
4. **Adjacent docs** — `LUCID_BOUNDARIES.md`, `LUCID_ASSUMED_GUARANTEES.md`, `LUCID_STACK_INTERACTION.md`, `LUCID_TERMINOLOGY_GUIDE_LLM.md`, `LUCID_COMPETITION_ALIGNMENT.md`  
5. **`docs/lucid.md` (this file)** — milestone status, active profile, canonical paths  
6. **Implementation** under `src/lucid/` — must satisfy the above; defects are tracked against contracts  

**Not canonical:** the archived master bundle in `docs/archive/` (historical export only).

---

## 3. Canonical doc map

| What | Where |
|------|--------|
| Contract index | `docs/contracts/LUCID_CONTRACT_INDEX.md` |
| Individual contracts (editable source) | `docs/contracts/*.md` |
| Active scoring profile (v1.1.0) | `docs/contracts/LUCID_SCORING_PROFILE_v1.1.0.md` |
| Template family specs | `docs/families/` |
| Moonshot anchor | `docs/LUCID_MOONSHOT.md` |
| Operating manual | `docs/LUCID_OPERATING_MANUAL.md` |
| Archived bundle export (v1.0.1) | `docs/archive/LUCID_contracts_master_bundle_v1.0.1_ARCHIVED.md` |
| Milestone plans | `docs/milestones/MNN/` |
| Kaggle notebook contract (standing) | `docs/kaggle/LUCID_KAGGLE_NOTEBOOK_CONTRACT.md` |
| Canonical Kaggle notebook — M01 transport (generated) | `notebooks/lucid_kaggle_transport_text_adapter_m_01.ipynb` (`scripts/generate_kaggle_notebook.py`) |
| Kaggle notebook — M04 Family 1 analytics (generated) | `notebooks/lucid_kaggle_family1_m04_analytics.ipynb` (`scripts/generate_family1_m04_notebook.py`) |
| M04 Kaggle analytics note | `docs/kaggle/LUCID_KAGGLE_NOTEBOOK_M04_FAMILY1_ANALYTICS.md` |
| Kaggle transport fixture manifest | `tests/fixtures/kaggle_transport/transport_manifest.json` |
| Canonical Family 1 pack (M03) | `tests/fixtures/family1_core_m03/family1_core_m03_manifest.json` (`scripts/generate_family1_core_m03_manifest.py --check`) |
| Canonical Family 2 pack (M05) | `tests/fixtures/family2_core_m05/family2_core_m05_manifest.json` (`scripts/generate_family2_core_m05_manifest.py --check`) |
| Canonical Family 3 pack (M06) | `tests/fixtures/family3_core_m06/family3_core_m06_manifest.json` (`scripts/generate_family3_core_m06_manifest.py --check`) |
| M01 Kaggle handoff runbook | `docs/milestones/M01/M01_KAGGLE_RUNBOOK.md` |
| Competition alignment (submission strategy, judging, family priorities) | `docs/LUCID_COMPETITION_ALIGNMENT.md` |
| M01 closeout (complete) | `docs/milestones/M01/M01_run1.md`, `docs/milestones/M01/M01_summary.md`, `docs/milestones/M01/M01_audit.md` |
| M02 plan & closeout (complete) | `docs/milestones/M02/M02_plan.md`, `docs/milestones/M02/M02_summary.md`, `docs/milestones/M02/M02_audit.md` |
| M02 evidence / CI run record | `docs/milestones/M02/M02_run1.md` |
| M03 plan & closeout (complete) | `docs/milestones/M03/M03_plan.md`, `docs/milestones/M03/M03_summary.md`, `docs/milestones/M03/M03_audit.md`, `docs/milestones/M03/M03_run1.md` |
| M03 tool log | `docs/milestones/M03/M03_toolcalls.md` |
| M04 plan & closeout (complete) | `docs/milestones/M04/M04_plan.md`, `docs/milestones/M04/M04_summary.md`, `docs/milestones/M04/M04_audit.md`, `docs/milestones/M04/M04_run1.md`, `docs/milestones/M04/M04_run2.md` |
| M04 tool log | `docs/milestones/M04/M04_toolcalls.md` |
| M04 Family 1 evidence artifacts | `docs/milestones/M04/artifacts/` |
| M05 plan & closeout (complete) | `docs/milestones/M05/M05_plan.md`, `docs/milestones/M05/M05_summary.md`, `docs/milestones/M05/M05_audit.md`, `docs/milestones/M05/M05_run1.md` |
| M05 tool log | `docs/milestones/M05/M05_toolcalls.md` |
| M05 Family 2 structural artifact | `docs/milestones/M05/artifacts/family2_pack_stats.json` |
| M06 plan & implementation | `docs/milestones/M06/M06_plan.md` |
| M06 tool log | `docs/milestones/M06/M06_toolcalls.md` |
| M06 Family 3 structural artifact | `docs/milestones/M06/artifacts/family3_pack_stats.json` |
| M07 plan (stub; next milestone) | `docs/milestones/M07/M07_plan.md` |
| M07 tool log | `docs/milestones/M07/M07_toolcalls.md` |
| M07 CI run log (stub) | `docs/milestones/M07/M07_run1.md` |

---

## 4. Current benchmark status

| Item | Status |
|------|--------|
| Active template families | **symbolic_negation_v1**, **contradiction_clarification_v1**, **scope_precedence_exception_v1** (see `docs/families/`) |
| Active scoring profile | **LUCID_SCORING_PROFILE v1.1.0** |
| Local minimal green path | **Complete (M00)** — `scripts/run_local_smoke.py` + tests |
| Family 1 offline core pack | **Complete (M03)** — pack `family1_core_m03_v1` (96 episodes, LOW/MEDIUM/HIGH balanced); committed manifest under `tests/fixtures/family1_core_m03/`; `scripts/generate_family1_core_m03_manifest.py`; Family 1 smoke `scripts/run_family1_pack_smoke.py` |
| Family 2 offline core pack | **Complete (M05)** — pack `family2_core_m05_v1` (72 episodes, LOW/MEDIUM/HIGH balanced; 12 unresolved + 12 resolved per bucket); committed manifest under `tests/fixtures/family2_core_m05/`; `scripts/generate_family2_core_m05_manifest.py`; Family 2 smoke `scripts/run_family2_pack_smoke.py` |
| Family 3 offline core pack | **Complete (M06)** — pack `family3_core_m06_v1` (72 episodes, LOW/MEDIUM/HIGH balanced; 8 scope + 8 precedence + 8 exception per bucket; drift types `SCOPE` / `PRECEDENCE` / `EXCEPTION`); committed manifest under `tests/fixtures/family3_core_m06/`; `scripts/generate_family3_core_m06_manifest.py`; Family 3 smoke `scripts/run_family3_pack_smoke.py` |
| Family 1 M04 analytics (local + Kaggle surface) | **Complete (M04)** — difficulty ladder / deterministic baseline artifacts; **additive** Kaggle notebook `lucid_family1_m04_task` on a **24-episode** stratified panel; verdict **retain provisionally** pending populated hosted-model CSV (`docs/milestones/M04/artifacts/`) |
| Kaggle Community Benchmarks E2E | **Complete (M01)** — repo transport + offline equivalence + **Kaggle platform proof** (hosted models, task wiring, scores); see `docs/milestones/M01/M01_run1.md` and §6 score ledger |
| Remote GitHub Actions | **Verified** — `pull_request` / `push` CI per `.github/workflows/ci.yml`; historical evidence in `docs/milestones/M00/M00_run1.md` |

### Family pack inventory (standing)

For each implemented family, record the canonical offline pack (audit trail for scale and difficulty design).

| Family | Pack ID | Episodes | LOW / MED / HIGH | Drift subtypes covered (`drift_type`) | Canonical path | Last milestone |
|--------|---------|----------|------------------|----------------------------------------|------------------|----------------|
| `symbolic_negation_v1` | `family1_core_m03_v1` | 96 | 32 / 32 / 32 | `NEGATION` | `tests/fixtures/family1_core_m03/family1_core_m03_manifest.json` | M04 |
| `contradiction_clarification_v1` | `family2_core_m05_v1` | 72 | 24 / 24 / 24 | `CONTRADICTION` | `tests/fixtures/family2_core_m05/family2_core_m05_manifest.json` | M05 |
| `scope_precedence_exception_v1` | `family3_core_m06_v1` | 72 | 24 / 24 / 24 | `SCOPE`, `PRECEDENCE`, `EXCEPTION` (24 each) | `tests/fixtures/family3_core_m06/family3_core_m06_manifest.json` | M06 |

### Family verdict ledger (standing)

| Family | Pack ID | Last analytics milestone | Verdict | Rationale pointer |
|--------|---------|---------------------------|---------|-------------------|
| `symbolic_negation_v1` | `family1_core_m03_v1` | **M04** | **retain provisionally** | `docs/milestones/M04/artifacts/family1_promotion_decision.md` |
| `contradiction_clarification_v1` | `family2_core_m05_v1` | **M05** | **retain provisionally** | `docs/milestones/M05/M05_summary.md` |
| `scope_precedence_exception_v1` | `family3_core_m06_v1` | **M06** | **retain provisionally** | `docs/milestones/M06/M06_summary.md` |

### Proof classes (audit-clean ledger)

Use these labels consistently in milestone docs and run analyses:

| Proof class | What it demonstrates | Typical evidence |
|-------------|------------------------|------------------|
| **Local proof** | Deterministic generate → score → bundle on a developer machine | `pytest`, `scripts/run_local_smoke.py`, transport fixture tests |
| **GitHub CI proof** | Lint/type/test gates on `ubuntu-latest` in CI | Green workflow run logs / run IDs |
| **Kaggle platform proof** | Real execution in Kaggle’s benchmark/task environment | Notebook version, task/benchmark links, model run outputs (see `M01_KAGGLE_EVIDENCE_TEMPLATE.md`) |

**Rule:** **Kaggle Community Benchmarks E2E** requires **Kaggle platform proof** (not CI alone). **M01** delivered that proof; **future milestones** must record their own external evidence when they claim platform work.

### Local execution posture

**GPU:** NVIDIA **RTX 5090** (**Blackwell**) — used for **local training** workloads when GPU-backed training is part of the workflow.

---

## 5. Semantic changelog

| Version | Notes |
|---------|--------|
| **1.0.1** | Frozen split contracts + historical master bundle archive; pre–scoring-profile lock |
| **1.1.0** | **M00:** Defines `target_confidence_t`, calibrated-response criterion, and abstention utility table in `LUCID_SCORING_PROFILE_v1.1.0.md`; updates `LUCID_SCORING_CONTRACT.md` to reference the profile; official scorer behavior is fully specified |

---

## 6. Competition alignment

Summary: LUCID targets the **Kaggle Measuring AGI** competition as a **benchmark construction** entry. Full facts, links, scope (M00 docs-only vs M01 E2E), submission strategy, and family priorities are in **`docs/LUCID_COMPETITION_ALIGNMENT.md`**.

### 6.1 Competition win conditions (standing)

| Judged axis (priority) | Role for LUCID |
|------------------------|----------------|
| **Dataset quality & task construction** | Highest-value axis; synthetic rule-worlds, explicit drift, audit-ready episodes. |
| **Novelty / insights / discriminatory power** | Second; hosted-model sweeps and family-level spread must show a meaningful gradient. |
| **Writeup quality** | Third; judge-facing narrative and evidence packaging. |

**Primary faculty (one):** LUCID optimizes for **metacognition** (detection, calibration, recovery under instructional drift) — not solver performance or multi-faculty sprawl.

**Standing rule:** Each future milestone should state **which judged axis** it primarily advances.

**M04 judged axis:** **Novelty / insights / discriminatory power** — difficulty-ladder + spread-analysis tooling and an additive Kaggle analytics notebook; dataset-quality positioning inherited from M03.

**M05 judged axis:** **Dataset quality & task construction** — canonical deterministic Family 2 offline pack (`contradiction_clarification_v1` / `family2_core_m05_v1`), tests, CI manifest check, and family spec; no hosted-model Family 2 evidence in milestone scope.

**M06 judged axis:** **Dataset quality & task construction** — canonical deterministic Family 3 offline pack (`scope_precedence_exception_v1` / `family3_core_m06_v1`), tests, CI manifest check, and family spec; no Kaggle Family 3 task or hosted-model evidence in milestone scope.

### 6.2 Submission posture

- **M01** established **transport proof** and an initial **hosted-model spread** on a fixed acceptance slice (`symbolic_negation_v1`).
- **M03** added a **canonical deterministic Family 1 offline pack** (96 episodes) including the M01 acceptance rows as an explicit subset — dataset construction advance; not a substitute for full **Kaggle evidence** on scaled runs.
- **M04** added **Family 1 analytics** (structural ladder + deterministic baseline + **M04** Kaggle analytics notebook on a **24-episode** stratified panel) and recorded verdict **retain provisionally** until hosted-model results populate `docs/milestones/M04/artifacts/family1_model_scores.csv`.
- **M05** added a **canonical deterministic Family 2 offline pack** (72 episodes, `contradiction_clarification_v1`) with local smoke and CI `--check`; Family 2 verdict **retain provisionally** pending future discriminatory evidence (no Kaggle Family 2 task in M05).
- **M06** added a **canonical deterministic Family 3 offline pack** (72 episodes, `scope_precedence_exception_v1`; drift types `SCOPE` / `PRECEDENCE` / `EXCEPTION`) with local smoke and CI `--check`; Family 3 verdict **retain provisionally** pending future discriminatory evidence (no Kaggle Family 3 task in M06).
- LUCID is **not submission-ready** after M06.
- **Remaining gaps** before a competition-ready submission include: **populated** hosted-model spread on the M04 panel (or documented fallback), **defensibility** hardening, broader **Kaggle evidence** on the mature pack as needed, and **writeup / packaging** aligned to the rules.

### 6.3 Standing family promotion rules (at milestone close)

Each future benchmark-family milestone must record:

1. **Sample size** (episodes / scale).
2. **Hosted-model spread summary** (or equivalent discriminatory evidence).
3. **Family verdict:** **promote**, **retain provisionally**, or **drop**.

This guards against faculty sprawl and “benchmark theater.”

### 6.4 Submission blockers (standing)

Until addressed, the entry should not be treated as submission-complete:

- **Family-level discriminatory power (full evidentiary closure)** — M04 delivered infrastructure + **retain provisionally**; **populate** `family1_model_scores.csv` from Kaggle (see `M04_run2.md`) or record an explicit blocked panel / subset rationale before claiming submission-grade spread.
- **Defensibility / ambiguity audit** (contamination resistance, task clarity).
- **Final writeup pack** (figures, narrative, judge-facing framing).
- **Final Kaggle benchmark / task / writeup linkage** per competition requirements.

### Kaggle hosted models — score ledger (reference)

**Coverage:** The table below is the **full set of competition-available hosted models** we track for this entry.

**Run posture:** We intend to run **all** of these models on **each** benchmark pass — the marginal cost is low, so exhaustive coverage is the default.

| Score | Model |
|------:|--------|
| 0.90 | Claude Opus 4.1 |
| 0.90 | Claude Sonnet 4 |
| 0.89 | Claude Sonnet 4.5 |
| 0.89 | Gemini 2.5 Pro |
| 0.89 | GLM-5 |
| 0.89 | Qwen 3 Coder 480B |
| 0.83 | Claude Haiku 4.5 |
| 0.68 | Claude Sonnet 4.6 |
| 0.68 | Gemini 2.0 Flash |
| 0.68 | Gemma 3 27B |
| 0.68 | Qwen 3 235B A22B Instruct |
| 0.67 | Claude Opus 4.5 |
| 0.67 | Gemini 2.0 Flash Lite |
| 0.67 | Gemma 3 12B |
| 0.67 | Qwen 3 Next 80B Instruct |
| 0.66 | Claude Opus 4.6 |
| 0.66 | DeepSeek-R1 |
| 0.66 | Gemini 3.1 Flash-Lite Preview |
| 0.66 | Gemini 3.1 Pro Preview |
| 0.65 | DeepSeek V3.2 |
| 0.65 | Gemini 2.5 Flash |
| 0.65 | Qwen 3 Next 80B Thinking |
| 0.64 | Gemini 3 Flash Preview |
| 0.47 | Deepseek V3.1 |
| 0.47 | Gemma 3 4B |
| 0.46 | Gemma 3 1B |

_Update this table when new platform runs produce different aggregates; cite notebook / task version in milestone evidence._

**M01 closeout:** This ledger was populated during **M01** with hosted-model scores and the “run all models” posture; it is **M01 evidence** — preserve when editing surrounding text.

---

## 7. Milestone ledger

Planned milestone arc (competition charter locked in **M02**):

| Milestone | Goal | Status |
|-----------|------|--------|
| **M00** | Bootstrap repo, semantic lock, local minimal green path, baseline CI | **Complete** |
| **M01** | Kaggle Community Benchmarks E2E verification | **Complete** |
| **M02** | Competition charter lock & milestone arc formalization | **Complete** |
| **M03** | Family 1 scale-up — symbolic negation / local rule-reversal dataset expansion | **Complete** |
| **M04** | Family 1 analytics — difficulty ladder, spread analysis, and promotion decision | **Complete** |
| **M05** | Family 2 — contradiction / clarification benchmark family | **Complete** |
| **M06** | Family 3 — scope / precedence / exception drift family | **Complete** |
| **M07** | Unified benchmark pack normalization across families | **Planned** |
| **M08** | Defensibility, QA, and contamination-resistance hardening | **Planned** |
| **M09** | Expanded Kaggle evidence run on mature benchmark | **Planned** |
| **M10** | Writeup evidence pack, figures, and judge-facing narrative | **Planned** |
| **M11** | Submission lock: final benchmark freeze and submission checklist | **Planned** |
| **M12** | Contingency A — platform / benchmark replacement buffer | **Planned** |
| **M13** | Contingency B — final polish / writeup / evidence cleanup buffer | **Planned** |

**Benchmark family priorities (first three, locked in M02):**

1. **Family 1 — symbolic negation / local rule reversal:** transport already proven in M01; fastest path to dataset scale.  
2. **Family 2 — contradiction / clarification:** metacognitive honesty, abstention, recovery.  
3. **Family 3 — scope / precedence / exception drift:** broadens drift taxonomy within the same faculty thesis.

---

## 8. Historical milestones (closed)

### M01 — Kaggle Community Benchmarks E2E verification

**Closed:** 2026-03-31 (repository record). **M01.1** (notebook contract, generator, text adapter) was **in-milestone** hardening, not a separate milestone.

**What M01 proved**

- **Repo:** Transport under `src/lucid/kaggle/`, deterministic fixtures, equivalence tests, generated canonical notebook `notebooks/lucid_kaggle_transport_text_adapter_m_01.ipynb`, standing contract `docs/kaggle/LUCID_KAGGLE_NOTEBOOK_CONTRACT.md`, CI notebook `--check`.
- **Kaggle:** Canonical notebook uploaded / used with the Community Benchmarks workflow; **single** main task `lucid_main_task`; benchmark execution on **hosted models** with **numeric scores**.
- **Signal:** Initial **discriminative spread** across the full hosted-model set (see §6); not a claim of final benchmark maturity.

**Authoritative plan (archived goal):** `docs/milestones/M01/M01_plan.md`  
**Evidence:** `docs/milestones/M01/M01_run1.md`, `docs/milestones/M01/M01_summary.md`, `docs/milestones/M01/M01_audit.md`  
**Handbook:** `docs/milestones/M01/M01_KAGGLE_RUNBOOK.md`

### M02 — Competition charter lock & milestone arc formalization

**Closed:** 2026-03-31 (repository record).

**What M02 delivered**

- **Charter:** Submission strategy locked around **metacognition under instructional drift**; judged axes and standing promotion rules recorded in this ledger and in `docs/LUCID_COMPETITION_ALIGNMENT.md`.
- **Arc:** Planned milestones **M03–M13** recorded in §7; first three benchmark-family priorities fixed at planning level (no new family implementation in M02).
- **Scope:** Documentation and governance only — **no** benchmark semantic change, **no** transport change, **no** Kaggle rerun, benchmark version remains **1.1.0**.

**Plan / evidence:** `docs/milestones/M02/M02_plan.md`, `docs/milestones/M02/M02_summary.md`, `docs/milestones/M02/M02_audit.md`, `docs/milestones/M02/M02_run1.md`  
**Tool log:** `docs/milestones/M02/M02_toolcalls.md`

### M03 — Family 1 scale-up (symbolic negation / local rule-reversal dataset expansion)

**Closed:** 2026-03-31 (repository record).

**What M03 delivered**

- **Canonical pack:** `family1_core_m03_v1` — **96** episodes, **32 / 32 / 32** LOW/MEDIUM/HIGH; committed manifest `tests/fixtures/family1_core_m03/family1_core_m03_manifest.json`; deterministic regeneration via `scripts/generate_family1_core_m03_manifest.py` (`--write` / `--check`); implementation `src/lucid/packs/family1_core_m03.py`.
- **M01 continuity:** The three **Kaggle transport** acceptance episodes (`tests/fixtures/kaggle_transport/transport_manifest.json`) are **included** in the pack and tagged with `m01_transport_fixture_id` in the manifest.
- **Local proof:** Tests + `scripts/run_family1_pack_smoke.py` (one episode per difficulty bucket); full-pack coverage via manifest and tests (not smoke).
- **Benchmark:** Version remains **1.1.0**; no scoring semantic change.

**Promotion / drop analytics:** Explicitly **deferred to M04** (standing family verdict rules).

**Plan / evidence:** `docs/milestones/M03/M03_plan.md`, `docs/milestones/M03/M03_summary.md`, `docs/milestones/M03/M03_audit.md`, `docs/milestones/M03/M03_run1.md`  
**Tool log:** `docs/milestones/M03/M03_toolcalls.md`

### M04 — Family 1 analytics — difficulty ladder, spread analysis, and promotion decision

**Closed:** 2026-03-31 (repository record).

**What M04 delivered**

- **Analytics scripts:** `scripts/analyze_family1_core_m03.py` (structural ladder + full-pack deterministic baseline), `scripts/summarize_family1_model_results.py`.  
- **M04 Kaggle surface:** generated notebook `notebooks/lucid_kaggle_family1_m04_analytics.ipynb` — task **`lucid_family1_m04_task`**, **24-episode** stratified panel via `m04_decision_eval_rows()`; generator `scripts/generate_family1_m04_notebook.py` + `build_m04_notebook_cells` in `scripts/generate_kaggle_notebook.py`.  
- **Artifacts:** `docs/milestones/M04/artifacts/` — `family1_bucket_stats.json`, `family1_deterministic_baseline.csv`, `family1_model_scores.csv` (fill from Kaggle), `family1_component_metrics.csv`, `family1_promotion_decision.md`, `m04_model_panel.json`.  
- **Verdict:** **retain provisionally** — structural ladder coherent; hosted-model CSV placeholders pending platform runs (`M04_run2.md`).  
- **Benchmark:** **1.1.0** unchanged.

**Plan / evidence:** `docs/milestones/M04/M04_plan.md`, `docs/milestones/M04/M04_summary.md`, `docs/milestones/M04/M04_audit.md`, `docs/milestones/M04/M04_run1.md`, `docs/milestones/M04/M04_run2.md`  
**Tool log:** `docs/milestones/M04/M04_toolcalls.md`

### M05 — Family 2 — contradiction / clarification core pack

**Closed:** 2026-04-01 (repository record).

**What M05 delivered**

- **Canonical pack:** `family2_core_m05_v1` — **72** episodes, **24 / 24 / 24** LOW/MEDIUM/HIGH, **12** unresolved + **12** resolved contradiction episodes per bucket; committed manifest `tests/fixtures/family2_core_m05/family2_core_m05_manifest.json`; deterministic regeneration via `scripts/generate_family2_core_m05_manifest.py` (`--write` / `--check`); generator `src/lucid/families/contradiction_clarification_v1.py`, pack `src/lucid/packs/family2_core_m05.py`, local runner `src/lucid/runner_family2.py`.
- **Local proof:** Tests + `scripts/run_family2_pack_smoke.py` (six representative episodes: unresolved + resolved per difficulty bucket).
- **Verdict:** **retain provisionally** — offline core-pack milestone; no Family 2 hosted-model spread in scope.
- **Benchmark:** **1.1.0** unchanged.

**Plan / evidence:** `docs/milestones/M05/M05_plan.md`, `docs/milestones/M05/M05_summary.md`, `docs/milestones/M05/M05_audit.md`, `docs/milestones/M05/M05_run1.md`  
**Tool log:** `docs/milestones/M05/M05_toolcalls.md`

### M06 — Family 3 — scope / precedence / exception core pack

**Closed:** 2026-03-31 (repository record).

**What M06 delivered**

- **Canonical pack:** `family3_core_m06_v1` — **72** episodes, **24 / 24 / 24** LOW/MEDIUM/HIGH, **8** scope + **8** precedence + **8** exception per bucket (`DriftType` **SCOPE / PRECEDENCE / EXCEPTION**); committed manifest `tests/fixtures/family3_core_m06/family3_core_m06_manifest.json`; deterministic regeneration via `scripts/generate_family3_core_m06_manifest.py` (`--write` / `--check`); generator `src/lucid/families/scope_precedence_exception_v1.py`, pack `src/lucid/packs/family3_core_m06.py`, local runner `src/lucid/runner_family3.py`.
- **Local proof:** Tests + `scripts/run_family3_pack_smoke.py` (nine representative episodes: one per subtype per difficulty bucket).
- **Verdict:** **retain provisionally** — offline core-pack milestone; no Family 3 hosted-model spread in scope.
- **Benchmark:** **1.1.0** unchanged.

**Plan / evidence:** `docs/milestones/M06/M06_plan.md`, `docs/milestones/M06/M06_summary.md`, `docs/milestones/M06/M06_audit.md`, `docs/milestones/M06/M06_run1.md`  
**Tool log:** `docs/milestones/M06/M06_toolcalls.md`

### Canonical notebook regeneration rule (standing)

- **Never** hand-edit canonical `.ipynb` JSON; regenerate via generators; **`--check`** must pass in CI.  
  - **M01 transport:** `scripts/generate_kaggle_notebook.py` → `notebooks/lucid_kaggle_transport_text_adapter_m_01.ipynb` (`docs/kaggle/LUCID_KAGGLE_NOTEBOOK_CONTRACT.md`).  
  - **M04 Family 1 analytics:** `scripts/generate_family1_m04_notebook.py` → `notebooks/lucid_kaggle_family1_m04_analytics.ipynb` (`docs/kaggle/LUCID_KAGGLE_NOTEBOOK_M04_FAMILY1_ANALYTICS.md`).  
- **Pin** ZIP installs to a commit whose tree includes required transport code (`docs/kaggle/LUCID_KAGGLE_NOTEBOOK_CONTRACT.md` §5.1 for M01; same discipline for M04).

**Competition alignment:** `docs/LUCID_COMPETITION_ALIGNMENT.md`.

---

## 9. Active milestone — M07 (next)

**Status:** **Planned** — stub at M06 handoff (see §7).

**Goal (from planned arc):** Unified benchmark pack normalization across families.

**Plan (stub):** `docs/milestones/M07/M07_plan.md`  
**Tool log:** `docs/milestones/M07/M07_toolcalls.md`  
**CI run log (stub):** `docs/milestones/M07/M07_run1.md`

---

## 10. Governance rule

- **Canonical contracts** = files under `docs/contracts/`.  
- **No manual dual maintenance** of the archived master bundle vs individual contracts.  
- Any benchmark-semantic change requires version bump and changelog per `LUCID_CHANGE_CONTROL.md`.
