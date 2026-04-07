"""Generate M11 probe Kaggle notebooks (P12 / P24 / P48).

Do not hand-edit ``notebooks/lucid_kaggle_m11_probe_p*.ipynb``. Regenerate with::

    python scripts/generate_m11_kaggle_notebooks.py --write

``--pin-sha`` defaults to ``auto`` (``git rev-parse HEAD``). The embedded SHA must be a
commit that **includes** ``src/lucid/kaggle/m11_probe_panels.py`` in the GitHub archive,
or Kaggle will install an older tree where ``lucid.kaggle.m11_probe_panels`` is missing.

Panel definitions: ``lucid.kaggle.m11_probe_panels`` — nested subsets of the M09 mature panel.

**P72** continues to use ``scripts/generate_m09_kaggle_notebook.py``
(``lucid_m09_mature_evidence_task``).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


def _load_gknb() -> Any:
    p = Path(__file__).resolve().parent / "generate_kaggle_notebook.py"
    spec = importlib.util.spec_from_file_location("generate_kaggle_notebook", p)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _load_m09_nb() -> Any:
    p = Path(__file__).resolve().parent / "generate_m09_kaggle_notebook.py"
    spec = importlib.util.spec_from_file_location("generate_m09_kaggle_notebook", p)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


_gknb = _load_gknb()
_m09 = _load_m09_nb()
_canonical_json = _gknb._canonical_json
_resolve_pin_sha = _gknb._resolve_pin_sha
_strip_cell_ids = _gknb._strip_cell_ids
_md_cell = _gknb._md_cell
_code_cell = _gknb._code_cell
extract_pin_sha_from_notebook = _gknb.extract_pin_sha_from_notebook
_SCORER_CODE = _m09._SCORER_CODE

PROBE_NOTEBOOKS: tuple[tuple[str, str, str, int, str], ...] = (
    (
        "P12",
        "notebooks/lucid_kaggle_m11_probe_p12.ipynb",
        "lucid_m11_probe_p12_task",
        12,
        "lucid_kaggle_m11_probe_p12",
    ),
    (
        "P24",
        "notebooks/lucid_kaggle_m11_probe_p24.ipynb",
        "lucid_m11_probe_p24_task",
        24,
        "lucid_kaggle_m11_probe_p24",
    ),
    (
        "P48",
        "notebooks/lucid_kaggle_m11_probe_p48.ipynb",
        "lucid_m11_probe_p48_task",
        48,
        "lucid_kaggle_m11_probe_p48",
    ),
)


def build_m11_probe_notebook(
    pin_sha: str,
    tier: str,
    out_task: str,
    n_episodes: int,
    slug: str,
) -> dict[str, Any]:
    """Full .ipynb dict — M09-style transport; parameterized probe tier."""
    banner = f"""# LUCID — generated M11 hosted-model probe metadata

| Field | Value |
|------|--------|
| **Repository pin (commit SHA)** | `{pin_sha}` |
| **Benchmark version** | 1.1.0 |
| **Probe tier** | `{tier}` |
| **Panel source** | Nested subset of `m09_mature_evidence_v1` (`lucid.kaggle.m11_probe_panels`) |
| **Episode count** | **{n_episodes}** |
| **Repeat lane** | Same episode IDs as **P12** when `tier=P12` (see M11 plan) |

This notebook is for **Kaggle hosted-model probe** runs. It does **not** change scoring semantics.
"""

    title = f"""# LUCID — M11 probe panel {tier} (Kaggle Benchmarks)

**Task:** `{out_task}`

This notebook evaluates a **deterministic {n_episodes}-episode** panel defined in code
(`lucid.kaggle.m11_probe_panels`), nested inside the M09 mature 72-episode substrate. Same
transport stack as M01/M09: plain-text prompts, JSON parsing via `lucid.kaggle.text_adapter`,
local scoring — **no** `schema=` on `llm.prompt`.
"""

    install_md = """## 1. Install LUCID from GitHub ZIP

Use a **commit-pinned ZIP** so the task is tied to a specific repo state (same SHA as the
metadata banner above).
"""

    install_code = f"""# Commit-pinned GitHub archive ZIP (no git required).
# SHA must match banner cell.
%pip install -q "https://github.com/m-cahill/lucid/archive/{pin_sha}.zip"
"""

    verify_md = """## 2. Preflight — M11 module visibility (after pip install)

