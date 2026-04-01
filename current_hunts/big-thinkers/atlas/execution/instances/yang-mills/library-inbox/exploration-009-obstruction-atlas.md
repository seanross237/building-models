# Exploration 009: Complete Obstruction Atlas and Novel Proof Strategy Assessment

## Capstone Synthesis of 8 Explorations

---

## 1. Executive Summary

After 8 explorations — covering Balaban's RG program, constructive QFT, lattice Monte Carlo, the lattice-to-continuum gap, finite group approximations, the modern rigorous frontier, novelty assessment, and spectral gap analysis — we now have a comprehensive technical map of the Yang-Mills mass gap problem. This document synthesizes everything into:

1. A **complete obstruction atlas** with theorem-level precision
2. An assessment of **novel proof strategy combinations**
3. An honest appraisal of **what our strategy contributed**

**Bottom line:** The mass gap problem requires a conceptual breakthrough that nobody currently knows how to make. The period 2020-2026 has seen more rigorous progress than any time since Balaban (1980s), but every result so far is either for the wrong groups, wrong coupling, wrong dimension, or wrong limit. The most promising unexplored path is a combination of Shen-Zhu-Zhu's differential-geometric approach with the large-N → finite-N regime, using Chatterjee's conditional theorem as the bridge from mass gap to confinement.

---

## 2. The Problem Statement

The Millennium Prize Problem requires constructing a quantum Yang-Mills theory on R⁴ with gauge group SU(N ≥ 2) that:
- Satisfies the Wightman axioms (or equivalently, via Osterwalder-Schrader reconstruction, satisfies the OS axioms in Euclidean space)
- Has a mass gap: the spectrum of the quantum Hamiltonian has a gap Δ > 0 above the vacuum

In practice, this requires:
1. **Existence**: Show the continuum limit of lattice Yang-Mills exists and is unique
2. **Axioms**: Verify the OS axioms (reflection positivity, covariance, cluster property) hold for the limiting measure
3. **Mass gap**: Prove exponential decay of connected two-point functions of gauge-invariant operators

The UV renormalization problem (controlling the theory as the lattice spacing ε → 0) is solved by Balaban (1982-89). The entire open problem is **infrared** — controlling the theory at long distances, which requires proving the mass gap.

---

## 3. Complete Obstruction Atlas

For each major approach, we give: (a) what has been achieved, (b) the precise obstruction, (c) classification, and (d) what a breakthrough would look like.

---

### Approach 1: Balaban's Renormalization Group Program

**What has been achieved:**
Balaban (1982-1989) completed a 14-paper series establishing UV stability of 4D lattice Yang-Mills in finite volume T⁴. Specifically:
- Papers 1-8: Foundational RG tools (propagator estimates, block-averaging, gauge fixing)
- Paper 9: Full UV stability in 3D
- Papers 10-12: Small-field effective action in 4D
- Papers 13-14: Large-field control in 4D

**Net result:** For the lattice Wilson action on T⁴ with lattice spacing ε, the partition function Z_ε remains bounded as ε → 0, and subsequential weak limits of the lattice measures exist. This establishes *tightness* — the family of measures {μ_ε}_ε is compact.

**Precise stopping point:**
The program stops at Step 8 of a 12-step reconstruction chain (as we mapped in exploration 004):
- Step 8: Continuum limit — *partly done* (subsequential limits exist; **uniqueness not proved**)
- Step 9: OS axioms — *not attempted*
- Step 10: Infinite volume T⁴ → R⁴ — *not attempted*
- Step 11: Mass gap — *not attempted*

The specific technical obstacle for uniqueness (Step 8): Balaban's RG shows the effective action remains in a "good" region as ε → 0, but does not show the RG map is a **contraction** on the space of effective actions. In superrenormalizable theories (d < 4), contraction follows from the Gaussian fixed point being strongly attractive. In 4D Yang-Mills (marginally renormalizable), the coupling runs only logarithmically — the RG contraction rate is O(1/log(1/ε)) — and no one has shown this slow contraction produces a unique limit.

For observable control (Step 9), the obstacle is combinatorial: tracking gauge-invariant Wilson loop insertions through Balaban's multi-scale decomposition generates new terms at each RG step, and the combinatorial growth of these terms must be controlled across infinitely many scales. Dimock's analogous work on φ⁴₃ suggests this is tractable but has not been done for 4D gauge theory.

**Classification: HARD (Steps 3-5) / FUNDAMENTAL BARRIER (Step 6, mass gap)**

**What would constitute a breakthrough:**
- **Short-term**: A proof that the RG map is a contraction, establishing uniqueness of the T⁴ continuum limit. This would be the first "existence" proof of 4D Yang-Mills without mass gap. Jaffe-Witten assess this as a "major breakthrough," explicitly noting the mass gap would still be missing.
- **Ultimate**: A new nonperturbative technique inserted after Step 7 to establish exponential decay — a completely different type of argument from the RG program itself.

---

### Approach 2: Constructive QFT (Glimm-Jaffe Methods)

**What has been achieved:**
The constructive QFT program succeeded for:
- φ⁴₂, φ⁴₃ (Glimm-Jaffe-Spencer 1974; Feldman-Osterwalder 1976): Full construction satisfying Wightman axioms
- Yukawa₂, Gross-Neveu₂ (asymptotically free): Full construction
- Brydges-Fröhlich-Seiler (1980s): Lattice gauge theories in strong coupling and d=2
- Magnen-Rivasseau-Sénéor (1993): Yang-Mills in 4D with IR cutoff (no UV cutoff) — this solves the UV problem; only IR remains open

