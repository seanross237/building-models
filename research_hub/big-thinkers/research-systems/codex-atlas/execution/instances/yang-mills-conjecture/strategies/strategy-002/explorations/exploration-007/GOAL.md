# Exploration 007: Bound Non-Staggered Eigenvalues of M(Q)

## Mission Context

We proved that the staggered Rayleigh quotient ≤ 16 for all Q. But the adversarial review (E006) found that this doesn't imply lambda_max(M(Q)) ≤ 16 for the full 192D matrix. The non-staggered eigenvalues (starting at 12 at Q=I) grow to ~14.6 for random Q but never exceed 16 in 700+ tests.

**The remaining gap:** Prove that ALL eigenvalues of M(Q) are ≤ 16, not just the staggered ones.

## What's Known

At Q=I (L=2, d=4):
- M(I) eigenvalues: {0(×57), 4(×36), 8(×54), 12(×36), 16(×9)} — total 192
- Eigenvalue formula: 4*sum_mu sin^2(k_mu/2) for momentum k in {0,π}^4
- The 12-eigenspace has dimension 36, from momenta with 3 components = π
- Spectral gap: 16 - 12 = 4

For Q ≠ I:
- Staggered eigenvalue drops from 16 to ~8-10 (PROVED ≤ 16)
- Non-staggered 12-eigenvalue grows to ~14.6 (NOT proved ≤ 16)
- Trace invariant: Tr(M(Q)) = 1152 always
- Max full lambda_max in 700+ tests: 14.66

## Your Task

Prove that all eigenvalues of M(Q) are ≤ 16 for all Q in SU(2)^E. The staggered subspace is already covered (proved in E001-E005). Focus on the NON-staggered eigenvalues.

### Stage 1: Characterize the Non-Staggered Growth

For 200+ random Q on L=2:
1. Compute full 192×192 M(Q). Find all eigenvalues.
2. Decompose eigenvectors into momentum sectors (project onto Q=I eigenspaces).
3. For the top eigenvector: what momentum sector does it come from? How does its momentum composition change with Q?
4. Compute R(Q)|_{complement of P}: the restriction of R(Q) = M(Q) - M(I) to the non-staggered subspace. Find its maximum eigenvalue.
5. Report: max eigenvalue of R(Q)|_{non-stag} across all Q tested. If it's ≤ 4, the bound follows immediately.

### Stage 2: Trace + Staggered Bound Argument

Use the proved staggered bound to constrain non-staggered eigenvalues:

Let P = staggered projection (9D), Q_perp = I - P (183D).
We proved: v^T M(Q) v ≤ 16|v|^2 for v in P.
Trace: Tr(M(Q)) = 1152.
So: Tr(M(Q)|_{non-stag}) = 1152 - Tr(M(Q)|_{stag}).

Since M(Q)|_{stag} ≤ 16*I_9: Tr(M(Q)|_{stag}) ≤ 16*9 = 144.
But also Tr(M(Q)|_{stag}) ≥ 0 (eigenvalues of M are ≥ 0? CHECK THIS).

So: Tr(M(Q)|_{non-stag}) = 1152 - Tr(M(Q)|_{stag}) ≥ 1152 - 144 = 1008.
And: Tr(M(Q)|_{non-stag}) ≤ 1152 - 0 = 1152.

Average non-stag eigenvalue: 1152/183 ≈ 6.3 (if stag ≈ 0) to 1008/183 ≈ 5.5.
This doesn't directly bound lambda_max of non-stag modes.

BUT: can you combine trace with Tr(M^2)?
Tr(M(Q)^2) is NOT constant (it's 11520 at Q=I and ~10380 for random Q).
The maximum eigenvalue satisfies: lambda_max ≤ sqrt(Tr(M^2)) ≈ sqrt(10380) ≈ 102. Too loose.

Better: Schur complement. If we write M(Q) = [P^T M P, P^T M Q_perp; Q_perp^T M P, Q_perp^T M Q_perp], then lambda_max(M) ≤ max(lambda_max(P^T M P), lambda_max(Q_perp^T M Q_perp + correction)).

Try this numerically first. Compute Q_perp^T M(Q) Q_perp for 100+ Q and find its max eigenvalue. If it's always ≤ 16, done (no need for Schur complement correction).

### Stage 3: Direct Per-Vertex Approach for Non-Staggered Modes

The per-vertex proof for staggered modes used v_{x,mu} = (-1)^{|x|+mu} T_mu. For the next eigenspace (eigenvalue 12 at Q=I), the spatial pattern is different.

For momentum k = (π,π,π,0) (3 components = π): v_{x,mu} = (-1)^{x_1+x_2+x_3} * s_mu * n where s is a spatial vector with constraint sum s_mu = 0 and the 4th direction is different.

Can you set up a per-vertex analysis for these modes? The key question: does the per-vertex bound still give ≤ 16? Or better: does the per-vertex bound give ≤ 12 + delta for small delta?

### Stage 4: Operator Norm Bound on R(Q)

R(Q) = M(Q) - M(I). We proved R|_P ≤ 0 (on staggered). For non-staggered:

||R(Q)|| = ||M(Q) - M(I)|| ≤ ||M(Q)|| + ||M(I)||

This is circular. But:

For the non-staggered subspace specifically:
lambda_max(M(Q)|_{non-stag}) = lambda_max(M(I)|_{non-stag} + R(Q)|_{non-stag})
≤ 12 + lambda_max(R(Q)|_{non-stag})

We need: lambda_max(R(Q)|_{non-stag}) ≤ 4.

The trace gives: Tr(R|_{non-stag}) = -Tr(R|_{stag}) ≥ 0 (since R|_{stag} ≤ 0 implies Tr(R|_{stag}) ≤ 0).
So average of R|_{non-stag} eigenvalues ≥ 0. But we need the MAX ≤ 4.

Compute lambda_max(R|_{non-stag}) for 200+ Q. If it's always ≤ 4 (or even ≤ 3), report this. Then investigate whether this follows from the B-field structure.

### Stage 5: L=4 Spot Check

If time permits, construct M(Q) for L=4 (much larger matrix) and verify lambda_max ≤ 16 for 10+ random Q. This checks the bound at larger lattice size.

## Success Criteria

- **Full success**: Proof that lambda_max(M(Q)) ≤ 16 for all Q, covering non-staggered modes.
- **Partial success**: lambda_max(R|_{non-stag}) ≤ 4 computed for 200+ adversarial Q with 0 violations.
- **Failure with value**: Precise characterization of why the non-staggered bound is hard.

## Output

Write REPORT.md (max 250 lines) and REPORT-SUMMARY.md. Write incrementally.
