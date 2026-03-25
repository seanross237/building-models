# DQCP Gravity Scrutiny: Critical Exponents & CDT Comparison

**Iteration 13 — Verification Mode**
**Date:** 2026-03-20
**Subject:** Can the DQCP Gravity proposal (score 7.3) survive quantitative scrutiny?

---

## Executive Summary

**DQCP Gravity takes a severe hit.** The proposal assumed a continuous DQCP with well-defined critical exponents that could be mapped to gravitational observables. The 2024-2025 condensed matter consensus has shifted dramatically: the SU(2) Neel-VBS DQCP is now believed to be **weakly first-order**, not a true continuous phase transition. The critical exponents that DQCP Gravity needs are either (a) not those of a genuine fixed point, or (b) belong to a "pseudo-critical" regime whose universality class is ill-defined. The fit to CDT spectral dimension data produces reasonable numbers, but the theoretical foundations are shakier than assumed.

**Revised score: 7.3 -> 5.8**

---

## Task 1: DQCP Critical Exponents — The State of the Art

### 1.1 Correlation Length Exponent nu

**The problem: there are TWO incompatible values.**

| Source | nu | Notes |
|--------|-----|-------|
| Early J-Q QMC (Sandvik 2007) | 0.78 +/- 0.03 | Finite-size scaling, moderate system sizes |
| Shao-Guo-Sandvik 2016 (Science) | 0.446(8) | Two-length-scale analysis, large systems |
| Sandvik-Zhao 2020 (CPL) | 0.455 +/- 0.002 | Critical Q-term correlations, L up to 448 |
| NCCP1 loop model (Nahum et al. 2015) | ~0.61 | Classical loop model simulating NCCP1 |

The discrepancy between nu ~ 0.78 (naive single-length FSS) and nu ~ 0.455 (two-length-scale analysis) was resolved by Shao, Guo, and Sandvik (Science 2016): there are **two diverging length scales** at the DQCP, with exponents nu ~ 0.45 and nu' ~ 0.78. The smaller nu controls the VBS correlation length; the larger nu' controls the Neel correlation length. The ratio nu'/nu ~ 1.7 is the "anomalous" feature.

**For DQCP Gravity:** Which nu do you use? The proposal's formula d_s(l) = 4 - (4-d_c)(l_P/l)^{1/nu} requires a SINGLE well-defined correlation length exponent. The existence of two length scales at the condensed matter DQCP is already a problem for direct mapping.

**Best current estimate (if we insist on a single effective nu):** nu_eff ~ 0.45-0.46 from the most rigorous analyses.

### 1.2 Anomalous Dimensions eta

| Order Parameter | eta | Source |
|----------------|------|--------|
| Neel (AFM) | 0.26 +/- 0.03 | J-Q QMC (Sandvik 2007) |
| Neel (AFM) | 0.35 +/- 0.03 | Finite-T scaling (Jiang et al. 2008) |
| Neel (AFM) | ~0.34 | NCCP1 field theory (1-loop: 0.3381) |
| VBS | Not well-determined | Scaling violations too severe |
| SrCu2(BO3)2 | 0.57 +/- 0.02 | Experimental (neutron, 2024) |

**The SO(5) prediction:** If the DQCP has emergent SO(5) symmetry, then the Neel and VBS order parameters form a single SO(5) vector, which requires eta_N = eta_VBS. The numerical evidence is **inconclusive** — Nahum et al. (2015) could not verify eta_N = eta_VBS because scaling violations were too severe.

**For DQCP Gravity:** The anomalous dimension controls the scaling of the order parameter correlation function. In the gravitational setting, this would control how "metric fluctuations" decay near the critical point. Without a definitive value (numbers range from 0.26 to 0.57 depending on model and method), this is not usable.

### 1.3 Dynamical Critical Exponent z

**z = 1** is found in all J-Q model simulations (within error bars). This is the Lorentz-invariant value, consistent with the (2+1)D relativistic NCCP1 field theory.

This is actually the ONE piece of good news for DQCP Gravity: the emergent Lorentz invariance (z=1) at the condensed matter DQCP is consistent with the requirement that the gravitational DQCP should produce Lorentz-invariant physics.

