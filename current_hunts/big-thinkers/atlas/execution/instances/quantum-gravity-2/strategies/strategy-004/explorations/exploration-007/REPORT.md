# The Unified QG+F–AS Framework

## A Complete Theory Document

### Final Deliverable of the Atlas Quantum Gravity Research Program
### 4 Strategies · 38 Explorations · Honest Assessment

---

## Abstract

The Unified QG+F–AS Framework is a **structural conjecture** proposing that Quadratic Gravity with Fakeons (QG+F) and Asymptotic Safety (AS) are perturbative and non-perturbative descriptions of a single UV-complete quantum gravity theory — analogous to perturbative QCD and lattice QCD describing the same physics in complementary regimes.

After exhaustive prediction extraction across six explorations and rigorous adversarial testing, the framework's status is:

- **Internally consistent** — no falsified predictions, no mathematical contradictions
- **Identifies three critical computations** that could generate genuine discriminating predictions
- **Makes zero novel discriminating predictions** that survive adversarial scrutiny — every claimed prediction is either inherited from one standalone component (QG+F or AS) or currently untestable
- **Practically unfalsifiable** on current timescales for its unification claims specifically

The framework's contribution is **organizational, not predictive**: it explains why both QG+F and AS work, identifies where they overlap, and specifies the precise calculations needed to test whether they are truly one theory. It is a research program, not a finished theory.

---

## I. Core Insight for Non-Specialists

Two of the most promising approaches to quantum gravity — the theory that would unify Einstein's general relativity with quantum mechanics — have developed independently over decades and appeared to be competitors. One approach, Quadratic Gravity with Fakeons (QG+F), adds higher-derivative terms to Einstein's equations, achieving mathematical consistency (renormalizability and unitarity) through a special prescription for handling a problematic "ghost" particle that appears in the theory. This approach works well at very high energies, where calculations are tractable, but breaks down at the Planck scale where gravity becomes extremely strong.

The other approach, Asymptotic Safety (AS), uses non-perturbative methods — powerful mathematical tools that work even when gravity is strong — to show that gravity remains well-defined at all energy scales thanks to a special "fixed point" that controls the theory's behavior. This approach handles Planck-scale physics well (resolving black hole singularities, for example) but has difficulty with the ghost particle that QG+F treats explicitly.

The Unified Framework proposes that these two approaches are not competitors at all — they are **complementary descriptions of the same physics**, like two different maps of the same terrain, each accurate in its own region. QG+F is the correct description at ultra-high energies (above the Planck scale), while AS is correct at and below the Planck scale. Where their domains overlap, they must agree — and the existing evidence suggests they do. If correct, this would mean that quantum gravity is already solved in principle: the theory is four-derivative gravity, and we simply need to develop the mathematical tools to extract its full predictions. The critical caveat is that the unification claim has not yet been proven — it remains a compelling conjecture awaiting three specific calculations that could confirm or refute it.

---

## II. The Theory Statement

### The Action

The unified theory is defined by the most general four-derivative extension of Einstein gravity:

$$S = \int d^4x \sqrt{-g} \left[ \frac{M_P^2}{2} R - \Lambda + \frac{1}{2f_2^2} C_{\mu\nu\rho\sigma} C^{\mu\nu\rho\sigma} + \frac{1}{f_0^2} R^2 \right]$$

where:
- $R$ is the Ricci scalar (Einstein gravity)
- $\Lambda$ is the cosmological constant
- $C_{\mu\nu\rho\sigma}$ is the Weyl tensor; the $C^2$ term introduces a massive spin-2 excitation (the "ghost")
- $R^2$ is the Starobinsky term that drives inflation
- $f_2, f_0$ are dimensionless couplings; $M_P$ is the (reduced) Planck mass

This action is simultaneously:
- The most general renormalizable gravity theory in four dimensions (Stelle 1977)
- The action of QG+F when the ghost is quantized via the fakeon prescription (Anselmi 2017–2018)
- The leading truncation of the effective action at the non-Gaussian fixed point (NGFP) in Asymptotic Safety (Codello & Percacci 2006; Falls, Kluth & Litim 2023)

The identity of the action across both programs is **the foundational observation** that motivates the unification conjecture.

### The Two Complementary Descriptions

**1. The Perturbative Sector (QG+F)**

Above the Planck scale, the Weyl-squared coupling $f_2$ is asymptotically free (Fradkin & Tseytlin 1982). The massive spin-2 excitation is quantized via the fakeon prescription, which preserves unitarity and Lorentz invariance at the cost of S-matrix analyticity. The ghost is a purely virtual particle — it propagates in loops (preserving renormalizability) but never appears in external states (preserving unitarity). This sector controls trans-Planckian scattering, inflationary dynamics (Starobinsky-type from the $R^2$ term), and the perturbative structure of black hole exteriors.

**2. The Non-Perturbative Sector (AS)**

The same theory, treated non-perturbatively via the functional renormalization group (FRG), exhibits a non-Gaussian fixed point (NGFP) — the Reuter fixed point (Reuter 1998). At and below the Planck scale, strong-coupling effects dominate: classical singularities are resolved by gravitational anti-screening ($G(k) \to g_*/k^2$ at high $k$), and Planck-mass remnants form as the stable endpoint of black hole evaporation. This sector controls Planck-scale physics, black hole interiors, and deep-IR cosmological running.

**The key insight:** QG+F and AS are not competing theories. They are two approximation schemes applied to the same underlying dynamics, valid in complementary energy regimes.

