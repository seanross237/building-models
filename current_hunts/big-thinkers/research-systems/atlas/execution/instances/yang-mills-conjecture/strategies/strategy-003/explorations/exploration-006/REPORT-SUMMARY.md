# Exploration 006 Summary: Direct Hessian Bound Attempts

## Goal
Prove |λ(Hess S(Q))| ≤ 4d via three approaches: (B) D/C anti-correlation, (C) concavity, (A) per-plaquette.

## Outcome: NEGATIVE on Approach B, C and A NOT RUN

**Approach B FAILS:** The combined bound |D_min| + ||C|| ≤ 4d is false. The uniform rotation at θ=2π/3 gives |D_min|+||C|| = 16.58 > 16 = 4d. The actual eigenvalues at this config are fine (λ_max=14.82), but the triangle-inequality pathway from D+C to eigenvalue bounds cannot work.

**Approaches C and A** were coded but not executed due to time constraints.

## Verification Scorecard
- **[COMPUTED] ×5**: Anti-correlation survey (500 configs), structured config table, gradient ascent, dimension scaling, counterexample to B
- **[CONJECTURED] ×1**: Mechanism for B failure (eigenvector misalignment)
- **[VERIFIED] ×0**

## Key Takeaway
No proof pathway through |D|+||C|| ≤ 4d exists. The bound |λ(H)| ≤ 4d holds empirically but CANNOT be proved by bounding D and C norms separately — the cancellation is at the eigenvector level. The most promising remaining direction is proving concavity of λ_max(H(Q)) on SU(2)^E (Approach C), which would make the known strict local max at flat into a global max.

## Proof Gaps Identified
1. |D|+||C|| > 4d at uniform θ=2π/3 — kills the anti-correlation approach
2. Concavity of λ_max untested — this is the critical open question
3. Per-plaquette ||H_□|| ≤ 4 untested — viable if graph coloring needs ≤ d colors

## Computations for Next Steps
1. **Test concavity of λ_max along geodesics** — code ready in `code/run_all_fast.py`
2. **Test per-plaquette bound ||H_□|| ≤ 4** — code ready
3. **Explore alternative decompositions** that respect eigenvector structure
