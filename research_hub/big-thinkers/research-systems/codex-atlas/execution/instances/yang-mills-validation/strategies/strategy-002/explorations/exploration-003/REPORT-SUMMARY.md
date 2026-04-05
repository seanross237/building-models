# Exploration 003 Summary: Path B — Flat Connections Maximize λ_max(H_actual)

## Goal
Determine whether flat connections (Q=I) are global maximizers of λ_max(H_actual(Q)) for SU(2) Yang-Mills on L=2 lattice, to repair the proof gap.

## Outcome: **FAIL — Flat connections are NOT global maximizers at any d ≥ 2**

Two independent mechanisms disprove the hypothesis:

1. **One-hot perturbations (d ≥ 3):** Rotating a single link by angle θ INCREASES λ_max(H_actual) while λ_max(H_formula) stays exactly at dβ. At d=3: excess = 0.2% (peak at θ≈1, verified at 4 FD step sizes, 9 link/color combos). At d=4: excess = 0.018·θ² for θ ≤ 0.2, confirmed at 2 FD step sizes with near-perfect agreement.

2. **Complex multi-link configs (all d):** Random walk ascent at d=2 found λ_max = 2.052, verified at 5 FD step sizes (h = 1e-3 to 2e-5, gap = -0.0523 ± 0.0001). This is 2.6% above the flat value of 2.0.

## Verification Scorecard
- **[CHECKED]**: 4 claims (d=2 random walk excess, d=3 one-hot, d=4 one-hot, formula invariance)
- **[COMPUTED]**: 10 claims (perturbation theory, line scans, gauge orbit, D(Q) analysis)
- **[CONJECTURED]**: 2 claims (d=4 true max estimate, proof repair options)

## Key Takeaway
**The proof strategy max_Q λ_max(H_actual(Q)) = dβ is wrong.** The true maximum exceeds dβ by a small but nonzero amount (2.6% at d=2, 0.2-0.5% at d=4). The proof chain needs either a tighter bound on the true max, or an entirely different approach.

## Unexpected Findings
- λ_max(H_formula) is **exactly** invariant under all one-hot perturbations at all d — the B² formula completely ignores single-link rotations
- The ratio r = λ_max(H_actual)/λ_max(H_formula) > 1 at d≥3, contradicting E001's universal r ≤ 1 finding (E001 tested large perturbations; the violation occurs for small single-link rotations)
- Flat connections ARE strict local maxima for multi-link perturbations (negative definite second-order matrix), but NOT global maxima

## Proof Gaps Identified
- The B² formula upper bound on HessS fails for concentrated perturbations
- Need to characterize max_Q λ_max(H_actual(Q)) or use a probabilistic/concentration argument

## Computations Identified
- Find the actual global maximizer of λ_max(H_actual) at d=4 (random walk ascent at d=4 would be very expensive but decisive)
- Compute the one-hot excess coefficient analytically as a function of d (it appears to increase with d)
- Test whether the excess at d=4 is small enough that the Bakry-Émery threshold is only marginally affected
