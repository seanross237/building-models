---
topic: Modular Hamiltonian catalog — four explicit systems for TTH analysis
confidence: verified
date: 2026-03-27
source: thermal-time/strategies/strategy-001/explorations/exploration-001/REPORT.md; primary refs: Bisognano & Wichmann (1975,1976), Casini & Huerta (2009), Connes & Rovelli (1994)
---

## Summary

Explicit modular Hamiltonians for four canonical systems, establishing the mathematical toolkit for analyzing the Connes-Rovelli Thermal Time Hypothesis (TTH). Each system illustrates a qualitatively different regime of the Tomita-Takesaki modular theory.

## Background: Tomita-Takesaki Theory

Given a von Neumann algebra M, Hilbert space H, and faithful normal state ω with cyclic separating vector Ω:
- Modular operator: Δ_ω = S†S (where S closes the operator S(aΩ) = a*Ω)
- Modular Hamiltonian: K = −log Δ_ω, so Δ_ω = e^{−K}
- Modular group: σ_t^ω(a) = Δ_ω^{it} a Δ_ω^{−it}
- For density matrix ρ on finite-dim space: K = −log ρ (up to additive constant)

## System 1: Rindler Wedge (Bisognano-Wichmann Theorem)

**Reference:** Bisognano & Wichmann, J. Math. Phys. 16 (1975), 985; 17 (1976), 303.

**Setup:** Minkowski vacuum |0⟩ restricted to the right Rindler wedge W_R = {x^1 > |x^0|}.

**Result (theorem, not conjecture):**
```
K = 2π K_boost = 2π ∫_{W_R} d^{d-1}x  x^1  T^{00}(x)
```

**Modular flow:** σ_t(φ(x^0, x^1)) = φ(x^0 cosh(2πt) + x^1 sinh(2πt), x^0 sinh(2πt) + x^1 cosh(2πt)) — Lorentz boost with rapidity 2πt. Maps wedge to itself.

**Physical meaning:** KMS condition gives Unruh temperature T_U = ℏa/(2πc k_B). The vacuum restricted to W_R is thermal at T_U with respect to this flow. This is the **prototype case where TTH is exact by theorem**: modular flow IS proper-time evolution for the Rindler observer. (TTH asserts this extends to all states; the BW theorem establishes it for the vacuum.)

## System 2: Two-Qubit Bell State (Maximally Mixed Marginal)

**State:** |Φ+⟩ = (|00⟩+|11⟩)/√2 on H = ℂ² ⊗ ℂ², subsystem A.

**Reduced state:** ρ_A = Tr_B[|Φ+⟩⟨Φ+|] = I/2.

**Modular Hamiltonian:** K_A = −log(I/2) = log(2)·I (scalar multiple of identity).

**Modular flow:** σ_t(a) = (1/2I)^{it} a (1/2I)^{−it} = e^{−it log 2} a e^{it log 2} = a (trivial).

**Implication for TTH:** Maximally mixed state → trivial modular flow → TTH predicts no time evolution. Maximum entanglement/entropy = no preferred time direction. Illustrates the extreme limit: maximum ignorance about a subsystem yields no modular dynamics.

## System 3: Harmonic Oscillator Thermal State

**State:** ρ = e^{−βH}/Z on ℓ²(ℕ), H = ω a†a.

**Modular Hamiltonian:** K = βH + log Z · I = β ω a†a + const (up to scalar).

**Modular operator:** Δ = e^{−K} = e^{−βH}/Z = ρ (up to normalization).

**Modular flow:** σ_t(a) = e^{itK} a e^{−itK} = e^{−iβωt} a; σ_t(a†) = e^{+iβωt} a†.

This is Heisenberg evolution under H with rescaled time τ = βt. The KMS condition is satisfied by construction (Takesaki's theorem).

**Implication for TTH:** For a thermal state, TTH (with normalization τ=β·t) exactly reproduces standard QM time evolution. TTH is consistent with standard QM but adds no new predictions in the thermal equilibrium regime. Novel content of TTH appears only for non-equilibrium and entangled states.

## System 4: CFT Vacuum on Interval [0,L] (Casini-Huerta)

**Reference:** Casini & Huerta, J. Phys. A 42 (2009), 504007.

**State:** 1+1d CFT vacuum restricted to interval [0, L] on the t=0 slice.

**Modular Hamiltonian:**
```
K_A = 2π ∫_0^L dx  [(L−x)x/L]  T_{00}(x)
```

Weight function f(x) = (L−x)x/L: quadratic, vanishes at endpoints x=0 and x=L, peaks at L/2 with value L/4.

**Modular flow:** Conformal (Möbius) transformation fixing endpoints:
```
g_t(x) = L · e^{2πt}(x/L) / [1 + (e^{2πt}−1)(x/L)]
```

**Entanglement entropy:** S_A = ⟨K_A⟩ = (c/3) log(L/ε) (universal CFT result, c = central charge, ε = UV cutoff).

**Key structural feature:** Modular Hamiltonians can be **non-local** — K_A integrates T_{00} with a position-dependent weight, unlike physical Hamiltonians. This non-locality is characteristic of modular Hamiltonians in interacting theories and grows with subsystem entanglement.

## Spectrum Summary

| System | State | K | Modular flow | Non-locality |
|--------|-------|---|-------------|--------------|
| Rindler wedge (BW) | Minkowski vacuum | 2π·(boost generator) | Lorentz boost | Integral over wedge |
| Bell state | Max entangled | log(2)·I | Trivial (identity) | None |
| HO thermal | Gibbs e^{−βH}/Z | βH + const | Heisenberg at rate β | Local |
| CFT interval | CFT vacuum | 2π·∫[(L−x)x/L]T₀₀dx | Möbius map | Non-local (position-weighted) |
