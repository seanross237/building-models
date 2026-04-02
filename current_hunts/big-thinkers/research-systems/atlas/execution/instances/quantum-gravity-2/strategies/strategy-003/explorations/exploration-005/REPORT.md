# Exploration 005: Black Hole Prediction Compatibility — QG+F vs Asymptotic Safety

## Goal

Can QG+F's Schwarzschild BH prediction be reconciled with AS's modified BH (running G, singularity resolution, Planck remnants)? Is this a perturbative vs non-perturbative split, or a genuine incompatibility?

## 1. The Apparent Contradiction — Stated Precisely

The two frameworks make the following predictions for static black holes:

**QG+F (perturbative):**
- Lichnerowicz theorem: All static BHs in quadratic gravity have R = 0. The R² term drops out; only C² (Weyl²) modifies GR.
- Three solution families exist (Lü-Perkins-Pope-Stelle 2015): Schwarzschild, non-Schwarzschild attractive, non-Schwarzschild repulsive.
- Fakeon prescription selects Schwarzschild: the ghost is purely virtual → Yukawa charge S₂⁻ = 0 → only Schwarzschild is physical.
- Singularity NOT resolved. Classical Schwarzschild singularity persists.
- Corrections: Wald entropy = A/(4G) + O(l_P²/r_H²). Hawking radiation indistinguishable from GR.
- Evaporation endpoint: No prediction (perturbative expansion breaks down).

**AS (non-perturbative):**
- G(r) → 0 near r = 0 (gravitational anti-screening at the NGFP).
- Two-horizon structure (outer + inner, resembles Reissner-Nordström).
- Singularity RESOLVED: de Sitter core replaces the central singularity.
- Planck-mass remnants: T → 0 as M → M_P. Evaporation halts.
- Modified entropy, QNMs, and grey-body factors from running G(k).
- Parameter α > 1 required for complete resolution (directly related to anomalous dimension at NGFP).

These predictions look contradictory: one says "Schwarzschild, singular, no remnant," the other says "modified metric, regular core, cold remnant." But the question is whether they describe the same physics in different regimes.

## 2. The QCD Analogy — The Resolution Framework

The Holdom-Ren analogy (2015, 2024) provides the precise conceptual framework for resolving this:

| Feature | QCD | Quadratic Gravity |
|---------|-----|-------------------|
| UV behavior | Asymptotically free (g_s → 0) | AF in f₂ (Weyl² coupling) |
| Strong-coupling scale | Λ_QCD ~ 200 MeV | M_P ~ 10¹⁹ GeV (conjectured) |
| Perturbative regime | E >> Λ_QCD | E >> M_P (or r << l_P) |
| Non-perturbative regime | E ~ Λ_QCD | E ~ M_P (or r ~ l_P) |
| Perturbative prediction | Parton model (quarks, gluons) | Schwarzschild + tiny corrections |
| Non-perturbative prediction | Confinement, hadrons | Modified BH, remnants |

In QCD, perturbative calculations (parton model) and non-perturbative results (confinement, hadron spectrum) are not contradictory — they describe the same theory in different regimes. Nobody says the parton model "contradicts" confinement. They are complementary descriptions with a smooth (but non-perturbatively controlled) transition between them.

**The same logic applies here.** QG+F's Schwarzschild prediction is a perturbative result valid for r >> l_P (equivalently, M >> M_P). AS's modified BH is a non-perturbative result valid for r ~ l_P (equivalently, M ~ M_P). Neither is wrong — they have different domains of validity.

## 3. Evidence for Compatibility — Five Arguments

### Argument 1: QG+F's Own Admission of Non-Perturbative Blindness

Anselmi explicitly acknowledges (JHEP 01 (2026) 104, arXiv:2510.05276) that classicized field equations — the basis for QG+F's BH predictions — miss non-perturbative effects. He calls this a "new type of uncertainty." This is not a minor caveat; it is an admission that the perturbative framework cannot access the physics that AS describes.

The QG+F prediction "BHs are Schwarzschild" should be read as: "BHs are Schwarzschild *to all orders in perturbation theory.*" This is entirely consistent with non-perturbative modifications near the singularity.

### Argument 2: The Perturbative Expansion Breaks Down Exactly Where AS Takes Over

QG+F corrections are suppressed by (l_P/r_H)² ~ (M_P/M_BH)². For astrophysical BHs, this is 10⁻⁷⁶ to 10⁻⁹⁶ — negligible. But as M_BH → M_P during evaporation, the corrections become O(1) and the perturbative expansion loses all predictive power.

