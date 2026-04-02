# Strategy 002 — TTH in Its Natural Habitat

## Objective

Test the thermal time hypothesis in the regimes where it has genuine non-trivial content: (1) type III von Neumann algebras in QFT, where no background Hamiltonian exists and modular flow is the only candidate for time evolution, and (2) non-equilibrium states, where even the global modular flow differs from standard Hamiltonian evolution.

Strategy-001 closed off the non-relativistic equilibrium regime with a definitive result: TTH either equals QM (global interpretation) or is falsified (local interpretation) for Gibbs states with known Hamiltonians. This strategy moves into the territory TTH was designed for.

The deliverable is: (a) a verification or falsification of TTH in the type III / QFT regime, backed by lattice computation, AND (b) characterization of TTH's predictions for non-equilibrium states.

## Context from Strategy-001

### What was established (carry forward as known facts):
- **Normalization**: τ_physical = β × t_modular (confirmed by Bisognano-Wichmann, Martinetti-Rovelli 2003, Connes-Rovelli 1994)
- **Connes-Rovelli use the LOCAL modular flow** (Section 4.3 of gr-qc/9406019, explicit quote confirmed)
- **For Gibbs states**: K_AB = βH_AB exactly → global TTH ≡ QM. Local TTH gives single-frequency autocorrelation (no normal-mode splitting) → already falsified by experiment
- **ΔK_A structure**: For bilinear coupling at O(λ²): temperature renormalization (Δβ = −1.36λ²) + squeezing (band-2 off-diagonal). O(λ¹) vanishes analytically
- **Takesaki's compatibility condition** marks the TTH domain boundary: where it fails, local ≠ global modular flow

### What was NOT resolved (these are strategy-002's targets):
1. Does local modular flow agree with physical dynamics for type III algebras? (Rindler wedge test)
2. Does TTH make novel predictions for excited/non-vacuum states in QFT? (Connes cocycle)
3. Does global TTH differ from standard QM for non-Gibbs states? (Non-equilibrium test)
4. Analytic form of ΔK_A coefficient (Duhamel perturbation theory)

### Code infrastructure available:
- Fock-space modular Hamiltonian toolkit: `strategy-001/explorations/exploration-001/code/`
- ΔK_A sweep code: `strategy-001/explorations/exploration-002/code/`
- C_full vs C_local comparison: `strategy-001/explorations/exploration-003/code/`
- KMS analysis: `strategy-001/explorations/exploration-004/code/kms_analysis.py`

### Computation Registry:
The file `../../COMPUTATIONS-FOR-LATER.md` contains three pre-specified computations with difficulty estimates, references, and expected outcomes. The Strategizer MUST read this file before designing explorations — these are the computations strategy-001 identified as the natural next steps.

## Methodology

### Phase 1: Three Parallel Computational Probes (explorations 1–3)

All three probes are **mandatory**. They can be launched in parallel or rapid sequence. Each is a self-contained computation that produces a concrete number.

**Probe 1: Rindler Wedge Verification (Vacuum State)**

Test TTH in its intended domain: type III₁ algebras with the Minkowski vacuum.

Setup: Discretize a free massless scalar field on a 1+1D lattice (N = 100–200 sites). Split into "left" and "right" sublattices at the midpoint (these are the lattice analogue of left/right Rindler wedges). Compute:
- The vacuum state correlation matrix C_ij = ⟨0|a†_i a_j|0⟩ for the right sublattice
- The single-particle modular Hamiltonian h via Peschel's formula: h = log((1-C)/C) (for free fields, K is quadratic and determined by h)
- The modular flow correlator: C_local(t) = Σ_{ij} [e^{iht}]_{i,k} C_{kj} (Gaussian state formula)
- The full QM correlator: C_full(t) = ⟨0|φ_k(t) φ_k(0)|0⟩ restricted to site k in the right sublattice, with φ_k(t) = e^{iHt} φ_k e^{-iHt} using the FULL lattice Hamiltonian
- Compare C_local vs C_full

