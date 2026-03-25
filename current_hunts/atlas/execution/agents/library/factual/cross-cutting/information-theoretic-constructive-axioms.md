---
topic: cross-cutting
confidence: provisional
date: 2026-03-24
source: exploration-001-escape-routes-survey (strategy-002)
---

# Information-Theoretic Constructive Axioms for Quantum Gravity

## The Idea

Instead of starting from d_s = 2 as a constructive axiom (which uniquely selects QG+F), one can start from information-theoretic principles and ask what UV-complete gravitational theory they select. These axioms are physically well-motivated, mathematically sharp, and have **not been systematically explored** as constructive axioms for building UV-complete theories.

This is identified as the most promising route for genuinely novel theory construction — the only escape route from the no-go theorem that changes the *starting point* rather than modifying an assumption within the existing framework.

## The Four Axioms

### 1. Positivity of Relative Entropy

**Axiom:** S(rho || sigma) >= 0 for all states rho, sigma.

Derived from the 2025 Unified Holographic Swampland Condition (Upadhyay et al., arXiv:2512.14389), which showed that a single inequality encapsulates the de Sitter gradient conjecture, Weak Gravity Conjecture, and Distance Conjecture:

    |nabla V|^2 / V^2 + q^2/(g^2 M_P^2) + 1/(R_moduli L^2) >= c_d

This is derived from three information-theoretic requirements: positivity of relative entropy in the boundary CFT, unitary modular flow, and monotonic evolution of holographic entanglement entropy under RG flow.

### 2. Maximal Vacuum Entanglement Hypothesis (Jacobson 2015)

**Axiom:** The vacuum of any QFT on smooth spacetime has maximal entanglement at the UV cutoff scale.

Jacobson showed this implies the Einstein equations via entanglement equilibrium in small causal diamonds. The UV extension asks: if the vacuum entanglement structure *changes* at the Planck scale (as expected in any UV completion), the modified entanglement entropy generates *modified* gravitational equations. The specific UV modification selects specific departures from Einstein gravity — a map from UV entanglement structures to gravitational theories.

**NOW EXPLORED CONSTRUCTIVELY — Result: produces QG+F.** The entanglement-gravity self-consistency bootstrap (MVEH + renormalizability + unitarity) uniquely selects quadratic gravity with fakeon quantization. QG+F is the unique fixed point of the entanglement-gravity map. See [`cross-cutting/entanglement-gravity-bootstrap.md`](entanglement-gravity-bootstrap.md) for the full construction.

Key sub-results:
- Bueno et al. (2017, arXiv:1612.04374) extended MVEH to higher-derivative gravity, but only recovers **linearized** equations (the "linearization barrier")
- The self-consistency bootstrap requires the theory to be renormalizable, uniquely selecting quadratic gravity
- **Modular flow unitarity** independently requires the fakeon prescription (ghost creation spoils modular Hamiltonian positivity)
- Six-derivative gravity is permitted but not required by MVEH

**Recent developments (2024-2026):**
- Feb 2026: Extension to non-Riemannian geometries (torsion, non-metricity) — naturally selects Einstein-Cartan over Palatini or metric-affine alternatives
- Nov 2025: Gravity as "thermodynamic phenomenon from a scalar field that sets the local rate of quantum evolution"

### 3. Quantum Focusing Condition (QFC)

**Axiom:** The quantum expansion theta_q = theta + 4 G_N S''_ent is non-increasing along null congruences (Bousso et al.).

This can be taken as more fundamental than the Einstein equations. It constrains the allowed UV completion by restricting how matter entropy and geometry can jointly evolve — any UV modification must preserve the QFC to avoid paradoxes in semiclassical black hole physics.

### 4. Entropic Action Principle (Bianconi 2025)

**Axiom:** The gravitational action IS the quantum relative entropy S(rho_metric || rho_matter).

