"""Fail if the built wheel does not ship `lucid.kaggle` (packaging regression guard).

Also requires ``m11_probe_panels.py`` so Kaggle M11 probe installs cannot silently omit M11.

Run after `python -m build --wheel` with ``dist/*.whl`` present.
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
    required_paths = (
        "lucid/kaggle/episode_llm.py",
        "lucid/kaggle/m11_probe_panels.py",
    )
    with zipfile.ZipFile(wheel) as zf:
        names = zf.namelist()
    normalized = [n.replace("\\", "/") for n in names]
    missing = [req for req in required_paths if not any(n.endswith(req) for n in normalized)]
    if missing:
        print(
            f"ERROR: required wheel members missing: {missing}\n"
            f"Wheel: {wheel.name}. Submodules of `lucid` must ship in full.\n"
            f"Members (sample): " + "\n".join(sorted(names)[:40]),
            file=sys.stderr,
        )
        return 1
    print(f"OK: kaggle + M11 probe modules present in {wheel.name} ({len(names)} wheel members)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
