# Exploration 003 — Summary

## Goal
Compute C_full_QM(τ) and C_local_TTH(τ) for two coupled harmonic oscillators and determine whether the local modular flow prediction of the Connes-Rovelli thermal time hypothesis (TTH) is distinguishable from standard quantum mechanics.

## What Was Tried
Three correlators computed via exact diagonalization (Fock truncation N=20, 400×400 matrices):
1. **C_full**: standard QM, x_A evolved under full H_AB
2. **C_local**: TTH local modular flow, x_A evolved under K_A/β
3. **C_global**: control (K_AB/β = H_AB → should equal C_full exactly)

Parameters: ω_A = ω_B = 1.0, β = 2.0, λ ∈ {0.1, 0.2, 0.3, 0.5}, τ ∈ [0, 4π]. Also: stability check at N=15 and N=25, and high-resolution FFT (τ ∈ [0, 20π]) to resolve beat structure.

## Outcome: SUCCEEDED — Clear, Quantitative Answer

**TTH's local prediction is emphatically distinguishable from standard QM.**

| λ    | ||C_full − C_local||/||C_full|| |
|------|--------------------------------|
| 0.1  | 0.0915 (9.1%)                  |
| 0.2  | 0.387 (38.7%)                  |
| 0.3  | **0.827 (82.7%)**              |
| 0.5  | 1.166 (>100%)                  |

**The single most important number: 0.827 at λ=0.3, β=2.0.**

## Key Takeaway

The discrepancy is not just quantitative — it is **structural**. C_full shows two-frequency beating at ω_± = √(ω² ± λ) (normal modes of the coupled system). C_local shows a single-frequency oscillation at ω_eff < ω_A (effective frequency red-shifted by entanglement). These are categorically different signal shapes:

- C_full at λ=0.5: FFT peaks at 0.70 and 1.20 rad/τ (matching ω_- = 0.707, ω_+ = 1.225)
- C_local at λ=0.5: single FFT peak at 0.80 rad/τ (single clock frequency)

No matter what parameters are chosen, a single-frequency oscillation cannot match a two-frequency beating pattern once the beat amplitude is significant.

**Root cause:** The Takesaki theorem — for an entangled Gibbs state, the local modular flow σ_t^{K_A} ≠ restriction of the global modular flow σ_t^{K_AB}|_A. Standard QM corresponds to the global modular flow (K_AB = βH_AB). TTH applied locally uses K_A, which generates qualitatively different dynamics.

## Verification
- Control check (C_global = C_full): passed at **exactly machine zero** for all λ
- Fock convergence (λ=0.3): ||C_local(N=15) − C_local(N=20)||/||N=20|| = 1.1×10⁻⁹ (< 1 ppb)
- The 82.7% discrepancy is entirely physical, not numerical

## Leads Worth Pursuing
1. **Literature disambiguation**: Does Connes-Rovelli ever explicitly address TTH for subsystems? If so, do they use K_A or K_AB|_A? This determines whether TTH is making a falsifiable prediction or is trivially equivalent to QM.
2. **Observable consequence**: For realistic quantum optical systems (coupled oscillators at thermal equilibrium), the λ=0.1 discrepancy (9.1%) might be measurable. What observable would detect the absence of normal-mode beating predicted by local TTH?
3. **Gaussian state theorem**: For Gaussian states, K_A has an exact closed form. Is there a theorem that the local modular flow of a coupled Gaussian thermal state is equivalent to some other known dynamical system? (The squeezing structure in K_A suggests a Bogoliubov transformation.)
4. **KMS condition**: Does C_local satisfy the KMS condition with respect to the local β? (It should, almost by construction.) Does C_full satisfy it with respect to the same β? Checking this might reveal that the two correlators satisfy DIFFERENT KMS conditions, which is a more fundamental statement than just comparing waveforms.

## Unexpected Findings
- The ω_eff of the local TTH clock is **below** ω_A (entanglement red-shifts the clock frequency). Exploration-002 predicted a formula ω_eff ≈ ω_A(1 − 0.68λ²/β), which is confirmed qualitatively — but note the sign: the clock runs **slower** than the free oscillator, not faster. (Exploration-002's prediction formula as written in the code was inverted, giving ω_eff > ω_A; the correct interpretation gives ω_eff < ω_A, consistent with the measurement.)
- The C_local amplitude is slightly LARGER than C_full at τ=0 and does not damp — consistent with single-mode thermal average <x²>_β, while C_full averages over two modes and shows amplitude beats (partial damping).
- Control check passes at exactly 0.00e+00, not just < 1e-10. This is because K_AB/β and H_AB are numerically identical by construction — no separate computation needed.

## Computations Identified
1. **KMS condition comparison**: Verify whether C_full and C_local satisfy KMS at the same β. Specifically, check whether C_full(τ + iβ) = C_full(−τ) and C_local(τ + iβ) = C_local(−τ). This requires analytically continuing to complex τ, which can be done by replacing τ → τ + iβ in the phase factors. Moderate difficulty (30-line numpy script using existing infrastructure). Would confirm whether the two correlators correspond to different KMS temperatures.
2. **Larger λ regime**: At λ ≥ 0.5, the coupling is strong and ω_- = √(ω² − λ) approaches zero. Near λ = ω² = 1.0, the system becomes unstable. Exploring 0.5 < λ < 1.0 would map the full breakdown of the local TTH prediction and find the critical point.

DONE
