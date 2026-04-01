# Exploration History

## Exploration 001: Catalog of Load-Bearing Inequalities in 3D NS Regularity Theory

**Explorer type:** Standard | **Outcome:** Succeeded | **Date:** 2026-03-29

**Goal:** Produce a comprehensive catalog of every load-bearing inequality in the major 3D Navier-Stokes regularity results with exact statements, sources, sharpness, scaling in Re, constant status, and Tao generic/NS-specific classification.

**What was done:** Assembled a 17-entry catalog covering all target inequality families: functional inequalities (Ladyzhenskaya, GNS, Sobolev embedding, Agmon, Calderón-Zygmund, Brezis-Gallouet-Wainger, Kato-Ponce, HLS), energy/enstrophy estimates (global energy inequality, enstrophy ODE, Constantin-Fefferman vortex stretching, H^s energy), regularity criteria (Prodi-Serrin, Beale-Kato-Majda), partial regularity (CKN local energy, CKN ε-regularity, ESS L³ endpoint), and Gronwall.

**Key takeaway:** The vortex stretching bound |VS| ≤ C||ω||^{3/2}_{L²}||∇ω||^{3/2}_{L²} is the single most load-bearing bottleneck — it's the inequality that makes the enstrophy ODE blow up (dy/dt ≤ Cy³/ν³). Constantin-Fefferman (1993) showed it IS loose for flows with disordered vorticity direction. Second most important: the CKN ε* threshold is completely uncomputed.

**Top 5 by expected slack:**
1. Vortex stretching bound (E2/E3) — actual VS ≈ Re^{-1/4} × Ladyzhenskaya bound for isotropic turbulence
2. Agmon + Gronwall chain (F4+G1) — astronomical overestimate at large Re
3. CKN ε-regularity constant (R4) — completely uncomputed existence constant
4. NS-specific Ladyzhenskaya constant (F1) — div-free constraint may reduce C_L
5. BKM log-Sobolev inequality (F6) — leading constant existential

**Unexpected findings:**
- Transport cancellation ⟨u·∇(J^s u), J^s u⟩ = 0 is NS-specific (uses div u = 0) — hidden use of NS structure
- Gap between CKN singular set dimension (≤1 parabolic) and conjectured (0) represents substantial slack in the entire partial regularity program
- All functional inequalities are sharp on ℝ³ but extremals are static/isotropic/non-divergence-free — the NS-specific constants may be strictly smaller

**Tao classification:** Generic inequalities (F1-F4, G1) cannot alone prove regularity. NS-specific inequalities (E2/E3, R1-R5) are where meaningful slack lives. Any proof must use specific NS nonlinearity structure.

---

## Exploration 002: Computational Slack Measurement — Infrastructure + Taylor-Green Vortex

**Explorer type:** Math | **Outcome:** Succeeded | **Date:** 2026-03-29

**Goal:** Build computational measurement infrastructure for 8 key NS inequalities (bound/actual Python function pairs) and run first slack measurements on Taylor-Green vortex at Re=100, 500, 1000, 5000.

**What was done:** All 8 inequality pairs implemented, validated against analytical test cases, and measured at 4 Reynolds numbers with N=128³ convergence check (all min slacks converged to <0.7%). Full code suite produced: ns_solver.py, slack_measurements.py, run_simulations.py, compile_results.py.

**Key takeaway — Slack Atlas (min slack across all Re):**

| Rank | Inequality | Min Slack | Trend |
|---|---|---|---|
| 1 (loosest) | E2/E3: Vortex Stretching | **237×** | Grows ∝ Re^0.28 |
| 2 | R1/F2: Prodi-Serrin | 31× | Stable |
| 3 | E4: Kato-Ponce | 25× | Grows ∝ Re^0.16 |
| 4 | F4+G1: Agmon | 12× | Grows ∝ Re^0.14 |
| 5 | F5: CZ Pressure | 7.8× | Stable |
| 6 | F3: Sobolev H¹→L⁶ | 4.5× | Stable |
| 7 | F1: Ladyzhenskaya | 4.3× | Stable |
| 8 (tightest) | E1: Energy | 1.0× | Exact |

