"""Smoke tests for analytics script (load via importlib — no subprocess)."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from lucid.families.symbolic_negation_v1 import generate_episode
from lucid.models import DriftSeverity
from lucid.packs import family1_core_m03 as p
from lucid.runner import fixture_turns
from lucid.scorer import score_episode

_REPO = Path(__file__).resolve().parents[1]
_MANIFEST = _REPO / p.CANONICAL_MANIFEST_RELPATH
_SCRIPT = _REPO / "scripts" / "analyze_family1_core_m03.py"


def _load_analyze_module() -> object:
    spec = importlib.util.spec_from_file_location("analyze_family1_core_m03", _SCRIPT)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_analyze_structural_no_duplicates() -> None:
    mod = _load_analyze_module()
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    structural = mod.analyze_structural(data)
    assert structural["duplicate_episode_ids"] == []
    assert structural["buckets"]["LOW"]["uniform_within_bucket"] is True


def test_deterministic_baseline_full_pack_matches_fixture() -> None:
    mod = _load_analyze_module()
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    rows = mod.deterministic_baseline_rows(data)
    assert len(rows) == 96
    first = rows[0]
    spec = generate_episode(
        seed=int(first["generation_seed"]),
        drift_severity=DriftSeverity[str(first["difficulty_bucket"])],
    )
    turns = fixture_turns(spec)
    s = score_episode(spec, turns)
    assert abs(float(first["lucid_score_episode"]) - float(s.lucid_score_episode)) < 1e-9
