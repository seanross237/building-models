# Strategy 003 — Verify, Stress-Test, Close

## Objective

This is the finishing strategy. Strategies 001 and 002 produced a comprehensive domain map of TTH's validity across 6 regimes and a central interpretive finding ("modular time is preparation-history time"). Strategy-003 has three jobs:

1. **Resolve the Gaussian approximation caveat** on the mission's strongest novel claim (Claim 3: excited-state modular flow diverges from physics in the continuum limit)
2. **Run a formal adversarial review** — prior art search, numerical artifact checks, and conceptual stress-testing of ALL claims from both strategies
3. **Synthesize** findings into a complete picture with experimental connections (Tier 5)

Budget: **4 explorations, all mandatory.** The strategy is complete when all 4 are done — no early stopping.

## Context from Strategies 001 and 002

### Complete domain map (6 regimes tested):

| Regime | State | TTH vs QM | Source |
|--------|-------|-----------|--------|
| Coupled oscillators, Gibbs | Equilibrium | Global TTH ≡ QM (tautological); Local TTH ≠ QM (single freq) | S1-E003 |
| Rindler wedge, vacuum | Vacuum | TTH ≡ boost (by BW) ✓ | S2-E001 |
| Coupled oscillators, post-quench | Non-Gibbs (product) | TTH ≠ QM — structural (wrong frequencies, 102%) | S2-E002 |
| Coupled oscillators, squeezed | Non-Gibbs (entangled) | TTH ≈ QM — quantitative (7.8%, correct frequencies) | S2-E002 |
| Rindler wedge, 1-particle | Excited | TTH ≠ QM — structural (wrong frequencies, grows as N^{0.33}) ⚠️ Gaussian approx | S2-E003 |

### Novel claims requiring verification:

**Claim 1 (Strong):** Post-quench modular flow generates pre-quench dynamics. Analytically verified for coupled oscillators. √3 asymptotic discrepancy. Prior art partially searched.

**Claim 3 (Strongest but caveated):** Excited-state modular flow has ZERO spectral weight at the physical frequency. Discrepancy grows as N^{0.33} in continuum limit. **CAVEAT: Uses Gaussian approximation for non-Gaussian state.** The true modular Hamiltonian has cubic+ terms that could contribute spectral weight at the physical frequency. Must be resolved.

**Claim 4 (Suggestive):** Squeezed states (close to Gibbs) have quantitative-not-structural discrepancy. Single data point — needs more evidence or explicit caveat.

**Central interpretation:** "Modular time is preparation-history time." Explains all 6 regimes. Novel as a physical framing.

### Code infrastructure:
- Rindler lattice: `strategy-002/explorations/exploration-001/code/rindler_verification.py`
- Non-equilibrium: `strategy-002/explorations/exploration-002/code/`
- Excited state: `strategy-002/explorations/exploration-003/code/`
- Fock space toolkit: `strategy-001/explorations/exploration-001/code/`

## Methodology

### ALL 4 explorations are mandatory. The strategy is NOT complete until all 4 have run.

**Exploration 1: Coherent State Resolution (resolve Gaussian caveat)**

This is the single most important exploration. Claim 3 is the mission's strongest novel result, but it relies on a Gaussian approximation for a non-Gaussian state.

**Setup:** Use the same Rindler lattice from S2-E001 (N = 50, 100, 200). Instead of a one-particle state, prepare a **coherent state** |α⟩ = D(α)|0⟩ where D(α) is a displacement operator on a mode localized in the right sublattice. Coherent states ARE Gaussian, so the Gaussian modular Hamiltonian is EXACT — no approximation caveat.

**Compute:**
1. The reduced covariance matrix for the right sublattice in state |α⟩
2. The modular Hamiltonian via Williamson decomposition (exact for Gaussian states)
3. δC_local(t) = C_local^{(α)}(t) - C_local^{(0)}(t) (modular flow response to coherent excitation)
4. δC_full(t) = C_full^{(α)}(t) - C_full^{(0)}(t) (physical response to coherent excitation)
5. FFT of both: does δC_local have spectral weight at the physical mode frequency?
6. Convergence study: does the discrepancy grow/shrink/plateau with N?

**Expected outcome:** If the structural mismatch persists (wrong frequencies, zero spectral weight at physical mode), Claim 3 is confirmed with no approximation caveat. If the coherent state DOES show spectral weight at the physical frequency, the Gaussian approximation matters and Claim 3 must be weakened.

**Control check:** For α = 0 (vacuum), everything must agree with S2-E001 results exactly.

**Baseline specification:** δC_full means ⟨α|φ_j(t) φ_j(0)|α⟩ - ⟨0|φ_j(t) φ_j(0)|0⟩, where φ_j(t) = e^{iHt} φ_j e^{-iHt} with H = full lattice Hamiltonian. δC_local means the same correlator but with φ_j(t) evolved under the modular Hamiltonian K_R^{(α)} of the coherent state's reduced density matrix on the right sublattice.

**Exploration 2: Adversarial Review**

A dedicated adversarial exploration targeting ALL claims from both strategies. This exploration MUST:

**Part A — Prior art search (the search MUST find prior art or demonstrate convincingly none exists):**

Search terms to use (web search + arXiv):
- "modular Hamiltonian quench" / "modular flow non-equilibrium" / "thermal time hypothesis test"
- "excited state modular Hamiltonian lattice" / "Bisognano-Wichmann excited state"
- "modular flow correlator" / "modular automorphism physical time"
- "thermal time preparation history" / "state-dependent time quantum"
- Authors to check: Lashkari, Casini, Huerta, Faulkner, Cardy, Tonni, Witten, Rovelli, Connes, Martinetti, Hollands, Sanders, Ciolli, Longo, Morinelli

