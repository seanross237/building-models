# Exploration 002: Computational Spacetime — Circuit Complexity as the Foundation of Geometry

## Goal
Survey the complexity-geometry program (2014–2026) and attempt to develop a constructive framework where spacetime geometry IS quantum circuit complexity. Assess whether this direction offers genuinely new physics or merely repackages holographic entanglement results.

---

## 1. Survey of the Complexity-Geometry Program

### 1.1 Complexity = Volume (CV) Conjecture

**Origin:** Susskind (2014) and Stanford & Susskind (2014) proposed that the quantum computational complexity of the boundary CFT state is proportional to the volume of the maximal codimension-one spacelike slice anchored to the boundary time slice:

**C(|ψ⟩) ∝ V(Σ_max) / (G_N ℓ)**

where Σ_max is the maximal volume slice, G_N is Newton's constant, and ℓ is an additional length scale (typically the AdS radius).

**Key motivation:** After a black hole thermalizes, its entanglement entropy saturates (reaching S = A/4G), but the interior volume continues to grow linearly in time for an exponentially long period. This growing volume must be dual to *something* on the boundary — Susskind identified it as computational complexity, which also grows linearly for exponentially long times before saturating.

**Crucial insight — entanglement vs. complexity:**
- **Ryu-Takayanagi** (entanglement entropy): S = Area(minimal surface)/4G — probes the *boundary* and *near-horizon* geometry
- **Complexity = Volume**: C ∝ Volume(maximal slice) — probes the *interior*, including behind-the-horizon physics

This is the key observation: entanglement describes the boundary/surface of spacetime, but complexity describes the interior/bulk. Entanglement entropy saturates quickly (at thermalization time ~ β ln S), but complexity continues growing for time ~ e^S.

**Limitations:** The CV conjecture has an ambiguity in the length scale ℓ (why the AdS radius and not some other scale?), and the proportionality constant is not uniquely determined.

### 1.2 Complexity = Action (CA) Conjecture

**Authors:** Brown, Roberts, Susskind, Swingle, and Zhao (2015-2016), arXiv:1509.07876.

**Proposal:** The complexity of the boundary state is proportional to the gravitational action evaluated on the Wheeler-DeWitt (WDW) patch:

**C(|ψ⟩) = I_WDW / (π ℏ)**

where I_WDW is the gravitational action computed on the WDW patch — the domain of dependence of any Cauchy slice anchored to the boundary time.

**Key advantage over CV:** The CA conjecture removes the ambiguity of the additional length scale ℓ — the proportionality constant (1/πℏ) is universal across all black holes (neutral, charged, rotating). This gives it a degree of universality not present in CV.

**Results:** The conjecture was tested for neutral, charged, and rotating black holes in AdS, as well as perturbed systems with shells and shock waves. For uncharged black holes, the late-time complexity growth rate saturates Lloyd's bound: dC/dt = 2M/πℏ.

**Physical implication:** If complexity = action, then the dynamics of spacetime itself (as captured by the gravitational action) IS the growth of quantum computational complexity. This is already a step toward "spacetime IS computation."

### 1.3 Nielsen's Geometric Approach to Circuit Complexity

**Origin:** Nielsen, Dowling, Gu, Doherty (2006), quant-ph/0701004.

**Core idea:** Finding the optimal quantum circuit (minimum gate count) to implement a unitary transformation U is equivalent to finding the shortest geodesic on the unitary group manifold SU(2^n), equipped with a right-invariant Riemannian metric determined by a "cost function" (penalty factor) that assigns different costs to different generators.

**The complexity metric:** The distance on this manifold is:
d(I, U) = min_γ ∫₀¹ F(γ(t), γ̇(t)) dt

where F is a cost function on the tangent space of SU(2^n). The complexity of U is this minimum distance. Different cost functions (penalty factors for non-local vs. local gates) give different complexity metrics.

**Application to QFT (Jefferson & Myers, 2017, arXiv:1707.08570):**
Extended Nielsen's framework to quantum field theory. For Gaussian states in free scalar field theory, the complexity becomes the length of the shortest geodesic in the space of circuits. This established a concrete computational framework for studying complexity in QFT, motivated by holographic complexity.

**Key property:** The geometry on the space of unitaries (the "complexity geometry") is highly curved and has negative sectional curvatures in important directions. This means nearby geodesics diverge — small perturbations to a circuit lead to exponentially different outcomes. This has been connected to quantum chaos and the scrambling properties of black holes.

**For our purposes:** The complexity geometry is a genuine Riemannian geometry. If spacetime geometry IS complexity geometry, then the Riemannian metric on the space of quantum states IS the spacetime metric. This is the core of the constructive framework we want to develop.

