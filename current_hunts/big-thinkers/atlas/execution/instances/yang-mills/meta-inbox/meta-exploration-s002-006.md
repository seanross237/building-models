# Meta-Learning Note: Strategy-002 Exploration 006

**Type:** Math Explorer — 4D lattice Hessian verification + adversarial search

## What Worked

1. **Direct follow-up of the unexpected finding (E005) worked perfectly.** The immediate 4D verification confirmed and strengthened the result — the slack is even larger in 4D (138× vs 45× in 3D). This is exactly the right use of a follow-up exploration: verify with one key change (dimension).

2. **Three-strategy adversarial search was thorough.** Testing aligned configs + gradient ascent + eigenvalue search covered the main attack vectors. All gave slack ≥ 176×. This is strong evidence the bound is genuinely loose.

3. **Code quality was excellent.** All code saved to files with deterministic seeds, fully reproducible. The math explorer followed all best practices from meta-lessons.

## What Didn't Work

1. **4D is significantly slower than 3D.** The 4⁴ lattice with 500 thermalization sweeps took ~8-10 minutes for β=1.0 (4 sweeps × 10 min = ~40 min total if all 4 β values were sequential). The explorer wisely ran the background computation while continuing with other work.

## Lessons

- For verification follow-ups: always include a direct comparison table between the new result and the prior result (E005 vs E006 at same β). This makes the change immediately visible.
- For adversarial searches: test at least 3 different strategies (random, gradient, structured). If all 3 give similar small H_norm, the result is robust.
- 4D lattice computations take ~3× longer than 3D. Plan accordingly.
- The unexpected finding (4D is TIGHTER than 3D) is important — it means the physical mechanism is real, not a dimensional artifact.
