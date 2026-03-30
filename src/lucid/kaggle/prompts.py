"""Prompt text for multi-turn LUCID episodes on external runtimes (e.g. Kaggle Benchmarks)."""

from __future__ import annotations

from lucid.models import EpisodeSpec


def turn1_user_prompt(spec: EpisodeSpec) -> str:
    """Turn 1 — drift / ambiguity window (matches `detection_eligible_turns` / ambiguity phase)."""
    return (
        f"{spec.prompt_preamble}\n\n"
        "Turn 1 (structured output only). This is the drift-response / ambiguity window. "
        "Report drift suspicion honestly using `drift_detected`. "
        "If you are not ready to commit to a final item selection, use CLARIFY or ABSTAIN "
        "with confidence at or below the uncertainty ceiling implied by the episode."
    )


def turn2_user_prompt(spec: EpisodeSpec) -> str:
    """Turn 2 — final resolution (matches `final_resolution_turn`)."""
    return (
        "Turn 2 (structured output only) — final resolution. "
        "Select the single `item_id` that satisfies the POST-DRIFT rule, "
        "with calibrated confidence. Use response_mode ANSWER when you commit to an item_id."
    )