Bianconi (Phys. Rev. D 111, 066001, 2025) proposes that gravity derives from the informational relationship between geometry and matter — instead of postulating an action, derive it from relative entropy. Claims include emergent positive Lambda from the G-field and a G-field candidate for dark matter.

**Now scrutinized — verdict: NOT VIABLE as QG theory.** Detailed assessment in [`emergent-gravity/bianconi-entropic-action.md`](../emergent-gravity/bianconi-entropic-action.md). Key issues: entirely classical (no quantization), fourth-order equations with unanalyzed ghost problem, induced metric phenomenologically constructed to reproduce GR, incomplete matter sector (no fermions/gauge fields). Tier 1 validation: FAILS. The idea of gravitational action = relative entropy remains interesting as a principle, but Bianconi's specific implementation is a classical modified gravity theory, not a quantum one. Inflationary predictions (n_s ∈ [0.962, 0.964], r ∈ [0.010, 0.012]) are testable by CMB-S4 but come from an unquantized framework.

## Why These Axioms Are Promising

1. **Physically well-motivated** — rooted in quantum information theory, which is increasingly recognized as the deepest layer of physics
2. **Mathematically sharp** — each is a precise mathematical condition, not a vague principle
3. **Do not presuppose d_s = 2** — but may predict it, or predict something close, as a derived consequence
4. **Connect to established results** — Jacobson's thermodynamic derivation, holographic principle, Swampland constraints
5. **Have not been systematically explored** as constructive axioms for UV-complete theories — this is genuine terra incognita
6. **Could lead to genuinely novel theories** not equivalent to QG+F, AS, HL, string theory, or any existing program

### 5. Modular Flow Unitarity (NEW — from exploration-009)

**Axiom:** The modular Hamiltonian K generates unitary flow: ρ(τ) = e^{iKτ} ρ e^{-iKτ}, requiring K to be self-adjoint and bounded below.

In Lee-Wick quantization, ghost particle creation above threshold spoils positivity of the modular Hamiltonian. The fakeon prescription projects out the ghost, preserving modular flow unitarity. This gives an independent, purely information-theoretic argument for the fakeon: MVEH + modular flow unitarity → fakeon → QG+F.

## What's Been Explored and What Remains

**MVEH (Axiom #2) has now been used constructively** — result: it uniquely produces QG+F through the self-consistency bootstrap. However, this does NOT produce a genuinely novel theory; it provides an alternative derivation of QG+F. The fundamental reason: MVEH operates on entanglement entropy (determined by UV propagator), which is constrained by the same symmetries (diff-invariance, Lorentz invariance, locality, renormalizability) that the no-go theorem already captures.

**Axioms #1, #3, #4 remain unexplored as constructive starting points.** However, QFC (#3) was shown to be insufficient alone (automatically satisfied in 4D quadratic gravity). Relative entropy positivity (#1) constrains coupling signs but requires holographic setup.

**To produce genuinely novel theories from information-theoretic axioms would require:** non-perturbative entanglement structures (beyond standard UV divergence expansion), axioms constraining nonlinear interactions (not just linearized equations), or new definitions of entanglement entropy.

## Relationship to Other Approaches

- The holographic entropy bound (Bousso) is compatible with: string theory (Hagedorn), QG+F (finite UV modes), AS (finite relevant couplings), Lee-Wick (finite complex poles) — necessary but not sufficient alone
- The cosmological constant Lambda ~ 10^{-122} M_P^4 does not select a unique theory — multiple frameworks accommodate it (CST everpresent Lambda, unimodular QG, Bianconi's entropic action) but none is uniquely selected
- Jacobson's framework provides a *tool* for theory construction (mapping UV entanglement structures to gravitational theories), not a specific theory

Also related: "Gravity as a thermodynamic deformation" (2025) — GR as a degenerate Otto cycle, with LIV and energy-momentum non-conservation arising from "work-producing legs." Predicts late-time cosmological acceleration.
