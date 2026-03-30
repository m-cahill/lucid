"""Episode generation entrypoints."""

from __future__ import annotations

from lucid.families.symbolic_negation_v1 import generate_episode as generate_symbolic_negation_v1
from lucid.models import DriftSeverity, EpisodeSpec


def generate_episode(
    *,
    seed: int,
    template_family: str = "symbolic_negation_v1",
    drift_severity: DriftSeverity | None = None,
) -> EpisodeSpec:
    """Dispatch deterministic generation by `template_family`."""
    if template_family == "symbolic_negation_v1":
        sev = drift_severity or DriftSeverity.MEDIUM
        return generate_symbolic_negation_v1(seed=seed, drift_severity=sev)
    msg = f"Unknown template_family: {template_family}"
    raise ValueError(msg)
