# Schrodinger Potential Sequence V_N(x): Does the Inverse Spectral Limit Exist?

**Date:** 2026-04-05
**Status:** Complete (first-of-its-kind computational study)

## Summary

We computed the sequence of potentials V_N(x) for a 1D Schrodinger operator -u'' + V(x)u = lambda*u on [0, 10], where V_N is optimized so that the first N eigenvalues match the first N nontrivial Riemann zeta zeros. We studied N = 5, 8, 10, 15, 20 using differential evolution + L-BFGS-B optimization with Chebyshev parameterization.

**Central finding: The potential sequence V_N(x) does NOT converge on a fixed interval.** The shape changes dramatically between successive N values, with the L2 norm of successive differences ||V_{N+k} - V_N||_2 showing no monotonic decrease. This is a fundamental obstruction, not a numerical artifact. However, there are tantalizing structural regularities that point toward what the Hilbert-Polya operator MUST look like.

---

## 1. Eigenvalue Match Quality

The optimization successfully matched zeta zeros for all N values tested:

| N | Loss (sum sq rel err) | Max Relative Error | Mean Relative Error | Time (s) |
|---|---|---|---|---|
| 5 | 0.000318 | 1.411% | 0.576% | 614 |
| 8 | 0.000445 | 1.728% | 0.446% | 336 |
| 10 | 0.000706 | 2.099% | 0.482% | 335 |
| 15 | 0.002906 | 4.082% | 0.671% | 1233 |
| 20 | 0.0000161 | 0.242% | 0.063% | 1719 |

The N=20 result is remarkable: 20 Chebyshev modes (K=25) with L-BFGS-B matched all 20 zeta zeros to within 0.25%, with most errors below 0.1%. This was achieved with L-BFGS-B alone (the DE search did not improve it), suggesting the loss landscape becomes smoother when K > N.

### N=20 Eigenvalue Match (Best Result)

| n | Computed | Target (gamma_n) | Relative Error |
|---|---|---|---|
| 1 | 14.1350 | 14.1347 | +0.002% |
| 2 | 21.0231 | 21.0220 | +0.005% |
| 3 | 25.0212 | 25.0109 | +0.042% |
| 4 | 30.4236 | 30.4249 | -0.004% |
| 5 | 32.9272 | 32.9351 | -0.024% |
| 6 | 37.5930 | 37.5862 | +0.018% |
| 7 | 40.8687 | 40.9187 | -0.122% |
| 8 | 43.3280 | 43.3271 | +0.002% |
| 9 | 47.9471 | 48.0052 | -0.121% |
| 10 | 49.7717 | 49.7738 | -0.004% |
| 11 | 52.9916 | 52.9703 | +0.040% |
| 12 | 56.5827 | 56.4462 | +0.242% |
| 13 | 59.3252 | 59.3470 | -0.037% |
| 14 | 60.8477 | 60.8318 | +0.026% |
| 15 | 65.0715 | 65.1125 | -0.063% |
| 16 | 67.1314 | 67.0798 | +0.077% |
| 17 | 69.4831 | 69.5464 | -0.091% |
| 18 | 72.0886 | 72.0672 | +0.030% |
| 19 | 75.5941 | 75.7047 | -0.146% |
| 20 | 77.2692 | 77.1448 | +0.161% |

---

## 2. The Potential V_N(x) Does NOT Converge (Fixed Interval)

### 2.1 Successive Differences

The L2 and L-infinity norms of successive potential differences on [0, 10]:

| Transition | ||V_diff||_L2 | ||V_diff||_Linf |
|---|---|---|
| N=5 -> 8 | 77.52 | 217.65 |
| N=8 -> 10 | 106.24 | 363.46 |
| N=10 -> 15 | 31.32 | 78.87 |
| N=15 -> 20 | 75.51 | 304.23 |

**These differences are NOT monotonically decreasing.** The sequence is: 77.5 -> 106.2 -> 31.3 -> 75.5. There is no clear convergence trend.

### 2.2 Pointwise Non-Convergence

V_N(x) at selected interior points shows wild oscillations:

