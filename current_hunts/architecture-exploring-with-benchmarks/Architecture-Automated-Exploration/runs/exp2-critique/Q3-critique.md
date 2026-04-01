# Q3 Critique — 2D Exciton Rydberg Energy

## VERDICT: CORRECTED

## Issues Found

### ISSUE 1: Ambiguous target quantity — plan doesn't resolve what "Rydberg energy for n=3" means (MODERATE)

The question asks for "the Rydberg energy for n = 3." This is ambiguous between three interpretations:

- **(a) The binding energy of the n=3 state:** E_3^(bind) = R_y / (n - 1/2)^2 = 0.5 / 6.25 = 0.08 eV
- **(b) The spectral position (photon energy) of the n=3 resonance:** E_gap - E_3^(bind) = 3 - 0.08 = 2.92 eV
- **(c) The material's exciton Rydberg constant R_y itself:** 0.5 eV (same for all n)

The most natural reading of "Rydberg energy for n=3" is **(a)**, the binding energy of the n=3 Rydberg state. The plan computes 0.5/6.25 but never states the final numerical answer (0.08 eV) and never explicitly declares which interpretation it is answering. This risks delivering a number without confirming it answers the right question.

### ISSUE 2: Plan does not state the final numerical answer (MINOR)

Step (2) writes E_3 = 0.5/6.25 but stops there. The plan should explicitly compute **0.08 eV** (or equivalently 80 meV). Leaving the answer as a fraction invites arithmetic slip during execution.

### ISSUE 3: Sign convention not resolved (MINOR)

The plan's step (3) flags sign convention but doesn't resolve it. Convention: binding energies are positive (energy to ionize). The energy *level* relative to the continuum would be -0.08 eV. Since the question says "Rydberg energy" (not "energy level"), the positive convention (0.08 eV) is correct. The plan should commit to this rather than leaving it as a check item.

### ISSUE 4: Screened Coulomb caveat (NEGLIGIBLE / Flag only)

The problem specifies "simple screened Coulomb potential." The 2D hydrogen formula E_n = R_y/(n-1/2)^2 is exact for the *unscreened* Coulomb potential. For truly screened (e.g., Keldysh/Rytova) potentials, the Rydberg series deviates — higher-n states are more weakly bound than the hydrogenic formula predicts. However, the problem clearly intends us to use the standard formula (the word "simple" signals this, and the numbers are chosen to work out cleanly). Not an error, but worth noting that in real 2D materials this formula would be approximate.

## What the Plan Gets Right

- **Formula:** E_n = R_y / (n - 1/2)^2 is the correct 2D exciton binding energy spectrum. Correct.
- **R_y extraction:** E_gap - 4R_y = 1 eV gives R_y = (3 - 1)/4 = 0.5 eV. Correct.
- **n=3 denominator:** (3 - 1/2)^2 = (5/2)^2 = 6.25. Correct.
- **Resonance peak interpretation:** The plan correctly identifies that the 1s resonance peak at 1 eV is the *spectral position* (photon energy), not the binding energy. This is the key physics insight and the plan handles it correctly.

## FINAL PLAN

1. **Identify the 2D exciton binding formula:** E_n^(bind) = R_y / (n - 1/2)^2, where n = 1, 2, 3, ...
2. **Extract R_y from the 1s resonance condition:** The 1s resonance peak appears at photon energy E_1 = E_gap - E_1^(bind) = E_gap - 4R_y. Setting 3 - 4R_y = 1 gives **R_y = 0.5 eV**.
3. **Compute the n=3 binding energy:** E_3^(bind) = R_y / (3 - 1/2)^2 = 0.5 / (2.5)^2 = 0.5 / 6.25 = **0.08 eV**.
4. **Sign convention:** Report as positive 0.08 eV (binding energy convention; energy required to ionize the n=3 exciton to the continuum).
5. **Sanity check:** The n=3 state should be much more weakly bound than n=1 (which has binding energy 4 x 0.5 = 2 eV). Indeed 0.08 << 2. The corresponding resonance peak would be at 3 - 0.08 = 2.92 eV, close to the band edge as expected for a high-n Rydberg state. Consistent.

**Answer: 0.08 eV**
