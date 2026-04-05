# Strategy-002 Final Report — TTH in Its Natural Habitat

**Strategy:** Three parallel computational probes testing TTH in the type III / QFT regime and non-equilibrium states
**Explorations:** 3 (001–003), all Math Explorer
**Completed:** 2026-03-28
**Status:** Complete — clear results across all three probes

---

## Summary

Strategy-002 tested the Connes-Rovelli Thermal Time Hypothesis in the regimes where it has genuine non-trivial content: (1) the Rindler wedge with the Minkowski vacuum (type III₁ algebras, where BW guarantees TTH works), (2) non-equilibrium post-quench states (where even global modular flow differs from Hamiltonian evolution), and (3) excited states in the Rindler wedge (where TTH predicts state-dependent time).

**Bottom line:** TTH is verified in the vacuum Rindler regime (the one case where BW guarantees it). For every non-vacuum state tested — post-quench, squeezed thermal, one-particle excitation — the modular flow generates dynamics at the **wrong frequencies**. The discrepancy is structural (different spectral content, not rescaling), and for excited states it **grows** in the continuum limit. The modular "clock" ticks at entanglement frequencies, not physical frequencies. TTH's thermal time tracks the entanglement structure / preparation history of the state, not the actual physical dynamics.

Combined with strategy-001 (non-relativistic equilibrium: TTH ≡ QM or falsified), this completes a comprehensive map of TTH's domain of validity.

---

## Exploration Results

### Exploration 001: Rindler Wedge Verification (Vacuum State) — SUCCESS

**Setup:** Free massless scalar field on 1+1D lattice (N = 50, 100, 200, 400 sites). Right half-lattice as subsystem. Williamson decomposition for bosonic modular Hamiltonian.

**Results:**
- **BW profile verified:** Modular Hamiltonian matches boost generator within 0.1% at entangling surface, degrading to ~6% at 3.5 lattice spacings. The BW-valid region is ~2-3 lattice spacings and is N-independent (a lattice-spacing effect, not finite-size).
- **KMS exactly satisfied:** Machine precision (10⁻¹⁶ relative error) at β = 2π.
- **Modular flow ≈ boost correlator:** 9% L² discrepancy at d = 0.5 from cut; converging at d = 1.5 (23% → 19% → 15% as N doubles).
- **Entanglement entropy:** Matches Calabrese-Cardy (c/6)ln(N) to 1.5%. Non-universal constant S₀ = −0.030 stable across N = 20–400.
- **Vacuum consistency:** All equal-time correlators agree to machine precision.

**Critical physics correction:** The GOAL expected C_local ≈ C_full (modular flow ≈ Hamiltonian time evolution). This is incorrect. BW says modular flow = Lorentz **boost**, not time translation. The ~24–34% discrepancy between modular and full-H correlators is the physically correct difference between Rindler time and Minkowski time. The right comparison is modular flow vs. boost correlator, which does converge.

**Unexpected finding:** Only 2–3 modes carry significant entanglement across the cut (leading mode = 91% of entropy). The entanglement spectrum is extremely sparse.

### Exploration 002: Non-Equilibrium TTH Test (Post-Quench) — SUCCESS

**Setup:** Two coupled oscillators H_AB(λ). Post-quench state: thermal state of uncoupled system (λ = 0), then coupling turned on. State is NOT Gibbs of coupled H, so K_AB ≠ βH_AB. Fock space N = 20, verified at N = 15, 25.

**Results:**

| λ | ‖C_QM − C_global‖ / ‖C_QM‖ | C_QM frequencies | C_global frequencies |
|---|---|---|---|
| 0.1 | 9.6% | ω_± = 1.049, 0.949 | ω = 1.0 |
| 0.3 | 102% | ω_± = 1.140, 0.837 | ω = 1.0 |
| 0.5 | 175% | ω_± = 1.225, 0.707 | ω = 1.0 |

- **Structural discrepancy:** C_QM has normal-mode frequencies ω_± = √(ω² ± λ); C_global has only uncoupled frequency ω = 1.0. Completely disjoint spectral content.
- **Modular time = pre-quench time:** Global modular flow generates evolution under H_AB(0), the pre-quench Hamiltonian. TTH "remembers" the preparation dynamics and ignores the post-quench coupling.
- **Analytical formulas verified:** C_QM(t) = A/2[cos(ω₊t) + cos(ω₋t)], C_global(t) = A·cos(ωt), matching numerics to 10⁻⁹.
- **Asymptotic discrepancy → √3 ≈ 1.732** for any λ > 0 (disjoint frequencies → zero cross-correlation).
- **Convergence:** Results stable to 9+ significant digits at N = 20.

