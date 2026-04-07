# M12 — Final submission checklist (operator)

Use with `M12_SUBMISSION_RUNBOOK.md`. Check each box before treating the competition entry as linkage-complete.

## A. Repository

- [ ] On branch intended for merge (e.g. `m12-final-linkage`); `docs/lucid.md` reflects M12 scope.
- [ ] `python scripts/generate_m12_submission_linkage.py --check` passes locally.
- [ ] Full CI green on the closing commit (lint, tests, all generator `--check` steps).

## B. Kaggle benchmark object

- [ ] Benchmark slug matches `m12_linkage_sources.json` / `m12_submission_linkage.json` (`michael1232/lucid-kaggle-community-benchmarks`).
- [ ] Owner-view confirms whether the benchmark is **public** or still **owner-only**; update `publication_status` and URLs in `m12_linkage_sources.json`, regenerate linkage, re-run `--check`.
- [ ] If URLs are filled in, every external URL also appears in `m12_submission_linkage.md` (generated) and `m12_public_links.json`.

## C. Tasks (six)

- [ ] `lucid_main_task` — transport / M01.
- [ ] `lucid_family1_m04_task` — Family 1 analytics panel.
- [ ] `lucid_m09_mature_evidence_task` — mature 72-episode panel.
- [ ] `lucid_m11_probe_p12_task`, `lucid_m11_probe_p24_task`, `lucid_m11_probe_p48_task` — probe ladder.

## D. Notebooks

- [ ] Canonical `.ipynb` files regenerated from repo generators; `m11_notebook_release_manifest.json` `--check` passes.
- [ ] Kaggle copies match committed SHAs before any publication step (see `M11_KAGGLE_RUNBOOK.md` discipline).

## E. Writeup

- [ ] Primary **project link** in the competition submission points to the **Kaggle benchmark page** (once URL is known).
- [ ] GitHub repo linked as **secondary** implementation/source in narrative or linkage pack.
- [ ] M10 narrative pack reviewed for stale links; M11 addendum present where probe evidence is cited.

## F. Evidence hygiene

- [ ] Authoritative M11 CSVs live under `docs/milestones/M11/artifacts/` (ingest + cost).
- [ ] No reliance on `.cursor-ci-runs.json` or other local-only caches for claims.
