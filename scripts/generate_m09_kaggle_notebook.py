"""Generate the M09 mature-benchmark Kaggle evidence notebook (cross-family).

Do not hand-edit ``notebooks/lucid_kaggle_m09_mature_evidence.ipynb``.
Regenerate with::

    python scripts/generate_m09_kaggle_notebook.py --pin-sha $(git rev-parse HEAD)

Panel definition: ``lucid.kaggle.m09_evidence_panel`` — task name ``lucid_m09_mature_evidence_task``.

This notebook is **not** a claim of final competition submission readiness; it is **hosted-model
evidence** on the deterministic M09 panel (see ``docs/milestones/M09/``).
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


_gknb = _load_gknb()
_canonical_json = _gknb._canonical_json
_resolve_pin_sha = _gknb._resolve_pin_sha
_strip_cell_ids = _gknb._strip_cell_ids
_md_cell = _gknb._md_cell
_code_cell = _gknb._code_cell
extract_pin_sha_from_notebook = _gknb.extract_pin_sha_from_notebook

# Scorer: identical scalar to M01/M04 (profile 1.1.0) — copied from generate_kaggle_notebook.py
_SCORER_CODE = """def _final_success(spec: Any, turn: dict[str, Any]) -> bool:
    return (
        turn["response_mode"] == "ANSWER"
        and turn["answer"] == spec.expected_outputs["final_correct_item_id"]
    )


def _target_confidence(spec: Any, turn_number: int, turn: dict[str, Any]) -> float:
    is_final = turn_number == spec.final_resolution_turn
    if not is_final:
        return float(spec.uncertainty_ceiling)

    if turn["response_mode"] in {"ABSTAIN", "CLARIFY"}:
        return float(spec.uncertainty_ceiling)

    if turn["response_mode"] == "ANSWER" and _final_success(spec, turn):
        return 1.0

    return float(spec.final_calibration_epsilon)


def _calibrated(spec: Any, turn_number: int, turn: dict[str, Any]) -> bool:
    if turn_number not in set(spec.calibration_eligible_turns):
        return False

    is_final = turn_number == spec.final_resolution_turn
    acceptable_modes = set(spec.acceptable_final_modes)

    if not is_final:
        return float(turn["confidence"]) <= float(spec.uncertainty_ceiling)

    if turn["response_mode"] not in acceptable_modes:
        return False

    if turn["response_mode"] in {"ABSTAIN", "CLARIFY"}:
        return float(turn["confidence"]) <= float(spec.uncertainty_ceiling)

    if _final_success(spec, turn):
        return float(turn["confidence"]) >= 1.0 - float(spec.final_calibration_epsilon)

    return float(turn["confidence"]) <= float(spec.final_calibration_epsilon)


def _abstention_utility(spec: Any, turns_by_number: dict[int, dict[str, Any]]) -> float:
    final_turn = turns_by_number[spec.final_resolution_turn]
    uncertainty_ceiling = float(spec.uncertainty_ceiling)
    epsilon = float(spec.final_calibration_epsilon)

    guarded_earlier = False
    for t in sorted(turns_by_number):
        if t == spec.final_resolution_turn:
            continue
        turn = turns_by_number[t]
        if (
            turn["response_mode"] in {"ABSTAIN", "CLARIFY"}
            or float(turn["confidence"]) <= uncertainty_ceiling
        ):
            guarded_earlier = True
            break

    if getattr(spec, "final_state_unresolved", False):
        if final_turn["response_mode"] in {"ABSTAIN", "CLARIFY"} and float(final_turn["confidence"]) <= uncertainty_ceiling:
            return 1.0
        if final_turn["response_mode"] == "ANSWER" and float(final_turn["confidence"]) <= uncertainty_ceiling:
            return 0.5
        return 0.0

    if _final_success(spec, final_turn) and guarded_earlier:
        return 1.0
    if _final_success(spec, final_turn) and not guarded_earlier:
        return 0.75
    if (
        final_turn["response_mode"] == "ANSWER"
        and not _final_success(spec, final_turn)
        and float(final_turn["confidence"]) <= epsilon
    ):
        return 0.25
    return 0.0


