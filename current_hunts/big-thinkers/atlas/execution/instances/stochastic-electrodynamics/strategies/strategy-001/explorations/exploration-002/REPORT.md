# Exploration 002 — SED Extension Landscape: What's Been Computed, What's Open

## Goal
Survey the landscape of SED computations across five key domains (hydrogen atom, anharmonic oscillators, multi-particle/entanglement, anomalous magnetic moment, and other systems) to identify the best extension direction for producing a novel, quantitative SED vs. QM/QED comparison.

---

## Part 1: What Has Been Computed in SED?

### 1.1 Hydrogen Atom / Coulomb Problem

The hydrogen atom is the most-studied extension of SED beyond the harmonic oscillator, and also the most problematic. The literature has gone through three distinct phases: initial optimism, computational falsification, and failed repair attempts.

#### Phase 1: Cole & Zou (2003, 2004) — Initial Optimism

**Key papers:**
- Cole & Zou, "Quantum Mechanical Ground State of Hydrogen Obtained from Classical Electrodynamics," Physics Letters A 317, 14–20 (2003). [arXiv:quant-ph/0307154]
- Cole & Zou, "Simulation Study of Aspects of the Classical Hydrogen Atom Interacting with Electromagnetic Radiation: Elliptical Orbits," J. Scientific Computing 20, 379–404 (2004)
- Cole & Zou, "Analysis of orbital decay time for the classical hydrogen atom interacting with circularly polarized electromagnetic radiation," Phys. Rev. E 69, 016601 (2004)

**Method:** Simulated a classical charged point particle in a Coulomb potential driven by classical electromagnetic zero-point radiation (ZPF). Used an adaptive 4th-order Runge-Kutta algorithm. 2D orbits in a simulation box (27 Å × 27 Å × 0.41 cm), with plane waves of wavelengths 0.1–900 Å. Ran 11 simulations starting at a radius of 0.53 Å (one Bohr radius) with different random field amplitudes.

**Result:** The probability density distribution was claimed to agree with the QM ground state (|ψ₁ₛ|²) of hydrogen, *without any fitting parameters*. The electron, driven by ZPF and damped by radiation reaction, appeared to settle into a distribution matching QM. Also found "striking subharmonic resonances."

**Critical limitation:** The simulations were relatively short. The question of long-term stability was left open.

#### Phase 2: Nieuwenhuizen & Liska (2015) — Self-Ionization Discovered

**Key papers:**
- Nieuwenhuizen & Liska, "Simulation of the hydrogen ground state in Stochastic Electrodynamics," Physica Scripta T165, 014006 (2015). [arXiv:1502.06856]
- Nieuwenhuizen & Liska, "Simulation of the hydrogen ground state in Stochastic Electrodynamics-2: Inclusion of Relativistic Corrections," Foundations of Physics 45, 1190–1202 (2015). [arXiv:1506.06787]
- Nieuwenhuizen & Liska, "On the Stability of Classical Orbits of the Hydrogen Ground State in Stochastic Electrodynamics," Entropy 18(4), 135 (2016)

**Method:** Extended Cole & Zou's work to full 3D using OpenCL-based GPU numerical integration of the Abraham-Lorentz equation in the dipole approximation. Stochastic Gaussian frequency components. Much longer run times than Cole & Zou.

**Critical result: SELF-IONIZATION.** In *all attempted simulations*, the atom ionized at longer times. While short-time results showed a trend toward ground-state-like behavior, the system was ultimately unstable. When the orbital angular momentum fell below ~0.588 ℏ, the electron entered highly eccentric orbits, gained energy with each revolution, and eventually escaped the Coulomb potential.

**Relativistic corrections:** The second paper included relativistic corrections. These had little effect — self-ionization persisted.

**Mechanism:** The failure appears linked to the behavior in highly eccentric (nearly radial) orbits. At very low angular momentum, the electron passes close to the nucleus, and the high-frequency components of the ZPF inject energy faster than radiation reaction can dissipate it.

#### Phase 3: Nieuwenhuizen (2020) — Renormalization Fails

**Key paper:** Nieuwenhuizen, "Stochastic Electrodynamics: Renormalized Noise in the Hydrogen Ground-State Problem," Frontiers in Physics 8, 335 (2020).

