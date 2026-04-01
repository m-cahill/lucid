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

## 2. PR / CI

| Field | Value |
|-------|--------|
| PR | https://github.com/m-cahill/lucid/pull/10 |
| PR head SHA | `594f0e2d1ad64a2945a5819fd81aeb13b1ac7d38` |
| Authoritative `pull_request` CI run ID | `23871248291` |
| CI URL | https://github.com/m-cahill/lucid/actions/runs/23871248291 |
| CI conclusion | **success** (job `lint-test`, ~2m23s) |

**Workflow:** `CI` — job `lint-test` per `.github/workflows/ci.yml`.

### Workflow inventory (Step 1 — `workflowprompt.md`)

| Step / check | Required | Pass |
|--------------|----------|------|
| Ruff check | yes | yes |
| Ruff format | yes | yes |
| Mypy | yes | yes |
| Pytest + coverage (≥85%) | yes | yes |
| Wheel + `lucid.kaggle` verify | yes | yes |
| M01 notebook `--check` | yes | yes |
| M04 notebook `--check` | yes | yes |
| M09 panel artifact `--check` | yes | yes |
| M09 notebook `--check` | yes | yes |
| F1/F2/F3/M07 manifest `--check` | yes | yes |
| M08 defensibility `--check` | yes | yes |

**Annotation:** Node.js 20 deprecation notice on `actions/checkout@v4` / `actions/setup-python@v5` — informational; does not fail the job.

**Signal:** PR head is a **trusted green** for merge gating on this change set.

---

## 3. Kaggle platform evidence (Phase C)

**Not recorded in this session** — see `docs/milestones/M09/artifacts/m09_kaggle_run_manifest.md`.

No notebook URL, task URL, hosted-model roster, or scores were supplied for ingestion. CSVs under `docs/milestones/M09/artifacts/` are **header-only** placeholders until a real run.

---

## 4. Merge / post-merge

| Field | Value |
|-------|--------|
| Merge commit SHA | *Fill after merge to `main`* |
| Post-merge `main` CI run ID | *Fill after merge* |
| Post-merge CI URL | *Fill after merge* |

**Merge discipline:** Merge only after PR CI is green; post-merge CI should be recorded when available.
