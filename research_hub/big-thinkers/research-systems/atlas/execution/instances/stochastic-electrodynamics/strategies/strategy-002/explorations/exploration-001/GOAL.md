# Exploration 001 — SED Tunneling: Double-Well Barrier Crossing vs WKB

## Mission Context

You are exploring Stochastic Electrodynamics (SED) — classical electrodynamics augmented by a real, Lorentz-invariant zero-point field (ZPF). SED succeeds for linear systems (harmonic oscillator) and fails for nonlinear ones. This is the first strategy to probe SED in new nonlinear regimes beyond the anharmonic oscillator.

**This exploration is the first numerical computation of barrier crossing in SED. No prior work exists.**

## Specific Goal

Simulate a particle in the double-well potential `V(x) = -½ω₀²x² + ¼λx⁴` driven by SED zero-point noise with the Landau-Lifshitz ALD equation. Measure the barrier-crossing rate. Compare quantitatively to the WKB quantum tunneling rate for the same potential.

## Critical Constraint: Use ALD, NOT Langevin

Strategy-001 proved that the Langevin approximation (constant damping Γ = τω₀²) fails qualitatively for ANY nonlinear potential — it creates a positive feedback loop where ω³ ZPF noise pumps the oscillator to infinite amplitude. You MUST use the Landau-Lifshitz order-reduced Abraham-Lorentz equation:

```
ẍ = -V'(x)/m - τ·V''(x)·ẋ + F_zpf + τ·F'_zpf
```

For `V(x) = -½ω₀²x² + ¼λx⁴`:
- `V'(x) = -ω₀²x + λx³`
- `V''(x) = -ω₀² + 3λx²`

So the ALD equation becomes:
```
ẍ = (ω₀²x - λx³) - τ(-ω₀² + 3λx²)ẋ + F_zpf + τ·F'_zpf
```

where `τF'_zpf` is the time-derivative of the ZPF force times τ (compute from consecutive noise samples).

## Verified Noise Infrastructure (Use Exactly)

**ZPF force power spectral density (one-sided, verified by three-way cross-check in Strategy-001):**
```
S_F(ω) = 2τℏω³/m   [one-sided, for ω > 0]
```
where τ = e²/(6πε₀mc³) ≈ 6.25 × 10⁻²⁴ s. In natural units (ℏ=1, m=1, ω₀=1), set τ = 0.001 (small enough to avoid runaway, large enough for the ZPF to matter).

**FFT amplitude for colored noise generation (verified):**
```python
A_k = np.sqrt(S_F(omega_k) * N / (2 * dt))
```
where N = number of time steps, dt = timestep. DO NOT include a factor of π here — it was wrong in an earlier version.

**UV divergence warning:** Velocity variance is UV-divergent (electromagnetic self-energy). Do NOT use total energy or velocity variance as your primary observable. Use position-based observables only.

## Simulation Parameters

Start with these parameters and verify basic stability before doing parameter sweeps:

- `ω₀ = 1.0`, `m = 1.0`, `ℏ = 1.0`, `τ = 0.001`
- `ω_max = 10` (UV cutoff), `dt = 0.05` (adequate for ω₀=1 and ω_max=10)
- `N = 200,000` time steps per trajectory (T = 10,000 ω₀⁻¹)
- `N_traj = 100` independent trajectories minimum

**Double-well parameters:** Start with `λ = 0.25, ω₀ = 1.0` → barrier height `V_barrier = ω₀⁴/(4λ) = 1.0` in natural units. Also test `λ = 0.1` (deeper, higher barrier) and `λ = 1.0` (shallower barrier).

**Initial conditions:** Start ALL particles at x=0 (top of barrier) with zero velocity, or at x = +x_min (bottom of one well) with zero velocity. Run both and compare.

## Sanity Checks (Run These First)

1. **β=0 sanity check:** Set `λ=0`, which gives a harmonic oscillator centered at x=0 (inverted). This is unstable — a particle at x=0 will drift away. That's expected. Verify your simulation is numerically stable with a regular HO (`V = ½ω₀²x²`) first.

