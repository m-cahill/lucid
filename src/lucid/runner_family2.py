"""Local green path for Family 2 — contradiction / clarification episodes."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from lucid.families.contradiction_clarification_v1 import (
    ContradictionState,
    episode_spec_to_dict,
    generate_episode,
)
from lucid.models import DriftSeverity, EpisodeResponse, EpisodeSpec, TurnRecord
from lucid.scorer import score_episode
from lucid.writer import build_episode_result, write_bundle


def fixture_turns_family2(spec: EpisodeSpec) -> Sequence[TurnRecord]:
    """Reference turns: guarded if unresolved; correct ANSWER if resolved."""
    if spec.final_state_unresolved:
        return (
            TurnRecord(
                turn=1,
                response=EpisodeResponse(
                    answer=None,
                    confidence=0.35,
                    response_mode="CLARIFY",
                    drift_detected="CONFIRMED",
                ),
            ),
            TurnRecord(
                turn=2,
                response=EpisodeResponse(
                    answer=None,
                    confidence=0.30,
                    response_mode="ABSTAIN",
                    drift_detected="CONFIRMED",
                ),
            ),
        )
    correct = str(spec.expected_outputs["final_correct_item_id"])
    return (
        TurnRecord(
            turn=1,
            response=EpisodeResponse(
                answer=None,
                confidence=0.35,
                response_mode="CLARIFY",
                drift_detected="CONFIRMED",
            ),
        ),
        TurnRecord(
            turn=2,
            response=EpisodeResponse(
                answer=correct,
                confidence=0.95,
                response_mode="ANSWER",
                drift_detected="CONFIRMED",
            ),
        ),
    )


def run_family2_smoke(
    *,
    seed: int,
    out_root: Path,
    model_id: str = "fixture",
    drift_severity: DriftSeverity | None = None,
    contradiction_state: str = "unresolved",
) -> tuple[Path, float]:
    """One Family 2 smoke run; returns bundle path and aggregate score."""
    sev = drift_severity if drift_severity is not None else DriftSeverity.MEDIUM
    state: ContradictionState = "resolved" if contradiction_state == "resolved" else "unresolved"
    spec = generate_episode(seed=seed, drift_severity=sev, contradiction_state=state)
    turns = fixture_turns_family2(spec)
    final = turns[-1].response
    scores = score_episode(spec, turns)
    spec_dict = episode_spec_to_dict(spec)
    result = build_episode_result(
        spec,
        model_identifier=model_id,
        turns=turns,
        final_response=final,
        scores=scores,
    )
    bundle = write_bundle(out_root, spec_dict=spec_dict, episode_result=result)
    return bundle, scores.lucid_score_episode
