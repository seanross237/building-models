# Exploration 004: Prove sum_S >= 0 (Closing the 9D Gap)

## Mission Context

We are proving Conjecture 1 for lattice SU(2) Yang-Mills: lambda_max(M(Q)) <= 16 for all Q.

**Proof chain so far:**
1. Budget identity: 16||T||^2 = 4 sum_{mu<nu} |T_mu - T_nu|^2 for T in V = {T: sum T_mu = 0} [PROVED]
2. Per-plaquette: 4|T_mu - T_nu|^2 - |B|^2 = 2f(U,T_mu) + 2f(W,T_nu) - 2 T_mu^T C T_nu [VERIFIED]
3. Sum-to-zero extraction: 16||T||^2 - F_x = 2*sum_mu f(R_mu, T_mu) + sum_S [VERIFIED to 5.7e-14]
4. term1 = 2*sum f(R_mu, T_mu) >= 0 [TRIVIAL, since f(R,p) = p^T(I-R)p >= 0]

**What remains:** Prove sum_S >= 0.

## The Target: sum_S >= 0

### Definition
sum_S = sum_{mu<nu} S_{mu,nu} where:
S_{mu,nu} = 2f(R_mu D_{mu,nu}, T_mu) + 2f(D_{mu,nu} R_nu^T, T_nu) - 2 T_mu^T [2I - D_{mu,nu}^T - R_mu D_{mu,nu} R_nu^T] T_nu

Here f(M,p) = p^T(I-M)p >= 0 for M in SO(3).

### Key Numerical Facts [ALL from E003, COMPUTED]
- 200 adversarial optimizations ALL converge to min eigenvalue = 0 (TIGHT)
- sum_S = 0 iff all D_{mu,nu} = I (for ANY R, ANY T in V)
- At R = I (all base links identity): sum_S = 2 * sum_{mu<nu} VCBL(D,D,-I,T_mu,T_nu) >= 0 (PROVED via C-S + AM-GM)
- Individual LEMMA_D and LEMMA_RDR are FALSE (counterexamples at -2.13, -1.45)
- Per-plaquette S_{mu,nu} can be negative. Complementary pairs can be negative. Need all 6 together.
- Near Q=I: sum_S ~ O(eps^2) with positive coefficient ~2.96
- max |harmful cross|/budget ≈ 0.28

## Your Specific Task

Prove sum_S >= 0 for all R_mu in SO(3), D_{mu,nu} in SO(3), T in V.

### Stage 1: Verify and Characterize the D=I Identity (MUST DO FIRST)

At D = I for all plaquettes:
S_{mu,nu}(D=I) = 2f(R_mu, T_mu) + 2f(R_nu^T, T_nu) - 2 T_mu^T [2I - I - R_mu R_nu^T] T_nu
              = 2f(R_mu, T_mu) + 2f(R_nu^T, T_nu) - 2 T_mu^T (I - R_mu R_nu^T) T_nu

E003 claims: sum_S(D=I) = 0 for ALL R, ALL T in V. VERIFY this numerically for 200+ random (R, T) configurations. If confirmed, prove it algebraically.

HINT: Try expanding f(R_mu, T_mu) = T_mu^T(I-R_mu)T_mu and summing. With sum T_mu = 0, the cross-terms may cancel. This identity, if proved, is a key building block.

### Stage 2: Factor Out D-Dependence

Since sum_S(D=I) = 0 for all R, T, write:
sum_S(R, D, T) = sum_S(R, D, T) - sum_S(R, I, T) = Delta_sum_S(R, D, T)

Compute Delta_sum_S explicitly. For each plaquette (mu,nu):
Delta_S_{mu,nu} = S_{mu,nu}(D) - S_{mu,nu}(D=I)
= 2[f(R_mu D, T_mu) - f(R_mu, T_mu)] + 2[f(D R_nu^T, T_nu) - f(R_nu^T, T_nu)]
  - 2 T_mu^T [(I-D^T) + (R_mu R_nu^T - R_mu D R_nu^T)] T_nu

Simplify using:
f(R_mu D, T_mu) - f(R_mu, T_mu) = T_mu^T [R_mu - R_mu D] T_mu = T_mu^T R_mu (I - D) T_mu

And:
f(D R_nu^T, T_nu) - f(R_nu^T, T_nu) = T_nu^T [R_nu^T - D R_nu^T] T_nu = T_nu^T (I - D) R_nu^T T_nu
Wait — check this: f(M,p) = p^T(I-M)p. So f(M',p) - f(M,p) = p^T(M - M')p.

So f(R_mu D, p) - f(R_mu, p) = p^T(R_mu - R_mu D)p = p^T R_mu(I-D)p
And f(D R_nu^T, q) - f(R_nu^T, q) = q^T(R_nu^T - D R_nu^T)q = q^T(I-D)R_nu^T q

Verify these identities computationally. Then:
Delta_S_{mu,nu} = 2 T_mu^T R_mu(I-D)T_mu + 2 T_nu^T(I-D)R_nu^T T_nu
  - 2 T_mu^T (I-D^T) T_nu - 2 T_mu^T R_mu(I-D)R_nu^T T_nu

