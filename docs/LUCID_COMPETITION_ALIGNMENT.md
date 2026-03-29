# LUCID — competition alignment

**Project:** LUCID  
**Document type:** Alignment note (facts + scope boundaries)  
**Verification:** M00 = documentation only; **M01** = platform E2E proof  
**Last checked:** March 2026 (sources below)

---

## 1. Official competition

| Field | Value |
|-------|--------|
| **Name** | **Measuring Progress Toward AGI — Cognitive Abilities** |
| **Host / platform** | Kaggle |
| **Official competition URL** | https://www.kaggle.com/competitions/kaggle-measuring-agi |
| **Rules (authoritative for deadlines & requirements)** | https://www.kaggle.com/competitions/kaggle-measuring-agi/rules |

**Deadline and prize structure:** Kaggle’s **Rules** tab is authoritative; static mirrors and third-party articles may be wrong or stale. Open the Rules page directly before relying on any date.

---

## 2. Cognitive tracks (competition framing)

Partner and competition materials describe evaluation along multiple **cognitive** dimensions. Commonly referenced **five thematic tracks** include areas such as **learning**, **metacognition**, **attention**, **executive functions**, and **social cognition** — used to organize benchmark proposals and judging. **Exact labels and eligibility** can vary by phase; confirm on the **official competition Overview/Rules** pages.

LUCID is intentionally scoped to **metacognitive calibration under instructional drift**, consistent with the **metacognition** pillar, without claiming coverage of unrelated tracks.

---

## 3. Kaggle Benchmarks / Community Benchmarks (platform)

| Resource | URL |
|----------|-----|
| **Kaggle Benchmarks documentation** (overview, tasks, leaderboards) | https://www.kaggle.com/docs/benchmarks |
| **Benchmarks hub** | https://www.kaggle.com/benchmarks |
| **Community Benchmarks** (same technical substrate as research benchmarks; different sourcing) | Described in official docs above |
| **Python SDK / examples** | https://github.com/Kaggle/kaggle-benchmarks |

Official docs state that **tasks** are Python-defined evaluations and **benchmarks** are collections of tasks composed in the UI; leaderboards can be downloaded (including via API). The platform emphasizes **robustness**, **reproducibility**, and **transparency**.

**Token / cost / latency:** Task notebooks and platform execution may surface model-call metrics; see current Kaggle Benchmarks documentation and task notebook patterns for what is recorded for a given run.

---

## 4. LUCID scope vs milestones

| Milestone | What is verified |
|-----------|------------------|
| **M00** | Repo, contracts, **local** deterministic smoke path, baseline CI, **documentation alignment** with official Kaggle URLs and Benchmarks docs |
| **M01** | **Kaggle Community Benchmarks end-to-end** — prove LUCID can be expressed and run through the platform without changing benchmark semantics |

**Do not** claim in writeups that Kaggle E2E is complete **before M01** closes.

---

## 5. Supplementary context (non-Kaggle)

Google DeepMind’s public materials describe a **cognitive framework** for measuring progress toward AGI; these blog posts are useful **background** but do **not** replace Kaggle’s rules:

- https://deepmind.google/blog/measuring-progress-toward-agi-a-cognitive-framework/

---

## 6. One-line summary

> LUCID aligns with the **Measuring AGI — Cognitive Abilities** competition and **Kaggle Benchmarks** documentation; deadlines and rules come from Kaggle’s **Rules** tab, and platform proof is explicitly **M01**.
