"""M09 Kaggle evidence panel — deterministic 72-row slice on ``unified_core_m07_v1``.

This module selects a **downstream evaluation panel** for hosted-model evidence. It does **not**
define pack construction; see ``lucid.packs.unified_core_m07`` for the canonical 240-episode
substrate.

**Family 1 (24 rows):** Exact M04 decision panel continuity — same ``(generation_seed,
drift_severity)`` pairs as ``m04_decision_subset_seeds`` / ``m04_decision_eval_rows``, mapped to
``unified_episode_id`` rows.

**Family 2 (24 rows):** Per difficulty (LOW / MEDIUM / HIGH), **4 unresolved + 4 resolved**
episodes, chosen as the first four rows by sorted ``unified_episode_id`` within each
``(difficulty, contradiction_state)`` bucket.

**Family 3 (24 rows):** **8 LOW + 8 MEDIUM + 8 HIGH** and **8 SCOPE + 8 PRECEDENCE + 8 EXCEPTION**
overall, via a fixed allocation table over ``(difficulty, subtype)`` cells; first-N by sorted
``unified_episode_id`` within each cell.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Final

from lucid.packs import family1_core_m03 as f1
from lucid.packs import family2_core_m05 as f2
from lucid.packs import family3_core_m06 as f3
from lucid.packs import unified_core_m07 as u

# --- Identity ---

M09_PANEL_ID: Final = "m09_mature_evidence_v1"
M09_SELECTOR_VERSION: Final = "1.0.0"
M09_SELECTOR_NOTE: Final = (
    "Deterministic selectors on unified_core_m07_v1; Family 1 = exact M04 decision rows; "
    "Family 2 = 4+4 per difficulty (unresolved/resolved) by sorted unified_episode_id; "
    "Family 3 = fixed (difficulty, subtype) allocation table (see family_3_allocation)."
)

# (difficulty, family_variant as subtype) -> count. Row/column sums = 8; 8+8+8 per axis overall.
_FAMILY_3_ALLOCATION: Final[dict[tuple[str, str], int]] = {
    ("LOW", "scope"): 3,
    ("LOW", "precedence"): 3,
    ("LOW", "exception"): 2,
    ("MEDIUM", "scope"): 3,
    ("MEDIUM", "precedence"): 2,
    ("MEDIUM", "exception"): 3,
    ("HIGH", "scope"): 2,
    ("HIGH", "precedence"): 3,
    ("HIGH", "exception"): 3,
}


def _unified_rows_by_pack() -> dict[str, list[dict[str, Any]]]:
    episodes = u.build_normalized_episodes()
    out: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for e in episodes:
        out[str(e["source_pack_id"])].append(e)
    return dict(out)


def _select_family1_m09_rows() -> list[dict[str, Any]]:
    """M04 decision panel mapped to unified rows (same order as ``m04_decision_subset_seeds``)."""
    by_key: dict[tuple[int, str], dict[str, Any]] = {}
    for e in _unified_rows_by_pack().get(f1.PACK_ID, []):
        key = (int(e["source_seed"]), str(e["difficulty"]))
        by_key[key] = e

    ordered: list[dict[str, Any]] = []
    for seed, sev in f1.m04_decision_subset_seeds():
        key = (int(seed), sev.value)
        if key not in by_key:
            msg = f"M09 Family 1: missing unified row for M04 key {key!r}"
            raise KeyError(msg)
        ordered.append(by_key[key])
    return ordered


def _select_family2_m09_rows() -> list[dict[str, Any]]:
    """8 per difficulty: 4 unresolved + 4 resolved (first N by ``unified_episode_id``)."""
    buckets: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for e in _unified_rows_by_pack().get(f2.PACK_ID, []):
        k = (str(e["difficulty"]), str(e["family_variant"]))
        buckets[k].append(e)
    for k in buckets:
        buckets[k].sort(key=lambda r: str(r["unified_episode_id"]))

    out: list[dict[str, Any]] = []
    for diff in ("LOW", "MEDIUM", "HIGH"):
        for variant in ("unresolved", "resolved"):
            cell = buckets[(diff, variant)]
            picked = cell[:4]
            if len(picked) < 4:
                msg = f"M09 Family 2: need 4 rows for ({diff}, {variant}), got {len(picked)}"
                raise ValueError(msg)
            out.extend(picked)
    return out


def _select_family3_m09_rows() -> list[dict[str, Any]]:
    """Subtype × difficulty allocation per ``_FAMILY_3_ALLOCATION``."""
    buckets: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for e in _unified_rows_by_pack().get(f3.PACK_ID, []):
        k = (str(e["difficulty"]), str(e["family_variant"]))
        buckets[k].append(e)
    for k in buckets:
        buckets[k].sort(key=lambda r: str(r["unified_episode_id"]))

    out: list[dict[str, Any]] = []
    for diff in ("LOW", "MEDIUM", "HIGH"):
        for subtype in ("scope", "precedence", "exception"):
            n = _FAMILY_3_ALLOCATION[(diff, subtype)]
            cell = buckets[(diff, subtype)]
            picked = cell[:n]
            if len(picked) < n:
                msg = f"M09 Family 3: need {n} rows for ({diff}, {subtype}), got {len(picked)}"
                raise ValueError(msg)
            out.extend(picked)
    return out


def _to_eval_row(unified_row: dict[str, Any]) -> dict[str, Any]:
    """Notebook / artifact row: generation fields + lineage IDs."""
    fam = str(unified_row["family_id"])
    row: dict[str, Any] = {
        "unified_episode_id": str(unified_row["unified_episode_id"]),
        "source_pack_id": str(unified_row["source_pack_id"]),
        "source_episode_id": str(unified_row["source_episode_id"]),
        "family_id": fam,
        "difficulty": str(unified_row["difficulty"]),
        "family_variant": str(unified_row["family_variant"]),
        "generation_seed": int(unified_row["source_seed"]),
    }
    if fam == f2.FAMILY_ID:
        row["contradiction_state"] = str(unified_row["family_variant"])
    if fam == f3.FAMILY_ID:
        row["family3_subtype"] = str(unified_row["family_variant"])
    return row


def m09_eval_rows() -> list[dict[str, Any]]:
    """Ordered panel: Family 1 block (24), Family 2 block (24), Family 3 block (24)."""
    parts: list[dict[str, Any]] = []
    for e in _select_family1_m09_rows():
        parts.append(_to_eval_row(e))
    for e in _select_family2_m09_rows():
        parts.append(_to_eval_row(e))
    for e in _select_family3_m09_rows():
        parts.append(_to_eval_row(e))
    return parts


def build_m09_panel_artifact_dict() -> dict[str, Any]:
    """Machine-readable panel definition for committed JSON (Phase B / closeout)."""
    rows = m09_eval_rows()
    return {
        "panel_id": M09_PANEL_ID,
        "selector_version": M09_SELECTOR_VERSION,
        "selector_note": M09_SELECTOR_NOTE,
        "benchmark_version": u.BENCHMARK_VERSION,
        "unified_pack_id": u.PACK_ID,
        "unified_normalization_version": u.NORMALIZATION_VERSION,
        "episode_count": len(rows),
        "ordering": "family_1_block_then_family_2_block_then_family_3_block",
        "balancing_rationale": {
            "family_1": (
                "Exact M04 decision continuity: keys from family1_core_m03."
                "m04_decision_subset_seeds(), mapped to unified_episode_id via unified manifest."
            ),
            "family_2": (
                "Per difficulty: 4 unresolved + 4 resolved; within each (difficulty, state) "
                "bucket, take first 4 rows by ascending unified_episode_id."
            ),
            "family_3": (
                "Fixed allocation over (difficulty, subtype) cells; within each cell, first N "
                "rows by ascending unified_episode_id. Table in family_3_allocation."
            ),
        },
        "family_3_allocation": {
            diff: {
                sub: _FAMILY_3_ALLOCATION[(diff, sub)]
                for sub in ("scope", "precedence", "exception")
            }
            for diff in ("LOW", "MEDIUM", "HIGH")
        },
        "rows": rows,
    }
