"""Deterministic benchmark audits (defensibility, lineage, QA)."""

from __future__ import annotations

from lucid.audits.defensibility import (
    AUDIT_ENGINE_VERSION,
    allowlist_covers_duplicate_group,
    run_defensibility_audit,
)

__all__ = [
    "AUDIT_ENGINE_VERSION",
    "allowlist_covers_duplicate_group",
    "run_defensibility_audit",
]
