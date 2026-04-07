"""Generate M10 PNG figures from committed M09 evidence (deterministic).

python scripts/generate_m10_figures.py --write
python scripts/generate_m10_figures.py --check
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
from pathlib import Path
from typing import Any

from matplotlib.figure import Figure

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

import matplotlib
from m10_common import (  # noqa: E402
    ModelScoreRow,
    completed_rows,
    load_model_scores,
    repo_root,
    scores_csv_path,
    short_model_label,
    status_counts,
)

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402


def _apply_style() -> None:
    plt.rcParams.update(
        {
            "figure.dpi": 100,
            "savefig.dpi": 100,
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "legend.fontsize": 9,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
        }
    )


def _png_bytes(fig: Figure) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    return buf.getvalue()


def _png_committed_matches_generated(committed: bytes, generated: bytes) -> bool:
    """Exact bytes match, or pixel-wise match within tolerance (OS/matplotlib AA variance).

    CI runs Linux; developers may run Windows — Agg output can differ slightly in RGBA.
    """
    if committed == generated:
        return True
    try:
        import numpy as np
        from PIL import Image
    except ImportError:
        return False
    try:
        ia = np.asarray(Image.open(io.BytesIO(committed)).convert("RGBA"))
        ib = np.asarray(Image.open(io.BytesIO(generated)).convert("RGBA"))
    except OSError:
        return False
    if ia.shape != ib.shape:
        return False
    return bool(np.allclose(ia.astype(np.float64), ib.astype(np.float64), atol=2.0, rtol=0.0))


def fig_m01_m09_paired(rows: list[ModelScoreRow]) -> bytes:
    _apply_style()
    rows = sorted(rows, key=lambda r: r.m09_mean or 0.0, reverse=True)
    n = len(rows)
    labels = [short_model_label(r.model_slug) for r in rows]
    m01 = [float(r.m01_mean or 0.0) for r in rows]
    m09 = [float(r.m09_mean or 0.0) for r in rows]
    y = list(range(n))
    fig_h = max(6.0, 0.35 * n + 1.8)
    fig, ax = plt.subplots(figsize=(9.5, fig_h))
    h = 0.34
    ax.barh(
        [i - h / 2 for i in y], m01, height=h, color="#2563eb", label="M01 mean (transport slice)"
    )
    ax.barh(
        [i + h / 2 for i in y],
        m09,
        height=h,
        color="#ea580c",
        label="M09 mean (mature 72-ep panel)",
    )
    ax.set_yticks(y, labels, fontsize=8)
    ax.set_xlabel("Mean score (aggregate)")
    ax.set_title("M01 vs M09 — paired means (15 completing models)\nSource: m09_model_scores.csv")
    ax.set_xlim(0.0, 1.0)
    ax.legend(loc="lower right")
    ax.grid(axis="x", alpha=0.25)
    return _png_bytes(fig)


def fig_m09_ranked(rows: list[ModelScoreRow]) -> bytes:
    _apply_style()
    rows = sorted(rows, key=lambda r: r.m09_mean or 0.0, reverse=True)
    labels = [short_model_label(r.model_slug) for r in rows]
    vals = [float(r.m09_mean or 0.0) for r in rows]
    y = list(range(len(rows)))
    fig_h = max(5.5, 0.32 * len(rows) + 1.6)
    fig, ax = plt.subplots(figsize=(9.0, fig_h))
    ax.barh(y, vals, height=0.65, color="#0f766e")
    ax.set_yticks(y, labels, fontsize=8)
    ax.set_xlabel("M09 mean (lucid_m09_mature_evidence_task)")
    ax.set_title("M09 scores — ranked (completing subset)\nSource: m09_model_scores.csv")
    ax.set_xlim(0.0, 1.0)
    ax.grid(axis="x", alpha=0.25)
    return _png_bytes(fig)


def fig_delta(rows: list[ModelScoreRow]) -> bytes:
    _apply_style()
    rows = sorted(rows, key=lambda r: r.delta or 0.0)
    labels = [short_model_label(r.model_slug) for r in rows]
    deltas = [float(r.delta or 0.0) for r in rows]
    colors = ["#16a34a" if d >= 0 else "#dc2626" for d in deltas]
    y = list(range(len(rows)))
    fig_h = max(5.5, 0.32 * len(rows) + 1.6)
    fig, ax = plt.subplots(figsize=(9.0, fig_h))
    ax.barh(y, deltas, height=0.65, color=colors)
    ax.set_yticks(y, labels, fontsize=8)
    ax.set_xlabel("Δ = M09 mean − M01 mean")
    ax.set_title("M01 → M09 delta (completing subset)\nSource: m09_model_scores.csv")
    ax.axvline(0.0, color="#64748b", linewidth=0.8)
    ax.grid(axis="x", alpha=0.25)
    return _png_bytes(fig)


def fig_completion_status(all_rows: list[ModelScoreRow]) -> bytes:
    _apply_style()
    counts = status_counts(all_rows)
    done = counts.get("completed", 0)
    fail = counts.get("failed_platform_limited", 0)
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    cats = ["completed\n(numeric M09)", "failed_platform_limited\n(no M09 numeric)"]
    vals = [done, fail]
    colors = ["#15803d", "#b45309"]
    ax.bar(cats, vals, color=colors, width=0.55)
    ax.set_ylabel("Model count")
    ax.set_title(
        "M09 hosted roster — completion status (N=33)\nSource: m09_model_scores.csv + m09_kaggle_run_manifest.md"
    )
    for i, v in enumerate(vals):
        ax.text(i, v + 0.35, str(v), ha="center", fontsize=11, fontweight="bold")
    ax.set_ylim(0, max(vals) + 4)
    ax.grid(axis="y", alpha=0.25)
    return _png_bytes(fig)


def fig_milestone_ladder() -> bytes:
    """Static ladder diagram — dates from repository milestone records."""
    _apply_style()
    milestones = [
        ("M01 — Kaggle transport / platform E2E", "2026-03"),
        ("M07 — unified pack unified_core_m07_v1 (240 ep)", "2026-03"),
        ("M08 — defensibility audit (CI --check)", "2026-03"),
        ("M09 — mature-benchmark Kaggle evidence ingest", "2026-04"),
    ]
    fig, ax = plt.subplots(figsize=(9.5, 3.8))
    ax.axis("off")
    y0 = 0.88
    dy = 0.2
    for i, (title, when) in enumerate(milestones):
        y = y0 - i * dy
        ax.add_patch(
            Rectangle(
                (0.06, y - 0.07), 0.88, 0.14, facecolor="#f1f5f9", edgecolor="#94a3b8", linewidth=1
            )
        )
        ax.text(0.08, y, title, fontsize=10, va="center")
        ax.text(0.92, y, when, fontsize=9, va="center", ha="right", color="#475569")
    ax.text(
        0.5,
        0.08,
        "Evidence ladder (conceptual) — see docs/lucid.md §8 and milestone folders",
        ha="center",
        fontsize=9,
        color="#475569",
    )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return _png_bytes(fig)


def _figures_out_dir(root: Path) -> Path:
    return root / "docs/milestones/M10/artifacts/figures"


def _manifest_path(root: Path) -> Path:
    return root / "docs/milestones/M10/artifacts/m10_figure_manifest.json"


def _build_manifest(root: Path, figure_paths: dict[str, Path]) -> dict[str, Any]:
    sources = [
        "docs/milestones/M09/artifacts/m09_model_scores.csv",
        "docs/milestones/M09/artifacts/m09_kaggle_run_manifest.md",
        "docs/milestones/M08/artifacts/m08_defensibility_summary.md",
        "docs/milestones/M08/artifacts/m08_contamination_posture.md",
        "docs/lucid.md",
    ]
    figs: list[dict[str, Any]] = []
    for key, path in sorted(figure_paths.items()):
        rel = path.relative_to(root).as_posix()
        h = hashlib.sha256(path.read_bytes()).hexdigest()
        figs.append({"id": key, "path": rel, "sha256": h})
    return {
        "manifest_kind": "m10_figure_manifest",
        "benchmark_version": "1.1.0",
        "generator": "scripts/generate_m10_figures.py",
        "provenance_sources": sources,
        "figures": figs,
    }


def generate_figures(root: Path, *, write: bool) -> int:
    scores_path = scores_csv_path(root)
    all_rows = load_model_scores(scores_path)
    done = completed_rows(all_rows)

    blobs: dict[str, bytes] = {
        "m10_fig_m01_m09_paired.png": fig_m01_m09_paired(done),
        "m10_fig_m09_ranked.png": fig_m09_ranked(done),
        "m10_fig_delta_m09_minus_m01.png": fig_delta(done),
        "m10_fig_completion_status.png": fig_completion_status(all_rows),
        "m10_fig_milestone_evidence_ladder.png": fig_milestone_ladder(),
    }

    out_dir = _figures_out_dir(root)
    paths: dict[str, Path] = {k: out_dir / k for k in blobs}

    if write:
        out_dir.mkdir(parents=True, exist_ok=True)
        for name, data in blobs.items():
            p = paths[name]
            p.write_bytes(data)
            print(f"Wrote {p}")
        man = _build_manifest(root, paths)
        mp = _manifest_path(root)
        mp.parent.mkdir(parents=True, exist_ok=True)
        mp.write_text(
            json.dumps(man, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
        )
        print(f"Wrote {mp}")
        return 0

    ok = True
    for name, data in blobs.items():
        p = paths[name]
        if not p.is_file():
            print(f"ERROR: {p} missing (run with --write)", file=sys.stderr)
            ok = False
            continue
        if not _png_committed_matches_generated(p.read_bytes(), data):
            print(
                f"ERROR: {p} differs from generator (beyond pixel tolerance).\n"
                f"Run: python scripts/generate_m10_figures.py --write",
                file=sys.stderr,
            )
            ok = False
        else:
            print(f"OK: {p}")

    mp = _manifest_path(root)
    if not mp.is_file():
        print(f"ERROR: {mp} missing (run with --write)", file=sys.stderr)
        ok = False
    else:
        expected_man = json.dumps(_build_manifest(root, paths), indent=2, sort_keys=True) + "\n"
        got = mp.read_text(encoding="utf-8").replace("\r\n", "\n")
        if got != expected_man:
            print(
                f"ERROR: {mp} differs from generator.\nRun: python scripts/generate_m10_figures.py --write",
                file=sys.stderr,
            )
            ok = False
        else:
            print(f"OK: {mp}")

    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--write", action="store_true")
    g.add_argument("--check", action="store_true")
    args = p.parse_args(argv)
    root = repo_root()
    return generate_figures(root, write=bool(args.write))


if __name__ == "__main__":
    raise SystemExit(main())