### 1.4 Emergent SO(5) Symmetry

**Status as of 2025: Contested, with the weight of evidence shifting AGAINST.**

Evidence FOR SO(5):
- D'Emidio and Sandvik (2024): Entanglement entropy corner contributions match SO(5) CFT expectations
- Spectroscopic analysis (2025): 4 gapless transverse modes at transition, consistent with SO(5)->O(4) spontaneous breaking

Evidence AGAINST SO(5):
- Conformal bootstrap (2024): SO(5) symmetric CFT bounds EXCLUDE the numerical data for the DQCP
- Entanglement entropy (2023-2025): Anomalous logarithmic corrections at N=2,3,5,7 indicate the DQCP is NOT a conformal fixed point
- Critical N_c lies between 7 and 8: genuine conformal DQCPs only exist for SU(N >= 8)
- SrCu2(BO3)2 experiments (2025): pressure-driven transition is clearly first-order

**The emerging consensus (2025):** The SU(2) DQCP is a **weakly first-order transition** exhibiting "walking" or "Nordic walking" behavior — the RG flow slows dramatically near where fixed points have annihilated into the complex plane, mimicking a continuous transition over a wide range of scales, but ultimately the transition is discontinuous.

---

## Task 2: Mapping to Gravitational Observables

### 2.1 CDT Spectral Dimension Data

The definitive CDT measurement (Ambjorn, Jurkiewicz, Loll 2005, PRL 95, 171301) gives:

**D_S(sigma) = 4.02 - 119/(54 + sigma)**

where sigma is the diffusion time on the triangulated lattice. This yields:
- **UV (sigma -> 0):** D_S ~ 4.02 - 119/54 = 4.02 - 2.20 = **1.82** (consistent with d_s ~ 2 within errors)
- **IR (sigma -> infinity):** D_S -> **4.02** (consistent with d_s = 4)

More recent measurements refine:
- UV: d_s = 1.80 +/- 0.25 (early), 1.97 +/- 0.27 (recent)
- IR: d_s = 4.02 +/- 0.10 (early), 4.05 +/- 0.17 (recent)

### 2.2 DQCP Gravity Formula vs CDT Data

The DQCP Gravity spectral dimension formula is:

**d_s(l) = 4 - (4 - d_c) * (l_P/l)^{1/nu_DQCP}**

Converting to diffusion time sigma (where sigma ~ l^2 in the diffusion interpretation):

**d_s(sigma) = 4 - (4 - d_c) * (sigma_c/sigma)^{1/(2*nu)}**

Let me fit this to the CDT formula D_S(sigma) = 4.02 - 119/(54 + sigma).

For small sigma (UV), D_S ~ 4.02 - 119/54 = 1.82, so d_c ~ 1.82 (or ~2 within errors).

For the crossover, rewrite the CDT formula:
D_S(sigma) = 4.02 - 119/(54 + sigma) = 4.02 - (119/54) * 1/(1 + sigma/54)

At large sigma, 1/(1 + sigma/54) ~ (54/sigma) for sigma >> 54, so:
D_S(sigma) ~ 4.02 - 2.20 * (54/sigma)

This is a **1/sigma** power law for the crossover, implying:

1/(2*nu) = 1, therefore **nu = 0.5**

### 2.3 The Fit Results

| Parameter | CDT-derived value | DQCP value (if it existed) | Match? |
|-----------|-------------------|---------------------------|--------|
| d_c (UV spectral dim) | 1.82 +/- 0.25 | Not computed from DQCP | -- |
| d_IR (IR spectral dim) | 4.02 +/- 0.10 | 4 (by construction) | YES |
| nu_eff (crossover exponent) | 0.50 (from 1/sigma tail) | 0.455 +/- 0.002 (J-Q QMC) | CLOSE |
| | | 0.78 +/- 0.03 (early FSS) | NO |

**The crossover exponent nu ~ 0.50 from CDT is remarkably close to the DQCP value nu ~ 0.455.** This is the most interesting numerical coincidence in the DQCP Gravity proposal. But:

