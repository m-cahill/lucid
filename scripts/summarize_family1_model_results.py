"""Aggregate per-model CSV results from M04 hosted-model runs into JSON summaries."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


def _mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def _float_col(rows: list[dict[str, Any]], key: str) -> list[float]:
    out: list[float] = []
    for x in rows:
        try:
            out.append(float(x[key]))
        except (KeyError, TypeError, ValueError):
            continue
    return out


def load_rows(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        return [dict(row) for row in r]


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate rows: model, episode_id, difficulty_bucket, D..C, lucid_score_episode."""
    by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        model = str(row.get("model", "")).strip()
        if not model:
            continue
        by_model[model].append(row)

    metrics = ("D", "L", "O", "A", "C", "lucid_score_episode")
    out_models: dict[str, Any] = {}

    for model, mrows in sorted(by_model.items()):
        agg = {m: _mean(_float_col(mrows, m)) for m in metrics}
        by_b: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for x in mrows:
            by_b[str(x.get("difficulty_bucket", ""))].append(x)
        bucket_agg: dict[str, Any] = {}
        for b in ("LOW", "MEDIUM", "HIGH"):
            br = by_b.get(b, [])
            bucket_agg[b] = {
                "n": len(br),
                **{mm: _mean(_float_col(br, mm)) for mm in metrics},
            }

        out_models[model] = {
            "episode_count": len(mrows),
            "aggregate": agg,
            "per_bucket": bucket_agg,
        }

    return {"models": out_models, "source_row_count": len(rows)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input_csv", type=Path, help="Per-episode model results CSV")
    ap.add_argument(
        "-o",
        "--out-json",
        type=Path,
        default=None,
        help="Write summary JSON (default: stdout)",
    )
    args = ap.parse_args(argv)

    rows = load_rows(args.input_csv)
    payload = summarize(rows)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.out_json:
        args.out_json.parent.mkdir(parents=True, exist_ok=True)
        args.out_json.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
