"""M07 unified benchmark pack — normalized composition of Families 1–3 offline core packs."""

from __future__ import annotations

import copy
import hashlib
from pathlib import Path
from typing import Any, Final

from lucid.canonical_json import dumps_canonical
from lucid.packs import family1_core_m03 as f1
from lucid.packs import family2_core_m05 as f2
from lucid.packs import family3_core_m06 as f3

# --- Unified pack identity ---

PACK_ID: Final = "unified_core_m07_v1"
PACK_VERSION: Final = "1.0.0"
BENCHMARK_VERSION: Final = "1.1.0"
SCORING_PROFILE_VERSION: Final = "1.1.0"
NORMALIZATION_VERSION: Final = "1.0.0"
EPISODE_COUNT: Final = 240

CANONICAL_MANIFEST_RELPATH: Final = "tests/fixtures/unified_core_m07/unified_core_m07_manifest.json"

_DIFFICULTY_ORDER: Final[tuple[str, ...]] = ("LOW", "MEDIUM", "HIGH")
_FAMILY_SOURCES: Final[tuple[tuple[str, Any, str], ...]] = (
    (f1.PACK_ID, f1, "symbolic_negation_v1"),
    (f2.PACK_ID, f2, f2.FAMILY_ID),
    (f3.PACK_ID, f3, f3.FAMILY_ID),
)


def canonical_manifest_path(repo_root: Path | None = None) -> Path:
    """Resolved path to the committed M07 unified manifest."""
    root = repo_root if repo_root is not None else Path(__file__).resolve().parents[3]
    return root / CANONICAL_MANIFEST_RELPATH


def episode_spec_hash(episode_spec: dict[str, Any]) -> str:
    """SHA-256 of canonical JSON for ``episode_spec`` (source-preservation audit)."""
    payload = dumps_canonical(episode_spec)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _family_variant(
    *,
    source_pack_id: str,
    source_row: dict[str, Any],
    episode_spec: dict[str, Any],
) -> str:
    if source_pack_id == f1.PACK_ID:
        return "negation"
    if source_pack_id == f2.PACK_ID:
        st = source_row.get("contradiction_state")
        if st not in ("unresolved", "resolved"):
            msg = f"unexpected contradiction_state: {st!r}"
            raise ValueError(msg)
        return str(st)
    if source_pack_id == f3.PACK_ID:
        fst = source_row.get("family3_subtype")
        if fst not in ("scope", "precedence", "exception"):
            msg = f"unexpected family3_subtype: {fst!r}"
            raise ValueError(msg)
        return str(fst)
    msg = f"unknown source pack: {source_pack_id}"
    raise ValueError(msg)


def normalize_episode_row(
    *,
    source_pack_id: str,
    family_id: str,
    source_row: dict[str, Any],
) -> dict[str, Any]:
    """One unified manifest row: lineage, normalized metadata, full source episode_spec."""
    episode_spec: dict[str, Any] = copy.deepcopy(source_row["episode_spec"])
    source_episode_id = str(episode_spec["episode_id"])
    unified_episode_id = f"u_{source_pack_id}__{source_episode_id}"
    prof = episode_spec["difficulty_profile"]
    drift_ev = episode_spec["drift_event"]
    seed = int(episode_spec["generation_seed"])
    out: dict[str, Any] = {
        "unified_episode_id": unified_episode_id,
        "family_id": family_id,
        "source_pack_id": source_pack_id,
        "source_episode_id": source_episode_id,
        "difficulty": str(prof["drift_severity"]),
        "drift_type": str(drift_ev["drift_type"]),
        "family_variant": _family_variant(
            source_pack_id=source_pack_id,
            source_row=source_row,
            episode_spec=episode_spec,
        ),
        "final_state_unresolved": bool(episode_spec["final_state_unresolved"]),
        "acceptable_final_modes": list(episode_spec["acceptable_final_modes"]),
        "target_behavior": str(prof.get("target_behavior", "")),
        "source_seed": seed,
        "source_template_version": str(episode_spec["template_version"]),
        "source_episode_spec_hash": episode_spec_hash(episode_spec),
        "episode_spec": episode_spec,
        "normalization_version": NORMALIZATION_VERSION,
    }
    return out


def ordered_source_triples() -> list[tuple[str, str, dict[str, Any]]]:
    """For each difficulty (LOW, MEDIUM, HIGH), Family 1 then 2 then 3 rows in source order."""
    m1 = f1.build_manifest_dict()
    m2 = f2.build_manifest_dict()
    m3 = f3.build_manifest_dict()
    by_pack: dict[str, list[dict[str, Any]]] = {
        f1.PACK_ID: m1["episodes"],
        f2.PACK_ID: m2["episodes"],
        f3.PACK_ID: m3["episodes"],
    }
    out: list[tuple[str, str, dict[str, Any]]] = []
    for bucket in _DIFFICULTY_ORDER:
        for pack_id, _mod, fid in _FAMILY_SOURCES:
            for row in by_pack[pack_id]:
                if row["difficulty_bucket"] == bucket:
                    out.append((pack_id, fid, row))
    return out


def build_normalized_episodes() -> list[dict[str, Any]]:
    """All unified rows in canonical deterministic order."""
    episodes: list[dict[str, Any]] = []
    for pack_id, fid, row in ordered_source_triples():
        episodes.append(
            normalize_episode_row(
                source_pack_id=pack_id,
                family_id=fid,
                source_row=row,
            )
        )
    return episodes


def _count_bool(rows: list[dict[str, Any]], key: str, value: bool) -> int:
    return sum(1 for r in rows if bool(r[key]) == value)


