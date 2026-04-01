# Exploration 001: Map the Escape Routes from the No-Go Theorem

## Goal
Systematically investigate all 5 "escape routes" from the no-go theorem that {d_s = 2, Lorentz invariance, diffeomorphism invariance, renormalizability} uniquely selects quadratic gravity with fakeon quantization (QG+F). For each route, determine whether the resulting theory space is EMPTY, SINGLETON, or OPEN.

## Route 1: Relax Lorentz Invariance

### Background

The no-go theorem requires Lorentz invariance to force the propagator to take a specific form constrained by the Källén-Lehmann spectral representation. Breaking Lorentz invariance allows anisotropic scaling between space and time, which opens a different route to UV finiteness: higher spatial derivatives without higher time derivatives, avoiding the Ostrogradsky ghost instability.

### Investigation

#### (a) Status of Hořava-Lifshitz Extra Scalar Mode

Hořava-Lifshitz (HL) gravity with anisotropic scaling z=3 gives d_s = 1 + d_spatial/z = 1 + 3/3 = 2 in the UV. However, reducing the diffeomorphism group from full Diff(M) to foliation-preserving diffeomorphisms Diff_F(M) introduces an extra scalar graviton mode. This mode suffers from:

1. **Strong coupling**: The scalar mode becomes strongly coupled at an extremely low energy cutoff, potentially as low as ~(M_Pl × H_0²)^{1/3} ~ 10^{-3} eV
2. **Instabilities**: Fast exponential instabilities at short distances
3. **Ghost behavior**: The scalar mode becomes a ghost when the parameter λ lies in the range 1/3 < λ < 1

**Resolution attempts:**
- **U(1) extension** (Hořava-Melby-Thompson 2010, Zhu-Wu-Wang 2011): Extending gauge symmetries to include a local U(1) symmetry eliminates the spin-0 graviton. This automatically resolves the stability, ghost, strong coupling, and speed problems. The U(1) has a geometric origin in the Bargmann extension of the local Galilean algebra acting on torsional Newton-Cartan geometries.
- **Detailed balance softly broken**: Reduces independent coupling constants from >70 down to 15, while preserving UV completeness and healthy IR limit.
- **Post-Newtonian analysis**: With U(1) extension, all solar system tests are satisfied in a large region of parameter space.

**Current status (2024-2025)**: The U(1) extension is considered the "healthy" version of HL gravity. Active research continues, with 2025 papers on quantum cosmology in the Bianchi IX framework and pseudo-complex GR within HL. However, no fundamentally new resolution has appeared since 2015. The U(1) extension appears to be the accepted fix, making the theory self-consistent but introducing additional structure.

#### (b) Theories Beyond HL That Break Lorentz Invariance and Achieve d_s = 2

The general formula d_s = 1 + D/z means any theory with anisotropic scaling z = D (where D is the number of spatial dimensions) achieves d_s = 2 in the UV. For D = 3, this requires z = 3.

Beyond HL, the theoretical landscape includes:
- **General Lifshitz-type theories**: Any field theory with z = 3 scaling in 3+1 dimensions gives d_s = 2. This is a large class, but HL is essentially the unique gravitational theory in this class (the most general z=3 gravity theory with foliation-preserving diffeomorphisms).
- **Tropological Yang-Mills theories** (2025): Recent work explores gauge theories with Lifshitz-type scaling, quantized via tropical geometry methods. This extends the anisotropic scaling idea beyond pure gravity.

However, the key constraint is that once you demand: (i) anisotropic scaling with z = 3, (ii) a gravitational theory, (iii) foliation-preserving diffeomorphisms, you are essentially forced to HL gravity (or its extensions). The theory space is narrow.

#### (c) Mechanisms for Emergent Lorentz Invariance

If Lorentz invariance is fundamentally broken at the Planck scale but must emerge at low energies, the theory must explain why LIV effects are suppressed to the extraordinary precision observed.

**Observational bounds (2024-2025):**
- GRB 221009A (the "BOAT" — brightest of all time) provides the most stringent constraints: E_QG > 5.9 E_Pl (subluminal) and 6.2 E_Pl (superluminal) for linear LIV (n=1). These bounds EXCEED the Planck energy by a factor of ~6.
- For quadratic LIV (n=2): E_QG > 5.8 × 10^{-8} E_Pl, which are the best time-of-flight constraints available.
- A 2025 study demonstrated the constancy of the speed of light with "unprecedented accuracy."

**Mechanisms for emergent Lorentz invariance:**
- HL theory has the parameter λ which must flow from its UV value to λ = 1 in the IR to recover full Lorentz invariance. However, the RG flow of λ and whether it naturally reaches 1 is not fully established.
- In condensed matter analogues, Lorentz invariance can emerge at low energies from microscopically non-relativistic systems (e.g., superfluid helium), but the tuning required is extreme.
- Recent 2025 work on Lorentz-violating pseudovectors in effective field theories notes that the correspondence between general EFT for Lorentz violation and emergent Lorentz symmetry is "mostly unexplored for higher mass dimension operators."

