# M11 — Allocation policy (empirical)

Each model receives one **allocation_action** using deterministic rules below. This is operational guidance, not a statistical model.

## Rules (in order)

1. If **P12** is not `completed` → `stop_spending_budget` (no reliable cheap probe signal).
2. Else if **P24** / **P48** / **P72** exports are missing for higher tiers → `repeat_for_stability` or `keep_at_mid_tier` until ladder runs exist.
3. Else if **P72** `completed` → `push_harder` if score_delta_vs_M01 ≥ 0 OR score_mean ≥ median P72 among completers; else `keep_at_mid_tier`.
4. Else → `keep_at_mid_tier`.

| model_slug | allocation_action | rationale |
|------------|-------------------|-----------|
| `claude-haiku-4-5-20251001` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `claude-opus-4-1-20250805` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `claude-opus-4-5-20251101` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `claude-opus-4-6-default` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `claude-sonnet-4-20250514` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `claude-sonnet-4-5-20250929` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `claude-sonnet-4-6-default` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `deepseek-v3.1` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `deepseek-v3.2` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `gemini-2.0-flash-001` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `gemini-2.0-flash-lite-001` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `gemini-2.5-flash` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `gemini-2.5-pro` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `gemini-3-flash-preview` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `gemini-3.1-flash-lite-preview` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `gemini-3.1-pro-preview` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `gemma-3-12b-it` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `gemma-3-1b-it` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `gemma-3-27b-it` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `gemma-3-4b-it` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `gemma-4-26b-a4b-it` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `gemma-4-31b-it` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `glm-5` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `gpt-5.4-2026-03-05` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `gpt-5.4-mini-2026-03-17` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `gpt-5.4-nano-2026-03-17` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `gpt-oss-20b` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `qwen3-235b-a22b-instruct-2507` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `qwen3-coder-480b-a35b-instruct` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `qwen3-next-80b-a3b-instruct` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
| `qwen3-next-80b-a3b-thinking` | `repeat_for_stability` | Higher-tier probe exports not present — rerun ladder when exports exist. |
