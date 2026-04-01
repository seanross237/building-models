# Exploration 001 — REPORT SUMMARY

**Phase:** 1 (Mathematical Toolkit Establishment)
**Status:** Complete
**Date:** 2026-03-27

---

## What Was Done

Cataloged explicit modular Hamiltonians for 4 systems, formalized the TTH prediction for a bipartite temperature-gradient system, identified and computed the discriminating observable.

## Key Findings

### Modular Hamiltonian Catalog

1. **Rindler wedge (Bisognano-Wichmann):** K = 2π · K_boost = 2π ∫ x¹ T₀₀ dx. Modular flow = Lorentz boost at rapidity 2πt. TTH is exact here (Unruh effect). This is the well-established benchmark.

2. **Maximally mixed Bell state:** K_A = log(2) · I (scalar). Modular flow is trivial. TTH predicts no time evolution for maximum-entropy subsystems. Instructive edge case.

3. **Thermal harmonic oscillator:** K = β H. Modular flow = physical time evolution at speed β. TTH agrees with standard QM in equilibrium — the non-trivial content of TTH is for non-equilibrium states.

4. **CFT interval (Casini-Huerta):** K_A = 2π ∫₀ᴸ [(L-x)x/L] T₀₀(x) dx. Non-local modular Hamiltonian. Modular flow is a conformal Möbius transformation of the interval.

### TTH vs Standard QM Predictions (Bipartite System)

For two thermal oscillators at β_A ≠ β_B:

- **TTH:** Modular Hamiltonian K_{AB} = β_A H_A + β_B H_B. Position autocorrelation C(t) oscillates at **β_A · ω_A**.
- **Standard QM:** Heisenberg evolution gives C(t) oscillating at **ω_A** (with Lindblad damping at rate Γ = λ² coth(β_B ω_B/2)).

### Discriminating Observable (Computed)

**C(t) = ⟨x_A(t) x_A(0)⟩** with β_A = 2.0, ω_A = 1.0:

| Prediction | Formula | Oscillation Frequency |
|---|---|---|
| TTH | 0.6565 · cos(2.0 · t) | **2.0** |
| Standard QM | 0.6565 · cos(1.0 · t) · e^{-0.020 t} | **1.0** |

The predictions disagree by a factor of β_A. Maximum discrimination at t = π/4 (TTH nodes, QM half-amplitude) and t = π/2 (QM nodes, TTH = -0.66).

### Central Ambiguity Identified

TTH's novel claim requires identifying modular time t with physical time τ. For a thermal state at β_A ≠ 1, this identification causes C(t) to oscillate at β_A ω_A instead of ω_A — a factor of β_A discrepancy from standard QM. This is the parameter that Phase 2 explorations should target: whether there exists a consistent normalization (τ = t/β_A?) that reconciles TTH with standard QM, or whether TTH makes a genuinely distinct observable prediction.

## Deliverables

- `REPORT.md` — full 350-line derivation
- `code/modular_hamiltonian.py` — full computation with plots
- `code/modular_flow_comparison.png` — 4-panel comparison figure

## Next Steps for Strategy

Phase 2 should: (1) address the time-normalization ambiguity quantitatively, (2) look for a physical setup where the β_A factor is observable (ultracold quantum optics?), and (3) examine whether adding the interaction H_int modifies the TTH-vs-QM discrepancy or resolves it.
