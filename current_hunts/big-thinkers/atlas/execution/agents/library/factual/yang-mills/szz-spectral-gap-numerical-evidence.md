---
topic: MCMC spectral gap proxy — numerical evidence SZZ bound conservative by ~100×
confidence: verified
date: 2026-03-27
source: "yang-mills strategy-002 exploration-002; SU(2) 4^4 lattice computation, Kennedy-Pendleton heat bath, checkerboard decomposition"
---

## Overview

Direct MCMC measurement of the spectral gap proxy γ ≈ 1/(2τ_int) for SU(2) lattice Yang-Mills on a 4^4 lattice at 8 β values spanning the SZZ strong-coupling regime (β < 1/48) through the physical lattice region (β ~ 2.0–3.0). All values show γ > 0: the spectral gap does **not** vanish in the range β ∈ [0.02, 3.0].

---

## Setup

- **Lattice:** 4^4 (L=4, hypercubic, 256 sites, 1024 links)
- **Algorithm:** Kennedy-Pendleton heat bath for SU(2) with checkerboard decomposition (proper detailed balance)
- **Thermalization:** 500 sweeps per β value
- **Measurement:** 2000 sweeps per β value
- **Observable:** Average plaquette P = (1/N_plaq) Σ_□ (1/2) Re Tr(U_□)
- **Spectral gap proxy:** γ ≈ 1/(2τ_int), where τ_int = integrated autocorrelation time of P

---

## Results [COMPUTED]

| β | ⟨P⟩ | τ_int (sweeps) | γ ≈ 1/(2τ_int) | C(1) | Notes |
|------|---------|----------------|----------------|-------|-------|
| 0.02 | 0.00510 | 0.56 | 0.897 | 0.018 | SZZ guaranteed (β < 1/48) |
| 0.05 | 0.01213 | 0.55 | 0.904 | 0.005 | Beyond SZZ bound |
| 0.10 | 0.02484 | 0.50 | 1.000 | −0.011 | τ_int minimum (C(1) < 0) |
| 0.20 | 0.04940 | 0.50 | 1.000 | −0.044 | τ_int minimum (C(1) < 0) |
| 0.50 | 0.12431 | 0.58 | 0.864 | 0.026 | |
| 1.00 | 0.24336 | 0.62 | 0.813 | 0.064 | |
| 2.00 | 0.50224 | 2.11 | 0.237 | 0.489 | Near deconfinement; τ_int peak |
| 3.00 | 0.72406 | 0.79 | 0.629 | 0.204 | Above deconfinement (β_c ≈ 2.3) |

Plaquette values cross-checked against known analytic and literature results [CHECKED]:
- β = 0.02: ⟨P⟩ = 0.00510, expected β/4 = 0.005 (strong coupling expansion) ✓
- β = 0.10: ⟨P⟩ = 0.02484, expected β/4 = 0.025 ✓
- β = 2.0: ⟨P⟩ = 0.50224, expected ~0.50 (literature) ✓
- β = 3.0: ⟨P⟩ = 0.72406, expected ~0.72 (literature) ✓

---

## Key Numbers [COMPUTED]

| Quantity | Value |
|----------|-------|
| γ at β = 0.02 (SZZ regime) | 0.897 |
| γ at β = 2.0 (physical region) | 0.237 |
| γ at β = 3.0 (above deconfinement) | 0.629 |
| Maximum τ_int | 2.11 (at β = 2.0) |
| τ_int ratio β=2.0 / β=0.02 | 3.77 |
| Factor beyond SZZ bound where gap persists | ≥ 100× |
| β range with no evidence of gap closure | [0.02, 3.0] |

---

## Analysis

### Spectral Gap Is Non-Monotone and Never Zero

The pattern is non-monotone:
- γ starts near 0.9 in the SZZ regime
- γ increases to 1.0 at β = 0.1–0.2 (anti-correlated chain; τ_int at minimum)
- γ decreases from β = 0.5 to β = 2.0
- **Minimum at β = 2.0** (near deconfinement β_c ≈ 2.3)
- γ recovers to 0.63 above deconfinement

### SZZ Bound Is Not a Sharp Threshold

No signature at β = 1/48 ≈ 0.021. Transition from β = 0.02 to β = 0.05 shows negligible change: τ_int 0.56 → 0.55, γ 0.897 → 0.904. The SZZ bound is a conservative sufficient condition, not a physical threshold.

### τ_int Peak = Critical Slowing Down, Not Gap Closure

The elevated τ_int = 2.11 at β = 2.0 is critical slowing down near the SU(2) deconfinement transition (β_c ≈ 2.3 on a 4^4 lattice). This is a well-known finite-volume lattice phenomenon, NOT evidence of a vanishing spectral gap. On this small lattice, the effect is modest (τ_int = 2.11, not >> 100).

### Conservative Factor of ~100×

The spectral gap shrinks by only a factor of ~4 from the SZZ regime to the physical region (τ_int ratio 3.77). This suggests the SZZ analytic bound β < 1/48 is conservative by roughly 100× — the gap persists empirically to β ≈ 2.0–3.0.

---

## Caveats

1. **Small lattice (4^4):** On larger lattices, τ_int near the phase transition would be larger (more critical slowing down). The thermodynamic limit behavior is not captured.

2. **τ_int ≠ physical mass gap:** The MCMC autocorrelation time measures the Markov chain spectral gap (computational mixing rate), not directly the physical mass gap (exponential decay of connected correlators). Both involve the spectral structure of the transfer matrix, but they are distinct quantities.

3. **τ_int = 0.5 artifact:** At β = 0.1 and 0.2, τ_int = 0.50 is the minimum of the formula (due to C(1) < 0). The γ = 1.0 values are artifacts of the cutoff; the chain actually mixes faster than one sweep.

4. **Computational note:** KP rejection sampling is slow at small β (β=0.02 took 488 seconds vs. 24 seconds at β=3.0).

---

## Implication for Extending SZZ

The data numerically supports the conjecture that the Yang-Mills Gibbs measure satisfies a Poincaré inequality far beyond the SZZ strong-coupling bound. The hardest region analytically (β ≈ 2.0, near deconfinement) shows γ = 0.237 — positive, but with the smallest gap in the scan. Extending the SZZ analytic result to this region remains the key challenge.
