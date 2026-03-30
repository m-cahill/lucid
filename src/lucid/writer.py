"""Write audit-ready episode bundles (`LUCID_ARTIFACT_BUNDLE_CONTRACT.md`)."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from lucid import __version__
from lucid.canonical_json import write_canonical
from lucid.hashing import sha256_file
from lucid.models import EpisodeResponse, EpisodeSpec, TurnRecord
from lucid.scorer import EpisodeScore


def _response_to_dict(r: EpisodeResponse) -> dict[str, Any]:
    return {
        "answer": r.answer,
        "confidence": r.confidence,
        "response_mode": r.response_mode,
        "drift_detected": r.drift_detected,
        "rationale_stub": r.rationale_stub,
    }


def build_episode_result(
    spec: EpisodeSpec,
    *,
    model_identifier: str,
    turns: Sequence[TurnRecord],
    final_response: EpisodeResponse,
    scores: EpisodeScore,
    parse_status: str = "OK",
) -> dict[str, Any]:
    """Episode result artifact payload."""
    turn_payload = [{"turn": tr.turn, "response": _response_to_dict(tr.response)} for tr in turns]
    return {
        "episode_id": spec.episode_id,
        "benchmark_version": spec.benchmark_version,
        "model_identifier": model_identifier,
        "output_schema_version": "1.1.0",
        "parser_version": __version__,
        "scorer_version": __version__,
        "typed_episode_response": _response_to_dict(final_response),
        "parse_status": parse_status,
        "scores": {
            "D": scores.D,
            "L": scores.L,
            "O": scores.O,
            "A": scores.A,
            "C": scores.C,
            "LUCID_SCORE_EPISODE": scores.lucid_score_episode,
        },
        "diagnostics": {
            "turns": turn_payload,
            "scoring_profile_version": spec.scoring_profile_version,
        },
        "success_flags": {"episode_complete": True},
    }


def write_bundle(
    out_root: str | Path,
    *,
    spec_dict: Mapping[str, Any],
    episode_result: Mapping[str, Any],
    created_by: str = "lucid-local",
) -> Path:
    """Write `episode_<id>/` with manifest and hashes."""
    out_root = Path(out_root)
    eid = str(spec_dict["episode_id"])
    ep_dir = out_root / f"episode_{eid}"
    ep_dir.mkdir(parents=True, exist_ok=True)

    spec_path = ep_dir / "episode_spec.json"
    result_path = ep_dir / "episode_result.json"
    manifest_path = ep_dir / "bundle_manifest.json"
    hashes_path = ep_dir / "hashes.json"

    write_canonical(str(spec_path), dict(spec_dict))
    write_canonical(str(result_path), dict(episode_result))

    manifest = {
        "bundle_version": "1.0.0",
        "bundle_type": "lucid_episode_bundle",
        "episode_id": eid,
        "benchmark_version": spec_dict["benchmark_version"],
        "artifact_files": [
            "episode_spec.json",
            "episode_result.json",
            "bundle_manifest.json",
        ],
        "hash_manifest_file": "hashes.json",
        "created_by": created_by,
        "created_at_mode": "non_semantic",
    }
    write_canonical(str(manifest_path), manifest)

    hashes = {
        "episode_spec.json": sha256_file(spec_path),
        "episode_result.json": sha256_file(result_path),
        "bundle_manifest.json": sha256_file(manifest_path),
    }
    write_canonical(str(hashes_path), hashes)

    return ep_dir
