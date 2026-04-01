# Exploration 002: Extract Viable Conceptual Moves from SCG v2.0

## Mission Context

We are building a focused novel theory around QG+F's most fertile explanatory gap. Exploration 001 identified the **fakeon interpretation cluster** as the #1 target: nobody knows what a fakeon IS physically, WHY the fakeon prescription works, or WHAT it means that analyticity must be sacrificed. The **non-perturbative completion** is the #2 target: QG+F can't define itself beyond perturbation theory.

The previous strategy (strategy-001) built **Stochastic Computational Gravity (SCG) v2.0** — an ambitious synthesis of Barandes stochastic mechanics, Pedraza complexity geometry, Oppenheim stochastic gravity, and causal set ideas. SCG couldn't compete with QG+F quantitatively (lost 16/21 sub-criteria), but it contained conceptual ideas that may be RIGHT even though the implementation failed.

**Your job:** Extract the conceptual raw materials from SCG v2.0 that could power the concept sprint in Phase 2. This is knowledge extraction, not construction.

## What to Extract

### A. Conceptual Ideas That Were Right (Even If Implementation Failed)

For each, assess: does this concept connect to our TOP 5 gaps (especially #1 fakeon interpretation, #2 non-perturbative completion)?

Key SCG concepts to evaluate:
1. **"Gravity as computational cost optimization"** — Pedraza et al. proved this for 2D. Full nonlinear Einstein equations from δC/δg = 0. This overcomes the linearization barrier. Can this idea illuminate the fakeon? (Is the fakeon a constraint on computational cost?)
2. **"Quantum mechanics from indivisible stochastic processes"** — Barandes-Doukas lifting. Proven as isomorphism. Could the "indivisibility" concept (multi-time memory, non-Markovian structure) be relevant to understanding the fakeon's purely-virtual nature?
3. **"Irreducible noise as fundamental"** — SCG's axiom 5 (σ > 0). Could irreducible noise at the Planck scale explain microcausality violation?
4. **"Finite configuration space"** — N ~ e^{10^122}. Does finiteness provide a natural non-perturbative regulator? Could QG+F be the continuum limit of some discrete theory?
5. **"Causal partial order as primitive"** — SCG v2.0's key fix. Via Malament's theorem, causal order + volume = Lorentzian geometry. Could a causal reformulation of QG+F provide the non-perturbative completion?
6. **"Decoherence-diffusion trade-off"** — Oppenheim's central mechanism. Could QG+F's fakeon have a stochastic interpretation (the ghost "diffuses" rather than propagates)?

### B. Technical Results Any Future Theory Must Address

From SCG's development and adversarial assessment:
1. **The fakeon cannot be derived from classical structures** — cost functions are classical geometric objects; the fakeon is a quantum prescription about propagator poles. The same Lagrangian gives Stelle gravity classically and QG+F quantum-mechanically. No classical argument can distinguish them.
2. **"Complexity = Anything" freedom (Belin et al. 2021)** — Infinite class of equally viable complexity functionals. Any construction based on "minimize complexity" must address this degeneracy.
3. **Barandes lifting is isomorphism, not derivation** — The direction (stochastic → QM or QM → stochastic) is metaphysical, not mathematical. Born rule is definitional. Indivisibility may smuggle in QM.
4. **Causal structure is mandatory** — Positive-definite structures cannot produce Lorentzian geometry. This killed SCG v1.0.
5. **Pedraza is 2D only** — The 4D gap is enormous (Einstein tensor vanishes in 2D).

### C. Failure Patterns to Avoid

Catalog which conceptual moves repeatedly led to dead ends in strategy-001:
- Over-ambitious synthesis (combining 5+ programs into one theory)
- Claiming predictions from component programs without independent derivation
- Constructing at the Lagrangian level and expecting it to select a quantization prescription
- Assuming continuum limit existence without proof
- Treating "isomorphism" as "derivation"

### D. Design Brief for Phase 2

Based on A-C, produce a **design brief** — a short document (100-150 lines) that Phase 2's concept sprints should use as their starting point. The brief should:
1. List 3-5 viable conceptual moves, each with an assessment of novelty potential
2. For each move, identify what SPECIFICALLY is new (vs. existing literature)
3. For each move, identify the connection to our TOP 5 gaps
4. Flag anti-patterns to avoid
5. Recommend which 3 gaps should be targeted in the Phase 2 concept sprint

## Context: SCG v2.0's Axioms and Structure

**Five Axioms:** (A1) Finite configuration space Ω, N ~ e^{10^122}. (A2) Indivisible stochastic dynamics. (A3) Causal cost structure: partial order ≺ + directed cost c(x,y) + volume measure v(x). (A4) Optimization: extremize total cost along causal paths. (A5) Irreducible noise σ > 0.

**QM emergence route:** Indivisible stochastic process → Barandes-Doukas lifting → Hilbert space, density matrices, CPTP maps, Born rule.

**Geometry emergence route:** Cost function → finite metric → continuum limit → Riemannian manifold → cost optimization → Einstein equations.

**Adversarial verdict:** "Alive but wounded." Three near-fatal problems: QM emergence is reformulation, continuum limit unproven, Pedraza 2D only.

## Context: The Fakeon Cluster (Exploration 001's #1 Gap)

The fakeon IS QG+F's defining innovation and nobody understands it physically:
- Fakeon is purely virtual — contributes to loops, never appears as asymptotic state
- No classical limit exists for the massive spin-2 mode
- Analyticity of the S-matrix must be sacrificed (JHEP 05, 2025)
- Anselmi proposes abandoning causality itself (arXiv:2601.06346, Jan 2026)
- IHO/DQFT gives competing interpretation (March 2026)
- Modular flow unitarity argument: MVEH → fakeon is the closest existing derivation
- Ghost confinement (QCD analogy) is physically intuitive but dynamically unproven

## Success Criteria

- ✅ At least 5 conceptual moves extracted and assessed for relevance to TOP 5 gaps
- ✅ Each move rated for genuine novelty (vs. existing literature)
- ✅ At least 3 failure patterns documented with specific examples from strategy-001
- ✅ Design brief produced with 3 recommended concept sprint targets
- ✅ Clear distinction between "concepts that connect to fakeon interpretation" and "concepts that don't"

## Failure Criteria

- ❌ Just re-describes SCG without critical extraction
- ❌ No connection made to the fakeon interpretation or non-perturbative completion gaps
- ❌ Design brief is vague ("explore complexity-based approaches") rather than specific

## Practical Notes

- Write REPORT.md IMMEDIATELY — skeleton first (title + section headers), BEFORE any research.
- Your exploration directory: `explorations/exploration-002/`
- This is primarily analysis of existing material, not new web research. You may do web searches to check novelty of specific concepts, but the bulk of the work is thinking and synthesizing.
- Aim for 200-300 lines in REPORT.md.
- Write REPORT-SUMMARY.md last.
