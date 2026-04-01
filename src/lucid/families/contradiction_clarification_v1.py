"""Contradiction / clarification drift — template `contradiction_clarification_v1` / v1.0.0."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from random import Random
from typing import Any, Literal

from lucid.models import DriftEvent, DriftSeverity, DriftType, EpisodeSpec

ContradictionState = Literal["unresolved", "resolved"]


def _stable_episode_id(seed: int, severity: str, state: str) -> str:
    h = hashlib.sha256(
        f"contradiction_clarification_v1:{seed}:{severity}:{state}".encode()
    ).hexdigest()[:16]
    return f"ep_cc_{h}"


def _mk_items(rng: Random, n_items: int, n_colors: int, n_shapes: int) -> list[dict[str, str]]:
    """Build `n_items` items with unique `(color, shape)` pairs."""
    pairs: list[tuple[int, int]] = [(c, s) for c in range(n_colors) for s in range(n_shapes)]
    if n_items > len(pairs):  # pragma: no cover
        msg = "n_items exceeds unique attribute combinations"
        raise ValueError(msg)
    rng.shuffle(pairs)
    items: list[dict[str, str]] = []
    for i in range(n_items):
        c_i, s_i = pairs[i]
        items.append({"id": f"I{i + 1}", "color": f"C{c_i}", "shape": f"S{s_i}"})
    return items


def _knobs_for_severity(drift_severity: DriftSeverity) -> dict[str, int]:
    if drift_severity == DriftSeverity.LOW:
        return {"n_items": 4, "n_colors": 3, "n_shapes": 2}
    if drift_severity == DriftSeverity.HIGH:
        return {"n_items": 12, "n_colors": 4, "n_shapes": 3}
    return {"n_items": 8, "n_colors": 4, "n_shapes": 2}


def generate_episode(
    *,
    seed: int,
    drift_severity: DriftSeverity = DriftSeverity.MEDIUM,
    contradiction_state: ContradictionState = "unresolved",
) -> EpisodeSpec:
    """Build a deterministic `EpisodeSpec` for the contradiction / clarification family."""
    rng = Random(seed)
    severity = drift_severity.value
    base_knobs = _knobs_for_severity(drift_severity)
    n_items = base_knobs["n_items"]
    n_colors = base_knobs["n_colors"]
    n_shapes = base_knobs["n_shapes"]
    items = _mk_items(rng, n_items, n_colors, n_shapes)

    # Pre-drift: match (color, shape) of items[0]; post-drift: conflicting claim for another item.
    rng.shuffle(items)
    pre_target = items[0]
    alt_pool = [it for it in items[1:] if it["id"] != pre_target["id"]]
    post_claim = rng.choice(alt_pool)

    pre_rule: dict[str, Any] = {
        "kind": "unique_item_by_predicate",
        "predicate": {
            "kind": "conjunction",
            "conjuncts": [
                {"attr": "color", "op": "eq", "value": pre_target["color"]},
                {"attr": "shape", "op": "eq", "value": pre_target["shape"]},
            ],
        },
        "declared_correct_id": pre_target["id"],
    }
    # Contradictory instruction: claims a different item is correct (same schema, different id).
    post_rule: dict[str, Any] = {
        "kind": "contradiction_claim",
        "conflicts_with_pre": True,
        "claimed_correct_id": post_claim["id"],
        "pre_claimed_id": pre_target["id"],
    }

    clarifier_present = contradiction_state == "resolved"
    if clarifier_present:
        # Authoritative resolution: second claim wins; deterministic typed rule.
        post_rule = {
            "kind": "resolved_by_clarifier",
            "clarifier_text_key": "second_instruction_authoritative",
            "authoritative_correct_id": post_claim["id"],
            "supersedes_pre_claim": True,
        }

    drift = DriftEvent(
        drift_type=DriftType.CONTRADICTION,
        drift_severity=drift_severity,
        drift_onset_turn=1,
        drift_parameters={
            "shape": "competing_correctness_claims",
            "pre_claim_item_id": pre_target["id"],
            "post_claim_item_id": post_claim["id"],
            "clarifier_applied": clarifier_present,
        },
    )

    final_unresolved = contradiction_state == "unresolved"
    if final_unresolved:
        expected: dict[str, Any] = {
            "final_correct_item_id": None,
            "metacognitive_preference": "guarded_uncertainty",
        }
        acceptable = frozenset({"ANSWER", "ABSTAIN", "CLARIFY"})
        target_behavior = "PREFER_ABSTAIN_CLARIFY_OR_LOW_CONFIDENCE"
        requires_final = False
    else:
        expected = {
            "final_correct_item_id": post_claim["id"],
            "metacognitive_preference": "answer_after_resolution",
        }
        acceptable = frozenset({"ANSWER"})
        target_behavior = "ANSWER_WITH_POST_CLARIFICATION_RULE"
        requires_final = True

    difficulty_profile: dict[str, Any] = {
        **base_knobs,
        "drift_severity": severity,
        "contradiction_state": contradiction_state,
        "clarifier_present": clarifier_present,
        "target_behavior": target_behavior,
    }

    episode_id = _stable_episode_id(seed, severity, contradiction_state)

    preamble = _render_preamble(
        items=items,
        pre_rule=pre_rule,
        pre_target=pre_target,
        post_claim=post_claim,
        contradiction_state=contradiction_state,
        drift_severity=drift_severity,
    )

    return EpisodeSpec(
        episode_id=episode_id,
        benchmark_version="1.1.0",
        generation_seed=seed,
        template_family="contradiction_clarification_v1",
        template_version="1.0.0",
        difficulty_profile=difficulty_profile,
        drift_event=drift,
        pre_drift_rule=pre_rule,
        post_drift_rule=post_rule,
        expected_outputs=expected,
        answer_schema_ref="item_id",
        drift_onset_turn=1,
        detection_eligible_turns=(1,),
        ambiguity_window_turns=(1, 2),
        clarification_eligible_turns=(1, 2) if final_unresolved else (1,),
        final_resolution_turn=2,
        recovery_probe_turns=(),
        uncertainty_ceiling=0.4,
        final_calibration_epsilon=0.05,
        final_success_condition=(
            "if final_state_unresolved: prefer ABSTAIN/CLARIFY/low confidence; "
            "else typed answer equals expected_outputs.final_correct_item_id"
        ),
        acceptable_final_modes=acceptable,
        scoring_profile_version="1.1.0",
        scored_post_drift_turns=(1, 2),
        calibration_eligible_turns=(1, 2),
        requires_final_answer=requires_final,
        final_state_unresolved=final_unresolved,
        items=tuple(items),
        prompt_preamble=preamble,
    )


def _render_preamble(
    *,
    items: list[dict[str, str]],
    pre_rule: Mapping[str, Any],
    pre_target: Mapping[str, str],
    post_claim: Mapping[str, str],
    contradiction_state: ContradictionState,
    drift_severity: DriftSeverity,
) -> str:
    """Human-readable episode text (debugging; not sole scoring input)."""
    lines = [
        "[RULE_INDUCTION] Items:",
        *[json.dumps(it) for it in items],
        f"[STABLE_APPLICATION] Declared correct item by initial rule: {pre_target['id']}",
        f"[DRIFT_EVENT] CONTRADICTION (severity={drift_severity.value}): "
        f"a new instruction claims the correct item is {post_claim['id']}, "
        f"conflicting with the prior claim {pre_target['id']}.",
    ]
    if contradiction_state == "unresolved":
        lines.append(
            "[AMBIGUITY_WINDOW] No resolution provided — a well-calibrated model should "
            "not treat this as uniquely answerable; prefer clarification, abstention, or "
            "guarded low confidence."
        )
    else:
        lines.append(
            "[CLARIFICATION] The second instruction is authoritative: the governing rule "
            f"selects item {post_claim['id']} as the unique correct answer."
        )
    lines.append("[FINAL_RESOLUTION] Output typed JSON per schema.")
    return "\n".join(lines)


def episode_spec_to_dict(spec: EpisodeSpec) -> dict[str, Any]:
    """Serialize spec for `episode_spec.json`."""
    de = spec.drift_event
    out: dict[str, Any] = {
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
    return out
