"""Family 3 M06 canonical pack — manifest, determinism, balance, metadata."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from lucid.canonical_json import dumps_canonical
from lucid.families.scope_precedence_exception_v1 import generate_episode
from lucid.models import DriftSeverity
from lucid.packs import family3_core_m06 as p
from lucid.runner_family3 import fixture_turns_family3, run_family3_smoke
from lucid.scorer import score_episode

_REPO = Path(__file__).resolve().parents[1]
_MANIFEST = _REPO / p.CANONICAL_MANIFEST_RELPATH
_SCRIPT = _REPO / "scripts" / "generate_family3_core_m06_manifest.py"

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


def test_drift_subtype_balance_per_bucket() -> None:
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    for bucket in ("LOW", "MEDIUM", "HIGH"):
        sub = [e for e in data["episodes"] if e["difficulty_bucket"] == bucket]
        assert len(sub) == 24
        sc = [e for e in sub if e["family3_subtype"] == "scope"]
        pr = [e for e in sub if e["family3_subtype"] == "precedence"]
        ex = [e for e in sub if e["family3_subtype"] == "exception"]
        assert len(sc) == 8
        assert len(pr) == 8
        assert len(ex) == 8


def test_drift_type_counts_match_enum() -> None:
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    assert data["drift_type_distribution"] == {"SCOPE": 24, "PRECEDENCE": 24, "EXCEPTION": 24}
    for row in data["episodes"]:
        dt = row["drift_type"]
        fs = row["family3_subtype"]
        if fs == "scope":
            assert dt == "SCOPE"
        elif fs == "precedence":
            assert dt == "PRECEDENCE"
        else:
            assert dt == "EXCEPTION"


def test_episode_ids_unique() -> None:
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    ids = [e["episode_spec"]["episode_id"] for e in data["episodes"]]
    assert len(ids) == len(set(ids))


def test_no_duplicate_logical_episodes() -> None:
    """Same (seed, bucket, family3_subtype) must not appear twice."""
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    keys = [
        (
            e["seed"],
            e["difficulty_bucket"],
            e["family3_subtype"],
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
        assert spec["drift_event"]["drift_type"] == row["drift_type"]
        assert row["difficulty_bucket"] == spec["difficulty_profile"]["drift_severity"]
        assert row["target_behavior"] == spec["difficulty_profile"]["target_behavior"]
        assert row["pack_id"] == p.PACK_ID
        assert row["family_id"] == p.FAMILY_ID
        assert row["final_state_unresolved"] is False
        assert spec["final_state_unresolved"] is False
        assert spec["expected_outputs"]["final_correct_item_id"] is not None
        assert spec["acceptable_final_modes"] == ["ANSWER"]
        fst = row["family3_subtype"]
        assert fst in ("scope", "precedence", "exception")
        if fst == "scope":
            assert row.get("scope_before") == "ALL"
            assert row.get("scope_after")
        elif fst == "precedence":
            assert row.get("precedence_before") == "A_over_B"
            assert row.get("precedence_after") == "B_over_A"
            assert row.get("rule_count") == 2
        else:
            assert row.get("general_rule")
            assert row.get("exception_class") is not None
            assert row.get("exception_trigger") == "excluded_item_ids"


def test_family3_pack_smoke_subset(tmp_path: Path) -> None:
    """Nine representative episodes — generate → score → bundle."""
    scores: list[float] = []
    for seed, sev, fst in p.smoke_subset_triples():
        bundle, s = run_family3_smoke(
            seed=seed,
            out_root=tmp_path,
            drift_severity=sev,
            family_subtype=fst,
        )
        assert bundle.is_dir()
        assert (bundle / "episode_spec.json").is_file()
        scores.append(s)
    assert all(0.0 <= x <= 1.0 for x in scores)


def test_manifest_episode_scorer_regression() -> None:
    """Each manifest episode is compatible with fixture_turns_family3 + score_episode."""
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    for row in data["episodes"]:
        seed = int(row["episode_spec"]["generation_seed"])
        sev = DriftSeverity[row["difficulty_bucket"]]
        fst = row["family3_subtype"]
        assert fst in ("scope", "precedence", "exception")
        spec = generate_episode(seed=seed, drift_severity=sev, family_subtype=fst)
        assert spec.episode_id == row["episode_spec"]["episode_id"]
        turns = fixture_turns_family3(spec)
        score_episode(spec, turns)


def test_generate_episode_determinism() -> None:
    a = generate_episode(seed=42, drift_severity=DriftSeverity.MEDIUM, family_subtype="scope")
    b = generate_episode(seed=42, drift_severity=DriftSeverity.MEDIUM, family_subtype="scope")
    assert a.episode_id == b.episode_id
    assert a.prompt_preamble == b.prompt_preamble


def test_subtype_same_seed_different_episode_ids() -> None:
    s_scope = generate_episode(seed=1, drift_severity=DriftSeverity.LOW, family_subtype="scope")
    s_prec = generate_episode(seed=1, drift_severity=DriftSeverity.LOW, family_subtype="precedence")
    assert s_scope.episode_id != s_prec.episode_id
