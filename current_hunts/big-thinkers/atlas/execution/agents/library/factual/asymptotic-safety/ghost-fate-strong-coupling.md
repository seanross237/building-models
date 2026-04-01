---
topic: asymptotic-safety
confidence: provisional
date: 2026-03-26
source: exploration-003-ghost-fate-strong-coupling (quantum-gravity-2 strategy-003)
---

# Fate of the Spin-2 Ghost at Strong Coupling in Asymptotic Safety

## Critical Gap

The mainstream AS program (Reuter, Saueressig, Percacci, Eichhorn) has **not directly confronted** the massive spin-2 ghost from the Weyl-squared (C²) term in Stelle's theory. The FRG approach tracks running couplings (G, Λ, higher-derivative couplings) rather than reconstructing the full dressed propagator with its pole structure. **The ghost pole's fate is largely implicit in the running couplings, not explicitly tracked.**

No paper has been found that computes the full non-perturbative dressed propagator of the massive spin-2 mode in the AS framework and checks whether the ghost pole persists, moves to complex momenta, or disappears. The spin-2 ghost occupies a **blind spot** in the AS literature.

### Closest Existing Computation: Knorr & Saueressig (2022)

**Paper:** Knorr & Saueressig (2022, SciPost Phys. 12, 001) — Reconstructed the graviton propagator from Euclidean FRG data. Found:
- The spectral function of the **background** graviton necessarily has negative parts (ghost-like contributions)
- The **dynamical** graviton spectral function is positive
- However, this was done in an **Einstein-Hilbert truncation** — no C² term included

This is the closest the literature comes to a direct propagator reconstruction, but it does not address the Stelle ghost because the truncation excludes the Weyl-squared term that generates it. The methodology (momentum-dependent form factors + spectral reconstruction) is what would be needed for the full C²-extended calculation.

See `../cross-cutting/unified-qgf-as-framework/discriminating-predictions.md` for the discrimination analysis of this computation.

## Four Proposed Mechanisms, Zero Confirmations

| Mechanism | Proposed by | Evidence | Status |
|-----------|-------------|----------|--------|
| Ghost confinement (QCD analogy) | Holdom & Ren (2016) | Heuristic only | Conjecture |
| Ghost mass → ∞ at NGFP | Becker, Ripken, Saueressig (2017) | Proven for scalar ghosts | Not shown for spin-2 |
| Fictitious ghost (truncation artifact) | Platania & Wetterich (2020) | Conceptual framework | Not demonstrated for Stelle ghost |
| Complex pole tower (form factors) | Draper, Knorr, Ripken, Saueressig (2020) | Computed for AS propagator | Most concrete but incomplete |

### Mechanism 1: Ghost Confinement (Holdom-Ren)

See `quadratic-gravity-fakeon/qcd-analogy-ghost-confinement.md` for full treatment. Two proposed scenarios for the ghost propagator ~G(k²)/k⁴:
- **Case A (softening):** Propagator softens to 1/k² with positive residue, no mass gap. Ghost pole transforms into a zero → massless physical graviton.
- **Case B (confinement):** Mass gap develops, all perturbative propagating modes removed from spectrum. Ghost pole vanishes entirely.

Evidence: Gribov copies exist in gravity (spherically symmetric metrics), measure factor 1/(1+N_F(h)) suppresses IR physics. But: "Presently we lack more direct arguments as to why the analogy should hold." No lattice formulation of asymptotically free gravity exists. Assessment: structurally motivated but zero non-perturbative evidence specific to gravity.

### Mechanism 2: Ghost Mass → ∞ at NGFP (Becker et al. 2017)

**Paper:** Becker, Ripken, Saueressig — "On avoiding Ostrogradski instabilities within Asymptotic Safety" (arXiv:1709.09098)

Studies gravity coupled to scalar fields with higher-derivative terms (□² in the scalar sector). Three families of NGFPs found:
- **NGFP₀ (y* = 0):** Higher-derivative coupling vanishes exactly → ghost mass μ² = 1/Y → ∞ for all RG scales k. Ghost decouples completely.
- **NGFP± (y* ≠ 0):** Ghost mass μ² = k²/y* → ∞ as k → ∞, so ghost decouples in the deep UV.
- **IR behavior:** For Type IIa trajectories, y_k → 0 in the IR, so ghost also decouples at low energies.

**CRITICAL CAVEAT:** Applies to **scalar field ghosts only**, not the gravitational spin-2 ghost. The gravitational sector remains at Einstein-Hilbert level. The authors explicitly state extending to gravitational ghosts "is beyond the present work." The mechanism is a proof of principle only.

### Mechanism 3: Fictitious Ghosts (Platania & Wetterich 2020)

**Paper:** "Non-perturbative unitarity and fictitious ghosts in quantum gravity" (arXiv:2009.06637)

Ghost-like poles in truncated effective actions may be **fictitious** — truncation artifacts whose residues vanish when all symmetry-compatible operators are included. When the effective action contains non-local form factors (branch cuts, logarithms), a finite-order derivative expansion generates spurious poles. As truncation order N increases: fictitious poles approach the boundary of the convergence domain, and their residues decrease monotonically → 0 as N → ∞.

