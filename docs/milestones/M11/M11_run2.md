# M11 — CI workflow analysis (run 2) + corrective recovery

**Milestone:** M11 — hosted-model probe ladder + response surface  
**Analysis template:** `docs/prompts/workflowprompt.md`  
**Date (UTC):** 2026-04-07  

This file records (1) the **initial** merge-blocking failure on `main`, (2) **root-cause analysis**, (3) the **corrective commits** that restored a **green** CI signal, and (4) the **formal closeout** follow-up (roster + regenerated artifacts + ledger).  

---

## A — Initial failure (authoritative record)

| Field | Value |
| ----- | ----- |
| Workflow | **CI** (`.github/workflows/ci.yml`) |
| Run ID | **24058104201** |
| URL | https://github.com/m-cahill/lucid/actions/runs/24058104201 |
| Trigger | push to `main` |
| Commit | `f2faeefa6eb673d4cf597c3dc32ee4b6445e6ced` |
| First failing step | `python scripts/generate_m11_notebook_release_manifest.py --check` |
| Conclusion | **failure** |

**Classification:** **Publication-contract drift** — not a scorer/runtime/semantic defect. Lint, format, mypy, and pytest completed before the manifest gate.

---

## B — Root causes (three separate issues)

### 1. Notebook release manifest (SHA-256)

**Symptom:** `m11_notebook_release_manifest.json` differed from generator output on Ubuntu.  

**Cause:** `.ipynb` files were hashed as **raw bytes**. Windows working trees often use **CRLF**; Linux CI and Git blobs use **LF**, producing different SHA-256 values for the same logical notebook.  

**Fix (commit `ba2e866`):** Normalize newlines before hashing `.ipynb` in `scripts/generate_m11_notebook_release_manifest.py`. Regenerate `m11_notebook_release_manifest.json`.

### 2. M11 ingest meta (`export_paths`)

**Symptom:** `ingest_m11_platform_exports.py --check` failed with `FileNotFoundError` for a path like  
`/home/runner/.../lucid/C:/coding/kaggle/lucid/docs/...`.  

**Cause:** Ingest meta stored **Windows-absolute** paths in `m11_model_response_surface.json`. On Linux, joining `root / Path("C:/...")` does not resolve to the repo file.  

**Fix (commit `fc60c93`):** Store **repo-relative** paths in meta (`_repo_relative`); resolve legacy absolute strings in `--check` (`_meta_export_path`). Regenerate ingest outputs touched by meta/manifest text.

### 3. Probe run manifest (export file hashes)

**Symptom:** After (1) and (2), CI failed with `m11_probe_run_manifest.md mismatch`.  

**Cause:** Embedded SHA-256 for **CSV** exports used **raw** bytes; CRLF vs LF again diverged Windows vs Linux.  

**Fix (commit `c0f55ce`):** In `scripts/m11_ingest_common.py`, LF-normalize **`.csv`** bytes in `file_sha256`. Regenerate `m11_probe_run_manifest.md`.

---

## C — Corrective CI series (maintenance commits)

| Run ID | Commit (short) | Conclusion | Notes |
| ------ | -------------- | ---------- | ----- |
| 24104774914 | `ba2e866` | failure | Ingest + tables step; `export_paths` / path join |
| 24105005656 | `fc60c93` | failure | `m11_probe_run_manifest.md` hash mismatch |
| **24105189098** | **`c0f55ce`** | **success** | **Authoritative green** after CSV hash normalization |

**Authoritative green (tooling recovery):** https://github.com/m-cahill/lucid/actions/runs/24105189098 — commit **`c0f55ce7cdbc8d9b3feca7625379cb59211b0cd1`**.  

**Verdict (through `c0f55ce`):** ⛔ Merge was blocked while `main` was red; **after `c0f55ce`, CI is green** and merge is **unblocked** for subsequent commits.

---

## D — Formal closeout follow-up (this milestone pack)

Content-closeout items (31 tracked / 2 excluded roster, regenerated ingest/tables/figures, ledger alignment) are applied **after** the `c0f55ce` baseline in a **separate** commit that:

- Restores **evidence-backed** exclusions in `generate_m11_probe_artifacts.py` and `m11_roster_canonical.json` (**31** `tracked`, **2** excluded).
- Regenerates **M11 ingest + tables + figures** artifacts so `--check` stays aligned.
- Updates **M11** summary / audit / toolcalls / `docs/lucid.md` and **M12** handoff files.

**Post–closeout-commit CI:** confirm on GitHub Actions for the **tip** of `main` after that push (run ID recorded in `M11_toolcalls.md`).

---

## E — Invariants (held)

| Invariant | Status |
| --------- | ------ |
| Benchmark **1.1.0** unchanged | Held |
| No scorer/parser/schema/family edits for exclusions | Held |
| Generator `--check` gates remain merge-blocking | Held |
| Cross-platform determinism for manifest + ingest hashes | Improved (LF normalization + repo-relative meta) |

---

## F — Next actions (post-closeout)

| Action | Owner |
| ------ | ----- |
| Confirm green CI on **closeout** tip after push | Maintainer |
| M12 execution per `docs/milestones/M12/M12_plan.md` | Maintainer |
