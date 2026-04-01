"""M09 evidence panel determinism and balance checks."""

from __future__ import annotations

from collections import Counter

from lucid.kaggle.m09_evidence_panel import (
    M09_PANEL_ID,
    M09_SELECTOR_VERSION,
    build_m09_panel_artifact_dict,
    m09_eval_rows,
)
from lucid.packs import family1_core_m03 as f1
from lucid.packs import family2_core_m05 as f2
from lucid.packs import family3_core_m06 as f3


def test_m09_panel_size_and_id() -> None:
    rows = m09_eval_rows()
    assert len(rows) == 72
    assert M09_PANEL_ID == "m09_mature_evidence_v1"
    assert M09_SELECTOR_VERSION == "1.0.0"
    uids = [r["unified_episode_id"] for r in rows]
    assert len(set(uids)) == 72


def test_m09_family1_matches_m04_keys_in_order() -> None:
    rows = m09_eval_rows()[:24]
    m04 = f1.m04_decision_eval_rows()
    assert len(m04) == 24
    for i, mrow in enumerate(m04):
        assert rows[i]["family_id"] == "symbolic_negation_v1"
        assert rows[i]["generation_seed"] == mrow["generation_seed"]
        assert rows[i]["difficulty"] == mrow["drift_severity"]


def test_m09_family2_balance() -> None:
    rows = [r for r in m09_eval_rows() if r["family_id"] == f2.FAMILY_ID]
    assert len(rows) == 24
    by_d = Counter(r["difficulty"] for r in rows)
    assert by_d == {"LOW": 8, "MEDIUM": 8, "HIGH": 8}
    for diff in ("LOW", "MEDIUM", "HIGH"):
        slice_d = [r for r in rows if r["difficulty"] == diff]
        states = Counter(r["contradiction_state"] for r in slice_d)
        assert states == {"unresolved": 4, "resolved": 4}


def test_m09_family3_balance() -> None:
    rows = [r for r in m09_eval_rows() if r["family_id"] == f3.FAMILY_ID]
    assert len(rows) == 24
    by_d = Counter(r["difficulty"] for r in rows)
    assert by_d == {"LOW": 8, "MEDIUM": 8, "HIGH": 8}
    by_sub = Counter(r["family3_subtype"] for r in rows)
    assert by_sub == {"scope": 8, "precedence": 8, "exception": 8}


def test_m09_artifact_dict_roundtrip_keys() -> None:
    d = build_m09_panel_artifact_dict()
    assert d["panel_id"] == M09_PANEL_ID
    assert d["episode_count"] == 72
    assert "family_3_allocation" in d
    assert len(d["rows"]) == 72
