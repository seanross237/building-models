---
topic: Explorers reason well but cannot perform novel computations
category: system-behavior
date: 2026-03-27
source: "strategy-004 meta-s4-003, strategy-004 meta-s4-004, strategy-004 meta-s4-001, classicality-budget strategy-001 meta-exploration-002, yang-mills strategy-001 meta-exploration-005, yang-mills strategy-002 meta-exploration-s002-002, yang-mills strategy-002 meta-exploration-s002-004, yang-mills strategy-002 meta-exploration-s002-006"
---

## Lesson

Explorers can evaluate formulas with given inputs and reason about whether computations would work, but they cannot perform novel calculations that nobody has published. The best prediction extraction results come when you give the explorer a FORMULA to evaluate. When a prediction requires a computation nobody has done, the explorer correctly identifies the missing step but can't fill it. This is valuable -- it precisely identifies what needs to be computed -- but don't expect the explorer to be the one to compute it.

## Evidence

- **strategy-004 exploration s4-003** — Part A (evaluate b using given critical exponents) succeeded. Part B (derive delta-3 from RG trajectory) failed because the calculation hasn't been done in the literature. Explorer correctly identified the gap.
- **strategy-004 exploration s4-004** — Explorer correctly identified that the fakeon prescription doesn't affect UV divergences through three independent arguments. This was reasoning about the structure of a calculation, not performing it.
- **strategy-004 exploration s4-001** — Explorer used published fixed-point values to derive a numerical estimate. The computation was evaluating an existing formula, not deriving a new one.

## Important exception: Standard explorers can compute too

Standard explorers (not just math explorers) can run Python scripts and perform meaningful computation, including eigenvalue decomposition, matrix operations, and numerical linear algebra. The standard vs. math explorer distinction matters for verifiability ([VERIFIED] tags) but not for computational capability.

- **yang-mills strategy-003 exploration-005** — Standard explorer computed full R(Q) eigenspectra (192×192 matrices), projected onto 9-dimensional subspaces, verified an exact linear formula (R²=1.000000), and tested 20 configurations — all as a standard explorer with Python/numpy.

## Important exception: Numerical simulation implementation

Explorers CAN implement complex numerical simulations from scratch and run them successfully. Lattice gauge theory (SU(2) Wilson action with Kennedy-Pendleton heat bath, Monte Carlo on 4⁴-8⁴ lattices) was implemented in Python/numpy/numba and produced results matching published literature within 1-2σ. The distinction is:

- **Can do:** Implement known algorithms, run simulations, extract observables from numerical data
- **Cannot do:** Derive new analytical results, perform novel theoretical calculations that nobody has published

The key enabler is specifying exact parameters (β values, lattice sizes, measurement counts) — see also: goal-design/specify-computation-parameters.md.

- **yang-mills strategy-001 exploration 003** — Full SU(2) lattice gauge theory implemented from scratch. Plaquette values, Wilson loops, Creutz ratios, Polyakov loops all reproduced. Glueball mass extraction from correlators failed (expected on small lattices).

### Practical limits for lattice simulations

4⁴-8⁴ lattices are adequate for basic observables (plaquette, Wilson loops, Creutz ratios). Glueball masses require ≥16⁴ which is borderline for pure Python even with numba optimization. Asymptotic scaling for SU(2) requires β ≥ 2.4 on ≥16⁴ lattices.

**Finite group lattice gauge theory is a fast computational domain.** The heat bath algorithm for finite groups requires no rejection sampling — for each link, compute the Boltzmann weight for all |G| group elements and sample exactly from the discrete distribution. This is O(|G|) per link but has zero waste (unlike continuous-group Metropolis/Kennedy-Pendleton). In practice, 2T (24 elements), 2O (48), and 2I (120) simulations run faster than equivalent SU(2) runs.

**Runtime expectations for complex lattice simulations:** A full β-scan across 7 coupling values with 3 finite groups + SU(2), including hysteresis analysis (hot/cold starts), takes approximately 20–30 minutes total. Plan for this when designing exploration timeouts. The coding/planning phase for a novel multi-group simulation can itself take 10–15 minutes before any code runs; if no code appears after 15 minutes, consider relaunching rather than waiting further.

