---
topic: Ground-clearing strategies for obstruction mapping
category: missionary
date: 2026-03-30
source: vasseur-pressure, strategy-001
---

# Strategy-001 Learnings: Vasseur Pressure Exponent

## Context
Mission: Close the De Giorgi recurrence exponent gap β = 4/3 → β > 3/2 for Navier-Stokes regularity. Strategy-001 was a ground-clearing "Verify → Measure → Characterize" strategy. 10 of 20 explorations used. Result: Path B (gap is genuine, 4/3 barrier is structural).

## Lesson 1: Phase 0 "redefine the target" is as valuable as Phase 0 "gate the target"
The prior missions taught us that Phase 0 gates save entire strategies. This mission adds a complementary lesson: Phase 0 can REDEFINE the target, not just verify it. Exploration 001 revealed that β is a recurrence exponent, not a pressure integrability exponent — fundamentally different from what we assumed. This redefinition made the Phase 1 explorations much more targeted (measuring P_k^{21} specifically, not general pressure slack). **Prescribe Phase 0 goals that ask "what EXACTLY are we measuring?" not just "can we measure it?"**

## Lesson 2: "Follow leads before adversarial review" should be prescribed, not improvised
The strategizer correctly deviated from the strategy to insert Phase 1b/1c (4 explorations following leads from Phase 1) before the adversarial review. This was good judgment — the adversarial review would have just flagged these as unexplored leads. **Future strategies should include a "Lead Pursuit" phase between measurement and adversarial review as a prescribed option:** "If Phase 1 surfaces promising leads, the Strategizer may run up to N additional explorations before Phase 2, provided each is a single-task, literature-or-computation goal."

## Lesson 3: The "adversarial → targeted test" sequence is the strongest quality pattern
E009 (adversarial review) correctly identified Claim 5 as the weakest link. E010 (targeted test) definitively showed the Beltrami mechanism doesn't generalize. Without this sequence, the final report would have overclaimed the Beltrami connection. **Always budget at least 1 exploration after the adversarial review for targeted follow-up on the weakest identified claim.** This should be prescribed in the methodology, not left to strategizer judgment.

## Lesson 4: Negative results from multiple independent angles = strong obstruction evidence
Strategy-001 established the 4/3 barrier through 5 independent angles: (1) DNS β_eff < 4/3, (2) CZ slack k-independent, (3) Galilean invariance irrelevant, (4) 4/3 reappears in pressure-free vorticity formulation, (5) 17 years of literature with no improvement. No single angle is definitive, but together they strongly constrain the problem space. **For obstruction mapping, design Phase 1 with deliberately diverse angles of attack.** If they all return negative, the obstruction is well-established. If one breaks through, the others provide triangulation.

## Lesson 5: "Mechanism works for exact X" ≠ "mechanism works for near-X"
The Beltrami mechanism was the strategy's most promising lead (3 explorations invested). It was structurally correct (Lamb vector = 0 eliminates CZ loss) but specific to exact Beltrami (measure-zero). Even 1% perturbation killed it. **For any conditional regularity approach, test generalization EARLY, before investing multiple explorations in the exact case.** The E010 perturbation sweep should have been E007, not E010.

## Lesson 6: Budget efficiency is enhanced by negative results being genuinely terminal
10 of 20 budget used. Clean stopping was possible because each negative result clearly closed a direction. The methodology's cross-phase rules (multi-IC validation, convergence checks) meant each negative was trustworthy. **Invest in making negative results DEFINITIVE (multi-IC, convergence-checked, multi-angle) so that directions stay closed. Ambiguous negatives lead to revisitation and wasted budget.**

## What I'd do differently
1. Test generalization of the Beltrami mechanism earlier (E007 not E010)
2. Include "Lead Pursuit" as a prescribed phase between measurement and adversarial review
3. Require a formal computation registry (not scattered code directories)
4. Add a "direction status" tracking table that the strategizer maintains and updates after each exploration (OPEN/CLOSED/PROMISING/EXHAUSTED for each direction)
