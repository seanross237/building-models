# Exploration 006 Summary: Prove lambda_max(M_total) <= 64

## Goal
Prove the Cube-Face Inequality: for all SO(3) rotations, lambda_max(M_total) <= 64. This is the last remaining step in proving Conjecture 1 (lambda_max(M(Q)) <= 16 for Yang-Mills on the d=4 torus).

## Outcome: SUCCESS — Proof complete

We provide a complete proof of lambda_max(M_total) <= 64, verified numerically at every step.

## Verification Scorecard
- **Verified**: 9 claims (algebraic identities, Cauchy-Schwarz, AM-GM, expansion, assembly)
- **Computed**: 3 claims (random/adversarial numerical checks)
- **Conjectured**: 0

## Key Takeaway

The proof has five steps:

1. **Trace identity** (algebraic): c + Tr(P) = 64, from the sign structure Σ σ_k = 20.

2. **Equivalence** (linear algebra): lambda_max(M) ≤ 64 iff lambda_max(P) ≤ Tr(P).

3. **Expansion**: 64I - M = 2 × [group_02 + group_13 + group_active], where group_active is a sum of 16 non-negative f-terms, and each inactive group is f(R_μ) + f(R_ν) + f(R_μD) + f(DR_ν^T) - f(D) - f(R_μDR_ν^T).

4. **Combined Bound Lemma** (the heart of the proof): For any A, B, D ∈ SO(3):
   f(A) + f(B) + f(AD) + f(DB^T) - f(D) - f(ADB^T) ≥ 0.

   Proved by an algebraic factorization identity:
   LHS = n^T(I-A)D(I-B^T)n + f(A) + f(B)

   Then Cauchy-Schwarz gives |cross term| ≤ 2√(f(A)f(B)), and AM-GM gives f(A) + f(B) - 2√(f(A)f(B)) = (√f(A) - √f(B))² ≥ 0.

5. **Assembly**: All three groups are ≥ 0, so 64I - M ≥ 0.

## Proof Gaps Identified
None — the proof is complete. The only remaining work is formal verification (e.g., in Lean), which would require:
- Formalizing the cross-term expansion (Step 3) — primarily bookkeeping
- Formalizing the algebraic factorization identity (Step 4a)
- The Cauchy-Schwarz and AM-GM steps are standard

## Unexpected Findings
- **Subadditivity f(AB) ≤ f(A) + f(B) FAILS** for SO(3) (max ratio ≈ 1.97). The proof works not because of subadditivity, but because of the deeper algebraic factorization f(A)+f(B)+f(AD)+f(DB^T)-f(D)-f(ADB^T) = n^T(I-A)D(I-B^T)n + f(A)+f(B).
- The Three Vectors Lemma (f(AB) ≤ 4f(A)+4f(B)) suffices for D=I but is too loose for general D. The Combined Bound Lemma is the right tool.

## Computations Identified
- Lean formalization of the complete proof
- Extension to d > 4 or L > 2 (different sign structures, different plaquette counts)
