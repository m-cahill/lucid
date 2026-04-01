# M09 — Run log 1 (local verification + PR / CI)

**Project:** LUCID  
**Milestone:** M09 — Expanded Kaggle evidence on the mature benchmark  
**Branch:** `m09-kaggle-evidence`  

---

## 1. Local verification (authoritative for this revision)

Commands run from repository root (Windows PowerShell; paths as in repo):

```bash
python scripts/generate_unified_core_m07_manifest.py --check
python scripts/run_unified_defensibility_audit.py --check
python scripts/run_unified_pack_smoke.py
pytest
python scripts/generate_m09_panel_artifact.py --check
python scripts/generate_m09_kaggle_notebook.py --check -o notebooks/lucid_kaggle_m09_mature_evidence.ipynb
```

**Outcome:** All steps **passed** (unified manifest OK; M08 audit artifacts OK; unified pack smoke `all_ok n=9`; pytest with coverage ≥85%; M09 panel JSON OK; M09 notebook `--check` OK).

**Notebook `--check` pin:** Extracted from `notebooks/lucid_kaggle_m09_mature_evidence.ipynb` — embeds **`3a0f774d6f7ed069ed088364ab7d9c175b079b01`** (GitHub ZIP install target; that commit contains `m09_evidence_panel.py`). Branch tip may be one commit ahead (notebook-only pin alignment).

---

## 2. PR / CI (update after push)

| Field | Value |
|-------|--------|
| PR URL | *Fill after `gh pr create` or GitHub UI* |
| PR head SHA | *Fill after push* |
| Authoritative `pull_request` CI run ID | *Fill from GitHub Actions* |
| CI conclusion | *Expected: success* |

**Workflow:** `CI` — job `lint-test` per `.github/workflows/ci.yml` (Ruff, Ruff format, Mypy, Pytest+coverage, wheel verify, M01/M04/M09 notebook `--check`, manifest `--check`s, M08 defensibility `--check`).

**Workflow analysis:** Follow structure in `docs/prompts/workflowprompt.md` — treat CI as truth signal; record job inventory and conclusion once the PR run exists.

---

## 3. Kaggle platform evidence (Phase C)

**Not recorded in this session** — see `docs/milestones/M09/artifacts/m09_kaggle_run_manifest.md`.

No notebook URL, task URL, hosted-model roster, or scores were supplied for ingestion. CSVs under `docs/milestones/M09/artifacts/` are **header-only** placeholders until a real run.

---

## 4. Merge / post-merge (update after merge)

| Field | Value |
|-------|--------|
| Merge commit SHA | *TBD* |
| Post-merge `main` CI run ID | *TBD* |
| Post-merge CI URL | *TBD* |

**Merge discipline:** Merge only after PR CI is green and governance docs are reviewed; avoid needless post-merge doc-only churn unless required.
