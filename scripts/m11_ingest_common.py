"""Shared helpers for M11 export ingest (Kaggle leaderboard CSV format).

CSV columns (observed): Benchmark, Model, Task_Name, Task_Version, Evaluation_Date,
Numerical_Result, Upper_Confidence_Limit, Lower_Confidence_Limit, Boolean_Result
"""

from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Final

from m10_common import ModelScoreRow, load_model_scores, repo_root, scores_csv_path

# --- Tier ↔ task wiring (benchmark semantics unchanged; task names only) ---

TASK_BY_TIER: Final[dict[str, str]] = {
    "P12": "lucid_m11_probe_p12_task",
    "P24": "lucid_m11_probe_p24_task",
    "P48": "lucid_m11_probe_p48_task",
    "P72": "lucid_m09_mature_evidence_task",
}

TIER_ORDER: Final[tuple[str, ...]] = ("P12", "P24", "P48", "P72")

DEFAULT_BENCHMARK_SLUG: Final = "michael1232/lucid-kaggle-community-benchmarks"


@dataclass(frozen=True)
class ExportRow:
    benchmark: str
    model: str
    task_name: str
    evaluation_date: str
    numerical_result: float | None
    boolean_result: bool | None


def _parse_float_cell(v: str) -> float | None:
    s = (v or "").strip()
    if s == "":
        return None
    return float(s)


def _parse_bool_cell(v: str) -> bool | None:
    s = (v or "").strip()
    if s == "":
        return None
    if s.lower() == "true":
        return True
    if s.lower() == "false":
        return False
    return None


def load_kaggle_export_csv(path: Path) -> list[ExportRow]:
    if not path.is_file():
        msg = f"Export file not found: {path}"
        raise FileNotFoundError(msg)
    out: list[ExportRow] = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for raw in reader:
            task = (raw.get("Task_Name") or "").strip()
            if not task:
                continue
            out.append(
                ExportRow(
                    benchmark=(raw.get("Benchmark") or "").strip(),
                    model=(raw.get("Model") or "").strip(),
                    task_name=task,
                    evaluation_date=(raw.get("Evaluation_Date") or "").strip(),
                    numerical_result=_parse_float_cell(raw.get("Numerical_Result") or ""),
                    boolean_result=_parse_bool_cell(raw.get("Boolean_Result") or ""),
                )
            )
    return out


def _parse_eval_ts(s: str) -> datetime | None:
    s = (s or "").strip().strip('"')
    if not s:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


def merge_latest_exports(
    paths: list[Path],
) -> tuple[dict[tuple[str, str], ExportRow], dict[tuple[str, str], str]]:
    """Merge CSVs; newest Evaluation_Date wins; return (latest_map, provenance basename)."""
    best: dict[tuple[str, str], tuple[ExportRow, str, datetime | None]] = {}
    for p in paths:
        for ex in load_kaggle_export_csv(p):
            key = (ex.model, ex.task_name)
            ts = _parse_eval_ts(ex.evaluation_date)
            cur = best.get(key)
            if cur is None:
                best[key] = (ex, p.name, ts)
                continue
            _, _, cur_ts = cur
            if ts is None:
                continue
            if cur_ts is None or ts >= cur_ts:
                best[key] = (ex, p.name, ts)
    latest = {k: v[0] for k, v in best.items()}
    prov = {k: v[1] for k, v in best.items()}
    return latest, prov


def classify_row(ex: ExportRow | None) -> tuple[str, float | None, str]:
    """Return (status, score_mean or None, failure_reason_code)."""
    if ex is None:
        return "export_missing", None, "no_row_for_task"
    if ex.numerical_result is not None:
        return "completed", float(ex.numerical_result), ""
    if ex.boolean_result is False:
        return "platform_limited", None, "boolean_false_no_numeric"
    return "export_missing", None, "no_numeric_in_row"


def load_canonical_roster(path: Path) -> list[str]:
    if not path.is_file():
        msg = f"Missing roster: {path}"
        raise FileNotFoundError(msg)
    data = json.loads(path.read_text(encoding="utf-8"))
    slugs: list[str] = []
    for m in data.get("models", []):
        if m.get("tracked") is True:
            slugs.append(str(m["model_slug"]))
    slugs.sort()
    return slugs


def m01_by_slug(scores: list[ModelScoreRow]) -> dict[str, float | None]:
    return {r.model_slug: r.m01_mean for r in scores}


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def na_if_none(x: Any) -> Any:
    if x is None:
        return "NA"
    return x


def fmt_float(x: float | None) -> str:
    if x is None:
        return "NA"
    return repr(float(x))


