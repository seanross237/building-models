# REPORT-SUMMARY — Exploration 001: CKN (1982) Proof Architecture

## Goal
Extract the 5 structural features of Caffarelli-Kohn-Nirenberg (1982) that determine the dimension bound on the Navier-Stokes singular set. Intended as the reference extraction for comparison with Lin (1998) and Vasseur (2007) in the same 5-item template.

## What Was Done
Deep literature extraction from the CKN (1982) paper and corroborating secondary sources (Robinson-Rodrigo-Sadowski 2016, Ladyzhenskaya-Seregin 1999, Kukavica 2009, Lin 1998 for contrast). All five items extracted with precise mathematical content.

## Outcome: Succeeded

All five items extracted with precise mathematical statements.

---

## Key Findings (5 Structural Features)

### 1. Epsilon-Regularity Criterion
**Precise form:** ∃ ε₀ > 0 (absolute constant) such that if
> A(r) + E(r) + C(r) + D(r) < ε₀
then z₀ = (x₀, t₀) is a regular point.

Where (all defined over parabolic cylinder Q_r(z₀) = B_r(x₀) × (t₀ − r², t₀)):
- A(r) = (1/r) sup_t ∫_{B_r} |u|²
- E(r) = (1/r) ∫∫_{Q_r} |∇u|²
- C(r) = (1/r²) ∫∫_{Q_r} |u|³
- D(r) = (1/r²) ∫∫_{Q_r} |p|^{3/2}

All four quantities are **scale-invariant** (dimensionless under NS parabolic rescaling). The exponents 3 for u and 3/2 for p are uniquely forced by NS scaling. ε₀ is existential (never computed).

### 2. Covering Argument
Vitali covering in the **parabolic metric** d_P((x,t),(y,s)) = max(|x−y|, |t−s|^{1/2}), which gives ambient parabolic dimension 5 (not 4). The key counting inequality:

> For each z_i ∈ Σ: E(r_i, z_i) ≥ ε₀ → ∫∫_{Q_{r_i}} |∇u|² ≥ ε₀ · r_i

Summing over disjoint cylinders: Σ_i r_i ≤ (1/ε₀) ∫∫ |∇u|² < ∞.

This gives **P¹(Σ) = 0** — parabolic 1-Hausdorff measure zero, hence parabolic Hausdorff dimension ≤ 1. In Euclidean space-time terms this is ≤ 5/3.

### 3. Localization Mechanism
Explicit smooth cutoff functions φ supported in Q_r with |∇φ| ~ 1/r, |∆φ| ~ 1/r², |∂_t φ| ~ 1/r². Applied to the local energy inequality (LEI), giving four error terms from the cutoff. Pressure is handled via explicit harmonic decomposition p = p₁ + p₂, where p₁ is controlled by Calderón-Zygmund and p₂ by the harmonic mean-value property. Net localized estimate:

> 2 ∫∫_{Q_{r/2}} |∇u|² ≤ C · r · [A(r) + C(r) + D(r)]

### 4. Critical Scaling Exponents
The key exponent is **α = 1** in:
> ∫∫_{Q_r(z₀)} |∇u|² ≥ ε₀ · r   (for z₀ ∈ Σ)

This follows directly from E(r) being scale-invariant and ≥ ε₀ on Σ. The parabolic Sobolev exponent is **10/3 = 2N/(N−2) with N = 5** (parabolic dimension). The dimension bound dim(Σ) ≤ 1 is forced by α = 1 in the covering sum. To get dim < 1 would require E(r, z₀) → ∞ as r → 0 for singular points — this is a deep open question.

### 5. Free-Parameter vs. Fixed Estimates
Four identified Young/absorption steps:
- **Y1** (pressure-velocity coupling): Young with exponents 3/2 and 3, no free ε — lossy but fixed.
- **Y2** (Ladyzhenskaya absorption): Young with exponents 4 and 4/3, **free parameter δ** — primary lossy step. This is where the explicit ε₀ constant is lost.
- **Y3** (parabolic Sobolev interpolation): fixed exponents 2/5 and 3/5, no free ε.
- **Y4** (pressure-regularity iteration): Young with exponents 2 and 2, free δ absorbed into LHS.

Y2 is the dominant lossy step. The proof is quantitative in structure (explicit powers of r everywhere) but non-quantitative in constants (ε₀ is never computed).

---

## Key Takeaway

**The dimension-1 bound is not a proof artifact — it is forced by scale-invariance.** The singular set Σ is defined as the set where the scale-invariant quantity E(r) stays ≥ ε₀ at all scales. Since E(r) = (1/r)∫∫|∇u|², the raw dissipation integral on Q_r scales as r¹ · ε₀. The Vitali covering sum Σ_i r_i is then bounded by the global L²(H¹) energy. There is no room to do better within this framework without knowing that E(r, z₀) → ∞ as r → 0 for singular points — an enhancement unavailable from the local energy inequality alone.

---

## Leads Worth Pursuing
- Whether Type I singular points (|u| ≤ C/√(T*−t)) satisfy E(r) → ∞ as r → 0 — if so, the dimension bound could be improved for Type I blow-ups.
- Lin's simplification replaces all the explicit cutoff machinery with compactness; need to check whether the 4-quantity criterion collapses to 2 quantities (C+D only) or whether A and E survive.
- Vasseur's De Giorgi approach avoids all cutoff functions — whether the scale-invariant bottleneck in the covering step is still the same.

## Unexpected Findings
The Morrey embedding step in the bootstrap requires the parabolic Sobolev exponent 10/3 > N/2 = 5/2. The dimensionless ratio 10/3 ÷ 5 = 2/3 suggests a pattern: the bootstrap works because 10/3 is strictly above the critical exponent N/2 for the parabolic Morrey embedding. Whether a sharper embedding (with smaller exponent) could be used is worth checking.

## Computations Identified
None required for this exploration — this was pure extraction. However, Step 2 of the chain (numerically measuring E(r) in DNS data near potential singularities) would be high-value. Input: DNS velocity fields near near-singular events; computation: profile E(r, z₀) as r → 0 to see if it stays bounded (CKN-consistent) or diverges (suggesting enhanced concentration). This is a 50–100 line scipy/numpy script once DNS data is available.