### The QCD Analogy

The structural parallel with QCD is the organizing metaphor of the framework:

| Feature | QCD | Unified QG+F–AS |
|---------|-----|------------------|
| UV behavior | Asymptotically free ($g_s \to 0$) | Asymptotically free ($f_2 \to 0$) |
| Running coupling | $\alpha_s(\mu)$ logarithmic | $f_2(\mu)$ logarithmic |
| Dynamical scale | $\Lambda_{\text{QCD}} \sim 200$ MeV | $M_P \sim 10^{19}$ GeV |
| Unphysical DOF (pert.) | Quarks/gluons (colored, confined) | Spin-2 ghost (fakeon, confined) |
| Confinement mechanism | Color confinement, mass gap | Ghost confinement, Planck mass gap |
| Non-perturbative tool | Lattice QCD | FRG / Asymptotic Safety |
| Perturbative tool | pQCD, Feynman diagrams | QG+F, fakeon Feynman rules |
| Fixed point (UV) | Gaussian (AF) | AF fixed point (perturbative) |
| Fixed point (non-pert.) | *N/A (confines first)* | NGFP (Reuter fixed point) |

This analogy was first proposed by Holdom & Ren (2015, 2016) and concretized by Draper et al. (2020), whose complex pole tower result showed the ghost pole dissolving into an infinite tower of complex conjugate pairs — the gravitational analog of quark confinement.

**Critical caveat (from adversarial assessment):** The QCD analogy breaks at three load-bearing joints — see Section III (Evidence Against).

### Regime Structure

| Regime | Energy Scale | Valid Description | Key Physics | Observational Handle |
|--------|-------------|-------------------|-------------|---------------------|
| Trans-Planckian | $E \gg M_P$ | QG+F perturbative | AF in $f_2$; fakeon prescription | Inaccessible |
| Planck-scale | $E \sim M_P$ | Full non-perturbative (AS/FRG) | Ghost confinement; phase transition | Inflation, PBH remnants |
| Sub-Planckian | $E \ll M_P$ | Einstein gravity (GR) | Ghost confined/decoupled | Standard gravity |
| Inflationary | $H \sim H_{\inf}$ | $R^2$ Starobinsky + NGFP corrections | CMB observables | LiteBIRD, Simons Obs. |
| BH exterior | $r \gg l_P$ | QG+F perturbative | Schwarzschild (exact) | EHT, LIGO/Virgo |
| BH interior | $r \sim l_P$ | AS non-perturbative | Singularity resolved; de Sitter core | Future PBH evap. |
| BH evaporation endpoint | $M \sim M_P$ | Phase transition regime | Perturbative → non-perturbative | PBH remnant searches |
| Cosmological IR | $H \sim H_0$ | GR + AS running corrections | Running $G(r)$; potential dark energy | Galaxy rotation (speculative) |

The transition between perturbative and non-perturbative regimes occurs at $E \sim M_P$, where $f_2$ becomes $O(1)$. Three independent lines of evidence locate this transition:

1. **Coupling strength:** The asymptotically free coupling $f_2(\mu)$ runs logarithmically and becomes $O(1)$ at $\mu \sim M_P$, signaling perturbative breakdown.
2. **Ghost mass threshold:** The ghost mass $m_2^2 = M_P^2/(2\alpha_W)$ sets the scale where the massive spin-2 mode becomes dynamically relevant.
3. **BH branch crossing:** Bonanno et al. (2025, arXiv:2505.20360) showed that Schwarzschild becomes linearly unstable below $r_H \approx 0.876/m_2$, triggering a transition to an exotic configuration.

### The RG Flow Picture

Under the Sen-Wetterich-Yamada (SWY, 2022–2023) picture, the unified theory has two distinct UV fixed points:

$$\text{AF (GFP)} \xrightarrow{E \gg M_P} \text{perturbative QG+F} \xrightarrow{E \sim M_P} \text{NGFP crossover} \xrightarrow{E \ll M_P} \text{GR (IR)}$$

Under the alternative Codello-Percacci (2006) picture, the AF and NGFP are the same fixed point seen at different approximation levels, and no connecting trajectory is needed. The SWY picture is more demanding and more testable.

### Bridge Mechanisms

The unified framework identifies five "bridges" — joints where the perturbative and non-perturbative descriptions must connect. These are the framework's technical core and its most vulnerable points.

**Bridge 1: Ghost — Fakeon ↔ Confinement**

At high energies ($E \gg M_P$), where $f_2 \ll 1$, the fakeon prescription exactly removes the ghost from the physical spectrum. As the coupling grows ($E \sim M_P$), the ghost must be dynamically removed by non-perturbative effects. Three candidate mechanisms exist in AS: (1) ghost mass divergence at NGFP (Becker et al. 2017 — proven for scalars only), (2) complex conjugate pole tower (Draper et al. 2020 — general truncation, not specifically the Stelle ghost), (3) fictitious ghost with vanishing residue (Platania & Wetterich 2020). All three are consistent with the fakeon requirement that the ghost never propagates, but none has been demonstrated for the gravitational spin-2 case specifically.

**Bridge 2: Fixed Points — AF ↔ NGFP**

QG+F's UV behavior is controlled by the Gaussian (AF) fixed point. AS's UV behavior is controlled by the NGFP. Two interpretations exist: (a) Codello-Percacci (2006): same fixed point seen at different approximation levels; (b) SWY (2022–2023): two distinct fixed points with different critical exponents. The SWY picture requires a connecting trajectory (AF → NGFP → GR), which has not been computed. This is the framework's central open conjecture.

