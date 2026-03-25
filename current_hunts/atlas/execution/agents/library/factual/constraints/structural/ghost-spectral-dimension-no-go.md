---
topic: constraints/structural
confidence: verified
date: 2026-03-24
source: exploration-002-spectral-dimension-constructive-axiom
---

# No-Go Theorem: Ghost Freedom + Lorentz Invariance Incompatible with d_s = 2

## The Theorem

In a Lorentz-invariant theory in d = 4 dimensions:

1. d_s = 2 in the UV requires f(p^2)/p^2 ~ p^2 asymptotically (propagator ~ 1/p^4)
2. Ghost freedom requires f(p^2)/p^2 = e^{gamma(p^2)} where gamma is an entire function (Hadamard factorization)
3. For d_s = 2: e^{gamma(p^2)} ~ p^2, so gamma(p^2) ~ ln(p^2)
4. But ln(p^2) is NOT an entire function (branch point at p^2 = 0)

**Therefore: d_s = 2 and ghost freedom are incompatible in Lorentz-invariant theories with standard propagator structure.**

The key mathematical fact: by the Hadamard factorization theorem, an entire function of finite order with no zeros must be of the form e^{P(z)} where P is a polynomial. For any non-constant polynomial P, e^{P(z)} grows at least exponentially -- it cannot grow merely polynomially like z^alpha.

## Independent Confirmation: Kallen-Lehmann Spectral Representation

In any local Lorentz-invariant QFT, the Kallen-Lehmann representation gives:

    G(p^2) = integral rho(mu^2)/(p^2 + mu^2) d(mu^2)  with rho >= 0

This implies G(p^2) ~ const/p^2 for large p^2. Any propagator falling faster than 1/p^2 (required for d_s < 4) necessarily has negative spectral weight -- i.e., a ghost. This provides a representation-theoretic proof that d_s < 4 requires non-standard quantization in local Lorentz-invariant theories.

## The Ghost Is Inescapable (Polynomial Case)

For any polynomial f(p^2) = p^2(1 + alpha * p^2/M^2) with alpha > 0:

    G(p^2) = M^2 / (p^2(p^2 + M^2/alpha))

By partial fractions: G = 1/p^2 - 1/(p^2 + M^2/alpha)

The massive pole always has residue **-1** (wrong sign = ghost). No choice of alpha avoids this.

## What Ghost-Free Theories Actually Give

| Theory | f(p^2) form | d_s (UV) | Ghost-free? |
|--------|------------|----------|-------------|
| GR | p^2 | 4 | Yes |
| Stelle (R + R^2) | p^2 + p^4/M^2 | 2 | No (ghost) |
| IDG (exponential) | p^2 exp(p^2/M^2) | 0 | Yes |
| IDG (Gaussian) | p^2 exp((p^2)^2/M^4) | 0 | Yes |
| Lee-Wick (1 pair) | p^2 |1-p^2/mu^2|^2 | 4/3 | ✗ (CLOP fails; fakeon → QG+F) |
| Horava-Lifshitz z=3 | k^2 + k^6/M^4 | 2 | Yes (no time ghosts) |

**Key finding:** Among Lorentz-invariant theories, only ghost-plagued Stelle gravity achieves d_s = 2. All ghost-free alternatives either overshoot (IDG: d_s = 0) or miss (Lee-Wick: d_s = 4/3).

## IDG Specifically Gives d_s -> 0

For entire function modifications f(p^2) = p^2 * exp(gamma(p^2)), the saddle-point formula gives:

    d_s(p^2) = 4/(1 + p^2 gamma'(p^2))

For standard IDG (gamma = p^2/M^2): d_s -> 0 as p -> infinity. For ANY entire function gamma(p^2) that is unbounded: d_s -> 0. IDG sacrifices d_s = 2 to achieve ghost freedom.

## The Five Escape Routes

The no-go theorem forces a choice. All five routes have been systematically surveyed — see `constraints/escape-routes-from-no-go.md` for detailed verdicts, rankings, and novel theory candidates.

**(A) Fakeon/Lee-Wick:** Accept the ghost pole but modify its quantization so it cannot appear as an asymptotic state (Anselmi-Piva 2018). -> d_s = 2 achieved. Cost: microcausality violation at Planck scale. See `quadratic-gravity-fakeon/`.

**(B) Lorentz violation:** Allow different spatial and temporal scaling (Horava-Lifshitz z=3). d_s = 1 + d_spatial/z = 2 with only spatial sixth-order derivatives -- no temporal ghosts. Cost: Lorentz symmetry breaking. Super-Planckian LIV bounds from GRB 221009A make this narrow. See `horava-lifshitz/`.

**(C) RG-emergent d_s = 2:** Have d_s = 2 emerge from the dressed propagator via RG flow rather than the bare action (asymptotic safety). The anomalous dimension eta_N = -2 at the fixed point modifies the effective propagator to 1/p^4 without explicit higher-derivative terms. Risk: may be the same theory as QG+F. See `asymptotic-safety/swy-two-fixed-points.md`.

**(D) Accept d_s -> 0:** Use IDG/nonlocal gravity and accept that d_s -> 0 rather than 2.

**(E) Complex poles / Lee-Wick: CLOSED.** Meromorphic propagators with complex conjugate poles escape the no-go mathematically, but the CLOP prescription fails unitarity (Kubo-Kugo 2023) and Lorentz invariance (Nakanishi 1971, Anselmi+Modesto 2025). With the fakeon prescription (the only viable one), the four-derivative version IS QG+F. The six-derivative super-renormalizable version is a known variant, not a genuinely independent theory. See `lee-wick-gravity/`.

## Significance

This no-go theorem reveals a **fundamental mathematical obstruction** at the intersection of three constraints that are individually well-motivated: ghost freedom, Lorentz invariance, and d_s = 2. It structures the landscape of quantum gravity approaches by showing which combinations of desiderata are jointly achievable and which require trade-offs.

Sources: arXiv:1806.03605 (Anselmi-Piva), arXiv:1704.07211 (Conroy, IDG thesis), arXiv:1105.6098 (Sotiriou-Visser-Weinfurtner)
