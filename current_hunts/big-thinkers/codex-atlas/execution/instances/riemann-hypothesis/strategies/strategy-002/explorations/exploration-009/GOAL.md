# Exploration 009 — Flat-Amplitude Δ₃ Spectral Rigidity Test

## Mission Context

You are a Math Explorer in the Atlas research system. This is Exploration 009 for the Riemann Hypothesis operator construction mission (Strategy 002). Your job is to run a single clean computation to resolve whether C1's anomalous intermediate spectral rigidity is caused by Von Mangoldt arithmetic or is generic to any GUE-class matrix.

**This is a COMPUTATION task.** Write Python/numpy code, run it, record exact numbers.

---

## Background: What Needs Resolving

Strategy 002 established that C1 (Von Mangoldt Hankel amplitudes + random complex phases) achieves GUE universality class (β≈1.18-1.67 depending on measurement, KS_GUE PASS). However, its spectral rigidity Δ₃_sat = 0.285 is intermediate — between:
- **GUE theory (infinite N):** Δ₃_sat ≈ 0.565
- **GUE finite-size N=500 simulation:** Δ₃_sat ≈ 0.250 (KNOWN from prior exploration)
- **C1 actual:** Δ₃_sat = 0.285
- **Riemann zeta zeros:** Δ₃_sat ≈ 0.155

Note: C1's value (0.285) is close to the GUE finite-size value (0.250). The "anomalous" claim may be wrong — C1's Δ₃ might simply be generic GUE-class behavior at N=500.