The key: every term involves (I-D) or (I-D^T). Try to write Delta_S as a quadratic form in (I-D).

SPECIFICALLY: Let E = I - D (a matrix near 0 for D near I). Then:
Delta_S_{mu,nu} = 2 T_mu^T R_mu E T_mu + 2 T_nu^T E R_nu^T T_nu - 2 T_mu^T E^T T_nu - 2 T_mu^T R_mu E R_nu^T T_nu

Can this be written as ||something||^2? Try: ||(I-D)^{1/2} [alpha T_mu + beta T_nu]||^2 for some choice of alpha, beta.

### Stage 3: Direct Squared Norm Approach

Forget the decomposition entirely. Go back to the per-plaquette identity:
|B_{mu,nu}|^2 = |(I + R_mu D) T_mu - (R_mu + R_mu D R_nu^T) T_nu|^2

So 4|T_mu - T_nu|^2 - |B|^2 = 4|T_mu - T_nu|^2 - |(I+U)T_mu - (U+W^{-T})T_nu|^2
where U = R_mu D, W = D R_nu^T. (Check W^{-T} = R_nu D^{-T} = R_nu D^T... careful with transposes.)

Actually, B = (I+R_mu D)T_mu - (R_mu + R_mu D R_nu^T)T_nu = (I+U)T_mu - R_mu(I+D R_nu^T)T_nu.

Try writing the gap 4|p-q|^2 - |(I+U)p - R_mu(I+W)q|^2 as a sum of squared norms.

Expand |(I+U)p - R_mu(I+W)q|^2 = |(I+U)p|^2 + |R_mu(I+W)q|^2 - 2 p^T(I+U)^T R_mu(I+W)q
= |p+Up|^2 + |q+Wq|^2 - 2 p^T(I+U^T R_mu)(I+W)q

Check if a completing-the-square identity exists. For D=I: U = R_mu, W = R_nu^T, and B = (I+R_mu)T_mu - R_mu(I+R_nu^T)T_nu = (I+R_mu)(T_mu - T_nu) + (T_nu - R_mu R_nu^T T_nu). Hmm.

### Stage 4: Prove sum_S >= 0 for Rank-1 T

A partial result: prove sum_S >= 0 for T_mu = s_mu n (all same color direction n). This SHOULD reduce to the uniform-color case (already proved in Strategy 001).

Verify: for rank-1 T in V (i.e., s in R^4 with sum s_mu = 0, n in R^3):
sum_S(R, D, s*n) = n^T [sum_S_matrix(R, D, s)] n

Does this reduce to a known quantity from the E006 proof? If so, sum_S >= 0 for rank-1 T follows from the uniform-color proof.

Then try: does sum_S being >= 0 for all rank-1 T imply sum_S >= 0 for all T in V? (This would require showing the 9x9 sum_S matrix is PSD given all its rank-1 projections are non-negative — which is exactly what PSD means!)

Actually, sum_S >= 0 for all T iff the 9x9 matrix M_{sum_S}|_V is PSD. And M is PSD iff n^T M n >= 0 for all n. But T is a 4x3 matrix, not a vector. The rank-1 case T_mu = s_mu n gives: sum_S = n^T [matrix in s] n. Being >= 0 for all n means [matrix in s] >= 0 as 3x3. Being >= 0 for all s in V means... this is the uniform color proof already.

Hmm, rank-1 T are special but don't span V. The sum_S >= 0 for general T requires PSD of the full 9x9 matrix, which cannot be deduced from rank-1 alone.

### Stage 5: Try Convexity in D

For fixed (R, T), consider g(D) = sum_S(R, D, T) as a function of D = (D_01,...,D_23) in SO(3)^6.

g(I,...,I) = 0 (proved in Stage 1). If g is geodesically convex in D, the minimum is at D=I and equals 0. Done.

Compute the Hessian d^2g/dD^2 at D = I along 50+ random geodesic directions. If ALL eigenvalues are non-negative, convexity is plausible.

If the Hessian is PSD at D=I, check convexity at OTHER D points too (50+ random D). If the Hessian is PSD everywhere, the function is convex and the proof follows.

## Success Criteria

- **Full success**: Algebraic proof of sum_S >= 0. This completes the full Conjecture 1 proof.
- **Significant partial success**: Proof of the D=I identity + proof that sum_S is convex in D (even without algebraic closed form).
- **Partial success**: Proof of sum_S >= 0 for rank-1 T, or for a specific subclass of D.
- **Failure with value**: If convexity fails, characterize where. If factoring fails, identify the obstruction.

## Dead Ends (DO NOT REVISIT)

- LEMMA_D >= 0: FALSE (min -2.13)
- LEMMA_RDR >= 0: FALSE (min -1.45)
- Per-plaquette S_{mu,nu} >= 0: FALSE
- Per-plaquette VCBL: can't handle rank-3 cross term
- Plaquette pair grouping: complementary pairs can be negative

## Output

Write results to REPORT.md (max 250 lines) and REPORT-SUMMARY.md. Write incrementally after each stage.
