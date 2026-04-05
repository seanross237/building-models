# Strategy-001 Final Report: Catalog-Measure-Tighten

## Executive Summary

Strategy-001 conducted a systematic computational investigation of the load-bearing inequalities in 3D Navier-Stokes regularity theory. Over 8 explorations (3 standard, 5 math), we produced a **quantified slack atlas** measuring the gap between proven bounds and actual flow behavior across multiple inequalities, initial conditions, and Reynolds numbers.

**The central finding:** The vortex stretching bound — the single inequality responsible for the failure of the enstrophy approach to prove global regularity — has **158-237× slack** across all tested flows. This slack is dominated (63% of log-slack) by the looseness of the Ladyzhenskaya interpolation constant, not by geometric alignment loss (31%). The Calderón-Zygmund/BKM approach to the same flows gives bounds that are near-tight (1.05× with empirical constant, ~3× with theoretical constant), showing that the ~200× slack is an artifact of the Ladyzhenskaya interpolation chain, not an intrinsic feature of NS dynamics.

**Explorations used:** 8 of 20 budget.
**Validation tier achieved:** Tier 3 (slack atlas with quantified factors) with partial Tier 4 (conditional tighter bound, adversarially reviewed).

---

## What We Accomplished

### Phase 1: Catalog (Exploration 001)
- 17-entry catalog of load-bearing inequalities with exact mathematical statements
- Tao generic/NS-specific classification for every inequality
- Ranked by expected slack: vortex stretching #1 by a wide margin

### Phase 2: Measure (Explorations 002-004)
- Built pseudospectral DNS solver + 8-inequality measurement infrastructure (bound/actual pairs)
- **Slack Atlas** on Taylor-Green vortex at Re=100-5000 (N=64, convergence-checked at N=128):

| Rank | Inequality | Min Slack | Trend with Re |
|---|---|---|---|
| 1 | Vortex Stretching (E2/E3) | **237×** | Grows ∝ Re^0.28 |
| 2 | Prodi-Serrin (R1/F2) | 31× | Stable |
| 3 | Kato-Ponce (E4) | 25× | Grows ∝ Re^0.16 |
| 4 | Agmon (F4+G1) | 12× | Grows ∝ Re^0.14 |
| 5 | CZ Pressure (F5) | 7.8× | Stable |
| 6 | Sobolev H¹→L⁶ (F3) | 4.5× | Stable |
| 7 | Ladyzhenskaya (F1) | 4.3× | Stable |
| 8 | Energy (E1) | 1.0× | Exact |

- Tested 5 initial conditions + adversarial search: **minimum achievable slack = 158×** (anti-parallel vortex tubes, σ=2.5)
- **Exact 3-factor decomposition** of the 237× vortex stretching slack:
  - α_geom = 5.3× (geometric alignment/Hölder loss) — 31% of log-slack
  - α_Lad = 31× (Ladyzhenskaya constant looseness) — 63% of log-slack
  - α_sym = √2 (symmetric factor, exact identity) — 6% of log-slack
  - Product verified to machine precision at all timesteps

### Phase 3: Tighten (Explorations 005-008)
- Literature survey: 28 papers. **No "spectral Ladyzhenskaya inequality" in the literature** (open problem). Tao (2014) hard obstruction: harmonic analysis alone can't close NS regularity.
- Spectral Ladyzhenskaya computation: **dead end for worst-case bounds** — adversarial phase alignment achieves near-sharp constant regardless of spectral support. The observed C_{L,eff} ~ Re^{-3/8} is statistical, not provable.
- **CZ/BKM gives near-tight bounds** on ‖∇u‖_{L^∞} (slack ~1.05× with empirical constant, ~3× with theoretical). The 237× slack lives entirely in the Ladyzhenskaya interpolation chain.
- **BMO/L^∞ ≈ 0.27** across Re=100-5000, giving ~4× Kozono-Taniuchi advantage.
- **Conditional bound:** C(F₄) ≈ 0.003/F₄ — effective vortex stretching constant scales inversely with vorticity flatness.
- Adversarial review identified genuine weaknesses in several claims (see Novel Claims section).

