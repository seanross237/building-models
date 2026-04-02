# Strategy 001 Final Report: Yang-Mills Existence and Mass Gap

## Executive Summary

This strategy conducted 10 explorations over three phases to map the technical landscape of the Yang-Mills Millennium Prize Problem, computationally attack tractable obstructions, and identify the most promising directions forward.

**Top-level finding:** The Yang-Mills mass gap problem is a 20-50+ year problem requiring conceptual breakthrough. The UV problem is solved (Balaban 1983-89, Magnen-Rivasseau-Sénéor 1993). The entire difficulty is infrared: proving confinement and mass gap rigorously for a continuous non-abelian gauge group in 4 dimensions. Every result from the remarkably active 2020-2026 period addresses either the wrong gauge groups (finite), wrong coupling (strong only), wrong dimension (3D), or wrong limit (N→∞). No existing technique has a clear path to the prize.

**Our strongest contribution:** Quantitative demonstration that the Adhikari-Cao (2025) mass gap bounds are vacuous by a factor of 57-69x in the physical regime, with the bounds diverging as finite subgroups approach SU(2). This constrains what any future proof strategy based on their approach must accomplish.

---

## What We Did

### Phase 1: Precision Probing (Explorations 001-002)

**Exploration 001:** Mapped Balaban's 14-paper renormalization group program (1983-89). Established that UV stability of 4D lattice Yang-Mills on torus T⁴ is achieved. Identified a two-tier, five-gap structure between Balaban's results and the Millennium Prize.

**Exploration 002:** Cataloged 8 rigorous QFT constructions in 2D/3D and identified 3 specific failure modes at d=4 (cluster expansion divergence, large field problem, infinite RG convergence). Discovered the critical reframing: Magnen-Rivasseau-Sénéor (1993) solved the UV problem for 4D YM. The entire difficulty is infrared.

### Phase 2: Computational Attack (Explorations 003-005, 008)

**Exploration 003 (Math):** Implemented full SU(2) Wilson lattice gauge theory Monte Carlo simulation in Python. Confirmed confinement (area law with R²>0.996), measured string tension σ=0.593-0.132 across β=2.0-3.0, demonstrated mass gap evidence through multiple observables.

**Exploration 004:** Mapped the lattice-to-continuum gap with theorem-level precision. Established a 7-step gap structure. Identified Adhikari-Cao (2025) mass gap for finite gauge groups and Chatterjee's probabilistic school as the most active research fronts.

**Exploration 005 (Math):** Implemented lattice gauge theory for binary polyhedral subgroups of SU(2) (2T: 24 elements, 2O: 48 elements, 2I: 120 elements). Demonstrated that the binary icosahedral group reproduces SU(2) observables to <0.5% accuracy. Measured convergence rates and phase transition scaling.

**Exploration 008 (Math, partial):** Computed spectral gaps of group Laplacians and Adhikari-Cao bounds. Found bounds are quantitatively vacuous (57-69x too large after adversarial correction), confirming the finite→continuous barrier is fundamental.

### Phase 3: Synthesis (Explorations 006-007, 009-010)

**Exploration 006:** Deep technical analysis of Adhikari-Cao, Chatterjee, and Shen-Zhu-Zhu results. Identified four-layer structural obstruction in the Adhikari-Cao approach. Assessed the problem as requiring 20-50+ years.

**Exploration 007:** Novelty search establishing that our convergence rate measurements appear novel, while β_c values are known since 1980 (Petcher-Weingarten) with modern refinement (Hartung 2022).

**Exploration 009:** Complete obstruction atlas covering 9 approaches with classifications. Identified 5 specific bottleneck theorems. Recommended multi-scale RG + Bakry-Émery spectral gap as the most promising unexplored combination.

**Exploration 010:** Adversarial review that found a definitional error (Cayley graph vs. character minimum Δ_G) which actually strengthened our vacuousness claim by 4x, downgraded the convergence rate claim from precise power law to qualitative ordering, and moderated the four-layer barrier claim.

---

## Complete Obstruction Atlas

| # | Approach | Best Result | Status | Bottleneck |
|---|----------|------------|--------|------------|
| 1 | **Balaban RG** | UV stability on T⁴ (1989) | TRACTABLE (existence) / FUNDAMENTAL (mass gap) | Observable control, uniqueness, then mass gap |
| 2 | **Constructive QFT** | d≤3 constructions | FUNDAMENTAL BARRIER | Marginal renormalizability at d=4 — 3 specific failure modes |
| 3 | **Lattice → continuum** | Extraordinary numerics | FUNDAMENTAL BARRIER | No rigorous weak-coupling framework for continuous groups |
| 4 | **Stochastic quantization** | 3D YMH local existence (Chandra-Hairer 2024) | FUNDAMENTAL BARRIER | d=4 is critical dimension; regularity structures don't extend |
| 5 | **Chatterjee probabilistic** | Strong mass gap ⟹ confinement (2021) | HARD | Conditional on unproven mass gap; first scaling limit is Gaussian |
| 6 | **Adhikari-Cao swapping map** | Mass gap for ALL finite gauge groups (2025) | FUNDAMENTAL BARRIER | 4-layer structural obstruction; bounds 57-69x vacuous for SU(2) subgroups |
| 7 | **Shen-Zhu-Zhu Bakry-Émery** | SU(N) mass gap at β < 1/48 (2025) | FUNDAMENTAL at weak coupling | First continuous-group mass gap — but only at strong coupling |
| 8 | **Large-N / 't Hooft** | Area law at N=∞ (2025) | HARD | Finite-N corrections completely uncontrolled |
| 9 | **OS reconstruction** | Axioms fully specified | TARGET | Not a barrier — framework for stating the result |

