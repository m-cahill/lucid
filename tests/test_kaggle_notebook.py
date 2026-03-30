"""Validate repo-tracked Kaggle notebook structure (offline; not a Kaggle platform run)."""

from __future__ import annotations

import json
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_NOTEBOOK = _ROOT / "notebooks" / "lucid_kaggle_benchmark.ipynb"


def test_kaggle_notebook_has_single_choose_and_main_task_name() -> None:
    data = json.loads(_NOTEBOOK.read_text(encoding="utf-8"))
    assert data.get("nbformat") == 4
    code_sources: list[str] = []
    for cell in data.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        src = cell.get("source", [])
        if isinstance(src, list):
            code_sources.append("".join(src))
        else:
            code_sources.append(str(src))

    joined = "\n".join(code_sources)
    assert "@kbench.task(name=" in joined
    assert "lucid_symbolic_negation_row" in joined
    assert "%choose lucid_main_task" in joined
    assert joined.count("%choose") == 1
    assert "find_spec" in joined and "lucid.kaggle" in joined
