"""Transport manifest loading and local equivalence checks (offline; not a platform stub)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from lucid.families.symbolic_negation_v1 import generate_episode
from lucid.models import DriftSeverity
from lucid.runner import fixture_turns
from lucid.scorer import EpisodeScore, score_episode


@dataclass(frozen=True, slots=True)
class TransportFixture:
    """One frozen transport row from `transport_manifest.json`."""

    id: str
    generation_seed: int
    drift_severity: DriftSeverity
    episode_id: str
    expected: EpisodeScore


def _severity(raw: str) -> DriftSeverity:
    return DriftSeverity[raw]


def load_transport_manifest(path: Path | str) -> dict[str, Any]:
    """Load the JSON manifest (transport metadata + fixture rows)."""
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    return cast(dict[str, Any], data)


def load_transport_fixtures(path: Path | str) -> list[TransportFixture]:
    """Parse manifest fixtures into typed rows with expected `EpisodeScore` fields."""
    data = load_transport_manifest(path)
    out: list[TransportFixture] = []
    for row in cast(list[dict[str, Any]], data["fixtures"]):
        exp = row["expected"]
        score = EpisodeScore(
            D=float(exp["D"]),
            L=float(exp["L"]),
            O=float(exp["O"]),
            A=float(exp["A"]),
            C=float(exp["C"]),
            lucid_score_episode=float(exp["lucid_score_episode"]),
        )
        out.append(
            TransportFixture(
                id=str(row["id"]),
                generation_seed=int(row["generation_seed"]),
                drift_severity=_severity(str(row["drift_severity"])),
                episode_id=str(row["episode_id"]),
                expected=score,
            )
        )
    return out


def verify_fixture_against_local(fixture: TransportFixture) -> EpisodeScore:
    """Recompute the official score for a manifest row using the reference fixture turns."""
    spec = generate_episode(seed=fixture.generation_seed, drift_severity=fixture.drift_severity)
    if spec.episode_id != fixture.episode_id:
        msg = (
            f"episode_id mismatch for {fixture.id}: manifest {fixture.episode_id} "
            f"vs spec {spec.episode_id}"
        )
        raise ValueError(msg)
    turns = fixture_turns(spec)
    return score_episode(spec, turns)