**Method:** Attempted to cure the self-ionization by renormalizing the stochastic force — suppressing high-frequency tails so frequency integrals are dominated by physical resonances. Tested multiple renormalization schemes: short-time regularization, absolute value variants, fractional power schemes.

**Result: ALL renormalization schemes failed.** Direct quote from paper: "in no situation did we find a way to escape from the previously signaled self-ionization." Nieuwenhuizen's frank conclusion: **"SED is not a basis for quantum mechanics."**

He speculated that the point-charge approximation for the electron might be the cause of the failure, but no resolution was proposed.

#### Also Relevant: Comments on Cole & Zou

**Paper:** Multiple comment papers appeared questioning Cole & Zou's methodology. See Springer "Comments on Cole and Zou's Calculation of the Hydrogen Ground State in Classical Physics," Foundations of Physics Letters (2004).

#### Current Status: **CONTESTED BUT LEANING STRONGLY NEGATIVE**

| Factor | Status |
|--------|--------|
| Short-time behavior | Looks QM-like (Cole & Zou 2003) |
| Long-time stability | Self-ionizes (Nieuwenhuizen 2015) |
| Relativistic corrections | Don't help (Nieuwenhuizen 2015) |
| Renormalized noise | Doesn't help (Nieuwenhuizen 2020) |
| Ground state energy -13.6 eV | Never cleanly reproduced |
| Community consensus | Most consider this a failure of SED |

The hydrogen problem is effectively closed as a research direction for our purposes — the computational evidence strongly suggests SED cannot reproduce a stable hydrogen ground state. The failure is fundamental (instability in eccentric orbits) rather than technical (insufficient simulation time or resolution).

---

### 1.2 Anharmonic Oscillator

#### Pesquera & Claverie (1982) — SED Disagrees with QM at Order β²

**Key paper:** Pesquera & Claverie, "The quartic anharmonic oscillator in stochastic electrodynamics," Journal of Mathematical Physics 23(7), 1315–1322 (1982).

**Setup:** A slightly anharmonic oscillator with potential V(x) = ½mω₀²x² + βx⁴, treated perturbatively in SED to second order in the coupling β.

**Key results — THREE distinct SED failures:**

1. **Energy correction:** The SED stationary mean energy agrees with QM at first order in β, but **disagrees at order β²**. In QM, the ground-state energy of the quartic oscillator is:
   - E₀(QM) = ½ℏω₀ + ¾(ℏ/mω₀)β - (21/8)(ℏ/mω₀)²β²/ℏω₀ + ...

   SED matches the ¾(ℏ/mω₀)β first-order correction but gives a *different coefficient* at β². The exact SED β² coefficient is computed in the paper but differs from 21/8.

2. **Absorption frequencies:** Using Kubo's linear response theory, the maximum absorption frequencies in SED **do not coincide with the quantum transition frequencies** when β ≠ 0. In QM, transitions occur at discrete frequencies ωₙₘ = (Eₙ - Eₘ)/ℏ. In SED, the absorption peaks shift differently with β.

3. **Radiation balance:** The equilibrium "radiation balance" (energy absorbed from ZPF = energy emitted via radiation reaction) is **not exactly satisfied** when β ≠ 0. In QM, this balance holds exactly at all orders. In SED, it breaks — meaning the anharmonic SED oscillator does not reach true equilibrium with the ZPF.

**Significance:** This is arguably the single most important SED result for our mission. It demonstrates:
- SED's success with the harmonic oscillator is **specific to linearity**
- The disagreement emerges at a computable, specific order (β²)
- Three independent signatures of disagreement exist (energy, frequencies, radiation balance)
- The calculation is perturbative and analytically tractable

#### Related Work

- Santos and others also studied anharmonic oscillators in SED during the late 1970s–early 1980s, reaching similar conclusions about nonlinear failures.
- Boyer, "Einstein-Hopf drag on an anharmonic oscillator moving through random radiation," Phys. Rev. D 29, 648 (1984) — studied anharmonic effects in a different context.
- A related paper: "The harmonic and anharmonic oscillator in classical stochastic electrodynamics," Il Nuovo Cimento B.

#### What Has NOT Been Done

