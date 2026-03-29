# M00 — CI run analysis (run 1)

**Status:** Placeholder until the first **GitHub Actions** workflow run is available on the remote.

**Local verification (2026-03-29):**

- `ruff check` / `ruff format --check` — pass  
- `mypy src` — pass  
- `pytest` — pass; coverage ≥85% on `src/lucid/`  
- `python scripts/run_local_smoke.py` — writes bundle; `LUCID_SCORE_EPISODE` printed  

After pushing to GitHub, replace this section with a run grounded in `docs/prompts/workflowprompt.md`.
