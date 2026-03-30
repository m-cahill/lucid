"""Tests for Kaggle-oriented LLM scoring wrapper."""

from __future__ import annotations

from typing import Any

import pytest

from lucid.families.symbolic_negation_v1 import generate_episode
from lucid.kaggle.episode_llm import score_episode_with_llm
from lucid.kaggle.llm_schema import LUCIDTurnPayload
from lucid.models import DriftSeverity
from lucid.runner import fixture_turns
from lucid.scorer import score_episode


class _StubLLM:
    """Returns the same two structured turns as `fixture_turns` for a given spec."""

    def __init__(self, spec: Any) -> None:
        self._turns = fixture_turns(spec)
        self._n = 0

    def prompt(self, text: str, *, schema: Any = None) -> Any:
        assert schema is not None
        self._n += 1
        tr = self._turns[self._n - 1].response
        return schema(
            answer=tr.answer,
            confidence=tr.confidence,
            response_mode=tr.response_mode,
            drift_detected=tr.drift_detected,
            rationale_stub=tr.rationale_stub,
        )


def test_score_episode_with_llm_matches_fixture_turns() -> None:
    spec = generate_episode(seed=42, drift_severity=DriftSeverity.MEDIUM)
    llm = _StubLLM(spec)
    got = score_episode_with_llm(llm, spec)
    ref = score_episode(spec, fixture_turns(spec))
    assert got.lucid_score_episode == pytest.approx(ref.lucid_score_episode)


def test_score_episode_with_llm_rejects_wrong_schema_type() -> None:
    spec = generate_episode(seed=1, drift_severity=DriftSeverity.LOW)

    class _BadLLM:
        def prompt(self, text: str, *, schema: Any = None) -> str:
            return "not-a-payload"

    with pytest.raises(TypeError):
        score_episode_with_llm(_BadLLM(), spec)


def test_turn_payload_round_trip() -> None:
    spec = generate_episode(seed=7, drift_severity=DriftSeverity.MEDIUM)
    llm = _StubLLM(spec)
    p1 = llm.prompt("x", schema=LUCIDTurnPayload)
    p2 = llm.prompt("y", schema=LUCIDTurnPayload)
    assert isinstance(p1, LUCIDTurnPayload)
    assert isinstance(p2, LUCIDTurnPayload)
