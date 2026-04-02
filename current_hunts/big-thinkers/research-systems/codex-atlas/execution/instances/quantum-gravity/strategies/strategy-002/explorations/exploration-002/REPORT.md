# Exploration 002: Scrutinize Bianconi's Entropic Action Quantum Gravity (2025)

## Goal
Provide a thorough critical assessment of Bianconi's 2025 "entropic action" quantum gravity proposal, which claims to derive gravity from quantum relative entropy. Determine whether this is a viable quantum gravity theory worth pursuing or a reformulation of existing work.

---

## Task 1: Reconstruct the Proposal

### Paper Identity
- **Title:** "Gravity from entropy"
- **Author:** Ginestra Bianconi (Queen Mary University of London)
- **Published:** Physical Review D, Vol. 111, Article 066001 (March 2025)
- **arXiv:** 2408.14391 (v2)
- **DOI:** 10.1103/PhysRevD.111.066001

### Author Background (Important Context)
Bianconi is a Professor of Applied Mathematics specializing in **network science and complex systems** — she is the author of books on multilayer networks and higher-order networks (simplicial complexes). She is NOT primarily a quantum gravity researcher or high-energy physicist. Her expertise is in statistical mechanics of networks, algebraic topology of complex systems, and information theory applied to networks. This background explains both the novel angle of the paper (applying information-theoretic tools to gravity) and many of its gaps (missing standard QG sanity checks).

### Core Claim
The gravitational action IS the quantum relative entropy S(ρ_metric || ρ_matter) between the spacetime metric and the metric induced by matter fields. Gravity emerges from information-theoretic divergence between geometry and matter.

### Mathematical Ingredients

**1. Spacetime metric as quantum operator:**
The metric tensor g_μν is reinterpreted as a quantum operator playing the role of a "renormalizable effective density matrix." Metrics between differential forms of different degree are treated as quantum operators generalizing density matrices. The requirement of unit trace is relaxed. Eigenvalues λ of the metric operator define an entropy:

H = Tr(Ĝ ln Ĝ⁻¹) = -Σ_λ ln λ

For flat spacetime, all eigenvalues = 1, so H_g = 0.

**2. Topological matter via Dirac-Kähler formalism:**
Matter fields are described as a topological bosonic field — the direct sum of differential forms:

|Φ⟩ = φ ⊕ ω_μ dx^μ ⊕ ζ_μν dx^μ ∧ dx^ν

- 0-form (scalar): φ(x) ∈ ℂ
- 1-form (vector): ω_μ dx^μ
- 2-form (bivector): ζ_μν dx^μ ∧ dx^ν (antisymmetric)

The Dirac operator D = δ + d (codifferential + exterior derivative) acts on this field.

**Important limitation acknowledged by author:** Only scalar/topological bosonic fields are included. Fermions and non-Abelian gauge fields are completely absent and "left for future investigations."

**3. Two metrics — the entropic action:**
Two "topological metrics" — direct sums of metrics acting on 0-forms, 1-forms, and 2-forms:

- g̃ = g_(0) ⊕ g_(1) ⊕ g_(2) — the spacetime metric (across form degrees)
- G̃ = g̃ + α M̃ − β R̃ — the metric induced by matter and curvature

where:
- M̃ = D|Φ⟩⟨Φ|D + (m² + ξR)|Φ⟩⟨Φ| encodes the matter field contribution
- R̃ encodes curvature contributions (Ricci scalar for 0-forms, Ricci tensor for 1-forms)
- α, β are coupling constants

The Lagrangian is the quantum relative entropy:

ℒ = -Tr ln(G̃ g̃⁻¹)

Action: S = (1/ℓ_P^d) ∫ √|−g| ℒ d^d x

**Critical observation from reading the full paper:** The induced metric G̃ is **prescribed phenomenologically** (designed by hand to give the right low-energy limit), NOT derived from first principles. The particular combination of Ricci scalar, Ricci tensor, and matter field was chosen to reproduce Einstein-Hilbert + scalar field in the low-coupling limit.

**4. The G-field:**
An auxiliary field G̃ (direct sum G_(0) ⊕ G_(1) ⊕ G_(2)) introduced as Lagrangian multipliers enforcing a constraint. This is claimed to linearize the logarithmic action into a "dressed Einstein-Hilbert action" with an emergent cosmological constant.

### Equations of Motion

**Low-coupling limit (α, β ≪ 1):**
ℒ ≈ 3βR − α|∇φ|² − α(m² + ξR)|φ|²

