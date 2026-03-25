# Stability Assessment of the 20 Core Tenets of Physics

Each tenet was independently assessed for: stability rating, known challenges/edge cases, existing reinterpretations, and room for novel reinterpretation relevant to quantum gravity and unification.

---

## 1. Conservation of Energy

### Stability: 9/10 locally; 6/10 globally in curved spacetime

### Known Challenges
- **Cosmological expansion**: Photons redshift and lose energy as the universe expands. There is no compensating "energy of the gravitational field" that is well-defined in a coordinate-invariant way. Sean Carroll (Caltech) has stated plainly: "Energy is not conserved in general relativity."
- **Pseudo-tensors**: Einstein, Landau-Lifshitz, and others constructed gravitational energy-momentum pseudo-tensors, but these are coordinate-dependent — not true tensors — making their physical meaning contested (Misner, Thorne & Wheeler, *Gravitation*, 1973).
- **ADM and Bondi energy**: For asymptotically flat spacetimes, ADM energy (1962) and Bondi energy (1962) are well-defined and conserved. But our actual universe (de Sitter-like) is not asymptotically flat.
- **Quantum mechanics**: The energy-time uncertainty relation permits transient violations (virtual particles, vacuum fluctuations), though energy is conserved in expectation values and in S-matrix amplitudes.

### Reinterpretations
- Padmanabhan and others have explored thermodynamic/emergent gravity framings where energy conservation is replaced by holographic entropy bounds.
- Erik Verlinde (*On the Origin of Gravity and the Laws of Newton*, 2011): gravity as an entropic force sidesteps the standard energy-conservation framing entirely.
- Barbour, Koslowski & Mercati (Shape Dynamics program): reformulate GR with a different symmetry group, trading refoliation invariance for spatial conformal invariance, which alters what "energy" means globally.

### Reinterpretation Potential: HIGH
The absence of a well-defined global energy in GR is not a settled philosophical matter; it is an active technical gap. A framework that either derives an exact conservation law from a deeper symmetry applicable to de Sitter spacetimes, or demonstrates that energy conservation is emergent rather than fundamental, could have significant implications for quantum gravity.

---

## 2. Conservation of Momentum

### Stability: 9.5/10

### Known Challenges
- **Curved spacetime (GR)**: Global momentum conservation breaks down in GR. No global translational symmetry means no well-defined global conserved momentum (Misner, Thorne & Wheeler, 1973). Local conservation (covariant divergence of stress-energy tensor = 0) still holds but does not integrate to a global quantity in general.
- **Cosmology**: In expanding spacetime (FLRW metric), photon redshift means individual photon momentum is not conserved. No global space-translation Killing vector exists (Peebles, *Principles of Physical Cosmology*, 1993).
- **Anomalies**: Translational symmetry has no known quantum anomaly. Momentum conservation is anomaly-free.

### Reinterpretations
- **Relational Mechanics (Barbour)**: Momentum conservation recast as a constraint on relational configurations, not an absolute statement about space.
- **Emergent Spacetime (Verlinde, Padmanabhan)**: If spacetime is emergent, Noether-derived conservation laws are themselves emergent, not fundamental. Momentum conservation becomes approximate.
- **Doubly Special Relativity (Amelino-Camelia, 2001; Magueijo & Smolin, 2002)**: Conservation holds, but the momentum composition law becomes nonlinear at Planck scale.

### Reinterpretation Potential: MODERATE
The absence of global momentum conservation in GR, combined with its exact enforcement in QFT, is a genuine tension. A novel framing of momentum as a derived, scale-dependent, or relational quantity could provide traction on unification.

---

## 3. Conservation of Angular Momentum

### Stability: 9.5/10

