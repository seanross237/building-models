---
topic: Hidden zeros and inter-theory structure — positive geometry beyond N=4 SYM
confidence: verified
date: 2026-03-27
source: "amplituhedron strategy-001 exploration-004, exploration-005; Arkani-Hamed et al. arXiv:2312.16282 JHEP 10(2024)231; Backus, Rodina arXiv:2503.03805 PRL 2025; Rodina arXiv:2406.04234 PRL 2025"
---

## The Discovery (2024)

Arkani-Hamed et al. discovered that bi-adjoint scalar ϕ³, pion (NLSM), and gluon (Yang-Mills) amplitudes share:
1. A specific **kinematic structure** — the three theories are related by a kinematic shift
2. **Hidden zeros**: specific kinematic loci where all three amplitudes vanish exactly

(arXiv:2312.16282, JHEP 10(2024)231)

**These zeros were not predicted by Lagrangian methods.** They are invisible from any single theory's perspective. They were discovered via positive geometry: at the zero kinematics, the ABHY associahedron collapses to a lower-dimensional polytope — the vanishing is a geometric fact. For the technical mechanism (causal diamonds, explicit formulas, factorization near zeros), see `hidden-zeros-mechanism.md`.

## The δ-Deformation: Unity of Colored Theories

The three theories — Tr(φ³), NLSM, and Yang-Mills — are unified by a **one-parameter family**:

```
I^δ_{2n} = I^{Tr(φ³)}_{2n}[α'X_{e,e} → α'(X_{e,e}+δ), α'X_{o,o} → α'(X_{o,o}−δ)]
```

- α'δ = 0: Tr(φ³) scalar theory
- α'δ ∈ (0,1): Non-Linear Sigma Model (pions)
- α'δ = 1: Yang-Mills / scaffolded gluons

This shift is **unique**: proved to be the only kinematic shift preserving the hidden zeros.
**All three theories have hidden zeros at exactly the same kinematic locus** (the "universal zero
property"). Gluon polarization vectors emerge from differences of pairs of scalar momenta in the
scaffolded construction.

## What the Zeros Reveal

Three apparently unrelated theories — colored scalars, pions, and gluons — share a common
geometric scaffold. Their amplitude relations are determined by the associahedron's combinatorial
structure. This is the strongest evidence that positive geometry reveals structure across theories
that no Lagrangian perspective makes visible.

**Zeros determine amplitudes (Rodina 2025, arXiv:2406.04234):** Hidden zeros are equivalent to
enhanced UV scaling under BCFW shifts. Combined with the structure of ordered propagators, this
**uniquely determines Tr(φ³) tree amplitudes**. Proved at all n. (NLSM uniqueness: observed at
n=6,8 in the original paper; formal proof open.)

## 2025 Extension: One-Loop Non-SUSY Emergence (arXiv:2503.03805, March 2025)

In Tr(φ³) theory (non-supersymmetric scalar theory), hidden zeros extend from tree-level to one-loop.
The key result (proved for local ansatz, conjectured for non-local):

- Start with a **generic non-local, non-unitary ansatz** for the one-loop integrand
- Impose **only the hidden-zero conditions** ("big mountain" zeros)
- The zeros **uniquely fix** the one-loop integrand
- Locality and unitarity emerge as consequences, not inputs

For detailed one-loop results, explicit integrands, and the loop-to-tree factorization, see
`hidden-zeros-one-loop.md`.

**Significance**: The amplituhedron formulation requires N=4 SYM because of Yangian symmetry
and UV finiteness. Hidden zeros suggest the underlying principle operates more broadly —
potentially for any theory with a positive geometry foundation, regardless of supersymmetry.

## Status

- **Hidden zeros at tree level** [ESTABLISHED]: Proved for Tr(φ³); proved for NLSM; observed for YM.
- **Zeros determine amplitudes** [ESTABLISHED, tree level]: Proved for Tr(φ³) (Rodina 2025); observed for NLSM.
- **Unity of colored theories via δ-deformation** [ESTABLISHED]: Unique zero-preserving shift.
- **One-loop hidden zeros** [PROVED for local ansatz; CONJECTURED for non-local at n>4].
- **Scope and extensions** (massive theories, double-copy, cosmology): See `hidden-zeros-scope-and-extensions.md`.

## Assessment: New Principle or Reformulation?

**Already proved as new structure:** The δ-deformation revealing Tr(φ³)/NLSM/YM as a single
one-parameter family is a genuine result not derivable from individual Lagrangians. The inter-theory
relationships were not known before positive geometry.

**The potentially revolutionary (still conjectural) claim:** That zeros from a NON-LOCAL ansatz
uniquely fix amplitudes at all loop orders, deriving locality and unitarity from a more primitive
geometric principle. If proved at all multiplicities and loop orders, this would parallel the
amplituhedron's elimination of locality/unitarity as inputs for N=4 SYM — but for the full class
of colored theories including non-SUSY gauge theories.

**Contrast with the amplituhedron**: Within N=4 SYM, the amplituhedron is a reformulation.
Hidden zeros produce inter-theory predictions visible from no single Feynman-diagram perspective.

For the parent framework (surfaceology) that encompasses both the ABHY associahedron and
hidden zeros, see `surfaceology-all-loop-framework.md`.
