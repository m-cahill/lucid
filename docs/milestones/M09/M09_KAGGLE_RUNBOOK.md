# M09 — Kaggle platform run (Phase C handoff)

**Milestone:** M09  
**Purpose:** Record **Kaggle platform proof** for the mature 72-episode evidence panel after Phase B (repo generators + CI) is merged.

Phase B ships:

- Panel logic: `src/lucid/kaggle/m09_evidence_panel.py`
- Committed panel JSON: `docs/milestones/M09/artifacts/m09_model_panel.json`
- Generated notebook: `notebooks/lucid_kaggle_m09_mature_evidence.ipynb`
- **Task name (in notebook):** `lucid_m09_mature_evidence_task`

## Before you run on Kaggle

1. Use a **commit-pinned** repo state. The notebook installs  
   `https://github.com/m-cahill/lucid/archive/<SHA>.zip` — the banner cell’s **40-character SHA** must match the commit you intend to evaluate.
2. Regenerate the notebook **from that commit** so the pin is consistent:

   ```bash
   python scripts/generate_m09_kaggle_notebook.py --pin-sha <40-char-sha> -o notebooks/lucid_kaggle_m09_mature_evidence.ipynb
   ```

3. Upload `notebooks/lucid_kaggle_m09_mature_evidence.ipynb` to Kaggle and create or attach the Community Benchmark **task** named `lucid_m09_mature_evidence_task` per Kaggle Benchmarks workflow (same pattern as M01/M04).

## What to record (for Phase D / closeout)

- Exact **notebook** revision (commit SHA in banner).
- **Benchmark / task** URLs on Kaggle.
- **Run date** (UTC).
- **Hosted-model roster** actually used (include skips/failures with reason — do not silently omit).
- Mean score and per-episode breakdown as exported from the platform or notebook output.

## After the run

Commit machine-readable results under `docs/milestones/M09/artifacts/` (CSV + manifest markdown) and add `m09_m04_blocker_disposition.md` per M09 acceptance criteria. **Do not** replace the M01 score ledger in `docs/lucid.md` §6; M09 evidence is **additive**.
