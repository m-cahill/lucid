# M12 — Contingency matrix (narrow lane)

**Scope:** Metadata, publication, and linkage repairs only. **Not** a default rerun of M11 probes or benchmark semantic changes.

| Situation | First action | Escalation |
|-----------|--------------|------------|
| Kaggle benchmark URL changes after submission | Update `kaggle_benchmark_url` in `m12_linkage_sources.json`; regenerate linkage; record in milestone run log | If slug changes, treat as new object: update ledger + M10 pointers |
| Task visibility mismatch (owner vs public) | Set `publication_status` honestly; avoid claiming `public_verified` without owner-view | Document in `m12_public_links.json` |
| Notebook re-upload with **identical** repo-generated `.ipynb` | Re-run `generate_m11_notebook_release_manifest.py --write`; verify `--check`; re-upload same bytes | If Kaggle mutates metadata only, note in runbook; do not edit cells in UI |
| Emergency metadata repair (title/description) | Fix in Kaggle UI per competition rules; sync prose in `m12_linkage_sources.json` if display names change | Defer broad re-evaluation to **M13** unless authorized |
| Parser / prompt rescue for excluded M11 models | **Out of scope** for M12 default lane | Explicit milestone authorization + separate run record |

**Deferred by default:** full hosted-model reruns, new probe tiers, structured-output hardening → **M13** or later.
