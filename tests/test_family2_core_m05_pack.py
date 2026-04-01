"""Family 2 M05 canonical pack — manifest, determinism, balance, metadata."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from lucid.canonical_json import dumps_canonical
from lucid.families.contradiction_clarification_v1 import generate_episode
from lucid.models import DriftSeverity
from lucid.packs import family2_core_m05 as p
from lucid.runner_family2 import fixture_turns_family2, run_family2_smoke
from lucid.scorer import score_episode

_REPO = Path(__file__).resolve().parents[1]
_MANIFEST = _REPO / p.CANONICAL_MANIFEST_RELPATH
_SCRIPT = _REPO / "scripts" / "generate_family2_core_m05_manifest.py"

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
        "final_state_unresolved",
        "acceptable_final_modes",
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
    assert data["episode_count"] == 72
    assert data["difficulty_distribution"] == {"LOW": 24, "MEDIUM": 24, "HIGH": 24}
    eps = data["episodes"]
    assert len(eps) == 72
    buckets = [e["difficulty_bucket"] for e in eps]
    assert buckets.count("LOW") == 24
    assert buckets.count("MEDIUM") == 24
    assert buckets.count("HIGH") == 24


def test_contradiction_state_balance_per_bucket() -> None:
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    for bucket in ("LOW", "MEDIUM", "HIGH"):
        sub = [e for e in data["episodes"] if e["difficulty_bucket"] == bucket]
        assert len(sub) == 24
        u = [e for e in sub if e["contradiction_state"] == "unresolved"]
        r = [e for e in sub if e["contradiction_state"] == "resolved"]
        assert len(u) == 12
        assert len(r) == 12


def test_episode_ids_unique() -> None:
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    ids = [e["episode_spec"]["episode_id"] for e in data["episodes"]]
    assert len(ids) == len(set(ids))


def test_no_duplicate_logical_episodes() -> None:
    """Same (seed, bucket, contradiction_state) must not appear twice."""
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    keys = [
        (
            e["seed"],
            e["difficulty_bucket"],
            e["contradiction_state"],
        )
        for e in data["episodes"]
    ]
    assert len(keys) == len(set(keys))


def test_required_metadata_on_every_episode() -> None:
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    for row in data["episodes"]:
        spec = row["episode_spec"]
        missing = _REQUIRED_EPISODE_SPEC_KEYS - spec.keys()
        assert not missing, missing
        assert spec["drift_event"]["drift_type"] == "CONTRADICTION"
        assert row["difficulty_bucket"] == spec["difficulty_profile"]["drift_severity"]
        assert row["target_behavior"] == spec["difficulty_profile"]["target_behavior"]
        assert row["drift_type"] == "CONTRADICTION"
        assert row["pack_id"] == p.PACK_ID
        assert row["family_id"] == p.FAMILY_ID
        assert row["clarifier_present"] == (row["contradiction_state"] == "resolved")
        assert row["final_state_unresolved"] == (row["contradiction_state"] == "unresolved")
        if row["contradiction_state"] == "unresolved":
            assert spec["final_state_unresolved"] is True
            assert spec["expected_outputs"].get("final_correct_item_id") is None
            assert set(spec["acceptable_final_modes"]) == {"ABSTAIN", "ANSWER", "CLARIFY"}
        else:
            assert spec["final_state_unresolved"] is False
            assert spec["expected_outputs"]["final_correct_item_id"] is not None
            assert spec["acceptable_final_modes"] == ["ANSWER"]


def test_family2_pack_smoke_subset(tmp_path: Path) -> None:
    """Six representative episodes — generate → score → bundle."""
    scores: list[float] = []
    for seed, sev, cstate in p.smoke_subset_triples():
        bundle, s = run_family2_smoke(
            seed=seed,
            out_root=tmp_path,
            drift_severity=sev,
            contradiction_state=cstate,
        )
        assert bundle.is_dir()
        assert (bundle / "episode_spec.json").is_file()
        scores.append(s)
    assert all(0.0 <= x <= 1.0 for x in scores)


def test_manifest_episode_scorer_regression() -> None:
    """Each manifest episode is compatible with fixture_turns_family2 + score_episode."""
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    for row in data["episodes"]:
        seed = int(row["episode_spec"]["generation_seed"])
        sev = DriftSeverity[row["difficulty_bucket"]]
        st = row["contradiction_state"]
        spec = generate_episode(seed=seed, drift_severity=sev, contradiction_state=st)
        assert spec.episode_id == row["episode_spec"]["episode_id"]
        turns = fixture_turns_family2(spec)
        score_episode(spec, turns)


def test_generate_episode_determinism() -> None:
    a = generate_episode(
        seed=42, drift_severity=DriftSeverity.MEDIUM, contradiction_state="unresolved"
    )
    b = generate_episode(
        seed=42, drift_severity=DriftSeverity.MEDIUM, contradiction_state="unresolved"
    )
    assert a.episode_id == b.episode_id
    assert a.prompt_preamble == b.prompt_preamble


def test_unresolved_vs_resolved_episode_ids_differ() -> None:
    u = generate_episode(seed=1, drift_severity=DriftSeverity.LOW, contradiction_state="unresolved")
    r = generate_episode(seed=1, drift_severity=DriftSeverity.LOW, contradiction_state="resolved")
    assert u.episode_id != r.episode_id
