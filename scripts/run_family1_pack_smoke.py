#!/usr/bin/env python3
"""M03 Family 1 E2E smoke: one episode per difficulty bucket (M01 transport seeds)."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_ROOT / "src"))

from lucid.models import DriftSeverity  # noqa: E402
from lucid.runner import run_smoke  # noqa: E402

# Subset: M01 acceptance-slice seeds, one per bucket (LOW / MEDIUM / HIGH).
_SUBSET: tuple[tuple[int, DriftSeverity], ...] = (
    (100, DriftSeverity.LOW),
    (42, DriftSeverity.MEDIUM),
    (200, DriftSeverity.HIGH),
)


def main() -> None:
    out_root = Path("out") / "family1_pack_smoke"
    scores: list[float] = []
    for seed, sev in _SUBSET:
        bundle, s = run_smoke(seed=seed, out_root=out_root, drift_severity=sev)
        scores.append(s)
        print(f"seed={seed} severity={sev.value} bundle={bundle} LUCID_SCORE_EPISODE={s:.6f}")
    print(f"all_ok scores={scores}")


if __name__ == "__main__":
    main()