This is precisely where AS's non-perturbative machinery becomes relevant. The running G(k) → g*/k² at the NGFP is invisible in any finite-order perturbative expansion. The smooth transition from Schwarzschild (perturbative, large BH) to de Sitter core (non-perturbative, Planck BH) is controlled by the full RG flow, not accessible to perturbation theory.

### Argument 3: Branch Crossing at Planck Scale — The Phase Transition

The Bonanno-Silveravalle-Zuccotti work (2024, arXiv:2409.16690) shows that the Schwarzschild and non-Schwarzschild branches cross at a critical horizon radius r_H ≈ 0.876/m₂. For m₂ ~ M_P, this crossing occurs at sub-Planckian radii.

Below this crossing, Schwarzschild is linearly unstable — even infinitesimal perturbations grow exponentially. This instability is driven by the massive spin-2 mode (the ghost). Three scenarios for what happens:
1. Continue as small Schwarzschild (EXCLUDED — unstable)
2. Transition to large Yukawa-attractive BH (EXCLUDED — incompatible with our universe)
3. Transition to Yukawa-repulsive BH (the only viable direction)

This branch crossing acts as a **phase transition** in BH physics at the Planck scale. It marks precisely the boundary where perturbative QG+F predictions (Schwarzschild) give way to non-perturbative physics. Under the "ghost-as-physical" treatment, the endpoint is an exotic naked singularity. Under AS, the endpoint is a regular remnant. Under QG+F = AS, the fakeon prescription implemented non-perturbatively should reproduce the AS result.

### Argument 4: AS Agrees With QG+F in the Perturbative Regime

The Bonanno-Reuter metric:

    f(r) = 1 - 4G₀m r² / [2r³ + g*⁻¹ ξ² G₀(2r + 9mG₀)]

At large r (r >> l_P), this reduces to:

    f(r) ≈ 1 - 2G₀m/r + O(l_P²/r²)

which is exactly Schwarzschild + tiny corrections — precisely what QG+F predicts. The two frameworks agree quantitatively in the regime where perturbation theory is valid. The modifications only become significant at r ~ l_P, where QG+F's perturbative expansion cannot reach.

### Argument 5: Holdom-Ren Phase Transition

Holdom & Ren (PRD 109, 086005, 2024) explicitly propose that quadratic gravity undergoes a phase transition at the Planck scale:
- Above M_P: the full QG spectrum (graviton + massive scalar + spin-2 ghost)
- Below M_P: strongly coupled phase, massless graviton only, ghost confined

Black hole physics near the singularity (curvatures ~ M_P⁴) is deep in the strongly coupled phase. The perturbative BH prediction (Schwarzschild) is the "partonic" description — correct at weak coupling (large BH). The AS modified BH is the "hadronic" description — correct at strong coupling (near singularity, Planck BH). The phase transition is the bridge.

## 4. Bonanno (2025) "Spontaneous Ghostification" — A Complication

The Bonanno-Silveravalle (May 2025, arXiv:2505.20360) paper proposes that the ghost destabilizes Schwarzschild at late evaporation stages, triggering a transition to a "stable exotic naked singularity." This resembles spontaneous scalarization: the BH acquires "ghost Yukawa hair."

**Critical assessment for the QG+F = AS conjecture:**

This paper treats the ghost as physical (not as a fakeon). Under the fakeon prescription, this effect is suppressed perturbatively. But non-perturbatively? There are three possibilities:

1. **Fakeon wins non-perturbatively:** The ghost remains purely virtual even non-perturbatively → spontaneous ghostification doesn't occur → AS remnant is the correct endpoint. This is the "QG+F = AS" scenario.

2. **Ghost is physical:** Spontaneous ghostification occurs → naked singularity endpoint. This contradicts AS's remnant prediction and would FALSIFY QG+F = AS.

3. **Something else:** The non-perturbative dynamics produces a result that neither the perturbative fakeon nor the ghost-as-physical treatment can access.

The ghost's fate at strong coupling remains the central unresolved question (see ghost-fate-strong-coupling assessment: INCONCLUSIVE, four proposed mechanisms, zero confirmations). The spontaneous ghostification paper does not change this — it simply shows what happens in one particular treatment (ghost as physical), which is precisely the treatment that the fakeon prescription rejects.

**Key point:** Spontaneous ghostification is not an obstacle to compatibility. It's a prediction of the *wrong* version of the theory (ghost-as-physical). The right question is what happens when the fakeon is implemented non-perturbatively, and AS's answer (singularity resolution, remnant) is one possible non-perturbative completion.

