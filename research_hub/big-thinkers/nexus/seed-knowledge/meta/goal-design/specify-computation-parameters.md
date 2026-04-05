---
topic: Specify exact computational parameters in simulation goals
category: goal-design
date: 2026-03-27
source: "yang-mills strategy-001 meta-exploration-003, classicality-budget strategy-001 meta-exploration-002, classicality-budget strategy-001 meta-exploration-005, classicality-budget strategy-002 meta-exploration-008, amplituhedron strategy-001 meta-exploration-006, riemann-hypothesis strategy-002 meta-exploration-004, yang-mills strategy-002 meta-exploration-s002-002, riemann-hypothesis s002-meta-exploration-005, stochastic-electrodynamics s002-meta-exploration-011, riemann-hypothesis s002-meta-exploration-006, yang-mills strategy-002 meta-exploration-s002-005, yang-mills strategy-002 meta-exploration-s002-006, stochastic-electrodynamics strategy-003 meta-exploration-s003-001, stochastic-electrodynamics strategy-003 meta-exploration-s003-003, riemann-hypothesis s003-meta-exploration-002, riemann-hypothesis s003-meta-exploration-004, thermal-time strategy-002 meta-exploration-001"
---

## Lesson

When a goal involves numerical simulation, specify exact parameter values: coupling constants (β values), lattice sizes, number of thermalization sweeps, measurement counts, and sweep gaps. Leaving these to the explorer's discretion produces usable but less comparable results. Specific parameters give clear, reproducible, comparable output.

## Evidence

- **yang-mills strategy-001 exploration 003** — Specifying exact β values (2.0, 2.2, 2.3, 2.5, 3.0) and lattice sizes (4⁴, 6⁴, 8⁴) produced a comprehensive, systematically organized dataset that could be compared directly against literature values. The explorer implemented a full SU(2) lattice gauge theory simulation from scratch with these parameters and every plaquette value matched the literature within 1-2σ.
- **classicality-budget strategy-001 exploration 002** — Providing all formulas (R_delta <= S_max/S_T - 1), physical constants (ℏ, c, G, l_P in SI), and system parameters (exact masses, radii, energies for 7 systems) meant the explorer could compute immediately without research. The exploration completed in ~8 minutes — the fastest in the mission. All 7 sanity checks passed on first run.

## Variant: Name the Exact Formula, Not Just the Concept

Specifying the exact named formula to use (e.g., "Sackur-Tetrode formula" rather than "ideal gas entropy") produces better results than a conceptual description. Named formulas are unambiguous; conceptual descriptions admit multiple valid implementations that may not be directly comparable.

- **classicality-budget strategy-001 exploration 005** — Providing explicit formula names (Sackur-Tetrode for translational entropy, Debye T³ law for phonons, Stefan-Boltzmann/Planck for photons) gave the explorer clear targets with no ambiguity. The formulas were correctly implemented and cross-verified. A goal saying "compute gas entropy" would have left the choice of formula to the explorer and risked inconsistent implementations across systems.

## Variant: Ask for the Key Ratio or Comparative Metric Explicitly

When comparing two related quantities (e.g., actual vs. theoretical, measured vs. predicted), ask explicitly for the ratio or comparison metric — not just the individual values. Without an explicit ratio request, explorers compute both values but may not compute or highlight the ratio, which is often the most revealing number.

- **classicality-budget strategy-001 exploration 005** — The most dramatic finding was S_eff/S_Bek = 10^{-16} to 10^{-35} across systems (Bekenstein overestimates by 16–80 orders of magnitude). This ratio was computed, but retrospectively the goal should have explicitly asked for "ratio S_eff/S_Bek for each system" — it would have been foregrounded in the report rather than derived from the table. The 80-order-of-magnitude range for the BH Hawking case (S_eff/S_Bek = 1.76 × 10^{-80}) was the most extreme finding and deserved top billing.

## Variant: Provide Actual Code Templates (Strongest Form)

The strongest version of parameter specification is to provide actual Python function skeletons (or pseudocode) in the goal, not just parameter lists. This eliminates not just parameter ambiguity, but also the exploration's research time for formula lookup.

- **classicality-budget strategy-002 exploration 003** — The goal included specific Python functions (`bekenstein_bits`, `photon_entropy_bits`) and a table template for output. The result was a systematic computation across 8 systems using appropriate physics formulas for each (phonon sum for ion trap, photon gas for BEC/BH, Debye solid for nanodot). The explorer spent zero time on "which formula to use" — it just implemented and ran them.

Use code templates when: the formulas are known, the explorer would otherwise spend time looking up the right formula, and reproducibility matters. The trade-off is that it constrains the explorer's approach — only use when there's a clear right answer for the formula.

