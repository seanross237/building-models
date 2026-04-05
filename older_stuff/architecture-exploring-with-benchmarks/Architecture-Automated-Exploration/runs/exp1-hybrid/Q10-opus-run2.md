# Q10 — Sintering / Coarsening Gas — Opus Run 2 (Hybrid M2+M4)

## PLAN

**Extracted constraints/entities/rules:**
1. System: ceramic oxide sintering with chloride impurity
2. Mechanism: chloride volatilizes → "coarsening gas" trapped in pores → internal pressure opposes densification
3. Key physics: gas-filled pores resist shrinkage, coarsen, and can cause bloating; gas escapes more easily near surfaces (short diffusion path) than in interior (long path)
4. Task: find the UNLIKELY effect

**Shortest path (3 steps):**
1. Coarsening gas = volatilized chloride creating internal gas pressure in closed pores
2. Screen each option against trapped-gas physics — A, B, C, E, F are all standard documented consequences
3. Option D (larger grains in interior) contradicts the mechanism: gas-filled pores in the interior inhibit grain growth there via pore drag, while near the surface gas escapes and grains grow freely → the real gradient is opposite to D's claim

END_PLAN

## SOLVE

- **A (higher heating rate → lower density):** LIKELY — fast heating closes surface porosity before gas escapes, trapping it inside. Well-documented.
- **B (de-densification atmosphere-dependent):** LIKELY — coarsening gas may dissolve into some atmospheres but not others (e.g., vacuum vs. inert gas). Classic observation.
- **C (large random voids):** LIKELY — trapped gas causes pore coarsening and bloating → randomly distributed large voids.
- **D (larger grains interior vs. surface):** UNLIKELY — coarsening gas is trapped preferentially in the interior (long diffusion path to surface). Gas-filled pores exert pore drag that retards grain growth. Near the surface, gas escapes, pores shrink, and grains grow freely. The expected gradient is larger grains near the surface, smaller in the interior — the opposite of D.
- **E (cracking):** LIKELY — rapid gas evolution generates internal stresses sufficient to crack the part.
- **F (higher green density → lower sintered density):** LIKELY — higher green density means smaller pores that close earlier in sintering, trapping gas sooner before it can vent through open porosity. A well-known paradoxical effect.

## ANSWER

**D**