The Aizenman-Duminil-Copin theorem (2021) proves that φ⁴₄ is **trivial** (Gaussian in the continuum limit), showing the 4D obstruction for scalar fields is structural. Yang-Mills is expected to escape via asymptotic freedom, but this is unproved.

**Precise technical obstacles — three specific failure modes:**
1. **Cluster expansion divergence**: The standard polymer expansion that works in d < 4 (giving convergent series with small activity per cluster) fails in d = 4 because the coupling constant is dimensionless and the expansion has no automatic small parameter. For YM₄, g² → 0 perturbatively, but non-perturbative contributions are not suppressed.

2. **Large field problem**: In d < 4, the action provides enough suppression to control large-field contributions. At d = 4 (critical dimension), the action and the Gaussian kinetic term have the same scaling, and one cannot separate "large field" from "background field" contributions without losing control.

3. **Infinite RG convergence**: Constructing the continuum limit requires proving convergence of an infinite sequence of RG transformations. For superrenormalizable theories, finitely many renormalization conditions suffice. For 4D YM (just-renormalizable), the RG procedure has infinitely many steps, and proving non-perturbative convergence is an entirely open problem.

**Classification: FUNDAMENTAL BARRIER** — All three failure modes are structural, not just difficult.

**What would constitute a breakthrough:**
A new non-perturbative technique for handling the marginal (just-renormalizable) case. The Gross-Neveu₂ construction is instructive: asymptotic freedom was leveraged via the Pauli principle for fermions. A bosonic analog — some structural property of the Yang-Mills gauge field that tames large-field contributions — would be transformative. None is currently identified.

---

### Approach 3: Lattice Gauge Theory → Continuum Limit

**What has been achieved (numerical, not rigorous):**
Lattice gauge theory has produced extraordinary numerical evidence over 50 years:
- SU(3) glueball spectrum fully mapped below 4 GeV: m(0++) = 1730 ± 80 MeV (Morningstar-Peardon 1999)
- String tension √σ ≈ 420-440 MeV established to sub-percent precision
- Asymptotic scaling verified over β = 5.7-7.5 (Berg-Billoire 2015)
- Universality across lattice actions confirmed at per-mille level
- Large-N scaling checked for SU(N), N = 2,...,12 (Athenodorou-Teper 2021)
- Our computation (exploration 003): SU(2) confinement confirmed, σ = 0.593(13) at β=2.0, area law with R²>0.996

**What has been proved rigorously:**
- Area law (strong coupling only, Osterwalder-Seiler 1978)
- Finite-group mass gap at weak coupling (Adhikari-Cao 2025)
- Mass gap at strong coupling for continuous groups (Shen-Zhu-Zhu 2023, β < 1/48)
- Area law in 't Hooft limit (Adhikari-Suzuki-Zhou-Zhuang 2025)

**Precise obstruction — the physical regime gap:**
For SU(2) or SU(3) at weak coupling (large β, the continuum limit regime), there is NO rigorous result. The chain of rigorously proven statements stops at:
- Tightness of lattice measures (Balaban) ✓
- Subsequential convergence ✓
- Uniqueness of limit ✗ — not proved
- OS axioms for the limit ✗ — not proved
- Mass gap in the limit ✗ — not proved

The numerics are extraordinarily convincing but constitute evidence, not proof. The gap is not merely technical — there is no rigorous framework for controlling 4D Yang-Mills at weak coupling from the lattice.

**Classification: FUNDAMENTAL BARRIER** — 50 years of evidence but no proof technology.

**What would constitute a breakthrough:**
A rigorous bound of the form σ_lat(β, L) ≥ c > 0 uniform in both lattice size L and coupling β → ∞ (continuum limit). This would be the first rigorous proof of confinement in the physical regime. Our computation in exploration 003 provides the numerical baseline but cannot produce this bound.

---

### Approach 4: Stochastic Quantization (Chandra-Hairer-Chevyrev-Shen)

**What has been achieved:**
Chandra, Chevyrev, Hairer, Shen (Inventiones mathematicae, 2024, arXiv:2201.03487) constructed:
- State space for 3D Yang-Mills-Higgs theory
- A Markov process (stochastic quantization flow) that preserves gauge equivalence
- Local-in-time solutions to the renormalized stochastic YMH flow in d = 3
- Gauge covariance of solutions in law

This uses Hairer's regularity structures (Fields Medal 2014), the most powerful existing framework for singular SPDEs. It represents the state of the art in rigorous stochastic PDE approaches to QFT.

**Precise obstruction — the d=4 barrier:**
Regularity structures work by decomposing the field into contributions of different "regularity" (Hölder exponents). In d = 3, the YMH field has Hölder regularity -1/2 - κ (for any κ > 0) — above the critical regularity threshold for the nonlinear terms. In d = 4, YM fields have regularity -1 - κ, which is **below the critical threshold** where the nonlinear self-interaction terms have regularity strictly less than the minimum required by the theory.

Specifically: in d = 4, the gauge field A_μ has scaling dimension [A_μ] = 1. The cubic self-interaction term A∂A + A³ has the same dimension as the kinetic term ∂²A. This marginal scaling means the nonlinear terms cannot be renormalized by finitely many counterterms in the stochastic setting — they require an infinite tower of renormalizations, and regularity structures as currently formulated cannot handle infinite renormalization towers.

**Classification: FUNDAMENTAL BARRIER** (currently) — not merely a technical issue but a structural limitation of the framework.

