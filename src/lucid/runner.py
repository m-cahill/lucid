"""Local minimal green path: generate → score → bundle."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from lucid.families.symbolic_negation_v1 import episode_spec_to_dict, generate_episode
from lucid.models import EpisodeResponse, EpisodeSpec, TurnRecord
from lucid.scorer import score_episode
from lucid.writer import build_episode_result, write_bundle


def fixture_turns(spec: EpisodeSpec) -> Sequence[TurnRecord]:
    """Deterministic multi-turn fixture: cautious intermediate + correct final."""
    correct = str(spec.expected_outputs["final_correct_item_id"])
    return (
        TurnRecord(
            turn=1,
            response=EpisodeResponse(
                answer=None,
                confidence=0.35,
                response_mode="CLARIFY",
                drift_detected="CONFIRMED",
            ),
        ),
        TurnRecord(
            turn=2,
            response=EpisodeResponse(
                answer=correct,
                confidence=0.95,
                response_mode="ANSWER",
                drift_detected="CONFIRMED",
            ),
        ),
    )


def run_smoke(*, seed: int, out_root: Path, model_id: str = "fixture") -> tuple[Path, float]:
    """Execute one deterministic smoke run; returns bundle path and score."""
    spec = generate_episode(seed=seed)
    turns = fixture_turns(spec)
    final = turns[-1].response
    scores = score_episode(spec, turns)
    spec_dict = episode_spec_to_dict(spec)
    result = build_episode_result(
        spec,
        model_identifier=model_id,
        turns=turns,
        final_response=final,
        scores=scores,
    )
    bundle = write_bundle(out_root, spec_dict=spec_dict, episode_result=result)
    return bundle, scores.lucid_score_episode


def main() -> None:
    """CLI entry (`python -m lucid.runner` or console script)."""
    p = argparse.ArgumentParser(description="LUCID local smoke run")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--out", type=Path, default=Path("out") / "smoke")
    args = p.parse_args()
    bundle, s = run_smoke(seed=args.seed, out_root=args.out)
    print(f"bundle={bundle}")
    print(f"LUCID_SCORE_EPISODE={s:.6f}")


if __name__ == "__main__":
    main()
