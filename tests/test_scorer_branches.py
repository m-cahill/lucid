"""Extra scorer branches for coverage."""

from __future__ import annotations

from lucid.models import (
    DriftEvent,
    DriftSeverity,
    DriftType,
    EpisodeResponse,
    EpisodeSpec,
    TurnRecord,
)
from lucid.scorer import compute_A, compute_C, compute_D, compute_O


def _spec_unresolved() -> EpisodeSpec:
    de = DriftEvent(DriftType.NEGATION, DriftSeverity.MEDIUM, 1, {})
    return EpisodeSpec(
        episode_id="u",
        benchmark_version="1.1.0",
        generation_seed=0,
        template_family="x",
        template_version="1",
        difficulty_profile={},
        drift_event=de,
        pre_drift_rule={},
        post_drift_rule={},
        expected_outputs={},
        answer_schema_ref="",
        drift_onset_turn=1,
        detection_eligible_turns=(1,),
        ambiguity_window_turns=(1,),
        clarification_eligible_turns=(),
        final_resolution_turn=2,
        recovery_probe_turns=(),
        uncertainty_ceiling=0.4,
        final_calibration_epsilon=0.05,
        final_success_condition="",
        acceptable_final_modes=frozenset({"ABSTAIN", "CLARIFY", "ANSWER"}),
        scoring_profile_version="1.1.0",
        scored_post_drift_turns=(1, 2),
        calibration_eligible_turns=(1, 2),
        requires_final_answer=False,
        final_state_unresolved=True,
    )


def test_A_unresolved_abstain() -> None:
    s = _spec_unresolved()
    turns = (TurnRecord(2, EpisodeResponse(None, 0.3, "ABSTAIN", "NONE")),)
    assert compute_A(s, turns) == 1.0


def test_D_no_detection() -> None:
    de = DriftEvent(DriftType.NEGATION, DriftSeverity.MEDIUM, 1, {})
    s = EpisodeSpec(
        episode_id="d",
        benchmark_version="1.1.0",
        generation_seed=0,
        template_family="x",
        template_version="1",
        difficulty_profile={},
        drift_event=de,
        pre_drift_rule={},
        post_drift_rule={},
        expected_outputs={"final_correct_item_id": "I1"},
        answer_schema_ref="",
        drift_onset_turn=1,
        detection_eligible_turns=(1,),
        ambiguity_window_turns=(1,),
        clarification_eligible_turns=(),
        final_resolution_turn=2,
        recovery_probe_turns=(),
        uncertainty_ceiling=0.4,
        final_calibration_epsilon=0.05,
        final_success_condition="",
        acceptable_final_modes=frozenset({"ANSWER"}),
        scoring_profile_version="1.1.0",
        scored_post_drift_turns=(1, 2),
        calibration_eligible_turns=(1, 2),
    )
    turns = (TurnRecord(1, EpisodeResponse("I1", 0.5, "ANSWER", "NONE")),)
    assert compute_D(s, turns) == 0.0


def test_O_skips_missing_turn() -> None:
    de = DriftEvent(DriftType.NEGATION, DriftSeverity.MEDIUM, 1, {})
    s = EpisodeSpec(
        episode_id="o",
        benchmark_version="1.1.0",
        generation_seed=0,
        template_family="x",
        template_version="1",
        difficulty_profile={},
        drift_event=de,
        pre_drift_rule={},
        post_drift_rule={},
        expected_outputs={"final_correct_item_id": "I1"},
        answer_schema_ref="",
        drift_onset_turn=1,
        detection_eligible_turns=(1,),
        ambiguity_window_turns=(1,),
        clarification_eligible_turns=(),
        final_resolution_turn=3,
        recovery_probe_turns=(),
        uncertainty_ceiling=0.4,
        final_calibration_epsilon=0.05,
        final_success_condition="",
        acceptable_final_modes=frozenset({"ANSWER"}),
        scoring_profile_version="1.1.0",
        scored_post_drift_turns=(1, 2, 3),
        calibration_eligible_turns=(1, 2, 3),
    )
    turns = (
        TurnRecord(1, EpisodeResponse("I1", 0.3, "ANSWER", "NONE")),
        TurnRecord(3, EpisodeResponse("I1", 0.96, "ANSWER", "NONE")),
    )
    assert compute_O(s, turns) >= 0.0


def test_C_wrong() -> None:
    de = DriftEvent(DriftType.NEGATION, DriftSeverity.MEDIUM, 1, {})
    s = EpisodeSpec(
        episode_id="c",
        benchmark_version="1.1.0",
        generation_seed=0,
        template_family="x",
        template_version="1",
        difficulty_profile={},
        drift_event=de,
        pre_drift_rule={},
        post_drift_rule={},
        expected_outputs={"final_correct_item_id": "I1"},
        answer_schema_ref="",
        drift_onset_turn=1,
        detection_eligible_turns=(1,),
        ambiguity_window_turns=(1,),
        clarification_eligible_turns=(),
        final_resolution_turn=2,
        recovery_probe_turns=(),
        uncertainty_ceiling=0.4,
        final_calibration_epsilon=0.05,
        final_success_condition="",
        acceptable_final_modes=frozenset({"ANSWER"}),
        scoring_profile_version="1.1.0",
        scored_post_drift_turns=(1, 2),
        calibration_eligible_turns=(1, 2),
    )
    turns = (TurnRecord(2, EpisodeResponse("I9", 0.1, "ANSWER", "NONE")),)
    assert compute_C(s, turns) == 0.0
