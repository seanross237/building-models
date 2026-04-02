# Exploration 008 Summary: Proof of H_norm ≤ 1/12

## Goal

Prove analytically that H_norm = |HessS(v,v)| / (8(d-1)Nβ|v|²) ≤ 1/12 for all Q,v in
d=4 SU(2) Yang-Mills, with equality at Q=I, v=staggered mode.

## What was tried

1. Derived the exact plaquette Hessian at Q=I: H_□ = (β/(2N))|discrete curl of v|²
2. Evaluated the staggered mode explicitly: computed per-plaquette contributions and
   identified active (μ+ν odd) vs inactive (μ+ν even) planes.
3. Applied Fourier (Plancherel) analysis: decomposed the Hessian in momentum space and
   bounded by the maximum momentum factor |c_k|² ≤ 4d.
4. Proved a per-plaquette operator inequality: H_□(v;Q) ≤ H_□(v;Q=I) (for fixed v)
   via the fact that Re Tr(−B²U) is maximized over SU(N) at U=I.

## Outcome: PARTIAL SUCCESS

**Proved (rigorous):**
- At Q=I: H_norm_max = ⌈d/2⌉⌊d/2⌋/(N²d(d-1)) = **1/12** for d=4, N=2.
- Achieved by staggered mode v_{x,μ} = (−1)^{|x|+μ} v₀.
- Fourier analysis proves H_norm ≤ 1/12 at Q=I (tight in d=4).
- Per-plaquette: H_□(v;Q) ≤ H_□(v;Q=I) for fixed tangent vectors v (U=I maximizes).

**Not proved (open gap):**
- For general Q ≠ I: parallel transport modifies the tangent vectors as B_□(Q,v).
- Need ∑_□ |B_□(Q,v)|² ≤ 4d|v|² for all Q — not yet shown.
- Weaker bound proved rigorously: H_norm ≤ 1/8 for all Q (from triangle inequality).

## Key Takeaway

The tightest proved bound is:
- **H_norm ≤ 1/12 at Q=I** (complete proof via Fourier analysis)
- **H_norm ≤ 1/8 for all Q** (complete proof via triangle inequality)
- **H_norm ≤ 1/12 conjectured for all Q** (supported by numerics, proved per plaquette for fixed v)

The resulting Poincaré threshold (if conjecture holds): β < N²/(4d) = **1/4** for SU(2), d=4.
This is **12× better than SZZ** (β < 1/48) and **6× better than CNS** (β < 1/24).

## Correction to GOAL.md

The GOAL.md formula "H_norm = 4/(3d)" is incorrect:
- For d=4: 4/(3×4) = 1/3 ≠ 1/12
- For d=3: 4/(3×3) = 4/9 ≠ 1/12

The correct formula is: **H_norm_max = ⌈d/2⌉⌊d/2⌋ / (N²d(d-1))**
- d=3, N=2: 1/12 ✓
- d=4, N=2: 1/12 ✓ (numerically verified in E007)
- d=5, N=2: 3/40

## Novelty Assessment

The Fourier analysis of the lattice Yang-Mills Hessian and identification of the staggered
mode as the maximizer do not appear in SZZ, CNS, or any related paper found. The result is
**likely new**, though the action convention (1/N normalization) should be cross-checked
against SZZ arXiv:2204.12737 to ensure matching.

## Leads Worth Pursuing

1. **Close the gap**: Prove ∑_□ |B_□(Q,v)|² ≤ 4d|v|² for general Q. May follow from
   a Fourier argument after gauge-fixing (Coulomb or temporal gauge), since the Fourier
   bound is the key ingredient and gauge-fixing preserves the lattice structure.

2. **Numerical confirmation**: Compute H_norm for non-identity Q configurations to
   verify H_norm ≤ 1/12 empirically and check if the bound is tight only at Q=I.

3. **Convention check**: Verify that SZZ uses S = −(β/N) Re Tr (normalized trace) and
   |·|² = −2 Tr(·²) (Killing form). Both are required for the H_norm = 1/12 match with
   numerics. If SZZ uses a different convention, all formulas need adjustment.

## Unexpected Findings

1. **Formula correction**: The claimed formula H_norm = 4/(3d) (from GOAL.md) is wrong.
   The correct formula is ⌈d/2⌉⌊d/2⌋/(N²d(d-1)), which coincidentally equals 1/12 for
   both d=3 and d=4 (not for the same reason).

2. **d=4 is special**: The Fourier bound is TIGHT only in d=4 among the dimensions tested.
   This is because N_active = d²/4 only in d=4 (where 4 = 16/4). This "coincidence" may
   have deeper geometric significance.

3. **Convention sensitivity**: Getting H_norm = 1/12 (vs. 1/3 or 1/6) requires BOTH
   the 1/N trace normalization AND the −2 Tr inner product. The conventions are coupled
   and must be consistent.

## Computations Identified

- **Numerical check of ∑_□ |B_□(Q,v)|² bound**: For random Q at various β, compute
  ∑_□ |B_□|² / (4d|v|²) and check if it ever exceeds 1. This is a 30-line Python script
  using the existing E007/E006 framework. Would resolve the main gap.