- **stochastic-electrodynamics strategy-002 exploration-005** — Pre-loading the exact Python function for the ALD/ZPF SED simulation (including the ω_max cutoff applied correctly in the PSD body) made E005 the fastest SED computation yet — the explorer pasted the code directly and ran 7 λ values with no debugging of noise normalization. By contrast, the GOAL.md code template had a bug: ω_max was declared as a parameter but not applied in the PSD formula body. The explorer had to find and fix the bug. Two lessons: (1) confirmed that exact code templates eliminate research + setup time; (2) **test your template code before pasting it** — see the "Verify Code Before Preloading" variant in preload-context-from-prior-work.md.

## Variant: Sequence Computations From Fast to Slow to Enable Early Filtering

When a goal has a cheap pre-computation (< 1 min per parameter value) that determines whether a costly simulation (> 5 min) is worthwhile, explicitly specify the order in the goal: **"Run [fast step] first for all parameter values, then proceed to [slow step] only for parameters that satisfy [criterion]."** Without explicit ordering, explorers often run steps in the order they appear in the goal — potentially wasting hours on uninteresting parameter values.

- **stochastic-electrodynamics strategy-002 exploration-005** — The goal asked to run SED simulations at 5+ λ values. For each λ, the QM diagonalization (Schrödinger eigenvalues via scipy.linalg) takes seconds and immediately tells you whether E₀ < V_barrier (tunneling regime) or E₀ > V_barrier (over-barrier). Specifying "run all QM first" let the explorer filter out over-barrier cases before committing any SED simulation time. This was especially valuable at λ=0.30, which was close to the crossover — QM confirmed tunneling regime before the long SED run.

**Pattern:** "Run [fast diagnostic] first. For parameter values where [condition satisfied], proceed to [slow computation]. Skip the rest." Most useful when: individual slow runs take > 5 min; there's a simple discriminating criterion available from a fast proxy; the fast step result fully determines whether the slow step is needed.

## Variant: Specify Integration Region for Physics Integrals

When a goal includes a definite integral with a non-obvious or potentially ambiguous integration domain (e.g., a WKB action integral, a Casimir integral over momenta, a partition function contour), **state the integration region explicitly — not just the formula.** The formula name alone leaves the domain unspecified, and wrong domain choices produce systematic errors that are hard to diagnose.

- **stochastic-electrodynamics strategy-002 exploration-005** — The goal stated S_WKB should be computed but did not specify "inner turning points only." One code version integrated from outer turning points (including the contribution of the outer confining walls), producing S_WKB values 20–50% larger than the correct inner-barrier-only integral. The correct specification is: "Integrate between the two inner turning points where V(x) − E₀ = 0 near x = 0 (the central forbidden region only). Do NOT include outer turning points where the confining potential eventually rises again." Adding this one sentence to the goal would have prevented the bug.

**Rule:** For any physics integral, include: (1) the integrand formula, (2) the integration variable, (3) the lower and upper limits with a plain-language description of what they are (e.g., "inner turning points," "first positive root," "below the Fermi surface"). If the limits are solutions to implicit equations, give the equation. Effort: 1 extra sentence. Cost of omission: potentially invalid data from the entire exploration.

## Variant: Ask a Threshold-Finding Scanning Question

When you suspect there's a critical parameter value (e.g., temperature, length, occupation number) that separates two qualitatively different regimes, ask explicitly: "For what value of [parameter X] does the system enter regime Y?" This causes the explorer to scan the parameter space and identify the transition, rather than only computing at fixed values.

- **classicality-budget strategy-002 exploration 003** — The BEC at L = 1 μm had R_max ~ 2 (tight regime) while L = 100 μm had R_max ~ 475 (non-tight). In retrospect, the goal should have included: "For what BEC length L does R_max first enter the R_max < 10 regime?" This would have flagged the 1 μm threshold explicitly. Instead, the scan was done post hoc as a table rather than as a targeted question.

Ask threshold-finding questions when: there's a qualitative phase transition likely in the parameter space (classical/quantum, constraining/non-constraining), and the transition value is not obvious from dimensional analysis alone.

## Variant: Specify Normalization to Match Prior Explorations

When comparing a fitted exponent (e.g., α in Δe ~ β^α) across multiple explorations, **explicitly specify which normalization target to use and whether it should match the prior run**. Normalization choice can shift the fitted exponent significantly even when the underlying physics is the same.

- **stochastic-electrodynamics strategy-001 exploration-007** — E004 used natural SED normalization (var_x(β=0) ≈ 0.516); E007 calibrated to 0.500. The fitted exponents disagreed by ~60%: α≈0.40 (E004) vs α≈0.25 (E007). The ratio tests were statistically consistent within ~1σ, so the qualitative finding was robust — but the fitted α was not comparable because the baselines differed. Had the goal specified "normalize to var_x(β=0) = 0.516, matching E004," the comparison would have been direct. Always state: "use [calibrated / physical / matched to Exx] normalization."

