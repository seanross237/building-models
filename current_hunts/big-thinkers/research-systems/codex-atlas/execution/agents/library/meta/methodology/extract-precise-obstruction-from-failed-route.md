---
topic: Extract precise obstruction when a route fails — it points to next direction
confidence: confirmed
date: 2026-03-30
source: "vasseur-pressure s2-meta-004"
---

## Lesson

**When a promising route fails, always extract the PRECISE obstruction — not just "it doesn't work."** The precise point of failure immediately suggests the next direction by identifying what would need to be different for the route to succeed.

## Evidence

Vasseur-pressure Strategy-002, Exploration 004: The compensated compactness / commutator route failed at three independent levels. But the PRECISE identification of each obstruction generated specific next directions:

1. **"Truncation kills div-free at high frequencies"** → suggests frequency-localized De Giorgi (treat low and high modes differently in pressure decomposition)
2. **"Commutator remainder dominates because div(u^{above}) != 0"** → suggests constructing a div-free approximation to u^{above} or finding a different splitting
3. **"CRW is vacuous for bounded multipliers"** → suggests finding a formulation where the multiplier is unbounded-but-BMO (a concrete mathematical target)

If the exploration had only reported "compensated compactness doesn't work," none of these three leads would have emerged.

## Protocol

When closing a route:
1. **Identify all independent obstruction layers** (not just the first barrier encountered)
2. **For each layer, state the precise mathematical condition that fails** (e.g., "div(u^{below}) = O(||nabla u||_{L^2}), not O(epsilon)" rather than "the field isn't divergence-free")
3. **For each obstruction, state what property of the problem would need to change** for the obstruction to disappear (e.g., "scalar active quantity" or "linear nonlinearity")
4. **Rank the resulting leads** by how achievable the required change is

## When to Apply

- After any exploration that produces a negative result on a specific mathematical approach
- Especially when the approach had a clear analogous success (SQG commutator → NS commutator attempt)
- Before declaring a direction "closed" in the strategizer report

## Relationship to Other Lessons

Distinct from `decisive-negative-pivot` (which handles the decision to pivot after a negative result; this handles extracting maximal information FROM the negative result before pivoting). Distinct from `useful-failure-extracts-secondary-results` (which captures secondary findings that happen to emerge; this is about deliberately extracting directional information from the obstruction itself). Complementary to `test-improvability-before-pursuing-variations` (which tests whether a target is attackable; this handles the aftermath when an attack fails).
