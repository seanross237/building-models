# Exploration 004 — Full Abraham-Lorentz Dynamics: Direct Test of Pesquera-Claverie

## Mission Context

We are testing SED (Stochastic Electrodynamics) against QM for the anharmonic oscillator V(x) = ½x² + βx⁴.

**Previous result (exploration 003):** Using the Langevin approximation (constant damping Γ = τω₀²), SED fails QUALITATIVELY — var_x increases with β while QM decreases. The failure is at O(β). Physical mechanism: ω³ noise + constant damping → positive feedback loop pumps the oscillator.

**The key question now:** Does the full Abraham-Lorentz dynamics (with position-dependent damping) fix the O(β) failure? Pesquera & Claverie (1982) proved analytically that SED with full ALD agrees with QM at O(β) but disagrees at O(β²). Exploration 003 used constant damping, which is a worse approximation.

## Your Task

This is a **computation task.** Implement the Landau-Lifshitz order reduction of the Abraham-Lorentz equation and repeat the anharmonic oscillator comparison.

### The Physics

The Abraham-Lorentz equation for a particle in V(x) = ½ω₀²x² + βx⁴ is:

    mẍ = F(x) - mΓẋ + mτx⃛ + F_zpf(t)

where F(x) = -ω₀²x - 4βx³ and τ is the radiation reaction time.

The third derivative x⃛ creates runaway solutions. The standard fix is the **Landau-Lifshitz order reduction**: replace mτx⃛ with τ(dF/dt) on the solution, giving:

    ẍ = F(x) - Γ_eff(x,v)·ẋ + F_zpf(t) + τ·F'_zpf(t)

where the effective damping is:

    Γ_eff(x,v) = τ·(∂F/∂x) = τ·(ω₀² + 12βx²)

and there's an additional noise term τ·F'_zpf (the time derivative of the ZPF force).

**Key difference from exploration 003:** The damping Γ_eff = τ(ω₀² + 12βx²) INCREASES at large x. When the oscillator has large amplitude (x large), the damping grows as 12βτx², which counteracts the ω³ noise pumping. This should eliminate the O(β) positive feedback loop found in exploration 003.

### Part 1: Implement the Landau-Lifshitz SED equation

Write Python code to solve:

    ẍ = -ω₀²x - 4βx³ - τ(ω₀² + 12βx²)ẋ + F_zpf(t) + τF'_zpf(t)

Implementation notes:
1. **Noise generation:** Generate F_zpf(t) with PSD S_F(ω) = 2τω³ using FFT (amplitude A_k = sqrt(S_F(ω_k) * N / (2*dt))). Verified normalization from prior explorations.
2. **Noise derivative:** F'_zpf(t) can be obtained from the FFT: multiply frequency components by iω before IFFT.
3. **Integration:** Euler-Cromer or Velocity Verlet. Use dt = 0.05, T = 20000 per trajectory.
4. **Parameters:** τ = 0.01, ω₀ = 1, ω_max = 10 (same as exploration 003).
5. **Ensemble:** N_ensemble = 200, 50 samples per trajectory = 10000 samples per β.
6. **β scan:** 0, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0 (same as exploration 003).
7. **Run β values SEQUENTIALLY** (one at a time, not in a single invocation).

### Part 2: Compare against exploration 003 (Langevin) and QM

For each β, report a 3-way comparison:

| β | var_x_QM | var_x_ALD | var_x_Langevin |
|---|----------|-----------|----------------|

QM reference values (computed in exploration 003 via matrix diagonalization):
- β=0.00: var_x = 0.500
- β=0.01: var_x = 0.486
- β=0.05: var_x = 0.446
- β=0.10: var_x = 0.413
- β=0.20: var_x = 0.370
- β=0.50: var_x = 0.306
- β=1.00: var_x = 0.257

Exploration 003 Langevin results:
- β=0.00: var_x = 0.515 ± 0.007
- β=0.01: var_x = 0.529 ± 0.008
- β=0.10: var_x = 0.735 ± 0.014
- β=1.00: var_x = 2.411 ± 0.043

### Part 3: Determine the order of failure

1. If ALD matches QM at O(β) but fails at O(β²), compute the discrepancy coefficient: Δvar_x / β² = ?
2. Compare this to Pesquera & Claverie's analytic prediction for the energy discrepancy.
3. If ALD still fails at O(β), that contradicts P&C and would be a new result. Document carefully.

### Part 4: Physical interpretation

Explain why position-dependent damping changes the behavior:
- Does Γ_eff(x) = τ(ω₀² + 12βx²) actually prevent the positive feedback loop?
- At equilibrium, what is the average value of Γ_eff? How does it compare to the constant Γ = τω₀²?

## Success Criteria

- ALD simulation runs for ≥ 4 β values including β=0
- β=0 check: var_x agrees with QM to within 5% (same as exploration 003)
- 3-way comparison table (QM vs ALD vs Langevin) produced
- Clear determination: does ALD fail at O(β) or O(β²)?

## Failure Criteria

- If ALD is numerically unstable (runaway solutions despite Landau-Lifshitz reduction), document at what parameters and try reducing τ.
- If ALD gives results identical to Langevin (position-dependent damping has no effect), that's a valid finding — document why.
- If time runs out, at minimum run β = 0 and β = 0.1 — the β=0.1 case showed the clearest Langevin failure (23.6σ).

## Deliverables

- `explorations/exploration-004/REPORT.md` — full report (300-500 lines)
- `explorations/exploration-004/REPORT-SUMMARY.md` — concise summary (30-50 lines)
- `explorations/exploration-004/code/` — all Python scripts

## IMPORTANT REMINDERS

- **UV divergence:** Velocity variance is UV-divergent. Focus on position-based observables (var_x, P(x), potential energy).
- **Noise normalization:** A_k = sqrt(S_F(ω_k) * N / (2*dt)) where S_F(ω) = 2τω³. THIS IS VERIFIED.
- **Don't spend more than 10 minutes on noise normalization.** Use the formula above directly.
- **Sequential runs.** Run one β value, print results, then the next.
