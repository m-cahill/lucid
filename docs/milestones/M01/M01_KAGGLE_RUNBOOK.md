# M01 — Kaggle Community Benchmarks handoff runbook

**Milestone:** M01 — transport proof for benchmark line **1.1.0**  
**Purpose:** Execute the **real Kaggle platform** steps after repo-side assets are merged. This document is **not** a substitute for the [Kaggle Benchmarks cookbook](https://github.com/Kaggle/kaggle-benchmarks/blob/ci/cookbook.md).

**Honesty rule:** **M01 Kaggle E2E is not complete** until a real on-platform notebook/task run succeeds with evidence captured. Install transport and CI green are necessary but not sufficient.

---

## 1. Repo-side prerequisites (offline)

- Transport work lives on **`m01-kaggle-transport-proof`** (pushed to `origin`); open PR for review — **do not merge** until milestone owner approves.
- Canonical notebook: `notebooks/lucid_kaggle_transport_text_adapter_m_01.ipynb` (regenerate with `scripts/generate_kaggle_notebook.py`). Contract: `docs/kaggle/LUCID_KAGGLE_NOTEBOOK_CONTRACT.md`.
- **One** `%choose` selecting **`lucid_main_task`**; **one** `@kbench.task` only.
- Deterministic slice matches `tests/fixtures/kaggle_transport/transport_manifest.json` (seeds **100/LOW**, **42/MEDIUM**, **200/HIGH**).
- Local gates green: `ruff`, `mypy`, `pytest`, `python scripts/run_local_smoke.py`.

---

## 2. Installing LUCID on Kaggle (transport order)

Many Kaggle notebook kernels **do not include `git`**, so `pip install git+https://...` often fails. Prefer the following order:

### 2.1 Preferred — pinned GitHub archive ZIP (no git)

**M01.1 proof pin (matches canonical notebook banner + install cell):** use this for an audit-clean install aligned with `notebooks/lucid_kaggle_transport_text_adapter_m_01.ipynb` (same `src/lucid` as branch tip while pin trails only notebook/docs commits — see `docs/kaggle/LUCID_KAGGLE_NOTEBOOK_CONTRACT.md` §5.1):

```text
%pip install -q "https://github.com/m-cahill/lucid/archive/da080cda0760ff742c7e4a69a0a873822049620c.zip"
```

**Branch tip (moves with branch head; not commit-pinned):**

```text
%pip install -q "https://github.com/m-cahill/lucid/archive/refs/heads/m01-kaggle-transport-proof.zip"
```

**Arbitrary commit (reproducible; replace `<FULL_SHA>` with the 40-character commit):**

```text
%pip install -q "https://github.com/m-cahill/lucid/archive/<FULL_SHA>.zip"
```

After install, verify (distribution metadata name is **`lucid-benchmark`**; import package is **`lucid`**):

```python
import importlib
importlib.import_module("lucid.kaggle")
```

### 2.2 Fallback — wheel uploaded as a Kaggle dataset

Build a wheel locally (`python -m build --wheel`); CI also verifies the wheel contains `lucid/kaggle/episode_llm.py`. Upload the `.whl` as a **notebook input dataset**, then install from the mounted path (adjust folder/filename to match your dataset):

```text
%pip install -q /kaggle/input/<your-dataset-name>/lucid_benchmark-0.1.0-py3-none-any.whl
```

Re-run the same `importlib.import_module("lucid.kaggle")` check.

### 2.3 Last resort — `git+https` (only if `git` exists)

Use only after confirming `git --version` works in the notebook session:

```text
%pip install -q "git+https://github.com/m-cahill/lucid.git@<ref>"
```

### 2.4 Path shadowing

Do not attach a **partial** `lucid/` source tree as a dataset if it would appear **before** `site-packages` on `sys.path` and omit `lucid/kaggle/`. Prefer one clean install path (ZIP or wheel) per session.

---

## 3. Kaggle notebook workflow

1. Create or open a Kaggle notebook in the **Community Benchmarks** flow (see competition / platform UI for the current entry point).
2. Install LUCID using **§2.1** (or **§2.2** / **§2.3** as needed).
3. Use the code cells in the **canonical** notebook `notebooks/lucid_kaggle_transport_text_adapter_m_01.ipynb` (generated; see `docs/kaggle/LUCID_KAGGLE_NOTEBOOK_CONTRACT.md`).
4. Copy any remaining cells so task names and `%choose` stay aligned.
5. **Model:** prefer a **Kaggle-hosted** model (e.g. examples in the upstream cookbook). One model is enough for the acceptance run; add a second only after the first proof is green.
6. **Save Version** after a successful run.

---

## 4. Leaderboard / main task

- The notebook must expose **exactly one** main leaderboard task via `%choose` in the **final** code cell (see cookbook: [Publishing Your Task to the Leaderboard](https://github.com/Kaggle/kaggle-benchmarks/blob/ci/cookbook.md)).
- Dataset evaluation uses `.evaluate(...)` over the fixed three-row slice; the main task aggregates per-row scores (see notebook implementation).

---

## 5. Evidence capture (commit back to `docs/milestones/M01/`)

Fill `M01_KAGGLE_EVIDENCE_TEMPLATE.md` (or rename to `M01_run1.md` once populated) with:

- Notebook URL / version identifier
- Task and Community Benchmark identifiers (as shown in the UI)
- Model identifier used on platform
- Screenshots or exports if links are brittle
- Install method used (ZIP SHA, wheel dataset name, etc.)
- Any manual steps, friction, or permission blockers

**Honesty rule:** If a full platform run cannot be completed, **do not** claim M01 E2E complete; record the blocker and keep CI green on offline transport checks only.

---

## 6. Semantic freeze

- **No** change to scoring profile **1.1.0**, output meaning, or family semantics under the banner of “Kaggle compatibility.” Transport-only differences must be documented as such.
