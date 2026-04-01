"""Local green path for Family 3 — scope / precedence / exception episodes."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from lucid.families.scope_precedence_exception_v1 import (
    Family3Subtype,
    episode_spec_to_dict,
    generate_episode,
)
from lucid.models import DriftSeverity, EpisodeResponse, EpisodeSpec, TurnRecord
from lucid.scorer import score_episode
from lucid.writer import build_episode_result, write_bundle


def fixture_turns_family3(spec: EpisodeSpec) -> Sequence[TurnRecord]:
    """Reference turns: cautious intermediate + correct ANSWER final (resolved family)."""
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


def run_family3_smoke(
    *,
    seed: int,
    out_root: Path,
    model_id: str = "fixture",
    drift_severity: DriftSeverity | None = None,
    family_subtype: Family3Subtype = "scope",
) -> tuple[Path, float]:
    """One Family 3 smoke run; returns bundle path and aggregate score."""
    sev = drift_severity if drift_severity is not None else DriftSeverity.MEDIUM
    spec = generate_episode(seed=seed, drift_severity=sev, family_subtype=family_subtype)
    turns = fixture_turns_family3(spec)
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
