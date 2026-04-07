"""Write or verify committed M11 probe ladder + canonical roster artifacts.

    python scripts/generate_m11_probe_artifacts.py --write
    python scripts/generate_m11_probe_artifacts.py --check

Ladder JSON is derived from ``lucid.kaggle.m11_probe_panels``. Roster JSON is derived from
``docs/milestones/M09/artifacts/m09_model_scores.csv`` (33 tracked models; duplicates flagged).
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


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

    tracked = [m for m in models if m["tracked"]]
    payload = {
        "roster_id": "m11_canonical_roster_v1",
        "source_artifact": "docs/milestones/M09/artifacts/m09_model_scores.csv",
        "canonical_tracked_count": len(tracked),
        "notes": (
            "Authoritative M11 tracked roster = 33 model_slug values from normalized M09 ingest "
            "(one row per slug). Raw platform exports may carry duplicate or stray rows; "
            "duplicates after first occurrence are listed with tracked=false."
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
