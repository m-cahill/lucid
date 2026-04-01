#!/usr/bin/env python3
"""M07 unified pack E2E smoke — nine representative episodes across families."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_ROOT / "src"))

from lucid.packs.unified_core_m07 import (  # noqa: E402
    build_normalized_episodes,
    unified_smoke_unified_episode_ids,
)
from lucid.runner_unified import run_unified_episode_smoke  # noqa: E402


def main() -> None:
    out_root = Path("out") / "unified_pack_smoke"
    ids = unified_smoke_unified_episode_ids()
    by_uid = {e["unified_episode_id"]: e for e in build_normalized_episodes()}
    scores: list[float] = []
    for uid in ids:
        row = by_uid[uid]
        bundle, s = run_unified_episode_smoke(unified_row=row, out_root=out_root)
        fam = row["family_id"]
        print(f"unified_episode_id={uid} family={fam} bundle={bundle} LUCID_SCORE_EPISODE={s:.6f}")
        scores.append(s)
    print(f"all_ok n={len(scores)} scores={scores}")


if __name__ == "__main__":
    main()
