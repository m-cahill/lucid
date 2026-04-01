# M04 — Run 2 — Hosted-model / Kaggle evidence (platform)

**Milestone:** M04  
**Status:** **Template / fill-in** — populate after running the M04 analytics notebook on Kaggle.

## Intended workflow

1. Upload / run `notebooks/lucid_kaggle_family1_m04_analytics.ipynb` in a Kaggle Benchmarks context.  
2. Pin `%pip` install to the same **40-character commit SHA** as the notebook banner (see `docs/kaggle/LUCID_KAGGLE_NOTEBOOK_M04_FAMILY1_ANALYTICS.md`).  
3. Run the default **10-model panel** (or document substitutions) from `docs/milestones/M04/artifacts/m04_model_panel.json`.  
4. Export per-episode scores into `docs/milestones/M04/artifacts/family1_model_scores.csv` (schema in file header).  
5. Run `python scripts/summarize_family1_model_results.py docs/milestones/M04/artifacts/family1_model_scores.csv -o docs/milestones/M04/artifacts/family1_model_summary.json` (optional output path).  
6. Copy aggregate metrics into `family1_component_metrics.csv` and revise `family1_promotion_decision.md` if evidence supports **promote** or **drop**.

## Record when available

| Field | Value |
|-------|--------|
| Notebook URL / version | _TBD_ |
| Benchmark / task IDs | _TBD_ |
| Run timestamp (UTC) | _TBD_ |
| Models executed | _TBD_ |
| Blockers (if any) | _None recorded at M04 implementation commit_ |

**Honesty:** M04 repository closeout includes the **evaluation surface** and **empty** model CSV placeholders; **promote** was not claimed without populated platform scores.