### 1.4 Tensor Network Models of Spacetime

**MERA (Multiscale Entanglement Renormalization Ansatz):** Proposed by Vidal (2007), later connected to holography by Swingle (2012). MERA has a natural hyperbolic geometry matching the AdS spatial structure. The tensor network acts as a coarse-graining circuit — each layer removes entanglement at a given scale, producing a layered structure that looks like a discretized AdS spatial slice.

**HaPPY code (2015):** Pastawski, Yoshida, Harlow, Preskill (arXiv:1503.06237). Built from perfect tensors on a hyperbolic lattice. Explicitly realizes:
- Ryu-Takayanagi entropy formula
- Bulk-to-boundary mapping as a quantum error-correcting code
- Subregion duality (a bulk region is reconstructible from multiple boundary subregions)

**Random tensor networks (2016):** Hayden, Nezami, Qi, Thomas, Walter, Yang (arXiv:1601.01694). When bond dimension is large, random tensor networks automatically satisfy the Ryu-Takayanagi formula. Connects to average over random quantum circuits, deepening the link between circuit structure and spacetime geometry.

**Space-time tensor networks (2018):** Extended from spatial to spacetime tensor networks, reproducing the covariant Hubeny-Rangamani-Takayanagi formula and supporting local bulk reconstruction.

**Limitation for our purposes:** Tensor networks beautifully reproduce entanglement structure (RT formula) but have more difficulty capturing the complexity aspects (interior volume growth). The MERA structure matches the spatial geometry of AdS but doesn't easily capture the time-dependent interior growth that complexity describes.

### 1.5 Quantum Error Correction and Holography (ADH)

**Authors:** Almheiri, Dong, Harlow (2014), arXiv:1411.7041.

**Key insight:** The bulk-to-boundary map in AdS/CFT is a quantum error-correcting code. Bulk operators in a region can be reconstructed from *any* boundary subregion whose entanglement wedge contains that bulk region. This is exactly the structure of a quantum error-correcting code — information about logical (bulk) qubits is redundantly encoded in physical (boundary) qubits.

**Implications:**
- Radial direction in AdS ↔ level of encoding/redundancy in the QEC code
- Entanglement wedge reconstruction ↔ error correction against erasure of boundary qubits
- The "code subspace" interpretation: the holographic code can correct errors (loss of boundary subregions) up to a threshold determined by the RT surface

**Connection to complexity:** ADH focused on the QEC structure of entanglement, but the *complexity* of the encoding circuit itself encodes the radial depth. States deeper in the bulk require more complex circuits to prepare, connecting circuit complexity to the radial/geometric direction.

### 1.6 Lloyd's Bound and Complexity Growth

**Lloyd's bound (2000):** The maximum rate of computation for a system of energy E is bounded by:

**dC/dt ≤ 2E / (π ℏ)**

This is derived from the Margolus-Levitin theorem, which bounds the speed of quantum state evolution.

**Application to black holes:** For the CA conjecture, the late-time complexity growth rate for a Schwarzschild-AdS black hole saturates Lloyd's bound:

dC/dt = 2M / (π ℏ)

This means **black holes are the fastest computers in nature** — they saturate the fundamental bound on computational speed. The rate of complexity growth equals the maximum allowed by quantum mechanics for a system of that energy.

**Violations and refinements:** Subsequent work found instances where the CA proposal appears to violate Lloyd's bound (for charged, rotating, and warped black holes). This led to debates about whether the bound is fundamental or approximate, and motivated the "complexity = anything" program which explored multiple possible geometric duals.

**For our purposes:** If time IS complexity growth, then Lloyd's bound becomes a statement about the maximum rate of time flow, directly connecting energy, computation, and temporal evolution.

### 1.7 De Sitter Complexity and the Complexity Plateau

**The problem:** Our universe has a positive cosmological constant and is asymptotically de Sitter, not anti-de Sitter. Extending holographic complexity to de Sitter space has been a major challenge.

**Hyperfast growth problem:** Naive application of complexity proposals to the de Sitter static patch predicts a diverging complexification rate — a "hyperfast growth" that seems unphysical for a system with a finite-dimensional Hilbert space (N ~ e^{A/4G}).

**Recent resolution (2024-2025):**
- A new prescription for computing holographic complexity in the dS static patch uses the volume of extremal **timelike** surfaces (not spacelike), anchored to the cosmological horizon or an observer worldline. The late-time growth is linear and proportional to the number of degrees of freedom, eliminating hyperfast growth.
- The double-scaled SYK (DSSYK) model provides a microscopic realization where spread complexity counts entangled chord states.
- The "complexity = anything" framework shows that among different gravitational complexity proposals, some predict linear growth and others exponential — the hyperfast growth is not universal.