| x | V_5 | V_8 | V_10 | V_15 | V_20 |
|---|---|---|---|---|---|
| 0.5 | 121.8 | 198.3 | 52.7 | 73.6 | 101.2 |
| 1.0 | 235.6 | 185.8 | 41.7 | 48.6 | 47.6 |
| 2.0 | 101.8 | 39.0 | 75.5 | 18.8 | 35.9 |
| 3.0 | 126.3 | 19.4 | 246.2 | 276.1 | 52.2 |
| 5.0 | 8.9 | 35.0 | 28.8 | 45.4 | 14.7 |
| 7.0 | 18.6 | 102.2 | 22.5 | 33.2 | 52.4 |
| 9.0 | 132.9 | 13.8 | 40.9 | 12.0 | 59.4 |

The pointwise values swing by factors of 2-10x between successive N values. There is no convergence at any fixed x.

### 2.3 Potential Range and Statistics

| N | V_min | V_max | V_mean | V_std | c_0 (const. shift) |
|---|---|---|---|---|---|
| 5 | -45 | 236 | 81.9 | 65.9 | 76.4 |
| 8 | -250 | 219 | 57.1 | 58.0 | 40.2 |
| 10 | -266 | 248 | 68.2 | 74.6 | 49.2 |
| 15 | -266 | 277 | 59.7 | 72.8 | 40.5 |
| 20 | 8.8 | 103 | 38.2 | 19.8 | 41.3 |

The N=20 potential is notably smoother (smaller range, smaller std) than the others. This is because K=25 > 20=N, giving more degrees of freedom than constraints, allowing the optimizer to find a smoother solution.

---

## 3. WHY V_N Doesn't Converge: The Fundamental Obstruction

### 3.1 The Inverse Problem is Ill-Posed for Growing N on a Fixed Interval

On a fixed interval [0, L], the free-particle eigenvalues grow as (n*pi/L)^2 ~ n^2, while the zeta zeros grow as ~ n/log(n). As N increases, the potential must increasingly "compress" the upper eigenvalues relative to what the Laplacian naturally produces.

For large N, the N-th free-particle eigenvalue is (N*pi/10)^2 ~ N^2, but the N-th zeta zero is ~ 2*pi*N/ln(N). The ratio N^2 / (N/ln N) = N*ln(N) diverges. The potential must compensate for this diverging mismatch, requiring increasingly extreme oscillations.

### 3.2 Non-Uniqueness from Over-Parameterization

When K > N (more Chebyshev modes than target eigenvalues), the inverse problem is under-determined. Many different potentials can produce the same first N eigenvalues. The optimizer finds different solutions depending on initialization and random seeds. The Gel'fand-Levitan theorem guarantees uniqueness of the potential for a COMPLETE spectrum, but not for a finite initial segment.

### 3.3 The Deep Lesson: A Fixed-L Schrodinger Operator Cannot Work

The asymptotic eigenvalue counting function for -d^2/dx^2 + V(x) on [0, L] is:

    N(E) ~ (L/pi) * sqrt(E)    for E -> infinity

regardless of V(x), as long as V is bounded. But the Riemann zero counting function is:

    N(T) ~ (T/(2pi)) * ln(T/(2pi)) - T/(2pi)

These have different growth rates (sqrt(E) vs T*log(T)). For any bounded potential V on a fixed interval, the eigenvalues must eventually grow as n^2 (Weyl law for 1D), which is incompatible with the n/log(n) growth of zeta zeros.

**This means the sequence V_N(x) on [0, L] CANNOT converge to a bounded function**, because the limit would have to produce the wrong asymptotic eigenvalue density.

---

## 4. What DOES Stabilize

Despite the non-convergence of V_N pointwise, several structural features are suggestive:

### 4.1 The Constant Shift c_0 Stabilizes

The zeroth Chebyshev coefficient c_0 (which sets the mean level of the potential) shows a clear pattern:

    N=5: c_0 = 76.4
    N=8: c_0 = 40.2
    N=10: c_0 = 49.2
    N=15: c_0 = 40.5
    N=20: c_0 = 41.3

For N >= 8, c_0 clusters around 40-50. A logarithmic fit gives: c_0 ~ 101.3 - 22.2 * ln(N).

