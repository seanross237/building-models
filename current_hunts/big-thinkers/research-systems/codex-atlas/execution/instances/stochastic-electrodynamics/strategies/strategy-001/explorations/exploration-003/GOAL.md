# Exploration 003 — Anharmonic SED Oscillator: First Numerical Test of the Linearity Boundary

## Mission Context

We are investigating Stochastic Electrodynamics (SED) — classical electrodynamics plus a real zero-point radiation field. SED successfully reproduces the QM harmonic oscillator ground state (our exploration 001 confirmed this: position variance matches to 1.4%). But SED is known to FAIL for nonlinear systems.

Pesquera & Claverie (1982, J. Math. Phys. 23(7), 1315–1322) proved ANALYTICALLY that for the quartic anharmonic oscillator V(x) = ½mω₀²x² + βx⁴, SED agrees with QM at order β (first-order perturbation theory) but DISAGREES at order β² (second-order). This has NEVER been verified numerically. Your job is to do that verification — the first numerical simulation of the anharmonic SED oscillator.

## Your Task

This is a **computation task.** Write and run Python code.

### Part 1: Compute QM reference values

Using scipy/numpy, compute the exact QM ground state energy and position distribution for the anharmonic oscillator V(x) = ½x² + βx⁴ (natural units: m=1, ω₀=1, ℏ=1):

1. **Matrix diagonalization:** Represent H = -½ d²/dx² + ½x² + βx⁴ in the harmonic oscillator basis (|n⟩, n=0,1,...,N_max). Diagonalize for N_max ≥ 50 (convergence check). Extract E₀(β) for β = 0, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0.
2. **Perturbation theory check:** Verify against E₀ = 0.5 + 0.75β - 2.625β² + ... for small β.
3. **Position distribution:** For each β, compute the QM ground state wavefunction ψ₀(x) and its variance var_x_QM.

Save these reference values — they are the targets the SED simulation must match.

### Part 2: SED time-domain simulation

Simulate the anharmonic SED Langevin equation:

    ẍ = -ω₀²x - 4βx³ - Γẋ + F_zpf(t)

where:
- Γ = τω₀² is the radiation reaction damping (use τ = 0.01)
- F_zpf(t) has power spectral density S_F(ω) = 2τℏω³/m (THIS IS THE CORRECTED NORMALIZATION — verified in our exploration 001)

**CRITICAL IMPLEMENTATION NOTES:**

1. **Time-domain simulation is required.** The frequency-domain approach (which worked for the harmonic oscillator) breaks for nonlinear systems because modes couple. You MUST solve the ODE in the time domain.

2. **UV divergence warning.** The velocity variance is UV-divergent (grows with frequency cutoff). This is a real physics effect, not a bug. **Focus on POSITION-based observables** (position variance var_x, position distribution P(x), potential energy PE) which are UV-convergent. Do NOT use total energy as the primary comparison — it requires mass renormalization.

3. **Cutoff strategy.** Use a frequency cutoff ω_max = 10ω₀ (i.e., dt = 2π/(20*ω₀) = π/10 ≈ 0.314). This captures the resonant physics around ω₀ while keeping the UV contamination manageable. For the harmonic case (β=0), this cutoff gives var_x ≈ 0.51 (vs target 0.5), so expect ~2% systematic from the cutoff.

4. **Noise generation.** Generate colored noise with S_F(ω) ∝ ω³ spectrum using FFT: generate white noise, FFT, multiply by sqrt(S_F(ω)), IFFT. Pre-generate the entire noise time series before the ODE integration.

5. **Integration scheme.** Use a symplectic integrator (Velocity Verlet or similar). The nonlinear force -4βx³ couples to the linear force -ω₀²x, so you need small enough dt to resolve the dynamics. Suggested dt = 0.05 (about 125 steps per oscillation period) to start.

6. **Ensemble and equilibration.**
   - Run N_ensemble ≥ 500 trajectories (more is better for statistics)
   - Equilibration: discard the first 50% of each trajectory (at least 100/Γ = 10000 time units)
   - Total simulation time per trajectory: at least 200/Γ = 20000 time units
   - Sample the position at a single late time point from each trajectory for the ensemble distribution

7. **Run parameter regimes sequentially, not all at once.** Run one β value, print results, then run the next. Do NOT try to run all β values in a single script invocation — this risks timeout.

### Part 3: Compare SED vs. QM

For each β value (0, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0):
1. Report: var_x_SED vs. var_x_QM (with ± uncertainties)
2. Report: PE_SED = ½ω₀²var_x + β⟨x⁴⟩_SED vs. PE_QM = ⟨V(x)⟩_QM
3. Test whether P(x) in SED matches |ψ₀(x)|² from QM (KS test or chi-squared)
4. **Verify the β=0 case recovers the harmonic oscillator** (var_x ≈ 0.5) — this is your sanity check.

### Part 4: Identify the SED-QM divergence

1. Plot or tabulate the fractional difference (var_x_SED - var_x_QM)/var_x_QM as a function of β.
2. Does the agreement hold at small β and break at large β, as Pesquera & Claverie predict?
3. At what β value does the discrepancy exceed the statistical uncertainty? This is the "linearity boundary" for this observable.
4. For the largest β values, characterize HOW SED differs from QM: is the position distribution too wide, too narrow, or a different shape?

## Success Criteria

- QM reference values computed for ≥ 5 β values via matrix diagonalization
- SED simulation runs for ≥ 4 β values including β=0 (harmonic check)
- β=0 harmonic check: var_x agrees with 0.5 to within 5%
- For at least one β > 0: a quantitative comparison between SED and QM position statistics is produced
- A clear statement of whether SED and QM agree or disagree, with numerical precision

## Failure Criteria

- If the SED simulation is numerically unstable for β > 0 (trajectories diverge), document: at what β? After how many time steps? Try reducing β until you find a stable regime. Even β = 0.001 is interesting if it shows the beginning of SED-QM divergence.
- If computational time is a bottleneck, reduce N_ensemble to 200 and reduce β scan to {0, 0.1, 1.0}.
- If the SED-QM discrepancy is smaller than statistical noise for all β, report that as a finding (it would mean the perturbative prediction fails to capture the dominant effect).

## Deliverables

Write your findings to:
- `explorations/exploration-003/REPORT.md` — full report with all derivations, tables, and results (target 300-500 lines)
- `explorations/exploration-003/REPORT-SUMMARY.md` — concise summary (30-50 lines)
- Save code to `explorations/exploration-003/code/`

## Key Prior Results You Should Know

- Correct ZPF spectral density: S_F^one(ω) = 2τℏω³/m (NOT (2τℏ/(πm))ω³ — there was a factor-of-π error in earlier work)
- For the harmonic case: var_x = 0.507 ± 0.05 with τ=0.01 (confirmed in exploration 001)
- The frequency-domain approach X(ω) = F(ω)/H(ω) is EXACT for the linear case but INVALID for nonlinear
- The velocity variance is UV-divergent and should be ignored as a primary observable
- Pesquera & Claverie (1982): SED energy = QM energy at O(β) but differs at O(β²). Three failures: wrong energy coefficient at β², wrong absorption frequencies, broken radiation balance.
