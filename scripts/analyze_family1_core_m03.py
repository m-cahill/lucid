"""Structural + deterministic baseline analytics for Family 1 M03 canonical pack."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from lucid.families.symbolic_negation_v1 import generate_episode
from lucid.models import DriftSeverity, EpisodeSpec
from lucid.packs import family1_core_m03 as p
from lucid.runner import fixture_turns
from lucid.scorer import score_episode


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _structural_row(spec: Mapping[str, Any]) -> dict[str, Any]:
    dp = spec["difficulty_profile"]
    de = spec["drift_event"]
    return {
        "n_items": int(dp["n_items"]),
        "n_colors": int(dp["n_colors"]),
        "n_shapes": int(dp["n_shapes"]),
        "drift_severity": str(dp["drift_severity"]),
        "drift_type": str(de["drift_type"]),
        "predicate": str(de["drift_parameters"].get("predicate", "")),
    }


def analyze_structural(data: dict[str, Any]) -> dict[str, Any]:
    """Bucket-level design stats and duplicate checks."""
    episodes = data["episodes"]
    by_bucket: dict[str, list[dict[str, Any]]] = defaultdict(list)
    episode_ids: list[str] = []

    for row in episodes:
        bucket = str(row["difficulty_bucket"])
        spec = row["episode_spec"]
        episode_ids.append(str(spec["episode_id"]))
        by_bucket[bucket].append(_structural_row(spec))

    dup_ids = [eid for eid, c in Counter(episode_ids).items() if c > 1]

    def bucket_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
        if not rows:
            return {"episode_count": 0}
        keys = ("n_items", "n_colors", "n_shapes", "drift_type", "predicate")
        first = rows[0]
        uniform = all(all(r[k] == first[k] for k in keys) for r in rows)
        return {
            "episode_count": len(rows),
            "structural_parameters": {k: first[k] for k in keys},
            "uniform_within_bucket": uniform,
        }

    out: dict[str, Any] = {
        "pack_id": data.get("pack_id"),
        "benchmark_version": data.get("benchmark_version"),
        "episode_count": len(episodes),
        "duplicate_episode_ids": dup_ids,
        "buckets": {
            "LOW": bucket_summary(by_bucket["LOW"]),
            "MEDIUM": bucket_summary(by_bucket["MEDIUM"]),
            "HIGH": bucket_summary(by_bucket["HIGH"]),
        },
        "ladder_design": {
            "low_n_items": by_bucket["LOW"][0]["n_items"] if by_bucket["LOW"] else None,
            "medium_n_items": by_bucket["MEDIUM"][0]["n_items"] if by_bucket["MEDIUM"] else None,
            "high_n_items": by_bucket["HIGH"][0]["n_items"] if by_bucket["HIGH"] else None,
            "attribute_cardinality_note": (
                "Per symbolic_negation_v1: LOW/MEDIUM/HIGH differ in n_items and "
                "color×shape grid size (see n_colors × n_shapes)."
            ),
        },
    }
    return out


def _score_one(spec: EpisodeSpec) -> dict[str, float]:
    turns = fixture_turns(spec)
    s = score_episode(spec, turns)
    return {
        "D": float(s.D),
        "L": float(s.L),
        "O": float(s.O),
        "A": float(s.A),
        "C": float(s.C),
        "lucid_score_episode": float(s.lucid_score_episode),
    }


def deterministic_baseline_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Full pack: regenerate spec from manifest row, fixture turns, official scorer."""
    rows_out: list[dict[str, Any]] = []
    for row in data["episodes"]:
        spec_dict = row["episode_spec"]
        seed = int(spec_dict["generation_seed"])
        sev = DriftSeverity[row["difficulty_bucket"]]
        spec = generate_episode(seed=seed, drift_severity=sev)
        assert spec.episode_id == spec_dict["episode_id"]
        sc = _score_one(spec)
        rows_out.append(
            {
                "episode_id": spec.episode_id,
                "generation_seed": seed,
                "difficulty_bucket": row["difficulty_bucket"],
                "m01_transport_fixture_id": row.get("m01_transport_fixture_id"),
                **sc,
            }
        )
    return rows_out


def write_baseline_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "episode_id",
        "generation_seed",
        "difficulty_bucket",
        "m01_transport_fixture_id",
        "D",
        "L",
        "O",
        "A",
        "C",
        "lucid_score_episode",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def aggregate_baseline_by_bucket(rows: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    by_b: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        by_b[str(r["difficulty_bucket"])].append(r)
    out: dict[str, dict[str, float]] = {}
    for b, lst in by_b.items():
        n = len(lst)
        keys = ("D", "L", "O", "A", "C", "lucid_score_episode")
        out[b] = {k: sum(float(x[k]) for x in lst) / n for k in keys}
    return out


def main(argv: list[str] | None = None) -> int:
    root = _repo_root()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--manifest",
        type=Path,
        default=root / p.CANONICAL_MANIFEST_RELPATH,
        help="Path to family1_core_m03_manifest.json",
    )
    ap.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="Write structural + baseline summary JSON (default: stdout only)",
    )
    ap.add_argument(
        "--baseline-csv",
        type=Path,
        default=None,
        help="Write full-pack deterministic baseline CSV",
    )
    args = ap.parse_args(argv)

    manifest_path = args.manifest if args.manifest.is_absolute() else root / args.manifest
    manifest_path = manifest_path.resolve()
    try:
        manifest_rel = manifest_path.relative_to(root.resolve())
        manifest_record = manifest_rel.as_posix()
    except ValueError:
        manifest_record = manifest_path.as_posix()
    data = _load_manifest(manifest_path)
    structural = analyze_structural(data)
    baseline_rows = deterministic_baseline_rows(data)
    bucket_means = aggregate_baseline_by_bucket(baseline_rows)

    payload: dict[str, Any] = {
        "manifest_path": manifest_record,
        "structural": structural,
        "deterministic_baseline": {
            "method": "fixture_turns + score_episode (official scorer)",
            "per_bucket_mean": bucket_means,
            "full_pack_row_count": len(baseline_rows),
        },
        "m04_decision_subset": {
            "episode_count": len(p.m04_decision_eval_rows()),
            "eval_rows": p.m04_decision_eval_rows(),
        },
    }

    if args.baseline_csv:
        out_csv = args.baseline_csv if args.baseline_csv.is_absolute() else root / args.baseline_csv
        write_baseline_csv(out_csv, baseline_rows)

    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        out_j = args.json_out if args.json_out.is_absolute() else root / args.json_out
        out_j.parent.mkdir(parents=True, exist_ok=True)
        out_j.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
