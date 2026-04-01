# Exploration 003: Prove LEMMA_D and LEMMA_RDR

## Mission Context

We are proving Conjecture 1 for lattice SU(2) Yang-Mills: lambda_max(M(Q)) <= 16 for all Q.

**What's already proved (Strategy 001 + Strategy 002 E001-E002):**
1. Budget identity: for T with sum_mu T_mu = 0, 16||T||^2 = 4 sum_{mu<nu} |T_mu - T_nu|^2 [PROVED]
2. Per-plaquette identity: 4|T_mu - T_nu|^2 - |B_{mu,nu}|^2 = 2f(U,T_mu) + 2f(W,T_nu) - 2 T_mu^T C_{mu,nu} T_nu [VERIFIED to 1e-13]
3. Sum-to-zero trick: sum_{mu<nu} T_mu^T [(I-R_mu) + (I-R_nu^T)] T_nu = -sum_mu f(R_mu, T_mu) [VERIFIED to 7e-15]
4. Vector CBL (VCBL): f(A,p) + f(B,q) + p^T(I-A)D(I-B^T)q >= 0 for all A,B,D in SO(3), p,q in R^3 [PROVED via C-S + AM-GM]
5. Total gap decomposition: 16||T||^2 - F_x(Q,T) = 2*sum_mu f(R_mu, T_mu) + sum_S [VERIFIED to 5.7e-14]

where:
- f(R,p) = p^T(I-R)p >= 0 for R in SO(3)
- U_{mu,nu} = R_mu D_{mu,nu}, W_{mu,nu} = D_{mu,nu} R_nu^T
- sum_S = LEMMA_D + LEMMA_RDR

**The term 2*sum_mu f(R_mu, T_mu) >= 0 is trivial.** The entire proof reduces to:

## THE TARGET: Prove sum_S >= 0

### LEMMA_D (to prove):
sum_{mu<nu} [f(R_mu D_{mu,nu}, T_mu) + f(D_{mu,nu} R_nu^T, T_nu) - 2 T_mu^T (I - D_{mu,nu}^T) T_nu] >= 0

for all T with sum_mu T_mu = 0, all R_mu in SO(3), all D_{mu,nu} in SO(3).

Numerical: 200K tests, 0 violations, min = 0.41 ||T||^2, safety margin ~4x.
FAILS without constraint sum T_mu = 0 (942/200K violations).

### LEMMA_RDR (to prove):
sum_{mu<nu} [f(R_mu D_{mu,nu}, T_mu) + f(D_{mu,nu} R_nu^T, T_nu) - 2 T_mu^T (I - R_mu D_{mu,nu} R_nu^T) T_nu] >= 0

for all T with sum_mu T_mu = 0, all R_mu, D_{mu,nu} in SO(3).

Numerical: 200K tests, 0 violations, min = 0.62 ||T||^2, safety margin ~6x.
FAILS without constraint sum T_mu = 0 (same T violations as LEMMA_D).

## Your Task

Prove LEMMA_D >= 0 and LEMMA_RDR >= 0 (or at least sum_S = LEMMA_D + LEMMA_RDR >= 0). Try multiple approaches. Focus your efforts on LEMMA_D first — it has the smaller safety margin and is likely harder.

### Approach 1: Cauchy-Schwarz Bound on Cross Terms

For each plaquette (mu,nu), the LEMMA_D has:
- Budget: f(R_mu D, T_mu) + f(D R_nu^T, T_nu) (non-negative)
- Cost: 2 T_mu^T (I - D^T) T_nu (can be positive or negative)

By Cauchy-Schwarz:
|T_mu^T (I - D^T) T_nu| <= ||T_mu|| * ||(I-D)T_nu||

Since ||(I-M^T)p||^2 = 2f(M,p) for M in SO(3) [VERIFIED], we get:
|T_mu^T (I - D^T) T_nu| <= ||T_mu|| * sqrt(2f(D,T_nu))

Question: Is the per-plaquette budget f(R_mu D, T_mu) + f(D R_nu^T, T_nu) >= 2|T_mu^T(I-D^T)T_nu|?

Numerically check this per-plaquette. If it fails per-plaquette (likely), check whether the SUM over all 6 plaquettes satisfies the bound (using sum T_mu = 0 somehow).

### Approach 2: Relate LEMMA_D to VCBL

The VCBL gives, for each plaquette:
f(U,p) + f(W,q) + p^T(I-U)M(I-W^T)q >= 0