For each claim, report: (a) closest prior art found, (b) what's genuinely new vs. what's a corollary of known results, (c) what an AQFT specialist would say.

**Part B — Numerical artifact check:**
- For E002 (post-quench): verify at N_Fock = 30, 40 (beyond the N=25 already checked). If results don't change, Fock truncation is not an issue.
- For S2-E003 (excited state): run at N_lattice = 250, 300 to extend the convergence study. Does N^{0.33} scaling persist?
- For S2-E001 (Rindler): check that BW convergence at d = 1.5 continues to improve at N = 500.

**Part C — Conceptual attacks:**
1. "TTH was never meant for non-equilibrium states" — engage seriously. What did Connes-Rovelli actually claim about TTH's scope? Re-read gr-qc/9406019, Sections 4-5 specifically. Does TTH require the state to be KMS? If so, testing non-KMS states is out-of-scope and Claims 1, 3, 4 are not falsifications of TTH but demonstrations of its limitations.
2. "The modular flow of an excited state SHOULD be different from the boost — that's a feature, not a bug" — the TTH proponent could argue that the modular flow of an excited state defines the CORRECT notion of time for an observer in that state. Why is the boost "more physical" than the modular flow? Can we distinguish them experimentally?
3. "The lattice is not type III" — the half-lattice algebra is type I (finite-dimensional). Type III₁ (Rindler) is only recovered in the continuum limit. Are the lattice results trustworthy predictors of the continuum behavior?

**Exploration 3: Distance-from-Gibbs Characterization**

Extend Claim 4 from a single data point to a systematic study. This is a clean, bounded computation.

**Setup:** Use the coupled oscillator code from S2-E002. Fix λ = 0.3, β = 2.0, ω = 1.0. Prepare a family of states parameterized by a single "distance from Gibbs" parameter:
- Squeezed states: vary squeezing parameter r from 0 to 1.0 in steps of 0.1
- Post-quench states: vary quench magnitude δλ = λ_final - λ_initial from 0 to 0.5

For each state, compute:
1. The relative entropy S(ρ || ρ_Gibbs) — this is the natural "distance from Gibbs" metric
2. The global TTH discrepancy ‖C_QM − C_global‖/‖C_QM‖
3. Whether the discrepancy is structural (wrong frequencies) or quantitative (correct frequencies, wrong amplitudes) — use FFT
4. The transition: at what relative entropy does the discrepancy switch from quantitative to structural?

**Expected outcome:** A clean curve: TTH discrepancy vs. relative entropy, with a marked transition from "quantitative" to "structural" regime. This quantifies the "preparation-history" interpretation.

**Control:** At r = 0, δλ = 0 (Gibbs state), discrepancy must be zero (global TTH ≡ QM for Gibbs).

**Exploration 4: Final Synthesis + Experimental Connection**

The last exploration produces the mission's final deliverable: a complete synthesis situating TTH across all tested regimes, with explicit experimental connections.

**This exploration must produce:**

1. **Complete domain map table** — all regimes from S1 and S2, with Claim status (confirmed/caveated/falsified) updated based on E1-E3 of this strategy.

2. **Experimental connection:** Post-quench quantum systems are routinely prepared in cold atom experiments (Bloch group, Greiner group, Chin group). Quenched BECs, optical lattices with sudden parameter changes — these are EXACTLY the systems where S2-E002's prediction applies. The explorer should:
   - Identify the specific experimental setup (e.g., two coupled optical traps with controllable tunneling)
   - Estimate the timescales: modular flow period τ_mod vs. physical oscillation period τ_phys
   - Estimate whether the frequency difference (ω vs. ω_±) is resolvable with current technology
   - Identify what would need to be measured (single-site autocorrelation function)

3. **"Preparation-history time" as a constructive principle:** Beyond TTH, does the observation that modular flow tracks preparation history have independent value? For example:
   - As a diagnostic for equilibration (modular flow = Hamiltonian flow ↔ state is Gibbs)
   - As a probe of quantum quench dynamics (modular spectrum reveals the pre-quench Hamiltonian)
   - As a reinterpretation of the BW theorem (vacuum state = "equilibrium" of the boost)

4. **Situate in the "is time fundamental?" debate** with explicit implications for approaches to quantum gravity.

## Validation Criteria

**Strategy-003 is complete when ALL 4 explorations have run.** No early stopping.

**Strategy is succeeding when:**
- E1 resolves the Gaussian caveat (either confirming or weakening Claim 3)
- E2 finds the closest prior art for each claim and engages seriously with conceptual attacks
- E3 produces a clean curve with at least 10 data points
- E4 names a specific experimental setup with estimated timescales

**Mission is complete when:**
- The domain map is comprehensive and all claims have been adversarially reviewed
- Each claim is rated: confirmed (evidence + adversarial survived), weakened (caveats remain), or falsified
- At least one claim survives adversarial review at Tier 4
- An experimental connection exists (even "in principle")

## Cross-cutting rules

1. **Explorers must compute.** Same as S1 and S2.
2. **Every computation has a control check.** Same as S2.
3. **Pre-load ALL prior findings.** Every GOAL.md must include the domain map table and the specific claims. Explorers should not re-derive anything from S1 or S2.
4. **The adversarial exploration (E2) has a minimum standard:** it must find the closest prior art for EACH claim, or provide specific evidence that no prior art exists (search terms used, papers checked, negative result documented).
5. **No early stopping.** This is the finishing strategy. All 4 explorations must run.
