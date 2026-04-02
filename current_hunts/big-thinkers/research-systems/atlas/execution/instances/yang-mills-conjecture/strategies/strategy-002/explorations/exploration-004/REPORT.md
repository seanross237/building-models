# Exploration 004: Prove sum_S >= 0

## Goal
Prove sum_S >= 0 for all R_mu ∈ SO(3), D_{mu,nu} ∈ SO(3), T ∈ V = {T: Σ T_mu = 0}.

## Stage 1: D=I Base Case [VERIFIED + PROVED]

**Correction of E003**: E003's claim "sum_S(D=I) = 0 for all R, T" is FALSE.
Correct statement: sum_S(D=I) >= 0 with min eigenvalue = 0 (tight, multiplicity always 1).

### Identity [VERIFIED to 1.1e-13, 500 trials]

**sum_S(R, D=I, T) = 6·Σ_mu f(R_mu, T_mu) + |Σ_mu R_mu^T T_mu|²**

### Proof [VERIFIED]

At D=I: S_{mu,nu} = 2f(R_mu, T_mu) + 2f(R_nu, T_nu) - 2T_mu^T(I - R_mu R_nu^T)T_nu.
Using f(R^T, p) = f(R, p) (scalar transpose identity).

**Diagonal**: Each mu in 3 pairs → sum = 6·Σ f(R_mu, T_mu).

**Cross**: Using Σ T = 0 → Σ_{mu<nu} T_mu·T_nu = -||T||²/2 → first part = ||T||².
Using T_mu^T R_mu R_nu^T T_nu = (R_mu^T T_mu)·(R_nu^T T_nu) → second part = |Σ R^T T|² - ||T||².
Total cross = |Σ R_mu^T T_mu|².

Both terms >= 0. **QED.** □

**Null space**: T_mu = c_mu·axis(R_mu) with Σ c_mu·axis(R_mu) = 0.
Zero eigenvalue multiplicity = 1 (500/500 configs). [COMPUTED]

## Stage 2: Delta_S Factoring [VERIFIED to 7.1e-14]

### Identity [VERIFIED]

**Δ S_{mu,nu} := S_{mu,nu}(D) - S_{mu,nu}(I) = 2·(R_mu^T T_mu - T_nu)^T · (I-D) · (T_mu - R_nu^T T_nu)**

Notation: u_{mu,nu} = R_mu^T T_mu - T_nu, v_{mu,nu} = T_mu - R_nu^T T_nu, E = I-D.

### Master Identity [VERIFIED]

**sum_S(R, D, T) = [6·Σ f(R_mu, T_mu) + |Σ R^T T|²] + Σ_{mu<nu} 2·u^T · E · v**

(baseline ≥ 0) + (Delta term, signed)

## Stage 3: Critical T Theorem [VERIFIED + PROVED]

### Theorem (Key Result)
For T on rotation axes (T_mu = c_mu·n_mu where n_mu = axis(R_mu), Σ c_mu n_mu = 0):

**sum_S(R, D, T) ≥ 0 for ALL D ∈ SO(3)^6.**

### Proof [VERIFIED]

For T on axes: R_mu^T T_mu = c_mu n_mu (since R_mu n_mu = n_mu) and R_nu^T T_nu = c_nu n_nu.
Therefore **u_{mu,nu} = v_{mu,nu} = c_mu n_mu - c_nu n_nu**.

Each Delta term becomes: 2·u^T(I-D)u = 2f(D, u) ≥ 0 (since f(M,p) ≥ 0 for M ∈ SO(3)).

So: Σ Δ S ≥ 0, and sum_S(D) = sum_S(I) + Σ Δ S = 0 + (≥0) ≥ 0. **QED.** □

**Significance**: This proves sum_S ≥ 0 for the MOST DANGEROUS T direction (the null eigenvector of M9 at D=I). The "hardest" case is exactly where the proof works cleanly.

### Numerical confirmation [COMPUTED]
- max ||u-v|| = 1.2e-15 (confirms u=v on axes)
- min Σ Δ S = 0.87 > 0 over 500 configs
- z^T Δ M9 z ≥ 2.95 over 1000 configs (strongly positive)
- 2x2 submatrix (z, w_2) of M9(D): min determinant = 12.3 > 0 [always PSD]

## Stage 4: Proof Gap — Full Result [COMPUTED, NOT PROVED]

### Approaches Attempted (Dead Ends)
| Approach | Result | Why it fails |
|----------|--------|--------------|
| Convexity in D | FAILS | Hessian negative at D=I and elsewhere |
| B9 ≥ C9 (budget ≥ cross as matrices) | FAILS | Generalized eigenvalue ratio = 2.36 |
| VCBL(-I) per-plaquette | FAILS | Remainder can reach -151 |
| Per-plaquette VCBL (any M) | IMPOSSIBLE | I-U rank 2, cross term outside range⊗range |
| Eigenvalue perturbation | FAILS | ||Δ||/λ₂ up to 12536 |
| Gershgorin block bound | FAILS | Always negative (too loose) |
| M12 PSD directly | FAILS | M12 has 2 negative eigs (need V restriction) |

### Adversarial Verification [COMPUTED]
- **50,000 random + gradient descent**: min eigenvalue = **3.9e-13 ≈ 0**
- Minimizer has D near I (||D-I|| ~ 0.1-0.25)
- Same R at D=I: min eigenvalue = 0 (as expected)
- **Every perturbation from D=I INCREASES min eigenvalue**
- All 5000 random + 2000 targeted + 10000 random: **zero negative eigenvalues**

### Remaining Structure [COMPUTED]
- M12 is NOT PSD (2 negative eigenvalues), but negative eigenvectors have non-zero V-projection
- Off-diagonal symmetric part of cross blocks is always NSD (negative semi-definite)
- Budget matrix B9 has min eigenvalue 0.63 (always PD)
- Cross/budget SCALAR ratio bounded at 0.29 (cross never exceeds 30% of budget)

## Summary of Verified Results

| Claim | Status | Evidence |
|-------|--------|----------|
| sum_S(D=I) = 6Σf + \|Σ R^T T\|² | **[VERIFIED]** | 500 trials, err < 1.1e-13 |
| sum_S(D=I) ≥ 0 | **[VERIFIED]** | Algebraic proof: both terms ≥ 0 |
| Null space = T on axes, mult 1 | **[VERIFIED]** | 500 configs, all mult 1 |
| Δ S factoring identity | **[VERIFIED]** | 500×6 trials, err < 7.1e-14 |
| sum_S ≥ 0 for critical T (on axes) | **[VERIFIED]** | Algebraic proof: u=v → f(D,u)≥0 |
| z^T Δ M9 z ≥ 0 (null direction) | **[VERIFIED]** | 1000 configs, min = 2.95 |
| 2x2 (z,w₂) submatrix PSD | **[COMPUTED]** | 500 configs, min det = 12.3 |
| sum_S ≥ 0 globally | **[COMPUTED]** | 67K adversarial, min = 3.9e-13 |
| Full algebraic proof of sum_S ≥ 0 | **[CONJECTURED]** | All attempts at proof incomplete |
