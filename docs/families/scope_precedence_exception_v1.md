# Family — `scope_precedence_exception_v1`

**Template family:** `scope_precedence_exception_v1`  
**Template version:** `1.0.0`  
**Benchmark / scoring profile:** **1.1.0** (unchanged in M06)

## Role

Family 3 isolates **structural rule change** under instructional drift: **scope narrowing**, **precedence reversal**, and **exception insertion**. Episodes are fully resolved at the final turn (`final_state_unresolved = False`, `acceptable_final_modes = {"ANSWER"}`). This family is **not** contradiction-first and does not optimize for abstention at final resolution (unlike Family 2 unresolved rows).

## Drift types (primary)

Episodes use the public `DriftType` enum directly:

| Episodes | `drift_type` |
|----------|----------------|
| Scope | `SCOPE` |
| Precedence | `PRECEDENCE` |
| Exception | `EXCEPTION` |

Optional manifest fields `family3_subtype` / `drift_subtype` echo `scope` | `precedence` | `exception` for pack-level summaries.

## Subtypes

### Scope drift

The predicate stays fixed (e.g. filter by color); the **universe** over which it applies **narrows** from all items to an explicit subset `S`. The post-drift correct item is the minimum item id among predicate matches **within** `S`.

### Precedence drift

Two rules **A** and **B** each match a **unique** item via a conjunction on `(color, shape)`. **Before:** A overrides B (apply A’s match if present, else B’s). **After:** B overrides A. The controlling order swap changes the final item id.

### Exception drift

**Class X** is a union of two colors. **Before:** select minimum item id among items in X. **After:** an **exception** excludes one item id from X; select minimum id among the remainder.

## Difficulty knobs

Difficulty scales by structural parameters (not prose):

- Item count and attribute grid (`n_items`, `n_colors`, `n_shapes`) — LOW / MEDIUM / HIGH match Family 1 / 2 pack profiles.
- Scope: distractor density and subset exclusion pattern (always two predicate-matching items in full universe; smallest id excluded from post scope).
- Precedence: unique conjunction targets embedded in larger grids.
- Exception: search over color pairs until a class with ≥2 items yields distinct pre/post minima.

## Metadata (audit)

Per manifest row / `difficulty_profile`, expect at least:

- `family3_subtype`, `drift_subtype`, `target_behavior`
- Scope: `scope_before`, `scope_after`, `predicate_color`
- Precedence: `precedence_before`, `precedence_after`, `rule_count`, `rule_a_item_id`, `rule_b_item_id`
- Exception: `general_rule`, `exception_class`, `exception_trigger`

## Non-goals

- Unresolved final state or clarification-resolution splits (Family 2 territory).
- Authority drift, open-ended ambiguity, or contradiction-as-final-state.
- Kaggle task or hosted-model evidence (out of M06 scope).

## Canonical pack

- **Pack ID:** `family3_core_m06_v1`
- **Manifest:** `tests/fixtures/family3_core_m06/family3_core_m06_manifest.json`
- **Regeneration:** `python scripts/generate_family3_core_m06_manifest.py --write` / `--check`
