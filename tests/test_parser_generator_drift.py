"""Parser, generator dispatch, and drift validation."""

from __future__ import annotations

import pytest

from lucid.drift import assert_negation_family_uses_negation, validate_single_primary_drift
from lucid.generator import generate_episode
from lucid.models import DriftEvent, DriftSeverity, DriftType
from lucid.parser import parse_episode_response


def test_parse_ok() -> None:
    r = parse_episode_response(
        {
            "answer": "I1",
            "confidence": 0.5,
            "response_mode": "ANSWER",
            "drift_detected": "NONE",
        }
    )
    assert r.answer == "I1"


def test_parse_invalid_mode() -> None:
    with pytest.raises(ValueError, match="response_mode"):
        parse_episode_response(
            {
                "answer": "I1",
                "confidence": 0.5,
                "response_mode": "NOPE",
                "drift_detected": "NONE",
            }
        )


def test_generator_symbolic_negation() -> None:
    spec = generate_episode(seed=5, template_family="symbolic_negation_v1")
    assert spec.template_family == "symbolic_negation_v1"


def test_generator_unknown_family() -> None:
    with pytest.raises(ValueError, match="Unknown"):
        generate_episode(seed=1, template_family="nope")


def test_drift_validate() -> None:
    de = DriftEvent(DriftType.NEGATION, DriftSeverity.LOW, 1, {})
    validate_single_primary_drift(de)
    assert_negation_family_uses_negation(de, "symbolic_negation_v1")


def test_negation_family_rejects_wrong_type() -> None:
    de = DriftEvent(DriftType.SCOPE, DriftSeverity.LOW, 1, {})
    with pytest.raises(ValueError, match="requires NEGATION"):
        assert_negation_family_uses_negation(de, "symbolic_negation_v1")
