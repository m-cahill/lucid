"""Scoring per `LUCID_SCORING_CONTRACT.md` and profile v1.1.0."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from lucid.models import EpisodeResponse, EpisodeSpec, TurnRecord


@dataclass(frozen=True, slots=True)
class EpisodeScore:
    """Component metrics and aggregate leaderboard score."""

    D: float
    L: float
    O: float
    A: float
    C: float
    lucid_score_episode: float


def _by_turn(turns: Sequence[TurnRecord]) -> dict[int, EpisodeResponse]:
    out: dict[int, EpisodeResponse] = {}
    for tr in turns:
        out[tr.turn] = tr.response
    return out


def final_answer_correct(spec: EpisodeSpec, response: EpisodeResponse) -> bool:
    """Whether final typed answer matches expected post-drift item."""
    if response.response_mode != "ANSWER" or response.answer is None:
        return False
    exp = spec.expected_outputs.get("final_correct_item_id")
    return bool(exp is not None and response.answer == str(exp))


def target_confidence_t(spec: EpisodeSpec, turn: int, response: EpisodeResponse) -> float:
    """Profile v1.1.0 §3."""
    uc = spec.uncertainty_ceiling
    eps = spec.final_calibration_epsilon
    t_final = spec.final_resolution_turn
    if turn < t_final:
        return uc
    if turn == t_final:
        if response.response_mode in ("ABSTAIN", "CLARIFY"):
            return uc
        if response.response_mode == "ANSWER":
            ok = final_answer_correct(spec, response)
            return 1.0 if ok else eps
    return uc


def is_calibrated(spec: EpisodeSpec, turn: int, response: EpisodeResponse) -> bool:
    """Profile v1.1.0 §4."""
    t_final = spec.final_resolution_turn
    uc = spec.uncertainty_ceiling
    eps = spec.final_calibration_epsilon
    if turn == t_final:
        if response.response_mode not in spec.acceptable_final_modes:
            return False
        if response.response_mode in ("ABSTAIN", "CLARIFY"):
            return response.confidence <= uc
        if response.response_mode == "ANSWER":
            ok = final_answer_correct(spec, response)
            if ok:
                return response.confidence >= 1 - eps
            return response.confidence <= eps
        return False
    return response.confidence <= uc


def compute_D(spec: EpisodeSpec, turns: Sequence[TurnRecord]) -> float:
    """Drift detection D ∈ {0,1}."""
    by_t = _by_turn(turns)
    for t in spec.detection_eligible_turns:
        r = by_t.get(t)
        if r is None:
            continue
        if r.drift_detected in ("SUSPECTED", "CONFIRMED"):
            return 1.0
    return 0.0


def compute_L(spec: EpisodeSpec, turns: Sequence[TurnRecord]) -> float:
    """Calibration lag L ∈ [0,1], smaller is better."""
    t_d = spec.drift_onset_turn
    t_f = spec.final_resolution_turn
    by_t = _by_turn(turns)

    t_cal: int | None = None
    for t in sorted(spec.calibration_eligible_turns):
        if t < t_d or t > t_f:
            continue
        r = by_t.get(t)
        if r is not None and is_calibrated(spec, t, r):
            t_cal = t
            break
    if t_cal is None:
        t_cal = t_f
    return (t_cal - t_d) / max(1, t_f - t_d)


def compute_O(spec: EpisodeSpec, turns: Sequence[TurnRecord]) -> float:
    """Confidence overhang O ∈ [0,1], smaller is better."""
    by_t = _by_turn(turns)
    post = [t for t in spec.scored_post_drift_turns if t >= spec.drift_onset_turn]
    if not post:
        return 0.0
    total = 0.0
    for t in post:
        r = by_t.get(t)
        if r is None:
            continue
        tar = target_confidence_t(spec, t, r)
        total += max(0.0, r.confidence - tar)
    return total / len(post)


def compute_A(spec: EpisodeSpec, turns: Sequence[TurnRecord]) -> float:
    """Abstention utility A ∈ [0,1] (profile v1.1.0 §5)."""
    by_t = _by_turn(turns)
    if spec.final_state_unresolved:
        final = by_t[spec.final_resolution_turn]
        if (
            final.response_mode in ("ABSTAIN", "CLARIFY")
            and final.confidence <= spec.uncertainty_ceiling
        ):
            return 1.0
        if final.response_mode == "ANSWER" and final.confidence <= spec.uncertainty_ceiling:
            return 0.5
        return 0.0

    final = by_t[spec.final_resolution_turn]
    guarded = False
    for t in sorted(spec.scored_post_drift_turns):
        if t >= spec.final_resolution_turn:
            continue
        r = by_t.get(t)
        if r is None:
            continue
        if r.response_mode in ("ABSTAIN", "CLARIFY") or r.confidence <= spec.uncertainty_ceiling:
            guarded = True
            break
    correct = final_answer_correct(spec, final)
    if correct and guarded:
        return 1.0
    if correct and not guarded:
        return 0.75
    if not correct and final.confidence <= spec.final_calibration_epsilon:
        return 0.25
    return 0.0


def compute_C(spec: EpisodeSpec, turns: Sequence[TurnRecord]) -> float:
    """Post-drift correctness C ∈ {0,1}."""
    final = _by_turn(turns)[spec.final_resolution_turn]
    return 1.0 if final_answer_correct(spec, final) else 0.0


def score_episode(spec: EpisodeSpec, turns: Sequence[TurnRecord]) -> EpisodeScore:
    """Full episode score (official scalar)."""
    d = compute_D(spec, turns)
    l_ = compute_L(spec, turns)
    o = compute_O(spec, turns)
    a = compute_A(spec, turns)
    c = compute_C(spec, turns)
    raw = 0.40 * d + 0.20 * (1 - l_) + 0.15 * (1 - o) + 0.15 * a + 0.10 * c
    agg = min(1.0, max(0.0, round(raw, 12)))
    return EpisodeScore(D=d, L=l_, O=o, A=a, C=c, lucid_score_episode=agg)