2. **Harmonic oscillator check:** Before any double-well runs, verify that your simulation recovers `var_x ≈ 0.500 ± 0.015` for `V = ½ω₀²x²`. This is the known SED result from Strategy-001. If you get something different, your noise normalization is wrong.

## What to Measure

### Primary Observable: Barrier-Crossing Rate

For particles starting in one well (x = +x_min = ω₀/√λ), count the number of times per unit time that x changes sign (crosses x=0). This gives the SED barrier-crossing rate Γ_SED.

Report: `Γ_SED [units: ω₀]` as a function of barrier height V_barrier and λ.

### Compare to WKB Rate

The WKB tunneling rate for a symmetric double-well `V = -½ω₀²x² + ¼λx⁴` with barrier height `V_0 = ω₀⁴/(4λ)`:

```
Γ_WKB ≈ (ω₀/π) × exp(-S_WKB/ℏ)
```

where `S_WKB = ∫_{-x_min}^{+x_min} √(2m(V(x)-E_0)) dx` with E_0 = ground state energy.

For a deep double-well, `E_0 ≈ ½ℏω₀ - ½(ℏω₀)²/(4V_0)` (ground state energy in one well). Compute this integral numerically.

Report: `Γ_SED / Γ_WKB` ratio. This is the key number.

### Secondary Observable: Long-Time Behavior

Does the particle:
(a) Oscillate between wells at rate Γ_SED (tunneling-like behavior)?
(b) Escape both wells entirely (like hydrogen self-ionization)?
(c) Get stuck in one well forever?

Track the distribution of x over the full run. If particles regularly escape to |x| > 3x_min, report this as "SED produces escape, not tunneling."

## Run Explorations Sequentially, Not All at Once

Run one parameter set at a time. Don't put all parameter sweeps in a single Python script invocation — they will time out. Run one λ value, check it works, then the next.

Write results to the REPORT.md file after EACH parameter run. Don't wait until the end.

## Success Criteria

**Positive result:** You obtain a clean SED barrier-crossing rate that you can compare to WKB. Report the ratio Γ_SED/Γ_WKB with at least 2 decimal places. Even if SED fails (ratio >> 1 or << 1), that's a success — we need the number.

**Partial success:** You observe that SED particles escape both wells (no stable tunneling dynamics). Report the escape rate and the mechanism (energy injection via ω³ ZPF).

**Negative result:** If the simulation is numerically unstable for the double-well (ALD damping becomes negative for V''(x) < 0), document this instability precisely and explain why.

**Failure:** Leaving without any quantitative result ("the double-well is difficult").

## Prior Art Search

Before writing your report, web search for:
1. "SED tunneling double well" and "stochastic electrodynamics barrier crossing"
2. "zero point field tunneling rate" and "Casimir tunneling SED"
3. "classical stochastic tunneling WKB comparison"

Document what you find. We believe this is completely novel but want to verify.

## Output Format

Write REPORT.md with:
1. Simulation code (paste the key simulation loop)
2. Sanity check results (HO var_x)
3. Barrier-crossing rate table: λ × [Γ_SED, Γ_WKB, Γ_SED/Γ_WKB, error bars]
4. Description of what SED particles actually do (oscillate, escape, stuck)
5. Mechanism analysis (why does SED predict this rate?)
6. Prior art search results
7. Overall verdict: Does SED match WKB tunneling rates?

Write REPORT-SUMMARY.md (max 300 words) with:
- The key quantitative result (Γ_SED/Γ_WKB ratio or escape finding)
- Whether SED tunneling matches QM or fails, and how spectacularly
- Whether this is novel (prior art found or not)

**Write incrementally — write to REPORT.md after each parameter run, not all at the end.**

## Your exploration directory

`/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/stochastic-electrodynamics/strategies/strategy-002/explorations/exploration-001/`

Save all code, REPORT.md, and REPORT-SUMMARY.md here.
