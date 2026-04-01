# Q4 Critique — Freely Jointed Chain Adiabatic Force Law

## VERDICT: APPROVED

## ISSUES: None (all flagged checkpoints pass)

---

## Detailed Audit

### (1) Degree of freedom count — CORRECT

The problem states "n identical mass points joined by massless struts of length l." This gives n mass points in 3D (3n momentum DOF) with (n-1) rigid-distance constraints, yielding 3n - (n-1) = 2n + 1 effective DOF. For large n, this is ~2n. The plan's claim of "~2n degrees of freedom" is correct.

### (2) Entropy decomposition — CORRECT

**Configurational part:** The Gaussian end-to-end distribution for a freely jointed chain with ~n links of length l gives P(x) ~ exp(-3x^2 / (2nl^2)). Taking S_config = k ln P:

S_config = -3kx^2 / (2nl^2) + const

This matches the plan exactly.

**Kinetic part:** For f ~ 2n quadratic momentum degrees of freedom, the microcanonical density of states scales as T^(f/2), giving S_kin = (f/2)k ln T + const = nk ln T + const. The plan's expression S_kinetic = nk ln(T) + const is correct.

### (3) Exponent in T(x) — CORRECT (it is 2n^2 l^2, not 2nl^2)

This was flagged as a checkpoint, and the plan gets it right. The derivation:

Setting dS_total = 0 with x_0 = 0:

nk ln(T/T_0) = 3kx^2 / (2nl^2)

ln(T/T_0) = 3x^2 / (2n^2 l^2)

The factor of n^2 arises because the configurational entropy has nl^2 in the denominator, and dividing by the nk prefactor of the kinetic term introduces a second factor of n. The plan correctly writes T = T_0 exp(3x^2 / (2n^2 l^2)).

Correspondingly, E = nkT (from equipartition with ~2n quadratic DOF), so E(x) = E(0) exp(3x^2 / (2n^2 l^2)). Correct.

### (4) Sign of force — CORRECT

F = -dE/dx. Stretching the polymer (x > 0) increases internal energy (the polymer heats up adiabatically due to reduced configurational entropy), so dE/dx > 0 and the restoring force F < 0. This is the correct entropic spring behavior.

### (5) Final coefficient — CORRECT

F = -dE/dx = -E(0) * (3x / (n^2 l^2)) * exp(3x^2 / (2n^2 l^2))

In the small-x limit: F ~ -3E(0)x / (n^2 l^2)

The coefficient 3/(n^2 l^2) is correct. No errors in the differentiation.

---

## FINAL_PLAN (unchanged — plan is approved as stated)

1. Decompose total entropy: S_config = const - 3kx^2/(2nl^2), S_kinetic = nk ln(T) + const, using ~2n DOF for large n.
2. Impose adiabatic constraint dS = 0 to get T(x) = T_0 exp(3x^2/(2n^2 l^2)), hence E(x) = E(0) exp(3x^2/(2n^2 l^2)).
3. Compute F = -dE/dx = -[3E(0)x/(n^2 l^2)] exp(3x^2/(2n^2 l^2)).

**Answer:** F(x) = -(3E(0)x / n^2 l^2) exp(3x^2 / 2n^2 l^2)
