# Exploration 002 — Two Coupled SED Oscillators: Entanglement-Like Correlations and Bell S

## Mission Context

You are exploring Stochastic Electrodynamics (SED) — classical electrodynamics augmented by a real, Lorentz-invariant zero-point field (ZPF). SED succeeds for all LINEAR systems (harmonic oscillator, Casimir, van der Waals). The question this exploration asks: does the shared classical ZPF between two spatially separated oscillators produce correlations that look like quantum entanglement? Specifically, what is the Bell-CHSH parameter S from SED dynamics?

**Key context from library:**
- Boyer (1973): two linearly coupled SED oscillators reproduce van der Waals correlations ∝ r⁻⁶ → SED SUCCEEDS for linear coupling. So we expect SED to match QM for two uncoupled/weakly coupled linear oscillators.
- de la Peña et al. (2010): LSED (a variant of SED) claims "non-factorizable states" for two oscillators at common resonance. But LSED ≠ standard SED; relationship is debated.
- NO direct simulation of Bell S from two SED oscillators sharing a ZPF realization has been done.

## Specific Goal

Simulate two harmonic oscillators (particles 1 and 2 at positions x₁ and x₂) each driven by the SAME ZPF realization evaluated at their respective positions. Compute:
1. Position-position correlation: `⟨x₁x₂⟩`
2. Momentum-momentum correlation: `⟨p₁p₂⟩`
3. Compare to QM ground-state predictions
4. Attempt to compute Bell-CHSH parameter S

## Simulation Setup

### Two Oscillators with Shared ZPF

Oscillator 1 at position `r₁ = 0` and oscillator 2 at position `r₂ = d` (separation d).

Both oscillators satisfy the ALD equation (use Euler-Cromer or Verlet integrator):
```
ẍᵢ = -ω₀²xᵢ - τω₀²ẋᵢ + F_zpf(rᵢ, t) + τ·Ḟ_zpf(rᵢ, t)
```

For LINEAR oscillators, V'' = ω₀² is constant, so ALD simplifies to constant damping τω₀². This is fine for harmonic oscillators.

### Generating Correlated ZPF Noise

The two oscillators SHARE the same ZPF realization but are sampled at different positions. For a ZPF mode with wavevector k, the field evaluated at position r has phase `k·r`. For simplicity, use a 1D version:

**Simplified approach:** Generate a single ZPF realization as a time series F_zpf(t) (as in Strategy-001). Apply it to oscillator 1 with a time delay τ_delay = d/c to get oscillator 2's force:
```
F₁(t) = F_zpf(t)
F₂(t) = F_zpf(t - d/c)   [retarded field at position d]
```

This captures the causal structure of the shared ZPF.

**For short separations (d ≪ c/ω₀):** F₁ ≈ F₂ (nearly correlated). Expect strong correlations.
**For long separations (d ≫ c/ω₀):** F₁ and F₂ are essentially independent. Expect weak correlations.

Run both regimes.

### Parameters

- `ω₀ = 1.0`, `m = 1.0`, `ℏ = 1.0`, `τ = 0.001`
- `ω_max = 10`, `dt = 0.05`, `N = 100,000` time steps, `N_traj = 200` trajectories
- Separations: `d = 0` (identical force, maximum correlation), `d = 0.1`, `d = 1.0`, `d = 10.0` (in units of c/ω₀ with c=1)

### Noise Formula (Verified from Strategy-001)

```
S_F(ω) = 2τℏω³/m   [one-sided PSD]
A_k = sqrt(S_F(omega_k) * N / (2 * dt))   [FFT amplitude]
```

Generate noise F_zpf(t) in frequency domain, apply phase shift e^{iωd/c} for the second oscillator, inverse FFT.

**UV divergence warning:** Do NOT compute velocity variance or total energy — they are UV-divergent. Use position and position-correlation as your primary observables.

## Primary Observables

### 1. Position-Position Correlation

```
C_xx(d) = ⟨x₁x₂⟩ / sqrt(⟨x₁²⟩ × ⟨x₂²⟩)   [normalized Pearson correlation]
```

**QM prediction:** For two uncoupled harmonic oscillators in the vacuum state (no interaction), the QM state is |0⟩₁|0⟩₂ which is separable. So `⟨x₁x₂⟩_QM = ⟨x₁⟩_QM × ⟨x₂⟩_QM = 0`.

