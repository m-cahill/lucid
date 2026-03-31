"""Fail if the built wheel does not ship `lucid.kaggle` (packaging regression guard).

Run after `python -m build --wheel` with `dist/*.whl` present.
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path


def _find_latest_wheel(dist_dir: Path) -> Path:
    wheels = sorted(dist_dir.glob("*.whl"), key=lambda p: p.stat().st_mtime)
    if not wheels:
        msg = f"No .whl files under {dist_dir}; run: python -m build --wheel"
        raise FileNotFoundError(msg)
    return wheels[-1]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--dist",
        type=Path,
        default=Path("dist"),
        help="Directory containing built wheels (default: ./dist)",
    )
    args = p.parse_args(argv)

    wheel = _find_latest_wheel(args.dist)
    required = "lucid/kaggle/episode_llm.py"
    with zipfile.ZipFile(wheel) as zf:
        names = zf.namelist()
    ok = any(n.replace("\\", "/").endswith(required) for n in names)
    if not ok:
        print(
            f"ERROR: {required} not found in {wheel.name}.\n"
            f"Submodules of `lucid` must ship in the wheel. Files:\n" + "\n".join(sorted(names)),
            file=sys.stderr,
        )
        return 1
    print(f"OK: {required} present in {wheel.name} ({len(names)} wheel members)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
