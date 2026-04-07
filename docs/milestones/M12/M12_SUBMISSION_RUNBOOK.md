# M12 — Submission runbook (zero-improvisation)

**Milestone:** M12 — final benchmark / task / writeup linkage  
**Benchmark version:** 1.1.0 (unchanged)

This runbook is the operator-facing sequence for **publication alignment** and **auditability**. It does **not** reopen M11 probe execution unless separately authorized.

---

## 1. Preconditions

1. Read `docs/lucid.md` (active milestone + doc map).
2. Confirm M11 closeout docs are intact: `M11_summary.md`, `M11_audit.md`, `M11_run1.md`, `M11_run2.md`.
3. Working tree clean except intentional M12 changes.

---

## 2. Repository verification (local)

```text
python -m ruff check src tests scripts
python -m ruff format --check src tests scripts
python -m mypy src
python -m pytest
```

Run all generator `--check` steps that CI runs (see `.github/workflows/ci.yml`), including:

```text
python scripts/generate_m12_submission_linkage.py --check
```

---

## 3. Kaggle benchmark (owner account)

1. Open the Community Benchmarks workflow for **Measuring Progress Toward AGI**.
2. Locate benchmark **`michael1232/lucid-kaggle-community-benchmarks`** (slug in `m12_linkage_sources.json`).
3. Confirm which **tasks** are attached (expect six LUCID tasks listed in the linkage manifest).
4. Record **publication status**:
   - If the benchmark is visible to logged-out users / incognito, you may set `publication_status` to `public_verified` in `m12_linkage_sources.json` and fill `kaggle_benchmark_url`.
   - Otherwise keep `owner_visible_unverified` or `pending_publication` and **do not** invent URLs.

**Citation (workflow framing):** Google’s launch post describes creating tasks and grouping them into a benchmark for evaluation and sharing. See `m12_linkage_sources.json` → `external_rules_citations`.

---

## 4. Task attachment verification

For each task name in `m12_submission_linkage.json` → `linkage` → `tasks`:

- Confirm the task exists under the benchmark in the Kaggle UI.
- When filling `task_url`, use the canonical task link from the owner UI; never guess from slugs alone.

---

## 5. Notebook pin verification

1. Regenerate canonical notebooks from the repo (never hand-edit `.ipynb` JSON).
2. `python scripts/generate_m11_notebook_release_manifest.py --check`
3. Compare uploaded notebook bytes to `file_sha256` in `m11_notebook_release_manifest.json` before treating a run as authoritative.

---

## 6. Writeup and project link

1. **Primary project link (competition submission):** Kaggle **benchmark** page URL once verified public.
2. **Secondary:** GitHub `https://github.com/m-cahill/lucid` for implementation and source.
3. Ensure M10 narrative (`m10_submission_narrative.md`) cross-links match the linkage manifest.

---

## 7. Drift and recovery

If benchmark metadata, task visibility, or notebook publication **drifts** after a green CI commit:

1. Consult `docs/milestones/M12/artifacts/m12_contingency_matrix.md`.
2. Update `m12_linkage_sources.json` truthfully; run `python scripts/generate_m12_submission_linkage.py --write` and `--check`.
3. Record the change in `M12_run1.md` (or next run file).

---

## 8. What not to do in M12

- No benchmark version bump; no scoring/parser/family edits.
- No default M11 probe reruns.
- No “parser rescue” for excluded models without a new milestone charter.
