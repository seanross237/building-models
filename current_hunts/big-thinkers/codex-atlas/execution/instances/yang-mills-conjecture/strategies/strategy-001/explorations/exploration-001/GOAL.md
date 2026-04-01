# Exploration 001: Maximal Tree Gauge Decomposition

## Mission Context

We are trying to prove Conjecture 1 for lattice SU(2) Yang-Mills on the d=4 hypercubic torus (Z/LZ)^4:

  **For all Q in SU(2)^E: lambda_max(M(Q)) <= 4d = 16**

Equivalently: P^T R(Q) P <= 0 for all Q, where P is the 9-dimensional top eigenspace of M(I) (spanned by staggered modes v_{x,mu} = (-1)^{|x|+mu} e_a for a=1,2,3), and R(Q) = M(Q) - M(I).

This would give H_norm <= 1/12 for all Q, hence mass gap at beta < 1/4 (12x improvement over SZZ 2023).

## What's Already Known

- **H_norm <= 1/8** for all Q (PROVED, triangle inequality -> beta < 1/6)
- **H_norm = 1/12** at Q=I (PROVED, Fourier analysis of M(I))
- **Pure gauge**: M(Q_pure) = Ad_G^T M(I) Ad_G (isospectral, PROVED)
- **Trace invariant**: Tr(M(Q)) = const for all Q (PROVED) -> full operator inequality M(Q) <= M(I) is IMPOSSIBLE
- **Conjecture verified**: 500+ configs including adversarial gradient ascent, zero violations
- **Weitzenbock formula**: max lambda[R(Q)|_P] = -W(Q)/12 (exact for single-link, R^2=1.0; <= -W(Q)/12 for all 42 tested general Q)
- **Per-plaquette bound is FALSE**: Per-plaquette |B_sq(Q,v)|^2 <= 4|v_local|^2 is false for Q!=I (ratios up to 8383x). The proof requires GLOBAL lattice structure.
- **Gradient ascent on P^T R P** stays at -8 to -11, far from 0.

### Dead ends (DO NOT revisit):
1. Full operator M(Q) <= M(I) -- IMPOSSIBLE (Tr(R)=0)
2. Global geodesic concavity -- FAILS at Q!=I
3. Per-plaquette factoring -- FALSE
4. Coulomb gauge -- Gribov problem
5. Jiang Weitzenbock F <= 0 -- no sign proved in general
6. Schur/Haar average -- average != maximum
7. Triangle inequality refinement -- caps at 1/8, structurally can't reach 1/12

## Corrected B_square Formula (MUST USE THIS)

SZZ conventions: S = -(beta/N) Sum_sq Re Tr(U_sq), |A|^2 = -2Tr(A^2), N=2.

For plaquette sq with edges e1, e2, e3, e4 (ordered: forward, forward, backward, backward):

  B_sq(Q,v) = v_{e1} + Ad_{Q_{e1}}(v_{e2}) - Ad_{Q_{e1}Q_{e2}Q_{e3}^{-1}}(v_{e3}) - Ad_{U_sq}(v_{e4})

where U_sq = Q_{e1}Q_{e2}Q_{e3}^{-1}Q_{e4}^{-1}. Backward edges include their OWN link in the partial holonomy. At Q=I both the corrected and uncorrected formulas coincide.

M(Q) = Sum_sq B_sq(Q,.)^T B_sq(Q,.) is the Gram operator. R(Q) = M(Q) - M(I).

## Your Specific Goal

**Fix a maximal spanning tree T of the L^4 hypercubic torus to identity (set all links on T to I via gauge transformation). Study P^T R(Q) P in this reduced gauge.**

### Stage 1: Setup and Verification (COMPUTE FIRST)

For L=2, d=4:
1. Construct the hypercubic torus graph. Count vertices (L^d = 16), edges (d*L^d = 64), plaquettes (d(d-1)/2 * L^d = 96).
2. Find a maximal spanning tree T. Count tree edges (L^d - 1 = 15) and non-tree edges (64 - 15 = 49). These 49 links are the "cocycle" links -- the free variables after gauge fixing.
3. Generate 20 random SU(2) configs Q on all 64 edges. For each:
   a. Gauge-transform to maximal tree gauge (set all tree links to I)
   b. Verify that M(Q) is unchanged (gauge covariance)
   c. Compute lambda_max(M(Q)) and verify it equals the pre-gauge-fix value
   d. Compute P^T R(Q) P (9x9 matrix) and verify it's <= 0

### Stage 2: Decomposition

In maximal tree gauge, every plaquette's holonomy U_sq involves only non-tree links (at most 4 per plaquette, many have fewer). The partial holonomies P_k in B_sq also simplify.

4. For each of the 96 plaquettes on L=2, classify by how many non-tree links they contain (0, 1, 2, 3, or 4). How does this distribution look?
5. For the staggered mode v = (-1)^{|x|+mu} e_a, compute the per-plaquette contribution f_sq(Q) = |B_sq(Q,v)|^2 - |B_sq(I,v)|^2 in maximal tree gauge. This is the R(Q) contribution from each plaquette.
6. Write out the algebraic form of P^T R(Q) P as a function of only the 49 non-tree SU(2) elements. How many effective real degrees of freedom? (49 x 3 = 147 real parameters)

### Stage 3: Tractability Assessment

7. In maximal tree gauge, many plaquettes have simplified structure (fewer non-trivial links). For plaquettes with only 1 non-tree link, write the explicit formula for f_sq(Q) and attempt to bound it.
8. For plaquettes with 2+ non-tree links, characterize the algebraic structure of f_sq.
9. Can you group plaquettes in a way that makes each group's contribution manifestly <= 0? (e.g., pairs sharing a non-tree link, stars around a non-tree link)
10. What is the WORST-CASE configuration among the 49 non-tree links? Use gradient ascent on P^T R(Q) P restricted to maximal tree gauge. Does it find configs closer to the bound than the full-space gradient ascent (which plateaus at -8 to -11)?

### Stage 4: Output

Produce a computational verification table with columns: config_id, lambda_max(M(Q)), max_eigenvalue(P^T R(Q) P), W(Q).

State clearly:
- The algebraic decomposition of P^T R(Q) P in maximal tree gauge
- The distribution of plaquettes by # of non-tree links
- Whether any sub-inequality suffices for a proof
- What the obstruction is if no tractable bound emerges

## Success Criteria
- A clear algebraic expression for P^T R(Q) P in maximal tree gauge as a function of 49 SU(2) variables
- Computational verification table for >= 20 configs
- Identification of which plaquette groups are tractable and which aren't
- A concrete sub-inequality that would suffice for the proof, OR a clear characterization of why the approach fails

## Failure Criteria
- If maximal tree gauge doesn't simplify the structure enough to suggest any bound strategy (all plaquettes equally complex in this gauge)
- If gradient ascent in tree gauge finds configs with P^T R(Q) P eigenvalue > -2 (approaching the bound)

## Output Location
Write your report to REPORT.md in this directory. Write a concise summary to REPORT-SUMMARY.md. Tag every claim as [PROVED], [COMPUTED], [CHECKED], or [CONJECTURED]. Write derivations incrementally -- output each step to file as you complete it.
