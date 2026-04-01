# Meta-Learning Note — Strategy 002, Exploration 001
## Complex Arithmetic Matrices for GUE Statistics

### What worked:
- **Pre-loading the β=0.44 Hankel baseline and 10-constraint catalog** worked very well. The explorer immediately produced a proper comparison table and knew what "success" meant.
- **Multi-ansatz sweep (7 constructions, one exploration)** was efficient for Phase 1 screening. All variants tested, comparison table produced, best variant identified. For Phase 1 screening this pattern is effective.
- **Primary success criterion (β > 1.5)** was the right discriminator. It was hit, the exploration was not ambiguous.

### What didn't work:
- **Two constructions failed at the design level:** C2 (odd Dirichlet characters → zero matrix) and C4 (lag-only zeta phase → Hermitian Toeplitz → Poisson). These failures could have been prevented by asking the explorer to verify Hermitian non-degeneracy before proceeding.
- **Pair correlation normalization and Δ₃ formula bugs:** MRD = 0.996 and physically wrong Δ₃ values. Both statistics have subtle normalization requirements. The goal should include the exact formulas, not just the statistic names.

### Lessons:
1. **Specify exact formulas for non-trivial statistics.** R₂ pair correlation: H(E-spacing)/N rather than raw counts. Δ₃: Dyson-Mehta integral (not mean-squared-residual/L). Include the exact implementation, not just the name.
2. **Add a sanity-check step:** "Before running statistical analysis, verify that (a) the matrix is Hermitian and non-degenerate, (b) the spacing distribution looks roughly bell-shaped (not all zeros)."
3. **The non-factorizability principle is worth propagating:** φ(j,k) must depend on j and k jointly (not f(|j-k|) or g(j)-g(k)) to break time-reversal symmetry and reach β > 1. This is a clear design rule for future arithmetic matrix constructions.
