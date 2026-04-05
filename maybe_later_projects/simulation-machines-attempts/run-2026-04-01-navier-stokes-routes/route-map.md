# Route Map

## Cycle 1 Ranking

| Route family | Score | Expected value | Information gain | Option value | Cost | Risk | Status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| criticality-and-concentration | 0.82 | High | High | High | Medium | Medium | Chosen |
| partial-regularity-and-epsilon-bootstrapping | 0.74 | High | High | Medium | Low | Low | Backup |
| frequency-cascade-and-structure-rules | 0.58 | Medium | Medium | Medium | Medium | Medium | Alive |
| barrier-and-morrey-control | 0.51 | Medium | Medium | Low | Low | Medium | Alive |

## Cycle 2 Ranking

| Route family | Score | Change | Reason |
| --- | ---: | ---: | --- |
| criticality-and-concentration | 0.77 | -0.05 | High leverage, but too broad under budget |
| partial-regularity-and-epsilon-bootstrapping | 0.79 | +0.05 | Sharper checkpoints, easier to test, lower execution risk |
| frequency-cascade-and-structure-rules | 0.56 | -0.02 | Still plausible, but too many moving parts |
| barrier-and-morrey-control | 0.49 | -0.02 | Useful as a check, not the main line |

## Cycle 3 Ranking

| Route family | Score | Final status | Rationale |
| --- | ---: | --- | --- |
| partial-regularity-and-epsilon-bootstrapping | 0.84 | Favored | Best balance of clarity, pruning power, and checkpointed progress |
| criticality-and-concentration | 0.76 | Secondary | Best long-horizon route, but higher search depth needed |
| frequency-cascade-and-structure-rules | 0.55 | Pruned | Too speculative for the remaining budget |
| barrier-and-morrey-control | 0.47 | Pruned | Lower leverage than the other two families |

## Pruning Notes

- `frequency-cascade-and-structure-rules` was pruned because it stayed informative but did not improve the next-step decision quality enough.
- `barrier-and-morrey-control` was kept alive briefly for cross-checking, then pruned because it did not change the frontier meaningfully.
- `criticality-and-concentration` remains important as a long-horizon research direction, but it lost the short-run contest because it was too diffuse.