**Complexity plateau:** For a finite system of dimension N = e^S, complexity grows linearly until time t ~ e^S, then plateaus at C_max ~ e^S. After the plateau, complexity fluctuates and exhibits quantum recurrences on doubly-exponential timescales ~ e^{e^S}. This plateau is the complexity analog of thermal equilibrium for entropy.

**Cosmological constant connection:** The de Sitter horizon has entropy S_dS = π/GΛ. The maximum complexity is C_max ~ e^{S_dS} ~ e^{π/GΛ}. If the cosmological constant encodes maximum complexity, then Λ ~ 1/log(C_max), connecting the smallness of Λ to the enormity of de Sitter complexity.

### 1.8 Recent Developments (2024–2026)

**1. Krylov complexity and holographic duality (2024-2026):**
- The momentum-Krylov correspondence (Fan 2024, Caputa et al. 2026) establishes that the rate of change of spread complexity is directly proportional to the proper momentum of a massive particle moving along the radial coordinate in AdS.
- This gives a concrete, calculable map between a boundary complexity measure and a bulk geometric quantity.

**2. Gravitation from optimized computation (Pedraza et al. 2023, JHEP):**
- **Key paper.** The principle of "spacetime complexity" states that gravitational physics emerges from spacetime seeking to optimize the computational cost of its quantum dynamics.
- They derive the full nonlinear Einstein equations from the CV proposal in Fermi normal coordinates.
- They extend beyond Einstein to derive **higher-derivative gravitational equations** by including corrections to the CV dictionary.
- Semi-classical equations arise from leading bulk quantum corrections.
- This was rigorously validated in 2D dilaton gravity.

**3. Black hole singularities from complexity (2025):**
- Using a second law of complexity, a black hole singularity theorem was proven — introducing "trapped extremal surfaces" whose existence implies null geodesic incompleteness.

**4. Complexity = Anything (2023-2025):**
- Multiple gravitational observables exhibit the expected behavior of complexity (linear growth, switchback effect, saturation). This "complexity = anything" problem suggests the field needs to identify which specific geometric observable IS complexity, or accept that multiple observables encode different aspects of it.

**5. Review: Quantum complexity in gravity, QFT, and QI (Bulchandani, Chapman, et al. 2025):**
- Comprehensive review identifying three paradigms: Nielsen circuit complexity, Krylov/spread complexity, and tensor-network complexity.
- Key open problems: proving superpolynomial growth bounds, resolving definition ambiguity (which complexity?), extending to strongly coupled QFT.
- Critical unresolved tension: the "holographic multiplicity problem" — multiple geometric duals appear valid.

---

## 2. Constructive Framework: Building Spacetime from Complexity

The existing literature (surveyed above) treats complexity as a *dual description* of spacetime — a correspondence. The question is: can we go further and propose that spacetime geometry IS complexity geometry, in a constructive (not merely dual) sense? Here I attempt to build such a framework, drawing on the existing tools but pushing toward a more radical identification.

### 2.1 Circuit Complexity as the Spacetime Metric

**The proposal:** The spacetime metric g_μν is identified with the complexity metric on the space of quantum states. Specifically:

In Nielsen's framework, the space of unitary operators SU(2^K) is equipped with a right-invariant Riemannian metric defined by a cost function F:

d(I, U) = min_γ ∫₀¹ F(γ(t), γ̇(t)) dt

This defines a "complexity geometry" — a genuine Riemannian (or more generally Finsler) manifold. The proposal is:

**The physical spacetime metric is a projection/emergence of the complexity metric on the space of all quantum states of the underlying degrees of freedom.**

**Evidence supporting this:**

1. **Erdmenger et al. (2023)** showed explicitly that in 3D AdS, there exists a geometric object in the bulk that is dual to the Fubini-Study distance (a natural complexity measure) on the space of CFT states. This is a concrete map between complexity geometry (where each point = a state, distances = Fubini-Study metric) and holographic spacetime geometry.

2. **The Nature paper (Brown et al. 2023)** on universality in long-distance complexity geometry showed that the complexity geometry has robust universal features: it is negatively curved (negative sectional curvature), with the radius of curvature much smaller than the diameter. At long distances, different complexity metrics give the same qualitative geometry — this universality is what you'd want if the metric has physical meaning.

