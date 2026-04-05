# Exploration 003: SU(2)/SO(3) Representation Theory Bound

## Mission Context

We are trying to prove Conjecture 1 for lattice SU(2) Yang-Mills on the d=4 hypercubic torus (Z/LZ)^4:

  **For all Q in SU(2)^E: lambda_max(M(Q)) <= 4d = 16**

Equivalently: P^T R(Q) P <= 0 for all Q, where P is the 9-dimensional top eigenspace of M(I).

## What's Already Known

- **H_norm <= 1/8** for all Q (PROVED, triangle inequality gives Sum|B_sq|^2 <= 8(d-1)|v|^2 = 24|v|^2)
- **H_norm = 1/12** at Q=I (PROVED). The gap between 24 and 16 is a factor 3/2.
- **Per-plaquette bound is FALSE**: |Sum_k c_k R_k n|^2 can exceed 4|n|^2 for individual plaquettes.
- **Triangle inequality gives 24, not 16**: The Cauchy-Schwarz bound gives per-plaquette max 16, which after summing over all active plaquettes gives lambda <= 24 (not 16). Need structure beyond triangle inequality.
- **Active planes**: Only 4 of 6 orientation classes contribute to staggered mode (mu+nu odd). This is WHY the max is 4d=16 not 4*C(d,2)=24 -- only 2/3 of orientations are active.
- **Saturation characterization**: lambda_max = 4d iff there exists a global n in su(2) fixed by all adjoint transports.
- **Abelian configs**: For abelian Q, the tau_3 block of R(Q) is exactly zero.
- **Weitzenbock**: max lambda[R(Q)|_P] = -W(Q)/12 (exact for single-link), <= -W(Q)/12 for general Q.

### Dead ends (DO NOT revisit): Same 7 as in MISSION.md.

## Corrected B_square Formula (MUST USE THIS)

  B_sq(Q,v) = v_{e1} + Ad_{Q_{e1}}(v_{e2}) - Ad_{Q_{e1}Q_{e2}Q_{e3}^{-1}}(v_{e3}) - Ad_{U_sq}(v_{e4})

where U_sq = Q_{e1}Q_{e2}Q_{e3}^{-1}Q_{e4}^{-1}. SZZ conventions: N=2, |A|^2 = -2Tr(A^2).

## Your Specific Goal

**Study the representation theory of the per-plaquette quantity for the staggered mode v = (-1)^{|x|+mu} n with fixed color direction n in su(2):**

For each plaquette, the staggered mode gives B_sq(Q,v) involving adjoint rotations Ad(P_k) in SO(3) applied to n. The key quantity is:

  f_sq = |B_sq(Q,v_stag)|^2 - |B_sq(I,v_stag)|^2

The target: Sum_sq f_sq <= 0 for all Q.

### Stage 1: Per-Plaquette Geometry (COMPUTE FIRST)

For L=2, d=4:

1. **Compute staggered signs explicitly.** For each of the 96 plaquettes, work out the effective coefficients in B_sq(Q,v_stag). The staggered mode has v_{x,mu} = (-1)^{|x|+mu} n. For a plaquette at vertex x in orientation (mu,nu) with edges e1=(x,mu), e2=(x+mu_hat,nu), e3=(x+nu_hat,mu), e4=(x,nu):

   B_sq(Q,v_stag) = (-1)^{|x|+mu} n + Ad_{Q_{e1}}[(-1)^{|x+mu_hat|+nu} n] - Ad_{Q_{e1}Q_{e2}Q_{e3}^{-1}}[(-1)^{|x+nu_hat|+mu} n] - Ad_{U_sq}[(-1)^{|x|+nu} n]

   Work out the signs (-1)^{...} for each edge carefully. The effective coefficients (c1, c2, -c3, -c4) with staggered signs encode the structure.

2. **Classify sign patterns.** How many distinct effective coefficient patterns appear among the 96 plaquettes? Which come from active orientations (mu+nu odd)?

3. **Per-plaquette maximum (unconstrained).** For each effective coefficient pattern, numerically maximize:
   |c1 n + c2 R1 n + c3 R2 n + c4 R3 n|^2
   over R1, R2, R3 in SO(3) independently (no holonomy constraint). Use gradient ascent with 500 random starts. Record the maximum.

4. **Per-plaquette maximum (constrained).** Add the holonomy constraint R4 = (R1 R2 R3^{-1} R4^{-1}) = Ad(U_sq). This constrains the 4th rotation. Repeat the maximization.

5. **Control check**: At Q=I (all R_k = I), compute f_sq for each plaquette. Verify Sum f_sq = 0.

### Stage 2: Global Constraint Analysis

6. **Shared-edge constraints.** Two plaquettes sharing an edge share partial holonomy rotations. Enumerate how many SO(3) parameters are shared between adjacent plaquettes.

7. **Can worst-case configs be simultaneous?** Take the per-plaquette maximizers from Step 3. For plaquettes sharing an edge, check if their maximizers are compatible (use the same R_k on the shared edge). Quantify the incompatibility.

8. **Forced neighbors.** Fix the worst-case R_k for one plaquette. Compute f_sq for all neighboring plaquettes that share edges. Are the neighbors forced to have f_sq < 0?

### Stage 3: Representation Theory

9. **SO(3) angle decomposition.** For R in SO(3) with rotation angle theta, |Rn - n|^2 = 2|n|^2(1 - cos theta). Use this to express f_sq in terms of rotation angles and relative orientations.

10. **Cross-term structure.** Expand f_sq = Sum_{j,k} c_j c_k |n|^2 [cos(angle between R_j n and R_k n) - 1]. The -1 terms give a negative contribution. The cos terms depend on relative rotations.

    Careful: the B_sq formula has minus signs on edges 3 and 4. The effective coefficients combine the staggered signs with these minus signs. Get this right!

11. **Bound via rotation angles.** Can you bound Sum_sq f_sq in terms of the holonomy rotation angles theta_sq = arccos((Tr(U_sq)-1)/2)? The Weitzenbock formula suggests Sum_sq f_sq ~ -C * Sum_sq (1 - cos theta_sq). Verify this numerically.

12. **Proof attempt.** If the relationship Sum_sq f_sq <= -C * Sum_sq (1 - cos theta_sq) holds, attempt to prove it. This would give R(Q)|_P <= -C * W(Q)/12 and close the conjecture.

### Stage 4: Output

Produce:
- Complete sign pattern classification for L=2, d=4
- Per-plaquette maximum table (unconstrained and constrained)
- Shared-edge analysis
- Algebraic expansion of f_sq in terms of SO(3) quantities
- The relationship between Sum f_sq and Sum(1-cos theta_sq)
- A concrete sub-inequality for the proof (or characterization of why it fails)

## Success Criteria
- A representation-theoretic bound tighter than the triangle inequality (24)
- A concrete relationship between Sum f_sq and the Wilson action density W(Q)
- Identification of the mechanism that prevents simultaneous worst-case

## Failure Criteria
- If no structure beyond triangle inequality emerges
- If the SO(3) analysis provides no path to tighter bounds

## Output Location
Write to REPORT.md and REPORT-SUMMARY.md in this directory. Tag every claim. Write incrementally.