**Product-state identity:** C_global = C_local exactly for the post-quench state (which is a product state ρ_A ⊗ ρ_B). The B-mode part of K_AB commutes with x_A ⊗ I_B and drops out. For entangled non-Gibbs states, this identity breaks.

**Squeezed state test (r = 0.3, λ = 0.3):**

| | Post-quench | Squeezed |
|---|---|---|
| Global TTH discrepancy | 102% (structural) | **7.8%** (quantitative) |
| Local TTH discrepancy | 102% | 180% |
| Correct frequencies? | NO | **YES** (amplitudes differ) |

The squeezed state's modular flow has the **correct** normal-mode frequencies — only amplitudes differ. This reveals a hierarchy: states "close" to Gibbs (like S·ρ_Gibbs·S†) have quantitative discrepancies; states "far" from Gibbs (post-quench) have structural discrepancies.

### Exploration 003: Excited-State Modular Flow — STRONG SUCCESS

**Setup:** Free massless scalar field, N = 20–200 sites. One-particle excitation |1_m⟩ = b†_m|0⟩. Gaussian approximation to modular Hamiltonian (exact two-point functions, quadratic modular Hamiltonian). Convergence study across multiple N values.

**Results:**

The response δC = C^{(1)} − C^{(0)} (change due to excitation) has completely different spectral content for modular vs. physical evolution:

| | δC_full (physical) | δC_local (modular) |
|---|---|---|
| Dominant frequency | ω_m (physical mode) | ε_k/(2π) (modular energies) |
| Amplitude at ω_m | 100% (by definition) | **0.01%** at N = 100 |
| Nature | Single clean cosine | Multiple modular peaks |

**The discrepancy GROWS in the continuum limit:** For fixed physical frequency ω ≈ 0.3:

| N | δ_disc |
|---|---|
| 30 | 4.2 |
| 50 | 5.4 |
| 100 | 10.0 |
| 150 | 12.6 |

Power-law: δ_disc ~ N^{+0.33}. The modular clock and the physical clock diverge as the lattice becomes finer.

**Mode-0 convergence is an artifact:** The apparent N^{−0.47} convergence for mode 0 is entirely due to ω_0 = π/(N+1) → 0, which makes δC_full flatten to a constant. For fixed physical frequency, the real trend is divergence.

**Momentum sector amplification:** The perturbation to the π-coupling of the modular Hamiltonian persists at ~30% even as N → ∞, while the φ-coupling perturbation vanishes as 1/N.

**Gaussian approximation caveat:** The one-particle state is non-Gaussian. The true modular Hamiltonian has nonlinear (cubic+) terms. However, the structural mismatch (completely wrong frequencies) makes it very unlikely perturbative corrections would restore the physical frequency.

---

## Synthesis Across Both Strategies

### Complete TTH Domain Map

| Regime | Algebra | State | TTH prediction | QM prediction | Agreement? | Source |
|--------|---------|-------|---------------|---------------|------------|--------|
| Coupled oscillators, Gibbs | Type I | Thermal equilibrium | Global: K_AB = βH_AB | H_AB evolution | **Global TTH ≡ QM** | S1-E003 |
| Coupled oscillators, Gibbs | Type I | Thermal equilibrium | Local: K_A/β evolution | H_AB evolution | **Local TTH ≠ QM** (single freq vs two-freq) | S1-E003 |
| Rindler wedge, vacuum | Type III₁ | Vacuum | Modular flow = boost | Boost (BW theorem) | **TTH ≡ QM** ✓ | S2-E001 |
| Coupled oscillators, post-quench | Type I | Non-Gibbs (product) | K_AB/β = H_AB(0) evol. | H_AB(λ) evolution | **TTH ≠ QM** (wrong frequencies, structural) | S2-E002 |
| Coupled oscillators, squeezed | Type I | Non-Gibbs (entangled) | Global: K_sq/β evolution | H_AB evolution | **TTH ≈ QM** (7.8%, quantitative, correct freqs) | S2-E002 |
| Rindler wedge, 1-particle | Type III₁ | Excited | Modular flow at ε_k/(2π) | Physical freq ω_m | **TTH ≠ QM** (wrong frequencies, grows with N) | S2-E003 |

