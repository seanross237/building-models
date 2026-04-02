# Exploration 002 Summary: Li's Criterion — Computational Probing

## Goal
Compute Li's criterion coefficients λ_n for n=1 to 500 using 2000 zeta zero pairs at 50-digit precision. Verify positivity, analyze asymptotic residuals, and search for patterns including GUE comparison.

## What Was Tried
1. Pre-computed 2000 zeta zeros (~569s), then computed all 500 λ_n (~80s)
2. Analyzed Bombieri-Lagarias and Coffey (2004) asymptotic residuals
3. FFT pattern search, prime correlation test
4. GUE random matrix comparison (5 realizations of GUE(2000))
5. Spectral rigidity (Δ₃) comparison between GUE and zeta zeros
6. Truncation convergence analysis at multiple zero counts

## Outcome: SUCCEEDED

**All 500 Li coefficients are strictly positive**, consistent with RH. λ_1 = 0.02265 (within 4.4×10⁻⁴ of exact value, explained by truncation). λ_500 = 881.43.

## Verification Scorecard
- **Verified:** 1 (|1-1/ρ| = 1 on critical line)
- **Computed:** 14 (all λ_n values, residuals, FFT, GUE comparison, Δ₃)
- **Conjectured:** 4 (phase cancellation interpretation, super-rigidity connection)

## Key Takeaway

The most important structural insight: **|1-1/ρ| = 1 exactly for zeros on the critical line**, meaning the Li series converges by phase cancellation, not amplitude decay. Each zero contributes 2(1 - cos(n·θ_k)) where θ_k ≈ 1/t_k. Li's criterion is thus a statement about the Fourier properties of the zero phase distribution. An off-critical-line zero would break this unit-modulus property, potentially driving λ_n negative.

## Leads Worth Pursuing
1. **Tail correction formula:** The truncation converges geometrically with ratio 0.646. Deriving an analytical correction from zero density would allow extraction of the true O(log(n)/n) Coffey correction term.
2. **Phase distribution analysis:** The connection between Li coefficients and zero phases (θ_k = arg((ρ_k-1)/ρ_k)) could be formalized — particularly whether the phase equidistribution theorem implies λ_n > 0.
3. **GUE deviation at large n:** λ_n^zeta/λ_n^GUE < 1 for n > 300, falling to 0.95 at n=500. This divergence encodes the super-rigidity difference. Computing to n=5000 with more zeros would quantify this.

## Unexpected Findings
- The truncation convergence ratio r ≈ 0.646 is remarkably uniform across ALL n values (1 to 500), suggesting the truncation error has a universal structure independent of n.
- GUE-zeta Li coefficient correlation is 97.1%, but the zeta residual has 5× higher standard deviation than GUE, consistent with arithmetic structure beyond random matrix statistics.

## Proof Gaps Identified
- The claim "|1-1/ρ| = 1 ⟹ convergence by phase cancellation ⟹ Li's criterion is about Fourier properties of zero phases" is a heuristic chain. Each link could be formalized but none is proven.
- No attempt was made to formalize anything in Lean — the exploration was purely computational.

## Computations Identified for Follow-Up
1. Compute λ_n for n up to 5000 using 10,000+ zeros (would require ~1 hour for zeros)
2. Compute λ_n using the ξ-function derivative formula (independent verification, avoids truncation issue)
3. Formalize the proof that |1-1/ρ| = 1 for ρ on the critical line in Lean
4. Compute the exact phase angles θ_k and analyze their equidistribution modulo 2π/n for various n