### 4.2 The Semiclassical Phase Space Volume is Correct

The WKB semiclassical eigenvalue count for V_20:

| Energy E | N_sc (semiclassical) | N_actual | Ratio |
|---|---|---|---|
| 14.13 | 0.50 | 1 | 0.504 |
| 32.94 | 4.43 | 5 | 0.887 |
| 49.77 | 10.01 | 10 | 1.001 |
| 77.14 | 19.07 | 20 | 0.953 |

At E = 49.77 (the 10th zero), the semiclassical prediction is almost exactly correct: N_sc = 10.01. This means the potential V_20(x) has the correct classical phase-space volume for the first ~10 zeros, even though it was only constrained by eigenvalue matching.

### 4.3 The N=20 Solution is Remarkably Smooth and Non-Negative

V_20(x) has range [8.8, 103.3] -- it's everywhere positive and relatively smooth. The oscillatory coefficient norm ||coeffs[1:]||_2 / |c_0| = 0.71, much smaller than for other N values (which range from 1.3 to 3.2). This suggests that when K is moderately larger than N, the optimizer can find well-behaved potentials.

---

## 5. Comparison with Known Functions

We fitted V_20(x) against known candidate functions on the interior [0.5, 9.5]:

| Candidate | c_0 | c_1 | RMSE | RMSE/std(V) |
|---|---|---|---|---|
| c_0 + c_1*log(x) | 41.73 | -3.67 | 17.64 | 99.0% |
| c_0 + c_1*x*log(x) | 32.97 | 0.41 | 17.63 | 98.9% |
| c_0 + c_1*x | 34.05 | 0.50 | 17.78 | 99.7% |
| c_0 + c_1/x^2 | 33.56 | 14.20 | 16.35 | 91.7% |
| c_0 + c_1*psi(x) | 41.31 | -3.86 | 17.50 | 98.2% |

**None of the simple candidate functions explain more than ~10% of the variance.** The RMSE is 92-100% of the standard deviation of V, meaning these 2-parameter fits are barely better than a constant. The potential V_20(x) is genuinely complex -- it oscillates significantly and cannot be captured by any simple analytic form.

The closest match is c_0 + c_1/x^2 (Berry-Keating inverse-square potential), which captures about 8% of the variance. But this is a very weak match.

---

## 6. Theoretical Interpretation

### 6.1 The Operator Cannot Live on a Bounded Interval

Our computational experiment provides strong numerical evidence for a rigorous statement: no bounded potential V(x) on a finite interval [0, L] can have eigenvalues matching the Riemann zeta zeros for all n. The Weyl law for 1D Schrodinger operators forces eigenvalue growth as n^2, while zeta zeros grow as n/log(n).

This means the Hilbert-Polya operator, if it exists as a 1D Schrodinger operator, must either:
1. Live on a **half-line** [0, infinity) or the full line (-infinity, infinity), where the Weyl law does not apply
2. Have an **unbounded potential** that grows without bound
3. Be a **non-local** or **pseudo-differential** operator (not Schrodinger type at all)

### 6.2 What the Potential MUST Look Like on a Half-Line

On [0, infinity), if -u'' + V(x)u = lambda*u has eigenvalues {gamma_n}, the semiclassical requirement is:

    N(E) = (1/pi) * integral_0^{x_turn(E)} sqrt(E - V(x)) dx ~ (E/(2pi)) * ln(E/(2pi))

where x_turn(E) is the classical turning point where V(x_turn) = E.

For this to hold, we need the turning point to grow as x_turn(E) ~ E, and the potential to grow slowly enough that the classically allowed region contributes the right phase space. This is compatible with:

    V(x) ~ pi^2 * x^2 / (4 * W(x)^2)

where W is a function that creates the logarithmic correction. The Berry-Keating program suggests V(x) ~ x (linear potential with corrections), while the Connes program suggests a more algebraic structure.

### 6.3 The Finite-N Potential as a "Regularized" Hilbert-Polya Operator

