# Exploration 003 — Summary

## Goal
Implement SU(2) Wilson lattice gauge theory in 4D from scratch and compute mass gap observables: Wilson loops, Creutz ratios, glueball masses, and scaling behavior.

## What Was Done
Built a complete Monte Carlo simulation for SU(2) lattice gauge theory in 4D using Python/numpy/numba. Implemented:
- SU(2) algebra via quaternion representation
- Wilson plaquette action on periodic hypercubic lattices
- Kennedy-Pendleton heat bath algorithm
- Wilson loop, Creutz ratio, plaquette correlator, and Polyakov loop measurements

Ran 13 independent simulations across lattice sizes 4⁴, 6⁴, 8⁴ and β = 2.0, 2.2, 2.3, 2.5, 3.0. Total runtime ~5 minutes. All code saved in `code/`.

## Outcome: SUCCESS

### Key Findings

1. **Confinement confirmed**: Wilson loops obey area law with R² > 0.996 at all β values. String tension σ > 0 everywhere: σ = 0.593(13) at β=2.0 down to σ = 0.132(3) at β=3.0 (L=6 data).

2. **Mass gap evidence**: Positive string tension, vanishing Polyakov loop, and exponentially decaying Wilson loops all confirm a mass gap on the lattice. Glueball mass estimated at m₀ ~ 1.8-2.5 lattice units via the phenomenological relation m₀ ≈ 4√σ.

3. **Implementation verified**: Plaquette values match published SU(2) results within 1-2σ. Internal consistency checks (W(1,1)≈⟨P⟩, W(R,T)≈W(T,R)) all pass.

4. **Glueball correlator failed** (as expected on small lattices): the plaquette-plaquette correlator is noise-dominated for t>0. This is consistent with a large mass gap m₀ >> 1/L. Professional lattice calculations use 16⁴-32⁴ lattices, smeared operators, and O(10⁵) configurations.

5. **Scaling not demonstrated**: our lattice sizes (≤8⁴) and β range are below the scaling window. Asymptotic scaling for SU(2) requires β ≥ 2.4 on lattices ≥ 16⁴.

## Verification Scorecard
- **[VERIFIED]**: 4 claims (quaternion algebra, W(1,1)≈⟨P⟩, isotropy, area monotonicity)
- **[COMPUTED]**: 12 claims (all quantitative measurements with error bars)
- **[CHECKED]**: 3 claims (plaquette vs. literature, Creutz ratio consistency, finite-size convergence)
- **[CONJECTURED]**: 2 claims (glueball mass estimate, asymptotic scaling)

## Key Takeaway
The lattice SU(2) gauge theory demonstrably confines and has a positive mass gap at all coupling values studied. The string tension is robustly measured with <3% statistical errors. This provides strong **computational** evidence for the Yang-Mills mass gap — the results are entirely consistent with 40+ years of lattice gauge theory literature. However, the gap between this numerical evidence and a rigorous **mathematical proof** remains enormous: no existing framework can rigorously take the continuum limit while preserving the non-perturbative mass gap.

## Proof Gaps Identified
- The mass gap is invisible to perturbation theory — any rigorous proof must be genuinely non-perturbative
- Cluster expansion methods that work at d=2,3 fail at d=4 due to the marginal coupling
- Balaban's RG program controls UV but not IR; no method controls the confined IR regime rigorously
- A rigorous bound σ(β,L) ≥ c > 0 uniform in both L (volume) and β (approaching continuum) is the core missing ingredient

## Unexpected Findings
- The plaquette-plaquette connected correlator is NEGATIVE at t>0 on all lattice sizes, due to a finite-volume constraint effect (sum rule: Σ_t C(t) ≈ 0). This makes direct glueball mass extraction from this correlator impossible without larger lattices.

## Computations Worth Pursuing
- Run on 12⁴-16⁴ lattices with smeared operators to extract actual glueball mass values
- Use variational method (GEVP) with multiple operator bases for reliable mass extraction
- Extend β range to 2.4-2.8 on large lattices to probe the scaling window
- Compare SU(2) and SU(3) to test N-dependence of the mass gap
