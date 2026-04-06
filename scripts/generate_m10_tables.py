"""Generate M10 markdown/CSV tables from committed M09 evidence.

python scripts/generate_m10_tables.py --write
python scripts/generate_m10_tables.py --check
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from m10_common import (  # noqa: E402
    completed_rows,
    load_model_scores,
    repo_root,
    scores_csv_path,
    status_counts,
)


def _tables_dir(root: Path) -> Path:
    return root / "docs/milestones/M10/artifacts/tables"


def _render_paired_csv(rows: list) -> str:
    lines = [
        "model_slug,m01_mean_lucid_main_task,m09_mean_lucid_m09_mature_evidence_task,"
        "delta_m09_minus_m01,status\n"
    ]
    for r in rows:
        lines.append(f"{r.model_slug},{r.m01_mean},{r.m09_mean},{r.delta},{r.status}\n")
    return "".join(lines)


def _render_paired_md(rows: list) -> str:
    header = "| model_slug | M01 mean | M09 mean | Δ (M09−M01) |\n|---|---:|---:|---:|\n"
    body = ""
    for r in rows:
        body += f"| `{r.model_slug}` | {r.m01_mean:.6f} | {r.m09_mean:.6f} | {r.delta:+.6f} |\n"
    prov = (
        "\n**Provenance:** derived from `docs/milestones/M09/artifacts/m09_model_scores.csv` "
        "— **completed** rows only (numeric M09 means).\n"
    )
    return "# M10 — Paired M01 vs M09 means (completing subset)\n\n" + header + body + prov


def _render_completion_csv(counts: dict[str, int]) -> str:
    completed = counts.get("completed", 0)
    failed = counts.get("failed_platform_limited", 0)
    total = completed + failed
    return (
        "category,count,notes\n"
        f"completed,{completed},Numeric M09 mean present on "
        f"`lucid_m09_mature_evidence_task`\n"
        f"failed_platform_limited,{failed},No M09 numeric in export; see M09 manifest\n"
        f"total_tracked_models,{total},\n"
    )


def _write_if_changed(path: Path, content: str, *, write: bool) -> bool:
    if write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        print(f"Wrote {path}")
        return True
    if not path.is_file():
        print(f"ERROR: {path} missing (run with --write)", file=sys.stderr)
        return False
    existing = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    if existing != content:
        print(
            f"ERROR: {path} differs from generator.\nRun: python scripts/generate_m10_tables.py --write",
            file=sys.stderr,
        )
        return False
    print(f"OK: {path}")
    return True


def generate_tables(root: Path, *, write: bool) -> int:
    scores_path = scores_csv_path(root)
    all_rows = load_model_scores(scores_path)
    done = completed_rows(all_rows)
    counts = status_counts(all_rows)

    tdir = _tables_dir(root)
    ok = True
    ok &= _write_if_changed(
        tdir / "m10_paired_scores_15.csv", _render_paired_csv(done), write=write
    )
    ok &= _write_if_changed(tdir / "m10_paired_scores_15.md", _render_paired_md(done), write=write)
    ok &= _write_if_changed(
        tdir / "m10_completion_summary.csv",
        _render_completion_csv(counts),
        write=write,
    )
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--write", action="store_true")
    g.add_argument("--check", action="store_true")
    args = p.parse_args(argv)
    root = repo_root()
    return generate_tables(root, write=bool(args.write))


if __name__ == "__main__":
    raise SystemExit(main())
