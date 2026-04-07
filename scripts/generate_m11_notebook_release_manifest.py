"""Generate ``m11_notebook_release_manifest.json`` — auditable pre-upload metadata.

Records pin SHA, file SHA-256, task name, and evidence role for each M11
notebook (plus the M09 P72-comparable surface) so the operator has a
machine-readable link between repo state and Kaggle execution.

    python scripts/generate_m11_notebook_release_manifest.py --write
    python scripts/generate_m11_notebook_release_manifest.py --check
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[1]
_ARTIFACT = (
    _ROOT / "docs" / "milestones" / "M11" / "artifacts" / "m11_notebook_release_manifest.json"
)
_BENCHMARK_VERSION = "1.1.0"


def _load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


_gknb = _load_module(
    "generate_kaggle_notebook",
    _ROOT / "scripts" / "generate_kaggle_notebook.py",
)
_m11 = _load_module(
    "generate_m11_kaggle_notebooks",
    _ROOT / "scripts" / "generate_m11_kaggle_notebooks.py",
)

extract_pin_sha_from_notebook = _gknb.extract_pin_sha_from_notebook


def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def _file_sha256(path: Path) -> str:
    raw = path.read_bytes()
    # Notebooks are JSON text; normalize newlines so Windows (CRLF) and Linux
    # (LF) working trees match Git blob bytes and Ubuntu CI hashes.
    if path.suffix.lower() == ".ipynb":
        raw = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    h = hashlib.sha256()
    h.update(raw)
    return h.hexdigest()


def _notebook_entries() -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for tier, rel, task, _n_ep, _slug in _m11.PROBE_NOTEBOOKS:
        nb_path = _ROOT / rel
        pin_sha = extract_pin_sha_from_notebook(nb_path) or "unknown"
        entries.append(
            {
                "notebook_path": rel,
                "task_name": task,
                "pin_sha": pin_sha,
                "file_sha256": _file_sha256(nb_path),
                "generator": "scripts/generate_m11_kaggle_notebooks.py",
                "panel_source": "src/lucid/kaggle/m11_probe_panels.py",
                "evidence_role": "probe",
                "probe_tier": tier,
                "canonical": "true",
                "benchmark_version": _BENCHMARK_VERSION,
            }
        )

    m09_path = _ROOT / "notebooks" / "lucid_kaggle_m09_mature_evidence.ipynb"
    if m09_path.is_file():
        pin_sha = extract_pin_sha_from_notebook(m09_path) or "unknown"
        entries.append(
            {
                "notebook_path": "notebooks/lucid_kaggle_m09_mature_evidence.ipynb",
                "task_name": "lucid_m09_mature_evidence_task",
                "pin_sha": pin_sha,
                "file_sha256": _file_sha256(m09_path),
                "generator": "scripts/generate_m09_kaggle_notebook.py",
                "panel_source": "src/lucid/kaggle/m09_evidence_panel.py",
                "evidence_role": "comparable",
                "probe_tier": "P72",
                "canonical": "true",
                "benchmark_version": _BENCHMARK_VERSION,
            }
        )

    return entries


def build_manifest() -> dict[str, Any]:
    return {
        "description": (
            "M11 notebook release manifest — pre-upload metadata "
            "linking repo state to Kaggle execution surface"
        ),
        "benchmark_version": _BENCHMARK_VERSION,
        "entries": _notebook_entries(),
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--write", action="store_true", help="Write manifest artifact")
    p.add_argument(
        "--check",
        action="store_true",
        help="Verify committed manifest matches current repo state",
    )
    args = p.parse_args(argv)

    if args.write:
        manifest = build_manifest()
        rendered = _canonical_json(manifest)
        _ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
        _ARTIFACT.write_text(rendered, encoding="utf-8")
        print(f"Wrote {_ARTIFACT}")
        return 0

    if args.check:
        if not _ARTIFACT.is_file():
            print(
                f"ERROR: {_ARTIFACT} missing (run with --write)",
                file=sys.stderr,
            )
            return 2
        manifest = build_manifest()
        rendered = _canonical_json(manifest)
        existing = _ARTIFACT.read_text(encoding="utf-8").replace("\r\n", "\n")
        if existing != rendered:
            print(
                f"ERROR: {_ARTIFACT} differs from current repo state.\n"
                "Run: python scripts/generate_m11_notebook_release_manifest.py --write",
                file=sys.stderr,
            )
            return 1
        print(f"OK: {_ARTIFACT}")
        return 0

    p.print_help()
    print("Specify --write or --check", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
