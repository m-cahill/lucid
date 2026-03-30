"""Parse untyped payloads into `EpisodeResponse`."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

from lucid.models import DriftDetected, EpisodeResponse, ResponseMode


def parse_episode_response(raw: Mapping[str, Any]) -> EpisodeResponse:
    """Validate and construct a typed response (strict)."""
    mode = raw["response_mode"]
    conf = float(raw["confidence"])
    dd = raw["drift_detected"]
    if mode not in ("ANSWER", "ABSTAIN", "CLARIFY"):
        msg = f"Invalid response_mode: {mode}"
        raise ValueError(msg)
    if dd not in ("NONE", "SUSPECTED", "CONFIRMED"):
        msg = f"Invalid drift_detected: {dd}"
        raise ValueError(msg)
    if not 0.0 <= conf <= 1.0:
        msg = "confidence must be in [0, 1]"
        raise ValueError(msg)
    ans = raw.get("answer")
    if mode == "ANSWER":
        if ans is None or (isinstance(ans, str) and not ans.strip()):
            msg = "ANSWER requires non-empty answer"
            raise ValueError(msg)
    else:
        ans = None
    rs = raw.get("rationale_stub")
    return EpisodeResponse(
        answer=ans if isinstance(ans, str) else None,
        confidence=conf,
        response_mode=cast(ResponseMode, mode),
        drift_detected=cast(DriftDetected, dd),
        rationale_stub=rs if isinstance(rs, str) else None,
    )
