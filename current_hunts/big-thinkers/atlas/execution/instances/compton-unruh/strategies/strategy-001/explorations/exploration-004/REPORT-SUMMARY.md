# Exploration 004 — Summary

## Goal
Investigate whether the de Sitter thermal crossover at a ~ cH_0 modifies force laws, potentially producing MOND-like dynamics.

## What Was Tried
1. Computed the Wightman function and spectral density for an accelerating observer in de Sitter — same functional form (sinh^-2, Planckian) as flat Rindler, but with effective temperature T_dS(a) = (hbar/(2*pi*c*kB))*sqrt(a^2 + c^2*H^2).
2. Attempted three routes to a modified force law: (a) naive entropic, (b) excess temperature, (c) temperature ratio.
3. Computed rotation curves and BTFR for the successful model.

## Outcome: MIXED — Tantalizing mathematical identity, but no rigorous derivation

**The key finding**: The ratio T_U(a)/T_dS(a) = a/sqrt(a^2 + c^2*H_0^2) is **algebraically identical** to the standard MOND interpolation function mu(x) = x/sqrt(1+x^2) with a_0 = cH_0. If the effective inertial mass is m_i = m * T_U/T_dS, the model reproduces MOND rotation curves, the BTFR (correct slope), and is consistent with solar system tests.

**The critical gap**: There is no first-principles derivation showing that m_i should be proportional to T_U/T_dS. The naive entropic approach (F ~ T_dS) gives the **wrong sign** (anti-MOND). The direct self-force (ALD) vanishes for constant acceleration. The ratio ansatz gives the right answer but is physically unjustified.

**The a_0 scale**: Predicted a_0 = cH_0 = 6.6*10^-10 m/s^2, which is 5.5x larger than observed. Using Verlinde's factor cH_0/6 gives agreement within 8%.

## Verification Scorecard
- **VERIFIED**: 0
- **COMPUTED**: 15 (temperatures, spectra, force laws, rotation curves, BTFR, solar system check, 8 plots)
- **CHECKED**: 1 (Wightman function vs Birrell & Davies)
- **CONJECTURED**: 4 (physical justification for T_U/T_dS, self-force in dS, originality, weakness ratings)

## Key Takeaway
The standard MOND interpolation function is hiding inside the temperature ratio T_U/T_dS — a simple algebraic identity. But making this physically meaningful requires a mechanism that nobody has yet derived: why should effective inertia be proportional to the acceleration-dependent fraction of the thermal environment, rather than the total?

## Leads Worth Pursuing
1. **DeWitt-Brehme self-force in de Sitter**: Compute the full back-reaction for an accelerating scalar charge in dS. Does the effective mass correction go as T_U/T_dS?
2. **Verlinde (2016) connection**: His "elastic entropy" argument gets a_0 = cH_0/(2*pi). Is his derivation equivalent to the ratio ansatz?
3. **Fluctuation-dissipation theorem in dS**: The FDT relates the response function to the fluctuation spectrum. Does the dS modification of the FDT produce the ratio form?

## Unexpected Findings
- The naive entropic approach (replace T_U with T_dS in Verlinde's formula) gives **anti-MOND** — the opposite of what is needed. This means the sign problem is a genuine physical constraint, not just a technicality.

## Computations Identified
- Full DeWitt-Brehme self-force integral for accelerating charge in de Sitter (requires numerical integration of the retarded Green function)
- Comparison of the ratio model with observed rotation curve data (SPARC database)
- Check whether the ratio identity T_U/T_dS = mu_MOND has been published