**Bridge 3: Inflation — Starobinsky ↔ NGFP-Driven**

Both descriptions predict Starobinsky inflation because they describe the same $R^2$ term: QG+F puts it in the action explicitly; AS generates it dynamically from the NGFP. The NGFP additionally predicts logarithmic corrections (the $b$ parameter from Bonanno-Platania) and $R^3$ corrections ($\delta_3$), though both are currently either negligible ($b \sim 10^{-14}$) or uncomputed ($\delta_3$).

**Bridge 4: Black Holes — Schwarzschild ↔ Singularity Resolution**

At large $r$, the Bonanno-Reuter AS metric reduces to Schwarzschild + $O(l_P^2/r^2)$ — exactly the QG+F result. At $r \sim l_P$, AS provides singularity resolution (de Sitter core, two horizons) that perturbative QG+F cannot access. The Bonanno et al. (2025) Schwarzschild instability at $r_H \approx 0.876/m_2$ marks the boundary where the perturbative description breaks down.

**Bridge 5: Analyticity — Fakeon Average Continuation ↔ Obstructed Wick Rotation**

QG+F sacrifices S-matrix analyticity via the "average continuation" (Anselmi 2018). AS has an independent Wick rotation problem (ghost poles obstruct the standard Euclidean-to-Lorentzian transition — Donoghue 2020; Draper et al. 2020). The unified framework proposes that the average continuation resolves AS's Wick rotation problem — a concrete methodological prediction that has not been tested in any actual FRG computation.

---

## III. Evidence For and Against

This section presents the evidence as an honest prosecution-defense scorecard, incorporating the full adversarial assessment from six explorations.

### Supporting Evidence

**S1. Identical action.**
QG+F's action (Stelle 1977, Anselmi 2017) is the most general four-derivative gravity. The NGFP truncation in AS at the four-derivative level produces the same action. Falls, Kluth & Litim (2023) showed the NGFP UV critical surface has exactly as many relevant directions as there are couplings in four-derivative gravity. This is the framework's strongest structural argument.

**S2. Both predict Starobinsky inflation with consistent $r \approx 0.003$.**
QG+F: The $R^2$ term drives Starobinsky inflation with $r \in [4\times10^{-4}, 4\times10^{-3}]$ (Anselmi, Bianchi & Piva 2020; Bianchi & Gamonal 2025).
AS: Multiple groups derive Starobinsky from the NGFP with $r \approx 0.003$ (Codello et al. 2014; Gubitosi et al. 2018).
The predictions cluster around the same value, as expected if they describe the same $R^2$ term.

**S3. Both predict $d_s \to 2$ in the UV.**
Higher-derivative propagators ($\sim 1/p^4$) in QG+F and the universal anomalous dimension $\eta_N = -2$ at the NGFP both give spectral dimension 2 in the UV. (Note: this is universal across essentially all QG approaches — Carlip 2019 — so while consistent, it has low discriminating power.)

**S4. Black hole exterior agreement.**
QG+F predicts exactly Schwarzschild for static BHs (Lichnerowicz theorem + fakeon prescription sets $S_2^- = 0$). The Bonanno-Reuter AS metric reduces to Schwarzschild + $O(l_P^2/r^2)$ corrections at large $r$. The two descriptions agree quantitatively wherever their domains overlap.

