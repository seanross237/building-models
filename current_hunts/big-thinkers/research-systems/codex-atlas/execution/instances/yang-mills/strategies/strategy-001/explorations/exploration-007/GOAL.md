# Exploration 007: Novelty Search — Finite Group Approximation in Lattice Gauge Theory

## Mission Context

This is a YANG-MILLS Millennium Prize Problem mission. Our exploration 005 produced a computational study of how lattice gauge theory observables (plaquettes, Wilson loops, Creutz ratios, string tension) converge as finite subgroups of SU(2) approach SU(2). The key findings that may be novel:

1. **Quantitative convergence rates**: |obs_G - obs_SU(2)| ~ |G|^{-α} with α ≈ 0.7-2.5 depending on observable
2. **Phase transition scaling**: Bulk first-order transition at β_c ~ |G|^{0.6} for the binary polyhedral subgroups (2T at β≈2.2, 2O at β≈3.2, 2I at β≈5.8)
3. **Hysteresis weakening**: Jump in plaquette decreases 0.39→0.18→0.09 as |G| increases
4. **Accuracy**: Binary icosahedral group (120 elements) matches SU(2) to <0.5% for all observables

We also found (exploration 006) that Adhikari-Cao (2025) proved mass gap for finite gauge groups using a "swapping map" technique, and that the finite→continuous barrier has 4 structural layers.

## Your Task

**Determine whether our finite-group convergence results are novel or already known.** This is a LITERATURE SEARCH, not computation.

## Specific Searches

### 1. Finite subgroup lattice gauge theory — prior art
Search for papers that study lattice gauge theory with discrete/finite gauge groups as approximations to continuous Lie groups. Key search terms:
- "finite subgroup" + "lattice gauge theory"
- "discrete gauge group" + "continuum limit"
- "binary icosahedral" + "gauge theory"
- "lattice gauge theory" + "group approximation"
- Authors who have worked on this: Bhanot, Creutz, Petcher, Halliday, Schwimmer, and anyone else you find

### 2. Phase transition structure
Search for known results about bulk phase transitions in lattice gauge theories with finite gauge groups:
- The β_c dependence on group size
- First-order vs. second-order nature
- Whether the β_c ~ |G|^{0.6} scaling is known
- Results for specific groups (2T, 2O, 2I in SU(2) gauge theory)

### 3. Convergence rates
Has anyone previously measured:
- How fast lattice gauge theory observables converge as the discrete group approximates the continuous group?
- The power-law exponent α in |G|^{-α} convergence?
- Whether different observables converge at different rates?

### 4. Adhikari-Cao connection
Has anyone studied:
- How Adhikari-Cao's finite-group mass gap bounds behave as |G| → ∞?
- Whether their bounds converge to a finite value for the continuous group?
- The spectral gap Δ_G of the Laplacian on finite subgroups of SU(2)?

### 5. Related mathematical work
- Approximation of Lie groups by finite subgroups (representation theory perspective)
- Convergence of integrals over finite groups to Haar integrals
- Rate of approximation of SU(2) by its finite subgroups

## Success Criteria
- For each of our 4 potentially novel findings, state whether it is: KNOWN (cite paper), PARTIALLY KNOWN (related work exists but not this specific result), or APPEARS NOVEL (no prior art found after thorough search)
- At least 5 relevant prior papers identified and summarized
- An honest assessment of whether our results would be publishable

## Failure Criteria
- Incomplete search (only checked one database)
- No specific citations for known results
- No clear assessment of novelty for each finding

## Output
- `REPORT.md` (target 300-500 lines)
- `REPORT-SUMMARY.md` (50-100 lines)

Write REPORT-SUMMARY.md as your FINAL action.