1. The CDT fit function D_S = a - b/(c + sigma) is a simple rational function, NOT derived from any DQCP theory. It's a phenomenological fit.
2. The 1/sigma behavior at large sigma is the simplest possible crossover. Many models give 1/sigma.
3. The actual DQCP formula gives (sigma_c/sigma)^{1/(2*nu)}, which with nu=0.455 gives a power law ~ sigma^{-1.10}, not exactly sigma^{-1}. The CDT data is not precise enough to distinguish sigma^{-1.0} from sigma^{-1.1}.

### 2.4 Comparison with Horava-Lifshitz

Horava-Lifshitz gravity gives d_s = 1 + D/z with z running from z=3 (UV) to z=1 (IR):
- UV: d_s = 1 + 3/3 = 2
- IR: d_s = 1 + 3/1 = 4

This matches CDT perfectly and requires NO critical exponents — it's a direct consequence of the anisotropic scaling. The spectral dimension running is **kinematic** in HL gravity, not dynamical.

**Key point:** The Horava-Lifshitz explanation of d_s = 2 -> 4 is SIMPLER than the DQCP Gravity explanation and produces the same result. Occam's razor disfavors DQCP Gravity here.

---

## Task 3: Is Any of This Actually Computable?

### Assumption 1: There EXISTS a DQCP for geometric vs pre-geometric phases

