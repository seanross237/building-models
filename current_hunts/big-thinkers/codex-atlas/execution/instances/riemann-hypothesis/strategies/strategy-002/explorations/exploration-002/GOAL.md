# Exploration 002 — Tournament Entry B: Optimization-Based Operator Construction

## Mission Context

We are investigating the Riemann Hypothesis through the lens of random matrix theory. Previous work (strategy-001) established a 10-point constraint catalog for the hypothetical Riemann operator:

**Zeta zeros match GUE statistics:**
- β = 2.0 (GUE symmetry class, no time-reversal symmetry)
- Pair correlation matches Montgomery: R₂(r) = 1 - (sin(πr)/(πr))², 9% mean relative deviation
- Nearest-neighbor spacing matches Wigner surmise, 4% mean absolute deviation
- Number variance Σ²(L) saturates at 0.3-0.5 for L > 2 (more rigid than GUE)
- Spectral rigidity Δ₃ = 0.156 for L > 15

**All arithmetic matrix candidates fail:** simple encoding of primes into matrices produces Poisson or partial GOE statistics, never GUE. The key lesson: **matrix structure determines universality class as much as arithmetic content**.

## Your Task

**Reverse-engineer the operator from its spectral statistics.** This is the novel approach: instead of guessing operator form and testing it, optimize a parameterized family of Hermitian matrices to produce GUE-like eigenvalue statistics. Then examine what the optimal matrix looks like.

This is genuinely novel — there is no published work on "what matrix structure produces GUE statistics?" as an optimization problem.

## Setup

### Parameterized Matrix Family

Start with a Hermitian matrix of size N=200 (small enough for fast optimization):

```python
# N×N complex Hermitian matrix parameterized by:
# - Real diagonal entries d_i (i=1,...,N)  [N parameters]
# - Complex upper-triangle entries: a_{ij} + i*b_{ij} (i<j)  [N(N-1) parameters]
# Total: N² parameters for full parameterization

# But that's too many. Use structured parameterization:
# Option A: Circulant structure — parameterized by N complex Fourier modes
# Option B: Low-rank perturbation of GUE — H = H_GUE + V where V has structure
# Option C: Hankel-like with complex entries — H_{ij} = f(i+j) for some complex function f
```

**Recommended approach — start simple:**

**Stage 1:** Parameterize a circulant Hermitian matrix: H_{jk} = c_{(j-k) mod N} where c_{-m} = c_m* ensures Hermiticity. This has N/2 complex parameters = N real parameters. Circulant matrices are diagonalized by DFT — their eigenvalues are the DFT of the first row. Start here.

**Stage 2:** If circulant fails, try a Hankel-like structure with complex entries: H_{jk} = f(|j-k|) where f is a complex-valued function of the "distance" |j-k|. Parameters: N complex values f(0), f(1), ..., f(N-1).

**Stage 3:** If both structured approaches fail, try full Hermitian parameterization for N=50 (manageable: 50² = 2500 parameters).

### Loss Function

The optimization objective measures how closely the eigenvalue statistics of H match GUE targets:

```python
def loss(params):
    # Construct H from params
    H = construct_matrix(params)
    # Compute eigenvalues
    eigenvalues = np.linalg.eigvalsh(H)
    # Unfold eigenvalues
    unfolded = unfold_eigenvalues(eigenvalues)
    # Compute spacing distribution
    spacings = np.diff(unfolded)
    spacings = spacings / np.mean(spacings)

    # Loss term 1: spacing distribution vs GUE Wigner surmise
    # P_GUE(s) = (32/π²) s² exp(-4s²/π)
    bins = np.linspace(0, 4, 20)
    hist, _ = np.histogram(spacings, bins=bins, density=True)
    s_centers = (bins[:-1] + bins[1:]) / 2
    P_GUE = (32/np.pi**2) * s_centers**2 * np.exp(-4*s_centers**2/np.pi)
    loss_spacing = np.mean((hist - P_GUE)**2)

    # Loss term 2: level repulsion β — want β near 2
    # Fit P(s) ~ s^β for small s, penalize |β - 2|
    small_s_mask = spacings < 0.5
    if small_s_mask.sum() > 10:
        beta = fit_level_repulsion(spacings[small_s_mask])
        loss_beta = (beta - 2.0)**2
    else:
        loss_beta = 10.0  # penalize no small spacings

    # Combine
    return loss_spacing + 0.5 * loss_beta
```

