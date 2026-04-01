---
topic: SED ħ-expansion hierarchy — Santos Moyal bracket formalism and quantified approximation levels
confidence: verified
date: 2026-03-27
source: "SED strategy-003 exploration-001; Santos 2022 (arXiv:2212.03077); Pesquera & Claverie 1982"
---

## Core Result: The ħ Hierarchy at β=1

For the quartic anharmonic oscillator V = ½x² + βx⁴ at β=1 (natural units ħ=m=ω₀=1):

```
⟨x²⟩_class = 0.183   (classical at T_eff = ħω₀/2 = 0.5)
⟨x²⟩_QM    = 0.258   (full quantum mechanics: O(ħ²) QED)
⟨x²⟩_ALD   = 0.303   (SED/QEDWC with ω³ ZPF: O(ħ) QED)
```

**SED overshoots QM**, not undershoots. The quantum Moyal correction is NEGATIVE — full QM constrains the ground state more tightly than SED predicts. This is counter-intuitive: quantum mechanics is more localized than the classical stochastic simulation.

## Santos (2022) Moyal Bracket Framing

Santos (2022), "On the analogy between stochastic electrodynamics and nonrelativistic quantum electrodynamics," Eur. Phys. J. Plus (arXiv:2212.03077), proves:

**Full QED in the Weyl-Wigner (WW) representation obeys the Moyal equation:**
```
∂F/∂t = {F, H}_M + {F, H_rad}_P
```
where {·,·}_M is the Moyal bracket (quantum) and {·,·}_P is the Poisson bracket (classical).

**The Moyal bracket expands in EVEN powers of ħ:**
```
{W, H}_M = {W, H}_P  +  (ħ²/24) × V'''(x) × ∂³W/∂p³  +  O(ħ⁴)
```

**Truncating to O(ħ) = classical Liouville equation** (Santos' "QEDWC"). This is SED: classical Liouville evolution + ω³ ZPF initial state.

**Proposition 1 (Santos p.13):** SED is formally identical to QEDWC, differing only in the class of allowed initial states.

## The O(ħ²) Correction Term

For the quartic potential V = ½x² + βx⁴: **V'''(x) = 24βx**

The O(ħ²) Moyal correction to the Wigner equation is:
```
Δ(∂W/∂t) = βħ²x × ∂³W/∂p³
```

This term is:
- **Proportional to β** → vanishes for harmonic oscillator (β=0), explaining SED's exactness there
- **Odd in x** (factor x) and **odd in p** (∂³/∂p³) → gives an odd correction ΔW(x,p)

## Symmetry Argument: O(ħ²) Correction to ⟨x²⟩ is ZERO at O(β)

**Novel synthesis (s003 E001):** Since ΔW is odd in x (from βħ²x factor), and x² is even:
```
Δ⟨x²⟩ = ∫∫ x² × ΔW(x,p) dx dp = 0   [odd integrand → zero by symmetry]
```

**Consequence:** SED and QM agree for ⟨x²⟩ at first order in β. The discrepancy between SED and QM for ⟨x²⟩ first appears at **O(β²)** — exactly what Pesquera & Claverie (1982) found analytically (they showed SED fails at O(β²) for ⟨x²⟩ via three independent signatures). This exploration confirms P&C's result from the Moyal perspective.

**Numerical verification:** d⟨x²⟩_QM/dβ|_{β→0} = −1.494 ≈ −3/2 (exact first-order PT); d⟨x²⟩_ALD/dβ|_{β→0} gives the same slope to within numerical precision. Divergence begins at O(β²) in both calculations. ✓

## The Levels of Approximation

| Level | Description | ⟨x²⟩ at β=1 |
|-------|-------------|-------------|
| **O(ħ⁰)**: classical, no ZPF | CED — particle at x=0 at T=0 | 0 (collapses to minimum) |
| **Classical at T_eff=ħω/2**: ZPF as heat bath | Boltzmann at effective temperature | 0.183 |
| **O(ħ) = SED/QEDWC**: classical Liouville + ω³ ZPF | ZPF adds zero-point energy; ω³ feedback overshoots | 0.303 |
| **O(ħ²) = full QM**: Moyal bracket + ZPF | Moyal term REDUCES ⟨x²⟩ from SED value | 0.258 |

The O(ħ²) Moyal correction = ⟨x²⟩_QM − ⟨x²⟩_ALD = 0.258 − 0.303 = **−0.046** (negative).

## Physical Interpretation: Quantum Localization

The O(ħ²) Moyal term represents genuine quantum non-locality — the Wigner function does NOT evolve as a classical probability distribution. For the quartic potential, this quantum non-locality makes the ground state **narrower (more localized)** than the classical stochastic process predicts.

This is the deep physical insight: **quantum mechanics is MORE constrained, not less, than SED for nonlinear systems.** The ω³ ZPF drives SED into an over-spread distribution, while the Moyal correction pulls it back toward the compact quantum ground state.

## Santos' Qualitative Prediction and Its Limits

Santos (p.13–14): "We should expect that SED fails badly for Hamiltonians not quadratic. Indeed the neglect of terms O(ħ²)... may produce **errors of order (ħω/E)²**, where in the microscopic (quantum) domain ħω/E is of order unity."

This correctly predicts the direction (SED overshoots QM) and scaling (∝β) of the anharmonic discrepancy. However, Santos does NOT provide:
- An independent numerical prediction for the 0.046 magnitude (requires running the ALD simulation)
- An analytic formula for ⟨x²⟩_SED in terms of β
- A prediction for the tunneling slope deviation (slope=1.049 — see note below)

**Status:** Santos framework provides Tier 4 validation (explains, confirms direction+scaling) but not Tier 5 (independent numerical prediction).

## Note: Slope=1.049 in Tunneling Formula is NOT an O(ħ²) Effect

Analysis of three O(ħ²) mechanisms for the double-well:
1. **Anharmonic energy correction** δE = −λ/4 in well minimum: gives λ-dependent slope correction → vanishes for deep barriers → **cannot explain constant 4.9% deviation over 4 decades**
2. **O(ħ²) prefactor correction**: shifts intercept only, not slope
3. **Higher-order WKB correction**: also vanishes for deep barriers

**Conclusion:** Slope=1.049 is most likely a finite-τ and/or finite-ω_max simulation artifact. The convergence rate τ^0.23 × ω_max^(−0.18) is very slow, but directionally toward slope=1.0 in the physical limit.

## References

- Santos, E. (2022). "On the analogy between stochastic electrodynamics and nonrelativistic quantum electrodynamics." Eur. Phys. J. Plus 137, 1409. arXiv:2212.03077.
- Pesquera, L. & Claverie, P. (1982). "The quartic anharmonic oscillator in stochastic electrodynamics." J. Math. Phys. 23(7), 1315–1322.
- SED strategy-003 exploration-001 (2026-03-27): quantified hierarchy + symmetry argument.
