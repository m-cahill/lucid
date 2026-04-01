"""Generate the M04 Family 1 Kaggle analytics notebook (separate from M01 transport).

Do not hand-edit ``notebooks/lucid_kaggle_family1_m04_analytics.ipynb``.
Regenerate with::

    python scripts/generate_family1_m04_notebook.py --pin-sha $(git rev-parse HEAD)

See ``docs/milestones/M04/M04_plan.md`` and ``docs/kaggle/LUCID_KAGGLE_NOTEBOOK_M04_FAMILY1_ANALYTICS.md``.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


def _load_gknb() -> Any:
    p = Path(__file__).resolve().parent / "generate_kaggle_notebook.py"
    spec = importlib.util.spec_from_file_location("generate_kaggle_notebook", p)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


_gknb = _load_gknb()
_canonical_json = _gknb._canonical_json
_resolve_pin_sha = _gknb._resolve_pin_sha
_strip_cell_ids = _gknb._strip_cell_ids
build_m04_notebook = _gknb.build_m04_notebook
extract_pin_sha_from_notebook = _gknb.extract_pin_sha_from_notebook


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--pin-sha",
        default="auto",
        help='Commit SHA for banner + ZIP install (use "auto" for git rev-parse HEAD)',
    )
    p.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("notebooks/lucid_kaggle_family1_m04_analytics.ipynb"),
        help="Output .ipynb path",
    )
    p.add_argument(
        "--check",
        action="store_true",
        help="Regenerate with resolved --pin-sha and require output to match exactly",
    )
    args = p.parse_args(argv)

    root = Path(__file__).resolve().parents[1]
    pin_sha = _resolve_pin_sha(args.pin_sha)
    out_path = args.output if args.output.is_absolute() else root / args.output

    if args.check:
        if not out_path.is_file():
            print(f"ERROR: {out_path} missing (run without --check to create)", file=sys.stderr)
            return 2
        extracted = extract_pin_sha_from_notebook(out_path)
        check_pin = extracted if extracted is not None else pin_sha
        rendered_check = _canonical_json(_strip_cell_ids(build_m04_notebook(check_pin)))
        existing_raw = out_path.read_text(encoding="utf-8").replace("\r\n", "\n")
        existing_norm = _canonical_json(_strip_cell_ids(json.loads(existing_raw)))
        if existing_norm != rendered_check:
            print(
                f"ERROR: {out_path} differs from generator output (check_pin={check_pin}).\n"
                f"Run: python scripts/generate_family1_m04_notebook.py --pin-sha <40-char-sha> -o {args.output}",
                file=sys.stderr,
            )
            return 1
        print(f"OK: {out_path} matches generator (check_pin={check_pin})")
        return 0

    rendered = _canonical_json(build_m04_notebook(pin_sha))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered, encoding="utf-8")
    print(f"Wrote {out_path} (pin_sha={pin_sha})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
