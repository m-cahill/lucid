"""Authoritative generator for the canonical Kaggle transport notebook (M01.1+).

Do not hand-edit ``notebooks/lucid_kaggle_transport_text_adapter_m_01.ipynb``.
Regenerate with::

    python scripts/generate_kaggle_notebook.py --pin-sha $(git rev-parse HEAD)

See ``docs/kaggle/LUCID_KAGGLE_NOTEBOOK_CONTRACT.md``.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

_PIN_RE = re.compile(r"`([0-9a-f]{40})`")


def extract_pin_sha_from_notebook(path: Path) -> str | None:
    """Read the metadata banner and return the 40-char hex pin if present."""
    data = json.loads(path.read_text(encoding="utf-8"))
    for cell in data.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        src = "".join(cell.get("source", []))
        m = _PIN_RE.search(src)
        if m:
            return m.group(1)
    return None


def _resolve_pin_sha(arg: str) -> str:
    if arg != "auto":
        return arg
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=Path(__file__).resolve().parents[1],
            check=True,
            capture_output=True,
            text=True,
        )
        return out.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def _source_lines(text: str) -> list[str]:
    if not text:
        return ["\n"]
    lines = text.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    return lines


def _md_cell(text: str) -> dict[str, Any]:
    return {"cell_type": "markdown", "metadata": {}, "source": _source_lines(text)}


def _code_cell(text: str) -> dict[str, Any]:
    return {
        "cell_type": "code",
        "metadata": {},
        "source": _source_lines(text),
        "execution_count": None,
        "outputs": [],
    }


def build_cells(pin_sha: str) -> list[dict[str, Any]]:
    """Return ordered notebook cells per LUCID_KAGGLE_NOTEBOOK_CONTRACT.md."""
    banner = f"""# LUCID — generated transport metadata (M01.1)

| Field | Value |
|------|--------|
| **Repository pin (commit SHA)** | `{pin_sha}` |
| **Benchmark version** | 1.1.0 |
| **Template family** | symbolic_negation_v1 |
| **Scoring profile** | 1.1.0 |
| **M01 acceptance slice** | `(100, LOW)`, `(42, MEDIUM)`, `(200, HIGH)` |

This cell is for **audit / evidence** only. Regenerate the notebook after changing transport code; keep the pin aligned with the commit you ship to Kaggle.
"""

    title = """# LUCID — Kaggle Community Benchmarks transport (M01)

This notebook is a **Kaggle transport adapter** for the locked **LUCID 1.1.0** line.

It keeps the benchmark family and scoring profile fixed, but adapts the **LLM interaction layer** for Kaggle Benchmarks by using:

1. **plain-text LLM prompts**
2. **strict JSON-only typed response parsing**
3. **local deterministic scoring in-notebook**

## Notebook shape

- **one** Kaggle Benchmark task: `lucid_main_task`
- fixed three-episode acceptance slice:
  - `(100, LOW)`
  - `(42, MEDIUM)`
  - `(200, HIGH)`

## Important note

This notebook is designed to work around Kaggle's structured-schema prompt limitations while preserving a **typed scoring boundary** through strict JSON parsing in the notebook itself.
"""

    install_md = """## 1. Install LUCID from GitHub ZIP

Use a **commit-pinned ZIP** so the task is tied to a specific repo state (same SHA as the metadata banner above).
"""

    install_code = f"""# Commit-pinned GitHub archive ZIP (no git required). SHA must match banner cell.
%pip install -q "https://github.com/m-cahill/lucid/archive/{pin_sha}.zip"
"""

    verify_md = """## 2. Verify installation and module resolution

This section prints enough context to debug shadowing / packaging issues without changing benchmark behavior.
"""

    verify_code = """import sys
import importlib
import importlib.util
import pathlib
import pkgutil

print("=== Python / pip context ===")
print("Python executable:", sys.executable)
print("Python version:", sys.version.split()[0])
print("First sys.path entries:")
for i, p in enumerate(sys.path[:10]):
    print(f"  [{i}] {p}")

print("\\n=== Distribution metadata ===")
try:
    import importlib.metadata as md
    dist = md.distribution("lucid-benchmark")
    print("lucid-benchmark version:", dist.version)
    print("Distribution location:", dist.locate_file(""))
except Exception as e:
    print("Could not read distribution metadata for lucid-benchmark:", repr(e))

