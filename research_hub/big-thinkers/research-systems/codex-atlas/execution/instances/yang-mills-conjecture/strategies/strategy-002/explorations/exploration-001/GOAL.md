# Exploration 001: SDP / Sum-of-Squares Certificate for 9D Eigenspace Bound

## Mission Context

We are proving Conjecture 1 for lattice SU(2) Yang-Mills: lambda_max(M(Q)) <= 16 for all Q in SU(2)^E on the d=4, even-L hypercubic torus.

**What's already proved (Strategy 001):** The per-vertex bound F_x(Q, n) = sum_{mu<nu} |B_{(x,mu,nu)}(Q, v_stag)|^2 <= 64|n|^2 for UNIFORM-COLOR staggered modes v = (-1)^{|x|+mu} n (fixed color n in R^3). Proof uses a 5-step argument: trace identity c+Tr(P)=64, expansion 64I-M=2[groups], Combined Bound Lemma, assembly.

**What remains (the gap this exploration attacks):** The uniform-color proof covers only 3 of 9 dimensions of the top eigenspace P. The full eigenspace has modes where color direction varies with spatial direction mu: v_{x,mu} = (-1)^{|x|+mu} T_mu where T = (T_0, T_1, T_2, T_3) is a 4x3 matrix with constraint sum_mu T_mu = 0 (giving 9 DOF).

**The target inequality:** F_x(Q, T) <= 16 ||T||_F^2 for all T with sum_mu T_mu = 0, all Q.

Equivalently: lambda_max(M_9(Q)) <= 16 where M_9(Q) is the 9x9 matrix obtained by restricting the 12x12 per-vertex Hessian M_12 to V = {T : sum_mu T_mu = 0}.

## Your Task

Attack the 9D bound via SDP / Sum-of-Squares techniques. The problem is a MATRIX INEQUALITY: 16I_9 - M_9(Q) >= 0 (PSD) for all Q parametrized by 10 SO(3) matrices (4 base links R_mu, 6 cross-links D_{mu,nu}).

### Stage 1: Numerical Verification (MANDATORY FIRST)

For 100+ random Q (each Q = set of 10 independent SO(3) matrices):
1. Construct M_12(Q) explicitly as a 12x12 matrix
2. Project to the 9D constraint space: M_9 = P_V^T M_12 P_V where P_V is the 12x9 orthogonal projector onto V
3. Compute lambda_max(M_9(Q))
4. Verify: all lambda_max < 16
5. Compute the gap: 16 - lambda_max(M_9(Q)) for each Q
6. Report the minimum gap and the Q that achieves it

Also: verify independently that the harmful cross-term ratio (max |cross|/f_same when cross < 0) is <= 8.2%, using the gap decomposition 16||T||^2 - F_x = f_same + cross.

### Stage 2: M_12 Formula Construction

The per-vertex F_x for general T involves:
- 6 plaquette orientations (mu,nu) with mu<nu
- For each: |B_{mu,nu}|^2 = |(I + R_mu D_{mu,nu}) T_mu - (R_mu + R_mu D_{mu,nu} R_nu^T) T_nu|^2

This is a quadratic form in vec(T) (the 12-vector stacking T_0, T_1, T_2, T_3). Write it as:

F_x(Q, T) = vec(T)^T M_12(Q) vec(T)

Construct M_12 symbolically in terms of the 10 SO(3) rotation matrices. Verify numerically that your symbolic formula matches direct computation for 50+ random Q.

### Stage 3: SDP Feasibility Check

For each tested Q:
1. Compute 16I_9 - M_9(Q).
2. Verify it's PSD (all eigenvalues >= 0).
3. Compute the minimum eigenvalue (the "slack").
4. Compute the eigenvalue distribution.

Then: run adversarial gradient ascent on lambda_max(M_9(Q)) over all SO(3)^{10} parameters. Use 50+ random starting points, 200+ iterations each. Report the best adversarial lambda_max found.

### Stage 4: SOS Decomposition Attempt

Try to write 16I_9 - M_9(Q) as a sum of squares in the SO(3) parameters:

16I_9 - M_9(Q) = sum_k G_k(Q)^T G_k(Q)

where each G_k depends on the rotation matrices.

Approaches to try (in order of likelihood):
1. **Direct factorization**: Can you write 16I_9 - M_9 = sum of rank-1 PSD contributions, each visibly >= 0?
2. **Schur complement**: Write M_9 in block form and use Schur complements to certify PSD.
3. **SOS modulo SO(3) constraints**: If R_mu^T R_mu = I is the only constraint, does an SOS proof exist modulo this ideal?

If none of these work, characterize WHY. What's the obstruction? Is it that the dependency on R and D is too nonlinear? Is it that the minimum eigenvalue is too small?

### Stage 5: Epsilon Bound

Even if a full SOS proof fails, try to establish a QUANTITATIVE bound:

lambda_max(M_9(Q)) <= 16 - epsilon

for some epsilon > 0. Use the adversarial results from Stage 3. If the minimum gap is delta > 0, report it as a candidate epsilon. Check whether delta depends on lattice size L.

## Key Formulas

**M_12 at Q=I**: M_12(I) = 16 I_12 - 4(J_4 ⊗ I_3) where J_4 is the 4x4 all-ones matrix. Eigenvalues: {0 (mult 3), 16 (mult 9)}.

**Budget identity**: For T with sum_mu T_mu = 0: 16||T||^2 = 4 sum_{mu<nu} |T_mu - T_nu|^2

**Per-plaquette expansion**: 4|T_mu - T_nu|^2 - |B_{mu,nu}|^2 = 2f(U_{mu,nu}, T_mu) + 2f(W_{mu,nu}, T_nu) - 2 T_mu^T C_{mu,nu} T_nu
where:
- f(R, p) = p^T(I-R)p >= 0 for R in SO(3), p in R^3
- U_{mu,nu} = R_mu D_{mu,nu}, W_{mu,nu} = D_{mu,nu} R_nu^T
- C_{mu,nu} = (I-R_mu) + (I-R_nu^T) + (I-D_{mu,nu}^T) + (I-R_mu D_{mu,nu} R_nu^T)

**The constraint sum_mu T_mu = 0 is ESSENTIAL**: Without it, lambda_max reaches ~21. Any approach MUST use this constraint.

**Cross-link dependence**: Cross-links D_{mu,nu} can INCREASE F_x by up to +28 relative to D=I (cross-link monotonicity fails). But lambda_max(M_9) is bounded by 16 for all tested D.

## Success Criteria

- **Full success**: An SOS decomposition or SDP dual certificate proving 16I_9 - M_9(Q) >= 0 for all SO(3)^{10}.
- **Partial success**: A quantitative epsilon bound, or a clear factorization structure that a follow-up exploration can complete.
- **Failure**: If you can show the SOS approach is fundamentally blocked (e.g., the polynomial degree is too high, or the constraint variety is too complex), that's a useful negative result. State the obstruction precisely.

## Dead Ends (DO NOT REVISIT)

- Full operator inequality M(Q) <= M(I): FALSE (trace invariant forces both signs)
- E006 trace identity for general patterns: FAILS (trace varies by factor ~3)
- Direct reduction to rank-1 T: FAILS (maximizers not always rank-1)
- Cross-link monotonicity: FAILS (can increase F_x by +28)

## Output

Write results to REPORT.md (full details, max 250 lines) and REPORT-SUMMARY.md (concise summary with key numbers) in your working directory. Write incrementally — output after each stage.
