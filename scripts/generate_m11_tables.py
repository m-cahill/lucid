"""Generate M11 markdown tables from ``m11_model_response_surface.json``.

Writes:

* ``m11_allocation_policy.md`` — rule-based allocation actions
* ``m11_analytical_summary.md`` — data-bound slope / stability / anomaly notes (honest gaps)

    python scripts/generate_m11_tables.py --write
    python scripts/generate_m11_tables.py --check
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from m11_ingest_common import (  # noqa: E402
    TIER_ORDER,
    artifacts_dir,
    build_allocation_policy_md,
    build_completion_frontier,
    repo_root,
)


def _load_surface(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data["rows"]
    frontier = build_completion_frontier(rows)
    return rows, frontier


def _render_allocation_md(rows: list[dict[str, Any]], frontier: list[dict[str, str]]) -> str:
    return build_allocation_policy_md(frontier, rows)


def _parse_float(x: Any) -> float | None:
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    return None


def _render_analytical_summary_md(rows: list[dict[str, Any]]) -> str:
    """Transparent summaries only—no inferred metrics beyond committed surface rows."""
    by_model: dict[str, dict[str, dict[str, Any]]] = {}
    for r in rows:
        by_model.setdefault(r["model_slug"], {})[r["probe_tier"]] = r

    lines = [
        "# M11 — Analytical summary (data-bound)",
        "",
        "Derived **only** from `m11_model_response_surface` rows. **No** "
        "family/difficulty/component slices from aggregate M09 exports.",
        "",
        "## 1. Completion coverage by tier",
        "",
    ]
    for tier in TIER_ORDER:
        n_done = sum(1 for r in rows if r["probe_tier"] == tier and r.get("status") == "completed")
        n_tot = sum(1 for r in rows if r["probe_tier"] == tier)
        lines.append(f"- **{tier}:** {n_done} / {n_tot} rows `completed`")
    lines.extend(["", "## 2. Ladder score slope (P12 → P72)", ""])

    any_slope = False
    for slug in sorted(by_model.keys()):
        m = by_model[slug]
        scores = []
        for tier in TIER_ORDER:
            cell = m.get(tier)
            if not cell or cell.get("status") != "completed":
                continue
            sm = _parse_float(cell.get("score_mean"))
            if sm is not None:
                scores.append((tier, sm))
        if len(scores) >= 2:
            any_slope = True
            break

    if not any_slope:
        lines.append(
            "**Not computable** with current ingest: need **≥2** completed tiers with numeric "
            "`score_mean` per model. Re-run ingest after P12/P24/P48 leaderboard exports exist."
        )
    else:
        lines.append("Models with ≥2 completed tiers with numeric scores (pairwise deltas):")
        lines.extend(
            [
                "",
                "| model_slug | tier_a | mean_a | tier_b | mean_b | delta_b_minus_a |",
                "|---|---:|---:|---:|---:|---:|",
            ]
        )
        for slug in sorted(by_model.keys()):
            m = by_model[slug]
            scores = []
            for tier in TIER_ORDER:
                cell = m.get(tier)
                if not cell or cell.get("status") != "completed":
                    continue
                sm = _parse_float(cell.get("score_mean"))
                if sm is not None:
                    scores.append((tier, sm))
            for i in range(len(scores) - 1):
                (ta, ma), (tb, mb) = scores[i], scores[i + 1]
                lines.append(f"| `{slug}` | {ta} | {ma:.6f} | {tb} | {mb:.6f} | {mb - ma:+.6f} |")

    lines.extend(["", "## 3. Sharp degradation / stability (heuristic)", ""])
    lines.append(
        "Requires **≥2** numeric tier means per model. With only **P72** numeric for most models, "
        "degradation vs ladder size is **not** measured here—**blocked** until smaller-tier "
        "exports exist."
    )

    lines.extend(["", "## 4. P72 completed — largest negative Δ vs M01 (anomaly signal)", ""])
    p72_rows = [
        r
        for r in rows
        if (
            r["probe_tier"] == "P72"
            and r.get("status") == "completed"
            and r.get("score_mean") is not None
        )
    ]
    scored = []
    for r in p72_rows:
        dm = _parse_float(r.get("score_delta_vs_M01"))
        if dm is not None:
            scored.append((str(r["model_slug"]), float(r["score_mean"]), dm))
    scored.sort(key=lambda x: x[2])
    if not scored:
        lines.append("*No P72 rows with both `score_mean` and `score_delta_vs_M01`.*")
    else:
        lines.extend(["| model_slug | p72_mean | delta_vs_M01 |", "|---|---:|---:|"])
        for slug, sm, dm in scored[:12]:
            lines.append(f"| `{slug}` | {sm:.6f} | {dm:+.6f} |")
        if len(scored) > 12:
            lines.append(f"| … | … | *(truncated; {len(scored)} total)* |")

    lines.extend(["", "## 5. Repeat lane (P12_repeat)", ""])
    lines.append(
        "Repeatability is **P12** episode IDs rerun on the same task. **No** duplicate run rows "
        "exist in leaderboard CSV ingest—track repeat runs as separate exports or manual notes."
    )
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--write", action="store_true", help="Write m11_allocation_policy.md")
    p.add_argument("--check", action="store_true", help="Verify committed file matches generator")
    args = p.parse_args(argv)

    root = repo_root()
    art = artifacts_dir(root)
    json_path = art / "m11_model_response_surface.json"
    out_alloc = art / "m11_allocation_policy.md"
    out_summary = art / "m11_analytical_summary.md"

    if not json_path.is_file():
        print(f"ERROR: missing {json_path} (run ingest --write first)", file=sys.stderr)
        return 2

    rows, frontier = _load_surface(json_path)
    rendered_alloc = _render_allocation_md(rows, frontier)
    rendered_summary = _render_analytical_summary_md(rows)

    if args.write:
        art.mkdir(parents=True, exist_ok=True)
        out_alloc.write_text(rendered_alloc, encoding="utf-8", newline="\n")
        out_summary.write_text(rendered_summary, encoding="utf-8", newline="\n")
        print(f"Wrote {out_alloc}")
        print(f"Wrote {out_summary}")
        return 0

    if args.check:
        ok = True
        if not out_alloc.is_file():
            print(f"ERROR: missing {out_alloc}", file=sys.stderr)
            ok = False
        else:
            existing = out_alloc.read_text(encoding="utf-8").replace("\r\n", "\n")
            if existing != rendered_alloc:
                print(
                    "ERROR: m11_allocation_policy.md differs from generator.\n"
                    "Run: python scripts/generate_m11_tables.py --write",
                    file=sys.stderr,
                )
                ok = False
            else:
                print("OK: m11_allocation_policy.md matches generator")
        if not out_summary.is_file():
            print(f"ERROR: missing {out_summary}", file=sys.stderr)
            ok = False
        else:
            ex2 = out_summary.read_text(encoding="utf-8").replace("\r\n", "\n")
            if ex2 != rendered_summary:
                print(
                    "ERROR: m11_analytical_summary.md differs from generator.\n"
                    "Run: python scripts/generate_m11_tables.py --write",
                    file=sys.stderr,
                )
                ok = False
            else:
                print("OK: m11_analytical_summary.md matches generator")
        return 0 if ok else 1

    p.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
