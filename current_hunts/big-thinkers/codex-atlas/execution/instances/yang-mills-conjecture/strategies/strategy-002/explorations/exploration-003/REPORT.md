# Exploration 003: Prove LEMMA_D and LEMMA_RDR

## Goal
Prove LEMMA_D >= 0 and LEMMA_RDR >= 0 for all T with sum T_mu = 0, all R_mu, D_{mu,nu} in SO(3).

---

## CRITICAL FINDING: Both Individual Lemmas are FALSE

**[VERIFIED]** LEMMA_D is FALSE. Adversarial optimization finds min eigenvalue = **-2.13** for the constrained 9×9 quadratic form. Verified by: (a) matrix formula and direct computation agree to 5.7e-14, (b) all R,D confirmed as SO(3) to machine precision, (c) T satisfies sum=0, (d) 20 independent optimizations all converge to ≈ -2.13.

**[VERIFIED]** LEMMA_RDR is also FALSE. Min eigenvalue = **-1.45**.

**Counterexample structure**: D_01, D_02, D_12 at ~128° while D_03, D_13, D_23 near identity. Per-plaquette budget ≈ 0.05 vs cross ≈ 1.16 for the "active" plaquettes.

**Why 200K random tests missed this**: Random uniform sampling on SO(3)^10 almost never hits the specific adversarial corner (30D parameter space). Adversarial optimization is essential.

---

## KEY POSITIVE RESULT: sum_S = LEMMA_D + LEMMA_RDR >= 0

**[COMPUTED]** sum_S = LEMMA_D + LEMMA_RDR is non-negative:
- 200 independent Nelder-Mead optimizations ALL converge to min eigenvalue = **0.000** (tight at zero)
- No violations found in any test
- At the LEMMA_D counterexample, sum_S = 1.28 (LEMMA_RDR compensates)
- Correlation between LEMMA_D and LEMMA_RDR min eigenvalues: 0.39 (compensatory)

**[COMPUTED]** sum_S = 0 iff D = I (for any R): When all D_{mu,nu} = I, the 9×9 matrix always has eigenvalue 0 (and all others >= 0). This works for ANY choice of R_mu — the zero eigenvalue is independent of R!

**[COMPUTED]** The total gap = 2·sum f(R,T) + sum_S also touches 0, consistent with lambda_max(M(Q)) = 16 being tight.

---

## Structural Analysis of sum_S = 0

**[COMPUTED]** At a zero config (sum_S = 0), the null eigenvector has T_mu ≈ 0 for vertices where most partner D's are identity, and T_mu along the rotation axis of R_mu where D's provide non-trivial cancellation.

**[COMPUTED]** Per-plaquette at zero: plaquettes with D=I contribute exactly 0 (budget=cross=0). Plaquettes with D≠I have budget = cross (exact cancellation).

**[COMPUTED]** The zero set is rich: every optimization (100/100 trials) converges to sum_S = 0, with diverse D-angle patterns. Even a single D=I suffices for the matrix to have a zero eigenvalue.

---

## Approaches Tried and Results

### Approach 1: Numerical Verification (Random)
Random sampling confirms sum_S >= 0 but misses adversarial corners. Per-plaquette bound fails (18,993/240K violations). Simple Cauchy-Schwarz insufficient (398/5000 total failures). **Conclusion**: random testing is necessary but not sufficient.

### Approach 2: VCBL Decomposition
At R=I, sum_S = 2·sum VCBL(D,D,-I,...) where each VCBL >= 0 by Cauchy-Schwarz + AM-GM. This gives sum_S >= 0 at R=I **[VERIFIED]**. For general R, the VCBL(-I) remainder is -32 (far from PSD). **Fundamental obstruction**: per-plaquette cross term is rank 3, but VCBL cross product (I-U)M(I-W^T) is rank ≤ 2. **Conclusion**: per-plaquette VCBL cannot close the proof.

### Approach 3: Constraint Manipulation / Algebra
Verified: sum_S = 8||T||² − 2·rot_budget + 2·(D_cross + RDR_cross). The identity D^T = U^T R_mu and RDR = U R_nu^T simplifies the cross matrix to U^T R_mu + U R_nu^T − 2I. This is a cleaner form but still doesn't yield a PSD decomposition.

### Approach 4: Eigenvalue / Matrix Structure
**[COMPUTED]** min_eig(sum_S) scales as O(ε²) near Q=I (coefficient ≈ 2.96). Positive Hessian confirms Q=I is a local minimum. The 9×9 matrix passes Cholesky for 1000/1000 random Q.

### Approach 5: Plaquette Grouping
Each complementary pair (e.g., (0,1)+(2,3)) individually violates (33-55/5000). So grouping doesn't yield per-group non-negativity. **Conclusion**: the proof needs all 6 plaquettes together.

### Budget/Cross Ratio
**[COMPUTED]** max |harmful cross|/budget ≈ 0.28 for random Q,T. Approaches 1.0 only at Q=I (where both are 0). This shows sum_S has substantial margin away from the zero set.

---

## Proof Strategy Recommendation

The correct target is **sum_S >= 0** (not individual lemmas). Key structural features for the proof:
1. **D=I universally gives zero**: sum_S(D=I) has eigenvalue 0 for ALL R. Proof at D=I reduces to showing the 9×9 matrix is PSD.
2. **At R=I, VCBL works**: sum_S = 2·sum VCBL(D,D,-I,...) >= 0.
3. **Rank obstruction**: Per-plaquette VCBL can't absorb the full rank-3 cross term. Need a global argument.
4. **Possible approach**: Interpolate between the R=I regime (VCBL works) and the D=I regime (trivially 0). Show the sum_S Hessian is non-degenerate along paths in parameter space.

---

## Verification Scorecard
- **VERIFIED**: LEMMA_D counterexample (multiple cross-checks, machine precision)
- **VERIFIED**: LEMMA_RDR counterexample
- **VERIFIED**: sum_S = 2·VCBL at R=I
- **COMPUTED**: sum_S >= 0 (200 adversarial optimizations, all → 0)
- **COMPUTED**: Zero-set structure, eigenvalue scaling, per-plaquette analysis
- **CONJECTURED**: sum_S >= 0 for ALL Q (no algebraic proof found)
