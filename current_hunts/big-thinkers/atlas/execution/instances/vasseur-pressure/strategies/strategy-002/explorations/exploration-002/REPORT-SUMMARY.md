# Exploration 002 Summary: Level-Set Distribution vs Chebyshev Bound

## Goal
Measure whether 3D Navier-Stokes solutions have faster tail decay than the Chebyshev prediction μ(λ) ~ λ^{-10/3}, and quantify the De Giorgi tightness ratios.

## What Was Tried
Ran 7 DNS cases (Taylor-Green, Random Gaussian, ABC flow at Re=100-1600) at N=128 and N=64. Computed μ(λ) power-law exponents and De Giorgi tightness ratios (Chebyshev bound / actual A_k) for k=1..10.

## Outcome: Mixed — Significant Slack Exists but Cannot Improve β

**μ(λ) tail exponents are IC-dependent:**
- Taylor-Green: p ≈ 10 (3× the Chebyshev exponent 10/3)
- Random Gaussian: p ≈ 8-9 (2.5×), with excellent R² ≈ 0.95
- **ABC Beltrami flow: p ≈ 2.1, BELOW 10/3** — Chebyshev is tight here

**De Giorgi tightness ratios are approximately constant at 3-5×**, independent of k and flow type. This constant slack does NOT improve β = 4/3 — it only changes the constant C in the recurrence U_k ≤ C^k · U_{k-1}^β. To improve β, one needs slack scaling as U_{k-1}^{-δ}, which is not observed.

## Verification Scorecard
- **[COMPUTED]:** 5 claims (μ(λ) exponents across 7 cases/~30 snapshots, tightness ratios for k=1..10, tightness ratio k-scaling, IC-dependent behavior, ABC worst-case)
- **[CHECKED]:** 1 (N=64 vs N=128 consistency)
- **[CONJECTURED]:** 3 (implications for β, persistence for near-singular solutions, structural nature of barrier)

## Key Takeaway
The Chebyshev step in Vasseur's proof has moderate constant slack (~3-5× at each De Giorgi level) but this slack does not accumulate in the right way to improve β. The ABC flow shows Chebyshev can be tight for global distributions (p < 10/3). **The β = 4/3 barrier appears structural, not distributional.**

## Leads Worth Pursuing
- The constant ~3-5× tightness is a geometric property of L^{10/3} on T³ — understanding WHY it's constant could reveal the true bottleneck
- Investigate whether divergence-free + energy inequality together constrain the tightness ratio's U_{k-1}-dependence
- The ABC flow's unique behavior (p < 10/3 but tightness ratios comparable to other flows) deserves analytical investigation
