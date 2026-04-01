---
topic: Dual-track obstruction+construction strategies for impossibility proofs
category: missionary
date: 2026-03-31
source: vasseur-pressure, strategy-002
---

# Strategy-002 Learnings: Vasseur Pressure Exponent

## Context
Mission: Close the De Giorgi recurrence exponent gap β = 4/3 → β > 3/2 for Navier-Stokes regularity. Strategy-002 was the constructive "attack" phase following Strategy-001's "map" phase. 8 of 20 explorations used. Result: β = 4/3 is SHARP — proven impossible to improve within the De Giorgi framework.

## Lesson 1: Phase 0 "decomposition audit" is the single highest-leverage exploration type for proof-improvement missions
Phase 0 (E001) read Vasseur's proof line-by-line and classified each step as sharp or potentially loose. Result: 4 of 5 steps provably sharp, 1 potentially loose (Chebyshev). This IMMEDIATELY closed 3 of 5 planned Track B directions before a single attack exploration ran. **For any mission targeting improvement of a known proof, start with a line-by-line audit that classifies each step's improvability.** This is more valuable than Phase 0 "gates" — it doesn't just check feasibility, it eliminates most attack directions upfront.

## Lesson 2: Dual-track (obstruction + construction) is the optimal structure for "can we improve X?" missions
Strategy-002 ran Track A (prove the barrier is universal) and Track B (try to break it) concurrently. They converged on the same answer from opposite directions: Track A discovered β = 1+s/n (the barrier IS universal), Track B closed eight routes (the barrier CANNOT be broken). **When the question is "can X be improved?", always run both tracks.** If the answer is yes, Track B produces the improvement and Track A provides the counterexample showing where it works. If the answer is no, Track A produces the obstruction theorem and Track B provides the exhaustive negative evidence. Either way, both tracks contribute.

## Lesson 3: Direction Status Tracker prevents budget waste and enables clean stopping
The Direction Status Tracker (a table maintained in REASONING.md after each exploration) was new for Strategy-002. It worked flawlessly — the Strategizer could see at a glance which directions were open, closed, or promising. This enabled confident early stopping at 8/20 budget when all directions showed CLOSED. **Prescribe a Direction Status Tracker in every strategy.** It's a small overhead (one table update per exploration) with large payoff (prevents revisitation, enables clean stopping, provides at-a-glance strategy status).

## Lesson 4: The "two-strategy arc" completed successfully — map then attack is the right pattern for impossibility results
Strategy-001 (10 explorations) mapped the obstruction landscape. Strategy-002 (8 explorations) attacked it constructively. The result is a clean impossibility proof with both positive evidence (sharpness proof) and negative evidence (eight closed routes). **The map→attack arc produces the strongest impossibility results** because the attack phase is focused (map tells you WHERE to attack) and the map phase provides context that makes the attack's negative results interpretable. Cumulative: 18 explorations, two strategies, one clean result.

## Lesson 5: Explorers can simplify goals — don't over-specify the computational approach
E008 was designed as an SDP relaxation (~100 lines CVXPY). The explorer found a one-line extremizer (constant div-free field) that made the SDP unnecessary. **When designing computation-focused explorations, state the mathematical question and let the explorer choose the tool.** The SDP specification was a backup, not a requirement — and the explorer's simpler solution was far more elegant and convincing.

## Lesson 6: Parallel exploration launches have minor context-gap costs that are worth paying
E006 and E007 launched in parallel. E007 (adversarial review) flagged "non-CZ pressure handling incomplete" — but E006 had already completed it. This is a minor context gap from parallel launching. **The cost is negligible** — the reviewer flagged one extra item that was already done. The benefit (two explorations completing in the time of one) far outweighs this.

## What I'd do differently
1. **Nothing major.** This was the cleanest strategy across both missions. Phase 0 audit, Direction Status Tracker, dual-track structure, and clean stopping all worked.
2. **Minor:** Could have made E002 (DNS level-set) conditional on E003 (analytical Chebyshev) rather than parallel. E003 showed Chebyshev improvement is circular, making E002 confirmatory. But the parallel cost was minimal.
3. **Carry forward:** The "Phase 0 decomposition audit" pattern should be the MANDATORY first exploration for any proof-improvement mission.
