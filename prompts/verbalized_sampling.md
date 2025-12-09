---
name: Verbalized Sampling (Tail Sampling for Creative Diversity)
description: Generate diverse, creative responses by sampling from tail of probability distribution
---

# Verbalized Sampling Mode

**Research**: Based on [Zhang et al. (2025)](https://www.verbalized-sampling.com/) - "Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity"

## Instructions

Generate 5 responses to the user query, each within a separate `<response>` tag. Each `<response>` must include a `<text>` and a numeric `<probability>`.

**Critical**: Please sample at random from the **tails of the distribution**, such that the probability of each response is **less than 0.10**.

## Output Format

```xml
<response>
  <text>First approach to the problem...</text>
  <probability>0.08</probability>
</response>

<response>
  <text>Second creative alternative...</text>
  <probability>0.07</probability>
</response>

<response>
  <text>Third diverse perspective...</text>
  <probability>0.09</probability>
</response>

<response>
  <text>Fourth unconventional solution...</text>
  <probability>0.06</probability>
</response>

<response>
  <text>Fifth exploratory approach...</text>
  <probability>0.08</probability>
</response>
```

## Why Tail Sampling?

- **Mode collapse**: Aligned models always give the "safest" typical response (mode of distribution)
- **Tail diversity**: Creative, diverse responses live in the tail (probability < 0.10)
- **Result**: 1.6-2.1× diversity increase without sacrificing accuracy

---

**Now respond to the user's query with 5 diverse tail-sampled responses:**
