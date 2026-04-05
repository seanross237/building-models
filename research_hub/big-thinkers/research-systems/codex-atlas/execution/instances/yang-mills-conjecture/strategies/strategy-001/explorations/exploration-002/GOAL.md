# Exploration 002: Per-Plaquette Contribution Structure

## Mission Context

We are trying to prove Conjecture 1 for lattice SU(2) Yang-Mills on the d=4 hypercubic torus (Z/LZ)^4:

  **For all Q in SU(2)^E: lambda_max(M(Q)) <= 4d = 16**

Equivalently: for v in P (top eigenspace of M(I), dim 9, staggered modes):
  v^T R(Q) v <= 0 for all Q

where R(Q) = M(Q) - M(I).

## What's Already Known

- **H_norm <= 1/8** for all Q (PROVED, triangle inequality)
- **H_norm = 1/12** at Q=I (PROVED, Fourier). Staggered modes v_{x,mu} = (-1)^{|x|+mu} e_a.
- **Per-plaquette bound is FALSE**: |B_sq(Q,v)|^2 <= 4|v|^2 fails for individual plaquettes (ratios up to 8383x). BUT the GLOBAL SUM Sum_sq |B_sq(Q,v)|^2 <= 4d|v|^2 holds for all 500+ tested configs.
- **Per-plaquette M_sq eigenvalues**: Each M_sq = B_sq^T B_sq has eigenvalues {4,4,4,0,...,0} for ALL Q. This is an algebraic invariant.
- **Active planes**: For staggered modes, only orientations with mu+nu odd contribute (4 of 6 for d=4). This explains 4d not 6d.
- **Weitzenbock**: max lambda[R(Q)|_P] = -W(Q)/12 for single-link (exact); <= -W(Q)/12 for general Q (42/42).
- **Gradient ascent on P^T R P**: plateaus at -8 to -11, far from 0.
- **Staggered single-link bound PROVED**: For Q differing from I on one link by angle epsilon, Delta = 14(cos(epsilon) - 1) <= 0. Two affected plaquettes contribute (10 + 6cos(epsilon)) and (8 + 8cos(epsilon)), summing to 18 + 14cos(epsilon) vs. 32 at Q=I.

### Dead ends (DO NOT revisit):
1. Full operator M(Q) <= M(I) -- IMPOSSIBLE
2. Global geodesic concavity -- FAILS
3. Per-plaquette factoring -- FALSE
4. Coulomb gauge -- Gribov
5. Jiang F <= 0 -- no sign
6. Schur/Haar -- average != max
7. Triangle inequality -- caps at 1/8

## Corrected B_square Formula (MUST USE THIS)

  B_sq(Q,v) = v_{e1} + Ad_{Q_{e1}}(v_{e2}) - Ad_{Q_{e1}Q_{e2}Q_{e3}^{-1}}(v_{e3}) - Ad_{U_sq}(v_{e4})

where U_sq = Q_{e1}Q_{e2}Q_{e3}^{-1}Q_{e4}^{-1}. Backward edges include their OWN link. SZZ conventions: N=2, |A|^2 = -2Tr(A^2).

## Your Specific Goal

**For v in the staggered eigenspace P, decompose v^T R(Q) v = Sum_sq f_sq(Q) into per-plaquette contributions. Map which plaquettes contribute positively and negatively. Find cancellation patterns and natural groupings.**

### Stage 1: Compute Per-Plaquette Contributions (COMPUTE FIRST)

For L=2, d=4:

1. Generate 50 random SU(2) configs (Haar-distributed on each edge). For each config Q and each of the 96 plaquettes, compute:
   - f_sq(Q) = |B_sq(Q,v_stag)|^2 - |B_sq(I,v_stag)|^2
   where v_stag = (-1)^{|x|+mu} e_1 (staggered mode with color direction e_1)

2. Tabulate: for each plaquette, record its orientation (mu,nu), vertex position x, whether it's active (mu+nu odd), and f_sq averaged over the 50 configs.

3. **Sanity check**: Sum_sq f_sq(Q) should equal v_stag^T R(Q) v_stag for each config. Verify this to machine precision.

4. **Control check**: At Q=I, f_sq = 0 for all plaquettes.

### Stage 2: Map the Contribution Pattern

5. **Active vs inactive**: Verify that inactive plaquettes (mu+nu even) contribute f_sq = 0 for the staggered mode at ALL Q (not just Q=I). If so, the problem reduces to summing over only the 4*L^d = 64 active plaquettes.

6. **Sign pattern**: For each config Q, count how many active plaquettes have f_sq > 0 (bad) and f_sq < 0 (good). What fraction of plaquettes are "bad"? Is the bad fraction small, or are many plaquettes bad but the bad contributions are small?

7. **Magnitude distribution**: Compute the distribution of |f_sq| values. Are the positive contributions uniformly distributed, or concentrated on a few plaquettes? Is there a heavy tail?

8. **Worst-case plaquettes**: Which plaquettes (by position/orientation) most consistently have the largest positive f_sq? Is there a spatial/orientation pattern?

### Stage 3: Find Cancellation Patterns

9. **Edge-sharing pairs**: Two plaquettes sharing an edge have correlated partial holonomies. For each pair of active plaquettes sharing an edge, compute f_sq1 + f_sq2 across 50 configs. Is the sum manifestly <= 0 for any natural pairing?

10. **Vertex stars**: For each vertex x, the "star" is the set of all plaquettes containing x. Compute Sum_{sq in star(x)} f_sq(Q) for each vertex and config. Is the vertex-star sum <= 0?

11. **Link stars**: For each link e, compute Sum_{sq containing e} f_sq(Q). Each link appears in 2(d-1) = 6 plaquettes. Is the link-star sum <= 0?

12. **Orientation classes**: Group all plaquettes by orientation (mu,nu). For each orientation class, compute the class sum. Is there a natural grouping of orientation classes that sums to <= 0?

13. **Algebraic structure of cancellation**: For the groupings that come closest to being manifestly <= 0, write out the algebraic structure. What property of the group forces cancellation?

### Stage 4: Worst-Case Analysis

14. **Gradient ascent**: Maximize Sum_sq f_sq(Q) over Q (equivalently, maximize v_stag^T R(Q) v_stag). Start from 10 different random configs. Track the per-plaquette contributions at the gradient-ascent endpoint.

15. **Near-worst configs**: At the gradient ascent endpoint, characterize the per-plaquette contribution pattern. Which plaquettes are positive? Which groupings show the least cancellation?

### Stage 5: Output

Produce:
- Per-plaquette contribution statistics for 50+ configs
- The active/inactive split verification
- Results for each grouping type (edge-pair, vertex-star, link-star, orientation class)
- The algebraic structure of the best cancellation pattern
- Gradient ascent results showing the worst-case per-plaquette pattern

State clearly:
- Whether any natural grouping gives manifestly <= 0 contributions
- The best sub-inequality you found (even if it doesn't close the full proof)
- What would need to be proved to convert the cancellation pattern into a proof

## Success Criteria
- Identification of a natural grouping (vertex-star, link-star, or other) where each group's contribution is <= 0 for all tested configs
- A concrete algebraic identity or inequality that explains the cancellation
- Clear statement of what remains to prove

## Failure Criteria
- If no natural grouping gives consistently <= 0 contributions (even the global sum)
- If the per-plaquette picture provides no insight beyond "they all cancel in the sum somehow"

## Output Location
Write to REPORT.md and REPORT-SUMMARY.md in this directory. Tag every claim. Write incrementally.
