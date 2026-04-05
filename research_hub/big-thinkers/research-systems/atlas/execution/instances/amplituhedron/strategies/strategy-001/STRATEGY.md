# Strategy 001 — Compute First, Then Break It

## Objective

Establish computational ground truth for the amplituhedron–QFT relationship, then systematically stress-test it to find where the frameworks diverge, where the geometric approach surpasses Feynman diagrams, and where extensions beyond N=4 SYM fail. The goal is to reach Tier 3+ of the validation guide by producing concrete computational evidence about whether the amplituhedron is a better calculator or a deeper theory.

## Methodology

### Protocol: Verify–Extend–Falsify Cycle

Each exploration should be **computational, not philosophical**. Explorers have full shell access with Python, sympy, numpy, scipy. Every exploration should produce equations, numbers, or proofs — not essays about what the answer "should" be.

The Strategizer should run explorations in three phases, though it has freedom to interleave or adapt:

#### Phase 1: Ground Truth (2–3 explorations)

Build the computational foundation. Each exploration should:

1. **Pick a specific scattering amplitude** (start simple: 4-point tree-level in N=4 SYM, then escalate).
2. **Compute it two ways**: via amplituhedron/positive geometry AND via Feynman diagrams or known analytic results.
3. **Verify agreement** numerically and/or symbolically.
4. **Document the computational cost** of each approach — how many terms, how many diagrams, how much simplification was needed.

The point is not just to confirm known results — it's to build working code and intuition that later phases will use. The Strategizer should ensure at least one exploration reaches beyond tree level (1-loop or higher).

Success criterion: At least two amplitudes independently computed and verified. Computational infrastructure exists for later explorations.

#### Phase 2: Stress Test (2–3 explorations)

Push into regimes where the frameworks differ in difficulty or applicability. Directions include (Strategizer chooses):

- **Higher multiplicity**: 6-point, 8-point amplitudes where Feynman diagrams explode but the amplituhedron may remain tractable
- **Higher loops**: Where does the amplituhedron formulation give cleaner results?
- **Beyond N=4 SYM**: Attempt to apply positive geometry to N<4 theories, pure Yang-Mills, or QCD-like amplitudes. Characterize precisely what breaks and why.
- **Cosmological polytopes**: Do the geometric correlators for cosmological observables reproduce known perturbation theory results? Are there cases where they don't?

Each exploration should produce a concrete comparison — either a computation where one framework succeeds and the other struggles, or a precise characterization of where an extension fails.

Success criterion: At least one case where the amplituhedron approach reaches a result that Feynman diagrams make impractical. At least one attempted extension beyond N=4 SYM with characterized failure mode.

#### Phase 3: Probe for Divergence (2–3 explorations)

This is where novel findings live. Now that the computational base exists, look for physical content:

- **Locality and unitarity**: The amplituhedron derives these as emergent. Are there "amplituhedron-allowed" configurations that violate locality or unitarity? Compute specific examples.
- **Non-planar sector**: The amplituhedron is best understood for planar amplitudes. What happens in the non-planar sector? Is there a geometric object? Does the equivalence survive?
- **Infrared structure**: Do the geometric and field-theoretic approaches handle IR divergences differently? Could they give different physical predictions for IR-safe observables?
- **Information beyond amplitudes**: Does the amplituhedron geometry encode information that scattering amplitudes alone don't capture? (E.g., off-shell structure, correlation functions)

Each exploration should either find a discrepancy or prove equivalence in a specific regime — and characterize the result precisely enough to be novel.

Success criterion: A concrete finding about physical equivalence or non-equivalence, with computation backing it up.

### Exploration Design Rules

- **Each exploration gets ONE well-scoped computational task.** Not "investigate the amplituhedron" but "compute the 4-point 1-loop amplitude in N=4 SYM via Grassmannian residues and compare to the known box integral result."
- **Explorations must produce code.** Reasoning-only explorations are failures. If an explorer can't compute something, it should say what blocked it and what tools/data would be needed.
- **Failed computations are valuable.** If an explorer tries to extend the amplituhedron to pure Yang-Mills and can't, the precise characterization of *why* is a Tier 2–3 result.
- **Prior art must be checked.** Every exploration should identify the closest existing result in the literature and say how its computation goes beyond it.

### Pivoting

If Phase 1 reveals that the amplitudes are too technically complex for explorers to compute from scratch within a single exploration, the Strategizer should pivot to:
- Using known analytic results from the literature as the "Feynman diagram" baseline, and computing only the amplituhedron side
- Focusing on structural/algebraic properties rather than full numerical computation
- Narrowing to the simplest non-trivial case where both computations are feasible

The Strategizer should not spend more than half its budget on Phase 1. If ground truth isn't established in 3 explorations, adapt the approach rather than continuing to bang on it.

## Validation Criteria

- **Tier 1 reached** if: at least one amplitude computed both ways with verified agreement
- **Tier 2 reached** if: at least one case where the amplituhedron gives results Feynman diagrams can't easily reach, OR a characterized extension/failure beyond N=4 SYM
- **Tier 3 reached** if: a concrete, computation-backed answer to "is this just a better calculator?" for at least one specific regime
- **Strategy exhausted** when: all three phases have been attempted, or the Strategizer has evidence that a fundamentally different approach is needed

## Context

- This is the first strategy. No prior exploration exists.
- The meta library is empty — we are generating the first lessons.
- Key figures in the field: Arkani-Hamed, Trnka (amplituhedron), Bai & He (associahedron), Ferro & Lam (Grassmannian), Benincasa (cosmological polytopes).
- The amplituhedron is defined in momentum-twistor space for planar N=4 SYM. Extensions beyond this are active research — the boundaries are not fully mapped.
- Explorers should use: sympy for symbolic computation, numpy for numerical checks, and can reference arXiv papers for known results to compare against.
