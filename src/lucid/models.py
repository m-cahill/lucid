"""Typed structures for episode specs and benchmark responses."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Literal

ResponseMode = Literal["ANSWER", "ABSTAIN", "CLARIFY"]
DriftDetected = Literal["NONE", "SUSPECTED", "CONFIRMED"]


class DriftType(StrEnum):
    """Primary drift families (taxonomy contract)."""

    NEGATION = "NEGATION"
    SCOPE = "SCOPE"
    PRECEDENCE = "PRECEDENCE"
    EXCEPTION = "EXCEPTION"
    AUTHORITY = "AUTHORITY"
    AMBIGUITY = "AMBIGUITY"
    CONTRADICTION = "CONTRADICTION"


class DriftSeverity(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass(frozen=True, slots=True)
class DriftEvent:
    """Typed primary drift event (single per scored episode)."""

    drift_type: DriftType
    drift_severity: DriftSeverity
    drift_onset_turn: int
    drift_parameters: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class EpisodeResponse:
    """Canonical typed response (`LUCID_OUTPUT_SCHEMA_CONTRACT.md`)."""

    answer: str | None
    confidence: float
    response_mode: ResponseMode
    drift_detected: DriftDetected
    rationale_stub: str | None = None


@dataclass(frozen=True, slots=True)
class TurnRecord:
    """One turn’s typed response for multi-turn scoring."""

    turn: int
    response: EpisodeResponse


@dataclass(frozen=True, slots=True)
class EpisodeSpec:
    """Subset of episode spec fields required for scoring + writing bundles."""

    episode_id: str
    benchmark_version: str
    generation_seed: int
    template_family: str
    template_version: str
    difficulty_profile: Mapping[str, Any]
    drift_event: DriftEvent
    pre_drift_rule: Mapping[str, Any]
    post_drift_rule: Mapping[str, Any]
    expected_outputs: Mapping[str, Any]
    answer_schema_ref: str
    drift_onset_turn: int
    detection_eligible_turns: Sequence[int]
    ambiguity_window_turns: Sequence[int]
    clarification_eligible_turns: Sequence[int]
    final_resolution_turn: int
    recovery_probe_turns: Sequence[int]
    uncertainty_ceiling: float
    final_calibration_epsilon: float
    final_success_condition: str
    acceptable_final_modes: frozenset[str]
    scoring_profile_version: str
    scored_post_drift_turns: Sequence[int]
    calibration_eligible_turns: Sequence[int]
    requires_final_answer: bool = True
    final_state_unresolved: bool = False
    items: Sequence[Mapping[str, Any]] = field(default_factory=tuple)
    prompt_preamble: str = ""
