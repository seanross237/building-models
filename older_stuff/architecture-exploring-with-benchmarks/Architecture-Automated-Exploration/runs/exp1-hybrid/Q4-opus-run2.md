# Q4 — Polymer (Opus Run 2, Hybrid M2+M4)

## PLAN

**Entities & Constraints extracted:**
- Freely jointed chain: n identical mass points, massless struts of length l
- No forces other than constraint forces => no potential energy, only kinetic energy
- Isothermal case (given): F proportional to T and linear in x (small x, slow changes)
- Question: force law when thermally ISOLATED (adiabatic, no heat exchange)
- Available variables: x, l, n, E(0) = kinetic energy at zero extension
- n is large

**Shortest path (3 steps):**
1. Write the known isothermal entropic force law for a freely jointed chain: F = -3kTx/(nl^2)
2. Count DOF (3n - n = 2n for large n), use equipartition to express T = E/(nk), eliminating T in favor of kinetic energy
3. For adiabatic process (dE = F dx), solve the resulting ODE dE/E = -3x dx/(n^2 l^2) to get E(x), then substitute back into F

END_PLAN

## SOLVE

### Step 1 — Isothermal force law

For a freely jointed chain (3D Gaussian random walk), the configurational entropy as a function of end-to-end separation x:

S(x) = S_0 - 3kx^2 / (2nl^2)

The entropic restoring force at constant T:

F_isothermal = T (dS/dx) = -3kTx / (nl^2)

This matches the given: proportional to T, linear in x.

### Step 2 — Replace T with kinetic energy

Degrees of freedom: n mass points in 3D = 3n. Subtract (n-1) ~ n rigid-rod constraints (large n). So f = 2n effective DOF.

By equipartition: E = (f/2)kT = nkT, hence T = E/(nk).

The force becomes: F = -3x E(x) / (n^2 l^2)

### Step 3 — Adiabatic energy conservation

Thermally isolated: dE = F dx (first law with delta Q = 0).

dE/dx = -3x E / (n^2 l^2)

Separate and integrate:

dE/E = -3x dx / (n^2 l^2)

ln[E(x)/E(0)] = -3x^2 / (2n^2 l^2)

E(x) = E(0) exp[-3x^2 / (2n^2 l^2)]

Substituting back:

**F(x) = -(3E(0)x / (n^2 l^2)) exp[-3x^2 / (2n^2 l^2)]**

### Verification

- At x = 0: F = 0 (correct, no restoring force at zero extension)
- For small x: exponential -> 1, so F ~ -3E(0)x/(n^2 l^2) = -3kT(0)x/(nl^2), recovering the isothermal result with T = E(0)/(nk). Consistent.
- Physical interpretation: adiabatic stretching costs kinetic energy (the polymer cools), reducing the effective temperature and making the restoring force weaker than the isothermal case at large extensions. The exponential factor captures this cooling.

## ANSWER

F(x) = -(3 E(0) x) / (n^2 l^2) * exp(-3x^2 / (2 n^2 l^2))
