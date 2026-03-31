# M01 — Kaggle platform run evidence (`M01_run1`)

**Milestone:** M01 — Kaggle Community Benchmarks E2E verification  
**Status:** **Complete** (repository record)  
**Benchmark:** LUCID **1.1.0** · family **symbolic_negation_v1** · scoring profile **1.1.0**

This document is the **authoritative M01 platform evidence record** alongside the hosted-model score ledger in `docs/lucid.md` §6.

---

## 1. What M01 proved (platform)

- **Canonical generated notebook** was uploaded and used with the Kaggle Community Benchmarks / Measuring AGI workflow.
- **Single main task** `lucid_main_task` was wired from notebook code (`%choose lucid_main_task` after `.run(kbench.llm)`).
- **Benchmark execution** ran on **Kaggle-hosted models**; numeric **task scores** were produced for the competition model set.
- **Transport** used the repo’s text adapter (`lucid.kaggle.text_adapter`) and centralized prompts (`lucid.kaggle.prompts`) — no schema-bound `llm.prompt(..., schema=...)` on the transport path.

LUCID remains a **benchmark construction** entry: scores measure model behavior under the fixed transport slice, not “solving” a contest puzzle.

---

## 2. Repository canonicals (frozen references)

| Artifact | Path / ref |
|----------|------------|
| Canonical notebook (generated) | `notebooks/lucid_kaggle_transport_text_adapter_m_01.ipynb` |
| Generator | `scripts/generate_kaggle_notebook.py` |
| Standing contract | `docs/kaggle/LUCID_KAGGLE_NOTEBOOK_CONTRACT.md` |
| Transport pin (example; match banner in notebook) | `45cfa43be89575fc7d94545eae838e413abd30e7` (see contract §5.1) |
| Fixture slice | Seeds **(100, LOW)**, **(42, MEDIUM)**, **(200, HIGH)** — `tests/fixtures/kaggle_transport/transport_manifest.json` |

---

## 3. Platform identifiers (Kaggle UI)

*Add or paste stable links from the Kaggle UI if you want them versioned in git; they are optional for ledger honesty if the platform UI is the system of record.*

**M02 hygiene note:** Repository search did not surface notebook/task/benchmark permalinks beyond the competition hub URLs in `docs/LUCID_COMPETITION_ALIGNMENT.md`. No backfill applied; copy from Kaggle UI when convenient (optional per M01 audit).

| Field | Value |
|--------|--------|
| Date (UTC) | 2026-03 (M01 closeout window) |
| LUCID git ref installed on Kaggle | Pinned ZIP per notebook banner / runbook (e.g. `45cfa43…` transport commit) |
| Notebook title / URL | *Populate from Kaggle if desired* |
| Notebook version id | *Populate from Kaggle if desired* |
| Task name | `lucid_main_task` (code contract) |
| Task URL / id | *Populate from Kaggle if desired* |
| Community Benchmark URL / id | *Populate from Kaggle if desired* |

---

## 4. Hosted models and scores

**Coverage:** The ledger in `docs/lucid.md` §6 lists **all competition-available hosted models** tracked for this entry.

**Run posture:** Full model sweeps are **cheap**; the default is to run **all** listed models on each benchmark pass when appropriate.

**Observed scores (M01):** See **`docs/lucid.md`** — table “Kaggle hosted models — score ledger (reference)”.

**High-level distribution (non-fabricated summary):**

- **Top cluster:** ~**0.89–0.90** (e.g. Claude Opus 4.1, Sonnet 4, Sonnet 4.5; Gemini 2.5 Pro; GLM-5; Qwen 3 Coder 480B).
- **Mid cluster:** ~**0.64–0.68** (several Sonnet/Opus/Gemini/Gemma/Qwen variants).
- **Lower cluster:** ~**0.46–0.47** (smaller / lighter models in the set).

This establishes **discriminative spread** across the hosted set for the fixed M01 transport slice; it is **not** a claim of final benchmark maturity or exhaustive episode coverage.

---

## 5. Caveats (honest scope)

- **Episode depth:** M01 used the **fixed three-row** acceptance slice for transport proof — not a large-scale benchmark release.
- **Not a solver milestone:** Success means **measurable benchmark execution on platform**, not “best possible leaderboard optimization.”
- **Future work:** Deeper families, more episodes, and harder ablations belong in **later milestones** (e.g. M02+), not retroactive M01 scope.

---

## 6. Friction / notes

_Record any UI friction, permission quirks, or manual steps here in follow-up commits if useful._

---

## 7. Artifacts

- **Score ledger:** `docs/lucid.md` §6 (canonical numbers for M01).
- **Summary / audit:** `M01_summary.md`, `M01_audit.md`.
