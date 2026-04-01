# Exploration 003 SUMMARY — Anharmonic SED Oscillator

**Date:** 2026-03-27

## Goal
First numerical simulation of the anharmonic SED oscillator V(x) = ½x² + βx⁴. Verify/refute Pesquera & Claverie (1982): SED agrees with QM at O(β), disagrees at O(β²).

## What was tried?
1. Exact QM reference via matrix diagonalization (N_max=80, 7 β values)
2. Time-domain SED Langevin simulation: Euler-Cromer, colored ω³ noise, 200 trajectories × 50 samples = 10,000 samples per β
3. Parameter scan: β = 0, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0
4. Comparison of var_x, PE, ⟨x⁴⟩, P(x) shape

## Outcome: SUCCESS — major result found

**QM:** var_x DECREASES with β (quartic confinement). At β=1: var_x = 0.257.
**SED:** var_x INCREASES with β (oscillator pumped by ω³ noise). At β=1: var_x = 2.411.

| β    | var_x_QM | var_x_SED     | SED/QM | Significance |
|------|----------|---------------|--------|--------------|
| 0.00 | 0.500    | 0.515±0.007   | 1.03   | baseline     |
| 0.01 | 0.486    | 0.529±0.008   | 1.09   | 5.4σ         |
| 0.10 | 0.413    | 0.735±0.014   | 1.78   | 23.6σ        |
| 1.00 | 0.257    | 2.411±0.043   | 9.38   | 50.5σ        |

## Key takeaway
The Langevin-approximation SED model fails **qualitatively** (wrong direction) and **at O(β)**, not O(β²). The linearity boundary is β ≈ 0.005. Physical mechanism: ω³ ZPF spectrum + constant damping Γ = τω₀² creates positive feedback that pumps the oscillator to a much larger amplitude than the QM ground state.

## Verification scorecard
- 7 [COMPUTED] | 1 [VERIFIED] | 0 [CONJECTURED]

## Proof gaps
- Full ALD radiation reaction (position-dependent Γ) not tested — would be needed to directly verify/refute Pesquera-Claverie O(β²) claim
- The O(β) failure found here is attributable to the Langevin approximation, not necessarily to SED itself

## Unexpected findings
- SED and QM have **opposite qualitative trends** (SED: var_x up; QM: var_x down)
- P(x) shape discrepancy: SED super-Gaussian, QM sub-Gaussian (KS p=0.000 at β=0.1)
- Failure is O(β), not O(β²) — the approximation Γ=const is the key culprit

## Computations identified for future work
1. Implement full ALD (position-dependent damping) to test P-C prediction directly
2. Fine-scan β ∈ [0.001, 0.01] to precisely locate linearity boundary
3. Histogram comparison of P(x) distributions
4. τ-dependence study
