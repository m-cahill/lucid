"""Canonical Family 1 core pack for M03 — `symbolic_negation_v1` at scale."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Final

from lucid.families.symbolic_negation_v1 import episode_spec_to_dict, generate_episode
from lucid.models import DriftSeverity

# --- Pack identity (committed manifest must match) ---

PACK_ID: Final = "family1_core_m03_v1"
PACK_VERSION: Final = "1.0.0"
TEMPLATE_FAMILY: Final = "symbolic_negation_v1"
TEMPLATE_VERSION: Final = "1.0.0"
BENCHMARK_VERSION: Final = "1.1.0"
SCORING_PROFILE_VERSION: Final = "1.1.0"
EPISODE_COUNT: Final = 96

# Path relative to repository root (single canonical home).
CANONICAL_MANIFEST_RELPATH: Final = "tests/fixtures/family1_core_m03/family1_core_m03_manifest.json"

# M01 Kaggle transport acceptance rows — included in this pack as an explicit subset.
M01_TRANSPORT_FIXTURE_IDS: Final[frozenset[str]] = frozenset(
    {"symneg_100_low", "symneg_42_medium", "symneg_200_high"}
)

M01_FIXTURE_ID_BY_KEY: Final[dict[tuple[int, str], str]] = {
    (100, "LOW"): "symneg_100_low",
    (42, "MEDIUM"): "symneg_42_medium",
    (200, "HIGH"): "symneg_200_high",
}


def canonical_manifest_path(repo_root: Path | None = None) -> Path:
    """Resolved path to the committed Family 1 M03 manifest."""
    root = repo_root if repo_root is not None else Path(__file__).resolve().parents[3]
    return root / CANONICAL_MANIFEST_RELPATH


def low_seeds() -> list[int]:
    """32 LOW episodes: M01 seed 100 plus 1..31."""
    return sorted([100] + list(range(1, 32)))


def medium_seeds() -> list[int]:
    """32 MEDIUM episodes: 32..63 (includes M01 seed 42)."""
    return list(range(32, 64))


def high_seeds() -> list[int]:
    """32 HIGH episodes: M01 seed 200 plus 64..94."""
    return sorted(list(range(64, 95)) + [200])


def episode_sequence() -> list[tuple[int, DriftSeverity]]:
    """Stable ordering: all LOW, then MEDIUM, then HIGH; seeds sorted within bucket."""
    out: list[tuple[int, DriftSeverity]] = []
    for s in low_seeds():
        out.append((s, DriftSeverity.LOW))
    for s in medium_seeds():
        out.append((s, DriftSeverity.MEDIUM))
    for s in high_seeds():
        out.append((s, DriftSeverity.HIGH))
    return out


def _m01_fixture_id(seed: int, severity: DriftSeverity) -> str | None:
    return M01_FIXTURE_ID_BY_KEY.get((seed, severity.value))


def episode_row(seed: int, drift_severity: DriftSeverity) -> dict[str, Any]:
    """One manifest episode: audit fields + full spec serialization."""
    spec = generate_episode(seed=seed, drift_severity=drift_severity)
    base = episode_spec_to_dict(spec)
    fid = _m01_fixture_id(seed, drift_severity)
    row: dict[str, Any] = {
        "difficulty_bucket": drift_severity.value,
        "m01_transport_fixture_id": fid,
        "episode_spec": base,
    }
    return row


def build_manifest_dict() -> dict[str, Any]:
    """Deterministic manifest payload (canonical JSON comparable)."""
    episodes: list[dict[str, Any]] = []
    m01_episode_ids: list[str] = []
    for seed, sev in episode_sequence():
        row = episode_row(seed, sev)
        spec = row["episode_spec"]
        eid = str(spec["episode_id"])
        if row.get("m01_transport_fixture_id"):
            m01_episode_ids.append(eid)
        episodes.append(row)

    return {
        "pack_id": PACK_ID,
        "pack_version": PACK_VERSION,
        "benchmark_version": BENCHMARK_VERSION,
        "scoring_profile_version": SCORING_PROFILE_VERSION,
        "template_family": TEMPLATE_FAMILY,
        "template_version": TEMPLATE_VERSION,
        "episode_count": EPISODE_COUNT,
        "difficulty_distribution": {"LOW": 32, "MEDIUM": 32, "HIGH": 32},
        "m01_acceptance_subset": {
            "description": (
                "M01 Kaggle transport proof rows (`tests/fixtures/kaggle_transport/"
                "transport_manifest.json`); same episodes are members of this pack."
            ),
            "transport_manifest_path": "tests/fixtures/kaggle_transport/transport_manifest.json",
            "fixture_ids": sorted(M01_TRANSPORT_FIXTURE_IDS),
            "episode_ids": sorted(m01_episode_ids),
        },
        "regeneration": {
            "python_module": "lucid.packs.family1_core_m03",
            "cli_write": "python scripts/generate_family1_core_m03_manifest.py --write",
            "cli_check": "python scripts/generate_family1_core_m03_manifest.py --check",
        },
        "canonical_manifest_path": CANONICAL_MANIFEST_RELPATH,
        "episodes": episodes,
    }
