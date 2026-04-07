# M11 — P24 candidate cohort (cost-aware)

Narrative priority: **collapse**, **inversion**, and **cost frontier** — not small midfield rank moves.

**Comparator:** `lucid_main_task` (``delta_vs_main_task`` = P12 mean − main-task mean).
**Cost assumption:** total observed cost for running this model on the P12 probe task (operator CSV; per-model total for this pass)

## Data-quality (cost)

- Two CSV rows labeled 'Gemini 2.5 Flash' were merged by summing cost ($0.15 + $0.03 → $0.18). This is conservative: it may reflect two separate billed batches for the same model.

## P24 cohort table

| cohort_role | model_slug | p12_mean | delta_vs_main_task | p12_cost_usd | notes |
|---|---|---:|---:|---:|---|
| `collapse_signal` | `gpt-5.4-mini-2026-03-17` | 0.649854 | -0.243563 | 0.03 |  |
| `collapse_signal` | `glm-5` | 0.674687 | -0.218229 | 0.14 |  |
| `collapse_signal` | `gpt-5.4-nano-2026-03-17` | 0.581208 | -0.164458 | 0.01 |  |
| `collapse_signal` | `gemma-3-12b-it` | 0.611938 | -0.062479 | 0.01 |  |
| `inversion_signal` | `deepseek-v3.1` | 0.709375 | +0.243125 | 0.02 |  |
| `inversion_signal` | `deepseek-v3.2` | 0.772292 | +0.121042 | 0.04 |  |
| `inversion_signal` | `claude-opus-4-5-20251101` | 0.738708 | +0.073292 | 0.87 | Expensive near-duplicate of other Opus/Sonnet anchors — narratively optional. |
| `inversion_signal` | `claude-opus-4-6-default` | 0.725521 | +0.065604 | 0.88 | Expensive near-duplicate of other Opus/Sonnet anchors — narratively optional. |
| `efficiency_anchor` | `qwen3-coder-480b-a35b-instruct` | 0.853646 | -0.040521 | 0.01 | Promoted as efficiency anchor when score-per-dollar is strong (see cost frontier CSV). |
| `top_tier_anchor` | `claude-sonnet-4-20250514` | 0.924063 | +0.024896 | 0.52 |  |
| `top_tier_anchor` | `claude-opus-4-1-20250805` | 0.923750 | +0.028333 | 2.56 |  |
| `top_tier_anchor` | `gemini-2.5-pro` | 0.895417 | +0.002500 | 1.15 | Optional for P24; consider dropping before P48 unless uniquely informative. |
| `top_tier_anchor` | `claude-sonnet-4-5-20250929` | 0.888854 | -0.006063 | 0.52 |  |

## Cost-efficiency (P12)

| model_slug | p12_mean | p12_cost_usd | mean_per_usd | delta_vs_main_task |
|---|---:|---:|---:|---:|
| `qwen3-coder-480b-a35b-instruct` | 0.853646 | 0.01 | 85.3646 | -0.040521 |
| `gemini-2.0-flash-lite-001` | 0.692812 | 0.01 | 69.2812 | +0.027396 |
| `gpt-oss-20b` | 0.691354 | 0.01 | 69.1354 | -0.031229 |
| `gemma-4-31b-it` | 0.674687 | 0.01 | 67.4688 | +0.026771 |
| `gemma-3-27b-it` | 0.650833 | 0.01 | 65.0833 | -0.026333 |
| `gemma-3-12b-it` | 0.611938 | 0.01 | 61.1938 | -0.062479 |
| `gpt-5.4-nano-2026-03-17` | 0.581208 | 0.01 | 58.1208 | -0.164458 |
| `deepseek-v3.1` | 0.709375 | 0.02 | 35.4688 | +0.243125 |
| `qwen3-next-80b-a3b-instruct` | 0.693438 | 0.02 | 34.6719 | +0.023021 |
| `gemma-4-26b-a4b-it` | 0.677188 | 0.02 | 33.8594 | +0.024271 |
| `gemma-3-1b-it` | 0.500104 | 0.02 | 25.0052 | +0.041354 |
| `gemma-3-4b-it` | 0.482958 | 0.02 | 24.1479 | +0.015458 |
| `gemini-2.0-flash-001` | 0.690625 | 0.03 | 23.0208 | +0.010208 |
| `qwen3-235b-a22b-instruct-2507` | 0.677292 | 0.03 | 22.5764 | -0.001875 |
| `gpt-5.4-mini-2026-03-17` | 0.649854 | 0.03 | 21.6618 | -0.243563 |
| `deepseek-v3.2` | 0.772292 | 0.04 | 19.3073 | +0.121042 |
| `gemini-3.1-flash-lite-preview` | 0.676875 | 0.04 | 16.9219 | +0.021458 |
| `qwen3-next-80b-a3b-thinking` | 0.675312 | 0.06 | 11.2552 | +0.024896 |

## Expensive / narratively optional

- **Gemini 2.5 Pro** — optional P24; likely drop-before-P48 unless it proves uniquely informative.
- **Claude Opus 4.6** vs **Claude Opus 4.5**: both carry premium cost; keep at most one unless the inversion/collapse story needs both.