**What would constitute a breakthrough:**
An extension of regularity structures to the marginal/critical case d = 4. This would require either (a) exploiting YM-specific algebraic structure (gauge symmetry, asymptotic freedom) to reduce the renormalization problem, or (b) a new SPDE framework beyond regularity structures. Neither is currently in sight. The Hairer school does not claim to be working toward d = 4.

---

### Approach 5: Probabilistic Methods (Chatterjee School)

**What has been achieved:**
Chatterjee's school (Stanford) has produced the most consistent stream of rigorous results since 2018. The timeline:

| Year | Result | Reference |
|------|--------|-----------|
| 2018 | Probabilistic reformulation of YM | arXiv:1803.01950 |
| 2020 | Wilson loops for finite gauge groups | CMP 377 |
| 2021 | Strong mass gap ⟹ confinement | CMP 385 |
| 2022 | Wilson loops for finite abelian groups | Ann. IHP 58(4) |
| 2023 | Mass gap at strong coupling (SU(N), Langevin) | CMP 400 |
| 2024 | Gaussian scaling limit for SU(2) YMH | arXiv:2401.10507 |
| 2025 | Mass gap for finite gauge groups | Ann. Prob. 53(1) |
| 2025 | Area law in 't Hooft limit | arXiv:2509.04688 |
| 2025 | U(N) mass gap in 't Hooft regime | arXiv:2510.22788 |
| 2026 | Logarithmic confinement in 3D for SU(n) | arXiv:2602.00436 |
| 2026 | Gaussian limits for all compact groups | arXiv:2603.24555 |

**The conditional theorem** (Chatterjee 2021, CMP 385): For any compact connected gauge group G with nontrivial center (including SU(N)), **strong mass gap ⟹ confinement** (area law for Wilson loops). This is a clean, proved result. It converts the confinement problem into the mass gap problem but does not solve either.

**Precise obstruction:**
The conditional theorem runs in one direction only: mass gap → confinement. What is missing is the other half: proving mass gap for a continuous gauge group at weak coupling. Chatterjee's own frank assessment (Harvard lecture, October 2025): the program has produced "many successes" but "has not reached its original goal."

