"""Prompt text for multi-turn LUCID episodes on external runtimes (e.g. Kaggle Benchmarks)."""

from __future__ import annotations

import json

from lucid.models import EpisodeSpec


def _items_block(spec: EpisodeSpec) -> str:
    lines: list[str] = []
    for item in spec.items:
        lines.append(json.dumps(item, sort_keys=True))
    return "\n".join(lines)


def _drift_event_obj(spec: EpisodeSpec) -> dict[str, object]:
    de = spec.drift_event
    return {
        "drift_type": de.drift_type.value
        if hasattr(de.drift_type, "value")
        else str(de.drift_type),
        "drift_severity": de.drift_severity.value
        if hasattr(de.drift_severity, "value")
        else str(de.drift_severity),
        "drift_onset_turn": de.drift_onset_turn,
        "drift_parameters": dict(de.drift_parameters),
    }


def turn1_user_prompt(spec: EpisodeSpec) -> str:
    """Turn 1 — drift window; JSON-only; use parse_turn_payload(..., False)."""
    return f"""
You are evaluating a synthetic rule-world benchmark episode.

CURRENT PHASE: DRIFT_RESPONSE_WINDOW
This is NOT the final answer turn.

Items:
{_items_block(spec)}

Pre-drift rule:
{json.dumps(spec.pre_drift_rule, sort_keys=True)}

Drift event:
{json.dumps(_drift_event_obj(spec), sort_keys=True)}

Post-drift rule:
{json.dumps(spec.post_drift_rule, sort_keys=True)}

You are in the ambiguity / calibration window.
Do NOT provide the final item choice yet unless absolutely necessary.
Return JSON ONLY with this exact schema:

{{
  "answer": null,
  "confidence": <float in [0,1]>,
  "response_mode": "ANSWER" | "ABSTAIN" | "CLARIFY",
  "drift_detected": "NONE" | "SUSPECTED" | "CONFIRMED"
}}

Guidance:
- If you are uncertain after the rule change, lower confidence.
- If response_mode is ANSWER, provide a provisional item id when you can;
  otherwise use ABSTAIN or CLARIFY.
- Output JSON only. No prose.
""".strip()


def turn2_user_prompt(spec: EpisodeSpec) -> str:
    """Turn 2 — final resolution; JSON-only; use parse_turn_payload(..., True)."""
    return f"""
Continue the same episode.

CURRENT PHASE: FINAL_RESOLUTION
You must now provide the final typed response.

Items:
{_items_block(spec)}

Post-drift rule:
{json.dumps(spec.post_drift_rule, sort_keys=True)}

Valid item ids:
{json.dumps([item["id"] for item in spec.items])}

Return JSON ONLY with this exact schema:

{{
  "answer": "<item_id>" | null,
  "confidence": <float in [0,1]>,
  "response_mode": "ANSWER" | "ABSTAIN" | "CLARIFY",
  "drift_detected": "NONE" | "SUSPECTED" | "CONFIRMED"
}}

Important:
- Final resolution for this family normally expects an ANSWER.
- If response_mode is ANSWER, answer must be one of the valid item ids.
- Output JSON only. No prose.
""".strip()
