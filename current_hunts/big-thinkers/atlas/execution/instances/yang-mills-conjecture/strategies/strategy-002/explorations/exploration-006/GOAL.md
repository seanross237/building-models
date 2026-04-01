# Exploration 006: Adversarial Review of Complete Proof

## Mission Context

We claim to have a complete proof that lambda_max(M(Q)) <= 16 for all Q in SU(2)^E on the d=4, even-L hypercubic torus. This would give H_norm <= 1/12 and mass gap at beta < 1/4.

Your job: TRY TO BREAK THIS PROOF. Find gaps, errors, unjustified steps, or counterexamples.

## The Complete Proof Chain

### Part A: Uniform-Color Bound (Strategy 001, E006)
For v = (-1)^{|x|+mu} n (uniform color n), the per-vertex bound:
n^T M_total n <= 64|n|^2

**Proof (5 steps):**
1. Trace identity: c + Tr(P) = 64 (from 28 positive, 8 negative cross-terms, net 20)
2. Equivalence: lambda_max(M_total) <= 64 iff lambda_max(P) <= Tr(P)
3. Expansion: 64I - M_total = 2[group_02 + group_13 + group_active]
4. Combined Bound Lemma: f(A)+f(B)+f(AD)+f(DB^T)-f(D)-f(ADB^T) >= 0
   Proof: LHS = n^T(I-A)D(I-B^T)n + f(A) + f(B), then C-S + AM-GM
5. Assembly: all three groups >= 0

This was adversarial-reviewed in Strategy 001 E007 and given CONDITIONAL PASS (core correct, two gaps: full eigenspace + odd L).

### Part B: Full 9D Eigenspace Extension (Strategy 002, E001-E005)
For general staggered mode v_{x,mu} = (-1)^{|x|+mu} T_mu with sum T_mu = 0:

**Step B1** (Budget identity [PROVED]):
16||T||^2 = 4 sum_{mu<nu} |T_mu - T_nu|^2 (for T with sum T_mu = 0)

**Step B2** (Per-plaquette identity [VERIFIED to 1e-13]):
4|T_mu - T_nu|^2 - |B_{mu,nu}|^2 = 2f(U,T_mu) + 2f(W,T_nu) - 2 T_mu^T C T_nu
where U = R_mu D, W = D R_nu^T, C = (I-R_mu)+(I-R_nu^T)+(I-D^T)+(I-R_mu D R_nu^T)

**Step B3** (Sum-to-zero extraction [VERIFIED to 5.7e-14]):
16||T||^2 - F_x = 2*sum f(R_mu, T_mu) + sum_S

**Step B4** (D=I base case [PROVED]):
sum_S(D=I) = 6*sum f(R_mu, T_mu) + |sum R_mu^T T_mu|^2 >= 0

**Step B5** (Delta factoring [VERIFIED to 7.1e-14]):
sum_S = baseline + sum_{mu<nu} 2 u^T (I-D) v
where baseline = 6*sum f + |sum R^T T|^2, u = R_mu^T T_mu - T_nu, v = T_mu - R_nu^T T_nu

**Step B6** (M9 is affine in D [VERIFIED to 3.5e-15]):
M_9(R, D) is an affine function of D

**Step B7** (Cauchy-Schwarz contraction [PROVED]):
u^T Dv <= ||u||*||v|| for D in SO(3)
=> u^T(I-D)v >= u*v - ||u||*||v||
=> sum_S >= F(R,T) = baseline - sum 2(||u||*||v|| - u*v)

**Step B8** (Key computation [VERIFIED to 1.1e-13]):
sum_{mu<nu} ||u-v||^2 = 4*sum f(R_mu, T_mu) + |sum R_mu^T T_mu|^2

**Step B9** (Cancellation [PROVED]):
F = 6*sum f + |sum a|^2 - (4*sum f + |sum a|^2) + sum(||u||-||v||)^2
= 2*sum f(R_mu, T_mu) + sum(||u||-||v||)^2 >= 0

