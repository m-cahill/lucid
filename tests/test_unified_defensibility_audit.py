"""M08 unified defensibility audit — determinism, lineage, duplicates, allowlist."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from lucid.audits.defensibility import (
    allowlist_covers_duplicate_group,
    extract_audit_text,
    prompt_skeleton,
    run_defensibility_audit,
)
from lucid.canonical_json import dumps_canonical
from lucid.packs.unified_core_m07 import episode_spec_hash

_REPO = Path(__file__).resolve().parents[1]
_MANIFEST = _REPO / "tests/fixtures/unified_core_m07/unified_core_m07_manifest.json"
_SCRIPT = _REPO / "scripts/run_unified_defensibility_audit.py"
_ART = _REPO / "docs/milestones/M08/artifacts"


def test_defensibility_audit_passes_committed_unified_manifest() -> None:
    r = run_defensibility_audit(
        repo_root=_REPO,
        unified_manifest_path=_MANIFEST,
        allowlist_path=_ART / "m08_exact_duplicate_allowlist.json",
    )
    assert r["passed"] is True
    assert r["counts"]["episodes"] == 240
    assert r["counts"]["hard_failure_count"] == 0


def test_defensibility_audit_deterministic_json() -> None:
    a = run_defensibility_audit(repo_root=_REPO, unified_manifest_path=_MANIFEST)
    b = run_defensibility_audit(repo_root=_REPO, unified_manifest_path=_MANIFEST)
    assert dumps_canonical(a) == dumps_canonical(b)


def test_lineage_accounts_all_source_episodes() -> None:
    r = run_defensibility_audit(repo_root=_REPO, unified_manifest_path=_MANIFEST)
    codes = {h["code"] for h in r["hard_failures"]}
    assert "H_MISSING_SOURCE_EPISODES" not in codes
    assert "H_EXTRA_LINEAGE_KEYS" not in codes


def test_exact_duplicate_groups_are_singletons_without_allowlist() -> None:
    r = run_defensibility_audit(repo_root=_REPO, unified_manifest_path=_MANIFEST)
    multi = [
        g
        for g in r["duplicate_scan"]["exact_duplicate_groups"]
        if len(g["unified_episode_ids"]) > 1
    ]
    assert multi == []


def test_allowlist_covers_duplicate_group_match() -> None:
    entries = [
        {
            "episode_spec_sha256": "abc",
            "unified_episode_ids": ["u_z", "u_a"],
            "rationale": "test",
        },
    ]
    assert allowlist_covers_duplicate_group("abc", ["u_a", "u_z"], entries) is True


def test_allowlist_covers_duplicate_group_no_match() -> None:
    entries = [
        {
            "episode_spec_sha256": "abc",
            "unified_episode_ids": ["u_a"],
            "rationale": "test",
        },
    ]
    assert allowlist_covers_duplicate_group("abc", ["u_a", "u_z"], entries) is False


def test_extract_audit_text_and_skeleton_deterministic() -> None:
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    spec = data["episodes"][0]["episode_spec"]
    t1 = extract_audit_text(spec)
    t2 = extract_audit_text(spec)
    assert t1 == t2
    assert prompt_skeleton(spec) == prompt_skeleton(spec)


def test_episode_spec_hash_matches_module() -> None:
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    spec = data["episodes"][0]["episode_spec"]
    assert episode_spec_hash(spec) == data["episodes"][0]["source_episode_spec_hash"]


def test_defensibility_script_check_exits_zero() -> None:
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), "--check"],
        cwd=_REPO,
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