If ``lucid.kaggle.m11_probe_panels`` is **MISSING**, the notebook pin SHA does **not** include
M11 in the GitHub archive (stale pin), or packaging is broken — **fix in repo**, regenerate
this notebook, re-upload from file. **Do not** patch imports in the Kaggle UI.
"""

    verify_code = """import importlib.util

for mod in [
    "lucid",
    "lucid.kaggle",
    "lucid.kaggle.m11_probe_panels",
]:
    print(mod, "->", "FOUND" if importlib.util.find_spec(mod) else "MISSING")
"""

    tier_literal = tier
    imports_md = """## 3. Imports, M11 probe panel, and benchmark constants"""

    imports_code = f"""import json
import math
import re
from typing import Any

import kaggle_benchmarks as kbench

from lucid.families.symbolic_negation_v1 import generate_episode as generate_episode_f1
from lucid.families.contradiction_clarification_v1 import generate_episode as generate_episode_f2
from lucid.families.scope_precedence_exception_v1 import generate_episode as generate_episode_f3
from lucid.models import DriftSeverity
from lucid.kaggle.prompts import turn1_user_prompt, turn2_user_prompt
from lucid.kaggle.text_adapter import parse_turn_payload
from lucid.kaggle.m11_probe_panels import m11_probe_eval_rows

M11_PROBE_TIER = "{tier_literal}"
EVAL_ROWS = m11_probe_eval_rows(M11_PROBE_TIER)

print("=== M11 probe panel ===")
print("probe_tier:", M11_PROBE_TIER)
print("benchmark_version:", "1.1.0")
print("panel_episodes:", len(EVAL_ROWS))
print("first unified_episode_id:", EVAL_ROWS[0]["unified_episode_id"])
print("last unified_episode_id:", EVAL_ROWS[-1]["unified_episode_id"])
"""

    adapter_md = """## 4. JSON-only typed response adapter

Uses **`lucid.kaggle.text_adapter.parse_turn_payload`** — same as offline tests; do not fork.
"""

    adapter_code = """# parse_turn_payload imported from lucid.kaggle.text_adapter (§3).
pass
"""

    prompts_md = """## 5. Prompt builders

All three template families use the same two-turn prompt surface (`lucid.kaggle.prompts`) with
`EpisodeSpec` from each family's `generate_episode`.
"""

    prompts_code = """# turn1_user_prompt / turn2_user_prompt from lucid.kaggle.prompts (§3).
pass
"""

    scorer_md = """## 6. Deterministic scorer (profile 1.1.0)

Same episode scalar as M01/M04/M09: `0.40*D + 0.20*(1-L) + 0.15*(1-O) + 0.15*A + 0.10*C`.
"""

    scorer_code = _SCORER_CODE

    runner_md = """## 7. Cross-family episode runner

Dispatches to the correct `generate_episode` by `family_id`, then runs the same two-turn JSON loop
as M01/M09.
"""

    runner_code = """def run_m11_probe_episode(llm: Any, row: dict[str, Any]) -> dict[str, Any]:
    fam = row["family_id"]
    seed = int(row["generation_seed"])
    sev = DriftSeverity[row["difficulty"]]

    if fam == "symbolic_negation_v1":
        spec = generate_episode_f1(seed=seed, drift_severity=sev)
    elif fam == "contradiction_clarification_v1":
        spec = generate_episode_f2(
            seed=seed,
            drift_severity=sev,
            contradiction_state=row["contradiction_state"],
        )
    elif fam == "scope_precedence_exception_v1":
        spec = generate_episode_f3(
            seed=seed,
            drift_severity=sev,
            family_subtype=row["family3_subtype"],
        )
    else:
        raise ValueError(f"unsupported family_id: {fam!r}")

    turn1_raw = llm.prompt(turn1_user_prompt(spec))
    turn1 = parse_turn_payload(turn1_raw, require_answer=False)

    turn2_raw = llm.prompt(turn2_user_prompt(spec))
    turn2 = parse_turn_payload(turn2_raw, require_answer=True)

    turns = {
        spec.drift_onset_turn: turn1,
        spec.final_resolution_turn: turn2,
    }
    score = score_episode_from_turns(spec, turns)

    return {
        "unified_episode_id": row["unified_episode_id"],
        "family_id": fam,
        "generation_seed": seed,
        "difficulty": row["difficulty"],
        "score": score,
    }
"""

    task_md = f"""## 8. Kaggle Benchmark task (M11 probe {tier})

**One** decorated task: `{out_task}` — mean episode score over **{n_episodes}** rows.
"""

    task_code = f"""@kbench.task(
    name="{out_task}",
    description=(
        "LUCID 1.1.0 M11 probe {tier} ({n_episodes} episodes) — nested M09 substrate"
    ),
)
def {out_task}(llm) -> float:
    episode_scores: list[float] = []

    print("=== {out_task} start ===")
    print("rows:", len(EVAL_ROWS))

    for row in EVAL_ROWS:
        result = run_m11_probe_episode(llm=llm, row=row)
        episode_scores.append(float(result["score"]["lucid_score_episode"]))
        print(
            f"id={{result['unified_episode_id']}} "
            f"episode_score={{result['score']['lucid_score_episode']:.6f}}"
        )

    mean_score = sum(episode_scores) / len(episode_scores)
    print("=== {out_task} complete ===")
    print("mean_score =", mean_score)
    return float(mean_score)
"""

    exec_md = """## 9. Execute the task once in the notebook"""

    exec_code = f"""{out_task}.run(kbench.llm)"""

    choose_md = """## 10. Select the M11 probe leaderboard task

This must be the **only** `%choose` cell in this notebook.
"""

    choose_code = f"""%choose {out_task}"""

    cells = [
        _md_cell(banner),
        _md_cell(title),
        _md_cell(install_md),
        _code_cell(install_code),
        _md_cell(verify_md),
        _code_cell(verify_code),
        _md_cell(imports_md),
        _code_cell(imports_code),
        _md_cell(adapter_md),
        _code_cell(adapter_code),
        _md_cell(prompts_md),
        _code_cell(prompts_code),
        _md_cell(scorer_md),
        _code_cell(scorer_code),
        _md_cell(runner_md),
        _code_cell(runner_code),
        _md_cell(task_md),
        _code_cell(task_code),
        _md_cell(exec_md),
        _code_cell(exec_code),
        _md_cell(choose_md),
        _code_cell(choose_code),
    ]

    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.11.0"},
        },
        "cells": cells,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--pin-sha",
        default="auto",
        help='Commit SHA for banner + ZIP install (use "auto" for git rev-parse HEAD)',
    )
    p.add_argument(
        "--write",
        action="store_true",
        help="Write all three M11 probe notebooks",
    )
    p.add_argument(
        "--check",
        action="store_true",
        help="Verify all three notebooks match generator output",
    )
    args = p.parse_args(argv)

    root = Path(__file__).resolve().parents[1]
    pin_sha = _resolve_pin_sha(args.pin_sha)

    if args.write:
        for tier, rel, task, n_ep, _slug in PROBE_NOTEBOOKS:
            out_path = root / rel
            nb = build_m11_probe_notebook(pin_sha, tier, task, n_ep, _slug)
            rendered = _canonical_json(_strip_cell_ids(nb))
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(rendered, encoding="utf-8")
            print(f"Wrote {out_path} (pin_sha={pin_sha})")
        return 0

    if args.check:
        ok = True
        for tier, rel, task, n_ep, _slug in PROBE_NOTEBOOKS:
            out_path = root / rel
            if not out_path.is_file():
                print(f"ERROR: {out_path} missing (run with --write)", file=sys.stderr)
                ok = False
                continue
            extracted = extract_pin_sha_from_notebook(out_path)
            check_pin = extracted if extracted is not None else pin_sha
            rendered_check = _canonical_json(
                _strip_cell_ids(build_m11_probe_notebook(check_pin, tier, task, n_ep, _slug))
            )
            existing_raw = out_path.read_text(encoding="utf-8").replace("\r\n", "\n")
            existing_norm = _canonical_json(_strip_cell_ids(json.loads(existing_raw)))
            if existing_norm != rendered_check:
                print(
                    f"ERROR: {out_path} differs from generator (check_pin={check_pin}).\n"
                    "Run: python scripts/generate_m11_kaggle_notebooks.py "
                    "--pin-sha <40-char-sha> --write",
                    file=sys.stderr,
                )
                ok = False
            else:
                print(f"OK: {out_path} matches generator (check_pin={check_pin})")
        return 0 if ok else 1

    p.print_help()
    print("Specify --write or --check", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