**On the spin-2 ghost:** Does NOT definitively classify Stelle's ghost as fictitious. Proposes a methodology (tracking residue behavior across truncation orders) but does not carry it out for the gravitational ghost. Main conclusion: "Fake ghosts do not indicate a violation of unitarity."

No mention of Anselmi's fakeon prescription — the two frameworks address the same phenomenology from independent angles.

### Mechanism 4: Complex Pole Tower (Draper, Knorr et al. 2020)

**Papers:** "Finite Quantum Gravity Amplitudes — no strings attached" (PRL 125, 181301, 2020) and "Graviton-mediated scattering amplitudes from the quantum effective action" (JHEP 11, 136, 2020; arXiv:2007.04396)

When full momentum-dependent form factors of AS are included, the graviton propagator develops **infinite towers of spin-0 and spin-2 poles at imaginary squared momentum** (complex masses). Despite these poles, scattering amplitudes are:
- Compatible with unitarity bounds
- Causal
- Scale-free at trans-Planckian energy

The ghost pole does not simply disappear — it gets replaced by an infinite tower of complex poles that do not contribute to the absorptive part of scattering amplitudes and can be consistently excluded from the physical spectrum. Reminiscent of the Lee-Wick mechanism (complex conjugate poles ensure unitarity at the cost of micro-causality violations at short distances).

**This is the closest the AS literature comes to a concrete mechanism for the ghost's fate.**

## Related but Negative Results

### Higher-Derivative Couplings Finite at NGFP (Benedetti et al. 2009)

Benedetti, Machado, Saueressig (arXiv:0901.2984, proceedings: 0909.3265) extended FRG to a four-parameter truncation including R² and C². **The higher-derivative couplings are NOT asymptotically free at the NGFP — they reach finite values.** This contrasts with perturbative Stelle theory where couplings are asymptotically free.

**Specific NGFP values (Eq. 12 of 0901.2984):**

| Coupling | Value | Physical meaning |
|----------|-------|------------------|
| g₀* | 0.00442 | Cosmological constant |
| g₁* | −0.0101 | Newton's constant |
| g₂* | 0.00754 | R²-related (dimensionless) |
| g₃* | −0.0050 | C²-related (dimensionless) |

Critical exponents: θ₀ = 2.51, θ₁ = 1.69, θ₂ = 8.40 (UV-attractive), θ₃ = −2.11 (UV-repulsive). Universal product (GΛ)* = 0.427.

**Ghost mass at the NGFP:** m₂²/k² = g₁*/g₃* = 2.02, giving **m₂/k ≈ 1.42**. The ghost mass is approximately 1.4 times the RG cutoff scale — comparable to M_P, neither parametrically large nor small.

**Implication:** Since g₃* = −0.0050 ≠ 0, the C²-related coupling does NOT vanish at the NGFP. The ghost mass stays finite (m₂ ~ M_P). The Becker et al. mass-divergence mechanism is **structurally excluded for the spin-2 ghost.** The NGFP does not remove the ghost through mass divergence — something else must happen.

See `../cross-cutting/unified-qgf-as-framework/ghost-propagator-prediction.md` for the quantitative prediction of what does happen (complex pole tower, pole migration pattern, amplitude equivalence test).

### CDT Cannot Resolve Ghost Modes

CDT (Ambjorn, Loll, Jurkiewicz) does not resolve individual propagating modes. Observables are geometric (volume profiles, spectral dimensions, Hausdorff dimension). CDT cannot currently determine whether the ghost is present or absent in the non-perturbative spectrum. The spectral dimension d_s ≈ 2 at short distances is consistent with higher-derivative gravity but not specific to the ghost.

### Frasca 2025 Mass Gap — Scalar Sector Only

Frasca (arXiv:2501.16445) demonstrates a mass gap in R² gravity via Dyson-Schwinger equations, but studies ONLY the scalar sector (scalaron). Does NOT address the spin-2 ghost and does NOT include C². Irrelevant to the spin-2 ghost question. See `quadratic-gravity-fakeon/qcd-analogy-ghost-confinement.md`.

## Synthesis and Verdict

### Does ghost confinement/suppression "naturally emerge" from AS?

**No, not naturally.** But it is not excluded either. The ingredients are there:
1. Becker et al. mechanism (ghost mass → ∞) works for scalars and *could* generalize
2. Platania-Wetterich argument (fictitious ghosts) provides a plausible escape
3. Draper et al. complex pole tower shows how unitarity survives with ghost-like poles

None constitutes a dynamical derivation of ghost confinement from first principles within AS.

### Verdict: INCONCLUSIVE, leaning SUPPORTS

The AS framework has multiple *consistent* mechanisms for removing the ghost from the physical spectrum, and no result that requires the ghost to persist. The complex pole tower (Draper et al.) is the most concrete positive signal. However, no one has directly shown that AS dynamics *forces* the ghost out. The literature is structurally permissive but not demonstrative.

### The Bridge Remains Unbuilt

The fakeon prescription (Anselmi) removes the ghost by fiat at the perturbative level; AS has plausible mechanisms that could achieve the same dynamically, but this has not been proven. **This is the single most important open calculation for the QG+F = AS conjecture.**

Cross-references: `quadratic-gravity-fakeon/qcd-analogy-ghost-confinement.md`, `swy-two-fixed-points.md`, `af-ngfp-fixed-point-connection.md`, `graviton-propagator.md`