## Variant: Request Sign and Magnitude for All Variants

When the goal compares multiple variants where the observable could be positive for some and negative for others, **explicitly ask for (1) the sign of the error for each variant and (2) the power-law fit |Δe| ~ β^α for each variant regardless of sign**. Without this, explorers may skip the power-law fit for "negative" variants, leaving the α-vs-n dependence uncharacterized.

- **stochastic-electrodynamics strategy-001 exploration-007** — The explorer correctly reported the sign reversal (n=3 positive, n<3 negative) but marked α=null for n=0,1,2 because Δe was negative. The report still noted qualitative behavior (saturation, flat α for n=0), but a systematic table of α(n) for all n required post-hoc extraction. Goal should have said: "For each spectrum, report: (a) sign of Δe, (b) power-law fit |Δe| = C × β^α at β ∈ {0.2, 0.5, 1.0}, regardless of sign."

## Variant: Verify Physical Constants in the Correct Unit System Before Writing the Goal

For simulations that require a physical constant (e.g., radiation reaction time τ, fine structure constant α, Bohr radius), **derive the constant explicitly in the target unit system and cross-check against published values before writing the goal.** Providing a value that is wrong by even a factor of 10 can make all quantitative outputs unphysical.

The most common failure mode: unit system conversion errors. If the goal needs τ in atomic units but the published value is in SI, the conversion must be explicitly verified — not assumed from memory.

- **stochastic-electrodynamics strategy-002 exploration-003** — The goal specified τ = 1.57×10⁻⁵ a.u. for the hydrogen simulation. The physical ALD value is τ_phys = 2e²/(3m_ec³) = 2α³/3 ≈ 2.6×10⁻⁷ a.u. (confirmed by Cole & Zou 2003). The goal value was ~60× too large. The explorer flagged this discrepancy in the report, rescuing the qualitative findings — but all T_ion values are ~60× shorter than physical hydrogen timescales. The fix: before writing, verify τ = (2/3)(e²/m_ec³) in atomic units. Provide the value in both SI and atomic units so the explorer can sanity-check.

**Template:** In goals requiring a physical constant, include: "Value: X [unit system]. Derivation: [formula]. Literature cross-check: [citation] gives X' = Y [same unit system]." If X ≠ X', investigate before proceeding.

## Variant: Provide Exact Implementation Formula for Normalization-Sensitive Statistics

For statistics with subtle normalization conventions (pair correlation R₂, spectral rigidity Δ₃, structure factors, etc.), **provide the exact implementation formula in the goal, not just the statistic's name**. The name alone is insufficient — there are multiple equivalent-looking formulas with different normalizations that produce wildly different numerical results.

- **riemann-hypothesis strategy-002 exploration-001** — Two statistics were computed incorrectly due to normalization ambiguity:
  - **Pair correlation R₂:** The explorer implemented R₂ using raw bin density as the denominator, rather than the smooth two-point density estimate. The resulting MRD = 0.996 was reported as a result but is numerically meaningless. The correct formula requires: `R₂(r) = (N/(N−1)) × Σ_{i≠j} K((E_i−E_j)/⟨Δ⟩ − r) / (N × bandwidth)` with a smoothing kernel K and normalization forcing R₂ → 1 for large r.
  - **Spectral rigidity Δ₃:** The explorer implemented `mean(residuals²)/L` rather than the correct Dyson-Mehta integral `Δ₃(L) = (1/L) ∫₀ᴸ [N(E+x)−ax−b]² dx (min over a,b)`. The bug produced values 10–25× too small and a decreasing trend with L (backwards from physical expectation).

Include the exact algorithmic formula — not just the physical definition — for any statistic where normalization convention matters. The physical definition and the correct computational formula are often different, and the gap is where bugs live.

**Additionally:** Provide a known numerical value from a prior exploration as a second anchor, not just the formula. Normalization bugs can produce a result that looks plausible but is wrong by a factor of 2 — a known value immediately identifies the error direction.

- **riemann-hypothesis strategy-002 exploration-004** — The goal provided *both* Berry's formula Δ₃_sat ≈ (1/π²) log(log(T/2π)) AND the prior measured value Δ₃ = 0.156 from strategy-001. This dual check revealed that the sum formula (which had been giving ~0.069) was wrong by a factor of ~2; the integral formula matched the prior value (0.156 ≈ 0.1550). Either check alone might have been inconclusive; together they identified both the formula bug and the correct formula.

## Variant: Include Physics Sanity Checks as Intermediate Verification Steps

