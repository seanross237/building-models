---
topic: De Sitter force modification mechanisms — naive entropic (wrong sign), ALD vanishes, ratio ansatz unjustified
confidence: provisional
date: 2026-03-27
source: "compton-unruh strategy-001 exploration-004"
---

## Finding

Three candidate mechanisms for deriving MOND-like dynamics from the de Sitter thermal crossover were systematically tested. Two are ruled out (naive entropic gives wrong sign; ALD self-force vanishes for constant acceleration). The third (ratio ansatz) gives exactly MOND but lacks a physical derivation. The rigorous path forward requires the DeWitt-Brehme self-force calculation in de Sitter spacetime.

## Mechanism 1: Naive Entropic Approach — WRONG SIGN

Following Verlinde (2010), F = T · dS/dx gives F = ma when T = T_U (flat space). In de Sitter:

    F_dS = T_dS(a) · (2πk_B mc/ℏ) = m · √(a² + c²H₀²)

The equation of motion g_N = √(a² + c²H₀²) gives a = √(g_N² - c²H₀²).

**Problem:** This predicts LESS acceleration than Newton at low g_N. It makes the particle appear heavier, not lighter — **opposite of MOND**. This approach is excluded.

## Mechanism 2: ALD Self-Force — VANISHES

The Abraham-Lorentz-Dirac radiation reaction force F_ALD = τ₀m·da/dt vanishes for uniform acceleration (ȧ = 0). The de Sitter modification to the self-force integral:

    F_self(a, ȧ) = (q²/(6π)) · (a·ȧ/c²) / √(a²/c² + H²)

also vanishes for constant acceleration (ȧ = 0). **The direct self-force cannot produce a steady-state modification to F = ma.** This route is closed.

## Mechanism 3: Excess Temperature Approach — WRONG a₀, AD HOC

If inertia is proportional to the "excess" temperature above the cosmological background:

    m_i(a) = m · (T_dS - T_GH) / T_U = m · [√(a² + c²H₀²) - cH₀] / a

For g_N ≪ cH₀: a ~ √(2cH₀·g_N) — MOND-like, but with a₀ = 2cH₀ ≈ 1.3 × 10⁻⁹ m/s², which is **11× too large**. Additionally, the subtraction of T_GH has no rigorous justification ("only the excess above background contributes") — it is physically ad hoc.

## Mechanism 4: Ratio Approach — MOND EXACT, BUT UNJUSTIFIED

    m_i(a) = m · T_U(a) / T_dS(a) = m · a / √(a² + c²H₀²)

This gives exactly the standard MOND interpolation function μ(x) = x/√(1+x²). See `tu-tds-mond-identity.md`.

**Problem:** There is NO first-principles derivation that the effective inertial mass should be the ratio T_U/T_dS. The three alternatives show that different well-motivated expressions produce very different results (wrong sign, wrong magnitude, or exact MOND). The choice of T_U/T_dS is **motivated by the desired result**, not derived from the physics.

## Comparative Summary

| Mechanism | Result | Status |
|-----------|--------|--------|
| Naive entropic: F ~ T_dS | Anti-MOND (heavier, wrong sign) | Excluded |
| ALD self-force | Vanishes at constant acceleration | Dead end |
| Excess temperature: F ~ T_dS - T_GH | MOND-like, a₀ = 2cH₀ (11× too large) | Ad hoc, wrong scale |
| Ratio: m_i ~ T_U/T_dS | Exact MOND (μ = x/√(1+x²)), a₀ = cH₀ | Algebraically exact, physically unjustified |

## Path to Rigor

To promote the ratio ansatz from CONJECTURED to VERIFIED would require one of:
1. Full QFT-in-curved-spacetime calculation: compute back-reaction of the de Sitter vacuum on a uniformly accelerating particle (DeWitt-Brehme self-force in de Sitter) and show the effective mass is proportional to T_U/T_dS.
2. Show that Verlinde's entropic argument, applied carefully to the de Sitter static patch, gives the ratio form rather than the naive form.
3. A fluctuation-dissipation argument where de Sitter background "screens" Unruh modes by exactly T_U/T_dS.

None of these calculations have been carried out in the literature (as of March 2026).

**Update (E006):** Option 3 (the FDT route) has now been explicitly tested and found NEGATIVE. Standard FDT gives χ''_dS = χ''_flat exactly — no inertia modification in either the classical or quantum case. Additionally, γ_dS > γ_flat (wrong direction, confirming the sign problem). A non-equilibrium Langevin route was explored but is self-referential (it assumes γ ~ T_U, which amounts to the ratio ansatz in disguise). The most promising remaining route is option 1 (DeWitt-Brehme self-force) or option 2 (Verlinde-FDT connection). See `fdt-no-inertia-modification.md`.