---

## Directions Tried

| Direction | Status | Explorations | Outcome |
|---|---|---|---|
| Catalog inequalities | Succeeded | 001 | 17-entry catalog |
| Slack measurements | Succeeded | 002-004 | Quantified atlas, 3-factor decomposition |
| Spectral Ladyzhenskaya | **Exhausted (dead end)** | 006 | Can't improve worst-case constant via spectral support |
| Literature survey | Succeeded | 005 | 28 papers, key gaps identified |
| BKM advantage + intermittency | Succeeded | 007 | CZ near-tight; flatness correlates with C_{L,eff} |
| Adversarial review | Succeeded | 008 | 3 claims weakened, 1 error caught, most defensible finding identified |

---

## Novel Claims

### Claim 1: Quantified Slack Atlas
- **Claim:** The vortex stretching bound has 237× minimum slack on the Taylor-Green vortex (158× adversarial minimum), making it the loosest inequality by 8× compared to the next (Prodi-Serrin at 31×). All 8 key inequalities are quantified with convergence-checked slack ratios across Re=100-5000.
- **Evidence:** Explorations 002-003. Pseudospectral DNS with N=64 primary, N=128 convergence check (<0.7% deviation). 5 initial conditions tested.
- **Novelty search:** No systematic quantification of inequality slack in NS regularity has been published at this level of detail. Individual inequality tightness studies exist (e.g., Protas group on max enstrophy) but not a comparative atlas.
- **Strongest counterargument:** The atlas is specific to T³ with L=2π. The optimal adversarial slack (158×) depends on domain size (σ_optimal ≈ 0.4L). Protas-type globally optimized ICs were not tested and might achieve lower slack.
- **Status:** Partially verified — computation checks pass; domain-dependence caveat.

### Claim 2: Ladyzhenskaya Dominates Vortex Stretching Slack
- **Claim:** The 237× vortex stretching slack decomposes as 63% Ladyzhenskaya constant looseness + 31% geometric alignment loss + 6% symmetric factor. The Ladyzhenskaya interpolation, not Hölder geometry, is the dominant bottleneck.
- **Evidence:** Exploration 004. Exact decomposition α_geom × α_Lad × α_sym = total verified to machine precision at all timesteps and both Re values. The effective Ladyzhenskaya constant C_{L,eff} = 0.147 is 18% of the sharp constant C_L = 0.827 because NS solutions are spectrally extended while the optimizer is spike-like.
- **Novelty search:** The specific decomposition and quantification appear novel. The qualitative observation that NS solutions are far from Sobolev optimizers is not new, but the 63/31/6 quantification is.
- **Strongest counterargument:** The decomposition is algebraically tautological (the product identity is guaranteed). Its value is in the *relative magnitudes*, which are IC-specific (tested only on TGV).
- **Status:** Partially verified — algebraic identity is exact; IC-specificity is a caveat.

### Claim 3: CZ/BKM Gives Near-Tight Bounds While Ladyzhenskaya Chain Does Not
- **Claim:** The Calderón-Zygmund/BKM approach to bounding ‖∇u‖_{L^∞} via ‖ω‖_{L^∞} with logarithmic correction produces bounds with ~3× slack (using theoretical constant), while the Ladyzhenskaya interpolation chain has ~237× slack for the same flows. The ~200× gap is an artifact of the interpolation methodology, not of NS dynamics.
- **Evidence:** Exploration 007. BKM slack computed at Re=100-5000. With theoretical CZ constant (0.24), BKM slack ≈ 3×. With empirical constant (0.68), slack ≈ 1.05×.
- **Novelty search:** The qualitative observation that BKM uses pointwise information while Ladyzhenskaya uses L² norms is standard. The **quantitative comparison** (~80× advantage with theoretical constant) on the same DNS data does not appear in the literature.
- **Strongest counterargument:** BKM and Ladyzhenskaya bound different quantities (‖∇u‖_{L^∞} vs ∫S_{ij}ω_iω_j dx). The comparison is not apples-to-apples. However, both quantities must be controlled for regularity, and the relative tightness of the two approaches is meaningful for proof strategy selection.
- **Status:** Partially verified — quantification is novel; comparison has methodological caveats.