**S5. Fakeon average continuation addresses AS's Wick rotation problem.**
AS struggles with Euclidean-to-Lorentzian analytic continuation (ghost poles obstruct the standard Wick rotation — Donoghue 2020; D'Angelo et al. 2024). QG+F's fakeon average continuation (Anselmi 2018) provides a concrete, well-defined replacement. This is a natural resolution if the two theories are one.

**S6. Multiple ghost dissolution mechanisms consistent with fakeon.**
Three independent AS mechanisms (ghost mass divergence — Becker et al. 2017; complex pole tower — Draper et al. 2020; fictitious ghost — Platania & Wetterich 2020) all remove the ghost from the physical spectrum, consistent with the fakeon prescription's requirement that the ghost never propagates.

### Unresolved

**U1. AF → NGFP connecting trajectory not computed.**
The SWY picture requires an RG trajectory connecting the asymptotically free fixed point to the NGFP. This trajectory has never been computed. Its existence is the central open conjecture. Under the Codello-Percacci picture, no trajectory is needed (same fixed point), but this may be a low-truncation artifact.

**U2. Spin-2 ghost confinement not demonstrated.**
No calculation has shown ghost confinement specifically for the gravitational spin-2 ghost. Becker et al. (2017) showed it for scalars only. Draper et al. (2020) used a general truncation, not specifically the Stelle ghost. The most important open calculation.

**U3. NGFP $R^3$ correction $\delta_3$ not mapped to physical parameter.**
The NGFP gives $\tilde{g}_3^* \approx -(0.86\text{–}1.10) \times 10^{-2}$ (Codello et al. 2009), but the mapping from this dimensionless fixed-point value to the physical inflationary correction $\delta_3$ at the relevant energy scale requires a full RG trajectory that has not been computed.

### Evidence Against (from Devil's Advocate — Exploration 006)

**A1. The QCD analogy breaks at its load-bearing joints.**

The analogy is the framework's primary organizing structure, and it fails at three critical points:

*(a) No compact gauge group.* QCD confinement rests on SU(3)'s compact, semisimple gauge group — the Wilson loop area law, center symmetry Z(3), and the Polyakov loop order parameter all require compactness. Gravity's diffeomorphism group is non-compact and infinite-dimensional. The entire mathematical machinery of confinement is absent. This is not a detail — it is the foundation on which QCD confinement is built.

*(b) No quantum number to confine.* In QCD, confinement confines color-charged objects; the color quantum number provides a clean selection rule. The spin-2 ghost carries no analogous quantum number — it has the same spin, couplings, and quantum numbers as the graviton. There is no selection rule separating "ghost-like" from "graviton-like" states non-perturbatively.

*(c) No lattice evidence.* QCD confinement was confirmed by lattice QCD. After 11 years since Holdom & Ren's conjecture (2015), there is: no lattice formulation of $C^2$-extended gravity, no CDT computation including the $C^2$ term, no Monte Carlo evidence for ghost confinement, no numerical evidence of any kind. CDT phase transitions are sometimes cited as supportive, but CDT does not include the $C^2$ term.

**A2. All "predictions" are either inherited from components or untestable.**

A systematic null hypothesis test (H₀: QG+F and AS are separate, compatible theories sharing the same classical action) reveals that every claimed prediction is equally well explained by H₀. No prediction requires unification. The devastating scorecard:

| Prediction | H₀ explains it? | Unification needed? |
|---|---|---|
| Ghost dissolution | Yes (AS generically does this) | No |
| BH remnants | Yes (standalone AS) | No |
| Bounded $r$ | Yes (standalone QG+F) | No |
| Higgs mass | Yes (standalone AS) | No |
| Spectral dimension $d_s \to 2$ | Yes (universal) | No |
| Consistency relation $r = -8n_T$ | Yes (standalone QG+F) | No |
| $\delta_3$ correct sign | Yes (standalone AS $f(R)$) | No |

H₀ is simpler (no confinement mechanism), equally explanatory (same predictions), and more parsimonious (no QCD analogy). By Occam's razor, H₀ should be preferred until the framework produces a prediction H₀ cannot match.

**A3. The framework is practically unfalsifiable on its unification claims.**

Experimentally testable predictions (bounded $r$, consistency relation) test standalone QG+F, not unification. Theoretically testable predictions (ghost pole tower, $\delta_3$ mapping) require calculations nobody has started in over a decade. Planck-scale predictions (BH phase transition, remnants) are forever inaccessible. The framework occupies a comfortable epistemic niche where it cannot be killed but cannot be confirmed.

---

## IV. Predictions — Honest Catalog

Every prediction has been classified through the full adversarial pipeline: initial derivation (Explorations 001–005) followed by six specific attacks (Exploration 006). Classifications below are **post-adversarial** — the final, honest assessment.

### Tier 1: Inherited from QG+F

These are genuine, testable predictions of **Quadratic Gravity with Fakeons**. The unified framework inherits them but adds nothing to them.

**P-QGF-1. Bounded tensor-to-scalar ratio: $r \in [4\times10^{-4}, 4\times10^{-3}]$**
- Source: Anselmi, Bianchi & Piva (2020), JHEP 07, 211
- Mechanism: Fakeon mass constraint $M_2 > M_0/4$ from perturbative unitarity gives the lower bound. Starobinsky inflation gives the upper bound.
- Testability: LiteBIRD (launch ~2032, results ~2036), $\sigma(r) < 10^{-3}$
- Post-adversarial status: **GENUINE PREDICTION** — but of QG+F, not of unification
- Note: The unified framework could in principle sharpen this range to a specific $r$ value (by computing the RG trajectory that fixes $M_2$), but this calculation has not been done. The lower bound $r > 4\times10^{-4}$ is genuinely unique to QG+F — no other quantum gravity approach produces it.

**P-QGF-2. Consistency relation $r = -8n_T$ preserved**
- Source: Bianchi & Gamonal (2025), arXiv:2502.03543
- Mechanism: Fakeon doesn't propagate → no new tensor modes → single-field consistency relation preserved
- Post-adversarial status: **CONSISTENCY CHECK** — non-trivial but expected for any theory without new propagating tensor modes

**P-QGF-3. All other CMB observables match Starobinsky**
- $n_s \approx 1 - 2/N \approx 0.964$–$0.967$ for $N = 50$–$60$
- Spectral index running $dn_s/d\ln k \approx -2/N^2 \approx -6\times10^{-4}$
- Post-adversarial status: Standard Starobinsky predictions. The $n_s$ tension ($n_s^{\text{obs}} = 0.9737 \pm 0.0025$, $2.3\sigma$ above) is a known issue.

### Tier 2: Inherited from AS

These are predictions of **Asymptotic Safety**. The unified framework inherits them, and the fakeon prescription does not alter them.

**P-AS-1. Higgs mass prediction ($m_H \approx 126$ GeV from NGFP boundary condition)**
- Source: Shaposhnikov & Wetterich (2010), confirmed 2012
- Unified framework check: Three independent arguments show the fakeon changes nothing: (1) beta functions are prescription-independent, (2) NGFP is Euclidean (fakeon is Lorentzian), (3) absorptive parts vanish below threshold. Upper bound: $|\Delta m_H| < 10^{-7}$ GeV.
- Post-adversarial status: **CONSISTENCY CHECK (clean pass)** — the unified framework inherits this unchanged

**P-AS-2. Black hole singularity resolution and Planck remnants**
- Source: Bonanno & Reuter (2000, 2006)
- Mechanism: Gravitational anti-screening $G(k) \to g_*/k^2$ at high $k$ → regular de Sitter core → two horizons → Planck-mass remnant ($m_{\text{rem}} \sim 10^{-5}$ g) as stable evaporation endpoint, $T \to 0$
- Post-adversarial status: **INHERITED from AS** — the unified framework adds only a narrative about the transition mechanism

**P-AS-3. Spectral dimension $d_s \to 2$ in the UV**
- Post-adversarial status: **CONSISTENCY CHECK (trivial)** — universal across essentially all QG approaches (Carlip 2019). Adds zero discriminating information.

### Tier 3: Novel to Unification (But Unconfirmed)

These predictions emerge only from the unification conjecture. They are the framework's genuine novel contributions — and none has been confirmed or computed to the point of being testable.

**P-UNI-1. Ghost confinement mechanism (complex pole tower)**
- Claim: In $C^2$-extended FRG, the spin-2 ghost pole dissolves into a complex conjugate tower (Draper et al. type), with $m_2/k \approx 1.42$ (from Benedetti et al. NGFP values).
- Post-adversarial status: **DOWNGRADED from DISCRIMINATING to CONSISTENCY CHECK**
  - Circularity problem: the prediction assumes unification to predict unification
  - $m_2/k \approx 1.42$ is arithmetic from existing data, not a prediction of unification
  - AS generically produces complex poles (no unification needed)
  - Three of four possible FRG outcomes are ambiguous; only persistent real ghost clearly refutes
  - Retains value as a well-defined computational target

**P-UNI-2. BH evaporation phase transition at $M_{\text{crit}} = 0.31\,M_P$**
- Claim: Black holes undergo a perturbative-to-non-perturbative phase transition at Schwarzschild instability threshold $r_H \approx 0.876/m_2$
- Post-adversarial status: **DEAD as a scientific prediction**
  - Forever observationally inaccessible (Planck-scale BH evaporation)
  - Self-undermined: in the $M_P$ convention, $M_{\text{rem}} (0.46\,M_P) > M_{\text{crit}} (0.31\,M_P)$, meaning the AS transition may preempt the QG+F trigger entirely
  - Phase transition order prediction (first-order in pure gravity, crossover with matter) depends entirely on the broken QCD analogy
  - Classification: NOVEL but UNTESTABLE and ANALOGY-DEPENDENT

**P-UNI-3. Ghost confinement scale $\Lambda_{\text{ghost}} = M_P$ (derived, not input)**
- Claim: In QG+F alone, the ghost mass $m_2$ is a free parameter. In the unified theory, it is fixed by the RG flow connecting AF and NGFP.
- Post-adversarial status: **CONCEPTUALLY APPEALING but UNCOMPUTED** — requires the AF → NGFP trajectory that has not been calculated

### Tier 4: Promising Leads (Not Yet Predictions)

**L1. NGFP $R^3$ correction has correct sign for $n_s$ tension resolution**
- The NGFP gives $\tilde{g}_3^* \approx -(0.86$–$1.10) \times 10^{-2}$ (negative, converged across truncations $n = 3$ to $n = 8$). The $R^3$ direction IS irrelevant at the NGFP ($\vartheta_3 \approx -4.17$), meaning $\tilde{g}_3^*$ is predicted, not free. The sign matches the phenomenological requirement ($\delta_3 < 0$ needed for $n_s \approx 0.974$).
- **But:** The mapping $\tilde{g}_3^* \to \delta_3$ has not been computed. Naive estimates give $\delta_3 \sim 10^{-12}$ to $10^{-22}$ (needed: $\delta_3 \approx -1.19 \times 10^{-4}$). The $b$ parameter fiasco is cautionary: the naive NGFP estimate gave $b \sim 0.01$, the actual perturbative calculation gave $b \sim 10^{-14}$ — suppressed by 12 orders of magnitude by RG running.
- Post-adversarial status: **LEAD, not prediction.** "Correct sign with unknown and probably wrong magnitude."

**L2. Fakeon average continuation as resolution for AS Wick rotation problem**
- QG+F's average continuation (Anselmi 2018) is a well-defined, non-analytic replacement for the Wick rotation. AS has an acknowledged Wick rotation problem (Donoghue 2020; Draper et al. 2020; D'Angelo et al. 2024).
- Post-adversarial status: **PROMISING but UNDEMONSTRATED** — nobody has applied the average continuation within an actual AS/FRG computation. This would be a genuinely novel methodological prediction if demonstrated.

