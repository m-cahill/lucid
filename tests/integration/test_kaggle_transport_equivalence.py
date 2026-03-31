"""Offline transport equivalence: manifest expected metrics match local official scoring."""

from __future__ import annotations

from pathlib import Path

import pytest

from lucid.kaggle.transport import load_transport_fixtures, verify_fixture_against_local

_FIX_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "kaggle_transport"
_MANIFEST = _FIX_DIR / "transport_manifest.json"


def test_transport_manifest_matches_local_scoring() -> None:
    fixtures = load_transport_fixtures(_MANIFEST)
    assert len(fixtures) >= 3
    for fx in fixtures:
        got = verify_fixture_against_local(fx)
        assert pytest.approx(fx.expected.D) == got.D
        assert pytest.approx(fx.expected.L) == got.L
        assert pytest.approx(fx.expected.O) == got.O
        assert pytest.approx(fx.expected.A) == got.A
        assert pytest.approx(fx.expected.C) == got.C
        assert got.lucid_score_episode == pytest.approx(fx.expected.lucid_score_episode)
