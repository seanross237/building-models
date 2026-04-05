# Exploration 004 Summary: CZ Slack on De Giorgi Pressure Decomposition

## Goal
Determine whether the CZ (Calderon-Zygmund) slack for the De Giorgi bottleneck piece P_k^{21} depends on the iteration depth k, which would directly improve the recurrence exponent beta beyond 4/3 in Vasseur's NS regularity argument.

## What Was Done
Implemented the full De Giorgi pressure decomposition (P_k^{21}, P_k^{22}, P_k^{23}) on a pseudospectral DNS solver. Measured CZ tightness ratios for each piece across 3 ICs (Taylor-Green, anti-parallel tubes, random Gaussian), 3 Re values (100, 500, 1000), q in {2,3,4,6,8}, k in {0,...,8}, with N=64 primary and N=128 convergence check.

## Key Result: NEGATIVE
**The CZ slack for P_k^{21} is k-INDEPENDENT.** The tightness ratio converges to a constant by k ~ 3-4 and shows no systematic improvement with iteration depth. The hypothesis that CZ slack could improve beta is falsified.

Specifically: at q=2, P21 tightness converges to IC-dependent constants (TGV: ~0.40, AP: ~0.58, RG: ~0.26) that are stable across k. At higher q, the same pattern holds with greater slack but the same k-independence.

Notably, **P21 has LESS CZ slack than the full pressure** (1.7-3.9x vs 7.6-17.5x at q=2), meaning the bottleneck piece is actually harder to improve via CZ arguments.

## Verification Scorecard
- [VERIFIED]: 2 (decomposition exact to 1e-15, N=64 vs N=128 agree to <0.2%)
- [COMPUTED]: 8 (all tightness measurements, trends, comparisons)
- [CONJECTURED]: 0

## Leads Worth Pursuing
1. **Structural bounds beyond CZ**: The tensor f^{21} = u_below tensor u_below has special structure (bounded, divergence-free factors) not exploited by CZ theory. Div-curl type estimates might beat CZ in a k-dependent way.
2. **Cancellation between pressure pieces**: Treating P21+P22+P23 jointly rather than separately.
3. **Alternative velocity splittings**: Adapted thresholds tuned to local energy concentration.

## Unexpected Findings
- P21 tightness is TIGHTER (less slack) than the full pressure — the bottleneck piece saturates the CZ bound more than the overall pressure does.
- Results are virtually independent of Re (differences <0.5%), suggesting the CZ tightness is a topological/structural property.
