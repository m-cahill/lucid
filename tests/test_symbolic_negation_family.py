"""Determinism and structure tests for `symbolic_negation_v1`."""

from __future__ import annotations

from lucid.families.symbolic_negation_v1 import (
    episode_spec_to_dict,
    generate_episode,
)
from lucid.models import DriftSeverity


def test_same_seed_same_spec() -> None:
    a = generate_episode(seed=123, drift_severity=DriftSeverity.MEDIUM)
    b = generate_episode(seed=123, drift_severity=DriftSeverity.MEDIUM)
    assert episode_spec_to_dict(a) == episode_spec_to_dict(b)


def test_different_seed_can_differ() -> None:
    a = generate_episode(seed=1, drift_severity=DriftSeverity.MEDIUM)
    b = generate_episode(seed=2, drift_severity=DriftSeverity.MEDIUM)
    assert a.expected_outputs != b.expected_outputs or a.episode_id != b.episode_id


def test_drift_onset_serialized() -> None:
    s = generate_episode(seed=0, drift_severity=DriftSeverity.LOW)
    d = episode_spec_to_dict(s)
    assert d["drift_onset_turn"] == 1
    assert d["drift_event"]["drift_type"] == "NEGATION"


def test_difficulty_knobs_severity() -> None:
    low = generate_episode(seed=10, drift_severity=DriftSeverity.LOW)
    high = generate_episode(seed=10, drift_severity=DriftSeverity.HIGH)
    assert int(low.difficulty_profile["n_items"]) < int(high.difficulty_profile["n_items"])
