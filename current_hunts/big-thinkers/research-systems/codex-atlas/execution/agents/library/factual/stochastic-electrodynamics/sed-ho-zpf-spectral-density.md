---
topic: SED harmonic oscillator — ZPF spectral density formula and factor-of-pi bug fix
confidence: verified
date: 2026-03-27
source: "stochastic-electrodynamics strategy-001 exploration-001; Boyer (1969), Marshall (1963)"
---

## The Correct ZPF Force Power Spectral Density

For a charged particle (mass m, charge e) driven by the zero-point field, the correct one-sided
power spectral density (PSD) of the ZPF force per unit mass is:

    S_F^one(w) = 2 * tau * hbar * w^3 / m

where tau = e^2 / (6*pi*epsilon_0*m*c^3) is the Abraham-Lorentz radiation reaction time.

**[VERIFIED]** — confirmed by three-way numerical cross-check (analytic quadrature, discrete spectral
sum, Monte Carlo ensemble; see sed-ho-numerical-verification.md).

## Full Derivation (8 Steps)

Tracking factors of 2 and pi carefully:

1. ZPF spectral energy density: rho(w) = hbar*w^3 / (2*pi^2*c^3)
2. Electric field energy density: u_E = (epsilon_0/2)*<E^2> = (1/2)*integral(rho(w) dw)
3. For one E-field component (x-polarization): (epsilon_0/2)*<E_x^2> = (1/6)*integral(rho dw)
4. Therefore: <E_x^2> = (1/(3*epsilon_0)) * integral(rho dw)
5. Matching to PSD convention: <E_x^2> = (1/(2*pi)) * integral_0^inf S_E^one dw
6. This gives: S_E^one(w) = 2*pi*rho(w) / (3*epsilon_0) = hbar*w^3 / (3*pi*epsilon_0*c^3)
7. Force PSD (force = e*E_x, divide by m): S_F^one = (e/m)^2 * S_E^one = e^2*hbar*w^3 / (3*pi*epsilon_0*m^2*c^3)
8. Using tau = e^2/(6*pi*epsilon_0*m*c^3): S_F^one = 2*tau*hbar*w^3 / m

## Critical Bug: Factor-of-Pi Error in Earlier Code

**[VERIFIED]** A prior code version used:

    S_F = (2*tau*hbar / (pi*m)) * w^3    ← WRONG

This formula is off by a factor of pi. The error originated from confusing the energy density rho(w)
with the PSD S_E(w) — the conversion from rho to PSD requires a factor of 2*pi (from the Parseval
relation) that was dropped.

**Effect of the bug:** With the incorrect formula, analytic quadrature gives variances that are pi
times too small. Coincidentally, the FFT amplitude normalization formula partially compensated for
the error in a non-obvious way. The bug was only caught via an independent cross-check comparing
analytic quadrature directly to the Monte Carlo ensemble. Code fix: `code/sed_corrected_run.py`.

## Usage in the Frequency-Domain Solution

The position variance integral is:

    var_x = (1/(2*pi)) * integral_0^inf S_F^one(w) / |H(w)|^2 dw

where H(w) = w0^2 - w^2 + i*tau*w^3 is the full Abraham-Lorentz transfer function. With the correct
PSD, this integral converges to hbar/(2*m*w0) = 0.5 in natural units. See also
sed-ho-uv-divergence-structure.md for the UV convergence analysis.