**CRITICAL GAP:** Pesquera & Claverie's result is purely analytical (perturbation theory). **No one has verified this result numerically.** A direct numerical simulation of an anharmonic SED oscillator — solving the Langevin equation with a quartic term and measuring the equilibrium energy — appears to be unstudied. This is surprising given its importance, and represents a clear opportunity.

#### Current Status: **SED FAILS — ANALYTICALLY PROVEN, NUMERICALLY UNVERIFIED**

The anharmonic oscillator is a clean, documented SED failure. SED and QM agree at O(β) but disagree at O(β²). This has been known since 1982 but has apparently never been confirmed by direct simulation.

---

### 1.3 Multi-Particle Systems / Entanglement / Bell Inequalities

This is the most complex and contested area of SED research. There are three distinct sub-questions: (a) Do coupled oscillators in SED show entanglement-like correlations? (b) Can SED violate Bell inequalities? (c) Does SED reproduce QM for two-particle systems?

#### (a) Coupled Oscillators and Entanglement-like Correlations

**Key paper:** de la Peña, Valdés-Hernández & Cetto, "Entanglement of particles as a result of their coupling through the common background zero-point radiation field," Physica E 42, 308–312 (2010).

**Result:** Using Linear Stochastic Electrodynamics (LSED), when two non-interacting particles are coupled through the shared ZPF background, and both resonate at common frequencies, "non-factorizable states" emerge that correspond to entangled states of QM. For identical particles, the theory predicts states of maximum entanglement.

**Critical caveat:** This uses LSED — a specific formulation developed by de la Peña and Cetto that imposes additional statistical constraints beyond standard SED. The relationship between LSED and standard SED is debated.

**Related work:** Boyer (1973) showed that two SED oscillators coupled through the ZPF exhibit van der Waals-type correlations consistent with QM. The van der Waals force between two dipole oscillators (both unretarded 1/r⁶ and retarded 1/r⁷) is derived correctly by SED. This is one of SED's uncontested successes, but it involves only linear oscillators.

#### (b) Bell Inequalities and Stochastic Optics

**Key papers:**
- Marshall & Santos, "Stochastic optics: A local realistic analysis of optical tests of Bell inequalities," Phys. Rev. A 39, 6271 (1989)
- Casado, Marshall & Santos, "Type II parametric downconversion in the Wigner-function formalism: entanglement and Bell's inequalities," J. Opt. Soc. Am. B 15, 1572 (1998)
- Santos, "Local Model of Entangled Photon Experiments Compatible with Quantum Predictions Based on the Reality of the Vacuum Fields," Foundations of Physics 50, 1587–1607 (2020)
- Santos, "Local Realistic Interpretation of Entangled Photon Pairs in the Weyl-Wigner Formalism," Frontiers in Physics 8, 191 (2020)

**Marshall & Santos's position:** They developed "Stochastic Optics" (SO) as a local realistic alternative to quantum optics, treating vacuum fields as real. Their claim: entanglement is merely a correlation between signal field fluctuations and vacuum field fluctuations. They argue the Bell definition of local realism is "not general enough" and that Bell inequality violations do not refute local realism when vacuum field correlations are properly accounted for.

**Santos (2020):** Showed that in the Weyl-Wigner formalism, a local model of SPDC (spontaneous parametric down-conversion) experiments can reproduce QM predictions for polarization correlations including Bell-inequality-violating ones. The argument hinges on treating vacuum field amplitudes as hidden variables that are *contextual* (measurement-dependent in their selection).

**Mainstream response:** Most physicists reject this line of argument. Bell's theorem is considered rigorous, and the loopholes exploited by Marshall & Santos (particularly the detection efficiency loophole) have been closed by loophole-free Bell tests (Hensen et al. 2015, Giustina et al. 2015, Shalm et al. 2015). The contextuality argument (de la Peña, Cetto, Brody 1972; updated by de la Peña et al. later) is generally not accepted as invalidating Bell's theorem.

**Key paper on coupled oscillator correlations:** de la Peña & Cetto also argued that bipartite entanglement can be "induced" by a common background radiation field. However, this is in the LSED formalism which is not standard SED.

#### (c) The Question of Quantum Correlations vs. SED Correlations

