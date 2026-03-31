"""Structured turn payloads compatible with `llm.prompt(..., schema=...)` patterns."""

from __future__ import annotations

from dataclasses import dataclass

from lucid.models import EpisodeResponse
from lucid.parser import parse_episode_response


@dataclass
class LUCIDTurnPayload:
    """Mirror of `EpisodeResponse` fields for schema-constrained LLM outputs."""

    answer: str | None
    confidence: float
    response_mode: str
    drift_detected: str
    rationale_stub: str | None = None


def turn_payload_to_response(payload: LUCIDTurnPayload) -> EpisodeResponse:
    """Convert a structured payload into the canonical `EpisodeResponse`."""
    raw: dict[str, object] = {
        "answer": payload.answer,
        "confidence": payload.confidence,
        "response_mode": payload.response_mode,
        "drift_detected": payload.drift_detected,
        "rationale_stub": payload.rationale_stub,
    }
    return parse_episode_response(raw)
