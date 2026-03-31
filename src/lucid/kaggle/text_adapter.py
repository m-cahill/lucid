"""Plain-text LLM output → typed turn dict for Kaggle (no schema-bound ``llm.prompt``)."""

from __future__ import annotations

import json
import math
import re
from typing import Any

ALLOWED_RESPONSE_MODES = {"ANSWER", "ABSTAIN", "CLARIFY"}
ALLOWED_DRIFT_DETECTED = {"NONE", "SUSPECTED", "CONFIRMED"}

# Flat object only (model turn payload). Safer than greedy \{.*\}; see contract §4.
JSON_OBJECT_RE = re.compile(r"\{[^{}]*\}", re.DOTALL)


def _strip_code_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _extract_first_json_object(text: str) -> str:
    cleaned = _strip_code_fences(text)
    match = JSON_OBJECT_RE.search(cleaned)
    if not match:
        msg = f"No JSON object found in model output: {cleaned[:300]!r}"
        raise ValueError(msg)
    return match.group(0)


def _normalize_confidence(value: Any) -> float:
    try:
        x = float(value)
    except Exception as exc:
        raise ValueError(f"Confidence is not numeric: {value!r}") from exc
    if math.isnan(x) or math.isinf(x):
        raise ValueError(f"Confidence must be finite: {value!r}")
    return max(0.0, min(1.0, x))


def _normalize_answer(value: Any) -> str | None:
    if value is None:
        return None
    value = str(value).strip()
    return value if value else None


def _normalize_enum(value: Any, allowed: set[str], field_name: str) -> str:
    val = str(value).strip().upper()
    if val not in allowed:
        raise ValueError(f"{field_name} must be one of {sorted(allowed)}, got {value!r}")
    return val


def parse_turn_payload(raw_text: str, require_answer: bool = False) -> dict[str, Any]:
    """Parse model JSON text into a normalized turn dict for scoring.

    * Enums and confidence are always validated strictly.
    * Turn 1 (``require_answer=False``): do not reject ``ANSWER`` with a null/empty
      ``answer`` — accept as parsed.
    * Turn 2 (``require_answer=True``): require a non-null ``answer`` only when
      ``response_mode == "ANSWER"``. ``ABSTAIN`` / ``CLARIFY`` may have null ``answer``.
    """
    obj = json.loads(_extract_first_json_object(raw_text))
    if not isinstance(obj, dict):
        raise ValueError("Parsed payload must be a JSON object")

    payload: dict[str, Any] = {
        "answer": _normalize_answer(obj.get("answer")),
        "confidence": _normalize_confidence(obj.get("confidence")),
        "response_mode": _normalize_enum(
            obj.get("response_mode", "ANSWER"),
            ALLOWED_RESPONSE_MODES,
            "response_mode",
        ),
        "drift_detected": _normalize_enum(
            obj.get("drift_detected", "NONE"),
            ALLOWED_DRIFT_DETECTED,
            "drift_detected",
        ),
    }

    if require_answer and payload["response_mode"] == "ANSWER" and payload["answer"] is None:
        raise ValueError("response_mode=ANSWER requires non-null answer")

    return payload
