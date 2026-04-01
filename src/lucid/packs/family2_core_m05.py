"""Canonical Family 2 core pack for M05 — `contradiction_clarification_v1` at scale."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Final

from lucid.families.contradiction_clarification_v1 import (
    ContradictionState,
    episode_spec_to_dict,
    generate_episode,
)
from lucid.models import DriftSeverity

# --- Pack identity (committed manifest must match) ---

PACK_ID: Final = "family2_core_m05_v1"
PACK_VERSION: Final = "1.0.0"
FAMILY_ID: Final = "contradiction_clarification_v1"
TEMPLATE_FAMILY: Final = "contradiction_clarification_v1"
TEMPLATE_VERSION: Final = "1.0.0"
BENCHMARK_VERSION: Final = "1.1.0"
SCORING_PROFILE_VERSION: Final = "1.1.0"
EPISODE_COUNT: Final = 72

CANONICAL_MANIFEST_RELPATH: Final = "tests/fixtures/family2_core_m05/family2_core_m05_manifest.json"


def canonical_manifest_path(repo_root: Path | None = None) -> Path:
    """Resolved path to the committed Family 2 M05 manifest."""
    root = repo_root if repo_root is not None else Path(__file__).resolve().parents[3]
    return root / CANONICAL_MANIFEST_RELPATH


def _seeds_unresolved_low() -> list[int]:
    return list(range(1, 13))


def _seeds_resolved_low() -> list[int]:
    return list(range(13, 25))


def _seeds_unresolved_medium() -> list[int]:
    return list(range(101, 113))


def _seeds_resolved_medium() -> list[int]:
    return list(range(113, 125))


def _seeds_unresolved_high() -> list[int]:
    return list(range(201, 213))


def _seeds_resolved_high() -> list[int]:
    return list(range(213, 225))


def episode_sequence() -> list[tuple[int, DriftSeverity, str]]:
    """Stable ordering: LOW (unresolved then resolved), then MEDIUM, then HIGH."""
    out: list[tuple[int, DriftSeverity, str]] = []
    for seed in _seeds_unresolved_low():
        out.append((seed, DriftSeverity.LOW, "unresolved"))
    for seed in _seeds_resolved_low():
        out.append((seed, DriftSeverity.LOW, "resolved"))
    for seed in _seeds_unresolved_medium():
        out.append((seed, DriftSeverity.MEDIUM, "unresolved"))
    for seed in _seeds_resolved_medium():
        out.append((seed, DriftSeverity.MEDIUM, "resolved"))
    for seed in _seeds_unresolved_high():
        out.append((seed, DriftSeverity.HIGH, "unresolved"))
    for seed in _seeds_resolved_high():
        out.append((seed, DriftSeverity.HIGH, "resolved"))
    return out


def episode_row(
    seed: int,
    drift_severity: DriftSeverity,
    contradiction_state: str,
) -> dict[str, Any]:
    """One manifest episode: audit fields + full spec serialization."""
    st: ContradictionState = "resolved" if contradiction_state == "resolved" else "unresolved"
    spec = generate_episode(seed=seed, drift_severity=drift_severity, contradiction_state=st)
    base = episode_spec_to_dict(spec)
    prof = base["difficulty_profile"]
    return {
        "difficulty_bucket": drift_severity.value,
        "contradiction_state": st,
        "family_id": FAMILY_ID,
        "pack_id": PACK_ID,
        "template_version": TEMPLATE_VERSION,
        "seed": seed,
        "drift_type": spec.drift_event.drift_type.value,
        "target_behavior": str(prof.get("target_behavior", "")),
        "clarifier_present": bool(prof.get("clarifier_present", False)),
        "final_state_unresolved": spec.final_state_unresolved,
        "expected_post_drift_rule": dict(spec.post_drift_rule),
        "episode_spec": base,
    }


def build_manifest_dict() -> dict[str, Any]:
    """Deterministic manifest payload (canonical JSON comparable)."""
    episodes: list[dict[str, Any]] = []
    for seed, sev, cstate in episode_sequence():
        episodes.append(episode_row(seed, sev, cstate))

    return {
        "pack_id": PACK_ID,
        "pack_version": PACK_VERSION,
        "benchmark_version": BENCHMARK_VERSION,
        "scoring_profile_version": SCORING_PROFILE_VERSION,
        "template_family": TEMPLATE_FAMILY,
        "template_version": TEMPLATE_VERSION,
        "family_id": FAMILY_ID,
        "episode_count": EPISODE_COUNT,
        "difficulty_distribution": {"LOW": 24, "MEDIUM": 24, "HIGH": 24},
        "contradiction_state_distribution": {
            "per_bucket": {"unresolved": 12, "resolved": 12},
            "total": {"unresolved": 36, "resolved": 36},
        },
        "regeneration": {
            "python_module": "lucid.packs.family2_core_m05",
            "cli_write": "python scripts/generate_family2_core_m05_manifest.py --write",
            "cli_check": "python scripts/generate_family2_core_m05_manifest.py --check",
        },
        "canonical_manifest_path": CANONICAL_MANIFEST_RELPATH,
        "episodes": episodes,
    }


def smoke_subset_triples() -> tuple[tuple[int, DriftSeverity, str], ...]:
    """One unresolved + one resolved per difficulty bucket (6 runs)."""
    return (
        (1, DriftSeverity.LOW, "unresolved"),
        (13, DriftSeverity.LOW, "resolved"),
        (101, DriftSeverity.MEDIUM, "unresolved"),
        (113, DriftSeverity.MEDIUM, "resolved"),
        (201, DriftSeverity.HIGH, "unresolved"),
        (213, DriftSeverity.HIGH, "resolved"),
    )
