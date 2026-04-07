"""Generate deterministic M11 figures from ``m11_model_response_surface.json``.

python scripts/generate_m11_figures.py --write
python scripts/generate_m11_figures.py --check
"""

from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path
from typing import Any

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

import matplotlib  # noqa: E402
from m11_ingest_common import TIER_ORDER, artifacts_dir  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402


def _png_bytes(fig: Figure) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    return buf.getvalue()


def _png_committed_matches_generated(committed: bytes, generated: bytes) -> bool:
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


def _apply_style() -> None:
    plt.rcParams.update(
        {
            "figure.dpi": 100,
            "savefig.dpi": 100,
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 11,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
        }
    )


def fig_completion_by_tier(rows: list[dict[str, Any]]) -> bytes:
    """Bar chart: completed count per probe tier (canonical 33 models)."""
    _apply_style()
    n_models = len({r["model_slug"] for r in rows})
    counts: dict[str, int] = {t: 0 for t in TIER_ORDER}
    for r in rows:
        if r.get("status") == "completed":
            counts[str(r["probe_tier"])] += 1
    xs = list(TIER_ORDER)
    ys = [counts[t] for t in xs]
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.bar(xs, ys, color="#0d9488")
    ax.set_ylim(0, max(n_models, 1) + 1)
    ax.set_ylabel("Models with numeric mean (completed)")
    ax.set_xlabel("Probe tier")
    ax.set_title(f"M11 — completion by tier (n={n_models} models per tier)")
    for i, v in enumerate(ys):
        ax.text(i, v + 0.15, str(v), ha="center", va="bottom", fontsize=9)
    return _png_bytes(fig)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--write", action="store_true")
    p.add_argument("--check", action="store_true")
    args = p.parse_args(argv)

    root = Path(__file__).resolve().parents[1]
    art = artifacts_dir(root)
    json_path = art / "m11_model_response_surface.json"
    out_dir = art / "figures"
    out_png = out_dir / "m11_fig_completion_by_tier.png"

    if not json_path.is_file():
        print(f"ERROR: missing {json_path}", file=sys.stderr)
        return 2

    data = json.loads(json_path.read_text(encoding="utf-8"))
    rows = data["rows"]
    blob = fig_completion_by_tier(rows)

    if args.write:
        out_dir.mkdir(parents=True, exist_ok=True)
        out_png.write_bytes(blob)
        print(f"Wrote {out_png}")
        return 0

    if args.check:
        if not out_png.is_file():
            print(f"ERROR: missing {out_png} (run --write)", file=sys.stderr)
            return 2
        if not _png_committed_matches_generated(out_png.read_bytes(), blob):
            print(
                f"ERROR: {out_png} differs from generator.\n"
                f"Run: python scripts/generate_m11_figures.py --write",
                file=sys.stderr,
            )
            return 1
        print(f"OK: {out_png}")
        return 0

    p.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
