# Exploration 010: Future Directions Survey — What Should the Next Strategy Target?

## Goal
Survey 4 promising directions for the next strategy beyond Strategy-002's interpretive bridge result. Assess feasibility, novelty potential, and prediction capacity of each direction.

---

## Direction A: Non-Perturbative QG+F / Ghost Confinement

### State of the Art
Non-perturbative lattice approaches to quantum gravity are active but **no one has simulated QG+F on a lattice**. The main lattice programs (CDT, EDT, Regge calculus) use Einstein-Hilbert or Hořava-Lifshitz-like actions. A 2024 lattice affine gravity framework (Silva, arxiv 2512.19315) discretizes connections on a hypercubic lattice with Monte Carlo, but only in 2D proof-of-principle. CDT's 2024 review (Ambjørn et al., arxiv 2401.09399) identifies a UV critical line in the A–C_dS phase transition, suggesting a continuum limit exists, but the continuum theory is probably Hořava-Lifshitz, not QG+F.

The ghost confinement analogy (QCD ↔ gravity) is suggestive but remains a conjecture. No lattice simulation has tested whether the massive spin-2 ghost confines. The QCD analogy would predict: (1) a mass gap for gravitational bound states, (2) ghost confinement below the Planck scale, (3) possible Planck-mass remnants. But no computational framework exists to test this.

A major 2025 development: Donoghue and collaborators showed that **physical running** of couplings in quadratic gravity (arxiv 2403.02397) achieves asymptotic freedom without tachyons, making the ghost less problematic than previously thought. Separately, a March 2026 paper (arxiv 2603.07150) reinterprets the massive tensor ghost as an inverted harmonic oscillator (IHO) instability within "direct-sum QFT," claiming to resolve the unitarity tension entirely.

### Feasibility for a 10-Exploration Strategy
**Low-Medium.** The core problem is that no computational infrastructure exists. Building a lattice QG+F simulator from scratch is a multi-year project far beyond 10 explorations. However, a conceptual strategy could: (a) formalize the confinement conjecture precisely, (b) identify what lattice observables would test it, (c) explore whether CDT's existing phase structure maps onto QG+F's, (d) study the IHO reinterpretation's implications for bound states.

### Novelty Potential
**High.** Ghost confinement is genuinely unexplored territory. If the analogy holds, it would predict new physics (bound states, mass gap). The IHO/direct-sum QFT framework is brand new (2026) and could open computational avenues.

### Prediction Potential
**Medium.** Confinement would predict a mass gap and Planck remnants (potential dark matter candidates), but these are not directly testable with current experiments.

### Recommended Scope
Focus on formalizing the confinement conjecture and mapping CDT phase structure onto QG+F. Avoid attempting actual lattice simulation.

---

## Direction B: Parameter Determination / Observable Predictions

