

M00 Plan — Bootstrap, Semantic Lock, and Local Minimal Green Path
=================================================================

0. Milestone identity

---------------------

**Milestone:** M00  
**Title:** Bootstrap, semantic lock, and local minimal green path  
**Intent:** Convert LUCID from a strong contract bundle into a canonical, initialized benchmark repo with explicit scoring semantics, three missing adjacent docs, one concrete template family, a live `docs/lucid.md` ledger, and a local deterministic smoke path.  
**Explicitly deferred to M01:** Kaggle Benchmarks end-to-end verification.

* * *

1. Decisions already locked for M00

-----------------------------------

Cursor should not reopen these unless a hard contradiction appears in the repo.

### 1.1 File naming

Keep the referenced adjacent document name exactly as:

* `LUCID_BOUNDARIES.md`

* `LUCID_ASSUMED_GUARANTEES.md`

* `LUCID_STACK_INTERACTION.md`

### 1.2 Scoring

Keep the official scalar score weights unchanged for now:
    0.40 * D
    0.20 * (1 - L)
    0.15 * (1 - O)
    0.15 * A
    0.10 * C

Do **not** redesign the top-level weighting in M00.  
Instead, lock the missing semantics cleanly and version them honestly.

### 1.3 Benchmark versioning

Treat the scoring-semantic lock as a **benchmark-semantic** change.  
Recommended outcome: bump the contract-set benchmark version from **1.0.1 → 1.1.0**.

Rationale:

* `calibrated-response criterion` is currently undefined.

* `target_confidence_t` is currently undefined.

* abstention utility is currently only profile-defined.

* hardening these changes official scorer behavior.

### 1.4 Concrete first family

Choose the first concrete template family as a **symbolic negation-drift family** with no clarification branch in M00.

Reason:

* easiest family to defend scientifically

* cleanest minimal green path

* best starting point for contamination resistance and deterministic scoring

* enough room later to expand into scope, contradiction, and clarification variants

### 1.5 Terminology supplement

Make the terminology supplement **LLM-focused**, not judge-facing prose first.

### 1.6 Kaggle

Do **not** attempt real Kaggle Benchmarks E2E in M00.  
Do record it prominently as **M01 priority** inside `docs/lucid.md`.

* * *

2. M00 scope

------------

M00 includes all of the following:

* repo initialization and scaffolding

* `docs/lucid.md` initialization as the living ledger / authority map

* competition-rule verification in documentation

* creation of:
  
  * `LUCID_BOUNDARIES.md`
  
  * `LUCID_ASSUMED_GUARANTEES.md`
  
  * `LUCID_STACK_INTERACTION.md`

* archival of `docs/LUCID_contracts_master_bundle.md`

* LLM-focused terminology/writeup guide

* scoring contract semantic lock

* one concrete template family doc

* local minimal green path implementation

* local deterministic E2E smoke verification

* baseline truthful CI

* M01 stub capture in `docs/lucid.md`

M00 does **not** include:

* Kaggle Benchmarks E2E execution

* Kaggle submission packaging proof

* multi-family expansion

* clarification-branch family support

* benchmark breadth optimization

* leaderboard-facing polish

* * *

3. Success condition for M00

----------------------------

At M00 close, LUCID should be able to say:

> “We have one canonical repo, one living ledger, one archived-not-canonical bundle export, one explicit scoring profile, one concrete family, and one local deterministic end-to-end run that writes an audit-ready episode bundle.”

That is enough to begin M01 with Kaggle E2E as a real engineering milestone rather than a vague promise.

* * *

4. Repository and scaffolding work

----------------------------------

Cursor should initialize the repo as a serious benchmark repo, not a throwaway notebook dump.

### 4.1 Create or normalize the top-level structure