**Expected result:** Agreement, by the Bisognano-Wichmann theorem (the lattice version should converge to it). This is the control — verifying that TTH works in its intended domain. If they DON'T agree on the lattice, the Strategizer should investigate finite-size effects vs. genuine discrepancy.

**Verification checks:** (a) The modular Hamiltonian h should approximate the BW profile h_i ∝ distance_from_boundary × lattice_hamiltonian_density as N → ∞. (b) The reduced state should satisfy KMS at β = 2π with respect to h.

**Probe 2: Non-Equilibrium Coupled Oscillators**

Test TTH where global modular flow ≠ Hamiltonian evolution.

Setup: Use strategy-001's coupled oscillator code (exploration-003). Prepare a **non-Gibbs initial state** — specifically, a post-quench state: start with the ground state of H_AB(λ=0) (uncoupled), then instantaneously turn on coupling λ. The state ρ = |ψ_0⟩⟨ψ_0| (the uncoupled ground state) is NOT the Gibbs state of H_AB(λ). Therefore K_AB = -log ρ ≠ βH_AB for any β.

Compute:
- C_global_TTH(τ) using modular flow of ρ under K_AB (the modular Hamiltonian of the non-Gibbs state)
- C_QM(τ) using Hamiltonian evolution under H_AB(λ)
- Compare. They should differ (since K_AB ≠ βH_AB). Characterize the discrepancy: how big? Structural or just quantitative?

**This is the probe most likely to find genuine novel content.** For non-Gibbs states, the global modular flow is not just a rescaling of Hamiltonian evolution — it's genuinely different dynamics. If the discrepancy is interesting (not just "modular flow is wrong"), it could reveal what TTH's modular time "means" physically for non-equilibrium situations.

**Probe 3: Excited-State Modular Flow in the Rindler Wedge**

Test whether TTH makes a state-dependent prediction for time in QFT.

Setup: Same lattice as Probe 1, but with a non-vacuum state. Prepare a one-particle excited state |1_k⟩ (one excitation in mode k localized near the boundary). Compute:
- The reduced state ρ_R^{(1)} of the right sublattice (this is a non-Gaussian perturbation of the vacuum reduced state)
- The modular Hamiltonian K_R^{(1)} of this excited state (use the first-order perturbative formula from Lashkari 2016 if the full computation is too expensive, or compute directly for small N)
- The modular flow correlator C_local^{(1)}(t)
- The full QM correlator C_full^{(1)}(t) = ⟨1_k|φ_j(t) φ_j(0)|1_k⟩ restricted to the right sublattice
- Compare C_local^{(1)} vs C_full^{(1)}

**This is the most conceptually important probe.** In the vacuum, TTH agrees with standard QFT (by BW). For an excited state, the modular flow changes but the "physical" dynamics (boost/Hamiltonian) don't. If C_local^{(1)} ≠ C_full^{(1)}, then TTH gives state-dependent time evolution — a radical prediction. If they agree (perhaps by some structural property of type III algebras), that's a deep result about the relationship between states and dynamics.

**Difficulty note:** This is the hardest probe. If direct computation of K_R^{(1)} is infeasible for the explorer, a perturbative approach is acceptable: compute δK = K_R^{(1)} - K_R^{(0)} to first order in the excitation amplitude, and derive the first-order correction to the correlator.

### Phase 2: Deepen + Mandatory Adversarial (explorations 4–5)

**Exploration 4: Deepen the best Phase 1 result.**

The Strategizer chooses which Phase 1 probe produced the most interesting or surprising result and designs a follow-up:
- If Probe 1 found unexpected disagreement → verify it's not a finite-size artifact; increase N; check continuum limit
- If Probe 2 found a specific non-equilibrium TTH prediction → test it in a second non-equilibrium state; characterize the parameter dependence
- If Probe 3 found state-dependent time → compute the Connes cocycle explicitly; check if the state-dependence is observable-dependent or universal
- If all three agreed with expectations → attempt the analytic ΔK_A derivation (Computation 3 from the registry) as a clean publishable result

