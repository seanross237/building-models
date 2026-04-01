# Exploration 002 — Optimization-Based Operator Construction

## Goal

Reverse-engineer a Riemann-like operator from its spectral statistics by optimizing parameterized Hermitian matrix families to match GUE eigenvalue statistics (β=2 level repulsion, Wigner-Dyson spacing distribution). Then analyze the structure of the optimal matrix for arithmetic patterns.

## Plan

1. **Stage 1**: Circulant matrix optimization (N=200) — fast O(N log N) eigenvalue computation
2. **Stage 2**: GUE projection, full Hermitian N=30, von Mangoldt constrained optimization
3. **Stage 3**: Structure analysis of best-found matrix
4. **Stage 4**: 10-constraint score for best construction

---

## Stage 1: Circulant Matrix Optimization

**Code**: `code/stage1_circulant_optimization.py`

A circulant Hermitian matrix of size N=200 is parameterized by N real Fourier coefficients (with Hermitian symmetry c[N-k] = c[k]*). Eigenvalues = DFT(first row) → computed in O(N log N).

**Initial loss function**: Histogram-based MSE between empirical spacing distribution and GUE Wigner surmise P_GUE(s) = (32/π²)s²exp(-4s²/π), plus penalty 0.5*(β-2)².

**CRITICAL FAILURE**: The histogram-based loss function is non-differentiable (piecewise constant), causing L-BFGS-B to declare convergence immediately (iters=0) on most trials. The gradient computed by finite differences is numerically zero.

### Experiment A: Unconstrained Circulant (N=200)
- 3 trials, L-BFGS-B, max 3000 iterations
- Result: β ∈ [0.0, 0.24], all best-match = Poisson
- Two trials converged immediately (iters=0)
- Trial 3: slowly moved from β=0.09 to β=0.24 (15000+ function evaluations, no convergence)

### Experiment B: Von Mangoldt Amplitudes, Optimize Phases
- Fix |c_k| = Λ(k)/(k+1)^α, optimize phases arg(c_k)
- Tested α ∈ {0.5, 1.0, 1.5}, 3 trials each
- Result: β ∈ [0.0, 0.23], all best-match = Poisson
- Most trials converged immediately (iters=0)
- The von Mangoldt amplitudes have only 60/200 nonzero entries (sparse)

### Experiment C: Direct Eigenvalue Optimization (upper bound)
- Directly optimize N=200 real eigenvalues for GUE spacing statistics
- Result: β=0.00, converged immediately (gradient=0)
- Even this trivially-solvable case fails with histogram loss!

**Stage 1 Conclusion** [COMPUTED]: The histogram-based loss function is fundamentally broken for gradient-based optimization. The loss landscape is flat at most points (piecewise constant loss). Even with 15,000 function evaluations, the best β achieved is only 0.24. A completely different approach is needed.

**Insight**: The problem is not just the optimizer — it's that histogram-based statistics of sorted eigenvalues are not differentiable with respect to matrix parameters. Need either gradient-free optimization or a smooth loss function.

---

## Stage 2: Improved Approaches

**Code**: `code/stage2_gue_projection_and_full_hermitian.py`

Four approaches with smooth loss functions (KDE-based) and gradient-free optimization:

**Approach A**: GUE projection onto circulant subspace
**Approach B**: Full Hermitian N=30, Nelder-Mead with KDE loss
**Approach C**: Von Mangoldt phases, Nelder-Mead with KDE loss
**Approach D**: Reference GUE statistics (N=500 ground truth)

**Smooth loss function**: KDE-based L2 distance between empirical spacing density and GUE Wigner surmise, plus level repulsion penalty (fraction of spacings < 0.3).

*Results being computed...*

---

## Stage 3: Structure Analysis

*(To be filled after best matrix found)*

---

## Stage 4: 10-Constraint Score

*(To be filled after structure analysis)*

---

## Summary of Findings

*(To be filled last)*
