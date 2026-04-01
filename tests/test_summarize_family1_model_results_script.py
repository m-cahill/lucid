"""Tests for summarize_family1_model_results.py."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_SCRIPT = _REPO / "scripts" / "summarize_family1_model_results.py"


def _load_mod() -> object:
    spec = importlib.util.spec_from_file_location("summarize_family1_model_results", _SCRIPT)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_summarize_one_model(tmp_path: Path) -> None:
    mod = _load_mod()
    p = tmp_path / "rows.csv"
    p.write_text(
        "model,episode_id,generation_seed,difficulty_bucket,D,L,O,A,C,lucid_score_episode\n"
        "TestModel,ep_a,1,LOW,1.0,0.0,0.0,1.0,1.0,1.0\n"
        "TestModel,ep_b,2,LOW,0.5,0.5,0.5,0.5,0.5,0.5\n",
        encoding="utf-8",
    )
    rows = mod.load_rows(p)
    out = mod.summarize(rows)
    assert out["source_row_count"] == 2
    agg = out["models"]["TestModel"]["aggregate"]
    assert abs(agg["lucid_score_episode"] - 0.75) < 1e-9
