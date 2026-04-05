---
topic: cross-cutting
confidence: verified
date: 2026-03-24
source: exploration-002-spectral-dimension-constructive-axiom
---

# Spectral Dimension d_s = 2 Forces Propagator ~ 1/p^4

The spectral dimension flow d_s = 4 (IR) to 2 (UV) is not merely a consistency check on quantum gravity theories -- it can be used as a **constructive axiom** that forces specific propagator forms, dispersion relations, and ultimately gravitational actions.

## Key Mathematical Results

### The Power-Law Formula

For a Lorentz-invariant theory in d Euclidean dimensions with modified d'Alembertian f(p^2) having asymptotic behavior f(p^2) ~ (p^2)^n for large p^2, the UV spectral dimension evaluates to:

    d_s(sigma -> 0) = d/n

In the IR (n = 1): d_s = d (the topological dimension). This formula, derived via substitution in the return probability integral P(sigma) = integral d^d p/(2pi)^d exp(-sigma f(p^2)), is exact for power-law f.

### The Saddle-Point Formula

For general smooth f(p^2), the saddle-point approximation gives a scale-dependent spectral dimension:

    d_s(p*^2) = d * f(p*^2) / (p*^2 * f'(p*^2))

where p* is the saddle-point momentum. This is exact for power laws and provides excellent approximation for smooth interpolations.

### The Forced UV Form in d = 4

Setting d_s = 2 with d = 4 gives n = d/2 = 2. Therefore:

    f(p^2) ~ (p^2)^2 / M^2  as p^2 -> infinity

The propagator G(p^2) = 1/f(p^2) must fall as **1/p^4** in the UV. The mass scale M sets the transition energy.

### Uniqueness via Differential Equation

The condition d_s = 2 exactly (at all UV scales) turns the saddle-point formula into an ODE:

    f'(p^2)/f(p^2) = 2/p^2  =>  f(p^2) = C * (p^2)^2

This means (p^2)^2 is the **unique asymptotic form** -- any deviation changes the UV spectral dimension.

### Quartic Upper Bound

For d_s = 2 in d = 4, f(p^2) must be at most quartic in p^2. Any higher power (e.g., p^6 terms) overshoots to d_s < 2 (specifically d_s = 4/3 for p^6). This eliminates all theories with more than four derivatives in the action from achieving d_s = 2.

## The Simplest Interpolation

The simplest f(p^2) interpolating between IR (d_s = 4) and UV (d_s = 2):

    f(p^2) = p^2 + p^4/M^2

gives a smooth spectral dimension profile:

    d_s(p^2) = 4(1 + p^2/M^2) / (1 + 2p^2/M^2)

    p << M:  d_s = 4      (classical GR)
    p ~ M:   d_s = 8/3    (transition)
    p >> M:  d_s -> 2      (UV regime)

The transition spans roughly one decade of energy around M.

## Connection to Sotiriou-Visser-Weinfurtner

These results follow the framework of Sotiriou, Visser, and Weinfurtner (Phys. Rev. D 84, 104018, 2011; arXiv:1105.6098), who established the connection between modified dispersion relations and spectral dimension:

    d_s(sigma) = 1 + 2 sigma <f(k^2)>_sigma

where the average is taken with heat kernel weight exp(-sigma f(k^2)).

## Significance

This mathematical framework transforms d_s = 2 from a post-hoc observation into a constructive tool: it directly constrains the UV propagator form, which in turn constrains the gravitational action (see `quadratic-gravity-fakeon/core-idea.md` and `constraints/structural/ghost-spectral-dimension-no-go.md`).

Sources: arXiv:1105.6098 (Sotiriou-Visser-Weinfurtner), arXiv:1705.05417 (Carlip)
