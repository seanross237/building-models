# Exploration 004 — De Sitter Crossover Mechanism: Vacuum Fluctuations and Force Laws at a ~ cH₀

## Mission Context

We are investigating whether Unruh-effect physics at low accelerations can modify dynamics in a way that explains galaxy rotation curves.

**CRITICAL PRIOR RESULT**: Exploration 001 showed that the direct Compton-Unruh resonance fails by 43 orders of magnitude. However, it identified an important physical feature: the de Sitter modified Unruh temperature

    T_dS(a) = (ℏ/2πck_B) √(a² + c²H₀²)

has a floor at the Gibbons-Hawking temperature T_GH = ℏH₀/(2πk_B) ≈ 2.7×10⁻³⁰ K. Below a ~ cH₀, the thermal environment is set by the cosmological horizon rather than by the acceleration. This crossover happens at the RIGHT acceleration scale (~10⁻¹⁰ m/s²).

The question for this exploration: **does this de Sitter thermal crossover modify the vacuum fluctuation spectrum in a way that changes the effective force law at low accelerations?**

## Your Task

This is a **computation and derivation** task. Use Python (sympy, numpy, scipy, matplotlib) for all calculations.

### Part 1: The Wightman function in the crossover regime

The Wightman function G⁺(Δτ) for a MASSLESS scalar field along a uniformly accelerating worldline in de Sitter spacetime determines the vacuum fluctuation spectrum experienced by an accelerating observer.

1. **Write down G⁺(Δτ) explicitly** for a massless scalar field in de Sitter, for a detector with proper acceleration a. Include the dependence on both a and H₀.

2. **Compare three regimes computationally:**
   - a >> cH₀: should recover flat-space Unruh (Rindler Wightman function)
   - a ~ cH₀: the crossover regime
   - a << cH₀: the cosmological-horizon-dominated regime

3. **Compute the spectral density** — the Fourier transform of G⁺(Δτ) — in each regime. Plot how the power spectrum changes as a crosses cH₀.

### Part 2: Vacuum fluctuation force (radiation reaction)

An accelerating detector in a thermal bath experiences a radiation reaction force. The question is whether this force has a non-trivial dependence on acceleration in the crossover regime.

1. **Compute the response function R(E, a)** for a detector with gap E in the de Sitter modified thermal state, as a function of a. How does R change across the crossover?

2. **Total absorbed power**: Integrate the response over all energies weighted by the field mode density. How does the total vacuum fluctuation power depend on a?

3. **Derive the effective force law**: If the radiation reaction force on a detector moving with acceleration a in de Sitter is F_rad(a), compute this force. In flat space, F_rad ∝ a (Abraham-Lorentz-Dirac force). How does the de Sitter modification change this?

4. **Key question**: Does F_rad(a) depart from linearity at a ~ cH₀? If F_rad = αa + β√(a² + c²H²) + ..., what does this imply for the effective equation of motion?

### Part 3: Modified equation of motion

If there is any modification:

1. **Write down the modified equation of motion**: F = m_i(a) × a where m_i(a) is the effective inertial mass.

2. **Compute m_i(a)/m**: What is the ratio of effective inertial mass to gravitational mass as a function of acceleration? Plot it from a = 10⁻¹⁵ to 10⁰ m/s².

3. **Compare to MOND**: The MOND interpolation function μ(x) = x/√(1+x²) with x = a/a₀ modifies Newton's law as μ(a/a₀) × a = g_N. Does your result have a similar functional form? Can you fit a₀ to the crossover scale cH₀?

4. **Compute a rotation curve**: If you get a modified force law, compute v(r) for a point mass M = 10¹¹ M_sun (typical galaxy) and compare to Newtonian v(r). Does the rotation curve flatten?

### Part 4: Honest assessment

1. **Where does this derivation break down?** Identify every step where you made an approximation, assumed something unverified, or couldn't complete the calculation.
2. **What is the weakest link?** If the whole argument fails, where does it fail?
3. **Is this derivation original**, or are you reproducing an existing result? If existing, cite it.

## Success Criteria
- G⁺(Δτ) written down for de Sitter + acceleration
- Power spectrum computed in at least 2 of the 3 regimes
- An explicit (even approximate) expression for F_rad(a) or m_i(a)
- Honest assessment of where the derivation breaks down

## Failure Criteria
- If the de Sitter modification produces NO change in the force law (everything cancels), that's a valid negative result. Explain precisely why.
- If the calculation is intractable, identify exactly where it breaks down and what techniques would be needed.

## Deliverables
Write to:
- `explorations/exploration-004/REPORT.md` — full report (300-500 lines)
- `explorations/exploration-004/REPORT-SUMMARY.md` — concise summary (30-50 lines, WRITE THIS LAST)
- `explorations/exploration-004/code/` — all Python scripts
