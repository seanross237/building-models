# Meta-Learning: Exploration 006

## What worked well
- **Combining FDT mechanism + galaxy fits** in one exploration was efficient. The FDT closure was clear enough that it didn't crowd out the galaxy fit work.
- **Mass modeling caution**: The explorer caught its own error when the initial NGC 2403 fit gave misleading results (stellar disk only vs. total baryonic). This self-correction, prompted by the "honest assessment" requirement, prevented a false positive.
- **Chi-squared quantification** made model comparison unambiguous. cH₀ at χ²/dof ~ 130-140 is not a borderline failure.

## What didn't work
- The FDT derivation attempt was comprehensive but the negative result was somewhat predictable — the FDT at equilibrium should give no modification by construction. A non-equilibrium formulation might be more promising but requires more setup.

## Lessons
1. **Require consistent baryonic mass modeling.** Galaxy rotation curve fits are meaningless without proper mass accounting (gas + stars). Always include both components or use BTFR-consistent masses.
2. **The FDT is the wrong tool for this problem.** At equilibrium, χ'' is determined by the KMS condition, which is satisfied for any temperature. The modification (if any) must come from non-equilibrium physics. Future explorations should focus on non-equilibrium scenarios.
3. **Quantify model comparisons with χ².** "The curve looks similar" is insufficient. χ²/dof gives a clean verdict.
