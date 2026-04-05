# Exploration 008 — Report Summary

## Goal
Final synthesis: literature search for the two strongest novel claim candidates (N²/p Gauss scaling and Dirichlet impossibility), novelty assessment, and Strategy 003 recommendation.

## What Was Done
- Web search across 12+ queries for prior literature on Gauss sum matrix level statistics and Dirichlet character Hamiltonian GOE impossibility
- Assessment of all 5 Strategy 002 claim candidates against library findings and external literature
- Writing of two "paper format" claim writeups

## Novelty Verdicts

### Claim A: N²/p ≈ 250-310 Optimal Ratio (Gauss Sum Matrices) — **SUPPORTED**
**Finding:** For H_{jk} = Λ(|j-k|+1) × exp(2πijk/p) at N=500, β peaks at N²/p ≈ 309 (p=809, β=1.154). For large p (N²/p → 0), β → Poisson. All constructions: β < 1.2 (permanently GOE).

**Literature:** No prior paper studies Gauss sum / chirp matrices for level statistics. Closest analogue: Fyodorov-Mirlin band matrix transition (W²/N ~ 1) — different matrix class, different governing constant, and band matrices CAN reach GOE whereas our matrices are β-capped. The specific N²/p ≈ 250-310 constant is original.

**Caveat:** Only N=500 tested. N-scaling of the constant is unknown. "Universal" claim requires multi-N verification.

### Claim B: Dirichlet Character Matrices are Algebraically Confined to GOE — **SUPPORTED**
**Finding:** Any Hermitian H_{jk} = Λ × f(χ(j+1), χ(k+1)) is either (a) real symmetric (after Hermitianizing multiplicative phases) or (b) unitarily equivalent to a real matrix (conjugate phase D A D†). Both routes → GOE. Proved algebraically, confirmed numerically (β ≤ 0.28 for χ_5, χ_13).

**Literature:** Not explicitly documented. Follows from Dyson's threefold way + Katz-Sarnak (quadratic L-function families → orthogonal symmetry), but this specific matrix-theoretic proof for the Dirichlet character Hamiltonian is original. Schumayer-Hutchinson review (2011) does not discuss character-based Hamiltonians.

**Caveat:** Only covers multiplicative characters. Non-multiplicative arithmetic phases (Jacobi sums, Ramanujan τ) are not covered.

### Other Claims:
- C1 intermediate Δ₃ = 0.285: **WEAK novelty** (expected by specialists, not published for this matrix)
- Berry saturation: **NOT NOVEL** (confirmation of Berry 1985)
- Prime form factor normalization: **WEAK** (clarification, not new result)

## Key Takeaway
Strategy 001 found zero novel claims. Strategy 002 identifies two **SUPPORTED** claims: the N²/p scaling law and the Dirichlet impossibility proof. Both are specific, quantitative, and not in the literature, though both follow from general principles that experts would consider expected.

The adversarial review (E007) correctly downgraded the pair correlation claim. The surviving strong result is the anomalous Δ₃ intermediate rigidity — unique to Von Mangoldt Hankel structure — but this requires the flat-amplitude comparison (not yet done) to confirm that the Von Mangoldt structure specifically causes it.

## Strategy 003 Recommendation
Focus on: (1) flat-amplitude Δ₃ test (one Math Explorer computation to confirm whether Von Mangoldt structure causes intermediate rigidity); (2) N-scaling of N²/p (test N=250, 1000); (3) prime-indexed constructions targeting Δ₃ < 0.2. The central unsolved problem: no construction achieves both β > 1.5 AND Δ₃ < 0.2 simultaneously. The non-arithmetic GUE route (C1) gives β=1.18 but Δ₃=0.285 (not zeta-like). All arithmetic routes (Gauss, Dirichlet) are GOE.
