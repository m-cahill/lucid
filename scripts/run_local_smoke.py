#!/usr/bin/env python3
"""Local smoke runner (M00 minimal green path)."""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running without installation (repo root)
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT / "src"))

from lucid.runner import main  # noqa: E402

if __name__ == "__main__":
    main()