## 5. Planck Remnants — No Internal Inconsistency

If QG+F = AS, the unified theory predicts Planck remnants. Does this create inconsistency with QG+F's perturbative predictions?

**No.** QG+F makes *no prediction* about evaporation endpoints. Its perturbative expansion breaks down at M ~ M_P, at which point it explicitly cannot say what happens. The remnant prediction is a non-perturbative result that fills this gap. There is no conflict — only complementarity.

The logic is analogous to QCD: perturbative QCD cannot predict the pion mass (a non-perturbative quantity). This does not contradict perturbative QCD — it simply lies outside its domain. Similarly, Planck remnants lie outside perturbative QG+F's domain.

## 6. Domain of Validity — The Precise Split

| Regime | Valid description | Key parameter |
|--------|------------------|---------------|
| r >> l_P, M >> M_P | QG+F perturbative (Schwarzschild + tiny corrections) | (l_P/r)² << 1 |
| r ~ l_P, M ~ M_P | AS non-perturbative (modified metric, de Sitter core) | G(k) running, NGFP controls |
| Evaporation endpoint | AS (Planck remnant, T → 0) | Full beta function needed |

The transition between regimes is smooth and controlled by the RG flow:
- G(k) ≈ G₀ for k << M_P (QG+F perturbative regime)
- G(k) → g*/k² for k >> M_P (AS non-perturbative regime)

## 7. What Would Genuine Incompatibility Look Like?

The predictions would be genuinely incompatible if:
1. QG+F's perturbative BH predictions contradicted AS even at large r (they don't — both give Schwarzschild + O(l_P²/r²))
2. The mathematical structure of QG+F forbade non-perturbative modifications of the Schwarzschild singularity (it doesn't — Anselmi acknowledges non-perturbative uncertainty)
3. AS's singularity resolution required physics inconsistent with QG+F's UV structure (this hasn't been shown — both share the same action with R + R² + C²)
4. The fakeon prescription were provably incompatible with G(k) → 0 at the NGFP (this hasn't been investigated)

None of these conditions are met. The predictions are not mathematically inconsistent; they describe different regimes.

## 8. Caveats and Open Questions

1. **No proof that QG+F perturbative regime smoothly connects to AS non-perturbative regime.** The compatibility is conceptually clean but mathematically undemonstrated. Nobody has shown a smooth interpolation from Schwarzschild + perturbative corrections → Bonanno-Reuter metric with de Sitter core.

2. **The α > 1 requirement for singularity resolution** in AS is tied to the anomalous dimension at the NGFP. If QG+F = AS, the quadratic gravity couplings must flow to a fixed point where this condition holds. Not proven but not excluded.

3. **Ghost fate remains the key bottleneck.** The BH prediction compatibility is downstream of the ghost question. If the ghost is NOT removed non-perturbatively (i.e., fakeon fails at strong coupling), then spontaneous ghostification may occur, producing a naked singularity rather than a remnant. This would break compatibility.

4. **The Draper-Knorr-Saueressig complex pole tower** — the most concrete mechanism for ghost removal in AS — suggests unitarity survives with ghost-like poles replaced by complex pole towers. This is compatible with both the fakeon prescription (perturbative ghost removal) and AS remnants (non-perturbative BH physics), but the connection is not made explicit.

## 9. Verdict: SUPPORTS

**The BH predictions of QG+F and AS are compatible.** They describe the same physics in different regimes — perturbative (large BHs, r >> l_P) and non-perturbative (Planck-scale BHs, r ~ l_P) — exactly as perturbative QCD and non-perturbative QCD describe the same theory.

**Evidence for SUPPORTS:**
- QG+F admits non-perturbative blindness (Anselmi 2026)
- Both frameworks agree quantitatively at large r
- QG+F's perturbative expansion breaks down precisely where AS takes over
- Planck remnants fill a gap that QG+F explicitly cannot address
- The QCD analogy (Holdom-Ren) provides a precise structural mapping

**Evidence against (considered but insufficient for FALSIFIES):**
- No explicit mathematical interpolation between Schwarzschild and BR metric
- Ghost fate unresolved — if ghost survives non-perturbatively, naked singularity (not remnant) may result
- Spontaneous ghostification paper assumes ghost is physical (contradicts fakeon)

**Key takeaway:** The BH sector does NOT falsify QG+F = AS. The apparent contradiction dissolves once you recognize that QG+F's Schwarzschild prediction is perturbative while AS's modified BH is non-perturbative. This is the expected structure of a unified theory with both weak-coupling and strong-coupling regimes.
