# Q8 — Mean-Field Lattice Gas Adsorption: Hybrid M2+M4 Meta-Plan

## PHASE 1 — PLAN

### Constraint Extraction

**Entities:**
- 2D lattice gas adsorption system with N sites
- Each site: occupied (n_i = 1) or empty (n_i = 0)
- Multilayer adsorption allowed (3D structure: multiple layers stacked)

**Given parameters:**
- Interaction energy: epsilon = -(k_B T)/(2 pi)
- Chemical potential: mu = 0.1 k_B T
- Horizontal coordination number: z_h = 4 (in-plane neighbors)
- Vertical coordination number: z_v = 8 (interlayer neighbors)
- Temperature: T = 300 K

**Framework:** Grand canonical ensemble + mean-field approximation.

**Target:** Average occupancy per site <n>, rounded to 3 decimal places.

### Shortest Path to Answer (3 steps)

1. **Identify total coordination number:** z_total = z_h + z_v = 12 (mean-field treats all neighbors equivalently when there is a single interaction energy epsilon).

2. **Write the mean-field self-consistency equation:** In a lattice gas under mean-field, each site sees an effective field from z neighbors replaced by <n>. The occupancy follows a Fermi-like distribution:
   <n> = 1 / (1 + exp(beta * (z_total * epsilon * <n> - mu)))

3. **Express in dimensionless units and solve:** Since beta * epsilon = -1/(2 pi) and beta * mu = 0.1, the equation becomes:
   <n> = 1 / (1 + exp(12 * (-1/(2 pi)) * <n> - 0.1))
   Solve iteratively for <n>.

---

## PHASE 2 — SOLVE

### Step 1: Total coordination number

In a multilayer lattice gas with a single interaction energy epsilon, the mean-field approximation sums over all nearest neighbors regardless of direction. The total coordination number is:

z_total = z_horizontal + z_vertical = 4 + 8 = 12

### Step 2: Mean-field self-consistency equation

The lattice gas Hamiltonian is:
H = epsilon * sum_{<ij>} n_i n_j - mu * sum_i n_i

In mean-field approximation, replace neighbors by their average. For a single site i, the effective single-site Hamiltonian is:
H_i^{eff} = (epsilon * z_total * <n> - mu) * n_i

The single-site grand partition function is:
xi = sum_{n_i=0,1} exp(-beta * H_i^{eff}) = 1 + exp(-beta * (epsilon * z_total * <n> - mu))

The average occupancy is:
<n> = exp(-beta*(epsilon * z_total * <n> - mu)) / xi
    = 1 / (1 + exp(beta * (epsilon * z_total * <n> - mu)))

### Step 3: Dimensionless form and numerical solution

Define dimensionless quantities:
- beta * epsilon = epsilon / (k_B T) = -1/(2 pi) ~ -0.159155
- beta * mu = mu / (k_B T) = 0.1

The self-consistency equation becomes:
<n> = 1 / (1 + exp(12 * (-1/(2 pi)) * <n> - 0.1))

Iterative solution (starting from <n> = 0.5, converges in ~25 iterations):

| Iteration | <n>        |
|-----------|------------|
| 0         | 0.5        |
| 1         | 0.8126     |
| 5         | 0.8478     |
| 10        | 0.8481     |
| 25        | 0.84809582 |

Self-consistency check:
- Exponent = 12 * (-0.159155) * 0.84810 - 0.1 = -1.7197
- exp(-1.7197) = 0.1791
- 1/(1 + 0.1791) = 0.8481 (matches)

The solution is unique (verified with initial guesses from 0.01 to 0.99 -- all converge to the same value).

### Exclusion checks (Phase 2 discipline)

1. **Opposite reading check:** Could z_h and z_v enter the equation differently (e.g., with different interaction energies)? No -- the problem specifies a single epsilon. In mean-field with one interaction energy, all neighbors are treated identically, so z_total = z_h + z_v is correct.

2. **Surface pattern check:** Could "multilayer adsorption" imply BET-type physics where a site can hold multiple particles? No -- the problem explicitly states "each site can be occupied by a single particle or remain empty," confirming a lattice gas (n_i in {0,1}). Multilayer simply means the lattice has vertical extent.

3. **Sign convention check:** epsilon < 0 means attractive interactions. Combined with positive mu, this correctly predicts <n> > 0.5 (sites prefer to be occupied).

### Grand partition function

For completeness, the full N-site grand partition function in mean-field is:
ln Z = N * ln(xi) + N * beta * epsilon * z_total * <n>^2 / 2

where xi = 1 + exp(-beta*(epsilon * z_total * <n> - mu)) = 1 + exp(1.7197) ~ 6.583

The second term corrects for double-counting of interactions in the mean-field decomposition.

---

## ANSWER

**<n> = 0.848**