---

## V. Three Critical Computations

These are the computations that would upgrade the framework from "structural conjecture" to "predictive theory" — or kill it. All three are well-defined, technically demanding, and none has been started.

### Computation 1: $C^2$-Extended FRG Graviton Propagator

**What:** Compute the spin-2 transverse-traceless (TT) graviton propagator within the $(R + R^2 + C^2)$ FRG truncation, using momentum-dependent form factors.

**Why it matters:** This is the most direct test of the ghost confinement conjecture. The spin-2 ghost is the central problematic degree of freedom. If the FRG computation shows it dissolving, the framework's core mechanism is confirmed; if the ghost persists as a real pole, the framework is falsified (or at minimum, its core narrative collapses).

**Possible outcomes and their implications:**

| FRG Result | Implication for Framework |
|---|---|
| Complex conjugate pole tower | Strong support — but also consistent with standalone AS generically producing complex poles |
| Real ghost pole persists | Framework falsified at its core (though advocates may argue truncation artifacts) |
| Ghost disappears entirely (fictitious) | Ambiguous — consistent with either unification or standalone AS |
| Residue vanishes | Ambiguous — partial support |

**The deeper test:** Even if complex poles appear, the truly discriminating test is whether the resulting scattering amplitudes match fakeon-prescription amplitudes at tree level. This amplitude equivalence is NOT predicted by the null hypothesis (compatible-but-separate) and would be the framework's first genuine discriminating prediction.

