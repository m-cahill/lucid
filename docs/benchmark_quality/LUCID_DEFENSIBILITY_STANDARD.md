# LUCID defensibility standard

**Project:** LUCID  
**Document type:** Canonical benchmark-quality / audit policy  
**Benchmark version:** **1.1.0** (scoring semantics unchanged unless change control bumps)  
**Authority:** Complements `docs/LUCID_MOONSHOT.md` §12 and `docs/lucid.md` (ledger).

---

## 1. What “defensibility” means in this repo

**Defensibility** is the property that a benchmark’s **task construction, lineage, and claims** can be **reconstructed and checked** from committed artifacts and deterministic tooling — not that every judge agrees with every design choice.

LUCID defensibility has three pillars:

1. **Synthetic construction** — episodes trace to **generation code + seeds + template versions**, not opaque human annotation.
2. **Manifest lineage** — unified rows map **one-to-one** back to canonical per-family manifests; hashes over canonical `episode_spec` JSON are stable audit anchors.
3. **Repeatable audits** — `scripts/run_unified_defensibility_audit.py` (`--write` / `--check`) produces **deterministic** JSON + summary outputs for CI and human review.

---

## 2. Contamination resistance (honest scope)

**Contamination resistance** means the benchmark is **designed to reduce** trivial memorization of fixed public items and to privilege **on-the-fly rule tracking** under drift.

It is **not** a claim of cryptographic impossibility of advantage. See `docs/milestones/M08/artifacts/m08_contamination_posture.md` for realistic leakage vectors (public repo, template repetition, hosted execution).

---

## 3. Hard blockers vs soft warnings

| Class | Enforced in CI | Purpose |
|-------|----------------|---------|
| **Hard** | **Yes** (`--check` fails) | Lineage integrity, uniqueness, rebuild parity with generators, hash correctness, required metadata, drift / variant validity, distribution consistency, **unapproved** exact-duplicate groups |
| **Soft** | **No** (informational) | High token / n-gram similarity, repeated prompt skeletons, ambiguity-window heuristics |

Soft findings are **surfaced** in `m08_defensibility_audit.json` and may be dispositioned in milestone summaries. They become merge blockers **only** if an explicit future policy ties thresholds to CI (not the default in M08).

---

## 4. Exact duplicates, near-duplicates, and family siblings

| Concept | Treatment |
|---------|-----------|
| **Exact duplicate** | Same canonical **episode_spec** bytes (SHA-256). More than one unified row per hash is a **hard failure** unless a **tiny, rationale-backed** entry exists in `m08_exact_duplicate_allowlist.json`. Default: **no silent exceptions.** |
| **Near-duplicate (soft)** | Similar **normalized text** (token-set Jaccard, character n-gram overlap) or repeated **skeleton** prefixes — reported, not blocked. |
| **Family siblings** | Episodes that share structural scaffolding within a template family are **expected**; soft tools quantify surface overlap for review. |

---

## 5. Evidence required for stronger dataset-quality claims

Future milestones may claim stronger **dataset quality & task construction** posture only when they ship:

- **Green** `python scripts/run_unified_defensibility_audit.py --check` in CI (or documented waiver with governance approval).
- **Committed** M08-style artifacts under `docs/milestones/M08/artifacts/` (or successor milestone paths referenced from `docs/lucid.md`).
- **Explicit** statement of **benchmark version** and whether any change was **semantic** (requires change control) vs **packaging / metadata / audit** only.

**Kaggle platform proof** remains a separate proof class (see `docs/lucid.md` §6.1). Defensibility audits do **not** substitute for platform evidence.

---

## 6. Version discipline

- **Benchmark / scoring semantics** — governed by `docs/contracts/` and `LUCID_CHANGE_CONTROL.md`; bump **benchmark version** when semantics change.
- **Normalization / audit engine** — `normalization_version` and `audit_engine_version` strings document packaging and audit tooling, not correctness labels by themselves.

If an audit discovers a **semantic** defect (labels, scoring expectations, episode meaning), **do not** smuggle a fix without explicit record: file an issue, milestone note, and version decision.
