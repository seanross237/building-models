# Exploration 001 Summary: Line-by-Line Decomposition Audit of β = 4/3

## Goal
Extract the precise chain of inequalities in Vasseur (2007) Proposition 3 that produces β = 4/3, classify each step as sharp or potentially loose, build a sensitivity table, and cross-compare with the Vasseur-Yang (2021) vorticity formulation.

## What was tried
Read both papers in full. Traced all 6 steps of the Proposition 3 proof (pages 14–24), identifying 8 distinct inequality applications with their tools, exponents, and sharpness. Built sensitivity table. Identified 5 free parameters. Cross-compared with Section 5 of Vasseur-Yang 2021.

## Outcome: SUCCESS

The 4/3 = 1/2 + 5/6 decomposes into a chain of 5 links, of which **4 are provably sharp and 1 is potentially loose**:

- **1/2**: from ||d_k||_{L²} ≤ U_{k-1}^{1/2} — definitional, immovable
- **5/6**: from a chain: Sobolev H¹→L⁶ (sharp) → parabolic interpolation to L^{10/3} (sharp) → Chebyshev at level 2^{-k} giving measure bound U^{5/3} (**potentially loose for NS**) → L² norm = U^{5/6} (sharp)

The bottleneck term in both formulations is a **non-divergence-form quadratic interaction** — the local pressure -P_{k21}·div(uv_k/|u|) in velocity, or the non-divergence trilinear term in vorticity. Both force the same Hölder pairing: gradient (1/2) × indicator (5/6).

## Key takeaway
**The Chebyshev inequality at the truncation level set is the single potentially improvable step.** It is sharp for arbitrary L^{10/3} functions but may not be tight for NS solutions. Improving |{v_{k-1} > 2^{-k}}| ≤ C^k U_{k-1}^{5/3} to U_{k-1}^{5/3+δ} with δ > 1/3 would break the barrier. No free parameters in the proof can help — the truncation shape, Sobolev exponents, Hölder pairs, and pressure decomposition are all optimized or irrelevant to β.

## Unexpected findings
The cross-comparison confirms something profound: the 4/3 is **intrinsic to the NS quadratic nonlinearity**, not to the pressure handling. Taking curl eliminates the pressure entirely but the same 4/3 reappears from vortex stretching. The pressure and the vortex stretching are dual manifestations of the same obstruction — u⊗u cannot be put in divergence form relative to the truncated variables.

## Computations identified
- **Level-set distribution for NS near singularities:** Numerically compute |{|u| > λ}| near potential blow-up scenarios (e.g., from DNS of high-Re flows or self-similar blow-up candidates). Compare with the Chebyshev prediction λ^{-10/3}·(energy)^{5/3}. If the actual decay is faster, this would indicate room for improvement. Difficulty: moderate (DNS data + post-processing), but interpreting results requires care.
