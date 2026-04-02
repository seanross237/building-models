# Exploration 002 — Non-Equilibrium TTH Test (Post-Quench State)

## Mission Context

You are testing the Connes-Rovelli Thermal Time Hypothesis (TTH) in a regime where it makes genuinely novel predictions: non-equilibrium states.

Strategy-001 established:
- **For Gibbs states:** K_AB = βH_AB exactly → global TTH ≡ QM. The modular flow is just rescaled Hamiltonian evolution.
- **For non-Gibbs states:** K_AB ≠ βH_AB → global TTH generates dynamics DIFFERENT from Hamiltonian evolution. This is the regime where TTH has genuine non-trivial content even for non-relativistic systems.
- **Normalization:** τ_physical = β × t_modular
- **Strategy-001 code infrastructure** exists at `../../strategy-001/explorations/exploration-003/code/compute_correlators.py` — a Fock-space toolkit for coupled oscillators with partial trace, modular Hamiltonian computation, and correlator comparison.

**This is the probe most likely to find genuine novel content.** For non-Gibbs states, the global modular flow is not just a rescaling of Hamiltonian evolution — it's genuinely different dynamics. If the discrepancy is interesting (not just "modular flow is wrong"), it could reveal what TTH's modular time "means" physically for non-equilibrium situations.

## Specific Goal

Compute three correlators for a **post-quench state** of coupled harmonic oscillators, and determine whether TTH's modular time makes physically meaningful predictions for non-equilibrium states.

## Detailed Setup

### The System
Two coupled harmonic oscillators:
```
H_AB(λ) = ½(p_A² + ω²q_A²) + ½(p_B² + ω²q_B²) + λ q_A q_B
```
with ω = 1.0, and coupling λ to be varied.

### The Non-Gibbs State (Post-Quench)
1. Start with the system at inverse temperature β = 2.0 in the UNCOUPLED state (λ = 0):
   ```
   ρ_0 = e^{-β H_AB(0)} / Z_0
   ```
   This is the thermal state of the uncoupled system.

2. At t = 0, instantaneously turn on the coupling to λ > 0. The state ρ_0 is now NOT the Gibbs state of H_AB(λ). Therefore:
   ```
   K_AB = -log(ρ_0) = β H_AB(0) + const ≠ β H_AB(λ) for any β
   ```
   The modular Hamiltonian of the full state is the uncoupled Hamiltonian, not the coupled one.

### The Three Correlators

Use the position operator x_A for all correlators. Use Fock space truncation with N = 20 levels per mode (consistent with strategy-001).

**C_QM(τ):** Standard quantum mechanics — evolve under the COUPLED Hamiltonian H_AB(λ):
```
C_QM(τ) = Tr[ρ_0  e^{i H_AB(λ) τ}  x_A  e^{-i H_AB(λ) τ}  x_A]
```
This is what actually happens physically after the quench.

**C_global_TTH(τ):** TTH prediction using global modular flow of ρ_0:
```
C_global_TTH(τ) = Tr[ρ_0  e^{i K_AB τ/β}  x_A  e^{-i K_AB τ/β}  x_A]
   = Tr[ρ_0  e^{i H_AB(0) τ}  x_A  e^{-i H_AB(0) τ}  x_A]
```
Since K_AB = β H_AB(0) + const, modular flow at rate 1/β generates evolution under H_AB(0) — the UNCOUPLED Hamiltonian. TTH says this is the "time evolution" defined by the state.

**C_local_TTH(τ):** TTH prediction using local modular flow of ρ_A = Tr_B[ρ_0]:
```
C_local_TTH(τ) = Tr[ρ_A  e^{i K_A τ/β}  x_A  e^{-i K_A τ/β}  x_A]
```
where K_A = -log(ρ_A) and ρ_A = Tr_B[ρ_0].

### Parameter Sweep
Run for λ = 0.1, 0.2, 0.3, 0.5 (same values as strategy-001 for direct comparison).

## Analysis Tasks

For each λ:

