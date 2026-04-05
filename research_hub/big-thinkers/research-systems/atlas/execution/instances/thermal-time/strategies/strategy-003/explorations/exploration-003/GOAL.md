# Exploration 003: Distance-from-Gibbs Characterization

## Mission Context

We are testing the Thermal Time Hypothesis (TTH). Prior work found that squeezed states (close to Gibbs) have only a 7.8% QUANTITATIVE discrepancy (correct frequencies, wrong amplitudes), while post-quench states (far from Gibbs) have 102% STRUCTURAL discrepancy (completely wrong frequencies). This exploration systematically maps this transition.

## Your Task

Compute a clean curve: **TTH discrepancy vs. relative entropy** (distance from Gibbs), systematically varying the state from Gibbs to far-from-Gibbs.

### Setup

Two coupled harmonic oscillators:
- H_AB = (1/2)(p_A² + ω²q_A²) + (1/2)(p_B² + ω²q_B²) + λ q_A q_B
- Fix: λ = 0.3, β = 2.0, ω = 1.0
- Normal mode frequencies: ω_± = √(ω² ± λ) = √(1.3) ≈ 1.140, √(0.7) ≈ 0.837
- Fock space truncation: N = 20 (verified stable in prior work)

### Family 1: Squeezed States

Starting from the Gibbs state ρ_Gibbs = e^{-βH_AB}/Z, apply two-mode squeezing:
ρ_sq = S(r) ρ_Gibbs S(r)†

Vary squeezing parameter r from 0 to 1.0 in steps of 0.1 (11 points).

For each r, compute:
1. **Relative entropy S(ρ_sq || ρ_Gibbs)** — natural distance metric. For Gaussian states: S = Tr[ρ_sq (log ρ_sq - log ρ_Gibbs)].
2. **Global TTH correlator** C_global(τ) = Tr[ρ_sq · e^{iK_sq τ/β_eff} x_A e^{-iK_sq τ/β_eff} x_A] where K_sq = -log ρ_sq
3. **Full QM correlator** C_QM(τ) = Tr[ρ_sq · e^{iH_AB τ} x_A e^{-iH_AB τ} x_A]
4. **Global TTH discrepancy** = ||C_QM - C_global|| / ||C_QM||
5. **Structural vs quantitative classification**: FFT both correlators. If C_global has peaks at ω_± (correct normal-mode frequencies): QUANTITATIVE. If C_global has peaks at wrong frequencies: STRUCTURAL.

### Family 2: Post-Quench States

The post-quench state: thermal state of uncoupled system (λ = 0) with H_AB at coupling λ.
Effective quench: ρ_quench(δλ) = e^{-β H_AB(λ - δλ)} / Z, dynamics under H_AB(λ).

Vary quench magnitude δλ from 0 to 0.5 in steps of 0.05 (11 points).
- At δλ = 0: state IS Gibbs of H_AB(λ) → discrepancy should be zero.
- At δλ = 0.3: state = Gibbs of uncoupled H → this is the post-quench case from prior work (102% discrepancy).

For each δλ, compute the same 5 quantities as above.

### Expected Output

A plot with:
- X-axis: S(ρ || ρ_Gibbs) (relative entropy / distance from Gibbs)
- Y-axis: ||C_QM - C_global|| / ||C_QM|| (TTH discrepancy)
- Points colored by classification: blue = quantitative, red = structural
- Both families (squeezed and quench) on the same plot

### Key Questions

1. **Is there a sharp transition from quantitative to structural?** Or is it gradual?
2. **At what relative entropy does the transition occur?** (If sharp)
3. **Do squeezed and quench families fall on the same curve?** Or do different types of departure from Gibbs produce different discrepancy behaviors?
4. **Does the structural/quantitative boundary depend on the TYPE of state (squeezing vs quench)?**

### Control

At r = 0 and δλ = 0 (Gibbs state): discrepancy must be zero. K_AB = βH_AB → C_global ≡ C_QM.

### Implementation Notes

The code from prior explorations (S2-E002) has the full Fock-space machinery for coupled oscillators. Key functions:
- Build H_AB in Fock basis
- Compute ρ = e^{-βH}/Z
- Compute K = -log(ρ)
- Time-evolve correlators via matrix exponentials
- FFT for spectral analysis

For the squeezed state: S(r) = exp[r(a_+ a_- - a_+† a_-†)] where a_± are normal-mode operators.
For relative entropy: S(ρ || σ) = Tr[ρ log ρ] - Tr[ρ log σ].

### Output

Write to REPORT.md (INCREMENTALLY — write each family's results as you complete them) and REPORT-SUMMARY.md.

Include:
- A data table: (state type, parameter, S_rel, discrepancy, classification)
- Summary of the transition behavior
- Whether the two families fall on a universal curve
- All code in code/

Tag results as [COMPUTED], [VERIFIED], or [CONJECTURED].

## Success Criteria
1. At least 20 data points (11 squeezed + 11 quench)
2. Clean plot of discrepancy vs relative entropy
3. Transition from quantitative to structural identified (if it exists)
4. Control check passes (discrepancy = 0 at Gibbs)

## Failure Criteria
- Control check fails
- Fewer than 10 total data points
- No FFT classification of structural vs quantitative
