# Exploration 001: Coherent & Squeezed State Resolution of the Gaussian Caveat

## Mission Context

We are testing the Connes-Rovelli Thermal Time Hypothesis (TTH) — the claim that physical time emerges as modular flow. Two prior strategies mapped TTH's domain of validity across 6 regimes. The strongest novel finding (Claim 3) is:

> **Claim 3:** For a one-particle excitation |1_m⟩ of a free scalar field on a half-lattice, the modular flow response δC_local has ZERO spectral weight at the physical mode frequency ω_m. The modular flow oscillates at modular frequencies ε_k/(2π), unrelated to ω_m. The discrepancy grows as N^{0.33} in the continuum limit.

**Critical caveat:** The one-particle state is non-Gaussian. The computation used a Gaussian approximation (correct two-point functions, quadratic modular Hamiltonian). The true modular Hamiltonian has cubic+ terms that COULD contribute spectral weight at ω_m.

**This exploration resolves the caveat** by testing Gaussian states (coherent and squeezed) where the Gaussian modular Hamiltonian is EXACT.

## Your Task

Compute the modular flow response to coherent and single-mode squeezed excitations on the Rindler lattice (free scalar field, half-lattice as subsystem). For these Gaussian states, the Williamson decomposition gives the EXACT modular Hamiltonian — no approximation.

### Part A: Coherent State Test (Analytical + Numerical Verification)

**Setup:** Same Rindler lattice as prior work. Free massless scalar on N sites, Dirichlet BC, right half-lattice as subsystem.

A coherent state |α⟩ = D_m(α)|0⟩ displaces mode m by amplitude α (take α real for simplicity):
- D_m(α) = exp(α b_m† - α b_m)
- ⟨α|φ_j|α⟩ = α √(2/ω_m) U_{j,m} (nonzero mean)
- ⟨α|π_j|α⟩ = 0

**Key property:** The covariance matrix of a coherent state is IDENTICAL to the vacuum:
- X^{(α)}_{ij} = ⟨α|φ_i φ_j|α⟩_connected = ⟨0|φ_i φ_j|0⟩ = X^{(0)}_{ij}
- P^{(α)}_{ij} = P^{(0)}_{ij}

Therefore the modular Hamiltonian K_R^{(α)} has the same quadratic form as the vacuum K_R^{(0)} (with a linear shift and constant). The modular FLOW (automorphisms on the algebra) is identical to the vacuum modular flow.

**Analytical prediction (verify this):**
- δC_local(τ) = C_local^{(α)}(τ) - C_local^{(0)}(τ) = μ_k² = (2α²/ω_m) U_{k,m}² = **constant** (no τ-dependence)
- δC_full(τ) = C_full^{(α)}(τ) - C_full^{(0)}(τ) = (2α²/ω_m) U_{k,m}² cos(ω_m τ) = **oscillates at ω_m**

where μ_k = ⟨α|φ_k|α⟩ and k is a probe site on the right half-lattice.

**Compute at N = 50, 100, 200.** Verify:
1. X_R^{(α)} = X_R^{(0)} to machine precision
2. δC_local = constant (FFT: only DC peak)
3. δC_full oscillates at ω_m (FFT: single peak at ω_m)
4. Vacuum control: for α = 0, everything agrees with prior work

Use α = 1.0 and mode m = N//4 (a mode with significant support on the right half).

### Part B: Single-Mode Squeezed State Test (THE MAIN COMPUTATION)

This is the more informative test. A squeezed state changes the covariance matrix (like the one-particle state does) but remains Gaussian (so the modular Hamiltonian is exact).

**Setup:** Squeezed vacuum |r⟩ = S_m(r)|0⟩ where S_m(r) = exp(r(b_m² - b_m†²)/2).

The correlation matrices are modified by a rank-1 correction:
- X^{(sq)}_{ij} = X^{(0)}_{ij} + U_{i,m} U_{j,m}/(2ω_m) · (e^{-2r} - 1)   [position squeezed for r > 0]
- P^{(sq)}_{ij} = P^{(0)}_{ij} + U_{i,m} U_{j,m} · ω_m/2 · (e^{2r} - 1)     [momentum anti-squeezed]

This is EXACT and the state IS Gaussian. The modular Hamiltonian from Williamson decomposition is EXACT.

