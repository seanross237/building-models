---
topic: cross-cutting
confidence: verified
date: 2026-03-25
source: exploration-009-entanglement-UV-construction (strategy-002)
---

# The Entanglement-Gravity Self-Consistency Bootstrap

## Summary

Starting from Jacobson's Maximal Vacuum Entanglement Hypothesis (MVEH) as a constructive UV axiom, the entanglement-gravity bootstrap uniquely produces QG+F (quadratic gravity with fakeon quantization). The construction shows QG+F is the unique fixed point of the entanglement-gravity self-consistency map: the theory whose UV entanglement structure, fed through MVEH, reproduces the same theory.

**The chain:** MVEH → entanglement determines gravity → self-consistency → renormalizability → quadratic gravity → unitarity → fakeon → QG+F.

## UV Divergence Structure of Entanglement Entropy

For a quantum field in 4D, entanglement entropy across a surface Σ has UV divergent structure (Solodukhin 2011, arXiv:1104.3712):

    S_EE = a₁ · A(Σ)/ε² + a₂ · ∫_Σ (geometric curvature terms) · ln(ε/μ) + finite

**The Susskind-Uglum identification:** UV divergences of S_EE are exactly the counterterms needed to renormalize the gravitational effective action:
- The 1/ε² divergence renormalizes 1/G (Newton's constant)
- The ln(ε) divergences renormalize the R², R_μν², R_μνρσ² couplings

### The Entanglement-Coupling Rosetta Stone (4D)

| UV divergence in S_EE | Gravitational coupling | Physical role |
|---|---|---|
| A/ε² coefficient | 1/(16πG) | Newton's constant |
| ∫R_Σ · ln(ε) coefficient | α (R² coupling) | Scalar mode mass: m₀² = 1/(6α) |
| ∫(Weyl terms) · ln(ε) | β (C² coupling) | Spin-2 ghost/fakeon mass: m₂² = 1/(2β) |
| ∫(extrinsic curvature²) · ln(ε) | γ (Gauss-Bonnet) | Topological in 4D |

This mapping is the key enabling result: different UV physics → different divergence coefficients → different gravitational theories.

### The Nesterov-Solodukhin No-Go Theorem

For a field equation F(□)φ = 0 with F(p²) ~ p^{2k} at large p (arXiv:1008.0777):

    S_EE ~ A · ε^{-(d-2-2k)}

In 4D with k=2 (1/p⁴ propagator): S_EE ~ A·ln(ε). **No propagator modification can make S_EE finite within QFT on a fixed background.** Even spectral dimension d_s = 2 does not suffice. Possible resolutions: analytic continuation or background-independent quantization (Pagani-Reuter 2018 showed AS makes S_EE finite by quantizing spacetime itself).

## The Bueno et al. Extension to Higher-Derivative Gravity

**Key result (arXiv:1612.04374, Phys. Rev. D 95, 046003):** Linearized higher-derivative gravitational field equations are equivalent to an equilibrium condition on entanglement entropy of small spherical regions in vacuum.

The construction replaces area with **Wald entropy** as the gravitational entropy functional:

    S_Wald = -2π ∫_{∂Σ} E^{abcd} n_{ab} n_{cd}

where E^{abcd} = ∂L/∂R_{abcd}. Setting δS = 0 at fixed generalized volume W → linearized field equations of the higher-derivative theory.

### The Linearization Barrier

**For Einstein gravity:** MVEH in small balls → fully **nonlinear** Einstein equations (Riemann normal coordinate expansion suffices).

**For higher-derivative gravity:** MVEH → only **linearized** equations. Reason: higher-order RNC terms needed for higher-curvature effects contribute at the same order as nonlinear corrections. **Entanglement equilibrium alone cannot determine the fully nonlinear higher-derivative action.** This is a precise statement about the limits of the entropic approach.

A 2025 paper (arXiv:2506.00265) using quantum reference frames recovers the full nonlinear Einstein equations, but this does not extend to higher-derivative gravity.

## The Self-Consistency Bootstrap Construction

### Core Idea

The UV physics of quantum gravity determines the entanglement entropy structure. The entanglement entropy, through MVEH, determines the gravitational equations. The gravitational equations ARE the UV physics. Therefore the theory must be a **fixed point of the entanglement-gravity map:**

    UV Theory → S_EE structure → MVEH → Gravitational Equations → UV Theory
                        (self-consistency loop)

### The Construction (6 Steps)

1. **Parameterize the UV theory:** Most general Lorentz-invariant, diff-invariant gravitational action with at most 4 derivatives in 4D: S = ∫ d⁴x √g [Λ + R/(16πG) + (1/2f₂²)C² + (1/6f₀²)R²]. Gauss-Bonnet is topological in 4D.

2. **Compute entanglement entropy this theory produces:** Matter + graviton loops produce UV divergences absorbed into gravitational couplings via Susskind-Uglum: η_eff = 1/(4G_ren), α_EE = (1/6f₀²)_ren, β_EE = (1/2f₂²)_ren.

3. **Apply MVEH to renormalized entanglement entropy:** Using Bueno et al.: δS_EE^{ren} = 0 at fixed generalized volume W gives linearized field equations of the same action with renormalized couplings.

4. **Self-consistency condition:** The gravitational action produced by MVEH must be the same action whose quantum effects produce the entanglement entropy. This is a fixed-point condition — simply the standard RG fixed-point condition.

5. **Demand renormalizability:** For the bootstrap to close (UV divergences absorbable by existing couplings), the theory must be renormalizable. In 4D, the **unique** renormalizable gravitational action is quadratic gravity (Stelle 1977).

6. **Demand unitarity:** The massive spin-2 ghost from C² must be treated as a fakeon (the only option preserving unitarity — Lee-Wick fails per Kubo-Kugo 2023, Anselmi-Modesto 2025).

**Result: MVEH + self-consistency + renormalizability + unitarity → QG+F**

### The Spectral Dimension Route (Alternative Path)

1. Demand d_s = 2 in UV → propagator ~ 1/p⁴
2. Diff-invariance + Lorentz invariance + 4 derivatives → R² + C² (unique)
3. Apply MVEH: S ~ A·ln(ε) + subleading → δS = 0 → linearized equations of R + R² + C²
4. Self-consistency ✓; unitarity → fakeon → QG+F ✓

**Same endpoint. Two independent paths to QG+F.**

## Modular Flow Unitarity Argument for the Fakeon

The modular Hamiltonian K generates unitary flow: ρ(τ) = e^{iKτ} ρ e^{-iKτ}. In Lee-Wick quantization, ghost particle creation above threshold spoils positivity of the modular Hamiltonian (Kubo-Kugo 2023). But with the **fakeon prescription**, the ghost is projected out, preserving modular flow unitarity.

This gives an independent, information-theoretic argument for the fakeon:

    MVEH + modular flow unitarity → fakeon prescription → QG+F

This is perhaps the most elegant information-theoretic selection of QG+F: the fakeon is REQUIRED for self-consistent entanglement structure.

## Six-Derivative Extension via MVEH

MVEH **permits but does not require** six-derivative gravity. The six-derivative theory is super-renormalizable (not strictly renormalizable), has more free parameters (10 independent couplings), and the self-consistency bootstrap has a larger solution space. MVEH + renormalizability prefers four-derivative QG+F as the minimal self-consistent solution.

## Why Entanglement Cannot Produce Genuinely Novel Theories

1. MVEH operates on entanglement entropy, determined by the UV propagator structure
2. In a diff-invariant, Lorentz-invariant theory, propagator UV behavior is determined by derivative order of the action
3. Renormalizability in 4D constrains to at most 4 derivatives (Stelle's theorem)
4. The unique such action is R + R² + C²
5. Unitarity requires the fakeon prescription

No room for anything else within {diff-invariance, Lorentz invariance, locality, renormalizability}. MVEH provides a beautiful derivation of WHY QG+F, but doesn't escape the no-go theorem's classification.

### What Would Enable Novelty

1. Non-perturbative entanglement structure that doesn't reduce to standard UV divergence expansion (e.g., Pagani-Reuter 2018 — AS makes S_EE finite via background-independent quantization)
2. Entanglement axiom constraining nonlinear interactions (arXiv:2506.00265 is a step)
3. Relaxation of locality or Lorentz invariance in entanglement structure
4. Completely new definition of entanglement entropy beyond standard return-probability approach

None currently exist in a form producing concrete alternatives to QG+F.

## QFC and Relative Entropy: Complementary but Not Constructive

**QFC as axiom:** In 4D, automatically satisfied by quadratic gravity due to Gauss-Bonnet. Provides no constraints beyond Einstein gravity. In d ≥ 5, constrains cutoff scale but doesn't select UV completion. **Cannot construct a UV-complete theory alone.**

**Relative entropy positivity:** Gives the sign of Newton's constant (G > 0) and constrains signs of higher-derivative couplings (f₀² > 0, f₂² > 0 for QG+F). But requires holographic (AdS/CFT) setup and cannot distinguish between theories with positive couplings. **Complementary to MVEH but not independently constructive.**

Sources: Jacobson (2015, arXiv:1505.04753); Bueno et al. (2017, arXiv:1612.04374); Nesterov & Solodukhin (2010, arXiv:1008.0777); Solodukhin (2011, arXiv:1104.3712); Calcagni (2017, arXiv:1704.01141); Pagani & Reuter (2018, JHEP07); Lashkari et al. (2014, arXiv:1312.7856); Bousso et al. (2016, arXiv:1506.02669); arXiv:2506.00265 (2025); Kanai et al. (2024, arXiv:2405.01296)
