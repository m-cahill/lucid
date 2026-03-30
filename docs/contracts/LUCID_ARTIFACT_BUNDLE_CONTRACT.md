# LUCID Artifact Bundle Contract

**Project:** LUCID  
**Benchmark Version:** 1.0.1  
**Document Type:** Execution Contract (Layer B)  
**Authority:** Audit-ready artifact structure and canonicalization  
**Status:** Frozen

---

## 1. Purpose

This contract defines how LUCID serializes benchmark artifacts so episodes and results can be:

- reconstructed
- rescored
- audited
- compared across models
- compared across benchmark versions

LUCID uses a split between episode spec artifacts and episode result artifacts.

---

## 2. Core artifact types

LUCID v1.0.1 defines the following canonical per-episode artifacts:

- episode spec artifact
- episode result artifact
- bundle manifest
- hash manifest

---

## 3. Canonical directory layout

```text
episode_<episode_id>/
  bundle_manifest.json
  episode_spec.json
  episode_result.json
  hashes.json
  raw/
    raw_model_output.jsonl        # optional
    auxiliary_notes.txt           # optional, non-scored
```

---

## 4. Episode spec artifact

`episode_spec.json` MUST contain, at minimum:

- `episode_id`
- `benchmark_version`
- `generation_seed`
- `template_family`
- `template_version`
- `difficulty_profile`
- `drift_event`
- `pre_drift_rule`
- `post_drift_rule`
- `expected_outputs`
- `answer_schema_ref`
- `drift_onset_turn`
- `detection_eligible_turns`
- `ambiguity_window_turns`
- `clarification_eligible_turns`
- `final_resolution_turn`
- `recovery_probe_turns` (optional)
- `uncertainty_ceiling`
- `final_calibration_epsilon`
- `final_success_condition`
- `acceptable_final_modes`
- `scoring_profile_version`

Eligibility windows are mandatory scoring inputs.

---

## 5. Episode result artifact

`episode_result.json` MUST contain, at minimum:

- `episode_id`
- `benchmark_version`
- `model_identifier`
- `output_schema_version`
- `parser_version`
- `scorer_version`
- `typed_episode_response`
- `parse_status`
- `scores`
- `diagnostics`
- `success_flags`
- `artifact_notes` (optional)

### 5.1 Raw output reference
If raw model output is stored, the result artifact MUST include:

- `raw_model_output_ref`
- `raw_model_output_sha256`

This ensures auditability and tamper visibility even when raw output is stored outside canonical scoring fields.

---

## 6. Bundle manifest

`bundle_manifest.json` MUST contain:

- `bundle_version`
- `bundle_type = "lucid_episode_bundle"`
- `episode_id`
- `benchmark_version`
- `artifact_files`
- `hash_manifest_file`
- `created_by`
- `created_at_mode`

If timestamps are stored, they MUST be non-semantic and MUST NOT affect canonical scoring hashes.

---

## 7. Hash manifest

`hashes.json` MUST contain SHA-256 hashes for:

- `episode_spec.json`
- `episode_result.json`
- `bundle_manifest.json`

Optional raw files MAY also be hashed.

---

## 8. Canonical JSON rules

All canonical scoring artifacts MUST be serialized using:

- UTF-8
- sorted keys
- stable numeric formatting
- no NaN / Infinity
- LF line endings

---

## 9. Invariants

- Spec and result remain distinct.
- Scoring windows are serialized.
- Result artifacts are rescoring-friendly.
- Raw model output references, if present, are hash-addressed.

---

## 10. One-line summary

> LUCID writes two audit-ready truths for every episode—what the benchmark generated and what the model did—and can anchor raw output by hash without letting it leak into scoring semantics.
