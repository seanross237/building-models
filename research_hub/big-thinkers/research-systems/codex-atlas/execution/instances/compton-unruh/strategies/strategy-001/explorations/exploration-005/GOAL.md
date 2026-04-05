# Exploration 005 — Literature Search: T_U/T_dS = μ_MOND Identity, Verlinde Comparison, and Free-Fall Objection

## Mission Context

We are investigating modified dynamics at low accelerations (a ~ cH₀) arising from de Sitter vacuum effects.

**KEY PRIOR RESULTS:**

1. **Exploration 001**: Direct Compton-Unruh resonance ruled out by 43 orders of magnitude.
2. **Exploration 003**: No universal no-go against Unruh-based inertia modification, but severe constraints. Surviving mechanisms: vacuum structure, Verlinde entropic gravity, de Sitter crossover.
3. **Exploration 004**: Found that the ratio T_U(a)/T_dS(a) = a/√(a² + c²H₀²) is ALGEBRAICALLY IDENTICAL to the standard MOND interpolation function μ(x) = x/√(1+x²) with a₀ = cH₀. If m_i = m × T_U/T_dS, the model reproduces MOND rotation curves and BTFR. But: (a) no first-principles derivation exists, (b) the naive entropic approach gives the wrong sign, (c) predicted a₀ = cH₀ is 5.5× too large.

## Your Task

This is a **literature survey and critical comparison** task. You are working on the COMPTON-UNRUH MISSION in the directory compton-unruh/strategies/strategy-001/. Write ALL output to explorations/exploration-005/.

### Part 1: Has T_U/T_dS = μ_MOND been published?

Search for any prior publication that explicitly identifies the algebraic identity:

    T_U(a)/T_dS(a) = a/√(a² + c²H₀²) = μ_MOND(a/cH₀)

where T_U = ℏa/(2πck_B) is the Unruh temperature, T_dS = (ℏ/2πck_B)√(a² + c²H₀²) is the de Sitter-modified Unruh temperature, and μ is the MOND interpolation function.

Specific search targets:
1. Deser & Levin (1997) — derived T_dS. Did they note the ratio?
2. Padmanabhan (2002-2010) — extensive work on horizon thermodynamics. Any MOND connection?
3. McCulloch (2007-2017) — different approach but same result?
4. Verlinde (2016, arXiv:1611.02269) — derives MOND from de Sitter entropy. Is it algebraically equivalent?
5. Lee (2012), Pikhitsa (2010) — papers connecting cosmological horizons to MOND
6. Any paper citing both "Unruh temperature" and "MOND" or "interpolation function"

### Part 2: Detailed comparison with Verlinde (2016/2017)

Verlinde's "Emergent Gravity and the Dark Universe" (2016) derives MOND-like behavior from de Sitter entropy. Compare:

1. **The mechanism**: Verlinde argues that de Sitter space has an "elastic" response to matter that displaces entropy. How does this relate to the thermal crossover T_U → T_dS?
2. **The equations**: Verlinde gets a₀ = cH₀/(2π). We get a₀ = cH₀. What accounts for the factor of 2π?
3. **The interpolation function**: Verlinde gets μ(x) = x/(1+x) (the "simple" MOND function, not the "standard" one). We get μ(x) = x/√(1+x²). These are different — do they lead to different predictions?
4. **Physical content**: Is the T_U/T_dS approach a simplification of Verlinde's holographic argument, an alternative derivation, or something genuinely different?
5. **The free-fall issue**: How does Verlinde handle the fact that orbiting stars are in free fall? What plays the role of "acceleration" in his framework?

### Part 3: The free-fall objection

The strongest surviving objection (from Exploration 003): stars in galaxies are in free fall, with zero proper acceleration. The standard Unruh effect requires proper acceleration. How can an Unruh-based mechanism modify the dynamics of freely-falling objects?

Investigate:
1. **The Sciama-Candelas effect**: Do freely-falling detectors near a mass see thermal radiation? (Sciama 1981, Candelas & Sciama 1977) What is the temperature?
2. **Unruh radiation in curved spacetime**: Some authors argue that what matters is not proper acceleration but the non-inertial character of the motion relative to the local vacuum state. Does this resolve the objection?
3. **Verlinde's resolution**: In Verlinde's framework, the "acceleration" that enters is the Newtonian gravitational acceleration g_N, not the proper acceleration. Why? Is this justified?
4. **Jacobson's thermodynamic derivation**: Jacobson (1995) uses local Rindler horizons. How does "acceleration" enter in his framework?

### Part 4: Assessment

1. **Novelty verdict**: Is T_U/T_dS = μ_MOND a known result, a trivial rearrangement of known results, or genuinely novel?
2. **Distinctness from Verlinde**: Is this approach equivalent to Verlinde (2016), a simplification, or distinct?
3. **Free-fall status**: Is the free-fall objection resolved by any existing argument?

## Success Criteria
- Clear answer on whether T_U/T_dS = μ_MOND has been published
- Side-by-side equation comparison with Verlinde (2016)
- At least 2 approaches to the free-fall objection evaluated
- Clear assessment of novelty and distinctness

## Deliverables
Write to:
- `explorations/exploration-005/REPORT.md` — full report (300-500 lines)
- `explorations/exploration-005/REPORT-SUMMARY.md` — concise summary (30-50 lines, WRITE THIS LAST)
