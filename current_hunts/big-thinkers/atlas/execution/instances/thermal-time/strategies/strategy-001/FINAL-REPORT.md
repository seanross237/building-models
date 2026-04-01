# Strategy-001 Final Report — Thermal Time Hypothesis: Empirical Content in Non-Relativistic QM

**Strategy:** Phase 1 (mathematical toolkit) → Phase 2 (head-to-head computation) → Final synthesis
**Explorations:** 4 (001–004)
**Completed:** 2026-03-27
**Status:** Complete — clear conclusion reached

---

## Summary

Strategy-001 investigated whether the Connes-Rovelli Thermal Time Hypothesis (TTH) makes empirically distinguishable predictions from standard quantum mechanics for non-relativistic bipartite thermal systems. Four explorations established the full mathematical setup and ran the key comparisons.

**Bottom line:** TTH does not make novel testable predictions for non-relativistic equilibrium Gibbs states. In the natural (local) interpretation intended by Connes-Rovelli, TTH predicts single-frequency autocorrelation for a coupled subsystem — a prediction that is already falsified by existing normal-mode splitting experiments. In the global interpretation, TTH is exactly equivalent to QM. TTH's genuine novel content is restricted to the generally covariant regime where no background Hamiltonian exists.

---

## Directions Tried

### Direction 1: Phase 1 — Mathematical Toolkit (Explorations 001–002)

**Goal:** Establish modular Hamiltonians explicitly for key systems; resolve normalization; compute ΔK_A for the coupled case.

**What was found:**

*Exploration 001* cataloged explicit modular Hamiltonians for four systems:
- Rindler wedge: K = 2π × boost generator (Bisognano-Wichmann)
- Bell state: K_A = log(2)·I (trivial flow, maximally mixed)
- Thermal harmonic oscillator (uncoupled): K = βH (modular flow = time evolution at rate β)
- 1+1d CFT interval: K = 2π∫f(x)T₀₀dx (Möbius flow, Casini-Huerta)

It also identified the normalization ambiguity: literal identification of modular time with physical time gives predictions differing from QM by factor β_A.

*Exploration 002* resolved the normalization question and computed ΔK_A:
- **Normalization confirmed:** τ_physical = β × t_modular (not 1:1). Established by Bisognano-Wichmann (τ = β_U × t_modular), Martinetti-Rovelli 2003 eq.18 (most explicit), Connes-Rovelli 1994 eq.55, Haggard-Rovelli 2013 eq.13.
- **ΔK_A = O(λ²) for coupled Gibbs state.** For H_AB = ½p_A² + ½ω²q_A² + ½p_B² + ½ω²q_B² + λq_Aq_B at temperature β, the modular Hamiltonian of subsystem A differs from βH_A by: (i) temperature renormalization Δβ = −1.36λ² (negative: entanglement red-shifts the effective temperature), and (ii) band-2 off-diagonal squeezing ∝ a_A² + a_A†². The O(λ¹) term vanishes analytically (⟨q_B⟩=0 for the thermal state).

**Outcome:** Full success. Mathematical foundation established, normalization resolved, ΔK_A characterized.

---

### Direction 2: Phase 2 — Head-to-Head Comparison (Explorations 003–004)

**Goal:** Compute C_full_QM(τ) vs C_local_TTH(τ); determine if TTH is distinguishable from QM; confirm interpretation; assess experimental feasibility.

**What was found:**

*Exploration 003* ran the critical numerical comparison at β=2.0, ω=1.0, N=20 Fock levels:

| λ   | ‖C_full − C_local‖/‖C_full‖ | C_full peak freqs         | C_local peak freq |
|-----|------------------------------|---------------------------|-------------------|
| 0.1 | 0.0915 (9.1%)               | ω_+ ≈ 1.048, ω_− ≈ 0.949 | ≈ 0.98            |
| 0.2 | 0.387 (38.7%)               | ω_+ ≈ 1.10, ω_− ≈ 0.89   | ≈ 0.89            |
| 0.3 | 0.827 (82.7%)               | ω_+ ≈ 1.14, ω_− ≈ 0.84   | ≈ 0.80            |
| 0.5 | 1.166 (>100%)               | ω_+ ≈ 1.20, ω_− ≈ 0.70   | ≈ 0.80            |

The discrepancy is **structural, not quantitative**: C_full shows two-frequency beating at ω_± = √(ω²±λ) (normal modes); C_local shows single-frequency oscillation at a red-shifted ω_eff. No amount of parameter tuning can fit a single-frequency curve to a beating pattern when the beating is significant.

**Control check:** C_global_TTH = C_full_QM to machine zero (K_AB = βH_AB for Gibbs state → global TTH ≡ QM exactly). The discrepancy is entirely between LOCAL and GLOBAL modular flows.

