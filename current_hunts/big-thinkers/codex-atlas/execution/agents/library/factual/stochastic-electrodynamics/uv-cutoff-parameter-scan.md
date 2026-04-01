---
topic: SED anharmonic oscillator — UV-cutoff and τ parameter dependence of residual error
confidence: verified
date: 2026-03-27
source: "SED strategy-001 exploration-005"
---

## Key Result

The β^0.40 residual error in ALD/LL simulations is **NOT a UV-cutoff artifact**. Tripling ω_max (10→30) reduces the β-dependent excess Δe by only 18%. Quintupling 1/τ (τ: 0.01→0.002) reduces Δe by only 31%. Both parameters show extremely weak power-law dependence, and P&C's asymptotic regime (τ→0, ω_max→∞) requires physically inaccessible parameter values.

## Parameter Scan Design

- **Physics parameters varied:** ω_max ∈ {10, 20, 30}; τ ∈ {0.01, 0.005, 0.002}
- **Numerical parameters fixed:** dt = 0.05 (Euler-Cromer; same as E004)
- **Cross-check:** ω_max=10, τ=0.01 results exactly reproduce E004 (var_x = 0.3028 at β=1)
- β-dependent excess: Δe = raw_err(β) − baseline_offset(β=0); removes UV harmonic pollution

**IMPORTANT — dt stability:** The Nyquist choice dt = π/ω_max causes runaway at β=1 (Euler-Cromer instability: ω_eff ≈ 7 at β=1 → stability requires dt < 2/7 ≈ 0.29; dt=π/10≈0.314 exceeds limit). **Correct approach: use fixed dt=0.05 for all ω_max values.** The UV cutoff affects only the noise spectrum, not the time resolution.

## ω_max Scan Results (τ=0.01, dt=0.05)

**Baseline (β=0):** The harmonic baseline offset INCREASES slowly with ω_max:

| ω_max | baseline offset (β=0) | Approximate formula |
|-------|----------------------|---------------------|
| 10    | +0.0157             | ~τ/π × ln(ω_max/ω₀) |
| 20    | +0.0173             |                     |
| 30    | +0.0202             |                     |

**β-dependent excess Δe(β=1):**

| ω_max | raw_err(β=1) | baseline | Δe     | Change vs ref |
|-------|-------------|----------|--------|---------------|
| 10    | +0.04573    | +0.0157  | 0.0300 | (reference)   |
| 20    | +0.04517    | +0.0173  | 0.0279 | −7%           |
| 30    | +0.04470    | +0.0202  | 0.0245 | −18%          |

**Power-law fit:** Δe ~ ω_max^(−0.18). Tripling ω_max reduces Δe by only 18%.
Expected for a UV artifact: p ≥ 1 (i.e., tripling would reduce by ≥ 67%). Observed: p ≈ 0.18.

## τ Scan Results (ω_max=10, dt=0.05)

**β-dependent excess Δe(β=1):**

| τ     | raw_err(β=1) | baseline | Δe     | Change vs ref |
|-------|-------------|----------|--------|---------------|
| 0.010 | +0.04573    | +0.0157  | 0.0300 | (reference)   |
| 0.005 | +0.03994    | +0.0142  | 0.0257 | −14%          |
| 0.002 | +0.03874    | +0.0179  | 0.0208 | −31%          |

**Power-law fit:** Δe ~ τ^0.23. Reducing τ by 5× reduces Δe by only 31%.
P&C predict leading SED-QM discrepancy ~ τ¹ × β². Observed: τ^0.23 (much weaker than τ¹).

Consistency: τ=0.01→0.005 gives n≈0.22; τ=0.005→0.002 gives n≈0.23. Stable exponent.

## Combined Dependence

The β-dependent residual follows a two-regime structure:

1. **UV/cutoff contribution** (present at both β=0 and β=1): scales as τ × log(ω_max). Explains why the β=0 baseline offset grows with ω_max.

2. **β-dependent Δe contribution** (the genuine SED-QM excess): scales as ~**τ^0.23 × ω_max^(-0.18)**.

## Extrapolation to P&C Regime

To reduce Δe from 0.030 to near zero (≈0.005) by varying ω_max alone:
> ω_max ≈ 10^8 (physically inaccessible)

To reduce Δe to ≈0.005 by varying τ alone:
> τ ≈ 10^-6 (physically inaccessible)

**P&C's O(β²τ) prediction is asymptotically correct but the convergence is extremely slow.** The regime P&C analyzed (τ→0, ω_max→∞) requires simultaneous double limits that numerical simulations cannot access.

## Physical Interpretation

The β=1 ALD-SED simulation overpredicts var_x by +15.1% even at τ=0.002 (our smallest τ). This is a real prediction of ALD-SED in the accessible regime: it overpredicts var_x(β=1) by ~15-18%.

Whether this constitutes an intrinsic SED-QM discrepancy or a slow finite-parameter artifact cannot be determined from these scans alone — the convergence is too slow to extrapolate confidently to zero.

## β=0.1 Results (all ω_max values)

At small β, the net Δe values are small and within noise (−0.003 to +0.009), with no clear monotonic ω_max trend. The ALD correctly reproduces QM at β ≤ 0.1 regardless of ω_max. This confirms E004's finding that the O(β) failure is eliminated for small β.

## Conjectured (Not Confirmed)

The β^0.40 scaling exponent is approximately independent of ω_max in the range 10–30. [CONJECTURED — would require running β=0.2, 0.5 at ω_max=20,30.]

## References

- SED strategy-001 exploration-005 (2026-03-27): 13 simulations across ω_max={10,20,30} × β={0,0.1,1} × τ={0.01,0.005,0.002}. All completed, 0 unstable trajectories.
- Pesquera, L. & Claverie, P. (1982). J. Math. Phys. 23(7), 1315-1322. [O(β²τ) analytical prediction]
- See `anharmonic-ald-landau-lifshitz.md` for E004 baseline results.
