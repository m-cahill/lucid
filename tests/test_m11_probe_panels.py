"""M11 probe ladder: nesting, sizes, and M09 compatibility."""

from __future__ import annotations

from collections import Counter

import pytest

from lucid.kaggle.m09_evidence_panel import m09_eval_rows
from lucid.kaggle.m11_probe_panels import (
    M11_TIER_P12,
    M11_TIER_P24,
    M11_TIER_P48,
    M11_TIER_P72,
    build_m11_probe_ladder_artifact_dict,
    m11_probe_eval_rows,
    m11_repeat_eval_rows,
)


def _uids(rows: list[dict]) -> set[str]:
    return {str(r["unified_episode_id"]) for r in rows}


def test_m11_p72_equals_m09() -> None:
    m09 = m09_eval_rows()
    p72 = m11_probe_eval_rows(M11_TIER_P72)
    assert len(p72) == 72
    assert [r["unified_episode_id"] for r in p72] == [r["unified_episode_id"] for r in m09]


def test_m11_panel_sizes() -> None:
    assert len(m11_probe_eval_rows(M11_TIER_P12)) == 12
    assert len(m11_probe_eval_rows(M11_TIER_P24)) == 24
    assert len(m11_probe_eval_rows(M11_TIER_P48)) == 48
    assert len(m11_probe_eval_rows(M11_TIER_P72)) == 72


def test_m11_nested_subsets() -> None:
    p12 = m11_probe_eval_rows(M11_TIER_P12)
    p24 = m11_probe_eval_rows(M11_TIER_P24)
    p48 = m11_probe_eval_rows(M11_TIER_P48)
    p72 = m11_probe_eval_rows(M11_TIER_P72)
    u12, u24, u48, u72 = _uids(p12), _uids(p24), _uids(p48), _uids(p72)
    assert u12 <= u24 <= u48 <= u72
    assert len(u12) == 12


def test_m11_repeat_lane_is_p12() -> None:
    assert [r["unified_episode_id"] for r in m11_repeat_eval_rows()] == [
        r["unified_episode_id"] for r in m11_probe_eval_rows(M11_TIER_P12)
    ]


def test_m11_p12_per_family_difficulty_counts() -> None:
    from lucid.packs import family1_core_m03 as f1
    from lucid.packs import family2_core_m05 as f2
    from lucid.packs import family3_core_m06 as f3

    p12 = m11_probe_eval_rows(M11_TIER_P12)
    for fid, fam_rows in (
        (f1.TEMPLATE_FAMILY, [r for r in p12 if r["family_id"] == f1.TEMPLATE_FAMILY]),
        (f2.FAMILY_ID, [r for r in p12 if r["family_id"] == f2.FAMILY_ID]),
        (f3.FAMILY_ID, [r for r in p12 if r["family_id"] == f3.FAMILY_ID]),
    ):
        assert len(fam_rows) == 4, fid
        by_d = Counter(r["difficulty"] for r in fam_rows)
        assert by_d == {"LOW": 1, "MEDIUM": 2, "HIGH": 1}, (fid, by_d)


def test_m11_unknown_tier_raises() -> None:
    with pytest.raises(ValueError, match="Unknown"):
        m11_probe_eval_rows("P99")


def test_m11_artifact_dict_shape() -> None:
    d = build_m11_probe_ladder_artifact_dict()
    assert d["artifact_id"] == "m11_probe_ladder_v1"
    assert len(d["rows_by_tier"][M11_TIER_P12]) == 12
    assert len(d["tiers"][M11_TIER_P72]["unified_episode_ids"]) == 72