3. **Pedraza et al. (2023)** derived the full nonlinear Einstein equations from optimizing the CV complexity functional. If the Einstein equations are what you get when you extremize complexity, then the spacetime metric IS the metric that minimizes computational cost.

**How it would work concretely:**

- Start with K qubits (or a K-dimensional Hilbert space) — the microscopic degrees of freedom of spacetime.
- The space of states is CP^{2^K - 1} (projective Hilbert space), equipped with the Fubini-Study metric or a more general Nielsen complexity metric.
- The classical spacetime metric emerges in the large-K, semiclassical limit of this complexity geometry.
- Different cost functions correspond to different gravitational theories — Einstein gravity from the simplest cost function, higher-derivative gravity from modified cost functions.

**Key difficulty:** The complexity geometry lives on a very high-dimensional space (dim ~ 2^K), while physical spacetime is 4-dimensional. The emergence mechanism requires a dramatic dimensional reduction — the 4D metric must be a low-energy effective description of the full complexity geometry. This is reminiscent of how the emergent AdS spacetime from MERA has many fewer dimensions than the Hilbert space.

### 2.2 Time as Complexity Growth (The Second Law of Complexity)

**The proposal:** The arrow of time IS the direction of increasing complexity. Physical time evolution IS the growth of circuit complexity.

**Brown & Susskind's Second Law of Complexity (2018):**
They showed that for a quantum system of K qubits, complexity grows linearly in time for exponentially long times (t ~ e^K), then plateaus at C_max ~ e^K. This parallels the second law of thermodynamics:

| Property | Entropy (2nd law) | Complexity (2nd law) |
|---|---|---|
| Growth | Increases to equilibrium | Increases for exp. long time |
| Saturation | At S_max ~ K | At C_max ~ e^K |
| Timescale | Thermalization: t ~ K | Complexity plateau: t ~ e^K |
| Fluctuations | Rare entropy decreases | Rare complexity decreases |
| Recurrence | Poincaré: t ~ e^{e^K} | Doubly-exponential: t ~ e^{e^K} |

**Key insight — uncomplexity as a resource:**
"Uncomplexity" (having less than maximal complexity) is a thermodynamic resource, analogous to having less than maximal entropy. Uncomplexity can be "spent" to do useful quantum computation, just as low entropy can be spent to do work.

**Connection to black hole interiors:** Brown & Susskind identified the uncomplexity resource as the accessible volume of spacetime behind a black hole horizon. As a black hole ages, its complexity grows, its interior volume grows, and its uncomplexity decreases. When complexity saturates, the interior has been "used up" — this is the complexity version of heat death.

**Constructive implication:** If time IS complexity growth, then:
- The **arrow of time** is explained by the overwhelming typicality of complexity-increasing evolution (just as the arrow of time in thermodynamics comes from typicality of entropy-increasing evolution, but on exponentially longer timescales).
- **Lloyd's bound** dC/dt ≤ 2E/πℏ becomes a bound on the **rate of time flow** — energy determines how fast time passes, which is reminiscent of gravitational time dilation (clocks run slower in gravitational potential wells where they have less energy to "spend" on computation).
- The **complexity plateau** at t ~ e^S corresponds to a kind of "deep equilibrium" — the quantum analog of the heat death of the universe, but occurring on much longer timescales.

**Critical question:** Is this genuinely different from thermodynamic time? The answer appears to be yes: entropy saturates quickly (at thermalization) while complexity continues growing for exponentially longer. The complexity arrow of time extends far beyond the thermodynamic arrow. This is precisely what's needed to explain the continued growth of black hole interiors (volume grows long after thermal equilibrium is reached).

### 2.3 Gravity as Computational Cost Optimization

**The proposal:** The Einstein equations (and their higher-derivative generalizations) are the equations of optimal computation — spacetime geometry is the configuration that minimizes the computational cost of quantum dynamics.

**Pedraza et al.'s "spacetime complexity" principle (2023):**
"Gravitational physics emerges from spacetime seeking to optimize the computational cost of its quantum dynamics."

Concretely:
1. Start with the CV conjecture: C = V(Σ)/(G_N ℓ)
2. Use Fermi normal coordinates in a geodesic causal ball
3. Varying the complexity functional with respect to the metric yields the Einstein equations: G_μν + Λg_μν = 8πG T_μν
4. Modifying the cost function (adding higher-order terms to the CV dictionary) yields higher-derivative gravitational equations.
5. Including quantum corrections to CV yields semi-classical equations.

**This was validated rigorously in 2D dilaton gravity** (where backreaction can be solved exactly) and proposed to extend to arbitrary dimensions.