**Use scipy.optimize.minimize with method='BFGS'** (gradient-based, fast for smooth loss).

## Stages of Analysis

### Stage 1: Circulant Matrix Optimization (N=200)

1. Initialize: random complex circulant (from GUE-like Fourier components)
2. Optimize to match GUE spacing distribution
3. Report: final β achieved, chi²_GUE, chi²_GOE, number of iterations, convergence quality
4. If β > 1.5: extract the optimal circulant parameters. Do they look like an arithmetic function? Is there a pattern?

### Stage 2: Structure Analysis of Optimal Matrix

If Stage 1 produces β > 1.0, examine the structure of the optimal matrix:

1. **Fourier structure**: Plot |c_k| vs k (the magnitude of circulant parameters). Does it decay like Λ(k)/k^α for some α? Like a power law? Exponentially?

2. **Eigenvector structure**: Are eigenvectors localized or extended? Compute inverse participation ratio (IPR): IPR = Σ|ψ_i|⁴ / (Σ|ψ_i|²)². IPR=1/N means fully extended (like GUE), IPR→1 means localized.

3. **Phase structure**: Plot the phase arg(c_k) vs k. Is it random? Periodic? Does it look like values of a Dirichlet character?

4. **Arithmetic content**: Is Λ(k) (von Mangoldt function) present in the magnitude of c_k? Compute Pearson correlation between |c_k| and Λ(k) for k=1,...,N.

### Stage 3: Constrained Optimization (if Stage 1 works)

If circulant optimization finds β > 1.5, try a **constrained version**:
- Fix the magnitude |c_k| = Λ(k) / k (von Mangoldt amplitudes)
- Only optimize the phases arg(c_k)
- Does this constrained version also achieve high β?

This tests whether the arithmetic content (von Mangoldt) is compatible with GUE statistics IF the right phases are chosen.

### Stage 4: Full Hermitian Optimization (N=50)

If circulant (N=200) doesn't work, try N=50 with full parameterization:
- 50² = 2500 real parameters
- Use L-BFGS-B (handles more parameters than BFGS)
- Same loss function but smaller N

## Key Questions to Answer

1. **Can optimization find a matrix with β > 1.5?** If yes, the construction approach works in principle.

2. **What does the optimal matrix look like?** Does it have interpretable arithmetic structure? Is the structure Toeplitz-like, Hankel-like, or something else?

3. **If von Mangoldt amplitudes are fixed, can right phases give GUE?** This is the key question: is the arithmetic content compatible with GUE if we only tune the phases?

4. **What is the full 10-constraint score** of the best construction?

5. **What does the structure tell us about the "true" Riemann operator?** Even if this is a toy model, the structure of an operator optimized to produce GUE might resemble the Riemann operator.

## Implementation Notes

- N=200 circulant: eigenvalue computation is O(N log N) via FFT — very fast
- scipy.optimize.minimize with BFGS typically converges in 100-1000 iterations for this type of problem
- Monitor convergence: print loss every 100 iterations
- Save the optimal parameters to `code/optimal_params.npy` for later analysis
- **Write to REPORT.md after each stage** — don't wait for all stages to complete

## Computation Platform

Python with numpy, scipy, mpmath. All installed.

## Success Criteria

**Primary success:** Find a matrix family where optimization achieves β > 1.5 AND the structure reveals interpretable arithmetic patterns.
**Secondary success:** Achieve β > 1.0 (any progress toward GUE, even without interpretable structure).
**Interesting failure:** Optimization converges but to β ≤ 0.5 — this tells us that the loss function landscape has no good GUE basin in the searched family.

## Exploration Directory

Your exploration directory is:
`/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/riemann-hypothesis/strategies/strategy-002/explorations/exploration-002/`

Write all scripts to `code/` subdirectory. Write REPORT.md incrementally as you complete each stage. Write REPORT-SUMMARY.md **last** — this signals you are finished.
