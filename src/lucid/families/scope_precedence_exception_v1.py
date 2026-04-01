"""Scope / precedence / exception drift — template `scope_precedence_exception_v1` / v1.0.0."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Mapping
from random import Random
from typing import Any, Literal

from lucid.models import DriftEvent, DriftSeverity, DriftType, EpisodeSpec

Family3Subtype = Literal["scope", "precedence", "exception"]


def _stable_episode_id(seed: int, severity: str, drift_type: str) -> str:
    h = hashlib.sha256(
        f"scope_precedence_exception_v1:{seed}:{severity}:{drift_type}".encode()
    ).hexdigest()[:16]
    return f"ep_spe_{h}"


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


def _min_id(items: list[dict[str, str]]) -> str:
    return min(it["id"] for it in items)


def _mk_items_scope_pair(
    rng: Random, n_items: int, n_colors: int, n_shapes: int
) -> tuple[list[dict[str, str]], str, dict[str, str], dict[str, str]]:
    """Guarantee two items share one color (for scope narrowing); unique (color, shape) pairs."""
    pairs: list[tuple[int, int]] = [(c, s) for c in range(n_colors) for s in range(n_shapes)]
    if n_items > len(pairs):  # pragma: no cover
        raise ValueError("n_items exceeds unique attribute combinations")
    rng.shuffle(pairs)
    anchor_c: int | None = None
    anchor_pair: tuple[tuple[int, int], tuple[int, int]] | None = None
    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            if pairs[i][0] == pairs[j][0]:
                anchor_c = pairs[i][0]
                anchor_pair = (pairs[i], pairs[j])
                break
        if anchor_pair is not None:
            break
    if anchor_pair is None or anchor_c is None:  # pragma: no cover
        msg = "scope episode: color grid cannot place two items on same color"
        raise RuntimeError(msg)
    used = {anchor_pair[0], anchor_pair[1]}
    rest = [p for p in pairs if p not in used]
    rng.shuffle(rest)
    chosen = [anchor_pair[0], anchor_pair[1]] + rest[: n_items - 2]
    rng.shuffle(chosen)
    items: list[dict[str, str]] = []
    for i in range(n_items):
        c_i, s_i = chosen[i]
        items.append({"id": f"I{i + 1}", "color": f"C{c_i}", "shape": f"S{s_i}"})
    pred_color = f"C{anchor_c}"
    same_c = [it for it in items if it["color"] == pred_color]
    i_small, i_large = sorted(same_c, key=lambda x: x["id"])[:2]
    return items, pred_color, i_small, i_large


def _generate_scope_episode(
    *,
    seed: int,
    drift_severity: DriftSeverity,
    rng: Random,
    base_knobs: dict[str, int],
) -> tuple[EpisodeSpec, dict[str, Any]]:
    """Scope: predicate applies to a color; universe shrinks from ALL to subset S."""
    n_items = base_knobs["n_items"]
    n_colors = base_knobs["n_colors"]
    n_shapes = base_knobs["n_shapes"]
    items, pred_color, i_small, _ = _mk_items_scope_pair(rng, n_items, n_colors, n_shapes)

    # Subset S: all items except i_small, includes i_large and distractors without pred_color.
    scope_after_ids = sorted([it["id"] for it in items if it["id"] != i_small["id"]])
    scope_before = "ALL"
    scope_after = scope_after_ids

    pred_matches_all = [it for it in items if it["color"] == pred_color]
    pred_matches_scoped = [
        it for it in items if it["color"] == pred_color and it["id"] in scope_after_ids
    ]

    pre_id = _min_id(pred_matches_all)
    post_id = _min_id(pred_matches_scoped)

    if pre_id == post_id:  # pragma: no cover
        msg = "scope episode invariant: pre/post answers must differ"
        raise RuntimeError(msg)

    pre_rule: dict[str, Any] = {
        "kind": "unique_item_by_predicate",
        "scope": scope_before,
        "predicate": {"attr": "color", "op": "eq", "value": pred_color},
        "tie_break": "min_item_id",
    }
    post_rule: dict[str, Any] = {
        "kind": "unique_item_by_predicate",
        "scope": {"type": "explicit_ids", "ids": scope_after},
        "predicate": {"attr": "color", "op": "eq", "value": pred_color},
        "tie_break": "min_item_id",
    }

    drift = DriftEvent(
        drift_type=DriftType.SCOPE,
        drift_severity=drift_severity,
        drift_onset_turn=1,
        drift_parameters={
            "shape": "scope_narrowing",
            "predicate_color": pred_color,
            "scope_before": scope_before,
            "scope_after_ids": scope_after,
        },
    )

    meta: dict[str, Any] = {
        "scope_before": scope_before,
        "scope_after": scope_after,
        "predicate_color": pred_color,
    }

    return (
        EpisodeSpec(
            episode_id=_stable_episode_id(seed, drift_severity.value, DriftType.SCOPE.value),
            benchmark_version="1.1.0",
            generation_seed=seed,
            template_family="scope_precedence_exception_v1",
            template_version="1.0.0",
            difficulty_profile=dict(
                **base_knobs,
                drift_severity=drift_severity.value,
                family3_subtype="scope",
                drift_subtype="scope",
                target_behavior="ANSWER_AFTER_SCOPE_NARROW",
                **meta,
            ),
            drift_event=drift,
            pre_drift_rule=pre_rule,
            post_drift_rule=post_rule,
            expected_outputs={
                "final_correct_item_id": post_id,
                "pre_drift_correct_item_id": pre_id,
            },
            answer_schema_ref="item_id",
            drift_onset_turn=1,
            detection_eligible_turns=(1,),
            ambiguity_window_turns=(1, 2),
            clarification_eligible_turns=(1,),
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
            prompt_preamble=_render_scope_preamble(
                items=items,
                pred_color=pred_color,
                pre_id=pre_id,
                post_id=post_id,
                scope_after=scope_after,
                drift_severity=drift_severity,
            ),
        ),
        meta,
    )


def _apply_precedence(
    items: list[dict[str, str]],
    pa: Callable[[dict[str, str]], bool],
    pb: Callable[[dict[str, str]], bool],
    order: Literal["A_over_B", "B_over_A"],
) -> str:
    """First rule in order wins; deterministic min id within chosen set."""
    a_m = [it for it in items if pa(it)]
    b_m = [it for it in items if pb(it)]
    if order == "A_over_B":
        if a_m:
            return _min_id(a_m)
        return _min_id(b_m)
    if b_m:
        return _min_id(b_m)
    return _min_id(a_m)


def _generate_precedence_episode(
    *,
    seed: int,
    drift_severity: DriftSeverity,
    rng: Random,
    base_knobs: dict[str, int],
) -> tuple[EpisodeSpec, dict[str, Any]]:
    """Precedence: two unique (color, shape) predicates; order of application swaps."""
    n_items = base_knobs["n_items"]
    n_colors = base_knobs["n_colors"]
    n_shapes = base_knobs["n_shapes"]
    items = _mk_items(rng, n_items, n_colors, n_shapes)
    rng.shuffle(items)
    item_a, item_b = items[0], items[1]

    def pa(it: dict[str, str]) -> bool:
        return it["color"] == item_a["color"] and it["shape"] == item_a["shape"]

    def pb(it: dict[str, str]) -> bool:
        return it["color"] == item_b["color"] and it["shape"] == item_b["shape"]

    pre_id = _apply_precedence(items, pa, pb, "A_over_B")
    post_id = _apply_precedence(items, pa, pb, "B_over_A")

    if pre_id == post_id:  # pragma: no cover
        msg = "precedence episode invariant: pre/post answers must differ"
        raise RuntimeError(msg)

    conj_a: dict[str, Any] = {
        "kind": "conjunction",
        "conjuncts": [
            {"attr": "color", "op": "eq", "value": item_a["color"]},
            {"attr": "shape", "op": "eq", "value": item_a["shape"]},
        ],
    }
    conj_b: dict[str, Any] = {
        "kind": "conjunction",
        "conjuncts": [
            {"attr": "color", "op": "eq", "value": item_b["color"]},
            {"attr": "shape", "op": "eq", "value": item_b["shape"]},
        ],
    }

    pre_rule: dict[str, Any] = {
        "kind": "precedence_pair",
        "rule_a": {"predicate": conj_a},
        "rule_b": {"predicate": conj_b},
        "order": "A_over_B",
        "tie_break": "min_item_id",
    }
    post_rule: dict[str, Any] = {
        "kind": "precedence_pair",
        "rule_a": {"predicate": conj_a},
        "rule_b": {"predicate": conj_b},
        "order": "B_over_A",
        "tie_break": "min_item_id",
    }

    drift = DriftEvent(
        drift_type=DriftType.PRECEDENCE,
        drift_severity=drift_severity,
        drift_onset_turn=1,
        drift_parameters={
            "shape": "precedence_reversal",
            "precedence_before": "A_over_B",
            "precedence_after": "B_over_A",
            "rule_count": 2,
        },
    )

    meta: dict[str, Any] = {
        "precedence_before": "A_over_B",
        "precedence_after": "B_over_A",
        "rule_count": 2,
        "rule_a_item_id": item_a["id"],
        "rule_b_item_id": item_b["id"],
    }

    return (
        EpisodeSpec(
            episode_id=_stable_episode_id(seed, drift_severity.value, DriftType.PRECEDENCE.value),
            benchmark_version="1.1.0",
            generation_seed=seed,
            template_family="scope_precedence_exception_v1",
            template_version="1.0.0",
            difficulty_profile=dict(
                **base_knobs,
                drift_severity=drift_severity.value,
                family3_subtype="precedence",
                drift_subtype="precedence",
                target_behavior="ANSWER_AFTER_PRECEDENCE_CHANGE",
                **meta,
            ),
            drift_event=drift,
            pre_drift_rule=pre_rule,
            post_drift_rule=post_rule,
            expected_outputs={
                "final_correct_item_id": post_id,
                "pre_drift_correct_item_id": pre_id,
            },
            answer_schema_ref="item_id",
            drift_onset_turn=1,
            detection_eligible_turns=(1,),
            ambiguity_window_turns=(1, 2),
            clarification_eligible_turns=(1,),
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
            prompt_preamble=_render_precedence_preamble(
                items=items,
                item_a=item_a,
                item_b=item_b,
                pre_id=pre_id,
                post_id=post_id,
                drift_severity=drift_severity,
            ),
        ),
        meta,
    )


def _generate_exception_episode(
    *,
    seed: int,
    drift_severity: DriftSeverity,
    rng: Random,
    base_knobs: dict[str, int],
) -> tuple[EpisodeSpec, dict[str, Any]]:
    """Exception: general rule on class X; post-drift excludes exception class E."""
    n_items = base_knobs["n_items"]
    n_colors = base_knobs["n_colors"]
    n_shapes = base_knobs["n_shapes"]
    items = _mk_items(rng, n_items, n_colors, n_shapes)

    # Class X: union of two colors; min id among X; exception excludes that id; new min differs.
    by_color: dict[str, list[dict[str, str]]] = {}
    for it in items:
        by_color.setdefault(it["color"], []).append(it)
    colors = list(by_color.keys())
    if len(colors) < 2:  # pragma: no cover
        msg = "exception episode: need at least two colors"
        raise RuntimeError(msg)
    rng.shuffle(colors)
    class_x_colors: list[str] = []
    pre_winner = ""
    post_id = ""
    found = False
    for i in range(len(colors)):
        for j in range(i + 1, len(colors)):
            cx, cy = colors[i], colors[j]
            cand_colors = sorted({cx, cy})
            cand_items = [it for it in items if it["color"] in cand_colors]
            if len(cand_items) < 2:
                continue
            pw = _min_id(cand_items)
            pool = [it for it in cand_items if it["id"] != pw]
            pid = _min_id(pool)
            if pw != pid:
                class_x_colors = cand_colors
                pre_winner = pw
                post_id = pid
                found = True
                break
        if found:
            break
    if not found:  # pragma: no cover
        msg = "exception episode: could not find a two-color class with >=2 items"
        raise RuntimeError(msg)
    # Exception: exclude the pre_winner item id from the class (by id).
    exception_ids = [pre_winner]

    pre_rule: dict[str, Any] = {
        "kind": "class_rule",
        "class_x": {"colors": class_x_colors},
        "selection": "min_item_id",
    }
    post_rule: dict[str, Any] = {
        "kind": "class_rule_with_exception",
        "class_x": {"colors": class_x_colors},
        "exception": {"excluded_item_ids": exception_ids},
        "selection": "min_item_id",
    }

    drift = DriftEvent(
        drift_type=DriftType.EXCEPTION,
        drift_severity=drift_severity,
        drift_onset_turn=1,
        drift_parameters={
            "shape": "exception_insertion",
            "general_class": class_x_colors,
            "exception_item_ids": exception_ids,
        },
    )

    meta: dict[str, Any] = {
        "general_rule": f"min_item_id among items with color in {class_x_colors}",
        "exception_class": exception_ids,
        "exception_trigger": "excluded_item_ids",
    }

    return (
        EpisodeSpec(
            episode_id=_stable_episode_id(seed, drift_severity.value, DriftType.EXCEPTION.value),
            benchmark_version="1.1.0",
            generation_seed=seed,
            template_family="scope_precedence_exception_v1",
            template_version="1.0.0",
            difficulty_profile=dict(
                **base_knobs,
                drift_severity=drift_severity.value,
                family3_subtype="exception",
                drift_subtype="exception",
                target_behavior="ANSWER_AFTER_EXCEPTION",
                **meta,
            ),
            drift_event=drift,
            pre_drift_rule=pre_rule,
            post_drift_rule=post_rule,
            expected_outputs={
                "final_correct_item_id": post_id,
                "pre_drift_correct_item_id": pre_winner,
            },
            answer_schema_ref="item_id",
            drift_onset_turn=1,
            detection_eligible_turns=(1,),
            ambiguity_window_turns=(1, 2),
            clarification_eligible_turns=(1,),
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
            prompt_preamble=_render_exception_preamble(
                items=items,
                class_x_colors=class_x_colors,
                pre_winner=pre_winner,
                post_id=post_id,
                exception_ids=exception_ids,
                drift_severity=drift_severity,
            ),
        ),
        meta,
    )


def generate_episode(
    *,
    seed: int,
    drift_severity: DriftSeverity = DriftSeverity.MEDIUM,
    family_subtype: Family3Subtype = "scope",
) -> EpisodeSpec:
    """Build a deterministic `EpisodeSpec` for the scope / precedence / exception family."""
    rng = Random(seed)
    base_knobs = _knobs_for_severity(drift_severity)
    if family_subtype == "scope":
        spec, _meta = _generate_scope_episode(
            seed=seed, drift_severity=drift_severity, rng=rng, base_knobs=base_knobs
        )
        return spec
    if family_subtype == "precedence":
        spec, _meta = _generate_precedence_episode(
            seed=seed, drift_severity=drift_severity, rng=rng, base_knobs=base_knobs
        )
        return spec
    spec, _meta = _generate_exception_episode(
        seed=seed, drift_severity=drift_severity, rng=rng, base_knobs=base_knobs
    )
    return spec


def _render_scope_preamble(
    *,
    items: list[dict[str, str]],
    pred_color: str,
    pre_id: str,
    post_id: str,
    scope_after: list[str],
    drift_severity: DriftSeverity,
) -> str:
    lines = [
        "[RULE_INDUCTION] Items:",
        *[json.dumps(it) for it in items],
        f"[STABLE_APPLICATION] Predicate: color == {pred_color}; scope: ALL items; "
        f"tie-break min id → correct item {pre_id}.",
        f"[DRIFT_EVENT] SCOPE (severity={drift_severity.value}): rule applies only to subset "
        f"with ids {scope_after}.",
        f"[POST_DRIFT] Same predicate under narrowed scope → correct item {post_id}.",
        "[FINAL_RESOLUTION] Output typed JSON per schema.",
    ]
    return "\n".join(lines)


def _render_precedence_preamble(
    *,
    items: list[dict[str, str]],
    item_a: Mapping[str, str],
    item_b: Mapping[str, str],
    pre_id: str,
    post_id: str,
    drift_severity: DriftSeverity,
) -> str:
    lines = [
        "[RULE_INDUCTION] Items:",
        *[json.dumps(it) for it in items],
        f"[STABLE_APPLICATION] Rules: A = color {item_a['color']}, B = color {item_b['color']}; "
        f"order A overrides B → item {pre_id}.",
        f"[DRIFT_EVENT] PRECEDENCE (severity={drift_severity.value}): order B overrides A.",
        f"[POST_DRIFT] Controlling order changed → correct item {post_id}.",
        "[FINAL_RESOLUTION] Output typed JSON per schema.",
    ]
    return "\n".join(lines)


def _render_exception_preamble(
    *,
    items: list[dict[str, str]],
    class_x_colors: list[str],
    pre_winner: str,
    post_id: str,
    exception_ids: list[str],
    drift_severity: DriftSeverity,
) -> str:
    lines = [
        "[RULE_INDUCTION] Items:",
        *[json.dumps(it) for it in items],
        (
            f"[STABLE_APPLICATION] Class X: colors in {class_x_colors}; "
            f"rule: min item id → {pre_winner}."
        ),
        (
            f"[DRIFT_EVENT] EXCEPTION (severity={drift_severity.value}): "
            f"exclude items {exception_ids} from the class."
        ),
        f"[POST_DRIFT] Revised rule → correct item {post_id}.",
        "[FINAL_RESOLUTION] Output typed JSON per schema.",
    ]
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