### Five Bottleneck Theorems

1. **Uniqueness of T⁴ continuum limit** — Show Balaban's RG map is a contraction. Would establish first 4D YM existence proof. Estimated difficulty: 5-10 years.
2. **Observable control on T⁴** — Track Wilson loop insertions through Balaban RG. Verify Osterwalder-Schrader axiom E2. Estimated: 3-7 years.
3. **SU(2) mass gap at ANY single coupling** — First continuous-group result at weak coupling. Revolutionary. Difficulty: unknown, possibly decades.
4. **Uniform mass gap for finite group sequence** — Bounds uniform in |G_n| as G_n → SU(2). Requires qualitatively new estimates beyond Adhikari-Cao. Estimated: 10-20 years.
5. **Non-Gaussian scaling limit** — First non-trivial continuum limit of non-abelian gauge theory in d>2. Potentially decades.

### Most Promising Unexplored Combination

**Multi-scale RG (Balaban) + Bakry-Émery spectral gap (Shen-Zhu-Zhu)**

Rationale: Shen-Zhu-Zhu's Bakry-Émery approach proves mass gap for SU(N) but only at very strong coupling (β < 1/48). The Poincaré inequality they use breaks down at weak coupling because the bare action's curvature vanishes. But after Balaban-style RG blocking, the effective action at each scale has a controlled coupling. If one could prove a scale-by-scale Poincaré inequality for the RG-improved effective action, the mass gap might follow by composition across scales.

This combination has not been attempted in the literature (to our knowledge), but each ingredient exists separately. It would require substantial new mathematical work.

---

## Novel Claims

### Claim 1: Adhikari-Cao Bounds Are Quantitatively Vacuous for SU(2) Subgroups

**Claim:** The Adhikari-Cao (2025) mass gap theorem requires β ≥ β_min = (114 + 4 log|G|) / Δ_G for the mass gap to hold. For the three binary polyhedral subgroups of SU(2), using the correct character-minimum spectral gap:

| Group | |G| | Δ_G | β_min | Measured β_c | Ratio |
|-------|-----|------|-------|-------------|-------|
| 2T    | 24  | 1.000 | 126.7 | 2.2 | 57.6x |
| 2O    | 48  | 0.586 | 221.0 | 3.2 | 69.1x |
| 2I    | 120 | 0.382 | 348.6 | 5.8 | 60.1x |

The bounds are 57-69x larger than the physical phase transition point. Moreover, β_min grows with |G| (as Δ_G → 0), meaning the bounds become MORE vacuous as finite groups approach SU(2).

**Evidence:**
- Spectral gaps computed from first principles using Adhikari-Cao's definition Δ_G = min_{g≠1} Re(χ_fund(1) − χ_fund(g)) = 2(1 − max Re(g₀)) (Exploration 008, corrected in Exploration 010)
- Phase transition values β_c confirmed against Hartung et al. (2022): 2T→2.15±0.05, 2O→3.20±0.10, 2I→5.70±0.20

**Novelty search:** No prior paper has computed these specific ratios or quantified the vacuousness of Adhikari-Cao for SU(2) subgroups. The Adhikari-Cao paper itself does not discuss this.

**Strongest counterargument:** Only 3 binary polyhedral subgroups exist, so the "divergence as |G|→∞" claim is an extrapolation of the analytic formula, not a limit of a literal sequence. Other finite subgroups (cyclic Z_n, dihedral 2D_n) could behave differently.

**Status:** VERIFIED (spectral gaps) / COMPUTED (ratios). The qualitative conclusion (bounds are vacuous, diverge with |G|) is robust even under 2x uncertainty.

---

### Claim 2: Monotone Convergence of Finite-Subgroup Observables to SU(2)

**Claim:** Lattice gauge theory observables (average plaquette, string tension, Creutz ratios) converge monotonically as binary polyhedral subgroups of SU(2) increase in size: 2T (24) → 2O (48) → 2I (120) → SU(2). The binary icosahedral group (120 elements) reproduces all SU(2) observables to <0.5% accuracy across β=1.0-4.0 on a 4⁴ lattice.

**Evidence:** Monte Carlo simulation of all four groups (2T, 2O, 2I, SU(2)) on 4⁴ lattice at β=1.0, 2.0, 2.5, 3.0, 3.5, 4.0 (Exploration 005).

