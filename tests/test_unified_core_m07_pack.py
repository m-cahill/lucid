"""M07 unified pack — manifest, lineage, determinism, normalization, smoke."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from lucid.canonical_json import dumps_canonical
from lucid.families.contradiction_clarification_v1 import generate_episode as gen_f2
from lucid.families.scope_precedence_exception_v1 import generate_episode as gen_f3
from lucid.families.symbolic_negation_v1 import generate_episode as gen_f1
from lucid.models import DriftSeverity
from lucid.packs import family1_core_m03 as p1
from lucid.packs import family2_core_m05 as p2
from lucid.packs import family3_core_m06 as p3
from lucid.packs.unified_core_m07 import (
    NORMALIZATION_VERSION,
    PACK_ID,
    build_manifest_dict,
    build_normalized_episodes,
    build_pack_stats_dict,
    canonical_manifest_path,
    episode_spec_hash,
    unified_smoke_unified_episode_ids,
)
from lucid.runner import fixture_turns as fixture_turns_f1
from lucid.runner_family2 import fixture_turns_family2
from lucid.runner_family3 import fixture_turns_family3
from lucid.runner_unified import run_unified_episode_smoke
from lucid.scorer import score_episode

_REPO = Path(__file__).resolve().parents[1]
_MANIFEST = _REPO / "tests/fixtures/unified_core_m07/unified_core_m07_manifest.json"
_SCRIPT = _REPO / "scripts/generate_unified_core_m07_manifest.py"


def test_manifest_file_matches_regeneration() -> None:
    on_disk = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    built = build_manifest_dict()
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
    assert data["episode_count"] == 240
    assert data["difficulty_distribution"] == {"HIGH": 80, "LOW": 80, "MEDIUM": 80}
    assert len(data["episodes"]) == 240


def test_family_composition() -> None:
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    assert data["family_distribution"] == {
        "symbolic_negation_v1": 96,
        "contradiction_clarification_v1": 72,
        "scope_precedence_exception_v1": 72,
    }


def test_expected_drift_and_variant_distributions() -> None:
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    assert data["drift_type_distribution"] == {
        "NEGATION": 96,
        "CONTRADICTION": 72,
        "SCOPE": 24,
        "PRECEDENCE": 24,
        "EXCEPTION": 24,
    }
    assert data["family_variant_distribution"] == {
        "negation": 96,
        "unresolved": 36,
        "resolved": 36,
        "scope": 24,
        "precedence": 24,
        "exception": 24,
    }
    assert data["final_state_resolution_counts"] == {"unresolved": 36, "resolved": 204}


def test_episode_spec_bytes_match_source_manifests() -> None:
    """Unified ``episode_spec`` is semantically identical to the source row (canonical JSON)."""
    unified = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    unified_by = {
        (e["source_pack_id"], e["source_episode_id"]): e["episode_spec"]
        for e in unified["episodes"]
    }
    sources: list[tuple[str, Path]] = [
        (p1.PACK_ID, _REPO / p1.CANONICAL_MANIFEST_RELPATH),
        (p2.PACK_ID, _REPO / p2.CANONICAL_MANIFEST_RELPATH),
        (p3.PACK_ID, _REPO / p3.CANONICAL_MANIFEST_RELPATH),
    ]
    for pack_id, path in sources:
        man = json.loads(path.read_text(encoding="utf-8"))
        for row in man["episodes"]:
            sid = str(row["episode_spec"]["episode_id"])
            u_spec = unified_by[(pack_id, sid)]
            assert dumps_canonical(u_spec) == dumps_canonical(row["episode_spec"])


def test_source_episodes_preserved_exactly_once() -> None:
    """Every source episode from the three canonical packs appears exactly once."""
    m1 = json.loads((_REPO / p1.CANONICAL_MANIFEST_RELPATH).read_text(encoding="utf-8"))
    m2 = json.loads((_REPO / p2.CANONICAL_MANIFEST_RELPATH).read_text(encoding="utf-8"))
    m3 = json.loads((_REPO / p3.CANONICAL_MANIFEST_RELPATH).read_text(encoding="utf-8"))
    expected: set[tuple[str, str]] = set()
    for row in m1["episodes"]:
        expected.add((p1.PACK_ID, str(row["episode_spec"]["episode_id"])))
    for row in m2["episodes"]:
        expected.add((p2.PACK_ID, str(row["episode_spec"]["episode_id"])))
    for row in m3["episodes"]:
        expected.add((p3.PACK_ID, str(row["episode_spec"]["episode_id"])))
    assert len(expected) == 240

    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    got: set[tuple[str, str]] = set()
    for row in data["episodes"]:
        got.add((row["source_pack_id"], row["source_episode_id"]))
    assert got == expected


def test_source_episode_spec_hash_matches_canonical_spec() -> None:
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    for row in data["episodes"]:
        spec = row["episode_spec"]
        assert row["source_episode_spec_hash"] == episode_spec_hash(spec)


def test_unified_episode_id_format() -> None:
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    for row in data["episodes"]:
        uid = row["unified_episode_id"]
        sp = row["source_pack_id"]
        se = row["source_episode_id"]
        assert uid == f"u_{sp}__{se}"


def test_unified_ids_unique() -> None:
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    ids = [e["unified_episode_id"] for e in data["episodes"]]
    assert len(ids) == len(set(ids))


def test_ordering_difficulty_then_family() -> None:
    """Per difficulty bucket: Family 1 block, then 2, then 3 — each in source order."""
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    ueps = data["episodes"]
    f1 = json.loads((_REPO / p1.CANONICAL_MANIFEST_RELPATH).read_text(encoding="utf-8"))
    f2 = json.loads((_REPO / p2.CANONICAL_MANIFEST_RELPATH).read_text(encoding="utf-8"))
    f3 = json.loads((_REPO / p3.CANONICAL_MANIFEST_RELPATH).read_text(encoding="utf-8"))

    off = 0
    for bucket in ("LOW", "MEDIUM", "HIGH"):
        exp_f1 = [
            r["episode_spec"]["episode_id"]
            for r in f1["episodes"]
            if r["difficulty_bucket"] == bucket
        ]
        exp_f2 = [
            r["episode_spec"]["episode_id"]
            for r in f2["episodes"]
            if r["difficulty_bucket"] == bucket
        ]
        exp_f3 = [
            r["episode_spec"]["episode_id"]
            for r in f3["episodes"]
            if r["difficulty_bucket"] == bucket
        ]
        n = len(exp_f1) + len(exp_f2) + len(exp_f3)
        block = ueps[off : off + n]
        got_f1 = [r["source_episode_id"] for r in block if r["source_pack_id"] == p1.PACK_ID]
        got_f2 = [r["source_episode_id"] for r in block if r["source_pack_id"] == p2.PACK_ID]
        got_f3 = [r["source_episode_id"] for r in block if r["source_pack_id"] == p3.PACK_ID]
        assert got_f1 == exp_f1
        assert got_f2 == exp_f2
        assert got_f3 == exp_f3
        off += n
    assert off == 240


def test_normalization_version_constant() -> None:
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    assert data["normalization_version"] == NORMALIZATION_VERSION == "1.0.0"
    for row in data["episodes"]:
        assert row["normalization_version"] == "1.0.0"


def test_pack_stats_json_matches_build() -> None:
    stats_path = _REPO / "docs/milestones/M07/artifacts/unified_pack_stats.json"
    on_disk = json.loads(stats_path.read_text(encoding="utf-8"))
    assert on_disk == build_pack_stats_dict()


def test_unified_smoke_panel_coverage() -> None:
    ids = unified_smoke_unified_episode_ids()
    assert len(ids) == 9
    assert len(set(ids)) == 9
    by_id = {e["unified_episode_id"]: e for e in build_normalized_episodes()}
    fams = {by_id[i]["family_id"] for i in ids}
    assert fams == {
        "symbolic_negation_v1",
        "contradiction_clarification_v1",
        "scope_precedence_exception_v1",
    }
    rows = [by_id[i] for i in ids]
    assert {r["difficulty"] for r in rows} == {"LOW", "MEDIUM", "HIGH"}
    f2_rows = [r for r in rows if r["source_pack_id"] == p2.PACK_ID]
    assert {r["family_variant"] for r in f2_rows} == {"unresolved", "resolved"}
    f3_rows = [r for r in rows if r["source_pack_id"] == p3.PACK_ID]
    assert {r["family_variant"] for r in f3_rows} == {"scope", "precedence", "exception"}


def test_unified_smoke_runs(tmp_path: Path) -> None:
    for uid in unified_smoke_unified_episode_ids():
        row = next(e for e in build_normalized_episodes() if e["unified_episode_id"] == uid)
        bundle, s = run_unified_episode_smoke(unified_row=row, out_root=tmp_path)
        assert bundle.is_dir()
        assert 0.0 <= s <= 1.0


def test_manifest_episode_scorer_regression() -> None:
    """Each unified row regenerates the same EpisodeSpec identity as the source pack."""
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    for row in data["episodes"]:
        spec_d = row["episode_spec"]
        fam = spec_d["template_family"]
        seed = int(spec_d["generation_seed"])
        sev = DriftSeverity[str(spec_d["difficulty_profile"]["drift_severity"])]
        if fam == "symbolic_negation_v1":
            spec = gen_f1(seed=seed, drift_severity=sev)
            turns = fixture_turns_f1(spec)
        elif fam == "contradiction_clarification_v1":
            st = spec_d["difficulty_profile"]["contradiction_state"]
            spec = gen_f2(
                seed=seed,
                drift_severity=sev,
                contradiction_state="resolved" if st == "resolved" else "unresolved",
            )
            turns = fixture_turns_family2(spec)
        else:
            fst = spec_d["difficulty_profile"]["family3_subtype"]
            assert fst in ("scope", "precedence", "exception")
            spec = gen_f3(seed=seed, drift_severity=sev, family_subtype=fst)
            turns = fixture_turns_family3(spec)
        assert spec.episode_id == spec_d["episode_id"]
        score_episode(spec, turns)


def test_canonical_manifest_path() -> None:
    assert canonical_manifest_path(_REPO) == _MANIFEST


def test_pack_id() -> None:
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    assert data["pack_id"] == PACK_ID == "unified_core_m07_v1"