For physics computations with known non-negativity or sign constraints (e.g., spectral densities, probabilities, optical theorem), **include explicit sanity check steps in the goal**: "Verify that Im M(s,0) ≥ 0 for all sample points before computing moments" or "Confirm normalization integral = [expected analytic value] within 5% before proceeding." These checks catch implementation bugs more reliably than code-level testing because physics expectations are often simpler to state and easier to violate than code logic.

- **amplituhedron strategy-001 exploration-006** — The explorer initially had a threshold bug in the Breit-Wigner model (threshold set at s=0 instead of near the resonance peak). The bug was caught not by a code error, but because the computed moment ratios were "unphysical" in scale. Had the goal included "verify Im M(s,0) = 0 below (M_res - 5Γ)²," the bug would have been caught immediately at Stage 1 before propagating into Stage 2 computations.

Include a sanity check when: the computation involves a quantity with a known physics sign/bound (spectral density ≥ 0, probability ∈ [0,1], cross-section ≥ 0, ratio close to an analytic limit). Frame it as "verify X before proceeding to Y."

## Variant: Build Formula Disambiguation Into the Goal When Implementations Disagree

When two implementations of the same statistic have previously given different answers, make the disambiguation explicit in the goal: **"Which formula is correct and why?"** rather than just providing parameters. This produces a cleaner result than hoping the explorer uses the right formula.

The pattern: name both implementations, state that they disagree, ask for a definitive resolution. The explorer will then investigate the structural reason (e.g., sum vs. integral formula), test both against an independent reference, and report a definitive conclusion.

- **riemann-hypothesis strategy-002 exploration-004** — The goal noted the prior discrepancy (sum formula giving ~0.069 vs. the prior measured value of 0.156) and asked the explorer to investigate which formula was correct. The explorer identified the integral vs. sum distinction, computed both, confirmed the integral formula matches the reference, and documented the precise algorithmic difference (staircase plateau regions included vs. omitted). Without the disambiguation framing, the explorer might have used the sum formula and reported a "result" that was wrong by 2×.

Apply when: a prior exploration used a formula that produced suspicious values, or two implementations of "the same" statistic are documented as disagreeing.

## Variant: Specify Physical Dimension Separately from Lattice Geometry

When a goal involves a lattice simulation for a d-dimensional physics problem, **explicitly specify d in the Hessian/action formula** as well as the lattice geometry. Saying "4³ lattice" is ambiguous: it could mean d=3 (3D physics, L=4) or d=4 physics on a small lattice. Specify: "d=4, L=4 lattice (4^4 = 256 sites)."

- **yang-mills strategy-002 exploration-005** — The goal said "4³ lattice (3D is fine)." The explorer used d=3 throughout, computing the Hessian with the d=3 bound factor (32β). The most important case is d=4 (physical Yang-Mills). The 3D result (12-45× slack) was still valuable, but required an immediate follow-up (E006) to verify in d=4. Better: "Run on a 4^3 lattice BUT use d=4 in the Hessian formula (bound = 48β). We are testing the 4D physics even on a small lattice."

**Rule:** For any goal where physical dimension ≠ lattice spatial dimension (e.g., measuring a d=4 bound on a 4³ lattice for speed), state both explicitly: "Physical dimension d=4 (used in all formulas). Lattice geometry: 4³ for speed."

## Variant: Include Both Typical-Config and Worst-Case Search for Bound Measurements

When measuring whether an analytic bound is tight (i.e., H_norm ≈ 1 vs. H_norm ≪ 1), **always include BOTH a typical Gibbs-configuration scan AND an adversarial worst-case search**. A bound that is loose for typical configurations might still be saturated by non-Gibbs configurations that the proof applies to.

- **yang-mills strategy-002 exploration-005** — Measured H_norm for Gibbs configurations only. The finding (12-45× slack) was major, but left open whether adversarial configurations could saturate the bound. Follow-up E006 tested three adversarial strategies (gradient ascent, aligned configs, eigenvalue search) — all gave slack ≥176×.

**Template for bound measurement goals:** "Run two sections: (1) Scan typical Gibbs configurations at β = [values]. (2) Adversarial search: test [aligned configs / gradient ascent / structured perturbations] to find configurations that maximize H_norm. Report slack factor for both sections. Goal is to determine if the bound is tight even in the worst case."

**Three adversarial strategies that are quick and thorough:** (a) aligned configurations (U_e = exp(iα_e σ_j) with fixed generator), (b) gradient ascent on H_norm (10-20 steps), (c) power iteration to find dominant Hessian eigenvector.

## Variant: Print-First Discipline for Long-Running Scans