### State of the Art
QG+F has two free mass parameters: M₂ (spin-2 ghost mass) and M₀ (scalar mass, related to Starobinsky's R²). Current constraints:
- **M₀**: Constrained by CMB data (Starobinsky inflation). Planck + BICEP/Keck give M₀ ~ 3 × 10¹³ GeV. Agravity (Salvio & Strumia 2014) predicts n_s ≈ 0.967 and r ≈ 0.13 if the inflaton is the Higgs of gravity.
- **M₂**: Essentially unconstrained. Must be below M_Planck for the theory to be perturbative, but no lower bound from data.
- **LiteBIRD** (launch ~2032) will measure r to δr < 0.001, which would sharply constrain R² inflation models and by extension M₀.

**Gravitational wave ringdown** is a rapidly developing field. A 2024 PRL paper (Cano et al., arxiv 2405.12280) introduced a universal Teukolsky equation for modified gravity, enabling quasinormal mode calculations for spinning black holes in higher-derivative gravity. The METRICS framework computes QNM frequency shifts in modified gravity. However, quadratic gravity corrections to QNMs are suppressed by (M_BH/M₂)² — for M₂ anywhere near Planck scale, the corrections are unmeasurably small for astrophysical black holes.

A 2024 paper on unimodular quadratic gravity (Salvio, arxiv 2406.12958) shows the unimodular constraint changes inflationary predictions, providing a different observational handle.

### Feasibility for a 10-Exploration Strategy
**Medium.** The parameter space is well-defined. A strategy could: (a) compute QG+F predictions for LiteBIRD-detectable observables, (b) explore whether self-consistency (e.g., asymptotic freedom requirements) constrains M₂, (c) investigate whether the physical running (Donoghue 2024) predicts specific coupling trajectories, (d) compute QNM corrections in quadratic gravity.

### Novelty Potential
**Medium.** Most of this is following established paths (constrain parameters with data). The novelty would come from finding self-consistency constraints that pin down M₂ without experiment.

### Prediction Potential
**High.** This direction is inherently about predictions. LiteBIRD will test them. Gravitational wave observations from LISA and next-gen detectors may eventually reach sensitivity for some higher-derivative effects.

### Recommended Scope
Compute the full LiteBIRD-testable prediction space for QG+F inflation. Investigate whether asymptotic freedom + unitarity + stability jointly constrain M₂. Survey gravitational wave observables.

---

## Direction C: Genuinely New Mathematics

### State of the Art
Several mathematical frameworks could host QG+F-like theories:

1. **Functorial / Extended TQFT**: A 2025 paper in Letters in Mathematical Physics (Lorentzian bordisms in AQFT) shows that globally hyperbolic Lorentzian bordisms arise naturally in algebraic QFT. The functorial framework assigns vector spaces to boundaries and linear maps to cobordisms. However, this framework naturally describes topological or conformal theories — incorporating the full dynamical content of QG+F would require substantial extension.

2. **Information-theoretic / Entropic gravity**: A 2025 Physical Review X publication realizes the 30-year-old conjecture that gravity arises from entropic rearrangement of information via microscopic quantum models. Newton's law emerges from free energy extremization of qubit collections. A separate 2025 study introduces an "informational stress-energy tensor" into Einstein's equations linking entanglement entropy to spacetime curvature. These are bottom-up approaches — not obviously compatible with QG+F's top-down UV completion.

3. **Direct-sum QFT**: The March 2026 framework (arxiv 2603.07150) that reinterprets ghosts as IHO instabilities uses a novel mathematical structure with "geometric superselection sectors" and two arrows of time. This is genuinely new mathematics that could be rigorously formalized.

4. **Non-local quantum gravity**: Modesto and collaborators develop non-local QG (infinite derivatives) as an alternative UV completion. Recent work by Anselmi et al. (2025, paper 25A1) on "Amplitude prescriptions in field theories with complex poles" explores the local limit connecting non-local and local (QG+F-like) theories.

### Feasibility for a 10-Exploration Strategy
**Low.** Mathematical framework development requires deep technical expertise and long timelines. A 10-exploration strategy would likely produce only a survey and initial formalization, not a working framework.

### Novelty Potential
**Very High.** New mathematical frameworks are the highest-impact contribution possible. The direct-sum QFT and information-theoretic approaches are barely explored.

### Prediction Potential
**Low.** Mathematical frameworks don't produce predictions directly. They enable future predictions.

### Recommended Scope
If pursued, focus narrowly on one sub-direction (e.g., rigorously formalizing direct-sum QFT for QG+F, or exploring whether information-theoretic gravity reproduces QG+F's structure). Avoid trying to survey all mathematical approaches.

---

## Direction D: The QG+F–AS Connection

### State of the Art
Quadratic gravity (QG+F) and asymptotic safety (AS) are treated as **distinct approaches** in the literature. A 2025 swampland/AS assessment (arxiv 2502.12290) explicitly lists them separately: AS relies on a non-perturbative UV fixed point (the Reuter fixed point), while QG+F is perturbatively renormalizable with asymptotic freedom.

Key developments:
- **Donoghue's critique of AS** (arxiv 1911.02967) questions whether the truncated functional RG calculations reliably identify a true fixed point, arguing the evidence is scheme-dependent.
- **Physical running results** (2024): The corrected beta functions for quadratic gravity show asymptotic freedom is achievable, which is a *different* UV behavior than AS's interacting fixed point. Asymptotic freedom means couplings go to zero; a UV fixed point means they go to finite nonzero values.
- **Lattice perspectives** (arxiv 2509.26352): A 2025 paper explores AS from both functional and lattice approaches, noting that one-loop results for power-counting marginal operators (quadratic in curvature) show universality, but this doesn't extend to relevant/irrelevant operators.
- **Two gravitational fixed points**: Recent FRG calculations (JHEP 2025) at fourth order in derivatives find two viable UV fixed points in the photon-graviton system.
- **CDT connection**: CDT's UV critical line may correspond to an AS fixed point, but CDT's continuum limit is likely Hořava-Lifshitz gravity, not QG+F.

The key question — "are QG+F and AS the same theory?" — remains open. They could be: (a) the same theory seen perturbatively vs. non-perturbatively, (b) different theories in the same universality class, or (c) genuinely distinct UV completions.

### Feasibility for a 10-Exploration Strategy
**Medium-High.** The question is sharply defined and the tools exist. A strategy could: (a) compare perturbative QG+F beta functions to AS truncated FRG results at matching order, (b) identify observational discriminators (different inflationary predictions?), (c) investigate whether QG+F's asymptotic freedom is compatible with AS's interacting fixed point, (d) determine what lattice/CDT evidence would distinguish them.

### Novelty Potential
**High.** Resolving this question — or even sharpening it into precise mathematical terms — would be a significant contribution. The community treats them as separate programs; demonstrating equivalence or inequivalence would reshape the field.

### Prediction Potential
**Medium-High.** If QG+F ≠ AS, they should make different predictions for inflation, black hole physics, or short-distance gravity. Identifying these discriminators would be valuable even without experimental tests.

### Recommended Scope
Sharply compare perturbative QG+F to AS at matching truncation order. Identify the precise mathematical condition that would make them equivalent or inequivalent. Compute distinguishing observables if they differ.

---

## Comparative Assessment & Recommendation

| Direction | Feasibility | Novelty | Predictions | Overall |
|-----------|------------|---------|-------------|---------|
| A: Non-perturbative / Confinement | Low-Med | High | Medium | ★★★ |
| B: Parameters / Observables | Medium | Medium | High | ★★★ |
| C: New Mathematics | Low | Very High | Low | ★★ |
| D: QG+F–AS Connection | Med-High | High | Med-High | ★★★★ |

### Top Recommendation: Direction D (QG+F–AS Connection)

**Rationale:** This direction has the best combination of feasibility and impact. The question is sharply defined, the technical tools exist (perturbative beta functions, FRG truncations), and the answer has immediate consequences for the field. It also naturally incorporates elements from Directions A and B — if QG+F and AS are different, the comparison itself identifies what's distinctive about each, which could reveal new observables (Direction B) and clarify the non-perturbative regime (Direction A).

### Runner-Up: Direction B (Parameters / Observables)
This is the safest choice — most likely to produce concrete results. LiteBIRD predictions are straightforward to compute. The risk is low novelty: we'd be doing standard phenomenology.

### Hybrid Recommendation
A strong strategy would combine D and B: use the QG+F–AS comparison to identify what's genuinely distinctive about QG+F, then compute the observational signatures of those distinctive features. This avoids both the pure-theory risk of Direction D and the low-novelty risk of Direction B.
