# Execution Plan for `ahc032-plan-exec-001`

## Objective and constraints summary

- Build `solver.py` in this run folder only.
- Read the AHC032 instance from stdin and print a valid sequence of at most `K = 81` stamp operations.
- Maximize the final score `sum(board[i][j] mod 998244353)` after all operations.
- Each action chooses one of `20` stamps and one top-left placement on the `7 x 7` placement grid, so there are `20 * 7 * 7 = 980` possible actions at every step.
- Output may stop early; `L` can be any integer in `[0, 81]`.
- Do not inspect sibling run folders. Do not write anything beyond this run folder.
- For this planning stage, do not write `solver.py` yet and do not use the scorer as the main solving mechanism.

## Sample-specific observations worth using

- Initial sample score is `42,088,674,043`.
- A pure best-immediate-gain greedy simulation reaches `62,599,942,872` in `18` operations, then no single remaining move has positive marginal gain.
- That greedy stall is not a true local optimum: from the stalled state, the best two-step sequence still gains about `951,162,318`.
- A “repeat one fixed action many times” strategy is much weaker on this sample than adaptive search.

These observations strongly suggest:

- the action evaluator should be based on exact marginal score change over the 9 affected cells;
- pure greedy is a useful baseline but should not be the final method;
- the primary solver should include short lookahead or beam search so it can cross temporarily negative intermediate states.

## Candidate approaches

### 1. Pure greedy by marginal gain

- At each step, evaluate all 980 actions.
- Apply the action with the best positive immediate delta.
- Stop when the best delta is non-positive.

Pros:

- Very easy to implement.
- Likely valid and decent immediately.
- Cheap enough because each action touches only 9 cells.

Cons:

- Confirmed to stall early on this sample.
- Cannot take a slightly negative move to unlock a larger later gain.

### 2. Short-horizon beam search over action sequences

- Keep the best `B` states after each depth expansion.
- Score a partial state by exact current score plus a rollout estimate.
- Allow negative immediate moves if the short sequence total is strong.

Pros:

- Fits the sample behavior.
- Still tractable because the state is only `9 x 9` and branching can be pruned hard.
- Natural extension of greedy.

Cons:

- Needs careful pruning to stay within the 20 second limit.
- State copying and duplicate handling matter.

### 3. Greedy plus tail repair / limited local search

- First build a greedy sequence.
- Then repeatedly remove the last `r` moves or a low-value window and re-search that segment using beam / exhaustive depth-2 or depth-3 search.

Pros:

- Lower implementation risk than a full beam from the start.
- Targets the exact place where greedy usually fails.

Cons:

- Can miss improvements that require changing early choices.
- More of a patch than a primary search method.

### 4. Multi-start seeded greedy

- Try several strong first moves or first move pairs.
- Complete each branch greedily or with shallow lookahead.

Pros:

- Simple diversity.
- Can recover from a bad first greedy tie-break.

Cons:

- Weaker than maintaining a real beam throughout the sequence.

## Chosen primary approach

Use a beam-style constructive search with exact action deltas and greedy rollout evaluation.

Concrete shape:

- Represent the board as residues modulo `998244353`; raw large integers are unnecessary.
- Precompute the 980 actions as lists of 9 `(r, c, add)` triples.
- For any state, compute an action’s exact marginal gain as:
  `sum(((cell + add) % MOD) - cell for the 9 touched cells)`.
- Search in stages:
  - keep a beam of the best current states;
  - expand each state only by its top `C` actions by immediate delta;
  - evaluate each child by `current_score + immediate_delta + rollout_bonus`;
  - rollout bonus should be a short greedy completion from that child for a few steps or until no positive move remains.

Why this is the primary approach:

- It preserves the strength of greedy on this sample.
- It explicitly addresses the observed need for positive multi-step combinations after greedy stalls.
- It stays simple enough to implement in one file without overengineering.

## Exact experiment order

1. Build the core primitives.
   - Parser for stdin.
   - Precomputed action list of 980 entries.
   - `apply(action, board)` and `delta(action, board)` helpers.
   - Exact score tracker updated incrementally from deltas.

2. Implement a zero-risk greedy baseline first.
   - Repeatedly take the best positive immediate delta.
   - Stop when best delta `<= 0`.
   - Record operation count, total score, and per-step gain history.

3. Add a depth-2 lookahead baseline before full beam.
   - For the current state, keep the top `C1` first moves by immediate delta.
   - For each, compute the best second move.
   - If the best pair gain is positive, play the first move of that pair.
   - Compare against pure greedy on score and op count.

4. Upgrade to beam search if depth-2 is better or comparable.
   - Suggested first settings:
     - beam width `B = 8`
     - child expansion per state `C = 24`
     - rollout depth `R = 4`
   - Score each child as:
     - exact score after the child
     - plus greedy rollout gains for up to `R` extra moves
   - Deduplicate states by the 81 board residues plus step count if needed.

5. Sweep a small parameter grid, not a huge one.
   - Try `B in {4, 8, 16}`.
   - Try `C in {16, 24, 40}`.
   - Try `R in {2, 4, 6}`.
   - Keep the best-scoring valid sequence found under the runtime budget.

6. If beam is too slow, switch to greedy plus repair.
   - Start from the greedy sequence.
   - Re-optimize the final 4 to 8 moves using depth-2/depth-3 beam on that suffix.
   - Then try re-optimizing one or two earlier windows with the lowest cumulative gains.

7. Only after the search logic is stable, wrap it in final output formatting.
   - Print `L`.
   - Print each `m p q` line.
   - Ensure `0 <= L <= 81` and all placements remain in `[0, 6]`.

## Metrics to watch

- Final sample score.
- Validity of output.
- Runtime margin versus the scorer timeout of 20 seconds.
- Number of operations used.
- Best immediate delta available at each step.
- Best two-step or rollout-estimated gain when immediate best delta becomes non-positive.
- Beam diversity:
  - do states collapse to near-identical boards too early?
- Marginal gain decay:
  - if the last several accepted moves contribute very little or negative net value under rollout, stop earlier.

## What to do if the first idea stalls

If pure greedy stalls:

- move immediately to depth-2 lookahead, because this sample already shows a positive two-step escape after greedy’s stopping point.

If depth-2 still underperforms:

- keep the same exact delta machinery and add beam width rather than inventing a new heuristic;
- allow mildly negative first steps when pair or rollout value is positive.

If beam is too slow:

- reduce copying cost by storing board residues in a flat 81-element list;
- prune each state to only the top immediate-delta actions before expansion;
- shorten rollout depth before shrinking beam width;
- fall back to greedy plus suffix repair instead of abandoning lookahead entirely.

If all constructive search variants plateau:

- add multi-start diversity by forcing the first move from the top 10 to 20 opening actions, then run the chosen search from each seed;
- keep the best resulting sequence.

## Implementation notes for the next agent

- Keep the code small and explicit; this problem size does not require exotic optimization.
- Because only 9 cells change per move, exact delta recomputation is cheap enough to favor correctness over clever caching at first.
- Preserve the best full action list seen so far at all times so the solver can always emit a valid answer, even if a later experiment branch fails.