Target structure:
    .
    ├── LICENSE
    ├── README.md
    ├── pyproject.toml
    ├── .gitignore
    ├── .github/
    │   └── workflows/
    │       └── ci.yml
    ├── docs/
    │   ├── lucid.md
    │   ├── LUCID_MOONSHOT.md
    │   ├── LUCID_OPERATING_MANUAL.md
    │   ├── LUCID_BOUNDARIES.md
    │   ├── LUCID_ASSUMED_GUARANTEES.md
    │   ├── LUCID_STACK_INTERACTION.md
    │   ├── LUCID_TERMINOLOGY_GUIDE_LLM.md
    │   ├── LUCID_COMPETITION_ALIGNMENT.md
    │   ├── archive/
    │   │   ├── README.md
    │   │   └── LUCID_contracts_master_bundle_v1.0.1_ARCHIVED.md
    │   ├── contracts/
    │   │   ├── LUCID_CONTRACT_INDEX.md
    │   │   ├── ...
    │   │   └── LUCID_SCORING_PROFILE_v1.1.0.md
    │   ├── families/
    │   │   └── LUCID_TEMPLATE_FAMILY_SYMBOLIC_NEGATION_V1.md
    │   └── milestones/
    │       ├── M00/
    │       │   └── M00_plan.md
    │       └── M01/
    │           └── M01_plan_stub.md
    ├── src/
    │   └── lucid/
    │       ├── __init__.py
    │       ├── models.py
    │       ├── generator.py
    │       ├── drift.py
    │       ├── parser.py
    │       ├── scorer.py
    │       ├── writer.py
    │       ├── runner.py
    │       ├── canonical_json.py
    │       ├── hashing.py
    │       └── families/
    │           └── symbolic_negation_v1.py
    ├── scripts/
    │   └── run_local_smoke.py
    └── tests/
        ├── test_scoring_profile.py
        ├── test_symbolic_negation_family.py
        ├── test_local_smoke_e2e.py
        └── fixtures/

### 4.2 Repo bootstrap specifics

* initialize git if missing

* ensure Apache-2.0 license is present

* create a concise `README.md` that clearly says LUCID is a benchmark, not a solver

* create a practical `.gitignore`

* use a modern Python package layout under `src/`

* use typed code from the start

* add a minimal local runner script for smoke validation

### 4.3 Tooling baseline

Add at minimum:

* Ruff

* mypy

* pytest

* pytest-cov

* a simple Makefile or equivalent task runner

Suggested bootstrap commands:
    make lint
    make test
    make smoke

* * *

5. Authority cleanup and archival cleanup

-----------------------------------------

This is a core M00 task, not a side chore.

### 5.1 Canonical source decision

Make the **individual contract files under `docs/contracts/` canonical**.

The master bundle must become archival only.

### 5.2 Archive the master bundle

Cursor must:

1. verify the individual contract files exist and are the canonical working copies

2. move the current master bundle out of the main docs surface

3. archive it as:
    docs/archive/LUCID_contracts_master_bundle_v1.0.1_ARCHIVED.md

4. add `docs/archive/README.md` that states:
   
   * this file is historical / export-only
   
   * it is not the canonical editable contract source
   
   * the canonical source is the individual files under `docs/contracts/`

### 5.3 Update references

Update any docs that currently imply the master bundle is active.  
`docs/lucid.md` must explicitly state:

* canonical = individual contract files

* archived = former concatenated master bundle

* no manual dual maintenance allowed

* * *

6. Initialize `docs/lucid.md` as the living ledger

--------------------------------------------------

`docs/lucid.md` must stop being a placeholder and become the repo’s live execution truth.

### 6.1 Required sections

Cursor should initialize `docs/lucid.md` with these sections:

1. **Project identity**
   
   * one-sentence benchmark identity
   
   * benchmark version
   
   * current milestone status

2. **Authority hierarchy**
   
   * moonshot
   
   * contract set
   
   * operating manual
   
   * adjacent docs
   
   * implementation code

3. **Canonical doc map**
   
   * where contracts live
   
   * where family docs live
   
   * where scoring profile lives
   
   * where archived docs live

4. **Current benchmark status**
   
   * active template families
   
   * active scoring profile
   
   * local minimal green path status
   
   * Kaggle E2E status = deferred to M01

5. **Semantic change log**
   
   * record that M00 locked scoring semantics
   
   * record benchmark version bump to 1.1.0
   
   * record archival of master bundle

6. **Competition alignment**
   
   * link to `docs/LUCID_COMPETITION_ALIGNMENT.md`
   
   * short summary of track and deadline

