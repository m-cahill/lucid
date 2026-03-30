"""Score an episode using a schema-capable LLM interface (e.g. Kaggle Benchmarks `llm.prompt`)."""

from __future__ import annotations

from typing import Any

from lucid.kaggle.llm_schema import LUCIDTurnPayload, turn_payload_to_response
from lucid.kaggle.prompts import turn1_user_prompt, turn2_user_prompt
from lucid.models import EpisodeSpec, TurnRecord
from lucid.scorer import EpisodeScore, score_episode


def score_episode_with_llm(llm: Any, spec: EpisodeSpec) -> EpisodeScore:
    """
    Two-turn evaluation: structured prompts for turn 1 and turn 2, then official scoring.

    `llm` must implement `prompt(self, text: str, *, schema: type | None = None) -> object`
    compatible with Kaggle Benchmarks (returns `schema` instances when provided).
    """
    p1 = llm.prompt(turn1_user_prompt(spec), schema=LUCIDTurnPayload)
    if not isinstance(p1, LUCIDTurnPayload):
        msg = "Turn 1 schema mismatch: expected LUCIDTurnPayload from llm.prompt"
        raise TypeError(msg)
    p2 = llm.prompt(turn2_user_prompt(spec), schema=LUCIDTurnPayload)
    if not isinstance(p2, LUCIDTurnPayload):
        msg = "Turn 2 schema mismatch: expected LUCIDTurnPayload from llm.prompt"
        raise TypeError(msg)

    turns = (
        TurnRecord(turn=1, response=turn_payload_to_response(p1)),
        TurnRecord(turn=2, response=turn_payload_to_response(p2)),
    )
    return score_episode(spec, turns)
