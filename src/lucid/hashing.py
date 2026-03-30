"""SHA-256 helpers for bundle manifests."""

from __future__ import annotations

import hashlib
from pathlib import Path


def sha256_file(path: str | Path) -> str:
    """Hex digest of file contents."""
    p = Path(path)
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()
