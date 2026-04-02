# Exploration History

## Exploration 001 — Modular Hamiltonians: Catalog, Formalization, and TTH Prediction
**Phase:** 1 (Mathematical Toolkit Establishment) | **Status:** Complete | **Date:** 2026-03-27

**Goal:** Catalog explicit modular Hamiltonians for key systems, formalize the TTH prediction for a bipartite temperature-gradient setup, identify a discriminating observable, and begin numerical computation.

**What was done:** Extracted modular Hamiltonians for four systems: (1) Rindler wedge via Bisognano-Wichmann (K = 2π × boost generator), (2) Bell state (K_A = log(2)·I, trivial flow), (3) thermal harmonic oscillator (K = βH, modular flow = physical time evolution at rate β), (4) 1+1d CFT interval via Casini-Huerta (K = 2π∫f(x)T₀₀dx, Möbius flow). Formalized TTH for bipartite β_A ≠ β_B product state. Ran Python computation in truncated Fock space (N=16).

**Key finding:** For position autocorrelation C(t) = ⟨x_A(t)x_A(0)⟩ with ρ_AB = ρ_A(β_A)⊗ρ_B(β_B): TTH predicts oscillation at **β_A ω_A**, standard QM predicts oscillation at **ω_A**. These differ by factor β_A. Numerically verified (β_A=2, ω_A=1): C_TTH(t) = 0.6565·cos(2t) vs C_QM(t) = 0.6565·cos(t)·e^{-0.020t}. Maximum discrimination at t=π/2.

**Central ambiguity identified:** TTH identifies modular time t with physical time τ, but this causes the β_A factor. If physical time = modular time (literal TTH claim), predictions disagree with QM by factor β_A. If physical time = β_A × modular time (normalization), predictions agree. Resolving this normalization question is the critical next step.

**Leads:** (1) Read Connes-Rovelli 1994 and Haggard-Rovelli 2013 carefully for the normalization convention. (2) Compute K_A for the COUPLED (entangled) thermal state — the product state is trivially β_A H_A, but the coupled state may give K_A ≠ βH_A, which would be TTH's genuine novel prediction. (3) Tolman-Ehrenfest effect derivation in TTH context.

---

## Exploration 002 — Normalization Resolution + Entangled-State Modular Hamiltonian
**Phase:** 1 (Foundation) → Phase 2 entry | **Status:** Complete (Full Success) | **Date:** 2026-03-27

**Goal:** (A) Resolve normalization ambiguity: τ_physical = t_modular or β×t_modular? (B) Compute ΔK_A = K_A - βH_A for bilinearly coupled global Gibbs state.

**Part A — RESOLVED:** Physical time = β × modular time (τ = β×t). Confirmed by three independent sources: Bisognano-Wichmann (τ = β_U × t_modular for Rindler), Martinetti-Rovelli 2003 eq.18 ("β ≡ -τ/s" — most explicit), Connes-Rovelli 1994 eq.55, Haggard-Rovelli 2013 eq.13. Consequence: with correct normalization, TTH reproduces standard QM for uncoupled equilibrium oscillators (period = 2π/ω_A). The β_A factor from exploration-001 was a normalization artifact.

**Part B — COMPUTED:** For H_AB = H_A + H_B + λ q_A q_B at single temperature β, ΔK_A ≠ 0 for λ≠0. Key results:
- Order: ΔK_A = O(λ²) exactly. O(λ¹) vanishes analytically (⟨q_B⟩=0). Numerically confirmed (power law p=1.998).
- Structure: diagonal part (Δβ = -1.36λ²: effective temperature renormalization) + band-2 off-diagonal (squeezing ∝ a²+a†²). Shape universal at λ=0.05 and λ=0.3.
- Observable prediction: local modular flow of ρ_A gives C_local_TTH(τ) with period LONGER than free-oscillator QM by Δτ/τ ≈ 0.68λ² (at λ=0.3: 6.48%).

**Critical open question:** Is C_local_TTH ≠ C_full_QM? Exploration-002 compared local modular flow to *free* oscillator (H_A only). The proper Phase 2 comparison requires computing the FULL QM autocorrelation Tr[ρ_AB x_A(τ) x_A(0)] with x_A(τ) evolved under H_AB, and seeing if this differs from C_local_TTH. Note: C_full_QM = C_global_TTH (since K_AB = βH_AB exactly), so the question is whether local modular flow ≠ global modular flow restricted to A.

**Unexpected finding:** ΔK_A has a squeezing component (band-2 off-diagonal) in addition to temperature renormalization. The modular Hamiltonian for the coupled state is that of a squeezed thermal state.

---

## Exploration 003 — Full QM vs Local TTH: The Critical Comparison
**Phase:** 2 (Core Computation) | **Status:** Complete (Full Success — Phase 2 Breakthrough) | **Date:** 2026-03-27

