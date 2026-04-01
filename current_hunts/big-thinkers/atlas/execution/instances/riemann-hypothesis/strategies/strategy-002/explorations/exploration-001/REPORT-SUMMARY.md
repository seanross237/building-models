# Exploration 001 — REPORT SUMMARY

## Goal
Test four families of complex Hermitian arithmetic matrices (Von Mangoldt amplitudes × complex phases) for GUE-like spectral statistics. Score each against the 10-point constraint catalog. Primary success: β > 1.5 for any construction.

## What Was Tried
7 constructions, all N=500:
- **GUE Control** — true random GUE (theoretical baseline)
- **C1: Random Phases** — Λ(|j-k|+1) × exp(iφ_{jk}), φ random
- **C2a/C2b: Dirichlet χ₄, χ₈ phases** — character evaluated at signed difference j-k
- **C3a/C3b: Gauss sum phases** — exp(2πi jk/p) for p=97, 997
- **C4: Zeta-value phases** — Im(ζ(½+i|j-k|)) as phase argument

Scripts: `code/analysis_v2.py` (screening), `code/full_analysis_c1.py` (full analysis on best construction).

## Outcome: SECONDARY SUCCESS (borderline PRIMARY)

**C1 (Random Phase Hankel) achieves β_Wigner = 1.655–1.675 > 1.5.** [COMPUTED]
This satisfies the primary success criterion (β > 1.5). The spacing distribution is best fit by GUE (KS_GUE = 0.027, KS_GOE = 0.057), ruling out GOE and Poisson.

**C3b (Gauss p=997) achieves β_Wigner = 1.092, best fit: GOE (χ²_GOE = 0.64).** [COMPUTED]
The best purely arithmetic result. Gauss sum phases (exp(2πi jk/997)) push the real-symmetric Hankel matrix from β=0.44 (baseline) to β=1.09, reaching the GOE boundary.

Two constructions **failed at the design level:**
- **C2 (Dirichlet χ₄, χ₈):** Both characters are *odd* (χ(-1) = -1), making the signed-difference matrix antisymmetric. After Hermitianization, all entries cancel → zero matrix → all eigenvalues = 0. Construction must be redesigned with complex-valued characters (χ mod 5 or similar).
- **C4 (Zeta phases):** Phase Im(ζ(½+i|j-k|)) depends only on |j-k|, making H a Hermitian Toeplitz matrix. Toeplitz matrices have Poisson statistics regardless of phase function. β ≈ 0, KS_Poisson = 0.082.

## Verification Scorecard
- **[COMPUTED]:** 12 results (β values, KS distances, χ² comparisons, number variance)
- **[CONJECTURED]:** 1 (structural principle about joint vs. marginal phase dependence)
- **[VERIFIED]:** 0 (no Lean proofs attempted — not appropriate for this computational exploration)

## Key Takeaway

**Complex phases work.** Moving from real symmetric (β ≤ 1 cap) to complex Hermitian with non-factorizable phases (C1: β=1.67, C3b: β=1.09) confirms the theoretical prediction. However:

1. **C1 is not a useful arithmetic operator.** Random phases with Mangoldt amplitudes is essentially a weighted GUE — it gets GUE statistics by construction (universality), not because of arithmetic content. The Mangoldt weights are incidental.

2. **C3b is the meaningful arithmetic result.** Gauss sum phases exp(2πi jk/p) are genuinely arithmetic and reach GOE (β=1.09). The gap from GOE (β=1) to GUE (β=2) remains open for arithmetic constructions.

3. **Structural principle [CONJECTURED]:** Phase φ(j,k) = f(|j-k|) always gives Toeplitz structure → Poisson or GOE at best. Phase φ(j,k) = g(j) − g(k) is unitarily equivalent to real symmetric → β ≤ 1. Only phases where φ(j,k) is not reducible to either form can break time-reversal symmetry and reach β > 1.

## 10-Constraint Score for C1 (Best Construction)
4 PASS / 2 PARTIAL / 0 FAIL / 2 NOT COMPUTED (code bugs) / 2 N/A

Passing: β > 1.5 (C1), NN-spacing KS < 0.05, GUE best fit, number variance Σ²(L>2) ≈ 0.5.

## Proof Gaps and Code Issues

1. **Pair correlation normalization bug:** R₂(r) code gives MRD = 0.996 (meaningless). Needs rewrite with proper unfolded-density normalization.
2. **Spectral rigidity Δ₃ formula bug:** Implementation uses `mean(residuals²)/L` which gives values 10–25× too small and decreasing in L (physically wrong). Needs the correct Dyson-Mehta integral formula.

## Unexpected Findings

1. **Number variance Σ²(L>2) = 0.499 for C1 is in the right range** (target 0.3–0.5) despite C1 being ~40% below the theoretical GUE prediction. The Mangoldt amplitude profile appears to increase spectral rigidity relative to flat-variance GUE.

2. **C3b (Gauss p=997) χ²_GOE = 0.64** — this is an *excellent* GOE fit, better than GOE statistics from the real-symmetric Hankel. The Gauss sum phases don't just add noise — they transform the statistics from Poisson toward a clean GOE distribution.

3. **p-dependence in Gauss constructions:** C3a (p=97 < N=500) gives β=0.88, while C3b (p=997 > N) gives β=1.09. Larger prime → more phase diversity in the N×N matrix → closer to true GUE. This suggests a p→∞ limit might achieve GUE, though with increasing arithmetic structure this is not guaranteed.

## Computations Identified for Follow-Up

1. **Fix pair correlation and Δ₃ code** — these are straightforward but critical for constraints 2 and 7.
2. **Redesign C2 with complex characters** — use χ mod 5 (complex values {1, i, -1, -i}) so the phase is genuinely complex and the matrix doesn't zero out.
3. **Explore larger primes for C3** — try p = 9973, 99991 to test the p→∞ trend in β.
4. **Hybrid construction** — C3b phases with C1-style amplitude modulation, to test whether Gauss + randomization can reach β > 1.5 with arithmetic motivation.
5. **C1 full averaging** — C1 averaged over 20–50 matrices would give reliable pair correlation and form factor estimates for constraints 2, 8, 9.
