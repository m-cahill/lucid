"""Canonical JSON for LUCID artifacts (UTF-8, sorted keys, no NaN)."""

from __future__ import annotations

import json
from typing import Any


def dumps_canonical(obj: Any) -> str:
    """Serialize to a canonical string for hashing and stable bundles."""
    return json.dumps(
        obj,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    )


def write_canonical(path: str, obj: Any) -> None:
    """Write JSON with LF newlines."""
    from pathlib import Path

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    text = dumps_canonical(obj) + "\n"
    p.write_text(text, encoding="utf-8", newline="\n")
