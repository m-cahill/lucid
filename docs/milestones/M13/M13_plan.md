# M13 — Contingency buffer

**Status:** **Active** — see `docs/lucid.md` section 9.

**Purpose:** Post-M12 follow-ups that are **not** blocking for the core M12 linkage deliverable:

- **Truthful documentation** of observed Kaggle benchmark/task state vs M12-intended linkage (`M13_run1.md`, `M13_run2.md`).
- Owner-view **public URL verification** when available; update `m12_linkage_sources.json` and regenerate linkage **only** with verified URLs / `public_verified`.
- **Narrow platform repair** per `m12_contingency_matrix.md` (e.g. reattach `lucid_m09_mature_evidence_task` if detached — **operator Kaggle UI**; not automatic from repo).
- **Post-submission polish** for narrative or evidence packaging (no benchmark semantic changes without change control).

**Explicitly out of scope by default:** benchmark version bump; parser/prompt rescue for excluded M11 models; new families; **creation** of `lucid_family1_m04_task` on Kaggle without a separate publication decision (see `M13_run2.md`).

**Deliverables:** `M13_run1.md`, `M13_run2.md`, `M13_toolcalls.md`; ledger updates in `docs/lucid.md`.

**M12 merge (reference):** PR https://github.com/m-cahill/lucid/pull/13 — merge commit `6211b0c9b0197ab89ac5ddcc5350f3bc4d3840ed` on `main`; final green PR CI run **24108099234** on head `513d230c0660f1e24b5995abf610e21116048a0f` (see `docs/milestones/M12/M12_run1.md`).
