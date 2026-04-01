# Exploration 007: Devil's Advocate — Attack Causal Fakeon Theory

## Goal
Ruthlessly stress-test CFT (4 axioms + 1 conjecture from Exploration 006) across 6 attack vectors. Rate each FATAL through MINOR. Deliver an honest verdict on whether CFT is worth further development.

---

## Attack Vector 1: The Loop-Level Gap
**Rating: NEAR-FATAL**

### The Problem
CFT's entire claim to being a "theory" rather than an "observation" rests on the Loop Extension Conjecture: that the causal set formalism can reproduce Anselmi's full fakeon prescription at loop level. This conjecture faces three compounding obstacles:

**Obstacle 1: The Wheeler propagator is provably wrong at loop level.**
Anselmi (JHEP 03(2020)142) explicitly proved that using the Wheeler propagator (= Cauchy principal value) inside loop diagrams causes three simultaneous failures: (a) renormalizability violation — the coexistence of +iε and −iε prescriptions produces UV divergences not absorbable by standard counterterms; (b) unitarity violation — the optical theorem fails because the principal value doesn't correctly separate absorptive from dispersive parts; (c) stability violation — the Hamiltonian is unbounded below. This is not a technicality — it's a proof that the naive extension of CFT's tree-level result is *impossible*.

**Obstacle 2: Interacting QFT on causal sets is in its infancy.**
The most advanced result is Albertini, Dowker, Nasiri & Zalel (arXiv:2402.08555, 2024), who derived a diagrammatic expansion for in-in correlators in scalar φ^n theories on causal sets and defined a notion of scattering amplitudes. This is impressive progress, but: (a) it's scalar fields only, (b) it gives tree-level diagrams, not loop corrections, (c) there is no mention of the SJ construction for interacting theories, ghosts, or the Wheeler/fakeon propagator. The gap between "tree-level scalar diagrams on causal sets" and "loop-level threshold-dropping for spin-2 ghosts" is enormous.

**Obstacle 3: The conjecture may be unfalsifiable in practice.**
To test the Loop Extension Conjecture, one would need: (a) an interacting SJ construction on causal sets, (b) extension to spin-2, (c) loop-level calculations, (d) proof that threshold-dropping emerges. Each step is an unsolved research problem. The conjecture cannot be tested without solving problems that may take decades — or may be impossible.

### Severity Assessment
The tree-level identity G_fakeon = G_Wheeler is exact and interesting. But CFT's conjecture that this extends to loops is not merely unproven — the naive extension is *provably wrong*, and the correct extension would require reproducing a highly specific, technically intricate procedure (Anselmi's threshold-dropping) from a formalism that currently can't even handle interacting scalars at loop level. This is the theory's Achilles heel.

**NEAR-FATAL because:** Without loop extension, CFT is a tree-level observation dressed up as a theory. The 4-axiom framing is misleading — Axioms 1-3 give you tree level, and the Conjecture (the actual theory) is not just unproven but faces provable obstacles to the naive approach.

---

## Attack Vector 2: The SJ Construction Limitations
**Rating: SERIOUS**

### The Problem
CFT's core mechanism is: SJ construction → negative spectral weight detected → mode excluded → Wheeler propagator. But the SJ construction exists only for **free scalar fields on fixed backgrounds**. The ghost in QG+F is a **massive spin-2 field on a dynamical background**. Every word of that description violates the SJ construction's domain of validity.

**Gap 1: Scalar → Spin-2.**
The SJ construction has been rigorously defined for free scalar fields (Johnston 2009, Afshordi-Aslanbeigi-Sorkin 2012). Johnston has preliminary proposals for spin-1/2 (using the Feynman checkerboard or "square root of Klein-Gordon" approaches), but these are incomplete. For spin-1, nothing exists. For **spin-2 — nothing exists at all.** There is no SJ construction for tensor fields on causal sets, period. The entire CFT argument about the spin-2 ghost is by *analogy* with the scalar case.

**Gap 2: Free → Interacting.**
The SJ construction defines a vacuum for free fields. In the full quantum gravity theory, the spin-2 ghost interacts with the graviton, matter, and itself. The SJ vacuum is undefined for interacting fields.

**Gap 3: Fixed background → Dynamical.**
In quantum gravity, the background metric (which defines the causal structure) is itself dynamical. The SJ construction requires a *given* causal structure to work with. On a dynamical background, you'd need a self-consistent determination: causal structure → SJ vacuum → quantum corrections → modified causal structure → ... This is precisely the circularity problem (Attack Vector 3).