*Exploration 004* resolved three remaining questions:

1. **Connes-Rovelli use the LOCAL modular flow.** Section 4.3 of Connes-Rovelli 1994 (gr-qc/9406019) explicitly states: "The restriction of the state |0⟩ to the algebra A_R is of course a state on A_R, and therefore it generates a modular group of automorphisms α_t over A_R." This is confirmed by Martinetti-Rovelli (2003) Class.Quant.Grav.20:4919 and the full TTH literature.

2. **KMS temperatures are identical for both correlators.** Both C_full and C_local satisfy KMS at β=2 exactly (Δβ_KMS ~ 10⁻³ for both). The local TTH prediction does not differ from QM in effective temperature — it differs in spectral structure (which frequencies are present). This is a more nuanced result than expected.

3. **The local TTH prediction is falsified by existing experiments.** The local interpretation predicts NO normal-mode splitting in coupled oscillator pairs. Normal-mode splitting has been observed routinely in trapped ions, coupled microwave cavities, and optomechanical systems. Existing data contradicts local TTH for non-relativistic coupled subsystems.

**Resolution:** TTH was designed for the generally covariant regime (QFT, cosmology, black holes) where no background Hamiltonian exists and modular time is the only available time parameter. For non-relativistic systems where H_AB is known and experimentally accessible, applying TTH in the local interpretation overshoots: the local modular flow is NOT the physical time evolution when the system has a known Hamiltonian. TTH = QM for equilibrium non-relativistic systems (global interpretation = QM, local interpretation = falsified).

---

## Most Promising Findings

1. **ΔK_A structure (Exploration 002):** The modular Hamiltonian correction has a specific form — temperature renormalization plus squeezing — that emerges from the bilinear coupling. The coefficient Δβ = −1.36λ² (numerically) may be derivable analytically via second-order Duhamel perturbation theory. This structure (squeezed modular Hamiltonian) may generalize to other coupled systems.

2. **Entanglement red-shifts the local clock (Exploration 003):** The local modular flow of ρ_A runs at ω_eff < ω_A for any λ > 0. The entanglement with B effectively lowers the local frequency. This is a clean, analytically verifiable statement (sign follows from ΔK_A being negative at leading order in λ²).

3. **TTH domain boundary (Exploration 004):** Takesaki's compatibility condition (existence of conditional expectation E: M → M_A such that E∘σ_t^ω = σ_t^{ω_A}∘E) serves as the precise marker of when local TTH predictions deviate from QM. For coupled Gibbs states this fails, and the failure is what produces the spectral discrepancy. This condition could be used to identify novel TTH regimes: wherever the conditional expectation exists, local TTH = global TTH = QM; wherever it fails (type III algebras, interacting QFTs), local TTH is genuinely different.

4. **Type III algebra test (Exploration 004, flagged):** The computation of C_full vs C_local for two adjacent Rindler wedges with the Minkowski vacuum (type III algebras, the regime TTH was designed for) remains undone. In this regime, the local and global flows may AGREE (by special properties of the Minkowski vacuum), which would vindicate TTH in its intended domain. This is the key follow-up computation.

---

## Recommendations for Next Strategy

The TTH-for-non-relativistic-QM question is closed: TTH makes no novel predictions in this regime. The remaining scientific value lies in two directions:

### Direction A (High priority): TTH in the Genuinely Covariant Regime

Test TTH in the setting it was designed for: type III von Neumann algebras in QFT, where no background Hamiltonian exists and the modular flow is the ONLY available time evolution. Specific setups:

1. **Adjacent Rindler wedges with Minkowski vacuum (1+1d lattice QFT):** Compute C_full (Minkowski vacuum two-point function restricted to one wedge) vs C_local (modular flow of the Rindler state on the wedge algebra). Check whether they agree — TTH predicts they should. This would verify TTH in its intended domain. Requires ~200 lines of code (scipy, lattice discretization).

2. **de Sitter horizon:** The Gibbons-Hawking temperature for de Sitter gives K = 2πK_dS by Bisognano-Wichmann-style arguments. Test whether the thermal correlator for a static observer in de Sitter satisfies KMS with respect to the modular flow — and check against the de Sitter Hamiltonian for the static patch. If they agree, TTH is verified in a cosmologically relevant setting.

### Direction B (Moderate priority): Non-Equilibrium TTH

For non-Gibbs states (post-quench states, squeezed thermal states), K_AB ≠ βH_AB even globally. In this regime, TTH (even the global interpretation) differs from standard Hamiltonian evolution, and may make genuinely novel predictions. The existing exploration-003 infrastructure can be extended with ~50 lines to test this.

### Direction C (Lower priority, but clean): Analytic ΔK_A

