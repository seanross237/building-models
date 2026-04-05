# PF5 Perturbation Theory: Can "Almost PF₅" Bound Λ?

**Date:** 2026-04-04
**Status:** In progress

## Executive Summary

We develop a perturbation theory for the "almost PF₅" property of the de Bruijn-Newman kernel. The kernel Φ(|u|) satisfies PF₄ globally but fails PF₅ by a margin of only 2.27% (measured by the f₂ coefficient boost needed). We investigate four directions:

1. **Heat flow monotonicity:** Does restoring PF₅ at heat-flow time t = δ imply Λ ≤ δ?
2. **Signed Toeplitz decomposition:** Which theta-function terms drive the D₅ negativity?
3. **Harmless violation argument:** Can approximate PF₅ imply approximate reality of zeros?
4. **Direct computation:** At what heat-flow time t is PF₅ actually restored?

### Key Findings (updating as computed)

*Computation in progress...*

---

## 1. Background

### 1.1 The Setup

The Polya kernel:
$$\Phi(u) = \sum_{n=1}^{\infty} \left[2\pi^2 n^4 e^{9u} - 3\pi n^2 e^{5u}\right] e^{-\pi n^2 e^{4u}}$$

The de Bruijn-Newman heat flow:
$$K_t(u) = e^{tu^2} \Phi(|u|)$$

Key facts from prior investigation (pf4-modular):
- PF₄ holds robustly (D₄ > 0 across 200+ configurations)
- PF₅ fails at (u₀=0.01, h=0.05): D₅ = -1.85 × 10⁻⁹
- The failure is localized to u₀ < 0.0311, h < h_crit(u₀)
- |D₅|/D₄ never exceeds 6.5 × 10⁻⁴
- The Gaussian deformation restores PF₅ at t ~ 11.4 but breaks PF₄ at t ~ 10

### 1.2 The Critical Distinction

The prior investigation found that the Gaussian deformation e^{tu²} does NOT monotonically improve PF order. It "trades" PF orders: restoring PF₅ while breaking PF₄. This means the naive approach (find t where PF₅ is restored, conclude Λ ≤ t) fails.

However, this was checked at the specific configuration (u₀=0.01, h=0.05). We need to understand:
- Does PF₅ restoration happen at DIFFERENT t values for different configurations?
- Is there a configuration-independent t where ALL 5×5 minors become positive?
- What happens at VERY small t (t = 0.001, 0.01)?

---

## 2. Investigation 1: Heat Flow and PF₅ Restoration

### 2.1 Theory

(To be filled after computation)

### 2.2 Computation: D₅ at small t values

(Results pending)

---

## 3. Investigation 2: Signed Toeplitz Minor Analysis

### 3.1 Decomposition of D₅

(To be filled after computation)

---

## 4. Investigation 3: The "Harmless Violation" Argument

### 4.1 Theoretical Framework

(Analysis in progress)

---

## 5. Investigation 4: Direct Computation

### 5.1 Fine-grained heat flow scan

(Results pending)

---

## 6. Conclusions

(To be written)
