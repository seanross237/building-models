# Exploration 004 Summary: Final Synthesis + Experimental Connection

## Goal
Final synthesis of the entire TTH mission: complete domain map, experimental connections, "preparation-history time" as a constructive principle, TTH status.

## Outcome: COMPLETE (written by strategizer due to explorer session degradation)

### 1. Complete Domain Map

| # | Regime | State | TTH vs QM | Discrepancy | Verdict | Source |
|---|--------|-------|-----------|-------------|---------|--------|
| 1 | Coupled osc., Gibbs (global) | Equilibrium | ≡ QM | 0% | KNOWN (tautological) | S1-E003 |
| 2 | Coupled osc., Gibbs (local) | Equilibrium | ≠ QM | 82.7% structural | CONFIRMED | S1-E003 |
| 3 | Rindler wedge, vacuum | Vacuum | ≡ boost (BW) | ~15% lattice, converging | KNOWN (BW theorem) | S2-E001 |
| 4 | Coupled osc., post-quench | Non-Gibbs (product) | ≠ QM | 102-160% structural | CONFIRMED | S2-E002, S3-E003 |
| 5 | Coupled osc., squeezed | Non-Gibbs (entangled) | ≈ QM | 0-6.8% quantitative | CONFIRMED | S2-E002, S3-E003 |
| 6 | Rindler, 1-particle (Gauss. approx) | Excited | ≠ QM | ~N^{0.33} | CONFIRMED* | S2-E003 |
| 7 | Rindler, squeezed vacuum (EXACT) | Excited (Gaussian) | ≠ QM | ~N^{0.44} | CONFIRMED | S3-E001 |
| 8 | Rindler, coherent (EXACT) | Displaced (Gaussian) | ≠ QM | constant vs oscillating | CONFIRMED | S3-E001 |

*Gaussian approximation caveat resolved by rows 7-8.

### 2. Experimental Connection

**Setup:** Two coupled optical traps (e.g., double-well BEC) with controllable tunneling λ. Prepare thermal state of uncoupled system, then turn on coupling (quantum quench). Measure single-site density autocorrelation ⟨n_A(t) n_A(0)⟩.

**Timescales (typical cold atom parameters):** ω ~ 2π × 1 kHz, λ ~ 2π × 100 Hz.
- Physical: ω_± = √(ω² ± λ) → beat frequency Δω ≈ λ/ω ≈ 100 Hz → beat period ~10 ms
- TTH: single frequency at ω → period ~1 ms
- The two predictions differ in spectral content (two peaks vs one), resolvable by FFT of ~100 ms time series at ~10 kHz sampling.

**Feasibility:** Quantum gas microscopes (Bakr et al. 2009, Greiner group) can measure single-site observables. Time-resolved correlations at ms timescales are standard. The experiment is feasible with existing technology.

### 3. "Preparation-History Time" as Constructive Principle

The key insight: **modular time = preparation-history time**. The modular flow generates evolution under the Hamiltonian that created the state, not the current physical Hamiltonian.

**New from S3-E003:** The discriminant for TTH validity is **spectrum preservation**: unitary deformations of Gibbs states (squeezing) preserve eigenvalues → quantitative agreement. Non-unitary deformations (quench = different Hamiltonian) change eigenvalues → immediate structural failure.

**Connection to ETH:** The eigenstate thermalization hypothesis says thermal equilibrium is reached when matrix elements in the energy eigenbasis are smooth functions of energy. TTH works when the state is thermal in the eigenbasis of the physical Hamiltonian. When it's thermal in a *different* Hamiltonian's eigenbasis (post-quench), TTH generates the wrong dynamics.

**Constructive value:** The modular spectrum can serve as a probe of preparation history — it reveals the Hamiltonian that created the state. This could be useful as an equilibration diagnostic (modular flow ≈ Hamiltonian flow ↔ equilibrium).

### 4. TTH Status

**Strengths:** Mathematically rigorous, works for vacuum/equilibrium, provides time definition in generally covariant systems.

**Weaknesses:** Generates wrong dynamics for non-equilibrium/excited states; state-dependent; the "preparation-history" dependence limits its utility as a physical time.

**Our contribution:** First systematic computational test across 8 regimes; Gaussian caveat resolved; adversarial review passed; spectrum-preservation discriminant discovered; "preparation-history time" interpretation articulated.

## Claim Status Summary

| Claim | Description | Novelty | Status |
|-------|-------------|---------|--------|
| 1 | Post-quench modular flow = pre-quench dynamics | 2.5/5 | Confirmed, partially known |
| 2 | Product-state identity | 1/5 | Known (Takesaki) |
| 3 | Excited-state structural mismatch, growing with N | 4/5 | **Confirmed (caveat resolved)** |
| 4 | Squeezed = quantitative, quench = structural | 3/5→4/5 | **Confirmed (systematic study)** |
| 5 | Spectrum preservation discriminant | 4/5 | **New finding** |
| Interp. | "Modular time = preparation-history time" | 4/5 | **New interpretation** |
