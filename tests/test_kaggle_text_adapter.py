"""Tests for plain-text JSON turn parsing (Kaggle text adapter)."""

from __future__ import annotations

import json

import pytest

from lucid.kaggle.text_adapter import parse_turn_payload


def _payload(
    *,
    answer: str | None,
    confidence: float = 0.5,
    response_mode: str = "ANSWER",
    drift_detected: str = "NONE",
) -> str:
    obj = {
        "answer": answer,
        "confidence": confidence,
        "response_mode": response_mode,
        "drift_detected": drift_detected,
    }
    return json.dumps(obj)


def test_turn1_accepts_answer_with_null_answer() -> None:
    raw = _payload(answer=None, response_mode="ANSWER")
    out = parse_turn_payload(raw, require_answer=False)
    assert out["response_mode"] == "ANSWER"
    assert out["answer"] is None


def test_turn2_rejects_answer_mode_without_answer() -> None:
    raw = _payload(answer=None, response_mode="ANSWER")
    with pytest.raises(ValueError, match="non-null answer"):
        parse_turn_payload(raw, require_answer=True)


def test_turn2_allows_abstain_with_null_answer() -> None:
    raw = _payload(answer=None, response_mode="ABSTAIN")
    out = parse_turn_payload(raw, require_answer=True)
    assert out["response_mode"] == "ABSTAIN"
    assert out["answer"] is None


def test_turn2_allows_clarify_with_null_answer() -> None:
    raw = _payload(answer=None, response_mode="CLARIFY")
    out = parse_turn_payload(raw, require_answer=True)
    assert out["response_mode"] == "CLARIFY"
    assert out["answer"] is None


def test_invalid_response_mode_rejected() -> None:
    raw = _payload(answer="x", response_mode="INVALID")
    with pytest.raises(ValueError, match="response_mode"):
        parse_turn_payload(raw, require_answer=False)


def test_fenced_json_extracted() -> None:
    inner = _payload(answer="a1", response_mode="ANSWER")
    raw = f"```json\n{inner}\n```"
    out = parse_turn_payload(raw, require_answer=True)
    assert out["answer"] == "a1"