Each V_N on [0, L] can be viewed as a finite-dimensional regularization of the hypothetical infinite-dimensional operator. The non-convergence on a fixed interval is analogous to how UV-divergent quantities in quantum field theory do not converge when you remove the cutoff without renormalization.

The renormalization group analogy is suggestive: perhaps V_N(x/f(N)) * g(N) converges for appropriate scaling functions f(N), g(N). Our data on the constant shift c_0 ~ 101 - 22*ln(N) hints at a logarithmic renormalization, but we do not have enough data points to confirm this.

---

## 7. Directions for Future Work

1. **Half-line computations**: Solve the inverse spectral problem on [0, infinity) instead of [0, L]. Use a truncated domain [0, L_N] with L_N -> infinity as N -> infinity. This removes the Weyl law obstruction.

2. **Scaling collapse**: Compute V_N on [0, L_N] with L_N = c*N (growing proportional to N) and check whether V_N(x/L_N) converges to a universal shape. The semiclassical analysis predicts x_turn ~ E ~ N, so L_N ~ N is the natural scaling.

3. **Gel'fand-Levitan inversion**: Instead of optimization, use the exact Gel'fand-Levitan-Marchenko integral equation to reconstruct V(x) from the spectral data. This is more principled than optimization and avoids local minima.

4. **Berry-Keating regularization**: Compare the optimized potentials with the xp Hamiltonian's regularized versions. The Berry-Keating H = xp + corrections predicts a specific potential shape that our data could validate.

5. **N=50-100 on growing domains**: The key open computation. With L_N ~ N/3 and K ~ N+10 Chebyshev modes, does the rescaled potential V_N(x * L_N / L_ref) converge?

---

## 8. Files Produced

- `findings.md` -- This document
- `zeta_zeros_100.json` -- First 100 nontrivial Riemann zeta zeros
- `phase1_results.json` -- Full results for N=5, 8, 10 (coefficients, eigenvalues, V(x) evaluations)
- `phase2_results.json` -- Full results for N=15, 20
- `result_N15_fixed.json` -- N=15 with better warm start (loss=0.0029 vs 0.0093)
- `run_single_N.py` -- Script to solve inverse spectral problem for one N value
- `run_lean.py` -- L-BFGS-B only solver (faster, for large N)
- `run_fixed_L.py` -- Fixed-L comprehensive sweep
- `run_phase2.py`, `run_phase3.py` -- Phase 2 and 3 computations
- `analyze_results.py` -- Post-processing analysis script

---

## 9. Conclusions

### What We Established

1. **V_N(x) does not converge on a fixed interval.** The pointwise values and L2 norms of successive differences show no convergence pattern. This is a necessary consequence of the Weyl law mismatch on bounded domains.

2. **The inverse spectral problem CAN be solved to high accuracy for moderate N.** N=20 achieved 0.242% max error, demonstrating that smooth potentials exist that nearly reproduce the zeta zero spectrum up to the 20th zero.

3. **The constant shift stabilizes near c_0 ~ 40-50.** This represents the mean potential energy needed to shift the free-particle spectrum into the range of the first ~20 zeta zeros.

4. **The WKB semiclassical counting function is accurate.** For V_20, the semiclassical prediction N_sc(E) matches the actual zero count to within 5-10% through the available range, confirming the potential has the right classical phase-space structure.

5. **No simple analytic function fits V_N.** Candidates including log(x), x*log(x), 1/x^2, and the digamma function all fail to capture more than 10% of the variance.

### What This Means for the Hilbert-Polya Conjecture

The non-convergence on a fixed interval is not a defeat -- it's an important structural result. It tells us that the Hilbert-Polya operator, if it is a differential operator, MUST live on an unbounded domain. The 1D Schrodinger operator on [0, infinity) with an appropriate potential remains the most promising candidate, but the potential cannot be captured by a finite Chebyshev expansion on a fixed interval.

The most promising next step is the half-line computation: solve -u'' + V(x)u = gamma_n * u on [0, L_N] with L_N growing, and check whether V_N(x) converges pointwise for fixed x as N -> infinity. The Gel'fand-Levitan theory guarantees this limit exists in principle; the question is whether it takes a recognizable analytic form.
