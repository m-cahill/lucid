# M03 Plan — Family 1 scale-up (symbolic negation / local rule-reversal dataset expansion)

**Project:** LUCID  
**Milestone:** M03  
**Title:** Family 1 scale-up — symbolic negation / local rule-reversal dataset expansion  
**Benchmark line:** **1.1.0** (no scoring-profile change; no benchmark version bump)

**Status:** **Closed** (repository record 2026-03-31)

---

## 1. Objective

Convert **Family 1** (`symbolic_negation_v1`) from the **three-row M01 transport acceptance slice** into the first **canonical deterministic offline benchmark pack** large enough to support **M04** analytics (difficulty / spread / promotion decision), without changing benchmark semantics or widening faculty scope.

**Primary judged axis (this milestone):** **Dataset quality & task construction** — explicit drift, audit-ready episodes, reproducible pack definition.

---

## 2. Scope

### In scope

- Scale Family 1 beyond the M01 slice to a **minimum 96-episode** core pack with **LOW / MEDIUM / HIGH** balance (32 each).
- **Committed canonical manifest** as source of truth plus **deterministic regeneration** and **`--check`** verification (pattern aligned with the Kaggle notebook generator).
- **Include** the three M01 transport episodes as an **explicit subset** (seeds 100/LOW, 42/MEDIUM, 200/HIGH) with documented linkage to `tests/fixtures/kaggle_transport/transport_manifest.json`.
- Per-episode audit metadata (embedded as full `episode_spec` in the manifest).
- Tests: determinism vs manifest, uniqueness, required fields, difficulty balance, scorer compatibility (full pack + transport parity), Family 1 **three-episode** E2E smoke (one per bucket).
- Local E2E smoke script: `scripts/run_family1_pack_smoke.py`.
- CI: manifest `--check` step.
- Documentation: `docs/lucid.md`, `docs/families/LUCID_TEMPLATE_FAMILY_SYMBOLIC_NEGATION_V1.md`, targeted `docs/LUCID_COMPETITION_ALIGNMENT.md`.
- `run_smoke` / CLI: optional **`--drift-severity`** so LOW/MEDIUM/HIGH smoke matches generator.

### Out of scope

- Family 2 / Family 3 implementation.
- Scoring profile or benchmark version change.
- Drift taxonomy expansion beyond NEGATION for this family.
- Full hosted-model Kaggle sweep (reserved for later milestones).
- **Promotion / retain / drop verdict** for Family 1 — **M04**.

---

## 3. Canonical pack definition

| Field | Value |
|-------|--------|
| **Pack ID** | `family1_core_m03_v1` |
| **Episode count** | 96 |
| **Difficulty distribution** | 32 LOW, 32 MEDIUM, 32 HIGH |
| **Committed manifest** | `tests/fixtures/family1_core_m03/family1_core_m03_manifest.json` |
| **Seed grid** | LOW: `{1..31, 100}`; MEDIUM: `{32..63}`; HIGH: `{64..94, 200}` (stable order: all LOW, then MEDIUM, then HIGH; seeds sorted within bucket) |
| **Regeneration** | `python scripts/generate_family1_core_m03_manifest.py --write` |
| **Verification** | `python scripts/generate_family1_core_m03_manifest.py --check` |
| **Implementation** | `src/lucid/packs/family1_core_m03.py` |

---

## 4. Exit criteria

1. Canonical manifest committed; `--check` passes locally and in CI.
2. ≥96 episodes; explicit LOW/MEDIUM/HIGH coverage as specified.
3. M01 three episodes are members of the pack and tagged with `m01_transport_fixture_id`.
4. Determinism and metadata tests pass; Family 1 three-episode smoke passes.
5. M01 notebook contract and transport manifest substance preserved; `generate_kaggle_notebook.py --check` passes.
6. Benchmark version remains **1.1.0**.
7. `docs/lucid.md` and family documentation updated; M04 seeded.

---

## 5. Authority

`docs/LUCID_MOONSHOT.md`, `docs/contracts/`, `docs/lucid.md`, `src/lucid/`.
