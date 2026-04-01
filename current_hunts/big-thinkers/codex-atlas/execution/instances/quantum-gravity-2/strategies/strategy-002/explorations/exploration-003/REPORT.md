# Exploration 003: Causal Order as the Physical Origin of the Fakeon

## Goal
Develop and evaluate a novel concept: the fakeon prescription in QG+F arises from spacetime's causal partial order. The claim is that the massive spin-2 ghost cannot become a real particle because doing so would violate the fundamental causal structure of spacetime.

## Part 1: Novelty Check

### 1.1 Anselmi on Causality and the Fakeon

Anselmi's own position on causality is the **opposite** of our concept. In his January 2026 paper "On Causality and Predictivity" (arXiv:2601.06346), he argues that:
- Microcausality violation is an acceptable price for renormalizability + unitarity
- The cause-effect relation is "inherently statistical" and "should be abandoned in fundamental physics"
- In theories with fakeons, we can only make "delayed prepostdictions" (verified retrospectively)
- The delay in quantum gravity is ~10⁻³⁷ seconds, practically irrelevant

Crucially, Anselmi does **not** derive the fakeon from causal structure. He goes the other way: he accepts that the fakeon violates causality and argues this is fine because causality was never fundamental anyway.

In his 2018 paper "Quantum gravity, fakeons and microcausality" (JHEP 11(2018)021), he establishes that the fakeon prescription violates microcausality at Planck scales — fields don't commute at spacelike separation below ~1/M₂. He treats this as a feature, not a bug.

### 1.2 The Wheeler Propagator — A Stunning Connection

**This is the most important finding of the novelty check.**

The fakeon propagator is defined as the **Cauchy principal value** of the pole:

> G_fakeon(p) = P.V. 1/(p² - m²)

In position space, this equals **(G_R + G_A)/2** — the average of the retarded and advanced propagators. This is mathematically identical to the **Wheeler propagator** (half-advanced + half-retarded), which is also the **real part of the Feynman propagator**.

Now, in a completely independent line of research, Belenchia, Benincasa & Liberati (JHEP 03(2015)036, arXiv:1411.6513) studied nonlocal scalar QFT derived from causal set dynamics. They found:

> "In 4-dimensions, the unstable modes of the non-local d'Alembertian are propagated via the so called Wheeler propagator and hence do not appear in the asymptotic states."

The causal set d'Alembertian, which arises from the fundamental causal partial order of the discrete spacetime, **naturally produces the Wheeler propagator for unstable modes**. These modes don't appear in asymptotic states — they are effectively **purely virtual**.

This means: **causal set structure independently produces fakeon-like behavior** for problematic degrees of freedom, through the same mathematical object (the Wheeler propagator).

However, Anselmi himself compared fakeons to Feynman-Wheeler particles in "The quest for purely virtual quanta: fakeons versus Feynman-Wheeler particles" (JHEP 03(2020)142, arXiv:2001.01942). He concluded they are **different at loop level**: the naive Feynman-Wheeler approach (using the Cauchy principal value in all diagrams) "violates renormalizability, unitarity and stability, due to the coexistence of the prescriptions ±iε." The fakeon prescription involves a more subtle procedure — use Feynman prescription first, then project out on-shell fakeon states.

**Nobody has connected these two findings.** The causal set community doesn't discuss fakeons; Anselmi doesn't discuss causal sets. The tree-level coincidence (Wheeler propagator = fakeon propagator) is unexploited.

### 1.3 Causal Structure in Higher-Derivative Gravity (Classical)

Emond, Moynihan & Roest (arXiv:2409.16935, 2024) and Ali & Suneeta (arXiv:2502.16527, 2025) studied classical causal structure in higher curvature gravity:
- Ghost modes can actually **restore** classical causality in Generalized Quadratic Gravity
- The causal structure must be defined using fastest propagating modes, not null curves
- This remains purely classical — no connection to quantization prescriptions

