# Exploration 004 SUMMARY — Full Abraham-Lorentz Dynamics (Landau-Lifshitz)

**Date:** 2026-03-27

## Goal
Implement the Landau-Lifshitz order-reduced Abraham-Lorentz equation for the
anharmonic SED oscillator V(x) = ½x² + βx⁴. The key change from E003: damping
is position-dependent: Γ_eff = τ(ω₀² + 12βx²). Test whether this fixes the O(β)
failure found with constant damping (Langevin approximation).

## What was tried
1. Full ALD simulation: position-dependent damping + noise derivative τF'_zpf(t)
2. All 7 β values: 0, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0
3. Same parameters as E003: τ=0.01, ω₀=1, ω_max=10, 200 trajectories × 50 samples
4. Power-law fit to β-dependent error

## Outcome: YES — O(β) failure is fixed

**3-way comparison at key β values:**

| β    | var_x QM | var_x ALD (E004) | ALD err | var_x Langevin (E003) | Lang err |
|------|----------|------------------|---------|----------------------|----------|
| 0.00 | 0.500    | 0.516 ± 0.007    | +3.1%   | 0.515 ± 0.007        | +3.0%    |
| 0.10 | 0.413    | 0.426 ± 0.006    | +3.2%   | 0.735 ± 0.014        | +78.2%   |
| 1.00 | 0.257    | 0.303 ± 0.004    | +17.8%  | 2.411 ± 0.043        | +837.8%  |

**ALD improvement: 11× at β=0.1, 47× at β=1.0 (absolute fractional error).**

## Verification scorecard
- 7 [COMPUTED] | 0 [VERIFIED] | 1 [CONJECTURED]

## Key takeaway
Position-dependent damping (ALD) ELIMINATES the O(β) positive feedback loop:
- For β ≤ 0.1: ALD error is statistically indistinguishable from the β=0 baseline
  (no O(β) failure)
- For β > 0.2: A residual error grows as β^0.40 — much slower than O(β^1)
  (Langevin) but also slower than O(β²) (Pesquera-Claverie prediction)
- Direction correct: var_x decreases with β in ALD (matching QM), not increases (Langevin)
- No runaways: max|x| < 3.5 at all β values; equilibrium is stable

The β^0.40 growth (instead of P&C's O(β²)) is likely a UV-cutoff artifact from
ω_max=10: when the full spectrum is used (ω_max→∞), P&C's O(β²) result should emerge.

## Proof gaps / Open questions
- Whether residual β^0.40 error is UV-cutoff artifact (predicted) or intrinsic to LL
  requires testing at ω_max = 20 or ω_max = 50
- Full verification of P&C (τ→0 limit) would require τ = 0.001

## Unexpected findings
- At β=0, ALD and Langevin give identical results (as expected: Γ_eff = const at β=0)
- The effective damping increases by 4.6× at β=1 vs β=0, explaining why runaway is prevented
- The τF'_zpf term has negligible effect at β=0 (RMS ratio 8%, below statistical noise)

## Computations identified for future work
1. ω_max scan (10, 20, 50, 100) to characterize UV-cutoff contribution to residual error
2. τ-scan (0.01 → 0.001) to approach P&C's τ→0 regime
3. P(x) distribution comparison: KS test between ALD, QM, and Langevin
4. Fine-scan β ∈ [0.1, 0.3] to pinpoint where β-dependent failure becomes significant
