# Exploration 006: Analyticity Reconciliation — Can QG+F's Analyticity Sacrifice Coexist with AS?

## Mission Context

We are testing the conjecture that QG+F and Asymptotic Safety are the same UV-complete theory. Scorecard: 0 FALSIFIED, 2 SUPPORTS (inflation, BH), 2 INCONCLUSIVE (fixed points, ghost fate). This is the final prosecution exploration — testing the hardest implication.

## Your Specific Goal

**ONE QUESTION:** Can QG+F's sacrifice of S-matrix analyticity be reconciled with AS's computational framework, which operates via Euclidean functional RG?

### Why this matters

QG+F is unique among ALL quantum gravity approaches in forfeiting S-matrix analyticity (Anselmi et al. JHEP 2025, arXiv:2503.01841). The fakeon prescription preserves unitarity + Lorentz invariance but breaks analyticity — no dispersion relations, no S-matrix bootstrap, no standard Euclidean↔Lorentzian Wick rotation. Anselmi (2026, arXiv:2601.06346) goes further: causality should be abandoned as fundamental.

If QG+F = AS, this creates a tension:
- QG+F says: no analyticity, no Wick rotation, causality is emergent
- AS (functional RG) typically: operates in Euclidean signature, uses analytic continuation
- These seem contradictory

**But is the contradiction real?** Investigate:

1. **Does AS actually require analyticity?** The Wetterich equation (functional RG) is formulated in Euclidean signature. Does it require the action to have standard analytic properties? Or can it accommodate non-analytic form factors?

2. **Does the Draper et al. complex pole tower break analyticity?** The complex pole towers found in AS graviton propagators (Draper, Knorr et al. 2020) — are these consistent with standard S-matrix analyticity, or do they violate it? If the AS propagator already has non-standard analytic properties, the tension dissolves.

3. **Is the Euclidean formulation of AS just a computational tool?** The FRG can be formulated in Lorentzian signature (Lorentzian AS, causal FRG). If so, the Euclidean formulation is an approximation, not a requirement, and analyticity isn't fundamental to AS either.

4. **What does the fakeon do to Wick rotation?** Anselmi has shown that the fakeon prescription modifies Wick rotation (it's not the standard one). Is this modification compatible with how AS handles the Euclidean→Lorentzian transition?

5. **Platania & Wetterich's fictitious ghosts (2020):** They discuss non-perturbative unitarity and ghost handling in AS. Do they require or assume analyticity?

**Give a verdict:**
- **SUPPORTS:** AS does not require standard analyticity, or its analytic structure is already non-standard in ways compatible with the fakeon
- **FALSIFIES:** AS fundamentally requires analyticity in a way incompatible with the fakeon prescription
- **INCONCLUSIVE:** The question hasn't been addressed in the literature

## Pre-loaded Context

**QG+F analyticity (from library):**
- The 4-prescription trade-off (Anselmi et al. JHEP 2025): only the fakeon prescription preserves unitarity + Lorentz invariance, but sacrifices analyticity
- No dispersion relations → no S-matrix bootstrap
- No standard Euclidean-Lorentzian connection
- Anselmi's radical position (2026): causality should be abandoned as fundamental; maximum achievable is "delayed prepostdictions"
- QG+F stands alone among major QG approaches in renouncing analyticity

**AS computational framework:**
- Wetterich equation: Euclidean functional RG, integrates out modes shell-by-shell in momentum
- Typically formulated in Euclidean signature
- Lorentzian formulations exist but are less developed
- Draper et al. (2020): complex pole towers in AS graviton propagator → compatible with unitarity

**Key authors to search:** Anselmi (analyticity sacrifice), Platania (AS + higher derivatives), Wetterich (functional RG foundations), Knorr (form factors in AS), Draper (complex poles), Manrique & Reuter (Lorentzian FRG), D'Angelo & Pawlowski (Lorentzian AS).

## Success Criteria
- Determine whether AS requires standard analyticity or can accommodate its violation
- Check if AS's own propagator structures already show non-standard analytic properties
- Clear verdict with evidence. 150-300 lines.

## Output
- `explorations/exploration-006/REPORT.md` (write incrementally every 3-4 searches)
- `explorations/exploration-006/REPORT-SUMMARY.md` (write LAST)