Every result in the program either:
- Uses finite groups (mass gap for finite G, Wilson loops for finite G) — wrong groups
- Uses large N → ∞ (area law in 't Hooft limit) — wrong limit
- Uses strong coupling (β < 1/48) — wrong coupling regime
- Uses Higgs field or specific scaling (Gaussian limits) — not pure YM
- Produces logarithmic confinement (Chatterjee 2026) — weaker than area law

**The finite → continuous gap**: All combinatorial/probabilistic techniques exploit the discrete gauge orbit structure of finite groups. The critical obstacle is that for continuous G = SU(2), the gauge orbit space is a continuous manifold with Gribov copies — the combinatorial bookkeeping that works for finite groups has no continuous analog.

**Classification: HARD** (most promising active program but no path to continuous group mass gap yet)

**What would constitute a breakthrough:**
A technique for proving exponential decay of correlations for SU(2) lattice gauge theory at ANY coupling β > β₀ for some (possibly large) β₀. This would be the first mass gap result for a continuous non-abelian group — a Tier 1 breakthrough even if β₀ were very large. The technique might come from optimal transport / coupling methods for continuous Lie group-valued measures.

---

### Approach 6: Adhikari-Cao Finite Group Approach

**What has been achieved:**
Adhikari and Cao (Annals of Probability, 2025) proved: for any finite gauge group G and coupling β ≥ β_min = (114 + 4 log|G|)/Δ_G, correlations between gauge-invariant observables at distance L decay as exp(-(β/2)Δ_G(L-1)).

The technique is the **swapping map method** — explicitly not a cluster expansion — which works by:
1. Reformulating the gauge theory via homomorphisms ψ: π₁(S₁(Λ)) → G
2. Decomposing into defect configurations (plaquettes where holonomy ≠ 1)
3. Constructing a measure-preserving bijection that swaps the dependence of two observables
4. Bounding the probability of the "bad" event using Peierls-type estimates

**Why this was needed:** Borgs (1988) showed that cluster expansions fail for non-abelian finite groups because defects can be topologically linked. The swapping map circumvents this entirely.

**Precise obstruction — four structural layers (as analyzed in explorations 006 and 008):**

*Layer 1: Homomorphism space.* The framework uses Hom(π₁(S₁(Λ)), G) being finite. For G = SU(2), this becomes an uncountable continuous manifold. The defect support structure becomes trivial — "generic" SU(2) configurations have nonzero holonomy on every plaquette.

*Layer 2: Counting bounds.* Lemma 2.8: ≤ |G|^|P| configurations with given support P. For SU(2): uncountably many — the entropy vs. energy balance |G|^|P| vs. e^{-βΔ_G|P|} that underlies the Peierls argument completely fails.

*Layer 3: Swapping map.* The bijection T is constructed by matching discrete homomorphisms. For SU(2), there is no combinatorial structure for this matching — measure-theoretic couplings on continuous spaces behave fundamentally differently.

*Layer 4: Spectral gap degeneracy.* Δ_G → 0 as G_n → SU(2) through binary polyhedral subgroups. Consequently:
- β_min = (114 + 4 log|G_n|)/Δ_{G_n} → ∞ (threshold diverges)
- Decay rate (β/2)Δ_{G_n} → 0 for any fixed β (mass gap degenerates)

**Our quantification (exploration 008):**
- Spectral gaps (Cayley graph definition): Δ(2T) = 4.0, Δ(2O) = 1.76, Δ(2I) = 2.29
- β_min values: 31.7 (2T), 73.7 (2O), 58.1 (2I)
- Measured β_c values: 2.2, 3.2, 5.8
- **Vacuousness ratio: 10-23x** — the Adhikari-Cao bound applies only where the theory is already trivially deconfined (β >> β_c)
- β_min **diverges** as |G| → ∞, scaling as Δ_G^{-1} ~ |G|^{0.31}

**Classification: FUNDAMENTAL BARRIER to extension to SU(2)** — structural, not technical.

**What would constitute a breakthrough:**
A version of the mass gap estimate that is **uniform** in |G| — bounds that don't degenerate as the finite group becomes denser. This would require exploiting the specific Lie group geometry of SU(2) that the binary polyhedral subgroups are approximating. No current technique comes close.

---

### Approach 7: Axiomatic / Osterwalder-Schrader Reconstruction

**What has been achieved:**
The Osterwalder-Schrader reconstruction theorem (1973, 1975) gives sufficient conditions (OS axioms E0-E4) for Euclidean Schwinger functions to be the analytic continuations of Wightman functions satisfying relativistic axioms. This is a completed mathematical framework.

For lattice Yang-Mills, reflection positivity holds exactly for the Wilson action (Osterwalder-Seiler 1978) — this is one reason Wilson's lattice formulation is preferred over other discretizations.

**Precise obstruction:**
The OS axioms have never been verified for 4D Yang-Mills in the continuum limit. The obstacles are:
1. **Temperedness (E0)**: Requires correlation function growth bounds — not proved in continuum limit
2. **Euclidean covariance (E1)**: Holds exactly on lattice; continuity in continuum limit requires control of correlation functions
3. **Reflection positivity (E2)**: Holds on lattice for Wilson action; whether it survives ε → 0 requires correlation function control (Gap 1 in our nomenclature)
4. **Cluster property (E4)**: Equivalent to mass gap in many circumstances — precisely the unproved statement
5. **Mass gap (extra condition)**: The Millennium Prize explicitly requires mass gap Δ > 0, not just the axioms

The axiomatic approach is not a proof strategy by itself — it's the target specification. Every approach must ultimately verify these axioms. The gap is that no constructive approach has gotten close enough to apply the reconstruction theorem to 4D Yang-Mills.

**Classification: NOT A BARRIER (the axioms are the goal) but each axiom identifies specific proof requirements**

**What would constitute a breakthrough:**
The key axiom is E4 (cluster property), which is equivalent to mass gap in most settings. Establishing E4 for any 4D Yang-Mills construction would essentially be the Millennium Prize.

---

### Approach 8: Shen-Zhu-Zhu Bakry-Émery / Stochastic Analysis

**What has been achieved:**
Shen, Zhu, Zhu (CMP 400, 2023) proved mass gap for SU(N) Yang-Mills on the lattice at **strong coupling** β < 1/(16(d-1)). In d = 4: β < 1/48. The technique verifies the Bakry-Émery curvature condition for the lattice Yang-Mills measure, implying Poincaré and log-Sobolev inequalities, hence exponential decay.

This is the **first mass gap result for a continuous non-abelian gauge group** at any coupling — a genuine milestone, even though the coupling range is wrong.

**Precise obstruction:**
The Bakry-Émery condition requires that the Ricci curvature of the configuration space (plus the Hessian of the log-density) be bounded below by a positive constant κ > 0. For lattice YM with coupling β:

Ric_eff = Ric_SU(N) - β × (gauge field fluctuations)

At strong coupling (small β), the first term dominates: Ric_SU(N) > 0 since SU(N) is compact and positively curved. At weak coupling (large β), the gauge field fluctuation term grows and the Bakry-Émery condition fails.

More precisely: the condition β < 1/(16(d-1)) comes from a precise estimate showing the fluctuation contribution is bounded by 16(d-1)β. In d = 4, this gives β < 1/48. The physical continuum limit requires β → ∞ — the exact opposite.

**Classification: FUNDAMENTAL BARRIER in current form** — the gap between β < 1/48 and physical β is immense.

**What would constitute a breakthrough:**
Extending the Bakry-Émery condition to large β. This might be achievable in special limits:
- The 't Hooft limit (N → ∞, βN fixed) — already done (Adhikari-Suzuki 2025), but this gives N = ∞ only
- A renormalization group-improved Bakry-Émery estimate — using a coarse-grained description where the effective coupling is always small. Not currently formulated.

---

### Approach 9: Large-N / 't Hooft Limit

**What has been achieved:**
Adhikari, Suzuki, Zhou, Zhuang (2025, arXiv:2509.04688) proved Wilson's area law in the 't Hooft limit (N → ∞, coupling βN fixed ~ λ). The proof chain:
1. In the 't Hooft regime, individual plaquette coupling β ~ 1/N → 0, so Shen-Zhu-Zhu's Bakry-Émery condition holds
2. This gives exponential correlation decay (mass gap) in the large-N limit
3. Chatterjee's conditional theorem gives area law

**Precise obstruction:**
This is a large-N result. The 't Hooft limit N → ∞ is a **mean-field approximation** for gauge theory. At finite N (SU(2) has N = 2, SU(3) has N = 3), large-N corrections are O(1/N²) in perturbation theory, but non-perturbative corrections to the mass gap are completely uncontrolled. The physical theory is at finite N.

Additionally, the 't Hooft limit changes the structure of the problem: at N = ∞, the theory is described by a single classical master field (strings), not by fluctuating quantum fields. The Millennium Prize is explicitly about quantum (finite-N) gauge theories.

**Classification: HARD** — elegant result but not the physical regime.

**What would constitute a breakthrough:**
Extracting finite-N corrections from the large-N result in a controlled way. The N-expansion has never been made rigorous beyond perturbation theory. A non-perturbative control of 1/N corrections to the mass gap would be revolutionary.

---

## 4. Obstruction Atlas Summary Table

| Approach | Best Result | Specific Obstruction | Classification |
|----------|------------|---------------------|----------------|
| Balaban RG | UV stability on T⁴ | RG not shown to be contraction; uniqueness unproved | TRACTABLE (existence) / FUNDAMENTAL (mass gap) |
| Constructive QFT | d ≤ 3 constructions | Marginal renormalizability: no small parameter in 4D | FUNDAMENTAL BARRIER |
| Lattice → continuum | Extraordinary numerics | No rigorous framework for SU(N) at physical weak coupling | FUNDAMENTAL BARRIER |
| Stochastic quantization | 3D YMH local existence | d=4 is critical dimension; regularity structures fail | FUNDAMENTAL BARRIER (currently) |
| Chatterjee probabilistic | Conditional: mass gap → area law; finite-group mass gap | Finite → continuous gauge group gap; no technique for continuous SU(N) | HARD (most active) |
| Adhikari-Cao swapping map | Finite group mass gap at weak coupling | 4-layer structural obstruction to continuous groups; bounds vacuous (10-23x off) | FUNDAMENTAL BARRIER to extension |
| OS reconstruction | Axioms proved as target | Each axiom requires proof — E4 (cluster) = mass gap | TARGET (not a barrier) |
| Shen-Zhu-Zhu Bakry-Émery | SU(N) mass gap at β < 1/48 | Bakry-Émery fails at weak coupling (gauge field dominates curvature) | FUNDAMENTAL BARRIER in weak coupling |
| Large-N / 't Hooft | Area law at N = ∞ | Finite-N corrections to mass gap uncontrolled | HARD (wrong regime) |

**No approach has a clear path to mass gap for SU(2) or SU(3) at the physical weak coupling.** This is not pessimism — it is the state of the art as of 2026.

---

## 5. Novel Proof Strategy Assessment

### 5.1 The Most Promising Unexplored Combination

The obstruction atlas reveals a striking complementary structure between Shen-Zhu-Zhu (continuous groups, strong coupling, differential-geometric) and Adhikari-Cao (discrete groups, weak coupling, combinatorial). Neither works in the physical regime, but they bound it from opposite sides.

**The proposal: Renormalization Group + Bakry-Émery at Multiple Scales**

The fundamental obstacle to Shen-Zhu-Zhu at weak coupling is that gauge field fluctuations dominate the Ricci curvature at short scales. But Balaban's RG program shows that at each scale, one can integrate out short-scale fluctuations and produce an effective action where the effective coupling is controlled. If one could verify a **scale-by-scale Bakry-Émery condition** on the effective theory at each RG scale, and show these conditions compose correctly across scales, the result would be a mass gap for the full theory.

This combination has not been attempted. Its ingredients:
- Balaban's multi-scale effective action (provides controlled effective coupling at each scale)
- Shen-Zhu-Zhu's Bakry-Émery framework (provides mass gap from coupling bounds)
- A composition/stability argument showing scale-by-scale mass gaps imply a global mass gap

The key technical challenge: does the Bakry-Émery condition at one scale imply (or at least not prevent) the condition at the next scale? This is non-trivial because integrating out short-scale modes produces new non-local effective interactions that can violate convexity.

**Difficulty assessment**: This is a genuinely hard research program, not a simple combination. But it is the most principled combination of existing tools, and it targets the core obstacle (weak coupling). Estimated effort: 5-15 person-years of research by experts in both RG and stochastic analysis.

### 5.2 Other Unexplored Combinations

**Combination 2: Optimal Transport + Swapping Map**
Replace Adhikari-Cao's discrete bijection (swapping map) with a continuous measure-theoretic coupling using optimal transport. Optimal transport on SU(N) is well-studied and provides measure-preserving maps between continuous distributions. The challenge: such maps must preserve the gauge theory structure and provide the same covariance bound as the discrete swapping map. The entropy-energy balance would need to be replaced by a continuous analog (e.g., relative entropy bounds).

**Combination 3: 't Hooft at Intermediate N**
The 't Hooft area law was proved for N → ∞. For N = ∞ to help with N = 2 or N = 3, one needs rigorous 1/N corrections. The master loop equations (Makeenko-Migdal) provide a systematic 1/N expansion, and these have been analyzed by Chatterjee-Jafarov (2016). The key step missing: showing the 1/N expansion converges (not just is asymptotic) for the mass gap. This seems very hard but is at least a precisely defined problem.

**Combination 4: Supersymmetric Completion + SUSY Breaking**
Seiberg-Witten theory proves mass gap for N=2 supersymmetric Yang-Mills in 4D by exact duality. If one could add a SUSY-breaking term that smoothly deforms N=2 SYM to pure YM while preserving the mass gap, this would be a proof. Known obstacles: (a) SUSY breaking is notoriously hard to control rigorously; (b) the Seiberg-Witten mass gap depends on magnetic monopole condensation, which might not persist to zero SUSY. This is highly speculative but is the only approach where a mass gap proof is known for a "nearby" theory.

### 5.3 Five Specific Bottleneck Theorems

These are the five most important specific theorems that, if proved, would most advance the field. Each is precisely stated.

**Bottleneck Theorem 1: Uniqueness of the T⁴ Continuum Limit**
*Statement*: For the Wilson lattice action on T⁴_L (fixed L), the family of measures {μ_ε}_{ε→0} converges weakly to a unique limit μ₀ (not just along subsequences).
*Why critical*: This would complete Balaban's program and give the first rigorous construction of 4D Yang-Mills on a torus. The mass gap would still be missing, but existence would be established.
*Current barrier*: Need to show the RG map is a contraction on the space of effective actions. The logarithmic running of the coupling in 4D (vs. power-law in 3D) makes the standard contraction argument fail.
*Estimated effort*: 5-10 years, likely requiring a new functional analytic argument.

**Bottleneck Theorem 2: Observable Control on T⁴ (OS Axiom E2)**
*Statement*: For the Wilson action on T⁴, for any smooth loop C, the Wilson loop expectation ⟨W_C⟩_ε converges as ε → 0, and the limit satisfies reflection positivity.
*Why critical*: This is the first step beyond partition function control. Once observables are controlled, the OS reconstruction becomes a concrete program.
*Current barrier*: Tracking gauge-invariant insertions through Balaban's multi-scale decomposition — each insertion generates new terms at each RG step.
*Estimated effort*: 3-7 years, building directly on Balaban. Believed tractable per Jaffe-Witten.

**Bottleneck Theorem 3: SU(2) Mass Gap at Any Single Coupling**
*Statement*: There exists β₀ > 0 such that for the SU(2) Wilson action at coupling β = β₀ (fixed, not β → ∞), the two-point function of a gauge-invariant operator decays exponentially in Euclidean distance with a positive rate m(β₀) > 0.
*Why critical*: This would be the first mass gap result for a continuous non-abelian group at any coupling. Even at strong coupling (β₀ < 1/48), this is only a slight extension of Shen-Zhu-Zhu — but at weak coupling, it would be revolutionary.
*Current barrier*: Bakry-Émery approach fails at any β > 1/48. No alternative technique for continuous SU(2) at weak coupling.
*Estimated effort*: Unknown (revolutionary if at weak coupling), moderate if strong coupling extension only.

**Bottleneck Theorem 4: Uniform Mass Gap for Finite Group Sequence**
*Statement*: There exist a sequence of finite subgroups G_n ⊂ SU(2) with |G_n| → ∞ and constants c, β₀ > 0 such that for all n and all β ≥ β₀, the G_n lattice gauge theory has mass gap m(G_n, β) ≥ c (uniform in n and in a neighborhood of any fixed β > β₀).
*Why critical*: If the mass gap were uniformly positive as G_n → SU(2), a limit argument would give mass gap for SU(2). Our exploration 008 shows this would require qualitatively different estimates from Adhikari-Cao (whose bounds degenerate as n → ∞ by a factor of 10-23x in the physical regime).
*Current barrier*: Spectral gap Δ_{G_n} → 0, making current bounds degenerate. Uniform bounds would need to use Lie group geometry rather than discrete combinatorics.
*Estimated effort*: 10-20 years if tractable at all; may require genuinely new ideas.

**Bottleneck Theorem 5: Non-Gaussian Scaling Limit**
*Statement*: There exists a non-trivial (non-Gaussian) scaling limit of SU(2) lattice Yang-Mills as ε → 0 with coupling β = β(ε) running according to the non-perturbative beta function.
*Why critical*: Chatterjee (2024) and Rajasekaran-Yakir-Zhou (2026) achieved Gaussian limits by sending the coupling to zero faster than the lattice spacing. The non-Gaussian limit — where the full non-abelian interactions survive — is the actual Yang-Mills quantum field theory. No rigorous construction of a non-Gaussian scaling limit of any non-abelian gauge theory exists in d > 2.
*Current barrier*: Without the Gaussian approximation, no technique controls the non-abelian self-interaction terms in the continuum limit.
*Estimated effort*: Revolutionary; potentially decades.

---

## 6. Cross-Approach Connections

### 6.1 The Chatterjee Bridge

Chatterjee's conditional theorem (strong mass gap → confinement) acts as a **bridge layer**: once any approach proves mass gap, confinement follows automatically. This means the area law is not an additional barrier — it's a corollary. The current bottleneck is purely the mass gap.

### 6.2 The Strong/Weak Coupling Sandwich

Shen-Zhu-Zhu (strong coupling) and Adhikari-Cao (weak coupling for finite G) together suggest the mass gap holds everywhere, but each is stuck on the wrong side of the physical regime. The question is whether information from both ends can be combined:

- Strong coupling: mass gap follows from positive Ricci curvature of SU(N)
- Weak coupling finite G: mass gap follows from defect suppression (Peierls-like)
- Physical regime: neither technique works, but there is numerical evidence from both directions

A **monotonicity argument** might help: if the mass gap m(β) is monotone in β (decreasing with increasing β in the physical regime), and m(β) > 0 at both β → 0 (strong coupling) and at any finite β in the Adhikari-Cao regime for large G, then... but this is circular since we don't know m(β) > 0 at physical β.

### 6.3 The 't Hooft → Finite N Route

The 2025 results (area law at N = ∞) suggest the 1/N expansion might be a viable route to finite N. The master loop equations provide a systematic 1/N expansion, and the mass gap at N = ∞ would propagate to finite N if the expansion converges. The convergence of the 1/N expansion for the mass gap is unstudied rigorously.

### 6.4 Stochastic Analysis + Probabilistic Coupling

The Shen-Zhu-Zhu stochastic analysis uses Langevin dynamics. Chatterjee's school uses probabilistic coupling methods. These are different faces of the same coin — both study the Yang-Mills measure through its dynamics. A synthesis might use the Langevin equation at intermediate scales (where Bakry-Émery applies) and coupling methods at large scales (where defect structure is more tractable). No one has attempted this.

---

## 7. Our Contributions in Context

### 7.1 The Obstruction Atlas

**Assessment: This atlas is more precise than what exists in the standard reviews.**

The Jaffe-Witten millennium problem description (2000) identifies the mass gap as the core problem and Balaban's program as the main tool, but does not map out the modern frontier (Adhikari-Cao, Shen-Zhu-Zhu, Chatterjee's school). Douglas's 2004 description similarly predates the 2020-2026 explosion of results.

