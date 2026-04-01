---
topic: Allow explorers to find analytic extremizers instead of over-specifying computational approach
date: 2026-03-30
source: "vasseur-pressure s2-meta-exploration-008"
---

## Lesson

When designing optimization-based explorations (SDP, LP, numerical optimization), always allow the explorer to find analytic extremizers. The computational approach should be the fallback when no closed-form solution exists — not the default.

## Evidence

S2-E008 goal described an SDP relaxation (~100 lines CVXPY) to determine whether the Chebyshev bound could be improved under div-free and energy constraints. The explorer realized that the constant vector field u = (c, 0, 0) is a one-line extremizer that makes the entire SDP unnecessary. The proof is elementary (ratio -> 1 as c -> lambda from above), yet it is the definitive answer.

## Protocol

When writing goals for optimization-based explorations:
1. State the mathematical question clearly (what quantity to optimize, what constraints)
2. Specify the computational approach as ONE possible tool, not the required method
3. Explicitly say: "If you can find an analytic extremizer or closed-form answer, do that instead"
4. Reserve the computation for cases where the analytic approach fails or is unclear

## Why This Matters

- Analytic extremizers are more convincing (exact proof vs. numerical evidence)
- They are faster to find when they exist
- They often reveal WHY the bound is tight (mechanism), not just THAT it is tight
- The constant field answer simultaneously reveals that div-free constrains direction not magnitude — a structural insight no SDP would produce
- S2-E008: entire strategy's eight-exploration sharpness program reduces to elementary observations: (1) 4 chain steps, (2) each individually tight, (3) constant div-free field extremizes three simultaneously

## When Computation IS Needed

Sometimes the extremizer is genuinely non-trivial (fractal structure, infinite-dimensional, parameter-dependent). In those cases, SDP/LP/numerical optimization is the right tool. The lesson is not "never compute" but "don't over-specify computation when the answer might be simple."

## Distinct From

- **allow-explorer-synthesis.md** — about leaving CONCLUSIONS open, not METHODS open
- **check-bypass-not-just-improve-bottleneck.md** — about whether to use a framework at all, not about computational vs. analytic within a framework
- **specify-computation-parameters.md** — about providing exact parameters when computation IS needed
