# Exploration 002: Block Extension of Combined Bound Lemma to 9D Eigenspace

## Mission Context

We are proving Conjecture 1 for lattice SU(2) Yang-Mills: lambda_max(M(Q)) <= 16 for all Q in SU(2)^E on the d=4, even-L hypercubic torus.

**What's already proved (Strategy 001):** For UNIFORM-COLOR staggered modes v = (-1)^{|x|+mu} n (fixed color n in R^3), the per-vertex bound holds: F_x(Q, n) <= 64|n|^2. The proof uses:

1. **Trace identity**: c + Tr(P) = 64 identically (c = scalar part of M_total = 24 + 2*net_sign = 24 + 40 = 64... wait, c + Tr(P) = 64 from 28 positive, 8 negative cross-terms, net sigma = 20).
2. **Expansion**: 64I - M_total = 2[group_02 + group_13 + group_active] where groups use pairs of (mu,nu) orientations.
3. **Combined Bound Lemma**: For A, B, D in SO(3), unit n in R^3:
   f(A) + f(B) + f(AD) + f(DB^T) - f(D) - f(ADB^T) >= 0
   where f(R) = 1 - n^T R n.
   PROOF: LHS = n^T(I-A)D(I-B^T)n + f(A) + f(B). Then |cross| <= 2 sqrt(f(A)f(B)) by Cauchy-Schwarz, and f(A)+f(B) >= 2 sqrt(f(A)f(B)) by AM-GM.
4. **Assembly**: All three groups >= 0, so 64I - M_total >= 0.

**What remains (the gap this exploration attacks):** The full 9D eigenspace has modes where T_mu varies with mu. For v_{x,mu} = (-1)^{|x|+mu} T_mu with T a 4x3 matrix and sum_mu T_mu = 0:

F_x(Q, T) = sum_{mu<nu} |B_{(x,mu,nu)}(Q,v)|^2 <= 16 ||T||_F^2

This is verified with 0 violations across 110K+ tests. The gap = f_same + cross where f_same >= 0 and harmful cross <= 8.2% of f_same. An enormous 12x safety margin.

## Your Task

Extend the Combined Bound Lemma from scalar (uniform-color) to the full 9D vector case. The key idea: decompose the quadratic form into same-color and cross-color parts, and show the cross-color surplus can be absorbed by the same-color deficit.

### Stage 1: Numerical Verification (MANDATORY FIRST)

For 200+ random Q (each Q = set of 10 random SO(3) matrices R_0..R_3, D_01, D_02, D_03, D_12, D_13, D_23):
1. For each Q, compute F_x(Q, T) for 20 random T with sum_mu T_mu = 0
2. Compute 16||T||^2 - F_x (the gap)
3. Decompose the gap into f_same and cross:
   - gap = f_same + cross
   - f_same = 2 sum_{mu<nu} [f(U_{mu,nu}, T_mu) + f(W_{mu,nu}, T_nu)]  (always >= 0)
   - cross = -2 sum_{mu<nu} T_mu^T C_{mu,nu} T_nu
   where f(R,p) = p^T(I-R)p, U_{mu,nu} = R_mu D_{mu,nu}, W_{mu,nu} = D_{mu,nu} R_nu^T,
   C_{mu,nu} = (I-R_mu) + (I-R_nu^T) + (I-D_{mu,nu}^T) + (I-R_mu D_{mu,nu} R_nu^T)
4. Verify f_same >= 0 in all cases
5. When cross < 0: compute |cross|/f_same. Verify <= 8.2%
6. Find the T that maximizes |cross|/f_same for each Q via gradient optimization
7. Report: max |cross|/f_same across all (Q, T) pairs

### Stage 2: Block Decomposition of M_12

Write F_x(Q, T) as a block matrix quadratic form:

F_x = sum_{mu,nu color blocks} T_mu^T [M_12]_{mu,nu} T_nu

where [M_12]_{mu,nu} are 3x3 blocks. There are 4x4 = 16 blocks (mu, nu each range 0..3).

**Same-color blocks** (diagonal, mu=nu): [M_12]_{mu,mu} = sum of contributions from plaquettes involving direction mu. For UNIFORM color (all T_mu = n), these give the proved M_total = cI + P with c + Tr(P) = 64.

**Cross-color blocks** (off-diagonal, mu != nu): [M_12]_{mu,nu} for mu != nu. These arise from the plaquette (mu,nu) and from the expansion. They are zero for the uniform-color case (since all T_mu are the same).

Compute these blocks symbolically. Verify numerically for 50+ Q.

### Stage 3: Epsilon-Delta Proof Strategy

The core proof idea: if we can show that the same-color surplus strictly dominates the cross-color contribution, we're done.