**The Belenchia et al. result is narrower than CFT claims.**
Belenchia, Benincasa & Liberati (JHEP 03(2015)036) proved that "unstable modes" of the nonlocal causal-set d'Alembertian propagate via the Wheeler propagator in **4D specifically** (in 2D, the Hamiltonian is positive-definite and the issue doesn't arise). Crucially: these are unstable modes of the *scalar* causal-set d'Alembertian — NOT spin-2 gravitational ghost modes. The analogy between "scalar unstable mode on a causal set" and "spin-2 ghost in quadratic gravity" is suggestive but unproven. Different spins have fundamentally different causal propagation properties.

### Severity Assessment
CFT's entire causal-order argument is built on a scalar analogy extended to spin-2 by assumption. This isn't dishonest — Exploration 006 acknowledges it — but it means the "derivation" of the fakeon prescription is really: "Here's how it would work *if* the SJ construction could be extended to spin-2 on dynamical backgrounds, which nobody has done." The honest description is: a *plausibility argument*, not a derivation.

**SERIOUS because:** The spin-2 gap is structural, not just technical. Spin-2 fields on causal sets require a vierbein formalism or equivalent that doesn't exist. This could be a decades-long program with no guarantee of success.

---

## Attack Vector 3: Circularity
**Rating: MODERATE**

### The Problem
CFT uses causal order ≺ to constrain the spin-2 ghost χ_μν. But χ_μν is a perturbation of the metric g_μν, which *defines* the causal order ≺. So CFT uses ≺ to constrain a mode that modifies ≺. Is this circular?

### Analysis
**Within perturbation theory: No genuine circularity.**
The background metric ḡ_μν defines a fixed causal order ≺₀. Perturbations (graviton h_μν and ghost χ_μν) are small corrections. The SJ construction and Wheeler propagator assignment are defined with respect to ≺₀. The ghost's purely virtual nature means it never produces a classical on-shell disturbance to ≺₀. This is self-consistent at every order in perturbation theory.

**Beyond perturbation theory: Genuine circularity, but shared with all perturbative QG.**
Non-perturbatively, there's no fixed ≺₀ to start from. The causal structure must be determined self-consistently. But this is the standard problem of *all* perturbative approaches to quantum gravity — not specific to CFT. String theory has background dependence. Asymptotic safety starts from a fixed background. Loop quantum gravity faces analogous issues with the semiclassical limit. CFT's circularity is "normal" for the field.

**Is it worse for CFT?**
Arguably yes, slightly — because CFT *makes causal order its foundational principle*. If you build your theory on ≺ and then admit ≺ is only well-defined perturbatively, that's a sharper tension than in frameworks that don't foreground causality. But the practical impact is nil: the theory works within perturbation theory, which is where all current calculations live.

### Severity Assessment
**MODERATE because:** The circularity is real but generic. It doesn't distinguish CFT from other approaches. It's a weakness of perturbative QG, not a specific flaw of CFT. The tension between "causal order is fundamental" and "causal order is only defined perturbatively" is philosophically uncomfortable but doesn't break anything computationally.

---

## Attack Vector 4: Does This Actually Derive the Fakeon?
**Rating: SERIOUS**

### The Problem
CFT claims to *derive* the fakeon prescription from causal order. But examine the logical chain:

1. Start with quadratic gravity (Stelle 1977) — this gives you the propagator with a negative-residue pole at p² = M₂².
2. Note that the residue is negative (this comes from the *continuum* theory).
3. Apply SJ construction — find it breaks down for negative spectral weight.
4. Assign Wheeler propagator to the excluded mode.
5. Observe G_Wheeler = G_fakeon at tree level.

**The critical question: Does step 2 come from causal order, or from the continuum theory?**

The answer is unambiguous: step 2 comes from the continuum theory. You must *already know* the propagator structure of quadratic gravity — specifically, that the spin-2 pole has negative residue — before the SJ exclusion mechanism kicks in. Causal order does not tell you the spectrum of the theory. Causal order does not tell you which modes have negative spectral weight. You need the continuum action, the field equations, and the propagator analysis to identify the ghost.

**CFT is therefore a selection principle, not a derivation.**
Given that you already know there's a ghost (from continuum QG), CFT provides a *reason* for choosing the fakeon prescription over the ghost prescription. It does not derive the existence of the ghost, the quadratic gravity action, or the negative spectral weight from causal order alone.