def score_episode_from_turns(spec: Any, turns_by_number: dict[int, dict[str, Any]]) -> dict[str, Any]:
    detection_turns = list(spec.detection_eligible_turns)
    t_first_detect = None
    for t in detection_turns:
        turn = turns_by_number.get(t)
        if turn and turn["drift_detected"] in {"SUSPECTED", "CONFIRMED"}:
            t_first_detect = t
            break
    D = 1.0 if t_first_detect is not None else 0.0

    t_drift = int(spec.drift_onset_turn)
    t_final = int(spec.final_resolution_turn)

    t_calibrated = None
    for t in sorted(spec.calibration_eligible_turns):
        turn = turns_by_number.get(t)
        if turn and _calibrated(spec, t, turn):
            t_calibrated = t
            break
    if t_calibrated is None:
        t_calibrated = t_final
    L = (t_calibrated - t_drift) / max(1, t_final - t_drift)

    overhangs = []
    for t in sorted(spec.scored_post_drift_turns):
        turn = turns_by_number.get(t)
        if not turn:
            continue
        target = _target_confidence(spec, t, turn)
        overhangs.append(max(0.0, float(turn["confidence"]) - target))
    O = sum(overhangs) / len(overhangs) if overhangs else 0.0

    A = _abstention_utility(spec, turns_by_number)

    final_turn = turns_by_number[t_final]
    C = 1.0 if _final_success(spec, final_turn) else 0.0

    lucid_score_episode = (
        0.40 * D
        + 0.20 * (1.0 - L)
        + 0.15 * (1.0 - O)
        + 0.15 * A
        + 0.10 * C
    )

    return {
        "D": float(D),
        "L": float(L),
        "O": float(O),
        "A": float(A),
        "C": float(C),
        "lucid_score_episode": float(lucid_score_episode),
        "t_first_detect": t_first_detect,
        "t_calibrated": t_calibrated,
    }
"""


def build_m09_notebook(pin_sha: str) -> dict[str, Any]:
    """Full .ipynb dict — dedicated cell pipeline (not M01/M04 index overrides)."""
    banner = f"""# LUCID — generated M09 mature-benchmark evidence metadata

| Field | Value |
|------|--------|
| **Repository pin (commit SHA)** | `{pin_sha}` |
| **Benchmark version** | 1.1.0 |
| **Panel ID** | `m09_mature_evidence_v1` |
| **Unified substrate** | `unified_core_m07_v1` |
| **Panel size** | **72** episodes (24 + 24 + 24 across Families 1–3) |
| **Selector** | `lucid.kaggle.m09_evidence_panel` |

This notebook is for **Kaggle hosted-model evidence** on the M09 panel. It is **not** the M01 transport proof and **not** a final submission package alone.
"""

    title = """# LUCID — M09 mature benchmark evidence (Kaggle Benchmarks)

**Task:** `lucid_m09_mature_evidence_task`

This notebook evaluates a **deterministic 72-episode panel** defined in code (`lucid.kaggle.m09_evidence_panel`):

- **Family 1:** exact **M04 decision** continuity (24 rows)
- **Family 2:** balanced **unresolved / resolved** per difficulty (24 rows)
- **Family 3:** balanced **scope / precedence / exception** with fixed allocation (24 rows)

Same transport stack as M01/M04: plain-text prompts, JSON parsing via `lucid.kaggle.text_adapter`, local scoring — **no** `schema=` on `llm.prompt`.
"""

    install_md = """## 1. Install LUCID from GitHub ZIP

Use a **commit-pinned ZIP** so the task is tied to a specific repo state (same SHA as the metadata banner above).
"""

    install_code = f"""# Commit-pinned GitHub archive ZIP (no git required). SHA must match banner cell.
%pip install -q "https://github.com/m-cahill/lucid/archive/{pin_sha}.zip"
"""

    verify_md = """## 2. Verify installation and module resolution"""

    verify_code = """import sys
import importlib.util
import pathlib
import pkgutil

print("=== Python / pip context ===")
print("Python executable:", sys.executable)
print("Python version:", sys.version.split()[0])

print("\\n=== Module resolution ===")
for name in ["lucid", "lucid.kaggle", "lucid.kaggle.m09_evidence_panel"]:
    spec = importlib.util.find_spec(name)
    print(f"{name}: {'FOUND' if spec else 'MISSING'}")
    if spec is not None:
        print("  origin:", spec.origin)

try:
    import lucid
    print("lucid imported from:", pathlib.Path(lucid.__file__).resolve())
    print("lucid submodules:", sorted([m.name for m in pkgutil.iter_modules(lucid.__path__)]))
except Exception as e:
    print("lucid import failed:", repr(e))

ok = importlib.util.find_spec("lucid.kaggle.m09_evidence_panel") is not None
print("\\nINSTALL_OK =", ok)
"""

    imports_md = """## 3. Imports, M09 panel, and benchmark constants"""

    imports_code = """import json
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
from lucid.kaggle.m09_evidence_panel import M09_PANEL_ID, m09_eval_rows

EVAL_ROWS = m09_eval_rows()

print("=== M09 mature evidence panel ===")
print("panel_id:", M09_PANEL_ID)
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

    prompts_code = """# turn1_user_prompt / turn2_user_prompt imported from lucid.kaggle.prompts (§3).