**Exploration 5: MANDATORY adversarial review.**

This exploration MUST attempt to break every claim from explorations 1–4. Specifically:
1. **Prior art search**: For each novel claim, search the literature systematically. Use specific search terms: "modular Hamiltonian lattice scalar field", "Bisognano-Wichmann lattice", "non-equilibrium modular flow", "excited state modular Hamiltonian Rindler", "thermal time hypothesis predictions". The search MUST find prior art or demonstrate convincingly that none exists.
2. **Numerical artifact check**: For each lattice computation, the adversarial exploration should vary N (lattice size) and check convergence. Finite-size effects in lattice QFT are real and can produce spurious results.
3. **Conceptual attack**: The strongest objection to any "TTH is falsified in regime X" claim is "TTH was never meant for regime X." The adversarial exploration must engage with this argument seriously — not dismiss it but identify exactly where TTH's domain boundary is and whether our results fall inside or outside.
4. **Verify the Peschel formula**: The lattice modular Hamiltonian computation depends on h = log((1-C)/C). Verify this numerically by checking that the reduced state satisfies KMS with respect to the resulting modular flow.

### Phase 3: Synthesis (exploration 6)

**Exploration 6: Final synthesis across both strategies.**

Combine strategy-001 (non-relativistic equilibrium: TTH ≡ QM or falsified) with strategy-002 (type III / non-equilibrium: results from Probes 1–3) into a comprehensive map:

| Regime | Algebra type | State | TTH prediction | QM prediction | Agreement? |
|--------|-------------|-------|---------------|---------------|------------|

This table should cover every system computed across both strategies. The synthesis should:
- Identify the PRECISE boundary of TTH's domain of validity
- Determine whether TTH makes ANY novel prediction in ANY regime
- State the strongest remaining open question
- Assess what would need to be true for TTH to have experimentally testable content

## Validation Criteria

**Strategy is succeeding when:**
- At least 2 of 3 Phase 1 probes produce clean numerical results
- The Rindler vacuum probe reproduces BW (control check)
- At least one probe finds either a genuine novel TTH prediction or a clean falsification in a new regime
- The adversarial review engages seriously with prior art

**Strategy is exhausted when:**
- All three probes are complete AND the adversarial review has verified (or falsified) the key claims
- OR a probe reveals that the lattice computation is fundamentally unreliable for the type III regime (finite-size effects dominate), and no workaround exists

**Red flags to pivot on:**
- If the lattice Rindler computation doesn't converge to BW even for the vacuum → something is wrong with the lattice setup, not with TTH. Debug before drawing conclusions.
- If Probe 3 (excited state) is computationally infeasible → fall back to the perturbative approach (first-order δK). If even that fails, replace with the analytic ΔK_A computation.
- If the non-equilibrium probe finds that modular time for non-Gibbs states is "just wrong" (gives unphysical correlators) → this is itself a result worth documenting. TTH's claim is that modular flow defines physical time; if that time is unphysical for non-equilibrium states, TTH's scope is narrower than claimed.

## Cross-cutting rules (carried from strategy-001 + strengthened)

1. **Explorers must compute.** Every exploration produces code that runs and outputs numbers. Reasoning-only explorations are failures.
2. **Every computation has a control check.** Something that should equal a known value by construction. No result is trusted without it.
3. **Specify baselines explicitly.** C_full means evolution under the FULL Hamiltonian (not the free/uncoupled one). C_local means evolution under the LOCAL modular Hamiltonian K_A (not the global K_AB). Be precise in GOAL.md.
4. **Pre-load strategy-001 findings.** Every GOAL.md should include the key facts from strategy-001 (normalization resolved, local interpretation confirmed, Gibbs regime closed). Explorers should not re-derive these.
5. **Use the existing code.** Strategy-001's code infrastructure (Fock space toolkit, correlation comparisons) should be referenced and extended, not rebuilt from scratch.
