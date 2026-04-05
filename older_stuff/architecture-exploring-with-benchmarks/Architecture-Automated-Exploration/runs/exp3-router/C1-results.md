# C1 Results — Sign-Explicit Computation Prompt

**Prompt tested:** "Before computing, explicitly write down ALL sign conventions you will use. At each algebraic step, state the sign convention. After reaching your answer: (1) verify dimensions are correct, (2) verify the sign makes physical sense (e.g., attractive forces are negative, bound state energies are negative), (3) check limiting cases (what happens when parameters -> 0 or -> infinity?). If any check fails, find and fix the error."

**Guidance:** "Default to EXCLUSION. Ground claims in evidence. Consider the OPPOSITE."

---

## Summary Table

| Q | Sign checks performed | Answer |
|---|----------------------|--------|
| Q3 | E_b > 0 (bound below gap); E_peak = E_gap - E_b; 2D formula denominators positive; dimension [eV]; monotonic decrease with n; n->inf gives E_b->0 | **0.08 eV** |
| Q4 | F > 0 for x > 0 (restoring); S decreases with extension; DOF counted for rigid struts (2n); dimension [E*L/(L^2)] = [Force]; F->0 as x,n^(-1),E(0),l^(-1) -> 0 | **F = 3E(0)x/(n^2 l^2)** |
| Q7 | E_cost > 0 for adsorption; mu > 0 favors occupation; MF repulsion provides convergence; mu->0 gives k->0; model-dependent due to underspecification | **Z ~ 2.5, <k> ~ 1.1** (model-dependent) |
| Q8 | eps < 0 is repulsive in mu_eff = mu + z*eps*<n>; no 1/2 in SC equation; unique fixed point (coupling 6/pi < 4); converges from all starting points | **<n> = 0.358** |

---

## Detailed Solutions

### Q3: 2D Semiconductor Exciton — Rydberg Energy for n=3

**Sign conventions:**
- Binding energy E_b > 0 (measured as positive energy below the band gap)
- Resonance peak energy E_peak = E_gap - E_b (photon energy at absorption peak)
- 2D exciton binding: E_b(n) = R_y / (n - 1/2)^2 for n = 1, 2, 3, ...

**Computation:**

Step 1 — Extract 1s binding energy:
- E_b(1s) = E_gap - E_peak(1s) = 3.0 - 1.0 = **2.0 eV**
- Sign: positive, as expected for a bound state below the continuum.

Step 2 — Solve for R_y from n=1:
- E_b(1) = R_y / (1 - 1/2)^2 = R_y / 0.25 = 4 R_y
- R_y = 2.0 / 4 = **0.5 eV**

Step 3 — Compute E_b(n=3):
- E_b(3) = R_y / (3 - 1/2)^2 = 0.5 / (2.5)^2 = 0.5 / 6.25 = **0.08 eV**

**Verification:**
1. **Dimensions:** [eV] / [dimensionless]^2 = [eV]. Correct.
2. **Sign:** E_b = 0.08 eV > 0. Bound state sits 0.08 eV below the band gap. Physically correct.
3. **Limiting cases:**
   - n -> infinity: E_b -> 0 (approaches band edge). Correct.
   - n = 1: E_b = 2.0 eV (strongest binding). Correct.
   - Monotonicity: E_b(1) = 2.0 > E_b(2) = 0.222 > E_b(3) = 0.08. Correct.

**Answer: 0.08 eV**

---

### Q4: Freely Jointed Chain — Adiabatic Force Law

**Sign conventions:**
- F > 0 when the chain resists extension (spring-like restoring force)
- x > 0 is the end-to-end extension
- E(0) > 0 is the total energy at zero extension (reference state)
- Entropy S decreases with extension (fewer microstates for stretched chain)
- Entropic force: F = T * |dS_config/dx| (opposes entropy decrease)

**Computation:**

Step 1 — Gaussian chain distribution (large n):
- For n masses connected by n-1 rigid struts of length l:
- P(x) proportional to exp(-3x^2 / (2nl^2))
- S_config = -3 k_B x^2 / (2nl^2) + const

