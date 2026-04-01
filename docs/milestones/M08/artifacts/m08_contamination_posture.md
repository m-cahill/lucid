# M08 — Contamination resistance posture (LUCID)

**Project:** LUCID  
**Artifact:** `docs/milestones/M08/artifacts/m08_contamination_posture.md`  
**Benchmark version:** **1.1.0** (unchanged in M08)  
**Role:** Honest, audit-facing statement of how this repository argues **contamination resistance** — not absolute immunity.

---

## 1. Factual construction posture

LUCID episodes are **synthetic**: programmatically generated from fixed templates, explicit drift parameters, and **integer seeds**, serialized into canonical manifests with **lineage** back to per-family source packs. There is **no** reliance on scraped web text, licensed benchmark dumps, or third-party “gold” labels as the primary source of tasks.

Concrete mechanisms:

- **Deterministic regeneration:** Family and unified manifests are reproducible from versioned Python modules (`--write` / `--check` discipline).
- **Committed provenance:** Each unified row carries `source_pack_id`, `source_episode_id`, and `source_episode_spec_hash` (SHA-256 over canonical `episode_spec` JSON).
- **No public benchmark-sourced examples** as the dataset spine: the instrument is built as a **rule-world** evaluator, not a remix of external items.

This is the strongest honest claim LUCID can make without overreaching: the **construction pipeline** is inspectable and the **labels** trace to generation code, not crowd annotation.

---

## 2. What “contamination resistance” means here

In this repository, **contamination resistance** means:

1. **Reduced memorization surface** versus static, widely mirrored datasets — tasks are parameterized synthetic instances, not single fixed strings lifted from public leaderboards.
2. **Auditability** — judges and reviewers can reconstruct *what* was measured from committed manifests and code, not from opaque bundles.
3. **Explicit drift semantics** — performance is tied to **instruction change** and **calibration behavior**, not to a single static prompt idiom.

It does **not** mean models cannot benefit from generic skills (reading, arithmetic, following instructions). Any benchmark that uses language has *some* overlap with pretraining. The claim is **narrower and structural**, not absolute.

---

## 3. Realistic leakage and attack vectors (acknowledged)

**Public repository visibility.** Once code, manifests, and generators are public, the *distribution* of templates and seeds is visible. A motivated party could train or adapt on disclosed artifacts. LUCID mitigates **accidental** training-set overlap more than **adversarial** reproduction of the exact benchmark snapshot. Future freezes (e.g., submission lock) should be explicit about what is considered “the” evaluated pack.

**Template and skeleton repetition.** Synthetic generation often reuses **phrasing scaffolds** across episodes. Models may exploit **format familiarity** rather than true drift detection. The M08 soft-similarity layer surfaces high-surface overlap as **informational** signal; it does not pretend that overlap is impossible.

**Hosted-model exposure.** Running on Kaggle (or other hosts) exposes prompts to platform logging and retention policies according to the provider’s terms. That is distinct from web-scraped training contamination but is still an **operational exposure** that should be named in writeups when relevant.

**Contamination resistance ≠ contamination impossibility.** LUCID uses precise language on purpose: the benchmark is **designed to resist** trivial memorization narratives and to favor **on-the-fly rule tracking**, not to claim cryptographic impossibility of advantage.

---

## 4. How M08 supports the argument

M08 adds a **repeatable defensibility audit** (hard checks + soft heuristics) over the unified pack and source manifests, recorded under `docs/milestones/M08/artifacts/`. This advances **dataset quality & task construction** evidence: lineage integrity, duplicate accounting, and documented similarity posture — **without** substituting for Kaggle platform proof (still recorded separately when claimed).

---

## 5. Judge-facing discipline

When claiming contamination-related properties in competition materials:

- Prefer **synthetic, seed-anchored construction** and **lineage-preserving manifests** as the core story.
- Cite **this artifact** and `docs/benchmark_quality/LUCID_DEFENSIBILITY_STANDARD.md` for definitions (hard vs soft checks, versioning discipline).
- Avoid absolute claims (“cannot leak”, “models cannot memorize”) unless formally true under stated threat models; use **resistance**, **auditability**, and **controlled drift** instead.
