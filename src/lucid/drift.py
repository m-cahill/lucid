"""Drift helpers (validation against taxonomy)."""

from __future__ import annotations

from lucid.models import DriftEvent, DriftType


def validate_single_primary_drift(event: DriftEvent) -> None:
    """Assert drift metadata is present (extended checks can be added per family)."""
    if not isinstance(event.drift_type, DriftType):
        msg = f"Invalid drift_type: {event.drift_type}"
        raise ValueError(msg)


def assert_negation_family_uses_negation(event: DriftEvent, family_id: str) -> None:
    if family_id == "symbolic_negation_v1" and event.drift_type != DriftType.NEGATION:
        msg = "symbolic_negation_v1 requires NEGATION drift"
        raise ValueError(msg)
