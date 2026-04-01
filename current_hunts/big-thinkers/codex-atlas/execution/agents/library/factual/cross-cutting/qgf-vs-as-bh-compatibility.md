---
topic: cross-cutting
confidence: provisional
date: 2026-03-26
source: exploration-005-bh-compatibility (quantum-gravity-2 strategy-003)
---

# QG+F vs. AS Black Hole Compatibility Analysis

Systematic assessment of whether QG+F's perturbative BH predictions (Schwarzschild, singular, no remnant) are compatible with AS's non-perturbative BH predictions (modified metric, regular de Sitter core, Planck remnant). **Verdict: SUPPORTS — the predictions are compatible.** The apparent contradiction dissolves once you recognize that QG+F describes the perturbative regime (r >> l_P) while AS describes the non-perturbative regime (r ~ l_P), exactly as perturbative QCD and non-perturbative QCD describe the same theory.

## The Apparent Contradiction

| Feature | QG+F (perturbative) | AS (non-perturbative) |
|---------|---------------------|----------------------|
| Metric | Schwarzschild (S₂⁻ = 0 via fakeon) | Bonanno-Reuter modified (running G) |
| Singularity | NOT resolved (perturbative expansion cannot reach r ~ l_P) | RESOLVED (G(r) → 0, de Sitter core) |
| Evaporation endpoint | No prediction (expansion breaks down) | Planck-mass remnant (T → 0) |
| Entropy | A/(4G) + O(l_P²/r_H²) | Modified by running G(k) |
| QNMs | Standard + virtual massive modes | Modified via G(k) |

These look contradictory, but the key question is whether they describe the same physics in different regimes.

## Resolution: Perturbative vs. Non-Perturbative Complementarity

The resolution is the QCD analogy (Holdom-Ren 2015/2024; see `quadratic-gravity-fakeon/qcd-analogy-ghost-confinement.md`). In QCD, the parton model (perturbative) and confinement (non-perturbative) are not contradictory — they describe different regimes of the same theory. The same logic applies to QG+F and AS BH predictions.

### Domain of Validity

| Regime | Valid description | Key parameter |
|--------|------------------|---------------|
| r >> l_P, M >> M_P | QG+F perturbative: Schwarzschild + O(l_P²/r²) corrections | (l_P/r)² << 1 |
| r ~ l_P, M ~ M_P | AS non-perturbative: modified metric, de Sitter core | G(k) running, NGFP controls |
| Evaporation endpoint | AS: Planck remnant, T → 0 | Full beta function needed |

The transition is smooth, controlled by the RG flow: G(k) ≈ G₀ for k << M_P (QG+F regime) → G(k) → g*/k² for k >> M_P (AS regime).

## Five Arguments for Compatibility

### 1. QG+F Admits Non-Perturbative Blindness

Anselmi explicitly acknowledges (JHEP 01 (2026) 104, arXiv:2510.05276) that classicized field equations miss non-perturbative effects — a "new type of uncertainty." QG+F's prediction "BHs are Schwarzschild" means "Schwarzschild to all orders in perturbation theory," which is entirely consistent with non-perturbative modifications near the singularity.

### 2. Perturbative Breakdown at Exact AS Takeover Point

QG+F corrections are suppressed by (l_P/r_H)² ~ (M_P/M_BH)². For astrophysical BHs: 10⁻⁷⁶ to 10⁻⁹⁶ (negligible). As M_BH → M_P during evaporation, corrections become O(1) and the perturbative expansion loses predictive power — precisely where AS's non-perturbative machinery (running G, NGFP) becomes relevant. The running G(k) → g*/k² at the NGFP is invisible in any finite-order perturbative expansion.

### 3. Branch Crossing as Phase Transition Boundary

The Schwarzschild and non-Schwarzschild solution branches cross at r_H ≈ 0.876/m₂ (Bonanno-Silveravalle-Zuccotti 2024, arXiv:2409.16690). Below this crossing, Schwarzschild is **linearly unstable** — infinitesimal perturbations grow exponentially, driven by the massive spin-2 mode. Three scenarios:

1. Continue as small Schwarzschild — **EXCLUDED** (unstable)
2. Transition to Yukawa-attractive BH — **EXCLUDED** (incompatible with our universe)
3. Transition to Yukawa-repulsive direction — **only viable option**

This branch crossing marks precisely the boundary where perturbative QG+F predictions give way to non-perturbative physics. Under QG+F = AS, the fakeon prescription implemented non-perturbatively should reproduce the AS result (regular remnant rather than naked singularity).

### 4. Quantitative Agreement at Large r

The Bonanno-Reuter metric at large r (r >> l_P) reduces to:

    f(r) ≈ 1 - 2G₀m/r + O(l_P²/r²)

This is exactly Schwarzschild + tiny corrections — precisely what QG+F predicts. The two frameworks agree quantitatively in the regime where perturbation theory is valid.

