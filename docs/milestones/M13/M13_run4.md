# M13 — Run 4 (public URL / publication verification — not completed in repo)

**Branch:** `m13-contingency-buffer`  
**Scope:** Final M13 step per `M12_SUBMISSION_RUNBOOK.md` §3–4: verify benchmark and task **public** visibility and canonical URLs; update `m12_linkage_sources.json` **only** with owner-view or logged-out evidence.

## Verification outcome (this session)

| Item | Result |
|------|--------|
| Owner-view Kaggle UI (copy canonical URLs from benchmark / task pages) | **Not performed** — requires human operator signed in as `michael1232` |
| Logged-out / incognito public visibility check | **Not performed** — requires human operator |
| Automated URL probe (non-authoritative) | Attempted **only** as a sanity check; see below |

### Non-authoritative probe (do not treat as proof)

Anonymous HTTP fetch was attempted for guessed Kaggle benchmark URL patterns; responses were **404** or inconclusive. **This does not prove** the benchmark is private, public, or unreachable — Kaggle routing, auth walls, and SPA behavior are not verifiable from this mechanism. **Do not** change `publication_status` on this basis alone.

## Currently attached LUCID tasks (operator-confirmed as of M13 run 3)

Per `M13_run3.md` and April 8 leaderboard export:

- `lucid_main_task`
- `lucid_m09_mature_evidence_task`
- `lucid_m11_probe_p12_task`
- `lucid_m11_probe_p24_task`
- `lucid_m11_probe_p48_task`

**Not attached:** `lucid_family1_m04_task` (repo-intended; not evidenced on-platform).

## Linkage artifacts

| File | Changed in M13 run 4? |
|------|------------------------|
| `m12_linkage_sources.json` | **No** — URLs remain `null`; `publication_status` remains **`owner_visible_unverified`** |
| `m12_submission_linkage.json` / `.md` | **No** |
| `m12_public_links.json` | **No** |

**Rationale:** Per M12 runbook, **do not invent URLs** from slugs. No verified canonical URLs were recorded in this pass.

## Operator checklist (exit criteria for `public_verified`)

When ready, the owner should:

1. Open benchmark **`michael1232/lucid-kaggle-community-benchmarks`** in the Community Benchmarks UI.
2. Copy the **browser address bar** URL for the benchmark page (canonical).
3. For each attached task above, open the task page and copy **canonical task URLs**.
4. Confirm whether each URL is reachable **logged out** or **incognito** (public) vs owner-only.
5. If and only if verification supports it, set top-level and per-task `publication_status` to `public_verified` in `m12_linkage_sources.json`, fill `kaggle_benchmark_url` and `task_url` fields, then run `python scripts/generate_m12_submission_linkage.py --write` and `--check`.

## M12 closure reference (unchanged)

| Field | Value |
|-------|--------|
| Authoritative green CI (PR #13) | Run ID **24108099234** |
| Merge to `main` | `6211b0c9b0197ab89ac5ddcc5350f3bc4d3840ed` |
