# Exploration 004 — Summary

## Goal
Resolve whether the Connes-Rovelli Thermal Time Hypothesis prescribes the LOCAL or GLOBAL modular flow for subsystem dynamics, verify with a KMS temperature analysis, and sketch a minimum experimental test.

## What Was Tried
1. **Literature analysis:** Extracted and read the full text of Connes & Rovelli (1994, gr-qc/9406019). Identified the decisive passage in Section 4.3 (Rindler wedge application) and cross-referenced with Martinetti & Rovelli (2003) and philosophical analyses.
2. **KMS temperature analysis:** Computed the spectral decomposition and detailed balance ratio for both C_full (QM) and C_local (TTH) at λ ∈ {0.1, 0.3, 0.5}. Verified KMS condition numerically.
3. **Experimental proposal:** Computed parameters for three candidate systems (superconducting cavities, trapped ions, optomechanical oscillators) and assessed feasibility.

## Outcome: RESOLVED — Both Interpretations Clarified

**Literature finding:** Connes-Rovelli explicitly use the **LOCAL modular flow** — the modular flow of the global state restricted to the local algebra. This is clearly stated in Section 4.3: "The restriction of the state |0⟩ to the algebra A_R is of course a state on A_R, and therefore it generates a modular group of automorphisms α_t over A_R." This is further confirmed by Martinetti-Rovelli (2003) and the broader TTH literature.

**KMS finding:** Both C_full and C_local satisfy KMS at β=2 exactly (within numerical precision Δβ ~ 10⁻³). The difference is NOT in temperature but in **spectral structure**: C_full has 2 peaks (normal-mode splitting at ω_±), C_local has 1 peak (single modular frequency ω_eff).

**Experimental finding:** The test is already implicitly done. Normal-mode splitting in coupled oscillator pairs has been observed routinely in trapped ions, coupled cavities, and mechanical systems. The QM prediction (two peaks) is always confirmed. The local TTH prediction (one peak) is contradicted by existing data.

## Key Takeaway

**The TTH does NOT make a novel testable prediction for non-relativistic equilibrium Gibbs states.** While the local interpretation (used by Connes-Rovelli for the Rindler wedge) does produce a prediction distinguishable from QM (single-frequency vs. two-frequency autocorrelation), this prediction is falsified by existing observations of normal-mode splitting. The correct resolution is that the TTH was designed for the **generally covariant regime** (where no Hamiltonian exists), not for non-relativistic subsystems where the global Hamiltonian dynamics is already available and experimentally confirmed.

For non-relativistic systems: TTH applied to the GLOBAL state on the GLOBAL algebra reproduces standard QM exactly (K_AB/β = H_AB for Gibbs states). TTH = QM in this regime.

## Unexpected Findings

1. **The KMS temperature is the same for both correlators** — the distinction between QM and local TTH is purely in spectral structure (which frequencies are present), not in the effective temperature. This is a more nuanced picture than "different temperatures for the subsystem."

2. **Takesaki's compatibility condition as the marker of TTH's domain boundary:** The failure of the conditional expectation (Takesaki's theorem) for coupled Gibbs states isn't a signature of new physics — it's a signature that the local modular flow is not the physical time evolution for non-relativistic subsystems. This condition could potentially be used to identify regimes where TTH predictions DO differ from QM meaningfully (e.g., type III algebras in QFT).

## Computations Identified

1. **Type III algebra test:** Repeat the C_full vs C_local comparison for a quantum field theory system (e.g., two adjacent Rindler wedges with the Minkowski vacuum), where the algebras are type III and the TTH is intended to apply. Check whether the local modular flow still disagrees with the global dynamics restricted to the subregion, or whether special properties of the vacuum/type III structure make them agree. This would require lattice discretization of a 1+1D QFT — a moderately complex numerical project (100-200 lines of code, scipy-level).

2. **Non-equilibrium state test:** Compute C_full vs C_local for a NON-Gibbs state (e.g., a squeezed thermal state, or a state after a quantum quench). In this case, K_AB ≠ βH_AB even for the full system, so the TTH might give genuinely different predictions from standard Hamiltonian dynamics. This would be a straightforward extension of exploration-003's code (~50 lines).