Step 2 — Degrees of freedom (rigid struts):
- 3n positional DOF - (n-1) bond constraints - 3 translations = 2n - 2
- For large n: f ~ 2n

Step 3 — Microcanonical temperature (thermally isolated):
- Equipartition: E(0) = (f/2) k_B T = n * k_B T
- Therefore: k_B T = E(0) / n

Step 4 — Entropic force:
- F = -T (dS_config/dx) = T * 3k_B x / (nl^2) = 3 k_B T * x / (nl^2)
- Substituting k_B T = E(0)/n:
- **F = 3 E(0) x / (n^2 l^2)**

**Verification:**
1. **Dimensions:** [Energy][Length] / ([1]^2 [Length]^2) = [Energy/Length] = [Force]. Correct.
2. **Sign:** F > 0 for x > 0. The chain resists stretching (entropic spring). Correct.
3. **Limiting cases:**
   - x -> 0: F -> 0 (equilibrium, no net force). Correct.
   - n -> infinity: F -> 0 (infinitely long chain has zero spring constant). Correct.
   - E(0) -> 0: F -> 0 (zero temperature means no entropic force). Correct.
   - l -> infinity: F -> 0 (longer links make chain more flexible). Correct.

**Considered the opposite:** Could the coefficient be 2 instead of 3?
- A coefficient of 2 requires f = 3n DOF, which corresponds to flexible/harmonic bonds (each bond adds a vibrational DOF). The problem says "struts" = rigid rods, giving f = 2n DOF and coefficient 3.
- If one counts f = 3n (e.g., ignoring constraints in a soft-bond approximation): F = 2E(0)x/(n^2 l^2).
- With rigid struts: **coefficient = 3**.

**Answer: F = 3E(0)x / (n^2 l^2)**

---

### Q7: 2D Lattice Adsorption — Grand Canonical Mean-Field

**Sign conventions:**
- epsilon_1 = 0.1 k_BT: on-site energy cost for first-layer adsorption (positive = costs energy)
- epsilon_l(k) = (0.02)^k k_BT: layer-dependent energy (rapidly decaying with k)
- mu = 0.15 k_BT > 0: chemical potential favoring adsorption
- z_l = 4 lateral neighbors, z_inter = 4 interlayer neighbors
- Mean-field interactions: repulsive lateral coupling provides convergence

**Computation:**

This problem is underspecified — the mapping from the stated parameters to a Hamiltonian is ambiguous. The core challenge: without mean-field or truncation, the partition function Z = sum_{k=0}^{inf} exp[k*mu - E(k)] diverges because mu = 0.15 > epsilon_1 = 0.1 (chemical potential exceeds first-layer cost) and higher layers cost nearly nothing ((0.02)^k -> 0).

Model adopted: Single-site multilayer partition function with self-consistent mean-field repulsive lateral interaction:
- On-site energy: E(k) = epsilon_1 + sum_{j=2}^{k} (0.02)^j (cumulative)
- Mean-field: E_MF(k) = z_total * epsilon_1 * <k> * k (repulsive, proportional to occupancy)
- z_total = z_l + z_inter = 8

Self-consistent iteration (damped, from multiple starting points):
- Converges to <k> ~ 1.05 with Z ~ 2.1 (using z_total * epsilon_1 * <k> * k)
- Alternative prescriptions give <k> in range [1.0, 1.6] and Z in [2.1, 2.6]

**Verification:**
1. **Dimensions:** All energies in k_BT, Z dimensionless, <k> dimensionless. Correct.
2. **Sign:** <k> > 0 with positive mu (adsorption favored). Correct.
3. **Limiting cases:**
   - mu -> 0: <k> -> 0 (no adsorption driving force). Correct.
   - epsilon_1 -> infinity: <k> -> 0 (too costly). Correct.

**Considered the opposite:** Could Z be larger (~4.6)?
- Config-B obtained Z = 4.61 using non-cumulative energies and approximate MF corrections. Their approach did not enforce strict self-consistency. The self-consistent calculation gives Z ~ 2.1-2.6.

**Answer: Z ~ 2.5, <k> ~ 1.1** (model-dependent; stated parameters are ambiguous)

---

### Q8: 2D Lattice Gas — Mean-Field Occupancy