**Current status:** Nobody has computed the $C^2$-extended FRG propagator. Existing FRG propagator computations (Bonanno et al. 2022; Draper et al. 2020) use Einstein-Hilbert or general $R^2$ truncations without explicit $C^2$ inclusion.

### Computation 2: $\tilde{g}_3^* \to \delta_3$ Mapping via Full RG Flow

**What:** Solve the full RG flow from the NGFP to inflationary energy scales in a $\geq 6$-derivative truncation ($R + R^2 + R^3 + ...$), tracking how the dimensionless fixed-point value $\tilde{g}_3^* \approx -0.01$ translates to the physical inflationary parameter $\delta_3$.

**Why it matters:** If $\delta_3 \approx -1.19 \times 10^{-4}$, the framework would have a genuine discriminating prediction: the spectral index shifts to $n_s \approx 0.974$, resolving the current tension with CMB + DESI BAO data ($n_s = 0.9737 \pm 0.0025$). Standalone QG+F treats $\delta_3$ as a free parameter; an NGFP-determined value would be novel.

**The $b$ parameter cautionary tale:** The logarithmic $R^2$ correction parameter $b$ provides a sobering precedent. Naive NGFP estimate: $b \sim \theta/(16\pi^2) \sim 0.01$. Actual perturbative calculation: $b \sim 10^{-14}$. The enormous RG running from Planck to inflationary scales suppressed $b$ by 12 orders of magnitude, rendering it "effectively zero." If the same suppression applies to $\delta_3$, this lead dies — and the naive estimates ($\delta_3 \sim 10^{-12}$ to $10^{-22}$ vs. needed $\sim 10^{-4}$) suggest it might.

**If $\delta_3 \approx -10^{-4}$:** The framework gains its strongest discriminating prediction — a specific, testable CMB observable derived from NGFP physics that standalone QG+F cannot produce.

**If $\delta_3$ is orders too small:** This lead collapses, as $b$ did. The framework loses its best candidate for a novel prediction.

### Computation 3: AF → NGFP Connecting Trajectory

**What:** Compute the full RG flow in the $(R + R^2 + C^2 + E)$ truncation (Gauss-Bonnet term $E$ included for completeness). Identify both fixed points (AF Gaussian and NGFP). Determine whether a trajectory exists connecting AF → NGFP → GR (IR).

**Why it matters:** The existence of this trajectory is the central open conjecture of the SWY version of the framework. Sen, Wetterich & Yamada (2022, 2023) identified both fixed points and showed AF → GR trajectories exist, but did not establish whether the NGFP plays a role as a crossover fixed point.

**If the trajectory exists:** The structural conjecture is confirmed — there is a single, continuous RG flow connecting the perturbative (QG+F) and non-perturbative (AS) regimes through the NGFP. The unified framework gains a mathematical foundation beyond analogy.

**If no trajectory exists:** The SWY version of the framework is falsified. The Codello-Percacci version (AF = NGFP at different approximation levels) might survive, but this interpretation is weaker and may itself be a low-truncation artifact.

**Current status:** Partially available. SWY (2022, 2023) computed the relevant beta functions and identified scaling solutions from AF to GR. Falls et al. (2023) computed NGFP critical exponents in four-derivative gravity. The missing piece is the explicit trajectory computation connecting AF through NGFP to GR.

---

## VI. Comparison to Alternatives

### vs. Standalone QG+F

The unified framework adds to standalone QG+F:
- A mechanism for ghost fate at strong coupling (confinement via AS, rather than leaving it unresolved)
- Black hole interior physics (singularity resolution, remnants from AS)
- A dynamical origin for the ghost mass (from NGFP, rather than treating it as a free parameter)
- A potential resolution of the $n_s$ tension (from NGFP $R^3$ corrections)

What it does NOT add: any experimentally testable prediction beyond what QG+F already provides. The bounded $r$ prediction, the consistency relation, and the CMB observables are all purely QG+F. This is the devil's advocate's sharpest finding: every testable prediction traces back to one standalone component.

### vs. Standalone AS

The unified framework adds to standalone AS:
- Perturbative control at trans-Planckian energies (via QG+F asymptotic freedom)
- The fakeon average continuation as a resolution for the Wick rotation problem
- A specific perturbative mechanism (fakeon prescription) that matches the non-perturbative ghost removal
- A clear physical interpretation of the ghost degree of freedom that appears in higher-derivative truncations

What it does NOT add: any prediction beyond what AS already provides. The Higgs mass, BH remnants, spectral dimension, and singularity resolution are all purely AS.

### vs. String Theory

- Fewer dimensions (4 vs. 10–11)
- Fewer free parameters (4 couplings vs. string landscape)
- No supersymmetry required
- But also fewer predictions and a much less developed mathematical framework
- String theory has dualities, AdS/CFT, and extensive formal structure; the unified framework has an analogy with QCD
- Honest assessment: the mathematical maturity gap is enormous

### vs. Loop Quantum Gravity (LQG)

