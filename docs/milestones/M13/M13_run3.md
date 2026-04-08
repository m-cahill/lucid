# M13 — Run 3 (M09 restoration confirmed + DeepSeek v3.1 parse failure)

**Branch:** `m13-contingency-buffer`  
**Scope:** Record successful `lucid_m09_mature_evidence_task` restoration, document `deepseek-v3.1` M09 parse failure without parser rescue, brief M09 coverage summary from April 8 leaderboard export. **No** code changes. **No** benchmark semantic edits.

## M12 closure reference (unchanged)

| Field | Value |
|-------|--------|
| Authoritative green CI (PR #13) | Run ID **24108099234** |
| Final PR head | `513d230c0660f1e24b5995abf610e21116048a0f` |
| Merge to `main` | `6211b0c9b0197ab89ac5ddcc5350f3bc4d3840ed` |

---

## A. M09 task restoration — confirmed

`lucid_m09_mature_evidence_task` was **successfully reattached** to benchmark `michael1232/lucid-kaggle-community-benchmarks` by the account owner in the Kaggle Community Benchmarks UI. The April 8 leaderboard export (supplemental artifact `docs/milestones/M13/artifacts/m13_leaderboard_export_20260408.csv`) shows M09 results across all tracked models.

**Post-restoration attached task set (five tasks):**

- `lucid_main_task`
- `lucid_m09_mature_evidence_task`
- `lucid_m11_probe_p12_task`
- `lucid_m11_probe_p24_task`
- `lucid_m11_probe_p48_task`

**Not attached:** `lucid_family1_m04_task` — not evidenced as ever created on-platform; **not** created in M13 (see `M13_run2.md`).

---

## B. DeepSeek v3.1 M09 parse failure (new event)

| Field | Value |
|-------|--------|
| Task | `lucid_m09_mature_evidence_task` |
| Model | `deepseek-ai/deepseek-v3.1` |
| Evaluation date | 2026-04-08 02:08:53 |
| Numerical result | — (absent) |
| Boolean result | `False` |
| Task state | `BENCHMARK_TASK_RUN_STATE_ERRORED` |

### Failure classification

**Surface compatibility failure / model-output parse incompatibility.**

The model returned malformed JSON in at least some turns. Observed symptoms:

- `json.decoder.JSONDecodeError` raised in `parse_turn_payload()`
- Corrupted JSON keys (e.g. `\u6781_detected` instead of expected key names)
- Stray invalid characters before JSON property names

### Decision

**No parser rescue performed in M13.** This matches the project's standing rule that parser / prompt rescue for malformed hosted-model output is **out of scope** for the default submission-linkage / contingency lane (`docs/milestones/M12/M12_SUBMISSION_RUNBOOK.md` §8, `docs/milestones/M12/artifacts/m12_contingency_matrix.md`).

**Deferred action:** If a narrowly scoped parser-hardening milestone is separately authorized, document the DeepSeek v3.1 failure pattern as the motivating case.

### Relationship to prior exclusions

M11 documented **two** evidence-backed exclusions (`deepseek-r1-0528`, `gpt-oss-120b`) for structured-output / surface-compatibility failures (`docs/milestones/M11/artifacts/m11_roster_canonical.json`). The DeepSeek v3.1 M09 error is the **same class** of issue — malformed model JSON output — on a different task and model.

---

## C. M09 coverage summary (brief — from April 8 export)

| Metric | Count |
|--------|-------|
| Models with numeric M09 mean | **18** |
| Models with M09 failure (`Boolean_Result = False`, no numeric result) | **13** |
| Total models with M09 rows | **31** |

The **13 failures** include the fresh DeepSeek v3.1 error plus **12** pre-existing M09 non-completions already documented in earlier milestone artifacts. The **18 completions** include three fresh April 8 scores (claude-sonnet-4, claude-sonnet-4-5, deepseek-v3.2) alongside 15 results from earlier M09 runs.

This export does **not** replace the authoritative M11 leaderboard artifact at `docs/milestones/M11/artifacts/michael1232_lucid-kaggle-community-benchmarks_leaderboard.csv`. It is preserved as supplemental M13 evidence only.

---

## D. Linkage artifacts

| File | Changed in M13 run 3? |
|------|------------------------|
| `m12_linkage_sources.json` | **No** |
| `m12_submission_linkage.json` / `.md` | **No** |
| `m12_public_links.json` | **No** |

No linkage regeneration was performed. M12 six-task intended surface preserved.

---

## E. Code changes

**None.** No files under `src/`, `tests/`, or `scripts/` were modified.

---

## F. Score ledger (`docs/lucid.md` §6)

**Not updated.** The M01 §6 score ledger is preserved as historical M01 evidence per standing governance rules.

---

## G. Supplemental artifact

| Path | Description |
|------|-------------|
| `docs/milestones/M13/artifacts/m13_leaderboard_export_20260408.csv` | April 8 full benchmark leaderboard export — reference evidence for M09 restoration and DeepSeek v3.1 failure documentation |

---

## H. Local verification (this commit)

Documentation-only delta; full repo gates run before commit.