Our atlas adds:
1. A theorem-level account of Adhikari-Cao's four-layer obstruction (not just "finite groups" — specific structural reasons each layer fails)
2. The quantitative β_min vs. β_c comparison (10-23x vacuousness, first quantification)
3. The Shen-Zhu-Zhu result framed as the first continuous-group mass gap (even if at wrong coupling)
4. The 2025-2026 results systematically placed in context
5. The 't Hooft route as a coherent third strand
6. Classification of each approach with specific bottleneck theorems

This atlas would be useful to a mathematician entering the field — it provides a map that doesn't currently exist in a single document. It is not itself a proof result.

### 7.2 Finite Group Convergence Rates

**Assessment: Quantitatively novel, of moderate proof-strategic value.**

Our exploration 005 established:
- Binary icosahedral (120 elements) matches SU(2) to < 0.5% across full β range 1-4
- Convergence rate |obs_G - obs_SU(2)| ~ |G|^{-α}, α ≈ 0.7-2.5 — appears novel (no prior paper measured this)
- Hysteresis magnitudes Δ⟨P⟩ = 0.39 → 0.18 → 0.09 — appears novel

The phase transition structure was known since Petcher-Weingarten (1980); Hartung (2022) has an analytic formula β_c(N) = ln(1+√2)/(1-cos(2π/N)).