### The Pattern

TTH works **if and only if** the modular Hamiltonian happens to coincide with (a rescaling of) the generator of the physical dynamics:

1. **Gibbs states + global algebra:** K_AB = βH_AB by construction → TTH ≡ QM (tautological)
2. **Vacuum + Rindler wedge:** K_R = 2π × boost generator by BW theorem → TTH ≡ boost (proven)
3. **Everything else:** K ≠ (const) × H_physical → TTH generates the wrong dynamics

The modular Hamiltonian encodes the **entanglement structure** of the state, which is related to (but not identical to) the physical Hamiltonian. For equilibrium/vacuum states, the entanglement structure is determined by the Hamiltonian, so K ∝ H. For non-equilibrium/excited states, the entanglement structure reflects the **preparation history** — the Hamiltonian that created the state — which may differ from the current physical Hamiltonian.

### What Modular Time "Means"

Across all explorations, a consistent picture emerges:

**Modular time is preparation-history time.** It generates evolution under the Hamiltonian that created the state, not the Hamiltonian currently governing the dynamics.

- Post-quench: modular flow evolves under the pre-quench Hamiltonian (E002)
- Excited state: modular flow ticks at entanglement frequencies determined by how the state was prepared (E003)
- Gibbs/vacuum: preparation Hamiltonian = current Hamiltonian (by definition), so TTH "accidentally" agrees

This interpretation explains why TTH works for equilibrium: equilibrium is precisely the condition where the preparation history and the current dynamics agree.

---

## Recommendations for Next Strategy

### Direction A (Highest priority): Adversarial Review + Prior Art Search

Strategy-002 produced several potentially novel claims but ran no adversarial exploration. The most urgent next step is a thorough adversarial review covering:
1. Prior art search for each novel claim (specific search terms provided below)
2. Numerical artifact checks (Gaussian approximation for E003, Fock truncation for E002)
3. Conceptual attacks ("TTH was never meant for non-equilibrium" defense)
4. Verification of the Peschel/Williamson formula via KMS (done for E001, should extend to E003)

### Direction B (High priority): Coherent State Test

E003 used a Gaussian approximation for a non-Gaussian state. A clean resolution: test with **coherent state excitations** (which ARE Gaussian), where the Gaussian modular Hamiltonian is exact. If the structural mismatch persists for coherent states, the Gaussian approximation caveat is eliminated.

### Direction C (Medium priority): "Distance from Gibbs" Metric

E002 found that squeezed states (7.8% discrepancy) are much closer to QM than post-quench states (102%). Quantifying the metric d(ρ, ρ_Gibbs) that predicts whether TTH gives structural vs. quantitative disagreement would be a clean result.

### Direction D (Lower priority): Analytic ΔK_A

The numerical coefficient Δβ = −1.36λ² from strategy-001 remains unproven analytically. Second-order Duhamel perturbation theory would give the exact coefficient.

### Direction E (Lower priority): Final Synthesis

Combine strategy-001 + strategy-002 into a comprehensive synthesis paper structure with the domain map table above.

---

## Novel Claims

### Claim 1: Modular Flow of a Post-Quench State Generates Pre-Quench Dynamics

**Claim:** For a system quenched from H₀ to H₁ (instantaneous coupling change), the global modular flow of the pre-quench thermal state ρ₀ = e^{−βH₀}/Z generates evolution under H₀, not H₁. The correlators have completely disjoint spectral content: C_QM contains normal-mode frequencies of H₁, while C_TTH contains only frequencies of H₀. The asymptotic relative discrepancy is √3 for any nonzero coupling change.

**Evidence:**
- Numerical: Fock space computation, N = 20, β = 2.0, ω = 1.0, λ = 0.1–0.5. Converged to 9+ significant digits (E002)
- Analytical: Exact formulas C_QM(t) = A/2[cos(ω₊t) + cos(ω₋t)], C_global(t) = A·cos(ωt), verified to 10⁻⁹ (E002)
- FFT: Spectral peaks at ω_± for C_QM, at ω for C_global, zero overlap (E002)
- Asymptotic: √3 follows from disjoint spectra + Parseval (E002)