- Different UV structure (fixed point vs. discrete geometry)
- Similar BH singularity resolution (both predict regular cores)
- LQG has a concrete non-perturbative formulation (spin foams); the unified framework's non-perturbative side is AS/FRG
- LQG makes specific predictions for BH entropy (logarithmic corrections); the unified framework's BH predictions are inherited from AS

### Overall Assessment

The unified framework is **competitive but not clearly superior** to any alternative. Its main virtue is parsimony — it uses only known physics (four-derivative gravity) and known tools (perturbative QFT + FRG). Its main weakness is that the "unification" adds nothing testable beyond the standalone components. It is best understood as an organizational principle that could become a predictive theory if the three critical computations yield favorable results.

---

## VII. Open Problems

### The Cosmological Constant

Both QG+F and AS treat $\Lambda$ as a running coupling, but neither resolves the cosmological constant problem ($\Lambda_{\text{obs}} \sim 10^{-122} M_P^4$). The unified framework inherits this complete blank. The ghost contribution $\delta\Lambda \sim M_2^4/(16\pi^2)$ is 95–111 orders of magnitude too large. AS's cosmological running ($G(r)$ at cosmic scales) might provide a partial resolution, but this remains speculative and no concrete mechanism has been proposed.

### Matter Coupling Beyond 1-Loop

The framework has been developed primarily for pure gravity. Including the full Standard Model introduces complications:
- How does the fakeon prescription interact with matter loops at higher orders?
- Are the NGFP boundary conditions for matter couplings (Shaposhnikov-Wetterich) compatible with fakeon quantization beyond the leading order?
- Does the ghost couple to matter, and if so, how does confinement affect matter physics?

These questions are answerable in principle but have not been addressed.

### Non-Perturbative Uncertainty Quantification

Anselmi (arXiv:2601.06346, January 2026) acknowledged that non-perturbative effects introduce "a new type of uncertainty" — predictions become "delayed prepostdictions" rather than sharp predictions. In the unified framework, this uncertainty is localized to the Planck-scale transition region, but its quantitative implications have not been worked out. Which observables are affected? By how much? These questions matter for the framework's predictive ambitions.

### Experimental Inaccessibility of Planck-Scale Predictions

The most novel predictions of the framework (BH phase transition, ghost confinement trigger, remnant formation details) all involve Planck-scale physics. No foreseeable technology can test them. This is not unique to this framework — all quantum gravity approaches face the same challenge — but it means the unification claim specifically is likely to remain untested for the foreseeable future. Only the three critical computations (Section V) offer a realistic path to progress, and these are theoretical, not experimental.

### The $n_s$ Tension

Current CMB + DESI BAO data give $n_s = 0.9737 \pm 0.0025$, which is $2.3\sigma$ above the standard Starobinsky prediction of $n_s \approx 0.964$–$0.967$. If this tension strengthens with future data, the framework faces a challenge:
- The NGFP $b$ parameter could shift $n_s$ upward — but the perturbative calculation gives $b \sim 10^{-14}$, effectively zero
- The $R^3$ correction could help — but the magnitude is unknown and likely suppressed
- A strengthened tension would require either a successful $\delta_3$ computation or a fundamental rethinking of the inflationary sector

---

## VIII. Conclusion

The Unified QG+F–AS Framework is the most parsimonious interpretation of why both Quadratic Gravity with Fakeons and Asymptotic Safety produce consistent results from the same classical action. It proposes that these are not competing approaches but complementary descriptions of a single UV-complete quantum gravity theory — the perturbative and non-perturbative faces of four-derivative gravity.

After exhaustive investigation across 4 strategies and 38 explorations, including rigorous adversarial testing, the honest assessment is:

**What the framework achieves:**
- A coherent organizational structure that unifies two major quantum gravity programs
- Identification of the Planck scale as a ghost confinement scale (analogous to $\Lambda_{\text{QCD}}$)
- Five bridge mechanisms connecting perturbative and non-perturbative phenomena
- A clear specification of three critical computations that would test the conjecture
- Internal consistency — no prediction contradicts another, no mathematical inconsistency found

**What the framework does not achieve:**
- Zero novel discriminating predictions that survive adversarial scrutiny
- The null hypothesis (compatible-but-separate) explains all evidence equally well
- The QCD analogy — the framework's primary organizing metaphor — breaks at its three most load-bearing joints
- Practical unfalsifiability of the unification claim on any foreseeable timescale

**The bottom line:** The framework is a well-structured research program that identifies important computations, not a predictive theory. Its value is organizational — it shows that two apparently competing approaches may be complementary and specifies exactly what calculations would prove or disprove this. Until at least one of the three critical computations is performed, it remains a compelling structural conjecture: internally consistent, aesthetically appealing, empirically vacuous.

**What would change this assessment:**

Three specific results would upgrade the framework from "research program" to "predictive theory":

1. If the $C^2$-extended FRG propagator shows a complex pole tower AND the resulting amplitudes match fakeon-prescription amplitudes, the framework gains its first genuinely discriminating prediction — because amplitude matching is NOT predicted by the null hypothesis (compatible-but-separate).

2. If the full $\tilde{g}_3^* \to \delta_3$ mapping yields $\delta_3 \in [-2\times10^{-4}, -5\times10^{-5}]$, the framework gains a specific, testable CMB prediction that standalone QG+F cannot make (since QG+F treats $\delta_3$ as free).