This recovers the Einstein-Hilbert action with zero cosmological constant coupled to a scalar field. This is the key consistency check the paper performs.

**Full modified Einstein equations (Eq. 45 in paper):**
β R^μν [G_(0)]⁻¹ − ½g^μν ℒ + B^μν = T̃^μν

where B^μν contains **fourth-order differential operators** and variations of the Ricci tensor. The stress-energy T̃^μν couples curvature to matter nonlinearly.

**Crucial admission:** The paper states "The study of the solutions of the modified Einstein equations (45) is beyond the scope of this paper and will be considered in future works." No solutions are computed in the original paper.

**With G-field, vacuum equations become:**
R^G_μν − ½g_μν(R_G − 2Λ_G) + D_μν = 0

where Λ_G is the emergent cosmological constant.

### Follow-Up Papers (all by Bianconi)
1. **Black hole entropy (arXiv: 2501.09491, Entropy 27(3), 266, 2025):** Derives area law S ∝ A/(4G) for Schwarzschild BH at large radii. Schwarzschild is NOT an exact solution — only approximate in low-coupling, small-curvature regime. A correction/erratum was published (Entropy 27(7), 724) fixing normalization constants and typos, though "main results unchanged."
2. **Anisotropic diffusion (arXiv: 2503.14048):** Shows Perona-Malik image denoising algorithm emerges from GfE action in 2D Euclidean warm-up. Not relevant to quantum gravity.
3. **Inflation from entropy (arXiv: 2509.23987):** Derives modified Friedmann equations. Claims geometric inflation without inflaton field. Predictions: n_s ∈ [0.962, 0.964], r ∈ [0.010, 0.012] for 60 e-folds. This is the most concrete predictive paper.
4. **Thermodynamics of GfE (arXiv: 2510.22545):** Develops thermodynamic aspects of the theory.

### Citation Response
- **Community uptake appears minimal.** The only citing works found outside Bianconi's own follow-ups are:
  - "Theory of Entropicity" by J. O. Obidi (Cambridge Open Engage / SSRN preprints, not peer-reviewed) — claims Bianconi's work is a special case of a more general framework
  - No published critiques from the QG community found
  - No engagement from Jacobson, Verlinde, Padmanabhan, or other entropic gravity researchers apparent

---

## Task 2: Novelty Assessment

### Comparison to Existing Programs

**vs. Jacobson (1995):**
- Jacobson: δQ = TdS at local Rindler horizons → Einstein equations. Uses Bekenstein-Hawking entropy, thermodynamic identity. A derivation technique, not a new action principle.
- Bianconi: Proposes a specific Lagrangian (quantum relative entropy between metrics). This IS a new action principle, not just a derivation technique.
- **Key difference:** Bianconi gives a concrete action to vary; Jacobson gives a thermodynamic argument. Bianconi's is genuinely different in structure.
- **But:** Bianconi's action is designed to reproduce Einstein's equations in the low-coupling limit, just as Jacobson's argument does. Both recover GR as their main result.

**vs. Jacobson (2015):**
- Jacobson 2015: Maximal vacuum entanglement hypothesis → Einstein equations from entanglement equilibrium.
- Bianconi: Uses relative entropy as action, not entanglement entropy as a state condition.
- **Different conceptually** but both in the "gravity from quantum information" family.

**vs. Verlinde (2010):**
- Verlinde: Entropic force from holographic screens. Derives Newton's law, MOND-like predictions.
- Bianconi: Not a force law derivation. Uses variational principle with specific Lagrangian. No holographic screens.
- **Substantially different** in technical implementation.

**vs. Padmanabhan:**
- Padmanabhan: TdS = dE + PdV on horizons, cosmological constant from shift invariance.
- Bianconi: Shares the "gravity as thermodynamics" philosophy. The emergent Λ is conceptually similar. But the specific mechanism (relative entropy action) is different.

**vs. Sakharov (1967):**
- Sakharov: Induced gravity from one-loop effective action of matter fields. Λ ~ cutoff⁴ (way too large).
- Bianconi: Not a loop calculation. The action is classical, not quantum effective.
- **Different mechanism** but shares the "gravity emerges from matter" ethos.

### Novelty Verdict

**The idea IS genuinely novel in its specific form.** No one has previously proposed the quantum relative entropy between two metrics (spacetime metric vs. matter-induced metric) as the gravitational action. The use of Dirac-Kähler formalism to package matter fields as differential forms, and the treatment of metrics as density matrices, is original.