This remains genuinely open, though the evidence leans against SED:
- SED reproduces correlations for *linear* systems (coupled harmonic oscillators) — these are essentially van der Waals-type correlations
- For nonlinear systems, SED correlations are expected to deviate from QM (by analogy with the single-particle anharmonic oscillator failure)
- No direct computation of Bell correlations from SED dynamics (solving coupled Langevin equations and measuring correlation functions) has been published

#### Current Status: **DEEPLY CONTESTED, PRACTICALLY INTRACTABLE FOR OUR PURPOSES**

The entanglement/Bell question in SED is a philosophical/foundational battleground. The computations needed to settle it definitively would require simulating full photon-pair experiments in SED, which is far beyond the scope of a single exploration. The most tractable sub-question — computing correlations between two coupled SED oscillators and comparing to QM — would be interesting but involves linear systems where SED is already expected to agree with QM.

---

### 1.4 Anomalous Magnetic Moment (g-2)

#### Pure SED: No Natural Framework for Spin

SED does not naturally incorporate spin. The electron in SED is a classical point charge — there is no intrinsic angular momentum. This makes formulating g-2 in pure SED fundamentally problematic.

#### de la Peña & Cetto (1981) — Phenomenological Treatment

**Key paper:** de la Peña & Cetto, "The spin and the anomalous magnetic moment of the electron in stochastic electrodynamics," Physics Letters A 81, 441 (1981).

**Approach:** Proposed that the zitterbewegung (rapid oscillation) induced on a harmonically bound electron by the ZPF accounts for spin. By selecting only the subensemble of the ZPF with a given circular polarization, they argued for a "satisfactory account" of both spin projection and the anomalous magnetic moment.

**Assessment:** This is qualitative, not a first-principles derivation. The treatment is phenomenological — it *assumes* a connection between ZPF circular polarization and spin rather than deriving it.

#### Cavalleri et al. (2010) — SEDS (Stochastic Electrodynamics with Spin)

**Key paper:** Cavalleri, Bosi, Barbero, Tonni, et al., "A quantitative assessment of stochastic electrodynamics with spin (SEDS): Physical principles and novel applications," Frontiers of Physics in China 5, 107–122 (2010).

**Key claim:** Using an extended electron model (center of charge in circular motion around center of mass at zitterbewegung frequency), they derive mass and charge corrections "without logarithmic divergence terms." The anomalous magnetic moment is expressed as a power series in the fine-structure constant α, claimed to be "accurate up to ninth decimal place with a difference of 90.22 × 10⁻¹² from the experimental value."

**Critical assessment — THIS CLAIM SHOULD BE VIEWED WITH EXTREME SKEPTICISM:**

1. **Not pure SED.** SEDS adds spin as a fundamental modification. This is a significant departure from the original SED program.
2. **Extended electron model.** The electron is given spatial structure (center of charge orbiting center of mass) — not a point particle. This introduces additional assumptions.
3. **Extraordinary precision claim.** Achieving 9-decimal-place accuracy from a classical theory would be as remarkable as QED's famous Schwinger calculation (α/2π = 0.00116...). The QED result required decades of effort by many groups.
4. **Non-mainstream venue.** Published in Frontiers of Physics in China, not a standard high-energy physics or foundations journal.
5. **Not independently verified.** No other group has reproduced or confirmed these results.
6. **The Lamb shift companion claim** (deriving the Lamb shift by imposing a cutoff at the de Broglie frequency) is similarly questionable — the cutoff is essentially put in by hand.

#### Boyer (1988) — Lamb Shift Environmental Effects

**Key paper:** Boyer, "Environmental effects on the Lamb shift according to stochastic electrodynamics," Phys. Rev. A 37, 1952 (1988).

This is a more rigorous treatment that studies how environmental modifications of the electromagnetic vacuum affect the Lamb shift in the SED framework. The results coincide with QED predictions for the environmental modification. However, this addresses the *modification* of the Lamb shift by boundaries, not the Lamb shift itself.

#### Current Status: **NOT A PRODUCTIVE DIRECTION**

Pure SED has no spin, so g-2 cannot be formulated. SEDS claims impressive results but from a small, non-mainstream group with unverified claims. The theoretical framework is too uncertain and the computation too ambitious for a single exploration.

---

### 1.5 Other SED Calculations

#### 1.5.1 The Four Established SED Successes

These are the "standard four" results where SED matches QM:

