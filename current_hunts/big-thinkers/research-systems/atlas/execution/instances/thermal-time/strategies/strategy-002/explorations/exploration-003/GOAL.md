# Exploration 003 — Excited-State Modular Flow in the Rindler Wedge

## Mission Context

You are testing the most conceptually important prediction of the Connes-Rovelli Thermal Time Hypothesis (TTH): whether time evolution is state-dependent in QFT.

**Background from strategy-001:**
- TTH says physical time IS modular flow: σ_t^ω, the modular automorphism group of the state ω
- For the Minkowski vacuum restricted to a Rindler wedge, the Bisognano-Wichmann (BW) theorem guarantees K = 2π × (boost generator). Modular flow = Lorentz boost. TTH agrees with standard physics.
- But the modular Hamiltonian DEPENDS ON THE STATE. For an excited state, K changes but the "physical" dynamics (Hamiltonian, boosts) don't.
- If C_local^{(1)} ≠ C_full^{(1)} for an excited state, TTH gives **state-dependent time evolution** — a radical prediction meaning different observers in different states experience genuinely different time flows.
- Normalization: τ_physical = β × t_modular (β = 2π for Rindler)

## Specific Goal

Compute and compare the modular flow correlator vs. the full QM correlator for a **one-particle excited state** of a free scalar field on a 1+1D lattice, with the right half-lattice as the subsystem (lattice Rindler analogue).

## Detailed Setup

### Stage 1: Build the lattice (same as Probe 1)

Free massless scalar field on N sites (start with N = 50, verify at N = 100):
```
H = (1/2) Σ_i [π_i² + (φ_{i+1} - φ_i)²]
```
Diagonalize to get normal modes ω_k and mode operators b_k. The vacuum |0⟩ is the state annihilated by all b_k.

### Stage 2: Vacuum baseline (control)