**Novelty search:** The convergence itself is qualitatively known (Petcher-Weingarten 1981, Bhanot-Creutz 1981). The specific <0.5% bound for 2I appears to be a new quantitative result. Power-law convergence rates (originally claimed as α≈0.7-2.5) are NOT statistically established with only 3 data points and deviations near the MC noise floor (Exploration 010 adversarial review).

**Strongest counterargument:** With 3 data points and deviations of order 0.001-0.01, the statistical significance is marginal. A higher-statistics study with larger lattices is needed to establish quantitative convergence rates.

**Status:** COMPUTED (convergence pattern) / CONJECTURED (power-law rates). The qualitative monotone ordering is robust; specific rate exponents are not.

---

### Claim 3: Complete Obstruction Atlas

**Claim:** Our 9-approach obstruction atlas with theorem-level barriers is more precise and up-to-date than existing published reviews (Jaffe-Witten 2000, Douglas 2004).

**Evidence:** Integrates results from 2020-2026 that are not covered in any published review: Adhikari-Cao (2025), Chatterjee (2024), Chandra-Hairer (2024), Shen-Zhu-Zhu (2025), Adhikari-Suzuki (2025).

**Novelty search:** No published review as of March 2026 covers all of these results in a single framework with obstruction classifications.

**Strongest counterargument:** This is a survey/synthesis contribution, not a proof result. Individual researchers in the field likely have this picture mentally, even if it's not written in one place.

**Status:** PARTIALLY VERIFIED. The atlas itself is a contribution to understanding, not to mathematics.

---

## Recommendations for Next Strategy

1. **Computational priority:** Test the multi-scale RG + Bakry-Émery combination numerically. Implement Balaban-style block-spin RG for one step, compute the effective action, and check whether a Poincaré/log-Sobolev inequality holds for the resulting distribution. This is a ~200-line computation that could either encourage or discourage a proof attempt.

2. **Theoretical priority:** Focus on Bottleneck Theorem 3 — proving SU(2) mass gap at ANY single coupling. Shen-Zhu-Zhu's approach works at β < 1/48. Pushing to β < 1 or β < 5 would be a meaningful advance, even if far from the continuum limit.

3. **Literature depth:** The Shen-Zhu-Zhu result appears underappreciated. A deep dive into their Langevin/Bakry-Émery technique and its relationship to Balaban's framework would be high-value.

4. **Computational strengthening:** Rerun the finite-group convergence study (Exploration 005) with 10x more MC statistics on larger lattices to either confirm or refute the power-law convergence rate with statistical significance. Also extend to cyclic subgroups Z_n for a longer |G| sequence.

5. **Cross-approach connection:** Investigate whether Chatterjee's conditional theorem (strong mass gap ⟹ confinement) combined with Shen-Zhu-Zhu's mass gap at strong coupling gives any rigorous confinement statement at strong coupling. This might already follow but hasn't been checked.

---

## Strategy Methodology Assessment

The "Precision Probing → Computational Attack → Synthesis" methodology worked well:
- Phase 1 (2 explorations) mapped the landscape efficiently. The UV/IR reframing was the single most important strategic insight.
- Phase 2 (4 explorations) produced both positive results (confinement confirmed, finite group convergence) and the strongest negative result (Adhikari-Cao vacuousness).
- Phase 3 (4 explorations) connected approaches, assessed novelty, and caught a real error through adversarial review.

**What I'd change:** Run the adversarial review EARLIER (after exploration 008, before synthesis). The Δ_G error could have been caught sooner. Also, the convergence rate claim should have been flagged as statistically questionable from the start — 3 data points for a power law is never sufficient.

**Exploration budget:** 10 was adequate for this problem. The 2-4-4 allocation across phases was close to optimal. Phase 2 could have used one more computation (higher-statistics convergence study) at the expense of one synthesis exploration.

---

## Appendix: Exploration Summary Table

| # | Type | Topic | Outcome | Key Finding |
|---|------|-------|---------|------------|
| 001 | Standard | Balaban RG program | Succeeded | UV stability on T⁴. 5-gap, 2-tier structure. |
| 002 | Standard | Constructive QFT 2D/3D vs 4D | Succeeded | UV solved (MRS 1993). Difficulty entirely IR. |
| 003 | Math | SU(2) lattice MC simulation | Succeeded | Confinement confirmed. σ > 0 at all β. |
| 004 | Standard | Lattice-continuum gap | Succeeded | 7-step gap. Finite→continuous is key bottleneck. |
| 005 | Math | Finite group convergence | Succeeded | 2I matches SU(2) <0.5%. Phase transition scaling. |
| 006 | Standard | Modern rigorous frontier | Succeeded | 4-layer obstruction. 20-50+ year problem. |
| 007 | Standard | Novelty search | Succeeded | Convergence rates appear novel. β_c known since 1980. |
| 008 | Math | Spectral gap / AC bounds | Partial | AC bounds 57-69x vacuous (corrected). β_min diverges. |
| 009 | Standard | Obstruction atlas synthesis | Succeeded | 9-approach atlas. 5 bottleneck theorems. RG+BE path. |
| 010 | Standard | Adversarial review | Succeeded | Found Δ_G error (strengthens claim). Convergence rate downgraded. |
