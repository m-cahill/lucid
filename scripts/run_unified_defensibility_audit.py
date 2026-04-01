#!/usr/bin/env python3
"""M08 — write or verify unified-pack defensibility audit artifacts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_ROOT / "src"))

from lucid.audits.defensibility import (  # noqa: E402
    render_defensibility_summary,
    run_defensibility_audit,
)
from lucid.canonical_json import dumps_canonical, write_canonical  # noqa: E402


def _artifacts_dir(repo_root: Path) -> Path:
    return repo_root / "docs/milestones/M08/artifacts"


def _default_paths(repo_root: Path) -> dict[str, Path]:
    _u = "tests/fixtures/unified_core_m07/unified_core_m07_manifest.json"
    return {
        "unified_manifest": repo_root / _u,
        "audit_json": _artifacts_dir(repo_root) / "m08_defensibility_audit.json",
        "duplicate_scan_json": _artifacts_dir(repo_root) / "m08_duplicate_scan.json",
        "summary_md": _artifacts_dir(repo_root) / "m08_defensibility_summary.md",
        "allowlist": _artifacts_dir(repo_root) / "m08_exact_duplicate_allowlist.json",
    }


def _run_audit(repo_root: Path, allowlist: Path | None) -> dict:
    return run_defensibility_audit(
        repo_root=repo_root,
        unified_manifest_path=_default_paths(repo_root)["unified_manifest"],
        allowlist_path=allowlist,
    )


def _write_artifacts(repo_root: Path, allowlist: Path | None) -> dict:
    audit = _run_audit(repo_root, allowlist)
    paths = _default_paths(repo_root)
    dup = audit["duplicate_scan"]
    write_canonical(str(paths["audit_json"]), audit)
    write_canonical(str(paths["duplicate_scan_json"]), dup)
    paths["summary_md"].parent.mkdir(parents=True, exist_ok=True)
    paths["summary_md"].write_text(
        render_defensibility_summary(audit),
        encoding="utf-8",
        newline="\n",
    )
    return audit


def _check_artifacts(repo_root: Path, allowlist: Path | None) -> None:
    paths = _default_paths(repo_root)
    audit = _run_audit(repo_root, allowlist)
    dup = audit["duplicate_scan"]

    if not paths["audit_json"].is_file():
        msg = f"missing {paths['audit_json']}"
        raise SystemExit(msg)
    if not paths["duplicate_scan_json"].is_file():
        msg = f"missing {paths['duplicate_scan_json']}"
        raise SystemExit(msg)
    if not paths["summary_md"].is_file():
        msg = f"missing {paths['summary_md']}"
        raise SystemExit(msg)

    import json

    on_disk_audit = json.loads(paths["audit_json"].read_text(encoding="utf-8"))
    on_disk_dup = json.loads(paths["duplicate_scan_json"].read_text(encoding="utf-8"))
    if dumps_canonical(on_disk_audit) != dumps_canonical(audit):
        msg = (
            f"audit artifact drift: {paths['audit_json']}\n"
            "Regenerate with: python scripts/run_unified_defensibility_audit.py --write"
        )
        raise SystemExit(msg)
    if dumps_canonical(on_disk_dup) != dumps_canonical(dup):
        msg = (
            f"duplicate scan artifact drift: {paths['duplicate_scan_json']}\n"
            "Regenerate with: python scripts/run_unified_defensibility_audit.py --write"
        )
        raise SystemExit(msg)
    if paths["summary_md"].read_text(encoding="utf-8") != render_defensibility_summary(audit):
        msg = (
            f"summary markdown drift: {paths['summary_md']}\n"
            "Regenerate with: python scripts/run_unified_defensibility_audit.py --write"
        )
        raise SystemExit(msg)

    if not audit.get("passed"):
        msg = "defensibility audit failed (hard checks); see m08_defensibility_audit.json"
        raise SystemExit(msg)

    posture = _artifacts_dir(repo_root) / "m08_contamination_posture.md"
    if not posture.is_file():
        msg = f"missing static doc: {posture}"
        raise SystemExit(msg)

    print(f"ok {paths['audit_json']}")
    print(f"ok {paths['duplicate_scan_json']}")
    print(f"ok {paths['summary_md']}")
    print(f"ok {posture}")


def main() -> None:
    p = argparse.ArgumentParser(description="M08 unified defensibility audit — write or check")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument(
        "--write",
        action="store_true",
        help="Regenerate audit JSON + summary under docs/milestones/M08/artifacts/.",
    )
    g.add_argument(
        "--check",
        action="store_true",
        help="Fail if artifacts differ from deterministic audit or hard checks fail.",
    )
    p.add_argument(
        "--repo-root",
        type=Path,
        default=_ROOT,
        help="Repository root (default: parent of scripts/).",
    )
    p.add_argument(
        "--allowlist",
        type=Path,
        default=None,
        help="Optional path to explicit duplicate allowlist JSON (default: M08 artifacts path).",
    )
    args = p.parse_args()
    if args.write:
        _write_artifacts(args.repo_root, args.allowlist)
        print("wrote M08 defensibility artifacts")
        return
    _check_artifacts(args.repo_root, args.allowlist)


if __name__ == "__main__":
    main()
