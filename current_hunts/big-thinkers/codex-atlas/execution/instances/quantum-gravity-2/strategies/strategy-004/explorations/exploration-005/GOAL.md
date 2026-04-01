# Exploration 005: Remaining Prediction Domains — Spectral Dimension, Cosmological Constant, GW

## Mission Context

The Unified QG+F–AS Framework has been systematically probed for predictions across 4 domains so far. The pattern: most predictions are consistency checks or inherited from standalone frameworks. The ONE strong lead is the NGFP-predicted R³ correction for inflation. This exploration wraps up the remaining prediction domains efficiently.

## Your Task

**Three focused questions — one per domain. For EACH, give the top 1-2 predictions with classification.**

### Domain 4: Spectral Dimension Profile d_s(E)

Both QG+F and AS independently predict d_s → 2 in the UV. The unified framework claims the FULL profile d_s(E) must match between the two descriptions.

**Question:** Is the spectral dimension profile d_s(E) an actual DISCRIMINATING prediction, or is it guaranteed to agree because both frameworks use the same action?

Compute:
- QG+F spectral dimension from the 1/p⁴ propagator: d_s = 2d/(2 + 2s) where s = 2 for the four-derivative propagator
- AS spectral dimension from η_N = -2 at the NGFP
- At INTERMEDIATE scales (E ~ M_P): do the two calculations give different profiles? Or are they automatically the same?

**Pre-loaded:** d_s → 2 is robust across ALL AS truncations because it depends only on η_N = -2. QG+F gives d_s = 2 from the 1/p⁴ propagator scaling. The transition profile between d_s = 4 (IR) and d_s = 2 (UV) is the interesting part — search for Modesto 2009, Calcagni 2013, Reuter & Saueressig 2012 spectral dimension calculations.

### Domain 6: Cosmological Constant

Neither QG+F nor AS has solved the CC problem (why Λ_obs ~ 10⁻¹²² M_P⁴).

**Question:** Does the unified framework say ANYTHING genuinely new about Λ beyond what the standalone theories say?

Check:
- AS: Λ is a running coupling at the NGFP. Does Λ flow to a specific value in the IR?
- QG+F/agravity: "old CC solved" (Λ_bare tuned once), "new CC NOT solved" (dynamical mechanism for smallness missing)
- Under unification: does the NGFP constrain Λ_IR? Does ghost confinement affect the vacuum energy? Does the running G(r) at cosmological scales provide a dark energy mechanism?
- Search for: Bonanno & Reuter 2002 cosmological running, Platania 2022 or 2023 CC in AS, Hindmarsh-Litim-Sherston 2011 CC and AS.

**Be honest:** If the unified framework has nothing new to say, state that clearly. Don't stretch.

### Domain 7: Gravitational Waves

**Question:** Does the unified framework predict any corrections to GW propagation, and are they detectable?

Check:
- Does ghost confinement affect the GW dispersion relation at sub-Planckian energies?
- Are there GW signatures of the BH phase transition at M ~ M_P (from E002: M_crit = 0.31 M_P)?
- Are there GW corrections from the running Newton's constant at cosmological scales?
- Search for: Calcagni-Kuroyanagi-Marsat-Sakellariadou-Tamanini-Tasinato (2019, JCAP) GW in QG; modifications to GW luminosity distance from AS running G.

**Pre-loaded (from library):** QG+F comprehensive non-CMB experimental catalog shows ALL signatures undetectable. QG+F is a "one-prediction theory" (r). But the unified framework's running G at cosmological scales might modify GW luminosity-distance relations — check if any group has computed this.

## Classification Rules

For EACH prediction:
- **DISCRIMINATING:** True only if unified, false if compatible-but-separate
- **NOVEL:** Neither QG+F alone nor AS alone predicts this
- **CONSISTENCY CHECK:** True if unified, also compatible with separate
- **INHERITED:** From one or both standalone theories

## Failure Path

For any domain where the unified framework has nothing genuinely new:
- State clearly: "The unified framework inherits [X] from [QG+F/AS] and adds nothing novel"
- This IS a valid finding — it tells us the framework's predictive scope

## Output

Write findings to:
- `explorations/exploration-005/REPORT.md` (200-400 lines)
- `explorations/exploration-005/REPORT-SUMMARY.md` (30-50 lines, write LAST)