**The predictiveness test:** Imagine you're a physicist who knows only about causal sets and the SJ construction, but has never seen quadratic gravity. Could you use CFT to *predict* that gravity should be described by a quadratic action with a fakeon? No. You'd need the continuum theory first.

**Comparison: How real derivations work.**
In string theory, the Einstein equations emerge from the worldsheet beta functions — you don't need to input GR. In loop quantum gravity, the area spectrum is derived from the quantization of geometry — you don't input it by hand. CFT does not achieve this level of derivation. It takes the QG+F answer and provides an interpretation in causal-set language.

### Severity Assessment
This is not fatal — explanatory frameworks have value. But the Exploration 006 report uses language like "derived" and "the causal order forbids" that overstates what CFT achieves. Honest language: "CFT provides a causal-order *motivation* for the fakeon prescription, given the prior identification of the ghost from continuum quadratic gravity."

**SERIOUS because:** The gap between "derives" and "motivates/selects" is the difference between a theory and an interpretation. CFT is closer to interpretation than derivation, which significantly reduces its value proposition.

---

## Attack Vector 5: Are the Novel Predictions Real?
**Rating: SERIOUS**

### Prediction 1: Dimensional Crossover at M₂
**Verdict: NOT A NOVEL PREDICTION.**

The spectral dimension flow d_s = 4 → 2 in the UV is arguably the most universal result in quantum gravity. It appears in:
- Causal Dynamical Triangulations (Ambjorn, Jurkiewicz, Loll)
- Asymptotic Safety (Reuter, Lauscher)
- Hořava-Lifshitz gravity (Hořava 2009)
- Noncommutative geometry
- Loop quantum gravity
- Causal set theory (Belenchia et al. 2016)
- Quadratic gravity / QG+F

Carlip (2017) argued this universality suggests a common deep origin. CFT claiming d_s = 4 → 2 as its prediction is like a new weather model claiming "it rains" as a novel prediction. Every approach gets this.

The claim that the *crossover profile* might differ between QG+F and causal-set-derived CFT is interesting but: (a) it hasn't been computed from either side, (b) there's no reason to expect a measurable difference, (c) even if there were, it would require probing physics at the fakeon mass scale (~10^{16} GeV or higher), which is experimentally inaccessible.

### Prediction 2: Stochastic Microcausality Violation
**Verdict: UNTESTABLE AND REDUNDANT.**

CFT claims the microcausality violation has a stochastic character (from Poisson sprinkling in the causal set) rather than the smooth character predicted by continuum QG+F. Problems: (a) the violation occurs at ~10^{-37} seconds — completely untestable by any foreseeable technology; (b) Anselmi (2026, arXiv:2601.06346) already argues microcausality should be "abandoned in fundamental physics" — CFT's reinterpretation doesn't add predictive content; (c) the "stochastic vs. smooth" distinction has no observable consequences.

### Prediction 3: Causal Sets Should Produce Quadratic Gravity
**Verdict: ACTUALLY A THREAT TO CFT.**

This is framed as a prediction, but it's really a *consistency requirement*. If CFT is correct, causal set dynamics should produce the quadratic gravity action in the continuum limit. What does the evidence say?

- The Benincasa-Dowker action recovers the **Einstein-Hilbert** action, not quadratic gravity.
- Eichhorn et al. (arXiv:2301.13525, 2023) constructed higher-order causal set operators. In the continuum limit, they get **R² − 2□R** — not the R² + C² (or equivalently R² + R_μν R^μν) needed for Stelle's quadratic gravity.
- There is *no* causal set action known to produce the specific combination of R² and Weyl² terms that defines quadratic gravity.

This "prediction" is therefore currently *falsified* or at best unsupported. The causal set program does not naturally produce quadratic gravity. If anything, the evidence suggests causal sets and quadratic gravity may be incompatible at the action level — which would undermine CFT's entire foundation.

### Summary
Zero of CFT's three "novel predictions" are genuinely novel, testable, and distinguishing. One (#3) actually threatens the theory's foundations.

**SERIOUS because:** A theory that claims to unify two programs but produces no new predictions is unfalsifiable. It's philosophy, not physics.

---

## Attack Vector 6: Comparison to Existing Programs
**Rating: MODERATE**

### What is CFT, really?
Strip away the axiom numbering and formalism. CFT is:
1. An observation: G_fakeon = G_Wheeler at tree level (mathematical identity).
2. A narrative: the SJ construction's failure for negative-spectral-weight modes *is* the causal-order origin of the fakeon.
3. A conjecture: this extends to loop level (unproven, faces obstacles).
4. A reinterpretation: microcausality violation = discreteness, analyticity sacrifice = causal enforcement.

