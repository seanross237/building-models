# Exploration 001 — Reproduce SED Harmonic Oscillator Ground State

## Mission Context
We are investigating Stochastic Electrodynamics (SED) — the program that attempts to derive quantum mechanical results from classical electrodynamics plus a real, Lorentz-invariant zero-point radiation field. This is the first exploration in a multi-exploration strategy. Your job is to build the computational foundation that later explorations will extend.

## Your Goal
Numerically reproduce the SED harmonic oscillator ground state. Specifically:
1. **State the SED axioms and equations explicitly** before writing any code. Write out:
   - The SED zero-point field spectral density: ρ(ω) = ℏω³/(2π²c³)
   - The Langevin equation for a charged particle (mass m, charge e) in a harmonic potential V = ½mω₀²x², including the Abraham-Lorentz radiation reaction term and the ZPF driving force
   - The known analytic result: ground state energy E₀ = ½ℏω₀, position variance σ_x² = ℏ/(2mω₀)
2. **Write and run a numerical simulation** that solves the stochastic differential equation. Use Python with numpy/scipy. The simulation should:
   - Sample the ZPF driving force with the correct spectral density
   - Include the radiation reaction (damping) term
   - Evolve an ensemble of trajectories to equilibrium
   - Measure the equilibrium energy and position distribution
3. **Compare your numerical results to the analytic QM predictions** with explicit numerical precision. Report:
   - Ground state energy: computed value ± uncertainty vs. ½ℏω₀
   - Position variance: computed value ± uncertainty vs. ℏ/(2mω₀)
   - Shape of position distribution: is it Gaussian? Quantify with a KS test or chi-squared
4. **Identify the assumptions** that this derivation makes which might break for more complex systems. Specifically discuss: dipole approximation, single particle, linearity of the potential, equilibrium assumption, non-relativistic approximation.

## Success Criteria
- Working Python code that simulates the SED harmonic oscillator
- Ground state energy matches ½ℏω₀ to within 5% (numerical simulation noise)
- Position distribution is consistent with Gaussian with correct variance
- Code is saved in `code/` directory and structured for reuse (the Langevin solver should be importable)
- Assumptions are explicitly listed

## Failure Criteria
- If the simulation does not converge to the QM ground state distribution, diagnose WHY:
  - Is it a numerical issue? (timestep too large, ensemble too small, not enough equilibration time)
  - Is it a physics issue? (wrong ZPF spectral density, missing radiation reaction term)
  - Try at least 3 different parameter regimes before declaring failure
  - Document all parameter choices tried and what happened

## Practical Notes
- Use natural units or a convenient unit system. A good choice: set m=1, ω₀=1, ℏ=1, then the target is E₀=0.5, σ_x²=0.5.
- The radiation reaction damping coefficient is τ = 2e²/(3mc³). In natural units with appropriate choice of e, this becomes a small parameter. Start with τ ≈ 0.01 (weakly damped) and check whether results depend on this choice.
- Ensemble size: start with 1000 trajectories, increase if statistics are noisy.
- Equilibration: run for at least 100/τ time steps to ensure steady state is reached.
- **Spend at most 5 minutes on background research.** The primary deliverable is working code and numerical results. The equations above should be sufficient to start coding.

## Output
Write your report to: `explorations/exploration-001/REPORT.md`
Write your summary to: `explorations/exploration-001/REPORT-SUMMARY.md`
Save code to: `explorations/exploration-001/code/`

Target report length: 300-500 lines.

## Relevant Context from Library
- **Nelson's stochastic mechanics** is closely related to SED. Nelson showed QM is equivalent to conservative diffusion with diffusion coefficient ℏ/2m. SED provides the physical noise source (the ZPF) for Nelson's abstract diffusion. Known limitation: single-time position probabilities match QM, but multi-time correlations give wrong answers (Blanchard et al. 1986).
- **SED is the electromagnetic sector instantiation of the abstract stochastic→QM pipeline:** zero-point field → Langevin equation → equilibrium distribution → QM ground state.
- **Caution from Barandes-Doukas:** The isomorphism between stochastic processes and QM runs both ways. SED reproducing QM for the harmonic oscillator could be "QM wearing a classical disguise" rather than a genuine derivation. Keep this in mind but don't let it distract from the computation.