Donoghue ("Arrow of causality and quantum gravity," 2019) found that ghost particles propagate backwards in time — their positive energy flow goes in the anti-causal direction. This is treated as a mild causal violation acceptable if the ghost is unstable enough.

### 1.4 Epstein-Glaser Causal Perturbation Theory

The Epstein-Glaser framework (1973) derives perturbative QFT from causal axioms. Key point: propagator prescriptions (Feynman vs. retarded vs. advanced) emerge from how one extends distributions at coincident points. The choice of two-point function on curved spacetimes is not unique — there is renormalization freedom.

This framework shows that causal structure *constrains* but does not *uniquely determine* propagator prescriptions. However, it doesn't address ghosts or wrong-sign residues specifically.

### 1.5 Sorkin-Johnston Vacuum

The SJ state construction (Johnston 2009) derives the vacuum state for a scalar field on a causal set from the positive eigenspectrum of the commutator function (Pauli-Jordan function). This replaces the notion of "positive frequency" (which requires a timelike Killing vector) with a causal-order-based criterion. The SJ construction is a genuine example of causal structure selecting quantum states.

### 1.6 Novelty Verdict

**The specific concept — "causal order selects the fakeon prescription" — does NOT exist in the literature.**

However, the building blocks are all there:
1. ✅ Wheeler propagator = fakeon propagator at tree level (known to Anselmi)
2. ✅ Causal set structure produces Wheeler propagator for unstable modes (Belenchia et al. 2015)
3. ✅ Ghost modes propagate acausally (Donoghue 2019)
4. ❌ Nobody has connected (1) + (2) to argue that causal order motivates the fakeon
5. ❌ Nobody has addressed the loop-level gap (Wheeler ≠ fakeon at loop level)
6. ❌ Nobody has formulated a rule: "causal partial order ≺ → specific propagator prescription for wrong-sign poles"

**Novelty assessment: The concept is genuinely novel, but it sits in a narrow gap** — the tree-level connection exists implicitly, and the loop-level challenge is serious. Proceeding to concept development.

---

## Part 2: Concept Development

### 2.1 Physical Picture

Imagine spacetime not as a smooth continuum but as a web of discrete events linked by causal relations — event A can influence event B if and only if a signal can travel from A to B without exceeding the speed of light. This web has a definite direction: causes precede effects. Mathematically, this is a **partial order** ≺ on events.

In quantum field theory, particles propagate through spacetime via objects called propagators. A propagator encodes how a disturbance at one event influences another. For ordinary particles (photons, gravitons), the propagator respects the causal web — disturbances flow from past to future. But when we add higher-derivative terms to make gravity renormalizable, we introduce a massive spin-2 mode with a fatal flaw: its propagator has a **negative residue** (wrong sign). This means the mode's energy flow is reversed — it "wants" to propagate backwards through the causal web, from future to past. If this mode became a real, on-shell particle, it would literally reverse the local causal order, turning effects into causes.

The fakeon prescription is nature's enforcement mechanism: it says this backwards-flowing mode **can only exist as a bookkeeping device** in quantum calculations (loop integrals) but can never materialize as a real particle. The mathematical implementation is elegant: instead of the Feynman propagator (which places the particle on-shell with a specific iε prescription), the fakeon propagator takes the **Cauchy principal value** — the average of past-to-future and future-to-past propagation. This average is the **Wheeler propagator**, (G_retarded + G_advanced)/2, which has no on-shell poles and thus no real particle production.

The striking discovery is that this same Wheeler propagator emerges naturally from **causal set theory** — when you build QFT on a fundamentally discrete, causally-ordered spacetime, the unstable modes are automatically propagated via the Wheeler propagator and excluded from physical (asymptotic) states. The causal web itself refuses to let them become real.

### 2.2 The Mechanism: How Causal Order Constrains Propagator Prescriptions

**The Proposed Rule:**

Given a fundamental causal partial order ≺ on spacetime events, the propagator for any field mode with mass m and residue r at the pole p² = m² must satisfy the **causal compatibility condition**:

> The propagator G(x, y) must be decomposable as G = G_causal + G_virtual, where:
> - G_causal has support only for x ≻ y or y ≻ x (causally related pairs)
> - G_virtual is symmetric under x ↔ y (no preferred causal direction)
> - Only G_causal contributes to the on-shell (asymptotic) states

For **positive-residue poles** (normal particles): The Feynman propagator satisfies this automatically. G_causal = the retarded propagator piece; G_virtual = the loop contributions. Real particle production is causal.

For **negative-residue poles** (ghosts): The Feynman propagator does NOT satisfy this. The negative residue flips the sign of G_causal, making it anti-causal (future→past). The ONLY prescription that maintains causal compatibility is the Wheeler/fakeon prescription: G = (G_R + G_A)/2, which has no asymptotic on-shell contribution. The ghost is entirely G_virtual — symmetric, directionless, purely virtual.

**The specific mechanism connecting causal order to the prescription:**

1. **Start from the Sorkin-Johnston construction**: On a causal set, the vacuum state is selected by the positive eigenspectrum of the Pauli-Jordan function Δ(x,y) = [ϕ(x), ϕ(y)], which encodes the causal structure (Δ vanishes for spacelike separation).

2. **For modes with positive spectral weight**: The SJ construction naturally yields the Feynman propagator. The positive-frequency decomposition is well-defined and coincides with the standard Wightman function.

3. **For modes with negative spectral weight** (the ghost): The SJ construction breaks down — the "positive frequency" decomposition would yield negative-norm states. The causal partial order cannot support a state space with negative norms while maintaining the probabilistic interpretation. The only consistent option is to exclude these modes from the physical spectrum entirely — propagate them via the Wheeler propagator, which has no on-shell part.

4. **The loop-level completion**: At tree level, the Wheeler propagator suffices. At loop level, the additional subtlety of the fakeon prescription (dropping thresholds involving fakeon frequencies) can be understood as requiring that the ghost mode remain purely virtual **at every order in perturbation theory**, not just at tree level. This is the quantum extension of the classical causal-order constraint: if the causal partial order forbids the ghost from materializing, it must be forbidden in virtual pair production as well.

### 2.3 Testable Prediction

**Prediction: Dimensional reduction signature in the fakeon sector.**

If the fakeon prescription genuinely arises from causal set structure, then the nonlocality scale of the causal set d'Alembertian (the discreteness scale ℓ) should be related to the fakeon mass M₂. Belenchia et al. (2015) showed that causal-set-derived QFT exhibits **universal spectral dimension reduction to d = 2 at high energies**. If the fakeon mass M₂ is identified with the discreteness scale, this predicts:

> The spectral dimension of spacetime as probed by graviton scattering should flow from d = 4 at energies ≪ M₂ to d = 2 at energies ≫ M₂, with the crossover occurring at the fakeon mass scale.

This differs from standard QG+F, which predicts no specific dimensional reduction. It's speculative but potentially distinguishable: the running of Newton's constant with energy in QG+F could carry an imprint of the d = 2 regime if this connection holds.

**A more modest prediction:** The micro-causality violation window (~1/M₂) should coincide with the nonlocality scale of the causal set. If causal order is fundamental, the violation isn't a "sacrifice" (as Anselmi frames it) but a **reflection of the discrete granularity** of the underlying causal order. Below the discreteness scale, the partial order ≺ is "coarse-grained" — events are neither causally related nor spacelike separated but simply unresolved. The micro-causality violation is the signature of this unresolved region.

### 2.4 Self-Assessment

**(a) Genuine novelty: 7/10**
The specific claim "causal order selects the fakeon" is absent from the literature. The Wheeler propagator connection (fakeon = Wheeler at tree level, causal sets produce Wheeler for unstable modes) is an unexploited bridge between two active programs. However, the individual pieces exist — this is a synthesis, not a discovery from scratch. And the loop-level gap (Wheeler ≠ fakeon at loop level) weakens the claim significantly.

