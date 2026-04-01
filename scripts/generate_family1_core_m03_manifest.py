#!/usr/bin/env python3
"""Write or verify the committed Family 1 M03 canonical pack manifest."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_ROOT / "src"))

from lucid.canonical_json import dumps_canonical, write_canonical  # noqa: E402
from lucid.packs.family1_core_m03 import (  # noqa: E402
    build_manifest_dict,
    canonical_manifest_path,
)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    p = argparse.ArgumentParser(description="Family 1 M03 pack manifest — write or check")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument(
        "--write",
        action="store_true",
        help="Regenerate and write the canonical manifest (LF, sorted keys).",
    )
    g.add_argument(
        "--check",
        action="store_true",
        help="Fail if committed manifest does not match deterministic regeneration.",
    )
    p.add_argument(
        "--repo-root",
        type=Path,
        default=_ROOT,
        help="Repository root (default: parent of scripts/).",
    )
    args = p.parse_args()
    out_path = canonical_manifest_path(args.repo_root)
    built = build_manifest_dict()

    if args.write:
        write_canonical(str(out_path), built)
        print(f"wrote {out_path}")
        return

    if not out_path.is_file():
        msg = f"missing manifest: {out_path}"
        raise SystemExit(msg)
    on_disk = _load_json(out_path)
    if dumps_canonical(on_disk) != dumps_canonical(built):
        msg = (
            f"manifest drift: {out_path}\n"
            "Regenerate with: python scripts/generate_family1_core_m03_manifest.py --write"
        )
        raise SystemExit(msg)
    print(f"ok {out_path}")


if __name__ == "__main__":
    main()
