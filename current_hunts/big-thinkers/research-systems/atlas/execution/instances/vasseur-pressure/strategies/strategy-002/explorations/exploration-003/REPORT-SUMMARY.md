# Exploration 003 Summary: Analytical Chebyshev Improvement and Model PDE Comparison

## Goal
Determine whether the Chebyshev estimate |{v_{k-1} > 2^{-k}}| ≤ C^k U_{k-1}^{5/3} can be analytically improved for NS solutions, and test universality of the 4/3 barrier across model PDEs.

## What was tried
1. Surveyed distributional estimates for structured functions (div-free, energy-bounded, parabolic) — checked CLMS (1993), Bourgain-Brezis (2004/2007), Van Schaftingen (2004/2013), Lorentz space theory.
2. Analyzed support-restricted Chebyshev, Holder interpolation with alternative exponents q, and isoperimetric/coarea approaches.
3. Computed De Giorgi β values for 1D Burgers, 2D NS, critical SQG, 3D MHD, and fractional NS (varying α).
4. Detailed analysis of Caffarelli-Vasseur (2010) SQG success mechanism via harmonic extension.

## Outcome: SUCCEEDED — All deliverables met

**The Chebyshev step is NOT independently improvable.** Every attempted route was ruled out:
- Support-restricted Chebyshev: weaker than direct Chebyshev in the convergent regime
- Holder interpolation with q ≠ 10/3: total U-exponent is 5/3 regardless of q (flat optimization)
- Lorentz space refinements: affect constants, not decay exponents
- Div-free constraint on |u|: no known mechanism; question appears OPEN but evidence strongly suggests NO (truncation to |u| > λ destroys divergence-free structure)

**Universal formula discovered: β = 1 + s/n** for dissipation H^s in dimension n. Confirmed across all PDEs tested. SQG succeeds not by beating this formula at Chebyshev, but by having the drift enter multiplicatively (not as extra U_{k-1} power) — no pressure.

## Key takeaway
**The Chebyshev step faithfully reflects the integrability gap between the energy space and the Serrin threshold.** Improving it from L^{10/3} to L^4 is equivalent to improving regularity from H^1 to H^{5/4} (the Lions threshold) — circular. The gap β = 4/3 vs 3/2 is NOT a proof artifact but a faithful encoding of the NS regularity gap. Routes 5 and 6 on the ranked list (Lorentz, support-restricted) are definitively ruled out. Route 3 (commutator improvement of the nonlinear estimate, following the SQG precedent) is the most promising remaining direction.

## Unexpected findings
- The question "does div(u) = 0 improve |{|u| > λ}|?" is genuinely open — no paper addresses it. Strong heuristic evidence says NO (div constrains direction, not magnitude), but a rigorous proof either way would be publishable.
- De Giorgi β for fractional NS reaches 3/2 only at α = 3/2, missing the Lions regularity threshold α = 5/4. The gap (17/12 vs 3/2 at α = 5/4) quantifies how much iterative energy bootstrapping gains over single-step De Giorgi.
- SQG in the Caffarelli-Silvestre extension has β = 4/3 (same as 3D NS!) — the improvement is entirely in how the drift couples, not in the Chebyshev chain.

## Computations identified
1. **Distributional sharpness test (numerical):** On DNS data near potential singularities, compute |{|u| > λ}| and compare with λ^{-10/3}·(energy)^{5/3}. If actual decay is faster, Chebyshev has slack for NS solutions specifically. Moderate difficulty (50-line Python on existing DNS post-processing). Would settle the open question empirically.
2. **Commutator estimate for P_{k21}:** Compute whether the non-divergence-form pressure interaction P_{k21}·div(uv_k/|u|) has Hardy space (H^1) structure exploitable via CLMS-type compensated compactness. Would require symbolic computation of the specific bilinear form. Medium difficulty (100-line Mathematica/sympy script). Would determine if Route 3 is viable.