**However, the novelty is primarily in the packaging, not in the output.** The theory is engineered to reproduce GR + scalar field in the low-coupling limit. The novel mathematical machinery (relative entropy, Dirac-Kähler) doesn't produce new physics at low energies — it's a new route to the same destination.

**The genuinely new elements are:**
1. The high-coupling regime modifications to Einstein's equations
2. The G-field as a potential dark matter candidate
3. The emergent cosmological constant mechanism
4. The inflationary predictions (from the follow-up paper)

---

## Task 3: Tier 1 Validation (Structural Sanity)

### 3.1 Correct Degrees of Freedom (Massless Spin-2 Graviton)
**VERDICT: NOT DEMONSTRATED**

The paper works entirely at the classical level. There is no identification of the propagating degrees of freedom around a flat background. The standard procedure would be to linearize the theory around Minkowski, identify the propagator, and show it contains a massless spin-2 mode (the graviton). This is never done.

In the low-coupling limit, the theory reduces to Einstein-Hilbert, which DOES contain the spin-2 graviton. But the full theory has additional structure (the B^μν fourth-order terms, the G-field) whose propagating degrees of freedom are completely unanalyzed.

**Critical concern:** The B^μν tensor in the full modified Einstein equations contains fourth-order derivatives of the metric. Fourth-order gravity theories generically propagate a massive spin-2 ghost in addition to the massless graviton (this is the Stelle gravity story). Whether Bianconi's specific fourth-order structure is degenerate enough to avoid this is completely unknown — the analysis has simply not been done.

### 3.2 Unitarity
**VERDICT: NOT ADDRESSED**

The paper is entirely classical. No Hilbert space is constructed. No propagator is computed. No S-matrix is defined. Unitarity is a quantum property and the theory has no quantum formulation.

The author explicitly states: "A canonical quantization of this field theory could bring new insights into quantum gravity" — acknowledging that quantization is entirely future work.

### 3.3 Ghost Freedom
**VERDICT: SERIOUS CONCERN — FOURTH-ORDER EQUATIONS**

The full modified Einstein equations (Eq. 45) contain **fourth-order derivatives** of the metric through the B^μν tensor (which includes variations of the Ricci tensor). By the Ostrogradsky theorem, non-degenerate Lagrangians with higher-than-second-order equations of motion generically lead to a Hamiltonian unbounded from below, signaling ghost instability.

The paper claims that with the G-field, equations become "second order in the metric and the G-field." If true, this would be a key result. However:
- The G-field introduces additional degrees of freedom
- Whether these additional degrees of freedom are ghostly is not analyzed
- The degeneracy structure needed to avoid Ostrogradsky ghosts is not verified
- No Hamiltonian analysis is performed

