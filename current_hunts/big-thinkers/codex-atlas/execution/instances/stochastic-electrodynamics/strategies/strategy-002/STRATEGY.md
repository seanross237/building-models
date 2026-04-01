# Strategy 002 — Frontier Mapping and the Minimal Modification Question

## Objective

Map the SED–QM boundary across multiple independent systems, then synthesize: **What is the minimal modification to SED that would recover full QM predictions?**

Strategy-001 found one precise failure point (anharmonic oscillator, ~15-18% ALD residual at β=1.0). But one data point on the frontier doesn't reveal the *shape* of the frontier. This strategy attacks 2-3 new systems to identify whether the failures share a common root cause, then asks what the simplest fix would be. The mission explicitly requests this: "Identify the minimal modification to SED that would recover full QM predictions, if pure SED fails."

The deliverable is either (a) a concrete minimal modification with evidence that it works, or (b) a proof that no simple modification exists, because different failures require different fixes. Either is a strong Tier 4 finding.

## Methodology

### Phase 1: Rapid Probes (3 explorations, run in parallel where possible)

Launch 2-3 focused computational explorations, each targeting a different system where SED's predictions are unknown or contested. Each probe should be SHORT — compute one quantitative comparison and report the result. Don't try to fully characterize the failure; just determine *whether* SED fails and *by how much*.

**Probe A — SED Tunneling (Double-Well Potential):**
Simulate a particle in V(x) = -½ω₀²x² + ¼λx⁴ (double-well) driven by SED zero-point noise. Measure the barrier-crossing rate. Compare to the WKB tunneling rate for the same potential. This is completely novel — nobody has computed tunneling in SED.

Key computational details:
- Use the ALD (Landau-Lifshitz order reduction), NOT the Langevin approximation. Strategy-001 proved the Langevin approximation fails at O(β) for any nonlinearity.
- The ZPF noise spectrum is S_F(ω) = 2τℏω³/m per unit bandwidth. The FFT amplitude for colored noise with PSD S(ω) is A_k = sqrt(S(ω_k) × N / (2×dt)). These are verified formulas from Strategy-001.
- Focus on POSITION-based observables. The velocity variance is UV-divergent (known SED feature, not a bug).
- Run parameter regimes sequentially, not all at once.
- Include a β=0 (single-well harmonic limit) sanity check.

**Probe B — Two Coupled Oscillators (Entanglement Test):**
Simulate two harmonic oscillators coupled through the shared ZPF (both immersed in the same zero-point radiation field). Compute the position-position correlation ⟨x₁x₂⟩ and the momentum-momentum correlation ⟨p₁p₂⟩. Compare to the QM ground state correlations for the same system.

The key question: does the shared classical ZPF produce correlations that look like quantum entanglement? If the correlations factorize (⟨x₁x₂⟩ = ⟨x₁⟩⟨x₂⟩), SED fails at entanglement. If they don't factorize, SED might have more structure than expected.

Key details:
- Use two spatially separated oscillators with the SAME ZPF realization (same random field, evaluated at different positions).
- Also compute the Bell-CHSH parameter S from the correlations. QM gives S up to 2√2 ≈ 2.83 for entangled states; local hidden variable theories give S ≤ 2.
- Keep oscillators far enough apart that retardation matters (d ≫ c/ω₀) to test whether the causal structure of the ZPF limits correlations.
- Noise normalization: same as above.

**Probe C — Hydrogen Circular Orbits (Controlled Attempt):**
Strategy-001's literature survey (E002) flagged hydrogen as "effectively closed" due to self-ionization (Nieuwenhuizen & Liska 2015). But Cole & Zou (2003) reported stable orbits in 3D SED hydrogen simulations. The contradiction is unresolved.

Run a SHORT, targeted computation: simulate a classical electron in a Coulomb potential plus SED noise for just the circular orbit case (L = nℏ). Measure the time to self-ionization and the mean orbital radius. Compare to Bohr radius. Don't try to get the full spectrum — just determine whether the ground state is stable and for how long.

If the electron self-ionizes in < 10⁴ orbital periods, report this as a clean negative result. If it's stable, measure the mean energy and compare to -13.6 eV.

Key details:
- Use 3D simulation (hydrogen is not a 1D problem).
- Include radiation reaction (ALD).
- Use adaptive timestep (Coulomb singularity demands small dt near nucleus).
- Cap simulation at a reasonable time (say 10⁵ orbital periods) to avoid infinite runs.

### Phase 2: Diagnose the Root Cause (1-2 explorations)

After Phase 1, evaluate the probe results. The Strategizer should ask: **Do the failures in different systems share a common root cause?**

Possible patterns:
- All failures trace to SED's ω³ spectral density creating energy-nonconservation in nonlinear potentials → the root cause is the mismatch between the ZPF spectrum and the actual system dynamics.
- Coupled oscillator correlations are too weak → the root cause is that a classical field can't produce entanglement-like correlations (Bell theorem in action).
- Hydrogen self-ionizes → the root cause is that SED can't confine particles in 1/r potentials (energy absorption without bound-state selection rules).