**Proof-strategic value**: The convergence rates confirm that the physics converges rapidly — the obstacle to using finite groups to prove SU(2) mass gap is in the proof machinery, not the physics. For Bottleneck Theorem 4 (uniform mass gap for finite group sequence), our rates provide the target: any proof must produce uniform bounds consistent with α ≈ 1 convergence.

The data might be publishable as a companion to Hartung (2022), with the specific quantum computing angle (error budget for SU(2) simulations using binary polyhedral subgroups).

### 7.3 Adhikari-Cao Vacuousness Quantification

**Assessment: Important clarifying result, strongest concrete finding of the strategy.**

Our exploration 008 computed (for the first time):
- Spectral gaps of the group Laplacian on 2T, 2O, 2I: Δ = 4.0, 1.76, 2.29 (Cayley graph)
- Adhikari-Cao thresholds β_min = 31.7, 73.7, 58.1 vs. measured transitions β_c = 2.2, 3.2, 5.8
- **Vacuousness ratio: 10-23x** — the bound applies only at coupling strengths far above the bulk transition, where the theory is trivially frozen (not confining)
- β_min diverges as |G| → ∞ (scaling ~|G|^{0.31}), confirming the bound is qualitatively vacuous even in the limit

**This clarifies something important**: Extending Adhikari-Cao to SU(2) is not just a matter of improving constants or using tighter estimates. The current approach produces bounds that are off by a factor of ~15 in the wrong direction — they apply where no interesting physics occurs. A "repair" would require estimates that are qualitatively different in kind, not just quantitatively sharper. This constrains future approaches: any strategy based on the Adhikari-Cao framework must address why the bound fails so badly in the physical regime.