**The adversarial review (E007) established** that Von Mangoldt amplitude is NOT needed for pair correlation (flat-amplitude gives MRD=6.8% < C1's 7.9%). The remaining question: does removing Von Mangoldt amplitude change Δ₃?

**The C1 construction:** H_{jk} = Λ(|j-k|+1) × exp(2πi φ_{jk}), where φ_{jk} are i.i.d. Uniform[0,2π] and Λ(n) is the Von Mangoldt function.

**The flat-amplitude construction:** H_{jk} = exp(2πi φ_{jk}) (same random phases, amplitude = 1, no arithmetic weights). To make it Hermitian: H_{jk} = exp(2πi φ_{jk}) for j<k, H_{kj} = exp(-2πi φ_{jk}), H_{jj} = 0.

---

## Your Task

### Computation: Compare Δ₃_sat for four ensembles at N=500

Run 5 realizations of each and average:

1. **H_flat**: Flat amplitude + random phases (amplitude=1)
   - H_{jk} = exp(2πi φ_{jk}) for j<k, H_{kj} = conj, H_{jj}=0
   - φ_{jk} ~ Uniform[0, 2π]

2. **C1**: Von Mangoldt Hankel + random phases
   - H_{jk} = Λ(|j-k|+1) × exp(2πi φ_{jk}) for j<k, H_{kj} = conj, H_{jj}=0
   - Λ(n): Von Mangoldt function = log(p) if n=p^k for prime p, 0 otherwise

3. **GUE_control**: Standard GUE sample
   - H = (A + A†)/√(2N) where A_{jk} = (x+iy)/√2, x,y ~ N(0,1)

4. **H_diagonal_flat**: Flat amplitude but diagonal amplitude only (Toeplitz-like, as control)
   - H_{jk} = exp(2πi φ_{jk}) for |j-k|==1 only (nearest neighbor), rest 0

### The Δ₃ Formula (EXACT — use this, not any other version)

```python
def compute_delta3(eigenvalues, L_max=50, n_windows=200):
    """
    Dyson-Mehta Δ₃ statistic.
    eigenvalues: sorted, unfolded eigenvalues
    Returns: array of (L_values, delta3_values)
    """
    N = len(eigenvalues)
    L_values = np.linspace(1, L_max, 50)
    delta3 = np.zeros(len(L_values))

    for i, L in enumerate(L_values):
        residuals = []
        # Slide window over unfolded spectrum
        for start_idx in range(0, N - int(L*2), max(1, int(N/n_windows))):
            x0 = eigenvalues[start_idx]
            x1 = x0 + L
            # Find eigenvalues in window
            mask = (eigenvalues >= x0) & (eigenvalues <= x1)
            n_in = np.sum(mask)
            if n_in < 3:
                continue
            # Build staircase N(x) at eigenvalue positions
            eigs_in = eigenvalues[mask]
            n_vals = np.arange(1, n_in+1, dtype=float)
            t_vals = eigs_in - x0
            # Least-squares fit: minimize (1/L) integral [N(t) - A*t - B]^2 dt
            # Discretize: use trapezoidal integration over staircase
            # Analytical formula: minimize sum_i (n_i - A*t_i - B)^2
            # (This is standard linear regression)
            T = t_vals  # shape (n_in,)
            A_mat = np.column_stack([T, np.ones(n_in)])
            coeffs, _, _, _ = np.linalg.lstsq(A_mat, n_vals, rcond=None)
            A_fit, B_fit = coeffs
            residuals.append(np.mean((n_vals - A_fit*T - B_fit)**2) / L)

        delta3[i] = np.mean(residuals) if residuals else np.nan

    return L_values, delta3

def unfold_spectrum(eigenvalues, poly_degree=7):
    """
    Unfold eigenvalues using polynomial fit to cumulative density.
    """
    N = len(eigenvalues)
    eigs_sorted = np.sort(eigenvalues)
    cumulative = np.arange(1, N+1, dtype=float)
    # Fit polynomial to cumulative count vs eigenvalue
    coeffs = np.polyfit(eigs_sorted, cumulative, poly_degree)
    unfolded = np.polyval(coeffs, eigs_sorted)
    return unfolded
```

**Saturation:** Average Δ₃ values for L ∈ [25, 50] to get Δ₃_sat. This is the saturated value.

**Sanity check:** GUE control should give Δ₃_sat ≈ 0.20-0.30 at N=500. If < 0.1 or > 0.6, the formula has a bug.

### Brody β Fitting (for completeness — uses only numpy)

```python
def brody_fit(spacings, n_grid=50):
    """Manual Brody fit without scipy."""
    # Normalize spacings
    s = np.array(spacings)
    s = s / np.mean(s)  # normalize to <s>=1

    best_beta = 0.0
    best_loss = np.inf

    for beta in np.linspace(0.0, 2.5, n_grid):
        # Brody distribution: p(s) = (1+beta)*b*s^beta*exp(-b*s^(beta+1))
        # where b = [Gamma((beta+2)/(beta+1))]^(beta+1)
        from math import gamma
        b = (gamma((beta+2)/(beta+1)))**(beta+1)

        # Bin spacings
        bins = np.linspace(0, 4, 30)
        hist, edges = np.histogram(s, bins=bins, density=True)
        centers = (edges[:-1] + edges[1:]) / 2

        # Predicted Brody density at bin centers
        pred = (1+beta) * b * centers**beta * np.exp(-b * centers**(beta+1))

        loss = np.sum((hist - pred)**2)
        if loss < best_loss:
            best_loss = loss
            best_beta = beta

    return best_beta
```

**NOTE: scipy.optimize is NOT available in this environment** (numpy.Inf was removed in NumPy 1.25+). Do NOT import scipy.optimize. The manual Brody grid search above works.

### Von Mangoldt Function

```python
def von_mangoldt(n, max_prime=None):
    """Λ(n) = log(p) if n = p^k for prime p, else 0."""
    if n <= 1:
        return 0.0
    for p in range(2, int(n**0.5) + 1):
        if n % p == 0:
            while n % p == 0:
                n //= p
            if n == 1:
                return np.log(p)
            else:
                return 0.0
    return np.log(n)  # n is prime

def build_c1_matrix(N, rng):
    """C1: Von Mangoldt Hankel + random complex phases."""
    amplitudes = np.array([von_mangoldt(k) for k in range(1, 2*N+1)])
    H = np.zeros((N, N), dtype=complex)
    for j in range(N):
        for k in range(j+1, N):
            phase = 2 * np.pi * rng.uniform()
            amp = amplitudes[abs(j-k) + 1]
            H[j, k] = amp * np.exp(1j * phase)
            H[k, j] = np.conj(H[j, k])
    return H

def build_flat_matrix(N, rng):
    """H_flat: flat amplitude + random complex phases."""
    H = np.zeros((N, N), dtype=complex)
    for j in range(N):
        for k in range(j+1, N):
            phase = 2 * np.pi * rng.uniform()
            H[j, k] = np.exp(1j * phase)
            H[k, j] = np.conj(H[j, k])
    return H
```

**Performance note:** For N=500, the double-loop matrix construction takes ~2 seconds per matrix. 5 realizations × 4 ensembles = 20 matrices = ~40 seconds. The Δ₃ scan takes ~30-60 seconds per realization. Total: expect 5-10 minutes.

---

## Interpreter Decision Logic

After computing Δ₃_sat for each ensemble, report:

| Ensemble | Δ₃_sat (mean ± std) | Interpretation |
|---|---|---|
| H_flat | ? | Generic GUE-class reference |
| C1 | ? | Should reproduce ≈0.285 from E005 |
| GUE_control | ? | Should be ≈0.20-0.30 at N=500 |
| H_diagonal_flat | ? | Comparison for sparsity effects |
| Riemann zeta zeros | 0.155 (known) | Target |

**Key decision:**
- If H_flat Δ₃_sat ≈ C1 Δ₃_sat: Von Mangoldt arithmetic amplitude DOES NOT cause the intermediate rigidity. C1's Δ₃ is generic GUE-class behavior. → "Anomalous intermediate rigidity" claim is NOT novel.
- If H_flat Δ₃_sat >> C1 Δ₃_sat (e.g., H_flat ≈ 0.5, C1 ≈ 0.285): Von Mangoldt structure IS causing anomalous rigidity. → Claim strengthened.

---

## Output Requirements

1. Create `code/delta3_test.py` with complete runnable code
2. Save results to `code/results.npz` containing: `delta3_flat`, `delta3_c1`, `delta3_gue`, `delta3_diag_flat`, `L_values` (one per realization)
3. Write findings to REPORT.md

**WRITE RESULTS INCREMENTALLY:**
- After computing H_flat results, write the H_flat section to REPORT.md and write `[SECTION COMPLETE: H_flat]` before moving to C1
- After computing C1 results, write the C1 section and write `[SECTION COMPLETE: C1]` before moving to GUE
- After computing GUE control, write that section and `[SECTION COMPLETE: GUE]`
- Write the comparison table + interpretation ONLY after all sections have `[SECTION COMPLETE]` markers

**DO NOT buffer results for a final write. Write each section immediately after computing it.**

## Success Criteria

**SUCCESS:** You compute Δ₃_sat for H_flat and C1 (minimum), determine whether they differ, and report a clear verdict on whether Von Mangoldt structure explains C1's intermediate rigidity.

**FAILURE:** You cannot run the computation (environment issue). In this case: write exactly what failed and what would need to be fixed.

Write REPORT-SUMMARY.md last — it signals completion.