| System | SED Result | QM Match | Key Reference |
|--------|-----------|----------|---------------|
| Harmonic oscillator ground state | E₀ = ½ℏω₀, Gaussian distribution | Exact | Marshall (1963), Boyer (1975) |
| Casimir effect | Correct force F = -π²ℏc/(240a⁴) | Exact | Boyer (1973) |
| Van der Waals forces | Correct 1/r⁶ (unretarded) and 1/r⁷ (retarded) | Exact | Boyer (1973) |
| Blackbody radiation | Planck spectrum ρ(ω,T) | Exact | Boyer (1969), Marshall (1965) |

All four involve either linear systems (harmonic oscillators) or free-field calculations (Casimir, blackbody). This is not a coincidence — linearity is the key ingredient enabling SED's successes.

#### 1.5.2 Additional Results (Lesser Known)

- **Diamagnetism:** SED correctly predicts the diamagnetic susceptibility of a charged harmonic oscillator. This follows directly from the harmonic oscillator result.
- **Unruh effect:** Boyer showed a connection between SED and the Unruh effect — a uniformly accelerated detector in the ZPF sees a thermal spectrum. This is a deep result but hard to compute quantitatively.
- **Specific heat decrease at low temperatures:** SED's quantized oscillator energy naturally gives the Einstein model of specific heats.

#### 1.5.3 Quantum Coherence Failure — Huang & Batelaan (2019)

**Key paper:** Huang & Batelaan, "Testing Quantum Coherence in Stochastic Electrodynamics with Squeezed Schrödinger Cat States," Atoms 7(2), 42 (2019). [arXiv:2011.12910]

**Setup:** Used two counter-propagating dichromatic laser pulses to promote a ground-state harmonic oscillator to a squeezed Schrödinger cat state (superposition of two macroscopically separated wavepackets).

**Result:** Upon recombination, QM predicts interference fringes in the probability distribution. **SED predicts no interference.** The SED probability distribution shows no fringe structure when the two separated wavepackets overlap.

**Significance:** This is a clean, falsifiable prediction. SED fails to reproduce quantum interference/coherence. The authors state this "gives a counterexample that rejects SED as a valid alternative to quantum mechanics." They further predict that "SED electron double-slit diffraction, if ever calculated, will not show fringes."

**Important nuance:** This result uses *excited states* of the harmonic oscillator, not just the ground state. SED notoriously has difficulty with excited states — in the standard SED harmonic oscillator, there are no discrete excited states. The ground state is an equilibrium distribution; excited states require non-equilibrium dynamics.

#### 1.5.4 Excited States and Discrete Spectra

**Key issue:** The SED harmonic oscillator has only one equilibrium state (the ground state). It has **no discrete excited states.** The quantum harmonic oscillator's excited states (n = 1, 2, 3, ...) with energies (n + ½)ℏω₀ have no natural SED counterpart.

Boyer (2019 review) notes that upon excitation by a single pulse, the SED oscillator shows "quantized excitation spectrum" behavior — the energy distribution after a pulse shows peaks near the QM energy levels. However, these are transient features of the non-equilibrium response, not true eigenstates.

This is a fundamental limitation: SED naturally produces only a single equilibrium state per system, not a discrete spectrum of states.

#### 1.5.5 Tunneling and Barrier Penetration

**Status: NOT computed in SED.** I found no papers computing barrier penetration or tunneling in the SED framework. The related work by Schafaschek, Vasconcelos & Macêdo (2024) on tunneling in Nelson's stochastic mechanics is relevant — they find Nelson's approach reproduces tunneling rates with τ_QM = (π/2)τ̄_stochastic. But Nelson's stochastic mechanics is mathematically equivalent to QM (by construction), so this is a consistency check, not a test of SED.

SED should in principle be able to produce barrier-crossing events — a particle driven by stochastic ZPF noise can occasionally gain enough energy to cross a classical barrier. Whether the *rates* would match QM tunneling rates is an open question, and a potentially interesting computation.

#### 1.5.6 Compton Scattering

**Status: NOT computed in SED.** Compton scattering involves photon-electron scattering with relativistic kinematics. This would require a fully relativistic SED treatment which is extremely challenging. Not a tractable direction.

---

## Part 2: Discriminating Power Assessment

### Assessment Matrix

