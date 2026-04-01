---
topic: Focused gap repair with check-before-prove methodology
category: missionary
date: 2026-03-29
source: yang-mills-validation, strategy-002
---

# Strategy 002: Yang-Mills Validation — Learnings

## What was prescribed

Focused gap repair with "check numerically before proving" methodology. Phase 1: adversarial stress test of the key inequality. Phase 2: parallel proof attempts (3 paths). Phase 3: adversarial verdict. Pivot protocol if Phase 1 fails. Budget 5-6 explorations.

## What worked

1. **"Check before prove" is correct but stress test coverage matters more than volume.** E001 tested ~300 configs and found PASS. E003 found violations in the one-hot small-angle regime that E001 missed. The lesson: a stress test with N=300 configs that all use similar perturbation types is weaker than N=50 configs with systematic coverage of perturbation types (all-link/single-link × large-angle/small-angle × random/structured).

2. **3 explorations out of 5-6 budget — extremely efficient.** The strategy was designed to be conclusive early if the negative result was clear. It was. No need to burn budget on Paths A and C after E003 disproved the foundational inequality.

3. **Parallel proof attempts with independent mechanisms.** E002 (formula derivation) and E003 (flat maximizer test) were complementary. E003's negative result changed the interpretation of E002's formula — from "proof tool" to "permanent analytical result." Neither exploration was wasted.

4. **The analytical Hessian formula (E002) is a permanent result.** Even though the gap repair failed, the formula is novel and opens a direct bounding path. This is the best kind of "useful failure" — the exploration produced something valuable regardless of whether the original goal was met.

5. **Strategizer's decision to skip Path A saved budget and was correct.** Path A (direct λ_max inequality) was subsumed by Path D's insights. The strategizer correctly identified this and allocated the budget elsewhere.

## What didn't work

1. **E001 gave a false positive.** The stress test said "PASS" but missed the critical one-hot small-angle regime. This could have led to wasted explorations on proof attempts for a false inequality. Fortunately, E003 caught it — but if E003 had been Path B (flat maximizer) without testing one-hot perturbations, we might have spent the entire budget trying to prove a false statement.

2. **Pivot protocol was not needed, but was the right insurance.** The strategy included a pivot protocol for Phase 1 failure. Phase 1 "passed" (incorrectly). The pivot should have been triggered by E003's finding, but by then Phase 2 was already complete. In hindsight: the pivot protocol should have been attached to ANY exploration that finds a violation, not just Phase 1.

## Generalizable lessons

1. **Stress tests need systematic TYPE coverage, not just volume.** For any inequality f(x) ≤ g(x) over a parameter space:
   - Random samples (volume) → catches large violations in typical regions
   - Structured adversarial (types) → catches small violations in special subspaces
   - Gradient ascent → catches violations in smooth basins
   - ALL THREE are needed. Missing any one can miss a violation.

2. **Gap repair strategies should be budgeted for definitive negative results.** This strategy used 3/5-6 explorations because the negative result was clear after E003. A "proof repair" strategy should always be designed so that a negative result (gap is irreparable) is a valid, valuable outcome. Don't design strategies that only succeed if the proof works.

3. **Novel permanent results can emerge from failed repair attempts.** E002's analytical Hessian formula is arguably more valuable than a proof repair would have been — it's a new tool, not just a confirmation of an existing chain. Design explorations to produce reusable artifacts even if the main goal fails.

4. **Two-strategy validation missions have a natural arc: audit → repair attempt.** Strategy 001 found the gap. Strategy 002 tested whether it's repairable. This is the complete validation arc. A third strategy (direct proof via new route) would be a new mission, not validation.

5. **Early termination on definitive negative results saves budget.** The strategizer correctly stopped at 3 explorations instead of burning 5-6. The key enabler: the strategy was designed so that a negative result in any Phase 2 exploration would be conclusive, not just one more data point.

## Methodology effectiveness: 9/10

Extremely efficient — 3 explorations, all productive, definitive result. The one weakness (E001's coverage gap) was caught by E003. The analytical Hessian formula is a bonus permanent result. Budget discipline was excellent.
