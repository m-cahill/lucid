# Template family: Symbolic Negation v1

**Family ID:** `symbolic_negation_v1`  
**Family version:** `1.0.0`  
**Benchmark version:** 1.1.0 (scoring profile `1.1.0`)  
**Status:** Active (M00)

---

## 1. Purpose

Provide the **minimal scientifically defensible** LUCID family: a tiny symbolic attribute world, a learnable selection rule, a single **NEGATION** drift event, and a **typed final answer** with mandatory confidence and drift detection fields. **No clarification branch** in v1.

---

## 2. Required family fields (`LUCID_TEMPLATE_FAMILY_CONTRACT.md`)

| Field | Value |
|-------|--------|
| `family_id` | `symbolic_negation_v1` |
| `family_version` | `1.0.0` |
| `rule_world_description` | Finite set of **items** with discrete string attributes; rules are Boolean predicates over attributes; one item is marked correct pre-drift and post-drift according to the active predicate. |
| `allowed_rule_operators` | Attribute equality, conjunction (`AND`), negation (`NOT`) over named attributes |
| `allowed_drift_operators` | **`NEGATION` only** in v1 — the selection predicate is replaced by its logical negation for the same attribute vocabulary |
| `output_domain` | A single **item id** string chosen from the declared candidate list (typed answer), or `null` when `response_mode ≠ ANSWER` |
| `ambiguity_contradiction_affordances` | **M00:** none encoded as a clarification branch; an **ambiguity window** exists as declared turns between drift onset and final resolution where high confidence is penalized relative to `uncertainty_ceiling` |
| `difficulty_knobs` | See §5 |
| `family_scoring_notes` | See §6 |

---

## 3. Episode shape (M00)

Phases follow `LUCID_EPISODE_STRUCTURE_CONTRACT.md`:

```text
RULE_INDUCTION → STABLE_APPLICATION → DRIFT_EVENT → DRIFT_RESPONSE_WINDOW → FINAL_RESOLUTION
```

- **Single primary drift** with `drift_type = NEGATION`, explicit `drift_severity` ∈ {`LOW`, `MEDIUM`, `HIGH`}.
- **Two scored model steps** in the reference implementation: (1) an optional intermediate turn inside `DRIFT_RESPONSE_WINDOW` for detection + cautious confidence; (2) **FINAL_RESOLUTION** with full `EpisodeResponse`.
- **No** `RECOVERY_PROBE` and **no** clarification subgraph in M00.

---

## 4. Rule world (informative sketch)

- **Items:** `id ∈ {I1, I2, …, In}` each with attributes `color`, `shape`, `size`, … from small enums.
- **Pre-drift rule example:** “Select the unique item where `color = red AND shape = circle`.”
- **Drift (NEGATION):** “Select items where **NOT** (`color = red AND shape = circle`) — i.e., the governing predicate is negated; the scoring spec marks exactly one **correct** item post-drift.”

Generator MUST serialize `pre_drift_rule` and `post_drift_rule` as structured objects in `episode_spec.json`, not as informal prose alone.

---

## 5. Difficulty knobs

| Knob | Effect |
|------|--------|
| Number of candidate items | Search space size |
| Attribute cardinality | Predicate complexity |
| Pre-drift rule complexity | Number of conjuncts / attributes used |
| Distractor similarity | Near-miss items sharing attributes with the target |
| Drift cue explicitness | How obvious the negation wording is (still typed drift metadata) |
| `drift_severity` | Maps to cue strength + distractor pressure (LOW/MEDIUM/HIGH) |

---

## 6. Family scoring notes

- Ambiguity window **starts at** `drift_onset_turn` and includes all turns listed in `ambiguity_window_turns` until `final_resolution_turn`.
- **M00 symbolic_negation_v1** uses `acceptable_final_modes = {ANSWER}` only — final resolution **requires** `ANSWER`; abstention utility therefore follows `LUCID_SCORING_PROFILE_v1.1.0.md` §5.2.
- Detection eligibility: `detection_eligible_turns` includes at least the first post-drift scored turn.
- Correctness `C`: final typed answer id equals `expected_outputs.final_correct_item_id`.

---

## 7. Example episodes (severity)

### 7.1 LOW

- 4 items, 2 attributes, simple predicate `color = red`; after negation, 3 items qualify — generator picks one unambiguous correct id with clear distractors.

### 7.2 MEDIUM

- 8 items, 3 attributes, predicate with two conjuncts; negation plus one near-miss distractor sharing one conjunct.

### 7.3 HIGH

- 12+ items, higher attribute cardinality, nested conjunction; negation paired with maximally similar distractors; drift cue still explicit in spec (metadata), not ambiguous prose.

---

## 8. One-line summary

> `symbolic_negation_v1` is the canonical **NEGATION-only**, **no-clarification** starter family with typed item-id answers and full drift metadata for audit and scoring.
