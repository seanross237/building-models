# Strategizer Reasoning Log

## Exploration 001: GUE Pair Correlation and Nearest-Neighbor Spacing

### Planning (pre-launch)

**Options considered:**
1. **Random Matrix Theory — pair correlation + spacing** (CHOSEN): The Montgomery-Odlyzko pair correlation is the foundational GUE-zeta connection. Computing it numerically establishes our baseline tooling and may reveal sub-leading corrections or finite-height deviations. Nearest-neighbor spacing is closely related and can be done in the same computation pass.
2. **Explicit formulas / Weil explicit formula**: More algebraic, harder to make computational. Better for exploration 2 after we have zero data infrastructure.
3. **Quantum chaos / semiclassical**: Requires more theoretical setup. Better after we have the statistical baseline.
4. **Moment conjectures (Keating-Snaith)**: Computationally expensive, requires zeta values on the critical line. Good for later.

**Why pair correlation first:** It's the most computationally concrete starting point. We need code that computes zeta zeros and manipulates them — this will be reused in every subsequent exploration. The pair correlation function has an exact prediction (Montgomery's conjecture) that we can test against, making success criteria unambiguous. Any deviations or sub-leading corrections would be immediately interesting.

**Scope decision:** The meta-learning warns about multi-task overload. I'm keeping this to TWO closely related statistics: pair correlation R2(x) and nearest-neighbor spacing P(s). These come from the same zero data and are conceptually one investigation ("how do zeta zeros compare to GUE at the two-point level?"). Number variance and spectral form factor will be exploration 002.

**Librarian query:** Queried the library. Factual library has zero RH content (all QG). Meta library returned 12+ useful lessons about exploration design. Key lesson: explorers need explicit instructions to write code, and formulas should be provided rather than left for the explorer to research.

### Reflection (post-completion)

**Did the explorer deliver what I asked?** Yes — pair correlation and nearest-neighbor spacing were both computed and compared to GUE predictions with quantitative error measures. The explorer also went beyond the ask by comparing against all four ensembles (Poisson, GOE, GUE, GSE) and performing KS tests.

**Was the scope right?** Slightly overambitious on computation scale. The goal asked for 10,000 zeros and high-height zeros near n=100,000 — both were infeasible with mpmath. The explorer adapted well (reducing to 2,000 low + 500 high), but I should have set more realistic computation targets.

**What would I do differently?**
- Set explicit computation time budgets ("aim for ~5 minutes of computation total")
- Ask for 1,000-2,000 zeros upfront instead of 10,000
- Skip the high-height request or make it optional
- The Wigner surmise approximation issue was predictable — should have mentioned it in the goal

**Key findings to carry forward:**
1. GUE is definitively the right universality class (Poisson 5x worse, GOE 2x worse)
2. Chi-squared/dof = 1.50 is mildly elevated — possible unfolding artifacts
3. Wigner surmise detectable at N=2000 — need exact GUE for tighter tests
4. mpmath tops out at ~2000 zeros practically; large-scale needs Odlyzko-Schonhage
5. The Riemann operator must: act on complex Hilbert space, break T-symmetry, have quadratic level repulsion

## Exploration 002: Number Variance, Spectral Rigidity, and Berry's Saturation

### Planning (pre-launch)

**Options considered:**
1. **Number variance + spectral rigidity** (CHOSEN): These are the long-range spectral statistics, complementing exploration 001's short-range results. Berry (1985) predicts that number variance saturates (deviates from GUE logarithmic growth) at a scale related to the shortest periodic orbit. This saturation IS a deviation from pure GUE and would constrain the periodic orbit structure of the Riemann operator. Most likely to produce a non-trivial finding.
2. **Explicit formulas / Weil explicit formula**: Still an option for exploration 003. Want to complete the RMT constraint catalog first.
3. **Spectral form factor K(tau)**: Closely related to number variance via Fourier transform. Could be combined with number variance, but keeping scope tight.
4. **Exact GUE spacing distribution**: Important computation (from exploration 001 leads) but more of a refinement than a new constraint.

