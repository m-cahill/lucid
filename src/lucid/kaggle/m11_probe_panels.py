"""M11 hosted-model probe ladder — nested deterministic panels on the M09 mature substrate.

Each tier selects rows **within** the corresponding M09 family block (24 rows per family) by:

* grouping by ``difficulty``
* sorting within each bucket by ``unified_episode_id`` (ascending)
* taking the first *N* rows per bucket per documented allocation
* re-ordering the chosen rows to preserve **M09 block iteration order** (subset stability)

**P72** is exactly ``m09_eval_rows()`` (same 72 episodes as ``m09_mature_evidence_v1``).

**Repeat lane:** ``P12_repeat`` uses the same episode set as **P12** (same IDs, same notebook/task
surface).

Benchmark semantics and scoring profile are unchanged (**1.1.0**); this module only defines
evaluation subsets.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Final

from lucid.kaggle.m09_evidence_panel import M09_PANEL_ID, m09_eval_rows

# --- Identity ---

M11_PROBE_SELECTOR_VERSION: Final = "1.0.0"
M11_PROBE_SELECTOR_NOTE: Final = (
    "Nested deterministic subsets within each M09 family block; per-difficulty first-N by "
    "sorted unified_episode_id; iteration order = M09 block order (index-stable)."
)

# Tier IDs
M11_TIER_P12: Final = "P12"
M11_TIER_P24: Final = "P24"
M11_TIER_P48: Final = "P48"
M11_TIER_P72: Final = "P72"

M11_PROBE_TIERS: Final[tuple[str, ...]] = (M11_TIER_P12, M11_TIER_P24, M11_TIER_P48, M11_TIER_P72)

# Per-family difficulty allocations (episode counts). All families use the same table per tier.
# P12: 1+2+1 = 4 per family; MEDIUM +1 vs base 3×3 grid (see M11 plan).
_P12_ALLOC: Final[dict[str, int]] = {"LOW": 1, "MEDIUM": 2, "HIGH": 1}
# P24: 2+3+3 = 8 per family; MEDIUM emphasis.
_P24_ALLOC: Final[dict[str, int]] = {"LOW": 2, "MEDIUM": 3, "HIGH": 3}
# P48: 5+6+5 = 16 per family; MEDIUM emphasis.
_P48_ALLOC: Final[dict[str, int]] = {"LOW": 5, "MEDIUM": 6, "HIGH": 5}

_M09_BLOCK_SIZE: Final = 24


def _bucket_by_difficulty(block: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in block:
        buckets[str(row["difficulty"])].append(row)
    for k in buckets:
        buckets[k].sort(key=lambda r: str(r["unified_episode_id"]))
    return dict(buckets)


def _take_from_buckets(
    buckets: dict[str, list[dict[str, Any]]],
    alloc: dict[str, int],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for diff in ("LOW", "MEDIUM", "HIGH"):
        n = alloc[diff]
        cell = buckets.get(diff, [])
        picked = cell[:n]
        if len(picked) < n:
            msg = f"M11 probe: need {n} rows for difficulty {diff}, got {len(picked)}"
            raise ValueError(msg)
        out.extend(picked)
    return out


def _order_like_m09_block(
    selected: list[dict[str, Any]],
    block: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Preserve relative order as in the M09 24-row family block."""
    index_by_uid = {str(r["unified_episode_id"]): i for i, r in enumerate(block)}
    return sorted(selected, key=lambda r: index_by_uid[str(r["unified_episode_id"])])


def _split_m09_family_blocks(m09_rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], ...]:
    if len(m09_rows) != 72:
        msg = f"Expected 72 M09 rows, got {len(m09_rows)}"
        raise ValueError(msg)
    b1 = m09_rows[0:_M09_BLOCK_SIZE]
    b2 = m09_rows[_M09_BLOCK_SIZE : 2 * _M09_BLOCK_SIZE]
    b3 = m09_rows[2 * _M09_BLOCK_SIZE : 3 * _M09_BLOCK_SIZE]
    return (b1, b2, b3)


def _probe_rows_for_alloc(
    alloc: dict[str, int],
    m09_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    blocks = _split_m09_family_blocks(m09_rows)
    out: list[dict[str, Any]] = []
    for block in blocks:
        buckets = _bucket_by_difficulty(block)
        picked = _take_from_buckets(buckets, alloc)
        out.extend(_order_like_m09_block(picked, block))
    return out


def m11_probe_eval_rows(tier: str) -> list[dict[str, Any]]:
    """Return evaluation rows for ``tier`` (``P12`` / ``P24`` / ``P48`` / ``P72``)."""
    t = tier.upper().strip()
    m09 = m09_eval_rows()
    if t == M11_TIER_P72:
        return list(m09)
    if t == M11_TIER_P12:
        return _probe_rows_for_alloc(_P12_ALLOC, m09)
    if t == M11_TIER_P24:
        return _probe_rows_for_alloc(_P24_ALLOC, m09)
    if t == M11_TIER_P48:
        return _probe_rows_for_alloc(_P48_ALLOC, m09)
    msg = f"Unknown M11 probe tier: {tier!r}"
    raise ValueError(msg)


def m11_repeat_eval_rows() -> list[dict[str, Any]]:
    """Repeatability lane — same episodes as P12."""
    return m11_probe_eval_rows(M11_TIER_P12)


def build_m11_probe_ladder_artifact_dict() -> dict[str, Any]:
    """Machine-readable ladder definition + row lists for CI and audit."""
    m09 = m09_eval_rows()
    tiers_payload: dict[str, Any] = {}
    for tier in M11_PROBE_TIERS:
        rows = m11_probe_eval_rows(tier)
        tiers_payload[tier] = {
            "episode_count": len(rows),
            "unified_episode_ids": [str(r["unified_episode_id"]) for r in rows],
        }

    return {
        "artifact_id": "m11_probe_ladder_v1",
        "selector_version": M11_PROBE_SELECTOR_VERSION,
        "selector_note": M11_PROBE_SELECTOR_NOTE,
        "m09_panel_id": M09_PANEL_ID,
        "repeat_lane_note": "P12_repeat uses the same unified_episode_ids as P12.",
        "allocations": {
            M11_TIER_P12: {
                "per_family_total": 4,
                "per_difficulty": dict(_P12_ALLOC),
                "rationale": (
                    "9-cell base (one per family×difficulty) + one extra MEDIUM per family "
                    "(signal-rich tier); first-N within each bucket by sorted unified_episode_id."
                ),
            },
            M11_TIER_P24: {
                "per_family_total": 8,
                "per_difficulty": dict(_P24_ALLOC),
                "rationale": "Equal family totals; MEDIUM emphasis; nested superset of P12.",
            },
            M11_TIER_P48: {
                "per_family_total": 16,
                "per_difficulty": dict(_P48_ALLOC),
                "rationale": "Equal family totals; MEDIUM emphasis; nested superset of P24.",
            },
            M11_TIER_P72: {
                "per_family_total": 24,
                "per_difficulty": "use_exact_m09_family_blocks",
                "rationale": "Identical to m09_mature_evidence_v1 (72 episodes).",
            },
        },
        "tiers": tiers_payload,
        "rows_by_tier": {
            M11_TIER_P12: m11_probe_eval_rows(M11_TIER_P12),
            M11_TIER_P24: m11_probe_eval_rows(M11_TIER_P24),
            M11_TIER_P48: m11_probe_eval_rows(M11_TIER_P48),
            M11_TIER_P72: m09,
        },
    }
