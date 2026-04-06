# M10 — Writeup evidence pack, figures, and judge-facing narrative

**Milestone identity:** M10  
**Primary judged axis:** Writeup quality  
**Secondary synthesis:** Dataset quality & task construction; novelty / insights / discriminatory power  
**Benchmark version target:** **1.1.0** (no bump)  
**Branch:** `m10-writeup-pack`

## Goal

Turn the closed M01–M09 evidence base into a **judge-facing submission-quality narrative pack** that is accurate, deterministic where possible, traceable to committed artifacts, and honest about limitations — **without** new benchmark semantics or broad reopened model-running scope.

## In scope (delivered)

- Judge-facing narrative artifacts under `docs/milestones/M10/artifacts/`
- Deterministic figure/table generation: `scripts/generate_m10_figures.py`, `scripts/generate_m10_tables.py` (`--write` / `--check`; CI `--check`)
- Claims-to-evidence matrix, limitations register, representative model portfolio, optional judge FAQ
- Ledger alignment: `docs/lucid.md`, `docs/LUCID_COMPETITION_ALIGNMENT.md`, `docs/LUCID_OPERATING_MANUAL.md` (tight updates only)

## Out of scope

- New Kaggle runs by default; full hosted-roster completion; new families/packs/scorer changes; benchmark version bump; fabricating unsupported slice metrics from exports

## Acceptance

See `docs/milestones/M10/M10_summary.md` and `docs/milestones/M10/M10_audit.md`.