Design 1-2 explorations that test the common-root-cause hypothesis. If the failures are related, one modification might fix them all. If they're independent, the "minimal modification" is not minimal — it's QM itself.

**If failures share a root cause**, design an exploration that:
1. States the proposed modification precisely (e.g., "replace the ω³ spectral density with a system-dependent density that self-consistently satisfies detailed balance").
2. Computes whether the modification fixes the anharmonic oscillator failure from Strategy-001.
3. Checks whether the modification preserves the known SED successes (harmonic oscillator, Casimir).

**If failures are independent**, design an exploration that:
1. Catalogs the distinct failure mechanisms.
2. Asks whether the failures correspond to known quantum features (nonlinearity → interference, multi-particle → entanglement, 1/r → bound-state quantization).
3. Argues whether these are one problem or irreducibly many.

### Phase 3: Adversarial Synthesis (1 exploration)

Take the best findings from Phases 1-2 and subject them to adversarial review:
- Search the literature for prior work on SED modifications (Boyer has some, de la Peña & Cetto have others).
- Test whether our proposed modification (or impossibility argument) is genuinely new.
- Identify the strongest objections a physicist would raise.
- Connect the findings to the broader question: "Is field quantization necessary, or is it an emergent consequence of classical electrodynamics plus the zero-point field?"

### Cross-Phase Rules

1. **Computation is mandatory.** Every exploration writes and runs code. No exceptions.
2. **Use ALD, not Langevin.** Strategy-001 proved the Langevin approximation fails at O(β) for any nonlinearity. All Phase 1 probes involving nonlinear potentials MUST use the Landau-Lifshitz order reduction.
3. **Pre-load verified formulas.** Every simulation exploration gets: S_F(ω) = 2τℏω³/m, A_k = sqrt(S(ω_k) × N / (2×dt)), and the warning about UV-divergent velocity variance. These are established from Strategy-001.
4. **Report numbers, not vibes.** "SED fails" is not a finding. "SED predicts a barrier-crossing rate of 3.2 × 10⁻⁴ ω₀ vs WKB rate of 1.7 × 10⁻⁷ ω₀, a factor of 1900× too high" is a finding.
5. **Prior art in every exploration.** Web search for prior work on each system in SED.
6. **Run a quick adversarial sanity check after Phase 1** before committing Phase 2 explorations. Don't save all critique for Phase 3.

## Validation Criteria

**Minimum success (Tier 2-3):**
- At least 2 of 3 Phase 1 probes produce quantitative SED–QM comparisons
- The failure modes are characterized (not just "SED fails" but "SED fails because...")
- The results are consistent with Strategy-001's findings

**Good success (Tier 3-4):**
- A common root cause is identified across multiple failure modes
- A minimal modification is proposed and tested on at least one system
- The modification is checked against known SED successes

**Excellent success (Tier 4-5):**
- A minimal modification is found that fixes multiple failures while preserving known successes
- OR a rigorous argument that no simple modification exists (different failures require different fixes)
- The finding is genuinely new — not in Boyer, de la Peña, or Cetto
- Implications for the necessity of field quantization are stated explicitly

## Context from Strategy-001

### Key findings to carry forward:
1. **SED harmonic oscillator works.** var_x = 0.507 vs QM 0.500 (1.4%). Any modification must preserve this.
2. **Langevin approximation fails at O(β) for nonlinear potentials.** Constant damping + ω³ noise → positive feedback. Use ALD instead.
3. **ALD-SED fails at ~15-18% for quartic oscillator at β=1.0.** Residual converges very slowly (τ^0.23 × ω_max^(-0.18)). This is a real failure, not a numerical artifact.
4. **The physical mechanism for Langevin failure is the ω³ positive feedback loop.** Anharmonicity shifts effective frequency up → ω³ ZPF delivers more power → constant damping can't compensate. ALD's position-dependent damping breaks this feedback but doesn't eliminate it entirely.
5. **No prior numerical simulation of anharmonic SED exists.** Pesquera & Claverie (1982) is analytic only.

### Verified computational infrastructure:
- ZPF spectral density: S_F(ω) = 2τℏω³/m
- FFT noise amplitude: A_k = sqrt(S(ω_k) × N / (2×dt))
- Velocity variance is UV-divergent → use position-based observables
- Euler-Cromer integrator with dt=0.05 is adequate for ω₀=1, ω_max=10-30
- ALD (Landau-Lifshitz): ẍ = F(x)/m - τ(ω₀² + V'''/m)ẋ + F_zpf + τF'_zpf

### What was NOT attempted in Strategy-001:
- Multi-particle systems (coupled oscillators, entanglement)
- Tunneling / barrier crossing
- Hydrogen (flagged as difficult but not attempted)
- Any modification to SED itself
- Connections to other programs (pilot-wave, information-theoretic)
- Implications for field quantization necessity

### Computation registry:
- SED tunneling rate (double-well): OPEN, medium priority
- All other Strategy-001 computations: DONE

### Exploration budget: Plan for 5-7 explorations across all phases.
