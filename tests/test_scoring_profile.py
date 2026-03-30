"""Tests for scoring profile v1.1.0 semantics."""

from __future__ import annotations

from lucid.models import (
    DriftEvent,
    DriftSeverity,
    DriftType,
    EpisodeResponse,
    EpisodeSpec,
    TurnRecord,
)
from lucid.scorer import (
    compute_A,
    compute_L,
    compute_O,
    is_calibrated,
    score_episode,
    target_confidence_t,
)


def _minimal_spec(**kwargs: object) -> EpisodeSpec:
    de = DriftEvent(
        drift_type=DriftType.NEGATION,
        drift_severity=DriftSeverity.MEDIUM,
        drift_onset_turn=1,
        drift_parameters={},
    )
    defaults: dict[str, object] = {
        "episode_id": "ep_test",
        "benchmark_version": "1.1.0",
        "generation_seed": 0,
        "template_family": "symbolic_negation_v1",
        "template_version": "1.0.0",
        "difficulty_profile": {},
        "drift_event": de,
        "pre_drift_rule": {},
        "post_drift_rule": {},
        "expected_outputs": {"final_correct_item_id": "I2"},
        "answer_schema_ref": "item_id",
        "drift_onset_turn": 1,
        "detection_eligible_turns": (1,),
        "ambiguity_window_turns": (1,),
        "clarification_eligible_turns": (),
        "final_resolution_turn": 2,
        "recovery_probe_turns": (),
        "uncertainty_ceiling": 0.4,
        "final_calibration_epsilon": 0.05,
        "final_success_condition": "test",
        "acceptable_final_modes": frozenset({"ANSWER"}),
        "scoring_profile_version": "1.1.0",
        "scored_post_drift_turns": (1, 2),
        "calibration_eligible_turns": (1, 2),
        "requires_final_answer": True,
        "final_state_unresolved": False,
    }
    defaults.update(kwargs)
    return EpisodeSpec(**defaults)  # type: ignore[arg-type]


def test_target_confidence_table() -> None:
    spec = _minimal_spec()
    mid = EpisodeResponse(None, 0.5, "CLARIFY", "NONE")
    assert target_confidence_t(spec, 1, mid) == spec.uncertainty_ceiling
    fin_ok = EpisodeResponse("I2", 0.96, "ANSWER", "NONE")
    assert target_confidence_t(spec, 2, fin_ok) == 1.0
    fin_bad = EpisodeResponse("I1", 0.04, "ANSWER", "NONE")
    assert target_confidence_t(spec, 2, fin_bad) == spec.final_calibration_epsilon


def test_calibrated_response_criterion() -> None:
    spec = _minimal_spec()
    assert is_calibrated(spec, 1, EpisodeResponse(None, 0.35, "CLARIFY", "NONE")) is True
    assert is_calibrated(spec, 1, EpisodeResponse(None, 0.99, "CLARIFY", "NONE")) is False
    assert is_calibrated(spec, 2, EpisodeResponse("I2", 0.96, "ANSWER", "NONE")) is True
    assert is_calibrated(spec, 2, EpisodeResponse("I1", 0.04, "ANSWER", "NONE")) is True


def test_abstention_utility_mapping() -> None:
    spec = _minimal_spec()
    turns = (
        TurnRecord(1, EpisodeResponse(None, 0.3, "CLARIFY", "NONE")),
        TurnRecord(2, EpisodeResponse("I2", 0.9, "ANSWER", "NONE")),
    )
    assert compute_A(spec, turns) == 1.0
    turns2 = (
        TurnRecord(1, EpisodeResponse("I2", 0.99, "ANSWER", "NONE")),
        TurnRecord(2, EpisodeResponse("I2", 0.9, "ANSWER", "NONE")),
    )
    assert compute_A(spec, turns2) == 0.75


def test_confidence_overhang_unresolved_turns() -> None:
    spec = _minimal_spec()
    turns = (
        TurnRecord(1, EpisodeResponse(None, 0.9, "CLARIFY", "NONE")),
        TurnRecord(2, EpisodeResponse("I2", 0.96, "ANSWER", "NONE")),
    )
    o = compute_O(spec, turns)
    assert o > 0.0


def test_final_correct_high_confidence_is_not_penalized() -> None:
    spec = _minimal_spec()
    turns = (
        TurnRecord(1, EpisodeResponse(None, 0.35, "CLARIFY", "NONE")),
        TurnRecord(2, EpisodeResponse("I2", 0.96, "ANSWER", "NONE")),
    )
    o = compute_O(spec, turns)
    assert o < 0.01


def test_L_early_calibration() -> None:
    spec = _minimal_spec()
    turns = (
        TurnRecord(1, EpisodeResponse(None, 0.35, "CLARIFY", "NONE")),
        TurnRecord(2, EpisodeResponse("I2", 0.96, "ANSWER", "NONE")),
    )
    assert compute_L(spec, turns) == 0.0


def test_score_episode_aggregate() -> None:
    spec = _minimal_spec()
    turns = (
        TurnRecord(1, EpisodeResponse(None, 0.35, "CLARIFY", "CONFIRMED")),
        TurnRecord(2, EpisodeResponse("I2", 0.96, "ANSWER", "CONFIRMED")),
    )
    es = score_episode(spec, turns)
    assert 0.0 <= es.lucid_score_episode <= 1.0