For scans across many parameter values where each run takes minutes, instruct **"print results as you compute each data point, don't wait until all runs finish."** This provides partial results even if later runs fail or time out, and allows the strategizer to assess quality early.

- **yang-mills strategy-002 exploration-002** — A spectral gap scan at 8 β values took ~8 minutes per β. Instructing "print results as you go" meant each data point was reported immediately when computed. This was essential because the total runtime (64 min) was at the edge of feasibility. Without print-first, a failure late in the scan would have lost all earlier data.

Apply for any β-scan, parameter sweep, or sequential computation where: individual runs take > 3 min, and total runtime > 30 min.

## Variant: Cross-Check First Data Point Before Full Scan

For parameter scans, instruct: **"Cross-check your first data point against a known analytic or literature value before running the full scan."** If the first result is wrong, stop and debug rather than running 8 more β values.

**Red flag rule:** "If computation finishes much faster than expected (e.g., < 30 seconds per data point when 8 minutes is expected), something is wrong — check against known results before proceeding."

- **yang-mills strategy-002 exploration-002** — The initial parallel heat bath implementation gave ⟨P⟩ ≈ 0 at all β including β=3.0 — obviously wrong, and the computation finished in seconds (not 8 minutes). The fast completion was the red flag: KP rejection sampling should be slow at small β. Cross-checking ⟨P⟩(β=3.0) ≈ 0.72 against literature would have caught this immediately. Instead, ~15 minutes were wasted before the bug was diagnosed.

Include explicitly: "Verify ⟨P⟩ ≈ [expected value] at β=[first point] before running the full scan. If it doesn't match, stop and debug the implementation."

Apply for any simulation scan. The one-point cross-check is cheap (one run) and prevents wasting hours on garbage data.

## Variant: Specify Parameter Bins for Testing Scaling Predictions

When testing a theoretical prediction of the form "quantity X increases monotonically with parameter T," **specify the explicit bins in the goal** (e.g., "divide the zeros into 4 height bins of 500 each; compute Δ₃_sat for each bin"). This produces a richer result than a single overall comparison: it reveals whether the formula is accurate at all T values or only on average, and it makes the monotone increase directly verifiable.

- **riemann-hypothesis strategy-002 exploration-004** — The goal specified 4 height bins (500 zeros each). The binned analysis revealed that Berry's formula is essentially exact (0.2% error) for the lowest T bin but overestimates by 7.8–12.5% for higher bins. This height-dependent accuracy is a physically interesting result — it suggests corrections from short prime orbits become more important at higher T. A single overall comparison (7.6% error) would have obscured this structure. The monotone increase (0.1435 → 0.1545 → 0.1569 → 0.1595) was directly confirmed, not just inferred.

Apply when: a theoretical formula predicts a quantity that depends on a control parameter, and you want to test both the overall accuracy and the T-dependence of the formula.

## Variant: Provide Exact Code or Formula for Baseline Comparison Values

When asking an explorer to reproduce or compare against a prior exploration's numerical result (e.g., β from a prior matrix sweep), **provide the exact code or formula used to generate that baseline value**. Do not just give the number. Small implementation differences — 0-indexed vs. 1-indexed, exact Hermitianization, polynomial degree — can shift β by 0.3–0.5.

- **riemann-hypothesis s002-meta-exploration-005** — The goal for exploration-005 included a baseline table with β=0.880 at p=97 and β=1.092 at p=997 from S002-E001. The explorer reproduced p=97: β=0.880 exactly, then spent time investigating why a v1/v2 implementation of the p sweep didn't match. Root cause: v1/v2 used 0-indexed (j,k) while S002-E001 used 1-indexed (j+1)(k+1). The baseline values were correct but their reproduction required matching the exact construction. Had the goal provided the exact S002-E001 loop structure (or noted "1-indexed: j,k ∈ {1,...,N}"), the investigation would have been shorter.

**Rule:** When a prior β, KS, or MRD value is given as a baseline, include either (1) the exact lines of code that generated it, or (2) a precise statement of the matrix construction (indexing, Hermitianization method, unfolding degree). β in particular is sensitive to: indexing convention, β estimation method (log-log vs. KS), polynomial unfolding degree, and number of matrices averaged.

## Variant: Add Startup Diagnostics for Fragile Library Imports

When a goal uses a scientific Python library known to have compatibility issues with newer NumPy/SciPy versions (scipy.optimize, sklearn, etc.), **add a one-line startup diagnostic** at the top of the goal's computation instructions: `python3 -c "import [library]; print([library].__version__)"`. If the import fails, the explorer immediately switches to an alternative — rather than discovering the failure mid-computation and burning exploration time on debugging.