**Why number variance now:** Berry's saturation prediction is one of the few places where we EXPECT a deviation from GUE. Pure GUE number variance grows as log(L). Berry's semiclassical prediction says it saturates at L ~ T_H (the Heisenberg time). Computing this with 2000 zeros is borderline — the saturation may only become visible at large L where we have poor statistics — but even a null result (no saturation detected) is informative.

**Scope:** Number variance + spectral rigidity (Dyson-Mehta Delta_3). Both computed from the same zero data. The spectral form factor is the Fourier transform of pair correlation, which we already have — so including it is minimal extra work. THREE statistics, all closely related long-range measures.

**Lessons applied from exploration 001:**
- Asking for 2000 zeros max (not 10,000)
- Providing all formulas explicitly
- Explicit computation time budget
- Making high-height computation optional

### Reflection (post-completion)

**Did the explorer deliver?** Yes — all three statistics computed with quantitative results. The explorer also went beyond the ask by generating a GUE simulation as a finite-size control, which was extremely valuable for separating real saturation from finite-N artifacts.

**Was the scope right?** Borderline. Three statistics in one exploration is a lot, but they're closely related enough that it worked. The report is dense but complete.

**Key findings:**
1. Berry's saturation confirmed — Sigma^2 and Delta_3 both saturate well below GUE
2. Delta_3 saturation at 0.156 is the cleanest signal (flat from L=15 to L=100)
3. Form factor ramp slope = 1.010 — GUE short-range confirmed
4. Zeta zeros are 30-50% more rigid than finite-size GUE at large L
5. Saturation onset at L~2-5 is earlier than Berry's L_max~100 estimate

**Phase pivot decision:** I'm moving to Phase 2 after just 2 Phase 1 explorations (strategy suggested 3). Rationale: We now have 10 quantitative constraints from 2 independent domains (short-range RMT and long-range RMT). The constraint catalog is rich enough to meaningfully test operator candidates. A third Phase 1 exploration on the Weil explicit formula would add one more constraint type, but Phase 2 candidate testing is likely to be more productive now. Saving the exploration budget for more Phase 2 testing (4→5 explorations) or Phase 3 adversarial checks.

## Exploration 003: Berry-Keating xp Operator — Spectrum Computation and Constraint Testing

### Planning (pre-launch)

**Options considered for first Phase 2 exploration:**
1. **Berry-Keating xp and regularizations** (CHOSEN): The most famous specific candidate for the Riemann operator. H = xp (or its regularizations) is motivated by semiclassical arguments. The spectrum can be computed for specific regularizations. Testing against our 10-constraint catalog would be the first comprehensive numerical check.
2. **Laplacians on hyperbolic surfaces**: Connected to Selberg zeta function. More technically demanding to compute spectra. Better for exploration 004.
3. **Random matrix realizations**: Generate GUE matrices and compare individual eigenvalue patterns to zeta zeros. Interesting but less specific than testing a named candidate.
4. **Toeplitz/Hankel operators from arithmetic functions**: Novel but underspecified. Need to choose which arithmetic function.

**Why Berry-Keating first:** It's the most cited candidate. If it passes our constraint catalog, that's a strong signal. If it fails specific constraints, identifying WHICH constraints it fails and by HOW MUCH would be a concrete contribution. The Sierra-Townsend and Bender-Brody-Mueller regularizations have explicit spectra that can be computed.

**Key challenge:** The raw H = xp operator doesn't have a discrete spectrum on the real line. Regularizations (boundary conditions, truncation, PT-symmetric modifications) are needed to get a discrete spectrum. The exploration needs to handle multiple regularization approaches and compare their spectra to zeta zeros.

**Scope:** ONE operator family (Berry-Keating xp), but testing MULTIPLE regularizations. Focus on getting at least one regularization's spectrum computed and tested against the full constraint catalog.

### Reflection (post-completion)
*[To be filled after exploration completes]*
