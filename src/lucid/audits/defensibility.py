"""M08 unified-pack defensibility audit — deterministic hard + soft checks."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Final

from lucid.canonical_json import dumps_canonical
from lucid.packs import family1_core_m03 as f1
from lucid.packs import family2_core_m05 as f2
from lucid.packs import family3_core_m06 as f3
from lucid.packs.unified_core_m07 import (
    build_manifest_dict,
    build_normalized_episodes,
    episode_spec_hash,
)

AUDIT_ENGINE_VERSION: Final = "1.0.0"

# Soft-reporting thresholds (informational; not merge blockers).
_SOFT_TOKEN_JACCARD_MIN: Final = 0.92
_SOFT_NGRAM_JACCARD_MIN: Final = 0.88
_SOFT_NGRAM_N: Final = 5
_SOFT_MAX_PAIRS: Final = 200
_SOFT_SKELETON_MIN_COUNT: Final = 4
_SOFT_AMBIGUITY_LENIENCY_MAX: Final = 12


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _tokenize(text: str) -> set[str]:
    return set(re.findall(r"[A-Za-z0-9_]+", text.lower()))


def _char_ngrams(text: str, n: int) -> set[str]:
    t = re.sub(r"\s+", " ", text.lower().strip())
    if len(t) < n:
        return {t} if t else set()
    return {t[i : i + n] for i in range(len(t) - n + 1)}


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return float(inter) / float(union) if union else 0.0


def extract_audit_text(episode_spec: Mapping[str, Any]) -> str:
    """Flatten prompt-facing fields for similarity heuristics (deterministic)."""
    parts: list[str] = []
    preamble = episode_spec.get("prompt_preamble")
    if isinstance(preamble, str):
        parts.append(preamble)
    items = episode_spec.get("items")
    if items is not None:
        parts.append(dumps_canonical(items))
    return "\n".join(parts)


def prompt_skeleton(episode_spec: Mapping[str, Any], max_chars: int = 320) -> str:
    """Stable shape signature: collapsed whitespace prefix of normalized text."""
    raw = extract_audit_text(episode_spec)
    collapsed = re.sub(r"\s+", " ", raw.strip().lower())
    return collapsed[:max_chars]


def _normalize_soft_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def allowlist_covers_duplicate_group(
    episode_spec_sha256: str,
    unified_episode_ids: Sequence[str],
    entries: Sequence[Mapping[str, Any]],
) -> bool:
    """Return True if an allowlist entry approves this exact duplicate-id set for the hash."""
    want = sorted(unified_episode_ids)
    for entry in entries:
        eh = str(entry.get("episode_spec_sha256", ""))
        raw_ids = entry.get("unified_episode_ids")
        if eh != episode_spec_sha256 or not isinstance(raw_ids, list):
            continue
        if sorted(str(x) for x in raw_ids) == want:
            return True
    return False


def load_exact_duplicate_allowlist(path: Path) -> list[dict[str, Any]]:
    """Load allowlist JSON; missing file => empty list."""
    if not path.is_file():
        return []
    data = _load_json(path)
    if not isinstance(data, dict):
        msg = f"allowlist root must be object: {path}"
        raise ValueError(msg)
    entries = data.get("entries")
    if entries is None:
        return []
    if not isinstance(entries, list):
        msg = f"allowlist.entries must be list: {path}"
        raise ValueError(msg)
    return [e for e in entries if isinstance(e, dict)]


def _expected_lineage_keys() -> set[tuple[str, str]]:
    keys: set[tuple[str, str]] = set()
    for pack_mod in (f1, f2, f3):
        man = pack_mod.build_manifest_dict()
        pid = str(man["pack_id"])
        for row in man["episodes"]:
            eid = str(row["episode_spec"]["episode_id"])
            keys.add((pid, eid))
    return keys


def _source_episode_specs(repo_root: Path) -> dict[tuple[str, str], dict[str, Any]]:
    """(pack_id, episode_id) -> episode_spec from committed family manifests."""
    out: dict[tuple[str, str], dict[str, Any]] = {}
    for pack_mod in (f1, f2, f3):
        path = repo_root / pack_mod.CANONICAL_MANIFEST_RELPATH
        man = _load_json(path)
        pid = str(man["pack_id"])
        for row in man["episodes"]:
            spec = row["episode_spec"]
            eid = str(spec["episode_id"])
            out[(pid, eid)] = spec
    return out


def _source_manifest_rows(repo_root: Path) -> dict[tuple[str, str], dict[str, Any]]:
    """(pack_id, episode_id) -> full source manifest row (for Family 2/3 variant fields)."""
    out: dict[tuple[str, str], dict[str, Any]] = {}
    for pack_mod in (f1, f2, f3):
        path = repo_root / pack_mod.CANONICAL_MANIFEST_RELPATH
        man = _load_json(path)
        pid = str(man["pack_id"])
        for row in man["episodes"]:
            eid = str(row["episode_spec"]["episode_id"])
            out[(pid, eid)] = row
    return out


def _validate_family_variant(
    source_pack_id: str,
    family_id: str,
    row: Mapping[str, Any],
    episode_spec: Mapping[str, Any],
    source_row: Mapping[str, Any] | None,
) -> str | None:
    if source_pack_id == f1.PACK_ID:
        if family_id != "symbolic_negation_v1":
            return "family_id mismatch for Family 1"
        if row.get("family_variant") != "negation":
            return "family_variant must be negation for Family 1"
        return None
    if source_pack_id == f2.PACK_ID:
        if family_id != f2.FAMILY_ID:
            return "family_id mismatch for Family 2"
        if source_row is None:
            return "missing Family 2 source manifest row"
        st = source_row.get("contradiction_state")
        if st not in ("unresolved", "resolved"):
            return "invalid contradiction_state on source manifest row"
        if row.get("family_variant") != st:
            return "family_variant must match source manifest contradiction_state"
        return None
    if source_pack_id == f3.PACK_ID:
        if family_id != f3.FAMILY_ID:
            return "family_id mismatch for Family 3"
        if source_row is None:
            return "missing Family 3 source manifest row"
        fst = source_row.get("family3_subtype")
        if fst not in ("scope", "precedence", "exception"):
            return "invalid family3_subtype on source manifest row"
        if row.get("family_variant") != fst:
            return "family_variant must match source manifest family3_subtype"
        return None
    return "unknown source_pack_id"


def _allowed_drifts_for_pack(source_pack_id: str) -> frozenset[str]:
    if source_pack_id == f1.PACK_ID:
        return frozenset({"NEGATION"})
    if source_pack_id == f2.PACK_ID:
        return frozenset({"CONTRADICTION"})
    if source_pack_id == f3.PACK_ID:
        return frozenset({"SCOPE", "PRECEDENCE", "EXCEPTION"})
    return frozenset()


def _check_ambiguity_window_shape(episode_spec: Mapping[str, Any]) -> str | None:
    """Soft: flag extreme ambiguity windows vs episode length (heuristic)."""
    amb = episode_spec.get("ambiguity_window_turns")
    if not isinstance(amb, list):
        return None
    fr = episode_spec.get("final_resolution_turn")
    if not isinstance(fr, int) or fr < 1:
        return None
    if len(amb) > fr + _SOFT_AMBIGUITY_LENIENCY_MAX:
        return "ambiguity_window_turns longer than resolution turn suggests"
    return None


def run_defensibility_audit(
    *,
    repo_root: Path,
    unified_manifest_path: Path,
    allowlist_path: Path | None = None,
) -> dict[str, Any]:
    """Run full audit; returns a JSON-serializable dict (deterministic ordering in dumps)."""
    allow_path = allowlist_path or (
        repo_root / "docs/milestones/M08/artifacts/m08_exact_duplicate_allowlist.json"
    )
    allow_entries = load_exact_duplicate_allowlist(allow_path)

    built = build_manifest_dict()
    on_disk = _load_json(unified_manifest_path)

    hard: list[dict[str, Any]] = []

    if dumps_canonical(on_disk) != dumps_canonical(built):
        hard.append(
            {
                "code": "H_REBUILD_DRIFT",
                "message": "Committed unified manifest does not match deterministic regeneration.",
                "detail": {"path": str(unified_manifest_path)},
            }
        )

    episodes: list[dict[str, Any]] = list(on_disk.get("episodes", []))
    expected_keys = _expected_lineage_keys()
    seen_unified: set[str] = set()
    seen_lineage: set[tuple[str, str]] = set()
    source_specs = _source_episode_specs(repo_root)
    source_rows = _source_manifest_rows(repo_root)

    # Ordering vs code
    code_order = [e["unified_episode_id"] for e in build_normalized_episodes()]
    disk_order = [e["unified_episode_id"] for e in episodes]
    if len(disk_order) != len(code_order):
        hard.append(
            {
                "code": "H_ORDER_LENGTH_MISMATCH",
                "message": "Unified episode count/order length does not match canonical build.",
                "detail": {
                    "disk_len": len(disk_order),
                    "code_len": len(code_order),
                },
            }
        )
    elif disk_order != code_order:
        hard.append(
            {
                "code": "H_ORDER_MISMATCH",
                "message": (
                    "Unified episode order does not match canonical build_normalized_episodes()."
                ),
                "detail": {
                    "first_mismatch_index": next(
                        (
                            i
                            for i, (a, b) in enumerate(
                                zip(disk_order, code_order, strict=True),
                            )
                            if a != b
                        ),
                        None,
                    ),
                },
            }
        )

    # Uniqueness + lineage
    for row in episodes:
        uid = str(row.get("unified_episode_id", ""))
        sp = str(row.get("source_pack_id", ""))
        sid = str(row.get("source_episode_id", ""))
        if uid in seen_unified:
            hard.append(
                {
                    "code": "H_DUPLICATE_UNIFIED_ID",
                    "message": "Duplicate unified_episode_id.",
                    "detail": {"unified_episode_id": uid},
                }
            )
        seen_unified.add(uid)
        lk = (sp, sid)
        if lk in seen_lineage:
            hard.append(
                {
                    "code": "H_DUPLICATE_LINEAGE",
                    "message": "Duplicate (source_pack_id, source_episode_id).",
                    "detail": {"source_pack_id": sp, "source_episode_id": sid},
                }
            )
        seen_lineage.add(lk)

    observed_lineage = seen_lineage
    if observed_lineage != expected_keys:
        missing = sorted(expected_keys - observed_lineage)
        extra = sorted(observed_lineage - expected_keys)
        if missing:
            hard.append(
                {
                    "code": "H_MISSING_SOURCE_EPISODES",
                    "message": "Unified pack is missing source episodes.",
                    "detail": {"missing": [{"pack": p, "episode_id": e} for p, e in missing]},
                }
            )
        if extra:
            hard.append(
                {
                    "code": "H_EXTRA_LINEAGE_KEYS",
                    "message": "Unified pack references unknown source episodes.",
                    "detail": {"extra": [{"pack": p, "episode_id": e} for p, e in extra]},
                }
            )

    # Per-row metadata + source match + hash
    required_row_keys = (
        "unified_episode_id",
        "family_id",
        "source_pack_id",
        "source_episode_id",
        "difficulty",
        "drift_type",
        "family_variant",
        "final_state_unresolved",
        "acceptable_final_modes",
        "target_behavior",
        "source_seed",
        "source_template_version",
        "source_episode_spec_hash",
        "episode_spec",
        "normalization_version",
    )
    diff_buckets = ("LOW", "MEDIUM", "HIGH")

    hash_groups: dict[str, list[str]] = {}

    for row in episodes:
        uid = str(row["unified_episode_id"])
        rk_missing = [k for k in required_row_keys if k not in row]
        if rk_missing:
            hard.append(
                {
                    "code": "H_METADATA_INCOMPLETE",
                    "message": "Unified row missing required keys.",
                    "detail": {"unified_episode_id": uid, "missing_keys": rk_missing},
                }
            )
            continue

        if row["difficulty"] not in diff_buckets:
            hard.append(
                {
                    "code": "H_INVALID_DIFFICULTY",
                    "message": "Invalid difficulty label.",
                    "detail": {"unified_episode_id": uid, "difficulty": row["difficulty"]},
                }
            )

        spec = row["episode_spec"]
        if not isinstance(spec, dict):
            hard.append(
                {
                    "code": "H_INVALID_EPISODE_SPEC",
                    "message": "episode_spec must be an object.",
                    "detail": {"unified_episode_id": uid},
                }
            )
            continue

        sp = str(row["source_pack_id"])
        sid = str(row["source_episode_id"])
        src = source_specs.get((sp, sid))
        src_row = source_rows.get((sp, sid))
        if src is None:
            continue
        if dumps_canonical(spec) != dumps_canonical(src):
            hard.append(
                {
                    "code": "H_SOURCE_EPISODE_SPEC_MISMATCH",
                    "message": "episode_spec does not match canonical source manifest row.",
                    "detail": {
                        "unified_episode_id": uid,
                        "source_pack_id": sp,
                        "source_episode_id": sid,
                    },
                }
            )

        computed = episode_spec_hash(spec)
        declared = str(row["source_episode_spec_hash"])
        if computed != declared:
            hard.append(
                {
                    "code": "H_SOURCE_EPISODE_SPEC_HASH_MISMATCH",
                    "message": (
                        "source_episode_spec_hash does not match canonical hash of episode_spec."
                    ),
                    "detail": {
                        "unified_episode_id": uid,
                        "declared": declared,
                        "computed": computed,
                    },
                }
            )

        hash_groups.setdefault(computed, []).append(uid)

        drift_t = str(row["drift_type"])
        allowed = _allowed_drifts_for_pack(sp)
        if drift_t not in allowed:
            hard.append(
                {
                    "code": "H_INVALID_DRIFT_TYPE",
                    "message": "drift_type not allowed for source pack.",
                    "detail": {
                        "unified_episode_id": uid,
                        "drift_type": drift_t,
                        "allowed": sorted(allowed),
                    },
                }
            )
        else:
            ev = spec.get("drift_event")
            if isinstance(ev, dict) and str(ev.get("drift_type", "")) != drift_t:
                hard.append(
                    {
                        "code": "H_DRIFT_TYPE_ROW_SPEC_MISMATCH",
                        "message": (
                            "Top-level drift_type must match episode_spec.drift_event.drift_type."
                        ),
                        "detail": {"unified_episode_id": uid},
                    }
                )

        fv_err = _validate_family_variant(sp, str(row["family_id"]), row, spec, src_row)
        if fv_err:
            hard.append(
                {
                    "code": "H_INVALID_FAMILY_VARIANT",
                    "message": fv_err,
                    "detail": {"unified_episode_id": uid},
                }
            )

    # Distribution consistency (manifest-level)
    if isinstance(on_disk.get("difficulty_distribution"), dict):
        rd: dict[str, int] = {}
        for row in episodes:
            d = str(row.get("difficulty", ""))
            rd[d] = rd.get(d, 0) + 1
        if rd != dict(on_disk["difficulty_distribution"]):
            hard.append(
                {
                    "code": "H_DISTRIBUTION_ROW_MANIFEST_MISMATCH",
                    "message": (
                        "difficulty_distribution does not match recomputation from episodes."
                    ),
                    "detail": {"manifest": on_disk["difficulty_distribution"], "recomputed": rd},
                }
            )

    if isinstance(on_disk.get("family_distribution"), dict):
        fd: dict[str, int] = {}
        for row in episodes:
            fid = str(row.get("family_id", ""))
            fd[fid] = fd.get(fid, 0) + 1
        if fd != dict(on_disk["family_distribution"]):
            hard.append(
                {
                    "code": "H_FAMILY_DISTRIBUTION_MISMATCH",
                    "message": "family_distribution does not match recomputation from episodes.",
                    "detail": {"manifest": on_disk["family_distribution"], "recomputed": fd},
                }
            )

    # Exact duplicate groups (same canonical episode_spec)
    exact_groups_out: list[dict[str, Any]] = []
    for h, ids in sorted(hash_groups.items()):
        uids = sorted(ids)
        exact_groups_out.append({"episode_spec_sha256": h, "unified_episode_ids": uids})
        if len(uids) <= 1:
            continue
        approved = allowlist_covers_duplicate_group(h, uids, allow_entries)
        if not approved:
            hard.append(
                {
                    "code": "H_EXACT_DUPLICATE_UNAPPROVED",
                    "message": (
                        "Multiple unified rows share the same canonical episode_spec "
                        "without allowlist entry."
                    ),
                    "detail": {"episode_spec_sha256": h, "unified_episode_ids": uids},
                }
            )

    # Soft checks
    soft: list[dict[str, Any]] = []
    texts: dict[str, str] = {}
    skeleton_index: dict[str, list[str]] = {}
    for row in episodes:
        uid = str(row["unified_episode_id"])
        spec = row["episode_spec"]
        if not isinstance(spec, dict):
            continue
        texts[uid] = _normalize_soft_text(extract_audit_text(spec))
        sk = prompt_skeleton(spec)
        skeleton_index.setdefault(sk, []).append(uid)
        aw = _check_ambiguity_window_shape(spec)
        if aw:
            soft.append(
                {
                    "kind": "ambiguity_window_shape",
                    "message": aw,
                    "detail": {"unified_episode_id": uid},
                }
            )

    # Skeleton clusters (informational)
    _sk_clusters = 0
    for sk, uids in sorted(skeleton_index.items(), key=lambda x: (-len(x[1]), x[0])):
        if len(uids) < _SOFT_SKELETON_MIN_COUNT:
            continue
        if _sk_clusters >= 12:
            break
        _sk_clusters += 1
        soft.append(
            {
                "kind": "repeated_prompt_skeleton",
                "message": "Several episodes share the same prompt skeleton prefix.",
                "detail": {
                    "skeleton_prefix": sk[:120],
                    "count": len(uids),
                    "sample_unified_episode_ids": sorted(uids)[:12],
                },
            }
        )

    # Pairwise token / n-gram similarity (O(n^2); n=240 is fine)
    uids_sorted = sorted(texts.keys())
    pair_rows: list[tuple[float, float, str, str]] = []
    for i in range(len(uids_sorted)):
        for j in range(i + 1, len(uids_sorted)):
            a, b = uids_sorted[i], uids_sorted[j]
            ta, tb = texts[a], texts[b]
            tok_a, tok_b = _tokenize(ta), _tokenize(tb)
            tj = _jaccard(tok_a, tok_b)
            ng_a, ng_b = _char_ngrams(ta, _SOFT_NGRAM_N), _char_ngrams(tb, _SOFT_NGRAM_N)
            nj = _jaccard(ng_a, ng_b)
            if tj >= _SOFT_TOKEN_JACCARD_MIN or nj >= _SOFT_NGRAM_JACCARD_MIN:
                pair_rows.append((tj, nj, a, b))
    pair_rows.sort(key=lambda x: (-max(x[0], x[1]), x[2], x[3]))
    for tj, nj, a, b in pair_rows[:_SOFT_MAX_PAIRS]:
        if tj >= _SOFT_TOKEN_JACCARD_MIN:
            soft.append(
                {
                    "kind": "high_token_jaccard",
                    "message": "High token-set Jaccard between two episodes (informational).",
                    "detail": {
                        "unified_episode_id_a": a,
                        "unified_episode_id_b": b,
                        "token_jaccard": round(tj, 6),
                    },
                }
            )
        elif nj >= _SOFT_NGRAM_JACCARD_MIN:
            soft.append(
                {
                    "kind": "high_ngram_overlap",
                    "message": (
                        "High character n-gram Jaccard between two episodes (informational)."
                    ),
                    "detail": {
                        "unified_episode_id_a": a,
                        "unified_episode_id_b": b,
                        "n": _SOFT_NGRAM_N,
                        "ngram_jaccard": round(nj, 6),
                    },
                }
            )

    passed = len(hard) == 0

    duplicate_scan = {
        "audit_engine_version": AUDIT_ENGINE_VERSION,
        "thresholds": {
            "soft_token_jaccard_min": _SOFT_TOKEN_JACCARD_MIN,
            "soft_ngram_jaccard_min": _SOFT_NGRAM_JACCARD_MIN,
            "soft_ngram_size": _SOFT_NGRAM_N,
            "soft_skeleton_min_count": _SOFT_SKELETON_MIN_COUNT,
        },
        "exact_duplicate_groups": exact_groups_out,
        "soft_findings_count": len(soft),
    }

    return {
        "audit_engine_version": AUDIT_ENGINE_VERSION,
        "passed": passed,
        "hard_failures": hard,
        "soft_findings": soft,
        "duplicate_scan": duplicate_scan,
        "counts": {
            "episodes": len(episodes),
            "hard_failure_count": len(hard),
            "soft_finding_count": len(soft),
            "exact_duplicate_multi_row_groups": sum(
                1 for g in exact_groups_out if len(g["unified_episode_ids"]) > 1
            ),
        },
        "paths": {
            "unified_manifest": str(unified_manifest_path),
            "allowlist": str(allow_path),
        },
    }


def render_defensibility_summary(audit: Mapping[str, Any]) -> str:
    """Markdown summary for human auditors (deterministic)."""
    lines = [
        "# M08 — Defensibility audit summary",
        "",
        f"- **Audit engine:** `{audit.get('audit_engine_version')}`",
        f"- **Result:** **{'PASS' if audit.get('passed') else 'FAIL'}**",
        f"- **Episodes audited:** {audit.get('counts', {}).get('episodes', '—')}",
        "",
        "## Hard failures",
        "",
    ]
    hf = audit.get("hard_failures")
    if isinstance(hf, Sequence) and len(hf) == 0:
        lines.append("*None.*")
    elif isinstance(hf, Sequence):
        for h in hf:
            if isinstance(h, dict):
                code = h.get("code", "?")
                msg = h.get("message", "")
                lines.append(f"- **`{code}`:** {msg}")
    else:
        lines.append("*Unparseable.*")
    lines.extend(
        [
            "",
            "## Soft findings (informational)",
            "",
        ]
    )
    sf = audit.get("soft_findings")
    n_soft = len(sf) if isinstance(sf, Sequence) else 0
    lines.append(
        f"Total soft findings recorded: **{n_soft}** "
        "(see `m08_defensibility_audit.json` and `m08_duplicate_scan.json`)."
    )
    lines.extend(
        [
            "",
            "## Policy",
            "",
            "Soft findings do not fail CI unless an explicit checked-in policy is added. "
            "Hard failures block merge.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"
