# Exploration 003 — REPORT SUMMARY: 3D ZPF Two-Point Correlator

## Goal

Determine what happens to the 1D SED prediction C_xx(d) = cos(ω₀d/c) when the full 3D ZPF (all k-vector directions and polarizations) is used instead of the 1D plane-wave model. Does the 3D orientational average eliminate the correlation (recovering QM), or does it persist?

## What Was Tried

1. Analytic integration of I(q) = ∫_{-1}^{1} (1+u²) e^{iqu} du — full closed-form derivation by parts.
2. Three-way numerical verification: direct quad integration, spherical Bessel function formula, Monte Carlo over N=500,000 k-directions.
3. Limiting cases: near-field (q→0), far-field (q→∞), special values.

## Outcome: Succeeded (Tier 4+)

**The 3D ZPF position-position correlator in the narrow-linewidth limit is:**

```
C_xx(d) = (3/2q³) [(q²-1)sin(q) + q cos(q)]     where q = ω₀d/c

         = j₀(q) - (1/2) j₂(q)                   [spherical Bessel form]

         = (3/2)[sin(q)/q + cos(q)/q² - sin(q)/q³]  [exact 3-term form]
```

This formula is **analytic, exact in closed form**, and verified numerically to machine precision.

**Limiting behaviors:**
- q→0 (near field):  C_xx ≈ 1 - q²/5 + O(q⁴)  [analytic at d=0, no singularity]
- q→∞ (far field):  C_xx ≈ (3/2)sin(q)/q          [oscillating, decaying ~1/d]
- C_xx(q=1) = (3/2)cos(1) ≈ 0.81 exactly

**Answer to the open question:**
The 3D orientational average does **NOT** eliminate the SED correlation. C_xx(d) ≠ 0 for all finite d. SED predicts:
- C_xx(d) ≈ 0.81 at d = c/ω₀ (one reduced wavelength)
- C_xx(d) ~ sin(ω₀d/c)/(ω₀d/c) at large d (oscillating, decays as 1/d)

Compare to **QM's prediction: C_xx = 0** everywhere for uncoupled oscillators.

The 3D discrepancy is weaker than the 1D discrepancy (which had constant-amplitude oscillations), but remains finite at all distances.

## Verification Scorecard

- **1 VERIFIED** (if formalized): analytic formula I(q) = (4/q³)[(q²-1)sin(q)+q cos(q)]
- **4 COMPUTED**: I(0) = 8/3, comparison table at 7 q-values (machine precision), Monte Carlo at 4 separations (~0.05% agreement), near-field Taylor expansion
- **1 CONJECTURED**: physical significance for SED-QM discrepancy

## Key Takeaway

**C_xx(d) ≠ 0 in 3D.** The SED-QM discrepancy survives the orientational average. The 3D result is j₀(q) - j₂(q)/2 (a standard electrodynamics Bessel combination), oscillating and decaying as 1/d at large separations. It is NOT the van der Waals r⁻⁶ term — that requires second-order Coulomb coupling, not ZPF correlations directly.

## Proof Gaps

None — the calculation is elementary (integration by parts) and does not require formal verification. The Monte Carlo closes any remaining doubt.

## Unexpected Findings

- The "3-term far-field form" (3/2)[sin(q)/q + cos(q)/q² - sin(q)/q³] is actually the **exact** formula, not an approximation — verified to machine precision.
- The formula is the xx-component of the transverse electromagnetic propagator, confirming this is the physically correct 3D ZPF correlator.
- Special value at q=1: since q²-1=0, C_xx(1) = (3/2)cos(1) exactly.

## Computations for Next Exploration

- Extend to the full susceptibility integral (not narrow-linewidth limit) — does the result change qualitatively?
- Check against Ibison-Haisch (1996) Phys. Rev. A 54, 2737 for the explicit published formula.
- Compute the separations where C_xx(d) is experimentally distinguishable from 0 given realistic oscillator parameters (γ/ω₀ ≈ 10⁻⁸ for atomic transitions).