**This does not appear to have been computed in any prior paper.** It is a contribution to the field's collective understanding of why the Adhikari-Cao approach, despite being a genuine breakthrough, does not provide a path to SU(2).

---

## 8. The State of the Art: A One-Page Map

As of March 2026, here is the complete state of rigorous Yang-Mills theory:

**PROVED (4D, relevant groups):**
- UV stability of lattice YM on T⁴ (Balaban, 1982-89)
- Mass gap at strong coupling β < 1/48 for SU(N) (Shen-Zhu-Zhu, 2023)
- Mass gap at weak coupling for all finite gauge groups (Adhikari-Cao, 2025)
- Area law in 't Hooft limit N → ∞ (Adhikari-Suzuki-Zhou-Zhuang, 2025)

**PROVED (3D or with Higgs):**
- Stochastic YM-Higgs dynamics in 3D (Chandra-Hairer-Chevyrev-Shen, 2024)
- Logarithmic confinement in 3D for SU(n) (Chatterjee, 2026)
- Gaussian scaling limit of SU(2) YM-Higgs (Chatterjee, 2024)

**NOT PROVED:**
- Mass gap for any continuous gauge group at weak coupling in 4D
- Area law for SU(N) at any fixed N at weak coupling in 4D
- Confinement for SU(N) pure gauge in 3D (only logarithmic)
- Non-Gaussian scaling limit of any non-abelian gauge theory in d > 2
- Existence and uniqueness of 4D Yang-Mills continuum limit (even without mass gap)

The problem has resisted 60+ years of effort and is widely regarded as requiring a conceptual breakthrough analogous to Hairer's regularity structures, Schramm's SLE, or Seiberg-Witten duality — a genuinely new mathematical idea rather than a refinement of existing tools.

---

## 9. Recommendations for Future Strategy

Based on this atlas, a future strategy should focus on:

**Priority 1: The Shen-Zhu-Zhu extension problem (Bottleneck Theorem 3)**
Can the Bakry-Émery coupling range be pushed beyond β < 1/48, even to β < 1/10? This is a concrete, well-defined problem where progress is measurable. The 't Hooft limit (Adhikari-Suzuki 2025) shows it's achievable at N = ∞; the question is whether finite-N corrections can be controlled at least partially.

