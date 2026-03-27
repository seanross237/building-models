# Exploration 001: Ghost Propagator Specification

## Mission Context

We are developing a Unified QG+F–AS Framework that treats Quadratic Gravity with Fakeons (QG+F) and Asymptotic Safety (AS) as perturbative/non-perturbative descriptions of one UV-complete theory (analogous to perturbative QCD / lattice QCD). The framework's biggest gap is **Predictive FAIL** — it lacks concrete, discriminating predictions. The single most discriminating prediction identified is the outcome of the ghost propagator computation in C²-extended FRG.

## Your Task

**One question:** What is the specific, quantitative predicted outcome of the ghost propagator computation in the C²-extended FRG, according to the unified framework?

Currently the prediction is vague: "the spin-2 ghost should dissolve somehow." Your job is to make it precise: "compute X in truncation Y, and the unified framework predicts result Z with specific form F."

## What You Must Deliver

A **computational specification** with these components:

1. **The predicted FORM of ghost dissolution.** Use the QCD analogy and existing results to predict which mechanism occurs:
   - Complex pole tower (Draper et al. model): ghost pole at p² = -m₂² splits into conjugate pairs
   - Residue vanishing (Platania model): ghost pole persists but residue → 0
   - Mass divergence: RULED OUT for spin-2 (see constraints below)
   - Something else?

   For whichever form you predict, give the mathematical structure. E.g., "the propagator in the spin-2 TT sector should have the form G(p²) = Σ_n c_n / (p² + M_n² ± iΓ_n) where M_n and Γ_n satisfy..."

2. **The critical scale.** At what momentum scale does the ghost dissolution begin? Derive this from:
   - The ghost mass m₂² = M_P²/(2α_W) where α_W is the Weyl coupling
   - The NGFP fixed-point value f₂* (Benedetti et al. 2009 found f₂ reaches a finite non-zero value)
   - The Bonanno et al. 2025 instability threshold at r_H ≈ 0.876/m₂

   Give a NUMBER (in Planck units or GeV), not just "O(M_P)."

3. **A precise computational specification.** State: "Compute the transverse-traceless spin-2 sector of the graviton propagator using the FRG in the (R + R² + C²) truncation, with momentum-dependent form factors as in Knorr-Saueressig 2022. The unified framework predicts: [specific outcome]. The null hypothesis (compatible-but-separate) predicts: [different outcome]."

4. **Classification of this prediction:**
   - DISCRIMINATING: yes/no — does this distinguish unified from compatible-but-separate?
   - NOVEL: yes/no — does neither QG+F alone nor AS alone predict this?
   - Numerical specificity: give actual numbers or parameter ranges where possible

## Critical Constraints (Pre-loaded)

You MUST incorporate these known results:

**Benedetti et al. (2009, arXiv:0909.3265):** Extended FRG to a four-parameter truncation including R² and C². The higher-derivative couplings are NOT asymptotically free at the NGFP — they reach finite values. f₂ reaches a finite non-zero fixed-point value f₂*. This means ghost mass M₂² ~ f₂² M_P² stays finite at the NGFP. The Becker mass-divergence mechanism CANNOT be extended to spin-2. This is a hard constraint.

**Draper, Knorr, Ripken, Saueressig (2020, PRL 125, 181301):** Reconstructed the non-perturbative graviton propagator from FRG data. Found infinite towers of complex conjugate pole pairs at imaginary p². These poles do NOT contribute to the absorptive part of scattering amplitudes. Done in Einstein-Hilbert truncation, not specifically for the Stelle ghost. This is the most concrete mechanism available.

**Knorr & Saueressig (2022, SciPost Phys. 12, 001):** Reconstructed graviton propagator from Euclidean FRG. Dynamical graviton: positive spectral function. Background graviton: negative parts (gauge artifact). Done in Einstein-Hilbert truncation only — no C² term. This is the methodology that would be extended.

**Holdom & Ren (2016, arXiv:1605.05006):** Two scenarios for the ghost propagator G(k²)/k⁴:
- Case A (softening): propagator softens to 1/k² with positive residue. Ghost pole transforms into a zero.
- Case B (confinement): mass gap develops, all perturbative propagating modes removed.

**QCD analogy breakdown points (from adversarial assessment):**
- No compact gauge group (diffeomorphisms vs SU(3)) — undermines center symmetry confinement mechanism
- No quantum number to confine — no color-like charge for the ghost
- No lattice evidence after 10+ years
- These are HIGH-severity breakdowns of the analogy

**Falls, Kluth & Litim (2023, PRD 108, 026005):** UV critical surface has exactly as many relevant directions as four-derivative couplings — a numerical coincidence supporting the unified picture.

**SWY (2022, JHEP 03, 130):** Two clearly resolved fixed points (AF and NGFP) with different critical exponents. The AF fixed point is Gaussian; NGFP is non-Gaussian. They're distinct.

## Failure Path

If you find that no specific quantitative prediction can be derived — that the unified framework genuinely cannot predict the outcome beyond "the ghost should dissolve somehow" — then:
1. Explain the structural reason WHY the prediction cannot be sharpened
2. Identify which unknown parameter or uncomputed quantity blocks the prediction
3. Propose what calculation or measurement WOULD allow a sharp prediction
4. Assess honestly: is the ghost propagator prediction actually discriminating, or is it just a consistency check dressed up as a prediction?

## Output

Write your findings to:
- `explorations/exploration-001/REPORT.md` (detailed findings, 200-400 lines)
- `explorations/exploration-001/REPORT-SUMMARY.md` (concise summary, 30-50 lines)

Write REPORT-SUMMARY.md LAST — it is the completion signal.