print("\\n=== Module resolution ===")
for name in ["lucid", "lucid.kaggle", "lucid.kaggle.episode_llm"]:
    spec = importlib.util.find_spec(name)
    print(f"{name}: {'FOUND' if spec else 'MISSING'}")
    if spec is not None:
        print("  origin:", spec.origin)

print("\\n=== Import test ===")
try:
    import lucid
    print("lucid imported from:", pathlib.Path(lucid.__file__).resolve())
    print("lucid submodules:", sorted([m.name for m in pkgutil.iter_modules(lucid.__path__)]))
except Exception as e:
    print("lucid import failed:", repr(e))

try:
    mod = importlib.import_module("lucid.kaggle")
    print("lucid.kaggle import: OK")
    print("lucid.kaggle path:", pathlib.Path(mod.__file__).resolve())
except Exception as e:
    print("lucid.kaggle import failed:", repr(e))

print("\\n=== Success criteria ===")
ok = (
    importlib.util.find_spec("lucid") is not None
    and importlib.util.find_spec("lucid.kaggle") is not None
)
print("INSTALL_OK =", ok)
"""

    imports_md = """## 3. Imports and benchmark constants"""

    imports_code = """import json
import math
import re
from typing import Any

import kaggle_benchmarks as kbench

from lucid.families.symbolic_negation_v1 import generate_episode
from lucid.models import DriftSeverity

# Fixed acceptance slice for M01 transport proof.
EVAL_ROWS = [
    {"generation_seed": 100, "drift_severity": "LOW"},
    {"generation_seed": 42, "drift_severity": "MEDIUM"},
    {"generation_seed": 200, "drift_severity": "HIGH"},
]

print("=== M01 proof context ===")
print("distribution:", "lucid-benchmark")
print("benchmark_version:", "1.1.0")
print("template_family:", "symbolic_negation_v1")
print("template_version:", "1.0.0")
print("scoring_profile_version:", "1.1.0")
print("fixture_slice:", [(r["generation_seed"], r["drift_severity"]) for r in EVAL_ROWS])
"""

    adapter_md = """## 4. JSON-only typed response adapter

Kaggle Benchmarks currently handles plain text prompts more reliably than schema-bound response formats.

So this notebook asks the model for **JSON text only**, then:

- extracts the first JSON object from the response
- validates the required fields
- normalizes enums and confidence
- produces a typed dict for scoring

This keeps the scorer independent from free-form prose.
"""

    adapter_code = """ALLOWED_RESPONSE_MODES = {"ANSWER", "ABSTAIN", "CLARIFY"}
ALLOWED_DRIFT_DETECTED = {"NONE", "SUSPECTED", "CONFIRMED"}

# Flat object only (model turn payload). Safer than greedy \\{.*\\}; see docs/kaggle/LUCID_KAGGLE_NOTEBOOK_CONTRACT.md §4.
JSON_OBJECT_RE = re.compile(r"\\{[^{}]*\\}", re.DOTALL)


def _strip_code_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\\s*", "", text)
        text = re.sub(r"\\s*```$", "", text)
    return text.strip()


def _extract_first_json_object(text: str) -> str:
    cleaned = _strip_code_fences(text)
    match = JSON_OBJECT_RE.search(cleaned)
    if not match:
        raise ValueError(f"No JSON object found in model output: {cleaned[:300]!r}")
    return match.group(0)


def _normalize_confidence(value: Any) -> float:
    try:
        x = float(value)
    except Exception as exc:
        raise ValueError(f"Confidence is not numeric: {value!r}") from exc
    if math.isnan(x) or math.isinf(x):
        raise ValueError(f"Confidence must be finite: {value!r}")
    return max(0.0, min(1.0, x))


def _normalize_answer(value: Any) -> str | None:
    if value is None:
        return None
    value = str(value).strip()
    return value if value else None


def _normalize_enum(value: Any, allowed: set[str], field_name: str) -> str:
    val = str(value).strip().upper()
    if val not in allowed:
        raise ValueError(f"{field_name} must be one of {sorted(allowed)}, got {value!r}")
    return val


def parse_turn_payload(raw_text: str) -> dict[str, Any]:
    obj = json.loads(_extract_first_json_object(raw_text))
    if not isinstance(obj, dict):
        raise ValueError("Parsed payload must be a JSON object")

    payload = {
        "answer": _normalize_answer(obj.get("answer")),
        "confidence": _normalize_confidence(obj.get("confidence")),
        "response_mode": _normalize_enum(
            obj.get("response_mode", "ANSWER"),
            ALLOWED_RESPONSE_MODES,
            "response_mode",
        ),
        "drift_detected": _normalize_enum(
            obj.get("drift_detected", "NONE"),
            ALLOWED_DRIFT_DETECTED,
            "drift_detected",
        ),
    }

    if payload["response_mode"] == "ANSWER" and payload["answer"] is None:
        raise ValueError("response_mode=ANSWER requires non-null answer")

    return payload
"""

    prompts_md = """## 5. Prompt builders

The family is the canonical starter family:

- `symbolic_negation_v1`
- explicit `NEGATION` drift
- two scored turns:
  - turn 1 = drift response window
  - turn 2 = final resolution

The prompts below keep that structure explicit.
"""

    prompts_code = '''def _items_block(spec: Any) -> str:
    lines = []
    for item in spec.items:
        lines.append(json.dumps(item, sort_keys=True))
    return "\\n".join(lines)


def turn1_user_prompt(spec: Any) -> str:
    return f"""
You are evaluating a synthetic rule-world benchmark episode.

CURRENT PHASE: DRIFT_RESPONSE_WINDOW
This is NOT the final answer turn.

Items:
{_items_block(spec)}

Pre-drift rule:
{json.dumps(spec.pre_drift_rule, sort_keys=True)}

Drift event:
{json.dumps({
    "drift_type": spec.drift_event.drift_type.value if hasattr(spec.drift_event.drift_type, "value") else str(spec.drift_event.drift_type),
    "drift_severity": spec.drift_event.drift_severity.value if hasattr(spec.drift_event.drift_severity, "value") else str(spec.drift_event.drift_severity),
    "drift_onset_turn": spec.drift_event.drift_onset_turn,
    "drift_parameters": spec.drift_event.drift_parameters,
}, sort_keys=True)}

Post-drift rule:
{json.dumps(spec.post_drift_rule, sort_keys=True)}

You are in the ambiguity / calibration window.
Do NOT provide the final item choice yet unless absolutely necessary.
Return JSON ONLY with this exact schema:

{{
  "answer": null,
  "confidence": <float in [0,1]>,
  "response_mode": "ANSWER" | "ABSTAIN" | "CLARIFY",
  "drift_detected": "NONE" | "SUSPECTED" | "CONFIRMED"
}}

Guidance:
- If you are uncertain after the rule change, lower confidence.
- If you choose ANSWER here, it may still be provisional.
- Output JSON only. No prose.
""".strip()


def turn2_user_prompt(spec: Any) -> str:
    return f"""
Continue the same episode.

CURRENT PHASE: FINAL_RESOLUTION
You must now provide the final typed response.

Items:
{_items_block(spec)}

Post-drift rule:
{json.dumps(spec.post_drift_rule, sort_keys=True)}

Valid item ids:
{json.dumps([item["id"] for item in spec.items])}

Return JSON ONLY with this exact schema:

{{
  "answer": "<item_id>" | null,
  "confidence": <float in [0,1]>,
  "response_mode": "ANSWER" | "ABSTAIN" | "CLARIFY",
  "drift_detected": "NONE" | "SUSPECTED" | "CONFIRMED"
}}

Important:
- Final resolution for this family normally expects an ANSWER.
- If response_mode is ANSWER, answer must be one of the valid item ids.
- Output JSON only. No prose.
""".strip()
'''

    scorer_md = """## 6. Deterministic scorer (profile 1.1.0)

This reproduces the official episode-level scalar:

- `D` = drift detection
- `L` = calibration lag
- `O` = confidence overhang
- `A` = abstention utility
- `C` = post-drift correctness

The scalar is:

`0.40*D + 0.20*(1-L) + 0.15*(1-O) + 0.15*A + 0.10*C`
"""

    scorer_code = """def _final_success(spec: Any, turn: dict[str, Any]) -> bool:
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

    runner_md = """## 7. Episode runner

