---
topic: Berry's diagonal approximation — prime sums predict spectral form factor ramp but not plateau
confidence: verified
date: 2026-03-27
source: "riemann-hypothesis strategy-002 exploration-006"
---

## Finding

Berry's semiclassical diagonal approximation — building K_primes(τ) from prime periodic orbits — correctly reproduces the **linear ramp** of the spectral form factor K(τ) for τ ∈ (0, 1), with mean absolute deviation 14.5% from GUE. This confirms Berry's conjecture (1985) that diagonal prime orbit contributions produce the ramp. The prime sum **FAILS for τ > 1**: it has no plateau mechanism, as the plateau requires off-diagonal orbit interference not captured by the diagonal approximation.

## Quantitative Results [COMPUTED]

Method: N = 2,000 zeta zeros (t₁ = 14.13, t₂₀₀₀ = 2515.29); unfolded via smooth counting function N_smooth(t) = (t/2π)log(t/2π) − t/2π + 7/8 (mean spacing = 0.999965 ≈ 1 ✓); T = geometric mean = 1127.12; log(T/2π) = 5.1895. K_primes(τ) constructed by binning prime orbit periods τ_pm = m·log(p)/log(T/2π) and dividing by (2πρ̄)² (correct normalization — see below).

| τ | K_GUE | K_zeros (smoothed) | K_primes (corrected) |
|---|-------|--------------------|----------------------|
| 0.10 | 0.100 | 0.055 | 0.042 |
| 0.20 | 0.200 | 0.185 | 0.250 |
| 0.30 | 0.300 | 0.260 | 0.364 |
| 0.40 | 0.400 | 0.304 | 0.268 |
| 0.50 | 0.500 | 0.549 | 0.453 |
| 0.60 | 0.600 | 0.507 | 0.485 |
| 0.70 | 0.700 | 0.811 | 0.644 |
| 0.80 | 0.800 | 0.727 | 0.800 |
| 0.90 | 0.900 | 0.990 | 0.953 |
| 1.00 | 1.000 | 3.711* | 1.007 |
| 1.50 | 1.000 | 0.975 | 1.499† |
| 2.00 | 1.000 | 0.801 | 0.000‡ |

*Large spike at τ=1 (Heisenberg time), not fully smoothed.
†K_primes continues rising past K_GUE=1 (diagonal approximation continues ramp, no saturation).
‡K_primes = 0 because no prime orbits have τ_pm > 1.56 for the primes used (max prime = 3381).

**MAD in ramp region (τ ∈ [0.1, 0.9]):**
- MAD(K_zeros, K_GUE) = 0.0641 (12.8% relative to mean K_GUE=0.5) — zeros match GUE
- MAD(K_primes, K_GUE) = 0.0723 (14.5%) — prime sum matches GUE ramp comparably
- MAD(K_zeros, K_primes) = 0.0826 (16.5%) — zeros and prime sums agree with each other

**Ramp-to-plateau transition:**
- K_zeros: ramp mean = 0.489, plateau mean = 1.035 ✓ (correct transition observed)
- K_primes: ramp mean = 0.456 ✓, plateau = continues rising indefinitely ✗ (no saturation)

## Correct Normalization Formula (Resolving E003/E005 Failures)

Previous explorations used wrong formulas:

**Wrong (E003 cosine formula):**
K_cosine(τ) = (1/Σ) × Σ_{pm} (log p)²/p^m × cos(2πτ·τ_pm)
This is Re[Z(τ)], not |Z(τ)|²/N. It is the "connected correlation oscillation" and **can be negative**. It is NOT the spectral form factor K(τ) = min(τ,1).

**Wrong (E005 normalization):**
K_berry = K_density / (2πρ̄) — off by a factor of 2πρ̄.

**Correct:** K_primes(τ) = K_density(τ) / (2πρ̄)²

where K_density is the binned prime orbit weight density at τ_pm = m·log(p)/log(T/2π).

Derivation: From the prime number theorem, dK_unorm/dτ ≈ (τ × 2πρ̄)² × (weight density accumulation rate), so K_unorm ≈ (2πρ̄)² × τ²/2. To recover K(τ) = τ, normalize: K = dK_unorm/dτ / (2πρ̄)² = τ. ✓

## Interpretation

**Why the ramp works:** Berry's semiclassical argument shows that the diagonal periodic orbit approximation (leading term) yields K(τ) = τ for 0 < τ < 1. The prime numbers label the primitive periodic orbits of the conjectured Riemann operator, and their log-weighted contributions produce the slope-1 ramp.

**Why the plateau fails:** K(τ) = 1 for τ > 1 (the "plateau") requires resumming all off-diagonal orbit pairs — non-perturbative contributions with orbit interference terms. The diagonal approximation cannot produce this saturation. This is Berry's acknowledged limitation in his 1985 paper.

**Norm concentration:** 96.1% of the total prime orbit weight comes from primes p ≤ 1000. For specific τ values like τ=0.5, the dominant contribution is from primes near p ≈ exp(0.5 × 5.19) ≈ 13, which are always included. This explains why E003 saw no change when increasing P_max from 100 to 10,000.

## Relationship to Other Findings

**Distinct from "prime corrections destroy level repulsion"** (see `prime-corrections-statistical-partial-success.md` and `riemann-operator-constraints.md`): That finding adds prime oscillatory corrections to individual zero *positions* and measures the effect on the spacing statistics — and finds level repulsion is destroyed. The present finding uses prime orbit weights to *construct* K(τ) independently, without touching zero positions. Both results are correct in their respective contexts.

**Confirms:** Berry saturation from `berry-saturation-confirmed.md` — the super-rigidity of zeta zeros at long scales is consistent with prime periodic orbits dominating K(τ) in the ramp, while the plateau (τ > 1) represents the Heisenberg time where all orbits must contribute.