### Known Challenges
- **Curved spacetime (GR)**: Angular momentum is difficult to define globally; well-defined only for asymptotically flat spacetimes (ADM and Bondi-Sachs formalisms). The Komar integral provides a conserved quantity only when a rotational Killing vector exists.
- **Galaxy angular momentum problem**: N-body simulations historically over/underpredict disk galaxy angular momentum ("angular momentum catastrophe," Navarro & Benz 1991). This is a modeling problem, not a fundamental violation.
- **Chiral anomalies in QFT**: Axial currents are not conserved (Adler-Bell-Jackiw anomaly), demonstrating that classical conservation laws can be broken by quantization.

### Reinterpretations
- **Einstein-Cartan theory**: Intrinsic spin couples to spacetime torsion rather than curvature (Kibble 1961, Sciama 1964).
- **Loop Quantum Gravity**: Angular momentum quantized via SU(2) spin networks. Discrete spectrum of area/volume operators (Rovelli & Smolin, 1995) reframes angular momentum as fundamentally combinatorial.
- **Twistor theory (Penrose, 1967)**: Angular momentum encoded in holomorphic structure of twistor space, unified with linear momentum in a projective geometric framework.
- **BMS group / asymptotic symmetries (Strominger, 2014-2017)**: Angular momentum conservation at null infinity is richer than previously understood, connecting to soft graviton theorems and the memory effect.

### Reinterpretation Potential: MODERATE
A reinterpretation unifying the BMS/asymptotic symmetry perspective with spin-network quantization remains an open and fertile direction — deepening conservation rather than breaking it.

---

## 4. Principle of Least Action

### Stability: 9/10 (as meta-framework)