This runs a single LUCID episode end-to-end against the Kaggle `llm` object:

- deterministic episode generation
- two JSON-only prompts
- strict local parse
- deterministic scoring
"""

    runner_code = """def run_lucid_episode(llm: Any, generation_seed: int, drift_severity: str, debug: bool = False) -> dict[str, Any]:
    sev = DriftSeverity[drift_severity]
    spec = generate_episode(seed=int(generation_seed), drift_severity=sev)

    turn1_raw = llm.prompt(turn1_user_prompt(spec))
    turn1 = parse_turn_payload(turn1_raw)

    turn2_raw = llm.prompt(turn2_user_prompt(spec))
    turn2 = parse_turn_payload(turn2_raw)

    turns = {
        spec.drift_onset_turn: turn1,
        spec.final_resolution_turn: turn2,
    }
    score = score_episode_from_turns(spec, turns)

    if debug:
        print("=" * 80)
        print("EPISODE:", spec.episode_id)
        print("SEED / SEVERITY:", generation_seed, drift_severity)
        print("EXPECTED FINAL ITEM:", spec.expected_outputs["final_correct_item_id"])
        print("TURN 1 RAW:", turn1_raw)
        print("TURN 1 PARSED:", json.dumps(turn1, indent=2, sort_keys=True))
        print("TURN 2 RAW:", turn2_raw)
        print("TURN 2 PARSED:", json.dumps(turn2, indent=2, sort_keys=True))
        print("SCORE:", json.dumps(score, indent=2, sort_keys=True))

    return {
        "episode_id": spec.episode_id,
        "generation_seed": int(generation_seed),
        "drift_severity": drift_severity,
        "expected_final_item_id": spec.expected_outputs["final_correct_item_id"],
        "turn_1": turn1,
        "turn_2": turn2,
        "score": score,
    }
