# Exploration 004: Large Lattice Verification of H_norm ≤ 1/12

## Goal
Test whether the conjecture H_norm ≤ 1/12 holds on larger lattices (L=4, L=6) using the correct LEFT B_□ formula (P3 = Q1@Q2@Q3†). Prior work (Exploration 003) confirmed the formula and tested L=2 only.

## Convention
- LEFT perturbation: Q_e → exp(t·v_e) @ Q_e
- P1=I, P2=U1, P3=U1@U2@U3†, P4=U1@U2@U3†@U4† = U_plaq
- H_norm = λ_max / (48β), bound: H_norm ≤ 1/12 = 0.083333...
- At Q=I: λ_max = 4β → H_norm = 1/12 exactly (sanity check, also upper bound)

---

## Summary of Results

| Task | Lattice | Configs | Max H_norm | Bound | All OK |
|------|---------|---------|-----------|-------|--------|
| Sanity | L=4 | Q=I | 0.08333333 | 0.08333333 | ✓ |
| Task 1 | L=4 | 21 | 0.08333333 | 0.08333333 | ✓ |
| Task 2 | L=6 | 11 | 0.08333333 | 0.08333333 | ✓ |
| Task 3 | L=2 | (in progress) | - | - | - |
| Task 4 | L=2 | 39 | 0.08333333 | 0.08333333 | ✓ |

**Key Finding:** The bound H_norm ≤ 1/12 holds for all tested configurations at L=2, L=4, and L=6. The maximum is H_norm = 1/12 = 0.083333, achieved exclusively at flat connections (U_plaq = I).

---

## Task 1: L=4 Verification [COMPUTED]

### Setup
- L=4, d=4, N=2, β=1, n_links=1024, n_dof=3072, n_plaq=1536
- Dense Hessian build (0.23s) + eigsh warm start (0.10s) + eigvalsh for final

### Sanity Check
- `[COMPUTED]` λ_max = 4.00000000 at Q=I (difference from 4β: 8.88e-16, machine precision)
- H_norm = 0.08333333 = 1/12 exactly

### 21 Configuration Results

| Config | λ_max | H_norm |
|--------|-------|--------|
| Q=I (sanity) | 4.000000 | 0.083333 |
| Haar 0 | 3.508282 | 0.073089 |
| Haar 1 | 3.529256 | 0.073526 |
| Haar 2 | 3.521504 | 0.073365 |
| Haar 3 | 3.521752 | 0.073370 |
| Haar 4 | 3.516869 | 0.073268 |
| Gibbs 0 | 3.515371 | 0.073237 |
| Gibbs 1 | 3.519589 | 0.073325 |
| Gibbs 2 | 3.513460 | 0.073197 |
| Gibbs 3 | 3.516338 | 0.073257 |
| Gibbs 4 | 3.514343 | 0.073215 |
| Near-I 0 | 3.989501 | 0.083115 |
| Near-I 1 | 3.988469 | 0.083093 |
| Near-I 2 | 3.989078 | 0.083106 |
| Near-I 3 | 3.988897 | 0.083102 |
| Near-I 4 | 3.988693 | 0.083098 |
| Adv 0 (random) | 3.630419 | 0.075634 |
| Adv 1 (aligned_τ₀, flat) | 4.000000 | 0.083333 |
| Adv 2 (aligned_τ₁, flat) | 4.000000 | 0.083333 |
| Adv 3 (alternating) | 3.924342 | 0.081757 |
| Adv 4 (fixed_axis, flat) | 4.000000 | 0.083333 |

**All 21 configurations satisfy H_norm ≤ 1/12. ALL WITHIN BOUND = TRUE.**

### Key Observations
1. **Haar random + Gibbs**: H_norm ≈ 0.073 (well below 1/12 = 0.083)
2. **Near-identity (eps=0.1)**: H_norm ≈ 0.0831 — close to but below the bound
3. **Adversarial from flat start**: H_norm stays at exactly 0.083333 — gradient ascent from flat connections is stuck at the maximum (critical point)
4. **Adversarial from random start**: max H_norm = 0.075634 after 30 steps
5. **Adversarial alternating config**: H_norm = 0.081757 — near but below bound

### ARPACK Artifact Warning
`[COMPUTED]` When λ_max is degenerate (multiplicity 3 at flat connections), ARPACK eigsh with tol=1e-7 can overestimate λ_max by up to ~0.003. Code: `verify_violation.py` confirms this. Always use eigvalsh or tol≤1e-9 for final accurate measurements.

---

## Task 2: L=6 Matrix-Free eigsh [COMPUTED]

### Setup
- L=6, d=4, N=2, β=1, n_links=5184, n_dof=15552, n_plaq=7776
- Matrix-free ARPACK eigsh via LinearOperator (each call ~11-154s depending on convergence)
- Local Metropolis update for Gibbs sampling (only recomputes affected plaquettes)