**The fundamental problem**: The GRB 221009A bounds already exceed E_Pl for n=1 LIV. This means ANY theory with Planck-scale linear LIV is experimentally excluded. Theories must either (i) produce only quadratic (n=2) or higher LIV, (ii) have a specific mechanism that suppresses LIV effects by factors > 6 beyond naive expectations, or (iii) achieve exact emergent Lorentz invariance. This is an extremely tight constraint.

#### (d) Verdict: OPEN but NARROW

**OPEN** — but barely. The theory space is not empty (HL with U(1) extension is viable), and it's not a pure singleton (variations exist: different matter couplings, different detailed-balance conditions, different values of coupling constants). However, the space is severely constrained:

1. The requirement z = 3 for d_s = 2 essentially selects HL gravity as the unique gravitational framework
2. The LIV bounds from GRB 221009A are super-Planckian for n=1, requiring quadratic or higher suppression
3. No mechanism for emergent Lorentz invariance has been convincingly demonstrated

**Novel territory**: The most promising sub-directions are:
- Exploring HL gravity with the U(1) extension in regimes where it makes predictions distinct from QG+F (e.g., cosmological perturbations, gravitational wave propagation)
- Theories where anisotropic scaling applies only to the gravitational sector, with matter remaining Lorentz-invariant
- Hybrid theories combining anisotropic scaling with other mechanisms (e.g., anisotropic scaling + nonlocality)

## Route 2: Relax Strict Renormalizability (Asymptotic Safety)

### Background

Instead of requiring perturbative renormalizability (which forces higher-derivative terms and thus ghosts), one can demand non-perturbative UV completeness via an interacting fixed point of the renormalization group. This is the asymptotic safety (AS) scenario. In AS, d_s = 2 follows automatically from the anomalous dimension η_N = -2 at the non-Gaussian fixed point (NGFP), regardless of the truncation used.

### Investigation

#### (a) Can AS Produce d_s = 2 via a Different Action than Stelle's Quadratic Gravity?

The key question is whether the UV fixed point of AS is the *same theory* as perturbative quadratic gravity (QG) or a genuinely different theory.

**The Sen-Wetterich-Yamada (SWY) result (2022):** Computing non-perturbative flow equations for fourth-order derivative gravity, SWY found *two* fixed points:
1. An **asymptotically free** fixed point — corresponding to perturbative higher-derivative gravity (Stelle theory)
2. An **asymptotically safe** (NGFP) fixed point — extending the Einstein-Hilbert NGFP to the full quadratic truncation

These are distinct fixed points, but the asymptotically free one is what connects to Stelle's theory. The NGFP is a genuinely non-perturbative fixed point. In the IR, both flow toward Einstein gravity plus small corrections.

**The critical relationship**: QQG (quantum quadratic gravity) has been shown to feature a UV fixed point "even in the presence of realistic matter sectors, and can therefore be regarded as a concrete realization of asymptotic safety." This suggests AS and QG are not independent theories but different descriptions of the same underlying physics, viewed from perturbative vs. non-perturbative perspectives.

However, the two fixed points found by SWY are *different* — they have different critical exponents, different numbers of relevant directions, and different physical predictions along the RG trajectories flowing from them. This leaves genuine ambiguity about which fixed point Nature selects.

#### (b) Do Different Truncations Change the UV Action?

The answer is nuanced:

- **Einstein-Hilbert truncation** (R + Λ): Finds the NGFP with η_N ≈ -2, giving d_s = 2. Two relevant directions.
- **R² truncation** (R + R² + Λ): NGFP persists. Still gives d_s = 2 (because η_N = -2 is robust).
- **f(R) truncations** (polynomial approximations of arbitrary functions of R): NGFP persists with qualitatively similar properties.
- **Weyl-squared truncation** (C_μνρσ C^{μνρσ}): Opens the connection to Stelle theory.
- **Full fourth-order truncation** (R² + C² + E + R + Λ, where E is the Euler density): SWY found two fixed points.

The critical result is that d_s = 2 is **robust across all truncations** because it depends only on η_N = -2, which is a universal property of the NGFP. The specific action at the UV fixed point does vary with truncation, but the spectral dimension prediction does not.

However, **the action that the theory flows to in the IR** — the physical predictions at accessible energies — *does* depend on which trajectory you're on and which fixed point you start from. This is where different truncations can yield different physics.

#### (c) Bimetric Structure (BMEG)

The functional renormalization group equation for quantum gravity inherently involves *two* metrics: the dynamical metric g_μν and the background metric ḡ_μν. The effective average action Γ_k[g, ḡ] depends on both, and contains three classes of interactions:
1. Pure dynamical metric terms (built from g_μν alone)
2. Pure background terms (built from ḡ_μν alone)
3. Mixed terms (involving both metrics)

Most studies use a **single-metric truncation** where Γ_k[g, ḡ] = Γ_k[g] + gauge-fixing terms, ignoring the bimetric structure. The BMEG (bimetric effective average gravity) framework goes beyond this, explicitly accounting for all three classes.

**Status (2024-2025):**
- Recent studies have initiated "the first study of the full-fledged gravitational RG flow which explicitly accounts for the bimetric structure"
- The bimetric structure is essential for background independence — a truncation that ignores it may miss physically relevant operators
- Lorentzian vs. Euclidean flows have been investigated using ADM decomposition, finding that the graviton two-point function shows consistent fixed points

