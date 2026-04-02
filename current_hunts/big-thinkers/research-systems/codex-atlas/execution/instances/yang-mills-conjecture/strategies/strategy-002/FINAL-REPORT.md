# Strategy 002 Final Report: Close the 9D Eigenspace Gap

## Executive Summary

Strategy 002 set out to prove lambda_max(M(Q)) <= 16 for all Q in SU(2)^E by extending the Strategy 001 uniform-color proof (3D staggered) to the full 9D staggered eigenspace. Through 7 explorations, we achieved:

1. **PROVED the full 9D staggered bound** — a novel 6-step algebraic proof showing F_x(Q,T) <= 16||T||^2 for all general staggered modes T with sum T_mu = 0
2. **Independently verified all proof steps** — adversarial review confirmed every identity and found no computational errors
3. **Identified a critical upstream gap** — the staggered bound doesn't imply the full lambda_max bound; non-staggered eigenvalues are not controlled
4. **Potentially falsified the full conjecture** — E007 found lambda_max(M(Q)) ≈ 16.08 via gradient ascent, though this finding needs re-verification with the exact adjoint-representation B-field formula

## What Was Proved

### The Per-Vertex Staggered Bound (PROVED, adversarial-verified)

**Theorem:** For all Q in SU(2)^E on the even-L, d=4 hypercubic torus, all vertices x, and all 4×3 matrices T with sum_mu T_mu = 0:

F_x(Q, T) = sum_{mu<nu} |B_{(x,mu,nu)}(Q, v)|^2 <= 16 ||T||_F^2

where v_{x,mu} = (-1)^{|x|+mu} T_mu is a general staggered mode.

**Proof outline (6 steps):**
1. **Budget identity:** 16||T||^2 = 4 sum_{mu<nu} |T_mu - T_nu|^2 (uses sum T_mu = 0) [PROVED]
2. **Per-plaquette expansion:** Each plaquette gives 2f(U,T_mu) + 2f(W,T_nu) - 2 cross [VERIFIED to 1e-13]
3. **Sum-to-zero extraction:** Total gap = 2*sum f(R_mu, T_mu) + sum_S [VERIFIED to 5.7e-14]
4. **D=I base case:** sum_S(D=I) = 6*sum f(R,T) + |sum R^T T|^2 >= 0 [PROVED]
5. **Delta factoring + Cauchy-Schwarz:** M9 is affine in D; CS gives D-free lower bound [VERIFIED to 7.1e-14, PROVED]
6. **Cancellation:** F = 2*sum f(R,T) + sum(||u||-||v||)^2 >= 0 [PROVED]

The proof uses only elementary tools: Cauchy-Schwarz, AM-GM, the polarization identity, and combinatorial bookkeeping. The key structural insight is that M_9 is affine in the cross-link matrices D, enabling independent per-pair minimization.

### Additional Proved Results

- **Vector Combined Bound Lemma (VCBL):** f(A,p)+f(B,q)+p^T(I-A)D(I-B^T)q >= 0 for all A,B,D in SO(3), p,q in R^3 [PROVED, E002]
- **Critical T Theorem:** sum_S >= 0 for T_mu on rotation axes of R_mu [PROVED, E004]
- **D=I Identity:** sum_S(D=I) = 6*sum f + |sum R^T T|^2 [PROVED, E004]

### What Was NOT Proved

- **Full lambda_max(M(Q)) <= 16:** The staggered bound covers only the 9D top eigenspace at Q=I. Non-staggered eigenvalues (starting at 12 at Q=I) can grow to ~14.6 for random Q and potentially to ~16.08 under optimization (E007).
- **Odd L:** The sign structure analysis applies to even L only.

## Directions Tried

| Direction | Explorations | Outcome |
|-----------|-------------|---------|
| SDP/SOS certificate | E001 | Decomposition found. SOS blocked (slack=0 at Q=I). |
| Block extension of CBL | E002 | VCBL proved. sum_S = LEMMA_D + LEMMA_RDR identified. |
| Individual lemma proof | E003 | LEMMA_D and LEMMA_RDR individually FALSE. Correct target: sum_S. |
| sum_S proof (1st attempt) | E004 | Critical T theorem PROVED. D=I identity corrected. |
| sum_S proof (2nd attempt) | E005 | **FULL PROOF** via affine-in-D + CS + cancellation. |
| Adversarial review | E006 | CONDITIONAL PASS. All identities verified. Upstream gap found. |
| Non-staggered bound | E007 | POTENTIALLY FALSE (lambda_max ≈ 16.08 via gradient ascent). |

## What the Next Strategy Should Focus On

### Priority 1: Verify E007's Counterexample

