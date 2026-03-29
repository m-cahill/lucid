"""Symbolic negation drift family — template `symbolic_negation_v1` / v1.0.0."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from random import Random
from typing import Any

from lucid.models import DriftEvent, DriftSeverity, DriftType, EpisodeSpec


def _stable_episode_id(seed: int, severity: str) -> str:
    h = hashlib.sha256(f"symbolic_negation_v1:{seed}:{severity}".encode()).hexdigest()[:16]
    return f"ep_symneg_{h}"


def _mk_items(rng: Random, n_items: int, n_colors: int, n_shapes: int) -> list[dict[str, str]]:
    """Build `n_items` items with unique `(color, shape)` pairs."""
    pairs: list[tuple[int, int]] = [(c, s) for c in range(n_colors) for s in range(n_shapes)]
    if n_items > len(pairs):
        raise ValueError("n_items exceeds unique attribute combinations")
    rng.shuffle(pairs)
    items: list[dict[str, str]] = []
    for i in range(n_items):
        c_i, s_i = pairs[i]
        items.append({"id": f"I{i + 1}", "color": f"C{c_i}", "shape": f"S{s_i}"})
    return items


def generate_episode(
    *,
    seed: int,
    drift_severity: DriftSeverity = DriftSeverity.MEDIUM,
) -> EpisodeSpec:
    """Build a deterministic `EpisodeSpec` for the symbolic negation family."""
    rng = Random(seed)
    severity = drift_severity.value
    knobs: dict[str, int | str] = {
        "n_items": 8,
        "n_colors": 4,
        "n_shapes": 2,
        "drift_severity": severity,
    }
    if drift_severity == DriftSeverity.LOW:
        knobs.update({"n_items": 4, "n_colors": 3, "n_shapes": 2})
    elif drift_severity == DriftSeverity.HIGH:
        knobs.update({"n_items": 12, "n_colors": 4, "n_shapes": 3})

    n_items = int(knobs["n_items"])
    n_colors = int(knobs["n_colors"])
    n_shapes = int(knobs["n_shapes"])
    items = _mk_items(rng, n_items, n_colors, n_shapes)

    # Pre-drift: (color == C0 AND shape == S0); post: logical negation — pick unique targets.
    target_color = items[0]["color"]
    target_shape = items[0]["shape"]

    def matches_pre(it: Mapping[str, str]) -> bool:
        return it["color"] == target_color and it["shape"] == target_shape

    def matches_post(it: Mapping[str, str]) -> bool:
        return not matches_pre(it)

    pre_matches = [it for it in items if matches_pre(it)]
    post_matches = [it for it in items if matches_post(it)]
    if len(pre_matches) != 1 or len(post_matches) < 1:
        msg = "Invariant broken: tune knobs or RNG"
        raise RuntimeError(msg)

    pre_id = pre_matches[0]["id"]
    post_id = sorted(pm["id"] for pm in post_matches)[0]

    drift = DriftEvent(
        drift_type=DriftType.NEGATION,
        drift_severity=drift_severity,
        drift_onset_turn=1,
        drift_parameters={
            "predicate": "negation_of_conjunction",
            "attribute_focus": ["color", "shape"],
        },
    )

    pre_rule = {
        "kind": "conjunction",
        "conjuncts": [
            {"attr": "color", "op": "eq", "value": target_color},
            {"attr": "shape", "op": "eq", "value": target_shape},
        ],
    }
    post_rule = {"kind": "negation", "inner": pre_rule}

    expected = {"final_correct_item_id": post_id, "pre_drift_correct_item_id": pre_id}

    episode_id = _stable_episode_id(seed, severity)

    return EpisodeSpec(
        episode_id=episode_id,
        benchmark_version="1.1.0",
        generation_seed=seed,
        template_family="symbolic_negation_v1",
        template_version="1.0.0",
        difficulty_profile=dict(knobs),
        drift_event=drift,
        pre_drift_rule=pre_rule,
        post_drift_rule=post_rule,
        expected_outputs=expected,
        answer_schema_ref="item_id",
        drift_onset_turn=1,
        detection_eligible_turns=(1,),
        ambiguity_window_turns=(1,),
        clarification_eligible_turns=(),
        final_resolution_turn=2,
        recovery_probe_turns=(),
        uncertainty_ceiling=0.4,
        final_calibration_epsilon=0.05,
        final_success_condition=(
            "typed answer item_id equals expected_outputs.final_correct_item_id"
        ),
        acceptable_final_modes=frozenset({"ANSWER"}),
        scoring_profile_version="1.1.0",
        scored_post_drift_turns=(1, 2),
        calibration_eligible_turns=(1, 2),
        requires_final_answer=True,
        final_state_unresolved=False,
        items=tuple(items),
        prompt_preamble=_render_preamble(items, pre_rule, post_id, drift_severity),
    )


def _render_preamble(
    items: list[dict[str, str]],
    pre_rule: Mapping[str, Any],
    _post_target: str,
    severity: DriftSeverity,
) -> str:
    """Human-readable episode text for debugging (not a scoring input)."""
    lines = [
        "[RULE_INDUCTION] Items:",
        *[json.dumps(it) for it in items],
        f"[STABLE_APPLICATION] Apply rule: {json.dumps(pre_rule)}",
        f"[DRIFT_EVENT] NEGATION drift injected (severity={severity.value}).",
        "[DRIFT_RESPONSE_WINDOW] Report drift suspicion and calibrated confidence.",
        "[FINAL_RESOLUTION] Output typed JSON per schema.",
    ]
    return "\n".join(lines)


def episode_spec_to_dict(spec: EpisodeSpec) -> dict[str, Any]:
    """Serialize spec for `episode_spec.json`."""
    de = spec.drift_event
    return {
        "episode_id": spec.episode_id,
        "benchmark_version": spec.benchmark_version,
        "generation_seed": spec.generation_seed,
        "template_family": spec.template_family,
        "template_version": spec.template_version,
        "difficulty_profile": dict(spec.difficulty_profile),
        "drift_event": {
            "drift_type": de.drift_type.value,
            "drift_severity": de.drift_severity.value,
            "drift_onset_turn": de.drift_onset_turn,
            "drift_parameters": dict(de.drift_parameters),
        },
        "pre_drift_rule": dict(spec.pre_drift_rule),
        "post_drift_rule": dict(spec.post_drift_rule),
        "expected_outputs": dict(spec.expected_outputs),
        "answer_schema_ref": spec.answer_schema_ref,
        "drift_onset_turn": spec.drift_onset_turn,
        "detection_eligible_turns": list(spec.detection_eligible_turns),
        "ambiguity_window_turns": list(spec.ambiguity_window_turns),
        "clarification_eligible_turns": list(spec.clarification_eligible_turns),
        "final_resolution_turn": spec.final_resolution_turn,
        "recovery_probe_turns": list(spec.recovery_probe_turns),
        "uncertainty_ceiling": spec.uncertainty_ceiling,
        "final_calibration_epsilon": spec.final_calibration_epsilon,
        "final_success_condition": spec.final_success_condition,
        "acceptable_final_modes": sorted(spec.acceptable_final_modes),
        "requires_final_answer": spec.requires_final_answer,
        "final_state_unresolved": spec.final_state_unresolved,
        "scoring_profile_version": spec.scoring_profile_version,
        "scored_post_drift_turns": list(spec.scored_post_drift_turns),
        "calibration_eligible_turns": list(spec.calibration_eligible_turns),
        "items": [dict(x) for x in spec.items],
        "prompt_preamble": spec.prompt_preamble,
    }