| System | Tractability | Discriminating Power | Novelty | Overall Score |
|--------|-------------|---------------------|---------|--------------|
| **Anharmonic oscillator** | ★★★★★ | ★★★★★ | ★★★★☆ | **Best** |
| Hydrogen atom | ★★☆☆☆ | ★★★★★ | ★☆☆☆☆ | Poor (already done) |
| Two coupled oscillators | ★★★★☆ | ★★☆☆☆ | ★★★☆☆ | Moderate |
| Bell inequality simulation | ★☆☆☆☆ | ★★★★★ | ★★★★★ | Poor (intractable) |
| g-2 / anomalous moment | ★☆☆☆☆ | ★★★★★ | ★★★★★ | Poor (no framework) |
| Lamb shift | ★★☆☆☆ | ★★★★☆ | ★★★☆☆ | Moderate |
| Tunneling / barrier | ★★★☆☆ | ★★★★☆ | ★★★★★ | Good |
| Quantum coherence/interference | ★★★☆☆ | ★★★★★ | ★★☆☆☆ | Moderate (already shown) |

### Detailed Assessment for Top Candidates

#### Anharmonic Oscillator — Score: EXCELLENT

**Tractability: 5/5.** The calculation is an extension of the harmonic oscillator code from Exploration 001. Add a βx⁴ term to the Langevin equation. The numerical simulation is straightforward — solve the SDE, collect equilibrium statistics, compare energy to QM perturbation theory. Can be done in a few hours of coding.

**Discriminating power: 5/5.** Pesquera & Claverie (1982) analytically proved that SED disagrees with QM at O(β²). This means:
- At O(β): SED and QM agree. We can verify this computationally (consistency check).
- At O(β²): SED and QM disagree. We can quantify the discrepancy precisely.
- The QM comparison value is known to arbitrary precision from perturbation theory.
- The discrepancy grows with β, so we can trace the exact boundary between agreement and disagreement.

**Novelty: 4/5.** Pesquera & Claverie computed this analytically in 1982. A numerical verification has apparently *never been done*. Our computation would:
- Be the first numerical simulation of the anharmonic SED oscillator
- Verify the perturbative result independently
- Extend beyond perturbation theory (large β) where the analytic calculation breaks down
- Characterize the full SED probability distribution (not just the energy)

#### Tunneling Through a Barrier — Score: GOOD

**Tractability: 3/5.** Requires setting up a double-well potential V(x) = -½mω₀²x² + ¼λx⁴ (or a generic barrier) and measuring passage rates. More complex than the anharmonic oscillator because you need long simulation times to observe rare events. But fundamentally the same Langevin equation approach.

**Discriminating power: 4/5.** QM tunneling rates are exponentially sensitive to barrier height and width (WKB formula). SED barrier-crossing would be driven by ZPF energy fluctuations. The *mechanism* is completely different (stochastic fluctuation vs. quantum tunneling), so the rates might agree or disagree dramatically. High discriminating power because the QM prediction is a specific number (tunneling rate) that SED would either match or not.

**Novelty: 5/5.** No one has computed tunneling in SED. This would be genuinely new.

**Risk:** The calculation is harder, the physics is less clear, and there's no prior analytic result to guide expectations.

#### Two Coupled Oscillators — Score: MODERATE

**Tractability: 4/5.** Two coupled Langevin equations with a shared ZPF. Straightforward to code.

**Discriminating power: 2/5.** For linear coupling, SED is expected to agree with QM (this is essentially the van der Waals result, which is already known to work). The interesting case would be nonlinear coupling, but that reintroduces the anharmonic oscillator problem in a more complex setting.

**Novelty: 3/5.** The van der Waals result is known. The interesting question (Bell correlations) is intractable.

---

## Part 3: Recommendation

### Primary Recommendation: Anharmonic Oscillator Ground State Energy

#### What to compute
**Ground state energy of the quartic anharmonic oscillator V(x) = ½mω₀²x² + βx⁴ in SED, to second order in β and beyond.**

Specifically:
1. Solve the SED Langevin equation: ẍ = -ω₀²x - 4βx³/m - Γẋ + (e/m)E_zpf(t) numerically
2. Collect the equilibrium energy ⟨E⟩_SED as a function of β
3. Compare to the QM perturbation theory result:
   - E₀(QM) = ½ℏω₀ + ¾(ℏ/mω₀)β − (21/8)(ℏ²/m²ω₀³)β² + O(β³)
   - (In natural units m=1, ω₀=1, ℏ=1: E₀ = 0.5 + 0.75β − 2.625β² + ...)
