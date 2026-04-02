## Objective

Build a `solver.py` in this directory that reads the AHC032 sample input from stdin and prints a valid sequence of at most `81` stamp operations. The output should maximize the measured sample score under `score_sample.py`. I also need to produce `final-output.md` with the measured result and run the scorer on the final solver.

## Constraints

- Work only in this run directory.
- Do not inspect or modify sibling run folders.
- Output format must be exactly:
  - first line: number of operations `L`
  - next `L` lines: `m p q`
- Valid ranges:
  - `0 <= L <= 81`
  - `0 <= m < 20`
  - `0 <= p, q <= 6`
- Scoring is the sum over all final board cells of `(value mod 998244353)`.
- Stamp applications commute, so only the multiset of operations matters for score, but the solver still must print a concrete sequence.

## Key observations

- Every stamp entry in the sample is nonnegative and appears large, often close to the modulus.
- For a single cell, adding a positive value is good only until the residue crosses `998244353`; after that the marginal effect becomes negative by roughly one modulus.
- Because each operation affects a `3 x 3` area, the optimization is coupled across cells and cannot be solved greedily per cell without approximation.
- This run scores only one fixed sample, so a solver tailored to the observed instance is acceptable as long as it reads stdin and emits valid operations.

## Candidate approaches

### 1. Greedy hill climbing on current board state

At each step, evaluate every possible operation `(stamp, p, q)` on the current residues and choose the one with the highest immediate score delta. Stop when no positive delta exists or when `81` operations have been used.

Pros:
- Simple and fast.
- Easy to validate and iterate.
- Uses the true modular marginal gain at the current state.

Cons:
- Myopic: a slightly bad move may unlock a much better later sequence.
- Can plateau early.

### 2. Beam search over partial sequences

Keep the top `B` states after each depth, using exact score as the ranking metric and deduplicating equal operation count / board states if practical.

Pros:
- Can escape some greedy traps.
- Still manageable because there are only `980` candidate operations per step.

Cons:
- State space is large.
- Pure Python may become slow if board copies are not handled carefully.

### 3. Greedy construction plus local improvement

Start with greedy hill climbing, then try:
- deleting one operation,
- replacing one operation with another,
- short random perturbations followed by greedy refill.

Pros:
- Usually stronger than plain greedy.
- Keeps implementation complexity moderate.

Cons:
- Needs careful bookkeeping to stay fast.
- Improvement quality depends on neighborhood design.

### 4. Randomized search / simulated annealing on operation counts

Represent a length-`<=81` multiset of operations and do score-guided random mutations.

Pros:
- Can sometimes find non-myopic solutions.
- Good fit for a fixed sample if enough iterations fit in time.

Cons:
- More tuning risk.
- Harder to make robust quickly than greedy + repair.

## First approach

I will start with **greedy hill climbing on exact marginal deltas**, then add **light local improvement** only if the greedy baseline leaves obvious headroom.

Reason:

- It is the lowest-risk path to a valid solver quickly.
- The action space is only `20 * 7 * 7 = 980` operations, so evaluating all moves each step is cheap enough.
- Since only the sample score matters here, even a moderately strong greedy baseline may already be good.

## Planned experiment sequence

1. Implement a scoring core that:
   - parses stdin,
   - stores the `9 x 9` board and `20` stamps,
   - precomputes the affected cells for each candidate operation,
   - computes exact score deltas from current residues.

2. Run **Experiment A**:
   - plain greedy selection for up to `81` moves,
   - stop when best delta is nonpositive,
   - measure sample score.

3. Run **Experiment B** if greedy stops early or looks weak:
   - force full `81` moves and compare with early-stop greedy.
   - This checks whether slightly negative intermediate moves can still pay off later.

4. Run **Experiment C**:
   - seed with greedy result,
   - attempt single-operation replacement:
     - remove one chosen move,
     - greedily refill remaining slots from the resulting board.
   - Keep any improvement.

5. Run **Experiment D** if time remains:
   - random restart tie-breaking among near-best greedy moves,
   - keep the best measured sequence.

6. Freeze the best solver behavior, rerun `score_sample.py`, and write `final-output.md`.

## Expected failure modes and plateaus

- **Greedy zero trap**: all immediate deltas become nonpositive while a two-step combination would help.
- **Edge overfitting**: the algorithm may overuse stamps that help some cells while repeatedly wrapping already-saturated cells.
- **Replacement search cost**: local improvement may become slow if every candidate recomputes too much state.
- **Tie sensitivity**: many moves may have similar deltas; arbitrary tie-breaking can change the final score materially.
- **No-benefit late stage**: after residues approach the modulus, most extra moves may become harmful, so using fewer than `81` operations may actually be correct.

## Decision rule during execution

- Prefer the simplest method that yields a strong valid score.
- Only add another layer of search if the measured improvement justifies the added complexity.
- Keep the final solver readable and self-contained.
