"""M12 submission linkage generator (scripts/generate_m12_submission_linkage.py)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from generate_m12_submission_linkage import (  # noqa: E402
    build_linkage_payload,
)


def test_build_linkage_payload_has_schema() -> None:
    p = build_linkage_payload(ROOT)
    assert p.get("schema_version") == "m12_submission_linkage_v1"
    assert "linkage" in p
    assert p["linkage"].get("benchmark_version") == "1.1.0"
    slug = "michael1232/lucid-kaggle-community-benchmarks"
    assert p["linkage"].get("kaggle_benchmark_slug") == slug