**Interpretation:** Just as in classical mechanics the equations of motion come from extremizing the action (principle of least action), in quantum gravity the equations of motion come from optimizing computational complexity (principle of optimal computation). The gravitational action IS the computational cost — this is exactly the CA conjecture's claim.

**What does "optimization" mean physically?** The system doesn't "choose" to optimize — rather, the metric that satisfies Einstein's equations IS the one that corresponds to optimal (geodesic) paths in complexity geometry. Just as a ball doesn't "choose" to follow Newton's laws — it follows geodesics in spacetime — spacetime itself follows "geodesics" in complexity space.

**Key extension:** The fact that modified cost functions yield higher-derivative gravity is deeply significant. In the QG+F framework (the unique UV-complete quadratic gravity), the Lagrangian includes R² and R_μν² terms. The complexity framework can potentially derive this specific Lagrangian from a specific choice of cost function — and the requirement of unitarity (ghost freedom) would constrain which cost functions are physically allowed.

### 2.4 Cosmological Constant and Maximum Complexity

**The proposal:** The cosmological constant Λ encodes the maximum complexity of the universe.

**Chain of reasoning:**

1. De Sitter space has a cosmological horizon with area A = 4π/HΛ, giving entropy S_dS = A/4G = π/(GΛ).
2. A system with entropy S has Hilbert space dimension N = e^S, and maximum circuit complexity C_max ~ e^S.
3. Therefore, the maximum complexity of de Sitter space is C_max ~ exp(π/GΛ).
4. For our universe, Λ ~ 10⁻¹²² M_P⁴, giving S_dS ~ 10¹²² and C_max ~ e^{10^{122}}.

**Inverting this:** Λ ~ π G / ln(C_max). The smallness of Λ follows from the enormity of the maximum complexity — the cosmological constant is small because the universe is an astronomically complex computer.

**Aaronson's computational perspective:** The cosmological constant limits computation — the maximum number of bits that can ever be used in a computation is ~ 1/Λ in Planck units. The class of solvable problems is DSPACE(1/Λ). Λ is not an energy density — it's a computational bound.

**Complexity plateau and cosmic fate:** At time t ~ e^{S_dS} ~ e^{10^{122}} (in Planck times), the universe reaches its complexity plateau. This is astronomically long but finite. After the plateau, the universe enters a regime of random complexity fluctuations on doubly-exponential timescales — analogous to Poincaré recurrences but for complexity.

**Critical assessment:** This is evocative but may be circular. The cosmological constant determines the de Sitter entropy, which determines the maximum complexity — but this is just restating the de Sitter entropy in complexity language. The question is whether the complexity perspective gives us anything NEW. One possible gain: it might explain *why* Λ takes its specific value — perhaps the universe selects the Λ that maximizes computational capacity (a computational anthropic principle?). But this is speculative.

### 2.5 Black Holes as Complexity Maximizers

**The proposal:** Black holes are systems that maximize the rate of complexity growth — they are the fastest computers in nature, and this property is what defines their gravitational character.

**Evidence:**

1. **Lloyd's bound saturation:** For the CA conjecture, Schwarzschild-AdS black holes saturate Lloyd's bound: dC/dt = 2M/πℏ. No other system in nature computes faster per unit energy.

2. **Fastest scramblers:** Black holes scramble information in time t_scr ~ β ln S (Hayden-Preskill), the minimum time allowed by quantum mechanics for a system of that entropy. Scrambling is the process by which simple information becomes computationally complex — black holes do this optimally.

3. **Interior growth:** The black hole interior volume grows linearly in time, dual to linear complexity growth. The interior IS the growing complexity of the quantum state.

4. **Complexity barrier = horizon:** The event horizon is the boundary between "accessible" complexity (reconstructible from the boundary) and "inaccessible" complexity (the interior, requiring exponentially complex operations to access). In QEC terms, the interior is the "logical" information encoded in an exponentially complex code.

5. **Hawking radiation as complexity reset:** When a black hole evaporates, its complexity eventually "resets" — the radiation allows access to the previously hidden interior information, but only after a Page-time worth of radiation. This is the complexity version of the information paradox resolution.

**Constructive implication:** If black holes are complexity maximizers, then the formation of a black hole IS the system reaching its maximum complexity growth rate. The Einstein equations (which predict black hole formation from sufficient energy concentration) are equivalent to the statement that concentrated energy maximizes computational throughput. Gravity is the force that optimizes computation.

