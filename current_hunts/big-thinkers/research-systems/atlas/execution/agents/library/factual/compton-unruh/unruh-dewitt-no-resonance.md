---
topic: Unruh-DeWitt detector response has no resonance structure
confidence: verified
date: 2026-03-27
source: "compton-unruh strategy-001 exploration-001 (detector response analysis)"
---

## Finding

The Unruh-DeWitt (UDW) detector transition rate R(E) has **no resonance structure** — no peaks, poles, divergences, or discontinuities at any energy or acceleration. The Compton frequency enters massive field responses only as a threshold zero, not a resonance.

## The Standard Result (Massless, Flat Spacetime)

For a uniformly accelerating UDW detector coupled to a massless scalar field:

    R(E) = (E/hbar) / (2*pi * (exp(2*pi*c*E/(hbar*a)) - 1))    [E > 0]

This is a **Planckian (Bose-Einstein) spectrum** at T_U = hbar*a/(2*pi*c*k_B). R(E) is:
- Smooth and monotonically decreasing in E at fixed a
- Smooth and monotonically increasing in a at fixed E

## Lethal Boltzmann Suppression

At a = cH_0 with E = m_p*c^2 (proton):

    Exponent = 2*pi*c*E/(hbar*a) = 4.07 x 10^42
    Boltzmann factor = exp(-4.07 x 10^42) ~ 10^(-1.77 x 10^42)

This suppression has more orders of magnitude than there are particles in the observable universe (~10^80).

## Massive Field: Van Hove Zero, Not Resonance

For a massive scalar field, the density of states is:

    rho(omega) ~ omega * sqrt(omega^2 - omega_C^2)    for omega > omega_C
    rho(omega) = 0                                     for omega < omega_C

At threshold (omega -> omega_C): rho -> 0. This is a **Van Hove singularity** — specifically a square-root onset (a zero), not a pole or peak. Both the Boltzmann suppression and the threshold behavior conspire to make the response essentially zero at the Compton energy.

## De Sitter Spacetime

Even with the de Sitter modification, the Boltzmann suppression at E = mc^2 is exp(-mc^2/(k_B*T_dS)) ~ exp(-2.88 x 10^42), indistinguishable from zero.

## What "Resonance" Would Require

In the detector response context, a resonance would require one of:
- A pole in R(E) at some specific E — does not exist
- A peak in R(E) vs. a at fixed E = mc^2 — does not exist (monotonically increasing)
- A divergence at critical acceleration — does not exist
- A discontinuity or non-analytic behavior — does not exist in standard Unruh framework

None of these occur.
