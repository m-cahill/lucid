"""Ingest Kaggle leaderboard CSV exports into normalized M11 response-surface artifacts.

Reads the **canonical 33-model roster** and one or more **Kaggle leaderboard** CSV files
(same column layout as ``m09_kaggle_leaderboard_export.csv``).

Default ingest uses the committed M09 export (contains **P72** / ``lucid_m09_mature_evidence_task``
rows). **P12 / P24 / P48** rows appear only after probe tasks are run and exported.

    python scripts/ingest_m11_platform_exports.py --write --notebook-pin-sha <40-char-sha>
    python scripts/ingest_m11_platform_exports.py --check --notebook-pin-sha <40-char-sha>

``--check`` regenerates from the same inputs and requires byte-stable JSON/CSV outputs.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from m11_ingest_common import (  # noqa: E402
    TIER_ORDER,
    artifacts_dir,
    build_completion_frontier,
    build_failure_taxonomy_md,
    build_response_rows,
    default_export_paths,
    file_sha256,
    load_canonical_roster,
    load_m01_table,
    merge_latest_exports,
    repo_root,
    response_surface_to_csv_rows,
)


def _resolve_pin_sha(explicit: str | None) -> str:
    if explicit and explicit.strip() and explicit != "auto":
        return explicit.strip()
    root = repo_root()
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            text=True,
            stderr=subprocess.DEVNULL,
        )
        return out.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def _render_probe_manifest(
    pin_sha: str,
    export_paths: list[Path],
    row_count: int,
) -> str:
    lines = [
        "# M11 — Probe run manifest (ingest)",
        "",
        f"**Notebook pin SHA:** `{pin_sha}`",
        "",
        "## Source exports",
        "",
        "| File | SHA-256 |",
        "|------|---------|",
    ]
    for p in export_paths:
        h = file_sha256(p) if p.is_file() else "NA"
        lines.append(f"| `{p.as_posix()}` | `{h}` |")
    lines.extend(
        [
            "",
            "## Coverage",
            "",
            f"- **Normalized rows (model × tier):** {row_count}",
            "- **P72:** from `lucid_m09_mature_evidence_task` when present in export(s).",
            "- **P12 / P24 / P48:** require `lucid_m11_probe_p*` task rows in an export; otherwise "
            "`export_missing`.",
            "",
        ]
    )
    return "\n".join(lines)


def _run_ingest(root: Path, export_paths: list[Path], pin_sha: str) -> dict[str, Any]:
    roster_path = root / "docs/milestones/M11/artifacts/m11_roster_canonical.json"
    roster = load_canonical_roster(roster_path)
    m01 = load_m01_table(root)
    latest, prov = merge_latest_exports(export_paths)
    rows = build_response_rows(roster, latest, m01, pin_sha, prov)
    frontier = build_completion_frontier(rows)
    tax_md = build_failure_taxonomy_md(rows)
    manifest_md = _render_probe_manifest(pin_sha, export_paths, len(rows))
    payload = {
        "meta": {
            "ingest_id": "m11_ingest_v1",
            "notebook_pin_sha": pin_sha,
            "export_paths": [p.as_posix() for p in export_paths],
            "canonical_tracked_models": len(roster),
            "tier_order": list(TIER_ORDER),
        },
        "rows": rows,
    }
    return {
        "payload": payload,
        "csv_rows": response_surface_to_csv_rows(rows),
        "frontier": frontier,
        "failure_taxonomy_md": tax_md,
        "probe_run_manifest_md": manifest_md,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--export",
        type=Path,
        action="append",
        help="Kaggle leaderboard CSV (repeatable). Default: M09 committed export only.",
    )
    p.add_argument(
        "--notebook-pin-sha",
        default="auto",
        help='40-char commit SHA for notebook ZIP pin (default: git rev-parse HEAD or "auto")',
    )
    p.add_argument(
        "--write",
        action="store_true",
        help="Write artifacts under docs/milestones/M11/artifacts/",
    )
    p.add_argument("--check", action="store_true", help="Verify artifacts match regenerated ingest")
    args = p.parse_args(argv)

    root = repo_root()
    out_dir = artifacts_dir(root)
    pin_sha = _resolve_pin_sha(args.notebook_pin_sha)

    export_paths = list(args.export) if args.export else default_export_paths(root)
    for path in export_paths:
        if not path.is_file():
            print(f"ERROR: export not found: {path}", file=sys.stderr)
            return 2

    rendered = _run_ingest(root, export_paths, pin_sha)
    json_path = out_dir / "m11_model_response_surface.json"
    csv_path = out_dir / "m11_model_response_surface.csv"
    frontier_path = out_dir / "m11_completion_frontier.csv"
    tax_path = out_dir / "m11_failure_taxonomy.md"
    manifest_path = out_dir / "m11_probe_run_manifest.md"

    if args.write:
        out_dir.mkdir(parents=True, exist_ok=True)
        json_path.write_text(_canonical_json(rendered["payload"]), encoding="utf-8", newline="\n")
        _write_csv(csv_path, rendered["csv_rows"])
        _write_csv(frontier_path, rendered["frontier"])
        tax_path.write_text(rendered["failure_taxonomy_md"], encoding="utf-8", newline="\n")
        manifest_path.write_text(rendered["probe_run_manifest_md"], encoding="utf-8", newline="\n")
        print(f"Wrote {json_path}")
        print(f"Wrote {csv_path}")
        print(f"Wrote {frontier_path}")
        print(f"Wrote {tax_path}")
        print(f"Wrote {manifest_path}")
        return 0

    if args.check:
        errs = []
        if not json_path.is_file():
            errs.append(f"missing {json_path}")
        if errs:
            print("ERROR: " + "; ".join(errs), file=sys.stderr)
            return 2
        existing_json = json.loads(json_path.read_text(encoding="utf-8"))
        meta = existing_json.get("meta") or {}
        check_paths = [root / Path(p) for p in meta.get("export_paths", [])]
        if not check_paths:
            check_paths = export_paths
        check_pin = str(meta.get("notebook_pin_sha") or pin_sha)
        regen = _run_ingest(root, check_paths, check_pin)
        if existing_json != regen["payload"]:
            print(
                "ERROR: m11_model_response_surface.json differs from ingest.\n"
                "Run: python scripts/ingest_m11_platform_exports.py --write "
                f"--notebook-pin-sha {pin_sha}",
                file=sys.stderr,
            )
            return 1
        if csv_path.read_text(encoding="utf-8").replace("\r\n", "\n") != _csv_text(
            regen["csv_rows"]
        ):
            print("ERROR: m11_model_response_surface.csv mismatch", file=sys.stderr)
            return 1
        if frontier_path.read_text(encoding="utf-8").replace("\r\n", "\n") != _csv_text(
            regen["frontier"]
        ):
            print("ERROR: m11_completion_frontier.csv mismatch", file=sys.stderr)
            return 1
        tax_got = tax_path.read_text(encoding="utf-8").replace("\r\n", "\n")
        if tax_got != regen["failure_taxonomy_md"]:
            print("ERROR: m11_failure_taxonomy.md mismatch", file=sys.stderr)
            return 1
        man_got = manifest_path.read_text(encoding="utf-8").replace("\r\n", "\n")
        if man_got != regen["probe_run_manifest_md"]:
            print("ERROR: m11_probe_run_manifest.md mismatch", file=sys.stderr)
            return 1
        print("OK: M11 ingest artifacts match generator")
        return 0

    p.print_help()
    return 2


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.write_text(_csv_text(rows), encoding="utf-8", newline="\n")


def _csv_text(rows: list[dict[str, str]]) -> str:
    if not rows:
        return ""
    import csv
    import io

    buf = io.StringIO()
    fieldnames = list(rows[0].keys())
    w = csv.DictWriter(buf, fieldnames=fieldnames, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow(r)
    return buf.getvalue()


if __name__ == "__main__":
    raise SystemExit(main())