**SED prediction:** Depends on d. At d=0 (same force), expect C_xx ≈ 1 (perfectly correlated). At large d, expect C_xx → 0.

Report C_xx as a function of d. If C_xx > 0 for large d, that's a SED-specific prediction beyond QM.

### 2. Momentum-Momentum Correlation

```
C_pp(d) = ⟨ẋ₁ẋ₂⟩ / sqrt(⟨ẋ₁²⟩ × ⟨ẋ₂²⟩)
```

Note: individual velocity variances are UV-divergent, but the CORRELATION ⟨ẋ₁ẋ₂⟩ may be UV-finite (the UV modes contribute equally to both oscillators, so their correlation could be finite). Check whether this is UV-stable.

### 3. Bell-CHSH Parameter S

**Simplified CHSH for two oscillators:** Use position quadratures as the measured observables. Define:
- A = sign(x₁ - a) for threshold a (measurement setting 1 for oscillator 1)
- A' = sign(x₁ - a') for threshold a' (measurement setting 2)
- B = sign(x₂ - b) for threshold b (measurement setting 1 for oscillator 2)
- B' = sign(x₂ - b') for threshold b' (measurement setting 2)

Then: `CHSH = |⟨AB⟩ + ⟨AB'⟩ + ⟨A'B⟩ - ⟨A'B'⟩| ≤ 2` for any local hidden variable theory.

Optimal settings for Gaussian distributions: `a = b = 0`, `a' = b' = σ/√2` (one standard deviation). Try several settings and report the maximum S you find.

**QM bound:** S ≤ 2√2 ≈ 2.83 for maximally entangled states.
**Classical bound:** S ≤ 2 for local realistic theories.
**Expected for vacuum state:** S ≤ 2 (vacuum is separable in QM too).

If SED gives S > 2, that would be a dramatic result (classical field exceeding Bell bound?). If S ≤ 2, consistent with SED being a local realistic theory.

### 4. Comparison to QM Two-Mode Ground State

For two uncoupled harmonic oscillators in QM ground state:
- `⟨x₁x₂⟩ = 0` (uncoupled, separable state)
- `⟨x₁²⟩ = ⟨x₂²⟩ = ℏ/(2mω₀) = 0.5` (in natural units)

For van der Waals coupling (induced dipole-dipole): QM gives corrections at order (e²a₀/ε₀) that are tiny. If you see significant C_xx at large d, that's non-QM.

## Prior Art Search

Before writing your report, web search for:
1. "SED entanglement two oscillators zero-point field"
2. "stochastic electrodynamics Bell inequality correlation"
3. "de la Pena LSED entanglement" and "Boyer coupled oscillators SED"
4. "classical zero-point field Bell violation"

## Success Criteria

**Positive result:** Clean measurement of C_xx(d), C_pp(d), and S(d) with error bars. Comparison to QM values. Even "SED correlations match QM for linear oscillators" is a valid success — it extends the linearity boundary to coupled systems.

**Interesting result:** S > 2 from SED (classical field appearing to violate Bell inequality). This would require careful checking — most likely a numerical artifact or misapplication of CHSH to continuous variables, but document it.

**Negative result:** "Linear coupled SED oscillators match QM exactly for all observables and S ≤ 2 as expected." Also a valid finding — establishes that entanglement failure requires nonlinearity.

**Failure:** No quantitative results computed.

## Sanity Checks

1. At d=0 (same force applied to both oscillators): C_xx should → 1 (they are driven identically)
2. At very large d (independent noise): C_xx should → 0
3. Each oscillator individually should have var_x ≈ 0.500 ± 0.015 (harmonic oscillator result from Strategy-001)

## Output Format

Write REPORT.md with:
1. Code for the shared-ZPF noise generation
2. Sanity check results (individual var_x, C_xx at d=0 and large d)
3. C_xx(d) table for all separations, with comparison to QM
4. C_pp(d) results (if UV-stable)
5. Bell-CHSH S values with settings used
6. Prior art search results
7. Overall verdict: Does the shared ZPF produce quantum-like correlations? Does it violate or respect the Bell bound?

Write REPORT-SUMMARY.md (max 300 words) with key quantitative findings.

**Write incrementally — write to REPORT.md as you complete each section.**

## Your exploration directory

`/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/stochastic-electrodynamics/strategies/strategy-002/explorations/exploration-002/`

Save all code, REPORT.md, and REPORT-SUMMARY.md here.
