"""Family 1 M03 canonical pack — manifest, determinism, transport parity."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from lucid.canonical_json import dumps_canonical
from lucid.families.symbolic_negation_v1 import generate_episode
from lucid.kaggle.transport import load_transport_fixtures, verify_fixture_against_local
from lucid.models import DriftSeverity
from lucid.packs import family1_core_m03 as p
from lucid.runner import fixture_turns, run_smoke
from lucid.scorer import score_episode

_REPO = Path(__file__).resolve().parents[1]
_MANIFEST = _REPO / p.CANONICAL_MANIFEST_RELPATH
_SCRIPT = _REPO / "scripts" / "generate_family1_core_m03_manifest.py"
_TRANSPORT_MANIFEST = _REPO / "tests/fixtures/kaggle_transport/transport_manifest.json"

_REQUIRED_EPISODE_SPEC_KEYS = frozenset(
    {
        "episode_id",
        "generation_seed",
        "template_family",
        "template_version",
        "benchmark_version",
        "scoring_profile_version",
        "difficulty_profile",
        "drift_event",
        "pre_drift_rule",
        "post_drift_rule",
        "expected_outputs",
    }
)


def test_manifest_file_matches_regeneration() -> None:
    on_disk = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    built = p.build_manifest_dict()
    assert dumps_canonical(on_disk) == dumps_canonical(built)


def test_manifest_script_check_exits_zero() -> None:
    r = subprocess.run(
        [sys.executable, str(_SCRIPT), "--check"],
        cwd=_REPO,
        check=False,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr


def test_pack_size_and_difficulty_balance() -> None:
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    assert data["episode_count"] == 96
    assert data["difficulty_distribution"] == {"LOW": 32, "MEDIUM": 32, "HIGH": 32}
    eps = data["episodes"]
    assert len(eps) == 96
    buckets = [e["difficulty_bucket"] for e in eps]
    assert buckets.count("LOW") == 32
    assert buckets.count("MEDIUM") == 32
    assert buckets.count("HIGH") == 32


def test_episode_ids_unique() -> None:
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    ids = [e["episode_spec"]["episode_id"] for e in data["episodes"]]
    assert len(ids) == len(set(ids))


def test_required_metadata_on_every_episode() -> None:
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    for row in data["episodes"]:
        spec = row["episode_spec"]
        missing = _REQUIRED_EPISODE_SPEC_KEYS - spec.keys()
        assert not missing, missing
        assert spec["drift_event"]["drift_type"] == "NEGATION"
        assert "final_correct_item_id" in spec["expected_outputs"]
        assert row["difficulty_bucket"] == spec["difficulty_profile"]["drift_severity"]


def test_m01_acceptance_episode_ids_in_pack() -> None:
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    ids = {e["episode_spec"]["episode_id"] for e in data["episodes"]}
    m01 = data["m01_acceptance_subset"]["episode_ids"]
    assert set(m01) <= ids
    assert len(m01) == 3


def test_m01_transport_fixture_ids_tagged() -> None:
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    tagged = {
        e["m01_transport_fixture_id"] for e in data["episodes"] if e.get("m01_transport_fixture_id")
    }
    assert tagged == {"symneg_100_low", "symneg_42_medium", "symneg_200_high"}


def test_m01_rows_match_transport_manifest() -> None:
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    by_id = {e["episode_spec"]["episode_id"]: e["episode_spec"] for e in data["episodes"]}
    fixtures = load_transport_fixtures(_TRANSPORT_MANIFEST)
    for fx in fixtures:
        spec = by_id[fx.episode_id]
        assert spec["generation_seed"] == fx.generation_seed
        assert spec["drift_event"]["drift_severity"] == fx.drift_severity.value


def test_scorer_transport_subset() -> None:
    """Reference turns score matches M01 manifest for all three fixtures."""
    fixtures = load_transport_fixtures(_TRANSPORT_MANIFEST)
    for fx in fixtures:
        got = verify_fixture_against_local(fx).lucid_score_episode
        assert got == fx.expected.lucid_score_episode


def test_family1_pack_smoke_subset(tmp_path: Path) -> None:
    """One LOW / one MEDIUM / one HIGH — generate → score → bundle."""
    triples = (
        (100, DriftSeverity.LOW),
        (42, DriftSeverity.MEDIUM),
        (200, DriftSeverity.HIGH),
    )
    scores: list[float] = []
    for seed, sev in triples:
        bundle, s = run_smoke(seed=seed, out_root=tmp_path, drift_severity=sev)
        assert bundle.is_dir()
        assert (bundle / "episode_spec.json").is_file()
        scores.append(s)
    assert all(0.0 <= x <= 1.0 for x in scores)


def test_manifest_episode_scorer_regression() -> None:
    """Each manifest episode is compatible with fixture_turns + score_episode."""
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    for row in data["episodes"]:
        seed = int(row["episode_spec"]["generation_seed"])
        sev = DriftSeverity[row["difficulty_bucket"]]
        spec = generate_episode(seed=seed, drift_severity=sev)
        assert spec.episode_id == row["episode_spec"]["episode_id"]
        turns = fixture_turns(spec)
        score_episode(spec, turns)