**Singularity as complexity saturation:** The 2025 result (black hole singularity theorem from complexity) suggests that the singularity corresponds to the point where complexity growth cannot continue — the computational resources have been exhausted. The "trapped extremal surfaces" whose existence implies geodesic incompleteness are complexity-theoretic objects.

---

## 3. Constraint Checks

### 3.1 Graviton Propagator

**Question:** Does the complexity framework reproduce the correct spin-2 graviton propagator at low energies?

**Assessment:** The complexity framework does not directly construct a propagator — it's not a quantized field theory in the traditional sense. However:

1. Pedraza et al. derived the full nonlinear Einstein equations from complexity optimization. The linearized Einstein equations around flat space automatically yield the correct spin-2 graviton propagator (this is a standard result in linearized gravity).

2. In the holographic context, the graviton is the dual of the stress-energy tensor on the boundary. The complexity approach inherits this identification — the spin-2 nature of the graviton is guaranteed by the conformal symmetry of the boundary theory.

3. **Gap:** There is no direct computation of the graviton propagator from complexity geometry in the manner that, say, loop quantum gravity computes it from spin foams. The complexity program currently relies on holography for its gravitational interpretation.

**Verdict:** Likely reproduced (inherited from holographic duality and from the derivation of Einstein equations), but not independently derived. **Partial pass.**

### 3.2 Lorentz Invariance

**Question:** Does a discrete circuit structure break Lorentz invariance?

**Assessment:** This is a significant concern. Quantum circuits are built from discrete gates, suggesting a fundamental discreteness that could break Lorentz symmetry.

However:

1. **Causal set theory precedent:** Fundamental discreteness need not violate local Lorentz invariance — the causal set program demonstrates this. A random sprinkling of points (Poisson process) on a manifold maintains statistical Lorentz invariance.

2. **QCA approach:** Quantum cellular automata on lattices recover Lorentz-invariant wave equations (including free QED) in the continuum limit. Lorentz symmetry emerges as an effective symmetry at long wavelengths.

3. **Finsler → Riemannian:** The natural metric on complexity space is Finsler (not Riemannian), but in the continuum/large-K limit, the Finsler structure can reduce to Riemannian, which is compatible with Lorentz invariance.

4. **Universality:** The Nature paper on universality in complexity geometry showed that different microscopic complexity metrics give the same long-distance behavior. This universality suggests that Lorentz invariance (a long-distance symmetry) is robust against microscopic details.

**Verdict:** Lorentz invariance is likely an emergent symmetry recovered in the continuum limit, similar to how it emerges in causal sets and CDT. Not proven but plausible. **Conditional pass.**

### 3.3 Spectral Dimension

**Question:** Does the complexity framework predict the universal d_s → 2 in the UV?

**Assessment:** This is an important test. The spectral dimension is a robust probe of short-distance spacetime structure.

1. **Dimensional reduction from complexity geometry:** The complexity geometry on SU(2^K) has dimension ~ 4^K, vastly higher than 4. But the *effective* dimension accessible at a given energy scale is much lower. At the highest energies (shortest distances), only the simplest circuits (lowest complexity) are accessible, and the effective dimensionality of the accessible space is dramatically reduced.

2. **Random circuit models:** Random circuits in d spatial dimensions have been shown to exhibit complexity growth consistent with d_s → 2 behavior, because at short distances/times, only local (1D chain-like) circuits contribute, reducing the effective dimension.

3. **CDT/asymptotic safety connection:** CDT finds d_s → 3/2 to 2 in the UV. If the complexity framework is dual to CDT-like dynamics, it should reproduce this.

4. **Tensor network structure:** MERA-like tensor networks have a natural tree structure that reduces effective dimension at short scales.

**Verdict:** The framework plausibly gives d_s → 2 (or close to it) in the UV, from the reduced dimensionality of short circuits, but this has not been rigorously computed. **Plausible but unproven.**

### 3.4 Bekenstein-Hawking Entropy

**Question:** Does S = A/4G follow from the complexity framework?

**Assessment:**

1. **From RT through tensor networks:** The HaPPY code and random tensor networks exactly reproduce the Ryu-Takayanagi formula S = Area(γ)/4G, from which Bekenstein-Hawking entropy follows when γ wraps the horizon.

2. **From complexity directly:** The Bekenstein-Hawking entropy counts the *number of microstates* (e^S = dimension of code subspace). In the complexity framework, this is the number of distinct quantum states that map to the same macroscopic black hole geometry — equivalently, the dimension of the logical Hilbert space of the QEC code.

3. **From the CV conjecture:** The entropy S is related to the complexity growth rate: dC/dt ~ TS (at late times for large black holes), connecting entropy to the rate of complexity increase.

