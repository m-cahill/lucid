# Template family: Contradiction / Clarification v1

**Family ID:** `contradiction_clarification_v1`  
**Family version:** `1.0.0`  
**Benchmark version:** 1.1.0 (scoring profile `1.1.0`)  
**Status:** Active (M05); canonical offline pack **`family2_core_m05_v1`**

---

## 1. Purpose

Exercise **metacognitive honesty, abstention, guarded updating, and recovery** under **contradiction drift**: competing correctness claims over the same synthetic item world, with two episode shapes — **unresolved contradiction** (no decisive resolution in-prompt) and **clarification-resolved contradiction** (a deterministic clarifier restores a unique post-drift answer). This family stays **synthetic, explicit, and legible** — not vague natural-language ambiguity.

---

## 2. Governing drift

- **Primary drift type:** `CONTRADICTION` (`DriftType.CONTRADICTION`) for all episodes.
- **Differentiation:** `contradiction_state` ∈ {`unresolved`, `resolved`}, plus `final_state_unresolved`, `clarifier_present`, and structured `post_drift_rule`.

---

## 3. Episode shapes

### 3.1 Unresolved contradiction

- After drift, two **explicit** competing claims about which item is uniquely correct remain **unresolved** in the episode text.
- **Scorer-facing:** `final_state_unresolved = True`, `acceptable_final_modes = {ANSWER, ABSTAIN, CLARIFY}`, `expected_outputs.final_correct_item_id = null`.
- **Design intent:** The **best** metacognitive pattern is **guarded** behavior (clarify, abstain, or appropriately low confidence). `ANSWER` remains technically allowed by the mode set; episodes are constructed so **forced high-confidence answering** is not the intended “good” behavior.

### 3.2 Clarification-resolved contradiction

- The same contradiction structure is followed by a **deterministic, decisive** clarifier embedded in the prompt (no new transport protocol).
- **Scorer-facing:** `final_state_unresolved = False`, `acceptable_final_modes = {ANSWER}`, unique `final_correct_item_id` per the authoritative rule.

---

## 4. Rule world (informative)

- Finite **items** with discrete attributes (`id`, `color`, `shape`, …).
- Pre-drift rule declares a unique **correct** item; drift introduces a **conflicting** claim that another item is correct.
- **Non-goals for M05:** authority ordering ladders, precedence reversals, nested exceptions, or scope drift — those belong to **Family 3** and later roadmap items.

---

## 5. Difficulty knobs

| Knob | Effect |
|------|--------|
| Candidate item count | Search space / distractor pressure |
| Attribute cardinality | Predicate complexity |
| `drift_severity` (LOW / MEDIUM / HIGH) | Item-space sizing (see implementation `difficulty_profile`) |

---

## 6. Audit metadata (manifest + episode spec)

Minimum machine-readable fields (see committed manifest rows):

- `episode_id`, `family_id`, `pack_id`, `difficulty_bucket`
- `contradiction_state`, `template_version`, `seed` (generation seed)
- `drift_type`, `target_behavior`, `expected_post_drift_rule`
- `clarifier_present`, `final_state_unresolved`
- Full `episode_spec` serialization for regeneration

---

## 7. Canonical M05 pack (`family2_core_m05_v1`)

**Episodes:** 72 — **24** LOW, **24** MEDIUM, **24** HIGH; **12** unresolved + **12** resolved per bucket.

**Committed manifest:** `tests/fixtures/family2_core_m05/family2_core_m05_manifest.json`

**Regeneration:** `python scripts/generate_family2_core_m05_manifest.py --write`  
**Verification:** `python scripts/generate_family2_core_m05_manifest.py --check`

**Local smoke (representative subset):** `scripts/run_family2_pack_smoke.py`

---

## 8. Non-goals

- Kaggle platform tasks or hosted-model claims for Family 2 in M05.
- Benchmark semantic / scorer / output-schema changes (benchmark remains **1.1.0**).
- Multi-turn clarification **protocols** beyond embedding text in the existing episode surface.

---

## 9. One-line summary

> `contradiction_clarification_v1` is the **CONTRADICTION**-first family for **unresolved vs clarification-resolved** episodes, with audit metadata and deterministic packs aligned to abstention utility and recovery under the locked scoring profile.