4. Verify agreement at O(β) and quantify discrepancy at O(β²)
5. Extend to moderate β values (beyond perturbation theory) to map the full divergence

#### What the QM comparison value is
The quantum mechanical ground state energy of V(x) = ½x² + βx⁴ is extremely well-known. For small β:
- E₀ = 0.5 + 0.75β − 2.625β² + 9.1875β³ − ... (perturbation theory)
- For moderate β, exact numerical diagonalization gives:
  - β = 0.1: E₀ ≈ 0.5592
  - β = 1.0: E₀ ≈ 0.8038 (known to many decimal places)
  - β = 10: E₀ ≈ 1.5076

These are textbook values, available from standard QM calculations (Bender & Wu 1969, many others).

#### Why this is the best use of our exploration budget
1. **Maximally leverages existing infrastructure.** The harmonic oscillator SED code from Exploration 001 needs only a single modification: adding -4βx³/m to the force.
2. **Known analytic prediction to check against.** Pesquera & Claverie (1982) proved analytically that SED and QM disagree at O(β²). We can verify this independently.
3. **Clean, quantitative result.** The output is a single number (⟨E⟩_SED(β)) compared to a known number (E₀_QM(β)). The discrepancy can be stated with arbitrary precision.
4. **Tests the central hypothesis.** The deepest question about SED is whether it only works for linear systems. The anharmonic oscillator is the *minimal nonlinear extension* — if SED fails here, it fails for all nonlinear potentials including hydrogen.
5. **Publication potential.** A numerical verification of Pesquera & Claverie (1982) — 40+ years later, using modern computational methods — would be a legitimate, citable result.
6. **Extends beyond perturbation theory.** For large β, the analytic perturbative result breaks down. Our simulation can map the full SED vs. QM divergence across all β values.

#### Likely outcome
SED will agree with QM at leading order in β (first-order perturbation theory) but will diverge at second order and beyond. The discrepancy will grow with β. At large β (strong anharmonicity), the SED energy will likely be qualitatively different from QM. This would be a clean demonstration of SED's "linearity boundary."

### Secondary Recommendation: SED Tunneling Rate

If the anharmonic oscillator proves intractable or the result is trivial:

#### What to compute
**Barrier-crossing rate for a particle in V(x) = V₀(1 - (x/a)²)² (double-well potential) driven by SED zero-point noise, compared to the WKB tunneling rate.**

#### Why it's the second choice
- Higher novelty (no one has computed this in SED)
- Higher risk (no analytic prediction to guide expectations)
- More complex computationally (rare events, long simulations)
- Less certain to produce a clean SED ≠ QM result

The anharmonic oscillator is the safer, more informative choice. Tunneling is the more adventurous but potentially more spectacular choice.

---

## Summary of Key Findings

### SED Scorecard

| System | Status | References |
|--------|--------|------------|
| Harmonic oscillator ground state | ✅ SED = QM | Marshall 1963, Boyer 1975 |
| Casimir effect | ✅ SED = QM | Boyer 1973 |
| Van der Waals forces | ✅ SED = QM | Boyer 1973 |
| Blackbody spectrum | ✅ SED = QM | Boyer 1969, Marshall 1965 |
| Diamagnetism | ✅ SED = QM | (follows from HO) |
| Specific heats | ✅ SED = QM | (follows from HO) |
| **Anharmonic oscillator** | ❌ SED ≠ QM at O(β²) | Pesquera & Claverie 1982 |
| **Hydrogen atom** | ❌ Self-ionizes | Nieuwenhuizen & Liska 2015, Nieuwenhuizen 2020 |
| **Quantum coherence** | ❌ No interference | Huang & Batelaan 2019 |
| **Excited states** | ❌ No discrete spectrum | Boyer 2019 review |
| Bell inequality violation | ⚡ Contested | Marshall & Santos, Santos 2020 |
| g-2 anomalous moment | ❓ SEDS claims (non-standard) | Cavalleri et al. 2010 |
| Lamb shift | ❓ Partial results | Boyer 1988, Cavalleri et al. |
| Tunneling | ❓ Not computed | — |