### Sanity Check
- `[COMPUTED]` λ_max = 4.00000000 at Q=I at L=6
- H_norm = 0.08333333 = 1/12
- Eigsh time: 10.9s

### 11 Configuration Results

| Config | λ_max | H_norm | Time |
|--------|-------|--------|------|
| Q=I (sanity) | 4.000000 | 0.083333 | 10.9s |
| Haar 0 | 3.524709 | 0.073431 | 100.0s |
| Haar 1 | 3.529357 | 0.073528 | 89.4s |
| Haar 2 | 3.526112 | 0.073461 | 119.1s |
| Haar 3 | 3.520687 | 0.073348 | 110.0s |
| Haar 4 | 3.526995 | 0.073479 | 82.6s |
| Gibbs 0 (β=0.1) | 3.530233 | 0.073547 | 73.6s |
| Gibbs 1 (β=0.1) | 3.521624 | 0.073367 | 96.5s |
| Gibbs 2 (β=0.1) | 3.531414 | 0.073571 | 153.8s |
| iσ₃_all | 4.000000 | 0.083333 | 19.1s |
| exp(0.5τ₀)_all | 4.000000 | 0.083333 | 26.2s |

**All 11 configurations satisfy H_norm ≤ 1/12. ALL_OK = TRUE.**

### Key Observations
1. **H_norm is L-independent**: Haar random gives H_norm ≈ 0.073 at both L=4 and L=6
2. **Flat connections** give exactly H_norm = 1/12 at L=6 (iσ₃_all and exp(0.5τ₀)_all)
3. **The bound is not tighter at larger lattice sizes** — H_norm can still reach 1/12

---

## Task 3: Adversarial Gradient Ascent [IN PROGRESS]

Running task3_adversarial.py (L=2 gradient ascent + L=4 verification). Output buffered, results pending.

---

## Task 4: Center Element Configurations [COMPUTED]

### Setup
- L=2, d=4, N=2, β=1.0, n_links=64
- 39 configurations tested

### Key Finding: ALL Uniform Configurations Give H_norm = 1/12 Exactly

For any uniform configuration (U_all = same SU(2) element g for all links):
- Plaquette holonomy U_plaq = g·g·g†·g† = I (flat connection)
- All flat connections are gauge-equivalent
- λ_max = 4β = 4, H_norm = 1/12

| Configuration | U_plaq | H_norm |
|---------------|--------|--------|
| θ=0.0 (Q=I) | I | 0.083333 |
| θ=0.1 through θ=π (all θ values) | I | 0.083333 |
| iσ₁ = exp(πτ₁) | I | 0.083333 |
| iσ₂ | I | 0.083333 |
| iσ₃ (prior case) | I | 0.083333 |
| -I (center element) | I | 0.083333 |
| exp(π/4 τ₁) (goal-specified) | I | 0.083333 |
| exp(π/2 τ₁) (goal-specified) | I | 0.083333 |
| Z2 twist (μ=0 links = -I) | I | 0.083333 |
| Mixed ±exp(θτ₁) | I | 0.083333 |

**Every tested uniform/periodic configuration gives H_norm = 1/12 exactly.**

### Physical Interpretation
The maximum H_norm = 1/12 corresponds to FLAT CONNECTIONS (zero field strength). For generic (non-flat) configurations, H_norm < 1/12. This is consistent with the conjecture: no configuration exceeds the flat connection maximum.

---

## ARPACK Artifact Investigation [COMPUTED]

Code: `verify_violation.py`

Initial task1 run triggered a false violation (H_norm = 0.083393). Investigation showed:
- eigsh with tol=1e-7 at a degenerate eigenvalue (multiplicity 3) gave λ_max = 4.002861 (artifact)
- eigvalsh with full matrix gave λ_max = 4.000000 (exact)
- The "violation" was 100% a numerical artifact from ARPACK tolerance, not a genuine counterexample

**Lesson**: For degenerate eigenvalues, always use eigvalsh or very tight eigsh tolerance (≤1e-9) for definitive measurements.

---

## Engineering Notes

### Performance Summary
| Method | Lattice | Time per call |
|--------|---------|---------------|
| Dense H build | L=4 | 0.23s |
| eigsh warm-start | L=4 | 0.10s |
| eigvalsh (full) | L=4 | 6.62s |
| eigsh (matrix-free) | L=6 | 10-154s |
| gradient step | L=2 | 0.18s |
| gradient step | L=4 | ~4.4s |

### Key Constraint on λ_max
The pattern across all lattice sizes:
- Flat connections: H_norm = 1/12 = 0.083333 (maximum, saturates bound)
- Haar random: H_norm ≈ 0.073 (typical value, ~12% below bound)
- Near-identity (eps=0.1): H_norm ≈ 0.0831 (97% of bound)
- This pattern is L-independent (L=2, L=4, L=6 give same values)
