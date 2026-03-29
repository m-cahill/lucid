# LUCID Submission Doctrine

**Project:** LUCID  
**Benchmark Version:** 1.0.1  
**Document Type:** Non-runtime doctrine  
**Authority:** Writeup, disclosure, and reporting posture  
**Status:** Frozen

---

## 1. Purpose

This doctrine governs how LUCID results are reported.

It does not change runtime semantics, scoring formulas, or episode generation.

---

## 2. Required disclosures

Any serious benchmark report SHOULD disclose:

- benchmark version
- template families used
- scoring profile version
- model identifiers
- decoding / prompting conditions
- parser version
- scorer version
- sample sizes by family and drift type

---

## 3. Reporting posture

LUCID reports SHOULD emphasize:

- one flagship faculty
- one canonical score
- clear component metrics
- family-level and drift-level breakdowns
- explicit uncertainty and benchmark limits

Reports SHOULD NOT claim unsupported breadth or hidden evaluator magic.

---

## 4. One-line summary

> LUCID reporting should be narrow, explicit, versioned, and honest: one faculty, one benchmark story, full disclosure of what produced the numbers.
