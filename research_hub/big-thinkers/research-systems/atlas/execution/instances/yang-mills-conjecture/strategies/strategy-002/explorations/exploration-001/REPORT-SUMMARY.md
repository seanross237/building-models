# Exploration 001 — Report Summary

**Goal:** SDP/SOS certificate for 9D eigenspace bound: lambda_max(M_9(Q)) <= 16 for all Q in SO(3)^{10}

---

## Outcome: Partial Success

The bound was numerically confirmed at large scale. A structural decomposition certificate was derived and verified. Full algebraic SOS proof was not achieved, but the proof gap was precisely characterized.

---

## What Was Tried

1. **Numerical verification** (1000 + 5000 random SO(3)^{10} configs, plus adversarial search)
2. **M_12 formula construction and verification** (200 random configs)
3. **SDP feasibility check** (200 configs, slack matrix positivity)
4. **Riemannian gradient ascent** (50 starts × 200 steps)
5. **Per-plaquette SOS attempt** — tested and ruled out
6. **Algebraic identity exploration** — found key identity and decomposition formula
7. **Epsilon bound and near-identity rate analysis**

---

## Key Results

**[VERIFIED]** M_12(I) = 16 I_12 - 4(J_4 ⊗ I_3), eigenvalues {0(×3), 16(×9)}

**[COMPUTED]** Bound lambda_max(M_9(Q)) <= 16 holds for 16,000+ tested configurations. Max found: **15.637** (adversarial gradient ascent).

**[VERIFIED]** Bound is **tight at Q=I**: lambda_max = 16.0000000000 exactly.

**[COMPUTED]** Per-plaquette bound FAILS: single-plaquette block lambda_max = **8** at Q=I (budget is 4). The constraint sum T_mu = 0 is *essential* and cannot be avoided.

**[VERIFIED]** Key algebraic identity (error 7e-15):
> sum_{mu<nu} T_mu^T [(I-R_mu) + (I-R_nu^T)] T_nu = -sum_mu f(R_mu, T_mu)

**[COMPUTED]** Exact decomposition formula (error 7e-14):
> 16||T||^2 - F_x = f_same + 2·f_R - Term_C - Term_D

where f_same, f_R >= 0 are sums of f(R,p) = p^T(I-R)p >= 0 terms.
This formula holds with 0 violations over 20,000 test cases.

**[COMPUTED]** Near Q=I, gap ~ O(||Q-I||^2) with log-log slope **1.94**.

**[VERIFIED]** No uniform epsilon > 0: lambda_max(Q=I) = 16 exactly (infimum of gap = 0).

---

## Verification Scorecard

| Tier | Count |
|------|-------|
| VERIFIED (formula/identity proofs) | 5 |
| COMPUTED (reproducible numerical) | 9 |
| CONJECTURED | 0 |

---

## Key Takeaway

The 9D bound holds in all tests, but a full SOS certificate is not achieved. The critical structural finding is the **decomposition formula**: 16||T||^2 - F_x = f_same + 2 f_R - C - D, where the constraint sum T_mu = 0 converts the cross terms (A+B) to -2 f_R via a verified identity. The remaining gap is proving C + D <= f_same + 2 f_R algebraically, which is equivalent to the original problem but in a cleaner, more explicit form.

---

## Proof Gaps Identified

1. **Term_C + Term_D <= f_same + 2·f_R**: The cross terms C = 2 sum T_mu^T(I-D^T)T_nu and D = 2 sum T_mu^T(I-R_mu D R_nu^T)T_nu involve cross-link rotations D_{mu,nu} which are different for each pair — no sum T_mu = 0 simplification applies. Need a different bounding strategy.

2. **SOS at Q=I**: 16 I_9 - M_9(I) = 0 (zero matrix). Any SOS certificate must vanish at Q=I. Standard degree-2 polynomial SOS is insufficient; degree 4 or Lie-algebra structure needed.

3. **Per-plaquette approach blocked**: Single-plaquette lambda_max = 8 >> budget 4. Global cancellation across all 6 plaquettes is required.

---

## Leads for Follow-Up

- **Bounded cross-links (D=I)**: If D_{mu,nu} = I for all pairs, Term_C = 0 and Term_D simplifies. Does an SOS proof exist in this restricted case?
- **SOS modulo SO(3) ideal**: With cvxpy/SDP solver, try degree-4 Putinar certificate modulo R^T R = I constraints.
- **Lie algebra certificate**: Near Q=I, 16||T||^2 - F_x = sum_k (omega_k · T)^2 + O(eps^3). Compute the quadratic form in the Lie algebra and check if it's a sum of squares.
- **Schur complement approach**: Write 16 I_12 - M_12 in terms of the projector P_V and look for a block-diagonal certificate.

---

## Unexpected Findings

1. **Per-plaquette budget is 2× exceeded**: lambda_max(M_AB) at Q=I is exactly **8**, not 4. Each plaquette "over-contributes" by factor 2, cancelled exactly by the 6-plaquette global structure and V constraint.

2. **Cross-term ratio 5.24% << 8.2%**: The ratio |cross|/f_same is conservatively bounded in the GOAL.md. Numerical max is 5.24% (vs claimed 8.2%), suggesting the GOAL.md bound has slack.

3. **Gap quadratic in ||Q-I||**: The tight bound (gap → 0 as Q → I) occurs with exactly quadratic approach rate, consistent with Q=I being a "flat maximum" of F_x on SO(3)^{10} × V.

---

## Computations Identified for Further Work

- Install cvxpy + SDP solver (mosek/scs) to run Positivstellensatz at degree 4
- Explicit Lie algebra quadratic form computation (symbolic, using sympy)
- Proof for D=I special case (simpler Term_C = 0)