3. If the AF → NGFP connecting trajectory exists, the structural conjecture gains mathematical substance beyond analogy. If it doesn't exist, the SWY version dies (the Codello-Percacci version survives but is weaker).

Conversely, the framework would be falsified if: LiteBIRD measures $r$ outside $[4\times10^{-4}, 0.01]$ (kills QG+F and therefore the framework); the FRG computation shows a persistent real ghost pole (kills the confinement narrative); or the AF → NGFP trajectory is proven not to exist (kills the SWY version).

The framework's contribution to the field, if accepted, would be to redirect effort: instead of choosing between QG+F and AS, the community should investigate their overlap regime. The three critical computations ($C^2$-extended FRG propagator, $\tilde{g}_3^* \to \delta_3$ mapping, AF → NGFP trajectory) are well-defined, technically demanding, and would definitively advance our understanding of quantum gravity regardless of whether the unification conjecture proves correct.

---

## Appendix: Key References

**Quadratic Gravity with Fakeons:**
- Stelle (1977) — Renormalizability of four-derivative gravity
- Fradkin & Tseytlin (1982) — Asymptotic freedom in higher-derivative gravity
- Anselmi (2017, JHEP 06, 086; 2018, JHEP 02, 141) — Fakeon prescription
- Anselmi, Bianchi & Piva (2020, JHEP 07, 211) — Bounded $r$ prediction
- Bianchi & Gamonal (2025, arXiv:2502.03543; arXiv:2506.10081) — Consistency relation, N³LO precision
- Bonanno et al. (2025, arXiv:2505.20360) — Schwarzschild instability ("spontaneous ghostification")
- Anselmi (2026, arXiv:2601.06346) — Non-perturbative uncertainty acknowledgment

**Asymptotic Safety:**
- Reuter (1998) — FRG approach and NGFP discovery
- Bonanno & Reuter (2000, 2006) — BH singularity resolution and remnants
- Codello & Percacci (2006, PRL 97, 221301) — One-loop FRG gives NGFP
- Codello, Percacci & Rahmede (2009) — $f(R)$ critical exponents, $\tilde{g}_3^*$
- Shaposhnikov & Wetterich (2010) — Higgs mass prediction from NGFP
- Codello, D'Odorico, Pagani (2014, PRD 91, 103530) — NGFP produces Starobinsky
- Bonanno & Platania (2015, 2018) — Logarithmic NGFP corrections to inflation
- Becker, Ripken, Saueressig (2017) — Ghost mass divergence at NGFP (scalars)
- Draper, Knorr, Ripken, Saueressig (2020, PRL 125, 181301) — Complex pole tower
- Platania & Wetterich (2020) — Fictitious ghost argument
- Falls, Kluth & Litim (2023, PRD 108, 026005) — NGFP UV critical surface dimension
- Bonanno, Denz, Pawlowski, Reichert (2022) — Positive spectral function for dynamical graviton

**Unification / Bridge:**
- Holdom & Ren (2015, PRD 93, 124030; 2016) — QCD analogy for ghost confinement
- Sen, Wetterich & Yamada (2022, JHEP 03, 130; 2023, JHEP 02, 054) — Two fixed points, AF viability
- Gubitosi, Ooijer, Ripken, Saueressig (2018) — $f(R)$ flow to Starobinsky
- Donoghue (2020) — Wick rotation obstruction in AS
- D'Angelo et al. (2024) — Lorentzian Asymptotic Safety
- Carlip (2019) — Universal $d_s \to 2$ across QG approaches

---

## Appendix: Consolidated Prediction Survival Table

| ID | Prediction | Pre-Adversarial | Post-Adversarial | Testable? |
|---|---|---|---|---|
| P-QGF-1 | $r \in [4\times10^{-4}, 4\times10^{-3}]$ | DISCRIMINATING | INHERITED (QG+F) | Yes (~2036) |
| P-QGF-2 | $r = -8n_T$ preserved | CONSISTENCY | CONSISTENCY | Yes (post-$r$ detection) |
| P-QGF-3 | CMB matches Starobinsky | CONSISTENCY | CONSISTENCY | Yes (ongoing) |
| P-AS-1 | Higgs mass unchanged | CONSISTENCY | CONSISTENCY (clean) | Done (retrodiction) |
| P-AS-2 | BH remnants, $T \to 0$ | CONSISTENCY | INHERITED (AS) | No (Planck scale) |
| P-AS-3 | $d_s \to 2$ | CONSISTENCY | CONSISTENCY (trivial) | No (Planck scale) |
| P-UNI-1 | Ghost complex pole tower | DISCRIMINATING | CONSISTENCY CHECK | Theoretically (years) |
| P-UNI-2 | BH phase transition trigger | DISCRIMINATING | UNTESTABLE NARRATIVE | No (forever) |
| P-UNI-3 | $\Lambda_{\text{ghost}} = M_P$ | NOVEL | UNCOMPUTED | Theoretically (years) |
| L1 | $\delta_3$ correct sign | POT. DISCRIMINATING | LEAD (not prediction) | Requires computation |
| L2 | Average continuation for AS | NOVEL | UNDEMONSTRATED | Requires computation |

**Genuinely discriminating predictions that survived adversarial scrutiny: 0**
**Potentially discriminating predictions pending computation: 2** (L1, L2)
**Clean consistency checks: 3** (P-AS-1, P-QGF-2, P-QGF-3)

---

*This document is the final deliverable of the Atlas Quantum Gravity Research Program.*
*4 strategies · 38 explorations · Explorer 007 (Strategy 004)*