**Novelty search:** The statement that K_AB ≠ βH for non-Gibbs states is standard (Takesaki, Bratteli-Robinson). The specific spectral consequence for post-quench states and the "modular time = pre-quench time" interpretation were not found in reviewed literature. Cardy & Tonni (2016, arXiv:1602.08273) study modular Hamiltonians after quenches in CFT but focus on entanglement entropy evolution, not correlator dynamics. Hollands & Sanders (2017, arXiv:1702.04924) discuss modular Hamiltonians for non-equilibrium states in QFT but do not compute correlators.

**Strongest counterargument:** This may be considered a trivial consequence of K = −log ρ = βH₀ + const for a Gibbs state of H₀. The "pre-quench dynamics" interpretation adds no mathematical content beyond identifying K with H₀. A skeptic would say: "of course modular flow under H₀ gives H₀ dynamics — what else would it give?"

**Status:** Verified numerically and analytically. The claim is mathematically rigorous for this system. The interpretation ("modular time = preparation-history time") is novel as a physical framing but may be considered obvious in hindsight.

---

### Claim 2: Product-State Identity — Global and Local Modular Flows Agree on Local Observables

**Claim:** For product states ρ = ρ_A ⊗ ρ_B, the global and local modular flows produce identical correlators for observables localized in A: C_global_TTH(τ) = C_local_TTH(τ) exactly. This is because the B-mode part of K_AB commutes with x_A ⊗ I_B and cancels.

**Evidence:**
- Numerical: C_global = C_local to machine precision (10⁻¹⁶) for all λ values (E002)
- Analytical: Algebraic proof from [K_B, x_A ⊗ I_B] = 0 for product states (E002)
- Counter-check: For entangled states (squeezed), C_global ≠ C_local (180% discrepancy) (E002)

**Novelty search:** This is likely a known result in the modular theory literature (it follows from the tensor product structure of modular operators for product states, cf. Takesaki Vol. II, Theorem IX.4.2). Not claimed as novel.

**Status:** Verified. Likely known but useful as a diagnostic.

---

### Claim 3: Excited-State Modular Flow Has Structurally Wrong Frequency Content

**Claim:** For a one-particle excitation |1_m⟩ of a free scalar field on a half-lattice, the modular flow response δC_local has NO spectral power at the physical mode frequency ω_m. The modular flow oscillates at modular frequencies ε_k/(2π) (determined by the entanglement spectrum), which are unrelated to ω_m. The relative discrepancy δ_disc ~ N^{+0.33} for fixed physical frequency — it **grows** in the continuum limit.

**Evidence:**
- Numerical: FFT analysis at N = 50, 100; amplitude at target frequency is 0.01% of physical response (E003)
- Convergence: δ_disc measured at N = 30, 50, 80, 100, 150 with fixed ω ≈ 0.3; power-law fit N^{+0.33} (E003)
- Multi-mode: Tested 8 modes, all show structural mismatch (E003)
- Mode-0 artifact identified: apparent convergence for mode 0 is due to ω_0 → 0, not genuine agreement (E003)

**Novelty search:** Faulkner (2015 series, arXiv:1501.06444), Lashkari (2016, arXiv:1508.03506), and Casini-Huerta (2009, arXiv:0903.5284) compute modular Hamiltonians for excited/deformed states but focus on the modular Hamiltonian itself, not on the correlator dynamics. The specific statement that modular flow response has zero spectral weight at the physical frequency was not found. The growing-discrepancy result (N^{+0.33}) has no known precedent.

**Strongest counterargument:** The Gaussian approximation. The one-particle state is non-Gaussian, and the true modular Hamiltonian has nonlinear terms. These could in principle contribute spectral weight at the physical frequency. However: (a) the mismatch is so complete (0.01% of expected amplitude) that perturbative corrections seem insufficient; (b) the structural argument (modular spectrum has no mode at ω_m) would require non-perturbative corrections to fix; (c) a clean resolution would be to test coherent states (Gaussian), where the approximation is exact.

**Status:** Computed under Gaussian approximation. The structural finding is robust but the Gaussian caveat must be addressed before claiming a definitive result. **Recommended next step: coherent state test (Direction B).**

---

### Claim 4: Squeezed Non-Gibbs States Have Quantitative (Not Structural) TTH Discrepancy