- **riemann-hypothesis strategy-002 exploration-006** — `scipy.optimize` failed with `ImportError: numpy.Inf` (removed in NumPy 1.25+). The explorer spent many iterations debugging this instead of extracting already-computed results. A startup check `python3 -c "import scipy.optimize; print(scipy.__version__)"` would have caught this before computation began.

**Fallback specification:** Pair the diagnostic with an explicit fallback: "If scipy.optimize import fails, use manual Brody fit: ρ(s) = A·s^β·exp(−C·s^(β+1)), fit A, β, C by minimizing sum of squared residuals using scipy.stats or numpy.linalg.lstsq on log-transformed data." The fallback should be complete and runnable — not "use an alternative method."

**Most fragile libraries:** scipy.optimize (numpy.Inf deprecation), sklearn (frequent API changes), sympy (symbolic computation timeouts).

## Variant: Specify Expected Output File Keys for Data Extraction

When a goal produces a saved output file (e.g., `.npz`, `.pkl`, `.h5`), **include the exact key names** the explorer should use to extract results. Without this, the explorer may re-compute results from scratch rather than loading the saved file, or spend time probing the file structure.

- **riemann-hypothesis strategy-002 exploration-006** — Part B results were saved to `part_b_results.npz` but the report took many nudges to extract data because the explorer wasn't sure which keys to use. Had the goal specified: "Results are in part_b_results.npz with keys `beta_wigner`, `ks_stat`, `construction_name`," the extraction would have been immediate.

**Template:** "Computation output is in `[filename]`. Load with `np.load('[filename]')`. Keys: `[key1]` ([description]), `[key2]` ([description]). Use these directly to fill in the results table."

Most useful when: the computation is long-running (> 5 min) and you want the explorer to be able to write the report from saved data even if the analysis code fails.

## Variant: Provide Explicit Analytic Integral Setup for Pure Math Explorations

For pure-math/analytic goals, the strongest form is to provide the **explicit integral in the goal** — not just the physical setup. When the computation is fully specified (the exact integral, substitution, split, verification methods, and limiting cases), the explorer can solve it in a single focused pass without any web search. Reference suggestions become unnecessary overhead.

- **stochastic-electrodynamics strategy-003 exploration-003** — The GOAL.md provided the explicit angular integral ∫₋₁^1 (1+u²) e^{iqu} du (after φ integration), the Monte Carlo verification approach (N modes, random k-vectors, x-polarization projection), and asked for limiting cases (d→0, d→∞, 1D comparison). The explorer completed the full analytic derivation + three-method numerical verification in a single pass without any web search. A suggested reference (Ibison-Haisch 1996) was correctly ignored — the physics was fully self-contained. Result: machine-precision analytic + Monte Carlo (N=500k) in one shot, Tier 4+, no nudging. Structured goal (6 explicit sections) translated directly into 7 REPORT.md sections of matching quality.

**Pattern for pure-math explorations:** "Evaluate the integral [exact expression]. Use [substitution]. Split into [parts A and B]. Verify at [limiting case]. Confirm via [independent method] with N=[value]." The integral setup is the analytic equivalent of a Python code template — it eliminates the explorer's research time and focuses effort entirely on derivation.

**Corollary:** Don't add reference suggestions to self-contained analytic goals. If the integral can be derived from first principles, the explorer will and should solve it directly. References become unused overhead.

## Variant: Provide the Hierarchy of Approximations for Theory/Synthesis Explorations

For explorations that ask an explorer to EXPLAIN a known discrepancy between two theoretical frameworks (rather than to compute new values), **provide the hierarchy of approximations in the goal**: what does each level of the theory predict for the target observable? This enables the explorer to construct a complete structural picture — not just verify the formula, but situate the result within the full theory.

- **stochastic-electrodynamics strategy-003 exploration-001** — The goal asked the explorer to explain the SED discrepancy from Santos (2022)'s O(ħ²) framework. The goal specified: the target numbers to explain (0.046 discrepancy, slope=1.049), the comparison trio (ALD value 0.303, QM value 0.257, classical Boltzmann value 0.183), and the unit convention. The explorer independently derived the classical(0.183) < QM(0.257) < ALD(0.303) hierarchy at β=1, plus a novel symmetry argument proving the O(ħ²) correction to ⟨x²⟩ is zero at O(β). None of this synthesis was specified in the goal — it emerged from having the right comparison framework loaded.

**Template for theory/synthesis explorations:** In the goal, provide: (1) the target quantity to explain (e.g., "15-18% discrepancy between ALD and QM at β=1"); (2) at least two reference values bounding or bracketing the result (e.g., "QM gives ⟨x²⟩=0.258, ALD gives 0.303, classical Boltzmann at T_eff=ħω/2 gives 0.183"); (3) the unit convention. The explorer will then situate the theoretical mechanism within the complete picture rather than just verifying the sign of the correction.

