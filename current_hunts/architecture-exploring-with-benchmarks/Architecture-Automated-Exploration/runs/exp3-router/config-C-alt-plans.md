# Config C — Alternate Plans (Haiku routed differently than Opus)

These plans use the mode Haiku selected, not the mode Opus selected.
The question is: does the alternate mode's plan structure lead to a worse, equal, or better answer?

---

## Q4 — Freely Jointed Chain Force Law

**Opus routed:** COMPUTATION (M4)
**Haiku routed:** DISCRIMINATION (M2)
**This plan uses:** M2

### Question
Freely jointed chain polymer, n masses joined by struts of length l, thermally isolated. What is the force law between ends? Answer may involve x, l, n, E(0). n is large.

### Plan (M2 — DISCRIMINATION)

PLAN:
1. **Extract entities.** Freely jointed chain: n masses, struts of length l, end-to-end distance x. Thermally isolated = microcanonical ensemble. Energy E(0) is reference/total energy. n is large (thermodynamic limit applies).
2. **Extract constraints and rules.**
   - Constraint C1: Each link has fixed length l (rigid struts, no potential energy stored in bonds).
   - Constraint C2: System is thermally isolated — total energy E is conserved, entropy is maximized at equilibrium. Must use microcanonical formalism, not canonical.
   - Constraint C3: n is large — Gaussian approximation for end-to-end distribution is valid.
   - Constraint C4: Force is the conjugate variable to the end-to-end distance x in the microcanonical ensemble: F = -T (dS_config/dx), where T comes from the kinetic entropy.
   - Constraint C5: The answer must be expressed in terms of x, l, n, E(0) only — no temperature T or Boltzmann constant k may remain in the final expression.
3. **Identify dependencies.**
   - Independent: C1 (chain geometry), C3 (Gaussian statistics for configuration space).
   - Dependent on C1+C3: configurational entropy S_config(x). The Gaussian end-to-end distribution gives S_config = const - 3kx^2/(2nl^2).
   - Dependent on C2: microcanonical temperature. From kinetic degrees of freedom: 1/T = dS_kin/dE_kin = (3n/2)k / E_kin, so kT = 2E_kin/(3n).
   - Dependent on C4 + previous: force formula F = -T dS_config/dx = 3kTx/(nl^2).
   - Dependent on C5: substitute kT to eliminate temperature, express in terms of E(0).
4. **Resolve independent constraints first.**
   - From C1+C3: S_config(x) = const - 3kx^2/(2nl^2). [Gaussian random walk, resolved independently of energy considerations.]
   - From C2: identify E_kin = E(0) (if E(0) is the total energy and struts store no potential energy, all energy is kinetic). If E(0) is ground-state energy and E is total, then E_kin = E - E(0). Microcanonical temperature: kT = 2(E - E(0))/(3n).
5. **Resolve dependent constraints.**
   - From C4: F = -T dS_config/dx = 3kTx/(nl^2).
   - From C5: substitute kT = 2(E - E(0))/(3n) to get F = 2(E - E(0))x / (n^2 l^2).
   - This is a linear (Hookean) restoring force. The "spring constant" is 2(E - E(0))/(n^2 l^2).
END_PLAN

---

## Q5 — Rhombohedral Perovskite Bragg Reflections

**Opus routed:** DISCRIMINATION (M2)
**Haiku routed:** COMPUTATION (M4)
**This plan uses:** M4

### Question
Rhombohedral R3m perovskite, pseudocubic indexing. How many Bragg reflections for {200}, {220}, {222}?

### Plan (M4 — COMPUTATION)

PLAN:
1. Cubic {hkl} family sizes under m3m: {200} has 3 distinct reflections, {220} has 6, {222} has 4 (after Friedel equivalence). The rhombohedral distortion along [111] reduces point symmetry from m3m to 3m, splitting each cubic family into orbits of the 3m subgroup.
2. Count the split peaks. The 3m group preserves the 3-fold axis along [111] and mirror planes containing [111]. Apply this to each family:
   - {200}: the three cubic faces (100), (010), (001) are no longer equivalent. Under 3m, the [111] axis relates them as a single orbit of size 3 — but since a rhombohedral distortion makes [111] the unique axis, the (100)/(010)/(001) triple forms one orbit (3 equivalent directions). So {200} gives 1 peak (multiplicity 3).
   - {220}: the 6 face-diagonal directions split. Under 3m, (110)/(011)/(101) form one orbit of size 3, and (1-10)/(01-1)/(10-1) form another orbit of size 3. So {220} gives 2 peaks.
   - {222}: the 4 body-diagonal directions: (111) is the unique axis direction, so it is a singlet. The other 3 — (-111), (1-11), (11-1) — form one orbit of size 3. So {222} gives 2 peaks.
3. Check R-centering extinctions. The R3m R-centering condition (in hexagonal axes: -h+k+l = 3n) may extinguish some of these peaks. Convert each pseudocubic reflection to rhombohedral/hexagonal indices and test. For the families listed, R-centering does not produce additional extinctions beyond the splitting — all split peaks survive.
4. Final count: {200} -> 1, {220} -> 2, {222} -> 2. Total across all three families: 5 Bragg reflections.
END_PLAN
