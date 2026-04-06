# M10 — Limitations and scope register

**Benchmark version:** 1.1.0  
**Role:** Explicit, judge-facing boundaries for what LUCID claims.

---

## 1. Hosted evidence breadth (M09)

- **Partial roster:** **15** models have numeric M09 means on `lucid_m09_mature_evidence_task`; **18** models are documented as **`failed_platform_limited`** (no M09 numeric in the ingested export).
- **Not asserted as benchmark defect:** Non-completions are framed as **platform / token / cost / breadth** limits on the larger panel, not as proof the benchmark is broken.
- **M01 historical table** in `docs/lucid.md` §6 remains **M01** evidence; it does not represent the mature-panel slice.

---

## 2. Slice granularity from exports

- **No** per-family, per-difficulty, or per-episode score series from the **aggregate** export used for M09 closeout.
- **No** component metric breakdown (D/L/O/A/C) from that export — see NA rows in `m09_component_metrics.csv` and `m09_kaggle_run_manifest.md`.

---

## 3. Notebook and run linkage

- **Exact Kaggle notebook URL / version** was **not** available in the export bundle used for closeout. Strongest linkage recorded: **notebook path** in this repo, **task name**, **benchmark slug**, **ZIP pin SHA** (`m09_kaggle_run_manifest.md`).

---

## 4. Instrument identity

- **Not a solver:** LUCID diagnoses behavior under drift; it does not optimize task-solving performance as an entry goal.
- **Not multi-faculty sprawl:** Primary faculty is **metacognition under instructional drift**; other cognitive tracks are out of scope.
- **No psychometric equivalence** across families beyond nominal LOW/MEDIUM/HIGH labels (`docs/benchmark_packs/unified_core_m07.md`).

---

## 5. Contamination and exposure

- Synthetic construction reduces trivial memorization narratives but does **not** eliminate all overlap with generic language skills; see `m08_contamination_posture.md` for realistic leakage vectors (public repo, template similarity, hosted logging).

---

## 6. M10 figure/table scope

- M10 visuals summarize **committed CSVs**; they do **not** infer new metrics. Regeneration: `scripts/generate_m10_figures.py`, `scripts/generate_m10_tables.py`.