def build_response_rows(
    roster: list[str],
    latest: dict[tuple[str, str], ExportRow],
    m01: dict[str, float | None],
    notebook_pin_sha: str,
    provenance: dict[tuple[str, str], str],
) -> list[dict[str, Any]]:
    """One row per (model, tier). provenance maps (model, task_name) -> source CSV basename."""
    raw_rows: list[dict[str, Any]] = []
    for slug in roster:
        p12_score: float | None = None
        for tier in TIER_ORDER:
            task = TASK_BY_TIER[tier]
            ex = latest.get((slug, task))
            status, score, fail_code = classify_row(ex)
            if tier == "P12" and score is not None:
                p12_score = score

            benchmark = ex.benchmark if ex else DEFAULT_BENCHMARK_SLUG
            src = provenance.get((slug, task), "NA")

            m01_mean = m01.get(slug)
            delta_m01 = None
            if score is not None and m01_mean is not None:
                delta_m01 = float(score) - float(m01_mean)

            delta_p12 = None
            if tier != "P12" and score is not None and p12_score is not None:
                delta_p12 = float(score) - float(p12_score)

            completion_binary = 1 if status == "completed" else 0

            notes_parts = []
            if status == "export_missing":
                notes_parts.append("No matching Task_Name row in provided export CSV(s).")
            if status == "platform_limited":
                notes_parts.append(
                    "Platform returned Boolean_Result=False without Numerical_Result; "
                    "not asserted as benchmark defect."
                )

            raw_rows.append(
                {
                    "model_slug": slug,
                    "probe_tier": tier,
                    "status": status,
                    "score_mean": score,
                    "score_delta_vs_M01": delta_m01,
                    "score_delta_vs_P12": delta_p12,
                    "completion_binary": completion_binary,
                    "runtime_proxy": "NA",
                    "latency_field": "NA",
                    "cost_field": "NA",
                    "failure_reason_code": fail_code if fail_code else "NA",
                    "task_name": task,
                    "benchmark_slug": benchmark or DEFAULT_BENCHMARK_SLUG,
                    "notebook_pin_sha": notebook_pin_sha,
                    "source_export": src,
                    "notes": " ".join(notes_parts).strip() or "NA",
                }
            )

    raw_rows.sort(key=lambda r: (r["model_slug"], TIER_ORDER.index(r["probe_tier"])))
    return raw_rows


