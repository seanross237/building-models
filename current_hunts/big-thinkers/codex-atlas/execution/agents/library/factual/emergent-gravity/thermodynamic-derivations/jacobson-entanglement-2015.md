---
topic: emergent-gravity
confidence: verified
date: 2026-03-22
source: https://arxiv.org/abs/1505.04753
---

# Jacobson's Entanglement Equilibrium and the Einstein Equation (2015)

Ted Jacobson published "Entanglement Equilibrium and the Einstein Equation" (arXiv:1505.04753, Physical Review Letters 116, 201101, 2016), extending his landmark 1995 thermodynamic derivation of Einstein's equations into the language of quantum entanglement.

## Core Hypothesis

The "maximal vacuum entanglement hypothesis" asserts that entanglement entropy in small geodesic balls is maximized at fixed volume in a locally maximally symmetric vacuum state of geometry and quantum fields.

## Two-Pronged Methodology

1. A qualitative argument showing the Einstein equation implies the validity of the hypothesis
2. A precise mathematical demonstration that for conformal quantum fields, vacuum entanglement achieves a stationary state if and only if the Einstein equation is satisfied

## Mathematical Machinery

**First law of entanglement:** δS_EE = (2π/ℏ) δ⟨K⟩, where K is the modular Hamiltonian.

**Modular Hamiltonian for a small geodesic ball (conformal case):**

    H_ζ = ∫_Σ T^{ab} ζ_b dΣ_a

where ζ is the conformal Killing vector generating hyperbolic boosts: ζ = (1/2ℓ)[(ℓ² - u²)∂_u + (ℓ² - v²)∂_v].

For constant stress-energy: δ⟨H_ζ⟩ = [Ω_{d-2} ℓ^d / (d² - 1)] δ⟨T₀₀⟩.

**Total entropy variation:** δS_tot = η·δA|_V + (2π/ℏ) δ⟨K⟩

**Area variation at fixed volume:** δA|_{V,λ} = -[Ω_{d-2} ℓ^d / (d² - 1)] (G₀₀ + λg₀₀)

**Requiring δS_tot = 0 yields:** G_{ab} + Λ g_{ab} = (2π / ℏη) δ⟨T_{ab}⟩ — the Einstein equation with G_Newton = 1/(4ℏη), reproducing Bekenstein-Hawking entropy density η = 1/(4ℏG).

## Key Result

For first-order variations of the local vacuum state of conformal quantum fields, the vacuum entanglement is stationary if and only if the Einstein equation holds. The Einstein equation emerges as an equilibrium condition for entanglement entropy -- gravity is what you get when entanglement is maximized.

## Structural Features

1. **No AdS required** — works in any maximally symmetric background (including flat and dS)
2. **No holographic duality required** — purely local argument based on causal diamonds
3. **UV structure enters through η** — the area density is the interface between UV physics and Einstein equations
4. **Conformal fields only (rigorous)** — non-conformal fields require a conjecture about the modular Hamiltonian
5. **Semiclassical regime only** — assumes smooth geometry with ℓ ≫ ℓ_Planck

## What Jacobson Does NOT Address

- What UV theory produces the finite η
- How the derivation modifies when the UV cutoff is comparable to ball size (ℓ ~ ℓ_P)
- Whether higher-curvature corrections emerge from subleading entanglement terms
- Backreaction of quantum gravity modes on entanglement structure

These gaps have now been addressed: see [`cross-cutting/entanglement-gravity-bootstrap.md`](../../cross-cutting/entanglement-gravity-bootstrap.md) for the UV extension.

## Significance

This work derives the full Einstein equations without assuming an Anti-de Sitter (AdS) background, unlike many holographic approaches. It establishes that spacetime geometry may emerge from entanglement properties of quantum fields, bridging quantum information theory and general relativity. The conclusion extends to nonconformal fields under specific conjectures about entropy variation.

## Publication Details

- Submitted: May 18, 2015
- Published: Physical Review Letters 116, 201101 (2016)
- Length: 8 pages (final version)

Source: https://arxiv.org/abs/1505.04753
