# History of Report Summaries

## Exploration 001 — Rindler Wedge Verification (Vacuum State)

**Goal:** Verify TTH in the Rindler wedge regime by computing the modular Hamiltonian of the Minkowski vacuum restricted to a half-lattice and checking the Bisognano-Wichmann prediction.

**Outcome: SUCCESS (with important physics correction)**

TTH verified in its intended domain. All five checks pass:
1. **BW profile**: Modular Hamiltonian matches boost generator within 0.1% at entangling surface
2. **KMS**: Exactly satisfied to machine precision (10⁻¹⁶)
3. **Modular ≈ boost correlator**: 9% L2 discrepancy at d=0.5, converging at d=1.5 (23%→19%→15% as N doubles)
4. **Entanglement entropy**: Matches Calabrese-Cardy (c/6)ln(N) to 1.5%
5. **Vacuum consistency**: All equal-time correlators agree to machine precision

**Critical physics finding**: BW says modular flow = Lorentz BOOST, not time translation. The ~24-34% C_mod vs C_full discrepancy is the correct physical difference between Rindler and Minkowski time.

**Unexpected**: Only 2-3 modes carry significant entanglement. BW-valid region is ~2-3 lattice spacings and N-independent (lattice spacing effect, not finite-size).

---

## Exploration 002 — Non-Equilibrium TTH Test (Post-Quench State)

**Goal:** Test TTH for a post-quench state (non-Gibbs) and determine whether modular time makes physically meaningful predictions for non-equilibrium states.

**Outcome: SUCCESS**

TTH makes genuinely different predictions for non-Gibbs states with large, structural discrepancies:
- λ=0.1: 9.6% discrepancy | λ=0.3: 102% | λ=0.5: 175%
- C_QM has normal-mode frequencies ω_±; C_global has only uncoupled ω = 1.0 — completely disjoint spectra

**Key takeaway**: Modular time = pre-quench time. TTH modular flow generates evolution under the pre-quench Hamiltonian, ignoring post-quench coupling entirely.

**Unexpected findings**:
1. C_global = C_local exactly for product states (product-state identity)
2. Squeezed state has much smaller global TTH discrepancy (7.8% vs 102% at λ=0.3) — quantitative, not structural. Correct frequencies, slightly wrong amplitudes.

---

## Exploration 003 — Excited-State Modular Flow (State-Dependent Time)

**Goal:** Test TTH's state-dependent time prediction for a one-particle excitation on a lattice scalar field.

**Outcome: STRONG SUCCESS**

TTH predicts structural state-dependent time for excited states:
1. delta_C_full is a clean cosine at physical frequency ω_m
2. delta_C_local has NO power at ω_m — dominant frequencies are modular frequencies ε_k/(2π)
3. At N=100, amplitude of delta_C_local at target frequency is 0.01% of delta_C_full
4. Discrepancy GROWS in continuum limit: delta_disc ~ N^{+0.33} for fixed physical frequency

**Key takeaway**: The modular "clock" ticks at entanglement frequencies, not physical frequencies. Parallels E002: modular time tracks entanglement structure, not physical dynamics.

**Unexpected**: Mode-0 convergence is an artifact (ω_0→0 makes delta_C_full → constant). Momentum sector sees persistent ~30% perturbation even as N→∞.