**Does the bimetric structure open additional theory space?** Yes, in principle. The space of possible bimetric truncations is much larger than single-metric truncations. Different bimetric fixed points could correspond to genuinely different physical theories, even if all share d_s = 2. However, this space has barely been explored computationally.

#### (d) Relationship to the Swampland

A 2025 conceptual assessment (Bonanno et al., SciPost Physics) examined the tension between AS and Swampland conjectures. Key findings:
- AS graviton scattering amplitudes may violate certain positivity bounds assumed in the Swampland program
- If AS is realized in Nature, some Swampland conjectures (particularly regarding de Sitter vacua) may need modification
- This tension could *differentiate* AS from string theory — if de Sitter vacua are allowed in AS but forbidden by string Swampland conjectures, this is a potentially testable distinction

#### (e) Verdict: OPEN but with SINGLETON risk

**OPEN** — AS provides a framework where d_s = 2 emerges naturally from η_N = -2, but the specific theory is *not* uniquely determined because:

1. Multiple fixed points exist (at least two in the SWY analysis: asymptotically free and asymptotically safe)
2. The bimetric structure opens a largely unexplored dimension of theory space
3. Matter content affects the fixed point structure — different matter sectors can give different physical theories all sharing d_s = 2
4. The Lorentzian vs. Euclidean formulations may yield different results

**SINGLETON risk**: There is a real danger that all these variations ultimately describe the same physical theory (QQG with the fakeon prescription), just viewed from different computational perspectives. The SWY result that both fixed points exist in the same truncation, and the IR limit "entails only unobservably small modifications of Einstein gravity," suggests convergence. But this is not proven.

**Most promising sub-directions for novel theory construction:**
- AS with specific matter content that produces predictions distinct from QG+F
- Lorentzian AS (formulated directly in Lorentzian signature, avoiding Wick rotation issues)
- Bimetric AS with genuinely new operators that have no single-metric counterpart
- AS theories that lie in a different universality class than QQG (if they exist)

## Route 3: Relax d_s = 2 Exactly

### Background

The no-go theorem takes d_s = 2 as an exact UV value. But numerical quantum gravity programs (CDT, spin foams, causal sets) give d_s values that are only *approximately* 2, with significant spread: CDT gives ~1.80 ± 0.25, LQG spin foams give 2 for some states and 1 for others, causal sets give d_mm ≈ 2.38 for generic orders. What if d_s = 2 is not exact?

### Investigation

#### (a) Is the "Universality" of d_s → 2 an Artifact?

**Multiple definitions of spectral dimension exist**, and they don't all agree:

1. **Random walk spectral dimension**: Defined from the return probability P(σ) of a random walk after diffusion time σ. This is the standard definition: d_s = -2 d(log P)/d(log σ).
2. **Causal spectral dimension**: Based on the meeting probability of *two* random walkers. Cases exist where this differs from the standard d_s.
3. **Hausdorff dimension**: Based on volume scaling V(r) ~ r^{d_H}. In quantum gravity, d_H ≠ d_s generically.
4. **Walk dimension d_w**: Related by d_s = 2 d_H / d_w. Different from both d_H and d_s.

**The universality question**: The "convergence" of multiple approaches to d_s ≈ 2 was once argued as evidence for universality. However:
- CDT gives d_s ≈ 1.80 ± 0.25 (or ~3/2 in some newer measurements), not exactly 2
- Different state-sum models in LQG give d_s = 2 or d_s = 1, depending on the coherent state used
- Causal sets give d_mm ≈ 2.38 for mid-order dimensions, not 2
- Liouville quantum gravity in 2D gives d_s = 2 exactly, but this is in 2D where d_s = d_H = 2 is somewhat trivial

**Verdict on universality**: The "universality" is approximate at best. The value d_s ≈ 2 is a rough attractor for many approaches, but exact values range from ~1.5 to ~2.5 depending on the approach, the definition used, and the computational details. This is likely NOT an artifact — the spread is real and physically meaningful, reflecting genuinely different UV structures.

#### (b) Theories Producing d_s ∈ [1.5, 2.5] That Are Not Already Known Programs

This is a critical question. The known programs that give d_s in this range are:
- **CDT** (d_s ≈ 1.5-2.0): well-established lattice quantum gravity program
- **HL gravity** (d_s = 2 exactly): z = 3 anisotropic scaling
- **AS** (d_s = 2 exactly): from η_N = -2
- **QG+F** (d_s = 2 exactly): quadratic gravity with fakeons
- **LQG/Spin foams** (d_s = 1-2.5): highly model/state dependent
- **Causal sets** (d_s ≈ 2.38): via myriad dimension

What about *genuinely unknown* theories? The space is open for theories that:
- Produce d_s in the range but via a *novel mechanism* (not anisotropic scaling, not anomalous dimensions, not lattice discretization)
- Use *fractional derivatives* or *multi-fractional spacetimes* — these can tune d_s to any desired value. The multi-fractional theories of Calcagni (2011-present) provide a framework where d_s is an adjustable parameter, but these are somewhat ad hoc.
- Arise from *tensor models* or *random geometry* approaches distinct from CDT

