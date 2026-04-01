# Exploration 008: Close Gap 1 — Full Eigenspace Bound

## Context

A proof has been established (E006, verified in E007) that for any color direction n in R^3:

  n^T M_total(Q) n <= 64 |n|^2   for all Q

where M_total is the 3x3 per-vertex matrix. This proves lambda_max(M(Q)) <= 16 for the 3D subspace of staggered modes v_{x,mu} = (-1)^{|x|+mu} n (uniform color).

However, the full top eigenspace P of M(I) is 9-DIMENSIONAL. It contains modes where the color direction varies with the lattice direction mu. The adversarial review (E007) identified this as Gap 1: the proof covers 3D of a 9D space.

**YOUR GOAL: Close this gap. Prove lambda_max(M(Q)) <= 16 for ALL directions in P, not just uniform-color staggered modes.**

## What's Known

### The 9D eigenspace P at Q=I

From Fourier analysis: M(I) at momentum k=(pi,...,pi) has the d×d kernel K(k)[mu,nu] = 4d*delta_{mu,nu} - 4 (constant matrix). Eigenvalues of K(k): 4d (multiplicity d-1 = 3) and 0 (multiplicity 1). The eigenvalue-0 mode is the uniform direction (1,1,1,1)/2.

So P at Q=I has dimension (d-1) * (N^2-1) = 3*3 = 9. A basis:

For each color a in {1,2,3} and each spatial mode s in {s1, s2, s3} where s1,s2,s3 are the 3 eigenvectors of K(k) with eigenvalue 4d (perpendicular to (1,1,1,1)):

  v^{a,s}_{x,mu} = (-1)^{|x|} s_mu e_a

Here s is a vector in R^d perpendicular to (1,1,...,1). For d=4, three such vectors are:
  s1 = (1,-1,0,0)/sqrt(2)
  s2 = (1,1,-2,0)/sqrt(6)  
  s3 = (1,1,1,-3)/sqrt(12)

At Q=I, these ALL have eigenvalue 16. The uniform-color staggered mode (-1)^{|x|+mu} n has s_mu = (-1)^mu, which is NOT in the eigenspace of K(k) at eigenvalue 4d. Wait — this needs checking!

Actually: the staggered mode is v_{x,mu} = (-1)^{|x|+mu} n = (-1)^{|x|} * (-1)^mu * n. So s_mu = (-1)^mu = {1, -1, 1, -1}. And (1,-1,1,-1) dot (1,1,1,1) = 0, so s IS perpendicular to (1,1,1,1). So the staggered mode IS one of the 9 eigenvectors (with s = (1,-1,1,-1)/2 and all 3 colors).

So P is spanned by vectors v_{x,mu} = (-1)^{|x|} s_mu e_a where s perp (1,...,1).

### What the cube-face inequality covers

For s_mu = (-1)^mu and fixed color n: F_x(n) = n^T M_total n <= 64|n|^2 (PROVED).

For general s perp (1,...,1): F_x^{(s)}(n) = ? This is a different quadratic form in n, with a DIFFERENT M_total^{(s)} matrix that depends on s.

The question: is M_total^{(s)} <= 64I for ALL s perp (1,...,1)?

### Numerical evidence

E007 found 0 violations of lambda_max(M(Q)) <= 16 in 200 full-matrix tests. This covers all 9 directions of P. Strong numerical support but no proof.

## Your Tasks

### Task 1: Characterize the General Staggered Mode (COMPUTE FIRST)

For L=2, d=4, implement:

a) The staggered Fourier basis: v_{x,mu}^{(s,a)} = (-1)^{|x|} s_mu e_a for s perp (1,1,1,1), a = 1,2,3.

b) Verify that these 9 modes (3 choices of s, 3 choices of a) are ALL in the eigenspace of M(I) with eigenvalue 16.

c) For general s perp (1,...,1), compute v^T M(Q) v for 100 random Q. Verify <= 16|v|^2.

d) Take general w in P: w = Sum_{s,a} alpha_{s,a} v^{(s,a)}. This is a general element of the 9D eigenspace. Compute w^T M(Q) w / |w|^2 for 100 random w and Q. Verify <= 16.

