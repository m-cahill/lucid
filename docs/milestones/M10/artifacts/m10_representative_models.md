# M10 — Representative model portfolio (narrative)

**Source data:** `docs/milestones/M09/artifacts/m09_model_scores.csv` (status = `completed` for M09 means).  
**Role:** Curated **story** for the writeup; the full table remains authoritative in M09.

Values below are **aggregate means** from the committed CSV (not per-family slices).

---

## Anchors and spread

| Role (conceptual) | Model slug | M01 mean | M09 mean | Δ (M09−M01) | Notes |
|-------------------|------------|---------:|---------:|-------------:|--------|
| **Ceiling (highest M09 in completing set)** | `gemini-2.5-pro` | 0.8929 | 0.8157 | −0.0772 | Top M09 score among **15** completions. |
| **Strong mature-benchmark performers** | `qwen3-coder-480b-a35b-instruct` | 0.8942 | 0.7433 | −0.1509 | High absolute M09 despite large negative delta vs M01 transport. |
| **Strong M09 / upward movers** | `qwen3-235b-a22b-instruct-2507` | 0.6792 | 0.7118 | +0.0326 | Positive delta on mature panel. |
| **Strong M09 / upward movers** | `gpt-5.4-2026-03-05` | 0.6612 | 0.7091 | +0.0479 | Notable improvement vs M01 mean. |
| **Positive improver / inversion** | `gemma-3-27b-it` | 0.6772 | 0.7242 | +0.0470 | Largest positive delta in this subset. |
| **Stable mid-tier (example)** | `gemini-2.0-flash-001` | 0.6804 | 0.6836 | +0.0031 | Near-flat M01→M09 move. |
| **Collapse / anomaly (large negative Δ)** | `glm-5` | 0.8929 | 0.6608 | −0.2321 | Among the strongest negative shifts. |
| **Collapse / anomaly (large negative Δ)** | `gpt-5.4-mini-2026-03-17` | 0.8934 | 0.6451 | −0.2483 | High M01 mean, sharp drop on M09 panel. |

---

## How to use this table

- **Do not** treat this as full-roster coverage: **18** models lack M09 numerics in the export.
- **Do** use it to explain **reordering** and **non-uniform** M01→M09 movement on the **mature 72-episode** slice vs the **M01 transport** task.

**Figures:** `docs/milestones/M10/artifacts/figures/m10_fig_m01_m09_paired.png`, `m10_fig_delta_m09_minus_m01.png`, `m10_fig_m09_ranked.png`.
