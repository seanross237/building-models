# Exploration 006: Prove lambda_max(M_total) <= 64 via 3x3 Matrix Analysis

## Mission Context

We are proving Conjecture 1: lambda_max(M(Q)) <= 16 for all Q in SU(2)^E on the d=4 torus.

The proof has been reduced to a SINGLE LEMMA through 5 prior explorations:

**Lemma 5 (Cube-Face Inequality):** For all vertices x and all Q:
  F_x(Q) := Sum_{mu<nu} |B_{(x,mu,nu)}(Q, v_stag)|^2 <= 64 |n|^2

**KEY REFORMULATION (from E005):** F_x = n^T M_total n where M_total is a 3x3 positive semidefinite matrix. Therefore:

  F_x <= 64 |n|^2   iff   lambda_max(M_total) <= 64

## What's Known About M_total

M_total is the sum of 6 rank-3 PSD matrices (one per plaquette orientation):
  M_total = Sum_{mu<nu} A_{mu,nu}^T A_{mu,nu}

where A_{mu,nu} is a 4x3 or 3x3 matrix encoding the plaquette's B-field contribution.

For vertex x=0 (WLOG by translation symmetry), the 6 plaquettes in planes (0,1), (0,2), (0,3), (1,2), (1,3), (2,3) involve:
- 4 "base link" rotations R_0, R_1, R_2, R_3 in SO(3) — from the 4 edges incident to x
- Cross-link rotations from edges NOT incident to x (these enter through partial holonomies)

### Known properties:
- At Q=I: M_total = 64*I_3 (all eigenvalues = 64) [VERIFIED]
- Tr(M_total) ranges 40-128 for random Q, max 192 at Q=I [COMPUTED]
- lambda_max(M_total): max observed 56.9 for random Q, 64.000 for adversarial [COMPUTED]
- Cross-link monotonicity FAILS: cross-links can increase F_x by +28 [COMPUTED]
- Adversarial gradient ascent: ALL 30 trials converge to lambda_max = 64.000 exactly [COMPUTED]

### Staggered sign structure:
The staggered mode v = (-1)^{|x|+mu} n gives signs on the 4 edges of each plaquette. For d=4:
- Active planes (mu+nu odd): contribute to the Q=I maximum. Signs: all same sign (+1,+1,+1,+1) or (-1,-1,-1,-1) depending on vertex.
- Inactive planes (mu+nu even): zero contribution at Q=I. Signs: alternating pattern.

## Your Specific Goal

**Prove lambda_max(M_total) <= 64 for all admissible R_mu, D_cross in SO(3).**

Focus on ONE approach and go DEEP. Do not attempt multiple approaches superficially.

### The Recommended Approach: Characteristic Function Bound

1. **Compute M_total explicitly.** For vertex x=0 with d=4, L=2: Write each A_{mu,nu} matrix in terms of the SO(3) rotations (R_0, R_1, R_2, R_3 for base links, and cross-link rotations D). The staggered signs are fixed by the lattice.

2. **Compute Tr(M_total), Tr(M_total^2), det(M_total) symbolically.** These are the elementary symmetric polynomials of the eigenvalues. If we can show:
   - Tr(M_total) <= 192 (= 3*64, already verified)
   - Tr(M_total^2) is related to Tr(M_total) in a way that forces lambda_max <= 64
   - Or: det(M_total) >= some function that prevents lambda_max from exceeding 64

3. **Alternative: Trace-off-diagonal bound.** Write M_total = diagonal + off-diagonal. The diagonal elements are sums of |R_k n_a|^2 terms (always <= 4 per plaquette). The off-diagonal elements are sums of <R_j n_a, R_k n_b> cross terms. If the off-diagonal is "small enough" relative to the diagonal, Gershgorin circles bound lambda_max.

4. **Alternative: Direct expansion.** Compute M_total as a function of R_mu in SO(3). Each entry (M_total)_{ab} is a sum of products like <sigma_a, R_j sigma_b> where sigma_a are Pauli matrices. These are Wigner D-matrix elements. Can you use representation theory of SO(3) to bound the eigenvalues?

### Stage 1: Compute (COMPUTE FIRST)

For L=2, d=4, implement M_total(R_0, R_1, R_2, R_3, D_cross) as a 3x3 matrix.

a) Verify: M_total(I,I,I,I,I) = 64*I_3
b) For 100 random configs, verify lambda_max(M_total) <= 64
c) For 30 adversarial configs (gradient ascent on lambda_max), verify all converge to 64.000

d) At the adversarial maximum configs: what is M_total? Is it always diagonal? What are the other eigenvalues?
e) Compute Tr(M_total), Tr(M_total^2), det(M_total) for the 100 random configs. Tabulate statistics.
f) CRITICAL: At configs where lambda_max = 64 exactly, what constraints do the rotations satisfy? Are the base links R_mu aligned with some direction? Is there a "fixed color" condition?

### Stage 2: Analyze the 64-saturation manifold

g) Characterize all configs where lambda_max = 64: systematically search for configs achieving lambda_max = 64 ± 0.001. Sample 1000 of them. What do they have in common?

h) From E001: single-link configs give lambda_max = 64 exactly. From the saturation characterization: lambda_max = 4d iff there exists a global direction n fixed by all adjoint transports. How does this condition translate to the 3x3 matrix M_total?

i) Hypothesis: lambda_max(M_total) = 64 iff there exists n in R^3 with M_total*n = 64*n, iff the rotations R_mu, D satisfy some alignment condition. Check this.

### Stage 3: Prove the bound

j) Based on the structure found in Stages 1-2, attempt to prove lambda_max(M_total) <= 64.

The most promising route depends on what you find:
- If M_total is always diagonally dominant: use Gershgorin
- If Tr(M_total) <= 192 and lambda_max can't concentrate: use trace + convexity
- If the saturation manifold has a clean algebraic characterization: prove by analyzing critical points

k) For ANY claimed proof step, verify numerically on at least 50 configs.

### Stage 4: Report

Write REPORT.md with:
1. The explicit formula for M_total
2. Statistics table (Tr, Tr^2, det, lambda_max, lambda_min)
3. Characterization of 64-saturation manifold
4. Proof attempt (or precise obstruction)

## Dead Ends Specific to This Problem
- Cross-link monotonicity FAILS (F_x can increase with cross-links)
- Per-plaquette bound: each A^T A has lambda_max = 16, but 6*16 = 96 >> 64 (too loose)
- Trace bound: Tr = 192 at Q=I, 192/3 = 64 only works if M ∝ I (which it isn't generically)

## Corrected B Formula
  B_sq(Q,v) = v_{e1} + Ad_{Q_{e1}}(v_{e2}) - Ad_{Q_{e1}Q_{e2}Q_{e3}^{-1}}(v_{e3}) - Ad_{U_sq}(v_{e4})
Backward edges include OWN link. SZZ conventions: N=2.

## Success Criteria
- A proof that lambda_max(M_total) <= 64 for all SO(3) rotations, verified on 50+ configs
- OR: The complete explicit formula for M_total with a clear characterization of the saturation manifold
- OR: A bound lambda_max(M_total) <= C < 96 (improving on naive per-plaquette bound)

## Failure Criteria
- If the 3×3 matrix has no tractable structure (entries involve too many cross terms)
- If the saturation manifold has no clean characterization

## Output
Write to REPORT.md and REPORT-SUMMARY.md. Tag all claims. Write incrementally.