### What does Sorkin/Dowker gain from CFT?
**Essentially nothing computational.** CFT doesn't help solve causal set dynamics, doesn't provide new actions, doesn't help with the entropy/measure problem, doesn't produce new observables for causal set cosmology. It gives them a *philosophical* connection to Anselmi's program, but Sorkin's group has shown no interest in pursuing this direction (no citations, no follow-up work connecting these programs).

### What does Anselmi gain from CFT?
**Nothing computational.** Anselmi already has a complete loop-level formalism. He doesn't need a causal-order motivation — he derives the fakeon from consistency requirements (unitarity + renormalizability). He has explicitly argued that causality should be *abandoned* (arXiv:2601.06346), which is philosophically opposed to CFT's causal-order foundation. Anselmi would likely view CFT as unnecessary metaphysics.

### Is it genuinely novel?
The tree-level Wheeler-fakeon identity has been noted by Anselmi himself (JHEP 03(2020)142). The connection between causal sets and the Wheeler propagator was established by Belenchia et al. (2015). CFT's contribution is connecting these two known results and providing interpretive glue. This is a modest intellectual contribution — a bridge observation — but the "4 axioms + 1 conjecture" framing makes it sound like a new theory when it's closer to a review connecting known results.

### Severity Assessment
**MODERATE because:** CFT has genuine conceptual value as a bridge between causal sets and QG+F. But it's oversold. It's an interpretive framework, not a research program that generates new calculations, predictions, or mathematical structures. Neither community (causal sets or QG+F) needs it or would obviously benefit from it.

---

## Overall Verdict

### Severity Summary
| Attack Vector | Rating | Key Issue |
|---|---|---|
| 1. Loop-Level Gap | **NEAR-FATAL** | Naive extension provably fails; correct extension requires nonexistent technology |
| 2. SJ Limitations | **SERIOUS** | Entire argument built on scalar analogy; spin-2 extension doesn't exist |
| 3. Circularity | **MODERATE** | Real but generic; shared with all perturbative QG |
| 4. Derivation vs. Selection | **SERIOUS** | CFT doesn't derive the fakeon; it selects/interprets it post-hoc |
| 5. Novel Predictions | **SERIOUS** | Zero genuinely novel predictions; one threatens CFT's foundation |
| 6. Comparison | **MODERATE** | Interpretive bridge, not a productive research program |

### What CFT Actually Achieves (Steel-Manning)
1. The tree-level identity G_fakeon = G_Wheeler is real and mathematically exact.
2. The SJ-exclusion story provides a physically intuitive *motivation* for the fakeon — "the causal order can't support negative-spectral-weight modes."
3. Connecting the Belenchia et al. result to Anselmi's fakeon is a genuine intellectual contribution.

### What CFT Does NOT Achieve
1. It does not *derive* the fakeon prescription — it *selects* it, given prior continuum input.
2. It does not work beyond tree level, and the extension faces provable obstacles.
3. It does not produce any novel, testable, quantitative prediction.
4. It does not help either the causal set or QG+F community solve their actual open problems.
5. Its "structural prediction" (causal sets → quadratic gravity) is currently unsupported by evidence.

### Recommendation: PIVOT

**CFT is not worth heavy further development.** It is an interesting bridge observation that was worth writing down (Exploration 006 did valuable work), but investing further exploration cycles in it would yield diminishing returns. The loop-level gap alone is likely insurmountable in any reasonable timeframe, and without it, CFT is a tree-level interpretation, not a theory.

**What to preserve:** The tree-level Wheeler-fakeon identity and the SJ exclusion story. These are worth noting as motivational context for the fakeon prescription. File them as an "interesting observation" in the library, not as an active research direction.

**Where to pivot:** Rather than trying to derive the fakeon from causal order (which CFT attempts and fails at beyond tree level), consider:
1. **The explanatory debts of QG+F directly** — what does the fakeon mean physically? Anselmi's "classicized dynamics" approach (JHEP 01(2026)104) may be more productive than causal-order reinterpretation.
2. **Non-perturbative QG+F** — the QCD analogy (asymptotic freedom → confinement). What is the non-perturbative gravitational physics? This bypasses the causal-set formalism entirely.
3. **Observable predictions** — tensor-to-scalar ratio, collider signatures. Things that connect to experiment rather than to interpretive philosophy.

The bottom line: CFT is a nice story about a real mathematical identity. It is not a theory, not a research program, and not a path to new physics. Acknowledge the observation; move on.