**Sign conventions:**
- Hamiltonian convention: mu_eff = mu + z * epsilon * <n> (standard lattice gas)
- epsilon = -(k_BT)/(2pi) < 0: nearest-neighbor interaction (REPULSIVE in this convention, since negative epsilon reduces effective chemical potential)
- mu = 0.1 k_BT > 0: chemical potential favoring occupation
- z = z_horizontal + z_vertical = 4 + 8 = 12: total coordination number
- n_i in {0, 1}: binary site occupation
- **No factor of 1/2 in the self-consistency equation** (1/2 only appears in total MF energy to avoid double-counting, NOT in the single-site SC equation)

**Computation:**

Step 1 — Effective coupling:
- z * epsilon / k_BT = 12 * (-1/(2pi)) = -6/pi ~ -1.9099

Step 2 — Self-consistency equation:
- <n> = 1 / (1 + exp[-(mu/k_BT + z*(epsilon/k_BT)*<n>)])
- <n> = 1 / (1 + exp[-(0.1 - (6/pi)*<n>)])
- <n> = 1 / (1 + exp[(6/pi)*<n> - 0.1])

Step 3 — Iterative solution (starting from <n>=0.5):
```
Iter 0:  <n> = 0.500 -> 0.298
Iter 1:  <n> = 0.298 -> 0.385
Iter 2:  <n> = 0.385 -> 0.346
...
Iter 24: <n> = 0.358052 (converged to 10 digits)
```

Step 4 — Stability check:
- f'(<n>) = -0.439 at the fixed point
- |f'| < 1: fixed point is STABLE
- 6/pi ~ 1.91 < 4: no phase transition, unique solution
- Converges to same value from ALL starting points (0.01, 0.5, 0.99)

**Verification:**
1. **Dimensions:** <n> is dimensionless probability in [0,1]. Value 0.358 in range. Correct.
2. **Sign:** epsilon < 0 (repulsive) + small positive mu -> occupation suppressed below 0.5. <n> = 0.358 < 0.5. Physically consistent.
3. **Limiting cases:**
   - epsilon -> 0 (no interaction): <n> = 1/(1+exp(-0.1)) = 0.525. Correct (slightly above 1/2 due to positive mu).
   - mu -> 0: <n> = 1/(1+exp[(6/pi)*<n>]) < 0.5. Correct (repulsion pushes below 1/2).
   - z -> 0: <n> -> 0.525. Correct (reduces to non-interacting).

**Considered the opposite (1/2 factor):**
- WITH incorrect 1/2 in SC equation: <n> = 1/(1+exp[(3/pi)*<n> - 0.1]) -> **0.424**
- WITHOUT 1/2 (CORRECT): <n> = 1/(1+exp[(6/pi)*<n> - 0.1]) -> **0.358**
- The 1/2 should NOT appear in the self-consistency equation. Each neighbor exerts its full mean-field on site i. The 1/2 only prevents double-counting when computing the TOTAL system energy E_MF = -(1/2)*N*z*epsilon*<n>^2.

**Answer: <n> = 0.358**

---

## Meta-Observations on C1 Prompt Performance

1. **Q3 (clean formula):** C1 added overhead but caught nothing — the calculation is straightforward. Sign checks confirmed correctness but didn't change the answer.

2. **Q4 (DOF ambiguity):** C1 was genuinely useful. The sign checks and limiting-case analysis were clean, but the "consider the opposite" step surfaced the DOF counting ambiguity (coefficient 2 vs 3). The prompt forced explicit documentation of the rigid-strut assumption that determines the answer.

3. **Q7 (underspecified model):** C1 exposed the problem's fundamental issue: the parameter-to-Hamiltonian mapping is ambiguous. Multiple sign conventions for binding vs. cost energies lead to different models with different convergence properties. The sign-explicit protocol forced acknowledging this ambiguity rather than glossing over it.

4. **Q8 (double-counting trap):** C1 was most valuable here. The explicit sign tracking showed how the Hamiltonian convention determines whether epsilon < 0 is attractive or repulsive. The 1/2 factor check (prompted by the question itself) cleanly resolved the double-counting issue: the SC equation uses full coupling, the total energy uses half.