7. **Milestone ledger**
   
   * M00 row
   
   * M01 reserved row

8. **Next milestone reminder**
   
   * explicit M01 priority:  
     “Kaggle Community Benchmarks E2E verification”

### 6.2 M01 note that must be added now

Cursor must add an explicit section in `docs/lucid.md`:
    Planned next milestone (M01):
    Priority = Kaggle Community Benchmarks E2E verification.
    Goal = prove that the local LUCID benchmark structure can be represented, run, and validated through Kaggle’s benchmark/task workflow without changing benchmark semantics.

This is mandatory so M01 cannot be forgotten.

* * *

7. Create the three missing adjacent docs

-----------------------------------------

These docs are referenced by the contract index and should exist by the end of M00.

### 7.1 `docs/LUCID_BOUNDARIES.md`

Purpose: define what LUCID owns, what it refuses to own, and where its integration boundaries sit.

Required contents:

* LUCID is a benchmark, not a solver

* no human-judged core scoring

* no hidden evaluator logic

* no free-form text scoring

* no Kaggle-platform-specific semantics inside the benchmark core

* no stack reimplementation

* no benchmark widening into generic reasoning omnibus

* local deterministic core remains canonical even when Kaggle integration arrives

* M01 Kaggle work must prove transport/execution compatibility, not redefine benchmark meaning

### 7.2 `docs/LUCID_ASSUMED_GUARANTEES.md`

Purpose: document what the implementation assumes about substrate posture.

Important instruction:  
Do **not** write this as though LUCID has already inherited certified guarantees from another codebase unless that is provably true in this repo.

Required framing:

* these are implementation assumptions / target guarantees for LUCID’s substrate

* assumptions include:
  
  * deterministic episode generation
  
  * canonical JSON serialization
  
  * reproducible hashing
  
  * typed output parsing
  
  * truthful CI
  
  * no hidden evaluator dependence

* clearly separate:
  
  * **assumed**
  
  * **implemented in this repo**
  
  * **not yet proven**

* make the tone audit-honest, not inherited-certification theater

### 7.3 `docs/LUCID_STACK_INTERACTION.md`

Purpose: define how LUCID draws posture from the surrounding stack without losing identity.

Required contents:

* CLARITY informs evaluation posture

* DARIA informs deterministic execution and artifact posture

* Foundry informs role separation and architecture posture

* RediAI informs truthful CI / governance posture

* LUCID does not become a reimplementation of any of them

* LUCID is allowed to borrow posture and patterns, not silently merge identities

* public-facing writeups should not over-emphasize stack lineage

This should align with the moonshot’s stack section while reducing ambiguity.

* * *

8. Create the LLM-focused terminology guide

-------------------------------------------

Create:
    docs/LUCID_TERMINOLOGY_GUIDE_LLM.md

Purpose: teach Cursor and other LLM agents how to write about LUCID without muddying its scientific identity.

Required contents:

### 8.1 Preferred terms

* benchmark

* cognitive ability

* metacognitive calibration

* instructional drift

* explicit rule change

* typed response

* deterministic episode

* artifact bundle

### 8.2 Terms needing caution

* latent

* policy

* faculty

* drift

* calibration

* episode

### 8.3 Public-writeup translation guidance

Examples:

* say “cognitive ability” in competition-facing copy more often than “faculty”

* define “instructional drift” as an explicit rule-change event

* avoid making “latent” sound like latent-representation analysis unless that is truly intended

* describe confidence as part of benchmark output, not auxiliary metadata

* describe LUCID as metacognition-first, not generic reasoning

### 8.4 Forbidden phrasing

* “LUCID solves”

* “LUCID is an AGI system”

* “LUCID proves general intelligence”

* “LUCID measures everything important”

The guide should be operational and brief, not essay-like.

* * *

9. Competition-rule verification in documentation

-------------------------------------------------

M00 should verify the competition and platform in docs, not in runtime.

Create:
    docs/LUCID_COMPETITION_ALIGNMENT.md

### 9.1 Must include official facts

Document, with official links:

* the competition name

* the five target tracks, including metacognition

