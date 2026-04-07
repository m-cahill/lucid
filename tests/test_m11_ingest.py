"""M11 export ingest helpers (scripts/m11_ingest_common.py)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from m11_ingest_common import (  # noqa: E402
    ExportRow,
    classify_row,
    merge_latest_exports,
)


def test_classify_completed() -> None:
    ex = ExportRow(
        benchmark="b",
        model="m",
        task_name="t",
        evaluation_date="2026-01-01 12:00:00",
        numerical_result=0.5,
        boolean_result=None,
    )
    st, score, code = classify_row(ex)
    assert st == "completed"
    assert score == 0.5
    assert code == ""


def test_classify_platform_limited() -> None:
    ex = ExportRow(
        benchmark="b",
        model="m",
        task_name="t",
        evaluation_date="2026-01-01 12:00:00",
        numerical_result=None,
        boolean_result=False,
    )
    st, score, code = classify_row(ex)
    assert st == "platform_limited"
    assert score is None
    assert code == "boolean_false_no_numeric"


def test_classify_export_missing_none() -> None:
    st, score, code = classify_row(None)
    assert st == "export_missing"
    assert score is None


def test_merge_latest_exports_prefers_newer(tmp_path: Path) -> None:
    p1 = tmp_path / "a.csv"
    p1.write_text(
        "Benchmark,Model,Task_Name,Task_Version,Evaluation_Date,Numerical_Result,"
        "Upper_Confidence_Limit,Lower_Confidence_Limit,Boolean_Result\n"
        'b,m,t,1,"2026-01-01 12:00:00",0.1,,,\n',
        encoding="utf-8",
    )
    p2 = tmp_path / "b.csv"
    p2.write_text(
        "Benchmark,Model,Task_Name,Task_Version,Evaluation_Date,Numerical_Result,"
        "Upper_Confidence_Limit,Lower_Confidence_Limit,Boolean_Result\n"
        'b,m,t,1,"2026-02-01 12:00:00",0.9,,,\n',
        encoding="utf-8",
    )
    latest, prov = merge_latest_exports([p1, p2])
    assert latest[("m", "t")].numerical_result == pytest.approx(0.9)
    assert prov[("m", "t")] == "b.csv"