pass
"""

    scorer_md = """## 6. Deterministic scorer (profile 1.1.0)

Same episode scalar as M01/M04: `0.40*D + 0.20*(1-L) + 0.15*(1-O) + 0.15*A + 0.10*C`.
"""

    scorer_code = _SCORER_CODE

    runner_md = """## 7. Cross-family episode runner

Dispatches to the correct `generate_episode` by `family_id`, then runs the same two-turn JSON loop
as M01.
"""

    runner_code = """def run_m09_episode(llm: Any, row: dict[str, Any]) -> dict[str, Any]:
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

    task_md = """## 8. Kaggle Benchmark task (M09)

**One** decorated task: `lucid_m09_mature_evidence_task` — mean episode score over **72** rows.
"""

    task_code = """@kbench.task(
    name="lucid_m09_mature_evidence_task",
    description=(
        "LUCID 1.1.0 M09 mature evidence panel (72 episodes) — unified_core_m07_v1 slice"
    ),
)
def lucid_m09_mature_evidence_task(llm) -> float:
    episode_scores: list[float] = []

    print("=== lucid_m09_mature_evidence_task start ===")
    print("rows:", len(EVAL_ROWS))

    for row in EVAL_ROWS:
        result = run_m09_episode(llm=llm, row=row)
        episode_scores.append(float(result["score"]["lucid_score_episode"]))
        print(
            f"id={result['unified_episode_id']} "
            f"episode_score={result['score']['lucid_score_episode']:.6f}"
        )

    mean_score = sum(episode_scores) / len(episode_scores)
    print("=== lucid_m09_mature_evidence_task complete ===")
    print("mean_score =", mean_score)
    return float(mean_score)
"""

    exec_md = """## 9. Execute the task once in the notebook"""

    exec_code = """lucid_m09_mature_evidence_task.run(kbench.llm)"""

    choose_md = """## 10. Select the M09 leaderboard task

This must be the **only** `%choose` cell in this notebook.
"""

    choose_code = """%choose lucid_m09_mature_evidence_task"""

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
        "-o",
        "--output",
        type=Path,
        default=Path("notebooks/lucid_kaggle_m09_mature_evidence.ipynb"),
        help="Output .ipynb path",
    )
    p.add_argument(
        "--check",
        action="store_true",
        help="Regenerate with resolved --pin-sha and require output to match exactly",
    )
    args = p.parse_args(argv)

    root = Path(__file__).resolve().parents[1]
    pin_sha = _resolve_pin_sha(args.pin_sha)
    out_path = args.output if args.output.is_absolute() else root / args.output

    if args.check:
        if not out_path.is_file():
            print(f"ERROR: {out_path} missing (run without --check to create)", file=sys.stderr)
            return 2
        extracted = extract_pin_sha_from_notebook(out_path)
        check_pin = extracted if extracted is not None else pin_sha
        rendered_check = _canonical_json(_strip_cell_ids(build_m09_notebook(check_pin)))
        existing_raw = out_path.read_text(encoding="utf-8").replace("\r\n", "\n")
        existing_norm = _canonical_json(_strip_cell_ids(json.loads(existing_raw)))
        if existing_norm != rendered_check:
            print(
                f"ERROR: {out_path} differs from generator output (check_pin={check_pin}).\n"
                f"Run: python scripts/generate_m09_kaggle_notebook.py --pin-sha <40-char-sha> -o {args.output}",
                file=sys.stderr,
            )
            return 1
        print(f"OK: {out_path} matches generator (check_pin={check_pin})")
        return 0

    rendered = _canonical_json(build_m09_notebook(pin_sha))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered, encoding="utf-8")
    print(f"Wrote {out_path} (pin_sha={pin_sha})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
