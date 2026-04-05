# Q4 — Polymer (Freely Jointed Chain, Adiabatic Force Law)
## Hybrid M2+M4 Meta-Plan | Opus Run 1

---

## PHASE 1 — PLAN

### Extracted Constraints, Entities, Rules, Relationships

**Entities:**
- Freely jointed chain: n identical mass points, (n-1) massless rigid struts of length l
- No forces except constraint forces from struts (purely kinetic energy, no potential)
- Thermal reservoir at temperature T (isothermal case, given)
- Thermally isolated polymer (adiabatic case, asked)

**Given rules:**
- Isothermal force: F proportional to T and linear in x (for small, slowly changing x)
- This is the standard entropic spring: F = -3kTx/(nl^2)
- E(0) = kinetic energy of polymer at zero extension
- n is large

**Key relationships:**
- Energy is purely kinetic (no potential in this model)
- Degrees of freedom: 3n coordinates minus (n-1) rigid-rod constraints minus 3 (fix one end) = 2n-2. For large n, f ~ 2n.
- Equipartition: E = (f/2)kT ~ nkT for large n
- Configurational entropy: S_config = S_0 - 3kx^2/(2nl^2) (Gaussian random walk)

**Shortest path to answer (3 steps):**
1. Write the total entropy as kinetic + configurational parts
2. Impose dS = 0 (adiabatic) to find T(x), then get E(x)
3. Compute F = -dE/dx and express in terms of E(0), x, n, l

---

## PHASE 2 — SOLVE

### Step 1: Entropy decomposition

The freely jointed chain has no potential energy. The total entropy separates into:
- **Configurational entropy** (from end-to-end distance x): For a random walk of n steps of length l, the number of configurations for small x gives S_config(x) = const - 3kx^2/(2nl^2)
- **Kinetic entropy** (from momenta): With f ~ 2n quadratic kinetic degrees of freedom, S_kinetic = (f/2)k ln(T) + const = nk ln(T) + const (for large n)

Total: S(x, T) = nk ln(T) - 3kx^2/(2nl^2) + const

### Step 2: Adiabatic constraint (dS = 0) gives T(x)

Setting dS = 0:

nk (dT/T) - 3kx dx/(nl^2) = 0

dT/T = 3x dx/(n^2 l^2)

Integrating from (x=0, T=T_0) to (x, T):

ln(T/T_0) = 3x^2/(2n^2 l^2)

T(x) = T_0 exp(3x^2/(2n^2 l^2))

The energy: E(x) = nkT(x) = nkT_0 exp(3x^2/(2n^2 l^2)) = E(0) exp(3x^2/(2n^2 l^2))

where E(0) = nkT_0 is the kinetic energy at zero extension.

### Step 3: Adiabatic force

F = -dE/dx = -E(0) * (3x/(n^2 l^2)) * exp(3x^2/(2n^2 l^2))

**For small x** (the regime of interest, matching the isothermal statement):

F = -3E(0)x / (n^2 l^2)

### Verification

**Cross-check with isothermal case:** In thermal equilibrium, E(0) = nkT, so:
F_adiabatic = -3(nkT)x/(n^2 l^2) = -3kTx/(nl^2)

This matches the known isothermal entropic force F = -3kTx/(nl^2), confirming consistency. The leading-order adiabatic and isothermal forces agree because the temperature correction from the adiabatic constraint is O(x^2), which contributes to force only at O(x^3).

**Opposite reading check:** Could the adiabatic force be zero (no entropy change means no force)? No — the force is -(dE/dx)_S, not -(TdS/dx). Even at constant entropy, the internal energy changes with extension because the temperature must adjust to maintain dS=0, and the energy changes accordingly.

**Surface pattern check:** The result F ~ -E(0)x/(n^2 l^2) has sensible units and limits. Larger E(0) (hotter polymer) means stronger restoring force. Longer chains (larger n) or longer links (larger l) mean weaker force per unit extension, as expected for a more flexible polymer.

---

## ANSWER

$$\boxed{F = -\frac{3\,E(0)\,x}{n^2\,\ell^2}}$$

The adiabatic force law for the freely jointed chain at small extension is:

**F = -3 E(0) x / (n^2 l^2)**

where E(0) is the kinetic energy at zero extension. This is equivalent to the isothermal result F = -3kTx/(nl^2) with the replacement kT -> E(0)/n, which follows from equipartition with ~2n degrees of freedom.