#### (c) Physical Predictions If d_s = 2 + ε

If d_s is not exactly 2, physical predictions change quantitatively but not qualitatively:

- **Graviton propagator UV behavior**: G(p²) ~ 1/(p²)^{d_s/2} in the UV. For d_s = 2, G ~ 1/p², which is the critical boundary for renormalizability. For d_s = 2 + ε with ε > 0, the propagator falls faster, *improving* UV behavior. For ε < 0, it falls slower, *worsening* it.
- **Renormalizability**: d_s = 2 is the critical value for power-counting renormalizability of gravitational amplitudes. d_s < 2 is super-renormalizable (better than needed), d_s > 2 is non-renormalizable (but might still be AS).
- **Heat kernel coefficients**: The short-distance structure of the heat kernel traces changes, affecting one-loop divergences and the effective action.
- **Cosmological observables**: Modifications to the primordial power spectrum, tensor-to-scalar ratio, and spectral indices depend on the exact UV spectral dimension.

#### (d) Is the Landscape Richer If We Relax to d_s ∈ [1.5, 2.5]?

**Yes, significantly.** The no-go theorem's power comes from demanding d_s = 2 *exactly*, which combines with Lorentz invariance to select a unique propagator form. Relaxing to d_s ∈ [1.5, 2.5]:

1. **Removes the uniqueness**: The propagator is no longer fixed to a single form. Multiple propagator structures can give d_s in this range.
2. **Allows CDT and LQG to be "on target"**: These approaches, currently excluded by the d_s = 2 exactness requirement, become legitimate candidates.
3. **Opens multi-parameter families**: Instead of a single theory, we get continuous families parameterized by d_s (or equivalently, by the UV anomalous dimension or anisotropy exponent).

However, this richness comes at a cost: **losing the constructive power** of d_s = 2 as a sharp axiom. The no-go theorem was powerful precisely because d_s = 2 is a sharp constraint. Relaxing it makes the landscape too large to be useful without additional principles.

#### (e) Verdict: OPEN and VAST but UNDERCONSTRAINED

**OPEN** — and indeed much more open than Route 1 or Route 2, precisely because relaxing d_s = 2 removes the strongest constraint. The theory space is vast:

- Continuous families parameterized by d_s
- Multiple mechanisms (anisotropic scaling, anomalous dimensions, discretization, fractal structures)
- All existing quantum gravity programs become candidates

**But**: This route is **underconstrained**. Without d_s = 2 as a sharp axiom, we need *replacement* constraints to narrow the landscape. Simply saying "d_s is approximately 2" is not enough to select a theory.

**Most promising sub-direction**: Use d_s as a *derived prediction* rather than an input axiom. Start from other principles (thermodynamic, holographic, information-theoretic) and see what d_s they predict. If a novel theory from Route 5 predicts d_s = 1.8 or 2.3, that's interesting and testable.

## Route 4: Relax Locality

### Background

The no-go theorem proves that for any Lorentz-invariant theory with propagator G(p²) = f(p²)/p² where f is an unbounded entire function with no zeros, d_s → 0 in the UV. This kills infinite derivative gravity (IDG) as a route to d_s = 2. The question is whether there are forms of nonlocality that escape this no-go.

### Investigation

#### (a) Partially Nonlocal Theories

The no-go applies specifically to propagators of the form f(p²)/p² with f an unbounded entire function. What about *partial* nonlocality — nonlocal in some sectors but local in others?

**Sector-dependent nonlocality**: Consider a theory where:
- The graviton propagator is modified by a nonlocal form factor: G(p²) = e^{-p²/M²} / p²
- But the ghost sector retains local dynamics with the fakeon prescription

