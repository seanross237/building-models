# Meta-Learning Note — Exploration 001 (Strategy-002)

**Date:** 2026-03-27
**Task:** SED double-well barrier crossing with ALD vs WKB

## What Worked Well

1. **Pre-loading the ALD equation and ZPF noise formula verbatim** saved the explorer significant debugging time. Simulations ran in ~6 seconds per λ value — very efficient.

2. **Including the sanity check (HO var_x)** as a mandatory first step caught noise normalization issues early. Explorer got 0.471 (expected 0.500) — close enough to confirm correct normalization.

3. **Running parameter values sequentially** (λ=0.25 first, then 0.10, then 1.0) worked well. Each gave a clean result before moving to the next.

4. **Including the prior art search explicitly as a success criterion** meant the explorer actually did it and found the key Faria & Franca (2005) paper that makes the novelty case.

5. **Warning about escape vs. tunneling** was well-placed — the explorer discovered particles don't escape at all, which was the first key finding.

## What Didn't Work Well

1. **Explorer started late** — ~8-10 minutes of idle time before writing first REPORT.md line. "Write incrementally" instruction helped once started but initial startup was slow.

## Key Unexpected Finding

The 15% agreement at λ=0.25 was genuinely surprising. The formula Γ_SED/Γ_WKB ≈ exp(S_WKB − V_barrier/E_zpf) is a new testable prediction that emerged from the computation. This kind of quantitative insight is exactly what math explorations should produce.

## Scope Assessment

Scope was right. Three λ values was the correct amount — enough to see the pattern, not so many that the explorer got bogged down.

## Recommendations for Future Goals

- Always include E_zpf ≈ ħω₀√2/2 for the double-well specifically, so explorer can use V_barrier/E_zpf directly
- The Faria & Franca (2005) paper should be included in context for any follow-up tunneling explorations
- The formula Γ_SED/Γ_WKB ≈ exp(S_WKB − V_barrier/E_zpf) should be verified with more λ values in a follow-up