The numerical result Δβ = −1.36λ² could be derived analytically via second-order Duhamel perturbation theory on ρ_A = Tr_B[e^{-β(H_A+H_B+λV)}]. This would give the exact coefficient and the full structure of ΔK_A to O(λ²). A closed-form result would be a clean publishable contribution.

---

## Novel Claims

### Claim 1: The Local Modular Flow of a Bilinearly Coupled Thermal Oscillator Lacks Normal-Mode Splitting

**Claim:** For coupled harmonic oscillators H_AB = ½(p_A² + ω²q_A²) + ½(p_B² + ω²q_B²) + λq_Aq_B at inverse temperature β, the position autocorrelation of subsystem A under the local modular flow C_local(τ) = Tr[ρ_A e^{iK_Aτ/β} x_A e^{-iK_Aτ/β} x_A] contains a single frequency ω_eff < ω_A. The standard QM autocorrelation C_full(τ) = Tr[ρ_{AB} e^{iH_{AB}τ} x_A e^{-iH_{AB}τ} x_A] contains two frequencies ω_± = √(ω²±λ). These are structurally distinct for all λ > 0.

**Evidence:**
- Numerical computation in Fock space (N=20), β=2.0, ω=1.0; exploration-003 code at `explorations/exploration-003/code/`
- ‖C_full − C_local‖/‖C_full‖ = 0.0915 at λ=0.1, 0.827 at λ=0.3, 1.166 at λ=0.5
- Control: C_global_TTH ≡ C_full_QM to machine zero (K_{AB}/β ≡ H_{AB} for Gibbs state, K_AB = -log ρ_{AB} = βH_{AB})
- Structural argument: ΔK_A has off-diagonal squeezing (band-2) that mixes ω_A modes without introducing ω_B structure → single-frequency output; H_{AB} couples A and B oscillators → two-frequency output

**Novelty search:** The statement that K_A ≠ βH_A for coupled systems is implicit in Araki's modular theory, but the specific spectral consequence (absence of normal-mode splitting in the local modular correlator) was not found in any reviewed literature. Martinetti-Rovelli 2003, Haggard-Rovelli 2013, and Connes-Rovelli 1994 do not compute oscillator autocorrelations. Papers on modular Hamiltonians for coupled oscillators (e.g., Lashkari 2014, Faulkner 2015 series) focus on entanglement entropy, not dynamical correlators.

**Strongest counterargument:** This is a finite-dimensional approximation (Fock truncation at N=20). For the exact infinite-dimensional oscillator, the modular Hamiltonian may have a richer structure that does include multi-frequency dynamics. The truncation introduces small errors (verified sub-ppb at N=15 to N=25 comparison), but the claim requires a full analytic treatment.

**Status:** Verified numerically. Analytic confirmation (second-order Duhamel) pending.

---

### Claim 2: The Entanglement-Induced Correction to the Modular Hamiltonian Has Squeezing Structure

**Claim:** For the bilinearly coupled Gibbs state, ΔK_A = K_A − βH_A = O(λ²) and decomposes as: (i) a diagonal part implementing a temperature renormalization Δβ = −1.36λ² (negative: entanglement lowers the effective temperature of A), and (ii) off-diagonal band-2 terms of the form ∝ (a_A² + a_A†²) — the squeezing generator. This structure is universal across λ ∈ [0.05, 0.3].

**Evidence:**
- Direct matrix computation: ρ_A = Tr_B[e^{-βH_{AB}}/Z] evaluated in Fock basis (N=20); K_A = −log(ρ_A); ΔK_A = K_A − βH_A
- Power-law fit for O(λ¹) cancellation: slope 1.998 in log-log fit of ‖ΔK_A‖ vs λ (exploration-002)
- Structure plot shows diagonal and band-2 separation; shape invariant from λ=0.05 to λ=0.3 (exploration-002 code: `explorations/exploration-002/code/sweep_results_v2.json`)
- Coefficient Δβ = −1.36λ² (numerical fit)

**Novelty search:** Araki (1976) and Takesaki (1972) establish that K_A ≠ βH_A in general. Petz (1988) gives abstract conditions. The specific decomposition into temperature renorm + squeezing for bilinear coupling was not found in the reviewed literature. The closest related work is Casini, Huerta, and collaborators on modular Hamiltonians for intervals in QFT — but these are spatial, not bipartite oscillator, settings.

**Strongest counterargument:** The coefficient 1.36 is numerical, not analytic. It may depend on the specific truncation N or other parameters. A closed-form result via perturbation theory would be stronger. Additionally, "squeezing" of the modular Hamiltonian may follow trivially from the Bogoliubov transformation that diagonalizes H_{AB} — if so, the structure is expected and not novel.

