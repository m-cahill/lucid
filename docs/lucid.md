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
| Canonical Kaggle notebook (generated) | `notebooks/lucid_kaggle_transport_text_adapter_m_01.ipynb` (`scripts/generate_kaggle_notebook.py`) |
| Kaggle transport fixture manifest | `tests/fixtures/kaggle_transport/transport_manifest.json` |
| M01 Kaggle handoff runbook | `docs/milestones/M01/M01_KAGGLE_RUNBOOK.md` |
| M01 closeout (complete) | `M01_run1.md`, `M01_summary.md`, `M01_audit.md` |
| M02 (planned) | `docs/milestones/M02/M02_plan.md` |

---

## 4. Current benchmark status

| Item | Status |
|------|--------|
| Active template families | **symbolic_negation_v1** (documented in M00; see `docs/families/`) |
| Active scoring profile | **LUCID_SCORING_PROFILE v1.1.0** |
| Local minimal green path | **Complete (M00)** — `scripts/run_local_smoke.py` + tests |
| Kaggle Community Benchmarks E2E | **Complete (M01)** — repo transport + offline equivalence + **Kaggle platform proof** (hosted models, task wiring, scores); see `docs/milestones/M01/M01_run1.md` and §6 score ledger |
| Remote GitHub Actions | **Verified** — `pull_request` / `push` CI per `.github/workflows/ci.yml`; historical evidence in `docs/milestones/M00/M00_run1.md` |

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

Summary: LUCID targets the **Kaggle Measuring AGI** competition as a **benchmark construction** entry. Full facts, links, and scope (M00 docs-only vs M01 E2E) are in **`docs/LUCID_COMPETITION_ALIGNMENT.md`**.

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

| Milestone | Goal | Status |
|-----------|------|--------|
| **M00** | Bootstrap repo, semantic lock, local minimal green path, baseline CI | **Complete** |
| **M01** | Kaggle Community Benchmarks E2E verification | **Complete** |
| **M02** | Next auditable step (charter TBD) | **Planned** — see `docs/milestones/M02/M02_plan.md` |

---

## 8. Historical milestone — M01 (closed)

**Closed:** 2026-03-31 (repository record). **M01.1** (notebook contract, generator, text adapter) was **in-milestone** hardening, not a separate milestone.

**What M01 proved**

- **Repo:** Transport under `src/lucid/kaggle/`, deterministic fixtures, equivalence tests, generated canonical notebook `notebooks/lucid_kaggle_transport_text_adapter_m_01.ipynb`, standing contract `docs/kaggle/LUCID_KAGGLE_NOTEBOOK_CONTRACT.md`, CI notebook `--check`.
- **Kaggle:** Canonical notebook uploaded / used with the Community Benchmarks workflow; **single** main task `lucid_main_task`; benchmark execution on **hosted models** with **numeric scores**.
- **Signal:** Initial **discriminative spread** across the full hosted-model set (see §6); not a claim of final benchmark maturity.

**Authoritative plan (archived goal):** `docs/milestones/M01/M01_plan.md`  
**Evidence:** `docs/milestones/M01/M01_run1.md`, `M01_summary.md`, `M01_audit.md`  
**Handbook:** `docs/milestones/M01/M01_KAGGLE_RUNBOOK.md`

### Canonical notebook regeneration rule (standing)

- **Never** hand-edit the canonical `.ipynb`; regenerate via `scripts/generate_kaggle_notebook.py` after changing `src/lucid/kaggle/` or the generator; **`--check`** must pass.
- **Pin** ZIP installs to a commit whose tree includes required transport code (`docs/kaggle/LUCID_KAGGLE_NOTEBOOK_CONTRACT.md` §5.1).

**Competition alignment:** `docs/LUCID_COMPETITION_ALIGNMENT.md`.

---

## 9. Active milestone — M02 (next)

**Status:** **Planned / not opened** — stub only.

**Plan:** `docs/milestones/M02/M02_plan.md`  
**Tool log:** `docs/milestones/M02/M02_toolcalls.md`

M02 is intended to be **smaller, enterprise-grade, auditable, and E2E-testable**, building on M01 evidence **without** redefining LUCID as a solver or casually widening benchmark semantics.

---

## 10. Governance rule

- **Canonical contracts** = files under `docs/contracts/`.  
- **No manual dual maintenance** of the archived master bundle vs individual contracts.  
- Any benchmark-semantic change requires version bump and changelog per `LUCID_CHANGE_CONTROL.md`.
