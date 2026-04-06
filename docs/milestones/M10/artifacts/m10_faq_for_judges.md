# M10 — FAQ for judges (compact)

**Benchmark version:** 1.1.0

---

## Why synthetic tasks?

Synthetic rule-worlds give **exact ground truth**, **controlled drift**, and **audit-ready** episodes. LUCID prioritizes **defensible construction** and **faculty isolation** (metacognition under drift) over open-domain realism that is hard to verify at scale.

---

## Why is partial hosted coverage still meaningful?

M09 records **real** platform aggregates for a **deterministic** mature panel on the unified benchmark. **15** completing runs support claims about **spread** and **reordering** on that slice; **18** non-completions are **explicitly documented** so the story stays honest about **breadth limits**, not just peak scores.

---

## Why does confidence matter?

The project thesis is that **wrong + overconfident under drift** is a distinct failure mode from **wrong alone**. LUCID’s contract requires **confidence-bearing outputs**; calibration and related signals are part of the measurement, not optional metadata.

---

## Why is LUCID a benchmark rather than a solver?

The entry goal is a **diagnostic instrument**: reproducible tasks, scoring, and artifacts that **separate models** on metacognitive behavior. Optimizing a system to “win” tasks would invert the project identity (`docs/LUCID_MOONSHOT.md` §17).

---

## Where is the evidence?

- **M09 scores and linkage:** `docs/milestones/M09/artifacts/m09_model_scores.csv`, `m09_kaggle_run_manifest.md`
- **M10 figures/tables:** `docs/milestones/M10/artifacts/figures/`, `tables/`, `m10_figure_manifest.json`
- **Defensibility:** `docs/milestones/M08/artifacts/`, `docs/benchmark_quality/LUCID_DEFENSIBILITY_STANDARD.md`
- **Ledger:** `docs/lucid.md`