### The Pattern

SED succeeds when and only when:
1. The system is **linear** (harmonic oscillator or free field)
2. The calculation involves only **equilibrium properties** (ground state, not excited states)
3. No **quantum coherence** or **interference** is involved

Every extension to nonlinear potentials, excited states, or interference phenomena has failed. This is the "linearity boundary" of SED.

---

## References (Complete)

1. Boyer, T.H. (1969). "Derivation of the Blackbody Radiation Spectrum without Quantum Assumptions." Phys. Rev. 182, 1374.
2. Boyer, T.H. (1973). "Retarded van der Waals forces at all distances derived from classical electrodynamics with classical electromagnetic zero-point radiation." Phys. Rev. A 7, 1832.
3. Boyer, T.H. (1975). "Random electrodynamics: The theory of classical electrodynamics with classical electromagnetic zero-point radiation." Phys. Rev. D 11, 790.
4. Boyer, T.H. (1984). "Einstein-Hopf drag on an anharmonic oscillator." Phys. Rev. D 29, 648.
5. Boyer, T.H. (1988). "Environmental effects on the Lamb shift according to stochastic electrodynamics." Phys. Rev. A 37, 1952.
6. Boyer, T.H. (2019). "Stochastic Electrodynamics: The Closest Classical Approximation to Quantum Theory." Atoms 7(1), 29. [arXiv:1903.00996]
7. Cavalleri, G., Bosi, L., Barbero, F., et al. (2010). "A quantitative assessment of stochastic electrodynamics with spin (SEDS)." Frontiers of Physics in China 5, 107–122.
8. Cole, D.C. & Zou, Y. (2003). "Quantum Mechanical Ground State of Hydrogen Obtained from Classical Electrodynamics." Phys. Lett. A 317, 14–20. [arXiv:quant-ph/0307154]
9. Cole, D.C. & Zou, Y. (2004). "Simulation Study of Aspects of the Classical Hydrogen Atom: Elliptical Orbits." J. Scientific Computing 20, 379–404.
10. de la Peña, L. & Cetto, A.M. (1981). "The spin and the anomalous magnetic moment of the electron in stochastic electrodynamics." Phys. Lett. A 81, 441.
11. de la Peña, L., Valdés-Hernández, A. & Cetto, A.M. (2010). "Entanglement of particles through coupling via the common background zero-point radiation field." Physica E 42, 308–312.
12. Huang, W.C.-W. & Batelaan, H. (2019). "Testing Quantum Coherence in Stochastic Electrodynamics with Squeezed Schrödinger Cat States." Atoms 7(2), 42. [arXiv:2011.12910]
13. Marshall, T.W. (1963). "Random Electrodynamics." Proc. R. Soc. A 276, 475.
14. Marshall, T.W. & Santos, E. (1989). "Stochastic optics: A local realistic analysis of optical tests of Bell inequalities." Phys. Rev. A 39, 6271.
15. Nieuwenhuizen, T.M. & Liska, M.T.P. (2015). "Simulation of the hydrogen ground state in Stochastic Electrodynamics." Physica Scripta T165, 014006. [arXiv:1502.06856]
16. Nieuwenhuizen, T.M. & Liska, M.T.P. (2015). "Simulation of the hydrogen ground state in SED-2: Inclusion of Relativistic Corrections." Found. Phys. 45, 1190–1202. [arXiv:1506.06787]
17. Nieuwenhuizen, T.M. (2020). "Stochastic Electrodynamics: Renormalized Noise in the Hydrogen Ground-State Problem." Front. Phys. 8, 335.
18. Pesquera, L. & Claverie, P. (1982). "The quartic anharmonic oscillator in stochastic electrodynamics." J. Math. Phys. 23(7), 1315–1322.
19. Santos, E. (2020). "Local Model of Entangled Photon Experiments Compatible with Quantum Predictions Based on the Reality of the Vacuum Fields." Found. Phys. 50, 1587–1607.
20. Schafaschek, D.F., Vasconcelos, G.L. & Macêdo, A.M.S. (2024). "Tunneling in double-well potentials within Nelson's stochastic mechanics." [arXiv:2512.16168]