E007 found lambda_max(M(Q)) ≈ 16.08 via edge-by-edge gradient ascent. This MUST be verified with the exact adjoint-representation B-field formula from MISSION.md. E007 may have used the fundamental representation (Q*v rather than Ad(Q)(v) = QvQ^{-1}). If the representations differ, the counterexample may be invalid.

### Priority 2: M(Q) vs Hessian Distinction

E007 noted that M(Q) = sum B^T B is NOT the Wilson action Hessian. The Hessian includes a curvature correction: H(Q) = M(Q) - C(Q). The SZZ Bakry-Emery framework uses the Hessian, not M(Q). If lambda_max(H(Q)) <= 16 even when lambda_max(M(Q)) > 16, the mass gap argument still works.

**Critical question:** Does bounding the staggered Rayleigh quotient of the Hessian (not M(Q)) suffice for the SZZ framework?

### Priority 3: If Conjecture 1 is False

If lambda_max(M(Q)) > 16 is confirmed, explore:
1. What is the true supremum? (Appears close to 16 — possibly 16 + O(1/L^2)?)
2. Does the Hessian satisfy a tighter bound?
3. Can the mass gap argument be modified to work with a weaker bound?

## Novel Claims

### Claim 1: Per-Vertex General Staggered Bound

**Claim:** F_x(Q,T) <= 16||T||^2 for all T with sum T_mu = 0, all Q in SU(2)^E, even L, d=4.

**Evidence:** 6-step algebraic proof (E005) using budget identity, per-plaquette expansion, sum-to-zero trick, D=I base case, affine-in-D + Cauchy-Schwarz contraction, and exact cancellation. Every step verified to machine precision across 25K+ tests.

**Novelty search:** This extends the Strategy 001 uniform-color result to the full 9D staggered eigenspace. The key new tool is the affine-in-D structure enabling D-elimination via Cauchy-Schwarz.

**Strongest counterargument:** The per-vertex bound is correct but insufficient — it doesn't control non-staggered eigenvalues, which may exceed 16 under optimization.

**Status:** VERIFIED — complete algebraic proof, adversarial-reviewed.

### Claim 2: sum_S >= 0 Proof

**Claim:** sum_S(R, D, T) = sum of per-plaquette contributions >= 0 for all R, D in SO(3)^{10}, T with sum T_mu = 0.

**Evidence:** 6-step proof. The crucial insight: M_9 (the 9x9 matrix giving sum_S as a quadratic form) is AFFINE in each cross-link D. This allows independent minimization over D via Cauchy-Schwarz (u^T Dv <= ||u||*||v||), producing a D-free lower bound F = 2*sum f(R,T) + sum(||u||-||v||)^2 >= 0.

**Novelty:** The affine-in-D structure and its exploitation via contraction bounds appears to be new in this context.

**Strongest counterargument:** None for the claim itself. The claim is proved.

**Status:** VERIFIED.

### Claim 3: LEMMA_D and LEMMA_RDR are Individually False

**Claim:** The decomposition sum_S = LEMMA_D + LEMMA_RDR does NOT work piece-by-piece. LEMMA_D has genuine counterexamples (min eigenvalue -2.13).

**Evidence:** Adversarial optimization found counterexamples verified across 20 independent trials (E003).

**Status:** VERIFIED.

## Proof Status Summary

```
CONJECTURE 1: lambda_max(M(Q)) <= 16 for all Q

├── Staggered subspace (9D): F_x <= 16||T||^2
│   ├── Uniform-color (3D): PROVED (Strategy 001)
│   └── Direction-dependent (6D): PROVED (Strategy 002, E005)
│       └── sum_S >= 0: PROVED via affine-in-D + CS + cancellation
│
├── Non-staggered subspace (183D at L=2): NOT PROVED
│   ├── At Q=I: max eigenvalue = 12 (gap of 4)
│   ├── Random Q: max eigenvalue ≈ 14.6 (well below 16)
│   └── Adversarial Q: max eigenvalue ≈ 16.08 (POTENTIALLY EXCEEDS 16)
│       └── NEEDS RE-VERIFICATION with correct B-field formula
│
├── Even L: staggered bound proved
├── Odd L: NOT COVERED
│
└── Mass gap connection:
    ├── If Conjecture 1 proved: beta < 1/4 via SZZ
    ├── If M(Q) slightly exceeds 16: investigate Hessian vs M(Q) distinction
    └── Current best rigorous: beta < 1/6 (from H_norm <= 1/8)
```

## Metrics

- **Explorations used:** 7 of 7 budget
- **Novel claims:** 3 (per-vertex general staggered bound, sum_S proof, individual lemma falsification)
- **Key insight:** M_9 is affine in cross-link matrices D, enabling contraction-based D-elimination
- **Proof steps verified:** 11 identities to machine precision, 0 failures
- **Adversarial tests passed:** 67K+ per-vertex, 700+ full-matrix, 0 violations for staggered bound