**Conclusion**: F_x(Q,T) <= 16||T||^2 for all T in V, all Q.

### Part C: Upstream Connection
- F_x <= 16||T||^2 for all vertices x => sum_x F_x <= 16*L^d*||T||^2 = 16*|v|^2
- sum_x F_x = sum_plaq |B_plaq|^2 = v^T M(Q) v
- So v^T M(Q) v <= 16|v|^2 for all v in P (top eigenspace of M(I))
- Since M(I) has eigenvalue 16 on P: v^T[M(Q) - M(I)]v <= 0 for v in P
- Therefore lambda_max(M(Q)) <= lambda_max(M(I)) = 16
- H_norm = lambda_max/(12*4) = 16/48 = 1/3... WAIT.

Actually check the normalization! H_norm = beta/(2N) * max_Q lambda_max(M(Q)). And SZZ requires H_norm < 1. If lambda_max <= 16 = 4d, then H_norm = beta/(2N) * 4d = beta * 2d/N = beta * 4 (for d=4, N=2). So H_norm < 1 iff beta < 1/4. CHECK THIS!

## Your Task

### Stage 1: Independent Verification of All Identities

Independently implement and verify every claimed identity (Steps B1-B9). Use 500+ random configurations. Do NOT copy code from prior explorations — write everything from scratch.

For each step, compute:
- The LHS
- The RHS
- The difference (should be < 1e-10)
- The minimum value (when a >= 0 is claimed)

### Stage 2: Adversarial Attack

For each step, try to find a COUNTEREXAMPLE:
1. Random SO(3) configs (1000+)
2. Extreme configs: D = -I (180-degree rotation), R = -I, D and R commuting, D and R anti-commuting
3. Degenerate T: T_mu all parallel, T_mu all perpendicular, T_3 = -(T_0+T_1+T_2) with T_0, T_1, T_2 nearly equal
4. Gradient ascent on the violation: maximize LHS - RHS (should stay <= 0)

### Stage 3: Check the Upstream Connection

Verify the normalization chain:
1. Does F_x <= 16||T||^2 for ALL x actually imply v^T M(Q) v <= 16|v|^2 for v in P?
   - Check: is there double-counting? Each plaquette belongs to TWO vertices.
   - The per-vertex F_x sums ALL 6 plaquettes at vertex x. The global sum v^T M(Q)v = sum_plaq |B|^2. If each plaquette is counted once per vertex it touches, the per-vertex sum is NOT the global sum divided by #vertices.
   - THIS IS THE MOST LIKELY ERROR. Check it carefully.

2. Does v^T M(Q) v <= 16|v|^2 for v in P imply lambda_max(M(Q)) <= 16?
   - Yes, by definition: lambda_max = max_{v in P, |v|=1} v^T M v.
   - But check: is P the TOP eigenspace? Does the bound on P suffice?

3. Does lambda_max(M(Q)) <= 16 imply H_norm <= 1/12?
   - SZZ Theorem 1.3 uses H_norm = max_Q ||nabla^2 S(Q) + 4 beta/N * I||. Check the exact formula.

### Stage 4: Check Strategy 001 Gaps

Strategy 001 E007 identified Gap 2: odd L sign structures differ. Is the Strategy 002 proof valid for odd L? The B-field formula and staggered mode definition should be checked for odd L.

### Stage 5: Stress Test at L=4

If possible, construct the FULL 192x192 matrix M(Q) for a small lattice (L=2, d=4), compute lambda_max, and verify it's <= 16. Do this for 200+ random Q including adversarial gradient ascent.

## Success Criteria

- **PASS**: All identities verified, no counterexamples found, upstream connection confirmed.
- **CONDITIONAL PASS**: All identities verified, but upstream connection has a quantitative issue (e.g., double-counting factor).
- **FAIL**: A counterexample found to any step, OR the upstream connection is wrong.

## Output

Write REPORT.md (max 250 lines) and REPORT-SUMMARY.md. For each step, report: VERIFIED / FAILED / CONDITIONAL with evidence.
