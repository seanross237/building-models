# Atlas Idea 003: Hodge Conjecture

## Description

The Hodge Conjecture is one of the seven Millennium Prize Problems ($1M prize). It states: on a smooth projective complex algebraic variety, every Hodge class is a rational linear combination of classes of algebraic cycles.

In less technical terms: complex algebraic varieties (shapes defined by polynomial equations in complex coordinates) have a rich topological structure described by cohomology groups. These groups decompose into pieces called Hodge types. The conjecture says that certain "special" cohomology classes (Hodge classes) always come from actual geometric sub-shapes (algebraic cycles), not just abstract topology.

Known partial results:
- **Lefschetz (1,1) theorem (1924):** The conjecture is true for codimension-1 cycles (divisors). This is the easiest case and was proved over a century ago.
- **Kodaira-Spencer:** True for surfaces (dimension 2).
- **Deligne (1974):** For abelian varieties, Hodge classes on products of elliptic curves are algebraic.
- **Voisin (2002):** Proved that the integral Hodge conjecture is FALSE — there exist integral Hodge classes that are not algebraic. The rational version (with rational coefficients) remains open.
- **Totaro (2013):** Further counterexamples to integral version.
- **Computational evidence:** Limited. Unlike Yang-Mills or Navier-Stokes, there is no large body of computational experiments testing the conjecture.

## Why Atlas-Suited (Honest Assessment)

This is the weakest Atlas fit among the Millennium Prize Problems:

- **Limited computational side:** The conjecture lives in algebraic geometry, where computation means symbolic algebra (Gröbner bases, sheaf cohomology) rather than numerical simulation. Math explorers could use SageMath/Macaulay2 for specific varieties, but the feedback loop is slower than Yang-Mills lattice simulations or Navier-Stokes fluid dynamics.
- **Highly abstract:** The concepts (sheaf cohomology, Chow groups, Hodge decomposition) have steep prerequisites. Explorer effectiveness depends heavily on how well the system handles abstract algebraic geometry.
- **Fewer partial results to tighten:** Unlike Yang-Mills (where existing bounds were 8× loose), the Hodge Conjecture doesn't have obvious "loose estimates" to tighten. Progress has come from structural insights, not bound improvements.
- **$1M Millennium Prize** — the prize factor is the main draw.

Where Atlas COULD contribute:
- **Map the obstruction landscape:** Systematically catalog which varieties the conjecture is known for, where it's open, and what structural properties distinguish the two.
- **Computational experiments on specific varieties:** Test the conjecture computationally for families of varieties where it hasn't been checked, using exact symbolic computation.
- **Cross-domain connections:** The Hodge Conjecture connects to motives, K-theory, and mathematical physics (mirror symmetry). Atlas's synthesis strength could find connections that specialists in one area miss.

## Verification Path

Algebraic geometry computations are exact (not numerical), so any claimed result is in principle machine-verifiable. Lean 4 formalization of algebraic geometry exists (Mathlib has schemes, sheaves, cohomology) but is less developed than the analysis/number theory libraries. Symbolic computation in SageMath/Macaulay2 provides a verification layer for specific varieties.

## Related Prior Work

- Atlas Yang-Mills mission: Millennium Prize precedent. Succeeded via estimate-tightening, which is less applicable here.
- Atlas Riemann Hypothesis mission: Millennium Prize precedent. The spectral approach had a computational side (random matrix simulations). Similar level of abstractness.

## Source

Added during Yang-Mills mission review (2026-03-28). Included for completeness as a Millennium Prize candidate.

---

## Validator Assessment

**Scores:**
| Dimension | Score | Notes |
|-----------|-------|-------|
| Breakthrough potential | 3/5 | $1M Millennium Prize, but the problem is very abstract with fewer handholds for incremental progress. Less likely to produce even modest publishable results compared to Yang-Mills or Navier-Stokes. |
| Atlas fit | 2.5/5 | Limited computational side, high abstraction level, fewer loose estimates to find. The landscape-mapping strength applies, but the estimate-tightening approach that worked for Yang-Mills doesn't transfer well. |
| Possible validation path | 3.5/5 | Algebraic computations are exact and machine-verifiable. Lean formalization possible but algebraic geometry support is immature. |
| Downside value | 3/5 | Obstruction landscape for the Hodge Conjecture would have pedagogical value. Computational verification for specific variety families is useful. But the floor is lower than Yang-Mills or Navier-Stokes. |
| Prize factor | 5/5 | $1M Millennium Prize. |

**Composite:** 3.4/5
**Verdict:** Consider — run after higher-priority missions

**Rationale:** The prize makes it worth considering, but the Atlas fit is genuinely weaker than Yang-Mills or Navier-Stokes. The lack of a rich computational verification layer means explorers spend more time on abstract reasoning and less on the compute-verify-iterate loop that Atlas excels at. Run this after exhausting better-fitted Millennium Prize targets, or if a specific computational angle emerges (e.g., a family of varieties where the conjecture is computationally testable).