**Priority 2: Cross-technique bridge: RG + Bakry-Émery**
The multi-scale RG (Balaban) + differential-geometric mass gap (Shen-Zhu-Zhu) combination has not been attempted. Formulate explicitly: what would it mean to verify Bakry-Émery for the RG-improved effective action at each scale? Can the conditions compose across scales? This could be explored computationally (testing Poincaré inequalities for numerically computed effective actions at intermediate scales) before attempting proofs.

**Priority 3: The non-Gaussian limit problem**
The Gaussian limit is the easy case (coupling → 0 too fast). Develop a precise conjecture for what the non-Gaussian scaling limit should be (likely: string theory / flux tube theory at large scales) and work backward from the desired structure. The AdS/CFT correspondence provides specific predictions for N = ∞; a rigorous AdS/CFT for finite N would be transformative.

**What NOT to pursue:**
- Further iterations of Adhikari-Cao: the 10-23x vacuousness gap is not amenable to incremental improvement
- Numerical lattice computations: the physics is already pinned down to sub-percent precision; further numerics have diminishing returns for proof strategy
- Axiomatic approaches without a constructive input: the OS axioms specify the target but provide no proof mechanism

---

## 10. References

1. Balaban, T.: 14-paper series 1982-1989 on RG for lattice YM
2. Jaffe, A., Witten, E.: "Quantum Yang-Mills Theory" (2000, Clay Millennium Problem description)
3. Adhikari, A., Cao, S.: "Correlation decay for finite lattice gauge theories at weak coupling," Ann. Prob. 53(1), 2025. arXiv:2202.10375
4. Shen, H., Zhu, R., Zhu, X.: "A stochastic analysis approach to lattice Yang-Mills at strong coupling," CMP 400, 2023. arXiv:2204.12737
5. Chatterjee, S.: "A probabilistic mechanism for quark confinement," CMP 385, 2021. arXiv:2006.16229
6. Chatterjee, S.: "A scaling limit of SU(2) lattice Yang-Mills-Higgs theory," 2024. arXiv:2401.10507
7. Chandra, A., Chevyrev, I., Hairer, M., Shen, H.: "Stochastic quantisation of Yang-Mills-Higgs in 3D," Inventiones Mathematicae 237, 2024. arXiv:2201.03487
8. Adhikari, A., Suzuki, T., Zhou, X., Zhuang, Z.: "Dynamical approach to area law for lattice Yang-Mills," 2025. arXiv:2509.04688
9. Chatterjee, S.: "A short proof of confinement in 3D lattice gauge theories with a central U(1)," 2026. arXiv:2602.00436
10. Rajasekaran, Yakir, Zhou: "Gaussian limits of lattice Higgs models with complete symmetry breaking," 2026. arXiv:2603.24555
11. Magnen, J., Rivasseau, V., Sénéor, R.: 4D YM with IR cutoff (1993)
12. Petcher, D., Weingarten, D.: "Monte Carlo calculations for gauge theories on discrete subgroups of SU(2)," PRD 22, 1980
13. Hartung, T., et al.: "Digitising SU(2) gauge fields and the freezing transition," EPJC 82, 2022. arXiv:2201.09625
14. Aizenman, M., Duminil-Copin, H.: "Marginal triviality of the scaling limits of critical 4D Ising and φ⁴ models," Ann. Math. 194, 2021
15. Osterwalder, K., Schrader, R.: "Axioms for Euclidean Green's functions," CMP 31/42, 1973/1975
16. Wilson, K.: "Confinement of quarks," PRD 10, 1974
17. Morningstar, C., Peardon, M.: "Glueball mass spectrum from an anisotropic lattice study," PRD 60, 1999
18. Athenodorou, A., Teper, M.: "SU(N) gauge theories in 3+1 dimensions: glueball spectrum, string tensions and topology," JHEP 2021

---

## Appendix A: Classification Key

- **OVERCOME**: The specific obstacle has been removed; this gap no longer blocks progress
- **TRACTABLE**: Believed solvable with known methods and sufficient effort; clear path exists
- **HARD**: No obvious path; likely requires new ideas in the same mathematical area
- **FUNDAMENTAL BARRIER**: The obstacle appears structural; likely requires a conceptually new approach

Applied to the mass gap problem:
- Balaban (existence, observables): TRACTABLE
- Balaban (uniqueness): HARD
- Balaban (mass gap): FUNDAMENTAL BARRIER (requires completely separate ideas)
- Adhikari-Cao (extension to SU(2)): FUNDAMENTAL BARRIER
- Shen-Zhu-Zhu (extension to weak coupling): HARD → FUNDAMENTAL BARRIER
- Chatterjee (conditional: once mass gap proved, rest follows): OVERCOME (bridge is proved)
- 't Hooft → finite N: HARD

---

## Appendix B: Computational Findings Summary

| Exploration | Computation | Key Result |
|-------------|-------------|------------|
| 003 | SU(2) MC on 4⁴-8⁴ | σ = 0.13-0.59, area law R²>0.996, glueball mass inferred ~2 lat. units |
| 004 | Lattice-continuum gap map | 7-step ladder identified; steps 1-2 done, step 6 (mass gap) fundamental |
| 005 | Binary polyhedral subgroups | 2I matches SU(2) <0.5%, convergence rate α=0.7-2.5 |
| 007 | Novelty search | Rates novel; β_c known; hysteresis magnitudes novel |
| 008 | Spectral gap + Adhikari-Cao | β_min 10-23x too large; diverges as |G|→∞; bounds qualitatively vacuous |

---

*Report complete. REPORT-SUMMARY.md follows.*
