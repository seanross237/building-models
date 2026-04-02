# Exploration 005 SUMMARY — UV-Cutoff Scan: β^0.40 Error is Real

**Date:** 2026-03-27

## Goal
Determine whether the β^0.40 residual error in ALD-SED (ω_max=10, τ=0.01) is a
UV-cutoff artifact or a genuine SED-QM discrepancy. Three scans:
- ω_max ∈ {10, 20, 30} at β=1.0 and β=0.1 (τ=0.01 fixed)
- τ ∈ {0.01, 0.005, 0.002} at β=1.0 (ω_max=10 fixed)

## What was tried
1. All 13 (β, ω_max, τ) combinations run sequentially; all stable (0 runaways)
2. Net β-dependent error Δe = raw_err(β) − baseline_offset(β=0) computed for each case
3. Power-law fitting for ω_max and τ dependence of Δe
4. Initial runs with dt=π/ω_max (Nyquist limit) discovered numerical instability for β=1.0;
   corrected to fixed dt=0.05 matching E004

## Outcome: β^0.40 error is REAL

**ω_max scan** (β=1.0, τ=0.01):

| ω_max | Δe     | Change vs ω_max=10 |
|-------|--------|-------------------|
| 10    | 0.0300 | reference         |
| 20    | 0.0279 | −7%               |
| 30    | 0.0245 | −18%              |

Tripling the cutoff reduces the net error by only 18%. Power-law fit: **Δe ~ ω_max^(−0.18)**.

**τ scan** (β=1.0, ω_max=10):

| τ     | Δe     | Change vs τ=0.01 |
|-------|--------|-----------------|
| 0.010 | 0.0300 | reference        |
| 0.005 | 0.0257 | −14%             |
| 0.002 | 0.0208 | −31%             |

Quintupling 1/τ reduces the net error by only 31%. Power-law fit: **Δe ~ τ^0.23**.

## Verification scorecard
- 13 [COMPUTED] | 1 [CHECKED] (E004 reproduction) | 1 [CONJECTURED] (β-exponent ω_max independence)

## Key takeaway
**The β^0.40 residual error is a genuine SED-QM discrepancy in the physically accessible
regime (τ ~ 0.002–0.01, ω_max ~ 10–30), not a simple UV-cutoff artifact.** The ALD-SED
simulation overpredicts var_x at β=1.0 by 15–18% at these parameter values, and this
error converges to zero only as τ^0.23 × ω_max^(-0.18) — far too slowly to disappear
at numerically accessible parameters. Pesquera & Claverie's O(β²) result is asymptotically
correct in the strict double limit, but that limit requires τ < 10^-6 and ω_max > 10^7.

## Proof gaps
- The β-scaling exponent 0.40 was measured only at ω_max=10 (E004). It likely persists
  at ω_max=20,30 (conjectured) but not verified.
- No analytic explanation for why τ^0.23 instead of τ^1. This is the main gap.

## Unexpected findings
- The harmonic (β=0) baseline offset INCREASES with ω_max (0.0157 → 0.0202 as ω_max 10→30),
  reflecting a slowly growing UV tail from the ZPF noise. This is physically expected
  (contribution scales as τ × ln(ω_max)) but not previously noted.
- Euler-Cromer is unstable at the Nyquist dt=π/ω_max for β=1.0 because the anharmonic
  term raises the instantaneous frequency above the stability threshold.

## Computations identified
1. Run β ∈ {0.2, 0.5, 1.0} at ω_max = {20, 30} to check if β^0.40 exponent is preserved
2. Run τ = 0.001, 0.0005 to extend τ extrapolation (needs longer T_total for equilibration)
3. Run ω_max = 50, 100 (still with dt=0.05) to test ω_max^(-0.18) scaling
4. Attempt analytic calculation of the leading τ correction to ⟨x²⟩ beyond P&C to
   understand the τ^0.23 behavior