Compute the vacuum-state comparison first (this should reproduce Exploration 001's result):
- Correlation matrix C^{(0)}_{ij} = ⟨0|a†_i a_j|0⟩ for the right sublattice
- Modular Hamiltonian h^{(0)} = log((1 - C^{(0)}) / C^{(0)}) (Peschel formula)
- Both correlators C_local^{(0)} and C_full^{(0)} at a probe site k

Verify agreement (BW theorem). This is your control.

### Stage 3: One-particle excited state

Prepare the state |1_m⟩ = b†_m |0⟩ where b_m is the creation operator for normal mode m. Choose m such that the mode is **localized near the boundary** between left and right sublattices (this maximizes the effect on the reduced state — modes deep in the bulk barely change ρ_R).

Specifically:
- Pick the mode m whose spatial profile has maximum amplitude near site N/2 (the boundary)
- The excited state is |1_m⟩ = b†_m |0⟩

### Stage 4: Reduced state and modular Hamiltonian for excited state

The reduced state of the right sublattice in the excited state is:
```
ρ_R^{(1)} = Tr_L[ |1_m⟩⟨1_m| ]
```

For a one-particle excitation of a free field, this is **not** a Gaussian state (it's a rank-2 perturbation of the Gaussian vacuum reduced state). There are two approaches:

**Approach A (Direct, preferred for small N):**
Compute |1_m⟩ explicitly in the lattice Fock space. Trace over the left sublattice sites to get ρ_R^{(1)} as a matrix. Then K_R^{(1)} = -log(ρ_R^{(1)}).

This is feasible for small N (N ≤ 30 gives a half-lattice of 15 sites). For free fields, the one-particle sector restricted to one sublattice has dimension equal to the number of right-sublattice sites, so ρ_R^{(1)} acts in a manageable space.

**IMPORTANT NOTE on Hilbert space:** For a lattice of N oscillators, the full Hilbert space is infinite-dimensional (Fock space per site). But for the one-particle sector, the state lives in a subspace of dimension N (one excitation shared among N sites). The restriction to the right sublattice of a one-particle state gives a reduced state that acts on the Fock space of the right sublattice — but effectively only involves the 0- and 1-particle sectors.

**Approach B (Perturbative, fallback):**
Use first-order perturbation theory:
```
δK = K_R^{(1)} - K_R^{(0)} ≈ perturbative correction
```
For a single-particle excitation, Lashkari (2016, arXiv:1508.03506) gives a formula for δK in CFT. On the lattice, the analogous formula involves the resolvent of ρ_R^{(0)} and the perturbation δρ_R = ρ_R^{(1)} - ρ_R^{(0)}.

Use Approach A if computationally feasible. Fall back to Approach B if the direct computation exceeds memory/time for the desired N.

### Stage 5: Compute both correlators for excited state

**C_local^{(1)}(τ):** Evolution under the modular Hamiltonian K_R^{(1)} of the excited state:
```
C_local^{(1)}(τ) = Tr[ρ_R^{(1)}  e^{i K_R^{(1)} τ/(2π)}  φ_k  e^{-i K_R^{(1)} τ/(2π)}  φ_k]
```
(normalized by 2π since the Rindler inverse temperature is 2π)

**C_full^{(1)}(τ):** Full QM evolution under the lattice Hamiltonian H:
```
C_full^{(1)}(τ) = ⟨1_m| φ_k(τ) φ_k(0) |1_m⟩
```
where φ_k(τ) = e^{iHτ} φ_k e^{-iHτ}.

### Stage 6: Compare and characterize

1. **Discrepancy:** ||C_local^{(1)} - C_full^{(1)}|| / ||C_full^{(1)}||
2. **Spectral analysis (FFT):** Do the two correlators have the same or different frequency content?
3. **State-dependence:** Compare δC = C_local^{(1)} - C_local^{(0)} (the change in modular flow correlator due to the excitation) vs. δC_full = C_full^{(1)} - C_full^{(0)} (the physical change). Does the modular flow "see" the excitation in the same way as the physical dynamics?
4. **Key question:** Is the discrepancy (if any) due to state-dependent time flow, or is it a finite-size artifact? Check by varying N.

## Control Checks (MANDATORY)

1. **Vacuum limit:** For |0⟩ instead of |1_m⟩, C_local^{(0)} should agree with C_full^{(0)} (BW theorem). This is your baseline.

2. **Normalization:** ρ_R^{(1)} must have trace 1 and be positive semidefinite.

3. **Equal-time check:** At τ = 0, C_local^{(1)}(0) = C_full^{(1)}(0) = ⟨1_m|φ_k²|1_m⟩.

## Success Criteria

- **Strong success:** C_local^{(1)} ≠ C_full^{(1)} with a discrepancy that persists and is characterized as N → ∞. This would mean TTH predicts state-dependent time — a radical, potentially falsifiable prediction.
- **Moderate success:** C_local^{(1)} ≈ C_full^{(1)} even for the excited state (perhaps due to special properties of type III algebras). This would be a deep structural result — the modular flow "knows" about the correct dynamics even for non-vacuum states.
- **Partial success:** The perturbative approach (Approach B) gives δK and a first-order correction to the correlator, even if the full computation is infeasible.
- **Failure:** Unable to compute K_R^{(1)} by either approach. Document what would be needed.

## Failure Paths

- **If direct computation (Approach A) exceeds memory:** Fall back to Approach B. Even the first-order δC is scientifically valuable.
- **If the vacuum baseline (control) fails:** Debug the lattice setup before attempting the excited state. The BW result is a theorem — lattice disagreement means a code bug or insufficient N.
- **If the one-particle state gives trivial results (ρ_R^{(1)} ≈ ρ_R^{(0)}):** The mode m may be too far from the boundary. Try multiple modes. If all modes give ρ_R^{(1)} ≈ ρ_R^{(0)}, this is itself a result — it means single-particle excitations don't significantly modify the reduced state of the half-space (plausible for UV modes).

## Output

Write REPORT.md and REPORT-SUMMARY.md in this directory. Include:
1. Vacuum baseline: C_local^{(0)} vs C_full^{(0)} discrepancy
2. Excited state: C_local^{(1)} vs C_full^{(1)} discrepancy
3. State-dependence analysis: δC_local vs δC_full
4. Spectral comparison (FFT)
5. Convergence with N (if multiple N tested)
6. Discussion: does TTH give state-dependent time? What does this mean?
7. All code in a `code/` subdirectory

## Your exploration directory
Write all output to: the current directory (where this GOAL.md is located).
