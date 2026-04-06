"""Shared paths and CSV parsing for M10 figure/table generators.

Primary evidence: ``docs/milestones/M09/artifacts/m09_model_scores.csv``.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ModelScoreRow:
    model_slug: str
    m01_mean: float | None
    m09_mean: float | None
    delta: float | None
    status: str


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def scores_csv_path(root: Path | None = None) -> Path:
    r = root or repo_root()
    return r / "docs/milestones/M09/artifacts/m09_model_scores.csv"


def load_model_scores(path: Path) -> list[ModelScoreRow]:
    if not path.is_file():
        msg = f"Missing required evidence file: {path}"
        raise FileNotFoundError(msg)
    rows: list[ModelScoreRow] = []

    def _parse_float(row: dict[str, str], key: str) -> float | None:
        v = (row.get(key) or "").strip()
        if v == "":
            return None
        return float(v)

    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for raw in reader:
            slug = (raw.get("model_slug") or "").strip()
            if not slug:
                continue

            rows.append(
                ModelScoreRow(
                    model_slug=slug,
                    m01_mean=_parse_float(raw, "m01_mean_lucid_main_task"),
                    m09_mean=_parse_float(raw, "m09_mean_lucid_m09_mature_evidence_task"),
                    delta=_parse_float(raw, "delta_m09_minus_m01"),
                    status=(raw.get("status") or "").strip(),
                )
            )
    return rows


def completed_rows(rows: list[ModelScoreRow]) -> list[ModelScoreRow]:
    out = [r for r in rows if r.status == "completed" and r.m09_mean is not None]
    out.sort(key=lambda r: r.model_slug)
    return out


def status_counts(rows: list[ModelScoreRow]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for r in rows:
        counts[r.status] = counts.get(r.status, 0) + 1
    return counts


def short_model_label(slug: str, max_len: int = 28) -> str:
    """Readable y-axis label; deterministic truncation."""
    if len(slug) <= max_len:
        return slug
    return slug[: max_len - 1] + "…"
