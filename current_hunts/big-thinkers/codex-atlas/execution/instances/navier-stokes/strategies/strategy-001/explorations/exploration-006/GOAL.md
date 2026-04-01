# Exploration 006: Spectral Ladyzhenskaya Inequality — Tighter Constants for Spectrally Localized Fields

## Mission Context

The vortex stretching bound in 3D Navier-Stokes has 158-237× slack. The dominant source (63% of log-slack) is the Ladyzhenskaya inequality:

||f||_{L⁴} ≤ C_L × ||f||^{1/4}_{L²} × ||∇f||^{3/4}_{L²}

where C_L = 0.827 (sharp on ℝ³, attained by Aubin-Talenti bubble).

**The problem:** The Ladyzhenskaya optimizer is a concentrated spike — high gradient relative to its L² norm. NS solutions (specifically their vorticity ω) are spectrally extended, typically with energy spectrum E(k) ~ k^{-5/3} in the inertial range. This spectral structure means NS fields never approach the optimizer, and the effective C_L for NS flows is only 0.147 (18% of the sharp constant).

**The question:** Can we prove a **tighter Ladyzhenskaya inequality** for fields with specific spectral structure?

## Your Goal

### Part A: Spectral Ladyzhenskaya — Analytical Framework

Consider the Ladyzhenskaya inequality on T³ = [0,2π]³ for fields f with Fourier support concentrated at wavenumbers |k| ~ k₀ (a "frequency band"):

f = Σ_{|k|∈[k₀/2, 2k₀]} f̂_k e^{ik·x}

For such fields:
- ||f||²_{L²} = Σ|f̂_k|²
- ||∇f||²_{L²} = Σ|k|²|f̂_k|² ~ k₀² × ||f||²_{L²}

This means ||∇f||_{L²} ~ k₀ × ||f||_{L²}. Plugging into Ladyzhenskaya:
C_L × ||f||^{1/4}_{L²} × (k₀ × ||f||_{L²})^{3/4} = C_L × k₀^{3/4} × ||f||_{L²}

But we want ||f||_{L⁴}. For a band-limited field, ||f||_{L⁴} is bounded by Bernstein's inequality:
||f||_{L⁴} ≤ C_{Bern} × k₀^{3/4} × ||f||_{L²} (since L²→L⁴ gains 3(1/2-1/4)=3/4 derivatives in 3D)

So the effective Ladyzhenskaya constant for band-limited fields is:
C_{L,band}(k₀) = ||f||_{L⁴} / (||f||^{1/4}_{L²} × ||∇f||^{3/4}_{L²})

**Compute this numerically** for various k₀ and spectral profiles.

### Part B: Numerical Computation

Write Python code to compute the effective Ladyzhenskaya constant for fields on T³ with specific spectral profiles:

1. **Band-limited fields:** f̂_k = a_k for |k| ∈ [k₀/2, 2k₀], zero otherwise. Optimize over the phases of a_k to MAXIMIZE ||f||_{L⁴}/(||f||^{1/4}_{L²}×||∇f||^{3/4}_{L²}). Use scipy.optimize starting from random phases.

2. **Power-law spectra:** f̂_k ~ |k|^{-α} × e^{iφ_k} with random phases. Compute the expected effective C_L for α = 5/6 (corresponds to E(k)~k^{-5/3} Kolmogorov spectrum), α = 1, α = 3/2.

3. **Div-free fields:** Restrict to f̂_k ⊥ k (incompressibility). Does this constraint further reduce C_L?

4. **NS solution spectra:** Use the spectral profile from the Taylor-Green vortex at Re=1000 (from exploration 002). Compute the effective C_L for fields whose Fourier amplitudes match this profile.

For each case, report C_{L,eff} / C_L and the slack reduction factor.

### Part C: Littlewood-Paley Decomposition

A natural framework for this is Littlewood-Paley decomposition: f = Σ_j Δ_j f where Δ_j localizes to wavenumbers |k| ~ 2^j.

For a field f with Littlewood-Paley decomposition, the Bernstein inequality gives:
||Δ_j f||_{L⁴} ≤ C × 2^{3j/4} × ||Δ_j f||_{L²}

But the full ||f||_{L⁴} involves interactions between different frequency bands. Compute:

1. The "diagonal" contribution: ||f||⁴_{L⁴,diag} ~ Σ_j ||Δ_j f||⁴_{L⁴}
2. The "cross-term" contributions: interactions between different frequency bands
3. For Kolmogorov-spectrum fields, which terms dominate?

If the diagonal term dominates, then a spectral Ladyzhenskaya inequality with tighter constants is possible by applying Bernstein to each band separately.

### Part D: Toward a Theorem

Based on Parts A-C, attempt to formulate (not necessarily prove rigorously) a **spectral Ladyzhenskaya inequality**:

For f: T³ → ℝ with energy spectrum Ê(k) = Σ_{|k'|∈[k,k+1]} |f̂_{k'}|², if Ê(k) ≤ A × k^{-β} for k ≥ k₁, then:

||f||_{L⁴} ≤ C_{L,spec}(β, k₁) × ||f||^{1/4}_{L²} × ||∇f||^{3/4}_{L²}

where C_{L,spec}(β, k₁) < C_L for β > some threshold.

Compute C_{L,spec} numerically as a function of β and k₁.

## Existing Code

The solver infrastructure is at `../exploration-002/code/`. Copy what you need.

## Output Format

### Results Table
| Spectral Profile | C_{L,eff} | Ratio C_{L,eff}/C_L | Slack Reduction Factor |
|---|---|---|---|

### Part D: Candidate Theorem Statement
State the tightest spectral Ladyzhenskaya inequality your data supports.

## Success Criteria
- C_{L,eff} computed for at least 4 spectral profiles (band-limited at 3+ values of k₀, Kolmogorov, NS solution)
- Div-free vs. general comparison for at least one profile
- A candidate theorem statement (even if not rigorously proved) with numerically determined constants
- Assessment of how much of the 158× slack a spectral Ladyzhenskaya could close

## Failure Criteria
- Only trivial cases computed (e.g., only single Fourier modes)
- No optimization over phases (just random phases without maximization)
- No candidate theorem formulation

## Critical Instructions
- Tag all numerical claims with [VERIFIED], [COMPUTED], [CHECKED], or [CONJECTURED]
- **Part B is highest priority** — the numerical computation of effective constants
- **If Bernstein-type analysis shows no improvement** (i.e., the spectral structure doesn't help), report this honestly. A negative result here is very important — it would redirect the strategy.
- Write incrementally: each part's results before starting the next

## File Paths
- Existing code: ../exploration-002/code/
- Your code: code/ (create this directory)
- Report: REPORT.md
- Summary: REPORT-SUMMARY.md
