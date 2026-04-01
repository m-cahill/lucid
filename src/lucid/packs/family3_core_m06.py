"""Canonical Family 3 core pack for M06 — `scope_precedence_exception_v1` at scale."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Final

from lucid.families.scope_precedence_exception_v1 import (
    Family3Subtype,
    episode_spec_to_dict,
    generate_episode,
)
from lucid.models import DriftSeverity

# --- Pack identity (committed manifest must match) ---

PACK_ID: Final = "family3_core_m06_v1"
PACK_VERSION: Final = "1.0.0"
FAMILY_ID: Final = "scope_precedence_exception_v1"
TEMPLATE_FAMILY: Final = "scope_precedence_exception_v1"
TEMPLATE_VERSION: Final = "1.0.0"
BENCHMARK_VERSION: Final = "1.1.0"
SCORING_PROFILE_VERSION: Final = "1.1.0"
EPISODE_COUNT: Final = 72

CANONICAL_MANIFEST_RELPATH: Final = "tests/fixtures/family3_core_m06/family3_core_m06_manifest.json"


def canonical_manifest_path(repo_root: Path | None = None) -> Path:
    """Resolved path to the committed Family 3 M06 manifest."""
    root = repo_root if repo_root is not None else Path(__file__).resolve().parents[3]
    return root / CANONICAL_MANIFEST_RELPATH


def _seeds_scope_low() -> list[int]:
    return list(range(1, 9))


def _seeds_precedence_low() -> list[int]:
    return list(range(9, 17))


def _seeds_exception_low() -> list[int]:
    return list(range(17, 25))


def _seeds_scope_medium() -> list[int]:
    return list(range(101, 109))


def _seeds_precedence_medium() -> list[int]:
    return list(range(109, 117))


def _seeds_exception_medium() -> list[int]:
    return list(range(117, 125))


def _seeds_scope_high() -> list[int]:
    return list(range(201, 209))


def _seeds_precedence_high() -> list[int]:
    return list(range(209, 217))


def _seeds_exception_high() -> list[int]:
    return list(range(217, 225))


def episode_sequence() -> list[tuple[int, DriftSeverity, Family3Subtype]]:
    """Stable ordering: per bucket — scope, precedence, exception."""
    out: list[tuple[int, DriftSeverity, Family3Subtype]] = []
    for seed in _seeds_scope_low():
        out.append((seed, DriftSeverity.LOW, "scope"))
    for seed in _seeds_precedence_low():
        out.append((seed, DriftSeverity.LOW, "precedence"))
    for seed in _seeds_exception_low():
        out.append((seed, DriftSeverity.LOW, "exception"))
    for seed in _seeds_scope_medium():
        out.append((seed, DriftSeverity.MEDIUM, "scope"))
    for seed in _seeds_precedence_medium():
        out.append((seed, DriftSeverity.MEDIUM, "precedence"))
    for seed in _seeds_exception_medium():
        out.append((seed, DriftSeverity.MEDIUM, "exception"))
    for seed in _seeds_scope_high():
        out.append((seed, DriftSeverity.HIGH, "scope"))
    for seed in _seeds_precedence_high():
        out.append((seed, DriftSeverity.HIGH, "precedence"))
    for seed in _seeds_exception_high():
        out.append((seed, DriftSeverity.HIGH, "exception"))
    return out


def episode_row(
    seed: int,
    drift_severity: DriftSeverity,
    family_subtype: Family3Subtype,
) -> dict[str, Any]:
    """One manifest episode: audit fields + full spec serialization."""
    spec = generate_episode(seed=seed, drift_severity=drift_severity, family_subtype=family_subtype)
    base = episode_spec_to_dict(spec)
    prof = base["difficulty_profile"]
    de = spec.drift_event
    row: dict[str, Any] = {
        "episode_id": spec.episode_id,
        "difficulty_bucket": drift_severity.value,
        "family3_subtype": prof.get("family3_subtype"),
        "drift_subtype": prof.get("drift_subtype"),
        "family_id": FAMILY_ID,
        "pack_id": PACK_ID,
        "template_version": TEMPLATE_VERSION,
        "seed": seed,
        "drift_type": de.drift_type.value,
        "target_behavior": str(prof.get("target_behavior", "")),
        "expected_post_drift_rule": dict(spec.post_drift_rule),
        "final_state_unresolved": spec.final_state_unresolved,
        "episode_spec": base,
    }
    if family_subtype == "scope":
        row["scope_before"] = prof.get("scope_before")
        row["scope_after"] = prof.get("scope_after")
    elif family_subtype == "precedence":
        row["precedence_before"] = prof.get("precedence_before")
        row["precedence_after"] = prof.get("precedence_after")
        row["rule_count"] = prof.get("rule_count")
    else:
        row["general_rule"] = prof.get("general_rule")
        row["exception_class"] = prof.get("exception_class")
        row["exception_trigger"] = prof.get("exception_trigger")
    return row


def build_manifest_dict() -> dict[str, Any]:
    """Deterministic manifest payload (canonical JSON comparable)."""
    episodes: list[dict[str, Any]] = []
    for seed, sev, fst in episode_sequence():
        episodes.append(episode_row(seed, sev, fst))

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
        "drift_subtype_distribution": {
            "per_bucket": {"scope": 8, "precedence": 8, "exception": 8},
            "total": {"scope": 24, "precedence": 24, "exception": 24},
        },
        "drift_type_distribution": {
            "SCOPE": 24,
            "PRECEDENCE": 24,
            "EXCEPTION": 24,
        },
        "regeneration": {
            "python_module": "lucid.packs.family3_core_m06",
            "cli_write": "python scripts/generate_family3_core_m06_manifest.py --write",
            "cli_check": "python scripts/generate_family3_core_m06_manifest.py --check",
        },
        "canonical_manifest_path": CANONICAL_MANIFEST_RELPATH,
        "episodes": episodes,
    }


def smoke_subset_triples() -> tuple[tuple[int, DriftSeverity, Family3Subtype], ...]:
    """One scope + one precedence + one exception per difficulty bucket (9 runs)."""
    return (
        (1, DriftSeverity.LOW, "scope"),
        (9, DriftSeverity.LOW, "precedence"),
        (17, DriftSeverity.LOW, "exception"),
        (101, DriftSeverity.MEDIUM, "scope"),
        (109, DriftSeverity.MEDIUM, "precedence"),
        (117, DriftSeverity.MEDIUM, "exception"),
        (201, DriftSeverity.HIGH, "scope"),
        (209, DriftSeverity.HIGH, "precedence"),
        (217, DriftSeverity.HIGH, "exception"),
    )
