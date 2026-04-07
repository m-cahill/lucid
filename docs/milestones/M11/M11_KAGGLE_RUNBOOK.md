# M11 — Kaggle probe runbook (ten-day cadence)

**Milestone:** M11  
**Purpose:** Disciplined spend of the remaining **daily** Kaggle benchmark budget through **deterministic** probe tasks (P12 / P24 / P48) and **M09-comparable** P72 reruns where justified.

**Competition deadline:** Confirm on the official [Rules](https://www.kaggle.com/competitions/kaggle-measuring-agi/rules) page before execution.

---

## Preconditions

1. **Commit-pinned** notebooks: regenerate from the release SHA so `%pip install` matches the evaluated code:

   ```text
   python scripts/generate_m11_kaggle_notebooks.py --write
   python scripts/generate_m09_kaggle_notebook.py --pin-sha <40-char-sha> -o notebooks/lucid_kaggle_m09_mature_evidence.ipynb
   ```

2. **Task names** (must match notebook decorators):

   * `lucid_m11_probe_p12_task`
   * `lucid_m11_probe_p24_task`
   * `lucid_m11_probe_p48_task`
   * `lucid_m09_mature_evidence_task` (P72)

3. **Canonical roster:** 33 tracked models — `docs/milestones/M11/artifacts/m11_roster_canonical.json` (aligned with `m09_model_scores.csv`).

4. **Pin SHA must include M11 code.** The `%pip install` URL embeds a GitHub archive for a single commit. If that commit predates `src/lucid/kaggle/m11_probe_panels.py`, Kaggle will show `lucid.kaggle.m11_probe_panels -> MISSING` in the preflight cell. **Fix in repo only:** merge or commit M11, then regenerate notebooks with `python scripts/generate_m11_kaggle_notebooks.py --write` (uses current `HEAD` unless you pass `--pin-sha`). Re-upload the `.ipynb` from file — **never** debug by editing cells on Kaggle.

### If preflight shows `m11_probe_panels` MISSING

**This is never fixed in the Kaggle UI.** Wrong pin or missing committed tree content — fix in the repo, regenerate notebooks, upload again. Retries use repo-generated `.ipynb` only.

| Cause | What to do |
|--------|------------|
| Stale pin (SHA before M11 landed) | Two-step: commit M11, then regenerate notebooks so `%pip` points at that post-M11 SHA (`python scripts/verify_m11_git_has_module.py --sha <pin>` must pass) |
| Packaging regression | Local: `python -m build --wheel` then `python scripts/verify_wheel_has_kaggle.py` — must list `m11_probe_panels.py` in the wheel |
| Wrong branch / unpushed commit | Push the commit GitHub serves in the ZIP URL, then regenerate |

**Notebook publication (minimal):** Kaggle notebooks are disposable execution surfaces. Canonical changes happen in repo generators only — never hand-edit task logic on Kaggle for benchmark runs.

---

## Outcome normalization (every run)

Classify each model × tier as one of:

* `completed`
* `platform_limited`
* `timeout_or_budget`
* `model_unavailable`
* `run_error`
* `export_missing`
* `manual_skip`

**Rule:** Missing platform fields = explicit `NA` + reason code in ingest (Phase 3), not silent blanks.

---

## Suggested cadence (calendar days)

| Window | Action |
|--------|--------|
| **Days 1–2** | Run **P12** across full tracked roster; establish completion baseline |
| **Days 3–4** | Run **P24** on P12 completers + strategically retested failures |
| **Days 5–7** | Run **P48** on models with acceptable P24 completion; include anomalies |
| **Days 8–9** | **P72** / M09 comparable on final-story candidates, collapse cases, 1–2 stable references |
| **Day 10** | Cleanup reruns; export ingest; response-surface generation; allocation memo |

**Repeat lane:** Use **P12** notebook/task for repeat runs on the M10-style portfolio (ceiling, upward movers, collapse cases, near-flat mid-tier) — same episode IDs as P12.

---

## What to record

* Notebook pin SHA, benchmark slug, task name, run timestamp (UTC)
* Raw leaderboard export paths (audit trail)
* Any platform-exposed latency / cost fields (verbatim) or explicit `NA`

---

## Publication / retry policy

**Repo-generated notebooks only.** Kaggle is a disposable execution surface — not an editing environment.

### Before upload

0. **Git must contain M11** at `HEAD` (otherwise the GitHub ZIP has no `m11_probe_panels`):

   ```text
   python scripts/verify_m11_git_has_module.py
   ```

   If this fails, add/commit `src/lucid/kaggle/m11_probe_panels.py` and related files, then continue.

1. Regenerate notebooks from repo (omit `--pin-sha` to use `git rev-parse HEAD`):

   ```text
   python scripts/generate_m11_kaggle_notebooks.py --write
   python scripts/generate_m09_kaggle_notebook.py --pin-sha $(git rev-parse HEAD) -o notebooks/lucid_kaggle_m09_mature_evidence.ipynb
   ```

   On Windows PowerShell, use ``--pin-sha (git rev-parse HEAD)`` or paste the 40-char SHA manually.

2. Verify generators match committed files:

   ```text
   python scripts/generate_m11_kaggle_notebooks.py --check
   python scripts/generate_m09_kaggle_notebook.py  --check -o notebooks/lucid_kaggle_m09_mature_evidence.ipynb
   ```

3. Generate notebook release manifest:

   ```text
   python scripts/generate_m11_notebook_release_manifest.py --write
   python scripts/generate_m11_notebook_release_manifest.py --check
   ```

4. Upload `.ipynb` from file to Kaggle (do **not** paste or retype code into the Kaggle editor).

### Retry after platform failure

If a run fails for platform-side reasons (DNS resolution failure, model-proxy timeout, network error), **do not** edit the notebook in the Kaggle UI.

* Classify the outcome as **`run_error`** with a reason code:
  - `platform_dns_failure` — `[Errno -3] Temporary failure in name resolution`
  - `platform_proxy_timeout` — model-proxy connection timeout
  - `platform_network_error` — other connectivity failure
* Retry by **re-running the same uploaded notebook** or **re-uploading a freshly regenerated copy** from the repo.
* Only change notebook content by changing generators or source code in the repo, regenerating locally, and verifying `--check`.

### Operator execution sequence

0. `python scripts/verify_m11_git_has_module.py` (must pass)
1. Regenerate notebooks from repo (pin SHA = `HEAD` after M11 is committed)
2. Run generator `--check`
3. Generate notebook release manifest (`--write`, then `--check`)
4. Record notebook SHA-256 (from manifest) in `M11_toolcalls.md`
5. Upload `.ipynb` from file to Kaggle
6. Run task on Kaggle
7. If platform failure → record `run_error` + reason code; retry with same or freshly regenerated notebook
8. Export leaderboard CSV after successful run
9. Ingest exports locally (`scripts/ingest_m11_platform_exports.py --write`)
10. Commit updated artifacts

---

## Diagnostic / smoke-test notebooks

If you need a non-benchmark diagnostic notebook (e.g. to test DNS resolution or model-proxy connectivity before spending budget on a probe run), **generate it from the repo** — do not create it by editing cells in the Kaggle UI.

A dedicated platform smoke-test notebook generator is **deferred** for now. If needed, create a minimal `scripts/generate_kaggle_platform_smoke_notebook.py` following the same pattern as the M11 probe generators, and label the notebook output clearly as **NON-EVIDENCE / DIAGNOSTIC** so it is never confused with benchmark claims.

---

## Honesty boundary

Do **not** claim family/difficulty/component slices from aggregate M09 exports. **Only** claim slices directly measured by M11 probe panels or explicitly present in raw per-episode exports if the platform provides them.