**Vortex stretching slack decomposition (237× = 9× × 18.6× × 1.4×):**
- 9× from Hölder losing geometric alignment information (ω-strain eigenvector alignment)
- 18.6× from using R³ constants on T³ (4.3² from Ladyzhenskaya squared in the chain)
- 1.4× from ||S|| ≤ ||ω|| factor (√2)

**Unexpected findings:**
- Min slack is Re-independent for ALL functional inequalities (F1, F3, F5) — minimum occurs at early time when flow retains TGV symmetry, determined by initial condition geometry not dynamics
- Three growth regimes: STABLE (F1, F3, E1, R1, F5), WEAKLY GROWING Re^0.14-0.16 (F4+G1, E4), MODERATELY GROWING Re^0.28 (E2/E3)
- The Prodi-Serrin bound's 31× slack may partly reflect non-optimal interpolation exponents

**Verification scorecard:** 3 VERIFIED, 8 COMPUTED, 8 CHECKED, 1 CONJECTURED (strain-antisymmetric decomposition factor √2). Energy conservation ≤0.15% at all Re.

---

## Exploration 004: Vortex Stretching Slack Decomposition — Isolating the Geometric Factor

**Explorer type:** Math | **Outcome:** Succeeded | **Date:** 2026-03-29

**Goal:** Decompose the 237× vortex stretching slack into three constituent factors and characterize the geometric factor through strain-vorticity alignment statistics.

**What was done:** Full 3-factor decomposition at 15+ timesteps for Re=100 (N=48) and Re=1000 (N=64). Strain eigendecomposition at every grid point. Enstrophy-weighted alignment PDFs, depletion factors, vorticity direction gradient. Sharp Ladyzhenskaya constant survey on T³.

**CRITICAL FINDING — Corrected decomposition (exploration 002 estimates were wrong):**

| Factor | Exploration 002 estimate | Corrected (Exploration 004) | % of log-slack |
|---|---|---|---|
| α_geom (geometric/Hölder) | ~9× | **5.3×** | **31%** |
| α_Lad (Ladyzhenskaya constant) | ~18.6× | **31×** | **63%** |
| α_sym (symmetric) | ~1.4× | **√2 (exact)** | **6%** |

**The Ladyzhenskaya inequality, not Hölder alignment, is the dominant source of vortex stretching slack.** This reverses the priority order from exploration 002.

**Why Ladyzhenskaya dominates:** The effective Ladyzhenskaya constant for the flow's vorticity is C_{L,eff} = 0.147, only 18% of the R³ sharp constant C_L = 0.827. NS solutions are smooth and spectrally extended; the Ladyzhenskaya optimizer is a concentrated spike. The bound is structurally suboptimal for NS-like fields.

**Alignment statistics at the 237× point:**
- Vorticity preferentially aligns with extensional strain: ⟨cos²θ₁⟩_ω = 0.479 (44% above isotropic)
- Vorticity avoids compressive strain: ⟨cos²θ₃⟩_ω = 0.213 (36% below isotropic)
- Depletion factor = 0.44 (actual stretching is 44% of worst-case)
- Compressive cancellation contributes 53% reduction
- Alignment is robust across Re (<2% difference at matched slack levels)

**Sharp Ladyzhenskaya constant on T³ (div-free):**
- Best found: C_{L,div-free} = 0.279 (single mode sin(x)ê_y)
- This is 34% of C_L(R³) = 0.827 — significant improvement but the effective constant for actual NS flows (0.147) is even lower
- Single modes can't approach C_L(R³) because they're spatially uniform; the R³ optimizer is concentrated

**Unexpected findings:**
- Time dynamics: α_geom drops from >50 to ~4.2 while α_Lad grows from ~18 to ~49. The 237× minimum occurs where they cross.
- TGV shows extensional alignment (cos²θ₁ dominant), not intermediate alignment as in fully-developed turbulence (Ashurst et al. 1987). Transition likely at higher Re.
- ||∇ξ||_{L²} (Constantin-Fefferman quantity) grows monotonically: 38→56 over the simulation.

**Verification scorecard:** 6 VERIFIED, 12 COMPUTED, 1 CHECKED, 3 CONJECTURED.

