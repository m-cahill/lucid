#!/usr/bin/env python3
"""M06 Family 3 E2E smoke: one representative episode per subtype per difficulty bucket."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_ROOT / "src"))

from lucid.packs.family3_core_m06 import smoke_subset_triples  # noqa: E402
from lucid.runner_family3 import run_family3_smoke  # noqa: E402


def main() -> None:
    out_root = Path("out") / "family3_pack_smoke"
    scores: list[float] = []
    for seed, sev, fst in smoke_subset_triples():
        bundle, s = run_family3_smoke(
            seed=seed,
            out_root=out_root,
            drift_severity=sev,
            family_subtype=fst,
        )
        scores.append(s)
        print(
            f"seed={seed} severity={sev.value} subtype={fst} "
            f"bundle={bundle} LUCID_SCORE_EPISODE={s:.6f}"
        )
    print(f"all_ok scores={scores}")


if __name__ == "__main__":
    main()