"""

    optional_md = """## 8. Optional local smoke debug cell

This cell is **optional** and should be run only when you want a single interactive debug pass.
It is safe to leave in the notebook, but not required for publishing.

Uncomment the last line if you want a one-episode debug printout.
"""

    optional_code = """# Example interactive smoke run after install succeeds:
# debug_result = run_lucid_episode(kbench.llm, generation_seed=100, drift_severity="LOW", debug=True)
# print(json.dumps(debug_result, indent=2, sort_keys=True))
"""

    task_md = """## 9. Kaggle Benchmark task

Only **one** task is decorated here. Helper functions remain plain Python.

The task loops over the fixed three-row M01 acceptance slice and returns the mean episode score.
"""

    task_code = """@kbench.task(
    name="lucid_main_task",
    description="LUCID 1.1.0 symbolic_negation_v1 transport task for Kaggle Benchmarks",
)
def lucid_main_task(llm) -> float:
    episode_scores: list[float] = []

    print("=== lucid_main_task start ===")
    print("Rows:", EVAL_ROWS)

    for row in EVAL_ROWS:
        result = run_lucid_episode(
            llm=llm,
            generation_seed=row["generation_seed"],
            drift_severity=row["drift_severity"],
            debug=True,
        )
        episode_scores.append(float(result["score"]["lucid_score_episode"]))
        print(
            f"row=({row['generation_seed']}, {row['drift_severity']}) "
            f"episode_score={result['score']['lucid_score_episode']:.6f}"
        )

    mean_score = sum(episode_scores) / len(episode_scores)
    print("=== lucid_main_task complete ===")
    print("mean_score =", mean_score)
    return float(mean_score)
"""

    exec_md = """## 10. Execute the task once in the notebook

Kaggle's benchmark flow expects the task to be executable in the notebook itself before publishing.
"""

    exec_code = """lucid_main_task.run(kbench.llm)"""

    choose_md = """## 11. Select the single leaderboard task

This must be the **only** `%choose` cell in the notebook.
"""

    choose_code = """%choose lucid_main_task"""

    seq = [
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
        _md_cell(optional_md),
        _code_cell(optional_code),
        _md_cell(task_md),
        _code_cell(task_code),
        _md_cell(exec_md),
        _code_cell(exec_code),
        _md_cell(choose_md),
        _code_cell(choose_code),
    ]
    return seq


def build_notebook(pin_sha: str) -> dict[str, Any]:
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
        "cells": build_cells(pin_sha),
    }


def _canonical_json(nb: dict[str, Any]) -> str:
    return json.dumps(nb, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


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
        default=Path("notebooks/lucid_kaggle_transport_text_adapter_m_01.ipynb"),
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
        rendered_check = _canonical_json(build_notebook(check_pin))
        existing = out_path.read_text(encoding="utf-8")
        if existing != rendered_check:
            print(
                f"ERROR: {out_path} differs from generator output (check_pin={check_pin}).\n"
                f"Run: python scripts/generate_kaggle_notebook.py --pin-sha <40-char-sha> -o {args.output}",
                file=sys.stderr,
            )
            return 1
        print(f"OK: {out_path} matches generator (check_pin={check_pin})")
        return 0

    rendered = _canonical_json(build_notebook(pin_sha))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered, encoding="utf-8")
    print(f"Wrote {out_path} (pin_sha={pin_sha})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