---

## Exploration 003: Vortex Stretching Slack Across Multiple ICs + Adversarial Search

**Explorer type:** Math | **Outcome:** Succeeded | **Date:** 2026-03-30

**Goal:** Measure vortex stretching slack across 5+ initial conditions (TGV, ABC, random Gaussian, vortex tube, anti-parallel tubes) and adversarially search for configurations that minimize it.

**What was done:** 5 ICs tested at N=64, Re=100/500/1000. 120-point parametric grid search over tube parameters. Sigma (tube width) sweep from 0.5-5.0. N=128 convergence validation.

**Key results — Slack comparison across ICs:**

| IC | Min Slack | Notes |
|---|---|---|
| TGV (baseline) | 237× | Re-independent minimum |
| ABC (Beltrami) | ∞ | Zero VS by geometric identity (ω=u) |
| Random Gaussian | 1587× | Loosest finite slack |
| Single vortex tube | 977× | σ=0.2 |
| Anti-parallel tubes | 1551× | σ=0.2 (narrow) |
| **Anti-parallel (adversarial)** | **158×** | σ=2.5, d=π/4, δ=1.2, Re=100 |

**Best adversarial VS slack: 158× (converged at N=128)** — 34% below TGV baseline. No IC achieved slack < 50×.

**Key finding: tube width (σ) is the dominant adversarial parameter** — bowl-shaped curve with minimum at σ ≈ 2.5 (≈ 0.4 × domain size). Narrow tubes >1000×, optimal width 158×, wide tubes 170×.

**Unexpected findings:**
- z-invariant vortex tubes have EXACTLY zero VS (strain acts in xy plane, ω in z — exactly orthogonal)
- ABC (Beltrami) flow has infinite slack at all times (VS ≡ 0 when ω=u by incompressibility)
- Optimal tube width ≈ 0.4× domain suggests periodic geometry plays a role
- Separation, perturbation amplitude, tilt, and circulation ratio are all secondary to tube width

**Strategic implication:** ~158× appears to be a fundamental limitation of the Hölder + Ladyzhenskaya proof structure, not our IC search. The bound is structurally suboptimal for NS flows.

**Verification scorecard:** 0 VERIFIED, 8 COMPUTED, 5 CHECKED, 2 CONJECTURED.

---

## Exploration 005: Literature Survey — Improved Vortex Stretching Bounds & Alternative Enstrophy Closures

**Explorer type:** Standard | **Outcome:** Succeeded | **Date:** 2026-03-30

**Goal:** Survey the literature on improved vortex stretching bounds, spectral/frequency-localized estimates, and alternative enstrophy closures.

**What was done:** 28 papers surveyed with exact theorem statements across three topics: geometric regularity criteria (CF93, DV-B02, Grujić, Chae-Lee — 8 papers), spectral/Besov methods (Koch-Tataru, Cheskidov-Shvydkoy, Gallagher-Koch-Planchon, Tao — 9 papers), alternative closures (BKM, Kozono-Taniuchi BMO, Doering-Foias ladder, stochastic, Bradshaw-Farhat-Grujić intermittency, Protas numerical — 11 papers).

**CRITICAL FINDINGS:**

1. **No "spectral Ladyzhenskaya inequality" exists in the literature.** No paper proves W^{1,2}↪L⁴ with reduced constant for spectrally extended fields. This is an open problem and a notable gap.

2. **Tao (2014) is a hard obstruction:** Averaged NS blows up despite satisfying all harmonic analysis bounds. Any tighter C_L must exploit the differential NS structure. Pure Fourier multiplier improvements cannot close regularity.

3. **BKM is ~13× tighter than Ladyzhenskaya for NS flows:** Our 12× Agmon slack vs 158× Ladyzhenskaya slack is NOT remarked on in the literature. This suggests translating BKM-type analysis back to enstrophy level via Kozono-Taniuchi could yield much tighter effective bounds.

4. **Bradshaw-Farhat-Grujić (2019) intermittency is the most relevant framework for the 63% C_L component.** Spatial intermittency (vorticity concentrated in fraction μ of volume) algebraically reduces the scaling gap.

