# LUCID — M04 Family 1 Kaggle analytics notebook

**Status:** Additive analytics surface (**M04**). Does **not** replace the M01 transport contract.  
**Canonical path:** `notebooks/lucid_kaggle_family1_m04_analytics.ipynb`  
**Generator:** `python scripts/generate_family1_m04_notebook.py --pin-sha <40-char-SHA>`

## Relationship to `LUCID_KAGGLE_NOTEBOOK_CONTRACT.md`

The **M01** contract governs `notebooks/lucid_kaggle_transport_text_adapter_m_01.ipynb` (three-episode acceptance slice, task `lucid_main_task`). **Do not** repurpose that notebook for M04.

This document governs the **M04** notebook:

| Rule | Detail |
|------|--------|
| **Task name** | `lucid_family1_m04_task` (distinct from `lucid_main_task`) |
| **Episode set** | `m04_decision_eval_rows()` — **24** stratified episodes (8 / 8 / 8) |
| **Prompt / parse / score** | Same stack as M01: `text_adapter` + `prompts` + inlined profile **1.1.0** scorer in-notebook |
| **No `schema=`** | Same as M01 — plain `llm.prompt` then local JSON parse |
| **Install** | Commit-pinned GitHub ZIP — SHA in banner must match `%pip` URL |
| **One task / one `%choose`** | `%choose lucid_family1_m04_task` |

## Regeneration

After changing `build_m04_notebook_cells` in `scripts/generate_kaggle_notebook.py` or transport imports used by the notebook:

```bash
python scripts/generate_family1_m04_notebook.py --pin-sha auto -o notebooks/lucid_kaggle_family1_m04_analytics.ipynb
python scripts/generate_family1_m04_notebook.py --check -o notebooks/lucid_kaggle_family1_m04_analytics.ipynb
```

## Evidence

Record notebook / benchmark / task identifiers in `docs/milestones/M04/M04_run2.md` after platform runs.
