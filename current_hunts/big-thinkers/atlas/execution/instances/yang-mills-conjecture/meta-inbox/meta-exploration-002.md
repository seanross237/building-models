# Meta-Learning: Exploration 002 (Per-Plaquette Contribution Structure)

## What worked well
- Staged computation approach (compute → group → test groups → algebraic analysis) was very effective
- The cube-face grouping discovery came from systematic testing of 4 different grouping types
- 160K numerical tests gave high confidence in the cube-face inequality
- The algebraic formula for cross-links=I was a concrete, verifiable result

## What didn't work well
- Goal could have been more specific about which groupings to try first — the edge-pairing and link-star were less useful
- Explorer didn't attempt the generalization to arbitrary cross-links (ran out of budget)

## Lessons
- For combinatorial/grouping problems, specify "test at least N grouping types including vertex-star, edge-pair, and face groups"
- The active/inactive split was already partially known — preloading this would have saved time
- Adversarial gradient ascent targeting specific sub-sums (not just the global sum) was a smart approach by the explorer
- The proof for cross-links=I gives a clear template — future explorations should try to extend it
