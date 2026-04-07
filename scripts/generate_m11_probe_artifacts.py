"""Write or verify committed M11 probe ladder + canonical roster artifacts.

    python scripts/generate_m11_probe_artifacts.py --write
    python scripts/generate_m11_probe_artifacts.py --check

Ladder JSON is derived from ``lucid.kaggle.m11_probe_panels``. Roster JSON is derived from
``docs/milestones/M09/artifacts/m09_model_scores.csv`` (33 unique slugs; duplicates flagged),
then **operator exclusions** are applied so two slugs remain listed but ``tracked: false``.
M11 historically started from a 33-model canonical roster; the active decision surface for
P12/P24 is **31** tracked models after exclusions.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

# Operator exclusions: still listed for audit, but excluded from tracked roster / allocation.
# Evidence recovered post-retry; now grounded in exact failure payloads.
_OPERATOR_EXCLUSIONS: dict[str, dict[str, str]] = {
    "deepseek-r1-0528": {
        "exclusion_reason": "surface_compatibility_failure",
        "failure_reason_code": "json_parse_failure_reasoning_wrapper",
        "failure_detail": (
            "Model emits <think>...</think> reasoning trace before JSON. "
            "Text adapter raises ValueError: Confidence is not numeric: None. "
            "Structured-output / parser-compatibility failure; model reachable, "
            "benchmark task valid, parse failed before score."
        ),
    },
    "gpt-oss-120b": {
        "exclusion_reason": "surface_compatibility_failure",
        "failure_reason_code": "json_parse_failure_truncated_output",
        "failure_detail": (
            "Model initially returns valid JSON but later emits truncated "
            "malformed JSON. Raises ValueError: No JSON object found in model "
            "output. Structured-output / surface-compatibility failure; model "
            "reachable, benchmark task valid, parse failed before score."
        ),
    },
}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _ladder_path(root: Path) -> Path:
    return root / "docs/milestones/M11/artifacts/m11_probe_ladder.json"


def _roster_path(root: Path) -> Path:
    return root / "docs/milestones/M11/artifacts/m11_roster_canonical.json"


def _render_ladder_json() -> str:
    from lucid.kaggle.m11_probe_panels import build_m11_probe_ladder_artifact_dict

    payload: dict[str, Any] = build_m11_probe_ladder_artifact_dict()
    return json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def _render_roster_json(root: Path) -> str:
    csv_path = root / "docs/milestones/M09/artifacts/m09_model_scores.csv"
    if not csv_path.is_file():
        msg = f"Missing M09 scores CSV: {csv_path}"
        raise FileNotFoundError(msg)

    seen: set[str] = set()
    models: list[dict[str, Any]] = []
    with csv_path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            slug = (row.get("model_slug") or "").strip()
            if not slug:
                continue
            if slug in seen:
                models.append(
                    {
                        "model_slug": slug,
                        "tracked": False,
                        "source": "m09_model_scores_normalized",
                        "exclusion_reason": "duplicate_row_after_first_occurrence",
                    }
                )
                continue
            seen.add(slug)
            models.append(
                {
                    "model_slug": slug,
                    "tracked": True,
                    "source": "m09_model_scores_normalized",
                    "exclusion_reason": None,
                }
            )

    for m in models:
        slug = str(m["model_slug"])
        if slug in _OPERATOR_EXCLUSIONS:
            excl = _OPERATOR_EXCLUSIONS[slug]
            m["tracked"] = False
            m["exclusion_reason"] = excl["exclusion_reason"]
            m["failure_reason_code"] = excl["failure_reason_code"]
            m["failure_detail"] = excl["failure_detail"]

    tracked = [m for m in models if m["tracked"]]
    payload = {
        "roster_id": "m11_canonical_roster_v1",
        "source_artifact": "docs/milestones/M09/artifacts/m09_model_scores.csv",
        "canonical_tracked_count": len(tracked),
        "notes": (
            "Authoritative M11 roster lists 33 unique model_slug values from normalized M09 "
            "ingest (one row per slug). M11 originally used a 33-model canonical roster; "
            "after exclusions the active tracked roster for P12/P24 is 31 models. "
            "Two models (deepseek-r1-0528, gpt-oss-120b) are excluded with "
            "surface_compatibility_failure: exact failure evidence was recovered from P12 "
            "runs showing structured-output / parser-compatibility issues on the current "
            "strict evaluation surface. M11 intentionally does not modify the parser or "
            "prompt to rescue these runs; they remain excluded to preserve comparability."
        ),
        "models": models,
    }
    return json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--write", action="store_true", help="Write artifacts from code / M09 CSV")
    g.add_argument("--check", action="store_true", help="Require on-disk artifacts to match")
    args = p.parse_args(argv)

    root = _repo_root()
    ladder_p = _ladder_path(root)
    roster_p = _roster_path(root)

    ladder_rendered = _render_ladder_json()
    roster_rendered = _render_roster_json(root)

    if args.write:
        ladder_p.parent.mkdir(parents=True, exist_ok=True)
        ladder_p.write_text(ladder_rendered, encoding="utf-8", newline="\n")
        roster_p.write_text(roster_rendered, encoding="utf-8", newline="\n")
        print(f"Wrote {ladder_p}")
        print(f"Wrote {roster_p}")
        return 0

    if args.check:
        ok = True
        for path, rendered, label in (
            (ladder_p, ladder_rendered, "m11_probe_ladder"),
            (roster_p, roster_rendered, "m11_roster_canonical"),
        ):
            if not path.is_file():
                print(f"ERROR: {path} missing (run with --write)", file=sys.stderr)
                ok = False
                continue
            existing = path.read_text(encoding="utf-8").replace("\r\n", "\n")
            if existing != rendered:
                print(
                    f"ERROR: {path} differs from generator ({label}).\n"
                    f"Run: python scripts/generate_m11_probe_artifacts.py --write",
                    file=sys.stderr,
                )
                ok = False
            else:
                print(f"OK: {path} matches generator ({label})")
        return 0 if ok else 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