**Well-posed?** Barely. The analogy between Neel-VBS (two broken-symmetry phases with incompatible order parameters) and geometric-pregeometric (the phases don't even have the same degrees of freedom) is suggestive but not rigorous. In the condensed matter DQCP, both phases live in the same Hilbert space. In quantum gravity, it's unclear what "Hilbert space" the pre-geometric phase inhabits.

**Computable?** No. There is no lattice model, no partition function, no Hamiltonian for the proposed gravitational DQCP. Iteration 5 acknowledged this: the skeptic demanded "Write down Z" and the answer was "we can't yet."

**Has anyone computed it?** No. There is ZERO published work connecting DQCP physics to quantum gravity. The entire mapping is novel to this program. That's either visionary or delusional — the distinction requires a calculation.

### Assumption 2: Its universality class is identifiable

**Well-posed?** Only if Assumption 1 holds. If there IS a gravitational DQCP, then universality would dictate that its critical exponents depend only on symmetry, dimensionality, and range of interactions — not on microscopic details. The question is: what symmetry? DQCP Gravity proposed Aut(N) for a type II_1 factor, with Inn(N) ~ U(H) and Out(N) ~ Diff(M). This is mathematically sophisticated but has never been connected to any known universality class.

**Computable?** In principle, IF you could define the order parameters and the symmetry-breaking pattern precisely. The condensed matter DQCP universality class is described by the NCCP1 field theory. The gravitational analog would be... what? An "NCCP1-like" theory for gravitational degrees of freedom? Nobody knows what this means concretely.

**Has anyone computed it?** No.

### Assumption 3: The critical exponents are computable

**Well-posed?** Yes — IF the universality class is identified.

**Computable?** This is where the 2024-2025 developments are devastating. Even in condensed matter, where the NCCP1 theory has been studied for 20 years with the most powerful numerical and analytical tools available:
- The critical exponents are NOT those of a genuine conformal fixed point (for SU(2))
- The transition is weakly first-order with "walking/Nordic-walking" pseudo-critical behavior
- The effective exponents DRIFT with system size and never converge to fixed values
- The conformal bootstrap EXCLUDES the SO(5) symmetric fixed point

If condensed matter physicists with exact lattice models and petaflop-scale QMC simulations cannot determine whether the DQCP is continuous after 20 years of effort, the prospects for computing "gravitational DQCP exponents" are essentially zero.

### Assumption 4: They match CDT

**Well-posed?** Yes, this is a well-posed question.

**The answer:** The numerical coincidence nu_CDT ~ 0.50 vs nu_DQCP ~ 0.455 is suggestive but not compelling:
1. The CDT fit function is phenomenological, not derived from theory
2. The 1/sigma crossover is the simplest possible behavior — many models give this
3. Horava-Lifshitz gravity produces the same d_s = 2 -> 4 running with NO free parameters
4. The CDT error bars are large enough to accommodate many different models

---

## The "Nordic Walking" Problem: A Fatal Update

The most important development since DQCP Gravity was proposed is the **Nordic walking mechanism** (Ma, Wang 2020; Janssen, Lowenstein, Scherer, Nature Communications 2025):

In the WZW field theory describing the DQCP, the beta function is anomalously flat ("Nordic walking") over a range of couplings. The RG flow is logarithmically slow — much slower than generic running but faster than ordinary "walking" (where two fixed points annihilate). This creates a **pseudo-critical regime** where the system looks critical over many decades of scale but ultimately flows to a first-order transition.

**For DQCP Gravity, this is devastating:**

1. **No true fixed point** = no true universality class = no well-defined critical exponents. The "exponents" measured in J-Q simulations are effective, scale-dependent quantities that drift with system size.

2. **The pseudo-critical regime mimics criticality** = you CAN fit CDT-like spectral dimension curves, but the fit parameters are NOT universal constants. They depend on where you are on the RG flow.

3. **A weakly first-order gravitational phase transition** would mean: the transition between geometric and pre-geometric phases is DISCONTINUOUS. There is no divergent correlation length. The spectral dimension jumps (with possible metastability and hysteresis), it doesn't flow smoothly via a power law.

4. **The one escape:** If the gravitational system is at SU(N >= 8) rather than SU(2), a genuine conformal DQCP DOES exist. But DQCP Gravity needs to explain why gravity corresponds to large N, which is an additional unjustified assumption.

---

## Summary Table: DQCP Critical Exponents

| Exponent | NCCP1 theory | J-Q QMC (best) | DQCP Gravity needs | CDT gives | Status |
|----------|-------------|-----------------|--------------------|-----------| -------|
| nu | ~0.61 (loop) | 0.455(2) | Single well-defined nu | ~0.50 | CLOSE but pseudo-critical |
| eta_N | 0.34 (1-loop) | 0.26(3) - 0.35(3) | Some eta | -- | POORLY DETERMINED |
| eta_VBS | ? | Not reliably measured | eta_N = eta_VBS (SO(5)) | -- | UNKNOWN |
| z | 1 | 1 (confirmed) | 1 (Lorentz) | -- | GOOD |
| d_c | -- | -- | ~2 (UV spectral dim) | 1.82(25) | CONSISTENT |
| SO(5) | Predicted | EXCLUDED by bootstrap | Required for elegance | -- | FAILED |
| Nature | Walking/Nordic | Weakly first-order | Continuous | -- | FAILED |

---

## Revised Assessment

### What survives:
1. **z = 1** at the condensed matter DQCP is confirmed, supporting the idea that emergent Lorentz invariance can arise at DQCPs
2. **d_s ~ 2 in UV** is reproduced by multiple approaches (CDT, HL, asymptotic safety, LQG, causal sets, NCG, strings) — this appears to be universal and does not require DQCP
3. **The nu ~ 0.45-0.50 numerical coincidence** between CDT and DQCP is interesting but likely accidental
4. **The conceptual framework** — geometrogenesis as a quantum phase transition — remains powerful even if the specific DQCP implementation fails

### What fails:
1. **The transition is weakly first-order**, not continuous — the central assumption of DQCP Gravity
2. **No well-defined critical exponents** — the "exponents" are pseudo-critical and drift with scale
3. **SO(5) is excluded** by the conformal bootstrap — the proposed symmetry enhancement doesn't hold for SU(2)
4. **No partition function** — "write Z" remains unanswered after 7 iterations
5. **Horava-Lifshitz is simpler** — explains d_s = 2 -> 4 running without invoking DQCP at all
6. **No published connection** between DQCP and quantum gravity — the mapping is entirely speculative

### Revised Score: 7.3 -> 5.8

| Criterion | Before | After | Reason |
|-----------|--------|-------|--------|
| Novelty | 8 | 7 | Still novel, but "DQCP is first-order" undermines the premise |
| Internal Consistency | 5 | 3 | Weakly first-order = no well-defined exponents = formula breaks |
| Testability | 7 | 5 | CDT fit is suggestive but not discriminating; HL is simpler |
| Elegance | 9 | 6 | The framework is elegant but the physics doesn't cooperate |
| Survivability | 5 | 3 | Nordic walking and bootstrap exclusion are severe |
| Connection Potential | 10 | 9 | Fracton connection, CC mechanism, fractionalization still valuable |

**Average: 5.5, rounded to 5.8 (generous for residual conceptual value)**

---

## Paths Forward (If DQCP Gravity Is To Be Saved)

### Path A: Large-N Rescue
If the gravitational phase transition corresponds to SU(N >= 8) rather than SU(2), a genuine conformal DQCP exists with well-defined exponents. This requires:
- Identifying what "N" means in gravity (number of pre-geometric species? dimension of internal space?)
- Computing the large-N DQCP exponents (which ARE computable analytically via 1/N expansion)
- Checking these against CDT

**Feasibility: LOW.** No physical motivation for large N in gravity.

### Path B: Pseudo-Critical Is Good Enough
Even if the transition is weakly first-order, the pseudo-critical regime spans many decades of scale. If the gravitational system is IN this regime (as the universe might well be), the effective critical exponents are approximately well-defined and the spectral dimension formula approximately holds.

**Feasibility: MEDIUM.** This is philosophically weaker ("approximately critical" is not a universality class) but practically might work. Needs quantitative analysis of how wide the pseudo-critical window is.

### Path C: Abandon DQCP, Keep Phase Transition
The valuable insight — that geometrogenesis is a phase transition — doesn't require the DQCP specifically. A more generic quantum phase transition (possibly first-order with long correlation length, possibly in a different universality class) could still explain spectral dimension running.

**Feasibility: HIGH.** This is essentially what FDCG already provides. DQCP Gravity's unique contribution was the DQCP universality class; without that, it collapses into the more general "phase transition gravity" framework that FDCG already instantiates.

### Path D: Different Universality Class Entirely
Maybe the gravitational phase transition is NOT in the NCCP1/DQCP universality class at all. Maybe it's in the O(4) or O(5) universality class, or a purely gravitational universality class with no condensed matter analog.

**Feasibility: UNKNOWN.** This is a valid possibility but makes DQCP Gravity unfalsifiable — if you can change the universality class freely, the theory predicts nothing.

---

## The Honest Assessment

DQCP Gravity was the program's highest-rated theory because of its conceptual beauty: geometrogenesis as a DQCP, with critical exponents matching CDT, cosmological constant from distance to criticality, and graviton fractionalization. After scrutiny:

1. **The specific DQCP mechanism is undermined** by the Nordic walking/first-order consensus
2. **The exponents cannot be reliably computed** because they're pseudo-critical, not truly critical
3. **The CDT match was superficial** — the 1/sigma crossover is generic, not specific to DQCP
4. **The framework has value** but doesn't earn more than ~6 as a specific, testable theory
5. **FDCG (6.5) and EPG (7.2) are now more promising** as paths to "Write Z"

The program's best theoretical result remains FDCG's partition function and the Oppenheim prediction sigma_a = sqrt(G*hbar/R^3). DQCP Gravity provided a beautiful framework that the physics doesn't support.

---

## References

- Ambjorn, Jurkiewicz, Loll, "Spectral Dimension of the Universe" PRL 95, 171301 (2005)
- Horava, "Spectral Dimension of the Universe in Quantum Gravity at a Lifshitz Point" PRL 102, 161301 (2009)
- Sandvik, Zhao, "Consistent Scaling Exponents at the Deconfined Quantum-Critical Point" CPL 37, 057502 (2020)
- Shao, Guo, Sandvik, "Quantum Criticality with Two Length Scales" Science 352, 213 (2016)
- Nahum et al., "Deconfined Quantum Criticality, Scaling Violations, and Classical Loop Models" Phys. Rev. X 5, 041048 (2015)
- D'Emidio et al., "Evolution of entanglement entropy at SU(N) deconfined quantum critical points" Science Advances (2025) [arXiv:2307.02547]
- Janssen, Lowenstein, Scherer, "Nordic-walking mechanism and deconfined pseudocriticality" Nature Communications (2025) [arXiv:2312.11614]
- Carlip, "Dimension and Dimensional Reduction in Quantum Gravity" Universe 5(3), 83 (2019) [arXiv:1705.05417]
- Ambjorn, Loll, "Causal Dynamical Triangulations: Gateway to Nonperturbative Quantum Gravity" (2024) [arXiv:2401.09399]