5. **Protas group (2020) confirms the bound is functionally tight:** Max enstrophy ~ E₀^{3/2} IS achievable for adversarial ICs. The 158× is for our tested flows, not the true worst case.

**Assessment of 158× slack reducibility:**
- By 2×: Almost certainly yes (geometric + intermittency)
- By 10×: Possibly (combined geometric + spectral + intermittency)
- Full closure (158× → 1): Not achievable without proving regularity. Requires differential NS structure (Tao obstruction).

**Key gap identified:** The "spectral Ladyzhenskaya inequality" — tighter C_L for spectrally localized fields — is an open problem with clear computational motivation from our data.

**Three most promising approaches:**
1. Spectral Ladyzhenskaya (addresses 63% component) — open problem, exploration 006 computing this
2. Bradshaw-Farhat-Grujić intermittency calibration (explains C_{L,eff}/C_L)
3. Kozono-Taniuchi BMO applied to enstrophy level (BKM's 12× advantage)

---

## Exploration 006: Spectral Ladyzhenskaya Inequality — Effective Constants for Spectrally Localized Fields

**Explorer type:** Math | **Outcome:** Partially Successful | **Date:** 2026-03-30

**Goal:** Compute effective Ladyzhenskaya constants for spectrally localized fields and formulate a spectral Ladyzhenskaya inequality.

**What was done:** C_{L,eff} computed for band-limited fields (k₀=2,4,8,12), power-law spectra (α=5/6,1,3/2,11/6), div-free vector fields, NS-like spectra. Littlewood-Paley decomposition analysis. Phase optimization via L-BFGS-B. 200-500 samples per configuration.

**KEY FINDING — Critical Negative Result:** A spectral Ladyzhenskaya with improved constant **CANNOT be proven** without phase information. For any spectral envelope, adversarial phase alignment achieves C_eff comparable to the universal sharp constant. The observed C_{L,eff} = 0.147 for NS flows is a *statistical property* (random-phase-like behavior), NOT a provable worst-case bound.

**Positive results:**

1. **Gaussian regime formula** [COMPUTED]: C_{L,eff} = 1.707 × Re^{-3/8} for Kolmogorov spectra. At Re=1000: C_{L,eff} ≈ 0.125, ratio = 0.20 (matches our observation of 0.147/0.827 = 0.18).

2. **Divergence-free factor** [VERIFIED]: C^{vec}_{L,eff}/C^{scalar}_{L,eff} = **(5/9)^{1/4} ≈ 0.863** exactly. Analytical derivation from flatness of χ²₃ distributions. Confirmed to 4 significant figures. This is a clean, provable ~14% reduction.

3. **LP analysis** [COMPUTED]: Cross terms dominate (63% of ||f||⁴_{L⁴} for Kolmogorov). Band-by-band Bernstein estimates FAIL — LP decomposition cannot improve the constant.

4. **Torus vs R³** [COMPUTED]: Band-limited fields at k₀=2 on T³ EXCEED C_L(R³) (up to 1.305 vs 0.629), confirming torus constants differ at low frequencies.

**Strategic implication:** The spectral direction is a dead end for worst-case bounds. The 63% Ladyzhenskaya slack is explained by statistical/phase properties, not spectral support. The path forward is: either prove flatness bounds for NS solutions (intermittency theory) or use alternative closure strategies (BKM/Kozono-Taniuchi).

**Verification scorecard:** 1 VERIFIED, 8 COMPUTED, 1 CHECKED, 2 CONJECTURED.

---

## Exploration 007: BMO Norms, Intermittency, BKM vs Ladyzhenskaya Advantage

**Explorer type:** Math | **Outcome:** Succeeded | **Date:** 2026-03-30

**Goal:** Quantify the BKM advantage over Ladyzhenskaya, compute BMO norms (Kozono-Taniuchi), measure spatial intermittency, and formulate a conditional enstrophy bound.

**HEADLINE FINDING: BKM has only 1.05× slack vs Ladyzhenskaya's 237× — a 226× advantage factor.** The BKM bound is near-tight for NS flows while Ladyzhenskaya wastes >200×. The advantage GROWS with Re (221× at Re=100 to 535× time-averaged at Re=5000). BKM min slack is completely Re-independent at 1.05.

**Other major findings:**

| Measurement | Value | Significance |
|---|---|---|
| BKM min slack | 1.05× | Near-tight — the BKM constant captures NS dynamics to within 5% |
| BKM advantage (min) | 226× | Ladyzhenskaya chain is 226× looser than BKM for same flows |
| BKM advantage (mean, Re=5000) | 535× | Advantage grows with Re |
| BMO/L^∞ ratio | 0.25-0.27 | Universal across Re; gives ~4× Kozono-Taniuchi tightening |
| Vorticity flatness F₄ | 3-12 (peak) | 2-7× more intermittent than Gaussian |
| Volume fraction μ(0.5) | 1-2.4% | Only 1-2% of domain has |ω| > 0.5×ω_max |
| Flatness-C_{L,eff} correlation | r = -0.93 | Strong correlation; exponent -0.30 (prediction was -0.25) |
| Conditional bound | C(F₄) ≈ 0.003/F₄ | Near-exact 1/F₄ scaling |

**Why BKM is tighter:** BKM uses pointwise vorticity ‖ω‖_{L^∞} directly with only a logarithmic correction (log term = 2.1-3.6 for smooth flows). Ladyzhenskaya chains through L² norms and interpolation, losing ~31× from the constant and ~5× from geometric alignment/cancellation.

**The conditional bound C(F₄) ≈ 0.003/F₄ means:** At Gaussian flatness (F₄=5/3), recovers the known 237× slack exactly. For more intermittent flows (F₄=10), the tightening is 1100×. But this is conditional — requires proving flatness stays bounded.

**Assessment:** The BKM 226× advantage is the headline finding. It shows the Ladyzhenskaya chain is the wrong tool for measuring regularity proximity. The intermittency analysis explains WHY Ladyzhenskaya is loose, but BKM simply bypasses the problem.

**Verification scorecard:** 0 VERIFIED, 18 COMPUTED, 0 CHECKED, 3 CONJECTURED.

---

## Exploration 008: Adversarial Review of All Strategy-001 Findings

**Explorer type:** Standard | **Outcome:** Succeeded — Multiple Genuine Weaknesses Identified | **Date:** 2026-03-30

**Goal:** Adversarially review 7 key claims from explorations 001-007.

**Verdicts:**

| Claim | Verdict | Novelty | Key Problem |
|---|---|---|---|
| BKM 226× advantage | **WEAKENED** | Partially Known | Apples-to-oranges comparison (different quantities); empirical C calibration makes 1.05× partly circular; with theoretical C, advantage is ~80× |
| 158× irreducible slack | **WEAKENED** | Novel | Domain-dependent; Protas adversarial ICs not tested; "irreducible" unjustified |
| 3-factor decomposition | **WEAKENED** | Partially Known | Product identity is algebraic tautology; IC-specific |
| BMO/L^∞ ≈ 0.27 | **INCONCLUSIVE** | Novel | Ball-sampling may underestimate; only TGV; Re range narrow |
| (5/9)^{1/4} div-free factor | **WEAKENED** | Partially Known | **FACTUAL ERROR: NOT about div-free constraint.** Vector component effect (3 vs 1), not incompressibility. Numerically confirmed. |
| C(F₄) ≈ 0.003/F₄ | **INCONCLUSIVE** | Novel | Purely empirical; single IC |
| Spectral Lad dead end | **INCONCLUSIVE** | Novel | Direction correct; phase optimization was local search only |

**Most defensible finding:** The decomposition showing Ladyzhenskaya interpolation is the dominant bottleneck (63% of log-slack) combined with C_{L,eff}/C_L ≈ 0.18 for NS flows. Novel and actionable.

**Key corrections:**
1. Reformulate BKM comparison: "CZ gives near-tight ‖∇u‖_{L^∞} bounds; 237× slack lives in interpolation chain" (not "BKM 226× advantage")
2. Remove div-free attribution from (5/9)^{1/4} — it's a vector component effect
3. Replace "irreducible" with "lower bound from tested ICs"
4. Use theoretical BKM constant (~80× advantage) not empirical (~226×)
