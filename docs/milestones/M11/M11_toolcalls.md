# M11 — Tool call log

**Milestone:** M11 — Hosted-model probe ladder + response surface
**Status:** Closeout — evidence collected, exclusions evidence-backed.

---

| Timestamp (UTC) | Tool | Purpose | Files / target | Status |
|-----------------|------|---------|----------------|--------|
| 2026-04-06 | — | Stub seeded at M10 closeout | this file | seeded |
| 2026-04-06 | implementation | M11 Phase 1: `m11_probe_panels.py`, artifacts, notebooks, stubs, CI, ledger | `src/lucid/kaggle/m11_probe_panels.py`, `scripts/generate_m11_*.py`, `docs/lucid.md`, `docs/LUCID_COMPETITION_ALIGNMENT.md`, `.github/workflows/ci.yml` | complete |
| 2026-04-06 | implementation | M11 Phase 3: full ingest, tables, figures; pin `13137d9`; `M11_run1/summary/audit` | `scripts/m11_ingest_common.py`, `ingest_m11_platform_exports.py`, `generate_m11_tables.py`, `generate_m11_figures.py`, `docs/milestones/M11/artifacts/` | complete |
| 2026-04-06 | implementation | Publication policy hardening: manifest generator, runbook retry rules, ledger policy section | `scripts/generate_m11_notebook_release_manifest.py`, `docs/lucid.md`, `M11_KAGGLE_RUNBOOK.md`, `M11_toolcalls.md`, `.github/workflows/ci.yml` | complete |
| 2026-04-06 | implementation | Kaggle pin + packaging: wheel guard for `m11_probe_panels`, git-HEAD verify, import tests, preflight cell | `scripts/verify_wheel_has_kaggle.py`, `scripts/verify_m11_git_has_module.py`, `tests/test_m11_package_visibility.py`, `generate_m11_kaggle_notebooks.py`, `pyproject.toml`, CI | complete |
| 2026-04-06 | incident | Kaggle preflight `m11_probe_panels` MISSING: pin `13137d907e938c6ed36c2b17eb0c4347f2d3943c` has no `m11_probe_panels.py` in tree; GitHub ZIP = committed tree only, not local untracked files | outcome `run_error`, reason `bad_pin_commit_missing_m11_module` | resolved by two-commit workflow (see `M11_run1.md`) |
| 2026-04-07 | evidence sync | P12 evidence ingest: leaderboard CSV + cost CSV, comparator `lucid_main_task`, Gemini 2.5 Flash cost merge, operator exclusions (31 tracked) | `m11_model_response_surface.*`, `m11_p12_vs_main_comparison.csv`, `m11_p12_cost_frontier.csv`, `m11_p24_candidate_set.md`, `m11_allocation_policy.md`, `m11_fig_p12_delta_vs_cost.png` | complete |
| 2026-04-07 | closeout | Evidence-backed failure classification for DeepSeek-R1 and gpt-oss-120b; roster updated with exact failure codes + detail; M11 docs hardened for closeout | `generate_m11_probe_artifacts.py`, `m11_roster_canonical.json`, `M11_run1.md`, `M11_summary.md`, `M11_audit.md`, `M11_toolcalls.md` | complete |
| 2026-04-07 | CI / shell | `gh run view 24058104201 --log-failed`; root cause: `generate_m11_notebook_release_manifest.py --check` (manifest JSON drift); `M11_run2.md` per `docs/prompts/workflowprompt.md` | `.github/workflows/ci.yml`, `M11_run2.md`, `M11_toolcalls.md` | complete |
| 2026-04-07 | CI fix | Notebook manifest: LF-normalize `.ipynb` before SHA-256 (`ba2e866`); ingest: repo-relative `export_paths` + legacy path resolution (`fc60c93`); CSV hashes LF-normalized in `file_sha256` (`c0f55ce`); green **24105189098** | `generate_m11_notebook_release_manifest.py`, `m11_notebook_release_manifest.json`, `ingest_m11_platform_exports.py`, `m11_ingest_common.py`, M11 artifacts | complete |
| 2026-04-07 | closeout | Roster **31** tracked / **2** excluded via `generate_m11_probe_artifacts.py`; regenerate ingest/tables/figures; align `M11_run1/2`, summary, audit, ledger, M12 handoff; push → confirm `CI` on tip | `docs/milestones/M11/*`, `docs/lucid.md`, `docs/milestones/M12/*`, `scripts/generate_m11_probe_artifacts.py` | complete |

---

## Excluded model failure evidence (closeout record)

### DeepSeek-R1 (`deepseek-r1-0528`)

- **failure_reason_code:** `json_parse_failure_reasoning_wrapper`
- **error:** `ValueError: Confidence is not numeric: None`
- **mechanism:** model emits `<think>...</think>` reasoning trace before JSON; strict text adapter cannot extract structured output
- **classification:** surface-compatibility failure — model reachable, task valid, parse failed before score

### gpt-oss-120b

- **failure_reason_code:** `json_parse_failure_truncated_output`
- **error:** `ValueError: No JSON object found in model output`
- **mechanism:** model returns valid JSON initially but later emits truncated malformed JSON
- **classification:** surface-compatibility failure — model reachable, task valid, parse failed before score

**M11 posture:** no parser/prompt/notebook changes to rescue. These models remain excluded (`tracked: false`) to preserve comparability.

---

## Operator note template (copy per Kaggle upload / run)

```text
### Kaggle run: <task_name> — <date UTC>

- Notebook pin SHA: <40-char-sha>
- Generator --check: PASS / FAIL
- Notebook SHA-256: <from m11_notebook_release_manifest.json>
- Kaggle notebook URL: <url or "not yet published">
- Kaggle notebook version: <version number or "initial">
- Upload type: fresh_upload / rerun / retry_after_platform_failure
- Outcome: completed / platform_limited / run_error / ...
- Failure reason (if any): <reason code, e.g. platform_dns_failure>
- Leaderboard CSV exported: yes / no
- Notes: <free text>
```