def response_surface_to_csv_rows(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Stringify for CSV (NA for missing numerics)."""
    out: list[dict[str, str]] = []
    for r in rows:
        out.append(
            {
                "model_slug": r["model_slug"],
                "probe_tier": r["probe_tier"],
                "status": r["status"],
                "score_mean": fmt_float(r["score_mean"]),
                "score_delta_vs_M01": fmt_float(r["score_delta_vs_M01"]),
                "score_delta_vs_P12": fmt_float(r["score_delta_vs_P12"]),
                "completion_binary": str(int(r["completion_binary"])),
                "runtime_proxy": str(r["runtime_proxy"]),
                "latency_field": str(r["latency_field"]),
                "cost_field": str(r["cost_field"]),
                "failure_reason_code": str(r["failure_reason_code"]),
                "task_name": r["task_name"],
                "benchmark_slug": r["benchmark_slug"],
                "notebook_pin_sha": r["notebook_pin_sha"],
                "source_export": r["source_export"],
                "notes": str(r["notes"]),
            }
        )
    return out


def build_completion_frontier(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    by_model: dict[str, dict[str, dict[str, Any]]] = {}
    for r in rows:
        by_model.setdefault(r["model_slug"], {})[r["probe_tier"]] = r

    out: list[dict[str, str]] = []
    for slug in sorted(by_model.keys()):
        mt = by_model[slug]
        p12 = mt.get("P12", {}).get("status") == "completed"
        p24 = mt.get("P24", {}).get("status") == "completed"
        p48 = mt.get("P48", {}).get("status") == "completed"
        p72 = mt.get("P72", {}).get("status") == "completed"
        tiers_ok = []
        for t in TIER_ORDER:
            if mt.get(t, {}).get("status") == "completed":
                tiers_ok.append(t)
        highest = tiers_ok[-1] if tiers_ok else "NA"
        if p72:
            bp = "P72"
        elif p48:
            bp = "P48"
        elif p24:
            bp = "P24"
        elif p12:
            bp = "P12"
        else:
            bp = "none"

        out.append(
            {
                "model_slug": slug,
                "highest_completed_tier": highest,
                "completion_breakpoint": bp,
                "p12_completed": "1" if p12 else "0",
                "p24_completed": "1" if p24 else "0",
                "p48_completed": "1" if p48 else "0",
                "p72_completed": "1" if p72 else "0",
                "notes": "NA",
            }
        )
    return out


def build_failure_taxonomy_md(rows: list[dict[str, Any]]) -> str:
    counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    for r in rows:
        st = str(r["status"])
        status_counts[st] = status_counts.get(st, 0) + 1
        fc = str(r["failure_reason_code"])
        if fc != "NA" and int(r["completion_binary"]) == 0:
            counts[fc] = counts.get(fc, 0) + 1

    lines = [
        "# M11 — Failure taxonomy (empirical counts)",
        "",
        "Codes are **normalized** from ingest; they do **not** assert benchmark defects.",
        "",
        "## Status distribution (all model × tier rows)",
        "",
        "| Status | Count |",
        "|--------|------:|",
    ]
    for k in sorted(status_counts.keys()):
        lines.append(f"| `{k}` | {status_counts[k]} |")
    lines.extend(
        [
            "",
            "## Failure reason codes (non-completed rows with code)",
            "",
            "| Code | Count |",
            "|------|------:|",
        ]
    )
    if not counts:
        lines.append("| — | 0 |")
    else:
        for k in sorted(counts.keys()):
            lines.append(f"| `{k}` | {counts[k]} |")
    lines.append("")
    return "\n".join(lines)


def build_allocation_policy_md(
    frontier: list[dict[str, str]],
    rows: list[dict[str, Any]],
) -> str:
    """Transparent rule-based allocation labels (no ML)."""
    by_slug = {r["model_slug"]: r for r in frontier}

    def surface(slug: str, tier: str) -> dict[str, Any] | None:
        for row in rows:
            if row["model_slug"] == slug and row["probe_tier"] == tier:
                return row
        return None

    lines = [
        "# M11 — Allocation policy (empirical)",
        "",
        "Each model receives one **allocation_action** using deterministic rules below. "
        "This is operational guidance, not a statistical model.",
        "",
        "## Rules (in order)",
        "",
        "1. If **P12** is not `completed` → `stop_spending_budget` "
        "(no reliable cheap probe signal).",
        "2. Else if **P24** / **P48** / **P72** exports are missing for higher tiers → "
        "`repeat_for_stability` or `keep_at_mid_tier` until ladder runs exist.",
        "3. Else if **P72** `completed` → `push_harder` if score_delta_vs_M01 ≥ 0 OR "
        "score_mean ≥ median P72 among completers; else `keep_at_mid_tier`.",
        "4. Else → `keep_at_mid_tier`.",
        "",
        "| model_slug | allocation_action | rationale |",
        "|------------|-------------------|-----------|",
    ]

    p72_scores = [
        float(s["score_mean"])
        for s in rows
        if s["probe_tier"] == "P72" and s["status"] == "completed" and s["score_mean"] is not None
    ]
    median_p72 = sorted(p72_scores)[len(p72_scores) // 2] if p72_scores else None

    for slug in sorted(by_slug.keys()):
        p12 = surface(slug, "P12")
        p72 = surface(slug, "P72")
        p24 = surface(slug, "P24")
        p48 = surface(slug, "P48")

        action = "keep_at_mid_tier"
        rationale = ""

        if p12 is None or p12["status"] != "completed":
            action = "stop_spending_budget"
            rationale = "P12 not completed — do not escalate spend."
        elif (
            (p24 and p24["status"] == "export_missing")
            or (p48 and p48["status"] == "export_missing")
            or (p72 and p72["status"] == "export_missing")
        ):
            action = "repeat_for_stability"
            rationale = "Higher-tier probe exports not present — rerun ladder when exports exist."
        elif p72 and p72["status"] == "completed" and p72["score_mean"] is not None:
            sm = float(p72["score_mean"])
            d_m01 = p72["score_delta_vs_M01"]
            if median_p72 is not None and (sm >= median_p72 or (d_m01 is not None and d_m01 >= 0)):
                action = "push_harder"
                rationale = "P72 completed; at/above median P72 or non-negative vs M01."
            else:
                action = "keep_at_mid_tier"
                rationale = (
                    "P72 completed; below median and negative vs M01 — limited marginal value."
                )
        else:
            rationale = "Partial ladder; default mid-tier posture."

        lines.append(f"| `{slug}` | `{action}` | {rationale} |")

    lines.append("")
    return "\n".join(lines)


def artifacts_dir(root: Path | None = None) -> Path:
    r = root or repo_root()
    return r / "docs/milestones/M11/artifacts"


def default_export_paths(root: Path) -> list[Path]:
    """Default committed M09 leaderboard export (contains P72 / M09 task rows)."""
    p = root / "docs/milestones/M09/artifacts/m09_kaggle_leaderboard_export.csv"
    return [p]


def load_m01_table(root: Path) -> dict[str, float | None]:
    return m01_by_slug(load_model_scores(scores_csv_path(root)))