**Compute for r = 0.5 and mode m = N//4, at N = 50, 100, 200:**

1. Reduced covariance matrices X_R^{(sq)}, P_R^{(sq)} for the right half-lattice
2. Modular Hamiltonian via Williamson decomposition (exact for this Gaussian state)
3. Modular energies ε_k — compare to vacuum modular energies. How much do they shift?
4. δC_local(τ) = C_local^{(sq)}(τ) - C_local^{(0)}(τ) under modular flow
5. δC_full(τ) = C_full^{(sq)}(τ) - C_full^{(0)}(τ) under full Hamiltonian evolution
6. FFT of both: does δC_local have spectral weight at the physical frequency ω_m?
7. Relative discrepancy: ‖δC_local - δC_full‖ / ‖δC_full‖

**The physical response δC_full should oscillate at ω_m:**
δC_full(τ) = U_{k,m}²/(2ω_m) · (e^{-2r} - 1) · cos(ω_m τ)

**The critical question:** Does δC_local also oscillate at ω_m (same frequency, maybe different amplitude)? Or does it oscillate at modular frequencies ε_k/(2π) (wrong frequencies, like the one-particle case)?

### Part C: Convergence Study for the Squeezed State

Run the squeezed state test at N = 50, 100, 200 with FIXED physical frequency:
- Choose mode index m(N) such that ω_m ≈ 0.3 for all N (i.e., m(N) = round(N × arcsin(0.15)/π))
- Compute the relative discrepancy δ_disc = ‖δC_local - δC_full‖ / ‖δC_full‖ at each N
- Does it grow (like N^{0.33} for the one-particle case), shrink, or plateau?

### Part D: Squeezing Parameter Sweep (if time permits)

Vary r from 0.1 to 1.0 in steps of 0.2 at fixed N = 100, m = N//4:
- How does the discrepancy depend on r?
- At r → 0 the state approaches vacuum (discrepancy should vanish)
- At large r the state is far from vacuum (what happens?)

## Definitions (be precise)

**C_full^{(state)}(τ)** = ⟨state| e^{iHτ} φ_k e^{-iHτ} φ_k |state⟩
where H = full lattice Hamiltonian, k = probe site on right half-lattice.

**C_local^{(state)}(τ)** = Tr[ρ_R^{(state)} · σ_τ(φ_k) · φ_k]
where ρ_R = Tr_L[|state⟩⟨state|], σ_τ(φ_k) = e^{iK_R τ} φ_k e^{-iK_R τ} with K_R = modular Hamiltonian of ρ_R.

For Gaussian states on the lattice, both correlators are computable from the covariance matrices and the modular Hamiltonian matrices h_φ, h_π via matrix exponentials.

## Code Infrastructure

Adapt the existing code:
- Lattice setup, vacuum correlators, Williamson decomposition: use the same approach as in the prior explorations. The key functions (build_lattice, vacuum_correlations, compute_modular_hamiltonian, compute_modular_correlator) are standard.
- The main new code: constructing the squeezed-state covariance matrices with rank-1 corrections.

## Success Criteria

1. **Part A verified:** δC_local = constant for coherent state, δC_full oscillates at ω_m. Numerical matches analytical prediction to machine precision.
2. **Part B — structural mismatch persists:** If δC_local has zero (or negligible) spectral weight at ω_m → Claim 3 is confirmed with NO Gaussian approximation caveat.
3. **Part B — structural mismatch disappears:** If δC_local has spectral weight at ω_m with correct frequency → the Gaussian approximation WAS the issue, and Claim 3 must be weakened for the one-particle case.
4. **Part C completed:** Convergence trend (growing/shrinking/plateau) characterized with power-law fit if applicable.

## Failure Criteria

- Vacuum control check fails (X_R^{(0)} doesn't match prior results)
- Williamson decomposition has reconstruction error > 10^{-8}
- Coherent state covariance matrix differs from vacuum (should be identical — if not, code bug)

## Output

Write your findings to REPORT.md and a concise summary to REPORT-SUMMARY.md in your exploration directory. Include:
- All numerical results in tables
- FFT comparison plots (save as .png)
- The analytical derivation for the coherent state
- The key verdict: does the Gaussian caveat matter?
- Tag all computed results: [COMPUTED], [VERIFIED], or [CONJECTURED]

Save all code to a `code/` subdirectory.