**Verdict:** **Pass.** Bekenstein-Hawking entropy is naturally reproduced, either through the tensor network / QEC connection or through the holographic duality.

### 3.5 Ghost Freedom

**Question:** Does the complexity framework avoid ghosts?

**Assessment:** This is the most subtle constraint.

1. **At the Einstein level:** The complexity framework derives the Einstein equations, which are ghost-free by construction (no higher-than-second-order time derivatives in the field equations).

2. **At the higher-derivative level:** Pedraza et al. showed that modified cost functions give higher-derivative gravity. But generic higher-derivative gravity has ghosts (Ostrogradsky instability). The critical question: does the requirement of a valid cost function (positive-definite, satisfying triangle inequality) automatically select ghost-free higher-derivative theories?

3. **Fakeon prescription connection:** In the QG+F approach, ghosts are handled by the fakeon prescription (quantizing ghost-like poles as virtual-only particles). If the complexity cost function corresponds to a specific propagator structure, the fakeon prescription might emerge as a computational constraint — negative-norm states are "uncomputable" or infinitely costly, hence excluded.

4. **Unitarity as computability:** In the complexity framework, unitarity is built in from the start (we work on the unitary group SU(2^K)). Any circuit in the space of unitaries is manifestly unitary. The ghost problem arises only in the field-theoretic description — in the complexity description, there are no ghosts because every state is physical.

**Verdict:** Ghost freedom is likely built in by construction (unitarity of the circuit framework), but the mechanism by which this selects specific higher-derivative theories (like QG+F) is unclear. **Conditional pass.**

---

## 4. Novelty Assessment

### 4.1 Comparison to Holographic Entanglement (RT/MVEH)

**Key question:** Does complexity add anything genuinely new beyond what Ryu-Takayanagi and MVEH already provide?

**Answer: YES, unambiguously.**

The entanglement program (RT → MVEH → Einstein equations) has a fundamental limitation: the **linearization barrier**. The entanglement first law gives *linearized* Einstein equations. Subsequent work (Ooguri et al. 2018) showed that the *relative entropy* gives the full nonlinear equations, but this requires going beyond the first law — and at that point, you're using the full structure of the CFT, not just entanglement.

Complexity genuinely extends beyond entanglement:

1. **Interior vs. boundary:** Entanglement (RT) probes the boundary/near-horizon geometry. Complexity (CV/CA) probes the **interior**, including the region behind the black hole horizon. These are genuinely different physical domains.

2. **Timescale separation:** Entanglement saturates at thermalization time t ~ β ln S. Complexity continues growing until t ~ e^S. The physics between thermalization and complexity saturation is entirely in the complexity domain — entanglement has nothing to say about it.

3. **Full nonlinear equations:** Pedraza et al. derived the full nonlinear Einstein equations (and beyond) from complexity optimization — not from entanglement.

4. **Higher-derivative gravity:** The complexity approach naturally generates higher-derivative gravity from modified cost functions. Entanglement-based approaches give at best linearized higher-derivative equations (the linearization barrier of Bueno et al. 2017).

### 4.2 Comparison to Tensor Network Approaches

Tensor networks (MERA, HaPPY) use computational structures but focus on **entanglement** structure, not complexity. They reproduce RT but have difficulty with:
- Time dependence (tensor networks are primarily spatial)
- Interior growth (complexity grows long after the tensor network reaches a fixed point)
- Dynamics (tensor networks describe states, not time evolution)

The complexity approach adds the *dynamical* and *time-dependent* aspects that tensor networks miss.

### 4.3 What Does Computational Spacetime Predict Differently?