Define:
- epsilon(Q) = min over T in V, ||T||=1 of: f_same(Q, T) / ||T||^2
- delta(Q) = max over T in V, ||T||=1 of: [cross(Q, T)]_- / ||T||^2  (negative part only)

If epsilon(Q) > delta(Q) for all Q, then gap = f_same + cross >= (epsilon - delta)||T||^2 > 0.

Compute epsilon(Q) and delta(Q) for 100+ Q including adversarial configs.

### Stage 4: Vector Combined Bound Lemma

Try to generalize the Combined Bound Lemma to vector-valued arguments. For p, q in R^3 (not necessarily parallel):

**Candidate lemma**: For A, B, D in SO(3), p, q in R^3:
  f(A,p) + f(B,q) + f(AD,p) + f(DB^T,q) - g(D,p,q) - g(ADB^T,p,q) >= 0

where f(R,p) = p^T(I-R)p and g needs to be identified.

The uniform-color case has p = q = n, and g(R,n,n) = f(R) = 1 - n^T R n.

For the general case, the B-field for plaquette (mu,nu) is:
|B_{mu,nu}|^2 = |(I + R_mu D) T_mu - (R_mu + R_mu D R_nu^T) T_nu|^2

Expand this. It has same-color terms (involving |T_mu|^2, |T_nu|^2) and cross-color terms (involving T_mu^T [...] T_nu). The cross-color terms come from:

-2 T_mu^T (I + R_mu D)^T (R_mu + R_mu D R_nu^T) T_nu + (other cross terms)

**Key question**: Can the factorization identity from the Combined Bound Lemma
  LHS = n^T (I-A) D (I-B^T) n + f(A) + f(B)
be extended to:
  LHS_vector = p^T (I-A) D (I-B^T) q + f(A,p) + f(B,q) + [correction terms] >= 0 ?

The cross term p^T (I-A) D (I-B^T) q is bounded by Cauchy-Schwarz:
|p^T (I-A) D (I-B^T) q| <= ||(I-A)^T p|| * ||(I-B^T) q|| = 2 sqrt(f(A,p)) sqrt(f(B,q))

And f(A,p) + f(B,q) >= 2 sqrt(f(A,p) f(B,q)) by AM-GM.

SO THE SAME ARGUMENT WORKS! The question is whether the per-plaquette expansion for general T has the same structure as the uniform-color case, just with (p,q) replacing (n,n).

**Verify this computationally**: For each plaquette (mu,nu), check whether:
  4|T_mu - T_nu|^2 - |B_{mu,nu}|^2 = p^T (I-A) D (I-B^T) q + f(A,p) + f(B,q) + [explicit correction]

for appropriate A, B, D, p, q depending on (mu,nu). If the correction is always >= 0, the proof is done.

### Stage 5: Assembly

If Stage 4 succeeds: write the full proof. Sum over plaquettes, use the budget identity 16||T||^2 = 4 sum |T_mu - T_nu|^2, and assemble.

If Stage 4 fails: characterize exactly which terms in the expansion prevent the factorization from working. Report the precise obstruction.

## Key Context: What Failed Before

- E006 trace identity FAILS for general T (trace varies by factor ~3 with spatial pattern s_mu)
- Maximizing T is NOT always rank-1 (can't reduce to uniform-color case)
- The constraint sum_mu T_mu = 0 is ESSENTIAL (unconstrained eigenvalue reaches ~21)
- Cross-link monotonicity FAILS

## Key Insight for This Exploration

The Combined Bound Lemma's proof structure (factorization → Cauchy-Schwarz → AM-GM) works for ANY vectors p, q — not just p = q = n. The scalar inner product n^T (I-A) D (I-B^T) n generalizes to the bilinear form p^T (I-A) D (I-B^T) q, and Cauchy-Schwarz still applies:

|p^T (I-A) D (I-B^T) q| <= sqrt(p^T(I-A)(I-A^T)p) * sqrt(q^T(I-B)(I-B^T)q)
                         = sqrt(f(A,p) * something) * sqrt(f(B,q) * something)

The "something" may involve norms of (I-A) and (I-B) as operators. CHECK whether ||(I-A)x||^2 = 2f(A,x) or whether there's an extra factor.

## Success Criteria

- **Full success**: A proof that 16||T||^2 - F_x(Q,T) >= 0 for all T in V, all Q, via a vector extension of the Combined Bound Lemma.
- **Partial success**: A proof for a subspace larger than 3D (e.g., all rank-1 T), or a quantitative epsilon bound.
- **Failure with value**: A precise characterization of which cross terms prevent the factorization argument from closing.

## Output

Write results to REPORT.md (full details, max 250 lines) and REPORT-SUMMARY.md (concise summary) in your working directory. Write incrementally — output after each stage.
