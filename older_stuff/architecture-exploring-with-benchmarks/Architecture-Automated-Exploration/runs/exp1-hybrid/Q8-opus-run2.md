# Q8 — Mean-Field Lattice Gas Adsorption: Hybrid M2+M4 Meta-Plan (Run 2)

## PHASE 1 — PLAN

### Constraint Extraction

**Entities:**
- N adsorption sites on a 2D surface, each with n_i in {0, 1}
- Multilayer adsorption allowed (vertical stacking, making the lattice 3D-like)
- Single interaction energy epsilon between all nearest-neighbor pairs

**Parameters:**
- epsilon = -k_BT/(2pi) (negative = attractive)
- mu = 0.1 k_BT (positive chemical potential favoring occupation)
- z_horizontal = 4 (in-plane neighbors, e.g., square lattice)
- z_vertical = 8 (interlayer neighbors)
- T = 300 K

**Framework:** Grand canonical ensemble + mean-field approximation

**Target:** Average occupancy per site, rounded to 3 decimal places

### Shortest Path (3 steps)

1. **Total coordination:** z_total = z_h + z_v = 12 (single epsilon, so mean-field treats all neighbors identically)
2. **Self-consistency equation:** In mean-field lattice gas, replace neighbor occupancies by <n>:
   <n> = 1 / (1 + exp(beta * (z * epsilon * <n> - mu)))
   With beta*epsilon = -1/(2pi), beta*mu = 0.1, this becomes:
   <n> = 1 / (1 + exp(-12/(2pi) * <n> - 0.1))
3. **Solve iteratively** and round to 3 decimal places

---

## PHASE 2 — SOLVE

### Step 1: Dimensionless parameters

- beta * epsilon = -1/(2pi) = -0.15915494...
- beta * mu = 0.1
- z_total = z_h + z_v = 4 + 8 = 12

### Step 2: Mean-field self-consistency equation

The lattice gas Hamiltonian:
H = epsilon * sum_{<ij>} n_i n_j

In the grand canonical ensemble with chemical potential mu, the effective single-site energy under mean-field replacement (all neighbors -> <n>) is:

H_i^{eff} = (epsilon * z_total * <n> - mu) * n_i

Single-site grand partition function:
xi = 1 + exp(-beta * (epsilon * z_total * <n> - mu))

Average occupancy:
<n> = 1 / (1 + exp(beta * (z_total * epsilon * <n> - mu)))
    = 1 / (1 + exp(12 * (-1/(2pi)) * <n> - 0.1))

### Step 3: Numerical solution

Iterating from <n> = 0.5:

| Iteration | <n>          |
|-----------|--------------|
| 0         | 0.7417204048 |
| 1         | 0.8200345559 |
| 5         | 0.8479904070 |
| 10        | 0.8480957260 |
| 24        | 0.8480958211 (converged) |

Verification at fixed point:
- exponent = 12 * (-0.15915494) * 0.84810 - 0.1 = -1.71974
- exp(-1.71974) = 0.17911
- 1/(1 + 0.17911) = 0.84810 (self-consistent)

### Exclusion checks

1. **Multiple solutions?** No. beta * |epsilon| * z = 1.91 < 4, so we are above the critical temperature. All initial conditions (0.01 through 0.99) converge to the same unique fixed point.

2. **Could z_h and z_v enter differently?** No. With a single epsilon, all neighbor interactions are identical. The mean-field effective field is simply z_total * epsilon * <n>.

3. **Sign convention check:** epsilon < 0 (attractive) + mu > 0 => occupancy > 0.5. Result of 0.848 is consistent. The opposite sign convention would give 0.358, which contradicts the physics (attractive interactions should enhance occupation).

4. **Multilayer = BET?** No. The problem states n_i in {0,1} per site, confirming standard lattice gas, not BET-type multi-occupation. "Multilayer" only means the lattice extends vertically.

### Grand partition function (for completeness)

ln Z = N * ln(xi) + N * beta * epsilon * z_total * <n>^2 / 2

where xi = 1 + exp(1.71974) = 6.5830...

The second term corrects for double-counting of pair interactions in the mean-field decomposition.

---

PLAN: (1) z_total = z_h + z_v = 12; (2) Write mean-field self-consistency <n> = 1/(1+exp(z*beta*eps*<n> - beta*mu)); (3) Solve iteratively with beta*eps = -1/(2pi), beta*mu = 0.1 END_PLAN

ANSWER: 0.848
