# M11 — Allocation policy (empirical)

Each model receives one **allocation_action** using deterministic rules below. This is operational guidance, not a statistical model.

## Rules (in order)

1. If **P12** is not `completed` → `stop_spending_budget` (no reliable cheap probe signal).
2. Else if **P24** / **P48** / **P72** exports are missing for higher tiers → `repeat_for_stability` or `keep_at_mid_tier` until ladder runs exist.
3. Else if **P72** `completed` → `push_harder` if score_delta_vs_M01 ≥ 0 OR score_mean ≥ median P72 among completers; else `keep_at_mid_tier`.
4. Else → `keep_at_mid_tier`.

| model_slug | allocation_action | rationale |
|------------|-------------------|-----------|
| `claude-haiku-4-5-20251001` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `claude-opus-4-1-20250805` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `claude-opus-4-5-20251101` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `claude-opus-4-6-default` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `claude-sonnet-4-20250514` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `claude-sonnet-4-5-20250929` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `claude-sonnet-4-6-default` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `deepseek-v3.1` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `deepseek-v3.2` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `gemini-2.0-flash-001` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `gemini-2.0-flash-lite-001` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `gemini-2.5-flash` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `gemini-2.5-pro` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `gemini-3-flash-preview` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `gemini-3.1-flash-lite-preview` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `gemini-3.1-pro-preview` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `gemma-3-12b-it` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `gemma-3-1b-it` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `gemma-3-27b-it` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `gemma-3-4b-it` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `gemma-4-26b-a4b-it` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `gemma-4-31b-it` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `glm-5` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `gpt-5.4-2026-03-05` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `gpt-5.4-mini-2026-03-17` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `gpt-5.4-nano-2026-03-17` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `gpt-oss-20b` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `qwen3-235b-a22b-instruct-2507` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `qwen3-coder-480b-a35b-instruct` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `qwen3-next-80b-a3b-instruct` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
| `qwen3-next-80b-a3b-thinking` | `stop_spending_budget` | P12 not completed — do not escalate spend. |
