"""Validate canonical Kaggle notebook structure (offline; not a Kaggle platform run)."""

from __future__ import annotations

import json
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_NOTEBOOK = _ROOT / "notebooks" / "lucid_kaggle_transport_text_adapter_m_01.ipynb"


def test_canonical_kaggle_notebook_contract() -> None:
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

    assert joined.count("@kbench.task") == 1
    assert 'name="lucid_main_task"' in joined
    assert "lucid_symbolic_negation_row" not in joined
    assert joined.count("%choose") == 1
    assert "%choose lucid_main_task" in joined
    assert "lucid_main_task.run(kbench.llm)" in joined
    assert "schema=" not in joined
    assert "lucid.kaggle.text_adapter" in joined
    assert "require_answer=False" in joined
    assert "require_answer=True" in joined
    assert "EVAL_ROWS" in joined
    assert '"generation_seed": 100' in joined
    assert "parse_turn_payload" in joined
    assert "def parse_turn_payload" not in joined  # lives in package, not inlined
    assert "def _strip_code_fences" in joined
    md_all = "".join(
        "".join(c.get("source", [])) for c in data["cells"] if c.get("cell_type") == "markdown"
    )
    assert "Repository pin (commit SHA)" in md_all
    assert "scoring profile" in md_all.lower() or "Scoring profile" in md_all


def test_generator_check_matches_committed_notebook() -> None:
    """Requires `python scripts/generate_kaggle_notebook.py --check` to pass."""
    import subprocess
    import sys

    r = subprocess.run(
        [
            sys.executable,
            str(_ROOT / "scripts" / "generate_kaggle_notebook.py"),
            "--check",
            "-o",
            "notebooks/lucid_kaggle_transport_text_adapter_m_01.ipynb",
        ],
        cwd=_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stdout + r.stderr
