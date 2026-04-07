"""Verify a git revision contains ``m11_probe_panels.py`` in the committed tree.

Kaggle notebooks install from ``https://github.com/.../archive/<sha>.zip``.
If that commit does not contain ``src/lucid/kaggle/m11_probe_panels.py``, the
preflight cell will show ``MISSING`` — this script catches that **before** upload.

Run from repo root::

    python scripts/verify_m11_git_has_module.py
    python scripts/verify_m11_git_has_module.py --sha <40-char-sha>
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_PATH = "src/lucid/kaggle/m11_probe_panels.py"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--sha",
        default="HEAD",
        help="Git revision to check (default: HEAD). Use a 40-char commit SHA for pins.",
    )
    args = p.parse_args(argv)

    root = Path(__file__).resolve().parents[1]
    ref = args.sha.strip()
    r = subprocess.run(
        ["git", "cat-file", "-e", f"{ref}:{_PATH}"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        print(
            f"ERROR: {_PATH} is not in git at {ref!r}.\n"
            "Kaggle ZIP installs from the committed tree only, not local untracked files. "
            "Commit M11, push, then regenerate notebooks with:\n"
            "  python scripts/generate_m11_kaggle_notebooks.py --write\n",
            file=sys.stderr,
        )
        return 1
    print(f"OK: {ref} contains {_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
