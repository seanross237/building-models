---
topic: Decompose matrix inequality corrections into PSD + indefinite components
category: methodology
date: 2026-03-29
source: "yang-mills-validation strategy-002 meta-exploration-002"
---

## Lesson

When analyzing a matrix inequality A ≤ B (i.e., C = B − A ≥ 0), decompose the correction C into sign-definite and indefinite components: C = C₊ + C₋, where C₊ is PSD and C₋ is indefinite. This clarifies the **mechanism** by which the inequality holds (or fails), and reveals the quantitative margins.

## Evidence

- **yang-mills-validation S002-E002** — Decomposition C = C_curv + C_comm for the Wilson action Hessian, where C_curv = (β/4)(1−cosθ)BᵀB (PSD, curvature bonus) and C_comm (indefinite, commutator correction). This immediately revealed: (1) C is NOT PSD (41 negative eigenvalues), so H_actual ≤ H_formula does NOT hold as a matrix inequality; (2) the curvature bonus barely compensates the commutator correction in the top eigenspace (ratio 1.10); (3) the mechanism is decoherence vs. cross terms, clarifying why per-plaquette proofs fail.

## Protocol

When facing a matrix inequality C = B − A ≥ 0:

1. **Identify natural sign-definite components.** Look for terms that are manifestly PSD (e.g., quadratic forms, BᵀB structures, (1−cosθ) factors) vs. terms that can have either sign (commutators, cross terms, interference).

2. **Decompose and verify numerically.** Confirm |C − (C₊ + C₋)| ≈ 0 to machine precision. Compute eigenvalues of each component separately.

3. **Check the mechanism at the relevant eigenspace.** Even if C is not PSD everywhere, it may be non-negative where it matters (e.g., at the top eigenvector of A). Compute v_top^T C₊ v_top and v_top^T C₋ v_top separately. The ratio C₊/|C₋| reveals the margin.

4. **Use the decomposition to guide proof strategy.** If C₊ always dominates C₋ at the relevant eigenspace, prove that relationship. If not, find alternative routes.

## Contrast with Other Patterns

- **check-affine-structure-before-bounding.md** — complementary: affine structure enables algebraic decomposition; PSD+indefinite decomposition is for understanding the mechanism.
- **structural-vs-quantitative-discrepancy.md** — complementary: that pattern diagnoses whether a discrepancy is fixable; this pattern reveals the internal structure of a matrix inequality.
