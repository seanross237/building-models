# Decision Memo - beyond-de-giorgi / decision-002

## Decision

`replan`

## Mission-Control Verdict

The active chain should not proceed. Step `step-001` was explicitly designed to front-load the Tao gate and kill the branch quickly if no NS-specific coefficient-shrinking mechanism survived the exact far-field reconstruction. That is what happened.

This is a branch-level negative result, not a mission-level terminal result. The step pinned down the live far-field pairing, showed that constants were already removed while affine-and-higher harmonic content still survives, and concluded that the remaining obstruction is coefficient-side. Under that reconstruction, the tested harmonic-tail gains are either cosmetic or Tao-compatible.

## Why `proceed` Is Wrong

Proceeding would ignore the chain's own gatekeeping standard. The latest step result says:

- the exact live obstruction has now been reconstructed sharply enough to evaluate the branch;
- the kill condition fired honestly;
- no screened NS-specific ingredient earned an estimate-level reduction of `C_far ~ ||u||_{L^2}^2 / r_k^3`;
- the step recommendation is to downgrade this route to the negative-result track.

That means the next ordered step of the current chain is no longer the best next mission move.

## Why `terminate` Is Wrong

The broader mission remains open. A negative result on the harmonic-tail pressure loophole does not answer the higher-level question of which NS-specific structure, if any, might still bypass the De Giorgi barrier outside this branch.

## Required Next Controller Move

Mission control should compare branches again rather than continue Chain 01 in order. The planning record still leaves refined Chain 02 (estimate-first algebraic reformulation testing) and refined Chain 03 (geometry-first obstruction testing) as live alternatives. Any pressure-tensor follow-up should be treated as a newly compared branch, not as continuation of the invalidated harmonic-tail chain.