**Goal:** Compute C_full_QM(τ) and C_local_TTH(τ) for coupled oscillators and determine whether TTH (local interpretation) is distinguishable from standard QM.

**Answer: EMPHATICALLY YES. The predictions are structurally different, not just quantitatively.**

**Key number:** ‖C_full − C_local‖/‖C_full‖ = 0.827 at λ=0.3, β=2.0, τ∈[0,4π]. Full table:
| λ   | ‖C_full − C_local‖/‖C_full‖ |
|-----|------------------------------|
| 0.1 | 0.0915 (9.1%)                |
| 0.2 | 0.387 (38.7%)                |
| 0.3 | 0.827 (82.7%)                |
| 0.5 | 1.166 (>100%)                |

**Root cause (structural):** C_full shows two-frequency beating at ω_± = √(ω²±λ) (normal modes). C_local shows single-frequency oscillation at ω_eff < ω_A (entanglement red-shifts the clock). No parameter choice can make a single-frequency signal match a two-frequency beating pattern once beats are significant.

**Control check:** C_global_TTH = C_full_QM to exactly machine zero (K_AB = βH_AB for Gibbs state → global TTH = QM). The discrepancy is entirely between LOCAL and GLOBAL modular flows.

**Unexpected finding:** Entanglement RED-SHIFTS the local clock (ω_eff < ω_A, confirmed sign). The local TTH clock runs SLOWER when A is entangled with B.

**Open question:** Does Connes-Rovelli explicitly intend the LOCAL modular flow for TTH? If yes, the 9-83% discrepancy is a genuine testable prediction. If they meant global, TTH = QM (trivially). This literature disambiguation is the critical next step.

**Leads for exploration-004:**
1. Connes-Rovelli local vs. global disambiguation (literature, focused)
2. KMS condition check: do C_full and C_local satisfy KMS at the same β, or different effective β? (30-line script using existing infrastructure)
3. Experimental proposal: what quantum optics setup would detect absence of normal-mode beating?


---

## Exploration 004 — TTH Interpretation Confirmed: Local Modular Flow Falsified by Normal-Mode Splitting
**Phase:** 2 (Core Computation + Synthesis) | **Status:** Complete (RESOLVED) | **Date:** 2026-03-27

**Goal:** Resolve whether Connes-Rovelli TTH prescribes the LOCAL or GLOBAL modular flow for subsystem dynamics; verify with KMS temperature analysis; sketch minimum experimental test.

**Part A — RESOLVED (Literature):** Connes-Rovelli 1994 (gr-qc/9406019) explicitly use the LOCAL modular flow. Section 4.3 (Rindler wedge application) states: "The restriction of the state |0⟩ to the algebra A_R is of course a state on A_R, and therefore it generates a modular group of automorphisms α_t over A_R." This is the local modular flow of the restricted state, not the global flow restricted to A_R. Confirmed by Martinetti-Rovelli (2003) and the broader TTH literature.

**Part B — RESOLVED (KMS Analysis):** Both C_full and C_local satisfy KMS at β=2 exactly (Δβ_KMS ~ 10⁻³ for both). The distinction between QM and local TTH is NOT in effective temperature — it is entirely in spectral structure. C_full has two peaks (normal-mode splitting at ω_±); C_local has one peak (single modular frequency ω_eff).

**Part C — FALSIFICATION (Experimental):** The local TTH prediction (no normal-mode splitting in subsystem A autocorrelation) is already contradicted by existing data. Normal-mode splitting in coupled oscillator pairs has been observed routinely in trapped ions (Monroe/Turchette, 1990s–2023), coupled superconducting cavities (standard circuit QED), and optomechanical systems. QM (two-frequency beating) is always confirmed. Local TTH (single frequency) is always contradicted.

**Synthesis:** TTH does NOT make novel testable predictions for non-relativistic equilibrium Gibbs states.
- Local interpretation: predicts single-frequency autocorrelation → falsified by existing experiments
- Global interpretation: K_AB = βH_AB → TTH = QM exactly
- TTH's genuine novel content is restricted to the generally covariant regime (type III algebras, no background Hamiltonian), which was the original domain of Connes-Rovelli 1994

**Unexpected finding:** Takesaki's compatibility condition (existence of conditional expectation E: M → M_A) is the precise marker of TTH's domain boundary. When the condition fails (coupled Gibbs states), local TTH ≠ QM but is falsified. When it holds (type III vacua), local TTH may agree with QM and be consistent with experiment. This condition could identify regimes where TTH makes novel predictions (type III algebras in QFT).

**Computations flagged for later:**
1. Type III algebra test: repeat C_full vs C_local for adjacent Rindler wedges with Minkowski vacuum (1+1D lattice QFT) — ~200 lines
2. Non-equilibrium state test: C_full vs C_local for non-Gibbs states (squeezed thermal, post-quench) — ~50 lines
3. Analytic ΔK_A: second-order Duhamel formula for Δβ = −1.36λ² coefficient




