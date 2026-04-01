# Q3 — 2D Exciton Rydberg Energy (Opus, Run 1, Hybrid M2+M4)

## PHASE 1 — PLAN

### Constraint/Entity Extraction

1. **System**: 2D semiconductor with a simple screened Coulomb potential.
2. **Band gap**: E_gap = 3 eV.
3. **1s exciton resonance peak**: Located at 1 eV (this is the photon energy or spectral position of the 1s absorption peak).
4. **Target**: Find the Rydberg energy for n = 3.

### Key Physics: 2D Exciton Energy Levels

For a 2D hydrogen-like exciton (with screened Coulomb potential), the binding energies follow:

$$E_n^{binding} = \frac{R_y}{(n - 1/2)^2}$$

where R_y is the exciton Rydberg energy, and n = 1, 2, 3, ...

The resonance peak (absorption energy) for the nth state is:

$$E_n^{resonance} = E_{gap} - E_n^{binding} = E_{gap} - \frac{R_y}{(n - 1/2)^2}$$

### Relationships

- For n = 1: E_1^{resonance} = E_gap - R_y / (1 - 0.5)^2 = E_gap - R_y / 0.25 = E_gap - 4 R_y
- The 1s resonance peak is at 1 eV: E_gap - 4 R_y = 1 eV
- Given E_gap = 3 eV: 3 - 4 R_y = 1, so R_y = 0.5 eV

### Shortest Path (3 steps)

1. Use the 2D exciton binding energy formula: E_n^{binding} = R_y / (n - 1/2)^2
2. From the 1s resonance condition, extract R_y: R_y = (E_gap - E_1^{resonance}) / 4
3. Apply the formula for n = 3 to get the Rydberg energy at n = 3.

---

## PHASE 2 — SOLVE

### Step 1: Extract R_y from the 1s exciton data

The 1s exciton resonance peak is the energy at which the n=1 exciton absorbs light:

E_1^{resonance} = E_gap - E_1^{binding}

For 2D excitons:

E_1^{binding} = R_y / (1 - 1/2)^2 = R_y / (1/2)^2 = R_y / (1/4) = 4 R_y

So:

1 eV = 3 eV - 4 R_y
4 R_y = 3 - 1 = 2 eV
**R_y = 0.5 eV**

### Step 2: Compute the n = 3 binding/Rydberg energy

For n = 3:

E_3^{binding} = R_y / (3 - 1/2)^2 = 0.5 / (2.5)^2 = 0.5 / 6.25 = **0.08 eV**

### Opposite-check / Sanity checks

- **Could the question mean something different by "Rydberg energy for n=3"?** The term "Rydberg energy" sometimes refers to the fundamental constant R_y itself (which is 0.5 eV here and independent of n). However, in context, "for n = 3" most naturally means "the binding energy of the n = 3 state" as computed from the Rydberg series formula. The phrasing "Rydberg energy for n = 3" specifically asks for the energy level within the Rydberg series at quantum number 3.
- **3D vs 2D formula check**: In 3D, binding goes as R_y/n^2. In 2D, it's R_y/(n-1/2)^2. The problem specifies 2D, so I use the 2D formula. Confirmed.
- **Is the 1 eV the binding energy or the resonance position?** The problem says "resonance peak for the 1s exciton is 1 eV." A resonance peak refers to the spectral position (absorption energy), not the binding energy directly. So E_1^{resonance} = 1 eV, and the binding energy is E_gap - E_1^{resonance} = 2 eV. This is consistent with my calculation.
- **Surface pattern check**: Nothing misleading — the problem is straightforward once the 2D formula is applied correctly.

### Final Answer

The Rydberg energy for n = 3 is:

**E_3 = 0.08 eV**

---

## Summary

| Quantity | Value |
|---|---|
| Band gap | 3 eV |
| 1s resonance peak | 1 eV |
| 1s binding energy | 2 eV |
| Exciton Rydberg constant R_y | 0.5 eV |
| n = 3 binding energy (2D) | 0.08 eV |
