---
topic: Beltrami-De Giorgi mechanism does NOT generalize to near-Beltrami flows — definitive negative result
confidence: verified
date: 2026-03-30
source: "vasseur-pressure exploration-010"
---

## Finding

The B_k = O(2^{-k}) decay and "pressure is >95% Bernoulli" properties demonstrated in E007 for exact Beltrami flows are **specific to exact Beltrami** and do not survive even small perturbations. This is the definitive negative result for the Beltrami-De Giorgi mechanism's generalizability.

## Perturbed-ABC Setup

Generated perturbed-ABC flows u = (1-eps) * u_ABC + eps * u_random where u_random is divergence-free with matched energy and Kolmogorov spectrum (k^{-5/3}). DNS at Re=500, N=64, evolved to T=2.0. All L^inf-normalized.

## Key Results

### B_k Decay Destroyed for Any eps > 0

| eps | B(k=2) | B(k=8) | B(k=8)/B(k=2) | Trend |
|-----|--------|--------|----------------|-------|
| 0.00 | 0.137 | 0.0009 | 0.006 | Exponential decay |
| 0.01 | 0.149 | 0.063 | 0.42 | Plateaus at ~0.063 |
| 0.05 | 0.346 | 0.324 | 0.94 | Nearly flat |
| 0.10 | 0.675 | 0.675 | 1.00 | Flat |
| 0.20 | 1.447 | 1.471 | 1.02 | Flat |
| 0.50 | 4.834 | 4.838 | 1.00 | Flat |

Even at eps=0.01 (99% ABC + 1% random), B_k saturates to B_full rather than continuing to decay. [COMPUTED]

### Bernoulli Dominance Lost for eps >= 0.05

| eps | R_floor (remainder fraction at high k) |
|-----|----------------------------------------|
| 0.00 | ~0 |
| 0.01 | 0.014 (1.4% non-Bernoulli) |
| 0.05 | 0.073 (7.3% non-Bernoulli) |
| 0.10 | 0.154 (15.4%) |
| 0.20 | 0.346 (34.6%) |
| 0.50 | 1.285 (R > 1 — decomposition meaningless) |

The ">95% Bernoulli" claim holds only for eps < ~0.01. [COMPUTED]

### beta_eff Degrades Continuously

| eps | beta_eff | std_err | R^2 |
|-----|----------|---------|------|
| 0.00 | 1.009 | 0.012 | 0.999 |
| 0.01 | 1.067 | 0.066 | 0.983 |
| 0.05 | 0.888 | 0.084 | 0.975 |
| 0.10 | 0.790 | 0.087 | 0.972 |
| 0.20 | 0.585 | 0.119 | 0.935 |
| 0.50 | 0.278 | 0.131 | 0.901 |

beta > 1 maintained only for eps < ~0.02. No sharp threshold — degradation is smooth. [COMPUTED]

### Viscosity Improves but Cannot Restore

At Re=500, viscous dissipation reduces B_full by ~50% over T=2.0 (non-Beltrami modes decay faster). But this improvement is far from sufficient to restore B_k decay with k. [COMPUTED]

## Physical Explanation

For exact Beltrami, curl(u) = lambda*u everywhere, so u_below inherits near-Beltrami structure except at the clipping boundary (which vanishes as k -> infinity). For perturbed flows, the non-Beltrami component exists at ALL velocity magnitudes, not just near the peak. Truncation cannot remove it, so B_k -> B_full as k -> infinity.

## Leray Projection Results

Leray projection of u_below (restoring div=0 spectrally) preserves the qualitative picture:
- B_k still decays as ~2^{-k} for exact Beltrami after projection
- Largest correction at k=1 (16% relative change), negligible at k>=5 (<0.4%)
- R_frac at k=1 drops by factor ~2 after projection (half the "remainder" was a div!=0 artifact)
- div(u_below) driven to machine precision (~1e-14) after projection

**The Leray correction is minor** and does not change any qualitative conclusions. The O(2^{-k}) decay for exact Beltrami is preserved; the failure for near-Beltrami is unchanged. [COMPUTED]

## Combined Verdict

| eps | B_floor | R_floor | beta_eff | Mechanism works? |
|-----|---------|---------|----------|-----------------|
| 0.00 | 0 | 0 | 1.01 | Yes (trivially: exact eigenstate) |
| 0.01 | 0.063 | 0.014 | 1.07 | Marginal (beta > 1 but B doesn't decay) |
| 0.05 | 0.324 | 0.073 | 0.89 | No (beta < 1, B flat) |
| >=0.10 | >=0.675 | >=0.154 | <=0.79 | No |

**The mechanism requires very precise Beltrami alignment.** A flow that is 95% ABC (eps=0.05) already has beta_eff = 0.89 < 1. Generic turbulent flows at high Re are far from Beltrami, so the mechanism applies only to a measure-zero set of initial conditions. [COMPUTED]

## Implications

1. **Confirms E009's assessment:** Claim 5 (truncation preserves Beltrami) is the weakest claim in Strategy-001, as predicted.
2. **Resolves open questions** from E007's `beltrami-deficit-truncation-survival.md` and `pressure-bernoulli-dominance-truncated.md`: the answer to "does B_k decay for perturbed ABC?" is definitively NO.
3. **Partially resolves** the div(u_below) != 0 concern from E009: Leray projection fixes it but doesn't change the picture.
4. **The Beltrami-De Giorgi connection** remains analytically novel (Lamb vector -> CZ loss story) but its practical significance for regularity theory is now known to be limited to exact eigenstates of curl.
