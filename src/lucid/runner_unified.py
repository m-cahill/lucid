"""Unified-pack local smoke: dispatch to family runners without changing family semantics."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from lucid.families.contradiction_clarification_v1 import ContradictionState
from lucid.families.scope_precedence_exception_v1 import Family3Subtype
from lucid.models import DriftSeverity
from lucid.runner import run_smoke
from lucid.runner_family2 import run_family2_smoke
from lucid.runner_family3 import run_family3_smoke


def run_unified_episode_smoke(
    *,
    unified_row: dict[str, Any],
    out_root: Path,
    model_id: str = "fixture",
) -> tuple[Path, float]:
    """Generate → score → bundle for one unified row; dispatches by ``template_family``."""
    spec_dict = unified_row["episode_spec"]
    family = str(spec_dict["template_family"])
    seed = int(spec_dict["generation_seed"])
    sev = DriftSeverity[str(spec_dict["difficulty_profile"]["drift_severity"])]

    if family == "symbolic_negation_v1":
        return run_smoke(seed=seed, out_root=out_root, model_id=model_id, drift_severity=sev)
    if family == "contradiction_clarification_v1":
        cstate = spec_dict["difficulty_profile"]["contradiction_state"]
        st: ContradictionState = "resolved" if cstate == "resolved" else "unresolved"
        return run_family2_smoke(
            seed=seed,
            out_root=out_root,
            model_id=model_id,
            drift_severity=sev,
            contradiction_state=st,
        )
    if family == "scope_precedence_exception_v1":
        fst_raw = spec_dict["difficulty_profile"].get("family3_subtype") or spec_dict[
            "difficulty_profile"
        ].get("drift_subtype")
        if fst_raw not in ("scope", "precedence", "exception"):
            msg = f"unknown Family 3 subtype: {fst_raw!r}"
            raise ValueError(msg)
        fst: Family3Subtype = fst_raw
        return run_family3_smoke(
            seed=seed,
            out_root=out_root,
            model_id=model_id,
            drift_severity=sev,
            family_subtype=fst,
        )

    msg = f"unsupported template_family for unified smoke: {family}"
    raise ValueError(msg)