### 5. Holdom-Ren Phase Transition

Holdom & Ren (PRD 109, 086005, 2024) explicitly propose a phase transition at M_P: above M_P the spectrum contains graviton + massive scalar + spin-2 ghost; below M_P, strongly coupled phase with massless graviton only (ghost confined). BH physics near the singularity (curvatures ~ M_P⁴) is deep in the strongly coupled phase. Schwarzschild is the "partonic" description (weak coupling, large BH); AS modified BH is the "hadronic" description (strong coupling, Planck BH).

## Spontaneous Ghostification: Not an Obstacle

Bonanno-Silveravalle (May 2025, arXiv:2505.20360) propose that treating the ghost as physical leads to spontaneous ghostification: Schwarzschild destabilized at late evaporation → stable exotic naked singularity. This treats the ghost as physical, which the fakeon prescription rejects. Three possibilities for QG+F = AS:

1. **Fakeon wins non-perturbatively** → ghost remains virtual → spontaneous ghostification doesn't occur → AS remnant is the correct endpoint. This IS the QG+F = AS scenario.
2. **Ghost is physical** → spontaneous ghostification occurs → naked singularity endpoint. Would **FALSIFY** QG+F = AS.
3. **Something else** → non-perturbative dynamics produces a result inaccessible to either treatment.

The ghost's fate at strong coupling remains the central unresolved question (see `asymptotic-safety/ghost-fate-strong-coupling.md`: INCONCLUSIVE, 4 mechanisms, 0 confirmations).

## Planck Remnants: No Internal Inconsistency

QG+F makes **no prediction** about evaporation endpoints — its perturbative expansion breaks down at M ~ M_P. AS's Planck remnant prediction fills this gap without creating conflict, just as the pion mass (a non-perturbative quantity) does not contradict perturbative QCD.

## What Would Constitute Genuine Incompatibility

The predictions would be genuinely incompatible only if:

1. QG+F contradicted AS even at large r — **not the case** (both give Schwarzschild + O(l_P²/r²))
2. QG+F's mathematical structure forbade non-perturbative singularity modification — **not the case** (Anselmi acknowledges non-perturbative uncertainty)
3. AS's singularity resolution required physics inconsistent with QG+F's UV structure — **not shown** (both share R + R² + C² action)
4. Fakeon prescription were provably incompatible with G(k) → 0 at NGFP — **not investigated**

None of these conditions are met.

## Caveats and Open Questions

1. **No mathematical interpolation proof.** The compatibility is conceptually clean but nobody has shown a smooth interpolation from Schwarzschild + perturbative corrections → Bonanno-Reuter metric with de Sitter core.
2. **α > 1 requirement.** AS requires α > 1 (related to anomalous dimension at NGFP) for complete singularity resolution. If QG+F = AS, the couplings must flow to an NGFP satisfying this. Not proven, not excluded.
3. **Ghost fate is the key bottleneck.** BH compatibility is downstream of the ghost question. If the ghost survives non-perturbatively (fakeon fails at strong coupling), spontaneous ghostification may produce naked singularity rather than remnant, breaking compatibility.
4. **Draper complex pole tower** — the most concrete mechanism for ghost removal in AS — is compatible with both fakeon (perturbative ghost removal) and AS remnants (non-perturbative BH physics), but the connection is not explicit.

## Verdict: SUPPORTS

**Evidence for SUPPORTS:**
- QG+F admits non-perturbative blindness (Anselmi 2026)
- Both frameworks agree quantitatively at large r
- Perturbative expansion breaks down precisely where AS takes over
- Planck remnants fill a gap QG+F cannot address
- QCD analogy (Holdom-Ren) provides precise structural mapping

**Evidence against (considered but insufficient for FALSIFIES):**
- No explicit mathematical interpolation
- Ghost fate unresolved
- Spontaneous ghostification (ghost-as-physical only)

**Bottom line:** The BH sector does NOT falsify QG+F = AS. The apparent contradiction dissolves once you recognize perturbative vs. non-perturbative regime complementarity.

Cross-references: `quadratic-gravity-fakeon/black-hole-predictions.md`, `asymptotic-safety/black-holes-and-singularity-resolution.md`, `quadratic-gravity-fakeon/qcd-analogy-ghost-confinement.md`, `asymptotic-safety/ghost-fate-strong-coupling.md`, `cross-cutting/qgf-vs-as-cmb-discrimination.md` (parallel CMB sector analysis)

Sources: Holdom & Ren (2015, 2024); Bonanno-Silveravalle-Zuccotti (2024, arXiv:2409.16690); Bonanno-Silveravalle (May 2025, arXiv:2505.20360); Anselmi (JHEP 01 (2026) 104, arXiv:2510.05276); Lü-Perkins-Pope-Stelle (2015); Bonanno & Reuter (2000)
