"""Write or verify the committed M09 panel JSON artifact.

The canonical panel is defined in ``lucid.kaggle.m09_evidence_panel`` (reproducible from code).

    python scripts/generate_m09_panel_artifact.py --write
    python scripts/generate_m09_panel_artifact.py --check
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _artifact_path(repo_root: Path) -> Path:
    return repo_root / "docs/milestones/M09/artifacts/m09_model_panel.json"


def _render_artifact() -> str:
    from lucid.kaggle.m09_evidence_panel import build_m09_panel_artifact_dict

    payload: dict[str, Any] = build_m09_panel_artifact_dict()
    return json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--write", action="store_true", help="Write artifact from code")
    g.add_argument("--check", action="store_true", help="Require on-disk artifact to match code")
    args = p.parse_args(argv)

    root = Path(__file__).resolve().parents[1]
    path = _artifact_path(root)
    rendered = _render_artifact()

    if args.write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8", newline="\n")
        print(f"Wrote {path}")
        return 0

    if args.check:
        if not path.is_file():
            print(f"ERROR: {path} missing (run with --write)", file=sys.stderr)
            return 2
        existing = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        if existing != rendered:
            print(
                f"ERROR: {path} differs from generator.\n"
                f"Run: python scripts/generate_m09_panel_artifact.py --write",
                file=sys.stderr,
            )
            return 1
        print(f"OK: {path} matches m09_evidence_panel")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
