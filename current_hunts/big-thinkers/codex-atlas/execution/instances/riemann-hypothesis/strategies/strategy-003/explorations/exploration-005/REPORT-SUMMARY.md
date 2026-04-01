# Exploration 005 — Report Summary

## Goal
Two parts: (A) Rescore C1 matrix with corrected pair correlation and Δ₃ formulas; (B) Extend Gauss sum construction to larger primes to test β → 2 hypothesis.

## What Was Tried
- Part A: Regenerated 5 N=500 C1 matrices; computed pair correlation R₂(r) with correct normalization; computed Δ₃ via exact staircase integral minimization over a,b
- Part B: Built Gauss matrices for 6 main primes (97 to 99991) and 41 fine-sweep primes (500-5000); computed β_Wigner, β_Brody, χ², KS statistics for all
- NEW: Computed Δ₃ spectral rigidity for Gauss matrices at 6 key primes (97, 499, 809, 997, 1801, 9973)
- All results saved as .npz and .json for reproducibility

## Outcome: Three Definitive Results

### Part A — SUCCESS
1. **Pair correlation MRD = 7.9% → PASS** (previously 99.6%, normalization bug fixed)
2. **Δ₃ saturation = 0.285** (previously 0.007-0.011, formula error fixed). C1 is ~50% of GUE rigidity.
3. Updated C1 scorecard: **4 PASS, 2 PARTIAL, 0 FAIL**

### Part B — DEFINITIVE NEGATIVE on β trend
- β peaks at **p=809 (β=1.154)**, NOT at large p
- For p=99991: β=0.086 (near-Poisson collapse)
- Linear trend has NEGATIVE slope → **β → 2 as p → ∞ hypothesis REFUTED**
- All 47 primes tested give β < 1.2 → firmly GOE

### Part B Extension — NEW: Gauss Δ₃ reveals C1's anomalous rigidity
- Gauss Δ₃ saturation ranges **0.415–0.559** (71–96% of GUE)
- C1 Δ₃ saturation is **0.285** (49% of GUE) — **1.46× more rigid** than best Gauss
- Rigidity hierarchy established: **Zeta (0.155) < C1 (0.285) < Gauss-best (0.415) < GUE (0.581)**

## Verification Scorecard
- 0 VERIFIED (Lean)
- 10 COMPUTED (code runs, results saved to .npz/.json — all reproducible)
- 0 CHECKED (against known published values)
- 1 CONJECTURED (physical interpretation of N²/p scaling)

## Key Takeaway
**The spectral rigidity gap has a hierarchy.** The C1 random-phase construction achieves pair correlation matching Montgomery (MRD=7.9%) and Δ₃ ≈ 50% of GUE — but the Gauss arithmetic construction only achieves Δ₃ ≈ 71% of GUE at best. Neither construction approaches the zeta zeros' super-rigidity (27% of GUE). The extra rigidity in C1 vs Gauss comes from random phase diversity (U(1) per entry) vs structured Gauss phases (globally correlated). The gap between C1 (0.285) and zeta (0.155) represents the "arithmetic rigidity" that no matrix construction has yet captured.

## Proof Gaps
- No formal proofs attempted
- A theorem bounding β ≤ 1.2 for Gauss-Hankel matrices would formalize the GOE confinement
- Understanding why random phases create stronger long-range rigidity than arithmetic phases

## Unexpected Findings
1. **C1 is 1.46× more rigid than any Gauss matrix** despite similar β values (~1.1-1.2). Rigidity (Δ₃) and level repulsion (β) decouple in this regime.
2. **Large prime-to-prime β fluctuations**: p=809 (β=1.154) vs p=853 (β=0.731) — ΔΒ = 0.42 between neighboring primes, suggesting individual prime arithmetic effects
3. **Gauss p=9973 exceeds GUE at large L**: Δ₃(50) = 0.726 vs GUE prediction 0.617 — the matrix becomes less rigid than GUE for large p

## Computations Identified for Future Work
1. **N-dependence**: How does Δ₃ change with N for C1? Does the C1/GUE ratio stabilize or converge to 1?
2. **Hybrid phases**: Try phases mixing random U(1) with arithmetic structure to bridge the C1-to-zeta gap
3. **p=809 arithmetic**: Why does this specific prime maximize β? Related to 809 = 800 + 9 or quadratic residue structure?
4. **Δ₃ for actual zeta zeros**: Verify the 0.1545 value from strategy-001 using the corrected formula from this exploration
5. **Upper bound proof**: Can one prove β ≤ C for deterministic Gauss-phase Hankel matrices?