**(b) Internal consistency: 5/10**
The tree-level story is clean and compelling. The loop-level extension is hand-wavy — "the constraint must persist at every order" is assertion, not derivation. The SJ construction argument for negative-spectral-weight modes is suggestive but not rigorous; the SJ formalism hasn't been applied to higher-spin fields or ghosts. The connection between causal set discreteness and the fakeon mass is speculative.

**(c) Explanatory clarity: 8/10**
The physical picture is intuitive and accessible. The mathematical skeleton (causal order → SJ construction → Wheeler propagator for ghosts → fakeon at tree level) is clear. The dimensional reduction prediction is concrete. The concept tells a coherent story even if the details need work.

**(d) Viability for further development: 6/10**
The tree-level connection is solid ground for a research program. The loop-level gap is the main obstacle — but it's a well-posed problem: "Can the causal set formalism, extended to loop level, reproduce the full fakeon prescription?" The SJ construction for higher-spin fields is an open question in causal set theory that would need to be addressed.

---

## Part 3: Devil's Advocate

### 3.1 The Classical→Quantum Gap

**This is the most serious objection.** The causal partial order ≺ is a classical structure — it describes the geometry of spacetime, not the quantum state of fields. The fakeon prescription is an inherently quantum operation — it modifies the path integral, not the geometry. How does a classical geometric structure constrain a quantum prescription?

**The defense** appeals to the SJ construction: the causal order constrains the *vacuum state* of the quantum theory, which in turn constrains the propagator. This isn't purely classical — the SJ state is a quantum state derived from classical causal data. However, this defense is weak for two reasons:
1. The SJ construction assumes a fixed background causal structure. In quantum gravity, the causal structure is itself dynamical and quantum. The fakeon is needed precisely for the graviton's spin-2 partner — a mode of the gravitational field that *defines* the causal structure. This is circular: using causal structure to constrain a mode that generates causal structure.
2. The SJ construction has only been developed for free scalar fields on fixed backgrounds. Extending it to spin-2 fields on dynamical backgrounds is a major unsolved problem.

**Verdict: The classical→quantum gap is NOT resolved.** The concept provides motivation and a suggestive tree-level connection, but the central challenge remains.

### 3.2 Is This Just Unitarity in Causal Language?

**Partially, yes.** The standard argument for the fakeon is: "unitarity requires removing the ghost from the physical spectrum." The causal argument is: "the causal order requires removing the ghost from the physical spectrum." If causal order → unitarity (which it does, via the connection between causality and the CPT theorem), then the causal argument may just be the unitarity argument wearing a new hat.

**The defense**: The causal argument is more specific than the unitarity argument. Unitarity alone doesn't tell you *which* prescription to use — you could also use the Lee-Wick prescription (complex-conjugate poles), PT-symmetric quantization (Mannheim), or other approaches. The causal-order argument specifically selects the Wheeler/fakeon prescription because:
- The Lee-Wick approach requires complex masses, incompatible with the real spectrum of the causal partial order
- PT-symmetric quantization modifies the inner product, not the propagator, and doesn't arise from causal structure
- The Wheeler propagator is the *unique* propagator that is both (a) real (no preferred time direction at the level of the ghost) and (b) derived from causal structure (as shown in causal set QFT)

**Verdict: Not merely unitarity in disguise**, but the additional content is thin. The main added value is the constructive derivation (causal order → Wheeler propagator) rather than just the requirement (unitarity → some ghost-free prescription).

### 3.3 Can This Select the Fakeon Without Prior Knowledge?

**This is the acid test.** If you start from a causal partial order and a higher-derivative action, can you derive that the spin-2 ghost must be a fakeon without already knowing it's a ghost?

**The honest answer is: probably not in the current formulation.** The argument requires:
1. Identifying which modes have negative residues (requires computing the propagator first)
2. Noting that negative residues are incompatible with causal order (requires the specific mechanism of Section 2.2)
3. Applying the Wheeler/fakeon prescription to those modes