**Novel prediction 1 — Complexity plateau in black hole interior:**
At time t ~ e^S after black hole formation, the interior volume stops growing. In GR, the interior grows forever. In the complexity framework, growth must stop because complexity saturates. This is a prediction that GR gets wrong and complexity gets right (GR doesn't know about the finite-dimensional Hilbert space).

**Novel prediction 2 — Singularity resolution:**
The 2025 result proving singularities from a second law of complexity suggests a connection, but the complexity framework may also resolve singularities: if complexity cannot grow past e^S, the infinite growth associated with singularities is replaced by a finite plateau. The "singularity" becomes a complexity barrier, not a point of infinite curvature.

**Novel prediction 3 — Corrections to Einstein gravity:**
The cost function determines the gravitational theory. Different cost functions give different higher-derivative corrections. If we can identify the physically correct cost function (from unitarity, positivity, etc.), we get a specific prediction for the higher-derivative corrections to GR — potentially identifying the specific UV completion.

**Novel prediction 4 — Maximum computation rate = maximum gravitational binding:**
Black holes saturate Lloyd's bound because they are maximally gravitationally bound. This predicts that ANY system approaching the Lloyd bound must have an event horizon. This is a testable prediction connecting information theory to gravitational physics.

### 4.4 Is This Genuinely New or Repackaging?

**Honest assessment:**

The complexity-geometry program is **partially new and partially repackaging**.

**Genuinely new:**
- The interior/post-thermalization physics (Section 4.1 points 1-2)
- The derivation of full nonlinear Einstein equations from complexity (not from entanglement)
- The higher-derivative extension
- The complexity plateau prediction
- The second law of complexity and its gravitational implications
- The connection between Lloyd's bound and gravitational physics

**Still repackaging (or at least dependent on holography):**
- The CV and CA conjectures are defined *within* AdS/CFT — they rely on having a known bulk geometry to define the volume or action. A truly constructive framework would derive the geometry from complexity, not compute complexity from geometry.
- The tensor network models that reproduce RT are entanglement-based, not complexity-based, even though they use computational structures.
- Krylov complexity results are largely restricted to specific models (SYK, JT gravity) and it's unclear they generalize.

**The critical gap:** The program has made impressive progress going from "complexity corresponds to geometry" toward "complexity determines geometry" (via the Pedraza derivation), but has NOT achieved "complexity CONSTRUCTS geometry" in a fully background-independent way. The Pedraza derivation still works within holography — it shows that the right equations emerge from optimizing complexity, but the complexity itself is defined relative to the known background.

A fully constructive theory would need:
1. A definition of complexity that doesn't presuppose spacetime
2. A mechanism for 4D spacetime to emerge from the high-dimensional complexity space
3. A derivation of the metric (not just the equations) from complexity

This has not been achieved.

---

## 5. Conclusions

### 5.1 The State of the Program

The complexity-geometry program (2014-2026) has made remarkable progress:

1. **Solid conjectures:** CV and CA provide concrete, testable correspondences between complexity and geometry.
2. **Constructive derivations:** Pedraza et al. derived Einstein equations (and beyond) from complexity optimization — a major step from correspondence to construction.
3. **New physics:** The interior/complexity plateau/second law of complexity genuinely extends beyond what entanglement can describe.
4. **Mathematical framework:** Nielsen's complexity geometry, Krylov complexity, and the Fubini-Study metric provide rigorous mathematical tools.
5. **Recent breakthroughs:** Black hole singularity theorems from complexity, Krylov-momentum correspondence, de Sitter complexity prescriptions.

### 5.2 Viability of "Computational Spacetime" as a QG Theory

**Viability: PROMISING BUT INCOMPLETE.**

The constructive framework outlined in Section 2 is internally consistent and has genuine predictive power. It passes most constraint checks (Section 3), though some are conditional. It genuinely extends beyond entanglement-based approaches.

However, it faces three critical gaps:

1. **Background dependence:** The framework still operates within holography. A truly constructive theory needs a background-independent definition of complexity.

2. **Dimensional reduction mystery:** How do 4 spacetime dimensions emerge from the exponentially-high-dimensional complexity geometry? No mechanism has been proposed.

3. **Which complexity?** The "complexity = anything" problem (Belin & Myers 2022-2023) shows that many geometric observables have the right qualitative behavior. Until we know WHICH complexity measure is fundamental, the framework has a serious ambiguity.

### 5.3 Relationship to QG+F

The complexity framework does NOT automatically produce QG+F. However:
- Modified cost functions in the Pedraza construction yield higher-derivative gravity.
- The requirement that the cost function be positive-definite and satisfy triangle inequality might constrain which higher-derivative theories are allowed.
- If the only allowed cost functions yield theories with the fakeon prescription for ghosts, the complexity framework could potentially DERIVE QG+F from computational principles.

This is a speculative but intriguing connection that has not been explored in the literature.

### 5.4 Key Takeaway

**Complexity is NOT just another language for entanglement.** It accesses genuinely different physics — the interior, the post-thermalization regime, the full nonlinear equations, and higher-derivative corrections. However, the program has not yet achieved a fully constructive, background-independent theory. It is currently the most promising direction for going BEYOND entanglement in the quantum gravity toolkit, but it is not yet a standalone theory of quantum gravity.

**Recommendation:** This direction deserves serious pursuit. The most promising next step would be to connect the Pedraza cost function constraints to the specific form of QG+F, potentially showing that the unique ghost-free, renormalizable, unitary theory (QG+F) corresponds to the unique "physically allowed" cost function in the complexity framework.