**This is the most dangerous structural issue.** Fourth-order equations in gravity are well-known to produce a massive spin-2 ghost (as in Stelle's quadratic gravity). The QG+F program specifically addresses this by turning the ghost into a "fakeon." Bianconi's paper doesn't even acknowledge this as a concern.

### 3.4 UV Completion
**VERDICT: NO — THIS IS NOT A UV COMPLETION**

Despite press claims about "unifying quantum mechanics and general relativity," the theory is:
- Entirely classical (no quantization)
- Does not address the UV divergences of quantum gravity
- Does not compute any quantum corrections
- Does not demonstrate renormalizability or asymptotic safety or finite quantum amplitudes

The author calls the metric a "renormalizable effective density matrix" but this is a **naming convention**, not a demonstration of renormalizability. No renormalization group analysis is performed.

**In its current form, this is a classical modified gravity theory, not a quantum gravity theory.** It is strictly an IR/classical reformulation, exactly the criticism made of Jacobson's and Verlinde's approaches.

### 3.5 Diffeomorphism Invariance
**VERDICT: FORMALLY PRESENT**

The action uses covariant derivatives, the √|−g| measure, and tensor quantities. It appears manifestly diffeomorphism invariant at the classical level.

**However:** No explicit gauge-fixing or BRST analysis is provided. The diffeomorphism invariance of the constraint equations involving the G-field is not verified. Whether the full system (metric + G-field + matter) preserves the correct number of gauge symmetries to eliminate the right number of unphysical degrees of freedom is unknown.

### 3.6 Weinberg-Witten Theorem
**VERDICT: NOT ADDRESSED — BUT POTENTIALLY EVADABLE**

The Weinberg-Witten theorem states: a massless spin-2 particle cannot carry a Lorentz-covariant, conserved energy-momentum tensor. This constrains theories where the graviton is "composite" or "emergent."

**How it applies:** Bianconi's theory claims gravity "emerges" from entropy. If the graviton is fundamental in the low-energy limit (as in GR), the WW theorem doesn't apply. If the graviton is truly emergent from the entropic degrees of freedom, then the theory must evade WW through one of the known escapes:
1. **GR's pseudo-tensor nature** — GR's energy-momentum is not gauge-invariant, so WW doesn't bite
2. **Holography** — not invoked here
3. **Broken Lorentz invariance** — not invoked here

Since the theory reduces to GR at low coupling, it likely inherits GR's pseudo-tensor escape. But this hasn't been explicitly checked.

### Tier 1 Summary Table

| Check | Status | Details |
|-------|--------|---------|
| Spin-2 graviton | ❌ Not demonstrated | No linearization or propagator analysis |
| Unitarity | ❌ Not addressed | No quantum formulation exists |
| Ghost freedom | ⚠️ Serious concern | Fourth-order equations, no Ostrogradsky analysis |
| UV completion | ❌ No | Entirely classical, no quantum corrections |
| Diffeo invariance | ✅ Formally present | But no gauge-fixing or BRST analysis |
| Weinberg-Witten | ⚠️ Unclear | Likely evadable via GR limit, but not checked |

**TIER 1 VERDICT: FAILS.** The theory does not pass Tier 1 validation. Multiple critical checks are simply not addressed. The ghost problem from fourth-order equations is a serious structural concern. The complete absence of quantization means this is not, in its current form, a quantum gravity theory at all.

---

## Task 4: Tier 2 Validation (Known Physics Recovery)

Despite failing Tier 1, let's assess what the theory claims about known physics recovery, since these results are at the classical level where the theory is defined.

### 4.1 Newton's Law
**VERDICT: YES (in low-coupling limit)**

In the low-coupling limit (α, β ≪ 1), the theory reduces to Einstein-Hilbert + scalar field. The Newtonian limit of GR gives Newton's law. So the theory recovers Newton's law, but only because it was designed to reduce to GR.

### 4.2 GR Reduction
**VERDICT: YES (by construction)**

The low-coupling expansion explicitly gives:
ℒ ≈ 3βR − α|∇φ|² − α(m² + ξR)|φ|²

which is GR coupled to a scalar field. This is the main consistency check in the paper and it works. But it's a design choice, not a prediction — the induced metric G̃ was constructed specifically to produce this limit.

### 4.3 PPN Parameters
**VERDICT: NOT COMPUTED**

The post-Newtonian parameters (γ, β_PPN, etc.) are not calculated. In the low-coupling limit, they should match GR (γ = β_PPN = 1). But the full theory's PPN parameters could deviate from GR, and this is not analyzed.

### 4.4 Gravitational Wave Speed
**VERDICT: NOT COMPUTED**

The speed of gravitational waves (constrained to |c_gw/c − 1| < 10⁻¹⁵ by GW170817/GRB170817A) is not calculated. In the low-coupling limit, it should be c. But the full theory could modify the graviton dispersion relation.

### Tier 2 Summary
The theory recovers known physics in the low-coupling limit **by construction**. No non-trivial Tier 2 checks have been performed. We cannot assess whether the full theory is consistent with precision tests of gravity.

---

## Task 5: Assessment of Predictive Claims

### 5.1 Emergent Cosmological Constant
**CLAIM: "Emergent small and positive cosmological constant only dependent on the G-field"**

**Assessment: MOSTLY EMPTY**

In the original paper (2408.14391), the cosmological constant Λ is simply **introduced as a parameter** (−Λ in Eq. 35). It is not derived from first principles. The claim that it "only depends on the G-field" means that Λ_G enters the dressed Einstein-Hilbert action through the G-field constraint — but the VALUE of Λ_G is not predicted. It depends on the G-field configuration, which is itself undetermined.

This is NOT a solution to the cosmological constant problem. The CC is not calculated — it is parameterized through the G-field. Without a mechanism to fix the G-field's vacuum expectation value, the CC is just as free as in standard GR.

**Comparison to QG+F:** QG+F also has an open CC problem (the "new CC problem"), but at least identifies the specific mechanism that makes it a problem. Bianconi's approach doesn't even reach that level — it just moves the CC from one parameter to another.

### 5.2 G-Field as Dark Matter Candidate
**CLAIM: "The G-field might be a candidate for dark matter"**

**Assessment: PURELY SPECULATIVE**

The G-field is introduced as an auxiliary field (Lagrangian multiplier). The paper offers:
- No mass for the G-field
- No coupling to Standard Model particles
- No production mechanism
- No density profile predictions
- No explanation of galaxy rotation curves
- No comparison to dark matter observations
- No particle physics model

The phrase "might be a candidate for dark matter" is aspirational, not scientific. An auxiliary field introduced to linearize an action is generically non-dynamical — it would need to acquire dynamics through some mechanism not discussed in the paper.

### 5.3 Inflationary Predictions (from arXiv: 2509.23987)
**CLAIM: n_s ∈ [0.962, 0.964], r ∈ [0.010, 0.012] for 60 e-folds**

**Assessment: THE MOST INTERESTING RESULT, BUT WITH CAVEATS**

This follow-up paper derives modified Friedmann equations and finds inflationary solutions WITHOUT an inflaton field — inflation arises purely from the entropic action's nonlinear structure. The predictions:

| Observable | Bianconi Prediction | QG+F Prediction | Planck Data |
|-----------|-------------------|-----------------|-------------|
| n_s | 0.962–0.964 | ~0.967 | 0.9649 ± 0.0042 |
| r | 0.010–0.012 | 0.0004–0.0035 | < 0.036 |

**Positive aspects:**
- n_s prediction is within Planck bounds
- r prediction is testable by next-generation experiments (Simons Observatory, CMB-S4)
- Inflation without inflaton is elegant if it works

**Serious caveats:**
- The paper acknowledges that a "comprehensive study of perturbations in entropic gravity is yet to be realized" — meaning the n_s and r calculations may not be fully rigorous
- The coupling β = 1/2 is chosen to match the original framework, not derived
- The high-entropy regime (x ≈ 1/6) where inflation occurs is precisely where the low-coupling approximation breaks down — but the ghost and stability analysis hasn't been done for this regime
- Without a proper perturbation theory or quantum treatment, the spectral index prediction is computed in a semi-classical framework whose validity is unestablished

**Comparison to QG+F:** QG+F's predictions come from a fully quantized theory with known perturbation theory. Bianconi's predictions come from classical modified Friedmann equations in an unquantized theory. The comparison is not on equal footing.

### 5.4 Black Hole Entropy
**CLAIM: Area law S ∝ A/(4G) for large Schwarzschild radius**

**Assessment: ENCOURAGING BUT CIRCULAR**

The black hole entropy paper (2501.09491) shows the quantum relative entropy of the Schwarzschild metric follows an area law at large radii:
S ≃ C · A/(4G) where C = 32 ln(3/2) β τ' ≈ 12.97 β τ'

**Issues:**
- The Schwarzschild metric is NOT an exact solution of the modified equations — only an approximate solution in the low-coupling limit
- The proportionality constant C involves the free parameter β and a "dimensionless time parameter" τ'
- Getting the standard Bekenstein-Hawking result S = A/(4G) requires tuning these parameters
- A correction/erratum was needed (fixing normalization constants), raising concerns about the calculation's robustness

The result is suggestive but not a clean derivation of black hole entropy from first principles.

---

## Task 6: Overall Verdict

### Is this a viable quantum gravity theory?

**NO.** In its current form, this is NOT a quantum gravity theory. It is a classical modified gravity theory based on an information-theoretic action principle. Specifically:

1. **No quantization exists.** The theory is entirely classical. The author explicitly defers quantization to future work.
2. **No UV completion.** The theory does not address ultraviolet divergences, renormalizability, or any quantum property of gravity.
3. **Serious ghost concerns.** The fourth-order equations of motion risk Ostrogradsky instability, and no analysis of ghost degrees of freedom has been performed.
4. **Incomplete matter sector.** Only scalar/topological bosonic fields are included. Fermions and gauge fields are absent.
5. **The induced metric is phenomenological.** The specific form of G̃ is designed to reproduce GR at low coupling, not derived from deeper principles.

### What does it get right that others don't?

1. **Concrete action principle.** Unlike Jacobson or Verlinde, who provide derivation techniques, Bianconi gives a specific Lagrangian that can be varied. This is a genuine advance over "gravity as thermodynamics" arguments.
2. **Information-theoretic framing.** The idea that the gravitational action measures information-theoretic divergence between geometry and matter is physically appealing.
3. **Inflationary solutions without inflaton.** If the perturbation theory can be made rigorous, geometric inflation from the entropic action is an interesting direction.
4. **Black hole area law.** Getting S ∝ A from the formalism is non-trivial, even if approximate.

### Fatal Flaws

1. **Not quantum.** The most fundamental flaw. You cannot claim a quantum gravity theory without quantum mechanics.
2. **Fourth-order equations → probable ghosts.** This is potentially fatal. If the full theory propagates ghost degrees of freedom, it is inconsistent even classically.
3. **Phenomenological construction.** The induced metric G̃ is built by hand to give the right answer. This undermines the claim that gravity "emerges" from entropy — rather, GR is input into the construction.
4. **Author's expertise mismatch.** Bianconi is a brilliant network scientist, but the paper lacks standard checks that any QG practitioner would include (linearized analysis, propagator, ghost spectrum, degrees of freedom count). This suggests the work hasn't been sufficiently vetted by the QG community.

### Recommended Decision: MOVE ON

**Do not pursue this approach further for quantum gravity.** The proposal is not viable as a QG theory in its current form, and the structural issues (especially ghosts) are severe enough that fixing them would likely require rebuilding the theory from scratch.

**However, take two lessons from it:**

1. **The idea of gravitational action = quantum relative entropy is worth remembering.** If someone could implement this idea within a theory that IS properly quantized (e.g., as a UV completion mechanism within asymptotic safety or as a way to derive the effective action in a path integral framework), the information-theoretic framing could be powerful.

2. **The inflationary predictions are worth tracking.** If n_s ∈ [0.962, 0.964] and r ∈ [0.010, 0.012] are confirmed by CMB-S4 / Simons Observatory, that would be interesting — though many other theories make similar predictions in that range.

### Lessons About Information-Theoretic Approaches to QG

Bianconi's failure mode is instructive for the entire "gravity from information" program:

1. **Classical information theory is not enough.** You need genuine quantum mechanics — Hilbert spaces, unitary evolution, operator algebras. Merely calling your classical objects "quantum operators" or "density matrices" doesn't make the theory quantum.

2. **Recovering GR is necessary but not sufficient.** Any modified gravity theory can be designed to reduce to GR at low coupling. The test is what happens at high coupling / UV regime, and this requires quantum analysis.

3. **The ghost problem is a killer.** Any action that isn't Einstein-Hilbert will generically introduce additional degrees of freedom. If these are higher-derivative, Ostrogradsky's theorem bites. The information-theoretic action must either be equivalent to GR (in which case, why bother?) or face the ghost music.

4. **Entropic gravity programs share a common weakness:** They derive the classical Einstein equations from thermodynamic/information arguments but never provide the UV completion. Jacobson (1995), Verlinde (2010), Padmanabhan, and now Bianconi all fall into this trap. The hard problem of quantum gravity is not "how to derive Einstein's equations" — it's "how to quantize them consistently."

---

## Sources
- [Gravity from entropy - Phys. Rev. D](https://link.aps.org/doi/10.1103/PhysRevD.111.066001)
- [arXiv: 2408.14391](https://arxiv.org/abs/2408.14391)
- [Schwarzschild BH area law - arXiv: 2501.09491](https://arxiv.org/abs/2501.09491)
- [Inflation from entropy - arXiv: 2509.23987](https://arxiv.org/abs/2509.23987)
- [Beyond holography / anisotropic diffusion - arXiv: 2503.14048](https://arxiv.org/abs/2503.14048)
- [Thermodynamics of GfE - arXiv: 2510.22545](https://arxiv.org/abs/2510.22545)
- [BH paper correction - Entropy 27(7), 724](https://www.mdpi.com/1099-4300/27/7/724)
- [Physics World coverage](https://physicsworld.com/a/new-research-suggests-gravity-might-emerge-from-quantum-information-theory/)
- [QMUL press release](https://www.qmul.ac.uk/media/news/2025/science-and-engineering/se/gravity-from-entropy-a-radical-new-approach-to-unifying-quantum-mechanics-and-general-relativity.html)
- [Constraints on emergent gravity (Carlip) - arXiv: 0904.0453](https://arxiv.org/abs/0904.0453)
- [Weinberg-Witten theorem - Wikipedia](https://en.wikipedia.org/wiki/Weinberg%E2%80%93Witten_theorem)