Step (1) requires knowing the theory. You can't derive the fakeon from pure causal structure — you need the Lagrangian. The concept explains *why* the ghost is a fakeon (causal incompatibility) but doesn't *predict* it from first principles.

**However:** If you take the Sorkin-Johnston approach seriously, you could in principle start from:
- A causal set (discrete causal order)
- A free field theory on that causal set
- The SJ vacuum construction

And discover that certain modes (those with negative spectral weight) are automatically excluded from physical states and propagated via the Wheeler propagator. This would be a genuine prediction from causal structure, without prior knowledge of ghosts. But this has never been done for spin-2 fields.

**Verdict: Currently, no — the concept cannot independently select the fakeon.** But there is a plausible path (SJ construction for higher-spin fields on causal sets) that could eventually get there.

### 3.4 Additional Objections

**Objection 1: The loop-level gap is fatal.**
The Wheeler propagator and the fakeon prescription agree at tree level but differ at loop level. Anselmi (2020) explicitly showed that using the Wheeler propagator naively in loops violates renormalizability, unitarity, and stability. The fakeon prescription requires the additional step of dropping thresholds involving fakeon frequencies — a procedure that has no obvious derivation from causal order. If the concept can't reproduce the full fakeon prescription (not just the tree-level propagator), it's incomplete.

**Objection 2: Causal sets don't produce quadratic gravity.**
The Benincasa-Dowker action on causal sets reproduces the Einstein-Hilbert action in the continuum limit, not the R² + R_μν² action of quadratic gravity. There is no known causal set action that gives higher-derivative gravity. So the connection is purely at the level of mode treatment, not at the level of the theory itself.

**Objection 3: The Belenchia et al. result is for scalar fields only.**
The Wheeler-propagator-for-unstable-modes result applies to a scalar field on a causal set. Extending this to spin-2 fields (the actual ghost in QG+F) is non-trivial and hasn't been attempted. Spin-2 fields on causal sets are essentially unexplored territory.

**Objection 4: Circularity in quantum gravity.**
In QG+F, the metric (and hence the causal structure) is dynamical. The spin-2 fakeon is a perturbation of the metric. Using the background causal structure to constrain the perturbation's propagation is only valid in the perturbative regime. But the fakeon is supposed to be fundamental — valid beyond perturbation theory. If causal structure is the origin of the fakeon, what happens in the non-perturbative regime where there's no classical background causal structure?

---

## Conclusions

The concept "causal order selects the fakeon prescription" is **genuinely novel** — no one has made this argument in the literature. It rests on a real and unexploited mathematical connection: the fakeon propagator equals the Wheeler propagator at tree level, and the Wheeler propagator emerges naturally from causal set dynamics for unstable modes (Belenchia et al. 2015).

**What works:**
- The physical picture is compelling and intuitive
- The tree-level connection (causal set → Wheeler propagator → fakeon) is mathematically grounded
- The concept provides a *constructive* derivation of the fakeon (from causal order) rather than just a *consistency* requirement (from unitarity)
- It offers concrete (if speculative) predictions: dimensional reduction at the fakeon mass scale

**What doesn't work:**
- The loop-level gap: Wheeler ≠ fakeon beyond tree level, and Anselmi explicitly showed naive use of Wheeler propagator in loops fails
- The classical→quantum gap: causal order is classical; the fakeon is quantum; the bridge (SJ construction) hasn't been extended to the relevant setting
- Circularity: the fakeon is a mode of the metric that defines causal structure
- The concept cannot currently select the fakeon without prior knowledge of the ghost

**Bottom line:** This is a **promising but incomplete bridge concept** — it connects two independent research programs (causal sets and QG+F) through a concrete mathematical coincidence (Wheeler = fakeon at tree level) that deserves exploration. The loop-level completion is the make-or-break challenge. Rating: concept worth a short paper exploring the connection, but far from a complete physical argument.
