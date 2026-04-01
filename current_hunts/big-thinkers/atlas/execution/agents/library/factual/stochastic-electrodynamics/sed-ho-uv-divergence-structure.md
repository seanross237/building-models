---
topic: SED harmonic oscillator — UV divergence structure and mass renormalization
confidence: verified
date: 2026-03-27
source: "stochastic-electrodynamics strategy-001 exploration-001"
---

## The Fundamental UV Asymmetry

Under the full Abraham-Lorentz transfer function H(w) = w0^2 - w^2 + i*tau*w^3, the position and
velocity variance integrands behave completely differently in the UV (w >> w0, where |H|^2 ~ tau^2*w^6):

| Quantity | Integrand ~ | UV behavior | Convergence |
|----------|-------------|-------------|-------------|
| var_x    | w^3 / |H|^2 | w^3 / w^6 = 1/w^3 | **Converges** |
| var_v    | w^5 / |H|^2 | w^5 / w^6 = 1/w   | **Diverges** (log/power-law) |

**[COMPUTED]** — confirmed numerically across w_max ranging over a factor of 10 (31.4 to 314.2 rad/s):

| w_max | var_x | var_v | Total energy |
|-------|-------|-------|--------------|
| 31.4  | 0.502 | 0.655 | 0.582        |
| 62.8  | 0.511 | 5.82  | 3.16         |
| 314.2 | 0.512 | 38.5  | 19.5         |

**Key conclusion:** Only the position variance is a physical (cutoff-independent) prediction of SED
for the harmonic oscillator. Velocity variance and total energy are UV-sensitive.

## Full Abraham-Lorentz is Required for var_x Convergence

**[COMPUTED]** The effective damping approximation H_eff = w0^2 - w^2 + i*Gamma*w (Gamma = tau*w0^2)
has |H_eff|^2 ~ w^4 at high frequencies, making the position variance integrand ~ 1/w (logarithmically
divergent). The effective damping approximation is fine near resonance but FAILS as a global formula.

In contrast, the full Abraham-Lorentz transfer function (cubic in w) provides the extra w^2 suppression
that converts the position variance from log-divergent to 1/w^3-convergent.

**Practical implication:** Any simulation using the effective damping approximation will see var_x
grow logarithmically with the UV cutoff — a spurious result. Always use the full Abraham-Lorentz
transfer function for SED simulations.

## Mass Renormalization Connection

The UV divergence of kinetic energy is not a simulation artifact — it reflects classical
electromagnetic self-energy physics. A classical point charge has infinite electromagnetic self-energy.
The Abraham-Lorentz equation implicitly uses a bare mass m_bare; the physically observed mass is:

    m_obs = m_bare + delta_m(w_max)

where delta_m grows with the UV cutoff. The "total energy" computed from the simulation includes
this bare-mass kinetic contribution. The position distribution and potential energy are
**renormalization-independent** because they don't depend on the UV tail of the velocity distribution.

This parallels mass renormalization in quantum field theory — it's satisfying to see it emerge
naturally in the classical SED setting.

## What "Success" Means for the HO

Given this UV structure, the correct statement of SED's success on the harmonic oscillator is:

- **Position variance:** matches QM (cutoff-independent, 1.4% error at tau=0.001)
- **Position distribution shape:** matches QM (Gaussian)
- **Potential energy:** matches QM (PE = 0.254 vs target 0.25, 2% error)
- **Total energy:** UV-divergent, NOT directly comparable to E0 = 0.5 without mass renormalization
- **Velocity variance:** UV-divergent, NOT a physical prediction

See also established-successes.md (general HO success) and sed-ho-numerical-verification.md
(numerical details).