This hybrid approach is essentially what QG+F already does: the quadratic terms R² and C² introduce higher poles that are handled by the fakeon prescription (making them neither particles nor ghosts but "fake" degrees of freedom). This is a form of "controlled nonlocality" — the theory is local at the level of the action but nonlocal at the level of the S-matrix (where fakeons don't propagate as asymptotic states).

**The loophole**: The no-go theorem assumes the *full* propagator takes the form f(p²)/p². If the graviton propagator has a more complex structure — e.g., a sum of terms with different analytic properties — the theorem's assumptions may not apply.

#### (b) Scale-Dependent Locality

A theory that is local below some scale M and nonlocal above it would effectively have:
- Standard GR behavior at E << M
- Modified UV behavior at E >> M
- A transition region around E ~ M

The Deser-Woodard nonlocal gravity models provide a cosmological implementation of this idea, with nonlocal terms that activate at cosmological scales. However, these are IR modifications, not UV completions.

For UV completions, scale-dependent locality would require:
- A form factor f(□) that transitions from f ≈ 1 (local) at low energies to some modified form at high energies
- The transition must be smooth enough to avoid introducing new poles (ghosts)

**Critical constraint**: Any smooth transition function that grows in the UV will either (i) be an entire function (giving d_s → 0 by the no-go) or (ii) introduce poles (giving ghosts). There is no obvious escape from this dichotomy within Lorentz-invariant theories.

#### (c) Bounded Nonlocality — Meromorphic and Lee-Wick Propagators

This is the most interesting sub-route. The no-go theorem specifically excludes *entire* functions (which have no poles). What about *meromorphic* functions (which have poles)?

**Lee-Wick gravity**: The propagator takes the form
G(p²) = 1/p² - 1/(p² + M₁²) + 1/(p² + M₂²) - ...
with alternating signs and complex conjugate mass poles. This is meromorphic, not entire.

Key properties:
- **Ghost-free in a generalized sense**: Complex conjugate poles don't contribute to the absorptive part of scattering amplitudes. The Lee-Wick-CLOP prescription removes these from the asymptotic state space.
- **Super-renormalizable**: In even dimensions, only finitely many diagrams diverge. In odd dimensions, the theory is finite.
- **UV behavior**: The propagator can fall as 1/p^{2n} for large p² (depending on the number of Lee-Wick partners), giving d_s = 2n.

**Can Lee-Wick gravity give d_s = 2?** With a single pair of complex conjugate poles:
G(p²) = 1/(p² (p² + M²))
This falls as 1/p⁴ in the UV, giving d_s = 4 (not 2). To get d_s = 2, you need the propagator to fall as 1/p² in the UV, which means... no modification at all. Lee-Wick theories generically give d_s > 2 (improved UV behavior).

However, this is actually *better* than d_s = 2 for renormalizability purposes. And the no-go theorem doesn't apply because:
1. The propagator is meromorphic, not entire
2. The extra poles are complex, not on the real axis
3. The Källén-Lehmann representation doesn't apply in its standard form (it requires positive spectral density, which Lee-Wick theories violate)

**The real question**: Is Lee-Wick gravity a *genuinely different* theory from QG+F, or just QG+F with a different prescription for handling ghosts?

The answer is: **they are related but distinct**. The fakeon prescription (Anselmi) and the Lee-Wick prescription (CLOP) handle the ghost poles differently:
- Fakeons: Ghosts are removed from both the state space AND internal lines (via a modified Feynman iε prescription)
- Lee-Wick: Complex conjugate poles are removed from asymptotic states but can appear in internal lines (they're "unstable" and decay before reaching the detector)

These give different S-matrix elements at loop level, making them genuinely different physical theories.

#### (d) No-Go Loophole: Theories with Non-Standard Propagator Structure

Beyond Lee-Wick, other loopholes in the no-go theorem include:

1. **Propagators that are not functions of p² alone**: If the theory breaks the assumption that G depends only on p² (e.g., G depends on p_μ separately, not just p² = p_μ p^μ), the no-go doesn't apply. But this typically requires breaking Lorentz invariance (Route 1).

2. **Multi-field theories**: If gravity involves multiple interacting fields whose combined propagator matrix has the right structure, the single-field no-go doesn't directly apply. The eigenvalues of the propagator matrix could have different analytic properties.

3. **Non-perturbative effects**: The no-go is a statement about the perturbative propagator. Non-perturbative effects (condensates, topological configurations) could modify the effective UV behavior in ways not captured by the perturbative propagator.

#### (e) Verdict: OPEN via Lee-Wick / Meromorphic Loophole

**OPEN** — but via a specific loophole: meromorphic propagators (Lee-Wick theories) escape the no-go theorem because they have complex poles rather than being entire functions. The resulting theory space includes:

1. **Lee-Wick gravity with N pairs of complex poles**: A discrete family of theories parameterized by N and the complex masses. For each N, the UV spectral dimension is d_s = 2(N+1).
2. **Super-renormalizable Lee-Wick gravity**: Modena and collaborators (2016) showed this is super-renormalizable or finite, with unitarity maintained via the CLOP prescription.
3. **Distinct from QG+F**: Lee-Wick and fakeon prescriptions give different loop-level predictions.

**Most promising sub-direction**: Lee-Wick quantum gravity is a genuinely distinct approach from QG+F that:
- Is ghost-free (in the Lee-Wick sense)
- Is super-renormalizable (better than merely renormalizable)
- Gives d_s > 2 (which is *better* than d_s = 2 for UV finiteness)
- Has a discrete family of theories (parameterized by the number and masses of Lee-Wick partners)
- Is not heavily studied in the quantum gravity context (most Lee-Wick work is in the Standard Model context)

**Caveat**: The unitarity of Lee-Wick theories at higher loops is debated. A 2023 paper (PTEP) found unitarity violations for complex ghosts at higher orders, while other works defend unitarity. The 2024 "anti-instability" paper argues complex ghosts are stable, which helps but doesn't fully resolve the unitarity question.

## Route 5: Replace Spectral Dimension with Alternative Constructive Axioms

### Background

Instead of starting from d_s = 2 as the fundamental UV constraint, we can ask: what if we start from a different physical principle and see what theory it selects? This route is about finding *alternative constructive axioms* that are sharp enough to narrow the landscape but different enough to lead to genuinely novel theories.

### Investigation

#### (a) The Cosmological Constant Λ ≈ 10^{-122} M_P⁴ as a Constructive Constraint

**What theory does this select?**

The cosmological constant problem is the most dramatic fine-tuning problem in physics: the observed Λ is ~122 orders of magnitude smaller than the "natural" QFT prediction. Any theory that *explains* this value (rather than simply inputting it) would be enormously powerful.

**Existing approaches:**
- **Causal set theory's "everpresent Λ"** (Sorkin 1987): Predicts Λ fluctuates with amplitude ~ 1/√N where N is the number of causal set elements in the past. For the current epoch, this gives Λ ~ H₀² ~ 10^{-122} M_P⁴, matching observations. Recent work (2023-2024) shows the model can fit current cosmological data as well as ΛCDM and even alleviates tensions (H₀ tension, BAO Lyman-α tension). However, the model requires fine-tuning of the fluctuation amplitude in certain implementations.

- **Unimodular gravity** (2024, Salvio): Unimodular gravity makes Λ a constant of integration rather than a coupling constant, addressing the "old" CC problem (why vacuum energy doesn't gravitate). Salvio's 2024 work on unimodular *quadratic* gravity shows this approach can be combined with QQG, but it does not solve the "new" CC problem (why Λ has the observed value) — the author resorts to anthropic/multiverse arguments.

- **Bianconi's "Gravity from Entropy"** (Phys. Rev. D, 2025): Derives gravity from quantum relative entropy between the spacetime metric and the matter-induced metric. Predicts emergence of a small positive Λ from the G-field. However, the quantitative prediction of Λ depends on parameters of the G-field, so it's not a clean prediction.

**Assessment**: Using Λ as a constructive constraint does not select a unique theory. Multiple frameworks can accommodate the observed value, but most either (i) predict it from a tunable parameter (not a genuine prediction) or (ii) appeal to anthropics. The causal set approach is the most genuinely predictive, but it's tied to a specific framework (CST) rather than being a general principle.

**Verdict for this sub-route**: OPEN but weakly constrained. Multiple theories can accommodate Λ; none is uniquely selected.

#### (b) Jacobson's Thermodynamic Derivation → UV Completion?

**The key idea**: Jacobson (1995) showed that demanding δQ = TdS for every local Rindler horizon, with S proportional to horizon area and T the Unruh temperature, *implies* the Einstein equations. This is not a derivation of GR from more fundamental physics — it's the reverse: GR is the equation of state of spacetime thermodynamics.

**Can this be extended to select a UV completion?**

Jacobson's 2015 update ("Entanglement Equilibrium and the Einstein Equation") replaced the Bekenstein-Hawking entropy with entanglement entropy across small causal diamonds. This yields Einstein's equations from the *maximal vacuum entanglement hypothesis* — the statement that the vacuum of any QFT on a smooth spacetime has maximal entanglement at the UV cutoff scale.

**UV implications:**
- If the vacuum entanglement structure *changes* at the Planck scale (as expected in any UV completion), the modified entanglement entropy would generate *modified* gravitational equations
- The specific UV modification selects specific departures from Einstein gravity
- This provides a *map* from UV entanglement structures to gravitational theories

**Recent developments (2024-2026):**
- A February 2026 paper extends Jacobson's approach to non-Riemannian geometries (torsion, non-metricity), showing the thermodynamic derivation naturally selects Einstein-Cartan theory over Palatini or metric-affine alternatives
- A November 2025 paper introduces gravity as "a thermodynamic phenomenon from a scalar field that sets the local rate of quantum evolution"
- The quantum entanglement dynamics of spacetime (2025, PMC) develops the entanglement-gravity correspondence further

**Does this select a unique UV completion?** No — but it does provide a *framework* for mapping between UV entanglement structures and gravitational theories. The key insight is that different UV completions correspond to different vacuum entanglement patterns, and Jacobson's approach lets you read off the gravitational equations from the entanglement structure. This is a tool for theory construction, not a theory itself.

**Verdict for this sub-route**: OPEN. Jacobson's framework provides a powerful constructive principle (thermodynamic/entanglement derivation of gravitational equations) that can be extended to the UV. The resulting theory space is parameterized by the UV entanglement structure, which is a genuinely new axis of theory construction not explored by the no-go theorem.

#### (c) Holographic Entropy Bound S ≤ A/4G

**What UV physics does this select?**

The Bousso covariant entropy bound (generalized second law) constrains the entropy of matter passing through any light-sheet to be less than A/4G, where A is the area of the bounding surface. This is an extremely powerful constraint on the density of states in any theory of quantum gravity.

**UV implications:**
- The bound implies the number of degrees of freedom in a region scales as the area, not the volume — this is fundamentally non-local and constrains any UV completion
- Any theory whose high-energy density of states grows too fast (faster than area-law) violates the bound
- The Bekenstein bound combined with the Planck cutoff gives ~ 10^{69} bits per square meter — this constrains the UV physics
- A 2024 paper derives a new covariant entropy bound from Cauchy slice holography, strengthening the constraints

**Does this select specific UV physics?**

Partially. The holographic bound excludes:
- Theories with too many UV degrees of freedom (e.g., theories with many light species beyond a certain threshold)
- Theories where the UV density of states grows volumetrically without bound

It is compatible with:
- String theory (which satisfies the bound via the Hagedorn temperature)
- QG+F (where the UV theory has a finite number of propagating modes)
- AS (where the UV fixed point has a finite number of relevant couplings)
- Lee-Wick gravity (finite number of complex poles)

The bound is necessary but not sufficient to select a unique theory.

**Verdict for this sub-route**: OPEN but weakly selective. The holographic bound excludes some theories but does not narrow the landscape enough to be a useful constructive axiom on its own.

#### (d) The 2025 Unified Holographic Swampland Condition

**The Holographic Emergence Bound** (Upadhyay et al., arXiv:2512.14389):

|∇V|²/V² + q²/(g²M_P²) + 1/(R_moduli L²) ≥ c_d

This single inequality encapsulates:
- The de Sitter gradient conjecture (first term)
- The Weak Gravity Conjecture (second term)
- The Distance Conjecture (third term)

**Derived from three foundational requirements:**
1. Positivity of relative entropy in the boundary CFT
2. Unitary modular flow
3. Monotonic evolution of holographic entanglement entropy under RG flow

**Can this be used as a starting axiom?**

The beauty of this bound is that it's *derived from information-theoretic principles* rather than string-specific constructions. The authors argue that "the Swampland program and holography are not independent frameworks but complementary manifestations of the same physical principle: the finiteness and consistency of quantum information in gravitational systems."

**However**, this bound is a *constraint* (inequality), not an *equation*. It tells you what theories are *excluded* (the "swampland") but doesn't uniquely select what's *included* (the "landscape"). It's a necessary condition, not a sufficient one.

**Assessment for theory construction**: The three foundational requirements (positivity of relative entropy, unitary modular flow, entanglement entropy monotonicity) could serve as constructive axioms for a new quantum gravity theory. Instead of starting from d_s = 2, one could start from:
- **Axiom 1**: S(ρ||σ) ≥ 0 for all states ρ, σ (positivity of relative entropy)
- **Axiom 2**: Modular flow is unitary
- **Axiom 3**: Generalized entropy obeys the quantum focusing condition

These axioms are sharp, physically motivated, and information-theoretically grounded. They constrain the theory space but don't uniquely select a theory — the resulting landscape is the "consistent" part of the Swampland landscape.

**Verdict for this sub-route**: OPEN and PROMISING. The information-theoretic axioms are genuinely different from d_s = 2 and could serve as constructive principles for novel theory building. The resulting landscape is the "holographic landscape" — theories consistent with all three axioms.

#### (e) Novel Entropic/Information-Theoretic Constructive Axioms

Beyond the specific proposals above, several novel constructive principles have emerged in 2024-2025:

1. **Bianconi's entropic action** (2025): The action for gravity IS the quantum relative entropy S(ρ_metric || ρ_matter). This is a genuinely novel constructive principle — instead of postulating an action, you derive it from the informational relationship between geometry and matter. Predictions include emergent Λ and a G-field candidate for dark matter.

2. **Gravity as a thermodynamic deformation** (2025): GR as a degenerate Otto cycle, with LIV and energy-momentum non-conservation arising from "work-producing legs." This predicts late-time cosmological acceleration.

3. **Quantum focusing condition** as a fundamental axiom: The QFC (Bousso et al.) states that the quantum expansion θ_q = θ + 4G_N S''_ent is non-increasing along null congruences. This can be taken as more fundamental than the Einstein equations.

### Overall Verdict for Route 5: OPEN and MOST PROMISING

**OPEN** — and this is the most promising route for genuinely novel theory construction. Unlike Routes 1-4 (which modify specific assumptions within the existing framework), Route 5 changes the entire starting point.

**Key finding**: The most promising alternative constructive axioms are *information-theoretic*:
- Positivity of relative entropy
- Maximal vacuum entanglement hypothesis
- Quantum focusing condition
- Entropic action principle (gravity as relative entropy)

These axioms:
1. Are physically well-motivated and mathematically sharp
2. Do not presuppose d_s = 2 (but may predict it or something close)
3. Connect to the holographic principle and Swampland constraints
4. Have not been systematically explored as constructive axioms for UV-complete theories
5. Could lead to genuinely novel theories not equivalent to QG+F, AS, HL, or any existing program

## Ranked Summary

### Verdicts

| Route | Verdict | Theory Space Size | Novelty Potential | Key Risk |
|-------|---------|-------------------|-------------------|----------|
| **Route 5**: Alternative Axioms | **OPEN** | Large | **Highest** | Underdetermined without additional constraints |
| **Route 4**: Relax Locality | **OPEN** | Moderate | **High** | Lee-Wick unitarity at higher loops debated |
| **Route 2**: Relax Renormalizability (AS) | **OPEN** | Moderate | **Medium** | SINGLETON risk — may reduce to QG+F |
| **Route 3**: Relax d_s = 2 | **OPEN** | Vast | **Low-Medium** | Too underconstrained without replacement axiom |
| **Route 1**: Relax Lorentz Invariance | **OPEN (narrow)** | Small | **Low** | Super-Planckian LIV bounds; HL essentially unique |

### Ranking from Most to Least Promising

**1. Route 5: Alternative Constructive Axioms (MOST PROMISING)**

This is the only route that changes the *starting point* rather than modifying an assumption within the existing framework. Information-theoretic axioms (positivity of relative entropy, maximal vacuum entanglement, quantum focusing condition, entropic action) provide genuinely novel foundations that have not been systematically explored. The resulting theories would be *constructed differently* from all existing programs, maximizing the chance of genuine novelty.

**Recommended next step**: Pick the sharpest information-theoretic axiom (likely the maximal vacuum entanglement hypothesis or the entropic action principle) and attempt to construct a UV-complete gravitational theory from it. Ask: what UV structure does the axiom *require*?

**2. Route 4: Relax Locality via Lee-Wick / Meromorphic Propagators (HIGH POTENTIAL)**

Lee-Wick quantum gravity is a genuinely distinct approach that escapes the no-go theorem via meromorphic propagators with complex conjugate poles. It is super-renormalizable (better than QG+F which is merely renormalizable), ghost-free in the Lee-Wick sense, and produces d_s > 2 (which is even better than d_s = 2 for UV behavior). The key uncertainty is higher-loop unitarity, which is actively debated.

**Recommended next step**: Analyze Lee-Wick quantum gravity systematically — determine whether it can be made fully consistent at all loop orders, and compute its physical predictions (scattering amplitudes, cosmological observables, black hole physics). Compare with QG+F predictions to identify testable differences.

**3. Route 2: Asymptotic Safety (MEDIUM, with SINGLETON risk)**

AS provides a natural mechanism for d_s = 2 and has a genuinely non-perturbative fixed point distinct from Stelle's asymptotically free fixed point. The bimetric structure opens unexplored theory space. However, there is significant risk that AS and QG+F are the same theory viewed from different perspectives. The relationship to Swampland constraints could differentiate AS from string-based approaches.

**Recommended next step**: Focus on identifying *observable predictions* that distinguish AS from QG+F. The bimetric structure and Lorentzian formulation are the most likely sources of such differences.

**4. Route 3: Relax d_s = 2 (OPEN but UNDERCONSTRAINED)**

Relaxing d_s = 2 opens a vast landscape but loses the constructive power of the sharp axiom. This route is best used in *combination* with Route 5: use alternative axioms to construct a theory, then *predict* d_s as an output rather than using it as an input. If the predicted d_s falls in the range [1.5, 2.5] but is not exactly 2, this would be a genuinely novel testable prediction.

**Recommended next step**: Do not pursue this route independently. Instead, combine with Route 5 by constructing theories from alternative axioms and computing their predicted d_s.

**5. Route 1: Relax Lorentz Invariance (NARROW)**

The theory space is essentially HL gravity (with U(1) extension), which is an existing research program. Super-Planckian LIV bounds from GRB 221009A make any theory with Planck-scale linear LIV experimentally dead. No convincing mechanism for emergent Lorentz invariance has been demonstrated. This is the least promising route for novel theory construction.

**Recommended next step**: Only revisit if a mechanism for emergent Lorentz invariance with super-Planckian suppression is discovered.

### Cross-Cutting Insights

1. **The most novel theories will likely combine multiple routes.** For example: Route 5 (information-theoretic axioms) + Route 4 (meromorphic propagator structure) could yield a theory built from entropic principles that naturally produces Lee-Wick-type propagators. This combination has not been explored by anyone.

2. **d_s should be a prediction, not an axiom.** The most powerful approach is to start from alternative axioms (Route 5) and see what d_s the resulting theory predicts. If the prediction is d_s = 2, the theory connects to QG+F. If it predicts d_s ≠ 2, it's genuinely novel.

3. **The fakeon prescription is the key benchmark.** Every new theory must be compared to QG+F, which is the "default" outcome of the no-go theorem. The novelty of any new theory is measured by how much its predictions differ from QG+F.

4. **Information-theoretic foundations are the frontier.** The 2024-2025 literature shows a clear trend toward information-theoretic foundations for quantum gravity (entropic gravity, holographic entanglement, quantum focusing). This is where the field is moving, and this is where genuinely new theories are most likely to be found.

### Specific Novel Theory Candidates Identified

1. **Entropic-action quantum gravity** (Bianconi 2025): Gravity from quantum relative entropy. Novel, published, makes predictions (emergent Λ, G-field dark matter). Status: very new, not yet widely scrutinized.

2. **Lee-Wick quantum gravity** (Modena et al. 2016): Super-renormalizable, ghost-free via CLOP prescription, distinct from QG+F. Status: established formalism, but not systematically studied as a complete quantum gravity program.

3. **Information-theoretic QG from the Holographic Emergence Bound** (2025): Starting from positivity of relative entropy + unitary modular flow + QFC. Status: the *bound* exists, but no one has tried to *construct* a UV-complete theory using these as axioms.

4. **Thermodynamic UV completion from Jacobson's framework**: Extend the maximal vacuum entanglement hypothesis to the UV by specifying a particular entanglement structure at the Planck scale. Status: the *framework* exists (Jacobson 2015), but the UV extension has not been systematically explored.