* the current submission deadline

* the fact that Kaggle’s Community Benchmarks platform is the intended benchmark-building surface

* the existence of task/benchmark creation docs

* the existence of token/cost/latency metrics on the benchmark platform

These facts are current as of March 2026 and should be captured from official sources only. ([Kaggle](https://www.kaggle.com/competitions/kaggle-measuring-agi/overview?utm_source=chatgpt.com "Measuring Progress Toward AGI - Cognitive Abilities"))

### 9.2 Must include a clear scope note

Add a note that says:

* M00 verifies documentation alignment only

* M01 performs actual Kaggle Benchmarks E2E proof

* no writeup should imply Kaggle E2E is already validated before M01 closes

* * *

10. Scoring semantic lock

-------------------------

This is the most important semantic work in M00.

### 10.1 Keep the official scalar score weights unchanged

Do not alter the top-level weights in M00.

### 10.2 Add a scoring profile document

Create:
    docs/contracts/LUCID_SCORING_PROFILE_v1.1.0.md

The scoring contract should reference this as the official concrete scoring profile for the current benchmark version.

### 10.3 Update the scoring contract

Update `LUCID_SCORING_CONTRACT.md` so the current official profile is no longer underspecified.

Do not leave:

* `target_confidence_t`

* `calibrated-response criterion`

* abstention utility mapping

as vague placeholders.

### 10.4 Lock these scoring definitions

#### A. `target_confidence_t`

Use existing episode-spec fields where possible.

Define:

* for unresolved post-drift turns:
  
  * `target_confidence_t = uncertainty_ceiling`

* for final resolution turn when `response_mode in {ABSTAIN, CLARIFY}`:
  
  * `target_confidence_t = uncertainty_ceiling`

* for final resolution turn when `response_mode = ANSWER` and final success condition is satisfied:
  
  * `target_confidence_t = 1.0`

* for final resolution turn when `response_mode = ANSWER` and final success condition is not satisfied:
  
  * `target_confidence_t = final_calibration_epsilon`

This preserves a strict penalty for stale high confidence while allowing correct final confidence to rise after resolution.

#### B. calibrated-response criterion

Define the earliest eligible calibrated turn as the earliest eligible turn where the typed response is phase-compatible and confidence-compatible.

Use this rule:

A response at turn `t` is **calibrated** iff:

1. it occurs in an eligible scored post-drift turn, and

2. one of the following holds:
* **unresolved post-drift turn**
  
  * `confidence <= uncertainty_ceiling`

* **final turn, response_mode in {ABSTAIN, CLARIFY}**
  
  * `response_mode in acceptable_final_modes`
  
  * `confidence <= uncertainty_ceiling`

* **final turn, response_mode = ANSWER and final success condition satisfied**
  
  * `response_mode in acceptable_final_modes`
  
  * `confidence >= 1 - final_calibration_epsilon`

* **final turn, response_mode = ANSWER and final success condition not satisfied**
  
  * `response_mode in acceptable_final_modes`
  
  * `confidence <= final_calibration_epsilon`

This makes “calibrated” mean “confidence aligned with the state of certainty,” not just “confidence not too high.”

#### C. abstention utility `A`

Lock a deterministic table in the scoring profile.

Recommended M00 mapping:

**When the final state remains unresolved and non-answer modes are allowed**

* acceptable `ABSTAIN` or `CLARIFY` with `confidence <= uncertainty_ceiling` → `A = 1.0`

* `ANSWER` with `confidence <= uncertainty_ceiling` → `A = 0.5`

* any disallowed mode or overconfident response → `A = 0.0`

**When final resolution requires `ANSWER`**

* correct final answer + at least one guarded unresolved-turn behavior earlier → `A = 1.0`

* correct final answer without earlier guarded behavior → `A = 0.75`

* incorrect final answer with `confidence <= final_calibration_epsilon` → `A = 0.25`

* otherwise → `A = 0.0`

Define “guarded unresolved-turn behavior” as:

* `ABSTAIN`, or

* `CLARIFY`, or

* any response with `confidence <= uncertainty_ceiling`

This keeps permanent abstention from becoming globally optimal while still rewarding metacognitive caution.

### 10.5 Add worked examples

The scoring profile doc must include at least three worked examples:

* detected drift + early confidence drop + correct final answer

* stale overconfident wrong answer after drift

* wrong final answer with appropriately low confidence

### 10.6 Version honesty

Because these definitions change official scorer behavior, update the relevant contract headers and `docs/lucid.md` to benchmark version **1.1.0**.

* * *

11. Concrete template family documentation

------------------------------------------

Create:
    docs/families/LUCID_TEMPLATE_FAMILY_SYMBOLIC_NEGATION_V1.md

This should satisfy the template family contract directly.

### 11.1 Family identity

Recommended:

* `family_id = symbolic_negation_v1`

* `family_version = 1.0.0`

### 11.2 Rule-world choice

Use a small symbolic attribute world.

Recommended shape:

* each item has a short ID and a few discrete attributes

* the model learns a local selection rule

* drift negates the rule

* output is a typed answer over candidate IDs

### 11.3 Family fields that must be declared

Include:

* rule-world description

* allowed rule operators

* allowed drift operators

* output domain

* ambiguity / contradiction affordances

* difficulty knobs

* family scoring notes

### 11.4 M00 family constraints

For M00, keep it deliberately clean:

* only **NEGATION** drift

* no clarification branch

* explicit drift onset

* deterministic candidate generation

* one final typed answer

* confidence always required

* minimal but real ambiguity window

### 11.5 Difficulty knobs

At minimum include:

* number of candidate items

* attribute cardinality

* pre-drift rule complexity

* distractor similarity

* drift cue explicitness

* drift severity

### 11.6 Example episodes

Document at least:

* one LOW severity example

* one MEDIUM severity example

* one HIGH severity example

* * *

12. Local minimal green path implementation

-------------------------------------------

M00 should include a real local smoke path, not docs alone.

### 12.1 Implement the minimum modules

Create minimal, typed, documented implementations for:

* `generator.py`

* `drift.py`

* `parser.py`

* `scorer.py`

* `writer.py`

* `runner.py`

These should map directly to the operating manual’s component model.

### 12.2 Minimal functional behavior

The local pipeline must support:
    generate deterministic episode
    → simulate / accept typed response
    → parse response
    → score with official profile
    → write artifact bundle

### 12.3 Typed response enforcement

Use a strict typed response model for:

* `answer`

* `confidence`

* `response_mode`

* `drift_detected`

Reject free-form scoring logic.

### 12.4 Artifact writing

The local writer must emit a deterministic bundle shape compatible with the artifact contract:
    episode_<episode_id>/
      episode_spec.json
      episode_result.json
      bundle_manifest.json
      hashes.json

Use canonical JSON and stable hashing.

### 12.5 Local runner

Add:
    scripts/run_local_smoke.py

The script should:

* generate one deterministic episode from the concrete family

* run a fixed typed response fixture

* score it

* write a bundle

* print the output path and summary score

This is M00’s executable proof.

* * *

13. Testing and verification in M00

-----------------------------------

M00 should leave behind a repo that already tests its own semantics.

### 13.1 Add tests for scoring semantics

At minimum:

* `test_target_confidence_table`

* `test_calibrated_response_criterion`

* `test_abstention_utility_mapping`

* `test_confidence_overhang_unresolved_turns`

* `test_final_correct_high_confidence_is_not_penalized`

### 13.2 Add tests for family determinism

At minimum:

* same seed + same profile → identical episode spec

* different seed → different episode spec when intended

* drift onset serialized correctly

* difficulty knobs respected

### 13.3 Add local E2E smoke test

One test must run the full local minimal green path and verify:

* bundle directory exists

* required artifact files exist

* hashes file is stable

* score fields are populated

* the run is deterministic

### 13.4 CI

Add a truthful baseline CI workflow that runs on PR and main:

* Ruff

* mypy

* pytest

Because the codebase will still be small in M00, require strong coverage from the start.

Recommended threshold:

* **85%+** on `src/lucid/`

* * *

14. README and repo-facing communication

----------------------------------------

Update `README.md` so a new contributor immediately sees:

* what LUCID is

* that it targets metacognitive calibration under instructional drift

* that it is a benchmark, not a solver

* where the authoritative docs are

* how to run the local smoke path

* that Kaggle E2E is reserved for M01

* * *

15. Required M00 deliverables

-----------------------------

By the end of M00, Cursor should have produced all of these:

### Docs

* initialized `docs/lucid.md`

* `docs/LUCID_BOUNDARIES.md`

* `docs/LUCID_ASSUMED_GUARANTEES.md`

* `docs/LUCID_STACK_INTERACTION.md`

* `docs/LUCID_TERMINOLOGY_GUIDE_LLM.md`

* `docs/LUCID_COMPETITION_ALIGNMENT.md`

* `docs/contracts/LUCID_SCORING_PROFILE_v1.1.0.md`

* updated `docs/contracts/LUCID_SCORING_CONTRACT.md`

* updated change-control references as needed

* `docs/families/LUCID_TEMPLATE_FAMILY_SYMBOLIC_NEGATION_V1.md`

### Repo / code

* initialized package scaffold

* minimal local benchmark modules

* local smoke runner

* tests

* baseline CI

### Cleanup

* archived master bundle

* updated references to canonical contract docs

* added M01 placeholder in `docs/lucid.md`

* * *

16. Acceptance criteria for M00

-------------------------------

M00 is complete only when all of the following are true:

1. the repo is initialized and installable

2. `docs/lucid.md` is live and no longer placeholder-grade

3. the three missing adjacent docs exist and are referenced correctly

4. the master bundle is archived and clearly marked non-canonical

5. the scoring contract is no longer underspecified

6. the benchmark version is updated honestly to reflect semantic lock

7. one concrete family is fully documented

8. one local deterministic end-to-end smoke run succeeds

9. artifact bundle writing works locally

10. tests pass

11. CI is green

12. `docs/lucid.md` explicitly records M01 as Kaggle E2E priority

* * *

17. Cursor execution sequence

-----------------------------

Cursor should implement M00 in this order:

1. create milestone folder and save this plan as `M00_plan.md`

2. bootstrap repo structure

3. initialize `docs/lucid.md`

4. archive master bundle and normalize authority map

5. create the three adjacent docs

6. create terminology guide

7. create competition alignment doc

8. lock scoring semantics and version bump

9. create concrete family doc

10. implement local minimal green path

11. add tests and CI

12. run local verification

13. push branch and monitor CI

14. fix CI until green

15. close out M00

16. seed M01 stub and record it in `docs/lucid.md`

* * *

18. Explicit closeout instructions for Cursor

---------------------------------------------

At milestone close, Cursor must do all of the following:

1. generate `M00_summary.md`

2. generate `M00_audit.md`

3. record:
   
   * branch used
   
   * merge SHA
   
   * CI runs
   
   * whether all acceptance criteria passed

4. merge only after CI is green

5. do **not** make post-close fixes on the closed M00 branch

6. create the next milestone folder for M01

7. seed:
   
   * `M01_plan_stub.md`
   
   * `M01_toolcalls.md` if your workflow expects it

8. update `docs/lucid.md` with:
   
   * M00 complete
   
   * M01 next
   
   * M01 priority = Kaggle Community Benchmarks E2E verification

### M01 stub must say, at minimum

    M01 priority:
    End-to-end verification through Kaggle Community Benchmarks.
    
    Target:
    Prove that LUCID’s local benchmark structure can be expressed through Kaggle’s task/benchmark workflow, run against the platform correctly, and measured without changing core benchmark semantics.

* * *

19. Short handoff note for Cursor

---------------------------------

Use this as the execution posture:

* prefer the benchmark’s identity over convenience

* prefer honest version bumps over quiet semantic edits

* prefer one strong family over vague family lists

* prefer a real local smoke run over aspirational prose

* do not claim Kaggle compatibility before M01 proves it

* do not let `docs/lucid.md` remain weak or secondary

This M00 plan is the right shape for winning: it locks the semantics judges will care about, gives the repo a truthful spine, and preserves Kaggle platform proof as a focused next milestone rather than mixing platform risk into foundational benchmark design.