where U = R_mu D, W = D R_nu^T, and M is ANY SO(3) matrix (the VCBL proof doesn't use M in SO(3) — D in the factorization identity can be any matrix).

The LEMMA_D cross term is T_mu^T(I-D^T)T_nu. Can we write:
(I-D^T) = (I-U^T)(something)(I-W) + correction?

Where U = R_mu D, so U^T = D^T R_mu^T, and W = D R_nu^T, so W^T = R_nu D^T.

Compute (I-U^T) = (I - D^T R_mu^T) and (I-W) = (I - D R_nu^T).

The product (I-U^T)^T (I-W) = (I-R_mu D)(I - D R_nu^T). Expand:
= I - D R_nu^T - R_mu D + R_mu D^2 R_nu^T

While (I-D^T) = I - D^T.

These don't match directly. But PERHAPS:
(I-D^T) = alpha * (I-U^T)^T (I-W) + beta * (I - something) + ...

Test this numerically. If (I-D^T) can be expressed as a linear combination of VCBL-type cross terms plus non-negative corrections, the proof follows.

### Approach 3: Direct Constraint Manipulation

Write T_3 = -T_0 - T_1 - T_2 (eliminating T_3). Then the 6 plaquette pairs (mu,nu) for mu<nu in {0,1,2,3} are:
(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)

The LEMMA_D cross term becomes:
2 sum_{mu<nu} T_mu^T D_{mu,nu} T_nu  (this is the harmful part — the I part sums to ||T||^2/2 via sum-to-zero)

Wait — LEMMA_D has cross term T_mu^T(I - D^T)T_nu. So:
sum cross = sum T_mu^T T_nu - sum T_mu^T D^T_{mu,nu} T_nu
          = -||T||^2/2 - sum T_mu^T D^T_{mu,nu} T_nu   [using sum-to-zero on first part]

So LEMMA_D = f_same/2 - ||T||^2 + sum T_mu^T D^T T_nu >= 0
(check this algebra computationally!)

This means LEMMA_D >= 0 iff f_same/2 + sum T_mu^T D^T T_nu >= ||T||^2.

At D = I for all: f_same/2 has a specific value involving U = R_mu, W = R_nu^T, and sum T_mu^T T_nu = -||T||^2/2.
So LEMMA_D(D=I) = f_same/2 - ||T||^2/2 - ||T||^2/2... no, need to recompute carefully.

The point: substitute the constraint FIRST, then see if the resulting expression has a simpler form.

### Approach 4: Schur Complement / Matrix Inequality

For fixed Q, LEMMA_D is a quadratic form in the 9-vector of T entries (after constraint elimination). Call it L_D(Q) as a 9x9 matrix. We need L_D(Q) >= 0 (PSD) for all Q.

Compute L_D(Q) numerically for 100+ Q. Check its eigenvalue structure. Is the minimum eigenvalue related to something we already know? Is L_D a sum of known PSD terms minus a small perturbation?

### Approach 5: Split and Conquer

LEMMA_D involves 6 terms. Group them:
- Group A: plaquettes (0,1), (2,3) — these share no indices
- Group B: plaquettes (0,2), (1,3)
- Group C: plaquettes (0,3), (1,2)

For each group of 2 plaquettes with disjoint indices (mu,nu) and (alpha,beta) where {mu,nu,alpha,beta} = {0,1,2,3}:
The cross terms T_mu^T(I-D^T)T_nu and T_alpha^T(I-D'^T)T_beta involve non-overlapping T_mu.

With T_3 = -T_0 - T_1 - T_2, the pairs aren't truly independent. But perhaps each group can be bounded separately, and the sum of group bounds gives LEMMA_D >= 0.

## Mandatory Numerical Verification

Before ANY algebraic manipulation:
1. Verify LEMMA_D for 500+ random Q × 20 random T in V. Report min value.
2. Verify LEMMA_D per-plaquette: does the per-plaquette bound hold? (Expected: NO)
3. For each approach, test the intermediate inequalities numerically BEFORE claiming they hold.

## Success Criteria

- **Full success**: Algebraic proof of LEMMA_D >= 0 and LEMMA_RDR >= 0 for all T in V, all Q.
- **Partial success**: Proof of sum_S = LEMMA_D + LEMMA_RDR >= 0 (even if individual lemmas not proved).
- **Other partial success**: Proof of LEMMA_D for a restricted class (e.g., D = I, or rank-1 T, or specific Q families).
- **Failure with value**: Precise characterization of WHY the algebraic proof fails. What inequality is needed that doesn't hold?

## Dead Ends (DO NOT REVISIT)

- Per-plaquette SOS: BLOCKED (single plaquette lambda_max = 8, budget = 4)
- SOS at degree 2: BLOCKED (slack = 0 at Q=I)
- Trace identity for general T: FAILS (varies by factor ~3)
- Rank-1 reduction: FAILS (maximizers not always rank-1)
- E006 uniform-color proof structure: already used for term1, doesn't extend to sum_S

## Output

Write results to REPORT.md (max 250 lines) and REPORT-SUMMARY.md in your working directory. Write incrementally after each approach tested.
