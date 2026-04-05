# C2 Results — Verify by Substitution

**Prompt:** "Solve using the fewest steps possible. After getting your answer, SUBSTITUTE it back into the original equation or constraint to verify it satisfies everything. Also check: does dimensional analysis confirm the form? Do limiting cases work? If verification fails, your answer is wrong — find the error before reporting."

**Guidance:** "Default to EXCLUSION. Ground claims in evidence. Consider the OPPOSITE."

---

## Q3: 2D Semiconductor Exciton — Rydberg Energy for n=3

**Setup:** Band gap 3 eV, screened Coulomb potential, 1s exciton resonance peak at 1 eV. Find the Rydberg energy for n=3.

**Solution:**

In the 2D hydrogen model, the exciton binding energy for quantum number n is:

$$E_n^{bind} = \frac{R_y}{(n - 1/2)^2}$$

The resonance peak (absorption) for state n occurs at:

$$E_{peak}(n) = E_{gap} - \frac{R_y}{(n - 1/2)^2}$$

For n=1 (1s state):

$$1.0 = 3.0 - \frac{R_y}{(1/2)^2} = 3.0 - 4 R_y$$

$$R_y = \frac{3.0 - 1.0}{4} = 0.5 \text{ eV}$$

For n=3:

$$E_3^{bind} = \frac{0.5}{(3 - 0.5)^2} = \frac{0.5}{6.25} = 0.08 \text{ eV}$$

**Verification:**
- **Substitution:** E_peak(1s) = 3.0 - 4(0.5) = 1.0 eV. Matches given data. CHECK.
- **Dimensional analysis:** All quantities in eV. CHECK.
- **Limiting cases:** As n → infinity, E_n^bind → 0 and peak → E_gap = 3 eV. CHECK. Binding energies decrease monotonically: E_1 = 2.0 eV > E_2 = 0.222 eV > E_3 = 0.08 eV. CHECK.

**Answer: E_3 = 0.08 eV (binding energy of n=3 exciton)**

---

## Q4: Freely Jointed Chain — Force Law (Thermally Isolated)

**Setup:** FJC polymer with n masses, struts of length l, thermally isolated. Find force law F(x, l, n, E(0)) for n large.

**Solution:**

For a freely jointed chain in 1D with n links of length l, the configurational entropy at end-to-end distance x is (using Stirling for large n):

$$S_{config}(x) = k_B \left[ n \ln 2 - \frac{n}{2}\left((1+\xi)\ln(1+\xi) + (1-\xi)\ln(1-\xi)\right) \right]$$

where xi = x/(nl).

The force is:

$$F = -T \frac{\partial S_{config}}{\partial x} = \frac{k_B T}{\ell} \operatorname{arctanh}\!\left(\frac{x}{n\ell}\right)$$

For a thermally isolated system, all energy E(0) is kinetic (rigid struts have no configurational potential energy). With n masses in 1D, each contributing one kinetic degree of freedom:

$$E(0) = \frac{n}{2} k_B T \implies k_B T = \frac{2 E(0)}{n}$$

For n large, x/(nl) is small, so arctanh(x/(nl)) ≈ x/(nl), giving the **Hookean (linear) regime**:

$$\boxed{F = \frac{2 E(0)}{n^2 \ell^2}\, x}$$

The exact result (before the large-n linear approximation) is:

$$F = \frac{2 E(0)}{n \ell}\, \operatorname{arctanh}\!\left(\frac{x}{n\ell}\right)$$

**Verification:**
- **Substitution/dimensional analysis:** [E(0)] = J, [x] = m, [l] = m, [n] = dimensionless. F ~ J·m/m² = J/m = N. CHECK.
- **Limiting cases:**
  - x → 0: F → 0 (no stretching, no force). CHECK.
  - E(0) → 0 (T → 0): F → 0 (no thermal restoring force at zero temperature). CHECK.
  - n → infinity (fixed x): F → 0 (infinitely long chain offers no resistance to finite extension). CHECK.
  - x → nl (full extension): arctanh → infinity (infinite force to fully extend). CHECK.
- **Opposite consideration:** Could the isolated constraint change T with x? No — since rigid struts carry no configurational energy, E_kinetic = E(0) always, so T is constant. The force is purely entropic.

**Answer: F = 2E(0)x / (n²l²) for large n**

---

## Q7: 2D Lattice Adsorption — Grand Canonical Mean-Field

**Setup:** eps_1 = 0.1 k_BT, eps_l = (0.02)^k k_BT, mu = 0.15 k_BT, z_l = 4, z_inter = 4, T = 318 K. Find Z and <k>.

**Solution:**

