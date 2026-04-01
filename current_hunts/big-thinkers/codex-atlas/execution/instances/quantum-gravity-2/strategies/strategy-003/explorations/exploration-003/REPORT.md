# Exploration 003: Ghost Fate at Strong Coupling — Does AS Produce Ghost Confinement?

## Goal

What does the non-perturbative / Asymptotic Safety literature say about the fate of the massive spin-2 ghost at strong coupling? Does ghost confinement, mass running to infinity, or spectral suppression naturally emerge?

---

## 1. Ghost Propagator in Non-Perturbative AS

### Key finding: The AS literature largely does not directly address the massive spin-2 ghost propagator.

The mainstream AS program (Reuter, Saueressig, Percacci, Eichhorn) works primarily with the Einstein-Hilbert truncation or modest extensions (R², R_μν R^μν). In these truncations, the graviton propagator is computed around flat or de Sitter backgrounds, and the focus is on the *massless* graviton propagator's momentum dependence — not on the fate of the massive spin-2 ghost that arises in R² + C² gravity.

The FRG (Wetterich equation) approach integrates out fluctuations shell-by-shell in momentum space. When applied to higher-derivative gravity, FRG studies typically track the running of couplings (Newton's constant G, cosmological constant Λ, and higher-derivative couplings) rather than reconstructing the full dressed propagator with its pole structure. **The ghost pole's fate is largely implicit in the running couplings, not explicitly tracked.**

**Critical gap:** No paper was found that computes the full non-perturbative dressed propagator of the massive spin-2 mode in the AS framework and checks whether the ghost pole persists, moves to complex momenta, or disappears.

---

## 2. Graviton Spectral Function Reconstruction (Bonanno et al. 2022)

**Paper:** Bonanno, Denz, Pawlowski, Reichert — "Reconstructing the graviton" (SciPost Phys. 12, 001, 2022) [arXiv:2102.02217]

**Background graviton spectral function:** Necessarily has negative parts. A sum rule (eq. 27): ∫₀^∞ dλ λ ρ_ḡ(λ) = 0 forces the spectral function to cross zero. The authors compare this to the QCD gluon spectral function — but explicitly state this has "nothing to do with strongly-correlated physics such as confinement."

**Fluctuation (dynamical) graviton spectral function:** Strictly positive, with anomalous dimension η_h ≈ 1.03. "Its positivity may hint at the unitarity of asymptotically safe quantum gravity."

**Regarding the ghost:** The paper does NOT discuss the massive spin-2 ghost pole. The reconstruction is done within the Einstein-Hilbert truncation (no C² term), so the ghost mode is absent from their truncation. The negative spectral weight is a gauge artifact.

**Assessment:** Demonstrates that spectral reconstruction techniques *exist* within AS, but says nothing about the ghost because the relevant operators are not included.

---

## 3. Running of Higher-Derivative Couplings at the NGFP

### 3a. Benedetti, Machado, Saueressig (2009) [arXiv:0909.3265]

Extended the FRG to a four-parameter truncation including R² and C² terms. Key finding: **The higher-derivative couplings are NOT asymptotically free — they reach finite values at the NGFP.** This contrasts with the perturbative result (Stelle's theory) where the couplings are asymptotically free. The non-perturbative FRG shifts the perturbative UV fixed point to a genuine NGFP with three UV-attractive and one UV-repulsive direction.

**Implication for ghost mass:** If the Weyl-squared coupling f₂ reaches a finite, non-zero fixed-point value f₂*, then the ghost mass M₂² ~ f₂² M_Pl² also stays finite. The ghost does NOT automatically decouple by its mass running to infinity in this scenario.

### 3b. Becker, Ripken, Saueressig (2017) [arXiv:1709.09098]

**Title:** "On avoiding Ostrogradski instabilities within Asymptotic Safety"

This paper studies gravity coupled to scalar fields with higher-derivative terms (□² in the scalar sector). Key findings:

- **Three families of NGFPs found:** NGFP₋ (y* < 0), NGFP₀ (y* = 0), NGFP₊ (y* > 0)
- **At NGFP₀:** The higher-derivative coupling y* = 0 exactly, meaning the Ostrogradski ghost mass μ² = 1/Y → ∞ **for all RG scales k**. The ghost decouples completely.
- **At NGFP±:** The ghost mass μ² = k²/y* → ∞ as k → ∞, so the ghost decouples in the deep UV.
- **IR behavior:** For physically relevant Type IIa trajectories, the dimensionless coupling y_k → 0 in the IR, so the ghost also decouples at low energies.

**CRITICAL CAVEAT:** This result applies to **scalar field ghosts only**, not to the gravitational spin-2 ghost. The gravitational sector remains at Einstein-Hilbert level in this paper. The authors explicitly state that extending to gravitational ghosts "is beyond the present work." However, the *mechanism* (ghost mass → ∞ at fixed point) is demonstrated as a proof of principle.

---

## 4. Fictitious Ghosts (Platania & Wetterich 2020) [arXiv:2009.06637]

**Title:** "Non-perturbative unitarity and fictitious ghosts in quantum gravity"

**Key concept:** Ghost-like poles that appear in truncated effective actions may be **fictitious** — truncation artifacts whose residues vanish when all symmetry-compatible operators are included.

**Mechanism:** When the effective action contains non-local form factors (branch cuts, logarithms), a finite-order derivative expansion generates spurious poles. As truncation order N increases:
- Fictitious poles approach the boundary of the convergence domain
- Their residues decrease monotonically → 0 as N → ∞

**On the spin-2 ghost:** The paper does NOT definitively classify Stelle's ghost as fictitious. It proposes a *methodology* to distinguish genuine from fake ghosts by tracking residue behavior across truncation orders, but does not carry out this program for the gravitational ghost specifically.

**Main conclusion:** "Fake ghosts do not indicate a violation of unitarity." Apparent ghost poles in truncated AS calculations may be artifacts, and AS is "not ruled out by apparent ghost poles."

**Relationship to fakeon:** No mention of Anselmi's fakeon prescription. The two frameworks (fictitious ghosts vs. fakeon quantization) address the same phenomenology from independent angles.

---

## 5. Complex Poles and Unitarity (Draper, Knorr, Ripken, Saueressig 2020)

**Papers:** "Finite Quantum Gravity Amplitudes — no strings attached" (PRL 125, 181301, 2020) and "Graviton-mediated scattering amplitudes from the quantum effective action" (JHEP 11, 136, 2020) [arXiv:2007.04396]

**Key result:** When the full momentum-dependent form factors of AS are included, the graviton propagator develops **infinite towers of spin-0 and spin-2 poles at imaginary squared momentum** (complex masses). Despite these poles, the resulting scattering amplitudes are:
- **Compatible with unitarity bounds**
- **Causal**
- **Scale-free at trans-Planckian energy**

**Ghost fate mechanism:** The ghost pole does not simply disappear — it gets replaced by an infinite tower of complex poles. These complex poles do not contribute to the absorptive part of scattering amplitudes and can be consistently excluded from the physical spectrum.

**Significance:** This is the closest the AS literature comes to providing a concrete mechanism for the ghost's fate. The complex pole tower is reminiscent of the Lee-Wick mechanism, where complex conjugate poles ensure unitarity at the cost of micro-causality violations at short distances.

---

## 6. CDT Evidence

CDT (Ambjorn, Loll, Jurkiewicz) does **not** resolve individual propagating modes. Observables are geometric (volume profiles, spectral dimensions, Hausdorff dimension). CDT cannot currently tell us whether the ghost is present or absent in the non-perturbative spectrum.

**Indirect hint:** The spectral dimension flowing to d_s ≈ 2 at short distances is consistent with higher-derivative gravity (p⁴ propagators), but is not specific to the ghost.

---

## 7. Mass Gap in R² Gravity (arXiv:2501.16445)

**Paper:** Frasca (2025) — "Mass gap in non-perturbative quadratic R² gravity via Dyson-Schwinger"

Studies only the **scalar sector** (scalaron from R² term) using Dyson-Schwinger equations. The mass gap M²_G ~ √R increases with the Ricci scalar. However:
- **Does NOT address the spin-2 ghost** (only the scalaron)
- **Does NOT include the Weyl-squared sector** (C²)
- Authors reference fakeon/Lee-Wick approaches for ghost handling as "beyond the scope"

**Assessment:** Irrelevant to the spin-2 ghost question. Applies only to the scalar sector.

---

## 8. Holdom-Ren Ghost Confinement Conjecture

**Papers:** "A QCD analogy for quantum gravity" (PRD 93, 124030, 2016) [arXiv:1512.05305] and "Quadratic gravity: from weak to strong" (IJMPD 25, 1643004, 2016) [arXiv:1605.05006]

### The Conjecture

Just as QCD's gluon "does not appear in the physical spectrum" through confinement, the spin-2 ghost in quadratic gravity should similarly vanish from the physical spectrum at strong coupling. The Planck mass M_Pl sets the confinement scale (analogous to Λ_QCD).

### Proposed Mechanism

Two scenarios for the ghost propagator ~G(k²)/k⁴:

- **Case A (softening):** Propagator softens to 1/k² with positive residue, no mass gap. Ghost pole transforms into a zero → massless physical graviton.
- **Case B (confinement):** Mass gap develops, all perturbative propagating modes removed from spectrum. Ghost pole vanishes entirely.

### Evidence Provided

- Gribov copies exist in gravity (shown for spherically symmetric metrics)
- Measure factor 1/(1+N_F(h)) suppresses IR physics
- Lattice QCD analogy (referenced, not computed for gravity)

### Limitations (acknowledged by authors)

1. "Presently we lack more direct arguments as to why the analogy should hold."
2. No lattice formulation of asymptotically free gravity exists
3. Non-locality concerns near M_Pl
4. M parameter instability from matter sector corrections
5. Black hole formation may block super-Planckian probes

**Assessment:** The conjecture is structurally motivated but has zero non-perturbative evidence specific to gravity. It remains a heuristic guide.

---

## 9. Synthesis and Verdict

### What the literature says: Three proposed mechanisms, zero confirmations

| Mechanism | Proposed by | Evidence | Status |
|-----------|-------------|----------|--------|
| Ghost confinement (QCD analogy) | Holdom & Ren (2016) | Heuristic only | Conjecture |
| Ghost mass → ∞ at NGFP | Becker et al. (2017) | Proven for scalar ghosts | Not shown for spin-2 |
| Fictitious ghost (truncation artifact) | Platania & Wetterich (2020) | Conceptual framework | Not demonstrated for Stelle ghost |
| Complex pole tower (form factors) | Draper, Knorr et al. (2020) | Computed for AS propagator | Most concrete but incomplete |

### Key observation

The non-perturbative AS literature has **not directly confronted** the massive spin-2 ghost. The field has developed sophisticated tools (spectral reconstruction, form factors, FRG for higher-derivative operators), but these tools have mostly been applied to:
- The massless graviton sector (Bonanno et al.)
- Scalar matter ghosts (Becker et al.)
- Abstract truncation convergence (Platania & Wetterich)
- Form factor phenomenology without explicit ghost identification (Draper et al.)

The spin-2 ghost from C² in Stelle's theory occupies a **blind spot** — it is acknowledged as an issue, multiple frameworks *could* address it, but no paper has carried out the definitive calculation.

### Does ghost confinement/suppression "naturally emerge" from AS?

**No, not naturally.** But it's not excluded either. The ingredients are there:
1. The Becker et al. mechanism (ghost mass → ∞) works for scalars and *could* generalize
2. The Platania-Wetterich argument (fictitious ghosts) provides a plausible escape
3. The Draper et al. complex pole tower shows how unitarity survives with ghost-like poles

None of these constitutes a dynamical derivation of ghost confinement from first principles within AS.

### Verdict: **INCONCLUSIVE**, leaning SUPPORTS

The AS framework has multiple *consistent* mechanisms for removing the ghost from the physical spectrum, and no result that requires the ghost to persist. The complex pole tower (Draper et al.) is the most concrete positive signal — it shows ghost-like poles naturally migrating to complex momenta where they don't affect unitarity. However, no one has directly shown that AS dynamics *forces* the ghost out. The literature is structurally permissive but not demonstrative.

**The bridge between QG+F and AS at the ghost level remains unbuilt.** The fakeon prescription (Anselmi) removes the ghost by fiat at the perturbative level; AS has plausible mechanisms that *could* achieve the same thing dynamically, but this has not been proven. This is the single most important open calculation for the QG+F = AS conjecture.