### Claim 4: Spectral Ladyzhenskaya is a Dead End for Worst-Case Bounds
- **Claim:** For any spectral envelope, adversarial phase alignment can achieve effective Ladyzhenskaya constants comparable to the universal sharp constant. Spectral support alone cannot improve the worst-case bound.
- **Evidence:** Exploration 006. Phase optimization over band-limited fields at multiple k₀ values.
- **Novelty search:** Consistent with Tao (2014) obstruction. The specific computational demonstration appears novel.
- **Strongest counterargument:** Phase optimization used local search (L-BFGS-B) — global maxima may not have been found. Also, the Bernstein inequality does give tighter L²→L⁴ bounds for band-limited functions; the claim needs to be stated more precisely (the improvement comes from the gradient term, not from a tighter constant per se).
- **Status:** Speculative — direction is correct per Tao (2014); computational details have caveats.

### Claim 5: Conditional Bound C(F₄) ≈ 0.003/F₄
- **Claim:** The effective vortex stretching constant scales approximately inversely with the vorticity flatness F₄.
- **Evidence:** Exploration 007. Empirical fit from DNS of TGV at Re=100-5000. Correlation r = -0.93.
- **Novelty search:** No equivalent conditional bound in the literature.
- **Strongest counterargument:** Purely empirical, single IC. The 1/F₄ scaling may not hold for more extreme flows. No theoretical derivation exists.
- **Status:** Speculative — strong numerical evidence but needs theoretical justification and multi-IC validation.

---

## What Didn't Work / Dead Ends

1. **Spectral Ladyzhenskaya:** 1 exploration spent. Can't improve worst-case constant via spectral support alone (Tao obstruction confirmed computationally).
2. **Geometric alignment as primary target:** Early explorations (002) estimated geometric alignment at 9× and Ladyzhenskaya at 18.6×. Exploration 004 corrected this: Ladyzhenskaya is 31× (63%), geometric is only 5.3× (31%). The correction changed the strategic direction.
3. **(5/9)^{1/4} "div-free factor":** Initially claimed as a divergence-free improvement. Adversarial review showed it's a trivial vector vs scalar component effect (chi-squared fourth moment), NOT related to incompressibility.

---

## Recommendations for Next Strategy

1. **Protas-type adversarial IC search:** Use adjoint-based PDE optimization to find globally optimal ICs that minimize the slack ratio. Our 158× may not be the true minimum.

2. **Multi-IC validation:** Test the slack atlas, decomposition, BMO ratios, and conditional bound on at least 3 more ICs (random Gaussian, Kida vortex, Protas-optimized) to establish generality.

3. **Theoretical derivation of C(F₄) ≈ 0.003/F₄:** The conditional bound has strong numerical support. A rigorous proof would be a genuine contribution. The key step: show that for div-free fields with bounded flatness, the Ladyzhenskaya optimizer is excluded, giving a tighter constant.

4. **Formal proof of the interpolation bottleneck:** Prove that for any NS regularity argument using the enstrophy equation → Ladyzhenskaya chain, the effective constant is at least C × α for some α > 1 when the solution has bounded Fourier spectral width. This would formalize the "interpolation is the wrong tool" insight.

5. **Explore the Kozono-Taniuchi/BKM path for enstrophy:** Can the BKM-type analysis (controlling ‖ω‖_{L^∞} or ‖ω‖_{BMO}) be translated back into an improved enstrophy differential inequality that avoids Ladyzhenskaya entirely?

---

## Code Artifacts

All code in `explorations/exploration-002/code/`:
- `ns_solver.py` — Pseudospectral DNS solver (3D, T³, RK4, 2/3 dealiasing)
- `slack_measurements.py` — 8 bound/actual pairs for all cataloged inequalities
- `run_simulations.py` — Simulation runner with diagnostics
- `compile_results.py` — Analysis and reporting

Additional code in explorations 003, 004, 006, 007 for specific measurements (alignment, adversarial search, spectral analysis, BMO norms, intermittency).