1. **Quantify the discrepancies:**
   - ||C_QM - C_global_TTH|| / ||C_QM|| (this should be > 0 for λ > 0, unlike in strategy-001!)
   - ||C_QM - C_local_TTH|| / ||C_QM||

2. **Spectral analysis (FFT):**
   - What frequencies appear in C_QM? (Should be the normal modes ω_± = √(ω²±λ) of the coupled system)
   - What frequencies appear in C_global_TTH? (Should be ω = 1.0, the uncoupled frequency, since evolution is under H_AB(0))
   - What frequencies appear in C_local_TTH?
   - Is the discrepancy **structural** (different frequency content) or **quantitative** (same frequencies, different amplitudes)?

3. **Characterize what modular time "means":**
   - C_global_TTH evolves under the pre-quench Hamiltonian. Physically, the modular flow "remembers" the pre-quench dynamics and ignores the post-quench coupling. Is this an interesting physical prediction or just "TTH uses the wrong Hamiltonian"?
   - Does the modular flow C_global_TTH bear any relationship to C_QM? (e.g., do they share any common spectral features?)

4. **Check a second non-equilibrium state** (if time permits):
   Prepare a squeezed thermal state: apply the squeezing operator S(r) = exp[r(a²-a†²)/2] with r = 0.3 to the thermal state of H_AB(λ=0.3). Compute the same three correlators. Does the pattern hold?

## Control Checks (MANDATORY)

1. **Gibbs state control:** Before running the non-Gibbs state, verify that for the GIBBS state ρ_Gibbs = e^{-β H_AB(λ)}/Z (at the same λ), C_global_TTH = C_QM to machine zero. This reproduces strategy-001's control check and validates your code.

2. **Uncoupled control:** At λ = 0, the post-quench state IS the Gibbs state of the "new" Hamiltonian (since H_AB(0) = H_AB(0)). So all three correlators should agree at λ = 0.

3. **Trace and positivity:** Check that ρ_0 has trace 1 and is positive semidefinite after Fock truncation.

## Success Criteria

- **Success:** C_QM ≠ C_global_TTH for λ > 0 (confirming TTH makes a different prediction for non-Gibbs states), with a clear characterization of the discrepancy (structural: different frequencies; specifically, C_global should show uncoupled ω while C_QM shows coupled ω_±).
- **Bonus success:** A physically interesting interpretation of what modular time means for non-equilibrium states.
- **Failure:** If C_QM = C_global_TTH even for non-Gibbs states (would be very surprising — would mean there's a deeper equivalence). Verify carefully before concluding.

## Failure Paths

- **If the Gibbs state control fails:** Your code has a bug. Debug using the strategy-001 results as reference (C_global = C_full at machine zero for Gibbs state at λ=0.3).
- **If Fock truncation is inadequate for the quench state:** The quench state may have higher occupation numbers than the equilibrium state. Check convergence by increasing N from 20 to 25.

## Code Approach

You can adapt the strategy-001 code at `../../strategy-001/explorations/exploration-003/code/compute_correlators.py`. The key modifications needed:
1. Build ρ_0 as the thermal state of H_AB(0) instead of H_AB(λ)
2. Build K_AB = -log(ρ_0) = β H_AB(0) + const (instead of β H_AB(λ))
3. Build K_A by partial tracing ρ_0 over B and taking -log
4. Evolve C_QM under H_AB(λ), C_global under K_AB/β = H_AB(0), C_local under K_A/β
5. Add FFT spectral analysis

## Output

Write REPORT.md and REPORT-SUMMARY.md in this directory. Include:
1. Discrepancy table: ||C_QM - C_global||/||C_QM|| and ||C_QM - C_local||/||C_QM|| for each λ
2. FFT frequency content of all three correlators
3. Comparison table: Gibbs vs. post-quench results side-by-side
4. Physical interpretation section: what does modular time "mean" for non-equilibrium states?
5. All code in a `code/` subdirectory

## Your exploration directory
Write all output to: the current directory (where this GOAL.md is located).