Interpreting as a lattice gas on a lattice with two types of bonds — lateral (z_l = 4, interaction energy eps_1 = 0.1 k_BT) and interlayer (z_inter = 4, interaction energy eps_l = 0.02 k_BT) — with each site occupied or empty (n_i in {0,1}).

Note: A multilayer (column) interpretation was explored but the partition function diverges without a solid-on-solid constraint or repulsive interactions. The single-layer lattice gas is the well-posed mean-field problem.

In mean-field, each site sees an effective chemical potential enhanced by attractive neighbor interactions:

$$\mu_{eff} = \mu + (z_l \cdot \varepsilon_1 + z_{inter} \cdot \varepsilon_l) \cdot \langle n \rangle = 0.15 + 0.48 \langle n \rangle$$

Self-consistency: <n> = 1/(1 + exp(-mu_eff))

Iterating to convergence:
- mu_eff = 0.4422
- <n> = 0.6088

Single-site grand partition function:
$$Z = 1 + e^{\mu_{eff}} = 1 + e^{0.4422} = 2.556$$

**Verification:**
- **Substitution:** 1/(1 + exp(-0.4422)) = 0.6088, and exp(0.4422)/2.556 = 0.6088. Self-consistent. CHECK.
- **Dimensional analysis:** All energies in units of k_BT, occupation dimensionless. CHECK.
- **Limiting cases:**
  - No interactions (eps → 0): <n> = 1/(1+exp(-0.15)) = 0.537. With attractive interactions, <n> = 0.609 > 0.537. CHECK (attraction increases occupation).
  - mu → -infinity: <n> → 0, Z → 1. CHECK.
  - mu → +infinity: <n> → 1, Z → 1 + exp(mu). CHECK.

**Answer: Z ≈ 2.556, <k> ≈ 0.609**

---

## Q8: 2D Lattice Gas — Mean-Field Occupation

**Setup:** eps = -(k_BT)/(2pi), mu = 0.1 k_BT, z_horizontal = 4, z_vertical = 8, T = 300 K. Mean-field Hamiltonian: H = (eps/2)·z·<n>·sum(n_i). Find <n> to 3 decimal places.

**Solution:**

Total coordination: z = z_h + z_v = 4 + 8 = 12

The mean-field per-site effective field:

$$h_{eff} = \frac{\varepsilon}{2} z \langle n \rangle - \mu = \frac{-1/(2\pi)}{2} \cdot 12 \cdot \langle n \rangle - 0.1 = -\frac{3}{\pi}\langle n \rangle - 0.1$$

Self-consistency equation:

$$\langle n \rangle = \frac{1}{1 + e^{h_{eff}}} = \frac{1}{1 + \exp\!\left(-\frac{3}{\pi}\langle n \rangle - 0.1\right)}$$

Numerical iteration converges to a unique, stable solution:

$$\langle n \rangle = 0.679$$

**Verification:**
- **Substitution:** h_eff = -(3/pi)(0.6788) - 0.1 = -0.9549(0.6788) - 0.1 = -0.7482. Then 1/(1+exp(-0.7482)) = 1/(1+0.4732) = 0.6788. CHECK (self-consistent to machine precision).
- **Stability:** |dRHS/dn| = 0.208 < 1 at the solution (stable fixed point, unique solution). CHECK.
- **Dimensional analysis:** All energies in units of k_BT, <n> dimensionless. CHECK.
- **Limiting cases:**
  - No interaction (eps = 0): <n> = 1/(1+exp(-0.1)) = 0.525. With attractive interaction (eps < 0), <n> = 0.679 > 0.525. CHECK (attraction increases occupation).
  - mu → -infinity: <n> → 0. CHECK.
  - mu → +infinity: <n> → 1. CHECK.
- **Opposite check:** Could there be multiple solutions (first-order transition)? Checked numerically — only one sign change in the self-consistency function over [0,1]. The coupling strength |(eps/2)z/(k_BT)| = 3/pi ≈ 0.955 is below the critical value for the mean-field Ising transition (which is 1.0 at half-filling), so a unique solution is expected. CHECK.

**Answer: <n> = 0.679**

---

## Summary Table

| Q | Verification Result | Answer |
|---|---|---|
| Q3 | Substitution exact (1.0 eV recovered); limiting cases and dimensions pass | E_3 = 0.08 eV |
| Q4 | Dimensions [N] confirmed; all 4 limiting cases pass (x→0, E→0, n→inf, x→nl) | F = 2E(0)x/(n²l²) |
| Q7 | Self-consistency verified to machine precision; attractive interaction correctly increases occupation above non-interacting baseline | Z ≈ 2.556, ⟨k⟩ ≈ 0.609 |
| Q8 | Self-consistency to machine precision; unique stable solution confirmed; attraction increases occupation above baseline 0.525 | ⟨n⟩ = 0.679 |
