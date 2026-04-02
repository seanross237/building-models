# Exploration 005: Proof of sum_S >= 0

## Goal
Prove sum_S(R, D, T) >= 0 for all R_mu ∈ SO(3), D_{mu,nu} ∈ SO(3), T with Σ T_mu = 0.

## Stage 1: Crude Polarization Bound — FAILS [COMPUTED]

The GOAL's polarization identity u^T(I-D)v = (1/2)[f(D,u+v) - f(D,u) - f(D,v)] is **incorrect** for non-symmetric E = I-D. It only gives the symmetric part; the antisymmetric part is missing.

- Crude polarization bound goes negative in 37% of trials, with ratio correction/baseline > 10.
- C-S + spectral bound is even worse (65% negative).
- **Any approach bounding bilinear forms per-pair independently via polarization fails.** [COMPUTED]

## Stage 2: Structural Discovery — M9 is Affine in D [VERIFIED]

**Key finding**: M9(R, D) is an AFFINE function of D. [VERIFIED to 3.5e-15]

Since M9 is linear in D, and each D_{mu,nu} enters only its own pair's contribution:
- We can minimize over each D independently
- The minimum of u^T(I-D)v over D ∈ SO(3) has a closed form

Additional findings:
- Opposite-face pairings not PSD (all negative)
- Vertex stars not PSD
- VCBL remainder deeply negative (-19.9)
- M9 rank is always 9 (full rank for D ≠ I) [COMPUTED]

## Stage 3: THE PROOF — Contraction Bound [VERIFIED + PROVED]

### Theorem
**sum_S(R, D, T) ≥ 0** for all R_mu ∈ SO(3)^4, D_{mu,nu} ∈ SO(3)^6, T ∈ V = {T : Σ T_mu = 0}.

### Proof

**Step 1** (Master Identity, E004 [VERIFIED to 7.1e-14]):

sum_S = baseline + Σ_{mu<nu} 2·u_{mu,nu}^T·(I - D_{mu,nu})·v_{mu,nu}

where baseline = 6·Σ f(R_mu, T_mu) + |Σ R_mu^T T_mu|² ≥ 0,
u = R_mu^T T_mu - T_nu, v = T_mu - R_nu^T T_nu.

**Step 2** (Per-pair Cauchy-Schwarz [PROVED]):

For D ∈ SO(3): u^T D v = u·(Dv) ≤ ||u||·||Dv|| = ||u||·||v|| (Cauchy-Schwarz + orthogonality).

Therefore: u^T(I-D)v = u·v − u^T D v ≥ u·v − ||u||·||v||.

**Step 3** (Independent minimization [PROVED]):

Since the 6 matrices D_{mu,nu} are independent, apply Step 2 to each pair:

sum_S ≥ F(R,T) := baseline − 2·Σ_{mu<nu}(||u||·||v|| − u·v)

**Step 4** (Algebraic identity [VERIFIED to 1.1e-14]):

2(||u||·||v|| − u·v) = ||u−v||² − (||u|| − ||v||)²

**Step 5** (Key computation [VERIFIED to 1.1e-13]):

Define w_mu = (I − R_mu^T)T_mu. Then:
- u − v = −(w_mu + w_nu)
- ||w_mu||² = 2·f(R_mu, T_mu)
- Σ w_mu = Σ(T_mu − R_mu^T T_mu) = 0 − Σ R_mu^T T_mu = −Σ a_mu (using Σ T = 0)

Therefore:
Σ_{mu<nu} ||u−v||² = Σ ||w_mu + w_nu||² = 2·Σ||w||² + |Σw|² = 4·Σf + |Σ R^T T|²

**Step 6** (Cancellation [PROVED]):

F = (6·Σf + |Σa|²) − (4·Σf + |Σa|²) + Σ(||u|| − ||v||)²
  = **2·Σ f(R_mu, T_mu) + Σ_{mu<nu}(||u_{mu,nu}|| − ||v_{mu,nu}||)² ≥ 0**

Both terms are manifestly non-negative: f(R,T) ≥ 0 for R ∈ SO(3), and (·)² ≥ 0.

**∴ sum_S ≥ F ≥ 0.** □

### Tightness

F = 0 iff f(R_mu, T_mu) = 0 for all mu AND ||u|| = ||v|| for all pairs.
- f = 0 iff T_mu is on the rotation axis of R_mu.
- On axes: u = v (E004 Critical T Theorem), so ||u|| = ||v||.
- This matches the null space of M9(D=I): T_mu = c_mu·axis(R_mu) with Σ c_mu·axis(R_mu) = 0.

### Stronger result

The proof actually shows sum_S ≥ 0 for **all contractions** ||D_{mu,nu}|| ≤ 1, not just SO(3). The SO(3) constraint is not needed — orthogonality of D enters only through ||Dv|| = ||v||, which holds for all D with ||D|| ≤ 1 (gives ||Dv|| ≤ ||v||, yielding u^T Dv ≤ ||u||·||v||). [VERIFIED: 0/2000 violations over contractions]

## Verification Scorecard

| Step | Claim | Status | Evidence |
|------|-------|--------|----------|
| 1 | Master identity | [VERIFIED] | E004, 500 trials, err < 7.1e-14 |
| 2 | u^T Dv ≤ \|\|u\|\|·\|\|v\|\| | [PROVED] | Cauchy-Schwarz + orthogonality |
| 3 | Per-pair independence | [PROVED] | D's are independent variables |
| 4 | Algebraic identity | [VERIFIED] | 1000 trials, err < 1.1e-14 |
| 5 | Σ\|\|u-v\|\|² = 4Σf + \|Σa\|² | [VERIFIED] | 2000 trials, err < 1.1e-13 |
| 5a | \|\|w\|\|² = 2f | [VERIFIED] | 500 trials, err < 2.8e-14 |
| 5b | Σw = -Σa | [VERIFIED] | 500 trials, err < 2.3e-15 |
| 6 | F = 2Σf + Σ(·)² | [VERIFIED] | 2000 trials, err < 1.4e-13 |
| — | F ≥ 0 | [VERIFIED] | 10K random + adversarial opt, min ≈ 0 |
| — | sum_S ≥ F | [VERIFIED] | 5000 trials, min gap = 6.1 |
| — | Full chain sum_S ≥ 0 | [VERIFIED] | 25K random + adversarial, 0 violations |

## Key Insights

1. **M9 is affine in D**: This structural property (verified to 3.5e-15) is crucial — it means per-pair minimization over D is valid and has a closed form.

2. **Cauchy-Schwarz is enough**: The simple bound u^T Dv ≤ ||u||·||v|| (from CS + orthogonality) suffices. No need for sophisticated spectral bounds.

3. **Beautiful cancellation**: The sum Σ||u-v||² = 4Σf + |Σa|² exactly cancels the cross term |Σa|² in the baseline, leaving 2Σf as the "margin" — just enough to absorb the correction.

4. **The hardest case is easy**: At the null eigenvector (T on axes), u = v so the correction vanishes and the bound is tight. The proof difficulty is entirely in the off-axis directions, where the baseline provides the margin.
