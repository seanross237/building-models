# Exploration 005: Proof Attempt — Cube-Face Inequality for General Q

## Mission Context

We are proving Conjecture 1: lambda_max(M(Q)) <= 16 for all Q in SU(2)^E on the d=4 torus.

The entire proof reduces to a single lemma (established by E001-E004):

**Lemma 5 (Cube-Face Inequality):** For all Q in SU(2)^E, all vertices x, and v_stag = (-1)^{|x|+mu} n:

  F_x(Q) := Sum_{mu<nu} |B_{(x,mu,nu)}(Q, v_stag)|^2  <=  64 |n|^2

where the sum is over the 6 plaquettes based at vertex x.

**Summing over all 16 vertices on L=2 gives:** Sum_sq |B_sq|^2 <= 16 * 64 = 1024 = 4d|v|^2, proving Conjecture 1.

## What's Already Proved

1. **F_x <= 64 for cross-links = I [PROVED]:** When all links NOT incident to vertex x are identity, the formula is:
   F_x = 32 + 8<n, W> - |A|^2
   where W = Sum_mu w_mu, A = Sum_mu s_mu w_mu, w_mu = R_mu^{-1} n, s_mu = (-1)^mu (staggered signs).
   Bound: 8<n,W> <= 32 (triangle inequality, |w_mu| = 1) and -|A|^2 <= 0. So F_x <= 64.

2. **F_x <= 64 for all Q [COMPUTED]:** Zero violations in 160,000 tests. Maximum observed: 48.3 for general Q. Adversarial gradient ascent converges to Q=I.

3. **Cross-links only help:** Max F_x for general Q (48.3) << max for cross-links=I (approaches 64). Cross-links REDUCE the maximum rather than increasing it.

4. **Single-link theorem [COMPUTED]:** For null vectors of P^T R P at single-link configs, each vertex achieves F_x = 64 exactly.

## Dead Ends (DO NOT pursue)
- Per-plaquette bound f_sq <= 0: FALSE (inactive plaquettes have f >= 0)
- Parallelogram pairing: BLOCKED (no canonical pairing exists generically)
- Single-link induction: BLOCKED (no inductive structure)
- Full operator M(Q) <= M(I): IMPOSSIBLE
- Triangle inequality: gives F_x <= 96 (per plaquette |B|^2 <= 16 x 6 = 96), too weak by 3/2

## Corrected B_square Formula (MUST USE THIS)

  B_sq(Q,v) = v_{e1} + Ad_{Q_{e1}}(v_{e2}) - Ad_{Q_{e1}Q_{e2}Q_{e3}^{-1}}(v_{e3}) - Ad_{U_sq}(v_{e4})

Backward edges include OWN link. SZZ conventions: N=2, |A|^2 = -2Tr(A^2).

## Your Specific Goal

**Prove (or make maximal progress toward proving) Lemma 5 for general Q.**

### Stage 1: Setup and Verification (COMPUTE FIRST)

1. Implement F_x(Q) for L=2, d=4 on the staggered mode v = (-1)^{|x|+mu} e_1.
2. Verify F_x(I) = 64 for all 16 vertices.
3. For 10 random Q, compute F_x for all 16 vertices. Verify all <= 64.
4. For a single-link perturbation Q_{e0} = exp(epsilon * tau_1), compute F_x for all 16 vertices. Which vertices achieve F_x = 64?

### Stage 2: Symbolic Expansion of F_x for General Cross-Links

This is the key computation. For a vertex x = 0 (WLOG):

The 6 plaquettes based at x = 0 are in planes (0,1), (0,2), (0,3), (1,2), (1,3), (2,3).

Each plaquette has 4 edges. Of these:
- 2 edges are incident to vertex x (the "base links" Q_{0,mu} and Q_{0,nu})
- 2 edges are NOT incident to vertex x (the "cross-links")

For the staggered mode, the B_sq formula for plaquette (x, mu, nu) involves:
- The base link rotations R_mu = Ad(Q_{0,mu}), R_nu = Ad(Q_{0,nu})
- The cross-link rotations, which appear via partial holonomies

**Step 2a:** For each of the 6 plaquettes, write out the FULL B_sq formula including cross-links, parametrized by all 4 link variables. The staggered signs are known. Write out the effective formula:

  B_{mu,nu} = a_1 n + a_2 R_alpha1(n) + a_3 R_alpha2(n) + a_4 R_alpha3(n)

where a_k in {+1, -1} and R_alpha_k involve products of link variables.

**Step 2b:** Expand F_x = Sum_{mu<nu} |B_{mu,nu}|^2 algebraically. The terms involve:
- |n|^2 (constant): how many?
- <n, R_k(n)> (inner products): these are cos(angle) terms
- <R_j(n), R_k(n)> (cross-products): these depend on relative rotations

**Step 2c:** Simplify using |R_k(n)|^2 = |n|^2 (rotations preserve norm).

**Step 2d:** Factor the cross-link dependence. If F_x can be written as F_x = F_base(R_mu) + G(R_mu, cross-links) where G <= 0 for all cross-links, then F_x <= F_base <= 64 (from the proved case).

### Stage 3: Attempt the Proof

Based on the symbolic expansion from Stage 2:

**Approach A (Cross-link monotonicity):** Show that F_x is maximized when cross-links are identity. Compute dF_x/d(cross-link) at cross-links=I and show it's <= 0 for all base-link configurations. If the function is concave in cross-links (or if the critical point at cross-links=I is always a maximum), this proves Lemma 5.

**Approach B (General formula extension):** Try to extend the formula F_x = 32 + 8<n,W_tilde> - |A_tilde|^2 to general cross-links with modified W_tilde and A_tilde that still satisfy the same bound.

**Approach C (Gauge fixing argument):** At each vertex x, can we gauge away the cross-links? The cube-face sum F_x involves 4 base links and up to 8 cross-links (for 6 plaquettes). Can we choose a gauge transformation at neighboring vertices to set some cross-links to I without changing F_x?

For each approach, verify every intermediate step numerically on at least 50 random Q configs.

### Stage 4: Report

Produce REPORT.md with:
1. Verification table (F_x for all configs)
2. The symbolic expansion of F_x
3. Whether any approach (A, B, or C) succeeds
4. If not, the precise obstruction (which term prevents the bound)
5. The tightest bound achieved for general Q

Produce REPORT-SUMMARY.md (under 80 lines).

## Success Criteria
- A proof of Lemma 5 for general Q, verified numerically on 50+ configs
- OR: A proof that F_x <= C for C < 96 (better than triangle inequality), even if C > 64
- OR: A precise characterization of the obstruction (which cross-link configurations make the bound hardest)

## Failure Criteria
- If the symbolic expansion is too complex to simplify (more than 200 terms with no structure)
- If cross-link monotonicity fails (F_x can increase with cross-link perturbation)

## IMPORTANT NOTES
- Tag every claim: [COMPUTED], [VERIFIED], [PROVED], [CONJECTURED]
- Write results incrementally. After every Python computation, append a 3-line summary to REPORT.md before proceeding.
- You are a math explorer: implement everything in Python, verify numerically, then attempt algebraic proofs.
