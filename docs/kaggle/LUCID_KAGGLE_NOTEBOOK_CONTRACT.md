# LUCID — Kaggle Notebook Contract

**Status:** Standing transport contract (introduced during **M01.1**; applies beyond M01.)  
**Authority:** Transport and notebook structure only — does **not** change benchmark semantics.  
**Frozen benchmark line:** **1.1.0** · **symbolic_negation_v1** · scoring profile **1.1.0**

---

## 1. Canonical artifact

| Item | Rule |
|------|------|
| **Single canonical notebook path** | `notebooks/lucid_kaggle_transport_text_adapter_m_01.ipynb` |
| **Production path** | `python scripts/generate_kaggle_notebook.py` — **do not** hand-edit committed JSON except via regeneration |
| **Superseded notebooks** | Older schema-based notebooks live under `notebooks/archive/` and are **non-canonical** |

---

## 2. Required notebook shape (cell order)

1. **Metadata banner** (markdown) — pinned commit SHA, benchmark version, family, scoring profile, acceptance slice (for audit / evidence).
2. Title / context (markdown).
3. Install (markdown + code) — **commit-pinned** GitHub archive ZIP URL only in the install cell (see §5).
4. Environment verification (markdown + code) — `sys.path`, distribution metadata, `lucid` / `lucid.kaggle` resolution.
5. Imports and constants (markdown + code) — includes fixed `EVAL_ROWS` for M01.
6. Adapter layer (markdown + code) — plain-text responses → strict JSON parse (no `schema=` on `llm.prompt`).
7. Prompt builders (markdown + code).
8. Deterministic scoring (markdown + code) — D, L, O, A, C and scalar  
   `0.40*D + 0.20*(1-L) + 0.15*(1-O) + 0.15*A + 0.10*C` (transport must match profile **1.1.0**).
9. Episode runner (markdown + code) — `llm.prompt(...)` then `parse_turn_payload(raw)` only.
10. Optional debug cell (markdown + code) — may be commented out.
11. **Exactly one** `@kbench.task(name="lucid_main_task")` (code).
12. `lucid_main_task.run(kbench.llm)` (code).
13. **Exactly one** `%choose lucid_main_task` (code) — final cell.

---

## 3. Hard rules

| Rule | Detail |
|------|--------|
| **One Kaggle task** | Exactly **one** `@kbench.task` — name **`lucid_main_task`**. No helper decorated tasks. |
| **One `%choose`** | Exactly **one** cell containing `%choose`; must select `lucid_main_task`. |
| **No schema prompts** | Forbidden: `llm.prompt(..., schema=...)`. Required: `raw = llm.prompt(...)` then local parse. |
| **Fixed acceptance slice** | `EVAL_ROWS` = `(100, LOW)`, `(42, MEDIUM)`, `(200, HIGH)` — unchanged for M01 transport proof. |
| **Run before choose** | `lucid_main_task.run(kbench.llm)` **before** `%choose lucid_main_task`. |
| **No semantic drift** | Kaggle compatibility must not change scoring meaning, profile, or family behavior. |

---

## 4. JSON extraction (M01.1)

For `parse_turn_payload`, the model returns a **flat** JSON object with keys  
`answer`, `confidence`, `response_mode`, `drift_detected`.

**Pattern:** `JSON_OBJECT_RE = re.compile(r"\{[^{}]*\}", re.DOTALL)`

**Rationale:** Greedy `\{.*\}` can over-match across multiple JSON objects or prose. The flat pattern matches a single object **without nested `{`/`}` inside the payload**, which matches the LUCID turn schema. Parsing applies to **model output only**, not to long prompt text.

If future payloads need nesting, replace with balanced-brace extraction and document here.

---

## 5. Install method hierarchy (Kaggle)

1. **Pinned GitHub archive ZIP** (preferred):  
   `https://github.com/m-cahill/lucid/archive/<FULL_SHA>.zip`
2. **Uploaded wheel** dataset fallback (see `M01_KAGGLE_RUNBOOK.md`).
3. **`git+https://...`** only if the environment has `git`.

The **generated** install cell must use the **same SHA** as the metadata banner.

### 5.1 Pin SHA vs branch tip (audit coherence)

The banner and `%pip` URL may reference a commit **older than** the branch tip when later commits touch **only** docs, the generator, or notebook JSON — not **`src/lucid/`** or packaging inputs. That is coherent for transport if the installed package is unchanged:

- Verify with `git diff <PIN_SHA>..<BRANCH_TIP> -- src/` (empty diff ⇒ same `lucid` code as tip).
- **Bump the pin** (regenerate with a new `--pin-sha`) whenever **`src/lucid/`** or wheel-relevant metadata changes.

**M01.1 current pin:** `da080cda0760ff742c7e4a69a0a873822049620c`. **Parity check:** `git diff da080cda0760ff742c7e4a69a0a873822049620c..HEAD -- src/` must be empty for the ZIP to match the same `lucid` package as tip (re-run before each Kaggle proof if tip moved).

---

## 6. Pre-submission checklist (notebook readiness)

Before claiming the notebook is ready for a Kaggle proof run:

- [ ] Regenerated with `python scripts/generate_kaggle_notebook.py` using an explicit `--pin-sha <40-char>` (or `auto` at release time), then committed; `python scripts/generate_kaggle_notebook.py --check` passes locally and in CI.
- [ ] Notebook runs top-to-bottom in a Kaggle-like environment (after install).
- [ ] Exactly one `@kbench.task` and one `%choose`.
- [ ] No `schema=` on `llm.prompt`.
- [ ] `lucid_main_task.run(kbench.llm)` succeeds.
- [ ] Task artifact / leaderboard task is produced and selectable in the benchmark UI (platform).
- [ ] First hosted model run succeeds (platform).
- [ ] Evidence recorded (`M01_KAGGLE_EVIDENCE_TEMPLATE.md` or `M01_run1.md`).

**Honesty:** **M01 Kaggle E2E** is not complete until **Kaggle platform proof** exists with evidence — see `docs/lucid.md` proof classes.

---

## 7. Regeneration workflow

1. **After any edit** to `scripts/generate_kaggle_notebook.py`, re-run the generator and commit the updated `.ipynb` so `--check` and CI stay green.
2. **Pin** the banner and `%pip` URL to a **40-character commit SHA** you intend to ship (e.g. `git rev-parse HEAD` at release time). After a commit that changes the generator, you may amend with a freshly regenerated notebook so the pin matches the tree you publish.
3. **`--check` comparison** ignores per-cell `id` fields (Jupyter may add them when you open/save the notebook; the generator does not emit them).

## 8. Related docs

- `docs/milestones/M01/M01_KAGGLE_RUNBOOK.md` — ZIP / wheel / git handoff.
- `docs/lucid.md` — ledger and proof-class rules.
- `scripts/generate_kaggle_notebook.py` — authoritative generator source.
