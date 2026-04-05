---
topic: barandes-stochastic
confidence: provisional
date: 2026-03-28
source: barandes-stochastic strategy-001 exploration-004
---

# Physical Content Verdict: Level 2 Reformulation

## Three Value Proposition Tests

### Test A -- Selection Principle: NEGATIVE within QM

The ISP framework does NOT select a proper subset of quantum theories. All finite-dimensional QM is covered in the forward direction (QM -> ISP via Gamma_ij = |U_ij|^2) and the reverse direction (ISP -> QM via Stinespring dilation).

**The selection runs the other way:** ISP selects FROM stochastic processes -- not all stochastic matrices are ISPs. CTMCs are excluded (infinitely divisible). The ISP framework characterizes which stochastic processes can be quantum: those with indivisible (non-Markovian) transition kernels.

**But this isn't new:** Non-Markovianity of quantum dynamics is well-known in quantum information (Breuer-Laine-Piilo measures, Rivas-Huelga-Plenio 2010). ISP uses the same concept under a different name.

### Test B -- Computational Advantage: NEGATIVE

ISP is a coarser description that erases coherences/phases. Every quantum calculation is harder or equivalent in the ISP formulation:

- **Open quantum systems:** Lindblad structure lost in ISP; calculations of decoherence rates require H and Lindblad operators
- **Classical limits:** Just decoherence in stochastic language; thermalization rates (Fermi's golden rule) more natural in Hilbert space
- **Interference:** ISP discards phases in Gamma; computing interference requires reconstructing Theta -- going back to Hilbert space
- **Bell inequalities:** CHSH/Tsirelson paper is foundational, not computational

### Test C -- Structural Insight: POSITIVE (3 insights)

1. **Complex numbers from indivisibility** (see `complex-numbers-from-indivisibility.md`) -- Genuine structural derivation, not completely without prior art (Stueckelberg 1960)
2. **Tsirelson bound from causal local ISP** (see `chsh-tsirelson-causal-locality.md`) -- Identifies which postulate does the work
3. **Phase-freedom = realm selection** (from E003b) -- Schur-Hadamard gauge freedom structurally analogous to consistent histories realm selection problem. NOT in the literature -- Barandes never cites consistent histories, Griffiths/Gell-Mann-Hartle never discuss ISP. Closest prior: Brun (2000) connects quantum trajectories to consistent histories but uses different mathematical object.

## Amplituhedron Comparison

| Amplituhedron Value | Barandes Analog | Present? |
|--------------------|-----------------|----------|
| UV finiteness as selection | Causal local ISP -> Tsirelson bound | PARTIAL |
| EFT-hedron: new inequalities on Wilson coefficients | New constraints on dynamics parameters | NO |
| Hidden zeros: inter-theory structure | Phase freedom = realm selection | POSSIBLE but undeveloped |
| Simpler computations | Stochastic language -> simpler calculations | NO -- harder |

**Key asymmetry:** The amplituhedron's most important contribution is the EFT-hedron (concrete measurable inequalities). Barandes has NO analog. The amplituhedron adds *operational* value (new computations). Barandes adds *conceptual* value (new explanations for known results). Both legitimate, but amplituhedron is more scientifically impactful.

## Overall Verdict

Level 2 reformulation (as classified in E002), refined to **Level 2+** after adversarial review (E005): a principled reformulation with genuine explanatory/foundational contributions and real potential for extension, but currently delivering zero operational novelty. The measurement problem dissolution and causal locality principle are substantive contributions beyond "just a reformulation," but no new predictions, no operational value, and no extension beyond QM has been demonstrated.

**Level 2 → Level 3 transition requires one of:**
- (a) Proof that causally local non-unistochastic ISPs also satisfy Tsirelson (removes QM assumption)
- (b) A stochastic variational principle for ISP dynamics (the "Lagrangian moment")
- (c) An operational result on quantum channel capacities or error correction from the stochastic language

None of these exist yet. See `steelman-and-level-3-paths.md` for the four steelman arguments and detailed transition analysis.

## One-Paragraph Answer: "What Does It Buy Me?"

"Barandes' indivisible stochastic dynamics buys you exactly one scientifically useful thing: a principled explanation for WHY Tsirelson's bound is 2sqrt(2) rather than the no-signaling maximum of 4 -- specifically, because causal local indivisible stochastic evolution is precisely the class of dynamics that achieves this bound. It also gives a structural derivation of why QM needs complex numbers (needed for amplitude-squared representation for N>2 states). Beyond these two structural insights, the framework adds nothing for working physics: no new predictions, no easier calculations, no access to new experiments, and no coverage of field theories or relativistic systems. Every calculation you'd want to do is either harder (you lose the coherences that carry phase information) or identical (you need Hilbert space anyway). The value is foundational/philosophical: if you care about the conceptual architecture of quantum mechanics, ISP offers a different and sometimes illuminating starting point. If you care about computing observables, it's a dead end."

## Minor Finding: Pilot-Wave as Hidden Markov Model

Barandes (arXiv:2602.10569, Feb 2026) proposes that de Broglie-Bohm pilot-wave theory is best understood as a hidden Markov model (7 latent-variable properties satisfied). Resolves the ontological-nomological debate in Bohmian foundations by proposing a third option. Explains the Deotto-Ghirardi ambiguity (1998) as gauge freedom. Makes no new predictions. Applies only to fixed, finite numbers of non-relativistic particles.