def build_manifest_dict() -> dict[str, Any]:
    """Deterministic unified manifest payload (canonical JSON comparable)."""
    episodes = build_normalized_episodes()
    rows = episodes

    drift_type_counts: dict[str, int] = {}
    for r in rows:
        dt = r["drift_type"]
        drift_type_counts[dt] = drift_type_counts.get(dt, 0) + 1

    fam_counts: dict[str, int] = {}
    for r in rows:
        fid = r["family_id"]
        fam_counts[fid] = fam_counts.get(fid, 0) + 1

    diff_counts: dict[str, int] = {}
    for r in rows:
        d = r["difficulty"]
        diff_counts[d] = diff_counts.get(d, 0) + 1

    variant_counts: dict[str, int] = {}
    for r in rows:
        v = r["family_variant"]
        variant_counts[v] = variant_counts.get(v, 0) + 1

    unresolved_final = _count_bool(rows, "final_state_unresolved", True)
    resolved_final = _count_bool(rows, "final_state_unresolved", False)

    return {
        "pack_id": PACK_ID,
        "pack_version": PACK_VERSION,
        "benchmark_version": BENCHMARK_VERSION,
        "scoring_profile_version": SCORING_PROFILE_VERSION,
        "normalization_version": NORMALIZATION_VERSION,
        "episode_count": EPISODE_COUNT,
        "source_packs": [
            {
                "pack_id": f1.PACK_ID,
                "family_id": "symbolic_negation_v1",
                "episodes_included": f1.EPISODE_COUNT,
            },
            {
                "pack_id": f2.PACK_ID,
                "family_id": f2.FAMILY_ID,
                "episodes_included": f2.EPISODE_COUNT,
            },
            {
                "pack_id": f3.PACK_ID,
                "family_id": f3.FAMILY_ID,
                "episodes_included": f3.EPISODE_COUNT,
            },
        ],
        "ordering": {
            "difficulty": list(_DIFFICULTY_ORDER),
            "family_priority": ["symbolic_negation_v1", f2.FAMILY_ID, f3.FAMILY_ID],
            "note": (
                "Within each difficulty bucket, episodes appear in Family 1, then 2, then 3 "
                "source-pack order."
            ),
        },
        "difficulty_distribution": diff_counts,
        "family_distribution": fam_counts,
        "drift_type_distribution": drift_type_counts,
        "family_variant_distribution": variant_counts,
        "final_state_resolution_counts": {
            "unresolved": unresolved_final,
            "resolved": resolved_final,
        },
        "regeneration": {
            "python_module": "lucid.packs.unified_core_m07",
            "cli_write": "python scripts/generate_unified_core_m07_manifest.py --write",
            "cli_check": "python scripts/generate_unified_core_m07_manifest.py --check",
        },
        "canonical_manifest_path": CANONICAL_MANIFEST_RELPATH,
        "episodes": episodes,
    }


def unified_smoke_unified_episode_ids() -> tuple[str, ...]:
    """Nine deterministic unified rows: all families, difficulties, F2 states, F3 variants."""
    episodes = build_normalized_episodes()

    def pick(**kwargs: Any) -> str:
        for e in episodes:
            ok = True
            for k, v in kwargs.items():
                if e.get(k) != v:
                    ok = False
                    break
            if ok:
                return str(e["unified_episode_id"])
        msg = f"no unified episode matching {kwargs!r}"
        raise KeyError(msg)

    # Family 1 — LOW / MEDIUM / HIGH (M01-aligned seeds).
    f1_low = pick(
        source_pack_id=f1.PACK_ID,
        difficulty="LOW",
        source_seed=100,
    )
    f1_med = pick(
        source_pack_id=f1.PACK_ID,
        difficulty="MEDIUM",
        source_seed=42,
    )
    f1_high = pick(
        source_pack_id=f1.PACK_ID,
        difficulty="HIGH",
        source_seed=200,
    )
    # Family 2 — mix unresolved/resolved across difficulties.
    f2_a = pick(
        source_pack_id=f2.PACK_ID,
        difficulty="LOW",
        family_variant="unresolved",
        source_seed=1,
    )
    f2_b = pick(
        source_pack_id=f2.PACK_ID,
        difficulty="MEDIUM",
        family_variant="resolved",
        source_seed=113,
    )
    f2_c = pick(
        source_pack_id=f2.PACK_ID,
        difficulty="HIGH",
        family_variant="unresolved",
        source_seed=201,
    )
    # Family 3 — scope / precedence / exception (one per difficulty tier).
    f3_scope = pick(
        source_pack_id=f3.PACK_ID,
        difficulty="LOW",
        family_variant="scope",
        source_seed=1,
    )
    f3_prec = pick(
        source_pack_id=f3.PACK_ID,
        difficulty="MEDIUM",
        family_variant="precedence",
        source_seed=109,
    )
    f3_exc = pick(
        source_pack_id=f3.PACK_ID,
        difficulty="HIGH",
        family_variant="exception",
        source_seed=217,
    )

    return (
        f1_low,
        f1_med,
        f1_high,
        f2_a,
        f2_b,
        f2_c,
        f3_scope,
        f3_prec,
        f3_exc,
    )


def build_pack_stats_dict() -> dict[str, Any]:
    """Compact structural stats for audit artifacts."""
    m = build_manifest_dict()
    eps = m["episodes"]
    return {
        "pack_id": PACK_ID,
        "normalization_version": NORMALIZATION_VERSION,
        "benchmark_version": BENCHMARK_VERSION,
        "total_episodes": len(eps),
        "family_distribution": m["family_distribution"],
        "difficulty_distribution": m["difficulty_distribution"],
        "drift_type_distribution": m["drift_type_distribution"],
        "family_variant_distribution": m["family_variant_distribution"],
        "final_state_resolution_counts": m["final_state_resolution_counts"],
    }
