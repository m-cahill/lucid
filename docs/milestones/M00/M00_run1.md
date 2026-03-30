# M00 — CI run analysis (run 1)

**Status:** **Placeholder.** Do **not** treat this file as evidence until the first **real** GitHub Actions run exists for the M00 PR and is pasted/analyzed below.

**What belongs here (after push):**

- Workflow name, run ID, trigger (`pull_request`), branch + **head SHA**
- Job inventory and pass/fail per `docs/prompts/workflowprompt.md`
- Verdict on whether the run is a trustworthy green signal

---

## Local verification only (not a substitute for GitHub)

Recorded before the authoritative remote run:

- `ruff check` / `ruff format --check` — pass  
- `mypy src` — pass  
- `pytest` — pass; coverage ≥85% on `src/lucid/`  
- `python scripts/run_local_smoke.py` — writes bundle; `LUCID_SCORE_EPISODE` printed  

---

## GitHub Actions — run 1 (to be filled after first real run)

*Replace this section when the first PR workflow completes.*