### Task 2: Per-Vertex Decomposition for General Modes

a) For a general staggered mode v_{x,mu} = (-1)^{|x|} s_mu n_a e_a (or more generally, (-1)^{|x|} T_{mu,a} where T is a d x 3 matrix):

Decompose v^T M(Q) v = Sum_x F_x^{(T)}(Q)

Write F_x^{(T)} as a quadratic form in the entries of T.

b) What is the per-vertex matrix M_total^{(T)} now? Is it still 3x3, or does it become larger?

For the staggered mode with pattern s_mu and fixed color n: v_{x,mu} = (-1)^{|x|} s_mu n, so:
  F_x = Sum_{mu<nu} |B_{(x,mu,nu)}|^2

The B-field for this mode uses s_mu, s_nu etc. instead of (-1)^mu, (-1)^nu. The per-vertex matrix M_total depends on the spatial pattern s. 

c) Compute M_total^{(s)} for several choices of s perpendicular to (1,...,1). Check if lambda_max(M_total^{(s)}) <= 64.

d) Check the WORST case: maximize lambda_max(M_total^{(s)}) over all s perp (1,...,1) and all Q. Is it always <= 64?

### Task 3: Color-Direction Coupling

For a general element w of P, the "color direction" varies with the lattice direction: v_{x,mu} = (-1)^{|x|} s_mu n_mu where n_mu depends on mu. This couples color and spatial directions.

a) Decompose v^T M(Q) v for this case. What is the per-vertex contribution?

b) Is the per-vertex quantity a quadratic form in a LARGER matrix (d x 3 = 4 x 3 = 12 parameters)?

c) If so, can the cube-face bound be extended to this larger matrix?

### Task 4: Simplified Approach — Eigenvalue Monotonicity

Maybe there's a simpler approach:

a) Compute the top eigenvalue lambda_max(M(Q)) for 1000 random Q on L=2, d=4. Track which eigenvector achieves it.

b) Is the top eigenvector ALWAYS a uniform-color staggered mode (up to rotation)? If so, the existing proof is sufficient.

c) More precisely: is the top eigenvector always of the form (-1)^{|x|} s_mu n for some fixed n? Or does n vary with mu?

d) If the top eigenvector is always uniform-color at adversarial Q (gradient ascent on lambda_max(M(Q))): run 100 adversarial trials and check.

### Task 5: Spectral Gap Argument

Even if the top eigenvector isn't always uniform-color:

The spectral gap of M(I) is 16 - 14 = 2. If we can show:
  v^T R(Q) v <= 0 for all v in P

then lambda_max(M(Q)) = v^T [M(I) + R(Q)] v <= 16 + 0 = 16.

But v^T R(Q) v = v^T M(Q) v - v^T M(I) v = v^T M(Q) v - 16|v|^2 (for v in P).

So the bound is: v^T M(Q) v <= 16|v|^2 for all v in P — which is exactly what we need.

The cube-face approach gives this for v = (-1)^{|x|+mu} n (uniform color). For v with direction-dependent color, we need a generalization.

a) Compute P^T R(Q) P (9x9 matrix) for 100 random Q. Verify P^T R(Q) P <= 0.
b) Run adversarial gradient ascent on lambda_max(P^T R(Q) P). Does it approach 0?
c) At adversarial Q: is the top eigenvector of P^T R(Q) P always in the uniform-color subspace?

## Corrected B Formula
B_sq(Q,v) = v_{e1} + Ad_{Q_{e1}}(v_{e2}) - Ad_{Q_{e1}Q_{e2}Q_{e3}^{-1}}(v_{e3}) - Ad_{U_sq}(v_{e4})
SZZ conventions: N=2.

## Success Criteria
- Prove v^T M(Q) v <= 16|v|^2 for ALL v in P (covering all 9 dimensions)
- OR: Prove that the top eigenvector of M(Q) is always a uniform-color staggered mode
- OR: Extend the cube-face inequality to handle direction-dependent color

## Failure Criteria
- If direction-dependent modes can exceed 16 (counterexample found)
- If no tractable approach to the full 9D bound

## Output
Write to REPORT.md and REPORT-SUMMARY.md. Tag all claims. Write incrementally.