**Status:** Partially verified. Numerical result is reproducible; analytic derivation pending.

---

### Claim 3: The Connes-Rovelli TTH Predictions for Non-Relativistic Coupled Systems Are Either Trivially Equivalent to QM or Already Falsified

**Claim:** For non-relativistic bipartite thermal systems with a known Hamiltonian H_{AB}:
- **Global interpretation** (σ_t acts on M_AB with state ρ_{AB}): K_{AB} = βH_{AB} exactly for Gibbs states → TTH ≡ QM. No novel prediction.
- **Local interpretation** (σ_t acts on M_A with restricted state ρ_A): K_A ≠ βH_A → C_local ≠ C_full. But local TTH predicts no normal-mode splitting, which is falsified by the extensive experimental record of normal-mode splitting in trapped ions, coupled microwave cavities, and optomechanical systems.

Therefore, TTH has no testable empirical content in the non-relativistic equilibrium regime.

**Evidence:**
- K_{AB} = βH_{AB} for Gibbs state: standard result (follows from ρ_{AB} = e^{−βH_{AB}}/Z → K_{AB} = −log ρ_{AB} = βH_{AB} + log Z · I); numerically confirmed by C_global = C_full at machine zero (exploration-003)
- Connes-Rovelli local interpretation confirmed: C-R 1994, Section 4.3 (gr-qc/9406019), explicit quote: "The restriction of the state |0⟩ to the algebra A_R is of course a state on A_R, and therefore it generates a modular group of automorphisms α_t over A_R." (exploration-004 literature analysis)
- Normal-mode splitting in coupled oscillators observed in: (a) trapped ion motional modes (Turchette et al. 1998; Monroe et al. 1995-2023); (b) coupled superconducting resonators (standard circuit QED); (c) optomechanical oscillators (Aspelmeyer group). All show two-frequency beating predicted by QM, not single-frequency predicted by local TTH.
- KMS temperatures identical: both C_full and C_local satisfy KMS at β=2 exactly (exploration-004 KMS analysis); the discrepancy is spectral structure, not temperature

**Novelty search:** The statement "TTH applies only to generally covariant systems" is implicit in Connes-Rovelli's framing but is typically not stated as a falsification claim for non-relativistic systems. The literature (Haggard-Rovelli 2013, Martinetti-Rovelli 2003) focuses on consistency of TTH with known results rather than asking when TTH fails. The explicit connection to normal-mode splitting falsification was not found in prior work.

**Strongest counterargument:** Experts in TTH would say this is not a "falsification" but a "domain of applicability" statement — TTH was never claimed to apply to non-relativistic systems with a known Hamiltonian. In that reading, Claim 3 is a tautology, not a discovery. The interesting question is whether TTH makes novel predictions in the covariant regime (unanswered by this strategy).

**Status:** Verified as a logical deduction from (a) confirmed local interpretation, (b) numerical discrepancy, (c) existing experimental record. The "falsification" framing is contested — the "domain of applicability" framing is the community consensus. Novel as an explicit proof-of-concept computation, not as a conceptual claim.

---

## What Was NOT Resolved

1. **TTH in the genuinely covariant regime**: Does the local modular flow agree with the "physical" time evolution in QFT settings with type III algebras (Rindler, de Sitter)? Strategy-001 did not reach this regime. This is the scientifically important open question.

2. **Non-equilibrium TTH**: Does TTH make novel predictions for non-Gibbs states (post-quench, squeezed thermal)? Not computed.

3. **Analytic ΔK_A to O(λ²)**: The numerical coefficient Δβ = −1.36λ² was not derived in closed form. Second-order Duhamel theory would give this.

4. **CFT interval**: The modular Hamiltonian for a CFT interval is local (Casini-Huerta), which means local TTH and global TTH agree in that case. This regime was identified as relevant but not explored.

---

## Appendix: Exploration Map

| Exploration | Phase | Type | Key Output |
|-------------|-------|------|------------|
| 001 | 1 | Standard | Modular Hamiltonian catalog; normalization ambiguity |
| 002 | 1 | Standard | τ=βt confirmed; ΔK_A = O(λ²), Δβ=−1.36λ², squeezing |
| 003 | 2 | Standard | C_full ≠ C_local (82.7% at λ=0.3); structural: two-freq vs single-freq |
| 004 | 2 | Standard | C-R use local flow; KMS β identical; local TTH falsified by exp. |

**Code locations:**
- Modular Hamiltonian toolkit: `explorations/exploration-001/code/`
- ΔK_A sweep: `explorations/exploration-002/code/` (`sweep_results_v2.json`)
- C_full vs C_local: `explorations/exploration-003/code/` (`comparison_results.json`)
- KMS analysis: `explorations/exploration-004/code/kms_analysis.py`
