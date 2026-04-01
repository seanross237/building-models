# Exploration 001: Classical Eigenvalue Concavity/Convexity Theorems

## Goal

Survey the mathematical literature on concavity and convexity of eigenvalue functions of matrix-valued maps. Produce a structured catalog of the main results, their conditions, and their applicability to the following motivating problem:

**Motivating problem:** Given a smooth Hermitian-matrix-valued function H(Q) defined on SU(N)^E (a product of compact Lie groups), determine conditions under which λ_max(H(Q)) is concave (or convex) as a function of Q. Specifically, we want to know when the maximum eigenvalue of a matrix that depends on group elements achieves its global max at a known point.

## Specific Theorems to Cover

1. **Davis-Lewis theorem** — concavity/convexity of spectral functions. What exactly does it say, what are its hypotheses, and when does it apply to functions on matrix spaces vs. functions on groups?
2. **Ando's theorem** — related convexity results for matrix functions.
3. **Löwner's theorem** — operator monotone functions and their connection to eigenvalue convexity.
4. **Matrix convexity** — when is a matrix-valued function "matrix convex" and what does this imply about eigenvalue concavity?
5. **Fan's inequality and Weyl's inequality** — eigenvalue perturbation bounds.
6. **Any other relevant results** you find — especially results from the last 10 years (2016-2026).

## For Each Result, Report

- Precise statement (hypotheses and conclusion)
- The domain: does it apply to functions on vector spaces, matrix spaces, manifolds, or groups?
- Whether it gives concavity of λ_max, convexity of λ_min, or something else
- Key limitations — what prevents direct application to a function on SU(N)^E?

## Critical Context

We already know that **global geodesic concavity of λ_max fails** for our specific problem. Numerical computation found F''(Q, W) > 0 at certain Q ≠ I, meaning λ_max(H(Q)) is not globally geodesically concave on SU(2)^E. However, λ_max still achieves its global max at Q = I (the flat connection). So we need techniques beyond "prove full concavity."

This means: pay special attention to:
- **Conditional concavity** — concavity under structural assumptions on H(Q) that might fail at some Q
- **Local concavity + trapping** — results that combine local concavity near a critical point with other structure to get global optimality
- **Restricted concavity** — concavity along certain submanifolds or paths
- **Concavity of restricted spectral functions** — e.g., concavity of spectral radius vs. individual eigenvalue

## Success Criteria

- A clear catalog of ≥4 major theorems with precise statements
- For each, an honest assessment of whether it applies to functions on compact Lie groups
- Identification of the "closest applicable theorem" — the one most likely to help with the motivating problem
- Forward-looking question answered: has anyone applied these theorems to lattice gauge theory or physics Hessians?

## Failure Criteria

- Vague summaries without precise hypotheses
- Missing Davis-Lewis or Ando entirely
- Claiming a theorem applies without checking its domain assumptions

## Output

Write REPORT.md and REPORT-SUMMARY.md in your exploration directory.