**Claim:** For squeezed thermal states ρ_sq = S·ρ_Gibbs·S†, the global TTH discrepancy is only 7.8% (vs. 102% for post-quench at same λ = 0.3), and the discrepancy is **quantitative** — the modular flow has the correct normal-mode frequencies ω_± but slightly wrong amplitudes. This contrasts with post-quench states where the discrepancy is structural (completely wrong frequencies).

**Evidence:**
- Numerical: FFT of squeezed-state C_global shows peaks at ω_± = 1.140, 0.843 matching C_QM (E002)
- Comparison: Post-quench C_global has single peak at ω = 1.0, missing both ω_± (E002)
- Physical argument: K_sq = S(βH)S† ≈ βH + O(r), so modular flow is a perturbation of the actual dynamics (E002)

**Novelty search:** No literature found comparing TTH predictions across different classes of non-equilibrium states. The distinction between structural and quantitative discrepancy based on "distance from Gibbs" appears novel.

**Strongest counterargument:** This is a single data point (one squeezing parameter r = 0.3, one coupling λ = 0.3). The pattern might not generalize. A systematic study of the metric d(ρ, ρ_Gibbs) is needed.

**Status:** Computed for one case. Suggestive of a deeper pattern but requires systematic study. Partially verified.

---

### Claim 5: The BW-Valid Region Is N-Independent (Lattice Spacing Effect)

**Claim:** On the lattice, the Bisognano-Wichmann profile (modular Hamiltonian ∝ distance × local energy density) is accurate within 0.1% for the first ~1.5 lattice spacings from the entangling surface and degrades to ~6% by 3.5 spacings. This region does NOT grow with N — the ratios h_actual/h_BW at fixed lattice distance are N-independent. The deviation is a lattice-spacing effect: to extend the BW-valid region, one needs a finer lattice (smaller spacing at fixed physical size), not a larger lattice.

**Evidence:**
- Numerical: BW profile ratios at d = 0.5, 1.5, 2.5, 3.5, 4.5 for N = 50, 100, 200 — all within 1% of each other across N values (E001)
- Both diagonal and off-diagonal elements checked (h_π and h_φ blocks) (E001)

**Novelty search:** Lattice modular Hamiltonian computations exist (Casini-Huerta 2009, Eisler-Peschel 2009 for fermions). The N-independence of the BW-valid region may be implicit in these works but was not found as an explicit statement.

**Strongest counterargument:** This is a property of the specific lattice discretization (Dirichlet BC, nearest-neighbor coupling). Different discretizations (periodic BC, higher-order stencils) might have different BW-valid regions.

**Status:** Computed. Likely implicit in prior work. Minor novelty.

---

## What Was NOT Resolved

1. **Gaussian approximation for E003:** The excited-state result uses a Gaussian approximation for a non-Gaussian state. A coherent-state test (Gaussian, exact) would resolve this.
2. **Adversarial review:** No adversarial exploration was run. All novel claims need prior-art search and numerical-artifact stress testing.
3. **Analytic ΔK_A:** The coefficient Δβ = −1.36λ² from strategy-001 remains numerical.
4. **"Distance from Gibbs" metric:** The squeezed-state result (Claim 4) suggests a hierarchy but is a single data point.
5. **de Sitter horizon test:** Mentioned in strategy-001 recommendations but not attempted.
6. **Connes cocycle for excited states:** The formal tool for computing the change in modular Hamiltonian between states. Would provide a rigorous (non-Gaussian) derivation.

---

## Appendix: Exploration Map

| Exploration | Phase | Type | Key Output |
|---|---|---|---|
| 001 | 1 | Math | BW verified on lattice; modular flow = boost ≠ time translation; KMS exact; entropy ∝ (1/6)ln N |
| 002 | 1 | Math | Post-quench: C_QM ≠ C_global (102% at λ=0.3, structural); modular time = pre-quench time; squeezed: 7.8% |
| 003 | 1 | Math | Excited state: modular flow at wrong frequencies; 0.01% amplitude at target freq; δ_disc ~ N^{+0.33} |

**Code locations:**
- Rindler verification: `explorations/exploration-001/code/rindler_verification.py`
- Non-equilibrium test: `explorations/exploration-002/code/` (compute_nonequilibrium.py, spectral_analysis.py, analytical_comparison.py, squeezed_state_test.py)
- Excited-state flow: `explorations/exploration-003/code/`