**Contrast with pure numerical goals:** For numerical simulations, the key parameters are dt, ω_max, τ, etc. For theory/synthesis, the key "parameters" are the reference values at different approximation levels.

## Variant: Save Intermediate Results to .npz After Each Computation Block

When a goal involves multiple sequential computation blocks (each taking several minutes), **explicitly instruct the explorer**: "After completing each [ensemble/parameter value/block], save results to `results_NAME.npz` before proceeding to the next block." This enables crash recovery at block granularity, not just at the end.

**Why this matters:** Usage-limit deaths, context exhaustion crashes, and tmux failures all terminate the session without a final write. If results were only accumulated in memory or printed to stdout, they are permanently lost. Intermediate .npz files are the only recovery path.

- **riemann-hypothesis strategy-002 exploration-009** — The math explorer hit Claude's usage limit before writing the report. Manual completion was possible because the explorer had saved all three ensembles to `code/results_exact.npz`. Without the file, all computation would have been lost. The strategizer completed the report directly from the saved data.

**Template:** "After computing ensemble N, immediately save: `np.savez('results_N.npz', delta3_sat=delta3_sat, beta_wigner=beta_wigner, ensemble='N')`. Save after each ensemble — do not wait until all are done."

**Companion instruction:** "If you run out of time before writing the report, save all computed data to .npz and I will complete the report manually."

**Recovery:** When a session dies mid-task, check `ls code/*.npz` first. If found, load with `np.load(...)` and complete the report manually. *From RH s002-meta-009.*

## Variant: Specify the Exact Comparison Baseline (Full Interacting Theory vs. Free)

When a goal compares a model's prediction against "standard QM," **specify what "standard QM" means exactly**. Does it mean the full interacting Hamiltonian (H_AB), the free single-subsystem Hamiltonian (H_A), or the thermal free Hamiltonian? Explorers default to the free theory — the cleanest comparison that avoids secondary interactions — which is often the wrong baseline for the physics question.

- **thermal-time strategy-001 meta-explorations 001 and 002** — Both noted independently: "GOAL.md should explicitly state 'compare local modular flow vs. FULL QM (H_AB dynamics), not just free oscillator.'" Exploration-002 compared C_local_TTH against C_free (H_A evolution), finding 6.4% period shift. Exploration-003 then correctly compared C_local_TTH against C_full (H_AB evolution), finding the period shift is only ~1.3% — but the L² discrepancy (83%) is the more meaningful metric. The wrong baseline produced a misleading claim about the size of the TTH–QM disagreement.

**Rule:** In goals that compare two theories or models, explicitly write out the dynamics equation for each comparison:
- ✅ "Compare C_full = Tr[ρ_AB · e^{iH_AB τ} x_A e^{−iH_AB τ} · x_A] against C_local = Tr[ρ_A · e^{iK_Aτ/β} x_A e^{−iK_Aτ/β} · x_A]"
- ❌ "Compare the TTH prediction against standard QM"

The second form is unambiguous to you but admits multiple interpretations to the explorer.

**When to apply:** Any goal comparing a modified dynamics or modified Hamiltonian against "standard" or "conventional" theory. Especially important when: (1) the system is interacting (the free theory may differ substantially from the interacting theory); (2) the paper or prior exploration computed against the free theory; (3) the subsystem vs. global distinction matters.

## Variant: Specify Computation Timeout for Long Pre-Computations

When a goal involves a one-time pre-computation that ALL subsequent analysis depends on (e.g., computing all zeta zeros before iterating over n), **explicitly extend the computation timeout** beyond the default. A computation that takes 9 out of 10 available minutes is at risk — any slowdown (system load, precision increase, larger N) pushes it past the limit.

- **riemann-hypothesis strategy-003 exploration-002** — The zero pre-computation (2000 zeros via mpmath at 50-digit precision) took ~569 seconds (~9.5 minutes). With a 10-minute default timeout, this barely fit. For larger runs (10,000 zeros), this would fail. The goal correctly specified "pre-compute ALL zeros first," but should have also specified `timeout 20m` or explicitly noted the expected runtime.

**Rule:** When a pre-computation is expected to take > 5 minutes, add: "This pre-computation may take up to [X] minutes. Use `timeout [2X]m` to ensure completion." The 2× safety margin covers system variability. If the pre-computation is the exploration's bottleneck, the timeout is the highest-priority parameter to specify.

**Pre-compute shared data pattern:** When many subsequent computations all use the same expensive data (e.g., zeros, eigenvalues, simulation trajectories), instruct: "Pre-compute [data] ONCE, save to [file], then iterate." This is the sequencing variant (fast→slow) applied to shared setup — the pre-computation is the slow step that enables all fast steps. RH s003-E002: 569s zero computation + 80s for all 500 λ_n values.

