# M11 — Analytical summary (data-bound)

Derived **only** from `m11_model_response_surface` rows. **No** family/difficulty/component slices from aggregate M09 exports.

## 1. Completion coverage by tier

- **P12:** 0 / 31 rows `completed`
- **P24:** 0 / 31 rows `completed`
- **P48:** 0 / 31 rows `completed`
- **P72:** 15 / 31 rows `completed`

## 2. Ladder score slope (P12 → P72)

**Not computable** with current ingest: need **≥2** completed tiers with numeric `score_mean` per model. Re-run ingest after P12/P24/P48 leaderboard exports exist.

## 3. Sharp degradation / stability (heuristic)

Requires **≥2** numeric tier means per model. With only **P72** numeric for most models, degradation vs ladder size is **not** measured here—**blocked** until smaller-tier exports exist.

## 4. P72 completed — largest negative Δ vs M01 (anomaly signal)

| model_slug | p72_mean | delta_vs_M01 |
|---|---:|---:|
| `gpt-5.4-mini-2026-03-17` | 0.645132 | -0.248285 |
| `glm-5` | 0.660816 | -0.232101 |
| `qwen3-coder-480b-a35b-instruct` | 0.743299 | -0.150868 |
| `gpt-5.4-nano-2026-03-17` | 0.612000 | -0.133667 |
| `gemini-2.5-pro` | 0.815712 | -0.077205 |
| `gemini-2.0-flash-lite-001` | 0.645278 | -0.020139 |
| `qwen3-next-80b-a3b-instruct` | 0.654358 | -0.016059 |
| `gemini-3.1-flash-lite-preview` | 0.642743 | -0.012674 |
| `qwen3-next-80b-a3b-thinking` | 0.651858 | +0.001441 |
| `gemini-2.0-flash-001` | 0.683559 | +0.003142 |
| `gemini-2.5-flash` | 0.652378 | +0.004462 |
| `gemini-3-flash-preview` | 0.662378 | +0.024462 |
| … | … | *(truncated; 15 total)* |

## 5. Repeat lane (P12_repeat)

Repeatability is **P12** episode IDs rerun on the same task. **No** duplicate run rows exist in leaderboard CSV ingest—track repeat runs as separate exports or manual notes.