### Known Challenges
- **Dissipative and open systems**: Friction, viscosity, and heat conduction lack straightforward action formulations. Workarounds exist (Galley's doubled-variable formalism, *Phys. Rev. Lett.* 110, 2013) but are not natural.
- **Quantum mechanics**: Feynman's path integral sums over *all* paths, not just extremal ones. The classical action principle emerges only in the stationary-phase (ℏ → 0) limit. The quantum reality is a democratic sum, not an extremization.
- **Causal structure in GR**: In Lorentzian signature the extremum is a saddle point, not a minimum — "least" action is a misnomer. The Gibbons-Hawking-York boundary term must be carefully added.
- **Discrete/combinatorial approaches**: Causal set theory (Sorkin) and lattice gravity approaches struggle to define a smooth action.

### Reinterpretations
- **Feynman (1948)**: Action as the phase weighting all paths, not a selection rule.
- **Schwinger's quantum action principle (1951)**: Variational principle directly at the quantum operator level.
- **Constructor theory (Deutsch & Marletto, 2015)**: Reformulates physics in terms of possible/impossible transformations, sidestepping action entirely.
- **Noncommutative geometry spectral action (Chamseddine & Connes, 1997)**: The entire Standard Model + gravity action emerges from the spectrum of a Dirac operator.

### Reinterpretation Potential: HIGH
The action principle presupposes a smooth differentiable manifold, a fixed causal structure, and a well-defined notion of "path" — all of which break down in quantum gravity. Replacing extremization with an information-theoretic or entropic selection principle, or deriving the action principle as emergent from deeper combinatorial/algebraic structure, are promising frontiers.

---

## 5. Noether's Theorem

### Stability: 10/10 (as mathematical theorem, within its domain)

### Known Challenges
- **GR / Cosmology**: In an expanding FRW spacetime, time-translation symmetry is absent. Noether's theorem still holds — the symmetry simply isn't present, so no conserved energy exists.
- **Noether's second theorem**: Local gauge symmetries yield identities (Bianchi identities) rather than conserved currents. This distinction (Brading and Brown, 2003) is frequently conflated with the first theorem.
- **Quantum anomalies**: Classical symmetries can fail to survive quantization (chiral anomaly, Adler 1969; Bell & Jackiw 1969).
- **Discrete symmetries**: The theorem applies only to continuous symmetries. CPT, parity, etc. fall outside its scope.

### Reinterpretations
- **Wald (1993) and Iyer-Wald (1994)**: Reformulated Noether charges for diffeomorphism-invariant theories, yielding black hole entropy as a Noether charge.
- **Covariant phase space methods (Crnkovic & Witten, 1987)**: Extended Noether's framework to field theories on arbitrary backgrounds.
- **Categorical / homotopy-theoretic framings (Schreiber et al.)**: Recast Noether's theorem in higher gauge theory using infinity-toposes, generalizing to extended field theories relevant to string theory.

### Reinterpretation Potential: HIGH
The opportunity lies in generalizing the theorem's logic beyond classical Lagrangian mechanics — Noether-like correspondences for approximate or emergent symmetries in quantum gravity, and a deeper Noether-type theorem linking information-theoretic symmetries to conserved quantities (cf. Harlow 2016 on bulk symmetries and boundary superselection in AdS/CFT).

---

## 6. Constancy of the Speed of Light

### Stability: 9/10

### Known Challenges
- **Variable Speed of Light (VSL) cosmologies**: Magueijo and Albrecht (1999) proposed c may have been larger in the early universe, offering an alternative to inflation.
- **Doubly Special Relativity (DSR)**: Amelino-Camelia (2001), Magueijo & Smolin (2002) — preserve c as invariant but introduce a second invariant scale (Planck energy), making dispersion relations energy-dependent.
- **Quantum gravity dispersion**: Loop quantum gravity and some string scenarios predict Planck-scale corrections to photon propagation. Fermi telescope observations constrain linear corrections but quadratic corrections remain viable.
- **Lorentz invariance violation**: The Standard Model Extension (Kostelecky et al.) parameterizes all possible LIV terms. Bounds are extraordinarily tight but finite.

### Reinterpretations
- c as a **conversion factor** between space and time rather than a "speed" (Minkowski geometric view, modernized by Dray and Manogue).
- c as an **emergent thermodynamic quantity** (Jacobson's 1995 derivation of Einstein's equations from thermodynamics).
- c as a **renormalization group fixed point**, exact only in the infrared limit (explored in Horava gravity).

### Reinterpretation Potential: HIGH
If c is reframed as a fundamental bound on causal information transfer that emerges from deeper quantum-gravitational structure, this could open productive avenues. The theoretical space between "exact" and "emergent" symmetry remains genuinely open.

---

## 7. Equivalence Principle

### Stability: 9/10 experimentally; theoretically expected to break

### Known Challenges
- **String theory dilaton couplings**: Damour and Polyakov (1994) showed light scalar fields produce composition-dependent WEP violations potentially detectable at 10^-18.
- **MICROSCOPE satellite** (Touboul et al., 2022): Constrained WEP violations to ~10^-15. No violation found.
- **Quantum superposition + gravity**: The interplay of superposition and gravitation remains unresolved (Penrose, Page-Geilker).
- **Self-energy corrections (Nordtvedt effect)**: Bodies with significant gravitational self-energy could violate the Strong EP.

### Reinterpretations
- **Jacobson (1995)**: Derived Einstein's equations as thermodynamic equation of state — EP becomes a statement about local thermal equilibrium of spacetime.
- **Verlinde (2011)**: Entropic gravity — EP is emergent from information-theoretic considerations.
- **Giacomini, Castro-Ruiz & Brukner (2019)**: Quantum reference frames reformulate the EP for quantum systems in superposition of gravitational fields.

### Reinterpretation Potential: VERY HIGH
The EP sits precisely at the junction where GR meets QM. Grounding it in quantum information or entanglement structure (ER=EPR conjecture) is a live and promising research direction. Planned experiments (AEDGE, STE-QUEST) targeting 10^-17 to 10^-18 could detect string-theoretic violations.

---

## 8. Lorentz Invariance

### Stability: 9.5/10

### Known Challenges
- **Loop quantum gravity**: Generically produces modified dispersion relations where photon speed becomes energy-dependent (Gambini & Pullin, 1999).
- **Standard Model Extension (SME)**: Colladay & Kostelecky (1998) — comprehensive EFT framework for all possible LIV operators. No violations found.
- **Horava-Lifshitz gravity**: Explicitly breaks Lorentz invariance at high energies while recovering it at low energies, trading the symmetry for power-counting renormalizability.
- **Very Special Relativity**: Cohen and Glashow (2006) showed a proper subgroup SIM(2) suffices to reproduce observed physics.

### Reinterpretations
- **Emergent Lorentz symmetry**: Volovik (*The Universe in a Helium Droplet*, 2003) treats Lorentz invariance as emergent from a deeper non-relativistic substrate.
- **Deformed symmetries**: Kappa-Poincare algebra (Lukierski, Nowicki, Ruegg, 1991) deforms rather than breaks the symmetry.
- **Causal set theory**: Sorkin et al. maintain exact Lorentz invariance by construction as a selection principle for discrete spacetime.

### Reinterpretation Potential: HIGH
The tension between discrete spacetime (suggested by black hole entropy, holographic principle) and exact Lorentz invariance (requiring a continuum) remains unresolved. Explaining how a discrete substrate gives rise to continuous Lorentz symmetry would be a genuine advance.

---

## 9. Mass-Energy Equivalence (E = mc²)

### Stability: 9.5/10

### Known Challenges
- **Binding energy / mass defect**: Mass is not additive — the mass of composites differs from constituent sum by binding energy/c² (Okun, *Physics Today*, 1989).
- **Gravitational context**: In GR, global energy is ill-defined in non-asymptotically-flat spacetimes. No universal local gravitational field energy density exists.
- **Cosmological constant problem**: The ~120 orders-of-magnitude discrepancy between QFT vacuum energy and observed dark energy raises the question of whether all energy gravitates as E = mc² implies (Weinberg, 1989).

### Reinterpretations
- **Emergent mass ("mass without mass")**: ~99% of proton mass arises from QCD binding energy, not quark rest masses (Wilczek, 1999).
- **Entropic/emergent gravity**: Verlinde (2011), Padmanabhan (2010) recast mass-energy as an entropy-gradient quantity.
- **Non-commutative geometry corrections**: Amelino-Camelia (2001) — modified dispersion relations at Planck energies.

### Reinterpretation Potential: MODERATE
The relation itself is unlikely to break, but its scope conditions — precisely when and how energy sources gravitate — remain the deepest open question (cosmological constant problem).

---

## 10. General Covariance

### Stability: 9/10 empirically; conceptually contested

### Known Challenges
- **Kretschmer objection (1917)**: Any theory can be written in generally covariant form, raising whether the principle has genuine physical content beyond diffeomorphism invariance.
- **Background dependence in string theory**: Perturbative string theory requires a fixed background spacetime, explicitly breaking background independence (Smolin, 2006).
- **Problem of time**: In canonical quantum gravity (Wheeler-DeWitt equation), the Hamiltonian constraint generates gauge transformations rather than physical time evolution (Isham 1993, Kuchar 1992).
- **Hole argument**: Einstein's hole argument (revived by Earman & Norton, 1987) forces interpretive choices about spacetime point ontology.

### Reinterpretations
- **Rovelli's relational interpretation**: Physical content lies in diffeomorphism-invariant relational observables only.
- **Anderson (1967)**: General covariance as gauge redundancy — the real content is the absence of absolute objects.
- **ER=EPR (Maldacena & Susskind, 2013)**: Smooth manifold structure may emerge from entanglement.

### Reinterpretation Potential: VERY HIGH
This principle sits at the exact fault line between GR and QM. Any successful quantum gravity theory must clarify what general covariance means when the manifold itself is subject to quantum fluctuations.

---

## 11. Quantization

### Stability: 9/10 empirically; 7/10 ontologically

### Known Challenges
- **Spacetime quantization unresolved**: No experimental evidence spacetime is discrete. LQG predicts discrete area/volume spectra; string theory operates on continuous background. Planck scale remains experimentally inaccessible.
- **QFT subtlety**: The quantum field itself is continuous; only its excitations (particles) are quantized.
- **Unruh and Hawking effects**: The particle concept is observer-dependent — undermining naive quantization ontology.

### Reinterpretations
- **'t Hooft's deterministic QM**: Quantum discreteness emerges from deterministic underpinning at Planck scale (arXiv:1405.1548).
- **Stochastic quantization (Parisi-Wu)**: QM reproduced via stochastic processes in fictitious extra time dimension.
- **Adler's trace dynamics**: QM as thermodynamic approximation of underlying classical matrix dynamics (2004).
- **Hardy's axioms**: Deriving quantum theory from five reasonable axioms (arXiv:quant-ph/0101012).

### Reinterpretation Potential: VERY HIGH
If quantization is emergent rather than axiomatic, quantum gravity may not require "quantizing gravity" at all — inverting the standard program. The question "why quanta?" remains one of the deepest open problems. Deriving Planck's constant from something more primitive would be a major breakthrough.

---

## 12. Heisenberg Uncertainty Principle

### Stability: 10/10 (mathematical theorem within QM)

### Known Challenges
- **Measurement vs. preparation**: Heisenberg's original noise-disturbance relation is formally incorrect. Ozawa (2003) proved a corrected version, experimentally confirmed by Erhart et al. (2012, Nature Physics).
- **Generalized Uncertainty Principle (GUP)**: In quantum gravity, a minimum length modifies the relation: ΔxΔp ≥ (ℏ/2)[1 + β(Δp)² + ...]. Arises in string theory (Veneziano 1986), LQG, and black hole thought experiments. The GUP strengthens the bound.
- **Entropic uncertainty relations**: Deutsch (1983), Maassen-Uffink (1988) — reformulated in information-theoretic terms. Berta et al. (2010) showed quantum entanglement with a memory system can reduce entropic uncertainty.

### Reinterpretations
- **Relational QM (Rovelli)**: Uncertainty reflects the relational nature of physical quantities.
- **QBism (Fuchs, Schack)**: Uncertainty as a constraint on rational betting odds.
- **Thermal/emergent approaches**: If spacetime is emergent, uncertainty may be downstream of deeper thermodynamic constraints.

### Reinterpretation Potential: MODERATE
The GUP remains semi-phenomenological — no universally accepted first-principles derivation. Connecting the modified commutator to specific quantum-gravitational microstructure, or linking quantum memory terms to horizon entanglement entropy, could bridge uncertainty and holographic bounds.

---

## 13. Superposition Principle

### Stability: 9.5/10

### Known Challenges
- **Gravitational decoherence (Penrose 1996, Diosi 1987)**: Superpositions of states with sufficiently different mass-energy distributions may collapse on a timescale inversely related to gravitational self-energy difference. MAQRO and TEQ satellite proposals aim to test this.
- **Spontaneous collapse models (GRW 1986, CSL by Pearle 1989)**: Modify Schrodinger equation with nonlinear stochastic term. Current X-ray emission bounds (Donadi et al., Nature Physics, 2021) constrain but don't fully rule out all parameter space.
- **Superselection rules**: Certain superpositions are physically forbidden in QFT — e.g., superpositions of different electric charge (Wick-Wightman-Wigner, 1952).

### Reinterpretations
- **Everett (1957)**: Superposition never collapses; all branches are real.
- **QBism**: Superposition reflects an agent's information, not ontological fact.
- **Relational QM (Rovelli, 1996)**: States defined only relative to an observer-system.
- **'t Hooft**: Superposition emerges from underlying deterministic ontology at Planck scale.

### Reinterpretation Potential: HIGH
If quantum gravity demands a non-linear, non-Hilbert-space structure — as hinted by the black hole information paradox and holographic bounds — superposition may be an emergent, approximate principle valid only below Planck-scale curvatures.

---

## 14. The Born Rule

### Stability: 10/10 empirically; foundationally unresolved

### Known Challenges
- **Derivation problem**: The Born Rule is the only QM postulate that resists clean derivation from deeper principles.
  - Gleason's theorem (1957): Proves |ψ|² is unique probability measure on Hilbert spaces dim ≥ 3, but assumes the framework it justifies.
  - Deutsch-Wallace decision-theoretic derivation: Criticized as circular (Kent, Albert).
  - Zurek's envariance (2005): Elegant but contested on hidden assumptions.
- **Quantum gravity**: The rule presupposes a fixed Hilbert space and clean observable-state distinction. No natural formulation in the Wheeler-DeWitt equation or wave function of the universe.
- **Sorkin's quantum measure theory**: Generalizes QM to allow third-order interference (violating Born Rule). No experimental violations found (Sinha et al., 2010), but framework remains open.

### Reinterpretations
- **Everett/Many-Worlds**: The rule becomes a statement about branch weights, not objective probability.
- **QBism**: |ψ|² reflects agent's rational degrees of belief, not objective frequencies.
- **Pilot-wave theory (Valentini, 1991)**: |ψ|² emerges as equilibrium distribution. Non-equilibrium deviations are a genuine theoretical crack.

### Reinterpretation Potential: VERY HIGH
The Born Rule sits at the seam between unitary evolution and measurement — the same seam where QM meets gravity. Deriving it from information geometry, thermodynamic constraints on spacetime, or algebraic structure of observables in background-independent theories would simultaneously illuminate the measurement problem and constrain quantum gravity.

---

## 15. Pauli Exclusion Principle

### Stability: 9.5/10

### Known Challenges
- **Anyons (2D systems)**: In 2D, particles can obey fractional statistics (Leinaas & Myrheim, 1977; Wilczek, 1982). Experimentally confirmed in fractional quantum Hall systems (Bartolomei et al., 2020). Dimension-dependent, not a violation.
- **Parastatistics**: Green (1953), Greenberg (1964) — frameworks allowing partial violations. Experimentally excluded to extraordinary precision (VIP-2 experiment, bounds at ~10^-29).
- **Extreme gravity**: Near singularities or Planck-scale densities, the spin-statistics theorem's status is uncertain because QFT on curved spacetime is incomplete.

### Reinterpretations
- **Topological framing**: Spin-statistics connection recast in terms of topology of configuration spaces (Finkelstein & Rubinstein, 1968; Berry & Robbins, 1997).
- **Greenberg (2002)**: Even small PEP violations would imply CPT or Lorentz violation, tying PEP integrity to spacetime symmetry.
- **Information-theoretic approaches**: Kaplan (2013) explored whether PEP emerges from deeper information constraints.

### Reinterpretation Potential: MODERATE
The spin-statistics theorem assumes smooth, fixed-topology spacetime. If topology fluctuates (quantum gravity), or if early universe physics is effectively 2D (Carlip 2017 — spectral dimension results), anyonic statistics could play a foundational role.

---

## 16. Wave-Particle Duality

### Stability: OBSOLETE as ontology; solid as pedagogy

### Known Challenges
- **QFT dissolution**: Weinberg, Schwinger et al. — there are neither waves nor particles in the classical sense. There are quantum fields and their excitations. Duality is an artifact of forcing quantum objects into classical categories.
- **Unruh effect**: Whether an observer detects "particles" depends on their acceleration — particle number is observer-dependent.
- **Englert's duality relation (1996)**: Replaced vague complementarity with rigorous inequality D² + V² ≤ 1. No "wave" or "particle" language needed.

### Reinterpretations
- **Bohmian mechanics**: Particles are always particles, guided by a pilot wave. Duality eliminated by construction.
- **Relational QM (Rovelli)**: Properties are relational; "wave" and "particle" are descriptions relative to interaction context.
- **Decoherence program (Zurek)**: Classical appearance emerges from environmental entanglement, not fundamental duality.

### Reinterpretation Potential: HIGH (by discarding it)
The productive move is to discard the duality entirely in favor of pre-geometric or algebraic quantum structures. Relevant to the amplituhedron program (Arkani-Hamed), Connes' noncommutative geometry, and it-from-qubit approaches (Susskind, Van Raamsdonk).

---

## 17. Second Law of Thermodynamics

### Stability: 9/10 (statistical, not fundamental)

### Known Challenges
- **Loschmidt's Paradox (1876)**: Microscopic laws are time-reversal invariant. The Second Law depends on the Past Hypothesis — a low-entropy initial state of the universe. This remains unexplained.
- **Fluctuation Theorems (Evans et al. 1993; Jarzynski 1997; Crooks 1999)**: Rigorously quantify transient entropy-decreasing fluctuations in small systems. Experimentally confirmed (Wang et al., 2002).
- **Black Hole Information Paradox (Hawking, 1976)**: If information is destroyed in black hole evaporation, entropy accounting breaks. Current consensus favors information preservation (island/replica wormhole calculations, Penington et al. 2019-2020), but mechanism is debated.
- **Poincare Recurrence**: Any finite bounded classical system will eventually return near its initial state, implying entropy must eventually decrease.

### Reinterpretations
- **Information-theoretic (Jaynes, 1957)**: Entropy as observer ignorance via maximum entropy inference, not objective property.
- **Penrose's Weyl Curvature Hypothesis**: Ties low initial entropy to Big Bang smoothness.
- **Carroll and Chen (2004)**: Entropy can increase in both temporal directions from a low-entropy fluctuation.
- **Eigenstate Thermalization Hypothesis (Deutsch 1991, Srednicki 1994)**: Derives thermodynamic behavior from quantum mechanics of individual eigenstates.

### Reinterpretation Potential: VERY HIGH
The key open question: why was the initial state low-entropy? Deriving the Past Hypothesis from quantum gravity would be transformative. Using the Second Law's directionality as a constitutive principle for emergent spacetime (Jacobson 1995) is a consonant approach.

---

## 18. Third Law of Thermodynamics

### Stability: 8.5/10

### Known Challenges
- **Residual entropy**: Frustrated systems (spin ice, water ice) retain finite entropy at T=0 due to macroscopic ground-state degeneracy (Pauling 1935, Ramirez et al. 1999). Violates Planck formulation but not Nernst (unattainability) formulation.
- **Topologically ordered systems**: Fractional quantum Hall states, Kitaev toric code possess robust ground-state degeneracy with nonzero topological entanglement entropy at T=0.
- **Negative absolute temperatures**: Braun et al. (Science, 2013) demonstrated negative temperatures in ultracold atomic systems with bounded energy spectra.
- **Extremal black holes**: T=0 but nonzero Bekenstein-Hawking entropy. Whether this is a genuine violation or semiclassical breakdown remains debated.

### Reinterpretations
- **Information-theoretic (Masanes & Oppenheim, 2017)**: Recast as a bound on cooling rate derived from quantum resource theory — entropy reduction requires diverging resources as T→0.
- **Nernst vs. Planck distinction**: Careful treatments separate unattainability from entropy-minimum claim.

### Reinterpretation Potential: MODERATE
The extremal black hole problem (T=0, S>0) is an active frontier. Connecting the Third Law to holographic entanglement entropy (Ryu-Takayanagi) or complexity=action conjectures (Susskind, Brown) could constrain viable quantum gravity theories.

---

## 19. Gauge Invariance

### Stability: 9/10 empirically; 7/10 ontologically

### Known Challenges
- **Anomalies**: Gauge symmetries can be broken at quantum level. Chiral anomalies must cancel for consistency. Gravitational anomalies impose further constraints (Alvarez-Gaume & Witten, 1984).
- **Gribov ambiguity (1978)**: Gauge-fixing is not globally well-defined for non-Abelian theories, revealing nontrivial topological structure (Singer, 1978).
- **Gravity as gauge theory**: GR can be framed as gauge theory of the Poincare group, but the analogy is imperfect — the metric is not a connection in the same sense as Yang-Mills fields.
- **Strong CP problem**: Gauge-inequivalent vacuum configurations carry physical consequences, blurring redundancy/symmetry line.

### Reinterpretations
- **Connes' noncommutative geometry (2007)**: Standard Model gauge group emerges from algebra of a noncommutative internal space — gauge symmetry as geometric.
- **Donnelly & Freidel (2016)**: Gauge edge modes connected to entanglement entropy — gauge structure encodes quantum information at boundaries.
- **Wen's string-net condensation**: Gauge symmetry as emergent from deeper condensed-matter-like structures.

### Reinterpretation Potential: VERY HIGH
Treating gauge invariance as derivable from more primitive informational or entanglement constraints, which could simultaneously yield both Yang-Mills and diffeomorphism invariance from a common origin, would be a paradigm shift.

---

## 20. CPT Symmetry

### Stability: 9.5/10

### Known Challenges
- **Experimental precision**: ALPHA and BASE at CERN — hydrogen/antihydrogen agreement to parts in 10^12. No violation found.
- **Greenberg (2002)**: CPT violation in interacting QFT necessarily entails Lorentz violation, linking two seemingly independent symmetries.
- **Quantum gravity**: If spacetime locality or exact Lorentz invariance breaks down at Planck scale, the CPT theorem's premises no longer strictly hold.
- **Matter-antimatter asymmetry**: Requires C and CP violation (Sakharov, 1967) but not CPT violation.

### Reinterpretations
- **Wald (1980)**: Generalized CPT theorem to curved spacetime, noting subtleties in non-globally-hyperbolic spacetimes.
- **Boyle, Finn & Turok (2018)**: CPT-symmetric cosmology where the pre-Big-Bang universe is the CPT mirror of ours — reinterpreting CPT as a cosmological boundary condition rather than merely a local symmetry. Eliminates the need for inflation.

### Reinterpretation Potential: MODERATE-HIGH
CPT as a cosmological/gravitational principle (extending Boyle-Finn-Turok), and CPT in non-local quantum gravity frameworks where the standard theorem's premises fail, are the most promising directions.

---

## Summary: Reinterpretation Potential Rankings

| Rank | Tenet | Potential | Key Opening |
|------|-------|-----------|-------------|
| 1 | Born Rule (#14) | VERY HIGH | Underived postulate at the QM-gravity seam |
| 2 | Quantization (#11) | VERY HIGH | May be emergent, not fundamental — inverts QG program |
| 3 | Second Law (#17) | VERY HIGH | Past Hypothesis unexplained; entropy as constitutive principle |
| 4 | Equivalence Principle (#7) | VERY HIGH | QM-gravity junction; expected to break |
| 5 | General Covariance (#10) | VERY HIGH | Fault line between GR and QM |
| 6 | Gauge Invariance (#19) | VERY HIGH | May be derivable from entanglement/information |
| 7 | Least Action (#4) | HIGH | Presupposes smooth manifold; may be emergent |
| 8 | Noether's Theorem (#5) | HIGH | Needs generalization beyond Lagrangian mechanics |
| 9 | Speed of Light (#6) | HIGH | "Exact" vs "emergent" symmetry — open territory |
| 10 | Lorentz Invariance (#8) | HIGH | Discrete spacetime tension |
| 11 | Superposition (#13) | HIGH | May break at Planck-scale curvatures |
| 12 | Wave-Particle Duality (#16) | HIGH | Already obsolete — replace with pre-geometric structures |
| 13 | Conservation of Energy (#1) | HIGH | Ill-defined globally in GR |
| 14 | CPT Symmetry (#20) | MOD-HIGH | Cosmological boundary condition reframing |
| 15 | Conservation of Momentum (#2) | MODERATE | GR-QFT tension |
| 16 | Angular Momentum (#3) | MODERATE | BMS/spin-network unification |
| 17 | Uncertainty Principle (#12) | MODERATE | GUP needs first-principles derivation |
| 18 | Mass-Energy Equiv. (#9) | MODERATE | Cosmological constant problem |
| 19 | Pauli Exclusion (#15) | MODERATE | Topology-dependent in QG |
| 20 | Third Law (#18) | MODERATE | Extremal black holes |
