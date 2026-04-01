# Exploration 006 Summary: Adversarial Review

## Goal
Independently verify the complete proof chain claiming lambda_max(M(Q)) ≤ 16 for Yang-Mills on the d=4 torus, and try to break it.

## Outcome: CONDITIONAL PASS — Logical Gap in Part C

**What works:** All per-vertex algebraic identities (B1-B9) independently verified from scratch. Per-vertex bound F_x ≤ 16||T||² is correct with large safety margin. No double counting. 0 violations in 1800+ per-vertex tests and 700+ full-matrix tests (L=2 and L=3).

**What doesn't work:** The upstream connection (Part C) has a genuine logical gap. The proof bounds v^T M(Q)v ≤ 16|v|² for the 9D staggered subspace, then claims lambda_max(M(Q)) ≤ 16 for the full 192D matrix. This doesn't follow. For random Q, the top eigenvector is predominantly non-staggered (staggered projection < 0.5), and the actual lambda_max (~14.5) is controlled by non-staggered modes, which the proof does not bound.

**Severity:** The non-staggered eigenvalue grows from 12 (at Q=I) to 14.6 (random Q) — it APPROACHES 16 but never exceeds it in 700+ tests. The proof is bounding the wrong subspace, but the overall bound likely holds.

## Verification Scorecard
- **[VERIFIED]:** 11 claims (all identities B1-B9, no double counting, lattice formula match)
- **[COMPUTED]:** 4 claims (full lambda_max ≤ 16, odd L holds, non-stag eigenvalue < 16, normalization)
- **[CONJECTURED]:** 1 claim (SZZ normalization convention)
- **[FAILED]:** 1 claim (staggered bound ⟹ full lambda_max bound — logical gap)

## Key Takeaway
The per-vertex proof chain (Parts A+B) is a solid, verified mathematical result. But it proves F_x ≤ 16||T||² per-vertex, which only bounds the staggered Rayleigh quotient. For the full lambda_max bound, an additional argument is needed to control the non-staggered eigenvalues (max ~14.6 at L=2, ~14.1 at L=3). The gap is NOT in the algebra — it's in the reduction from per-vertex to global.

## Proof Gaps Identified
1. **Non-staggered eigenvalue bound:** Need to show eigenvalues from the 12-eigenspace (at Q=I) don't exceed 16 for any Q. This is the only remaining gap for the full claim.
2. **Odd L coverage:** At L=3, Q=I max eigenvalue is 12 (not 16). The staggered bound of 16 is slack. The proof's sign structure analysis applies to even L only.
3. **SZZ normalization:** The exact H_norm formula (N=2 vs N=3 convention) needs pinning down.

## Computations Identified
- Prove eigenvalue bound for non-staggered modes (the k=(0,π,π,π) sector and its rotations)
- Trace argument: Tr(M(Q)) = 1152 is invariant. Could constrain lambda_max jointly with per-vertex bound.
- Investigate why non-stag eigenvalues appear capped at ~14.6 (well below 16)

## Unexpected Findings
- For all tested random Q, the top eigenvector of M(Q) is MOSTLY non-staggered (100% of 200 trials). The staggered eigenvalue drops to ~8-10 while non-staggered grows to ~14. The per-vertex proof bounds a subspace that is never the binding constraint for Q ≠ I.
- L=3 max eigenvalue at Q=I is 12 (= 4d·sin²(π/3)), not 16. Different from L=2 (= 4d·sin²(π/2) = 16). The staggered bound of 16 has a margin of 4 at Q=I for odd L.
