# Exploration 006 Summary: Beltrami-Near Structure and Geometric Conditional Regularity

## Goal
Survey geometric regularity criteria for NS exploiting velocity-vorticity alignment. Determine whether Beltrami-near structure can improve the De Giorgi recurrence exponent β.

## What Was Tried
Surveyed Constantin-Fefferman (1993), Beirao da Veiga-Berselli (2002), Chae-Lee (2002), and Vasseur (2007) geometric regularity criteria. Derived and numerically verified the pressure structure of exact Beltrami flows. Performed perturbation analysis for near-Beltrami flows. Assessed viability of conditional regularity via Beltrami deficit.

## Outcome: SUCCESS — Grade (B): Promising but needs work

**The mechanism is identified and verified.** For exact Beltrami flows (curl u = λu), the Lamb vector L = ω × u = 0 identically, so the nonlinear advection u·∇u = ∇(|u|²/2) is a pure gradient. This makes the pressure p = −|u|²/2 + const — a pointwise Bernoulli function requiring no Calderon-Zygmund inversion. The pressure Poisson source is a pure Hessian, so CZ "loss" is zero. This fully explains the DNS finding (exploration 002) that ABC flows have β_eff ≈ 1.0 vs 0.35–0.73 for other ICs.

For near-Beltrami flows (u = u_B + εv), the "bad" pressure requiring CZ bounds enters at O(ε) — the degradation is continuous and linear, confirmed numerically (Lamb vector and pressure deviation both scale as ε).

## Key Takeaway
The Beltrami pressure simplification is real and rigorously understood. The main obstacle to formalizing a conditional regularity result is that the De Giorgi truncation u_below breaks the Beltrami property — even when the full velocity u is Beltrami, the truncated velocity is not. A rigorous estimate of how much Beltrami structure survives in u_below is the critical missing piece.

## Leads Worth Pursuing
1. **Hessian/Lamb decomposition of P_k^{21}**: Split the bottleneck pressure into a CZ-lossless Hessian piece and a CZ-lossy Lamb piece. If the Lamb piece is subdominant (which the near-Beltrami analysis suggests for small deficit), β could improve.
2. **De Giorgi truncation vs Beltrami structure**: Quantify how much the truncation u → u_below degrades the Beltrami deficit — this is a computable question on DNS data.
3. **Geometric regularity criteria in De Giorgi framework**: No existing paper connects Constantin-Fefferman-type conditions to the De Giorgi iteration. This appears to be unexplored territory and could be novel.

## Unexpected Findings
- Exact Beltrami flows on T³ have the remarkable property that u(t) = u₀ exp(−νλ²t): exponential decay preserving spatial structure. They are trivially regular — the regularity question is only interesting for near-Beltrami flows.
- The gap between β_eff ≈ 1.0 (ABC) and β > 3/2 (regularity threshold) means even the best-case Beltrami structure is insufficient alone — the mechanism must be combined with something else.

## Computations Identified
1. **Beltrami deficit of u_below on DNS data**: For ABC flow at various Re, compute B(u_below) = ||curl(u_below) − λu_below||/||u_below|| as a function of De Giorgi level k. This reveals whether the truncation destroys or preserves Beltrami structure. ~50 lines Python, uses existing DNS infrastructure. Would determine whether the conditional regularity path is viable.
2. **Hessian vs Lamb decomposition of P_k^{21}**: Decompose the measured bottleneck integral into Hessian (CZ-lossless) and Lamb (CZ-lossy) contributions for ABC vs other ICs. ~100 lines. Would quantify the analytical leverage from Beltrami structure within the De Giorgi framework.
