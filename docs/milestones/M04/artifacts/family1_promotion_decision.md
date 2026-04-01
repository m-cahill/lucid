# Family 1 — M04 promotion verdict (`symbolic_negation_v1` / `family1_core_m03_v1`)

**Benchmark:** 1.1.0 (unchanged)  
**Pack:** `family1_core_m03_v1` — 96 episodes, 32 / 32 / 32 LOW / MEDIUM / HIGH  
**M04 evaluation scope:** structural + deterministic baseline (committed); hosted-model **decision panel** × **24-episode stratified subset** (notebook `notebooks/lucid_kaggle_family1_m04_analytics.ipynb`).

---

## Pre-registered criteria (from `M04_plan.md`)

1. **Pack quality** — determinism, metadata, balance, no duplicates/malformed episodes.  
2. **Difficulty ladder coherence** — LOW / MEDIUM / HIGH distinct in design; model ladder not obviously flat once real LLM runs exist.  
3. **Discriminatory power** — meaningful spread on Family 1; not all-perfect / all-zero; components show interpretable differences.  
4. **Competition usefulness** — supports metacognition-under-drift story; judge-defensible; no obvious shortcut invalidating signal.

---

## Evidence summary

### Structural ladder (manifest / generator)

- **LOW:** `n_items=4`, `n_colors=3`, `n_shapes=2` (uniform within bucket).  
- **MEDIUM:** `n_items=8`, `n_colors=4`, `n_shapes=2`.  
- **HIGH:** `n_items=12`, `n_colors=4`, `n_shapes=3`.  
- **Duplicates:** none (`duplicate_episode_ids` empty in `family1_bucket_stats.json`).  
- **Conclusion:** buckets are **meaningfully distinct in design** (item count + attribute grid); ladder is **coherent and defensible** structurally.

### Deterministic baseline (fixture policy)

- Full-pack pass with `fixture_turns` + official scorer yields **flat 1.0** per-bucket means — expected for a fixed “good student” policy; **not** used as discriminatory evidence. It validates **pipeline coherence** only.

### Hosted-model spread (M04 primary)

- **Verdict depends on** filling `docs/milestones/M04/artifacts/family1_model_scores.csv` from Kaggle runs using the M04 notebook and the **default panel** in `m04_model_panel.json` (or documented variant).  
- **M01 ledger scores** (`docs/lucid.md` §6) are **continuity / sanity only** — three-episode transport slice, not sufficient for Family 1 promotion.

---

## Verdict: **retain provisionally**

**Rationale**

- **Pack quality** and **structural ladder coherence** meet the **promote** bar.  
- **Discriminatory power** on the **M03 pack** is **not yet established in committed machine-readable hosted-model results** at M04 implementation time — the repository includes the evaluation surface and CSV schema; platform runs must populate scores for a final **promote** vs **retain** vs **drop** decision.  
- Until `family1_model_scores.csv` contains the M04 panel × subset grid with stable task/benchmark identifiers recorded in `M04_run2.md`, the honest milestone verdict is **retain provisionally**.

### If / when promote criteria become satisfied

Record in this memo and `docs/lucid.md`: update verdict to **promote** only after **new** M04 (or M04.1) hosted-model evidence shows meaningful spread and non-degenerate ladder behavior per criteria above.

### If discriminatory power fails after panel runs

Re-evaluate toward **drop** or **retain** with a narrowed claim — document in a follow-on milestone; do not change scoring semantics without version bump.

---

## Pointers

| Artifact | Role |
|----------|------|
| `docs/milestones/M04/artifacts/family1_bucket_stats.json` | Structural + deterministic summary |
| `docs/milestones/M04/artifacts/family1_deterministic_baseline.csv` | Full 96-episode fixture baseline |
| `docs/milestones/M04/artifacts/family1_model_scores.csv` | Per-episode hosted-model results (fill from Kaggle) |
| `docs/milestones/M04/artifacts/m04_model_panel.json` | Default model panel |
| `notebooks/lucid_kaggle_family1_m04_analytics.ipynb` | M04 Kaggle analytics surface (not M01) |