## Variant: Specify Fitting Method When Comparing to Prior Explorations

When a goal requires comparing β, fit quality, or any statistic against a prior exploration's values, **specify the exact fitting method used to produce the baseline values.** Different fitting methods (Wigner interpolated histogram, Brody MLE, KS-based) give systematically different β estimates for the same data — differences of 0.1–0.2 are common.

- **riemann-hypothesis strategy-003 exploration-004** — The S002 target β=1.154 at p=809 was measured using the **Wigner interpolated** distribution P(s;β) = A s^β exp(-B s²), NOT the Brody distribution. The explorer tested 6 fitting methods against S002 targets and found only the Wigner histogram (no trim, 50 bins, s_max=4, degree-15 polynomial unfolding) reproduced S002 values to total error < 0.04. The Brody MLE gave β=1.010 (not 1.154) for the same data. Identifying the exact fitting method was essential before any cross-N comparison could be meaningful.

**Rule:** When a prior exploration reports a β or fit value, include in the goal: "Prior value β=X was measured using [method name]. Use the same method for direct comparison. If you use a different method, report both and label clearly."

**Red flag:** If your new β disagrees with a prior exploration's β by > 0.1, the FIRST hypothesis should be "different fitting method" — not "different physics." Check the method before investigating.

## Variant: Specify Which Symmetry Generator for QFT/Relativity Comparisons

When a goal involves comparing modular flow (or any abstract flow) against "physical dynamics" in a QFT or relativistic setting, **specify exactly which Poincare transformation** the flow should be compared against: Lorentz boost, time translation, spatial rotation, or conformal transformation. "Compare to full QM" is ambiguous in relativistic settings — the BW theorem says modular flow = boost, NOT time translation.

- **thermal-time strategy-002 exploration-001** — The original goal asked for C_local ~ C_full (modular flow ~ time evolution). The explorer caught and corrected the physics error: BW says modular flow = Lorentz boost, which maps (x,0) -> (x cosh tau, x sinh tau), NOT time translation (x,0) -> (x, tau). The correct comparison was modular-flow vs. boost correlator. The explorer saved the exploration by identifying this — but a correct goal would have specified "compare C_mod against the Wightman function at the boosted spacetime point" from the start.

**Rule:** For any QFT goal involving modular flow or operator algebra automorphisms, write: "Compare against [specific generator]: [explicit spacetime mapping]." Don't write "compare against standard QM dynamics" — specify the generator.

## Variant: Specify Williamson (not Peschel) for Bosonic Lattice Modular Hamiltonians

For bosonic lattice field theories, the correct modular Hamiltonian extraction method is the **Williamson decomposition** (symplectic diagonalization of the covariance matrix), NOT Peschel's formula (which applies to fermionic systems). Goals for bosonic lattice modular Hamiltonians should specify: "Use the Williamson decomposition (bosonic Peschel method): (1) compute X_ij, P_ij; (2) form D = X^{1/2} P X^{1/2}; (3) eigenvalues give symplectic eigenvalues."

- **thermal-time strategy-002 meta-exploration-001** — Noted that explorations 001 and 003 both used the Williamson decomposition successfully for the bosonic scalar field. Goals should specify this method by name to prevent explorers from using the fermionic Peschel formula, which gives wrong results for bosons.

## When to apply

Any exploration that involves implementing and running a numerical simulation. Especially important when results need to be compared against published benchmarks or across multiple explorations. Also applies when a goal compares two quantities (actual vs. theoretical, method A vs. B) — request the ratio or comparison metric explicitly. Use code templates for computation-heavy goals where the right formula is known. Use threshold-finding scan questions when a qualitative transition is expected. Specify normalization when results must be compared across explorations. Request sign+magnitude explicitly when the observable could change sign across variants. For statistics with subtle normalization (R₂, Δ₃, etc.), provide the exact implementation formula AND a known numerical value as a second anchor. When two implementations have previously disagreed, build the disambiguation ("which formula is correct and why?") into the goal explicitly. When testing scaling predictions (quantity X increases with T), specify explicit parameter bins so the T-dependence is directly testable. When a fast pre-filter (seconds) determines whether to run an expensive simulation (minutes+), specify "run fast step first" explicitly. When a goal involves a definite integral, state the integration region in plain language — not just the formula. **Also applies to pure-math/analytic explorations:** provide the explicit integral setup (substitution, split, limits) when the computation is derivable from first principles — same benefit as code templates, but for analytic derivations. **For QFT/relativity:** specify the exact symmetry generator (boost, translation, rotation) when comparing flows. **For bosonic lattice:** specify Williamson decomposition, not Peschel.
