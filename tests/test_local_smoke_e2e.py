"""End-to-end local smoke: bundle on disk, deterministic score."""

from __future__ import annotations

import json
from pathlib import Path

from lucid.runner import run_smoke


def test_e2e_smoke_writes_bundle(tmp_path: Path) -> None:
    out = tmp_path / "out"
    bundle, score = run_smoke(seed=42, out_root=out)
    assert bundle.is_dir()
    assert (bundle / "episode_spec.json").is_file()
    assert (bundle / "episode_result.json").is_file()
    assert (bundle / "bundle_manifest.json").is_file()
    assert (bundle / "hashes.json").is_file()
    spec = json.loads((bundle / "episode_spec.json").read_text(encoding="utf-8"))
    result = json.loads((bundle / "episode_result.json").read_text(encoding="utf-8"))
    assert spec["episode_id"] == result["episode_id"]
    assert "LUCID_SCORE_EPISODE" in result["scores"]
    assert 0.0 <= score <= 1.0


def test_e2e_deterministic(tmp_path: Path) -> None:
    a = tmp_path / "a"
    b = tmp_path / "b"
    ba, sa = run_smoke(seed=7, out_root=a)
    bb, sb = run_smoke(seed=7, out_root=b)
    assert sa == sb
    assert (ba / "hashes.json").read_text(encoding="utf-8") == (bb / "hashes.json").read_text(
        encoding="utf-8"
    )
