# Q3 — 2D Exciton Rydberg Energy (Opus Run 2, Hybrid M2+M4)

## PLAN

**Constraints & entities extracted:**
- 2D semiconductor, band gap E_g = 3 eV
- Simple screened Coulomb potential
- 1s exciton resonance peak at 1 eV (photon energy of absorption peak)
- 2D exciton binding energy formula: E_b(n) = E_Ry / (n - 1/2)^2
- Need: binding energy at n = 3

**Shortest path (3 steps):**
1. E_b(1s) = E_g - E_resonance = 3 - 1 = 2 eV
2. E_Ry = E_b(1s) / 4 = 0.5 eV (since for n=1, denominator = (0.5)^2 = 0.25, so E_b = 4 E_Ry)
3. E_b(n=3) = 0.5 / (2.5)^2 = 0.5 / 6.25 = 0.08 eV

## END_PLAN

## SOLVE

**Step 1 — 1s binding energy from resonance peak:**
The exciton resonance peak is the photon energy at which the exciton absorption occurs:
E_resonance(1s) = E_g - E_b(1s) => E_b(1s) = 3 eV - 1 eV = **2 eV**

**Step 2 — Extract 2D Rydberg energy:**
In 2D, exciton binding energies follow E_b(n) = E_Ry / (n - 1/2)^2.
For n = 1: E_b(1) = E_Ry / (0.5)^2 = 4 E_Ry.
Therefore: E_Ry = 2 eV / 4 = **0.5 eV**

**Step 3 — n = 3 binding energy:**
E_b(3) = E_Ry / (3 - 1/2)^2 = 0.5 / (2.5)^2 = 0.5 / 6.25 = **0.08 eV**

**Opposite checks performed:**
1. "Rydberg energy for n=3" — could mean E_Ry itself (0.5 eV)? No: the "for n=3" qualifier specifically requests the level-dependent quantity. If they wanted the Rydberg constant, "for n=3" would be superfluous.
2. Could 1 eV be the binding energy itself? No: "resonance peak" in spectroscopy means the photon energy of the absorption peak, not the binding energy.

## ANSWER

**0.08 eV**