- **yang-mills strategy-001 exploration 005** — 4⁴ lattice, 4 gauge groups (2T/2O/2I/SU(2)), 7 β values, hysteresis scans. First attempt failed and required relaunch. Second attempt succeeded in ~20–30 minutes total runtime.

- **yang-mills strategy-002 exploration-002** — SU(2) spectral gap scan (MCMC autocorrelation time) at 8 β values on a 4⁴ lattice with 2000 sweeps per β. Sequential KP heat bath: **~8 minutes per β value**, 64 minutes total. This is at the edge of feasibility. For larger lattices (6⁴, 8⁴) this becomes completely infeasible in one run. **Practical limits for spectral gap scans:** use ≤ 500 sweeps and ≤ 6 β values for 4⁴ lattice. Use 500 sweeps (not 2000) for exploratory scans — sufficient for autocorrelation measurement on 4⁴.

**Dimension scaling for lattice simulations:** 4D lattice (4⁴=256 sites) is approximately 3× slower than an equivalent 3D lattice (4³=64 sites) for the same algorithm and β scan. When designing sequential dimension comparisons (d=3 then d=4), budget 3× extra time for the 4D run. From yang-mills E006: 4⁴ with 500 thermalization sweeps took ~8-10 minutes per β value for 4 β values total.

**Formula optimization (pure calculus, no simulation):** Math explorers complete pure formula manipulation (optimize over parameters, scan C_eff, compute ratios) in **~2 minutes**. This is the floor for math explorer tasks — if a math explorer is taking longer than 2 minutes on pure algebra, it is likely researching or exploring, not just computing.

- **yang-mills strategy-002 exploration-004** — Computed all results from known threshold formulas in ~2 minutes. For pure formula manipulation (no simulation, no literature search), math explorers are extremely fast. The bottleneck in E004 was trying to verify a key formula from the paper (Proposition 3.23) — that part required a sub-agent to read the PDF, which took longer.

### Self-Debugging: Math Explorers Can Fix Code Bugs with Expected-Output Context

Math explorers are capable of diagnosing and fixing serious implementation bugs — IF given context about what the correct output should look like.

- **yang-mills strategy-002 exploration-002** — Initial parallel heat bath implementation gave ⟨P⟩ ≈ 0 at ALL β values including β=3.0 (obviously wrong). The explorer identified this as "parallel updates violate detailed balance" and rewrote with a correct checkerboard decomposition. This produced physically correct results. **Key enabler:** the goal specified "plaquette ≈ 0.50 at β=2.0" as an expected value, giving the explorer a ground truth to check against. Without this expected-output context, the wrong results might have been accepted.

**Implication:** Provide expected output values in the goal (e.g., "⟨P⟩ ≈ β/4 for β << 1") not just as sanity checks for the strategizer, but as debugging scaffolding for the explorer itself. The explorer uses these values to self-validate mid-run.

## Important exception: Computation reveals non-obvious insights

Beyond implementing known algorithms, computation can generate physical insights that are hard to predict theoretically. When a formula is evaluated across a wide range of scales, the pattern of where it becomes constraining vs. trivial can be the main finding.

- **classicality-budget strategy-001 exploration 002** — Computing R_delta <= S_max/S_T - 1 for 7 systems from Planck to cosmological scales revealed that the budget spans 122 orders of magnitude and is only constraining at the Planck scale. This was the key insight of the mission — it would have been hard to predict without running the numbers.

## When to apply

When designing prediction extraction or technical investigation goals. If the prediction requires a novel calculation, frame the goal as "identify what computation is needed and what it would tell us" rather than "perform the computation." Also: killing a non-prediction (showing something is suppressed from ~0.01 to ~10^-14 by RG running) is as valuable as finding a real prediction. For numerical simulations, provide exact parameters and expect correct implementations — but don't expect glueball-precision results on small lattices.
